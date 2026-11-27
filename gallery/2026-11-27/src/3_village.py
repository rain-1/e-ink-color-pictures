"""Afternoon — Falu red. A village under snow at three o'clock, low sun, long blue shadows."""
import math, random
import numpy as np
from PIL import Image, ImageDraw
from kit import *
rnd = random.Random(1701)
img, d = canvas(WH)
shadow = Image.new("L", (W * S, H * S), 0); sd = ImageDraw.Draw(shadow)
def shpoly(pts): sd.polygon(P(*pts), fill=255)

# ---------- sky ----------
rect(d, 0, 0, 400, 172, fill=Y)
sunx, suny = 66, 104
for i in range(40):
    a = i * math.pi / 20
    line(d, [(sunx + 27 * math.cos(a), suny + 27 * math.sin(a)), (sunx + (36 if i % 2 else 44) * math.cos(a), suny + (36 if i % 2 else 44) * math.sin(a))], WH, 1)
circ(d, sunx, suny, 23, fill=WH, outline=R, w=1.5)
for cy_, x0, x1 in [(36, 150, 330), (48, 200, 390), (60, 20, 150), (78, 240, 360), (26, 30, 120), (92, 280, 400), (120, 120, 250)]:
    for k in range(4):
        o = k * 9; 
        if x0 + o < x1 - o: line(d, [(x0 + o, cy_ + k * 3), (x1 - o, cy_ + k * 3)], WH if k < 3 else R, 1.6 if k < 3 else 0.7)
for bx, by in [(150, 86), (164, 80), (180, 90), (310, 110), (322, 104)]:   # crows
    line(d, [(bx - 4, by - 2), (bx, by), (bx + 4, by - 2.5)], K, 1)
# far hills and forest
hillf = lambda x: 150 - 16 * math.sin(x / 70 + 1) - 7 * math.sin(x / 29)
poly(d, [(0, 200)] + [(x, hillf(x)) for x in range(0, 401, 4)] + [(400, 200)], B)
for x in range(0, 400, 7):
    line(d, [(x, hillf(x) + 4), (x + 10, hillf(x + 10) + 9)], WH, 0.6)
for row in range(3):
    for x in range(-3, 404, 5):
        xx = x + rnd.uniform(-1.5, 1.5); base = 176 + row * 7 + 3 * math.sin(xx / 40 + row); h = rnd.uniform(11, 19)
        poly(d, [(xx - 3.5, base), (xx, base - h), (xx + 3.5, base)], G if (rnd.random() < 0.5 + row * 0.15) else K)
        if rnd.random() < 0.5: line(d, [(xx - 1.5, base - h * 0.45), (xx, base - h * 0.8)], WH, 0.7)

# ---------- helpers ----------
SV = (0.9, 0.22)   # shadow direction per unit height (sun low, upper left)
def spruce(x, y, h, col=G):
    shpoly([(x - 2, y), (x + h * SV[0], y + h * SV[1] - 2), (x + h * SV[0], y + h * SV[1] + 2), (x + 2, y + 2)])
    objs.append((y, lambda: _spruce(x, y, h, col)))
def _spruce(x, y, h, col):
    rect(d, x - 1, y - 5, x + 1, y, fill=K)
    n = max(4, int(h / 5))
    for i in range(n):
        f = i / n; yy = y - 4 - f * (h - 6); wd = (1 - f) * h * 0.27 + 2
        poly(d, [(x - wd, yy + 3), (x, yy - 7), (x + wd, yy + 3)], col, K, 0.6)
        if wd > 3: poly(d, [(x - wd * 0.75, yy + 1.5), (x - 0.5, yy - 5.5), (x + wd * 0.2, yy - 1)], WH)
def birch(x, y, h):
    shpoly([(x - 1, y), (x + h * SV[0], y + h * SV[1] - 1), (x + h * SV[0], y + h * SV[1] + 1), (x + 1, y + 1)])
    objs.append((y, lambda: _birch(x, y, h)))
