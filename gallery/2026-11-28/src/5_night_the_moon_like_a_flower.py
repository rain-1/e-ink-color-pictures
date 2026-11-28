"""Night — "The moon like a flower / In heaven's high bower".
Tonight's waning gibbous (80%) as the heart of a blue flower, Jupiter beside it, a bare
November tree with an owl and a nest, a cottage with one lit window, the fold asleep."""
import math, sys, os
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(__file__))
from common import *

rng = np.random.default_rng(1789)
a = Art(K, crisp=True)
MX, MY, MR = 236, 168, 60

yy, xx = np.mgrid[0:H * S, 0:W * S].astype(np.float32)
X, Yv = xx / S, yy / S
d = np.hypot(X - MX, Yv - MY)
n = fbm(2, 90 * S, 3, W * S, H * S)
# sky: black, warming to blue round the moon
t = np.clip(1 - (d - 60) / 330 + (n - .5) * .25, 0, 1) ** 1.5 * .62
t = np.where(Yv > 470, t * np.clip(1 - (Yv - 470) / 50, 0, 1), t)
sky = np.array(K, np.float32) * (1 - t[..., None]) + np.array(B, np.float32) * t[..., None]
sky = np.clip(sky, 1, 254)
a.col = Image.fromarray(sky.astype(np.uint8)); c = a.c = ImageDraw.Draw(a.col)

# ---- the flower: two rings of petals behind the moon
for (cnt, r0, L_, wd, col, off) in ((14, 50, 92, 25, mix(B, K, .22), .11), (14, 48, 66, 21, B, .335)):
    for i in range(cnt):
        th = off + i * 2 * math.pi / cnt
        p = leaf(MX + r0 * math.cos(th), MY + r0 * math.sin(th), th, L_, wd, 14)
        poly(c, p, col, K, 1.0)
        for s_ in (-.045, 0, .045):
            line(c, [(MX + (r0 + 16) * math.cos(th + s_), MY + (r0 + 16) * math.sin(th + s_)),
                     (MX + (r0 + L_ * .72) * math.cos(th + s_ * 1.7), MY + (r0 + L_ * .72) * math.sin(th + s_ * 1.7))], mix(B, WH, .35), .7)

# ---- stars and Jupiter
for i in range(700):
    x, y = int(rng.integers(8, W - 8)), int(rng.integers(8, 470))
    if math.hypot(x - MX, y - MY) < 148: continue
    col = WH if rng.random() < .8 else Y
    c.rectangle([x * S, y * S, x * S + S - 1, y * S + S - 1], fill=col)
    if rng.random() < .1:
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            c.rectangle([(x + dx) * S, (y + dy) * S, (x + dx) * S + S - 1, (y + dy) * S + S - 1], fill=col)
jx, jy = 352, 52
for L_, w_ in ((11, 1.0), (5, 2.4)):
    line(c, [(jx - L_, jy), (jx + L_, jy)], Y, w_); line(c, [(jx, jy - L_), (jx, jy + L_)], Y, w_)
disc(c, jx, jy, 3.2, WH)
for k, dx in enumerate((-16, -9, 8, 19)):               # the four moons, in a line
    c.rectangle([(jx + dx) * S, (jy + 9) * S, (jx + dx) * S + S - 1, (jy + 9) * S + S - 1], fill=WH)

