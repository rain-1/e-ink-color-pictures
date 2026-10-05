"""Shared helpers for 2026-10-05: palette, Bayer-mixed tones, noise, canvas at 400x600."""
import numpy as np
from PIL import Image

W, H = 400, 600
K = np.array((0, 0, 0)); Wt = np.array((255, 255, 255)); R = np.array((0xE0, 0x1B, 0x24))
Y = np.array((0xF5, 0xD4, 0x00)); B = np.array((0x12, 0x3D, 0xB0)); G = np.array((0x1E, 0x9B, 0x3C))
COL = dict(k=K, w=Wt, r=R, y=Y, b=B, g=G)

_b8 = np.array([[0,32,8,40,2,34,10,42],[48,16,56,24,50,18,58,26],[12,44,4,36,14,46,6,38],
                [60,28,52,20,62,30,54,22],[3,35,11,43,1,33,9,41],[51,19,59,27,49,17,57,25],
                [15,47,7,39,13,45,5,37],[63,31,55,23,61,29,53,21]]) / 64.0 + 1/128
BAYER = np.tile(_b8, (H // 8 + 1, W // 8 + 1))[:H, :W]

def canvas(c='w'):
    return np.tile(COL[c], (H, W, 1)).astype(np.uint8)

def mix(img, mask, c1, c2, t):
    """Inside mask, screen between colour c1 (t=0) and c2 (t=1). t scalar or HxW array."""
    t = np.broadcast_to(np.asarray(t, float), (H, W))
    pick2 = BAYER < t
    m = mask & pick2; img[m] = COL[c2]
    m = mask & ~pick2; img[m] = COL[c1]

def fill(img, mask, c):
    img[mask] = COL[c]

def grid():
    y, x = np.mgrid[0:H, 0:W]
    return x.astype(float), y.astype(float)

def vnoise(shape, scale, rng, octaves=4):
    """Fractal value noise, returns 0..1."""
    h, w = shape; out = np.zeros(shape); amp = 1; tot = 0
    for o in range(octaves):
        s = max(1, int(scale / 2**o))
        gh, gw = h // s + 2, w // s + 2
        g = rng.random((gh, gw))
        yi = np.arange(h) / s; xi = np.arange(w) / s
        y0 = yi.astype(int); x0 = xi.astype(int)
        fy = (yi - y0)[:, None]; fx = (xi - x0)[None, :]
        fy = fy*fy*(3-2*fy); fx = fx*fx*(3-2*fx)
        a = g[y0][:, x0]; b = g[y0][:, x0+1]; c = g[y0+1][:, x0]; d = g[y0+1][:, x0+1]
        out += amp * (a*(1-fx)*(1-fy) + b*fx*(1-fy) + c*(1-fx)*fy + d*fx*fy)
        tot += amp; amp *= 0.5
    return out / tot

def noise1(n, scale, rng, octaves=4):
    """1-D fractal noise of length n, 0..1."""
    return vnoise((1, n), scale, rng, octaves)[0]

def save(img):
    import os
    Image.fromarray(img.astype(np.uint8)).save(os.environ.get('OUT_RAW', 'out.png'))