def _birch(x, y, h):
    r2 = random.Random(int(x * 7 + y))
    def br(x0, y0, a, ln, wd, dep):
        x1, y1 = x0 + math.cos(a) * ln, y0 + math.sin(a) * ln
        line(d, [(x0, y0), (x1, y1)], K, wd)
        if dep:
            for sg in (-1, 1): br(x1, y1, a + sg * r2.uniform(0.25, 0.6), ln * 0.66, max(0.5, wd * 0.7), dep - 1)
    for k in range(7):
        yy = y - h * (0.35 + 0.09 * k); br(x, yy, -math.pi / 2 + (0.8 if k % 2 else -0.8) + r2.uniform(-0.2, 0.2), h * 0.17, 0.9, 3)
    poly(d, [(x - 2.2, y), (x - 0.8, y - h), (x + 0.8, y - h), (x + 2.2, y)], WH, K, 0.7)
    for k in range(int(h / 6)):
        yy = y - 3 - k * 6 - r2.uniform(0, 3); line(d, [(x - 1.8, yy), (x + r2.uniform(-0.5, 1.5), yy)], K, 1)
def smoke(x, y, n=8, sc=1.0):
    for i in range(n):
        circ(d, x + i * 3.5 * sc + 2 * math.sin(i * 1.3), y - i * 7 * sc, (2.5 + i * 0.8) * sc, fill=WH, outline=K, w=0.6)
def window(x, y, w, h, lit=False):
    rect(d, x - 1.2, y - 1.2, x + w + 1.2, y + h + 1.2, fill=WH, outline=K, w=0.5)
    rect(d, x, y, x + w, y + h, fill=Y if lit else K)
    line(d, [(x + w / 2, y), (x + w / 2, y + h)], WH, 0.9); line(d, [(x, y + h * 0.4), (x + w, y + h * 0.4)], WH, 0.9)
def house(x, y, w, h, dz, col=R, door=0.5, lit=(), chim=0.6, therm=False, name=None):
    """oblique house: front wall base-left (x,y); ridge runs along the front."""
    vx, vy = dz * 0.55, -dz * 0.32; rh = dz * 0.42
    ax, ay = x + w + vx / 2, y + vy / 2 - h - rh
    shpoly([(x + w, y), (x + w + vx, y + vy), (x + w + vx + (h + rh) * SV[0], y + vy + (h + rh) * SV[1]), (x + w + (h + rh * 0.3) * SV[0], y + (h + rh * 0.3) * SV[1] + 4), (x + 4, y + 5), (x, y)])
    def draw():
        # gable end (in shade)
        g = [(x + w, y), (x + w + vx, y + vy), (x + w + vx, y + vy - h), (ax, ay), (x + w, y - h)]
        poly(d, g, col)
        for k in range(1, int(vx / 1.6)):
            gx = x + w + k * 1.6; t = (gx - x - w) / vx
            top = (y - h) + (ay - (y - h)) * min(t, 1 - t) * 2 + vy * t
            line(d, [(gx, y + vy * t), (gx, top)], K, 0.5)
        line(d, g + [g[0]], K, 0.9)
        window(x + w + vx * 0.38, y + vy * 0.5 - h * 0.62, vx * 0.26, h * 0.3)
        # front wall
        rect(d, x, y - h, x + w, y, fill=col, outline=K, w=0.9)
        for k in range(1, int(w / 3.2)): line(d, [(x + k * 3.2, y - h), (x + k * 3.2, y)], K, 0.4)
        rect(d, x, y - h, x + 2.4, y, fill=WH, outline=K, w=0.4); rect(d, x + w - 2.4, y - h, x + w, y, fill=WH, outline=K, w=0.4)
        rect(d, x, y - 2.5, x + w, y, fill=K)
        # openings
        dw = min(9, w * 0.16); dx_ = x + w * door - dw / 2
        rect(d, dx_ - 1.5, y - h * 0.62 - 1.5, dx_ + dw + 1.5, y - 2, fill=WH, outline=K, w=0.5); rect(d, dx_, y - h * 0.62, dx_ + dw, y - 2, fill=G if col == R else B)
        circ(d, dx_ + dw - 1.8, y - h * 0.3, 0.7, fill=Y)
        rect(d, dx_ - 3, y - 2, dx_ + dw + 3, y + 1.5, fill=WH, outline=K, w=0.5)
        nwin = max(2, int(w / 17)); ww = min(8, w / nwin * 0.45)
        for k in range(nwin):
            wx = x + w * (k + 0.5) / nwin - ww / 2
            if abs(wx + ww / 2 - (dx_ + dw / 2)) < dw / 2 + ww / 2 + 2: continue
            window(wx, y - h * 0.72, ww, h * 0.36, lit=k in lit)
        if therm:
            tx_ = dx_ + dw + 5; rect(d, tx_, y - h * 0.66, tx_ + 4.5, y - h * 0.2, fill=WH, outline=K, w=0.5)
            line(d, [(tx_ + 2.25, y - h * 0.4), (tx_ + 2.25, y - h * 0.27)], R, 1); circ(d, tx_ + 2.25, y - h * 0.26, 1.3, fill=R)
        # roof: snow, with a dark band where it has slid off the eave
        ov = 3
        rf = [(x - ov, y - h + 1), (x + w + ov * 0.3, y - h + 1), (ax + ov * 0.3, ay), (ax - w - ov, ay)]
        poly(d, rf, WH, K, 0.9)
        e0, e1, r0, r1 = rf[0], rf[1], rf[3], rf[2]
        band = [e0, e1, (e1[0] + (r1[0] - e1[0]) * 0.22, e1[1] + (r1[1] - e1[1]) * 0.22), (e0[0] + (r0[0] - e0[0]) * 0.22, e0[1] + (r0[1] - e0[1]) * 0.22)]
        poly(d, band, K)
        for k in range(1, int(w / 4)):
            f = k / (w / 4); line(d, [(e0[0] + (e1[0] - e0[0]) * f, e0[1]), (band[3][0] + (band[2][0] - band[3][0]) * f, band[3][1])], R, 0.5)
        for k in range(3):                                   # snow drift lines
            f = 0.4 + k * 0.2
            line(d, [(e0[0] + (r0[0] - e0[0]) * f + 4 + k * 5, e0[1] + (r0[1] - e0[1]) * f), (e1[0] + (r1[0] - e1[0]) * f - 9 + k * 3, e1[1] + (r1[1] - e1[1]) * f)], B, 0.5)
        for k in range(int(w / 5)):                           # icicles
            ix = x - ov + 2 + k * 5 + rnd.uniform(-1, 1); line(d, [(ix, y - h + 1.5), (ix, y - h + 3.5 + rnd.uniform(0, 3))], WH, 0.8)
        # chimney + smoke
        cx_ = ax - w * chim; cy_ = ay
        rect(d, cx_ - 3, cy_ - 9, cx_ + 3, cy_ + 2, fill=col, outline=K, w=0.7); rect(d, cx_ - 4, cy_ - 11, cx_ + 4, cy_ - 8.5, fill=WH, outline=K, w=0.5)
        smoke(cx_ + 1, cy_ - 15, 7, 0.9)
    objs.append((y, draw))