# ---- the moon
img = np.asarray(a.col, np.float32).copy()
mx_, my_ = X - MX, Yv - MY
inm = d < MR
term = .6 * np.sqrt(np.clip(MR ** 2 - my_ ** 2, 0, None))
lit = inm & (mx_ < term)
mn = fbm(11, 34 * S, 4, W * S, H * S); mn2 = fbm(12, 9 * S, 2, W * S, H * S)
img[inm] = np.array(mix(B, K, .55), np.float32)                  # earthshine side
img[lit] = np.array(WH, np.float32)
img[lit & (d > MR - 7)] = np.array(mix(WH, Y, .3), np.float32)
sea = mn + .12 * (mn2 - .5) + .1 * np.exp(-((mx_ + 14) ** 2 + (my_ + 12) ** 2) / 900)
img[lit & (sea > .55)] = np.array(mix(WH, K, .28), np.float32)
img[lit & (sea > .64)] = np.array(mix(WH, K, .45), np.float32)
a.col = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)); c = a.c = ImageDraw.Draw(a.col)
for i in range(26):                                              # craters
    th = rng.uniform(0, 2 * math.pi); r = MR * math.sqrt(rng.uniform(0, .86)); cr = rng.uniform(1.8, 5.5)
    x, y = MX + r * math.cos(th), MY + r * math.sin(th)
    if x - MX > .6 * math.sqrt(max(0, MR ** 2 - (y - MY) ** 2)) - cr - 2: continue
    disc(c, x, y, cr, WH); c.arc([(x - cr) * S, (y - cr) * S, (x + cr) * S, (y + cr) * S], 300, 120, fill=K, width=int(.9 * S))
tx, ty = MX - 12, MY + 38                                        # a rayed crater
for i in range(11):
    th = i * 2 * math.pi / 11 + .2
    line(c, [(tx + 4 * math.cos(th), ty + 4 * math.sin(th)), (tx + rng.uniform(10, 19) * math.cos(th), ty + rng.uniform(10, 19) * math.sin(th))], WH, .8)
disc(c, tx, ty, 3.2, WH, K, .8)
disc(c, MX, MY, MR, None, K, 1.0)

# ---- ground, cottage, fold
hn = fbm(6, 70, 3, W, 4)[0]
hy = [498 + 12 * (hn[x] - .5) + 10 * (x / 400) for x in range(W)]
poly(c, [(x, hy[x]) for x in range(W)] + [(W, H), (0, H)], K)
for x in range(0, W, 3):                                         # moonlit rim of grass
    L_ = rng.uniform(2, 6)
    line(c, [(x, hy[x] + 1), (x + rng.uniform(-1.5, 1.5), hy[x] - L_)], B if x % 2 else mix(B, WH, .4), .8)
hx, hb = 286, hy[310] + 2
wall = [(hx, hb), (hx, hb - 26), (hx + 70, hb - 26), (hx + 70, hb)]
poly(c, wall, mix(B, K, .5), None)
roof = [(hx - 7, hb - 24), (hx + 10, hb - 50), (hx + 62, hb - 50), (hx + 77, hb - 24)]
poly(c, roof, mix(Y, K, .62), WH, .8)
for k in range(13):
    x = hx + 2 + k * 5.6
    line(c, [(x, hb - 26), (x + (4 if k < 6 else -4) * .6, hb - 48)], K, .8)
line(c, [(hx, hb - 25), (hx, hb), (hx + 70, hb), (hx + 70, hb - 25)], WH, .8)
c.rectangle([(hx + 46) * S, (hb - 56) * S, (hx + 53) * S, (hb - 44) * S], fill=mix(B, K, .5), outline=WH, width=2)
c.rectangle([(hx + 12) * S, (hb - 19) * S, (hx + 24) * S, (hb - 7) * S], fill=Y, outline=K, width=3)
line(c, [(hx + 18, hb - 19), (hx + 18, hb - 7)], K, .9); line(c, [(hx + 12, hb - 13), (hx + 24, hb - 13)], K, .9)
c.rectangle([(hx + 36) * S, (hb - 20) * S, (hx + 47) * S, hb * S], fill=K, outline=WH, width=2)
c.rectangle([(hx + 54) * S, (hb - 18) * S, (hx + 63) * S, (hb - 9) * S], fill=K, outline=WH, width=2)
px, py = hx + 49.5, hb - 58                                      # smoke
pts = [(px + 5 * math.sin(k * .5) + k * .9, py - k * 3.2) for k in range(22)]
for k in range(0, 21, 2):
    line(c, pts[k:k + 2], mix(B, WH, .6), 1.0)
