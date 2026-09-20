# Night -- "Victoria alone, the Southern Cross". Palette: black, blue, red.
# Black sky, a band of deep sea-blue at the foot, red for every point of light. Trinidad
# has been left behind (later seized); Victoria sails on alone for Spain, the one ship of
# five that will finish the circuit -- home 6 September 1522, eighteen of two-seventy
# aboard. Crux and the Pointers, plotted true; a red lantern and a red wake, the day's
# last little light.
import os, math, numpy as np
from PIL import Image, ImageDraw
import sys
sys.path.insert(0, os.path.dirname(__file__))
from _ship import ship

W, H = 400, 600
BLK, BLU, RED = (0, 0, 0), (18, 61, 176), (224, 27, 36)
rng = np.random.default_rng(15220906)
im = Image.new("RGB", (W, H), BLK)
d = ImageDraw.Draw(im)

HORIZON = 420

# --- stars: sparse red pinpoints across the deep-blue sky ---
for _ in range(220):
    x, y = rng.integers(0, W), rng.integers(0, HORIZON)
    if rng.random() < 0.85:
        im.putpixel((int(x), int(y)), RED)
    else:
        d.ellipse((x - 1, y - 1, x + 1, y + 1), fill=RED)

# --- Crux (the Southern Cross) and the Pointers, plotted, centred high overhead ---
# local pixel layout approximating the true shape: long axis (Gacrux-Acrux) vertical,
# short axis (Mimosa-Delta Crucis) horizontal, Pointers (Alpha/Beta Centauri) to the left.
cx, cy = 190, 140
Gacrux = (cx + 6, cy - 62)
Acrux = (cx - 4, cy + 58)
Mimosa = (cx + 58, cy - 6)
DeltaCru = (cx - 56, cy + 4)
AlphaCen = (cx - 150, cy + 30)
BetaCen = (cx - 168, cy - 22)
for a, b in ((Gacrux, Acrux), (Mimosa, DeltaCru)):
    d.line((a, b), fill=RED, width=1)
for name, (x, y), mag in ((("Acrux"), Acrux, 0.8), ("Gacrux", Gacrux, 1.6),
                           ("Mimosa", Mimosa, 1.3), ("Delta Crucis", DeltaCru, 2.8),
                           ("Alpha Cen", AlphaCen, 0.0), ("Beta Cen", BetaCen, 0.6)):
    r = max(2, 6 - mag * 1.6)
    d.ellipse((x - r, y - r, x + r, y + r), fill=RED)
d.line((AlphaCen, (cx - 40, cy + 14)), fill=RED, width=1)
d.line((BetaCen, (cx - 40, cy + 14)), fill=RED, width=1)
# small ticks marking where the long axis points -- to the south celestial pole, off-frame
gx, gy = Gacrux; ax, ay = Acrux
ux, uy = (ax - gx), (ay - gy); L = math.hypot(ux, uy); ux, uy = ux / L, uy / L
ex, ey = ax + ux * 90, ay + uy * 90
for t in np.linspace(0, 1, 6):
    tx, ty = ax + (ex - ax) * t, ay + (ey - ay) * t
    d.line((tx - 2, ty, tx + 2, ty), fill=RED, width=1)
d.text((cx - 20, cy + 90), "CRUX", fill=RED)

# --- sea: a deep-blue band, black ripple hatch, calmer than the strait ---
d.rectangle((0, HORIZON, W, H), fill=BLU)
for y in range(HORIZON, H, 6):
    x = 0
    while x < W:
        L = int(rng.integers(10, 34))
        if rng.random() < 0.5:
            d.line((x, y, x + L, y), fill=BLK, width=1)
        x += L + int(rng.integers(10, 26))

# --- Victoria, alone, sailing on; a lit stern lantern, a red wake ---
vx, vy, vs = 210, HORIZON + 110, 130
ship(d, vx, vy, vs, hull=RED, sail=RED, facing=-1, detail=True, lantern=RED)
for i, dx in enumerate((30, 55, 82, 112)):
    wy = vy + 10 + i * 3
    d.line((vx + dx, wy, vx + dx + 22, wy - 3), fill=RED, width=1)

d.text((16, 566), "VICTORIA, ALONE -- crossing for home, 1521-1522", fill=RED)
d.text((16, 580), "one ship of five returns: SANLUCAR, 6 september 1522 -- 18 of 270", fill=RED)

im.save(os.environ["OUT_RAW"])
