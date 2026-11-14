"""Shared bits for the 2026-11-14 Monet pieces: palette, noise, tone screens."""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

W, H = 400, 600
K = (0, 0, 0); WH = (255, 255, 255); R = (0xE0, 0x1B, 0x24)
Y = (0xF5, 0xD4, 0x00); B = (0x12, 0x3D, 0xB0); G = (0x1E, 0x9B, 0x3C)
COLS = [K, WH, R, Y, B, G]

BAYER8 = np.array([
    [0, 32, 8, 40, 2, 34, 10, 42], [48, 16, 56, 24, 50, 18, 58, 26],
    [12, 44, 4, 36, 14, 46, 6, 38], [60, 28, 52, 20, 62, 30, 54, 22],
    [3, 35, 11, 43, 1, 33, 9, 41], [51, 19, 59, 27, 49, 17, 57, 25],
    [15, 47, 7, 39, 13, 45, 5, 37], [63, 31, 55, 23, 61, 29, 53, 21]]) / 64.0 + 1 / 128
BAYER = np.tile(BAYER8, (H // 8 + 1, W // 8 + 1))[:H, :W]


def save(img):
    img.save(os.environ.get("OUT_RAW", "out.png"))


def noise(cell, seed, w=W, h=H):
    """Smooth value noise in 0..1, feature size ~cell px."""
    r = np.random.default_rng(seed)
    gw, gh = max(2, w // cell + 2), max(2, h // cell + 2)
    a = (r.random((gh, gw)) * 255).astype(np.uint8)
    im = Image.fromarray(a).resize((w, h), Image.BICUBIC)
    return np.asarray(im, dtype=np.float32) / 255.0


def fbm(cell, seed, octaves=3):
    out = np.zeros((H, W), np.float32); amp = 1.0; tot = 0
    for i in range(octaves):
        out += amp * noise(max(2, cell // (2 ** i)), seed + i * 17); tot += amp; amp *= 0.5
    return out / tot


def mask(draw_fn, blur=0):
    """Greyscale mask 0..1 drawn by draw_fn(ImageDraw)."""
    m = Image.new("L", (W, H), 0)
    draw_fn(ImageDraw.Draw(m))
    if blur:
        m = m.filter(ImageFilter.GaussianBlur(blur))
    return np.asarray(m, dtype=np.float32) / 255.0


def pick(rng, w):
    """w: 6 weights (K, W, R, Y, B, G) -> palette colour."""
    w = np.clip(np.asarray(w, dtype=np.float64), 0, None)
    s = w.sum()
    if s <= 0:
        return WH
    return COLS[int(rng.choice(6, p=w / s))]
