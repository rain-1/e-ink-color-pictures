"""Shared drawing kit for 2026-10-03.

Draw at 2x on a PIL canvas; tones are Bayer screens between two palette inks, laid
down in aligned 2x2 blocks so they survive the box-downsample exactly. save() snaps
to the six inks, so render with --dither none.
"""
import os
import numpy as np
from PIL import Image, ImageDraw

W, H, S = 400, 600, 2
K, Wh, R, Y, B, G = (0, 0, 0), (255, 255, 255), (224, 27, 36), (245, 212, 0), (18, 61, 176), (30, 155, 60)
INKS = np.array([K, Wh, R, Y, B, G], np.float32)

_b = np.array([[0, 32, 8, 40, 2, 34, 10, 42], [48, 16, 56, 24, 50, 18, 58, 26],
               [12, 44, 4, 36, 14, 46, 6, 38], [60, 28, 52, 20, 62, 30, 54, 22],
               [3, 35, 11, 43, 1, 33, 9, 41], [51, 19, 59, 27, 49, 17, 57, 25],
               [15, 47, 7, 39, 13, 45, 5, 37], [63, 31, 55, 23, 61, 29, 53, 21]]) / 64 + 1 / 128
BAYER = np.tile(_b, (H // 8 + 1, W // 8 + 1))[:H, :W]


def up(a):
    """1x array -> 2x (block repeat)."""
    return np.repeat(np.repeat(a, S, 0), S, 1)


def mix(c1, c2, t):
    """Screen between ink c1 (t=0) and c2 (t=1). t scalar or HxW field at 1x. Returns 2x RGB array."""
    t = np.broadcast_to(np.asarray(t, np.float32), (H, W))
    m = (t > BAYER)[..., None]
    a = np.where(m, np.array(c2, np.uint8), np.array(c1, np.uint8)).astype(np.uint8)
    return up(a)


def ramp(stops, t):
    """Multi-ink screen: stops = [c0, c1, c2...], t in 0..1 field at 1x. 2x RGB array."""
    t = np.clip(np.asarray(t, np.float32), 0, 1) * (len(stops) - 1)
    i = np.minimum(t.astype(int), len(stops) - 2)
    f = t - i
    lo = np.array(stops, np.uint8)[i]
    hi = np.array(stops, np.uint8)[i + 1]
    m = (f > BAYER)[..., None]
    return up(np.where(m, hi, lo).astype(np.uint8))


class Canvas:
    def __init__(self, bg=Wh):
        self.im = Image.new("RGB", (W * S, H * S), bg)
        self.d = ImageDraw.Draw(self.im)

    # all coordinates in 1x units; scaled here
    def _p(self, pts):
        return [(x * S, y * S) for x, y in pts]

    def poly(self, pts, fill=None, outline=None, width=1):
        self.d.polygon(self._p(pts), fill=fill if isinstance(fill, tuple) else None,
                       outline=outline, width=int(width * S))
        if fill is not None and not isinstance(fill, tuple):
            self.paste(fill, lambda d: d.polygon(self._p(pts), fill=255))

    def rect(self, x0, y0, x1, y1, fill=None, outline=None, width=1):
        self.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], fill, outline, width)

    def ellipse(self, cx, cy, rx, ry, fill=None, outline=None, width=1):
        box = [(cx - rx) * S, (cy - ry) * S, (cx + rx) * S, (cy + ry) * S]
        if fill is not None and not isinstance(fill, tuple):
            self.paste(fill, lambda d: d.ellipse(box, fill=255))
            fill = None
        self.d.ellipse(box, fill=fill, outline=outline, width=int(width * S))

    def line(self, pts, fill=K, width=1):
        self.d.line(self._p(pts), fill=fill, width=max(1, int(round(width * S))), joint="curve")

    def paste(self, arr, drawfn):
        """Paste a 2x RGB array through a mask drawn by drawfn(ImageDraw)."""
        mask = Image.new("L", self.im.size, 0)
        drawfn(ImageDraw.Draw(mask))
        src = arr if isinstance(arr, Image.Image) else Image.fromarray(arr)
        self.im.paste(src, (0, 0), mask)

    def paste_mask(self, arr, mask1x):
        """Paste a 2x array where a 1x boolean mask is true."""
        mask = Image.fromarray((up(mask1x.astype(np.uint8)) * 255).astype(np.uint8))
        if isinstance(arr, tuple):
            self.im.paste(arr, (0, 0, *self.im.size), mask)
            return
        self.im.paste(Image.fromarray(arr), (0, 0), mask)

    def text(self, xy, s, fill=K, size=12, font=None, anchor="la"):
        from PIL import ImageFont
        f = ImageFont.truetype(font or FONT, int(size * S))
        self.d.text((xy[0] * S, xy[1] * S), s, fill=fill, font=f, anchor=anchor)

    def save(self, path=None):
        # snap each 2x pixel to an ink, then take the majority of each 2x2 block;
        # ties go to the darker ink so one-subpixel-wide lines survive.
        a = np.asarray(self.im, np.float32).reshape(-1, 3)
        idx = ((INKS[None] - a[:, None]) ** 2).sum(-1).argmin(1).reshape(H, S, W, S)
        prio = np.array([5, 0, 4, 1, 3, 2], np.float32) * 0.1  # K R B G Y W
        cnt = np.stack([(idx == i).sum((1, 3)) + prio[i] for i in range(6)], -1)
        out = Image.fromarray(INKS[cnt.argmax(-1)].astype(np.uint8))
        out.save(path or os.environ.get("OUT_RAW", "out.png"))
        return out


def _font():
    import glob
    for pat in ["/usr/share/fonts/**/DejaVuSans-Bold.ttf", "/usr/share/fonts/**/*Bold*.ttf",
                "/usr/share/fonts/**/*.ttf"]:
        g = glob.glob(pat, recursive=True)
        if g:
            return g[0]
    return None


FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
