# Evening -- "Tidore, the Spice Islands". Palette: red, white.
# November 1521: Trinidad and Victoria anchor at Tidore and load cloves. Magellan is
# already dead (Mactan, 27 April 1521); Concepcion was burned for lack of hands months
# before. A botanical plate: the volcano behind, a clove branch drawn in the foreground,
# two ships riding at anchor in the bay.
import os, math, numpy as np
from PIL import Image, ImageDraw
import sys
sys.path.insert(0, os.path.dirname(__file__))
from _ship import ship

W, H = 400, 600
RED, WHT = (224, 27, 36), (255, 255, 255)
rng = np.random.default_rng(15211100)
im = Image.new("RGB", (W, H), WHT)
d = ImageDraw.Draw(im)

HORIZON = 330

# --- the volcano of Tidore, red silhouette, a plume drifting off the peak ---
vx, vb = 235, HORIZON + 4
volcano = [(vx - 150, vb), (vx - 40, 120), (vx - 14, 96), (vx + 6, 118), (vx + 150, vb)]
d.polygon(volcano, fill=RED)
# crater notch and a thin plume of red dashes drifting right
d.polygon([(vx - 20, 108), (vx - 2, 100), (vx + 10, 112), (vx - 6, 118)], fill=WHT)
px, py = vx, 104
for i in range(26):
    px += rng.uniform(3, 7); py -= rng.uniform(0, 2)
    if rng.random() < 0.7:
        d.ellipse((px - 2, py - 2, px + 2, py + 2), fill=RED)

# --- sea: white with fine red ripple hatch ---
d.rectangle((0, HORIZON, W, H), fill=WHT)
for y in range(HORIZON, H, 6):
    x = 0
    while x < W:
        L = int(rng.integers(8, 30))
        d.line((x, y, x + L, y), fill=RED, width=1)
        x += L + int(rng.integers(6, 16))

# --- clove branch, foreground, botanical-plate detail: leaves, buds in clusters ---
def leaf(cx, cy, length, ang, w):
    ux, uy = math.cos(ang), math.sin(ang)
    nx, ny = -uy, ux
    tip = (cx + ux * length, cy + uy * length)
    base = (cx, cy)
    mid = length * 0.55
    d.polygon([base, (cx + ux * mid + nx * w, cy + uy * mid + ny * w), tip,
               (cx + ux * mid - nx * w, cy + uy * mid - ny * w)], outline=RED, width=2)
    d.line((base, tip), fill=RED, width=1)

def clove_bud(cx, cy, s):
    d.ellipse((cx - s * 0.35, cy - s, cx + s * 0.35, cy), fill=RED)          # the bud head
    d.line((cx, cy, cx, cy + s * 0.9), fill=RED, width=max(1, int(s * 0.18)))  # the stem
    for a in (-1, 1):
        d.line((cx, cy + s * 0.9, cx + a * s * 0.22, cy + s * 1.2), fill=RED, width=1)  # calyx

stem = [(34, 558), (46, 520), (40, 440), (58, 370), (50, 300)]
d.line(stem, fill=RED, width=5)
leaf_specs = [(46, 500, 70, -0.5), (42, 460, 78, -2.9), (52, 400, 66, -0.55), (46, 360, 74, -2.85),
              (56, 320, 60, -0.6)]
for cx, cy, L, ang in leaf_specs:
    leaf(cx, cy, L, ang, 16)
bud_specs = [(96, 470, 20), (112, 486, 16), (100, 430, 18), (72, 340, 22), (88, 356, 16), (60, 300, 14)]
for cx, cy, s in bud_specs:
    clove_bud(cx, cy, s)

# --- two ships riding at anchor in the bay ---
ship(d, 250, HORIZON + 70, 70, hull=RED, sail=RED, facing=1, detail=True)
ship(d, 310, HORIZON + 130, 92, hull=RED, sail=RED, facing=1, detail=True)
for x, y, s in ((250, HORIZON + 70, 70), (310, HORIZON + 130, 92)):
    d.line((x + s * 0.30, y - 0.10 * s, x + s * 0.30, y + s * 0.30), fill=RED, width=1)  # anchor line

d.text((16, 566), "TIDORE, THE SPICE ISLANDS -- loading cloves, november 1521", fill=RED)
d.text((16, 580), "two ships left: TRINIDAD and VICTORIA -- Magellan dead at Mactan", fill=RED)

im.save(os.environ["OUT_RAW"])
