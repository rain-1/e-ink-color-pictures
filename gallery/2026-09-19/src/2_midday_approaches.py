"""Midday: a working nautical chart of an invented harbour approach, drawn
with the real conventions -- yellow land with height contours, a green
drying line, blue shallow-water stipple and depth contours, soundings in
metres, a sectored light, lateral buoys (red cans to port, green cones to
starboard), a wreck, an anchorage, a signal station (the day's flag), a
32-point rose with rhumb lines, a cartouche, and a graduated neatline."""
import math
import os
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFont

S = 4
W, H = 400 * S, 600 * S
K = (0, 0, 0); Wt = (255, 255, 255); R = (0xE0, 0x1B, 0x24)
Y = (0xF5, 0xD4, 0x00); B = (0x12, 0x3D, 0xB0); G = (0x1E, 0x9B, 0x3C)
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
random.seed(1919)

def P(x, y):  # 1x chart units -> supersampled pixels
    return (x * S, y * S)

# ---------------------------------------------------------------- geometry
coast = [(0, 0), (240, 0), (250, 30), (230, 60), (260, 90), (280, 130), (255, 160),
         (275, 200), (250, 230), (210, 240), (190, 270), (150, 255), (120, 280),
         (90, 265), (60, 290), (30, 270), (0, 285)]
island = [(305, 300), (335, 292), (362, 312), (356, 345), (330, 360), (300, 345), (292, 320)]
ROSE = (170, 450); ROSE_R = 78
LIGHT = (272, 204)

img = Image.new("RGB", (W, H), Wt)
d = ImageDraw.Draw(img)

# rhumb lines first, so everything else prints over them
for k in range(16):
    a = k * math.pi / 8
    d.line([P(*ROSE), P(ROSE[0] + 900 * math.sin(a), ROSE[1] - 900 * math.cos(a))],
           fill=K, width=int(1.2 * S))

# distance field to both coastlines (in 1x units) and a land mask
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
xx /= S; yy /= S
dist = np.full((H, W), 1e9, dtype=np.float32)
for poly in (coast, island):
    n = len(poly)
    for i in range(n):
        ax, ay = poly[i]; bx, by = poly[(i + 1) % n]
        if poly is coast and i == n - 1:
            continue  # the coast's closing edge runs along the frame, not water
        vx, vy = bx - ax, by - ay
        L2 = vx * vx + vy * vy
        t = np.clip(((xx - ax) * vx + (yy - ay) * vy) / L2, 0, 1)
        dist = np.minimum(dist, np.hypot(xx - (ax + t * vx), yy - (ay + t * vy)))
mask = Image.new("L", (W, H), 0)
md = ImageDraw.Draw(mask)
md.polygon([P(*p) for p in coast], fill=255)
md.polygon([P(*p) for p in island], fill=255)
land = np.asarray(mask) > 0

arr = np.asarray(img).copy()
water = ~land
# land, with height contours
arr[land] = Y
relief = dist + 3.0 * np.sin(xx / 11.0) + 2.5 * np.cos(yy / 9.0) + 1.5 * np.sin((xx + yy) / 6.0)
for c in (10, 22, 34, 46, 58):
    arr[land & (np.abs(relief - c) < 0.6)] = K
