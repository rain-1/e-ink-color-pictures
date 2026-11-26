"""Midday — Khepri pectoral. A winged scarab in cloisonne, pushing the noon sun."""
import math, random
from common import *

random.seed(26)
c = C(B)
CX, CY = 200, 338


def pol(r, a, side=1):
    a = math.radians(a)
    return (CX + side * r * math.cos(a), CY - r * math.sin(a))


def wedge(r0, r1, a0, a1, side, n=6, tip=0.0):
    pts = [pol(r0, a0 + (a1 - a0) * i / n, side) for i in range(n + 1)]
    outer = []
    for i in range(n + 1):
        f = i / n
        bulge = tip * math.sin(math.pi * f)
        outer.append(pol(r1 + bulge, a1 + (a0 - a1) * f, side))
    return pts + outer


A0, A1 = -20, 74
ROWS = [  # r0, r1, count, bands (frac0, frac1, colour), tip bulge
    (40, 74, 8, [(0, .55, G), (.55, 1, WH)], 5),
    (76, 120, 12, [(0, .34, R), (.34, .72, G), (.72, 1, R)], 6),
    (122, 178, 17, [(0, .22, WH), (.22, .5, G), (.5, .74, R), (.74, 1, WH)], 7),
]
for side in (1, -1):
    for r0, r1, n, bands, tip in reversed(ROWS):
        da = (A1 - A0) / n
        for k in range(n):
            a0, a1 = A0 + k * da, A0 + (k + 1) * da
            c.poly(wedge(r0 - 1, r1 + 1.5, a0, a1, side, tip=tip), Y)           # gold cell wall
            g = 1.3 / r1 * 57.3                                                # wall thickness in degrees
            for f0, f1, col in bands:
                ra, rb = r0 + (r1 - r0) * f0 + 1, r0 + (r1 - r0) * f1 - 1
                last = f1 == 1
                c.poly(wedge(ra, rb, a0 + g, a1 - g, side, tip=tip - 1.5 if last else 0), col)
            # a black quill line on the tip
            if r1 > 150:
                am = (a0 + a1) / 2
                c.line([pol(r0 + (r1 - r0) * .78, am, side), pol(r1 + 2, am, side)], K, 1)
    # shoulder plate
    c.poly(wedge(22, 39, A0 - 4, A1 + 4, side), Y, K, 1)
    for k in range(9):
        c.circ(*pol(31, A0 + 2 + k * (A1 - A0 - 4) / 8, side), 2.2, fill=R, outline=K)

# --- the sun, held up by the forelegs ---
SX, SY = 200, 226
for side in (1, -1):
    leg = bez((CX + side * 13, 296), (CX + side * 30, 280), (CX + side * 36, 262), (SX + side * 25, SY + 8))
    c.line(leg, K, 7); c.line(leg, Y, 4.6)
    for i in range(3, len(leg) - 2, 4):                                        # serrations
        x, y = leg[i]
        c.poly([(x + side * 2, y - 3), (x + side * 8, y), (x + side * 2, y + 3)], Y, K, .8)
c.circ(SX, SY, 31, fill=K); c.circ(SX, SY, 29.5, fill=Y); c.circ(SX, SY, 25, fill=K); c.circ(SX, SY, 23.5, fill=R)
for k in range(24):                                                            # granulation on the ring
    a = k * math.pi / 12
    c.circ(SX + 27.3 * math.cos(a), SY + 27.3 * math.sin(a), 1.1, fill=K)
c.arc(SX, SY, 17, 200, 290, Y, 1.6)                                            # a gleam
# uraei hanging from the disc
for side in (1, -1):
    body = bez((SX + side * 28, SY - 6), (SX + side * 52, SY - 14), (SX + side * 50, SY + 22), (SX + side * 40, SY + 30))
    c.line(body, K, 6.5); c.line(body, Y, 4)
    hx, hy = SX + side * 41, SY + 33
    c.ell(hx - 7, hy - 4, hx + 7, hy + 16, fill=Y, outline=K, w=1.2)           # hood
    c.ell(hx - 3.5, hy, hx + 3.5, hy + 12, fill=G, outline=K, w=.8)
    for j in range(3):
        c.line([(hx - 3, hy + 3 + j * 3), (hx + 3, hy + 3 + j * 3)], K, .8)
    c.circ(hx + side * 1, hy - 6, 4.2, fill=Y, outline=K, w=1); c.circ(hx + side * 2.5, hy - 6.5, 1, fill=K)

