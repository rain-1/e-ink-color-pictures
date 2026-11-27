"""Evening — Kakelugn. Twenty-one degrees inside: tiled stove, Mora clock, cat, dusk at the window."""
import math, random
import numpy as np
from PIL import Image, ImageDraw
from kit import *
rnd = random.Random(21)

# ---------- 1x background: wallpaper + dusk window + floor glow ----------
bg = np.zeros((H, W, 3), np.uint8); bg[:] = R
yy, xx = np.mgrid[0:H, 0:W]
WX0, WY0, WX1, WY1 = 242, 78, 366, 300
t = np.clip((yy - WY0) / (WY1 - WY0 - 60), 0, 1) ** 1.4          # black above -> blue at the horizon
win = screen(t, K, B, bayer())
m = (xx >= WX0) & (xx < WX1) & (yy >= WY0) & (yy < WY1); bg[m] = win[m]
img, d = canvas(bg)
FLOOR = 446

# wallpaper: damask of yellow sprigs on red, with thin black stripes
for x in range(0, 400, 26):
    line(d, [(x + 13, 0), (x + 13, FLOOR)], K, 0.5)
for row, y in enumerate(range(8, FLOOR, 22)):
    for x in range(0, 420, 26):
        cx = x + (13 if row % 2 else 0) - 13 + 13; cy = y
        if row % 2 == 0: cx -= 13
        for a in range(4):
            an = a * math.pi / 2 + math.pi / 4
            ell(d, cx + 3.2 * math.cos(an), cy + 3.2 * math.sin(an), 2, 2, fill=Y)
        circ(d, cx, cy, 1.2, fill=K)
        line(d, [(cx, cy + 5), (cx, cy + 10)], Y, 0.8); line(d, [(cx, cy + 8), (cx - 3, cy + 6)], Y, 0.8); line(d, [(cx, cy + 8), (cx + 3, cy + 6)], Y, 0.8)
# cornice
rect(d, 0, 0, 400, 16, fill=WH); line(d, [(0, 16), (400, 16)], K, 1.2); line(d, [(0, 11), (400, 11)], B, 0.6)
for x in range(0, 400, 8): poly(d, [(x, 16), (x + 4, 21), (x + 8, 16)], WH, K, 0.5)
# wainscot
rect(d, 0, 366, 400, FLOOR, fill=WH); line(d, [(0, 366), (400, 366)], K, 1.4); rect(d, 0, 362, 400, 368, fill=WH, outline=K, w=0.7)
for x in range(-10, 400, 58):
    rect(d, x + 5, 376, x + 53, 436, outline=B, w=0.8); rect(d, x + 9, 380, x + 49, 432, outline=K, w=0.4)
rect(d, 0, FLOOR - 7, 400, FLOOR, fill=WH, outline=K, w=0.8)

# ---------- floor: planks to a vanishing point, glow from the fire ----------
rect(d, 0, FLOOR, 400, 600, fill=Y)
vpx, vpy = 190, 250
for i in range(-14, 30):
    xb = i * 34 - 60
    line(d, [(vpx + (xb - vpx) * (FLOOR - vpy) / (600 - vpy), FLOOR), (xb, 600)], K, 0.8)
for i in range(60):
    y = rnd.uniform(FLOOR + 4, 598); x = rnd.uniform(0, 400)
    dx = (x - vpx) / (y - vpy) * 9
    line(d, [(x, y), (x + dx, y + 9)], K, 0.4)
for i in range(16):                      # plank ends
    y = rnd.uniform(FLOOR + 6, 596); x = rnd.uniform(0, 400); line(d, [(x - 6, y), (x + 6, y)], K, 0.6)

# ---------- window ----------
# outside: snow roofs, lit house, stars, Saturn
poly(d, [(WX0, 270)] + [(x, 262 - 6 * math.sin(x / 23) - 3 * math.sin(x / 9)) for x in range(WX0, WX1 + 1, 3)] + [(WX1, 300), (WX0, 300)], WH)
for x in range(WX0 + 2, WX1, 6):
    y = 262 - 6 * math.sin(x / 23) - 3 * math.sin(x / 9); h = rnd.uniform(9, 20)
    poly(d, [(x - 3.5, y + 2), (x, y - h), (x + 3.5, y + 2)], K)
