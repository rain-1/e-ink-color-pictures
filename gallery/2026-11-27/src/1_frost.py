"""Morning — Frost on the pane, seven below. Window, dawn, frost ferns, amaryllis."""
import math, random
import numpy as np
from kit import *
rnd = random.Random(27)

# ---------- sky (1x tone, screened) ----------
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
cloud = (np.sin(xx / 47 + yy / 9) + np.sin(xx / 23 - yy / 6 + 2) * 0.6 + np.sin(xx / 90 + yy / 15 + 1)) * 0.07
bg = np.zeros((H, W, 3), np.uint8)
bay = bayer()
t1 = np.clip((yy - 10) / 150 + cloud, 0, 1)            # blue -> white
t2 = np.clip((yy - 150) / 95 + cloud * 1.6, 0, 1)      # white -> yellow
t3 = np.clip((yy - 250) / 95 + cloud * 2.2, 0, 1)      # yellow -> red
bg[:] = screen(t1, B, WH, bay)
m = yy > 150; bg[m] = screen(t2, WH, Y, bay)[m]
m = yy > 250; bg[m] = screen(t3, Y, R, bay)[m]
img, d = canvas(bg)

# ---------- landscape ----------
HZ = 338
circ(d, 128, HZ + 4, 30, fill=WH); circ(d, 128, HZ + 4, 25, fill=Y, outline=R, w=1)
# far ridge
ridge = [(0, HZ)] + [(x, HZ - 14 - 9 * math.sin(x / 37) - 5 * math.sin(x / 13 + 1)) for x in range(0, 401, 4)] + [(400, 400), (0, 400)]
poly(d, ridge, B)
for x in range(2, 400, 5):                       # tree line on the ridge
    y = HZ - 14 - 9 * math.sin(x / 37) - 5 * math.sin(x / 13 + 1)
    hgt = rnd.uniform(5, 11)
    poly(d, [(x - 2.5, y + 1), (x, y - hgt), (x + 2.5, y + 1)], K)
# snowfield
field = [(0, HZ + 18)] + [(x, HZ + 12 + 7 * math.sin(x / 60 + 2)) for x in range(0, 401, 5)] + [(400, 540), (0, 540)]
poly(d, field, WH)
# blue shadow hatching following the slope
for i in range(46):
    y0 = HZ + 22 + i * 4.2
    x0 = rnd.uniform(-20, 380); ln = rnd.uniform(20, 110)
    pts = [(x0 + k, y0 + 3 * math.sin((x0 + k) / 50 + i)) for k in range(0, int(ln), 6)]
    if len(pts) > 1: line(d, pts, B, 0.8)
# long dawn shadows + spruces
def spruce(x, y, h, col=K, snow=True):
    line(d, [(x, y), (x, y - h)], K, 1.2)
    n = int(h / 4.5)
    for i in range(n):
        f = i / n
        yy_ = y - 3 - f * (h - 4); wd = (1 - f) * h * 0.26 + 1.5
        poly(d, [(x - wd, yy_ + 3), (x, yy_ - 5), (x + wd, yy_ + 3)], col)
        if snow and i % 2 == 0 and wd > 3:
            line(d, [(x - wd * 0.7, yy_ + 1.5), (x - 1, yy_ - 2.5)], WH, 1)
trees = sorted([(rnd.uniform(0, 400), HZ + rnd.uniform(14, 70), 0) for _ in range(26)], key=lambda t: t[1])
for x, y, _ in trees:
    if (200 < x < 300 and y < HZ + 50) or 85 < x < 175: continue
    h = 22 + (y - HZ) * 0.75 + rnd.uniform(-4, 6)
    poly(d, [(x, y), (x + h * 1.9, y + h * 0.33), (x + h * 1.9, y + h * 0.33 + 3)], B)   # shadow, sun at left
    spruce(x, y, h, G if rnd.random() < 0.45 else K)
