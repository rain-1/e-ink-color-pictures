# Night — "Pier 86". Palette: black, blue, red (beacon).
# Enterprise's last berth: a pavilion on the flight deck of the retired carrier Intrepid,
# on the Hudson at Manhattan's West Side. Mostly black, per the house rule for night — the
# skyline and water in blue, and on the mast above the pavilion, the day's light comes home:
# a single red beacon, the same signal that opened the day at Palmdale.
import os
import numpy as np
from PIL import Image, ImageDraw

W, H = 400, 600
BLK, BLU, RED = (0, 0, 0), (0x12, 0x3D, 0xB0), (0xE0, 0x1B, 0x24)
rng = np.random.default_rng(20080410)

im = Image.new("RGB", (W, H), BLK)
d = ImageDraw.Draw(im)

# a few faint stars, high up — sparse, so black stays dominant
for _ in range(35):
    x, y = int(rng.integers(0, W)), int(rng.integers(0, 130))
    d.point((x, y), fill=BLU)

# Manhattan skyline: black towers with a scatter of small blue lit windows, silhouetted
# against nothing (the sky is already black) — so only the windows carry the shape
SKY_BASE = 330
x = 0
towers = []
while x < W:
    tw = int(rng.integers(20, 46))
    th = int(rng.integers(60, 230))
    towers.append((x, tw, th))
    x += tw + int(rng.integers(0, 3))
for x, tw, th in towers:
    top = SKY_BASE - th
    d.line((x + 2, top, x + tw - 2, top), fill=BLU, width=2)   # roofline, so the top reads
    for wy in range(top + 10, SKY_BASE - 6, 10):
        for wx in range(x + 4, x + tw - 4, 8):
            if rng.random() < 0.6:
                d.rectangle((wx, wy, wx + 2, wy + 4), fill=BLU)

# the river: black, with vertical blue reflection streaks under the lit towers
d.rectangle((0, SKY_BASE, W, H), fill=BLK)
for x, tw, th in towers:
    if th > 130 and rng.random() < 0.7:
        rx = x + tw // 2
        for dy in range(0, 60, 4):
            if rng.random() < 0.6:
                d.line((rx - 1, SKY_BASE + dy, rx + 1, SKY_BASE + dy + 2), fill=BLU, width=1)

# the Intrepid's flight deck, a long low black hull-and-deck mass across the foreground,
# breaking the water's edge
DECK_Y = 430
d.polygon([(-10, DECK_Y + 40), (30, DECK_Y - 10), (370, DECK_Y - 22), (410, DECK_Y + 24),
           (410, DECK_Y + 60), (-10, DECK_Y + 60)], fill=BLK)
d.line((30, DECK_Y - 10, 370, DECK_Y - 22), fill=BLU, width=1)   # deck edge catches a little light
# island superstructure, aft
d.rectangle((300, DECK_Y - 70, 340, DECK_Y - 18), fill=BLK)
d.line((300, DECK_Y - 70, 300, DECK_Y - 18), fill=BLU, width=1)
for wy in range(DECK_Y - 64, DECK_Y - 24, 12):
    d.point((312, wy), fill=BLU)
    d.point((326, wy), fill=BLU)

# the pavilion: a translucent tent over the orbiter, drawn as a blue-rimmed dark shape so it
# reads as glass/fabric rather than solid hull
PX, PY = 160, DECK_Y - 20
pav = [(PX - 110, PY), (PX - 70, PY - 58), (PX + 90, PY - 58), (PX + 120, PY), (PX - 110, PY)]
d.polygon(pav, fill=BLK)
d.line([(PX - 110, PY), (PX - 70, PY - 58)], fill=BLU, width=1)
d.line([(PX - 70, PY - 58), (PX + 90, PY - 58)], fill=BLU, width=1)
d.line([(PX + 90, PY - 58), (PX + 120, PY)], fill=BLU, width=1)
for rx in range(-60, 90, 20):     # rib lines of the pavilion frame, up to the ridge
    d.line((PX + rx, PY - 2, PX + rx, PY - 56 + abs(rx) * 0.05), fill=BLU, width=1)

# the orbiter's tail fin, just visible above the pavilion ridge — the only part of Enterprise
# herself that shows, dark against the last blue of the sky glow
d.polygon([(PX - 6, PY - 55), (PX + 14, PY - 55), (PX + 26, PY - 112), (PX + 8, PY - 112)], fill=BLK)
d.line([(PX - 6, PY - 55), (PX + 8, PY - 112)], fill=BLU, width=1)

# the mast, above the tail fin, and on it — the day's light comes home
mx, my = PX + 17, PY - 112
d.line((mx, PY - 55, mx, my), fill=BLK, width=2)
d.line((mx, PY - 55, mx, my), fill=BLU, width=1)
d.ellipse((mx - 3, my - 3, mx + 3, my + 3), fill=RED)
d.ellipse((mx - 7, my - 7, mx + 7, my + 7), outline=RED, width=1)

d.text((14, H - 30), "PIER 86, NEW YORK", fill=BLU)
d.text((14, H - 16), "Intrepid Sea, Air & Space Museum", fill=BLU)

im.save(os.environ["OUT_RAW"])