hx, hy = 292, 284
rect(d, hx, hy - 16, hx + 36, hy, fill=R, outline=K, w=0.7); poly(d, [(hx - 3, hy - 16), (hx + 18, hy - 30), (hx + 39, hy - 16)], WH, K, 0.7)
rect(d, hx + 6, hy - 11, hx + 13, hy - 4, fill=Y, outline=K, w=0.5); rect(d, hx + 22, hy - 11, hx + 29, hy - 4, fill=Y, outline=K, w=0.5)
for k in range(6): line(d, [(WX0 + 4 + k * 22, 290 + (k % 2) * 3), (WX0 + 16 + k * 22, 291 + (k % 2) * 3)], B, 0.7)
for _ in range(38):
    sx, sy = rnd.uniform(WX0 + 3, WX1 - 3), rnd.uniform(WY0 + 3, 215); circ(d, sx, sy, rnd.choice([0.6, 0.6, 0.9]), fill=WH)
sx, sy = 338, 128                                  # Saturn, the one evening planet
circ(d, sx, sy, 2.2, fill=Y); line(d, [(sx - 5, sy + 1.5), (sx + 5, sy - 1.5)], Y, 0.8)
for (cx, cy, a0) in [(WX0, 188, -40), (WX1, 188, 220), (WX0, WY1, -50), (WX1, WY1, 230), (304, 188, -90), (304, WY1, -90)]:   # frost in pane corners
    for k in range(7):
        a = math.radians(a0 + rnd.uniform(-45, 45)); ln = rnd.uniform(8, 22)
        ex, ey = cx + ln * math.cos(a), cy + ln * math.sin(a); line(d, [(cx, cy), (ex, ey)], WH, 0.8)
        for s2 in (-1, 1):
            b = a + s2 * 1.0; mx, my = (cx + ex) / 2, (cy + ey) / 2; line(d, [(mx, my), (mx + ln * 0.35 * math.cos(b), my + ln * 0.35 * math.sin(b))], WH, 0.6)
# frame
rect(d, WX0 - 7, WY0 - 7, WX1 + 7, WY0, fill=WH, outline=K, w=0.8); rect(d, WX0 - 7, WY0 - 7, WX0, WY1 + 4, fill=WH, outline=K, w=0.8); rect(d, WX1, WY0 - 7, WX1 + 7, WY1 + 4, fill=WH, outline=K, w=0.8)
rect(d, 301, WY0, 307, WY1, fill=WH, outline=K, w=0.7); rect(d, WX0, 185, WX1, 191, fill=WH, outline=K, w=0.7)
rect(d, WX0 - 13, WY1, WX1 + 13, WY1 + 9, fill=WH, outline=K, w=0.9); line(d, [(WX0 - 10, WY1 + 5), (WX1 + 10, WY1 + 5)], B, 0.5)
# curtains: green, tied back, with a scalloped pelmet
def curtain(side):
    x0 = WX0 - 16 if side < 0 else WX1 + 16
    pts = []
    for i in range(31):
        f = i / 30; y = WY0 - 12 + f * 250
        wd = 30 - 16 * math.sin(min(1, f / 0.72) * math.pi / 2) ** 2 + (12 * (f - 0.72) / 0.28 if f > 0.72 else 0)
        pts.append((x0 - side * wd, y))
    edge = pts
    poly(d, [(x0, WY0 - 12)] + edge + [(x0, WY0 + 238)], G, K, 0.9)
    for k in range(1, 5):
        line(d, [(x0 + (ex - x0) * k / 5, y) for ex, y in edge], K, 0.5)
    ty = WY0 - 12 + 0.72 * 250; tx = edge[int(0.72 * 30)][0]
    line(d, [(x0, ty - 3), (tx, ty)], Y, 2.2); circ(d, tx, ty + 1, 2.4, fill=Y, outline=K, w=0.5); line(d, [(tx, ty + 3), (tx - side * 1, ty + 12)], Y, 1.2)
    for k in range(9): circ(d, edge[-1][0] + (x0 - edge[-1][0]) * k / 8, WY0 + 240, 1.5, fill=Y, outline=K, w=0.4)