# light spilling from the window
poly(c, [(hx + 10, hb + 3), (hx + 26, hb + 3), (hx + 34, hb + 22), (hx - 2, hb + 22)], mix(Y, K, .6))
# fold: hurdles and sleeping sheep
for x in range(176, 280, 13):
    y = hy[x] + 16
    line(c, [(x, y), (x, y - 13)], WH, .9)
line(c, [(176, hy[176] + 8), (267, hy[267] + 8)], WH, .8); line(c, [(176, hy[176] + 12.5), (267, hy[267] + 12.5)], WH, .8)
for (sx, sy, s) in ((200, 540, 1.0), (232, 552, 1.1), (262, 540, .9), (296, 556, 1.0), (214, 568, 1.0), (332, 566, .9), (366, 548, 1.0)):
    for k in range(5):
        disc(c, sx + (k - 2) * 3.4 * s, sy + (k % 2) * 1.2, 4.4 * s, WH)
    for k in range(4):
        c.arc([(sx + (k - 2) * 3.4 * s - 3) * S, (sy - 1) * S, (sx + (k - 2) * 3.4 * s + 3) * S, (sy + 5) * S], 20, 160, fill=B, width=2)
    disc(c, sx - 9 * s, sy + 2, 2.6 * s, mix(B, WH, .5), None)

# ---- the tree: bare, November
tips = []
def branch(x, y, ang, L_, w_, depth):
    x2, y2 = x + L_ * math.cos(ang), y + L_ * math.sin(ang)
    if w_ > 2.5:
        line(c, [(x, y), (x2, y2)], mix(B, WH, .0), w_ + 1.4)   # moonlit edge
    line(c, [(x - .0, y), (x2, y2)], K, w_)
    if depth == 0:
        tips.append((x2, y2)); return
    for da in (rng.uniform(-.7, -.28), rng.uniform(.25, .65), rng.uniform(-.12, .12)):
        if rng.random() < .9 or depth > 4:
            branch(x2, y2, ang + da - .02 * math.cos(ang) * 4, L_ * rng.uniform(.68, .84), max(.8, w_ * .66), depth - 1)
branch(66, 530, -math.pi / 2 + .1, 96, 13, 7)
poly(c, [(46, 540), (58, 500), (76, 500), (92, 540)], K)
# owl on a bough, nest in a fork
ox, oy = 118, 316
line(c, [(84, oy + 13), (150, oy + 11)], K, 3.4)
ell(c, ox, oy, 9, 13, K, WH, .8)
poly(c, [(ox - 8, oy - 9), (ox - 6, oy - 17), (ox - 2, oy - 11)], K); poly(c, [(ox + 8, oy - 9), (ox + 6, oy - 17), (ox + 2, oy - 11)], K)
for sg in (-1, 1):
    disc(c, ox + sg * 4, oy - 5, 3.3, Y, None); disc(c, ox + sg * 4, oy - 5, 1.3, K)
poly(c, [(ox - 1.4, oy - 2), (ox + 1.4, oy - 2), (ox, oy + 1.5)], Y)
for k in range(3):
    c.arc([(ox - 5) * S, (oy + 1 + k * 3) * S, (ox + 5) * S, (oy + 6 + k * 3) * S], 20, 160, fill=WH, width=2)
nx, ny = 52, 250
c.chord([(nx - 11) * S, (ny - 7) * S, (nx + 11) * S, (ny + 7) * S], 0, 180, fill=mix(Y, K, .5), outline=WH, width=2)
for sg in (-1, 1):
    disc(c, nx + sg * 4, ny - 1.5, 3, WH, K, .7)

# ---- the stanza
tk = a.ink(WH)
f = font(13.5)
for k, s_ in enumerate(("The moon like a flower", "In heaven's high bower,", "With silent delight", "Sits and smiles on the night.")):
    text(tk, (16, 536 + k * 15), s_, f, anchor="lm")
border(a, B, 5, 1.6, 3)
a.finish()
