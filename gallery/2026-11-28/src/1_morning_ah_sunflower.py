"""Morning — Ah! Sun-flower.  Phyllotaxis seed head, engraved sunrise, illuminated border."""
import math, sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from common import *

rng = np.random.default_rng(1757)
a = Art(PALE)
c = a.c
HOR = 400            # horizon y
SX, SY = 290, 392    # the rising sun the flower is counting the steps of
FX, FY = 172, 232    # flower head

# ---- sky: bands of dawn, painted as concentric glows round the sun
for r, col in ((640, SKY), (520, mix(SKY, WH, .5)), (430, PALE), (350, CREAM), (270, mix(CREAM, Y, .4)),
               (200, mix(Y, WH, .25)), (140, Y), (95, AMBER), (62, ORANGE)):
    disc(c, SX, SY, r, col)
disc(c, SX, SY, 40, mix(R, Y, .3))
disc(c, SX, SY, 31, Y)

# engraved rays (alternating long/short, broken where the flower will sit)
ray = a.ink(R)
for i in range(72):
    th = math.pi + i * math.pi / 72 + .01
    r0 = 46 if i % 2 == 0 else 58
    r1 = (700 if i % 4 == 0 else 150 if i % 2 == 0 else 96)
    line(ray, [(SX + r0 * math.cos(th), SY + r0 * math.sin(th)), (SX + r1 * math.cos(th), SY + r1 * math.sin(th))], w=.9 if i % 4 else 1.3)
disc(ray, SX, SY, 41, 0); disc(ray, SX, SY, 41, None, 255, 1.2); disc(ray, SX, SY, 31, None, 255, 1)

# little clouds, long and flat
cl = a.ink(WH); clk = a.ink(K)
for (x, y, s) in ((70, 70, 1.0), (310, 120, .8), (250, 46, .6), (60, 330, .7)):
    for k in range(5):
        ell(cl, x + (k - 2) * 15 * s, y + (k % 2) * 4 * s, 16 * s, 6 * s)
    for k in range(3):
        line(clk, [(x - 34 * s + k * 9, y + 9 * s + k * 3), (x + 30 * s - k * 6, y + 9 * s + k * 3)], w=.8)

# birds (larks) going up
bd = a.ink(K)
for (x, y, s) in ((330, 210, 1.2), (352, 188, .9), (308, 176, .8), (70, 150, 1.0), (92, 128, .7), (240, 92, .7)):
    line(bd, bez((x - 9 * s, y - 2 * s), (x - 5 * s, y - 7 * s), (x - 2 * s, y - 4 * s), (x, y)), w=1.5)
    line(bd, bez((x, y), (x + 2 * s, y - 5 * s), (x + 6 * s, y - 7 * s), (x + 10 * s, y - 1 * s)), w=1.5)

# ---- land: three ranges of hills with furrows, hedges, a village
def hill(y0, amp, seed, col, step=1):
    n = fbm(seed, 90, 3, W, 4)[0]
    ys = [y0 - amp * (n[x] - .5) * 2 for x in range(W)]
    poly(c, [(x, ys[x]) for x in range(W)] + [(W, H), (0, H)], col)
    return ys
h1 = hill(HOR, 18, 3, mix(B, WH, .45))
h2 = hill(HOR + 26, 16, 5, mix(G, WH, .25))
h3 = hill(HOR + 62, 14, 8, mix(G, Y, .35))
h4 = hill(HOR + 112, 12, 11, G)
h5 = hill(HOR + 160, 8, 12, FOREST)
ld = a.ink(K)
for ys in (h1, h2, h3, h4, h5):
    line(ld, [(x, ys[x]) for x in range(0, W, 2)], w=1.1)
# far-hill hatching
for x in range(4, W, 5):
    line(ld, [(x, h1[x] + 3), (x - 3, h1[x] + 3 + 5 + (x * 7) % 9)], w=.7)
# furrows on the middle fields: fans of curves converging toward the sun's foot
fur = a.ink(K)
poly(ray, [(x, h1[x]) for x in range(W)] + [(W, H), (0, H)], 0)   # rays stop at the hills
for i in range(-40, 41):
    th = math.pi / 2 + i * .036
    pts = []
    for t in np.linspace(0, 260, 90):
        x, y = SX + t * math.cos(th) * 2.2, HOR + 70 + t * math.sin(th) * .55
        if 0 <= x < W and h3[int(x)] + 3 < y < h4[int(x)] - 1:
            pts.append((x, y))
    if len(pts) > 1:
        line(fur, pts, w=.8)