curtain(-1); curtain(1)
rect(d, WX0 - 22, WY0 - 22, WX1 + 22, WY0 - 9, fill=G, outline=K, w=0.9)
for k in range(11):
    cx = WX0 - 22 + (WX1 - WX0 + 44) * (k + 0.5) / 11
    d.pieslice([s(cx - 8), s(WY0 - 17), s(cx + 8), s(WY0 - 1)], 0, 180, fill=G, outline=K, width=2); circ(d, cx, WY0 - 2, 1.6, fill=Y, outline=K, w=0.4)
line(d, [(WX0 - 22, WY0 - 18), (WX1 + 22, WY0 - 18)], Y, 1.2)
# amaryllis on the sill (the morning's plant, seen from the room)
px, py = 270, WY1
poly(d, [(px - 9, py - 14), (px + 9, py - 14), (px + 7, py), (px - 7, py)], WH, K, 0.8); line(d, [(px - 8, py - 9), (px + 8, py - 9)], B, 1)
line(d, [(px, py - 14), (px + 1, py - 62)], G, 2.4)
for (ax, ay, bx, by) in [(px - 1, py - 14, px - 18, py - 44), (px + 1, py - 14, px + 16, py - 50)]:
    poly(d, [(ax - 2, ay), (bx, by), (ax + 2, ay)], G, K, 0.5)
for cx, cy, a0 in [(px - 6, py - 64, 0.2), (px + 9, py - 60, 0.8)]:
    for k in range(6):
        a = a0 + k * math.pi / 3; poly(d, [(cx, cy), (cx + 5 * math.cos(a - 0.5), cy + 5 * math.sin(a - 0.5)), (cx + 11 * math.cos(a), cy + 10 * math.sin(a)), (cx + 5 * math.cos(a + 0.5), cy + 5 * math.sin(a + 0.5))], R, K, 0.5)
    circ(d, cx, cy, 1.6, fill=Y)

# ---------- the stove ----------
SX0, SX1, STOP, SBOT = 22, 136, 96, 470
scx, srad = (SX0 + SX1) / 2, (SX1 - SX0) / 2
# glow on the floor
a = np.asarray(img).copy()
Y3, X3 = np.mgrid[0:H * S, 0:W * S]; yb, xb = Y3 // S, X3 // S
glow = 1 - np.sqrt(((xb - 150) / 120.0) ** 2 + ((yb - 480) / 60.0) ** 2)
thr3 = bayer()[yb, xb]
isY = (a == np.array(Y)).all(-1)
a[isY & (glow * 0.9 > thr3) & (yb > FLOOR)] = WH
img = Image.fromarray(a); d = ImageDraw.Draw(img); d.fontmode = "1"
rect(d, SX0 - 5, SBOT - 14, SX1 + 5, SBOT + 2, fill=K)                               # plinth
ell(d, scx, SBOT + 2, srad + 5, 7, fill=K)
rect(d, SX0, STOP, SX1, SBOT - 14, fill=WH, outline=K, w=1.1)
ncol = 9
colx = [scx + srad * math.sin(-math.pi / 2 + math.pi * i / ncol) for i in range(ncol + 1)]
rows = list(range(STOP, SBOT - 14, 26))
for x in colx[1:-1]: line(d, [(x, STOP), (x, SBOT - 14)], K, 0.6)
for y in rows[1:]: line(d, [(SX0, y), (SX1, y)], K, 0.6)
for ri, y in enumerate(rows):
    for ci in range(ncol):
        x0, x1 = colx[ci], colx[ci + 1]; wd = x1 - x0; cx, cy = (x0 + x1) / 2, y + 13
        if wd < 6:
            line(d, [(cx, y + 5), (cx, y + 21)], B, 0.8); continue
        sx_ = wd / 20
        if (ri + ci) % 2 == 0:                                   # flower tile
            for k in range(6):
                an = k * math.pi / 3; ell(d, cx + 5 * sx_ * math.cos(an), cy + 5 * math.sin(an), 2.6 * sx_, 2.6, fill=B)
            circ(d, cx, cy, 1.8, fill=Y, outline=B, w=0.4)
        else:                                                    # diamond + sprigs
            poly(d, [(cx, cy - 7), (cx + 6 * sx_, cy), (cx, cy + 7), (cx - 6 * sx_, cy)], WH, B, 0.9); circ(d, cx, cy, 1.5, fill=B)
        for (qx, qy) in [(x0 + 2 * sx_, y + 2.5), (x1 - 2 * sx_, y + 2.5), (x0 + 2 * sx_, y + 23.5), (x1 - 2 * sx_, y + 23.5)]: circ(d, qx, qy, 0.9, fill=B)
