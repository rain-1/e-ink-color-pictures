# Midday -- "Off Patagonia, the coast run south". Palette: blue, white.
# An engraved chart plate: a 32-point compass rose, a rhumb line running the fleet
# south along the coast, and the wreck of the Santiago marked where she was lost
# in a river mouth, April 1520 -- five ships down to four.
import os, math
from PIL import Image, ImageDraw
import sys
sys.path.insert(0, os.path.dirname(__file__))
from _ship import ship

W, H = 400, 600
BLU, WHT = (18, 61, 176), (255, 255, 255)
im = Image.new("RGB", (W, H), WHT)
d = ImageDraw.Draw(im)

CX, CY, R = 200, 185, 128

# --- outer engraved rings ---
for rr in (R + 18, R + 24):
    d.ellipse((CX - rr, CY - rr, CX + rr, CY + rr), outline=BLU, width=1)

# --- compass rose: 32 points, alternating long/medium/short, N marked ---
for i in range(32):
    ang = math.radians(i * 11.25 - 90)
    if i % 8 == 0:
        length, w = R, 2
    elif i % 4 == 0:
        length, w = R * 0.82, 1
    elif i % 2 == 0:
        length, w = R * 0.62, 1
    else:
        length, w = R * 0.46, 1
    x1, y1 = CX + length * math.cos(ang), CY + length * math.sin(ang)
    d.line((CX, CY, x1, y1), fill=BLU, width=w)
# tick ring
for i in range(64):
    ang = math.radians(i * 5.625 - 90)
    r0, r1 = R + 4, R + (10 if i % 4 == 0 else 6)
    d.line((CX + r0 * math.cos(ang), CY + r0 * math.sin(ang),
            CX + r1 * math.cos(ang), CY + r1 * math.sin(ang)), fill=BLU, width=1)

# the eight main direction diamonds where long spokes meet the ring
for i in range(0, 32, 8):
    ang = math.radians(i * 11.25 - 90)
    x1, y1 = CX + R * math.cos(ang), CY + R * math.sin(ang)
    s = 7
    d.polygon([(x1, y1 - s), (x1 + s, y1), (x1, y1 + s), (x1 - s, y1)], outline=BLU, width=1)

# N fleur, drawn a little larger, pointing to true north (up)
nx, ny = CX, CY - R
d.polygon([(nx, ny - 26), (nx - 9, ny + 4), (nx, ny - 6), (nx + 9, ny + 4)], fill=BLU)
d.text((CX - 4, CY - R - 42), "N", fill=BLU)

# centre flower
d.ellipse((CX - 5, CY - 5, CX + 5, CY + 5), outline=BLU, width=1)

# --- the coast: a ragged line down the left side (Patagonia), hatched on the land side ---
coast = [(0, 40), (30, 130), (18, 230), (44, 340), (26, 430), (50, 540), (30, 600)]
d.line(coast, fill=BLU, width=2)
for i in range(len(coast) - 1):
    (x0, y0), (x1, y1) = coast[i], coast[i + 1]
    for t in range(0, 10):
        u = t / 10
        lx, ly = x0 + (x1 - x0) * u, y0 + (y1 - y0) * u
        d.line((lx, ly, lx - 14, ly + 3), fill=BLU, width=1)

# --- rhumb line the fleet is following: south-south-west, past the rose, off the sheet ---
path = [(CX + 20, CY + R + 30), (150, 430), (118, 490), (95, 545)]
for i in range(len(path) - 1):
    x0, y0 = path[i]; x1, y1 = path[i + 1]
    L = math.hypot(x1 - x0, y1 - y0); n = int(L / 10)
    for k in range(n):
        t0, t1 = k / n, (k + 0.6) / n
        d.line((x0 + (x1 - x0) * t0, y0 + (y1 - y0) * t0,
                x0 + (x1 - x0) * t1, y0 + (y1 - y0) * t1), fill=BLU, width=1)

# --- four ships, in a line down the rhumb, shrinking with distance ---
stops = [(path[0][0], path[0][1] + 4, 42), (150, 430, 30), (120, 486, 20), (98, 528, 13)]
for x, y, size in stops:
    ship(d, x, y, size, hull=BLU, sail=BLU, facing=-1, detail=size > 20)

# --- the wreck of the Santiago: a small X and broken mast, on the coast ---
wx, wy = 58, 400
d.line((wx - 8, wy - 8, wx + 8, wy + 8), fill=BLU, width=2)
d.line((wx - 8, wy + 8, wx + 8, wy - 8), fill=BLU, width=2)
d.line((wx + 2, wy - 2, wx + 2, wy - 18), fill=BLU, width=1)
d.text((wx + 10, wy - 5), "SANTIAGO", fill=BLU)
d.text((wx + 10, wy + 6), "wrecked, rio santa cruz", fill=BLU)

d.text((16, 566), "OFF PATAGONIA -- the coast run south, april 1520", fill=BLU)
d.text((16, 580), "four ships remain: TRINIDAD SAN ANTONIO CONCEPCION VICTORIA", fill=BLU)

im.save(os.environ["OUT_RAW"])
