# Afternoon — "Der Gelbe Klang" (The Yellow Sound), Kandinsky's 1912 stage piece,
# and his synesthesia more broadly: yellow as a trumpet blast, sharp and advancing.
# A diagonal eruption of jagged triangles from upper right to lower left, one black
# circle at the point of impact (the note landing). Palette: yellow, red, black.
import os, math
from PIL import Image, ImageDraw
import numpy as np
W, H = 400, 600
YEL, RED, BLK = (0xF5, 0xD4, 0x00), (0xE0, 0x1B, 0x24), (0, 0, 0)
rng = np.random.default_rng(191)
im = Image.new("RGB", (W, H), YEL)
d = ImageDraw.Draw(im)

# the impact point — low-left, where the circle motif lands
ix, iy = 120, 460

# jagged red shards radiating from the impact, longest toward the upper right
for a_deg in range(-200, 20, 7):
    a = math.radians(a_deg)
    length = 620 + rng.uniform(-40, 40)
    spread = math.radians(2.6)
    x1 = ix + length * math.cos(a - spread)
    y1 = iy + length * math.sin(a - spread)
    x2 = ix + length * math.cos(a + spread)
    y2 = iy + length * math.sin(a + spread)
    if rng.random() < 0.55:
        d.polygon([(ix, iy), (x1, y1), (x2, y2)], fill=RED)

# black jagged shards interleaved, shorter, giving the burst a hard edge
for a_deg in range(-200, 20, 11):
    a = math.radians(a_deg)
    length = 340 + rng.uniform(-30, 60)
    spread = math.radians(1.6)
    x1 = ix + length * math.cos(a - spread)
    y1 = iy + length * math.sin(a - spread)
    x2 = ix + length * math.cos(a + spread)
    y2 = iy + length * math.sin(a + spread)
    d.polygon([(ix, iy), (x1, y1), (x2, y2)], fill=BLK)

# a few short black ticks scattered near the top, sound dissipating into the field
for _ in range(40):
    x = rng.uniform(0, W)
    y = rng.uniform(0, iy - 150)
    if rng.random() < (1 - y / iy):
        L = rng.uniform(8, 22)
        ang = rng.uniform(0, math.pi)
        d.line((x, y, x + L * math.cos(ang), y + L * math.sin(ang)), fill=BLK, width=2)

# the note itself: a black circle at the point of impact, the day's motif
d.ellipse((ix - 34, iy - 34, ix + 34, iy + 34), fill=BLK)
d.ellipse((ix - 14, iy - 14, ix + 14, iy + 14), fill=YEL)

im.save(os.environ["OUT_RAW"])