# shading on the right flank
for i in range(26):
    x = SX1 - 1 - i * 0.9
    if i % 2 == 0: line(d, [(x, STOP + 2), (x, SBOT - 15)], B if i > 8 else K, 0.4)
# crown
rect(d, SX0 - 6, STOP - 10, SX1 + 6, STOP, fill=WH, outline=K, w=1); rect(d, SX0 - 3, STOP - 18, SX1 + 3, STOP - 10, fill=WH, outline=K, w=0.9)
for k in range(12):
    cx = SX0 - 3 + (SX1 - SX0 + 6) * (k + 0.5) / 12; d.arc([s(cx - 5), s(STOP - 9), s(cx + 5), s(STOP - 1)], 0, 180, fill=B, width=3); circ(d, cx, STOP - 14, 1.4, fill=B)
crown = [(SX0 + 4, STOP - 18)] + [(scx + (srad - 4) * math.cos(math.pi - math.pi * i / 20), STOP - 18 - 26 * math.sin(math.pi * i / 20) ** 0.7) for i in range(21)] + [(SX1 - 4, STOP - 18)]
poly(d, crown, WH, K, 1)
for k in range(5):
    an = math.pi * (k + 1) / 6; line(d, [(scx, STOP - 20), (scx + (srad - 10) * math.cos(an), STOP - 20 - 20 * math.sin(an))], B, 0.8)
circ(d, scx, STOP - 22, 5, fill=Y, outline=K, w=0.7); circ(d, scx, STOP - 46, 4, fill=WH, outline=K, w=0.8); circ(d, scx, STOP - 46, 1.5, fill=B)
# brass doors, ajar, fire inside
DY0, DY1 = 330, 400
rect(d, scx - 30, DY0 - 5, scx + 30, DY1 + 5, fill=Y, outline=K, w=1)
rect(d, scx - 24, DY0, scx + 24, DY1, fill=K)
for k in range(9):                        # flames
    fx = scx - 20 + k * 5; fh = 26 + 16 * math.sin(k * 1.9) + rnd.uniform(0, 10)
    poly(d, [(fx - 5, DY1), (fx - 2, DY1 - fh * 0.5), (fx, DY1 - fh), (fx + 3, DY1 - fh * 0.45), (fx + 5, DY1)], R)
for k in range(8):
    fx = scx - 18 + k * 5.2; fh = 14 + 9 * math.sin(k * 2.3 + 1)
    poly(d, [(fx - 3.5, DY1), (fx, DY1 - fh), (fx + 3.5, DY1)], Y)
for k in range(5): poly(d, [(scx - 14 + k * 7 - 2, DY1), (scx - 14 + k * 7, DY1 - 6), (scx - 14 + k * 7 + 2, DY1)], WH)
for k in range(4): ell(d, scx - 16 + k * 11, DY1 - 2, 6, 2.5, fill=K)
for side in (-1, 1):                      # the two door leaves, swung open
    x0 = scx + side * 24; x1 = scx + side * 43
    poly(d, [(x0, DY0), (x1, DY0 - 5), (x1, DY1 + 5), (x0, DY1)], Y, K, 0.9)
    poly(d, [(x0 + side * 3, DY0 + 5), (x1 - side * 3, DY0 + 1), (x1 - side * 3, DY1 - 1), (x0 + side * 3, DY1 - 5)], Y, K, 0.5)
    circ(d, (x0 + x1) / 2, (DY0 + DY1) / 2, 4, fill=Y, outline=K, w=0.6); circ(d, (x0 + x1) / 2, (DY0 + DY1) / 2, 1.3, fill=K)
rect(d, scx - 14, DY1 + 16, scx + 14, DY1 + 30, fill=Y, outline=K, w=0.8); circ(d, scx, DY1 + 23, 2, fill=K)       # ash door
rect(d, scx - 6, 268, scx + 6, 280, fill=Y, outline=K, w=0.7); line(d, [(scx, 270), (scx, 278)], K, 0.8)           # damper
# hearth plate + firewood basket + poker
poly(d, [(SX0 - 12, SBOT + 4), (SX1 + 12, SBOT + 4), (SX1 + 30, SBOT + 30), (SX0 - 26, SBOT + 30)], K); poly(d, [(SX0 - 8, SBOT + 7), (SX1 + 9, SBOT + 7), (SX1 + 23, SBOT + 27), (SX0 - 19, SBOT + 27)], K, Y, 0.5)
bx, by = 150, 478
for k in range(5):
    lx = bx + 4 + k * 8; rect(d, lx, by - 34 - (k % 2) * 6, lx + 7, by - 4, fill=WH if k % 2 else Y, outline=K, w=0.6)
    if k % 2: [line(d, [(lx + 1, by - 30 + j * 6), (lx + 4, by - 30 + j * 6)], K, 0.8) for j in range(4)]
