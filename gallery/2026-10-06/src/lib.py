"""Shared helpers for 2026-10-06 (Kon-Tiki day). Everything works at 400x600, in palette colours."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 400, 600
K = (0, 0, 0); WH = (255, 255, 255); R = (224, 27, 36)
Y = (245, 212, 0); B = (18, 61, 176); G = (30, 155, 60)

def _bayer(n):
    m = np.array([[0]])
    while m.shape[0] < n:
        m = np.block([[4 * m, 4 * m + 2], [4 * m + 3, 4 * m + 1]])
    return (m + 0.5) / m.size
B8 = _bayer(8)
B4 = _bayer(4)

def thresh(h=H, w=W, m=B8):
    return np.tile(m, (h // m.shape[0] + 1, w // m.shape[1] + 1))[:h, :w]

YY, XX = np.mgrid[0:H, 0:W].astype(np.float32)
T8 = thresh()

def put(img, mask, col):
    img[mask] = col

def screen(img, mask, tone, a, b, T=None):
    """Within mask, mix colour a (tone 0) and b (tone 1) with an ordered screen."""
    T = T8 if T is None else T
    on = tone > T
    img[mask & ~on] = a
    img[mask & on] = b

def noise(seed, scale, octaves=4, h=H, w=W):
    """Cheap value noise, 0..1."""
    rng = np.random.default_rng(seed)
    out = np.zeros((h, w), np.float32); amp = 1; tot = 0
    for o in range(octaves):
        s = max(2, int(scale / 2 ** o))
        g = rng.random((h // s + 3, w // s + 3)).astype(np.float32)
        im = Image.fromarray((g * 255).astype(np.uint8)).resize(((w // s + 3) * s, (h // s + 3) * s), Image.BICUBIC)
        out += amp * np.asarray(im, np.float32)[:h, :w] / 255; tot += amp; amp *= 0.5
    return out / tot

def font(size, kind="serif"):
    p = {"serif": "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
         "serifb": "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
         "serifi": "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf",
         "sans": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
         "sansb": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
         "mono": "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"}[kind]
    return ImageFont.truetype(p, size)

def to_img(a):
    return Image.fromarray(a.astype(np.uint8), "RGB")

def snap(im):
    """Snap an RGB PIL image to the nearest palette colour (kills draw antialiasing)."""
    pal = np.array([K, WH, R, Y, B, G], np.float32)
    a = np.asarray(im.convert("RGB"), np.float32)
    d = ((a[:, :, None, :] - pal[None, None]) ** 2).sum(-1)
    return pal[d.argmin(-1)].astype(np.uint8)