# hedgerows / trees along ridges
tr = a.ink(K); trg = a.ink(G)
for x in range(6, W, 9):
    xx = x + int(rng.integers(-3, 4)); s = rng.uniform(2.6, 4.6)
    disc(tr, xx, h2[xx] - s * .6, s)
for x in range(10, W, 23):
    xx = min(W - 1, x + int(rng.integers(-6, 7))); s = rng.uniform(5, 9)
    line(tr, [(xx, h4[xx] + 2), (xx, h4[xx] - s * 1.5)], w=1.3)
    disc(tr, xx, h4[xx] - s * 1.7, s + 1); disc(trg, xx, h4[xx] - s * 1.7, s - .4)
    for k in range(5):
        disc(tr, xx + rng.uniform(-s, s) * .6, h4[xx] - s * 1.7 + rng.uniform(-s, s) * .6, .8)
# village on the second ridge: church + houses
vk = a.ink(K); vw = a.ink(WH); vr = a.ink(R)
vx = 78
by = h3[vx] + 1
for i, (dx, w_, hh) in enumerate(((-34, 12, 8), (-20, 10, 7), (-8, 13, 9), (16, 11, 7), (29, 12, 8), (43, 9, 6))):
    x = vx + dx; y = h3[x] + 2
    poly(vw, [(x, y), (x, y - hh), (x + w_, y - hh), (x + w_, y)])
    poly(vr, [(x - 1.5, y - hh), (x + w_ / 2, y - hh - 6), (x + w_ + 1.5, y - hh)])
    poly(vk, [(x, y), (x, y - hh), (x + w_, y - hh), (x + w_, y)], 0, 255, .9)
    line(vk, [(x - 1.5, y - hh), (x + w_ / 2, y - hh - 6), (x + w_ + 1.5, y - hh)], w=.9)
    vk.rectangle([(x + w_ / 2 - 1) * S, (y - 5) * S, (x + w_ / 2 + 1) * S, y * S], fill=255)
x = vx + 4; y = h3[x] + 2
poly(vw, [(x, y), (x, y - 20), (x + 7, y - 20), (x + 7, y)])
poly(vk, [(x, y), (x, y - 20), (x + 7, y - 20), (x + 7, y)], 0, 255, .9)
poly(vk, [(x - 1, y - 20), (x + 3.5, y - 36), (x + 8, y - 20)])
line(vk, [(x + 3.5, y - 36), (x + 3.5, y - 41)], w=.9); line(vk, [(x + 1.5, y - 39), (x + 5.5, y - 39)], w=.9)
vk.rectangle([(x + 2.5) * S, (y - 15) * S, (x + 4.5) * S, (y - 10) * S], fill=255)
# foreground grass blades
gr = a.ink(K)
for i in range(150):
    x = rng.uniform(0, W); y = rng.uniform(h5[int(x)] + 6, H - 6); L = rng.uniform(6, 14); b = rng.uniform(-4, 4)
    line(gr, bez((x, y), (x, y - L * .5), (x + b * .5, y - L * .8), (x + b, y - L), 6), w=.9)
ygr = a.ink(Y)
for i in range(70):
    x = rng.uniform(0, W); y = rng.uniform(h5[int(x)] + 8, H - 10)
    disc(ygr, x, y, 1.3)

# ---- the sunflower: stem, leaves, petals, seed head
stem = bez((150, 610), (120, 500), (205, 400), (FX + 6, FY + 40), 40)
sk = a.ink(K); sg = a.ink(G)
line(sk, stem, w=11); line(sg, stem, w=8.4)
sl = a.ink(K)
line(sl, [(x + 2.2, y) for x, y in stem], w=.8)

def big_leaf(cx, cy, ang, L, wd):
    pts = leaf(cx, cy, ang, L, wd, 20)
    lg = a.ink(G); lk = a.ink(K)
    poly(lg, pts); poly(lk, pts, 0, 255, 1.4)
    ca, sa = math.cos(ang), math.sin(ang)
    line(lk, [(cx, cy), (cx + L * ca, cy + L * sa)], w=1.1)
    for i in range(1, 9):
        t = i / 9.5; hw = wd * math.sin(math.pi * t) ** .8 * (1 - .35 * t) * .86
        bx, by = cx + L * t * ca, cy + L * t * sa
        for sgn in (1, -1):
            ex = bx + L * .1 * ca - sgn * hw * sa; ey = by + L * .1 * sa + sgn * hw * ca
            line(lk, [(bx, by), (ex, ey)], w=.75)
    # light side: yellow-green screen hatch
    ly = a.ink(Y)
    for i in range(2, 18):
        t = i / 19; hw = wd * math.sin(math.pi * t) ** .8 * (1 - .35 * t) * .55
        bx, by = cx + L * t * ca, cy + L * t * sa
        disc(ly, bx + hw * sa * .6, by - hw * ca * .6, .9)
