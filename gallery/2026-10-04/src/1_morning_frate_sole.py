# 1 — morning — "Frate Sole"
# Dawn over Assisi from the Umbrian plain: a medieval sun-face with alternating straight and
# flame rays over Monte Subasio; the Rocca on the ridge, the town stacked up the flank,
# the Basilica of San Francesco on its arched substructure at the left; mist, the patchwork
# plain with Santa Maria degli Angeli, terraced olive groves, cypresses and a friar on the path.
import os, sys, math
sys.path.insert(0, os.path.dirname(__file__))
from common import *

rng = np.random.default_rng(31226)
A = np.array(new(WH)[0])
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)


# ---------------------------------------------------------------- helpers (1x coords)
def P(pts):
    return [(int(round(x)) * S, int(round(y)) * S) for x, y in pts]

def draw(fn):
    global A
    img = Image.fromarray(A)
    fn(ImageDraw.Draw(img))
    A = np.array(img)

def M(fn):
    return mask_of(fn)

def put(mask, col):
    A[mask] = col

def scr(mask, tone, ink, paper=None):
    t = tone if isinstance(tone, np.ndarray) else np.full((H, W), tone, np.float32)
    m = screen(t)
    A[mask & m] = ink
    if paper is not None:
        A[mask & ~m] = paper

def poly_m(pts):
    return M(lambda d: d.polygon(P(pts), fill=255))

def rect_m(x0, y0, x1, y1):
    return M(lambda d: d.rectangle([int(x0) * S, int(y0) * S, int(x1) * S - 1, int(y1) * S - 1], fill=255))

def ell_m(cx, cy, rx, ry):
    return M(lambda d: d.ellipse([int(cx - rx) * S, int(cy - ry) * S, int(cx + rx) * S, int(cy + ry) * S], fill=255))

def R_(d, x0, y0, x1, y1, c):
    d.rectangle([int(x0) * S, int(y0) * S, int(x1) * S - 1, int(y1) * S - 1], fill=c)

def L_(d, pts, c, w=1):
    d.line(P(pts), fill=c, width=w * S, joint="curve")

def full(t):
    return np.full((H, W), t, np.float32)


# ---------------------------------------------------------------- sky: aureole rings
SX, SY = 200, 104
dist = np.hypot(xx - SX, yy - SY)
bands = [(98, "pale"), (122, 0.0), (146, 0.125), (174, 0.25), (210, 0.375), (9999, 0.5)]
prev = 0
for r, t in bands:
    ring = up((dist >= prev) & (dist < r))
    if t == "pale":
        scr(ring, 0.5, Y, WH)
    else:
        scr(ring, t, R, Y)
    prev = r
# thin dotted circlets between rings (manuscript ruling)
def ring_dots(rad, col, step):
    n = int(2 * math.pi * rad / step)
    def f(d):
        for i in range(n):
            a = 2 * math.pi * i / n
            x, y = SX + rad * math.cos(a), SY + rad * math.sin(a)
            R_(d, x - 1, y - 1, x + 1, y + 1, col)
    draw(f)
ring_dots(122, R, 6)
ring_dots(146, WH, 7)
ring_dots(174, Y, 8)

# clouds: scalloped bars, white with a yellow belly and a red underline
def cloud(x0, x1, yb, seed):
    r = np.random.default_rng(seed)
    def f(d):
        R_(d, x0, yb - 5, x1, yb, WH)
        x = x0 + 3
        while x < x1 - 3:
            rad = r.integers(3, 7)
            d.ellipse([int(x - rad) * S, int(yb - 5 - rad) * S, int(x + rad) * S, int(yb - 5 + rad) * S], fill=WH)
            x += rad + r.integers(1, 4)
        R_(d, x0 + 2, yb - 2, x1 - 2, yb, Y)
        R_(d, x0 + 5, yb, x1 - 4, yb + 2, R)
    draw(f)
cloud(14, 96, 52, 1)
cloud(30, 110, 160, 2)
cloud(300, 388, 40, 3)
cloud(288, 372, 150, 4)
cloud(330, 392, 186, 5)

# ---------------------------------------------------------------- the sun
NR = 32
def rays(d):
    for i in range(NR):
        a = 2 * math.pi * (i + 0.5) / NR - math.pi / 2
        if i % 2 == 0:  # straight ray
            r0, r1, hw = 44, 112, math.radians(4.2)
            pts = [(SX + r0 * math.cos(a - hw), SY + r0 * math.sin(a - hw)),
                   (SX + r1 * math.cos(a), SY + r1 * math.sin(a)),
                   (SX + r0 * math.cos(a + hw), SY + r0 * math.sin(a + hw))]
            d.polygon(P(pts), fill=Y, outline=R, width=2 * S)
        else:  # wavy flame ray
            left, right = [], []
            r0, r1 = 44, 92
            for k in range(15):
                f = k / 14
                rr = r0 + (r1 - r0) * f
                off = math.sin(f * 3 * math.pi) * 0.09 * (1 - 0.3 * f)
                w = 0.075 * (1 - f) + 0.004
                left.append((SX + rr * math.cos(a + off - w), SY + rr * math.sin(a + off - w)))
                right.append((SX + rr * math.cos(a + off + w), SY + rr * math.sin(a + off + w)))
            d.polygon(P(left + right[::-1]), fill=R)
draw(rays)

