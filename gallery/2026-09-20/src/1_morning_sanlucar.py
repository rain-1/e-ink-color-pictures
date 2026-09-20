# Morning -- "Sanlucar de Barrameda, dawn". Palette: red, yellow.
# 20 September 1519: Magellan's fleet of five ships puts out to sea. A woodcut-style
# departure: a red sun lifting clear of the water, a fleet of five in perspective
# heading out past a harbour tower, ripples cut yellow into the red sea.
import os, math, numpy as np
from PIL import Image, ImageDraw
import sys
sys.path.insert(0, os.path.dirname(__file__))
from _ship import ship

W, H = 400, 600
RED, YEL = (224, 27, 36), (245, 212, 0)
rng = np.random.default_rng(15190920)
im = Image.new("RGB", (W, H), YEL)
d = ImageDraw.Draw(im)

HORIZON = 250

# --- sky: a few long horizontal cut-lines, thinning upward (dawn haze low) ---
for y in range(0, HORIZON, 5):
    density = 1 - abs(y - (HORIZON - 40)) / HORIZON
    x = 0
    while x < W:
        L = int(rng.integers(10, 50))
        if rng.random() < 0.35 * density:
            d.line((x, y, x + L, y), fill=RED, width=1)
        x += L + int(rng.integers(6, 24))

# --- sun: a big red disc, three-quarters clear of the horizon ---
sx, sy, sr = 205, HORIZON - 6, 92
d.pieslice((sx - sr, sy - sr, sx + sr, sy + sr), 180, 360, fill=RED)
d.ellipse((sx - sr, sy - sr - 2, sx + sr, sy + 4), fill=RED)

# --- sea: red field, yellow ripple cuts, denser/longer near the bottom (near) ---
d.rectangle((0, HORIZON, W, H), fill=RED)
for y in range(HORIZON, H, 4):
    depth = (y - HORIZON) / (H - HORIZON)
    x = 0
    while x < W:
        L = int(4 + depth * 30)
        if rng.random() < 0.8:
            d.line((x, y, x + L, y + rng.integers(-1, 2)), fill=YEL, width=1 if depth < 0.6 else 2)
        x += L + int(rng.integers(3, 10) - depth * 5)

# --- the harbour tower, left, small red silhouette with a flag ---
tx, tb = 34, HORIZON + 6
d.polygon([(tx - 10, tb), (tx + 10, tb), (tx + 8, tb - 70), (tx - 8, tb - 70)], fill=RED)
d.polygon([(tx - 12, tb - 70), (tx + 12, tb - 70), (tx, tb - 92)], fill=RED)
d.line((tx, tb - 92, tx, tb - 112), fill=RED, width=2)
d.polygon([(tx, tb - 112), (tx + 16, tb - 106), (tx, tb - 100)], fill=RED)

# --- the fleet: five ships outbound, far (small, near the sun) to near (large, foreground) ---
# Trinidad (flagship, largest/nearest), San Antonio, Concepcion, Victoria, Santiago (smallest/farthest)
fleet = [
    (0.98, 320, HORIZON + 150, 116),
    (0.72, 250, HORIZON + 96, 84),
    (0.52, 300, HORIZON + 60, 58),
    (0.34, 175, HORIZON + 34, 42),
    (0.20, 230, HORIZON + 16, 30),
]
fleet.sort(key=lambda t: t[0])  # far to near, so nearer ships paint on top
for depth, x, y, size in fleet:
    # whole silhouette in yellow -- a cut-paper shape against the red sea
    ship(d, x, y, size, hull=YEL, sail=YEL, facing=1, detail=size > 34)

d.text((16, 566), "SANLUCAR DE BARRAMEDA -- 20 SEPTEMBER 1519", fill=RED)
d.text((16, 580), "five ships outbound: TRINIDAD SAN ANTONIO CONCEPCION VICTORIA SANTIAGO", fill=RED)

im.save(os.environ["OUT_RAW"])
