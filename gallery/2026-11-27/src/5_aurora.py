"""Night — The needle trembles. Aurora over the snow; Celsius and Hiorter, Uppsala 1741, found it moves the compass."""
import math, random
import numpy as np
from PIL import Image, ImageDraw
from kit import *
rnd = random.Random(1741); rng = np.random.default_rng(1741)

def smooth1(a, sig):
    k = np.exp(-0.5 * (np.arange(-int(3 * sig), int(3 * sig) + 1) / sig) ** 2); k /= k.sum()
    return np.convolve(np.pad(a, len(k) // 2, mode="wrap"), k, mode="valid")
def rays(seed):
    r = np.random.default_rng(seed)
    f = smooth1(r.random(W + 200), 1.6); c = smooth1(r.random(W + 200), 14)
    f = (f - f.min()) / (np.ptp(f)); c = (c - c.min()) / (np.ptp(c))
    return 0.25 + 0.75 * (0.55 * f + 0.45 * c) * (0.4 + 0.6 * c)

yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
Ig = np.zeros((H, W), np.float32); Ir = np.zeros((H, W), np.float32)
curt = [  # y0, amp1, L1, ph1, amp2, L2, height, strength, seed
    (318, 46, 92, 0.4, 12, 29, 92, 1.00, 1),
    (196, 30, 70, 2.6, 9, 23, 62, 0.8, 2),
    (396, 18, 120, 4.0, 6, 37, 46, 0.6, 3),
]
for (y0, a1, L1, p1, a2, L2, hg, st, seed) in curt:
    yb = y0 + a1 * np.sin(xx / L1 + p1) + a2 * np.sin(xx / L2 + p1 * 2)
    slope = np.abs(a1 / L1 * np.cos(xx / L1 + p1) + a2 / L2 * np.cos(xx / L2 + 2 * p1))
    ry = rays(seed)
    xs = np.clip(xx + (xx - 200) * (yb - yy) / 900 + 100, 0, W + 199).astype(int)      # rays fan from a vanishing point
    r = ry[xs] * (0.75 + 0.9 * np.clip(slope, 0, 0.6))
    dh = yb - yy
    hloc = hg * (0.6 + 0.8 * ry[xs])
    I = np.where(dh > 0, np.exp(-np.clip(dh, 0, None) / hloc) ** 1.5 * (1 - np.exp(-np.clip(dh, 0, None) / 3.0)), np.exp(np.clip(dh, -60, 0) / 2.0) * 0.5) * r * st
    Ig = np.maximum(Ig, I) + 0.25 * np.minimum(Ig, I)
    Ir = np.maximum(Ir, np.exp(-((dh / hloc - 1.7) / 0.6) ** 2) * r * st * 0.62 * (dh > 0))
Ig = np.clip(Ig * 1.25, 0, 1)

bay = bayer()
bg = np.zeros((H, W, 3), np.uint8)
bg[Ir > bay * 1.5 + 0.12] = R
bg[Ig > bay * 0.85 + 0.1] = G
bg[Ig > 0.74 + bay * 0.5] = WH
# stars where the sky is dark
dark = (Ig < 0.16) & (Ir < 0.2)
for _ in range(520):
    x, y = int(rng.integers(0, W)), int(rng.integers(0, 440))
    if dark[y, x]:
        bg[y, x] = WH
        if rng.random() < 0.13 and x + 1 < W: bg[y, x + 1] = WH; bg[y + 1, x] = WH; bg[y + 1, x + 1] = WH
# lake: the aurora again, upside down and broken by ice
LY0, LY1 = 452, 504
for y in range(LY0, LY1):
    src = int(LY0 - 40 - (y - LY0) * 6.5)
    if src < 0: break
    row = np.clip(Ig[src] * 1.6, 0, 1) * (0.9 - 0.3 * (y - LY0) / (LY1 - LY0))
    shift = int(2 * math.sin(y * 1.3))
    row = np.roll(row, shift)
    line_ = np.zeros((W, 3), np.uint8)
    if y % 3 != 0:
        line_[row > bay[y] * 0.8 + 0.1] = G
        line_[row > 0.72 + bay[y] * 0.5] = WH
    else:
        line_[bay[y] < 0.3] = B
    bg[y] = line_
# snow: near-black blue
low = smooth1(rng.random(W), 20); low = (low - low.min()) / np.ptp(low)
t = 0.30 + 0.25 * (yy - LY1) / (H - LY1) + 0.25 * low[None, :] * np.sin(yy / 13.0 + xx / 50.0)
snow = screen(t, K, B, bay)
m = yy >= LY1; bg[m] = snow[m]
gl = (rng.random((H, W)) < 0.012) & m; bg[gl] = WH
img, d = canvas(bg)

# ---------- the Plough and the Pole Star ----------
dip = [(0, 0), (4, 23), (33, 30), (38, 9), (62, 3), (84, -6), (108, 4)]
ca, sa = math.cos(math.radians(30)), math.sin(math.radians(30)); ox, oy = 110, 150
D = [(ox + x * ca - y * sa, oy + x * sa + y * ca) for x, y in dip]
for (x, y) in D:
    circ(d, x, y, 3.2, fill=K); circ(d, x, y, 1.7, fill=WH)
px, py = D[0][0] + (D[0][0] - D[1][0]) * 5, D[0][1] + (D[0][1] - D[1][1]) * 5
circ(d, px, py, 5, fill=K); circ(d, px, py, 2, fill=WH); line(d, [(px - 6, py), (px + 6, py)], WH, 0.7); line(d, [(px, py - 6), (px, py + 6)], WH, 0.7)
# waning gibbous moon, low in the north-east
mx, my = 362, 366
circ(d, mx, my, 14, fill=K); circ(d, mx, my, 11, fill=WH)
ell(d, mx + 8.5, my + 1, 5, 11.5, fill=K)
for (qx, qy, qr) in [(-4, -3, 2.4), (-1, 4, 1.8), (-6, 3, 1.3), (1, -5, 1.2)]: circ(d, mx + qx, my + qy, qr, fill=B)

# ---------- far shore, forest ----------
shore = lambda x: LY0 - 3 - 5 * math.sin(x / 45 + 1) - 2 * math.sin(x / 13)
poly(d, [(0, LY0 + 3)] + [(x, shore(x)) for x in range(0, 401, 4)] + [(400, LY0 + 3)], K)
for x in range(0, 402, 3):
    h = rnd.uniform(8, 24) * (0.7 + 0.5 * math.sin(x / 31) ** 2)
    poly(d, [(x - 3, shore(x) + 2), (x, shore(x) - h), (x + 3, shore(x) + 2)], K)
def spruce(x, y, h, snowy=True):
    rect(d, x - 1.5, y - 6, x + 1.5, y, fill=K)
    n = max(5, int(h / 7))
    for i in range(n):
        f = i / n; yy_ = y - 5 - f * (h - 8); wd = (1 - f) * h * 0.25 + 2.5
        poly(d, [(x - wd, yy_ + 4), (x - wd * 0.5, yy_ - 2), (x, yy_ - 10), (x + wd * 0.5, yy_ - 2), (x + wd, yy_ + 4), (x + wd * 0.4, yy_ + 2), (x, yy_ + 5), (x - wd * 0.4, yy_ + 2)], K)
        if snowy and wd > 4:
            poly(d, [(x - wd * 0.85, yy_ + 2.5), (x - wd * 0.4, yy_ - 2), (x - 0.5, yy_ - 8), (x - wd * 0.15, yy_ - 1.5)], WH)
            line(d, [(x + wd * 0.2, yy_ + 1), (x + wd * 0.75, yy_ + 3)], B, 0.9)
            line(d, [(x - wd * 0.2, yy_ - 0.5), (x + wd * 0.5, yy_ - 2.5)], G, 0.7)
big = [(22, 540, 210), (64, 560, 150), (-6, 590, 170), (388, 548, 190), (346, 566, 120), (104, 596, 90), (318, 598, 70)]
for x, y, h in sorted(big, key=lambda t: t[1]): spruce(x, y, h)

# ---------- hut, observers, instruments ----------
hx, hy = 248, 540
poly(d, [(hx + 60, hy), (hx + 84, hy - 8), (hx + 84, hy - 34), (hx + 72, hy - 50), (hx + 60, hy - 30)], K, B, 0.7)
rect(d, hx, hy - 30, hx + 60, hy, fill=K, outline=B, w=0.8)
for k in range(1, 6): line(d, [(hx + 1, hy - 30 + k * 5), (hx + 59, hy - 30 + k * 5)], B, 0.4)
poly(d, [(hx - 4, hy - 29), (hx + 62, hy - 29), (hx + 74, hy - 50), (hx + 8, hy - 50)], WH, K, 0.8)
for k in range(4): line(d, [(hx + 4 + k * 14, hy - 33), (hx + 16 + k * 14, hy - 47)], B, 0.5)
rect(d, hx + 36, hy - 22, hx + 50, hy - 9, fill=Y, outline=K, w=0.8); line(d, [(hx + 43, hy - 22), (hx + 43, hy - 9)], K, 0.8); line(d, [(hx + 36, hy - 15.5), (hx + 50, hy - 15.5)], K, 0.8)
rect(d, hx + 10, hy - 24, hx + 24, hy, fill=K, outline=Y, w=0.7); rect(d, hx + 20, hy - 22, hx + 24, hy - 1, fill=Y)      # door ajar
poly(d, [(hx + 20, hy), (hx + 24, hy), (hx + 6, hy + 30), (hx - 14, hy + 30)], Y)                                         # light spill
for k in range(5): line(d, [(hx + 19 - k * 5, hy + 4 + k * 6), (hx + 22 - k * 3.4, hy + 4 + k * 6)], K, 1.2)
rect(d, hx + 52, hy - 60, hx + 59, hy - 44, fill=K, outline=B, w=0.6)
for i in range(9): circ(d, hx + 56 + 3 * math.sin(i * 0.9), hy - 64 - i * 8, 2.2 + i * 0.5, outline=WH, w=0.6)
# thermometer by the door: twenty-two below
rect(d, hx + 27, hy - 24, hx + 32, hy - 6, fill=WH, outline=K, w=0.5); line(d, [(hx + 29.5, hy - 11), (hx + 29.5, hy - 9)], R, 1); circ(d, hx + 29.5, hy - 8.5, 1.4, fill=R)
def figure(x, y, sc, arm):
    line(d, [(x - 2 * sc, y), (x - 1 * sc, y - 9 * sc)], K, 2.4 * sc); line(d, [(x + 2.5 * sc, y), (x + 1 * sc, y - 9 * sc)], K, 2.4 * sc)
    poly(d, [(x - 4.5 * sc, y - 5 * sc), (x + 4.5 * sc, y - 5 * sc), (x + 3 * sc, y - 19 * sc), (x - 3 * sc, y - 19 * sc)], K)
    circ(d, x, y - 22 * sc, 3 * sc, fill=K); poly(d, [(x - 5.5 * sc, y - 23.5 * sc), (x + 5.5 * sc, y - 23.5 * sc), (x + 2 * sc, y - 27 * sc), (x - 2 * sc, y - 27 * sc)], K)
    line(d, [(x + 3 * sc, y - 17 * sc), (x + arm[0] * sc, y + arm[1] * sc)], K, 2 * sc)
    line(d, [(x - 3.4 * sc, y - 19 * sc), (x - 4.8 * sc, y - 5 * sc)], WH, 0.7); line(d, [(x - 2.6 * sc, y - 24 * sc), (x - 1 * sc, y - 26.5 * sc)], WH, 0.7)   # rim light
fx, fy = 176, 556
# tripod with a telescope
for lx in (-9, 0, 9): line(d, [(fx + 30, fy - 26), (fx + 30 + lx, fy + 2)], K, 1.4)
line(d, [(fx + 16, fy - 22), (fx + 46, fy - 38)], K, 4.2); line(d, [(fx + 17, fy - 24.5), (fx + 45, fy - 39.5)], Y, 0.9); circ(d, fx + 46.5, fy - 38.5, 2.6, fill=K, outline=Y, w=0.6)
figure(fx + 8, fy + 2, 1.25, (9, -24))
# table with the compass box and a lantern; second observer bending to the needle
tx_, ty_ = 118, 566
rect(d, tx_ - 2, ty_ - 14, tx_ + 30, ty_ - 11, fill=K, outline=Y, w=0.5); line(d, [(tx_ + 1, ty_ - 11), (tx_ - 1, ty_ + 2)], K, 1.5); line(d, [(tx_ + 27, ty_ - 11), (tx_ + 29, ty_ + 2)], K, 1.5)
ell(d, tx_ + 10, ty_ - 16, 6, 2.4, fill=WH, outline=K, w=0.5); line(d, [(tx_ + 6, ty_ - 16.5), (tx_ + 14, ty_ - 15.5)], R, 0.9)
rect(d, tx_ + 21, ty_ - 23, tx_ + 27, ty_ - 14, fill=Y, outline=K, w=0.7); poly(d, [(tx_ + 20, ty_ - 23), (tx_ + 24, ty_ - 28), (tx_ + 28, ty_ - 23)], K)
for k in range(8):
    an = k * math.pi / 4; line(d, [(tx_ + 24 + 7 * math.cos(an), ty_ - 19 + 7 * math.sin(an)), (tx_ + 24 + 10 * math.cos(an), ty_ - 19 + 10 * math.sin(an))], Y, 0.6)
figure(tx_ - 12, ty_ + 4, 1.2, (9, -14))
# tracks between hut and instruments
for i in range(16):
    f = i / 15; x = hx + 4 - f * 62; y = hy + 22 + 10 * math.sin(f * 3)
    ell(d, x, y + (2 if i % 2 else -1), 1.8, 1, fill=K)

# ---------- inset: the compass ----------
cx, cy, cr = 322, 86, 50
circ(d, cx, cy, cr + 5, fill=K, outline=WH, w=1.2); circ(d, cx, cy, cr, outline=WH, w=0.6); circ(d, cx, cy, cr - 9, outline=WH, w=0.5)
for i in range(72):
    an = math.radians(i * 5); r0 = cr - (9 if i % 18 == 0 else 6 if i % 2 == 0 else 3.5)
    line(d, [(cx + r0 * math.sin(an), cy - r0 * math.cos(an)), (cx + cr * math.sin(an), cy - cr * math.cos(an))], WH, 0.9 if i % 18 == 0 else 0.5)
for i in range(8):
    an = i * math.pi / 4 + math.pi / 8; r = 15
    poly(d, [(cx, cy), (cx + 4 * math.cos(an - 1.2), cy + 4 * math.sin(an - 1.2)), (cx + r * math.cos(an), cy + r * math.sin(an))], B)
for i in range(4):
    an = i * math.pi / 2 + math.pi / 4; r = 24; tip = (cx + r * math.cos(an), cy + r * math.sin(an))
    poly(d, [(cx, cy), (cx + 5 * math.cos(an - 1.3), cy + 5 * math.sin(an - 1.3)), tip], B, WH, 0.4)
def needle(deg, col, wd, full=True):
    an = math.radians(deg); L = cr - 12
    nx, ny = math.sin(an), -math.cos(an); qx, qy = -ny, nx
    if full:
        poly(d, [(cx + nx * L, cy + ny * L), (cx + qx * 3, cy + qy * 3), (cx - qx * 3, cy - qy * 3)], col, WH, 0.5)
        poly(d, [(cx - nx * L, cy - ny * L), (cx + qx * 3, cy + qy * 3), (cx - qx * 3, cy - qy * 3)], WH, K, 0.5)
    else:
        line(d, [(cx - nx * L, cy - ny * L), (cx + nx * L, cy + ny * L)], col, wd)
for dg in (-22, -14, 10, 17, 25): needle(dg, R, 1.0, full=False)
needle(-4, R, 1)
circ(d, cx, cy, 3, fill=Y, outline=K, w=0.7)
for sg in (-1, 1):       # tremor arcs
    for k in range(2):
        r = cr - 3 + 0; a0 = -90 + sg * (8 + k * 9) - 4; 
        d.arc([s(cx - (cr - 14 + k * 0)), s(cy - (cr - 14)), s(cx + (cr - 14)), s(cy + (cr - 14))], a0 if sg > 0 else a0 - 4, (a0 + 6) if sg > 0 else a0 + 2, fill=Y, width=2)

def post(p, out):
    f = font("serifb", 10); fi = font("serifi", 12); fs = font("sans", 8)
    p.text((cx, cy - cr + 11), "N", font=f, fill=WH, anchor="mm"); p.text((cx, cy + cr - 12), "S", font=f, fill=WH, anchor="mm")
    p.text((cx + cr - 13, cy), "Ö", font=f, fill=WH, anchor="mm"); p.text((cx - cr + 13, cy), "V", font=f, fill=WH, anchor="mm")
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1): p.text((cx + dx, cy + cr + 18 + dy), "Upsala, 1741", font=fi, fill=K, anchor="mm")
    p.text((cx, cy + cr + 18), "Upsala, 1741", font=fi, fill=WH, anchor="mm")
finish(img, post, ink=(WH, Y))
