"""Shared drawing kit for 2026-11-26. Draw at 3x in pure palette colours (no anti-aliasing),
then reduce to 400x600 by majority vote per 3x3 block: crisp edges, no off-palette fringes."""
import math, os, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont

S = 3
W, H = 400, 600
K = (0, 0, 0); WH = (255, 255, 255); R = (0xE0, 0x1B, 0x24)
Y = (0xF5, 0xD4, 0x00); B = (0x12, 0x3D, 0xB0); G = (0x1E, 0x9B, 0x3C)
PALS = [K, WH, R, Y, B, G]
BAYER = np.array([[0, 32, 8, 40, 2, 34, 10, 42], [48, 16, 56, 24, 50, 18, 58, 26],
                  [12, 44, 4, 36, 14, 46, 6, 38], [60, 28, 52, 20, 62, 30, 54, 22],
                  [3, 35, 11, 43, 1, 33, 9, 41], [51, 19, 59, 27, 49, 17, 57, 25],
                  [15, 47, 7, 39, 13, 45, 5, 37], [63, 31, 55, 23, 61, 29, 53, 21]]) / 64.0 + 1 / 128


def font(size, name="DejaVuSerif-Bold.ttf"):
    return ImageFont.truetype(name, int(size * S))


class C:
    def __init__(s, bg):
        s.img = Image.new("RGB", (W * S, H * S), bg)
        s.d = ImageDraw.Draw(s.img)
        s.d.fontmode = "1"

    @staticmethod
    def P(pts):
        return [(x * S, y * S) for x, y in pts]

    def poly(s, pts, fill, outline=None, w=1.0):
        if fill is not None:
            s.d.polygon(s.P(pts), fill=fill)
        if outline is not None:
            s.line(list(pts) + [pts[0]], outline, w)

    def line(s, pts, fill, w=1.0):
        ww = max(1, round(w * S))
        s.d.line(s.P(pts), fill=fill, width=ww, joint="curve")
        if ww >= 4:
            r = ww / 2
            for x, y in (pts[0], pts[-1]):
                s.d.ellipse([x * S - r, y * S - r, x * S + r, y * S + r], fill=fill)

    def circ(s, x, y, r, fill=None, outline=None, w=1.0):
        s.d.ellipse([(x - r) * S, (y - r) * S, (x + r) * S, (y + r) * S], fill=fill,
                    outline=outline, width=max(1, round(w * S)))

    def ell(s, x0, y0, x1, y1, fill=None, outline=None, w=1.0):
        s.d.ellipse([x0 * S, y0 * S, x1 * S, y1 * S], fill=fill, outline=outline, width=max(1, round(w * S)))

    def rect(s, x0, y0, x1, y1, fill=None, outline=None, w=1.0):
        s.d.rectangle([x0 * S, y0 * S, x1 * S, y1 * S], fill=fill, outline=outline, width=max(1, round(w * S)))

    def arc(s, x, y, r, a0, a1, fill, w=1.0, ry=None):
        ry = r if ry is None else ry
        s.d.arc([(x - r) * S, (y - ry) * S, (x + r) * S, (y + ry) * S], a0, a1, fill=fill, width=max(1, round(w * S)))

    def pie(s, x, y, r, a0, a1, fill, ry=None):
        ry = r if ry is None else ry
        s.d.pieslice([(x - r) * S, (y - ry) * S, (x + r) * S, (y + ry) * S], a0, a1, fill=fill)

    def text(s, x, y, t, fill, f, anchor="mm"):
        s.d.text((x * S, y * S), t, fill=fill, font=f, anchor=anchor)

    def star(s, x, y, r, fill, w=1.0):
        """Egyptian five-armed star: five strokes from a small centre."""
        for k in range(5):
            a = -math.pi / 2 + k * 2 * math.pi / 5
            s.line([(x, y), (x + r * math.cos(a), y + r * math.sin(a))], fill, w)
        s.circ(x, y, max(0.8, r * 0.22), fill=fill)

    def is_plain(s, x, y, r, col):
        """True if the square around (x,y) is all one colour `col` (for scattering ornaments)."""
        box = s.img.crop((int((x - r) * S), int((y - r) * S), int((x + r) * S), int((y + r) * S)))
        cols = box.getcolors(4)
        return cols is not None and len(cols) == 1 and cols[0][1] == col

    def array(s):
        return reduce(np.asarray(s.img))

    def save(s, arr=None):
        arr = s.array() if arr is None else arr
        out = os.environ.get("OUT_RAW", "preview.png")
        Image.fromarray(arr, "RGB").save(out)


def reduce(a):
    """3x palette image -> 1x by majority vote."""
    pal = np.array(PALS, dtype=np.int32)
    d = ((a[:, :, None, :].astype(np.int32) - pal[None, None]) ** 2).sum(-1)
    idx = d.argmin(-1)
    votes = np.zeros((H, W, 6), dtype=np.int32)
    for i in range(6):
        votes[:, :, i] = (idx == i).reshape(H, S, W, S).sum((1, 3))
    return pal[votes.argmax(-1)].astype(np.uint8)


def block_border(c, x0, y0, x1, y1, t, cols, seg=10, line=K, bg=Y):
    """Egyptian block border: coloured tiles between two rules, all round a rectangle."""
    c.rect(x0, y0, x1, y1, fill=None, outline=line, w=t)
    c.rect(x0 + 1, y0 + 1, x1 - 1, y1 - 1, fill=None, outline=bg, w=t - 2)
    i = 0
    n = round((x1 - x0) / seg)
    sw = (x1 - x0) / n
    for k in range(n):
        for yy in (y0, y1 - t):
            c.rect(x0 + k * sw + 1.5, yy + 2.5, x0 + (k + 1) * sw - 1.5, yy + t - 2.5, fill=cols[(k + i) % len(cols)])
    n = round((y1 - y0 - 2 * t) / seg)
    sh = (y1 - y0 - 2 * t) / n
    for k in range(n):
        for xx in (x0, x1 - t):
            c.rect(xx + 2.5, y0 + t + k * sh + 1.5, xx + t - 2.5, y0 + t + (k + 1) * sh - 1.5, fill=cols[(k + 1) % len(cols)])


def bez(p0, p1, p2, p3, n=24):
    out = []
    for i in range(n + 1):
        t = i / n; u = 1 - t
        out.append((u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0],
                    u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1]))
    return out
