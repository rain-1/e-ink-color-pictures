"""Storm - the fourth Sea Interlude. An engraved sea: forty ridgelines stacked back to
front, each hatched along its own slope, foam torn off the crests; lighthouse, rain,
one bolt of lightning, and LT 13 (gone from the beach) running for home."""
import math, random
from common import *

rng = random.Random(404)
d = D(B)
HOR = 236

# ---- sky: thunderheads built from hatched lobes
d.rect(0, 0, W, HOR, fill=B)
for y in range(2, HOR, 3):                                   # ruled sky, heavier at the top
    t = 1 - y / HOR
    d.line([(0, y), (W, y)], K, 0.5 + 1.9 * t ** 1.3)
lobes = []
for (cx, cy, n, spread, r0) in [(70, 40, 16, 70, 30), (250, 22, 18, 95, 34), (360, 70, 12, 50, 26), (150, 96, 14, 80, 24), (20, 120, 8, 40, 22), (310, 140, 10, 70, 18)]:
    for _ in range(n):
        lobes.append((cx + rng.gauss(0, spread * 0.5), cy + rng.gauss(0, 14), r0 * rng.uniform(0.55, 1.1)))
lobes.sort(key=lambda l: l[1])
for (cx, cy, r) in lobes:
    d.ell(cx, cy, r, r * 0.8, fill=K)
    d.arc(cx, cy, r, r * 0.8, 200, 340, WH, 0.8)             # lit rim
    for k in range(1, 5):                                    # inner contour hatching
        d.arc(cx, cy + k * 1.2, r * (1 - k * 0.16), r * 0.8 * (1 - k * 0.16), 215 + k * 6, 325 - k * 6, B, 0.55)
    d.rect(cx - r, cy, cx + r, cy + r * 0.8 + 1, fill=K)
# lightning
def bolt(x, y, y1, w, depth=0):
    pts = [(x, y)]
    while y < y1:
        y += rng.uniform(7, 16); x += rng.uniform(-13, 11)
        pts.append((x, y))
        if depth < 2 and rng.random() < 0.3:
            bolt(x, y, y + rng.uniform(25, 70), w * 0.55, depth + 1)
    d.line(pts, K, w + 2.2); d.line(pts, Y, w + 0.6)
    if depth == 0: d.line(pts, WH, w * 0.4)
bolt(132, 70, HOR - 2, 2.4)

# ---- lighthouse beam (behind the tower), then rocks + tower
LXH, LYH = 330, 150
for sgn in (-1, 1):
    for k in range(13):
        a = math.radians((200 if sgn < 0 else -20) + (k - 6) * 1.9)
        d.line([(LXH, LYH), (LXH + 300 * math.cos(a), LYH + 300 * math.sin(a))], Y, 0.5 + (0.9 if k in (5, 6, 7) else 0))

# ---- the sea
def crest(theta):                                            # sharp crest, round trough, in [-1, 1]
    return 1 - 2 * abs(math.sin(theta / 2)) ** 1.35
ROWS = 40
rows = []
for j in range(ROWS):
    t = j / (ROWS - 1)
    rows.append(dict(base=HOR + 6 + 370 * t ** 1.45, amp=3 + 44 * t ** 1.5, k=0.11 - 0.082 * t ** 0.7,
                     ph=rng.uniform(0, 6.28), k2=rng.uniform(0.02, 0.05), ph2=rng.uniform(0, 6.28), t=t))
def ridge(r, x):
    return r["base"] - r["amp"] * (0.72 * crest(r["k"] * x + r["ph"] + 0.6 * math.sin(r["k2"] * x + r["ph2"])) + 0.28 * math.sin(r["k"] * 2.3 * x + r["ph2"]))
