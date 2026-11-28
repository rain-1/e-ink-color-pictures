"""Evening — Jacob's Ladder.  A depth-sorted spiral stair of ~120 steps climbing from a
sleeper on a hill to an orb, with small figures going up and coming down."""
import math, sys, os
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(__file__))
from common import *

rng = np.random.default_rng(1805)
a = Art(B, crisp=True)
OX, OY = 200, 74

# ---------- twilight sky as a ramp through ink pairs, plus the orb's glow
yy, xx = np.mgrid[0:H * S, 0:W * S].astype(np.float32)
X, Yv = xx / S, yy / S
stops = [(0, mix(B, K, .62)), (150, mix(B, K, .25)), (250, B), (400, mix(B, WH, .5)), (452, mix(WH, Y, .35)),
         (486, mix(R, Y, .7)), (520, mix(R, Y, .35)), (600, R)]
n = fbm(3, 120 * S, 3, W * S, H * S)
yw = Yv + (n - .5) * 46 + 10 * np.sin(X / 37 + Yv / 90)
sky = np.zeros((H * S, W * S, 3), np.float32)
for (y0, c0), (y1, c1) in zip(stops[:-1], stops[1:]):
    m = (yw >= y0) & (yw < y1) if y0 > 0 else (yw < y1)
    t = np.clip((yw - y0) / (y1 - y0), 0, 1)[..., None]
    sky[m] = (np.array(c0, np.float32) * (1 - t) + np.array(c1, np.float32) * t)[m]
sky[yw >= 600] = R
d = np.hypot(X - OX, Yv - OY)
g = np.clip(1 - (d - 30) / 120, 0, 1)[..., None] ** 1.6
sky = sky * (1 - g * .85) + np.array(mix(WH, B, .25), np.float32) * g * .85
g2 = np.clip(1 - (d - 24) / 34, 0, 1)[..., None]
sky = sky * (1 - g2) + np.array(mix(WH, Y, .5), np.float32) * g2
sky = np.clip(sky, 1, 254)        # keep tones off the pure-ink values
a.col = Image.fromarray(sky.astype(np.uint8)); c = a.c = ImageDraw.Draw(a.col)

# engraved halo rings + rays round the orb
for r in (44, 58, 76, 98):
    disc(c, OX, OY, r, None, WH, .7)
for i in range(48):
    th = i * math.pi / 24; r0, r1 = (34, 112) if i % 2 == 0 else (40, 70)
    line(c, [(OX + r0 * math.cos(th), OY + r0 * math.sin(th)), (OX + r1 * math.cos(th), OY + r1 * math.sin(th))], WH, .7)

# stars: crisp pixels, a few four-pointed
for i in range(900):
    x, y = int(rng.integers(8, W - 8)), int(rng.integers(8, 400))
    if math.hypot(x - OX, y - OY) < 112 or rng.random() < (y / 430) ** 1.5: continue
    col = WH if rng.random() < .8 else Y
    c.rectangle([x * S, y * S, x * S + S - 1, y * S + S - 1], fill=col)
    if rng.random() < .16:
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            c.rectangle([(x + dx) * S, (y + dy) * S, (x + dx) * S + S - 1, (y + dy) * S + S - 1], fill=col)
        if rng.random() < .5:
            for dx, dy in ((2, 0), (-2, 0), (0, 2), (0, -2)):
                c.rectangle([(x + dx) * S, (y + dy) * S, (x + dx) * S + S - 1, (y + dy) * S + S - 1], fill=col)
# long evening clouds
for i in range(9):
    x, y = rng.uniform(-20, 380), rng.uniform(405, 478); L_ = rng.uniform(50, 130)
    col = mix(R, WH, .45) if y > 440 else mix(B, WH, .78)
    for k in range(3):
        c.rounded_rectangle([(x + k * 9) * S, (y + k * 3.4) * S, (x + L_ - k * 14) * S, (y + k * 3.4 + 2.6) * S], radius=4, fill=col)

