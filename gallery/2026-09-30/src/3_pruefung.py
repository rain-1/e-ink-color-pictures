"""3 · Afternoon — Die Feuer- und Wasserprobe. A cutaway through a mountain in the manner of a
geological section: red rock in strata, a cavern of fire at the root, a cavern of water above
it, and the two lovers climbing through both while the flute plays, toward the temple and
the sun on the summit."""
import math, random
import numpy as np
from PIL import Image, ImageDraw
from common import *

random.seed(7)
c = Canvas(Wh)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)

# sky + sun behind the summit temple
c.tone(lambda d, s: d.rectangle([0, 0, W * s, 170 * s], fill=255), np.clip(1 - yy / 160, 0, 1) * 0.55, Y, Wh)
c.snapshot_layer()
SX, SY = 200, 56
for i in range(48):
    a = i * math.pi * 2 / 48
    c.line([(SX + 34 * math.cos(a), SY + 34 * math.sin(a)), (SX + (90 if i % 2 else 60) * math.cos(a), SY + (90 if i % 2 else 60) * math.sin(a))], R if i % 2 else Y, 1)
c.ell(SX, SY, 30, fill=Y, outline=R, width=1.5)

# mountain silhouette
ridge = [(0, 180), (40, 168), (80, 150), (120, 138), (160, 118), (200, 110), (240, 116), (280, 132), (330, 150), (370, 162), (400, 172)]
ridge = [(x, y + 5 * math.sin(x / 13)) for x, y in ridge]
mount = ridge + [(W, H), (0, H)]
c.poly(mount, fill=R)
# temple on the summit: little portico
c.rect(168, 86, 232, 90, fill=K)
for k in range(7): c.rect(170 + k * 9.5, 90, 174 + k * 9.5, 112, fill=Wh, outline=K, width=.5)
c.poly([(164, 86), (200, 70), (236, 86)], fill=Wh, outline=K, width=.8)
c.rect(164, 110, 236, 116, fill=Wh, outline=K, width=.8)

