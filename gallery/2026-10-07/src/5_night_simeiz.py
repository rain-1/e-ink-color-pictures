"""5. Night — Simeiz. Where the pictures came down. New moon is on the 10th, so tonight
the near side is dark and the far side stands in full sun; the sky is ours."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from common import *

rng = np.random.default_rng(1959)
ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
SEA = 452
img = np.zeros((H, W, 3), np.uint8)

# --- Milky Way: a diagonal river of faint blue with dark rifts and dense stars
def fbm(seed, scales=(4, 8, 16, 32, 64)):
    r = np.random.default_rng(seed); out = np.zeros((H, W), np.float32)
    for s in scales:
        g = r.normal(0, 1, (H // s + 3, W // s + 3)).astype(np.float32)
        up = np.asarray(Image.fromarray(g).resize(((W // s + 3) * s, (H // s + 3) * s), Image.BICUBIC))[:H, :W]
        out += up * (s / 64) ** 0.6
    return out / 2.2
a, b, c = 0.62, 1.0, -330.0                       # band: a*x + b*y + c = 0
dist = (a * xs + b * ys + c) / math.hypot(a, b)
n1, n2 = fbm(5), fbm(9, (4, 8, 16))
band = np.exp(-(dist / 62) ** 2) * (0.8 + 0.5 * n1)
rift = np.exp(-((dist - 8 + 14 * n2) / 9) ** 2) * (ys > 120) * 0.9
glow = np.clip(band - rift, 0, 1) * (ys < SEA)
th = bayer()
air = np.clip((ys - 300) / (SEA - 300), 0, 1) ** 1.5 * 0.42
img[(glow * 0.75 > th) | (air > th)] = INK["B"]
img[(glow > 0.85) & (th < (glow - 0.85) * 2.5)] = INK["W"]
# stars: density follows the band; a few bright ones with colour
for _ in range(1400):
    x, y = rng.integers(0, W), rng.integers(0, SEA)
    if rng.uniform() < 0.25 + 0.75 * glow[y, x]:
        img[y, x] = INK["W"]
bright = [(rng.integers(10, W - 10), rng.integers(10, 360)) for _ in range(34)]
for (x, y) in bright:
    col = INK[rng.choice(["W", "W", "W", "Y", "R", "B"])]
    img[y, x - 1:x + 2] = col; img[y - 1:y + 2, x] = col
    if rng.uniform() < 0.3:
        img[y, x - 3:x + 4:6] = col; img[y - 3:y + 4:6, x] = col
# Draco, the radiant, and its meteors (peak on the 9th)
draco = [(70, 64), (86, 52), (100, 60), (92, 74), (76, 78), (60, 98), (52, 124), (66, 146), (92, 160), (122, 150), (148, 166)]
L = Layer()
for i in range(len(draco) - 1):
    for k in range(0, 10, 3):
        u0, u1 = k / 10, (k + 1.4) / 10
        (x0, y0), (x1, y1) = draco[i], draco[i + 1]
        L.line([(x0 + (x1 - x0) * u0, y0 + (y1 - y0) * u0), (x0 + (x1 - x0) * u1, y0 + (y1 - y0) * u1)], "B", 0.6)
for (x, y) in draco:
    L.ellipse(x, y, 1.6, 1.6, "W")
L.text((74, 40), "DRACO", "B", 8, "sansb", "mm")
RAD = (82, 66)
for ang, r0, r1 in ((0.55, 60, 190), (1.05, 90, 230), (0.2, 120, 250), (1.35, 40, 120)):
    x0, y0 = RAD[0] + r0 * math.cos(ang), RAD[1] + r0 * math.sin(ang)
    x1, y1 = RAD[0] + r1 * math.cos(ang), RAD[1] + r1 * math.sin(ang)
    n = 16
    for k in range(n):
        u0, u1 = k / n, (k + 1) / n
        w = 0.4 + 2.2 * u1
        c = "R" if u1 < 0.4 else "Y" if u1 < 0.8 else "W"
        L.line([(x0 + (x1 - x0) * u0, y0 + (y1 - y0) * u0), (x0 + (x1 - x0) * u1, y0 + (y1 - y0) * u1)], c, w)
    L.ellipse(x1, y1, 2.2, 2.2, "W")
img = L.onto(img)

# --- the sea: black, with broken reflections
sea = ys >= SEA
img[sea] = INK["K"]
for _ in range(500):
    y = min(H - 1, int(SEA + 2 + (H - SEA - 3) * rng.uniform() ** 1.3))
    x = rng.integers(0, W)
    ln = int(2 + (y - SEA) * 0.12 * rng.uniform(0.5, 1.5))
    img[y, x:x + ln] = INK["B"] if rng.uniform() < 0.8 else INK["W"]

# --- Koshka mountain with the observatory, right; coastal hill, left
def ridge(x0, x1, base, peak_x, peak_y, rough, seed):
    r = np.random.default_rng(seed)
    xsr = np.arange(W, dtype=np.float32)
    yv = base - (base - peak_y) * np.exp(-((xsr - peak_x) / ((x1 - x0) / 3)) ** 2)
    jag = np.cumsum(r.normal(0, 1, W)); jag -= np.linspace(jag[0], jag[-1], W)
    return yv + rough * jag / (np.abs(jag).max() + 1e-6)
rk = ridge(160, 400, SEA + 2, 296, 316, 9, 4)
mtn = ys >= rk[None, :].repeat(H, 0)
img[mtn & (ys < SEA + 30)] = INK["K"]
# a faint blue rim of skyglow on the ridge
rim = mtn & ~np.roll(mtn, 2, 0) & (ys < SEA)
img[rim & (bayer() < 0.6)] = INK["B"]

L = Layer()
# observatory on the summit: three domes, one open and lit
top = int(296)
for (dx, r, opened) in ((-26, 9, False), (0, 13, True), (24, 8, False)):
    x = 296 + dx; base = rk[int(x)] + 2
    L.rect(x - r, base - r * 0.9, x + r, base + 2, "K")
    L.ellipse(x, base - r * 0.9, r, r, "K")
    if opened:
        L.poly([(x - 2.5, base - r * 1.9), (x + 2.5, base - r * 1.9), (x + 3, base - r * 0.9), (x - 3, base - r * 0.9)], "Y")
        L.line([(x, base - r * 1.4), (x - 10, base - r * 3.2)], "Y", 0.8)   # the telescope's tube, dimly
    L.line([(x - r, base - r * 0.9), (x + r, base - r * 0.9)], "B", 0.5)
    for k in range(2):
        L.rect(x - r + 3 + k * r, base - 4, x - r + 5 + k * r, base - 2, "Y")
# the receiving array: a crossed-yagi on a mast, pointed up the sky toward the Moon
mx, my = 342, rk[342] + 2
L.line([(mx, my), (mx, my - 34)], "K", 1.6)
L.line([(mx - 26, my - 46), (mx + 26, my - 22)], "B", 1.2)
for k in range(9):
    u = k / 8
    px, py = mx - 26 + 52 * u, my - 46 + 24 * u
    L.line([(px - 4, py - 8), (px + 4, py + 8)], "B", 0.8)
L.ellipse(mx, my - 34, 2, 2, "R")
# switchback road up the mountain with tiny lamps
for (x, y) in ((214, 444), (232, 430), (252, 418), (270, 402), (282, 386), (300, 372), (262, 412)):
    L.ellipse(x, y, 0.9, 0.9, "Y")
img = L.onto(img)

# reflection of the lit dome in the sea: a wobbling yellow column
for y in range(SEA + 3, H, 3):
    wob = int(3 * math.sin(y * 0.7)) + rng.integers(-2, 3)
    w = max(1, int(2 + (y - SEA) * 0.05))
    if rng.uniform() < 0.8:
        img[y, 296 + wob - w:296 + wob + w] = INK["Y"]

# --- left foreground: a terrace, cypresses, an autumn plane tree, a house, a watcher
L = Layer()
hill = [(0, 380), (40, 384), (80, 400), (120, 420), (160, 446), (190, 470), (220, 520), (240, 600), (0, 600)]
L.poly(hill, "K")
for k, (x, y, hgt, w) in enumerate([(30, 386, 120, 10), (52, 392, 150, 12), (70, 398, 96, 9), (150, 446, 80, 8), (172, 462, 60, 7)]):
    pts = [(x - w, y)]
    for i in range(1, 12):
        u = i / 12
        ww = w * (1 - u) ** 0.8 * (1 + 0.15 * math.sin(i * 2.3 + k))
        pts.append((x - ww, y - hgt * u))
    pts.append((x, y - hgt - 4))
    for i in range(11, 0, -1):
        u = i / 12
        ww = w * (1 - u) ** 0.8 * (1 + 0.15 * math.sin(i * 1.7 + k))
        pts.append((x + ww, y - hgt * u))
    pts.append((x + w, y))
    L.poly(pts, "K")
    # starlit flicks on the right edges (greenish)
    for i in range(2, 11, 2):
        u = i / 12
        ww = w * (1 - u) ** 0.8
        L.line([(x + ww * 0.3, y - hgt * u), (x + ww * 0.9, y - hgt * u + 3)], "G", 0.6)
# the house with lit windows
hx, hy = 92, 430
L.rect(hx, hy - 34, hx + 58, hy + 40, "K")
L.poly([(hx - 6, hy - 34), (hx + 29, hy - 54), (hx + 64, hy - 34)], "K")
L.line([(hx - 6, hy - 34), (hx + 29, hy - 54), (hx + 64, hy - 34)], "R", 0.8)
for (wx, wy, lit) in ((hx + 8, hy - 24, True), (hx + 24, hy - 24, False), (hx + 40, hy - 24, True), (hx + 8, hy - 4, True), (hx + 40, hy - 4, False)):
    if lit:
        L.rect(wx, wy, wx + 10, wy + 13, "Y")
        L.line([(wx + 5, wy), (wx + 5, wy + 13)], "K", 0.8); L.line([(wx, wy + 6), (wx + 10, wy + 6)], "K", 0.8)
    else:
        L.rect(wx, wy, wx + 10, wy + 13, None, "B", 0.6)
L.rect(hx + 24, hy - 6, hx + 34, hy + 14, "R")
L.rect(hx + 46, hy - 66, hx + 54, hy - 40, "K")
# a wisp of chimney smoke against the Milky Way
L.line([(hx + 50, hy - 68), (hx + 46, hy - 80), (hx + 54, hy - 94), (hx + 48, hy - 110)], "B", 1.4)
# light spilling onto the terrace
L.poly([(hx + 8, hy + 40), (hx + 18, hy + 40), (hx + 34, hy + 66), (hx - 6, hy + 66)], "Y")
for x in range(int(hx - 4), int(hx + 34), 6):
    L.line([(x, hy + 66), (x + 2, hy + 40)], "K", 0.6)
# the watcher on the terrace, looking up
wx, wy = 104, 494
L.ellipse(wx, wy - 22, 3.2, 3.2, "K")
L.line([(wx, wy - 19), (wx - 1, wy - 8)], "K", 3.2)
L.line([(wx - 1, wy - 8), (wx - 4, wy)], "K", 1.6); L.line([(wx - 1, wy - 8), (wx + 2, wy)], "K", 1.6)
L.line([(wx, wy - 17), (wx + 6, wy - 26)], "K", 1.4)
L.line([(wx + 2.5, wy - 24), (wx + 1, wy - 21)], "Y", 0.6)  # rim of light on the face
img = L.onto(img)

# the plane tree: recursive, bare-ish, last leaves catching the windowlight
L = Layer()
leaves = []
def branch(x, y, ang, ln, w, depth):
    x2, y2 = x + ln * math.cos(ang), y - ln * math.sin(ang)
    L.line([(x, y), (x2, y2)], "K", w)
    if depth == 0 or ln < 4:
        leaves.append((x2, y2)); return
    for da in (rng.uniform(0.25, 0.55), -rng.uniform(0.25, 0.55)) + ((rng.uniform(-0.15, 0.15),) if rng.uniform() < 0.4 else ()):
        branch(x2, y2, ang + da, ln * rng.uniform(0.66, 0.8), w * 0.7, depth - 1)
branch(20, 600, math.radians(80), 70, 8, 8)
for (x, y) in leaves:
    if rng.uniform() < 0.2 and x < 86:
        d = math.hypot(x - 110, y - 420)
        c = "Y" if d < 110 and rng.uniform() < 0.6 else ("R" if rng.uniform() < 0.6 else "G")
        L.poly([(x - 2, y), (x, y - 2.4), (x + 2, y), (x, y + 2.4)], c)
# falling leaves
for _ in range(14):
    x, y = rng.uniform(20, 220), rng.uniform(400, 590)
    L.poly([(x - 1.8, y), (x, y - 1.2), (x + 1.8, y), (x, y + 1.2)], rng.choice(["R", "Y"]))
# caption
L.text((228, 592), "СИМЕИЗ · 22:00 · new moon in three nights", "B", 9, "sans", "rs")
img = L.onto(img)
save(img)
