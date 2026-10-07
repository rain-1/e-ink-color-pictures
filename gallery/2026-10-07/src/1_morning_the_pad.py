"""1. Morning — The Pad. R-7 8K72 'Luna' in its tulip at Tyuratam, first light."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from common import *

rng = np.random.default_rng(1004)
HZ = 438                       # horizon
CX = 200                       # rocket axis
SUN = (318, HZ + 2)
ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)

# ---- sky: night overhead, dawn on the eastern (right) horizon
d_sun = np.hypot((xs - SUN[0]) * 0.55, ys - SUN[1])
t = (ys / HZ) ** 1.6 * 0.78 + 0.32 * np.exp(-(d_sun / 120) ** 2)
img = ramp(t, ["K", "K", "B", "B", "R", "Y", "Y"])
glow = np.exp(-(d_sun / 26) ** 2) > bayer() * 0.9
img[glow & (ys < HZ)] = INK["W"]

# stars where it is still night
for _ in range(260):
    x, y = rng.integers(0, W), rng.integers(0, 250)
    if t[y, x] < 0.24 + rng.uniform(-0.04, 0.04):
        img[y, x] = INK["W"]
        if rng.uniform() < 0.08 and 1 < x < W - 2 and y > 1:
            img[y - 1:y + 2, x] = INK["W"]; img[y, x - 1:x + 2] = INK["W"]
        elif rng.uniform() < 0.15:
            img[y, x] = INK["Y"]

# waning crescent with earthshine, low in the east, lit toward the sun
mx, my, mr = 292, 168, 17
dm = np.hypot(xs - mx, ys - my)
lit = (dm < mr) & (np.hypot(xs - (mx - 7), ys - (my - 6)) > mr - 0.5)
disc = dm < mr
img[disc] = np.where((bayer() < 0.25)[disc, None], INK["B"], INK["K"])
img[lit] = INK["W"]
img[lit & (np.hypot(xs - (mx - 9), ys - (my - 8)) < mr + 2.5)] = INK["Y"]

# ---- steppe
gy = np.clip((ys - HZ) / (H - HZ), 0, 1)
ground = ramp(0.1 + 0.9 * gy ** 0.7, ["Y", "Y", "G", "G", "G"])
# low sun: long raking light, broken by swells
swell = np.sin(xs * 0.031 + np.sin(ys * 0.05) * 2 + ys * 0.11) * 0.5 + 0.5
shade = (swell * (0.3 + gy) * 0.6) > bayer() + 0.35
ground[shade] = INK["K"]
img[ys >= HZ] = ground[ys >= HZ]

back = Layer()
# clouds: thin lens-shaped strands catching the sun
for cy0, x0, x1, c, th in [(330, 210, 400, "R", 3), (350, 150, 380, "R", 2.4), (372, 240, 400, "Y", 2.0),
                           (394, 170, 330, "Y", 1.6), (300, 250, 400, "B", 2.2), (312, 290, 400, "R", 1.4),
                           (405, 0, 120, "R", 1.6), (385, 0, 90, "B", 2.0), (418, 30, 150, "Y", 1.2)]:
    pts_top, pts_bot = [], []
    for k in range(25):
        u = k / 24; x = x0 + (x1 - x0) * u
        h = th * math.sin(math.pi * u) ** 0.7
        pts_top.append((x, cy0 - h + 2 * math.sin(u * 7))); pts_bot.append((x, cy0 + h * 0.6 + 2 * math.sin(u * 7)))
    back.poly(pts_top + pts_bot[::-1], c)

# distant settlement and second pad silhouette on the horizon
def hut(x, w, h, roof=False):
    back.rect(x, HZ - h, x + w, HZ + 1, "K")
    if roof: back.poly([(x - 1, HZ - h), (x + w / 2, HZ - h - 4), (x + w + 1, HZ - h)], "K")
for x in range(4, 120, 9):
    hut(x, rng.integers(5, 9), rng.integers(3, 9), rng.uniform() < 0.3)
for x in range(268, 396, 11):
    hut(x, rng.integers(5, 10), rng.integers(2, 7))
# water tower + chimney + distant radio mast
back.rect(94, HZ - 22, 96, HZ, "K"); back.rect(101, HZ - 22, 103, HZ, "K"); back.rect(90, HZ - 30, 107, HZ - 22, "K")
back.rect(352, HZ - 34, 356, HZ, "K"); back.line([(354, HZ - 34), (346, HZ - 52), (330, HZ - 60)], "B", 3)
back.line([(382, HZ), (382, HZ - 46)], "K", 1); back.line([(372, HZ), (382, HZ - 46), (392, HZ)], "K", 0.6)
back.rect(380, HZ - 48, 384, HZ - 45, "R")
# distant lit windows
for x in range(6, 118, 9):
    if rng.uniform() < 0.4: back.rect(x + 2, HZ - 3, x + 3, HZ - 2, "Y")

def lattice(x0, y0, x1, y1, w0, w1, c="R", oc="K", step=10, lw=1.0):
    """A tapering lattice tower from base (x0,y0) to top (x1,y1)."""
    n = max(2, int(abs(y0 - y1) / step))
    L, Rr = [], []
    for i in range(n + 1):
        u = i / n
        x = x0 + (x1 - x0) * u; y = y0 + (y1 - y0) * u; w = w0 + (w1 - w0) * u
        L.append((x - w / 2, y)); Rr.append((x + w / 2, y))
    back.line(L, oc, lw * 1.6); back.line(Rr, oc, lw * 1.6)
    for i in range(n):
        back.line([L[i], Rr[i + 1]], c, lw); back.line([Rr[i], L[i + 1]], c, lw)
        back.line([L[i], Rr[i]], oc, lw * 0.8)
    back.line([L[-1], Rr[-1]], oc, lw * 0.8)
    return L, Rr

# retracted service gantry, far left
L, Rr = lattice(52, HZ + 18, 52, 128, 46, 30, "R", "K", 12, 1.0)
for yy in range(150, HZ, 40):
    back.rect(28, yy, 78, yy + 3, "K"); back.line([(28, yy), (78, yy)], "Y", 0.6)
    back.rect(30, yy - 7, 31, yy, "K"); back.rect(75, yy - 7, 76, yy, "K")
back.rect(36, 118, 68, 128, "K"); back.rect(46, 104, 58, 118, "K")
back.line([(52, 104), (52, 82)], "K", 1.2); back.ellipse(52, 82, 2.5, 2.5, "R")
for yy in range(158, HZ, 40):
    back.ellipse(40, yy, 1.6, 1.6, "Y"); back.ellipse(64, yy + 18, 1.6, 1.6, "Y")
# crane jib on the gantry top
back.line([(36, 120), (6, 140)], "K", 2); back.line([(6, 140), (6, 178)], "K", 0.6); back.rect(3, 178, 9, 183, "Y")
# lightning mast, right
lattice(356, HZ + 10, 356, 60, 12, 4, "B", "K", 14, 0.8)
back.ellipse(356, 58, 2.2, 2.2, "R")
for yy in (140, 230, 320):
    back.line([(356, yy), (396, yy + 90)], "K", 0.5)

# cable masts either side of the rocket
lattice(CX - 74, HZ + 8, CX - 70, 300, 14, 8, "Y", "K", 9, 0.8)
lattice(CX + 74, HZ + 8, CX + 70, 285, 14, 8, "Y", "K", 9, 0.8)
back.line([(CX - 70, 302), (CX - 18, 262)], "K", 1.0); back.line([(CX - 70, 312), (CX - 15, 300)], "K", 0.8)
back.line([(CX + 70, 287), (CX + 16, 205)], "K", 1.0); back.line([(CX + 70, 296), (CX + 18, 270)], "K", 0.8)

# pad deck
back.rect(70, HZ - 2, 330, HZ + 18, "W", "K", 1.2)
back.rect(70, HZ + 12, 330, HZ + 18, "B")
for x in range(72, 330, 8):
    back.line([(x, HZ - 8), (x, HZ - 2)], "K", 0.6)
back.line([(70, HZ - 8), (330, HZ - 8)], "K", 0.8); back.line([(70, HZ - 5), (330, HZ - 5)], "K", 0.5)
# flame pit opening (we look over its lip)
back.poly([(150, HZ + 18), (250, HZ + 18), (268, HZ + 52), (132, HZ + 52)], "K")
for k in range(9):
    back.line([(132 + k * 3, HZ + 52 - k * 4), (268 - k * 3, HZ + 52 - k * 4)], "B", 0.5)
back.poly([(120, HZ + 52), (280, HZ + 52), (288, HZ + 58), (112, HZ + 58)], "W", "K", 1)
img = back.onto(img)

# ---- the rocket, shaded per pixel as solids of revolution (sun from the right)
def solid(axis_x, r_of_y, y0, y1, stops=("K", "B", "W", "W", "Y"), lx=0.75):
    global img
    yy = np.arange(H)[:, None].astype(np.float32)
    r = r_of_y(yy)
    ax = axis_x(yy) if callable(axis_x) else axis_x
    u = (xs - ax) / np.maximum(r, 0.01)
    m = (np.abs(u) <= 1) & (ys >= y0) & (ys <= y1) & (r > 0.3)
    nz = np.sqrt(np.clip(1 - u * u, 0, 1))
    l = np.clip(lx * u + 0.66 * nz, 0, 1)
    tone = ramp(l ** 1.2, list(stops))
    img[m] = tone[m]
    edge = m & (np.abs(u) > 1 - 1.4 / np.maximum(r, 1))
    img[edge] = INK["K"]
    return m

def lin(a, ya, b, yb):
    return lambda y: a + (b - a) * np.clip((y - ya) / (yb - ya), 0, 1)

# core stage: waisted — narrow at the base, widest under the boosters' noses, tapering at top
def core_r(y):
    return np.interp(y, [150, 160, 255, 300, 430], [12, 15.5, 15.5, 13.5, 11])
solid(CX, core_r, 150, 432)
# interstage truss, Block E, payload fairing
for k in range(6):
    x = CX - 11 + k * 4.4
    img[136:150, int(x)] = INK["K"]
img[136, CX - 12:CX + 12] = INK["K"]
solid(CX, lambda y: np.interp(y, [104, 116, 136], [7, 12.5, 12.5]), 104, 136)
solid(CX, lambda y: np.interp(y, [70, 84, 104], [0.4, 7, 9.5]), 70, 104, ("K", "B", "W", "Y", "Y"))
# boosters: conical, inner edge hugs the core, nose leans in
for side in (-1, 1):
    rb = lambda y: np.interp(y, [238, 250, 420], [1.5, 5, 17])
    axis = lambda y, s=side: CX + s * (core_r(y) - 3 + rb(y))
    solid(axis, rb, 238, 422)
# front booster
solid(CX, lambda y: np.interp(y, [246, 258, 422], [1.5, 5.5, 17.5]), 246, 422)

lay = Layer()
# seams, hatches, markings
for y in (180, 214, 300, 340, 380, 410):
    w = float(core_r(np.array(y)))
    lay.line([(CX - w, y), (CX + w, y + 1)], "K", 0.5)
for y in (116, 124, 92):
    lay.line([(CX - 11, y), (CX + 11, y)], "K", 0.5)
lay.rect(CX - 3, 112, CX + 3, 118, "R")
for i, ch in enumerate("СССР"):
    lay.text((CX + 4, 160 + i * 13), ch, "R", 11, "cond", "ma")
# booster ring seams and the red nose bands
for side in (-1, 0, 1):
    for y in (300, 350, 395):
        rbv = np.interp(y, [246, 258, 422], [1.5, 5.5, 17.5])
        ax = CX + side * (core_r(np.array(y)) - 3 + rbv) if side else CX
        lay.line([(ax - rbv, y), (ax + rbv, y + 1)], "K", 0.5)
# engines: four nozzles per booster + core, bell shapes
for bx in (CX - 30, CX - 14, CX + 14, CX + 30, CX - 6, CX + 6):
    lay.poly([(bx - 3, 422), (bx + 3, 422), (bx + 5, 434), (bx - 5, 434)], "K")
    lay.line([(bx - 4, 431), (bx + 4, 431)], "R", 0.5)
# steering verniers
for bx in (CX - 44, CX + 44):
    lay.poly([(bx - 2, 418), (bx + 2, 418), (bx + 3, 426), (bx - 3, 426)], "K")

# tulip: four petals, two seen, gripping the boosters' shoulders
for side in (-1, 1):
    base = (CX + side * 62, HZ - 4); top = (CX + side * 40, 302)
    for k in range(3):
        off = (k - 1) * 3.5
        lay.line([(base[0] + off * side, base[1]), (top[0] + off, top[1])], "R", 1.6)
    for k in range(11):
        u0, u1 = k / 11, (k + 1) / 11
        p = lambda u, o: (base[0] + (top[0] - base[0]) * u + o, base[1] + (top[1] - base[1]) * u)
        lay.line([p(u0, -3.5), p(u1, 3.5)], "K", 0.6)
    lay.poly([(top[0] - 5, top[1] - 4), (top[0] + 5, top[1] - 4), (top[0] + side * 12, top[1] + 4), (top[0] - 3, top[1] + 6)], "K")
    lay.ellipse(base[0], base[1] - 2, 3.5, 3.5, "K")
    lay.ellipse(base[0], base[1] - 2, 1.4, 1.4, "Y")
# front petal: foreshortened, straight up the middle
lay.line([(CX - 4, HZ - 4), (CX - 4, 404)], "R", 2); lay.line([(CX + 4, HZ - 4), (CX + 4, 404)], "R", 2)
for y in range(406, HZ - 4, 5):
    lay.line([(CX - 4, y), (CX + 4, y + 5)], "K", 0.6)

# venting LOX: billowing white puffs, blue in their shadow side (left)
def puff(x, y, r):
    lay.ellipse(x, y, r, r * 0.8, "W")
    lay.arc(x, y, r * 0.95, 110, 230, "B", max(1, r * 0.25))
for x, y, r in [(150, 430, 10), (162, 424, 12), (176, 432, 9), (232, 428, 12), (246, 436, 10), (220, 434, 8),
                (138, 438, 8), (262, 440, 9), (128, 444, 6), (276, 446, 7), (188, 440, 6), (212, 442, 7)]:
    puff(x, y, r)
for x, y, r in [(214, 128, 5), (222, 122, 6), (232, 117, 5), (243, 114, 4), (252, 113, 3)]:
    puff(x, y, r)
img = lay.onto(img)

# ---- foreground: rails to the pad, a road, poles, people, grass
fg = Layer()
# long shadow of the rocket thrown west across the steppe
fg.poly([(170, HZ + 58), (196, HZ + 58), (40, HZ + 78), (0, HZ + 84), (0, HZ + 76)], "G")
# railway: two rails converging toward the pit edge, sleepers widening toward us
vx, vy = 182, HZ + 58
for rx in (-58, 30):
    fg.line([(vx + rx * 0.05, vy), (vx + rx * 2.6, H + 10)], "K", 1.3)
for rx in (-50, 22):
    fg.line([(vx + rx * 0.05 + 2, vy), (vx + rx * 2.6 + 6, H + 10)], "W", 1.0)
yk = vy + 2.0
while yk < H:
    u = (yk - vy) / (H - vy)
    xa = vx - 58 * 0.05 + (-58 * 2.6 + 58 * 0.05) * u - 6 * u
    xb = vx + 30 * 0.05 + (30 * 2.6 - 30 * 0.05) * u + 6 * u
    fg.line([(xa, yk), (xb, yk)], "K", 0.6 + 2.4 * u)
    yk += 2 + 22 * u ** 1.4
# road with poles bending away to the right
road = [(250, HZ + 58), (300, HZ + 90), (360, HZ + 130), (400, HZ + 150)]
fg.line(road, "W", 6); fg.line(road, "Y", 3)
prev = None
for i, (px, py, s) in enumerate([(286, HZ + 70, 0.4), (318, HZ + 90, 0.65), (360, HZ + 118, 1.0), (408, HZ + 152, 1.4)]):
    top = (px, py - 34 * s)
    fg.line([(px, py), top], "K", 1.0 * s + 0.4)
    fg.line([(px - 6 * s, top[1] + 3 * s), (px + 6 * s, top[1] + 3 * s)], "K", 0.8 * s + 0.3)
    if prev:
        for dx in (-5, 5):
            a = (prev[0] + dx * prev[2], prev[1] + 3 * prev[2]); b = (top[0] + dx * s, top[1] + 3 * s)
            mid = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + 4 * s)
            fg.line([a, mid, b], "K", 0.5)
    prev = (top[0], top[1], s)
# a GAZ truck and a bus on the road
def vehicle(x, y, s, c):
    fg.rect(x, y - 9 * s, x + 18 * s, y - 2 * s, c, "K", 0.6)
    fg.rect(x + 18 * s, y - 7 * s, x + 25 * s, y - 2 * s, c, "K", 0.6)
    fg.rect(x + 19 * s, y - 6 * s, x + 23 * s, y - 4 * s, "B")
    for wx in (x + 4 * s, x + 20 * s):
        fg.ellipse(wx, y - 1 * s, 2.4 * s, 2.4 * s, "K")
vehicle(296, HZ + 86, 0.8, "G")
vehicle(334, HZ + 112, 1.0, "R")
# people: tiny engineers walking to the bunker, one waving
def person(x, y, s=1.0, c="K", wave=False):
    fg.ellipse(x, y - 11 * s, 1.6 * s, 1.6 * s, c)
    fg.line([(x, y - 9.5 * s), (x, y - 4 * s)], c, 1.6 * s)
    fg.line([(x, y - 4 * s), (x - 1.8 * s, y)], c, 1.0 * s); fg.line([(x, y - 4 * s), (x + 1.8 * s, y)], c, 1.0 * s)
    if wave: fg.line([(x, y - 8.5 * s), (x + 3 * s, y - 13 * s)], c, 0.9 * s)
    else: fg.line([(x - 2 * s, y - 5 * s), (x, y - 8.5 * s), (x + 2 * s, y - 5 * s)], c, 0.8 * s)
    fg.line([(x + 0.5, y), (x - 9 * s, y + 1.5)], "G", 0.8)
for x, y, s, w in [(110, HZ + 26, 0.7, False), (117, HZ + 27, 0.7, False), (290, HZ + 28, 0.7, True),
                   (228, HZ + 66, 0.9, False), (60, HZ + 100, 1.3, False), (70, HZ + 102, 1.3, False), (78, HZ + 99, 1.3, True)]:
    person(x, y, s, wave=w)
# bunker on the left, earth-bermed
fg.poly([(0, HZ + 40), (30, HZ + 28), (88, HZ + 28), (112, HZ + 42), (0, HZ + 48)], "G", "K", 0.8)
fg.rect(40, HZ + 32, 70, HZ + 40, "K"); fg.rect(44, HZ + 34, 66, HZ + 37, "Y")
fg.line([(56, HZ + 28), (56, HZ + 10)], "K", 0.8); fg.line([(50, HZ + 14), (62, HZ + 14)], "K", 0.6)
# grass: feather-grass tufts thickening toward the viewer, lit gold at the tips
for _ in range(620):
    y = HZ + 60 + (H - HZ - 60) * rng.uniform() ** 0.6
    x = rng.uniform(0, W)
    u = (y - HZ) / (H - HZ)
    hgt = 3 + 18 * u ** 1.5 * rng.uniform(0.5, 1.2)
    lean = rng.uniform(-0.6, 0.2) * hgt
    c = "K" if rng.uniform() < 0.7 else "Y"
    fg.line([(x, y), (x + lean * 0.5, y - hgt * 0.6), (x + lean, y - hgt)], c, 0.5 + u)
    if u > 0.35 and rng.uniform() < 0.35:
        fg.line([(x + lean, y - hgt), (x + lean + 3 * u, y - hgt - 4 * u)], "Y", 0.5 + 0.6 * u)
img = fg.onto(img)
save(img)
