"""Morning — the Valley of the Kings at sunrise, 26 November 1922: el-Qurn, the cliffs,
the dig below the tomb of Ramesses VI, sixteen steps going down."""
import math, random
from common import *

random.seed(1922)
c = C(Y)

# ---------- sky: night-blue thinning into paper, then into gold ----------
c.rect(0, 0, 400, 300, fill=WH)
c.rect(0, 0, 400, 70, fill=B)
y = 70.0
for i in range(26):                      # blue rules thinning out
    t = i / 25
    th = 3.4 * (1 - t) + 0.5
    c.rect(0, y, 400, y + th, fill=B)
    y += th + 0.7 + 3.2 * t
y0 = y
for i in range(30):                      # gold rules thickening in
    t = i / 29
    th = 0.6 + 3.0 * t
    c.rect(0, y, 400, y + th, fill=Y)
    y += th + 2.6 * (1 - t) + 0.5
c.rect(0, y, 400, 320, fill=Y)
for _ in range(46):                      # last stars
    x, yy = random.uniform(6, 394), random.uniform(6, 92)
    r = random.choice([2.2, 2.2, 3, 4.2])
    c.star(x, yy, r, WH, .9)
# sun and its rays
SX, SY = 262, 212
for k in range(72):
    a = k * math.pi / 36
    r1 = 150 if k % 2 == 0 else 96
    if k % 6 == 0: r1 = 230
    c.line([(SX + 56 * math.cos(a), SY + 56 * math.sin(a)), (SX + r1 * math.cos(a), SY + r1 * math.sin(a))], R, 1 if k % 2 else 1.4)
c.circ(SX, SY, 50, fill=K); c.circ(SX, SY, 48.5, fill=R)
c.circ(SX, SY, 42, outline=Y, w=1.2)


def ridge(ctrl, rough=2.0, step=4):
    pts = []
    for (xa, ya), (xb, yb) in zip(ctrl, ctrl[1:]):
        n = max(1, int(abs(xb - xa) / step))
        for i in range(n):
            t = i / n
            pts.append((xa + (xb - xa) * t, ya + (yb - ya) * t + random.uniform(-rough, rough)))
    pts.append(ctrl[-1])
    return pts


def yat(pts, x):
    for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
        if xa <= x <= xb:
            return ya + (yb - ya) * (x - xa) / max(1e-6, xb - xa)
    return pts[-1][1]


# ---------- el-Qurn, the pyramid-shaped peak, against the light ----------
far = ridge([(0, 232), (40, 214), (78, 196), (112, 160), (136, 128), (150, 118), (166, 132), (196, 170),
             (226, 200), (262, 214), (300, 206), (332, 190), (368, 196), (400, 180)], 2.2)
c.poly(far + [(400, 330), (0, 330)], R)
c.line(far, K, 1.6)
for x in range(2, 400, 3):               # the unlit face: hatching falling off the crest
    yt = yat(far, x)
    slope = yat(far, min(399, x + 6)) - yt
    lit = slope > 1.5                    # faces falling to the right catch the sun
    ln = random.uniform(18, 60) if not lit else random.uniform(4, 14)
    if random.random() < (0.95 if not lit else 0.5):
        c.line([(x, yt + 2), (x - ln * .28, yt + ln)], K, 1)
    if lit and random.random() < .8:
        l2 = random.uniform(14, 40)
        c.line([(x, yt + 3), (x + l2 * .35, yt + l2)], Y, 1.2)
for yy in range(150, 300, 9):            # bedding planes
    x = 0
    while x < 400:
        ln = random.uniform(10, 34)
        if yy > yat(far, x) + 10 and yy > yat(far, min(399, x + ln)) + 10:
            c.line([(x, yy + random.uniform(-1, 1)), (x + ln, yy + random.uniform(-1, 1))], K, 1)
        x += ln + random.uniform(5, 16)

# ---------- the cliff wall: buttresses, lit from the right ----------
top = ridge([(0, 268), (50, 250), (90, 262), (128, 246), (170, 270), (214, 282), (250, 268), (290, 250),
             (330, 262), (368, 244), (400, 252)], 3.5, 3)