poly(d, [(bx, by - 18), (bx + 46, by - 18), (bx + 41, by + 6), (bx + 5, by + 6)], Y, K, 0.9)
for k in range(9): line(d, [(bx + 2 + k * 5, by - 18), (bx + 6 + k * 4.2, by + 6)], K, 0.5)
for k in range(4): line(d, [(bx + 1 + k * 0.6, by - 13 + k * 5), (bx + 45 - k * 0.6, by - 13 + k * 5)], K, 0.5)
line(d, [(140, 470), (146, 392)], K, 1.6); circ(d, 146, 390, 2.5, outline=K, w=1)

# ---------- wall thermometer (+21) ----------
tx, ty, th = 146, 196, 92
rect(d, tx, ty, tx + 20, ty + th, fill=WH, outline=K, w=1); poly(d, [(tx, ty), (tx + 10, ty - 9), (tx + 20, ty)], WH, K, 1); circ(d, tx + 10, ty - 3, 1.3, fill=K)
top, bot = ty + 8, ty + th - 20
tyv = lambda v: bot - (v + 10) / 50 * (bot - top)          # -10 .. +40
rect(d, tx + 8, top - 3, tx + 12, bot + 4, fill=WH, outline=K, w=0.7); rect(d, tx + 9, tyv(21), tx + 11, bot + 4, fill=R)
circ(d, tx + 10, bot + 9, 5, fill=R, outline=K, w=0.8)
for v in range(-10, 41, 2):
    L = 4 if v % 10 == 0 else 2; line(d, [(tx + 13.5, tyv(v)), (tx + 13.5 + L, tyv(v))], K, 0.6); line(d, [(tx + 6.5 - L, tyv(v)), (tx + 6.5, tyv(v))], B if v <= 0 else K, 0.6)

# ---------- Mora clock ----------
cx, base = 200, FLOOR - 2
body = []
for i in range(41):
    f = i / 40; y = base - f * 250
    wd = 15 + 6 * math.sin(f * math.pi * 0.9) * (1 if f < 0.62 else 0.2) + (16 * math.exp(-((f - 0.36) / 0.13) ** 2)) - 4 * math.exp(-((f - 0.66) / 0.05) ** 2) + 12 * math.exp(-((f - 0.86) / 0.11) ** 2)
    body.append((wd, y))
poly(d, [(cx - w_, y) for w_, y in body] + [(cx + w_, y) for w_, y in body[::-1]], WH, K, 1.1)
rect(d, cx - 22, base - 8, cx + 22, base + 2, fill=WH, outline=K, w=1)
fy = base - 0.86 * 250
circ(d, cx, fy, 21, fill=WH, outline=K, w=1); circ(d, cx, fy, 17, fill=WH, outline=B, w=1.2)
for k in range(12):
    an = k * math.pi / 6; line(d, [(cx + 13 * math.sin(an), fy - 13 * math.cos(an)), (cx + 16 * math.sin(an), fy - 16 * math.cos(an))], K, 1 if k % 3 == 0 else 0.5)
line(d, [(cx, fy), (cx, fy + 8.5)], K, 1.5); line(d, [(cx, fy), (cx + 0.5, fy - 13)], K, 1); circ(d, cx, fy, 1.5, fill=R)      # six o'clock
poly(d, [(cx - 14, fy - 20), (cx - 6, fy - 30), (cx, fy - 24), (cx + 6, fy - 30), (cx + 14, fy - 20)], WH, K, 0.9); circ(d, cx, fy - 31, 3, fill=Y, outline=K, w=0.6)
by2 = base - 0.36 * 250
ell(d, cx, by2, 9, 12, fill=K, outline=B, w=0.8); circ(d, cx + 2, by2 + 3, 5, fill=Y, outline=K, w=0.5); line(d, [(cx, by2 - 11), (cx + 2, by2 + 2)], Y, 0.8)
for (gy, sc) in [(base - 0.16 * 250, 1), (base - 0.57 * 250, 0.8)]:     # painted garlands
    for k in range(-3, 4):
        ell(d, cx + k * 4 * sc, gy + abs(k) * -1.5 * sc + 4, 2, 1.4, fill=B)
    circ(d, cx, gy + 5, 1.6, fill=R)

