"""Irworobongdo — Sun, Moon and Five Peaks, after the Joseon throne screens.
Peaks as nested contour bands, pines with scaled red trunks, two waterfalls, a scaled sea."""
import math, random
import numpy as np
from PIL import Image, ImageDraw
from kit import *

random.seed(9)
img = Image.new("RGB", (W, H), B)
d = ImageDraw.Draw(img)
a = to_arr(img)

# sky: blue, lifting to white-screened band just above the peaks (dawn)
yy = np.arange(H)[:, None] * np.ones((1, W))
sky = np.ones((H, W), bool)
screen(a, sky, B, WH, np.clip((yy - 170) / 260, 0, 1) * 0.55)
img = Image.fromarray(a); d = ImageDraw.Draw(img)

# sun (right) and moon (left)
def disc(cx, cy, r, fill, ring):
    for k, col in enumerate(ring):
        rr = r + 10 - k * 4
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=col)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill)
disc(312, 92, 34, R, [WH, Y, K])
disc(88, 92, 30, WH, [Y, WH, K])
# sun rays as fine ticks
for i in range(48):
    t = i / 48 * 2 * math.pi
    r0, r1 = 48, 56 + (6 if i % 2 else 0)
    d.line([(312 + r0 * math.cos(t), 92 + r0 * math.sin(t)), (312 + r1 * math.cos(t), 92 + r1 * math.sin(t))], fill=Y, width=2)
# moon craters
for cx, cy, r in [(80, 84, 6), (97, 101, 4), (92, 78, 3), (74, 103, 3)]:
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(200, 200, 200) if False else Y, width=1)

def peak_poly(cx, base, half, top, n=60, bump=0.0, seed=0):
    rnd = random.Random(seed)
    pts = []
    for i in range(n + 1):
        u = -1 + 2 * i / n
        h = (1 - abs(u) ** 1.6) ** 1.3
        h += bump * math.sin(u * 9 + seed) * (1 - abs(u))
        pts.append((cx + u * half, base - h * (base - top)))
    return pts

