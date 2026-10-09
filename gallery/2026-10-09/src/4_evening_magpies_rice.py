"""Kkachi-bap — 'magpie's rice', the persimmons left on the tree for the birds.
A recursive black tree against a screened dusk (blue → red → yellow), sixty-odd persimmons,
two magpies, a tiled stone wall and the eave of a hanok roof."""
import math, random
import numpy as np
from PIL import Image, ImageDraw
from kit import *

rnd = random.Random(1446)
a = np.zeros((H, W, 3), np.uint8)
yy, xx = np.mgrid[0:H, 0:W]
HOR = 470
t = np.clip(yy / HOR, 0, 1) ** 1.15
everything = np.ones((H, W), bool)
up = t < 0.55
screen(a, everything & up, B, R, (t / 0.55) ** 1.4)
screen(a, everything & ~up, R, Y, (t - 0.55) / 0.45 * 0.55)
# a hard sun-disc sitting low behind the wall
sun = (xx - 300) ** 2 + (yy - 412) ** 2 < 30 ** 2
a[sun] = Y
img = Image.fromarray(a); d = ImageDraw.Draw(img)
# horizontal cloud bars across the sun
for y0, x0, x1 in [(400, 236, 390), (414, 256, 400), (424, 210, 340), (360, 120, 260), (372, 150, 300)]:
    d.rectangle([x0, y0, x1, y0 + 3], fill=R if y0 > 410 else B)
    d.line([(x0 + 6, y0 + 4), (x1 - 6, y0 + 4)], fill=K)

# distant ridge
ridge = [(0, 448)] + [(x, 438 - 18 * math.sin(x / 70) - 8 * math.sin(x / 23 + 1)) for x in range(0, W + 1, 4)] + [(W, 470), (0, 470)]
d.polygon(ridge + [(W, 520), (0, 520)], fill=B)
arr = np.array(img)
fieldm = mask_of(lambda mm: mm.rectangle([0, 462, W, 520], fill=255))
screen(arr, fieldm, G, K, np.clip((yy - 462) / 70, 0, 1) * 0.8 + 0.1)
img.paste(Image.fromarray(arr)); d = ImageDraw.Draw(img)
for x in range(0, W, 7):  # stubble rows in the harvested field
    d.line([(x, 470 + (x * 7) % 40), (x + 1, 466 + (x * 7) % 40)], fill=Y)
for x in range(0, W, 5):
    yr = 438 - 18 * math.sin(x / 70) - 8 * math.sin(x / 23 + 1)
    d.line([(x, yr), (x + 2, yr - 4)], fill=K)  # far pines bristle

# ---- tree
persimmons, leaves = [], []
def branch(x, y, ang, L, w, depth):
    x1, y1 = x + L * math.cos(ang), y + L * math.sin(ang)
    # slightly crooked segments
    mx, my = (x + x1) / 2 + rnd.uniform(-L * .12, L * .12), (y + y1) / 2 + rnd.uniform(-L * .08, L * .08)
    d.line([(x, y), (mx, my), (x1, y1)], fill=K, width=max(1, int(w)), joint="curve")
    if depth == 0 or L < 7:
        if rnd.random() < 0.55: persimmons.append((x1, y1 + 7))
        elif rnd.random() < 0.5: leaves.append((x1, y1))
        return
    n = 2 if rnd.random() < .75 else 3
    for i in range(n):
        da = rnd.uniform(.25, .7) * (1 if i % 2 else -1) + rnd.uniform(-.1, .1)
        branch(x1, y1, ang + da - 0.06, L * rnd.uniform(.68, .82), w * .66, depth - 1)
    if depth < 4 and rnd.random() < .5:
        persimmons.append((x1 + rnd.uniform(-6, 6), y1 + 8))

trunk = [(60, 600), (64, 520), (78, 430), (82, 360)]
for k in range(len(trunk) - 1):
    d.line([trunk[k], trunk[k + 1]], fill=K, width=30 - k * 6)
branch(82, 360, -1.25, 86, 15, 8)
branch(80, 420, -0.45, 70, 11, 7)
branch(84, 380, -2.2, 40, 8, 5)
# bark texture where the trunk meets the light
for k in range(30):
    y = 600 - k * 8
    d.line([(52 + k * .7, y), (58 + k * .7, y - 4)], fill=B, width=1)

def persimmon(x, y, r=7):
    m = (xx - x) ** 2 + ((yy - y) * 1.1) ** 2 < r * r
    arr = np.array(img)
    shade = np.clip(0.08 + 0.75 * (((xx - x + 3) ** 2 + (yy - y + 3) ** 2) / (r * r * 1.8)), 0, 1)
    screen(arr, m, Y, R, shade)
    img.paste(Image.fromarray(arr))
    d.ellipse([x - r, y - r / 1.1, x + r, y + r / 1.1], outline=K, width=1)
    d.line([(x - 4, y - r + 1), (x + 4, y - r + 1)], fill=K, width=3)  # calyx
    d.line([(x, y - r - 4), (x, y - r)], fill=K, width=1)
    d.point((x - 3, y - 2), fill=WH)

