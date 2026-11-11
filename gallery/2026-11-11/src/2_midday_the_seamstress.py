"""Midday — The Seamstress (for Edouard Vuillard, born 11 November 1868).
An intimiste interior in which everything is pattern: wallpaper, curtain, dress, gingham,
rug. Every surface is its own repeat, drawn flat in pure inks; the woman is told from the
wall only by the change of repeat, which was Vuillard's whole trick."""
import math, random
from PIL import Image, ImageDraw
from kit import *

random.seed(1868)
im, d = canvas(Y)
FULL = (W * S, H * S)

def layer(bg):
    L = Image.new("RGB", FULL, bg); return L, ImageDraw.Draw(L)
def stamp(pat, pts=None, ellipse=None):
    m = Image.new("L", FULL, 0); md = ImageDraw.Draw(m)
    if pts: md.polygon(P(pts), fill=255)
    if ellipse: x, y, rx, ry = ellipse; md.ellipse([(x - rx) * S, (y - ry) * S, (x + rx) * S, (y + ry) * S], fill=255)
    im.paste(pat, (0, 0), m)

def flower(dd, x, y, r, col, eye=Y, n=5, rot=0):
    for k in range(n):
        a = rot + k * 2 * math.pi / n
        circ(dd, x + math.cos(a) * r * .62, y + math.sin(a) * r * .62, r * .48, fill=col)
    circ(dd, x, y, r * .34, fill=eye)
def leaf(dd, x, y, a, l, col=G):
    ca, sa = math.cos(a), math.sin(a)
    poly(dd, [(x, y), (x + ca * l * .5 - sa * l * .22, y + sa * l * .5 + ca * l * .22), (x + ca * l, y + sa * l),
              (x + ca * l * .5 + sa * l * .22, y + sa * l * .5 - ca * l * .22)], fill=col)

# ---------- the repeats ----------
wall, wd = layer(Y)                                     # wallpaper: half-drop sprigs
for gx in range(-1, 16):
    for gy in range(-1, 16):
        x = gx * 28; y = gy * 30 + (gx % 2) * 15
        line(wd, [(x, y + 9), (x + 3, y + 2), (x, y - 5)], G, 0.9)
        leaf(wd, x + 2, y + 5, -0.5, 8); leaf(wd, x + 1, y + 1, 3.6, 7)
        flower(wd, x, y - 7, 4.6, R, Wh, rot=gx + gy)
        circ(wd, x + 14, y - 2, 1.5, fill=Wh); circ(wd, x + 14, y + 13, 1.1, fill=R)
        circ(wd, x + 9, y + 15, 1.0, fill=Wh); circ(wd, x + 19, y + 15, 1.0, fill=Wh)
for x in range(0, W, 28):
    line(wd, [(x + 14, 0), (x + 14, H)], Wh, 0.4)

dress, dr = layer(B)                                    # dress: white spot, red bud
for gy in range(120):
    for gx in range(80):
        x = gx * 6 + (gy % 2) * 3; y = gy * 5
        if (gx + gy * 3) % 7 == 0: flower(dr, x, y, 2.2, R, Y, 4)
        else: circ(dr, x, y, 1.05, fill=Wh)

ging, gd = layer(Wh)                                    # gingham
for k in range(0, 700, 12):
    rect(gd, 0, k, W, k + 6, fill=None)
    for t in range(0, 6, 2): line(gd, [(0, k + t + .5), (W, k + t + .5)], R, 0.75)
for k in range(0, 420, 12):
    for t in range(0, 6, 2): line(gd, [(k + t + .5, 0), (k + t + .5, H)], R, 0.75)
for kx in range(0, 420, 12):
    for ky in range(0, 700, 12):
        rect(gd, kx, ky, kx + 6, ky + 6, fill=R)