def fence(x0, y0, x1, y1, n):
    def draw():
        for i in range(n + 1):
            f = i / n; fx, fy = x0 + (x1 - x0) * f, y0 + (y1 - y0) * f
            line(d, [(fx, fy), (fx + 0.6, fy - 9)], K, 1.1); line(d, [(fx + 2.2, fy), (fx + 1.6, fy - 9)], K, 0.6)
            circ(d, fx + 1, fy - 9.5, 1.2, fill=WH, outline=K, w=0.4)
            if i < n:
                gx, gy = x0 + (x1 - x0) * (i + 1) / n, y0 + (y1 - y0) * (i + 1) / n
                for k in range(3): line(d, [(fx, fy - 1 - k * 2.5), (gx + 2, gy - 4.5 - k * 2.5)], K, 0.6)
    objs.append((max(y0, y1), draw))
    for i in range(n + 1):
        f = i / n; fx, fy = x0 + (x1 - x0) * f, y0 + (y1 - y0) * f
        shpoly([(fx, fy), (fx + 9 * SV[0], fy + 9 * SV[1]), (fx + 9 * SV[0] + 1.5, fy + 9 * SV[1] + 1), (fx + 2, fy + 1)])
def person(x, y, coat, scarf=R, sc=1.0, pose=0):
    shpoly([(x - 1, y), (x + 11 * sc * SV[0], y + 11 * sc * SV[1] - 1), (x + 11 * sc * SV[0], y + 11 * sc * SV[1] + 1), (x + 1.5, y + 1)])
    def draw():
        line(d, [(x - 1.2 * sc, y), (x - 0.4 * sc - pose * 1.5, y - 4.5 * sc)], K, 1.3 * sc); line(d, [(x + 1.6 * sc + pose * 2, y), (x + 0.4 * sc, y - 4.5 * sc)], K, 1.3 * sc)
        poly(d, [(x - 2.4 * sc, y - 4 * sc), (x + 2.4 * sc, y - 4 * sc), (x + 1.8 * sc, y - 9.5 * sc), (x - 1.8 * sc, y - 9.5 * sc)], coat, K, 0.5)
        line(d, [(x - 2 * sc, y - 9 * sc), (x - 4 * sc - pose, y - 6 * sc)], K, 1.1 * sc); line(d, [(x + 2 * sc, y - 9 * sc), (x + 4 * sc + pose * 2, y - 7 * sc - pose * 2)], K, 1.1 * sc)
        circ(d, x, y - 11.3 * sc, 1.9 * sc, fill=WH, outline=K, w=0.5); poly(d, [(x - 2 * sc, y - 12 * sc), (x, y - 15 * sc), (x + 2 * sc, y - 12 * sc)], scarf)
        line(d, [(x - 2 * sc, y - 9.4 * sc), (x + 2 * sc, y - 9.4 * sc)], scarf, 1.1 * sc)
    objs.append((y, draw))