for (x, y) in leaves[:70]:
    ang = rnd.uniform(0, math.pi)
    lx, ly = x + 7 * math.cos(ang), y + 7 * math.sin(ang)
    d.polygon([(x, y), (lx + 3, ly - 3), (lx, ly), (lx - 3, ly + 3)], fill=rnd.choice([R, Y, G]), outline=K)
rnd.shuffle(persimmons)
for (x, y) in persimmons[:48]:
    if 0 < x < W and y < 470:
        persimmon(x, y, rnd.choice([6, 7, 8]))

# falling leaves
for i in range(14):
    x, y = rnd.uniform(120, 390), rnd.uniform(280, 455)
    ang = rnd.uniform(0, math.pi)
    d.polygon([(x, y), (x + 8 * math.cos(ang) + 2, y + 8 * math.sin(ang) - 2), (x + 8 * math.cos(ang), y + 8 * math.sin(ang)), (x + 8 * math.cos(ang) - 2, y + 8 * math.sin(ang) + 2)], fill=rnd.choice([R, Y]), outline=K)

# ---- magpies
def magpie(x, y, s=1.0, flip=1, pecking=False):
    P = lambda pts: [(x + flip * px * s, y + py * s) for px, py in pts]
    tail = P([(-8, 2), (-46, 18), (-50, 14), (-12, -4)])
    d.polygon(tail, fill=K)
    d.line(P([(-10, 0), (-46, 15)]), fill=B, width=2)
    body = P([(-12, -6), (0, -14), (14, -14), (22, -8), (18, 4), (4, 10), (-10, 4)])
    d.polygon(body, fill=K)
    belly = P([(-4, 2), (6, -4), (16, -2), (14, 4), (2, 8)])
    d.polygon(belly, fill=WH)
    wing = P([(-10, -8), (8, -12), (2, -2), (-12, 0)])
    d.polygon(wing, fill=K, outline=B)
    d.line(P([(-6, -6), (4, -9)]), fill=WH, width=max(2, int(3 * s)))  # white scapular
    hx, hy = (22, -18) if not pecking else (26, -6)
    d.ellipse([x + flip * hx * s - 7 * s, y + hy * s - 6 * s, x + flip * hx * s + 7 * s, y + hy * s + 6 * s], fill=K)
    bx = x + flip * (hx + 7) * s
    d.polygon([(bx, y + (hy - 2) * s), (bx + flip * 9 * s, y + hy * s + (2 * s if pecking else 0)), (bx, y + (hy + 2) * s)], fill=K)
    d.ellipse([x + flip * (hx + 2) * s - 1.5, y + (hy - 2) * s - 1.5, x + flip * (hx + 2) * s + 1.5, y + (hy - 2) * s + 1.5], fill=WH)
    d.line(P([(4, 9), (2, 18)]), fill=K, width=2); d.line(P([(10, 7), (12, 18)]), fill=K, width=2)

# perch branches for the birds
d.line([(84, 300), (190, 270), (250, 258)], fill=K, width=6)
d.line([(160, 278), (200, 300), (230, 296)], fill=K, width=3)
persimmon(222, 266, 9); persimmon(240, 268, 8)
magpie(178, 252, 1.35, 1, pecking=False)
magpie(268, 330, 1.1, -1)
d.line([(220, 350), (330, 342)], fill=K, width=4)

# ---- stone wall with tiled cap (bottom)
wall_top = 520
d.rectangle([0, wall_top, W, H], fill=K)
arr = np.array(img)
rows = [(wall_top + 14, 16), (wall_top + 30, 18), (wall_top + 48, 22)]
for ry, rh in rows:
    x = rnd.randint(-20, 0)
    while x < W:
        sw = rnd.randint(22, 44)
        m = mask_of(lambda mm: mm.rounded_rectangle([x + 2, ry + 1, x + sw - 2, ry + rh - 1], radius=6, fill=255))
        screen(arr, m, B, WH, rnd.uniform(0.15, 0.4))
        x += sw
img.paste(Image.fromarray(arr))
d.rectangle([0, 578, W, H], fill=K)
# roof-tile cap
d.polygon([(0, wall_top + 12), (0, wall_top - 2), (W, wall_top - 8), (W, wall_top + 10)], fill=K)
for x in range(0, W + 8, 9):
    yv = wall_top - 2 - x * 6 / W
    d.arc([x - 5, yv + 8, x + 5, yv + 18], 0, 180, fill=WH, width=2)
    d.line([(x, yv), (x, yv + 10)], fill=B)
d.line([(0, wall_top - 3), (W, wall_top - 9)], fill=WH, width=2)
# hanok eave sweeping in at upper right
eave = [(W, 40), (330, 58), (285, 66), (262, 60), (270, 72), (330, 76), (W, 66)]
d.polygon(eave, fill=K)
for k in range(10):
    x = 290 + k * 11
    d.line([(x, 66 - (x - 285) * .1), (x + 2, 74 - (x - 285) * .05)], fill=R, width=3)  # rafter ends, dancheong red
    d.ellipse([x - 2, 70 - (x - 285) * .06, x + 4, 76 - (x - 285) * .06], fill=G, outline=K)
d.line([(262, 60), (330, 54), (W, 36)], fill=WH, width=1)

d.rectangle([0, 0, W - 1, H - 1], outline=K, width=4)
save(img)
