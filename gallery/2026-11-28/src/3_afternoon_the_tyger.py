"""Afternoon — The Tyger.  A mirror-symmetric face ("fearful symmetry") built from
implicit fields in numpy: stripes are warped rings round the nose-bridge; jungle leaves
are drawn behind and in front."""
import math, sys, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.dirname(__file__))
from common import *

rng = np.random.default_rng(1794)
a = Art(K)
c = a.c
CX, CY = 200, 300

# ---------- background: forest of the night
nb = fbm(9, 80, 3, W * S, H * S)
bgc = np.zeros((H * S, W * S, 3), np.float32)
for i in range(3):
    bgc[..., i] = np.array(K)[i] * (1 - nb * .5) + np.array(mix(B, K, .5))[i] * nb * .5
a.col = Image.fromarray(bgc.astype(np.uint8)); c = a.c = ImageDraw.Draw(a.col)
back_k = Image.new("L", (W * S, H * S), 0); bk = ImageDraw.Draw(back_k)
LCOL = [G, G, FOREST, mix(G, K, .3), LIME, TEAL, mix(G, Y, .25), mix(G, K, .7), mix(G, WH, .2)]

def jungle_leaf(cd, kd, x, y, ang, L, wd, col):
    pts = leaf(x, y, ang, L, wd, 18)
    poly(cd, pts, col); poly(kd, pts, 0, 255, 1.3)
    ca, sa = math.cos(ang), math.sin(ang)
    line(kd, [(x, y), (x + L * ca, y + L * sa)], w=1.1)
    n = int(L / 9)
    for i in range(1, n):
        t = i / n; hw = wd * math.sin(math.pi * t) ** .8 * (1 - .35 * t) * .85
        bx, by = x + L * t * ca, y + L * t * sa
        for sg in (1, -1):
            line(kd, [(bx, by), (bx + L * .09 * ca - sg * hw * sa, by + L * .09 * sa + sg * hw * ca)], w=.75)

def frond(cd, kd, x, y, ang, L, col):
    ca, sa = math.cos(ang), math.sin(ang)
    line(kd, [(x, y), (x + L * ca, y + L * sa)], w=1.6)
    n = int(L / 7)
    for i in range(1, n):
        t = i / n; ll = L * .34 * math.sin(math.pi * t) ** .6 + 5
        bx, by = x + L * t * ca, y + L * t * sa
        for sg in (1, -1):
            p = leaf(bx, by, ang + sg * 1.05, ll, 2.6, 5)
            poly(cd, p, col); poly(kd, p, 0, 255, .8)

items = []
for i in range(150):
    th = rng.uniform(0, 2 * math.pi); r = rng.uniform(95, 330)
    items.append((r, th))
items.sort(reverse=True)
for r, th in items:
    x, y = CX + r * math.cos(th) * .8, CY + 10 + r * math.sin(th)
    ang = th + rng.uniform(-.7, .7)
    col = LCOL[int(rng.integers(len(LCOL)))]
    if rng.random() < .25:
        frond(c, bk, x, y, ang, rng.uniform(60, 110), col)
    else:
        jungle_leaf(c, bk, x, y, ang, rng.uniform(55, 120), rng.uniform(12, 26), col)
# flowers and fireflies
flw = []
for i in range(9):
    th = rng.uniform(0, 2 * math.pi); r = rng.uniform(190, 300)
    x, y = CX + r * math.cos(th) * .8, CY + r * math.sin(th)
    for k in range(5):
        t = k * 2 * math.pi / 5 + i
        p = leaf(x, y, t, 11, 4.5, 6); poly(c, p, R); poly(bk, p, 0, 255, .8)
    disc(c, x, y, 3, Y); disc(bk, x, y, 3, None, 255, .8)

# ---------- the face, as fields at 3x
yy, xx = np.mgrid[0:H * S, 0:W * S].astype(np.float32)
X, Yv = (xx + .5) / S, (yy + .5) / S
u = np.abs(X - CX); v = Yv
# symmetric noise: sample noise by (u, v)
def symn(seed, scale, oc=3):
    n = fbm(seed, scale * S, oc, W * S, H * S)
    ui = np.clip((u * S).astype(int), 0, W * S - 1); vi = np.clip((v * S).astype(int), 0, H * S - 1)
    return n[vi, ui]
n1, n2, n3 = symn(21, 46), symn(22, 30), symn(23, 9, 2)