# ---------- the stair
N, TURNS = 124, 3.3
def geom(t):
    ax = 200 + 30 * math.sin(2.1 * math.pi * t) * (1 - t)
    ay = 520 - 430 * t ** .86
    ro = 124 * (1 - t) ** 1.12 + 7
    k = .25 + .2 * t
    return ax, ay, ro, k
def pt(t, phi, f):
    ax, ay, ro, k = geom(t)
    return (ax + ro * f * math.cos(phi), ay + ro * f * k * math.sin(phi))
PH0 = 1.1
def phi(i): return PH0 + 2 * math.pi * TURNS * i / N
FIN = .40
people = {}
for i in range(3, N - 10):
    if rng.random() < .30 and math.sin(phi(i + .5)) > -.45 and i - 1 not in people and i - 2 not in people:
        people[i] = (rng.random() < .5, int(rng.integers(4)))
people[1] = (True, 0)

def figure(x, y, h, winged, kind):
    robe = (WH, WH, R, WH)[kind] if h > 9 else WH
    w_ = h * .26
    if winged and h > 8:
        for sg in (1, -1):
            p = leaf(x + sg * w_ * .3, y - h * .72, -math.pi / 2 + sg * .75, h * .62, h * .16, 6)
            poly(c, p, Y if robe == WH else WH, K, .8)
    body = [(x - w_ * .45, y - h * .78), (x + w_ * .45, y - h * .78), (x + w_, y), (x - w_, y)]
    poly(c, body, robe, K, .8)
    if h > 12:
        line(c, [(x, y - h * .7), (x - w_ * .2, y - 1)], K, .7)
        sg = 1 if kind % 2 else -1
        line(c, [(x + sg * w_ * .4, y - h * .7), (x + sg * w_ * 1.3, y - h * (.95 if kind > 1 else .45))], K, 1.0)
    disc(c, x, y - h * .88, max(1.3, h * .13), WH, K, .8)

order = sorted(range(N), key=lambda i: (math.sin(phi(i + .5)) * geom(i / N)[2], i))
for i in order:
    t0, t1 = i / N, (i + 1) / N
    p0, p1 = phi(i), phi(i + 1)
    front = math.sin((p0 + p1) / 2) > 0
    ax, ay, ro, k = geom(t0)
    rise = geom(t0)[1] - geom(t1)[1]
    lw = .9 if ro > 34 else (.67 if ro > 16 else 0)
    ol = K if lw else None
    tread = [pt(t0, p0, FIN), pt(t0, p0, 1), pt(t0, p1, 1), pt(t0, p1, FIN)]
    hr = ro * .2 + 3
    def rail(f):
        if ro < 22: return
        q0, q1 = pt(t0, p0, f), pt(t1, p1, f)
        line(c, [q0, (q0[0], q0[1] - hr)], K, .8)
        line(c, [(q0[0], q0[1] - hr), (q1[0], q1[1] - hr)], K, 1.0)
    if not front: rail(1)
    # outer skirt (front) / inner wall (back)
    drop = rise * 2.6 + 2
    if front:
        s_ = [tread[1], tread[2], (tread[2][0], tread[2][1] + drop), (tread[1][0], tread[1][1] + drop)]
        poly(c, s_, R, ol, lw)
    else:
        s_ = [tread[0], tread[3], (tread[3][0], tread[3][1] + drop), (tread[0][0], tread[0][1] + drop)]
        poly(c, s_, mix(R, K, .45), ol, lw)
    # riser up to the next tread
    rz = [pt(t0, p1, FIN), pt(t0, p1, 1), pt(t1, p1, 1), pt(t1, p1, FIN)]
    poly(c, rz, mix(R, Y, .45), ol, lw)
    poly(c, tread, Y if i % 2 else mix(Y, WH, .45), ol, lw)
    if i in people:
        fx, fy = pt(t0, (p0 + p1) / 2, .72)
        figure(fx, fy, ro * .26 + 5, *people[i])
    if front: rail(1)

