"""Shared helpers for 2026-10-11 (momijigari). Canvas is 800x1200 (2x panel)."""
import math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 800, 1200
K = (0, 0, 0); WH = (255, 255, 255); R = (0xE0, 0x1B, 0x24)
Y = (0xF5, 0xD4, 0x00); B = (0x12, 0x3D, 0xB0); G = (0x1E, 0x9B, 0x3C)
ORANGE = (235, 120, 18)     # dithers to red+yellow
RUST = (150, 30, 20)        # red+black
OLIVE = (100, 120, 20)      # green+yellow+black
SKY = (130, 160, 220)       # blue+white
DUSK = (70, 40, 120)        # blue+red+black

FONT_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
FONT_SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FONT_ITAL = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
FONT_SC = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def vgrad(img, box, stops):
    """Vertical gradient in box through [(t, colour), ...]."""
    x0, y0, x1, y1 = box
    d = ImageDraw.Draw(img)
    for y in range(y0, y1):
        t = (y - y0) / max(1, y1 - y0 - 1)
        for (ta, ca), (tb, cb) in zip(stops, stops[1:]):
            if ta <= t <= tb:
                c = lerp(ca, cb, (t - ta) / max(1e-6, tb - ta)); break
        d.line([(x0, y), (x1 - 1, y)], fill=c)


def value_noise(w, h, scale, seed=0, octaves=4):
    rng = np.random.default_rng(seed)
    out = np.zeros((h, w)); amp = 1.0; tot = 0
    for o in range(octaves):
        s = scale / (2 ** o)
        gw, gh = int(w / s) + 3, int(h / s) + 3
        g = rng.random((gh, gw))
        im = Image.fromarray((g * 255).astype(np.uint8)).resize(
            (int(gw * s), int(gh * s)), Image.BICUBIC)
        out += amp * np.asarray(im, dtype=float)[:h, :w] / 255
        tot += amp; amp *= 0.5
    return out / tot


def _rot(cx, cy, x, y, angle):
    c, s = math.cos(angle), math.sin(angle)
    return (cx + x * c - y * s, cy + x * s + y * c)


def _lobe_dirs(lobes, spread_deg=290):
    sp = math.radians(spread_deg)
    return [-sp / 2 + sp * (i + 0.5) / lobes for i in range(lobes)]


def _lobe_len(i, lobes):
    m = (lobes - 1) / 2
    return 1.0 - 0.45 * (abs(i - m) / m) ** 1.6


def maple_leaf(cx, cy, size, angle=0.0, lobes=7, depth=0.38, jag=0.05, seed=None, spread=290):
    """Palmate maple outline, stem pointing down (before rotation by `angle` radians)."""
    rnd = random.Random(seed)
    sp = math.radians(spread)
    pts = []
    n = 70 * lobes
    for k in range(n + 1):
        u = k / n
        th = -sp / 2 + sp * u
        lp = u * lobes
        i = min(lobes - 1, int(lp)); f = lp - i
        prof = max(0.0, 1 - abs(2 * f - 1)) ** 1.6
        r = size * _lobe_len(i, lobes) * (depth + (1 - depth) * prof)
        teeth = 5
        r *= 1 + jag * prof * (abs(math.sin(f * math.pi * teeth * 2)) - 0.5)
        pts.append(_rot(cx, cy, r * math.sin(th), -r * math.cos(th), angle))
    return pts


def maple_veins(cx, cy, size, angle=0.0, lobes=7, spread=290):
    out = []
    for i, th in enumerate(_lobe_dirs(lobes, spread)):
        L = size * _lobe_len(i, lobes) * 0.9
        out.append([_rot(cx, cy, 0, 0, angle),
                    _rot(cx, cy, L * math.sin(th), -L * math.cos(th), angle)])
    return out


def stem(cx, cy, size, angle=0.0):
    return [_rot(cx, cy, 0, 0, angle), _rot(cx, cy, size * 0.08, size * 0.75, angle)]


def draw_maple(d, cx, cy, size, angle, fill, outline=K, vein=None, lobes=7, seed=None, ow=2):
    pts = maple_leaf(cx, cy, size, angle, lobes=lobes, seed=seed)
    d.polygon(pts, fill=fill)
    if outline is not None:
        d.line(pts + [pts[0]], fill=outline, width=ow)
    if vein is not None:
        for ln in maple_veins(cx, cy, size, angle, lobes):
            d.line(ln, fill=vein, width=max(1, ow - 0))
    d.line(stem(cx, cy, size, angle), fill=outline if outline else fill, width=max(2, ow))


def save(img, path):
    img.convert("RGB").save(path)