boat_row = 22
def draw_boat(r):
    bx = 118
    by = ridge(r, bx) + 12
    slope = (ridge(r, bx + 12) - ridge(r, bx - 12)) / 24
    ang = math.atan(slope) - 0.18
    ca, sa = math.cos(ang), math.sin(ang)
    T = lambda pts: [(bx + 1.35 * (x * ca - y * sa), by + 1.35 * (x * sa + y * ca)) for x, y in pts]
    hull = [(-30, -9), (-24, 1), (18, 2), (27, -10), (22, -8), (-22, -7)]
    d.line(T([(-4, -8), (-4, -50)]), K, 1.8)
    d.poly(T([(-2, -48), (-2, -14), (20, -14)]), fill=R, outline=K, w=1)
    for k in range(1, 4):
        d.line(T([(-2, -14 - k * 8.5), (20 - k * 5.5, -14)]), K, 0.45)
    d.poly(T([(-6, -40), (-6, -14), (-20, -12)]), fill=WH, outline=K, w=0.9)
    d.line(T([(-4, -50), (27, -10)]), K, 0.45); d.line(T([(-4, -50), (-30, -9)]), K, 0.45)
    d.poly(T(hull), fill=K, outline=WH, w=0.9)
    d.line(T([(-27, -5), (23, -5)]), WH, 1.3)
    d.line(T([(-24, -1.5), (20, -1)]), R, 1.2)
    d.poly(T([(8, -8), (9, -16), (17, -16), (18, -8)]), fill=WH, outline=K, w=0.7)
    d.rect(*T([(11, -14)])[0], *T([(15, -10)])[0], fill=Y)
    d.text(*T([(-12, -2.6)])[0], "LT 13", WH, size=6.4, font="sans")
    d.poly(T([(-4, -50), (-13, -47.5), (-4, -45)]), fill=Y, outline=K, w=0.4)
    fx, fy = T([(-14, -8)])[0]                               # the man at the tiller
    d.poly([(fx - 2.5, fy), (fx - 2, fy - 8), (fx + 2, fy - 8), (fx + 2.5, fy)], fill=Y, outline=K, w=0.5); d.ell(fx, fy - 10, 2, fill=K)

def rocks_and_tower():
    rk = [(262, 330), (276, 300), (292, 292), (300, 274), (318, 268), (346, 270), (362, 282), (380, 286), (404, 300), (404, 340)]
    d.poly(rk, fill=K, outline=WH, w=0.9)
    for _ in range(46):
        x, y = rng.uniform(270, 398), rng.uniform(280, 326)
        d.line([(x, y), (x + rng.uniform(4, 12), y + rng.uniform(3, 9))], WH if rng.random() < 0.5 else B, 0.5)
    tw = [(316, 270), (322, 172), (340, 172), (346, 270)]
    d.poly(tw, fill=WH, outline=K, w=1.2)
    for k in range(3):                                       # red bands
        y0, y1 = 186 + k * 30, 200 + k * 30
        f = lambda y: (316 + 6 * (270 - y) / 98, 346 - 6 * (270 - y) / 98)
        d.poly([(f(y0)[0], y0), (f(y0)[1], y0), (f(y1)[1], y1), (f(y1)[0], y1)], fill=R, outline=K, w=0.7)
    for y in range(176, 268, 5):                             # courses + shadow side
        f0, f1 = 316 + 6 * (270 - y) / 98, 346 - 6 * (270 - y) / 98
        d.line([(f1 - 6.5, y), (f1 - 0.8, y)], K, 0.9)
    for (wy) in (208, 238):
        d.rect(329, wy, 333, wy + 7, fill=K)
    d.poly([(326, 270), (326, 258), (331, 253), (336, 258), (336, 270)], fill=K)
    d.rect(318, 166, 344, 172, fill=K); d.line([(316, 160), (346, 160)], K, 0.8)
    for x in range(316, 347, 5): d.line([(x, 160), (x, 166)], K, 0.6)
    d.rect(322, 142, 340, 166, fill=Y, outline=K, w=1.1)     # lantern
    for x in (328, 334): d.line([(x, 142), (x, 166)], K, 0.6)
    d.ell(331, 152, 3.2, fill=WH, outline=K, w=0.6)
    d.poly([(319, 143), (331, 130), (343, 143)], fill=K); d.line([(331, 130), (331, 122)], K, 0.9); d.ell(331, 121, 1.5, fill=K)
    # keeper's cottage
    d.rect(352, 258, 378, 284, fill=WH, outline=K, w=1); d.poly([(349, 259), (365, 246), (381, 259)], fill=R, outline=K, w=1)
    d.rect(357, 266, 363, 273, fill=Y, outline=K, w=0.6); d.rect(368, 270, 374, 284, fill=K)