rug, rd = layer(K)                                      # rug: lattice of lozenges
for gy in range(-2, 40):
    for gx in range(-2, 30):
        x = gx * 22 + (gy % 2) * 11; y = 380 + gy * 9
        poly(rd, [(x, y - 7), (x + 9, y), (x, y + 7), (x - 9, y)], fill=G if (gx + gy) % 3 else R)
        poly(rd, [(x, y - 3.5), (x + 4.5, y), (x, y + 3.5), (x - 4.5, y)], fill=Y if (gx * 2 + gy) % 4 else Wh)

curt, cd = layer(Wh)                                    # curtain: blue stripe + rosebud
for x in range(0, W, 9):
    line(cd, [(x + 1, 0), (x + 1, H)], B, 1.6); line(cd, [(x + 4, 0), (x + 4, H)], B, 0.5)
    for y in range((x // 9 % 2) * 8, H, 16):
        circ(cd, x + 6.2, y, 1.7, fill=R); leaf(cd, x + 6.2, y + 2, 1.2, 4)

chair, chd = layer(G)                                   # armchair: green, yellow sprig
for gy in range(120):
    for gx in range(60):
        x = gx * 8 + (gy % 2) * 4; y = gy * 7
        circ(chd, x, y, 1.5, fill=Y); line(chd, [(x - 3, y + 3.5), (x + 3, y + 3.5)], K, 0.5)

boards, bd = layer(Wh)                                  # floorboards
for k, x in enumerate(range(-200, 700, 17)):
    line(bd, [(x, 600), (200 + (x - 200) * .62, 400)], K, 0.6)
    for t in range(3):
        yy = random.uniform(410, 596); xx = 200 + (x - 200) * (.62 + .38 * (yy - 400) / 200)
        line(bd, [(xx + 4, yy), (xx + 9, yy + random.uniform(4, 12))], Y, 0.7)

# ---------- the room ----------
im.paste(wall)
FLOOR = 404
stamp(boards, [(0, FLOOR), (W, FLOOR), (W, H), (0, H)])
rect(d, 0, FLOOR - 9, W, FLOOR, fill=Wh, outline=K, w=0.7)            # skirting board
for x in range(0, W, 5): line(d, [(x, FLOOR - 6), (x + 3, FLOOR - 3)], K, 0.4)
rect(d, 0, 20, W, 27, fill=R); line(d, [(0, 20), (W, 20)], K, 0.6); line(d, [(0, 27), (W, 27)], K, 0.6)   # picture rail
for x in range(4, W, 10): circ(d, x, 23.5, 1.4, fill=Y)
stamp(rug, [(18, 446), (318, 430), (392, 588), (-30, 600)])
for a, b in [((18, 446), (318, 430)), ((318, 430), (392, 588)), ((18, 446), (-30, 600))]:
    line(d, [a, b], R, 3); line(d, [a, b], Y, 1)
for k in range(40):                                                   # rug fringe
    x = 18 + (318 - 18) * k / 39; y = 446 - 16 * k / 39
    line(d, [(x, y - 1), (x - 1, y - 6)], K, 0.6)

# window, left: November garden outside
wx0, wy0, wx1, wy1 = 34, 58, 150, 300
rect(d, wx0, wy0, wx1, wy1, fill=Wh)
rect(d, wx0, wy0, wx1, 170, fill=B)
for y in range(wy0 + 4, 170, 7):                                      # combed sky
    line(d, [(wx0, y), (wx1, y)], Wh, 0.5 + 1.6 * (y - wy0) / 112)
circ(d, 122, 88, 9, fill=Wh); circ(d, 122, 88, 6, fill=Y)             # low late-autumn sun
poly(d, [(wx0, 176), (62, 160), (96, 172), (128, 158), (wx1, 168), (wx1, wy1), (wx0, wy1)], fill=G)
for k in range(60):
    x, y = random.uniform(wx0, wx1), random.uniform(180, wy1); line(d, [(x, y), (x + 2, y - 4)], Y if k % 3 else K, 0.6)
for hx, hw, hh, c in [(40, 26, 30, R), (70, 20, 22, Wh), (118, 28, 26, Y)]:   # roofs across the garden wall
    rect(d, hx, 190 - hh, hx + hw, 190, fill=c, outline=K, w=0.6)
    poly(d, [(hx - 2, 190 - hh), (hx + hw / 2, 190 - hh - 10), (hx + hw + 2, 190 - hh)], fill=K)
    rect(d, hx + 5, 190 - hh + 7, hx + 9, 190 - hh + 13, fill=K); rect(d, hx + hw - 9, 190 - hh + 7, hx + hw - 5, 190 - hh + 13, fill=K)
rect(d, wx0, 190, wx1, 200, fill=R, outline=K, w=0.5)
for x in range(wx0, wx1, 8): line(d, [(x, 190), (x, 200)], K, 0.4)
def tree(x, y, a, l, wdt, depth):
    if depth == 0 or l < 3:
        if random.random() < .5: circ(d, x, y, 1.6, fill=random.choice([R, Y, Y]))
        return
    x2, y2 = x + math.cos(a) * l, y + math.sin(a) * l
    line(d, [(x, y), (x2, y2)], K, wdt)
    for da_ in (-0.5, 0.42, 0.05 if depth % 2 else None):
        if da_ is not None: tree(x2, y2, a + da_ + random.uniform(-.15, .15), l * .72, max(.5, wdt * .68), depth - 1)
tree(88, 262, -math.pi / 2 - .05, 44, 3.4, 6)
for k in range(26): circ(d, random.uniform(50, 132), random.uniform(262, 296), 1.5, fill=random.choice([R, Y, Y, K]))  # fallen leaves
# sashes
rect(d, wx0, wy0, wx1, wy1, outline=K, w=1.2)
for x in (wx0 + 58,): rect(d, x - 2.5, wy0, x + 2.5, wy1, fill=Wh, outline=K, w=0.6)
for y in (wy0 + 80, wy0 + 160): rect(d, wx0, y - 2, wx1, y + 2, fill=Wh, outline=K, w=0.6)
rect(d, wx0 - 7, wy0 - 7, wx1 + 7, wy0, fill=Wh, outline=K, w=0.8); rect(d, wx0 - 10, wy1, wx1 + 10, wy1 + 8, fill=Wh, outline=K, w=0.8)
rect(d, wx0 - 7, wy0, wx0, wy1, fill=Wh, outline=K, w=0.8); rect(d, wx1, wy0, wx1 + 7, wy1, fill=Wh, outline=K, w=0.8)
# curtains with tie-backs, and a pelmet
lc = [(14, 44)] + [(14 + (k % 2) * 3, 44 + k * 14) for k in range(1, 20)] + [(22, 330), (58, 330), (52, 250), (36, 214), (56, 150), (60, 44)]
rc = [(168, 44), (172, 330), (136, 330), (140, 250), (154, 214), (132, 150), (126, 44)]
stamp(curt, lc); stamp(curt, rc)
line(d, lc + [lc[0]], K, 0.8); line(d, rc + [rc[0]], K, 0.8)
for x in (44, 148): rect(d, x - 9, 208, x + 9, 216, fill=R, outline=K, w=0.6); circ(d, x, 222, 3.5, fill=Y, outline=K, w=0.5)
rect(d, 8, 34, 176, 48, fill=R, outline=K, w=0.9)
for x in range(12, 176, 8): poly(d, [(x, 48), (x + 4, 56), (x + 8, 48)], fill=Y, outline=K, w=0.5)
# geraniums on the sill
for px_ in (60, 84, 118):
    poly(d, [(px_ - 6, 286), (px_ + 6, 286), (px_ + 4, 299), (px_ - 4, 299)], fill=R, outline=K, w=0.6)
    for k in range(5):
        a = -math.pi / 2 + (k - 2) * .45; line(d, [(px_, 286), (px_ + math.cos(a) * 13, 286 + math.sin(a) * 13)], G, 1)
        flower(d, px_ + math.cos(a) * 14, 286 + math.sin(a) * 14, 3, Wh if px_ == 84 else R, Y)

# pictures on the wall: the little sailing picture (for Signac) and two silhouettes
def frame(x0, y0, x1, y1, c=K):
    rect(d, x0 - 4, y0 - 4, x1 + 4, y1 + 4, fill=c, outline=K, w=0.7); rect(d, x0, y0, x1, y1, fill=Wh, outline=K, w=0.5)
    line(d, [((x0 + x1) / 2, 27), ((x0 + x1) / 2, y0 - 4)], K, 0.4)
frame(212, 70, 276, 118, Y)
rect(d, 212, 70, 276, 94, fill=Wh); rect(d, 212, 96, 276, 118, fill=B)
for k in range(30): circ(d, random.uniform(213, 275), random.uniform(71, 94), 0.9, fill=random.choice([Y, R, B]))
for k in range(26): circ(d, random.uniform(213, 275), random.uniform(98, 117), 0.9, fill=random.choice([Wh, Y, G]))
poly(d, [(240, 100), (244, 76), (256, 100)], fill=R); poly(d, [(242, 100), (238, 82), (232, 100)], fill=Y)
poly(d, [(230, 101), (260, 101), (255, 106), (234, 106)], fill=K); circ(d, 266, 78, 3.2, fill=Y)
for fx in (302, 346):
    frame(fx, 78, fx + 26, 112, K); ell(d, fx + 13, 95, 10, 14, fill=Y, outline=K, w=0.5)
    circ(d, fx + 13, 91, 5, fill=K); poly(d, [(fx + 5, 108), (fx + 13, 96), (fx + 21, 108)], fill=K)
# hanging lamp over the table
lx = 292
line(d, [(lx, 27), (lx, 150)], K, 0.8)
for y in range(34, 150, 9): circ(d, lx, y, 1.3, outline=K, w=0.5)
poly(d, [(lx - 34, 196), (lx - 14, 150), (lx + 14, 150), (lx + 34, 196)], fill=G, outline=K, w=0.9)
for k in range(-3, 4): line(d, [(lx + k * 4, 152), (lx + k * 9.5, 195)], K, 0.4)
for x in range(lx - 34, lx + 35, 5): line(d, [(x, 196), (x, 203)], R, 0.9); circ(d, x, 204, 1.1, fill=Y)
ell(d, lx, 198, 9, 5, fill=Wh, outline=K, w=0.5)
# dresser at the right with crockery
dx0 = 330
rect(d, dx0, 240, W + 4, FLOOR - 2, fill=R, outline=K, w=1)
for y in (268, 310, 352): rect(d, dx0 + 5, y, W, y + 34, fill=K); rect(d, dx0 + 5, y + 30, W, y + 34, fill=Wh, outline=K, w=0.5)
for y, things in ((268, "ppp"), (310, "jcj"), (352, "bbb")):
    for k, t in enumerate(things):
        cx = dx0 + 18 + k * 21
        if t == "p": circ(d, cx, y + 16, 10, fill=Wh, outline=K, w=0.5); circ(d, cx, y + 16, 6.5, outline=B, w=1.2); flower(d, cx, y + 16, 3, B, Y)
        if t == "j": poly(d, [(cx - 6, y + 30), (cx - 7, y + 14), (cx - 3, y + 6), (cx + 3, y + 6), (cx + 7, y + 14), (cx + 6, y + 30)], fill=Y, outline=K, w=0.5); rect(d, cx - 6, y + 17, cx + 6, y + 21, fill=B)
        if t == "c": ell(d, cx, y + 23, 8, 7, fill=Wh, outline=K, w=0.5); rect(d, cx - 8, y + 15, cx + 8, y + 22, fill=K); ell(d, cx, y + 22, 8, 2.5, fill=B)
        if t == "b":
            for q, c in enumerate([G, Y, Wh, B]): rect(d, cx - 10 + q * 5, y + 6 + (q % 2) * 3, cx - 6 + q * 5, y + 30, fill=c, outline=K, w=0.4)
rect(d, dx0 - 4, 232, W + 4, 242, fill=Y, outline=K, w=0.8)
poly(d, [(346, 232), (343, 214), (350, 204), (360, 204), (367, 214), (364, 232)], fill=B, outline=K, w=0.6)   # ginger jar
for k in range(5): circ(d, 349 + k * 3, 218 + (k % 2) * 6, 1.3, fill=Wh)
rect(d, 378, 206, 396, 232, fill=Wh, outline=K, w=0.6); circ(d, 387, 219, 7, outline=K, w=0.6)           # clock
line(d, [(387, 219), (387, 213)], K, 0.8); line(d, [(387, 219), (387.6, 214)], R, 0.5)

# ---------- the table ----------
tcx, tcy, trx, try_ = 282, 392, 104, 30
skirt = [(tcx - trx, tcy)] + [(tcx - trx + 2 * trx * k / 16 + (4 if k % 2 else -3), 520 + 12 * math.sin(k * 1.3) + 26 * math.sin(math.pi * k / 16)) for k in range(17)] + [(tcx + trx, tcy)]
stamp(ging, skirt); line(d, skirt, K, 0.9)
for k in range(1, 16, 2):                                             # folds in the cloth
    x = tcx - trx + 2 * trx * k / 16
    line(d, [(x, tcy + 26 + 4 * (k % 3)), (x + (4 if k % 4 == 1 else -3), 512 + 22 * math.sin(math.pi * k / 16))], K, 0.5)
for x in (tcx - 60, tcx + 62): rect(d, x - 4, 520, x + 4, 572, fill=K); rect(d, x - 6, 572, x + 6, 578, fill=K)
stamp(ging, ellipse=(tcx, tcy, trx, try_)); ell(d, tcx, tcy, trx, try_, outline=K, w=1)
# vase of chrysanthemums
vx, vy = 300, 380
random.seed(11)
for k in range(11):
    a = -math.pi / 2 + (k - 5) * .23 + random.uniform(-.06, .06); l = random.uniform(52, 86)
    ex, ey = vx + math.cos(a) * l, vy - 26 + math.sin(a) * l
    line(d, [(vx, vy - 24), ((vx + ex) / 2 + 3, (vy - 24 + ey) / 2), (ex, ey)], G, 1.1)
    leaf(d, (vx + ex) / 2, (vy - 24 + ey) / 2, a + 1.1, 12); leaf(d, (vx * .3 + ex * .7), (vy - 24) * .3 + ey * .7, a - 1.2, 10)
    c = [Wh, R, Wh, Y, R, Wh][k % 6]; rr = random.uniform(9, 12.5)
    circ(d, ex, ey, rr, fill=c, outline=K, w=0.5)
    for q in range(16):
        aa = q * math.pi / 8; line(d, [(ex + math.cos(aa) * 2.5, ey + math.sin(aa) * 2.5), (ex + math.cos(aa + .3) * rr * .92, ey + math.sin(aa + .3) * rr * .92)], K, 0.45)
    circ(d, ex, ey, 2.4, fill=Y if c != Y else R)
poly(d, [(vx - 9, vy - 30), (vx + 9, vy - 30), (vx + 14, vy - 8), (vx + 9, vy + 8), (vx - 9, vy + 8), (vx - 14, vy - 8)], fill=B, outline=K, w=0.8)
for k in range(-2, 3): line(d, [(vx + k * 4, vy - 28), (vx + k * 5.5, vy - 8), (vx + k * 4, vy + 6)], Wh, 0.6)
rect(d, vx - 14, vy - 12, vx + 14, vy - 8, fill=Y)
# teapot, cup and saucer, sugar, a plate of three pears
tx, ty = 352, 388
ell(d, tx, ty, 17, 13, fill=Wh, outline=K, w=0.8); ell(d, tx, ty - 12, 8, 3, fill=B, outline=K, w=0.5); circ(d, tx, ty - 16, 2.2, fill=R)
line(d, [(tx - 16, ty - 2), (tx - 26, ty - 10), (tx - 28, ty - 14)], K, 2.4); line(d, [(tx - 16, ty - 2), (tx - 26, ty - 10)], Wh, 1.0)
d.arc([(tx + 12) * S, (ty - 9) * S, (tx + 28) * S, (ty + 7) * S], -80, 90, fill=K, width=5)
for k in range(-2, 3): flower(d, tx + k * 6.4, ty + 1 - abs(k) * .8, 2.6, B if k % 2 else R, Y)
for y_ in (-8, 8): line(d, [(tx - 15, ty + y_ * .8), (tx + 15, ty + y_ * .8)], B, 0.6)
ell(d, 236, 404, 14, 4.5, fill=Wh, outline=K, w=0.6); poly(d, [(228, 394), (244, 394), (242, 404), (230, 404)], fill=Wh, outline=K, w=0.6)
ell(d, 236, 394, 8, 2.4, fill=R, outline=K, w=0.5); line(d, [(229, 399), (243, 399)], B, 1)
ell(d, 318, 408, 22, 7, fill=Wh, outline=K, w=0.6); ell(d, 318, 408, 17, 5, outline=B, w=0.8)
for px_, c in ((308, Y), (318, G), (329, Y)):
    ell(d, px_, 402, 5.5, 6.5, fill=c, outline=K, w=0.5); circ(d, px_, 395.5, 3.2, fill=c, outline=K, w=0.5); line(d, [(px_, 392), (px_ + 2, 388)], K, 0.7)
    circ(d, px_ - 2, 401, 1, fill=R)

# ---------- the seamstress, in profile, bent to her work ----------
# chair first
line(d, [(128, 300), (122, 420), (116, 560)], K, 3); line(d, [(128, 300), (150, 296)], K, 3)
for k in range(1, 5): line(d, [(127 - k * .8, 300 + k * 26), (158, 300 + k * 26 + 2)], K, 1.2)
line(d, [(124, 438), (196, 440)], K, 3); line(d, [(194, 440), (200, 566)], K, 3)
body = [(150, 312), (166, 296), (190, 296), (212, 318), (226, 356), (252, 372), (250, 390), (224, 394),
        (238, 430), (262, 560), (130, 566), (128, 440), (140, 380)]
stamp(dress, body); line(d, body + [body[0]], K, 1)
hem = [(130, 552), (262, 546), (264, 562), (128, 568)]
poly(d, hem, fill=Wh, outline=K, w=0.6)
for k in range(22): poly(d, [(132 + k * 6, 556), (135 + k * 6, 562), (138 + k * 6, 556)], fill=R)
poly(d, [(250, 562), (262, 560), (276, 570), (272, 576), (250, 574)], fill=K)                       # shoe
poly(d, [(176, 330), (214, 322), (228, 362), (242, 432), (190, 444), (170, 384)], fill=Wh, outline=K, w=0.7)   # apron bib
for k in range(8): line(d, [(180 + k * 6, 332 - k * 1.2), (196 + k * 6, 442 - k * 1.5)], R, 0.5)
line(d, [(176, 330), (160, 306)], Wh, 2.2); line(d, [(214, 322), (196, 300)], Wh, 2.2)
arm = [(196, 318), (214, 322), (236, 366), (262, 378), (260, 390), (228, 386), (204, 352)]
stamp(dress, arm); line(d, arm + [arm[0]], K, 0.9)
poly(d, [(258, 377), (263, 379), (262, 391), (256, 390)], fill=Wh, outline=K, w=0.5)                # cuff
poly(d, [(262, 380), (276, 380), (282, 385), (274, 390), (262, 390)], fill=Wh, outline=K, w=0.7)    # hand
line(d, [(280, 384), (296, 372)], K, 0.6); line(d, [(296, 372), (286, 350), (300, 334), (316, 352)], R, 0.5)   # needle + thread
# the white work spilling off her lap
work = [(232, 388), (270, 392), (284, 404), (268, 420), (276, 452), (252, 470), (236, 440), (226, 410)]
poly(d, work, fill=Wh, outline=K, w=0.8)
for k in range(6): line(d, [(238 + k * 6, 394 + k), (242 + k * 5, 462 - k * 4)], B, 0.45)
for k in range(5): flower(d, 244 + k * 7, 410 + (k % 2) * 22, 2.4, R, Y)
# head: collar, face, hair in a bun, comb
poly(d, [(168, 296), (190, 290), (204, 300), (190, 306), (172, 306)], fill=Wh, outline=K, w=0.7)
for k in range(5): circ(d, 173 + k * 6.5, 305 - (1 if k in (1, 2, 3) else 0), 2, fill=Wh, outline=K, w=0.4)
face = [(184, 296), (180, 276), (184, 258), (198, 250), (212, 254), (218, 266), (222, 276), (217, 279), (218, 286), (213, 293), (200, 297)]
poly(d, face, fill=Wh, outline=K, w=0.9)
hair = [(180, 280), (172, 262), (178, 246), (194, 238), (212, 242), (218, 256), (206, 254), (194, 258), (190, 272), (186, 284)]
poly(d, hair, fill=K); circ(d, 170, 252, 11, fill=K); poly(d, [(160, 244), (166, 238), (170, 250)], fill=R)
line(d, [(207, 268), (213, 268)], K, 1.1); line(d, [(205, 263), (214, 262)], K, 0.7)
line(d, [(210, 286), (215, 285)], R, 1.2); circ(d, 204, 280, 2.6, fill=None, outline=R, w=0.5)
circ(d, 189, 275, 1.6, fill=Y, outline=K, w=0.4)                                                    # earring
# sewing basket on the floor, cotton reels, scissors
bx, by = 96, 556
poly(d, [(bx - 26, by - 20), (bx + 26, by - 20), (bx + 20, by + 12), (bx - 20, by + 12)], fill=Y, outline=K, w=0.9)
for k in range(-4, 5): line(d, [(bx + k * 6, by - 20), (bx + k * 4.6, by + 12)], K, 0.5)
for y in range(-14, 12, 6): line(d, [(bx - 25 + (y + 14) * .2, by + y), (bx + 25 - (y + 14) * .2, by + y)], R, 0.6)
for k, c in enumerate([R, B, Wh, G]):
    circ(d, bx - 16 + k * 11, by - 24, 5.5, fill=c, outline=K, w=0.5); circ(d, bx - 16 + k * 11, by - 24, 1.5, fill=K)
line(d, [(bx + 6, by - 24), (bx + 40, by - 10), (bx + 30, by + 14), (bx + 62, by + 22)], G, 0.6)
circ(d, 150, 584, 4, outline=K, w=1); circ(d, 158, 588, 4, outline=K, w=1); line(d, [(153, 581), (178, 572)], K, 1); line(d, [(160, 585), (178, 572)], K, 1)
# the cat on the patterned armchair, lower right
ch = [(312, 480), (322, 440), (356, 428), (W + 4, 432), (W + 4, H), (318, H)]
stamp(chair, ch); line(d, ch, K, 1.1)
arm_ = [(306, 512), (326, 500), (350, 508), (352, H), (310, H)]
stamp(chair, arm_); line(d, arm_, K, 1.1)
ell(d, 372, 528, 26, 15, fill=K); circ(d, 352, 518, 10, fill=K)
poly(d, [(344, 512), (345, 502), (351, 509)], fill=K); poly(d, [(354, 508), (359, 500), (361, 511)], fill=K)
line(d, [(396, 532), (392, 546), (368, 547), (352, 542)], K, 3.2)
line(d, [(347, 519), (351, 520)], Y, 1); line(d, [(354, 520), (358, 519)], Y, 1); circ(d, 352.5, 523, 0.9, fill=R)
for k in range(5): line(d, [(362 + k * 7, 518 + (k % 2)), (364 + k * 7, 538)], Wh, 0.5)
save(im)
