"""Shared helpers for 2026-10-09. Everything is drawn directly in palette colours at 1x,
so pieces render with --dither none. Tones between two inks use an 8x8 Bayer screen."""
import os
import numpy as np
from PIL import Image, ImageDraw

W, H = 400, 600
K = (0, 0, 0); WH = (255, 255, 255); R = (0xE0, 0x1B, 0x24)
Y = (0xF5, 0xD4, 0x00); B = (0x12, 0x3D, 0xB0); G = (0x1E, 0x9B, 0x3C)

_b = np.array([[0, 32, 8, 40, 2, 34, 10, 42], [48, 16, 56, 24, 50, 18, 58, 26],
               [12, 44, 4, 36, 14, 46, 6, 38], [60, 28, 52, 20, 62, 30, 54, 22],
               [3, 35, 11, 43, 1, 33, 9, 41], [51, 19, 59, 27, 49, 17, 57, 25],
               [15, 47, 7, 39, 13, 45, 5, 37], [63, 31, 55, 23, 61, 29, 53, 21]]) / 64 + 1 / 128
BAYER = np.tile(_b, (H // 8 + 1, W // 8 + 1))[:H, :W]


def screen(arr, mask, a, b, t):
    """Inside boolean mask, paint ink b where Bayer < t (t scalar or HxW array), else a."""
    t = np.broadcast_to(np.asarray(t, float), (H, W))
    pick = BAYER < t
    arr[mask & pick] = b
    arr[mask & ~pick] = a


def to_arr(img):
    return np.array(img.convert("RGB"))


def save(img_or_arr):
    img = img_or_arr if isinstance(img_or_arr, Image.Image) else Image.fromarray(img_or_arr.astype(np.uint8))
    img.save(os.environ.get("OUT_RAW", "out.png"))


def mask_of(draw_fn):
    """Return a boolean mask of whatever draw_fn(ImageDraw) paints."""
    m = Image.new("L", (W, H), 0)
    draw_fn(ImageDraw.Draw(m))
    return np.array(m) > 127


def jamo(d, ch, x, y, s, fill, w=None):
    """Draw a basic Hangul letter shape as strokes in a box of size s at (x, y)."""
    w = w or max(2, int(s * 0.13))
    L = lambda a, b, c, e: d.line([(x + a * s, y + b * s), (x + c * s, y + e * s)], fill=fill, width=w)
    if ch == "ㄱ":
        L(.15, .2, .8, .2); L(.8, .2, .8, .85)
    elif ch == "ㄴ":
        L(.2, .15, .2, .8); L(.2, .8, .85, .8)
    elif ch == "ㅁ":
        d.rectangle([x + .2 * s, y + .2 * s, x + .8 * s, y + .8 * s], outline=fill, width=w)
    elif ch == "ㅅ":
        L(.5, .15, .15, .85); L(.5, .4, .85, .85)
    elif ch == "ㅇ":
        d.ellipse([x + .18 * s, y + .18 * s, x + .82 * s, y + .82 * s], outline=fill, width=w)
    elif ch == "·":
        r = s * .14; d.ellipse([x + .5 * s - r, y + .5 * s - r, x + .5 * s + r, y + .5 * s + r], fill=fill)
    elif ch == "ㅡ":
        L(.1, .5, .9, .5)
    elif ch == "ㅣ":
        L(.5, .1, .5, .9)


# stroke specs in unit box: ("l", x0,y0,x1,y1) line, ("r", x0,y0,x1,y1) rect, ("o", cx,cy,r) circle
JAMO = {
    "ㄱ": [("l", .15, .2, .8, .2), ("l", .8, .2, .8, .85)],
    "ㅋ": [("l", .15, .2, .8, .2), ("l", .8, .2, .8, .85), ("l", .2, .5, .8, .5)],
    "ㄴ": [("l", .2, .15, .2, .8), ("l", .2, .8, .85, .8)],
    "ㄷ": [("l", .85, .2, .2, .2), ("l", .2, .2, .2, .8), ("l", .2, .8, .85, .8)],
    "ㅌ": [("l", .85, .2, .2, .2), ("l", .2, .2, .2, .8), ("l", .2, .8, .85, .8), ("l", .2, .5, .8, .5)],
    "ㅁ": [("r", .2, .2, .8, .8)],
    "ㅂ": [("l", .22, .12, .22, .85), ("l", .78, .12, .78, .85), ("l", .22, .45, .78, .45), ("l", .22, .85, .78, .85)],
    "ㅍ": [("l", .12, .2, .88, .2), ("l", .12, .82, .88, .82), ("l", .35, .2, .35, .82), ("l", .65, .2, .65, .82)],
    "ㅅ": [("l", .5, .15, .15, .85), ("l", .5, .4, .85, .85)],
    "ㅈ": [("l", .15, .2, .85, .2), ("l", .5, .2, .15, .85), ("l", .5, .45, .85, .85)],
    "ㅊ": [("l", .5, .02, .5, .12), ("l", .15, .22, .85, .22), ("l", .5, .22, .15, .88), ("l", .5, .47, .85, .88)],
    "ㅇ": [("o", .5, .52, .32)],
    "ㆆ": [("l", .2, .2, .8, .2), ("o", .5, .6, .25)],
    "ㅎ": [("l", .5, .0, .5, .12), ("l", .2, .2, .8, .2), ("o", .5, .62, .24)],
    "·": [("d", .5, .5, .14)],
    "ㅡ": [("l", .1, .5, .9, .5)],
    "ㅣ": [("l", .5, .1, .5, .9)],
}


def glyph(d, ch, x, y, s, fill, w=None):
    w = w or max(2, int(s * 0.12))
    for st in JAMO[ch]:
        k = st[0]
        if k == "l":
            _, a, b, c, e = st
            d.line([(x + a * s, y + b * s), (x + c * s, y + e * s)], fill=fill, width=w)
            for px, py in ((a, b), (c, e)):  # round the joints
                d.ellipse([x + px * s - w / 2 + .5, y + py * s - w / 2 + .5, x + px * s + w / 2 - .5, y + py * s + w / 2 - .5], fill=fill)
        elif k == "r":
            _, a, b, c, e = st
            d.rectangle([x + a * s, y + b * s, x + c * s, y + e * s], outline=fill, width=w)
        elif k == "o":
            _, cx, cy, r = st
            d.ellipse([x + (cx - r) * s, y + (cy - r) * s, x + (cx + r) * s, y + (cy + r) * s], outline=fill, width=w)
        elif k == "d":
            _, cx, cy, r = st
            d.ellipse([x + (cx - r) * s, y + (cy - r) * s, x + (cx + r) * s, y + (cy + r) * s], fill=fill)


def font(size, serif=True, bold=False):
    from PIL import ImageFont
    name = ("DejaVuSerif" if serif else "DejaVuSans") + ("-Bold" if bold else "") + ".ttf"
    for base in ("/usr/share/fonts/truetype/dejavu/", ""):
        try:
            return ImageFont.truetype(base + name, size)
        except OSError:
            pass
    return ImageFont.load_default()