# --- scarab ---
# hind legs & shen ring
for side in (1, -1):
    leg = bez((CX + side * 22, 384), (CX + side * 44, 398), (CX + side * 34, 420), (CX + side * 13, 428))
    c.line(leg, K, 7); c.line(leg, Y, 4.6)
    mid = bez((CX + side * 28, 352), (CX + side * 50, 356), (CX + side * 58, 372), (CX + side * 52, 390))
    c.line(mid, K, 6); c.line(mid, Y, 3.6)
    for i in range(4, len(mid) - 1, 5):
        x, y = mid[i]
        c.poly([(x + side * 1, y - 2.5), (x + side * 7, y + 1), (x + side * 1, y + 3)], Y, K, .8)
c.circ(200, 436, 16, fill=K); c.circ(200, 436, 14.5, fill=Y); c.circ(200, 436, 9.5, fill=K); c.circ(200, 436, 8, fill=R)
c.rect(176, 451, 224, 458, fill=Y, outline=K, w=1)
for x in range(180, 224, 6):
    c.line([(x, 452), (x, 457)], K, .8)
# elytra
c.ell(CX - 31, 318, CX + 31, 404, fill=K); c.ell(CX - 29.5, 319.5, CX + 29.5, 402.5, fill=G)
c.line([(CX, 322), (CX, 402)], Y, 2.2); c.line([(CX, 322), (CX, 402)], K, .7)
for side in (1, -1):
    for j, off in enumerate((7, 13, 19, 24)):                                  # striae
        pts = []
        for i in range(21):
            t = i / 20
            y = 326 + t * 72
            half = 29.5 * math.sqrt(max(0, 1 - ((y - 361) / 41.5) ** 2))
            pts.append((CX + side * min(off, half - 2) * (0.75 + 0.25 * math.sin(math.pi * t)), y))
        c.line(pts, Y if j % 2 == 0 else K, .9)
# pronotum
c.d.chord([(CX - 30) * S, 296 * S, (CX + 30) * S, 344 * S], 180, 360, fill=K)
c.d.chord([(CX - 28.5) * S, 297.5 * S, (CX + 28.5) * S, 342.5 * S], 180, 360, fill=Y)
c.line([(CX - 30, 320), (CX + 30, 320)], K, 1.6)
for x in range(-22, 23, 4):
    c.line([(CX + x, 304 + abs(x) * .28), (CX + x, 317)], K, .8)
c.arc(CX, 320, 19, 180, 360, R, 2.2, ry=14)
# head and clypeus
c.poly([(CX - 15, 298), (CX - 19, 286), (CX - 12, 289), (CX - 9, 280), (CX - 4, 286), (CX, 278), (CX + 4, 286),
        (CX + 9, 280), (CX + 12, 289), (CX + 19, 286), (CX + 15, 298)], Y, K, 1.2)
c.circ(CX - 9, 294, 2.3, fill=K); c.circ(CX + 9, 294, 2.3, fill=K)

