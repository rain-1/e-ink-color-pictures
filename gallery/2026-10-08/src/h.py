# shared helpers for 2026-10-08 — everything drawn at 2x (800x1200) in exact palette colours
import math, os, numpy as np
from PIL import Image, ImageDraw, ImageFont
S = 2; W, H = 400*S, 600*S
K, Wh, R, Y, B, G = (0,0,0), (255,255,255), (0xE0,0x1B,0x24), (0xF5,0xD4,0x00), (0x12,0x3D,0xB0), (0x1E,0x9B,0x3C)
FONTS = "/usr/share/fonts/truetype/"
def font(px, name="dejavu/DejaVuSerif.ttf"): return ImageFont.truetype(FONTS + name, px)
def serif(px, bold=False, italic=False):
    n = "liberation/LiberationSerif-" + ("BoldItalic" if bold and italic else "Bold" if bold else "Italic" if italic else "Regular") + ".ttf"
    return font(px, n)
def xform(pts, cx, cy, ang, sc):
    c, s = math.cos(ang), math.sin(ang)
    return [(cx + sc*(x*c - y*s), cy + sc*(x*s + y*c)) for x, y in pts]
def value_noise(w, h, cell, rng):
    gw, gh = w//cell + 2, h//cell + 2
    g = rng.random((gh, gw))
    ys, xs = np.mgrid[0:h, 0:w] / cell
    x0, y0 = xs.astype(int), ys.astype(int); fx, fy = xs - x0, ys - y0
    fx = fx*fx*(3-2*fx); fy = fy*fy*(3-2*fy)
    a = g[y0, x0]*(1-fx) + g[y0, x0+1]*fx; b = g[y0+1, x0]*(1-fx) + g[y0+1, x0+1]*fx
    return a*(1-fy) + b*fy
def fbm(w, h, rng, cells=(160, 80, 40, 20, 10)):
    out = np.zeros((h, w)); amp = 1; tot = 0
    for c in cells: out += amp*value_noise(w, h, c, rng); tot += amp; amp *= 0.55
    return out/tot
BAYER = np.array([[0,32,8,40,2,34,10,42],[48,16,56,24,50,18,58,26],[12,44,4,36,14,46,6,38],[60,28,52,20,62,30,54,22],
                  [3,35,11,43,1,33,9,41],[51,19,59,27,49,17,57,25],[15,47,7,39,13,45,5,37],[63,31,55,23,61,29,53,21]])/64+1/128
def screen(tone, cellpx=2):
    """tone 0..1 array at full res -> boolean 'on' mask through a Bayer screen of 8*cellpx pixels"""
    h, w = tone.shape
    t = np.kron(np.ones((h//(8*cellpx)+1, w//(8*cellpx)+1)), np.kron(BAYER, np.ones((cellpx, cellpx))))[:h, :w]
    return tone > t
PALS = np.array([K, Wh, R, Y, B, G], dtype=float)
def save(im):
    """Downsample 2x -> 1x by palette-mode of each 2x2 block (ties go to the globally rarer
    colour, i.e. the ink), so thin lines and text survive without grey halos."""
    a = np.asarray(im.convert("RGB"), dtype=float)
    idx = ((a[:, :, None, :] - PALS[None, None]) ** 2).sum(-1).argmin(-1)
    grey = (a.max(-1) - a.min(-1)) < 40                      # antialiased greys -> black/white, never green
    idx[grey] = np.where(a[grey].mean(-1) < 140, 0, 1)
    h, w = idx.shape[0]//S, idx.shape[1]//S
    blk = idx[:h*S, :w*S].reshape(h, S, w, S).transpose(0, 2, 1, 3).reshape(h, w, S*S)
    cnt = np.stack([(blk == k).sum(-1) for k in range(6)], -1).astype(float)
    rarity = 1 - np.bincount(idx.ravel(), minlength=6) / idx.size
    out = (cnt + rarity[None, None] * 0.5).argmax(-1)
    Image.fromarray(PALS[out].astype(np.uint8)).save(os.environ.get("OUT_RAW", "out.png"))