# red cottage
hx, hy = 232, HZ + 44
poly(d, [(hx, hy), (hx + 95, hy + 30), (hx + 95, hy + 36), (hx, hy + 5)], B)
rect(d, hx, hy - 22, hx + 44, hy, fill=R, outline=K, w=0.8)
for bx in range(hx + 4, hx + 44, 4): line(d, [(bx, hy - 21), (bx, hy)], K, 0.5)
poly(d, [(hx - 4, hy - 21), (hx + 22, hy - 38), (hx + 48, hy - 21)], WH, K, 0.9)
poly(d, [(hx - 4, hy - 21), (hx + 48, hy - 21), (hx + 46, hy - 18), (hx - 2, hy - 18)], K)
rect(d, hx + 6, hy - 14, hx + 14, hy - 5, fill=Y, outline=WH, w=0.9); line(d, [(hx + 10, hy - 14), (hx + 10, hy - 5)], WH, 0.7)
rect(d, hx + 30, hy - 14, hx + 38, hy - 5, fill=Y, outline=WH, w=0.9); line(d, [(hx + 34, hy - 14), (hx + 34, hy - 5)], WH, 0.7)
rect(d, hx + 18, hy - 15, hx + 26, hy, fill=WH, outline=K, w=0.7)
rect(d, hx + 31, hy - 42, hx + 37, hy - 30, fill=R, outline=K, w=0.7)
for i in range(9):                                   # smoke
    circ(d, hx + 35 + i * 3.2 + 3 * math.sin(i), hy - 46 - i * 9, 3 + i * 0.9, fill=WH, outline=B, w=0.6)
# fence
for i in range(14):
    fx = 150 + i * 13; fy = HZ + 86 + i * 2.2
    line(d, [(fx, fy), (fx, fy - 11)], K, 1.3)
    if i < 13:
        line(d, [(fx, fy - 8), (fx + 13, fy - 5.8)], K, 0.8); line(d, [(fx, fy - 4), (fx + 13, fy - 1.8)], K, 0.8)
# hare tracks
for i in range(22):
    tx = 20 + i * 9; ty = HZ + 120 + 14 * math.sin(i / 4)
    circ(d, tx, ty, 1, fill=B); circ(d, tx + 3, ty - 2, 1, fill=B)

# ---------- frost ferns ----------
segs = []
def frond(x, y, ang, ln, depth, wd):
    n = max(3, int(ln / 5)); step = ln / n; curve = rnd.uniform(-0.035, 0.035)
    for i in range(n):
        nx, ny = x + math.cos(ang) * step, y + math.sin(ang) * step
        segs.append((x, y, nx, ny, wd * (1 - 0.5 * i / n)))
        x, y = nx, ny; ang += curve
        if depth > 0 and i > 0:
            rem = ln * (1 - i / n)
            for sgn in (-1, 1):
                if rnd.random() < 0.92:
                    frond(x, y, ang + sgn * math.radians(rnd.uniform(48, 62)), rem * rnd.uniform(0.32, 0.5), depth - 1, wd * 0.7)
panes = [(22, 22, 194, 232), (206, 22, 378, 232), (22, 244, 194, 520), (206, 244, 378, 520)]
for (x0, y0, x1, y1) in panes:
    # corners grow big, edges grow small
    for cx, cy, a0 in [(x0, y1, -45), (x1, y1, -135), (x0, y0, 45), (x1, y0, 135)]:
        big = cy == y1
        for k in range(5 if big else 3):
            frond(cx, cy, math.radians(a0 + rnd.uniform(-40, 40)), (rnd.uniform(70, 150) if y1 > 300 else rnd.uniform(55, 100)) if big else rnd.uniform(25, 60), 3 if big else 2, 1.6)
    for k in range(16):
        bx = rnd.uniform(x0, x1)
        frond(bx, y1, math.radians(-90 + rnd.uniform(-35, 35)), rnd.uniform(14, 46), 2, 1.2)
    for k in range(9):
        by = rnd.uniform(y0, y1); side = rnd.random() < 0.5
        frond(x0 if side else x1, by, math.radians((0 if side else 180) + rnd.uniform(-35, 35)), rnd.uniform(10, 30), 2, 1.1)