def draw_peak(cx, base, half, top, seed, main=G, alt=B):
    bands = 9
    for k in range(bands):
        s = 1 - k / bands
        poly = peak_poly(cx, base, half * s, base - (base - top) * (0.15 + 0.85 * s) if k else top, bump=0.03, seed=seed)
        if k:
            poly = peak_poly(cx, base, half * s, top + (base - top) * (k / bands) * 0.55, bump=0.03, seed=seed + k)
        col = main if k % 2 == 0 else alt
        d.polygon(poly + [(cx + half * s, base + 2), (cx - half * s, base + 2)], fill=col)
        d.line(poly, fill=K, width=2)
        d.line([(x, y - 1) for x, y in poly[len(poly) // 4: 3 * len(poly) // 4]], fill=WH, width=1)
    # moss dots (cun) along the outer ridge
    for i, (x, y) in enumerate(peak_poly(cx, base, half, top, bump=0.03, seed=seed)):
        if i % 3 == 0 and 0 < i < 60:
            d.ellipse([x - 2, y + 2, x + 2, y + 6], fill=K)

base = 430
# far pair, near pair, then the centre peak — back to front
draw_peak(30, base, 95, 250, 1)
draw_peak(370, base, 95, 250, 2)
draw_peak(110, base + 10, 85, 215, 3, main=G, alt=Y)
draw_peak(290, base + 10, 85, 215, 4, main=G, alt=Y)
draw_peak(200, base + 20, 110, 150, 5)

# waterfalls: white ribbons in the gaps
for x0 in (152, 248):
    for k in range(5):
        xs = x0 + k * 3 - 6
        d.line([(xs, 300 + k * 6), (xs + (k % 2), base + 18)], fill=WH, width=2)
    d.line([(x0 - 8, 300), (x0 - 9, base + 18)], fill=K, width=1)
    d.line([(x0 + 9, 300), (x0 + 10, base + 18)], fill=K, width=1)

# sea: rows of fish-scale waves
seatop = base + 15
d.rectangle([0, seatop, W, H], fill=B)
row = 0
for y in range(seatop, H + 20, 13):
    off = (row % 2) * 13
    for x in range(-26 + off, W + 26, 26):
        d.arc([x - 13, y - 9, x + 13, y + 15], 180, 360, fill=WH, width=3)
        d.arc([x - 8, y - 2, x + 8, y + 14], 200, 340, fill=WH, width=1)
        d.point((x, y - 5), fill=WH)
    row += 1
# foam curls where falls meet the sea
for x0 in (152, 248):
    for k in range(6):
        r = 4 + k * 3
        d.arc([x0 - r, seatop - r // 2, x0 + r, seatop + r], 180, 360, fill=WH, width=2)
d.line([(0, seatop), (W, seatop)], fill=K, width=2)

def pine(x, ybase, height, lean, seed, flip=1):
    rnd = random.Random(seed)
    pts = []
    for i in range(13):
        t = i / 12
        pts.append((x + flip * lean * math.sin(t * 2.4) * height * 0.25, ybase - t * height))
    for k in range(len(pts) - 1):
        wdt = int(18 - 12 * k / len(pts))
        d.line([pts[k], pts[k + 1]], fill=R, width=wdt)
    # bark scales
    for k in range(1, len(pts) - 2):
        (x0, y0), (x1, y1) = pts[k], pts[k + 1]
        wdt = 9 - 6 * k / len(pts)
        for j in range(3):
            yy_ = y0 + (y1 - y0) * j / 3
            xx_ = x0 + (x1 - x0) * j / 3
            d.arc([xx_ - wdt, yy_ - 4, xx_ + wdt, yy_ + 4], 20, 160, fill=K, width=1)
    d.line(pts, fill=K, width=1)
    # branches with needle fans
    for k in range(4, len(pts), 2):
        bx, by = pts[k]
        side = 1 if (k // 2) % 2 else -1
        ex, ey = bx + side * rnd.randint(30, 52), by - rnd.randint(4, 16)
        d.line([(bx, by), (ex, ey)], fill=R, width=4)
        d.line([(bx, by), (ex, ey)], fill=K, width=1)
        fan(ex, ey, rnd.randint(20, 28), rnd)
    fan(*pts[-1], 26, rnd)

def fan(cx, cy, r, rnd):
    d.ellipse([cx - r, cy - r * 0.55, cx + r, cy + r * 0.45], fill=G, outline=K, width=2)
    for i in range(19):
        t = math.pi + i / 18 * math.pi
        d.line([(cx, cy + r * 0.25), (cx + r * 0.95 * math.cos(t), cy + r * 0.25 + r * 0.7 * math.sin(t))], fill=K, width=1)
    d.line([(cx - r * 0.8, cy + r * 0.3), (cx + r * 0.8, cy + r * 0.3)], fill=Y, width=1)

# rocks the pines stand on
for x0, flip in ((0, 1), (W, -1)):
    poly = [(x0, H), (x0, 470), (x0 + flip * 30, 455), (x0 + flip * 70, 480), (x0 + flip * 85, 530), (x0 + flip * 60, H)]
    d.polygon(poly, fill=Y, outline=K)
    for k in range(8):
        y = 480 + k * 15
        d.line([(x0 + flip * 5, y), (x0 + flip * (55 - k * 2), y + 6)], fill=K, width=1)
pine(28, 600, 330, 0.6, 11, 1)
pine(58, 600, 250, -0.4, 12, 1)
pine(372, 600, 330, 0.6, 13, -1)
pine(342, 600, 250, -0.4, 14, -1)

# frame
d.rectangle([0, 0, W - 1, H - 1], outline=K, width=6)
d.rectangle([7, 7, W - 8, H - 8], outline=R, width=2)
save(img)
