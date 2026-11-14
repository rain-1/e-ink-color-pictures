"""Midday — Coquelicots. The poppy field at Argenteuil (1873) drawn blade by blade:
every grass stem, every poppy and both walkers are individual marks, back to front."""
import math
import numpy as np
from PIL import Image, ImageDraw
from common import *

rng = np.random.default_rng(1873)
S = 2                                   # draw at 2x, quantise hard afterwards
img = Image.new("RGB", (W * S, H * S), WH)
d = ImageDraw.Draw(img)
yy, xx = np.mgrid[0:H * S, 0:W * S].astype(np.float32)

def L(pts, col, w=1):
    d.line([(x * S, y * S) for x, y in pts], fill=col, width=max(1, int(round(w * S))))
def E(cx, cy, rx, ry, col):
    d.ellipse([(cx - rx) * S, (cy - ry) * S, (cx + rx) * S, (cy + ry) * S], fill=col)
def P(pts, col):
    d.polygon([(x * S, y * S) for x, y in pts], fill=col)

def ridge(x):                            # the skyline of the field: rises to the left
    return 262 - 40 * math.exp(-((x - 60) / 150) ** 2) + 10 * math.sin(x / 70.0)

# ---- sky: engraved blue rules that thin out toward the horizon, cumulus left as paper ----
n = fbm(70, 5, 4)
n = np.asarray(Image.fromarray((n * 255).astype(np.uint8)).resize((W * S, H * S), Image.BICUBIC), np.float32) / 255
cloud = np.clip((n - 0.47 + 0.10 * np.sin(xx / (60 * S)) - 0.00035 * (yy / S - 110) ** 2 / 10) * 9, 0, 1)
a = np.asarray(img).copy()
tone = (0.85 - 0.5 * (yy / S) / 270) * (1 - cloud)            # how blue
period = 6 * S
phase = ((yy + 3 * S * np.sin(xx / (45 * S))) % period) / period
a[(phase < tone) & (yy < 280 * S)] = B
# cloud undersides: short blue hatch
shade = np.clip(cloud - np.roll(cloud, -9 * S, axis=0), 0, 1) * (cloud > 0.5)
hatch = (((xx + yy) % (5 * S)) < 1.4 * S)
a[(shade > 0.12) & hatch & (yy < 270 * S)] = B
img = Image.fromarray(a); d = ImageDraw.Draw(img)
# a noon sun, small and white-hot behind a ring
E(318, 62, 17, 17, Y); E(318, 62, 12, 12, WH)
for k in range(24):
    a_ = k * math.pi / 12
    L([(318 + 21 * math.cos(a_), 62 + 21 * math.sin(a_)), (318 + (27 + 4 * (k % 2)) * math.cos(a_), 62 + (27 + 4 * (k % 2)) * math.sin(a_))], Y, 1.5)

# ---- the tree line and the house ----
def tree(cx, base, h, w, dark=K):
    L([(cx, base), (cx, base - h * 0.5)], K, 2)
    for i in range(int(w * h / 9)):
        t = rng.random()
        px = cx + rng.normal(0, w * (0.25 + 0.5 * math.sin(math.pi * min(1, t + .15))))
        py = base - h * (0.25 + 0.75 * t)
        r = rng.uniform(2.2, 4.5)
        lit = (px - cx) < -w * 0.1 and rng.random() < 0.6
        E(px, py, r, r * 0.8, G if lit else dark)
    for i in range(int(w * h / 40)):
        px = cx + rng.normal(-w * 0.2, w * 0.3); py = base - h * rng.uniform(0.35, 0.95)
        E(px, py, 1.2, 1.0, Y)

for x in range(-10, W + 20, 9):
    if 232 < x < 290:
        continue
    b = ridge(x) + 3
    tree(x + rng.normal(0, 3), b, rng.uniform(26, 50) * (1.25 if x < 150 else 1.0), rng.uniform(9, 15))
tree(205, ridge(205) + 3, 88, 21)        # the big dark tree that anchors the painting
tree(30, ridge(30) + 3, 70, 18)
# house with red roof between the trees
hx, hy = 262, ridge(262) + 2
P([(hx - 24, hy), (hx - 24, hy - 22), (hx + 24, hy - 22), (hx + 24, hy)], WH)
P([(hx - 28, hy - 21), (hx - 18, hy - 37), (hx + 18, hy - 37), (hx + 28, hy - 21)], R)
for i in range(-26, 27, 4):
    L([(hx + i * 0.68, hy - 37), (hx + i, hy - 21)], K, 0.5)
