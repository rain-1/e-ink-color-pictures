# Midday — after "Several Circles" (1926), Kandinsky's crowded field of coloured
# discs on black. Palette exception for the day: black ground (dominant) with
# red, yellow, blue, green accents — the one piece allowed the full accent set,
# because the subject itself is the riot of circles.
import os, math
from PIL import Image, ImageDraw
import numpy as np
W, H = 400, 600
BLK = (0, 0, 0)
COLS = [(0xE0, 0x1B, 0x24), (0xF5, 0xD4, 0x00), (0x12, 0x3D, 0xB0), (0x1E, 0x9B, 0x3C), (255, 255, 255)]
rng = np.random.default_rng(1866)
im = Image.new("RGB", (W, H), BLK)
d = ImageDraw.Draw(im)

circles = []
# a few large anchor circles, biased toward the upper two-thirds
for _ in range(6):
    r = rng.integers(55, 105)
    x = rng.integers(r, W - r)
    y = rng.integers(r, int(H * 0.7))
    circles.append((x, y, r))
# a scatter of smaller ones filling the rest, including low into the night-adjacent foot
for _ in range(16):
    r = rng.integers(14, 45)
    x = rng.integers(r, W - r)
    y = rng.integers(r, H - r)
    circles.append((x, y, r))
circles.sort(key=lambda c: -c[2])  # biggest first, so small ones sit on top

for i, (x, y, r) in enumerate(circles):
    col = COLS[i % len(COLS)]
    d.ellipse((x - r, y - r, x + r, y + r), fill=col)
    # a concentric ring one size down, in a second colour — Kandinsky's circles
    # are rarely flat discs, they carry a ring or a second field inside
    col2 = COLS[(i + 2) % len(COLS)]
    if r > 22:
        r2 = int(r * 0.55)
        d.ellipse((x - r2, y - r2, x + r2, y + r2), fill=col2)
    if r > 60:
        r3 = int(r * 0.22)
        d.ellipse((x - r3, y - r3, x + r3, y + r3), fill=BLK)

# a few thin lines of tension between nearby large circles (Kandinsky's grid remnants)
big = [c for c in circles if c[2] > 55]
for i in range(len(big) - 1):
    x0, y0, _ = big[i]
    x1, y1, _ = big[i + 1]
    d.line((x0, y0, x1, y1), fill=(255, 255, 255), width=1)

im.save(os.environ["OUT_RAW"])