objs = []

# ---------- frozen lake with skaters ----------
lake = [(118 + 104 * math.cos(a) + 8 * math.sin(3 * a), 262 + 30 * math.sin(a) + 3 * math.cos(5 * a)) for a in [i * math.pi / 30 for i in range(60)]]
poly(d, lake, B, K, 0.9)
for i in range(60):
    if i % 3 == 0:
        x, y = lake[i]; line(d, [(x, y), (118 + (x - 118) * 0.93, 262 + (y - 262) * 0.9)], WH, 0.6)
for _ in range(11):                                  # skate traces
    cx_, cy_ = rnd.uniform(50, 185), rnd.uniform(246, 278); rr = rnd.uniform(8, 26); a0 = rnd.uniform(0, 6); a1 = a0 + rnd.uniform(1.5, 4.5)
    line(d, [(cx_ + rr * math.cos(a0 + (a1 - a0) * k / 14), cy_ + rr * 0.35 * math.sin(a0 + (a1 - a0) * k / 14)) for k in range(15)], WH, 0.6)
# reeds
for i in range(26):
    x = 205 + rnd.uniform(-10, 16); y = 262 + rnd.uniform(-22, 22)
    line(d, [(x, y), (x + rnd.uniform(-2, 2), y - rnd.uniform(6, 12))], K, 0.6)

# ---------- the village (painter's order by base y) ----------
# back row
def church(x, y):
    shpoly([(x + 44, y), (x + 60, y - 5), (x + 60 + 70 * SV[0], y - 5 + 70 * SV[1]), (x + 44 + 40 * SV[0], y + 40 * SV[1]), (x, y + 5)])
    def draw():
        poly(d, [(x + 44, y), (x + 60, y - 6), (x + 60, y - 30), (x + 52, y - 40), (x + 44, y - 26)], WH, K, 0.8)
        for k in range(1, 10): line(d, [(x + 44 + k * 1.6, y - k * 0.6), (x + 44 + k * 1.6, y - 28 - min(k, 10 - k) * 2)], B, 0.5)
        rect(d, x + 12, y - 26, x + 44, y, fill=WH, outline=K, w=0.9)
        poly(d, [(x + 10, y - 25), (x + 45, y - 25), (x + 53, y - 40), (x + 18, y - 40)], K)
        for k in range(8): line(d, [(x + 12 + k * 4.4, y - 25.5), (x + 19 + k * 4.4, y - 39.5)], WH, 0.4)
        for k in range(3):
            wx = x + 17 + k * 9; rect(d, wx, y - 18, wx + 4, y - 6, fill=Y, outline=K, w=0.6); circ(d, wx + 2, y - 18, 2, fill=Y, outline=K, w=0.6)
        rect(d, x, y - 44, x + 14, y, fill=WH, outline=K, w=0.9)
        poly(d, [(x - 2, y - 44), (x + 7, y - 78), (x + 16, y - 44)], K)
        line(d, [(x + 7, y - 78), (x + 7, y - 88)], K, 1); line(d, [(x + 4, y - 84), (x + 10, y - 84)], K, 1)
        circ(d, x + 7, y - 33, 4, fill=Y, outline=K, w=0.7); line(d, [(x + 7, y - 33), (x + 7, y - 36)], K, 0.6); line(d, [(x + 7, y - 33), (x + 9, y - 32)], K, 0.6)
        rect(d, x + 4.5, y - 12, x + 9.5, y, fill=R, outline=K, w=0.5)
    objs.append((y, draw))
