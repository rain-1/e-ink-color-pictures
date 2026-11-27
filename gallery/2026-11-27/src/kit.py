"""Shared helpers for the 2026-11-27 pieces.

Draw at 3x in pure palette colours (PIL shapes are not antialiased), put any tonal
passages in as pre-screened 1x arrays, then reduce by majority vote per 3x3 block so
no off-palette fringe colours ever appear. Small text is set at 1x afterwards.
"""
import os, math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, S = 400, 600, 3
K = (0, 0, 0); WH = (255, 255, 255); R = (0xE0, 0x1B, 0x24)
Y = (0xF5, 0xD4, 0x00); B = (0x12, 0x3D, 0xB0); G = (0x1E, 0x9B, 0x3C)
PAL = np.array([K, WH, R, Y, B, G], dtype=np.int32)

FD = "/usr/share/fonts/truetype/"
FONTS = {
    "sans": FD + "dejavu/DejaVuSans.ttf", "sansb": FD + "dejavu/DejaVuSans-Bold.ttf",
    "serif": FD + "dejavu/DejaVuSerif.ttf", "serifb": FD + "dejavu/DejaVuSerif-Bold.ttf",
    "serifi": FD + "liberation/LiberationSerif-Italic.ttf", "mono": FD + "dejavu/DejaVuSansMono.ttf",
    "cond": FD + "liberation/LiberationSans-Regular.ttf", "condb": FD + "liberation/LiberationSans-Bold.ttf",
    "libi": FD + "liberation/LiberationSerif-Italic.ttf", "libb": FD + "liberation/LiberationSerif-Bold.ttf",
    "lib": FD + "liberation/LiberationSerif-Regular.ttf",
}
def font(name, size):
    return ImageFont.truetype(FONTS[name], size)

BAYER8 = np.array([
    [0, 32, 8, 40, 2, 34, 10, 42], [48, 16, 56, 24, 50, 18, 58, 26],
    [12, 44, 4, 36, 14, 46, 6, 38], [60, 28, 52, 20, 62, 30, 54, 22],
    [3, 35, 11, 43, 1, 33, 9, 41], [51, 19, 59, 27, 49, 17, 57, 25],
    [15, 47, 7, 39, 13, 45, 5, 37], [63, 31, 55, 23, 61, 29, 53, 21]]) / 64.0 + 1 / 128.0

def bayer(h=H, w=W):
    return np.tile(BAYER8, (h // 8 + 1, w // 8 + 1))[:h, :w]

def noise(h=H, w=W, seed=1):
    return np.random.default_rng(seed).random((h, w))

def screen(t, ca, cb, thr=None):
    """Two-colour screen: cb where tone t exceeds the threshold map, else ca. -> HxWx3 uint8"""
    thr = bayer(*t.shape) if thr is None else thr
    m = (t > thr)[..., None]
    return np.where(m, np.array(cb, np.uint8), np.array(ca, np.uint8)).astype(np.uint8)

def canvas(bg=WH):
    """bg: colour tuple or a 1x HxWx3 uint8 array."""
    if isinstance(bg, np.ndarray):
        img = Image.fromarray(bg).resize((W * S, H * S), Image.NEAREST)
    else:
        img = Image.new("RGB", (W * S, H * S), bg)
    d = ImageDraw.Draw(img)
    d.fontmode = "1"
    return img, d

def to_index(a):
    a = a.astype(np.int32)
    out = np.empty(a.shape[:2], np.uint8)
    for y0 in range(0, a.shape[0], 200):
        blk = a[y0:y0 + 200]
        d = ((blk[:, :, None, :] - PAL[None, None]) ** 2).sum(-1)
        out[y0:y0 + 200] = d.argmin(-1)
    return out

def finish(img, post=None, ink=()):
    """Majority-vote reduce to 400x600. `ink`: colours given a head start so thin lines survive."""
    idx = to_index(np.asarray(img))
    blocks = idx.reshape(H, S, W, S).transpose(0, 2, 1, 3).reshape(H, W, S * S)
    counts = np.stack([(blocks == i).sum(-1) for i in range(6)], -1).astype(np.float32)
    for c in ink:
        i = int((PAL == np.array(c)).all(1).argmax())
        counts[..., i] *= 1.9
    out = Image.fromarray(PAL[counts.argmax(-1)].astype(np.uint8))
    if post:
        d = ImageDraw.Draw(out); d.fontmode = "1"
        post(d, out)
    out.save(os.environ.get("OUT_RAW", "out.png"))
    return out

def P(*pts):
    """scale 1x coords to 3x"""
    return [(x * S, y * S) for x, y in pts]

def s(v):
    return int(round(v * S))

def line(d, pts, fill, w=1.0):
    d.line(P(*pts), fill=fill, width=max(1, s(w)), joint="curve")

def poly(d, pts, fill, outline=None, w=1.0):
    d.polygon(P(*pts), fill=fill)
    if outline:
        d.line(P(*pts, pts[0]), fill=outline, width=max(1, s(w)), joint="curve")

def rect(d, x0, y0, x1, y1, fill=None, outline=None, w=1.0):
    d.rectangle([s(x0), s(y0), s(x1), s(y1)], fill=fill, outline=outline, width=max(1, s(w)) if outline else 0)

def circ(d, x, y, r, fill=None, outline=None, w=1.0):
    d.ellipse([s(x - r), s(y - r), s(x + r), s(y + r)], fill=fill, outline=outline, width=max(1, s(w)) if outline else 0)

def ell(d, x, y, rx, ry, fill=None, outline=None, w=1.0):
    d.ellipse([s(x - rx), s(y - ry), s(x + rx), s(y + ry)], fill=fill, outline=outline, width=max(1, s(w)) if outline else 0)

def text(d, x, y, t, f, fill=K, anchor="la"):
    """1x text (use in post) or 3x text if the font was sized for 3x and coords pre-scaled."""
    d.text((x, y), t, font=f, fill=fill, anchor=anchor)

def thermometer(d, x, y, h, lo, hi, val, bg=WH, w=9, ticks=True):
    """A small mercury thermometer at 1x coords: top-left x,y; height h; returns nothing."""
    rect(d, x, y, x + w, y + h, fill=bg, outline=K, w=1)
    cx = x + w / 2
    top, bot = y + 5, y + h - 9
    rect(d, cx - 1.2, top, cx + 1.2, bot + 2, fill=WH, outline=K, w=0.7)
    fy = bot - (val - lo) / (hi - lo) * (bot - top)
    rect(d, cx - 0.9, fy, cx + 0.9, bot + 2, fill=R)
    circ(d, cx, bot + 4, 3, fill=R, outline=K, w=0.7)
    if ticks:
        n = 10
        for i in range(n + 1):
            ty = top + (bot - top) * i / n
            line(d, [(x + 1, ty), (x + (3 if i % 5 == 0 else 2), ty)], K, 0.7)