for j, r in enumerate(rows):
    if j == 9: rocks_and_tower()
    t = r["t"]
    pts = [(x, ridge(r, x)) for x in range(-6, W + 8, 2)]
    fill = B if j % 3 != 2 else K
    d.poly(pts + [(W + 8, H + 4), (-6, H + 4)], fill=fill)
    # hatch along the slope beneath the ridge
    nh = 3 + int(9 * t)
    for h in range(1, nh):
        off = h * (1.6 + 3.4 * t)
        seg = []
        for (x, y) in pts:
            c = crest(r["k"] * x + r["ph"] + 0.6 * math.sin(r["k2"] * x + r["ph2"]))
            keep = c > -0.82 + h * 0.14 - 0.25 * math.sin(x * 0.09 + h)       # hatch thins toward the troughs
            if keep: seg.append((x, y + off + 0.25 * off * (1 - c)))
            else:
                if len(seg) > 1: d.line(seg, (K if fill == B else B) if h % 3 else WH, 0.45 + 0.75 * t)
                seg = []
        if len(seg) > 1: d.line(seg, (K if fill == B else B) if h % 3 else WH, 0.45 + 0.75 * t)
    d.line(pts, WH, 0.6 + 1.3 * t)
    # foam on the crests, and spray torn off downwind
    for i in range(1, len(pts) - 1):
        x, y = pts[i]
        c = crest(r["k"] * x + r["ph"] + 0.6 * math.sin(r["k2"] * x + r["ph2"]))
        if c > 0.45 and t > 0.08:
            s = (c - 0.45) / 0.55
            rr = (1.0 + 5.5 * t) * s * rng.uniform(0.6, 1.2)
            d.ell(x + rng.uniform(-1, 1), y + rr * 0.3, rr * 1.3, rr, fill=WH)
            if rng.random() < 0.6 * s:
                d.arc(x, y + rr * 1.1, rr * 1.2, rr * 0.8, 20, 160, B, 0.5)
            for _ in range(int(3 * s * (1 + 4 * t))):
                q = rng.random()
                d.ell(x + q * (10 + 46 * t) + rng.uniform(-3, 3), y - q * (4 + 24 * t) * rng.uniform(0.3, 1) - 1, 0.35 + (1 - q) * (0.5 + 1.4 * t), fill=WH)
            if s > 0.6 and t > 0.3 and i % 3 == 0:               # foam streaks running down the face
                d.line(bez((x, y + rr), (x - 6 - 18 * t, y + 8 + 20 * t), (x - 10 - 34 * t, y + 12 + 44 * t), 8), WH, 0.5 + 0.6 * t)
    if j == boat_row + 2: draw_boat(rows[boat_row])
    if j == 12:                                                # surf breaking white round the rocks
        for _ in range(120):
            a = rng.uniform(math.pi, 2 * math.pi); q = rng.random() ** 0.5
            d.ell(288 + 44 * q * math.cos(a) * 1.3 + 12, 322 + 46 * q * math.sin(a), 0.5 + 2.2 * (1 - q), fill=WH)

# ---- rain, driven from the right
for _ in range(520):
    x, y = rng.uniform(-40, W + 120), rng.uniform(-20, H)
    ln = rng.uniform(8, 26)
    d.line([(x, y), (x - ln * 0.42, y + ln)], WH if rng.random() < 0.72 else K, 0.42)
# three storm-petrels
for (gx, gy, s) in [(52, 214, 7), (224, 196, 5), (196, 226, 4)]:
    gull(d, gx, gy, s, WH, 1.0)
d.save()
