"""Evening — a garden pool in the manner of the Theban tomb painters: the pond in plan,
the trees laid flat around it, fish and ducks in profile, the sun going into the horizon."""
import math, random
from common import *

random.seed(18)
c = C(WH)


class T:
    """Local frame: origin at a tree's foot, -y is 'up the tree', rotated by ang (degrees)."""
    def __init__(s, ox, oy, ang=0, sc=1.0):
        s.ox, s.oy, s.sc = ox, oy, sc
        a = math.radians(ang); s.ca, s.sa = math.cos(a), math.sin(a)

    def __call__(s, x, y):
        x *= s.sc; y *= s.sc
        return (s.ox + x * s.ca - y * s.sa, s.oy + x * s.sa + y * s.ca)

    def pts(s, ps): return [s(x, y) for x, y in ps]


def leaf(t, x0, y0, ang, ln, wd, fill, rib=K):
    a = math.radians(ang); ca, sa = math.cos(a), math.sin(a)
    def L(u, v): return t(x0 + u * ca - v * sa, y0 + u * sa + v * ca)
    c.poly([L(0, 0), L(ln * .3, -wd), L(ln * .75, -wd * .8), L(ln, 0), L(ln * .75, wd * .8), L(ln * .3, wd)], fill, K, .8)
    if rib: c.line([L(0, 0), L(ln * .9, 0)], rib, .8)


def date_palm(t):
    c.poly(t.pts([(-5.5, 0), (5.5, 0), (3.5, -62), (-3.5, -62)]), Y, K, 1.1)
    for i in range(10):
        y = -4 - i * 6
        c.line([t(-5 + i * .2, y), t(0, y - 3.5), t(5 - i * .2, y)], K, .9)
    for sd in (-1, 1):                                    # date clusters
        st = bez((sd * 2, -60), (sd * 12, -66), (sd * 15, -56), (sd * 14, -44), 8)
        c.line(t.pts(st), Y, 1.4)
        x, y = t(sd * 14, -38)
        c.circ(x, y, 7.5 * t.sc, fill=R, outline=K, w=.9)
        for k in range(6):
            px, py = t(sd * 14 + 3.4 * math.cos(k * 1.05), -38 + 3.4 * math.sin(k * 1.05))
            c.circ(px, py, 1, fill=K)
    for ang in (-170, -10, -150, -30, -130, -50, -112, -68, -90):   # fronds
        droop = 1 if ang in (-170, -10) else 0
        ln = 44 - abs(ang + 90) * .12
        a = math.radians(ang)
        mid = [(ln * f * math.cos(a), -62 + ln * f * math.sin(a) + droop * 26 * f * f) for f in (0, .25, .5, .75, 1)]
        for i in range(1, 5):
            (xa, ya), (xb, yb) = mid[i - 1], mid[i]
            seg = math.degrees(math.atan2(yb - ya, xb - xa))
            for sd in (-1, 1):
                leaf(t, xa, ya, seg + sd * 38, 13 - i * 1.2, 2.6, G, None)
        c.line(t.pts(mid), K, 1.2)
    c.circ(*t(0, -62), 3.5 * t.sc, fill=Y, outline=K, w=.9)


def sycamore(t):
    c.poly(t.pts([(-6, 0), (6, 0), (3.5, -34), (10, -52), (5, -54), (0, -40), (-5, -54), (-10, -52), (-3.5, -34)]), Y, K, 1.1)
    c.line(t.pts([(-2, -4), (-1, -30)]), K, .8); c.line(t.pts([(2.5, -8), (1.5, -26)]), K, .8)
    blob = [(34 * math.cos(a) * (1 + .09 * math.sin(5 * a)), -66 + 36 * math.sin(a) * (1 + .07 * math.cos(4 * a))) for a in np.linspace(0, 2 * math.pi, 44)]
    c.poly(t.pts(blob), G, K, 1.3)
    for br in ([(0, -40), (-4, -60), (-16, -78)], [(0, -40), (6, -64), (17, -84)], [(-4, -60), (-20, -58)], [(6, -64), (22, -62)], [(0, -50), (0, -92)]):
        c.line(t.pts(br), Y, 1.5)
    for _ in range(46):                                   # leaves
        a, r = random.uniform(0, 2 * math.pi), random.uniform(.1, .86) ** .6
        x, y = 30 * r * math.cos(a), -66 + 32 * r * math.sin(a)
        ang = random.uniform(0, 360)
        c.line([t(x, y), t(x + 5 * math.cos(math.radians(ang)), y + 5 * math.sin(math.radians(ang)))], K, 1.1)
    for _ in range(13):                                   # figs
        a, r = random.uniform(0, 2 * math.pi), random.uniform(.2, .8)
        px, py = t(30 * r * math.cos(a), -66 + 32 * r * math.sin(a))
        c.circ(px, py, 2.9 * t.sc, fill=R, outline=K, w=.8)


