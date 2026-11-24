# Shared helpers for the 2026-11-24 generators. Everything is drawn at the panel's native
# 400x600 with no anti-aliasing, in pure palette colours; tone comes from screens (Bayer or
# spatter) applied here, so render.py can run with --dither none.
import os, math, subprocess, functools
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 400, 600
K = (0, 0, 0); Wh = (255, 255, 255); R = (0xE0, 0x1B, 0x24)
Y = (0xF5, 0xD4, 0x00); B = (0x12, 0x3D, 0xB0); G = (0x1E, 0x9B, 0x3C)

def _bayer(n):
    m = np.array([[0, 2], [3, 1]])
    while m.shape[0] < n:
        m = np.block([[4 * m, 4 * m + 2], [4 * m + 3, 4 * m + 1]])
    return (m + 0.5) / m.size
BAYER = np.tile(_bayer(8), (H // 8 + 1, W // 8 + 1))[:H, :W].astype(np.float32)
YY, XX = np.mgrid[0:H, 0:W].astype(np.float32)

def spatter(seed):
    """A lithographer's crachis: clumpy random screen instead of the regular Bayer."""
    rng = np.random.default_rng(seed)
    a = rng.random((H, W)); b = rng.random((H // 2, W // 2)).repeat(2, 0).repeat(2, 1)
    s = 0.55 * a + 0.45 * b
    return ((s.argsort(None).argsort().reshape(H, W) + 0.5) / s.size).astype(np.float32)

def fbm(seed, scale=64, octv=4):
    rng = np.random.default_rng(seed); out = np.zeros((H, W), np.float32); amp, tot = 1.0, 0.0
    for o in range(octv):
        s = max(2, int(scale / 2 ** o))
        g = rng.random((H // s + 3, W // s + 3)).astype(np.float32)
        im = Image.fromarray(g).resize(((W // s + 3) * s, (H // s + 3) * s), Image.BICUBIC)
        out += amp * np.asarray(im)[s:s + H, s:s + W]; tot += amp; amp *= 0.5
    out /= tot
    return (out - out.min()) / (out.max() - out.min())

def new(bg=Wh):
    img = Image.new("RGB", (W, H), bg); d = ImageDraw.Draw(img); d.fontmode = "1"
    return img, d

def tone(img, mask, ca, cb, t, screen=None):
    """Inside mask: colour cb where t beats the screen, else ca (ca=None leaves it alone)."""
    scr = BAYER if screen is None else screen
    a = np.asarray(img).copy(); on = mask & (t > scr)
    a[on] = cb
    if ca is not None:
        a[mask & ~on] = ca
    img.paste(Image.fromarray(a))

def mask_of(fn):
    m = Image.new("1", (W, H), 0); fn(ImageDraw.Draw(m)); return np.asarray(m).astype(bool)

def poly_mask(pts): return mask_of(lambda d: d.polygon(pts, fill=1))
def ell_mask(cx, cy, rx, ry): return ((XX - cx) / rx) ** 2 + ((YY - cy) / ry) ** 2 <= 1

@functools.lru_cache(None)
def _path(spec):
    return subprocess.check_output(["fc-match", "-f", "%{file}", spec]).decode()
def font(spec, size): return ImageFont.truetype(_path(spec), size)

def spaced(d, x, y, s, f, fill, gap=2, anchor="m"):
    """Letter-spaced text; x is the centre ('m'), left ('l') or right ('r')."""
    ws = [d.textlength(c, font=f) for c in s]; tot = sum(ws) + gap * (len(s) - 1)
    x0 = x - tot / 2 if anchor == "m" else (x if anchor == "l" else x - tot)
    for c, w in zip(s, ws):
        d.text((round(x0), y), c, font=f, fill=fill); x0 += w + gap

def branch(d, x, y, ang, ln, wd, depth, col, rng, spread=0.5, shrink=0.72, tips=None, bend=0.0):
    """Recursive tree limb. ang in radians (0 = right, -pi/2 = up). tips collects twig ends."""
    if depth == 0 or ln < 2:
        if tips is not None: tips.append((x, y))
        return
    segs = 3; a = ang
    for _ in range(segs):
        a += rng.uniform(-0.18, 0.18) + bend
        x2 = x + math.cos(a) * ln / segs; y2 = y + math.sin(a) * ln / segs
        d.line((x, y, x2, y2), fill=col, width=max(1, round(wd)))
        x, y = x2, y2
    n = 2 if rng.random() < 0.75 else 3
    for i in range(n):
        da = rng.uniform(0.25, spread + 0.25) * (1 if i % 2 == 0 else -1) * rng.uniform(0.6, 1.2)
        branch(d, x, y, a + da, ln * shrink * rng.uniform(0.8, 1.15), wd * 0.68, depth - 1, col, rng,
               spread, shrink, tips, bend)

def save(img):
    out = os.environ.get("OUT_RAW", "out.png"); img.save(out)