# the orb itself, over the top of the stair
disc(c, OX, OY, 27, Y, K, 1.0); disc(c, OX, OY, 19, WH, None)
disc(c, OX, OY, 19, None, R, .8)
for i in range(12):
    th = i * math.pi / 6
    line(c, [(OX + 21 * math.cos(th), OY + 21 * math.sin(th)), (OX + 26 * math.cos(th), OY + 26 * math.sin(th))], R, .8)

# ---------- the hill, the sleeper, sheep, a thorn tree
hn = fbm(6, 80, 3, W, 4)[0]
hy = [512 + 26 * ((x - 200) / 200) ** 2 + 10 * (hn[x] - .5) for x in range(W)]
poly(c, [(x, hy[x]) for x in range(W)] + [(W, H), (0, H)], mix(G, K, .62))
line(c, [(x, hy[x]) for x in range(W)], K, 1.6)
for i in range(420):                       # grass hatch
    x = rng.uniform(0, W - 1); y = rng.uniform(hy[int(x)] + 3, H - 8); L_ = rng.uniform(4, 9)
    line(c, [(x, y), (x + rng.uniform(-2, 2), y - L_)], K if rng.random() < .6 else G, .8)
# tree at right
def branch(x, y, ang, L_, w_, depth):
    x2, y2 = x + L_ * math.cos(ang), y + L_ * math.sin(ang)
    line(c, [(x, y), (x2, y2)], K, w_)
    if depth:
        for da in (rng.uniform(-.75, -.25), rng.uniform(.2, .7), rng.uniform(-.15, .15)):
            if rng.random() < .85:
                branch(x2, y2, ang + da, L_ * rng.uniform(.62, .8), max(.8, w_ * .62), depth - 1)
branch(352, hy[352] + 6, -math.pi / 2 - .12, 34, 5, 5)
branch(40, hy[40] + 6, -math.pi / 2 + .2, 20, 3, 4)
# Jacob, asleep with his head on a stone
jx, jy = 92, 556
ell(c, jx - 46, jy - 2, 13, 7, mix(WH, K, .45), K, 1.0)                        # stone
body = bez((jx - 36, jy - 6), (jx - 10, jy - 26), (jx + 40, jy - 16), (jx + 70, jy + 2), 20) + bez((jx + 70, jy + 2), (jx + 40, jy + 10), (jx - 10, jy + 8), (jx - 36, jy + 4), 20)
poly(c, body, R, K, 1.2)
for k in range(5):
    line(c, bez((jx - 20 + k * 16, jy - 14 + k), (jx - 14 + k * 16, jy - 6), (jx - 16 + k * 16, jy), (jx - 10 + k * 16, jy + 5), 8), K, .8)
disc(c, jx - 42, jy - 10, 7.5, WH, K, 1.1)
line(c, bez((jx - 49, jy - 13), (jx - 46, jy - 20), (jx - 38, jy - 20), (jx - 35, jy - 13), 8), K, 2.2)   # hair
line(c, [(jx - 45, jy - 9), (jx - 41, jy - 9)], K, .8)                                                    # closed eye
line(c, bez((jx - 30, jy - 4), (jx - 18, jy + 4), (jx - 6, jy + 6), (jx + 6, jy + 2), 8), WH, 2.2)         # arm
line(c, [(jx - 30, jy + 14), (jx + 78, jy + 10)], K, 1.4)                                                 # staff
# sheep
for (sx, sy, s) in ((262, 560, 1.0), (292, 572, 1.15), (322, 556, .9), (236, 578, 1.1), (372, 574, 1.0)):
    for k in range(5):
        disc(c, sx + (k - 2) * 3.4 * s, sy + (k % 2) * 1.5, 4.6 * s, WH, K, .8)
    for k in range(5):
        disc(c, sx + (k - 2) * 3.4 * s, sy + (k % 2) * 1.5, 4.6 * s - .8, WH)
    disc(c, sx - 9.5 * s, sy - 1, 2.8 * s, K)
    line(c, [(sx - 4 * s, sy + 4 * s), (sx - 4 * s, sy + 8 * s)], K, .9); line(c, [(sx + 4 * s, sy + 4 * s), (sx + 4 * s, sy + 8 * s)], K, .9)
border(a, Y, 5, 1.6, 3)
a.finish()