x = -4.0
while x < 404:
    w = random.uniform(9, 24)
    yt = yat(top, max(0, min(399, x + w / 2))) + random.uniform(-4, 4)
    yb = 352 + 22 * math.sin(x / 60.0) + random.uniform(-3, 3)
    sh = w * random.uniform(.32, .5)
    c.poly([(x, yt + 3), (x + w * .5, yt), (x + w, yt + 4), (x + w + 2, yb), (x - 2, yb)], Y)
    c.poly([(x, yt + 3), (x + sh, yt + 1), (x + sh + 1, yb), (x - 2, yb)], R)          # shadow flank
    c.poly([(x, yt + 3), (x + w * .5, yt), (x + w, yt + 4), (x + w * .5, yt + 7)], WH, K, .8)  # cap rock
    c.line([(x, yt + 3), (x - 2, yb)], K, 1.5)
    n = int(sh / 2.2)
    for i in range(n):                    # hatch in the shadow
        hx = x + 1.5 + i * 2.2
        c.line([(hx, yt + 8 + random.uniform(0, 12)), (hx - .6, yb - random.uniform(0, 30))], K, .9)
    for i in range(random.randint(1, 3)):  # cracks in the lit face
        hx = x + sh + random.uniform(2, max(3, w - sh - 1))
        ya = random.uniform(yt + 10, yb - 30)
        c.line([(hx, ya), (hx + random.uniform(-1, 1), ya + random.uniform(10, 34))], K, .9)
    for yy in (yt + (yb - yt) * .38, yt + (yb - yt) * .7):   # ledges
        c.line([(x + sh, yy + random.uniform(-2, 2)), (x + w + 1, yy + random.uniform(-2, 2))], R, 1.4)
    x += w

# ---------- scree and the valley floor ----------
scree = ridge([(0, 352), (60, 340), (130, 356), (200, 370), (270, 356), (340, 338), (400, 348)], 2, 5)
c.poly(scree + [(400, 600), (0, 600)], Y)
c.line(scree, K, 1.2)
for _ in range(900):
    x, yy = random.uniform(0, 400), random.uniform(345, 600)
    if yy < yat(scree, x) + 3: continue
    r = random.random()
    if r < .55: c.line([(x, yy), (x + random.uniform(2, 5), yy + random.uniform(-.6, .6))], K, .9)
    elif r < .8: c.circ(x, yy, random.uniform(.8, 1.6), fill=R)
    else: c.poly([(x, yy), (x + 4, yy - 2.5), (x + 7, yy + .5), (x + 3, yy + 2)], WH, K, .7)
for k in range(9):                        # talus fans coming off the cliff foot
    fx = 20 + k * 46 + random.uniform(-8, 8)
    fy = yat(scree, fx) + 2
    for i in range(9):
        a = math.radians(60 + i * 7.5)
        ln = random.uniform(14, 36)
        c.line([(fx, fy), (fx + ln * math.cos(a), fy + ln * math.sin(a))], R, 1)
# the path up the wadi
pathL = bez((150, 600), (190, 540), (120, 500), (176, 470), 30)
pathR = bez((214, 470), (190, 505), (262, 540), (236, 600), 30)
c.poly(pathL + pathR, WH)
c.line(pathL, K, 1); c.line(pathR, K, 1)
for _ in range(60):
    t = random.random(); i = int(t * 30)
    xa, ya = pathL[i]; xb, yb = pathR[30 - i] if False else pathR[min(30, 30 - i)]
    u = random.uniform(.15, .85)
    c.line([(xa + (xb - xa) * u, ya), (xa + (xb - xa) * u + 4, ya)], K, .8)

# ---------- the tomb of Ramesses VI, in the hillside above ----------
c.poly([(150, 420), (172, 384), (228, 384), (250, 420)], Y, K, 1.2)
for i in range(7):                        # dry-stone revetment
    for j in range(4):
        bx, by = 156 + i * 13 + (j % 2) * 6 - j * 0, 388 + j * 8
        if 150 + (by - 384) * -.6 < bx < 236 + (by - 384) * .5:
            c.rect(bx, by, bx + 11, by + 6, fill=WH if (i + j) % 3 else Y, outline=K, w=.8)