def doum(t):
    c.poly(t.pts([(-5, 0), (5, 0), (3.5, -36), (-3.5, -36)]), Y, K, 1.1)
    for sd in (-1, 1):
        c.poly(t.pts([(sd * -1, -34), (sd * 4, -36), (sd * 20, -62), (sd * 15, -64)]), Y, K, 1.1)
        fx, fy = sd * 18, -64
        for k in range(9):                                # fan
            a0 = -90 + sd * 20 - 68 + k * 15
            leaf(t, fx, fy, a0, 30, 4.2, G, K)
        for k in range(3):
            px, py = t(fx - sd * 7 + k * 3 * sd, fy + 6 + k * 3)
            c.circ(px, py, 3 * t.sc, fill=R, outline=K, w=.8)
    for i in range(6):
        c.line([t(-4.6, -3 - i * 5.5), t(4.6, -5.5 - i * 5.5)], K, .9)


def pomegranate(t):
    c.line(t.pts([(0, 0), (0, -30)]), K, 3.2); c.line(t.pts([(0, 0), (0, -30)]), Y, 1.6)
    for (bx, by, ang) in ((0, -30, -90), (0, -22, -140), (0, -22, -40), (0, -12, -160), (0, -12, -20)):
        a = math.radians(ang); ln = 36 if ang == -90 else 30
        ex, ey = bx + ln * math.cos(a), by + ln * math.sin(a)
        for f in (.25, .5, .75, 1):
            for sd in (-1, 1):
                leaf(t, bx + (ex - bx) * f, by + (ey - by) * f, ang + sd * 50, 10, 2.6, G, None)
        c.line(t.pts([(bx, by), (ex, ey)]), K, 1)
        px, py = t(ex, ey)
        c.circ(px, py, 5 * t.sc, fill=R, outline=K, w=1)
        qx, qy = t(ex + 6.5 * math.cos(a), ey + 6.5 * math.sin(a))
        c.circ(qx, qy, 1.8 * t.sc, fill=Y, outline=K, w=.7)


KINDS = [date_palm, sycamore, doum, sycamore, date_palm]

# ---------- the pool ----------
PX0, PY0, PX1, PY1 = 116, 196, 284, 424
c.rect(PX0 - 26, PY0 - 26, PX1 + 26, PY1 + 26, fill=G, outline=K, w=1.4)       # the planted margin
c.rect(PX0 - 9, PY0 - 9, PX1 + 9, PY1 + 9, fill=Y, outline=K, w=1.4)           # mud-brick coping
for x in range(PX0 - 9, PX1 + 9, 9):
    c.line([(x, PY0 - 9), (x, PY0)], K, .8); c.line([(x + 4, PY1), (x + 4, PY1 + 9)], K, .8)
for y in range(PY0 - 9, PY1 + 9, 9):
    c.line([(PX0 - 9, y), (PX0, y)], K, .8); c.line([(PX1, y + 4), (PX1 + 9, y + 4)], K, .8)
c.rect(PX0, PY0, PX1, PY1, fill=B, outline=K, w=1.4)
for j, y in enumerate(range(PY0 + 7, PY1 - 3, 8)):                              # water: the zigzag sign
    pts = [(PX0 + 2 + i * 5, y + (2.2 if (i + j) % 2 else -2.2)) for i in range(34)]
    c.line(pts, K, 1)