big_leaf(139, 520, math.radians(200), 92, 30)
big_leaf(152, 470, math.radians(-28), 104, 32)
big_leaf(176, 400, math.radians(168), 84, 26)
big_leaf(196, 352, math.radians(-12), 70, 20)

# petals: two rings, back ring orange, front ring yellow, each outlined and veined
pk = a.ink(K)
def petals(n, r0, L, wd, col, off, vein=True):
    lay = a.ink(col); kk = a.ink(K)
    for i in range(n):
        th = off + i * 2 * math.pi / n + rng.uniform(-.03, .03)
        LL = L * rng.uniform(.9, 1.08)
        pts = leaf(FX + r0 * math.cos(th), FY + r0 * math.sin(th), th + rng.uniform(-.08, .08), LL, wd, 10)
        poly(lay, pts); poly(kk, pts, 0, 255, 1.1)
        if vein:
            for s in (-.3, 0, .3):
                line(kk, [(FX + (r0 + 6) * math.cos(th + s * .05), FY + (r0 + 6) * math.sin(th + s * .05)),
                          (FX + (r0 + LL * .62) * math.cos(th + s * .09), FY + (r0 + LL * .62) * math.sin(th + s * .09))], w=.7)
petals(21, 62, 62, 13, mix(R, Y, .0), .07, False)   # deep back ring (red, reads as shadow petals)
petals(21, 60, 56, 14, Y, .22)
petals(21, 58, 50, 13, Y, 0.0)

# seed head: Vogel spiral, 610 florets, coloured by ring
hk = a.ink(K)
disc(hk, FX, FY, 67)
N = 610; ga = math.pi * (3 - math.sqrt(5))
layers = {c_: a.ink(c_) for c_ in (Y, R, G, WH)}
for i in range(N, 0, -1):
    r = 65 * math.sqrt(i / N); th = i * ga
    x, y = FX + r * math.cos(th), FY + r * math.sin(th)
    s = .9 + 1.25 * (i / N) ** .7
    if r < 14: col = G
    elif r < 25: col = Y
    elif r < 47: col = R if i % 3 else Y
    elif r < 58: col = Y if i % 2 else R
    else: col = WH if i % 3 == 0 else Y
    disc(layers[col], x, y, s)
ring = a.ink(K)
disc(ring, FX, FY, 67.5, None, 255, 1.6)

# ---- illuminated border with a running vine, and the line itself
bw = a.ink(WH)
bw.rectangle([0, 0, W * S, 13 * S], fill=255); bw.rectangle([0, (H - 34) * S, W * S, H * S], fill=255)
bw.rectangle([0, 0, 13 * S, H * S], fill=255); bw.rectangle([(W - 13) * S, 0, W * S, H * S], fill=255)
bk = a.ink(K); bg = a.ink(G); br = a.ink(R)
bk.rectangle([13 * S, 13 * S, (W - 13) * S, (H - 34) * S], outline=255, width=int(1.6 * S))
bk.rectangle([3 * S, 3 * S, (W - 3) * S, (H - 3) * S], outline=255, width=int(1 * S))
def vine(p0, p1, n):
    (x0, y0), (x1, y1) = p0, p1
    L = math.hypot(x1 - x0, y1 - y0); ux, uy = (x1 - x0) / L, (y1 - y0) / L
    pts = [(x0 + ux * t + -uy * 2.2 * math.sin(t / L * n * math.pi), y0 + uy * t + ux * 2.2 * math.sin(t / L * n * math.pi)) for t in np.linspace(0, L, n * 8)]
    line(bg, pts, w=1.2)
    for k in range(n):
        t = (k + .5) / n * L; sgn = 1 if k % 2 else -1
        bx, by = x0 + ux * t - uy * 2.2 * sgn, y0 + uy * t + ux * 2.2 * sgn
        ang = math.atan2(uy, ux) + sgn * 1.0
        poly(bg, leaf(bx, by, ang, 5.2, 1.9, 6))
        if k % 4 == 1:
            disc(br, x0 + ux * t + uy * 2.6 * sgn, y0 + uy * t - ux * 2.6 * sgn, 1.5)
vine((18, 8), (W - 18, 8), 30); vine((8, 18), (8, H - 38), 44); vine((W - 8, 18), (W - 8, H - 38), 44)
tk = a.ink(K)
text(tk, (W / 2, H - 19), "Ah! Sun-flower, weary of time,", font(15))
a.finish()