# strata in the rock: wavy bands, some filled
rock = Image.new("L", (W * S, H * S), 0); ImageDraw.Draw(rock).polygon([(x * S, y * S) for x, y in mount], fill=255)
rockm = np.asarray(rock.resize((W, H), Image.BOX)) > 128
n1 = vnoise(H, W, 60, 1)
strata = (yy + 40 * n1 + 12 * np.sin(xx / 37)) / 11.0
band = np.floor(strata).astype(int)
frac = strata - band
rgb = np.zeros((H, W, 3), np.uint8); rgb[:] = R
lines = frac < 0.13
rgb[lines] = K
dotted = (band % 5 == 2) & (((xx.astype(int) // 3 + yy.astype(int) // 3) % 2) == 0) & ~lines
rgb[dotted] = K
yband = (band % 7 == 4) & ~lines
rgb[yband & ((xx.astype(int) + yy.astype(int)) % 4 == 0)] = Y
paste_1x(c, rgb, rockm & (yy > 128))

# caverns
def cave(cx, cy, rx, ry, seed):
    rng = random.Random(seed)
    pts = []
    for t in np.linspace(0, 2 * math.pi, 64, endpoint=False):
        rr = 1 + 0.08 * math.sin(3 * t + seed) + rng.uniform(-0.04, 0.04)
        pts.append((cx + rx * rr * math.cos(t), cy + ry * rr * math.sin(t) * (0.85 if math.sin(t) > 0 else 1)))
    return pts
water = cave(210, 290, 158, 78, 1)
fire = cave(190, 485, 168, 80, 2)
def poly_mask(pts):
    m = Image.new("L", (W, H), 0); ImageDraw.Draw(m).polygon(pts, fill=255); return np.asarray(m) > 0
wm, fm = poly_mask(water), poly_mask(fire)

# connecting shafts (drawn as black voids with ladders)
shafts = [[(46, 572), (70, 572), (70, 520), (46, 520)],        # entrance from below-left
          [(318, 440), (344, 440), (340, 348), (314, 348)],    # fire -> water
          [(84, 250), (108, 250), (122, 136), (98, 136)]]     # water -> summit
for sp in shafts:
    c.poly(sp, fill=K)
    x0 = min(p[0] for p in sp) + 5; x1 = max(p[0] for p in sp) - 5
    y0 = min(p[1] for p in sp); y1 = max(p[1] for p in sp)
    slope = (sp[3][0] - sp[0][0]) / (sp[3][1] - sp[0][1] + 1e-9)
    for y in np.arange(y0 + 4, y1, 7):
        dx = (y - y1) * slope
        c.line([(x0 + dx, y), (x1 + dx, y)], Y, 1)
    c.line([(x0 + (y0 - y1) * slope, y0), (x0, y1)], Y, 1); c.line([(x1 + (y0 - y1) * slope, y0), (x1, y1)], Y, 1)

# FIRE: flame field (value noise stretched upward, hot at the floor)
def tall(cell, seed, k=3):   # noise stretched vertically, like flame tongues
    n = vnoise(H // k + 2, W, cell, seed)
    return np.asarray(Image.fromarray((n * 255).astype(np.uint8)).resize((W, H), Image.BILINEAR), np.float32) / 255
fn = 0.65 * tall(14, 5) + 0.35 * tall(6, 6, 2)
flo = 560.0
heat = np.clip(1 - (flo - yy) / 125, 0, 1)
v = fn + 0.15 * np.sin(xx / 7 + 4 * vnoise(H, W, 30, 8)) - heat * 1.05 + 0.1
frgb = np.zeros((H, W, 3), np.uint8)            # black cavern air
frgb[v < 0.28] = R
frgb[v < 0.05] = Y
frgb[v < -0.15] = Wh
# embers
rng = np.random.default_rng(4)
em = (rng.random((H, W)) < 0.012) & (v > 0.28)
frgb[em] = Y
paste_1x(c, frgb, fm)
# WATER: interference ripples, a waterfall from the upper left
wv = np.sin(yy / 2.4 + 7 * vnoise(H, W, 34, 9) + xx / 50)
wn = vnoise(H, W, 22, 10)
wrgb = np.zeros((H, W, 3), np.uint8); wrgb[:] = B
wrgb[(wv > 0.55) & (wn > 0.35)] = Wh
wrgb[(wv < -0.75) & (wn < 0.42)] = G
surf = 262 + 3 * np.sin(xx / 11)
wrgb[yy < surf] = K
fall = (np.abs(xx - 90 - 4 * np.sin(yy / 13)) < 16) & (yy < surf + 20)
streak = (np.sin(xx * 1.9 + vnoise(H, W, 12, 11) * 6) > 0.1)
wrgb[fall & streak] = Wh; wrgb[fall & ~streak] = B
spray = (np.abs(xx - 90) < 40) & (np.abs(yy - surf) < 10) & (rng.random((H, W)) < 0.35)
wrgb[spray] = Wh
paste_1x(c, wrgb, wm)
# stalactites in both caves + rims
for pts, col in ((water, K), (fire, K)):
    c.poly(pts, outline=Y, width=1.4)
for cx0, cx1, ytop in ((120, 330, 214), (60, 330, 410)):
    for x in range(cx0, cx1, 11):
        L = random.uniform(8, 22)
        c.poly([(x - 3, ytop - 6), (x + 3, ytop - 6), (x, ytop + L - 6)], fill=R, outline=K, width=.6)

# the path: stepping stones across the water, a bridge over the fire
for i, x in enumerate(range(130, 318, 24)):
    y = 282 + 4 * math.sin(i)
    c.poly(oval(x, y, 10, 4), fill=K); c.poly(oval(x, y - 2, 9, 3.4), fill=Wh, outline=K, width=.5)
bx0, bx1, by = 60, 334, 440
bridge = [(bx0 + (bx1 - bx0) * t, by + 22 * math.sin(math.pi * t)) for t in np.linspace(0, 1, 40)]
c.line(bridge, Wh, 4); c.line([(x, y + 2.4) for x, y in bridge], K, 1)
for x, y in bridge[::3]: c.line([(x, y), (x, y - 12)], Y, 0.9); c.line([(x, y + 2), (x - 3, y + 9), (x + 3, y + 9), (x, y + 2)], Wh, .6)
c.line([(x, y - 12) for x, y in bridge], Y, 1.1)

def person(x, y, s, robe, flute=False, hand=None):
    c.ell(x, y - 30 * s, 4.5 * s, fill=Wh, outline=K, width=.8)
    c.poly([(x - 5 * s, y - 25 * s), (x + 5 * s, y - 25 * s), (x + 8 * s, y), (x - 8 * s, y)], fill=robe, outline=K, width=.9)
    c.rect(x - 5 * s, y - 16 * s, x + 5 * s, y - 14 * s, fill=Y)
    if flute:
        c.line([(x + 2 * s, y - 28 * s), (x + 16 * s, y - 34 * s)], Y, 1.8); c.line([(x + 2 * s, y - 28 * s), (x + 16 * s, y - 34 * s)], K, .5)
        c.line([(x + 4 * s, y - 22 * s), (x + 10 * s, y - 31 * s)], Wh, 1.4)
    if hand is not None:
        c.line([(x - 4 * s, y - 20 * s), hand], Wh, 1.4)
# on the bridge, in the fire
px, py = 190, by + 22 * math.sin(math.pi * (190 - bx0) / (bx1 - bx0)) - 2
person(px - 12, py, 1.1, Wh, hand=(px - 2, py - 18))
c.poly([(px - 18, py - 38), (px - 12, py - 42), (px - 6, py - 38), (px - 12, py - 34)], fill=K)  # Pamina's hair
person(px + 6, py, 1.2, B, flute=True)
# notes rising from the flute through the rock
notes = [(222, 420, 1), (240, 402, 2), (262, 390, 1), (285, 374, 2), (305, 360, 1), (318, 336, 2)]
for x, y, k in notes:
    c.ell(x, y, 3.2, 2.4, fill=Wh, outline=K, width=.6); c.line([(x + 3, y), (x + 3, y - 12)], Wh, 1)
    if k == 2: c.line([(x + 3, y - 12), (x + 8, y - 7)], Wh, 1)
# ghost footprints on the stones: they came this way
for i, x in enumerate(range(130, 318, 48)):
    c.ell(x - 2, 280, 1.4, fill=K); c.ell(x + 2, 281, 1.4, fill=K)

# legend panel, geological-plate style
c.rect(250, 560, 392, 594, fill=Wh, outline=K, width=1)
for i, (col, lab) in enumerate(((Y, "FEUER"), (B, "WASSER"))):
    c.rect(256 + i * 68, 566, 268 + i * 68, 578, fill=col, outline=K, width=.6)
    c.text((272 + i * 68, 572), lab, K, 8, "lm", bold=True)
c.text((321, 587), "Profil der Prüfungen · 1791", K, 7.5, "mm")
c.finish()