# framed map (the midday piece) + sconce
fx, fy0 = 172, 44
rect(d, fx, fy0, fx + 56, fy0 + 78, fill=Y, outline=K, w=1); rect(d, fx + 5, fy0 + 5, fx + 51, fy0 + 73, fill=WH, outline=K, w=0.6)
rect(d, fx + 5, fy0 + 60, fx + 51, fy0 + 73, fill=B)
rv = [(fx + 30 + 5 * math.sin(k / 2.0), fy0 + 6 + k * 5.5) for k in range(11)]; line(d, rv, B, 1.4)
tp = [(fx + 27, fy0 + 58), (fx + 18, fy0 + 48), (fx + 37, fy0 + 44), (fx + 22, fy0 + 34), (fx + 38, fy0 + 27), (fx + 24, fy0 + 20), (fx + 34, fy0 + 11)]
for i in range(len(tp) - 2): line(d, [tp[i], tp[i + 1], tp[i + 2], tp[i]], R, 0.6)
for k in range(9): px_, py_ = fx + 9 + (k * 17) % 38, fy0 + 12 + (k * 23) % 44; poly(d, [(px_ - 1.5, py_ + 2), (px_, py_ - 2), (px_ + 1.5, py_ + 2)], G)
line(d, [(fx + 28, fy0), (fx + 28, fy0 - 12)], K, 0.5)
sx, sy = 388, 150
rect(d, sx - 5, sy, sx + 5, sy + 22, fill=Y, outline=K, w=0.8); rect(d, sx - 2, sy - 16, sx + 2, sy, fill=WH, outline=K, w=0.6)
poly(d, [(sx - 3, sy - 17), (sx, sy - 29), (sx + 3, sy - 17)], Y, K, 0.5); circ(d, sx, sy - 19, 1.2, fill=WH)
for k in range(10):
    an = k * math.pi / 5; line(d, [(sx + 9 * math.cos(an), sy - 22 + 9 * math.sin(an)), (sx + 14 * math.cos(an), sy - 22 + 14 * math.sin(an))], Y, 0.8)

# ---------- rag rug ----------
def rug(x0, x1, y0, y1, slope):
    cols = [R, WH, B, WH, G, Y, K, WH, R, R, WH, B, Y, WH, G, WH, K, R, WH, B]
    n = 34
    for i in range(n):
        f0, f1 = i / n, (i + 1) / n
        ya, yb_ = y0 + (y1 - y0) * f0 ** 1.25, y0 + (y1 - y0) * f1 ** 1.25
        xa0, xa1 = x0 - slope * (ya - y0), x1 + slope * (ya - y0) * 0.6; xb0, xb1 = x0 - slope * (yb_ - y0), x1 + slope * (yb_ - y0) * 0.6
        poly(d, [(xa0, ya), (xa1, ya), (xb1, yb_), (xb0, yb_)], cols[i % len(cols)])
        if i % 3 == 0: line(d, [(xa0, ya), (xa1, ya)], K, 0.4)
    A, Bq, C, D = (x0, y0), (x1, y0), (x1 + slope * (y1 - y0) * 0.6, y1), (x0 - slope * (y1 - y0), y1)
    line(d, [A, Bq, C, D, A], K, 1)
    for k in range(30):
        f = k / 29; fx_ = D[0] + (C[0] - D[0]) * f; line(d, [(fx_, y1), (fx_ + rnd.uniform(-1, 1), y1 + 5)], WH, 0.8); line(d, [(fx_ + 1, y1), (fx_ + 1, y1 + 4)], K, 0.4)
rug(110, 250, 500, 592, 0.55)