L([(hx - 24, hy), (hx - 24, hy - 22)], K, 1); L([(hx + 24, hy), (hx + 24, hy - 22)], K, 1)
for wx in (-15, -3, 9):
    P([(hx + wx, hy - 5), (hx + wx, hy - 16), (hx + wx + 6, hy - 16), (hx + wx + 6, hy - 5)], B)
    L([(hx + wx + 3, hy - 5), (hx + wx + 3, hy - 16)], WH, 0.5)
P([(hx + 8, hy - 37), (hx + 8, hy - 45), (hx + 13, hy - 45), (hx + 13, hy - 37)], R)
tree(238, ridge(238) + 3, 30, 9); tree(292, ridge(292) + 3, 36, 11)

# ---- the field: ground tone first ----
a = np.asarray(img).copy()
rl = np.array([ridge(x / S) for x in range(W * S)], np.float32) * S
field = yy > rl[None, :]
g1 = np.asarray(Image.fromarray((fbm(40, 9) * 255).astype(np.uint8)).resize((W * S, H * S), Image.BICUBIC), np.float32) / 255
bay = np.tile(BAYER8, (H * S // 8 + 1, W * S // 8 + 1))[:H * S, :W * S]
a[field] = G
a[field & (bay < 0.30 * g1 + 0.12)] = Y
a[field & (bay > 0.93 - 0.25 * (1 - g1))] = K
img = Image.fromarray(a); d = ImageDraw.Draw(img)

def poppy_zone(x, y):                    # the red drift runs down the left bank
    t = (y - ridge(x)) / (H - ridge(x))
    centre = 40 + 150 * t
    return math.exp(-((x - centre) / (70 + 90 * t)) ** 2) * (0.35 + 0.65 * t) + 0.06

def blade(x, y, h, col, w=1):
    lean = rng.normal(0.25, 0.35)
    pts = [(x, y)]
    for i in range(1, 5):
        t = i / 4
        pts.append((x + lean * h * t * t, y - h * t))
    L(pts, col, w)

def poppy(x, y, r):
    if r < 2.2:
        E(x, y, r, r * 0.8, R); return
    L([(x, y), (x + rng.normal(0, r * .3), y + r * 3.2)], K, max(0.5, r / 6))
    for k in range(4):
        a_ = k * math.pi / 2 + rng.uniform(-.3, .3)
        E(x + r * .45 * math.cos(a_), y + r * .36 * math.sin(a_), r * .68, r * .55, R)
    if r > 4:
        for k in range(4):                # petal seams
            a_ = k * math.pi / 2 + 0.8
            L([(x, y), (x + r * .95 * math.cos(a_), y + r * .75 * math.sin(a_))], K, 0.5)
        E(x - r * .3, y - r * .3, r * .22, r * .16, WH)
    E(x, y, r * .26, r * .22, K)
    if r > 5:
        E(x, y, r * .1, r * .08, Y)

def walker(x, y, s, parasol):
    # skirt, bodice, hat; drawn dark blue so it sits against the green
    P([(x - 7 * s, y), (x - 3 * s, y - 20 * s), (x + 3 * s, y - 20 * s), (x + 8 * s, y)], B)
    for i in range(-5, 7, 3):
        L([(x + i * s * .4, y - 19 * s), (x + i * s, y)], K, 0.5)
    P([(x - 3.5 * s, y - 20 * s), (x - 4 * s, y - 31 * s), (x + 4 * s, y - 31 * s), (x + 3.5 * s, y - 20 * s)], K)
    L([(x - 3 * s, y - 24 * s), (x + 3 * s, y - 24 * s)], WH, 0.6)
    E(x, y - 34.5 * s, 3 * s, 3.4 * s, WH)
    E(x, y - 38 * s, 7 * s, 2.2 * s, Y); E(x, y - 39.5 * s, 3.6 * s, 2.4 * s, Y)
    L([(x - 4 * s, y - 37.6 * s), (x + 4 * s, y - 37.6 * s)], K, 0.7)
    if parasol:
        L([(x + 4 * s, y - 27 * s), (x + 12 * s, y - 50 * s)], K, 0.8)
        px, py = x + 13 * s, y - 52 * s
        d.pieslice([(px - 17 * s) * S, (py - 11 * s) * S, (px + 17 * s) * S, (py + 11 * s) * S], 180, 360, fill=B)
        d.pieslice([(px - 15 * s) * S, (py - 9 * s) * S, (px + 15 * s) * S, (py + 9 * s) * S], 180, 360, fill=WH)
        for k in range(-3, 4):
            L([(px, py - 10 * s), (px + k * 5 * s, py)], B, 0.5)
        L([(px - 17 * s, py), (px + 17 * s, py)], B, 0.8)

def child(x, y, s):
    P([(x - 4 * s, y), (x - 2 * s, y - 11 * s), (x + 2 * s, y - 11 * s), (x + 4 * s, y)], WH)
    L([(x - 4 * s, y), (x - 2 * s, y - 11 * s), (x + 2 * s, y - 11 * s), (x + 4 * s, y)], B, 0.6)
    E(x, y - 14 * s, 2.4 * s, 2.6 * s, WH)
    E(x, y - 16.6 * s, 5 * s, 1.6 * s, Y); L([(x - 3 * s, y - 16.2 * s), (x + 3 * s, y - 16.2 * s)], R, 0.8)
    E(x + 4.5 * s, y - 6 * s, 2 * s, 2 * s, R)       # the bunch she has picked

# everything in the field as one depth-sorted list
items = []
for _ in range(15000):
    x = rng.uniform(-5, W + 5); t = rng.random() ** 0.62
    y = ridge(x) + 2 + t * (H + 30 - ridge(x))
    items.append((y, 'g', x, t))
for _ in range(7000):
    x = rng.uniform(-5, W + 5); t = rng.random() ** 0.8
    y = ridge(x) + 2 + t * (H + 20 - ridge(x))
    if rng.random() < poppy_zone(x, y):
        items.append((y + 0.1, 'p', x, t))
for _ in range(500):
    x = rng.uniform(-5, W + 5); t = rng.random()
    y = ridge(x) + 2 + t * (H - ridge(x))
    items.append((y + 0.1, 'd', x, t))
items += [(ridge(84) + 16, 'w2', 84, 0), (ridge(96) + 18, 'c2', 96, 0),
          (462, 'w1', 268, 0), (468, 'c1', 236, 0)]
items.sort(key=lambda it: it[0])

for y, kind, x, t in items:
    if kind == 'g':
        h = 3 + 34 * t ** 1.5
        r_ = rng.random()
        col = K if r_ < 0.27 else (Y if r_ < 0.47 else (G if r_ < 0.93 else WH))
        blade(x, y, h * rng.uniform(.6, 1.2), col, 0.5 if t < 0.5 else (1 if t < .85 else 1.5))
    elif kind == 'p':
        r = 1.1 + 8.5 * t ** 1.7
        poppy(x, y - (3 + 26 * t ** 1.5) * rng.uniform(.5, 1), r * rng.uniform(.7, 1.2))
    elif kind == 'd':                      # daisies and buttercups
        r = 0.8 + 2.6 * t
        hgt = (3 + 24 * t ** 1.5)
        col = WH if rng.random() < .5 else Y
        if r > 2:
            for k in range(6):
                E(x + r * math.cos(k * 1.047), y - hgt + r * .8 * math.sin(k * 1.047), r * .5, r * .45, col)
            E(x, y - hgt, r * .4, r * .35, Y if col == WH else K)
        else:
            E(x, y - hgt, r, r * .8, col)
    elif kind == 'w1': walker(x, y - 24, 1.9, True)
    elif kind == 'c1': child(x, y - 22, 1.9)
    elif kind == 'w2': walker(x, y, 0.62, False)
    elif kind == 'c2': child(x, y, 0.62)

# a few poppies close enough to count the petals
for x, y, r in [(46, 548, 15), (118, 574, 18), (20, 590, 13), (188, 556, 12), (318, 580, 14), (372, 540, 10), (250, 592, 12)]:
    L([(x, y), (x + 5, y + 60)], K, 1.5)
    poppy(x, y, r)
    for _ in range(14):
        blade(x + rng.normal(0, 22), y + 40 + rng.uniform(0, 30), rng.uniform(30, 60), K if rng.random() < .4 else G, 1.5)

save(img)