# papyrus and poppies around the margin
def margin_plant(x, y, ang, k):
    t = T(x, y, ang)
    if k % 3 == 0:                                                               # papyrus umbel
        c.line(t.pts([(0, 0), (0, -9)]), K, 1)
        for a in range(-60, 61, 20):
            c.line([t(0, -9), t(8 * math.sin(math.radians(a)), -9 - 8 * math.cos(math.radians(a)))], Y, 1.2)
    elif k % 3 == 1:                                                             # poppy
        c.line(t.pts([(0, 0), (0, -9)]), K, 1); c.circ(*t(0, -11), 3.3, fill=R, outline=K, w=.8)
    else:                                                                        # cornflower
        c.line(t.pts([(0, 0), (0, -9)]), K, 1); c.circ(*t(0, -11), 3.1, fill=B, outline=WH, w=.9)
k = 0
for x in range(PX0 - 4, PX1 + 8, 12):
    margin_plant(x, PY0 - 10, 0, k); margin_plant(x, PY1 + 10, 180, k + 1); k += 1
for y in range(PY0 + 2, PY1 + 2, 12):
    margin_plant(PX0 - 10, y, -90, k); margin_plant(PX1 + 10, y, 90, k + 2); k += 1


def fish(x, y, d=1, s=1.0):
    def P(px, py): return (x + d * px * s, y + py * s)
    c.poly([P(-15, 0), P(-25, -8), P(-22, 0), P(-25, 8)], R, K, .9)                 # tail
    c.poly([P(-8, -7), P(2, -13), P(10, -6)], R, K, .9); c.poly([P(-4, 7), P(2, 12), P(7, 6)], R, K, .9)
    body = [P(18 * math.cos(a) - 0, 8.5 * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 24)]
    c.poly(body, WH, K, 1.1)
    for i in range(5):
        c.arc(x + d * (-10 + i * 5) * s, y, 5 * s, 300 if d > 0 else 120, 60 if d > 0 else 240, K, .8, ry=6.5 * s)
    c.circ(*P(12, -2), 1.7, fill=K)
    c.line([P(8, -7), P(7, 7)], K, .8)


def duck(x, y, d=1):
    def P(px, py): return (x + d * px, y + py)
    c.poly([P(-17, -2), P(-25, -9), P(-20, 1)], K)
    body = [P(17 * math.cos(a), 8 * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 24)]
    c.poly(body, WH, K, 1.1)
    c.poly([P(-12, -3), P(4, -6), P(8, 1), P(-8, 4)], Y, K, .8)                     # wing
    for i in range(4): c.line([P(-9 + i * 4, -3), P(-7 + i * 4, 2)], K, .8)
    neck = bez(P(12, -3), P(18, -8), P(15, -16), P(20, -19), 8)
    c.line(neck, K, 5.5); c.line(neck, G, 3.2)
    c.circ(*P(21, -20), 4.6, fill=G, outline=K, w=.9); c.circ(*P(22, -21), 1, fill=WH)
    c.poly([P(24, -22), P(32, -20), P(24, -17.5)], Y, K, .8)
    c.line([P(13, -7), P(16, -7)], WH, 1.4)
    for i in range(3): c.arc(x, y + 9, 12 + i * 5, 20, 160, WH, 1, ry=3 + i)        # ripples


def pad(x, y, r, rot):
    c.circ(x, y, r, fill=G, outline=K, w=1)
    c.pie(x, y, r + 1, rot, rot + 34, B)
    for kk in range(7):
        a = math.radians(rot + 60 + kk * 42)
        c.line([(x, y), (x + (r - 2) * math.cos(a), y + (r - 2) * math.sin(a))], K, .7)


def lotus(x, y, s=1.0, closed=False):
    """Seen from the side though the pool is seen from above — as the tomb painters did."""
    spread = [(-13, G), (13, G), (-8, WH), (8, WH), (-3.5, WH), (3.5, WH), (0, WH)]
    if closed: spread = [(-4, G), (4, G), (0, WH)]
    c.line([(x, y), (x, y + 13 * s)], G, 1.6)
    for dx, col in spread:
        tipx, tipy = x + dx * s, y - (25 - abs(dx) * .55) * s
        c.poly([(x - 2.5 * s, y), (x + dx * .6 * s - 2.6 * s, y - 13 * s), (tipx, tipy), (x + dx * .6 * s + 2.6 * s, y - 13 * s), (x + 2.5 * s, y)], col, K, .9)
    if not closed: c.circ(x, y - 22 * s, 1.4, fill=R)
    c.pie(x, y, 5.5 * s, 0, 180, Y); c.arc(x, y, 5.5 * s, 0, 180, K, .9)