# --- wedjat eyes, either side of the shen ---
def wedjat(ox, oy, side):
    def T(x, y): return (ox + side * x, oy + y)
    eye = [T(*p) for p in bez((-30, 0), (-14, -17), (16, -17), (32, -2), 14)] + \
          [T(*p) for p in bez((32, -2), (14, 11), (-14, 10), (-30, 0), 14)]
    c.poly(eye, WH, K, 2)
    c.circ(*T(1, -3), 9, fill=K); c.circ(*T(1, -3), 5, fill=B); c.circ(*T(-1, -5), 1.6, fill=WH)
    brow = [T(*p) for p in bez((-34, -14), (-12, -30), (22, -30), (46, -12), 16)]
    c.line(brow, K, 5.5); c.line(brow, Y, 3)
    c.line([T(32, -2), T(52, -1)], K, 4.5); c.line([T(32, -2), T(52, -1)], Y, 2.2)   # cosmetic line
    drop = [T(-6, 10), T(-9, 30), T(-2, 30), T(2, 10)]
    c.poly(drop, G, K, 1.3)
    sp = []
    for i in range(40):                                                         # falcon curl
        t = i / 39
        a = math.pi * 0.5 + t * math.pi * 2.6
        r = 13 * (1 - t * 0.78)
        sp.append(T(22 + 14 * t + r * math.cos(a) * 1.0 - 8, 20 + r * math.sin(a) - 4))
    c.line([T(6, 9)] + sp, K, 4.2); c.line([T(6, 9)] + sp, Y, 2)

wedjat(92, 440, -1); wedjat(308, 440, 1)

# --- pendant bar and lotus fringe ---
c.rect(26, 474, 374, 486, fill=Y, outline=K, w=1.2)
cols = [R, G, WH, G]
for i, x in enumerate(range(30, 370, 12)):
    c.rect(x, 477, x + 9, 483, fill=cols[i % 4], outline=K, w=.8)
N = 9
for i in range(N):
    x = 44 + i * (312 / (N - 1))
    for j in range(3):
        c.circ(x, 490 + j * 5, 2.2, fill=Y, outline=K, w=.7)
    top = 504
    if i % 2 == 0:                                                              # open lotus
        petals = [(-17, 0, G), (17, 0, G), (-11, -1, WH), (11, -1, WH), (-5, -1, R), (5, -1, R), (0, -2, WH)]
        for dx, dy, col in petals:
            c.poly([(x - 3 + dx * .15, top), (x + dx - 2.5, top + 38 + dy - abs(dx) * .5),
                    (x + dx, top + 46 + dy - abs(dx) * .6), (x + dx + 2.5, top + 38 + dy - abs(dx) * .5),
                    (x + 3 + dx * .15, top)], col, K, 1)
        c.pie(x, top + 1, 7, 0, 180, Y); c.arc(x, top + 1, 7, 0, 180, K, 1)
    else:                                                                       # bud / poppy drop
        c.ell(x - 7, top, x + 7, top + 34, fill=K); c.ell(x - 5.6, top + 1.4, x + 5.6, top + 32.6, fill=R)
        c.pie(x, top + 2, 7.5, 0, 180, G); c.arc(x, top + 2, 7.5, 0, 180, K, 1)
        c.line([(x, top + 12), (x, top + 30)], Y, 1)

# --- cobra frieze along the top ---
c.rect(26, 28, 374, 34, fill=Y, outline=K, w=1)
c.rect(26, 92, 374, 100, fill=Y, outline=K, w=1)
for i, x in enumerate(range(30, 370, 8)):
    c.rect(x, 94, x + 5, 98, fill=[R, G, WH][i % 3])
for i in range(11):
    x = 43 + i * 31.4
    c.poly([(x - 9, 91), (x - 11, 62), (x - 6, 50), (x, 46), (x + 6, 50), (x + 11, 62), (x + 9, 91)], Y, K, 1.1)
    c.poly([(x - 5, 91), (x - 6, 64), (x, 54), (x + 6, 64), (x + 5, 91)], [G, R][i % 2], K, .8)
    for j in range(4):
        c.line([(x - 5, 68 + j * 6), (x + 5, 68 + j * 6)], Y, 1)
    c.circ(x, 41, 6.5, fill=R, outline=K, w=1)

# --- stars in whatever lapis is left ---
pts = []
for _ in range(4000):
    x, y = random.uniform(26, 374), random.uniform(104, 470)
    if all((x - px) ** 2 + (y - py) ** 2 > 19 ** 2 for px, py in pts) and c.is_plain(x, y, 8, B):
        pts.append((x, y))
for x, y in pts:
    c.star(x, y, 5.2, Y, 1.1)

block_border(c, 6, 6, 394, 594, 14, [R, WH, G, WH], seg=11)
c.rect(20, 20, 380, 580, outline=K, w=1)
c.save()