# ---------- armchair + cat ----------
ax, ay = 262, 540
poly(d, [(ax - 8, ay + 30), (ax + 124, ay + 30), (ax + 140, ay + 44), (ax - 26, ay + 44)], K)                           # shadow
back = [(ax + 6, ay - 60)] + [(ax + 56 + 54 * math.cos(math.pi - math.pi * i / 20), ay - 150 - 34 * math.sin(math.pi * i / 20)) for i in range(21)] + [(ax + 106, ay - 60)]
poly(d, back, G, K, 1.2)
for r_ in range(5):                                                                   # button tufting
    for c_ in range(5 - (r_ % 2)):
        bx_ = ax + 22 + c_ * 17 + (8.5 if r_ % 2 else 0); by_ = ay - 160 + r_ * 20
        circ(d, bx_, by_, 1.6, fill=Y, outline=K, w=0.5)
        for (ddx, ddy) in [(-8.5, -10), (8.5, -10)]: line(d, [(bx_, by_), (bx_ + ddx * 0.8, by_ + ddy * 0.8)], K, 0.4)
rect(d, ax + 2, ay - 64, ax + 110, ay - 30, fill=G, outline=K, w=1.1)                                                # seat cushion
line(d, [(ax + 8, ay - 36), (ax + 104, ay - 36)], K, 0.5)
rect(d, ax, ay - 30, ax + 112, ay + 14, fill=G, outline=K, w=1.1)
for k in range(14): line(d, [(ax + 4 + k * 8, ay + 6), (ax + 4 + k * 8, ay + 14)], Y, 1.2)                              # fringe
line(d, [(ax, ay + 6), (ax + 112, ay + 6)], K, 0.6)
for side, x_ in ((-1, ax - 12), (1, ax + 100)):                                                                       # arms
    rect(d, x_, ay - 74, x_ + 24, ay + 14, fill=G, outline=K, w=1.1); ell(d, x_ + 12, ay - 76, 14, 9, fill=G, outline=K, w=1.1)
    d.arc([s(x_ + 5), s(ay - 82), s(x_ + 19), s(ay - 70)], 20, 320, fill=K, width=2)
    for k in range(5): line(d, [(x_ + 4 + k * 4, ay - 62), (x_ + 4 + k * 4, ay + 8)], K, 0.4)
for x_ in (ax - 8, ax + 110):
    poly(d, [(x_ - 3, ay + 14), (x_ + 5, ay + 14), (x_ + 3, ay + 30), (x_ - 1, ay + 30)], K)
# blanket over the arm
poly(d, [(ax + 98, ay - 86), (ax + 126, ay - 84), (ax + 130, ay - 20), (ax + 120, ay - 14), (ax + 100, ay - 22)], WH, K, 0.9)
for k in range(7): line(d, [(ax + 99, ay - 78 + k * 9), (ax + 128, ay - 76 + k * 9)], B if k % 2 else R, 1.6)
# the cat, curled
ccx, ccy = ax + 54, ay - 74
ell(d, ccx, ccy, 30, 15, fill=K)
circ(d, ccx - 24, ccy - 6, 10, fill=K); poly(d, [(ccx - 33, ccy - 11), (ccx - 32, ccy - 22), (ccx - 25, ccy - 15)], K); poly(d, [(ccx - 23, ccy - 15), (ccx - 17, ccy - 22), (ccx - 15, ccy - 11)], K)
d.arc([s(ccx - 16), s(ccy - 6), s(ccx + 34), s(ccy + 20)], 10, 170, fill=WH, width=2)                                   # tail line
ell(d, ccx - 28, ccy - 6, 2.2, 1.3, fill=Y); ell(d, ccx - 20, ccy - 6, 2.2, 1.3, fill=Y); line(d, [(ccx - 28, ccy - 7), (ccx - 28, ccy - 5)], K, 0.7); line(d, [(ccx - 20, ccy - 7), (ccx - 20, ccy - 5)], K, 0.7)
poly(d, [(ccx - 25, ccy - 2), (ccx - 23, ccy - 2), (ccx - 24, ccy - 0.5)], R)
for sg in (-1, 1):
    for k in range(2): line(d, [(ccx - 24 + sg * 3, ccy - 1 + k), (ccx - 24 + sg * 13, ccy - 3 + k * 3)], WH, 0.4)
# slippers + book on the floor
for k in range(2):
    ell(d, 236 + k * 16, 572 + k * 3, 7, 3.5, fill=R, outline=K, w=0.7); ell(d, 238 + k * 16, 572 + k * 3, 3.5, 2, fill=K)

finish(img, None, ink=(K,))