hc = 318
th = np.arctan2(v - hc, u); rad = np.hypot(u, v - hc)
Rh = 146 + 24 * np.exp(-((th - .55) / .45) ** 2) - 10 * np.exp(-((th + 1.57) / .5) ** 2) - 16 * np.exp(-((th - 1.57) / .4) ** 2)
tri = np.abs(((th * 21) % 2) - 1)
jag = np.where(th > -.5, 7 * tri * np.clip((th + .5) / .5, 0, 1), 0)
head = rad < Rh + jag - 3
ear_d = np.hypot(u - 108, v - 186)
ear = ear_d < 42
ear_in = np.hypot(u - 106, v - 194) < 25
body = (v > 430) & (u < 150 + (v - 430) * .75 + 6 * np.abs(((v * .19) % 2) - 1))
fig = head | ear | body

# fur colour: yellow heart, orange, red-orange rim
t_ = np.clip(np.hypot(u / 150, (v - 320) / 170) + (n1 - .5) * .35, 0, 1.2)
fur = np.zeros(bgc.shape, np.float32)
c0, c1, c2 = np.array(mix(R, Y, .64), np.float32), np.array(mix(R, Y, .48), np.float32), np.array(mix(R, Y, .3), np.float32)
w01 = np.clip(t_ / .55, 0, 1)[..., None]; w12 = np.clip((t_ - .55) / .5, 0, 1)[..., None]
fur = c0 * (1 - w01) + c1 * w01; fur = fur * (1 - w12) + c2 * w12

# white areas
wn = (n2 - .5) * .22 + (n3 - .5) * .12
muzz = (np.hypot(u - 30, v - 388) < 44 * (1 + wn)) | (np.hypot(u / 42, (v - 430) / 28) < 1 + wn)
brow = np.hypot((u - 60) / 31, (v - 257) / 15) < 1 + wn
ruff = (np.hypot((u - 146) / 66, (v - 402) / 74) < 1 + wn * 1.4) & (v > 318)
chest = body & (u < 46 + (v - 430) * .28 + 30 * (n2 - .5)) & (v > 446)
white = (muzz | brow | ruff | chest) & (head | body)

# stripes: rings round the nose bridge, warped and broken
rr = np.hypot(u * 1.0, (v - 344) * 1.06) + 26 * (n1 - .5) + 7 * (n3 - .5)
ring = np.sin(rr * .345)
core = np.hypot(u / 96, (v - 352) / 86)                 # open face: no stripes
gate = np.clip((core - 1.0) / .35, 0, 1)
fore = (v < 250) & (u < 78)                              # forehead wedge keeps stripes
gate = np.maximum(gate, np.where(fore, np.clip((258 - v) / 26, 0, 1), 0))
brk = np.clip((n2 - .22) / .22, 0, 1)                    # breaks & tapers
thick = .12 + .9 * (1 - gate * brk)
stripe = (ring > thick) & head & ~(np.hypot((u - 60) / 36, (v - 262) / 20) < 1)
# forehead centre: a few short bars
bar = (np.abs(u) < 5 + 9 * np.clip((240 - v) / 60, 0, 1)) & (np.sin(v * .42) > .45) & (v > 188) & (v < 250)
# body stripes: chevrons
bs = (np.sin((v - .42 * u + 18 * (n1 - .5)) * .33) > .55 + .6 * (1 - brk)) & body & ~head & (u > 30)
stripe = stripe | bar | bs

# eyes
ev = (v - 291) + (u - 58) * .24
eye = np.hypot((u - 58) / 27, ev / 14.5) < 1
liner = (np.hypot((u - 57) / 34, (ev - 1) / 20.5) < 1) | ((np.abs(u - 26 + (v - 300) * .35) < 4.2 - (v - 300) * .12) & (v > 296) & (v < 330))
iris_r = np.hypot(u - 58, v - 291)
pupil = iris_r < 7.6
glint = np.hypot(u - 54, v - 286.5) < 2.6
# nose
nt = np.clip((v - 345) / 27, 0, 1)
nose = (v > 345) & (v < 372) & (u < 19 * (1 - nt ** 1.7) ** .7 + 1)
nose_k = (v > 343) & (v < 374.5) & (u < 21 * (1 - np.clip((v - 343) / 31, 0, 1) ** 1.7) ** .7 + 3)
nostril = (np.hypot((u - 9) / 4.5, (v - 362) / 2.6) < 1)
bridge_l = (np.abs(u - (20 + (345 - v) * .10)) < 1.1) & (v > 300) & (v < 345)   # sides of the nose bridge

# compose colour
img = np.asarray(a.col, np.float32).copy()
def put(mask, col):
    img[mask] = np.array(col, np.float32)