def sunface(d):
    r = 48
    d.ellipse([(SX - r) * S, (SY - r) * S, (SX + r) * S, (SY + r) * S], fill=R)
    r = 45
    d.ellipse([(SX - r) * S, (SY - r) * S, (SX + r) * S, (SY + r) * S], fill=Y)
    # beaded ring
    for i in range(36):
        a = 2 * math.pi * i / 36
        x, y = SX + 41 * math.cos(a), SY + 41 * math.sin(a)
        R_(d, x - 1, y - 1, x + 1, y + 1, R)
    r = 37
    d.ellipse([(SX - r) * S, (SY - r) * S, (SX + r) * S, (SY + r) * S], fill=Y, outline=R, width=2 * S)
draw(sunface)
# face shading: a soft white bloom on the brow
scr(up((np.hypot(xx - SX + 8, yy - SY + 14) < 16)), 0.5, WH)
def face(d):
    # brows
    d.arc([(SX - 24) * S, (SY - 16) * S, (SX - 4) * S, (SY + 2) * S], 200, 330, fill=R, width=2 * S)
    d.arc([(SX + 4) * S, (SY - 16) * S, (SX + 24) * S, (SY + 2) * S], 210, 340, fill=R, width=2 * S)
    # eyes: almond whites, black pupils
    for ex in (-13, 13):
        d.ellipse([(SX + ex - 7) * S, (SY - 6) * S, (SX + ex + 7) * S, (SY + 1) * S], fill=WH, outline=R, width=2 * S)
        R_(d, SX + ex - 2, SY - 5, SX + ex + 2, SY, K)
    # nose
    L_(d, [(SX, SY - 8), (SX - 1, SY + 6), (SX - 4, SY + 10), (SX + 3, SY + 11)], R, 2)
    # mouth
    d.arc([(SX - 11) * S, (SY + 8) * S, (SX + 11) * S, (SY + 23) * S], 20, 160, fill=R, width=2 * S)
    L_(d, [(SX - 5, SY + 19), (SX + 5, SY + 19)], R, 2)
draw(face)
# cheeks
for cx in (SX - 20, SX + 20):
    scr(up(np.hypot(xx - cx, yy - SY - 10) < 6), 0.5, R)

# swallows
def swallow(d, x, y, s, flip=1):
    pts = [(x - 6 * s, y - 2 * s), (x - 2 * s, y), (x, y - 1 * s), (x + 2 * s, y),
           (x + 6 * s, y - 3 * s), (x + 3 * s, y + 1 * s), (x + 1 * s, y + 1.5 * s),
           (x + 2 * s, y + 4 * s), (x, y + 2 * s), (x - 2 * s, y + 4 * s), (x - 1 * s, y + 1.5 * s),
           (x - 3 * s, y + 1 * s)]
    if flip < 0:
        pts = [(2 * x - px, py) for px, py in pts]
    d.polygon(P(pts), fill=K)
draw(lambda d: [swallow(d, *a) for a in
                [(62, 92, 1.4), (88, 108, 1.1), (44, 124, 1.0, -1), (330, 92, 1.3, -1),
                 (352, 112, 1.0), (312, 210, 1.0), (96, 205, 1.1, -1), (260, 30, 1.0)]])


# ---------------------------------------------------------------- mountains
def ridge(x, pts, amp=2.5, seed=0):
    xs, ys = zip(*pts)
    base = np.interp(x, xs, ys)
    n = noise(1, W + 8, 14, seed=seed, octaves=3)[0][: len(np.atleast_1d(x))] if False else 0
    return base

xs = np.arange(W, dtype=np.float32)
nz = noise(8, W, 10, seed=7, octaves=3)[0] - 0.5
# distant Apennine ridge on the left (pale blue)
far = np.interp(xs, [0, 40, 90, 140, 400], [226, 216, 228, 240, 260]) + nz * 3
farm = up(yy >= far[None, :])
scr(farm, 0.25, B, WH)
put(up((yy >= far[None, :]) & (yy < far[None, :] + 2)), B)
# Subasio
sub_pts = [(0, 262), (50, 252), (110, 238), (160, 226), (205, 212), (240, 205), (275, 202),
           (320, 192), (352, 182), (378, 186), (400, 194)]
sub = np.interp(xs, *zip(*sub_pts)) + nz * 4
subm = up(yy >= sub[None, :])
mt_tone = 0.45 + 0.25 * noise(H, W, 30, seed=11) + 0.004 * (yy - 200)
scr(subm, np.clip(mt_tone, 0.3, 0.8), G, B)
# contour hatching parallel to the ridge (woodblock lines)
def hatch(d):
    for k in range(1, 14):
        pts = []
        for x in range(0, W + 1, 4):
            yv = sub[min(x, W - 1)] + k * 6 + 2 * math.sin(x / 17 + k)
            pts.append((x, yv))
        # break the line into dashes
        for i in range(0, len(pts) - 3, 5):
            if rng.random() < 0.75:
                L_(d, pts[i:i + 4], B, 1)
draw(hatch)
# woods: tufts on the slope
def tufts(d):
    for _ in range(260):
        x = rng.uniform(0, W)
        y = sub[int(min(x, W - 1))] + rng.uniform(5, 70)
        r = rng.integers(2, 4)
        d.ellipse([int(x - r) * S, int(y - r) * S, int(x + r) * S, int(y + r) * S], fill=G)
        R_(d, x, y + r - 1, x + 2, y + r + 1, K)
draw(tufts)
# rim of sunlight along the crest
draw(lambda d: L_(d, [(x, sub[min(x, W - 1)] + 1) for x in range(0, W + 1, 2)], Y, 2))
# bare limestone streaks near the summit
def streaks(d):
    for _ in range(18):
        x = rng.uniform(280, 400)
        y = sub[int(min(x, W - 1))] + rng.uniform(4, 16)
        L_(d, [(x, y), (x + rng.uniform(-6, -2), y + rng.uniform(5, 10))], WH, 2)


