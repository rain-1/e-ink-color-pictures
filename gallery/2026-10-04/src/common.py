# Shared helpers for 2026-10-04 (Laudes Creaturarum).
# Draw at 2x (800x1200) in pure palette colours with PIL, put tonal areas in with an
# 8x8 Bayer screen computed at 1x (so it survives the 2x->1x downsample), then finish()
# downsamples with a box filter and snaps every pixel to the nearest palette colour.
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

S = 2
W, H = 400, 600
W2, H2 = W * S, H * S
K = (0, 0, 0); WH = (255, 255, 255); R = (0xE0, 0x1B, 0x24)
Y = (0xF5, 0xD4, 0x00); B = (0x12, 0x3D, 0xB0); G = (0x1E, 0x9B, 0x3C)
PAL = np.array([K, WH, R, Y, B, G], dtype=np.float32)

_b2 = np.array([[0, 2], [3, 1]])
def _bayer(n):
    m = _b2
    while m.shape[0] < n:
        m = np.block([[4 * m, 4 * m + 2], [4 * m + 3, 4 * m + 1]])
    return (m + 0.5) / m.size
BAYER8 = _bayer(8)

def threshold_1x(h=H, w=W):
    return np.tile(BAYER8, (h // 8 + 1, w // 8 + 1))[:h, :w]

def up(a):
    """1x array -> 2x (nearest)."""
    return np.repeat(np.repeat(a, S, 0), S, 1)

def screen(tone_1x):
    """tone in 0..1 at 1x -> boolean 2x mask, True where 'ink' (tone above threshold)."""
    return up(tone_1x > threshold_1x(*tone_1x.shape))

def new(bg=WH):
    img = Image.new("RGB", (W2, H2), bg)
    return img, ImageDraw.Draw(img)

def paint(img, mask2x, colour):
    """Set pixels of img where boolean 2x mask is True. Returns new Image."""
    a = np.asarray(img).copy()
    a[mask2x] = colour
    return Image.fromarray(a)

def tone_fill(img, region2x, tone_1x, ink, paper):
    """Inside region2x, screen tone (0..1) of ink over paper."""
    m = screen(tone_1x)
    a = np.asarray(img).copy()
    a[region2x & m] = ink
    a[region2x & ~m] = paper
    return Image.fromarray(a)

def mask_of(draw_fn):
    """Build a 2x boolean mask by calling draw_fn(ImageDraw) on an L canvas (fill=255)."""
    m = Image.new("L", (W2, H2), 0)
    draw_fn(ImageDraw.Draw(m))
    return np.asarray(m) > 127

def noise(h, w, scale, seed=0, octaves=4):
    """Smooth fractal value noise in 0..1, shape (h, w); scale = feature size in px."""
    rng = np.random.default_rng(seed)
    out = np.zeros((h, w), np.float32); amp = 1.0; tot = 0
    for o in range(octaves):
        s = max(1.0, scale / (2 ** o))
        gh, gw = int(h / s) + 3, int(w / s) + 3
        g = rng.random((gh, gw)).astype(np.float32)
        img = Image.fromarray((g * 255).astype(np.uint8)).resize(
            (int(gw * s), int(gh * s)), Image.BICUBIC)
        out += amp * (np.asarray(img, np.float32)[:h, :w] / 255)
        tot += amp; amp *= 0.5
    out /= tot
    return (out - out.min()) / (out.max() - out.min() + 1e-6)

FONTS = {
    "serif": "/usr/share/fonts/truetype/freefont/FreeSerif.ttf",
    "serif-b": "/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf",
    "serif-i": "/usr/share/fonts/truetype/freefont/FreeSerifItalic.ttf",
    "dejavu-serif-b": "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
}
def font(name, size):
    return ImageFont.truetype(FONTS[name], size)

def finish(img):
    """2x RGB -> 1x, every pixel snapped to the nearest palette colour, saved to OUT_RAW."""
    small = img.resize((W, H), Image.BOX)
    a = np.asarray(small, np.float32).reshape(-1, 3)
    d = ((PAL[None] - a[:, None]) ** 2).sum(-1)
    out = PAL[d.argmin(1)].astype(np.uint8).reshape(H, W, 3)
    res = Image.fromarray(out)
    res.save(os.environ.get("OUT_RAW", "out.png"))
    return res