for x, y, nx, ny, wd in segs: line(d, [(x + 1, y + 1), (nx + 1, ny + 1)], B, wd)
for x, y, nx, ny, wd in segs: line(d, [(x, y), (nx, ny)], WH, wd)
# rime crust + sparkle along the bottom of each pane
for (x0, y0, x1, y1) in panes:
    for k in range(260):
        px = rnd.uniform(x0, x1); py = y1 - abs(rnd.gauss(0, 9))
        circ(d, px, py, rnd.uniform(0.6, 1.6), fill=WH)
    for k in range(40):
        px = rnd.uniform(x0, x1); py = y1 - abs(rnd.gauss(0, 14)); circ(d, px, py, 0.6, fill=B)

# ---------- window frame ----------
def bar(x0, y0, x1, y1):
    rect(d, x0, y0, x1, y1, fill=WH, outline=K, w=0.9)
rect(d, 0, 0, 400, 22, fill=WH); rect(d, 0, 0, 22, 600, fill=WH); rect(d, 378, 0, 400, 600, fill=WH)
rect(d, 21, 21, 379, 521, outline=K, w=1.2)
rect(d, 6, 6, 394, 600, outline=B, w=0.8); rect(d, 9, 9, 391, 600, outline=K, w=0.6)
bar(194, 22, 206, 520); bar(22, 232, 378, 244)
line(d, [(200, 26), (200, 228)], B, 0.6); line(d, [(200, 248), (200, 516)], B, 0.6); line(d, [(26, 238), (190, 238)], B, 0.6); line(d, [(210, 238), (374, 238)], B, 0.6)
# latch
rect(d, 196, 300, 204, 330, fill=Y, outline=K, w=0.8); circ(d, 200, 315, 5, fill=Y, outline=K, w=0.8); line(d, [(200, 315), (212, 322)], K, 2)

# ---------- outdoor thermometer on the mullion (upper right pane) ----------
tx, ty, th = 214, 58, 150
rect(d, tx, ty, tx + 26, ty + th, fill=WH, outline=K, w=1.2)
rect(d, tx + 2, ty + 2, tx + 24, ty + th - 2, outline=B, w=0.6)
circ(d, tx + 13, ty + 6, 1.6, fill=K); circ(d, tx + 13, ty + th - 5, 1.6, fill=K)
top, bot = ty + 14, ty + th - 24          # +30 .. -30
def ty_of(v): return bot - (v + 30) / 60 * (bot - top)
rect(d, tx + 11, top - 3, tx + 15, bot + 4, fill=WH, outline=K, w=0.8)
rect(d, tx + 12, ty_of(-7), tx + 14, bot + 4, fill=R)
circ(d, tx + 13, bot + 9, 5.5, fill=R, outline=K, w=0.9); circ(d, tx + 11.5, bot + 7.5, 1.3, fill=WH)
for v in range(-30, 31, 2):
    yv = ty_of(v); L = 5 if v % 10 == 0 else 2.5
    line(d, [(tx + 16.5, yv), (tx + 16.5 + L, yv)], K, 0.8 if v % 10 == 0 else 0.5)
    line(d, [(tx + 9.5 - L, yv), (tx + 9.5, yv)], K, 0.8 if v % 10 == 0 else 0.5)

# ---------- sill, cup, amaryllis, book ----------
rect(d, 0, 520, 400, 600, fill=Y)
for i in range(11):
    y = 526 + i * 5.5
    line(d, [(x, y + 1.5 * math.sin(x / 31 + i * 1.7)) for x in range(0, 401, 8)], K, 0.5)
line(d, [(0, 520), (400, 520)], K, 1.5)
rect(d, 0, 584, 400, 600, fill=K); line(d, [(0, 590), (400, 590)], Y, 0.6)
# amaryllis
px, py = 318, 578
poly(d, [(px - 26, py - 40), (px + 26, py - 40), (px + 20, py), (px - 20, py)], R, K, 1)
rect(d, px - 29, py - 46, px + 29, py - 38, fill=R, outline=K, w=1)
for i in range(6): line(d, [(px - 22 + i * 9, py - 34), (px - 19 + i * 8, py - 4)], K, 0.5)
ell(d, px, py - 46, 12, 5, fill=K)
def leaf(ax, ay, bx, by, bend, wd):
    L, Rr = [], []
    for i in range(13):
        t = i / 12
        x = ax + (bx - ax) * t + bend * math.sin(t * math.pi) ; y = ay + (by - ay) * t
        w_ = wd * math.sin(min(1, t * 1.25 + 0.15) * math.pi) ** 0.6 * (1 - t * 0.4)
        L.append((x - w_, y)); Rr.append((x + w_, y))
    poly(d, L + Rr[::-1], G, K, 0.8)
    line(d, [((l[0] + r[0]) / 2, l[1]) for l, r in zip(L, Rr)], K, 0.5)