# ---------------------------------------------------------------- Rocca Maggiore
def rocca(d):
    cx, base = 236, 214
    stone, shade = WH, Y
    # curtain walls stepping down the ridge
    R_(d, cx - 40, base - 8, cx + 34, base + 6, stone)
    R_(d, cx - 40, base - 8, cx + 34, base - 6, K)
    for x in range(cx - 40, cx + 34, 4):
        R_(d, x, base - 11, x + 2, base - 8, stone)
    # polygonal tower at the left
    R_(d, cx - 46, base - 22, cx - 34, base + 6, stone)
    R_(d, cx - 38, base - 22, cx - 34, base + 6, shade)
    for x in range(cx - 46, cx - 34, 4):
        R_(d, x, base - 25, x + 2, base - 22, stone)
    R_(d, cx - 42, base - 16, cx - 40, base - 11, K)
    # the keep
    R_(d, cx - 10, base - 34, cx + 10, base + 6, stone)
    R_(d, cx + 4, base - 34, cx + 10, base + 6, shade)
    for x in range(cx - 10, cx + 10, 4):
        R_(d, x, base - 37, x + 2, base - 34, stone)
    R_(d, cx - 10, base - 30, cx + 10, base - 28, R)  # string course
    for wx in (cx - 6, cx):
        R_(d, wx, base - 24, wx + 2, base - 18, K)
        R_(d, wx, base - 12, wx + 2, base - 7, K)
    # round tower at the right
    d.ellipse([(cx + 24) * S, (base - 20) * S, (cx + 38) * S, (base - 12) * S], fill=stone)
    R_(d, cx + 24, base - 16, cx + 38, base + 6, stone)
    R_(d, cx + 33, base - 16, cx + 38, base + 6, shade)
    for x in range(cx + 24, cx + 38, 4):
        R_(d, x, base - 23, x + 2, base - 18, stone)
    R_(d, cx + 28, base - 10, cx + 30, base - 5, K)
    # flag
    L_(d, [(cx, base - 37), (cx, base - 47)], K, 1)
    d.polygon(P([(cx + 1, base - 47), (cx + 9, base - 45), (cx + 1, base - 42)]), fill=R)
draw(rocca)


# ---------------------------------------------------------------- the town
# upper and lower edges of the town on the flank
def town_top(x): return np.interp(x, [150, 220, 300, 390], [282, 262, 246, 240])
def town_bot(x): return np.interp(x, [150, 260, 390], [332, 316, 300])

PINK = "pink"; CREAM = "cream"
walls_pal = [PINK, PINK, WH, CREAM, PINK, WH]

def wall_fill(x0, y0, x1, y1, kind):
    m = rect_m(x0, y0, x1, y1)
    if kind == PINK:
        scr(m, 0.25, R, WH)
    elif kind == CREAM:
        scr(m, 0.5, Y, WH)
    else:
        put(m, WH)

