"""Shared drawing helpers for 2026-10-12. Draw in 400x600 units on a 2x canvas;
finish() mode-downsamples 2x2 blocks so the output stays on-palette and crisp."""
import os, math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont

S = 2
W, H = 400, 600
K = (0, 0, 0); Wt = (255, 255, 255); R = (0xE0, 0x1B, 0x24)
Y = (0xF5, 0xD4, 0x00); B = (0x12, 0x3D, 0xB0); G = (0x1E, 0x9B, 0x3C)
PAL = [K, Wt, R, Y, B, G]

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SERIF_BI = "/usr/share/fonts/truetype/liberation/LiberationSerif-BoldItalic.ttf"


class Canvas:
    def __init__(self, bg=Wt):
        self.im = Image.new("RGB", (W * S, H * S), bg)
        self.d = ImageDraw.Draw(self.im)

    def _p(self, pts):
        return [(x * S, y * S) for x, y in pts]

    def poly(self, pts, fill=None, outline=None, width=1):
        pts = self._p(pts)
        if fill is not None:
            self.d.polygon(pts, fill=fill)
        if outline is not None:
            self.d.line(pts + [pts[0]], fill=outline, width=max(1, round(width * S)), joint="curve")

    def line(self, pts, fill=K, width=1):
        self.d.line(self._p(pts), fill=fill, width=max(1, round(width * S)), joint="curve")

    def rect(self, x0, y0, x1, y1, fill=None, outline=None, width=1):
        self.d.rectangle([x0 * S, y0 * S, x1 * S, y1 * S], fill=fill, outline=outline,
                         width=max(1, round(width * S)) if outline else 0)

    def ellipse(self, cx, cy, rx, ry, fill=None, outline=None, width=1):
        self.d.ellipse([(cx - rx) * S, (cy - ry) * S, (cx + rx) * S, (cy + ry) * S],
                       fill=fill, outline=outline, width=max(1, round(width * S)) if outline else 0)

    def circle(self, cx, cy, r, **kw):
        self.ellipse(cx, cy, r, r, **kw)

    def arc(self, cx, cy, rx, ry, a0, a1, fill=K, width=1):
        self.d.arc([(cx - rx) * S, (cy - ry) * S, (cx + rx) * S, (cy + ry) * S], a0, a1,
                   fill=fill, width=max(1, round(width * S)))

    def text(self, xy, s, size, fill=K, font=SERIF, anchor="la", spacing=0):
        f = ImageFont.truetype(font, round(size * S))
        if spacing:
            x, y = xy
            total = sum(f.getlength(c) for c in s) / S + spacing * (len(s) - 1)
            if anchor[0] == "m":
                x -= total / 2
            for c in s:
                self.d.text((x * S, y * S), c, font=f, fill=fill, anchor="l" + anchor[1])
                x += f.getlength(c) / S + spacing
        else:
            self.d.text((xy[0] * S, xy[1] * S), s, font=f, fill=fill, anchor=anchor)

    def mask_fill(self, mask, colour):
        """mask: bool array at canvas resolution."""
        a = np.asarray(self.im).copy()
        a[mask] = colour
        self.im = Image.fromarray(a)
        self.d = ImageDraw.Draw(self.im)

    def arr(self):
        return np.asarray(self.im)


def snap(a):
    pal = np.array(PAL, dtype=np.int32)
    flat = a.reshape(-1, 3).astype(np.int32)
    idx = ((flat[:, None, :] - pal[None]) ** 2).sum(-1).argmin(1)
    return idx.reshape(a.shape[:2])


def finish(c: Canvas):
    idx = snap(np.asarray(c.im))
    h, w = idx.shape
    blk = idx.reshape(h // S, S, w // S, S).transpose(0, 2, 1, 3).reshape(h // S, w // S, S * S)
    counts = np.stack([(blk == k).sum(-1) for k in range(6)], -1)
    # tie-break toward the darker/inkier colour so thin lines survive
    pri = np.array([0.6, 0.0, 0.5, 0.1, 0.5, 0.5])
    out = np.array(PAL, dtype=np.uint8)[(counts + pri).argmax(-1)]
    Image.fromarray(out).save(os.environ.get("OUT_RAW", "out.png"))


def bayer(n=8):
    m = np.array([[0]])
    while m.shape[0] < n:
        m = np.block([[4 * m, 4 * m + 2], [4 * m + 3, 4 * m + 1]])
    return (m + 0.5) / m.size


def screen(tone, h, w, n=8):
    """tone 0..1 array (h,w) -> bool 'ink' where tone > threshold."""
    b = bayer(n)
    t = np.tile(b, (h // n + 1, w // n + 1))[:h, :w]
    return tone > t