c.poly([(186, 420), (189, 390), (211, 390), (214, 420)], WH, K, 1.2)
c.poly([(191, 420), (193, 395), (207, 395), (209, 420)], K)
c.rect(187, 386, 213, 390, fill=R, outline=K, w=.8)

# ---------- the cut: sixteen steps ----------
nl, nr, fl, fr = (156, 500), (244, 500), (181, 426), (219, 426)       # rim, near and far
bl, br = (187, 452), (213, 452)                                       # foot of the stair
c.poly([nl, fl, bl], K)                                               # shadowed wall
c.poly([nr, fr, br], WH, K, 1)                                        # sunlit wall
for i in range(8):
    t = (i + 1) / 9
    c.line([(nr[0] + (fr[0] - nr[0]) * t, nr[1] + (fr[1] - nr[1]) * t),
            (nr[0] + (br[0] - nr[0]) * t, nr[1] + (br[1] - nr[1]) * t)], K, .8)
c.poly([fl, fr, br, bl], WH, K, 1)
c.poly([(192, 452), (192, 432), (208, 432), (208, 452)], K)           # the doorway
c.rect(190, 429, 210, 432, fill=R)
for i in range(16):                                                    # treads
    t0, t1 = (i / 16) ** 1.25, ((i + 1) / 16) ** 1.25
    def at(t): return [(nl[0] + (bl[0] - nl[0]) * t, nl[1] + (bl[1] - nl[1]) * t),
                       (nr[0] + (br[0] - nr[0]) * t, nr[1] + (br[1] - nr[1]) * t)]
    a, b = at(t0), at(t1)
    mid = at(t0 + (t1 - t0) * .62)
    c.poly([a[0], a[1], mid[1], mid[0]], WH if i < 12 else Y)
    c.poly([mid[0], mid[1], b[1], b[0]], K if i % 2 == 0 or i > 9 else R)
c.line([nl, fl, fr, nr, nl], K, 1.6)
for i in range(9):                         # stones along the rim
    t = i / 9
    for (p, q, s) in ((nl, fl, -1), (nr, fr, 1)):
        bx, by = p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t
        c.poly([(bx, by), (bx + s * 9, by - 1), (bx + s * 10, by - 7), (bx + s * 1, by - 7)], WH if i % 2 else Y, K, .8)

# ---------- spoil heap, right ----------
heap = [(268, 520), (290, 486), (318, 470), (352, 478), (384, 500), (400, 518), (400, 532), (268, 532)]
c.poly(heap, WH, K, 1.2)
for _ in range(110):
    x, yy = random.uniform(272, 398), random.uniform(474, 530)
    if yy > 470 + abs(x - 325) * .55 + 6:
        c.line([(x, yy), (x + random.uniform(2, 5), yy + random.uniform(1, 3))], K if random.random() < .7 else R, .9)


def worker(x, y, h, d=1, load=True, robe=WH):
    """A basket-carrier; (x, y) is the feet, h the height."""
    c.line([(x - 2, y), (x - 1.5, y - h * .25)], K, 1.4); c.line([(x + 2.5 * d, y), (x + 1.5, y - h * .25)], K, 1.4)
    c.poly([(x - h * .17, y - h * .2), (x + h * .17, y - h * .2), (x + h * .12, y - h * .72), (x - h * .12, y - h * .72)], robe, K, .9)
    c.circ(x, y - h * .8, h * .1, fill=K)
    if load:
        c.line([(x + h * .1, y - h * .66), (x + h * .2 * d, y - h * .95)], K, 1.2)
        c.pie(x, y - h * .9, h * .2, 180, 360, R, ry=h * .14)
        c.line([(x - h * .22, y - h * .9), (x + h * .22, y - h * .9)], K, 1)
    else:
        c.rect(x - h * .12, y - h * .93, x + h * .12, y - h * .86, fill=WH, outline=K, w=.7)   # turban


# the basket line: out of the cut, across, and up the heap
line = bez((238, 496), (262, 512), (284, 516), (300, 498), 6) + bez((312, 490), (322, 484), (334, 480), (344, 480), 2)
for i, (x, yy) in enumerate(line):
    worker(x, yy, 25 - i * .5, 1, True, WH if i % 3 else B)