leaf(px - 4, py - 46, px - 62, py - 150, -8, 7); leaf(px + 5, py - 46, px + 44, py - 190, 16, 7); leaf(px - 1, py - 46, px - 30, py - 215, 10, 6)
stem = [(px + 1, py - 46), (px + 3, py - 130), (px + 1, py - 215), (px - 3, py - 262)]
line(d, stem, K, 6.5); line(d, stem, G, 4.5)
def bloom(cx, cy, ang, sc):
    for k in range(6):
        a = ang + k * math.pi / 3; ln = 30 * sc; wd = 11 * sc
        tip = (cx + math.cos(a) * ln, cy + math.sin(a) * ln * 0.8)
        l = (cx + math.cos(a - 0.5) * wd * 1.3, cy + math.sin(a - 0.5) * wd * 1.1); r = (cx + math.cos(a + 0.5) * wd * 1.3, cy + math.sin(a + 0.5) * wd * 1.1)
        poly(d, [(cx, cy), l, tip, r], R, K, 0.8)
        line(d, [(cx, cy), ((cx + tip[0]) / 2, (cy + tip[1]) / 2)], WH, 0.8)
    circ(d, cx, cy, 4 * sc, fill=G)
    for k in range(5):
        a = ang + 0.3 + k * 1.2; ex, ey = cx + math.cos(a) * 12 * sc, cy + math.sin(a) * 10 * sc
        line(d, [(cx, cy), (ex, ey)], Y, 0.9); circ(d, ex, ey, 1.6, fill=Y, outline=K, w=0.4)
bloom(px - 30, py - 272, 0.3, 1.5); bloom(px + 26, py - 262, 0.9, 1.3)
poly(d, [(px - 5, py - 262), (px - 1, py - 300), (px + 4, py - 262)], G, K, 0.8)   # bud
# cup with steam
cx, cy = 92, 572
for k in range(3):
    line(d, [(cx - 10 + k * 10 + 5 * math.sin(t / 7 + k * 2), cy - 30 - t) for t in range(0, 64, 3)], K, 3)
    line(d, [(cx - 10 + k * 10 + 5 * math.sin(t / 7 + k * 2), cy - 30 - t) for t in range(0, 64, 3)], WH, 1.6)
ell(d, cx, cy + 3, 34, 7, fill=WH, outline=K, w=1); ell(d, cx, cy + 2, 24, 4, outline=B, w=0.6)
poly(d, [(cx - 20, cy - 26), (cx + 20, cy - 26), (cx + 15, cy + 2), (cx - 15, cy + 2)], WH, K, 1)
ell(d, cx, cy - 26, 20, 5, fill=K); ell(d, cx, cy - 25.5, 17, 3.2, fill=R)
ell(d, cx + 23, cy - 13, 7, 9, outline=K, w=2)
for k in range(7):
    bx = cx - 17 + k * 5.6; line(d, [(bx, cy - 17), (bx + 2.5, cy - 12), (bx + 5, cy - 17)], B, 1)
line(d, [(cx - 18, cy - 8), (cx + 18, cy - 8)], B, 1.2)
# book + spoon
poly(d, [(150, 566), (236, 560), (240, 574), (154, 581)], B, K, 1); poly(d, [(154, 581), (240, 574), (240, 579), (155, 586)], WH, K, 0.8)
for k in range(3): line(d, [(156, 582.5 + k * 1.2), (239, 575.5 + k * 1.2)], K, 0.3)
poly(d, [(162, 569), (228, 564.5), (229, 568), (163, 572.5)], Y)

finish(img, None, ink=(K,))