church(286, 226)
house(18, 222, 40, 17, 16, lit=(0,), chim=0.4)
house(96, 216, 34, 15, 14, col=Y, lit=())
house(196, 224, 36, 16, 15, lit=(1,), chim=0.7)
house(358, 232, 40, 17, 14, lit=(0,))
for x, y, h in [(8, 228, 34), (78, 222, 30), (150, 226, 38), (168, 222, 28), (262, 224, 34), (346, 222, 40), (392, 240, 36)]: spruce(x, y, h, G if rnd.random() < 0.6 else K)
for i in range(5): person(60 + i * 26 + rnd.uniform(-6, 6), 256 + rnd.uniform(-8, 20), [R, K, Y, G, R][i], scarf=[Y, R, R, Y, K][i], sc=0.9, pose=rnd.choice([0, 1, 2]))
# middle rows
house(236, 318, 62, 24, 24, lit=(0, 2), chim=0.3)
house(330, 300, 44, 20, 18, col=Y, lit=(1,))
house(20, 356, 70, 26, 26, lit=(1, 3), chim=0.65)
house(138, 372, 46, 21, 20, lit=(0,), chim=0.5)
fence(228, 340, 330, 352, 9); fence(8, 380, 120, 392, 10)
for x, y, h in [(222, 300, 46), (312, 296, 36), (386, 316, 52), (118, 344, 44), (206, 364, 50), (4, 330, 40)]: spruce(x, y, h, G if rnd.random() < 0.7 else K)
birch(302, 338, 58); birch(128, 392, 52)
# woodpile
def woodpile(x, y):
    def draw():
        rect(d, x, y - 12, x + 26, y, fill=Y, outline=K, w=0.8)
        for r_ in range(3):
            for c_ in range(6): circ(d, x + 2.6 + c_ * 4.2, y - 2.3 - r_ * 3.9, 1.9, fill=Y, outline=K, w=0.5)
        poly(d, [(x - 2, y - 12), (x + 28, y - 12), (x + 26, y - 16), (x, y - 16)], WH, K, 0.6)
    shpoly([(x + 26, y), (x + 26 + 14, y + 4), (x + 4, y + 5)])
    objs.append((y, draw))
woodpile(188, 392)
# flagpole
def flag(x, y):
    shpoly([(x, y), (x + 80 * SV[0], y + 80 * SV[1] - 1), (x + 80 * SV[0], y + 80 * SV[1] + 1), (x + 1, y + 1)])
    def draw():
        line(d, [(x, y), (x, y - 86)], K, 1.6); line(d, [(x - 0.3, y), (x - 0.3, y - 86)], WH, 0.6); circ(d, x, y - 87, 1.8, fill=Y, outline=K, w=0.5)
        fl = [(x + 1, y - 84), (x + 33, y - 82), (x + 33, y - 62), (x + 1, y - 64)]
        poly(d, fl, B, K, 0.7)
        poly(d, [(x + 9, y - 83.5), (x + 14, y - 83.2), (x + 14, y - 63.2), (x + 9, y - 63.5)], Y)
        poly(d, [(x + 1, y - 76.5), (x + 33, y - 74.5), (x + 33, y - 70), (x + 1, y - 72)], Y)
    objs.append((y, draw))