for i, (x, yy) in enumerate(bez((330, 548), (300, 556), (268, 548), (250, 520), 4)):   # coming back, empty-handed
    worker(x, yy, 27, -1, False, WH if i % 2 else B)

# ---------- the camp, left ----------
def tent(x, y, w, h):
    c.poly([(x - w / 2, y), (x, y - h), (x + w / 2, y)], WH, K, 1.2)
    for i in range(1, 6):
        t = i / 6
        c.line([(x, y - h), (x - w / 2 + w * t, y)], B, 1.2)
    c.poly([(x - 4, y), (x, y - h * .55), (x + 4, y)], K)
    c.line([(x, y - h), (x, y - h - 7)], K, 1); c.poly([(x, y - h - 7), (x + 7, y - h - 5), (x, y - h - 3)], R)
    c.line([(x - w / 2, y), (x - w / 2 - 8, y + 4)], K, .8); c.line([(x + w / 2, y), (x + w / 2 + 8, y + 4)], K, .8)
tent(52, 478, 48, 38); tent(104, 494, 40, 31)
# a donkey with water jars
dx, dy = 96, 548
c.ell(dx - 15, dy - 20, dx + 15, dy - 6, fill=K)
for lx in (-11, -6, 8, 12): c.line([(dx + lx, dy - 9), (dx + lx - 1, dy + 4)], K, 1.8)
c.poly([(dx + 12, dy - 16), (dx + 22, dy - 28), (dx + 28, dy - 22), (dx + 20, dy - 12)], K)
c.line([(dx + 22, dy - 27), (dx + 21, dy - 36)], K, 1.8); c.line([(dx + 25, dy - 26), (dx + 27, dy - 35)], K, 1.8)
c.line([(dx - 15, dy - 14), (dx - 20, dy - 4)], K, 1.2)
c.ell(dx - 8, dy - 26, dx + 2, dy - 8, fill=R, outline=K, w=1); c.ell(dx + 1, dy - 25, dx + 10, dy - 9, fill=WH, outline=K, w=1)
worker(70, 556, 30, 1, False, WH)
# crates and a sieve tripod by the cut
for (bx, by, col) in ((118, 520, WH), (132, 524, R), (122, 508, WH)):
    c.rect(bx, by - 11, bx + 15, by, fill=col, outline=K, w=1); c.line([(bx, by - 5.5), (bx + 15, by - 5.5)], K, .8)
c.line([(262, 470), (270, 446), (278, 470)], K, 1.3); c.line([(270, 446), (273, 472)], K, 1.3)
c.ell(264, 456, 276, 462, fill=WH, outline=K, w=.9)

# ---------- foreground: dark shoulders of rock framing the wadi ----------
for side, ctrl in ((-1, [(0, 500), (30, 512), (64, 548), (96, 572), (128, 600)]),
                   (1, [(272, 600), (300, 574), (336, 566), (366, 548), (400, 540)])):
    rp = ridge(ctrl, 2.5, 4)
    c.poly(rp + [(400 if side > 0 else 0, 600)] + ([(0, 600)] if side < 0 else [(272, 600)]), K)
    for (x, yy) in rp[::2]:
        for i in range(1, 9):
            yb = yy + i * 9 + random.uniform(-2, 2)
            if yb < 598:
                ln = random.uniform(5, 16)
                c.line([(x + random.uniform(-3, 3), yb), (x + ln, yb + random.uniform(-2, 2))], Y if random.random() < .7 else R, 1)
for (bx, by, r) in ((158, 578, 13), (212, 586, 10), (252, 572, 8)):     # boulders
    pts = [(bx + r * (1 + .25 * math.sin(k * 2.3)) * math.cos(k * math.pi / 4), by + r * .7 * math.sin(k * math.pi / 4)) for k in range(8)]
    c.poly(pts, WH, K, 1.2)
    for i in range(4):
        c.line([(bx - r * .7 + i * 3, by + r * .1), (bx - r * .5 + i * 3, by + r * .55)], K, .8)

block_border(c, 0, 0, 400, 600, 8, [K, WH, R, WH], seg=10)
c.save()