for (x, y, r, rot) in ((136, 214, 10, 20), (262, 222, 11, 200), (150, 298, 9, 90), (254, 318, 10, 300), (200, 252, 8, 140),
                       (140, 392, 11, 250), (262, 400, 10, 60), (206, 346, 9, 10), (128, 340, 7, 170), (272, 274, 7, 320)):
    pad(x, y, r, rot)
fish(172, 226, 1, 1.0); fish(232, 262, -1, .9); fish(150, 366, 1, .85); fish(244, 356, -1, 1.05); fish(198, 408, 1, .8)
duck(222, 300, -1); duck(168, 326, 1); duck(226, 222, 1)
for (x, y, s, cl) in ((132, 262, 1, False), (268, 250, .9, True), (182, 282, .9, True), (268, 370, 1, False), (184, 384, 1, False),
                      (132, 316, .8, True), (212, 240, .75, False), (232, 398, .8, True)):
    lotus(x, y, s, cl)

# ---------- the orchard, laid flat on all four sides ----------
for i in range(5):
    x = 52 + i * 74
    KINDS[i](T(x, 162, 0, 1.0))                              # far side, upright
    KINDS[(i + 2) % 5](T(x, 574, 0, 1.0))                    # near side, upright
for i in range(3):
    y = 232 + i * 78
    [sycamore, date_palm, doum][i](T(90, y, -90, .66))       # west side, heads to the west
    [doum, sycamore, date_palm][i](T(310, y, 90, .66))       # east side
for (x, y, ang) in ((96, 196, -45), (304, 196, 45), (100, 440, -128), (300, 440, 128)):
    pomegranate(T(x, y, ang, .78))
c.line([(22, 163), (378, 163)], K, 1.4); c.line([(22, 575), (378, 575)], K, 1.4)   # ground lines

# ---------- top register: akhet, the sun in the horizon, between lotus and bud ----------
c.rect(22, 20, 378, 60, fill=Y, outline=K, w=1.2)
c.circ(200, 39, 15, fill=R, outline=K, w=1.2)
for sd in (-1, 1):
    hill = [(200 + sd * 4, 60)] + bez((200 + sd * 4, 60), (200 + sd * 10, 30), (200 + sd * 36, 30), (200 + sd * 44, 60), 14)
    c.poly(hill, WH, K, 1.2)
    for j in range(5): c.circ(200 + sd * (14 + j * 5), 54 - (j % 2) * 5, 1, fill=R)
    for i in range(6):
        x = 200 + sd * (62 + i * 20)
        if i % 2 == 0:
            for dx, col in ((-9, G), (9, G), (-5, WH), (5, WH), (0, B)):
                c.poly([(x - 2, 58), (x + dx * .6 - 2, 44), (x + dx, 27 + abs(dx) * .6), (x + dx * .6 + 2, 44), (x + 2, 58)], col, K, .8)
        else:
            c.line([(x, 58), (x, 44)], G, 1.6); c.ell(x - 3.4, 30, x + 3.4, 46, fill=R, outline=K, w=.8)

# small flowers wherever the ground is still bare
pts = []
for _ in range(5000):
    x, y = random.uniform(24, 376), random.uniform(66, 572)
    if all((x - px) ** 2 + (y - py) ** 2 > 13 ** 2 for px, py in pts) and c.is_plain(x, y, 6, WH):
        pts.append((x, y))
for i, (x, y) in enumerate(pts):
    c.line([(x, y + 4), (x, y - 1)], G, 1.2)
    c.line([(x, y + 2), (x + 3, y)], G, 1); c.line([(x, y + 2), (x - 3, y)], G, 1)
    c.circ(x, y - 3, 2.3, fill=[R, B, Y, R][i % 4], outline=K, w=.7)

block_border(c, 6, 6, 394, 594, 14, [G, WH, B, WH, R, WH], seg=11)
c.rect(20, 20, 380, 580, outline=K, w=1)
c.save()