flag(112, 470)
# front row
house(196, 512, 128, 44, 44, lit=(0, 2, 5), door=0.42, chim=0.7, therm=True)
house(8, 486, 78, 32, 30, lit=(1,), door=0.3, chim=0.4)
fence(150, 560, 400, 584, 14)
birch(366, 548, 96); birch(170, 520, 80)
for x, y, h in [(128, 498, 62), (388, 500, 70), (104, 560, 44)]: spruce(x, y, h, G)
# snowman, sled, children, dog
def snowman(x, y):
    shpoly([(x, y), (x + 22, y + 4), (x + 22, y + 9), (x, y + 4)])
    def draw():
        circ(d, x, y - 7, 8, fill=WH, outline=K, w=0.9); circ(d, x, y - 19, 5.5, fill=WH, outline=K, w=0.9); circ(d, x, y - 28, 4, fill=WH, outline=K, w=0.9)
        rect(d, x - 3.5, y - 36, x + 3.5, y - 31, fill=K); line(d, [(x - 5.5, y - 31), (x + 5.5, y - 31)], K, 1.3)
        poly(d, [(x + 1, y - 28), (x + 8, y - 27), (x + 1, y - 26.5)], R); circ(d, x - 1.5, y - 29.5, 0.7, fill=K); circ(d, x + 1.5, y - 29.5, 0.7, fill=K)
        for k in range(3): circ(d, x, y - 22 + k * 4, 0.8, fill=K)
        line(d, [(x - 5, y - 20), (x - 14, y - 26)], K, 0.9); line(d, [(x + 5, y - 20), (x + 14, y - 27)], K, 0.9); line(d, [(x - 4, y - 24), (x + 4, y - 23.5)], R, 1.6)
    objs.append((y, draw))
snowman(52, 556)
person(84, 566, B, scarf=R, sc=1.5, pose=2); person(26, 572, R, scarf=Y, sc=1.3, pose=1)
def sled(x, y):
    def draw():
        line(d, [(x, y), (x + 22, y), (x + 26, y - 4)], K, 1); rect(d, x + 2, y - 4.5, x + 20, y - 2.5, fill=R, outline=K, w=0.5)
        line(d, [(x + 5, y - 2.5), (x + 5, y)], K, 0.7); line(d, [(x + 17, y - 2.5), (x + 17, y)], K, 0.7); line(d, [(x + 26, y - 4), (x + 40, y - 12)], K, 0.5)
    objs.append((y, draw))
sled(122, 586)
def dog(x, y):
    def draw():
        ell(d, x, y - 5, 6, 3, fill=K); circ(d, x + 6.5, y - 8, 2.6, fill=K); poly(d, [(x + 5, y - 10), (x + 6, y - 13), (x + 7.5, y - 10)], K)
        for lx in (-4, -2, 3, 5): line(d, [(x + lx, y - 3), (x + lx, y)], K, 1)
        line(d, [(x - 6, y - 6), (x - 9, y - 11)], K, 1)
    shpoly([(x - 4, y), (x + 12, y + 2), (x + 12, y + 4), (x - 4, y + 2)])
    objs.append((y, draw))
dog(156, 590)

# ---------- ground: drifts, paths, then shadows screened in blue ----------
for _ in range(70):
    x = rnd.uniform(0, 400); y = rnd.uniform(215, 598); ln = rnd.uniform(8, 30)
    line(d, [(x + k, y - 1.5 * math.sin(k / ln * math.pi)) for k in range(0, int(ln), 3)], B, 0.5)
def path(pts, n=40):
    for i in range(n):
        f = i / (n - 1) * (len(pts) - 1); k = min(int(f), len(pts) - 2); t = f - k
        x = pts[k][0] + (pts[k + 1][0] - pts[k][0]) * t; y = pts[k][1] + (pts[k + 1][1] - pts[k][1]) * t
        ell(d, x + (1.5 if i % 2 else -1.5), y, 1.3, 0.8, fill=B)
path([(250, 514), (240, 540), (200, 556), (150, 600)], 30); path([(266, 320), (250, 350), (200, 400), (160, 420), (120, 470), (60, 490)], 60)
path([(60, 358), (70, 380), (140, 400)], 24); path([(292, 228), (280, 250), (265, 290)], 20); path([(230, 262), (250, 280), (262, 300)], 12)
a = np.asarray(img).copy(); m = np.asarray(shadow) > 0
yy, xx = np.mgrid[0:H * S, 0:W * S]
pat = (((xx // S) + (yy // S)) % 2 == 0)
white = (a == 255).all(-1)
a[m & white & pat] = B
img = Image.fromarray(a); d = ImageDraw.Draw(img); d.fontmode = "1"
for y, fn in sorted(objs, key=lambda o: o[0]): fn()
finish(img, None, ink=(K,))
