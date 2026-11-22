"""Shared drawing kit for 2026-11-22. Work in 400x600 'panel units', drawn at 3x,
then reduced by majority vote per 3x3 block so every output pixel is a pure palette
colour (no antialias fringes -> render with --dither none)."""
import os, math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont

S = 3
W, H = 400, 600
K = (0, 0, 0); WH = (255, 255, 255); R = (0xE0, 0x1B, 0x24)
Y = (0xF5, 0xD4, 0x00); B = (0x12, 0x3D, 0xB0); G = (0x1E, 0x9B, 0x3C)
PAL = np.array([K, WH, R, Y, B, G], dtype=np.int32)
FONTS = {
    "serif": "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "sans": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "ital": "/usr/share/fonts/truetype/freefont/FreeSerifBoldItalic.ttf",
}


class D:
    def __init__(self, bg):
        self.im = Image.new("RGB", (W * S, H * S), bg)
        self.d = ImageDraw.Draw(self.im)

    def _p(self, pts):
        return [(x * S, y * S) for x, y in pts]

    def poly(self, pts, fill=None, outline=None, w=1):
        if fill is not None:
            self.d.polygon(self._p(pts), fill=fill)
        if outline is not None:
            self.line(list(pts) + [pts[0]], outline, w)

    def line(self, pts, fill, w=1):
        self.d.line(self._p(pts), fill=fill, width=max(1, round(w * S)), joint="curve")

    def rect(self, x0, y0, x1, y1, fill=None, outline=None, w=1):
        self.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], fill, outline, w)

    def ell(self, cx, cy, rx, ry=None, fill=None, outline=None, w=1):
        ry = rx if ry is None else ry
        box = [(cx - rx) * S, (cy - ry) * S, (cx + rx) * S, (cy + ry) * S]
        self.d.ellipse(box, fill=fill, outline=outline, width=max(1, round(w * S)) if outline else 0)

    def arc(self, cx, cy, rx, ry, a0, a1, fill, w=1):
        box = [(cx - rx) * S, (cy - ry) * S, (cx + rx) * S, (cy + ry) * S]
        self.d.arc(box, a0, a1, fill=fill, width=max(1, round(w * S)))

    def pie(self, cx, cy, rx, ry, a0, a1, fill):
        box = [(cx - rx) * S, (cy - ry) * S, (cx + rx) * S, (cy + ry) * S]
        self.d.pieslice(box, a0, a1, fill=fill)

    def text(self, x, y, s, fill, size=12, font="serif", anchor="mm", spacing=0):
        f = ImageFont.truetype(FONTS[font], round(size * S))
        if spacing:
            tw = sum(f.getlength(c) for c in s) + spacing * S * (len(s) - 1)
            cx = x * S - tw / 2
            for c in s:
                self.d.text((cx, y * S), c, fill=fill, font=f, anchor="lm")
                cx += f.getlength(c) + spacing * S
        else:
            self.d.text((x * S, y * S), s, fill=fill, font=f, anchor=anchor)

    def save(self):
        a = np.asarray(self.im).astype(np.int32)
        idx = ((a[:, :, None, :] - PAL[None, None]) ** 2).sum(-1).argmin(-1)
        blk = idx.reshape(H, S, W, S).transpose(0, 2, 1, 3).reshape(H, W, S * S)
        cnt = np.stack([(blk == c).sum(-1) for c in range(6)], -1)
        out = PAL[cnt.argmax(-1)].astype(np.uint8)
        Image.fromarray(out, "RGB").save(os.environ.get("OUT_RAW", "out.png"))


def bez(p0, p1, p2, n=24):
    """quadratic bezier as a point list"""
    return [((1 - t) ** 2 * p0[0] + 2 * t * (1 - t) * p1[0] + t * t * p2[0],
             (1 - t) ** 2 * p0[1] + 2 * t * (1 - t) * p1[1] + t * t * p2[1])
            for t in (i / n for i in range(n + 1))]


def gull(d, x, y, s, col, w=1.0):
    d.line(bez((x - s, y + s * 0.15), (x - s * 0.5, y - s * 0.6), (x, y), 8), col, w)
    d.line(bez((x, y), (x + s * 0.5, y - s * 0.6), (x + s, y + s * 0.15), 8), col, w)