# drying line hugging the shore, then dashed depth contours
arr[water & (dist < 4.5)] = G
dash = ((xx + yy) // 7).astype(int) % 3 != 0
for c in (18, 40, 70):
    arr[water & (np.abs(dist - c) < 0.6) & dash] = B
img = Image.fromarray(arr)
d = ImageDraw.Draw(img)

# shallow-water stipple: dense by the shore, thinning seaward
for gx in range(0, 400, 5):
    for gy in range(0, 600, 5):
        x = gx + random.uniform(-2, 2); y = gy + random.uniform(-2, 2)
        xi, yi = int(x * S), int(y * S)
        if not (0 <= xi < W and 0 <= yi < H) or land[yi, xi]:
            continue
        dd = dist[yi, xi]
        if dd < 6 or dd > 42:
            continue
        if random.random() < (1 - (dd - 6) / 36) ** 1.6:
            r = 1.1 * S
            d.ellipse([xi - r, yi - r, xi + r, yi + r], fill=B)

# coastline ink
d.line([P(*p) for p in coast[1:]], fill=K, width=int(1.8 * S), joint="curve")
d.line([P(*p) for p in island] + [P(*island[0])], fill=K, width=int(1.8 * S), joint="curve")

# ---------------------------------------------------------------- soundings
sf = ImageFont.truetype(SERIF, 11 * S)
sub = ImageFont.truetype(SERIF, 8 * S)
placed = []
def clear_of(x, y):
    if math.hypot(x - ROSE[0], y - ROSE[1]) < ROSE_R + 14: return False
    if 236 <= x <= 392 and 522 <= y <= 592: return False          # cartouche
    if math.hypot(x - LIGHT[0], y - LIGHT[1]) < 26: return False
    if 40 <= x <= 95 and 300 <= y <= 600: return False             # channel
    return all(math.hypot(x - px, y - py) > 26 for px, py in placed)
for _ in range(900):
    x, y = random.uniform(14, 386), random.uniform(14, 586)
    xi, yi = int(x * S), int(y * S)
    if land[yi, xi] or dist[yi, xi] < 9 or not clear_of(x, y):
        continue
    depth = dist[yi, xi] * 0.42 + random.uniform(-1.5, 1.5)
    if depth < 1: depth = 1 + random.random()
    whole = int(depth); frac = int((depth - whole) * 10)
    d.text(P(x, y), str(whole), font=sf, fill=K, anchor="rs")
    if depth < 20:
        d.text(P(x + 1, y + 2), str(frac), font=sub, fill=K, anchor="ls")
    placed.append((x, y))

# ---------------------------------------------------------------- symbols
def buoy_can(x, y):      # port hand: red can
    d.rectangle([*P(x - 4, y - 12), *P(x + 4, y - 2)], fill=R, outline=K, width=int(0.8 * S))
    d.line([P(x, y - 2), P(x, y)], fill=K, width=int(1.2 * S))
    d.ellipse([*P(x - 1.6, y - 1.6), *P(x + 1.6, y + 1.6)], fill=K)
def buoy_cone(x, y):     # starboard hand: green cone
    d.polygon([P(x - 5, y - 2), P(x + 5, y - 2), P(x, y - 13)], fill=G, outline=K)
    d.ellipse([*P(x - 1.6, y - 1.6), *P(x + 1.6, y + 1.6)], fill=K)
def wreck(x, y):
    d.line([P(x - 9, y), P(x + 9, y)], fill=K, width=int(1.5 * S))
    for k in (-5, 0, 5):
        d.line([P(x + k, y - 6), P(x + k, y + 6)], fill=K, width=int(1.5 * S))
    d.line([P(x - 9, y + 6), P(x + 9, y + 6)], fill=K, width=int(1.5 * S))
def anchor(x, y):
    d.line([P(x, y - 10), P(x, y + 8)], fill=K, width=int(1.6 * S))
    d.line([P(x - 6, y - 5), P(x + 6, y - 5)], fill=K, width=int(1.6 * S))
    d.arc([*P(x - 8, y - 4), *P(x + 8, y + 10)], 20, 160, fill=K, width=int(1.6 * S))
    d.ellipse([*P(x - 2.5, y - 13), *P(x + 2.5, y - 8)], outline=K, width=int(1.2 * S))

# the buoyed channel into harbour
chan = [(66, 582), (64, 500), (70, 420), (78, 340), (84, 300)]
d.line([P(*p) for p in chan], fill=K, width=int(0.8 * S))
for i in range(4):
    x0, y0 = chan[i]; x1, y1 = chan[i + 1]
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    buoy_can(mx - 14, my)
    buoy_cone(mx + 14, my)
wreck(346, 262)
anchor(340, 470)
d.text(P(352, 470), "Anch.", font=sub, fill=K, anchor="lm")

# the light and its sectors
lx, ly = LIGHT
d.ellipse([*P(lx - 3, ly - 3), *P(lx + 3, ly + 3)], fill=K)
for k in range(8):
    a = k * math.pi / 4
    d.line([P(lx + 4 * math.cos(a), ly + 4 * math.sin(a)),
            P(lx + 10 * math.cos(a), ly + 10 * math.sin(a))], fill=K, width=int(1.2 * S))
d.ellipse([*P(lx - 5, ly - 5), *P(lx + 5, ly + 5)], fill=R)
SR = 62
d.arc([*P(lx - SR, ly - SR), *P(lx + SR, ly + SR)], 5, 75, fill=R, width=int(2.4 * S))
d.arc([*P(lx - SR, ly - SR), *P(lx + SR, ly + SR)], 75, 150, fill=K, width=int(1.2 * S))
for ang in (5, 75, 150):
    a = math.radians(ang)
    d.line([P(lx + 12 * math.cos(a), ly + 12 * math.sin(a)),
            P(lx + SR * math.cos(a), ly + SR * math.sin(a))], fill=K, width=int(0.7 * S))
d.text(P(lx + 14, ly - 18), "Fl(2) 10s 18M", font=sub, fill=K, anchor="lm")

# signal station on the headland: a mast and flag, and "SS"
sx, sy = 236, 182
d.line([P(sx, sy), P(sx, sy - 22)], fill=K, width=int(1.6 * S))
d.polygon([P(sx, sy - 22), P(sx + 13, sy - 18), P(sx, sy - 13)], fill=R, outline=K)
d.text(P(sx + 4, sy - 2), "SS", font=sub, fill=K, anchor="lm")

# harbour town: blocks, a church, a pier
for bx, by, bw, bh in [(66, 238, 10, 8), (80, 236, 8, 10), (94, 240, 12, 8), (110, 246, 8, 8),
                       (72, 250, 9, 7), (88, 252, 10, 8), (58, 226, 8, 8), (100, 228, 9, 7)]:
    d.rectangle([*P(bx, by), *P(bx + bw, by + bh)], fill=K)
d.line([P(84, 224), P(84, 214)], fill=K, width=int(1.4 * S))
d.line([P(80, 218), P(88, 218)], fill=K, width=int(1.4 * S))
d.line([P(86, 268), P(84, 296)], fill=K, width=int(2.2 * S))
d.text(P(70, 210), "PORT ROGER", font=sub, fill=K, anchor="lm")
d.text(P(300, 372), "Gull I.", font=sub, fill=K, anchor="mm")
d.text(P(150, 120), "CAPE HALYARD", font=ImageFont.truetype(SERIF, 10 * S), fill=K, anchor="mm")
# a few tree symbols and a spot height on the land
for tx, ty in [(40, 60), (70, 90), (120, 40), (170, 70), (60, 150), (140, 180), (200, 140), (30, 200)]:
    d.ellipse([*P(tx - 2.5, ty - 2.5), *P(tx + 2.5, ty + 2.5)], outline=K, width=int(1 * S))
    d.line([P(tx, ty + 2.5), P(tx, ty + 6)], fill=K, width=int(1 * S))
d.ellipse([*P(95, 128), *P(99, 132)], fill=K)
d.text(P(102, 130), "• 114", font=sub, fill=K, anchor="lm")

# ---------------------------------------------------------------- compass rose
cx, cy = ROSE
for rr, w in ((ROSE_R, 1.6), (ROSE_R - 7, 0.8), (ROSE_R * 0.55, 1.0)):
    d.ellipse([*P(cx - rr, cy - rr), *P(cx + rr, cy + rr)], outline=K, width=int(w * S))
for deg in range(0, 360, 2):
    a = math.radians(deg)
    L = 7 if deg % 10 == 0 else 3.5
    r0, r1 = ROSE_R - 7, ROSE_R - 7 - L
    d.line([P(cx + r0 * math.sin(a), cy - r0 * math.cos(a)),
            P(cx + r1 * math.sin(a), cy - r1 * math.cos(a))], fill=K, width=int((1.1 if L > 4 else 0.7) * S))
def point(ang, length, half, fill_dark):
    ca, sa = math.cos(ang), math.sin(ang)
    tip = (cx + length * sa, cy - length * ca)
    l = (cx + half * math.sin(ang - math.pi / 2), cy - half * math.cos(ang - math.pi / 2))
    r = (cx + half * math.sin(ang + math.pi / 2), cy - half * math.cos(ang + math.pi / 2))
    d.polygon([P(*tip), P(*l), P(cx, cy)], fill=K if fill_dark else Wt, outline=K)
    d.polygon([P(*tip), P(*r), P(cx, cy)], fill=Wt if fill_dark else K, outline=K)
for k in range(16):  # sixteen half-points
    point(k * math.pi / 8 + math.pi / 16, ROSE_R * 0.36, 3, True)
for k in range(8):   # eight intercardinal
    point(k * math.pi / 4 + math.pi / 8, ROSE_R * 0.5, 5, True)
for k in range(4):   # ordinal
    point(k * math.pi / 2 + math.pi / 4, ROSE_R * 0.62, 6.5, True)
for k in range(4):   # cardinal
    point(k * math.pi / 2, ROSE_R * 0.9, 8, True)
d.ellipse([*P(cx - 3, cy - 3), *P(cx + 3, cy + 3)], fill=K)
cf = ImageFont.truetype(SERIF, 14 * S)
for lbl, (ox, oy) in zip("NESW", [(0, -ROSE_R - 10), (ROSE_R + 10, 0), (0, ROSE_R + 10), (-ROSE_R - 10, 0)]):
    d.text(P(cx + ox, cy + oy), lbl, font=cf, fill=K, anchor="mm")
# fleur at north
d.polygon([P(cx, cy - ROSE_R + 4), P(cx - 5, cy - ROSE_R + 14), P(cx + 5, cy - ROSE_R + 14)], fill=R)

# ---------------------------------------------------------------- cartouche
d.rectangle([*P(238, 524), *P(390, 590)], fill=Wt, outline=K, width=int(1.6 * S))
d.rectangle([*P(241, 527), *P(387, 587)], outline=K, width=int(0.7 * S))
d.text(P(314, 538), "PIRATE'S REACH", font=ImageFont.truetype(SERIF, 12 * S), fill=K, anchor="mm")
d.text(P(314, 551), "Approaches to Port Roger", font=sub, fill=K, anchor="mm")
d.text(P(314, 562), "Soundings in metres  ·  1:25 000", font=sub, fill=K, anchor="mm")
for i in range(4):  # scale bar
    d.rectangle([*P(262 + i * 26, 572), *P(288 + i * 26, 577)], fill=K if i % 2 == 0 else Wt, outline=K)
d.text(P(262, 584), "0", font=sub, fill=K, anchor="mm")
d.text(P(366, 584), "1 M", font=sub, fill=K, anchor="mm")

# ---------------------------------------------------------------- neatline
d.rectangle([*P(6, 6), *P(394, 594)], outline=K, width=int(1.6 * S))
d.rectangle([*P(10, 10), *P(390, 590)], outline=K, width=int(1.0 * S))
for i, x in enumerate(range(10, 390, 20)):
    if i % 2 == 0:
        d.rectangle([*P(x, 6.8), *P(min(x + 20, 390), 9.8)], fill=K)
        d.rectangle([*P(x, 590.2), *P(min(x + 20, 390), 593.2)], fill=K)
for i, y in enumerate(range(10, 590, 20)):
    if i % 2 == 0:
        d.rectangle([*P(6.8, y), *P(9.8, min(y + 20, 590))], fill=K)
        d.rectangle([*P(390.2, y), *P(393.2, min(y + 20, 590))], fill=K)

def ink_downsample(im, s):
    """Downsample so that any pixel with a fair share of ink stays black
    (hairlines survive as 1px black instead of fading to grey)."""
    a = np.asarray(im).astype(np.float32)
    h, w, _ = a.shape
    a = a.reshape(h // s, s, w // s, s, 3)
    dark = a.max(-1) < 90
    frac = dark.mean(axis=(1, 3))
    light = np.where(dark[..., None], 0, a).sum(axis=(1, 3))
    cnt = np.maximum((~dark).sum(axis=(1, 3)), 1)[..., None]
    out = light / cnt
    out[frac >= 0.28] = 0
    return Image.fromarray(out.astype(np.uint8), "RGB")

ink_downsample(img, S).save(os.environ["OUT_RAW"])
