"""Midday: a fathometer/chart plate, green ink on a black instrument ground.
Dominant black -- the open water the rose and soundings sit in. Coastline is
a headland along the top edge only. One pennant marks a fixed buoy, the
day's small recurring motif."""
import math
import os
import random

from PIL import Image, ImageDraw

S = 4  # supersample for clean lines before render.py downsamples
W, H = 400 * S, 600 * S
GREEN = (0x1E, 0x9B, 0x3C)
BLACK = (0x00, 0x00, 0x00)

img = Image.new("RGB", (W, H), BLACK)
d = ImageDraw.Draw(img)


def line(a, b, w):
    d.line([a, b], fill=GREEN, width=w)


# --- coastline: a low jagged headland tucked along the top edge only ---
edge = [(400, 0), (400, 190), (350, 170), (368, 120), (322, 140), (338, 95),
        (295, 115), (262, 75), (222, 100), (196, 65), (168, 95), (136, 72),
        (104, 105), (70, 85), (36, 115), (0, 95), (0, 0)]
pts = [(x * S, y * S) for x, y in edge]
d.polygon(pts, fill=GREEN)

# short cliff hatches just under the shoreline, not full-width lines
for i in range(1, len(edge) - 1):
    x, y = edge[i]
    d.line([(x * S, y * S), ((x - 6) * S, (y + 16) * S)], fill=BLACK, width=int(1.5 * S))

# --- compass rose, centred in the open water below ---
cx, cy = 200 * S, 430 * S
r_out = 140 * S
for k in range(32):
    ang = k * math.pi / 16
    length = r_out if k % 8 == 0 else (r_out * 0.62 if k % 4 == 0 else r_out * 0.34)
    w = int((6 if k % 8 == 0 else 3) * S)
    x = cx + length * math.sin(ang)
    y = cy - length * math.cos(ang)
    line((cx, cy), (x, y), w)
for rr in (r_out, r_out * 0.62):
    d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=GREEN, width=int(2 * S))

# bold triangle at true north
tip = (cx, cy - r_out - 26 * S)
d.polygon([tip, (cx - 20 * S, cy - r_out + 6 * S), (cx + 20 * S, cy - r_out + 6 * S)], fill=GREEN)

# --- depth soundings scattered in the open water ---
random.seed(19)
for _ in range(40):
    x = random.uniform(10, 390) * S
    y = random.uniform(240, 585) * S
    if (x - cx) ** 2 + (y - cy) ** 2 < (r_out * 0.72) ** 2:
        continue
    depth = random.choice([1, 1, 2, 2, 3])  # shallower = bigger mark
    rad = (2 + depth) * S
    d.ellipse([x - rad, y - rad, x + rad, y + rad], fill=GREEN)
    if depth == 1:  # shoal warning ring around the shallowest marks
        d.ellipse([x - rad * 2.4, y - rad * 2.4, x + rad * 2.4, y + rad * 2.4],
                   outline=GREEN, width=int(1.5 * S))

# --- one pennant marking the day's fixed buoy, clear of the rose ---
bx, by = 335 * S, 320 * S
d.line([(bx, by), (bx, by - 55 * S)], fill=GREEN, width=int(3 * S))
d.polygon([(bx, by - 55 * S), (bx + 32 * S, by - 44 * S), (bx, by - 33 * S)], fill=GREEN)
d.ellipse([bx - 6 * S, by, bx + 6 * S, by + 12 * S], fill=GREEN)

img = img.resize((400, 600), Image.LANCZOS)
img.save(os.environ["OUT_RAW"])
