# Afternoon -- "A squall in the Strait of Magellan". Palette: green, black.
# The strait discovered late October 1520: a corridor of cliffs closing in, a storm
# overhead, three ships threading through while a fourth -- the San Antonio -- turns
# back for Spain in the night, deserting with much of the fleet's food.
import os, math, numpy as np
from PIL import Image, ImageDraw
import sys
sys.path.insert(0, os.path.dirname(__file__))
from _ship import ship

W, H = 400, 600
GRN, BLK = (30, 155, 60), (0, 0, 0)
rng = np.random.default_rng(15201031)
im = Image.new("RGB", (W, H), BLK)
d = ImageDraw.Draw(im)

HORIZON = 300

# --- cliffs closing in from both sides: solid green masses, a black channel between ---
left_ridge = [(0, 0), (55, 10), (95, 55), (78, 100), (135, 140), (108, 195), (150, HORIZON - 10)]
left_poly = left_ridge + [(0, HORIZON + 30)]
right_ridge = [(400, 0), (345, 15), (308, 60), (326, 108), (268, 145), (296, 198), (255, HORIZON - 10)]
right_poly = right_ridge + [(400, HORIZON + 30)]
d.polygon(left_poly, fill=GRN)
d.polygon(right_poly, fill=GRN)
# strata: black hatch lines following the slope
for ridge, side in ((left_ridge, 1), (right_ridge, -1)):
    for i in range(len(ridge) - 1):
        (px, py), (qx, qy) = ridge[i], ridge[i + 1]
        for t in np.linspace(0.2, 0.9, 4):
            lx, ly = px + (qx - px) * t, py + (qy - py) * t
            d.line((lx, ly, lx + side * 20, ly + 6), fill=BLK, width=2)
    d.line(ridge, fill=BLK, width=2)

# --- storm sky in the open channel: a jagged black-on-black gap holds green lightning + rain ---
bolt = [(212, 0), (188, 60), (206, 66), (172, 130), (192, 136), (168, 190)]
d.line(bolt, fill=GRN, width=3)
for _ in range(90):
    x = rng.integers(160, 250); y = rng.integers(0, 220)
    L = int(rng.integers(6, 16))
    d.line((x, y, x - L * 0.3, y + L), fill=GRN, width=1)

# --- water: black, green chevron chop, denser toward the foreground ---
d.rectangle((0, HORIZON, W, H), fill=BLK)
for y in range(HORIZON, H, 5):
    depth = (y - HORIZON) / (H - HORIZON)
    x = 0
    while x < W:
        w = int(6 + depth * 22)
        if rng.random() < 0.55 + depth * 0.3:
            d.line((x, y, x + w, y - 2), fill=GRN, width=1 if depth < 0.5 else 2)
            d.line((x + w, y - 2, x + 2 * w, y), fill=GRN, width=1 if depth < 0.5 else 2)
        x += 2 * w + int(rng.integers(2, 8))

# --- three ships threading the channel, receding into the bend ---
through = [(200, HORIZON + 150, 60), (188, HORIZON + 80, 36), (206, HORIZON + 30, 20)]
through.sort(key=lambda t: t[2])
for x, y, size in through:
    ship(d, x, y, size, hull=GRN, sail=GRN, facing=-1, detail=size > 24)

# --- the San Antonio, turning back, wake curling the other way ---
sx, sy, ssize = 92, HORIZON + 190, 46
ship(d, sx, sy, ssize, hull=GRN, sail=GRN, facing=1, detail=True)
d.line([(sx + 10, sy + 6), (sx + 38, sy - 4), (sx + 66, sy + 10), (sx + 92, sy - 2)], fill=GRN, width=1)

d.text((16, 566), "THE STRAIT OF MAGELLAN -- a squall, october-november 1520", fill=GRN)
d.text((16, 580), "three press on: TRINIDAD CONCEPCION VICTORIA -- SAN ANTONIO turns back", fill=GRN)

im.save(os.environ["OUT_RAW"])