def house(x, yb, w, h, kind, roof="gable"):
    wall_fill(x, yb - h, x + w, yb, kind)
    side = max(2, (w // 5) // 2 * 2)
    put(rect_m(x + w - side, yb - h, x + w, yb), Y)   # sunlit/ochre side
    def f(d):
        # roof
        if roof == "gable":
            d.polygon(P([(x - 1, yb - h), (x + w + 1, yb - h), (x + w - 2, yb - h - 4), (x + 2, yb - h - 4)]), fill=R)
        else:
            d.polygon(P([(x - 1, yb - h), (x + w + 1, yb - h), (x + w // 2, yb - h - 5)]), fill=R)
        R_(d, x, yb - h, x + w, yb - h + 2, K) if rng.random() < 0.5 else None
        # windows
        cols = max(1, (w - side - 2) // 5)
        for r in range(max(1, (h - 4) // 6)):
            for c in range(cols):
                if rng.random() < 0.8:
                    wx = x + 2 + c * 5
                    wy = yb - h + 4 + r * 6
                    if wy + 3 <= yb - 1:
                        R_(d, wx, wy, wx + 2, wy + 3, K)
        if rng.random() < 0.35 and w >= 10:
            dx = x + 2
            R_(d, dx, yb - 5, dx + 3, yb, B)
    draw(f)

def tower(x, yb, w, h, kind=WH, cap="pyr"):
    wall_fill(x, yb - h, x + w, yb, kind)
    put(rect_m(x + w - 2, yb - h, x + w, yb), Y)
    def f(d):
        R_(d, x, yb - h + 3, x + w, yb - h + 5, R)
        # belfry openings
        R_(d, x + 2, yb - h + 6, x + w - 4, yb - h + 12, K)
        if w >= 9:
            R_(d, x + w // 2 - 1, yb - h + 6, x + w // 2 + 1, yb - h + 12, kind if kind != PINK else WH)
        for k in range(yb - h + 16, yb - 3, 7):
            R_(d, x + w // 2 - 1, k, x + w // 2 + 1, k + 3, K)
        if cap == "pyr":
            d.polygon(P([(x - 1, yb - h), (x + w + 1, yb - h), (x + w / 2, yb - h - 8)]), fill=R)
        else:
            for k in range(x, x + w, 3):
                R_(d, k, yb - h - 2, k + 2, yb - h, kind if kind != PINK else WH)
    draw(f)

def santa_chiara(x, yb):
    # striped pink-and-white facade, rose window, big flying buttresses, campanile
    w, h = 26, 24
    def f(d):
        for i, yv in enumerate(range(yb - h, yb, 3)):
            R_(d, x, yv, x + w, min(yv + 3, yb), WH if i % 2 == 0 else R)
        d.polygon(P([(x - 1, yb - h), (x + w + 1, yb - h), (x + w / 2, yb - h - 9)]), fill=WH)
        L_(d, [(x - 1, yb - h), (x + w / 2, yb - h - 9), (x + w + 1, yb - h)], R, 1)
        d.ellipse([(x + w / 2 - 5) * S, (yb - h + 2) * S, (x + w / 2 + 5) * S, (yb - h + 12) * S], fill=WH, outline=R, width=2 * S)
        R_(d, x + w / 2 - 1, yb - h + 5, x + w / 2 + 1, yb - h + 9, B)
        d.rectangle([int(x + w / 2 - 3) * S, (yb - 8) * S, int(x + w / 2 + 3) * S - 1, yb * S - 1], fill=K)
        # flying buttresses (left side)
        for k in range(3):
            bx = x - 6 - 6 * k
            d.polygon(P([(bx, yb), (bx + 4, yb), (bx + 4, yb - 10 + 2 * k), (x, yb - 18 + 2 * k), (x, yb - 14 + 2 * k), (bx, yb - 8)]), fill=WH)
            R_(d, bx + 2, yb - 6, bx + 4, yb, Y)
    draw(f)
    tower(x + w + 1, yb, 9, 44, PINK, "pyr")

def san_rufino(x, yb):
    w, h = 22, 22
    wall_fill(x, yb - h, x + w, yb, CREAM)
    def f(d):
        R_(d, x, yb - h - 3, x + w, yb - h, WH)
        L_(d, [(x, yb - h - 3), (x + w, yb - h - 3)], R, 1)
        for i, cx in enumerate((x + 5, x + 11, x + 17)):
            rr = 3 if i != 1 else 4
            d.ellipse([(cx - rr) * S, (yb - 15 - rr) * S, (cx + rr) * S, (yb - 15 + rr) * S], fill=R)
            R_(d, cx - 1, yb - 16, cx + 1, yb - 14, Y)
        for cx in (x + 4, x + 10, x + 16):
            R_(d, cx, yb - 6, cx + 3, yb, K)
    draw(f)
    tower(x + w + 1, yb, 9, 38, WH, "flat")

houses = []
for x0 in range(146, 396, 2):
    pass
for k in range(12):
    x = 140 + rng.integers(0, 8)
    while x < 400:
        w = int(rng.integers(5, 12)) * 2
        h = int(rng.integers(5, 9)) * 2
        top = town_top(x + w / 2)
        bot = town_bot(x + w / 2)
        yb = int(top + 8 + k * 7)
        if yb <= bot:
            houses.append(("h", x, yb, w, h, walls_pal[rng.integers(0, len(walls_pal))]))
        x += w + int(rng.integers(0, 2)) * 2
monuments = [("chiara", 340, 300), ("rufino", 270, 268), ("tower", 222, 292, 8, 42), ("tower", 186, 300, 8, 30),
             ("tower", 310, 258, 7, 30)]
# drop houses that would hide the monuments' bases badly: just painter-sort everything
items = [(it[2], it) for it in houses] + [(m[2], m) for m in monuments]
items.sort(key=lambda t: t[0])
for _, it in items:
    if it[0] == "h":
        _, x, yb, w, h, kind = it
        house(x, yb, w, h, kind, "gable" if rng.random() < 0.8 else "hip")
    elif it[0] == "chiara":
        santa_chiara(it[1], it[2])
    elif it[0] == "rufino":
        san_rufino(it[1], it[2])
    else:
        _, x, yb, w, h = it
        tower(x, yb, w, h, PINK if rng.random() < 0.5 else WH, "pyr")

# town walls along the bottom
def townwall(d):
    pts = [(x, town_bot(x) + 2) for x in range(150, 401, 2)]
    for x, y in pts:
        R_(d, x, y, x + 2, y + 6, WH)
    for x, y in pts[::2]:
        R_(d, x, y - 3, x + 2, y, WH)
    L_(d, [(x, y + 6) for x, y in pts], K, 1)
    for x, y in pts[::14]:
        R_(d, x, y - 6, x + 6, y + 6, WH)
        R_(d, x + 4, y - 6, x + 6, y + 6, Y)
        R_(d, x + 2, y - 3, x + 3, y + 1, K)
draw(townwall)


# ---------------------------------------------------------------- Basilica di San Francesco
def basilica():
    # massive substructure with tall arches
    x0, x1, yt, yb = 8, 172, 312, 350
    sub = poly_m([(x0, yt), (x1, yt - 6), (x1, yb), (x0, yb)])
    scr(sub, 0.25, R, WH)
    def f(d):
        for i, ax in enumerate(range(x0 + 6, x1 - 8, 15)):
            top = yt + 8 - i * 0.35
            d.rectangle([ax * S, int(top + 5) * S, (ax + 9) * S - 1, yb * S - 1], fill=B)
            d.ellipse([ax * S, int(top) * S, (ax + 9) * S - 1, int(top + 10) * S - 1], fill=B)
            R_(d, ax, yb - 8, ax + 9, yb, K)
            # buttress between arches
            d.polygon(P([(ax + 10, top), (ax + 14, top), (ax + 16, yb), (ax + 10, yb)]), fill=Y)
        R_(d, x0, yb - 2, x1, yb, K)
        # convent block: rows of windows
        R_(d, x0, 292, 128, 312, WH)
        for r, yv in enumerate((295, 303)):
            for wx in range(x0 + 3, 126, 5):
                R_(d, wx, yv, wx + 2, yv + 4, K)
        # loggia arcade row along the top of the convent
        R_(d, x0, 286, 128, 292, WH)
        for wx in range(x0 + 2, 126, 4):
            d.rectangle([wx * S, 288 * S, (wx + 2) * S - 1, 292 * S - 1], fill=B)
        d.polygon(P([(x0 - 1, 286), (129, 286), (127, 282), (x0 + 1, 282)]), fill=R)
        # upper church: long nave, buttresses, gable to the right with rose window
        R_(d, 60, 268, 160, 292, WH)
        for bx in range(66, 150, 12):
            d.polygon(P([(bx, 292), (bx + 5, 292), (bx + 3, 274), (bx, 274)]), fill=Y)
            R_(d, bx + 6, 276, bx + 8, 286, K)
        d.polygon(P([(58, 268), (160, 268), (160, 260), (64, 260)]), fill=R)
        L_(d, [(64, 260), (160, 260)], K, 1)
        # facade gable
        d.polygon(P([(146, 292), (176, 292), (176, 268), (161, 254), (146, 268)]), fill=WH)
        R_(d, 170, 268, 176, 292, Y)
        L_(d, [(146, 268), (161, 254), (176, 268)], R, 1)
        d.ellipse([155 * S, 266 * S, 167 * S, 278 * S], fill=WH, outline=R, width=2 * S)
        R_(d, 160, 270, 162, 274, B)
        R_(d, 157, 284, 165, 292, K)
        d.ellipse([157 * S, 280 * S, 165 * S, 288 * S], fill=K)
        # lower church & apse buildings under the gable
        R_(d, 128, 292, 176, 312, WH)
        for wx in range(132, 172, 6):
            R_(d, wx, 298, wx + 2, 304, K)
        # campanile at the left end of the nave
        cx = 40
        R_(d, cx, 232, cx + 14, 292, WH)
        R_(d, cx + 10, 232, cx + 14, 292, Y)
        for yv in (246, 266):
            R_(d, cx, yv, cx + 14, yv + 2, R)
        R_(d, cx + 2, 236, cx + 6, 244, K); R_(d, cx + 7, 236, cx + 10, 244, K)
        R_(d, cx + 3, 252, cx + 5, 262, K); R_(d, cx + 7, 252, cx + 9, 262, K)
        R_(d, cx + 5, 272, cx + 7, 280, K)
        d.polygon(P([(cx - 1, 232), (cx + 15, 232), (cx + 7, 222)]), fill=R)
        L_(d, [(cx + 7, 222), (cx + 7, 216)], K, 1)
        R_(d, cx + 5, 218, cx + 9, 220, K)
    draw(f)
basilica()

# slope below the town: olive terraces of the flank
def lower_slope_y(x): return np.interp(x, [0, 172, 260, 400], [350, 350, 322, 306])
ls = np.array([lower_slope_y(x) for x in range(W)])
slope = up((yy >= ls[None, :] + 2) & (yy < 372))
put(slope, Y)
def slope_detail(d):
    for k in range(7):
        pts = [(x, ls[min(x, W - 1)] + 5 + k * 5 + math.sin(x / 13 + k) * 1.5) for x in range(0, W + 1, 4)]
        L_(d, pts, G, 1)
        for x in range(int(rng.integers(0, 6)), W, 6):
            y = ls[min(x, W - 1)] + 2 + k * 5
            d.ellipse([x * S, int(y) * S, (x + 4) * S, int(y + 3) * S], fill=G)
            R_(d, x + 1, y + 3, x + 3, y + 4, K)
draw(slope_detail)

# ---------------------------------------------------------------- mist over the foot of the hill
def mist_band(x0, x1, y, h, seed):
    r = np.random.default_rng(seed)
    def f(d):
        d.rounded_rectangle([x0 * S, (y - h) * S, x1 * S, y * S], radius=h * S, fill=WH)
        x = x0 + h
        while x < x1 - h:
            rad = int(r.integers(2, 5))
            d.ellipse([(x - rad) * S, (y - h - rad + 1) * S, (x + rad) * S, (y - h + rad + 1) * S], fill=WH)
            x += rad + int(r.integers(2, 6))
        L_(d, [(x0 + h, y + 2), (x1 - h, y + 2)], WH, 1)
    draw(f)
for i, (x0, x1, y, h) in enumerate([(-10, 120, 360, 5), (150, 300, 366, 4), (250, 410, 356, 5),
                                    (60, 210, 374, 3), (310, 400, 376, 3), (-10, 70, 248, 3), (88, 140, 242, 2)]):
    mist_band(x0, x1, y, h, 40 + i)


# ---------------------------------------------------------------- the plain
plain_top = 372
put(up((yy >= plain_top) & (yy < 440)), Y)
VPX, VPY = 200, 330
field_styles = ["yellow", "green", "ochre", "stripe_g", "stripe_r", "yellow", "furrow", "stripe_g"]
def plain(d):
    pass
rows_y = [372, 381, 392, 405, 420, 440]
for ri in range(len(rows_y) - 1):
    y0, y1 = rows_y[ri], rows_y[ri + 1]
    x = -10 - rng.integers(0, 30)
    while x < W + 10:
        w = int(rng.integers(26, 60) * (1 + ri * 0.35))
        # trapezoid converging to the vanishing point
        def at(xv, yv):
            return VPX + (xv - VPX) * (yv - VPY) / (y0 - VPY)
        q = [(x, y0), (x + w, y0), (at(x + w, y1), y1), (at(x, y1), y1)]
        m = poly_m(q) & up((yy >= y0) & (yy < y1))
        st = field_styles[rng.integers(0, len(field_styles))]
        if st == "yellow":
            put(m, Y)
        elif st == "green":
            scr(m, 0.5, G, Y)
        elif st == "ochre":
            scr(m, 0.25, R, Y)
        elif st == "pale":
            scr(m, 0.5, WH, Y)
        else:
            put(m, Y if st != "stripe_g" else Y)
            col = G if st == "stripe_g" else (R if st == "stripe_r" else K)
            lines = M(lambda d: [d.line(P([(x + t, y0), (at(x + t, y1), y1)]), fill=255, width=S)
                                 for t in range(2, w, 4)]) if st == "furrow" else \
                M(lambda d: [d.line(P([(x, yv), (x + 2 * w, yv)]), fill=255, width=S)
                             for yv in range(y0 + 1, y1, 3)])
            put(m & lines, col if st != "furrow" else R)
        # hedgerow on the field's left edge
        draw(lambda d: L_(d, [q[0], q[3]], G, 1))
        x += w
    draw(lambda d: L_(d, [(0, y1 - 1), (W, y1 - 1)], G, 1))

# farmhouses, poplars and cypress rows on the plain
def plain_things(d):
    for _ in range(14):
        x = rng.uniform(10, 390); y = rng.choice(rows_y[1:5]) - 1
        s = 1 + (y - 372) / 40
        w, h = int(6 * s), int(4 * s)
        R_(d, x, y - h, x + w, y, WH)
        R_(d, x + w - 2, y - h, x + w, y, Y)
        d.polygon(P([(x - 1, y - h), (x + w + 1, y - h), (x + w / 2, y - h - 3)]), fill=R)
        R_(d, x + 1, y - h + 1, x + 3, y - h + 3, K)
    for _ in range(40):
        x = rng.uniform(4, 396); y = rng.choice(rows_y[1:5])
        s = 1 + (y - 372) / 30
        hgt = int(6 * s + rng.integers(0, 3))
        d.polygon(P([(x, y), (x + 2, y), (x + 2, y - hgt + 2), (x + 1, y - hgt), (x, y - hgt + 2)]), fill=G)
        R_(d, x + 1, y - hgt + 3, x + 2, y, K) if rng.random() < 0.5 else None
draw(plain_things)

# Santa Maria degli Angeli: the great dome on the plain
def angeli(d):
    x, y = 304, 392
    R_(d, x - 24, y - 10, x + 24, y, WH)
    R_(d, x + 18, y - 10, x + 24, y, Y)
    for wx in range(x - 21, x + 16, 5):
        R_(d, wx, y - 7, wx + 2, y - 3, K)
    R_(d, x - 10, y - 16, x + 10, y - 10, WH)
    d.pieslice([(x - 10) * S, (y - 27) * S, (x + 10) * S, (y - 5) * S], 180, 360, fill=B)
    for k in (-6, -2, 2, 6):
        L_(d, [(x + k * 0.6, y - 27 + 1), (x + k, y - 16)], WH, 1)
    R_(d, x - 2, y - 32, x + 2, y - 26, WH)
    d.polygon(P([(x - 2, y - 32), (x + 2, y - 32), (x, y - 36)]), fill=B)
    # campanile
    R_(d, x + 26, y - 26, x + 32, y, WH)
    R_(d, x + 27, y - 22, x + 31, y - 18, K)
    d.polygon(P([(x + 25, y - 26), (x + 33, y - 26), (x + 29, y - 31)]), fill=R)
draw(angeli)


# ---------------------------------------------------------------- foreground ground & terraces
fg_top = 440
grd = up(yy >= fg_top)
put(grd, Y)
def tilled(d):
    for k in range(40):
        y0 = fg_top + 4 + k * 3.2
        amp = 2 + k * 0.1
        x = rng.uniform(-10, 10)
        while x < W:
            ln = rng.uniform(6, 16) * (1 + k / 30)
            if rng.random() < 0.4:
                L_(d, [(x + t, y0 + amp * math.sin((x + t) / 60 + k * 0.05)) for t in np.linspace(0, ln, 4)], R, 1)
            x += ln + rng.uniform(4, 12)
draw(tilled)
# grass texture: short green strokes in bands
def grass(d):
    for _ in range(500):
        x = rng.uniform(0, W); y = rng.uniform(fg_top + 2, 566)
        ln = 2 + (y - fg_top) / 40
        L_(d, [(x, y), (x + rng.uniform(-1.5, 1.5), y - ln)], G, 1)
draw(grass)

def terrace_y(x, base, amp, ph):
    return base + amp * math.sin(x / 70 + ph)

def terrace(base, amp, ph, hgt):
    def f(d):
        pts_top = [(x, terrace_y(x, base, amp, ph)) for x in range(-4, W + 6, 2)]
        poly = pts_top + [(x, y + hgt) for x, y in pts_top[::-1]]
        d.polygon(P(poly), fill=WH)
        # stones
        for i, (x, y) in enumerate(pts_top[::3]):
            off = 0 if i % 2 else 2
            R_(d, x + off, y + 1, x + off + 4, y + hgt - 1, WH if rng.random() < 0.6 else Y)
            R_(d, x + off + 4, y, x + off + 5, y + hgt, K)
        L_(d, [(x, y + hgt // 2) for x, y in pts_top], K, 1)
        L_(d, [(x, y + hgt) for x, y in pts_top], K, 1)
        L_(d, pts_top, G, 1)
    draw(f)
    # pink screening on the stones
    tm = M(lambda d: d.polygon(P([(x, terrace_y(x, base, amp, ph)) for x in range(-4, W + 6, 2)] +
                                  [(x, terrace_y(x, base, amp, ph) + hgt) for x in range(W + 4, -6, -2)]), fill=255))
    stones = (np.asarray(Image.fromarray(A).convert("RGB")) == np.array(WH)).all(-1)
    put(tm & stones & screen(full(0.25)), R)

# ---------------------------------------------------------------- olive trees
def olive(cx, by, s, seed):
    r = np.random.default_rng(seed)
    # shadow cast toward the viewer (sun behind)
    sh = ell_m(cx + 2, by + 4 * s, 16 * s, 3.2 * s)
    scr(sh, 0.5, G, None)
    # twisted trunk: two or three intertwined strands
    def trunk(d):
        for k in range(3):
            pts = []
            for i in range(9):
                f = i / 8
                x = cx + math.sin(f * 4 + k * 2.1 + seed) * 2.2 * s * (1 - f * 0.3) + (k - 1) * 1.6 * s * (1 - f)
                pts.append((x, by - f * 16 * s))
            L_(d, pts, K, max(1, int(round(1.4 * s))))
        # forks into the crown
        for a in (-1, 1):
            L_(d, [(cx, by - 13 * s), (cx + a * 7 * s, by - 20 * s)], K, max(1, int(round(s))))
        R_(d, cx - 5 * s, by - 1, cx + 5 * s, by + 1, K)
    draw(trunk)
    # crown: clusters of blobs, dark green underside, silvery upper
    blobs = []
    n = int(9 + 4 * s)
    for i in range(n):
        a = r.uniform(0, 2 * math.pi)
        rr = r.uniform(0, 1) ** 0.6
        bx = cx + math.cos(a) * 15 * s * rr
        bys = by - 25 * s + math.sin(a) * 7 * s * rr
        rx = r.uniform(4, 7) * s; ry = rx * r.uniform(0.55, 0.75)
        blobs.append((bx, bys, rx, ry))
    blobs.sort(key=lambda b: b[1])
    for bx, bys, rx, ry in blobs:
        m = ell_m(bx, bys, rx, ry)
        put(m, G)
        hi = ell_m(bx - rx * 0.15, bys - ry * 0.3, rx * 0.8, ry * 0.6)
        scr(hi, 0.375, WH, G)
        # leaf glints and gaps
        def leaves(d):
            for _ in range(int(rx * ry / 6)):
                lx = bx + r.uniform(-rx, rx) * 0.8; ly = bys + r.uniform(-ry, ry) * 0.7
                c = WH if ly < bys else K
                if c == K and r.random() < 0.5:
                    continue
                L_(d, [(lx, ly), (lx + 2, ly - 1)], c, 1)
        draw(leaves)
    # sky holes in the crown (a few dark shadow notches)
    def notches(d):
        for _ in range(int(3 * s)):
            bx, bys, rx, ry = blobs[r.integers(0, len(blobs))]
            R_(d, bx - 1, bys + ry - 2, bx + 1, bys + ry, K)
    draw(notches)

def cypress(x, by, h, w):
    pts = []
    for i in range(21):
        f = i / 20
        prof = math.sin(math.pi * min(1, f * 1.15)) ** 0.7 * (1 - f) ** 0.25
        pts.append((x - w / 2 * prof, by - h * f))
    pts += [(2 * x - px, py) for px, py in pts[::-1]]
    m = poly_m(pts)
    put(m, G)
    scr(m & up(xx > x), 0.5, K, G)
    def tex(d):
        for yv in range(int(by - h + 6), int(by - 2), 4):
            f = (by - yv) / h
            hw = w / 2 * math.sin(math.pi * min(1, f * 1.15)) ** 0.7 * (1 - f) ** 0.25
            for xo in np.arange(-hw + 2, hw - 1, 4):
                L_(d, [(x + xo - 1, yv), (x + xo + 0.5, yv - 2), (x + xo + 2, yv)], K if xo < 0 else G, 1)
        # yellow rim on the left (backlight)
        L_(d, pts[:20], Y, 1)
        R_(d, x - 1, by - 2, x + 1, by + 2, K)
    draw(tex)

# path from the bottom up toward the town
def path_c(y): return 214 + 38 * math.sin((566 - y) / 46) - (566 - y) * 0.15
def path_w(y): return 3 + (y - 440) * 0.30
def path():
    ys = list(range(440, 568, 2))
    left = [(path_c(y) - path_w(y), y) for y in ys]
    right = [(path_c(y) + path_w(y), y) for y in ys]
    m = poly_m(left + right[::-1])
    put(m, WH)
    def f(d):
        L_(d, left, R, 1); L_(d, right, R, 1)
        for _ in range(26):
            y = rng.uniform(444, 566)
            x = path_c(y) + rng.uniform(-0.8, 0.8) * path_w(y)
            sz = 1 + (y - 440) / 70
            c = [R, Y, Y][rng.integers(0, 3)]
            R_(d, x, y, x + 2 * sz, y + sz + 1, c)
        # ruts
        for o in (-0.45, 0.45):
            L_(d, [(path_c(y) + o * path_w(y), y) for y in range(470, 566, 2)], Y, 1)
    draw(f)

# far row of olives on the plain edge
terrace(440, 3, 0.2, 5)
for i, x in enumerate(range(8, 400, 30)):
    if abs(x - path_c(450)) < 10:
        continue
    olive(x + rng.integers(-3, 4), 452, 0.72, 100 + i)
cypress(38, 468, 74, 13)
cypress(54, 466, 56, 10)
cypress(372, 464, 66, 12)
terrace(474, 4, 1.4, 7)
path()

# the friar walking up the path toward Assisi
def friar(x, y, k=1.4):
    sh = poly_m([(x - 3 * k, y), (x + 3 * k, y), (x + 9 * k, y + 14 * k), (x + 2 * k, y + 14 * k)])
    scr(sh, 0.5, B, None)
    def Q(pts): return [(x + px * k, y + py * k) for px, py in pts]
    def f(d):
        d.polygon(P(Q([(-4.5, 0), (4.5, 0), (3, -10), (3, -14), (0, -17), (-3, -14), (-3, -10)])), fill=K)
        d.ellipse([int(x - 3 * k) * S, int(y - 21 * k) * S, int(x + 3 * k) * S, int(y - 14 * k) * S], fill=K)
        L_(d, Q([(-3, -9), (3, -9)]), WH, 1)
        L_(d, Q([(1, -9), (2, -3)]), WH, 1)
        L_(d, Q([(6, 1), (6.5, -21)]), R, 1)
        R_(d, x - 3 * k, y, x - 1, y + 2, R)
        R_(d, x + 1, y, x + 3 * k, y + 2, R)
    draw(f)

def wayside(x, y):
    def f(d):
        # stone plinth, wooden cross with a little gable, posy of flowers
        R_(d, x - 6, y - 5, x + 6, y, WH); R_(d, x + 2, y - 5, x + 6, y, Y)
        L_(d, [(x - 6, y), (x + 6, y)], K, 1)
        R_(d, x - 1, y - 34, x + 2, y - 5, K)
        R_(d, x - 8, y - 27, x + 9, y - 24, K)
        d.polygon(P([(x - 4, y - 34), (x + 5, y - 34), (x + 0.5, y - 39)]), fill=R)
        R_(d, x - 1, y - 27, x + 2, y - 24, Y)
        for dx, c in ((-5, R), (-2, WH), (2, R), (5, B)):
            R_(d, x + dx, y - 8, x + dx + 2, y - 6, c)
    draw(f)
friar(int(path_c(494)), 494)
wayside(int(path_c(540) - path_w(540) - 14), 540)

# middle row
for i, x in enumerate([20, 80, 140, 284, 338, 394]):
    olive(x + rng.integers(-3, 4), 502, 1.25, 200 + i)
terrace(514, 5, 2.6, 8)

# front framing olives (big, partly cut)
olive(40, 566, 1.9, 301)
olive(360, 564, 2.0, 302)

# wildflowers along the front
def flowers(d):
    for _ in range(90):
        x = rng.uniform(10, 390); y = rng.uniform(530, 566)
        if abs(x - path_c(y)) < path_w(y) + 2:
            continue
        c = [R, WH, B, R, WH][rng.integers(0, 5)]
        L_(d, [(x + 1, y + 2), (x + 1, y + 6)], G, 1)
        R_(d, x, y, x + 2, y + 2, c)
        if c == R and rng.random() < 0.5:
            R_(d, x + 2, y - 1, x + 4, y + 1, c)
draw(flowers)


# ---------------------------------------------------------------- frame and title band
def frame(d):
    # title band
    R_(d, 0, 566, W, H, K)
    fnt = font("dejavu-serif-b", 17 * S)
    txt = "FRATE  SOLE"
    bb = d.textbbox((0, 0), txt, font=fnt)
    tw = bb[2] - bb[0]
    tx = (W * S - tw) // 2
    d.text((tx, 571 * S - bb[1] + 2 * S), txt, font=fnt, fill=Y)
    # small suns either side
    for cx in ((tx // S) - 22, (tx + tw) // S + 22):
        cy = 582
        for i in range(12):
            a = 2 * math.pi * i / 12
            ln = 8 if i % 2 == 0 else 6
            L_(d, [(cx + 4 * math.cos(a), cy + 4 * math.sin(a)), (cx + ln * math.cos(a), cy + ln * math.sin(a))],
               Y if i % 2 == 0 else R, 1)
        d.ellipse([(cx - 4) * S, (cy - 4) * S, (cx + 4) * S, (cy + 4) * S], fill=Y)
        R_(d, cx - 1, cy - 1, cx + 1, cy + 1, R)
    # dot rule at the edges of the band
    for x in range(14, W - 12, 6):
        R_(d, x, 590, x + 2, 592, R)
    R_(d, 0, 566, W, 568, Y)
    # outer border: black / yellow with red studs / black
    R_(d, 0, 0, W, 2, K); R_(d, 0, H - 2, W, H, K)
    R_(d, 0, 0, 2, H, K); R_(d, W - 2, 0, W, H, K)
    for (x0, y0, x1, y1) in [(2, 2, W - 2, 6), (2, 2, 6, 566), (W - 6, 2, W - 2, 566)]:
        R_(d, x0, y0, x1, y1, Y)
    for x in range(6, W - 6, 8):
        R_(d, x, 3, x + 2, 5, R)
    for y in range(6, 566, 8):
        R_(d, 3, y, 5, y + 2, R); R_(d, W - 5, y, W - 3, y + 2, R)
    R_(d, 6, 6, W - 6, 8, K); R_(d, 6, 6, 8, 566, K); R_(d, W - 8, 6, W - 6, 566, K)
draw(frame)

finish(Image.fromarray(A))