img[fig] = fur[fig]
put(ear & ~head, mix(R, Y, .35)); put(ear_in & ~head, WH)
put(white, WH)
# soft shading under brow / chin on white: pale cream screens
put(eye, Y); put(eye & (iris_r > 11.5) & (iris_r < 14), mix(Y, G, .45))
put(nose, mix(R, WH, .35))
a.col = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)); c = a.c = ImageDraw.Draw(a.col)

def L(mask):
    return Image.fromarray((mask * 255).astype(np.uint8))
# background outlines, cut by the figure
a.ink_image(K, L((np.asarray(back_k) > 127) & ~fig))
# black: silhouette edge, stripes, liner, pupils, nose rim
edge = np.asarray(L(fig).filter(ImageFilter.MaxFilter(9))) > 127
edge_in = np.asarray(L(fig).filter(ImageFilter.MinFilter(5))) > 127
ear_edge = ear & ~head & ((ear_d > 37.5) | (ear_in & (np.sin(th * 0 + np.arctan2(v - 194, u - 106) * 9) > .72) & (np.hypot(u - 106, v - 194) > 9)))
black = (edge & ~edge_in) | stripe | (liner & ~eye) | pupil | (nose_k & ~nose) | nostril | ear_edge | (bridge_l & head)
black = black & ~glint
a.ink_image(K, L(black))
a.ink_image(WH, L(glint | (eye & (np.hypot(u - 63, v - 296) < 1.5))))

# mouth, whisker pads, whiskers
mk = a.ink(K)
for sg in (1, -1):
    line(mk, bez((CX, 372), (CX, 386), (CX + sg * 3, 396), (CX + sg * 18, 401), 14), w=2.4)
    line(mk, bez((CX + sg * 18, 401), (CX + sg * 34, 404), (CX + sg * 46, 396), (CX + sg * 52, 384), 14), w=2.0)
    for r_ in range(3):
        for k in range(4 - r_ // 2):
            disc(mk, CX + sg * (22 + k * 10 + r_ * 3), 372 + r_ * 8 + k * 1.5, 1.5)
line(mk, bez((CX - 14, 412), (CX - 6, 420), (CX + 6, 420), (CX + 14, 412), 10), w=1.6)
# fur ticks on the chin and brow
for i in range(40):
    x = rng.uniform(4, 36); y = rng.uniform(424, 452)
    for sg in (1, -1):
        line(mk, [(CX + sg * x, y), (CX + sg * (x + 1.5), y + 5)], w=.8)
wk = a.ink(WH)
for sg in (1, -1):
    for k, (dy, ex, ey) in enumerate(((0, 150, -34), (6, 162, -6), (12, 158, 22), (18, 140, 46), (3, 120, -52))):
        x0, y0 = CX + sg * (34 + k * 4), 376 + dy
        line(wk, bez((x0, y0), (x0 + sg * 40, y0 + ey * .1), (x0 + sg * ex * .7, y0 + ey * .5), (x0 + sg * ex, y0 + ey), 30), w=1.25)
    for k in range(4):   # brow whiskers
        x0, y0 = CX + sg * (50 + k * 7), 246
        line(wk, bez((x0, y0), (x0 + sg * 6, y0 - 24), (x0 + sg * 16, y0 - 44), (x0 + sg * (30 + k * 6), y0 - 58), 20), w=1.0)

# ---------- foreground leaves over the chest
fk = a.ink(K)
fg_col = Image.new("RGB", (W * S, H * S)); fgm = Image.new("L", (W * S, H * S), 0)
for (x, y, ang, L_, wd, col) in ((-10, 610, -62, 150, 34, G), (40, 620, -78, 120, 28, LIME), (-20, 540, -28, 120, 26, FOREST),
                                 (410, 610, -118, 150, 34, G), (360, 620, -102, 120, 28, mix(G, Y, .25)), (420, 540, -152, 120, 26, FOREST),
                                 (120, 625, -96, 86, 22, TEAL), (280, 625, -84, 86, 22, TEAL)):
    lay = a.ink(col if col in (G,) else G)
    pts = leaf(x, y, math.radians(ang), L_, wd, 18)
    poly(c, pts, col)
    # ensure colour shows: knock the figure's black/white inks out under the leaf
    m = Image.new("L", (W * S, H * S), 0); poly(ImageDraw.Draw(m), pts, 255)
    for i_, (rgb, im) in enumerate(a.inks[:-1]):
        im.paste(0, mask=m)
    a.inks.pop()
    kd = a.ink(K)
    jungle_leaf(Image.new("RGB", (1, 1)) and ImageDraw.Draw(Image.new("RGB", (W * S, H * S))), kd, x, y, math.radians(ang), L_, wd, col)
border(a, Y, 5, 1.6, 3)
a.finish()
