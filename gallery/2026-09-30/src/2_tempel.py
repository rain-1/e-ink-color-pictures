"""2 · Midday — O Isis und Osiris. Sarastro's Temple of Wisdom as a painted hypostyle hall
in one-point perspective: banded papyrus columns covered in glyphs, a blue ceiling of
yellow stars, the winged sun over the far gate, noon light throwing the column shadows
toward us. Two tiny figures walk in."""
import math, random
import numpy as np
from common import *

random.seed(11)
c = Canvas(Y)
VX, VY = 200, 318
FLOOR, CEIL = 262, -262
def P(X, Y_, z): return (VX + X / z, VY + Y_ / z)

# ceiling: blue, star grid in perspective; floor: pale stone with joints
c.poly([(0, 0), (W, 0), P(200, CEIL, 9.5), P(-200, CEIL, 9.5)], fill=B)
for zi in np.arange(1.0, 9.5, 0.42):
    for xi in np.arange(-150, 151, 30):
        x, y = P(xi, CEIL, zi)
        if 0 < y < VY: c.star(x, y, 5.5 / zi ** 0.8, Y, 5, 0.42)
c.poly([(0, H), (W, H), P(200, FLOOR, 9.5), P(-200, FLOOR, 9.5)], fill=Wh)
for xi in np.arange(-300, 301, 40):
    c.line([P(xi, FLOOR, 0.45), P(xi, FLOOR, 9.5)], K, 0.6)
for zi in [0.5 * 1.18 ** k for k in range(20)]:
    if zi < 9.5: c.line([P(-400, FLOOR, zi), P(400, FLOOR, zi)], K, 0.6)
# central red runner with a key pattern
c.poly([P(-38, FLOOR, 0.45), P(38, FLOOR, 0.45), P(38, FLOOR, 9.5), P(-38, FLOOR, 9.5)], fill=R)
for zi in [0.5 * 1.13 ** k for k in range(30)]:
    if zi < 9.4:
        a, b = P(-30, FLOOR, zi), P(30, FLOOR, zi)
        c.line([a, b], Y, max(0.5, 1.6 / zi))

# far wall: pylon gate with the winged sun
ZW = 9.5
wl, wt = P(-200, CEIL, ZW), P(200, FLOOR, ZW)
c.rect(wl[0], wl[1], wt[0], wt[1], fill=Y, outline=K, width=0.8)
for k in range(8):
    y = wl[1] + k * (wt[1] - wl[1]) / 8
    c.line([(wl[0], y), (wt[0], y)], R if k % 2 else B, 0.8)
dl, dt = P(-34, FLOOR - 190, ZW), P(34, FLOOR, ZW)
c.rect(dl[0] - 3, dl[1] - 3, dt[0] + 3, dt[1], fill=K)
c.rect(dl[0], dl[1], dt[0], dt[1], fill=Wh)
sx, sy = (dl[0] + dt[0]) / 2, dl[1] + 7
c.ell(sx, sy - 12, 4.2, fill=R, outline=K, width=0.5)
for side in (-1, 1):
    for k in range(4):
        c.poly([(sx + side * 4, sy - 13 + k), (sx + side * (26 - k * 4), sy - 16 + k * 2.5), (sx + side * (24 - k * 4), sy - 12 + k * 2.5), (sx + side * 4, sy - 10 + k)],
               fill=[B, G, B, G][k])
for k in range(12):   # light spilling from the door
    a = -math.pi / 2 + (k - 5.5) * 0.12
    c.line([(sx, dl[1] + 20), (sx + 30 * math.cos(a + math.pi), dt[1])], Y, 0.5)

# columns, far to near
GLY = []
def glyph(x, y, s, kind, col=K):
    if kind == 0: c.ell(x, y, 2.2 * s, outline=col, width=0.5); c.ell(x, y, .6 * s, fill=col)          # sun
    elif kind == 1: c.line([(x - 3 * s, y), (x - 1.5 * s, y - 1.2 * s), (x, y), (x + 1.5 * s, y - 1.2 * s), (x + 3 * s, y)], col, 0.6)  # water
    elif kind == 2:                                                                                     # ankh
        c.ell(x, y - 1.8 * s, 1.1 * s, 1.4 * s, outline=col, width=0.5); c.line([(x, y - .4 * s), (x, y + 3 * s)], col, 0.6); c.line([(x - 1.6 * s, y + .4 * s), (x + 1.6 * s, y + .4 * s)], col, 0.6)
    elif kind == 3:                                                                                     # bird
        c.ell(x, y, 1.6 * s, 1.1 * s, fill=col); c.ell(x + 1.4 * s, y - 1.6 * s, .8 * s, fill=col); c.line([(x - 1 * s, y + 1 * s), (x - 1 * s, y + 2.6 * s)], col, 0.5)
    elif kind == 4:                                                                                     # eye
        c.ell(x, y, 2.4 * s, 1 * s, outline=col, width=0.5); c.ell(x, y, .6 * s, fill=col); c.line([(x - .6 * s, y + 1 * s), (x - 1.4 * s, y + 2.6 * s)], col, 0.5)
    elif kind == 5: c.rect(x - 2 * s, y - .6 * s, x + 2 * s, y + .6 * s, fill=col)                       # bar
    elif kind == 6: c.line([(x, y + 2.4 * s), (x, y - 2.4 * s), (x + 1.4 * s, y - 1.2 * s)], col, 0.6)  # reed
    else: c.poly([(x - 2 * s, y + 1.5 * s), (x, y - 2 * s), (x + 2 * s, y + 1.5 * s)], outline=col, width=0.5)  # hill

XC, RC = 118, 30
zs = [1.0 * 1.45 ** k for k in range(7)][::-1]
cap_y, shaft_top = CEIL + 64, CEIL + 104
for z in zs:
    for side in (-1, 1):
        X = side * XC
        # cast shadow on the floor, toward us (sun is beyond the gate)
        f0, f1 = P(X - RC, FLOOR, z), P(X + RC, FLOOR, z)
        g0, g1 = P(X - RC * 1.3 + side * 16, FLOOR, max(z * 0.62, 0.4)), P(X + RC * 1.3 + side * 16, FLOOR, max(z * 0.62, 0.4))
        c.poly([f0, f1, g1, g0], fill=K)
        x0, top = P(X - RC, shaft_top, z); x1, bot = P(X + RC, FLOOR, z)
        wz = x1 - x0
        # base drum
        c.poly(oval((x0 + x1) / 2, bot, wz * .6, wz * .1), fill=Y, outline=K, width=.6)
        c.rect(x0, top, x1, bot, fill=Y)
        # shading on the side away from the aisle: hatched
        lit_left = side > 0
        n = max(3, int(wz / 2.4))
        for k in range(n):
            t = k / (n - 1)
            shade = t if not lit_left else 1 - t
            if shade > 0.55:
                xx = x0 + t * wz
                c.line([(xx, top), (xx, bot)], K, 0.5 + 1.3 * (shade - .55) / .45)
        # painted bands around the shaft
        hband = [(FLOOR - 30, R), (FLOOR - 42, B), (shaft_top + 70, G), (shaft_top + 56, R), (shaft_top + 16, B)]
        for yw, col in hband:
            _, yb = P(0, yw, z)
            hh = 9 / z
            c.rect(x0, yb, x1, yb + hh, fill=col)
            c.line([(x0, yb), (x1, yb)], K, .5); c.line([(x0, yb + hh), (x1, yb + hh)], K, .5)
            if col == G and wz > 14:
                zz = [(x0 + i * wz / 10, yb + (0 if i % 2 else hh)) for i in range(11)]
                c.line(zz, Y, .6)
        # glyph panel down the middle
        if wz > 12:
            _, gy0 = P(0, shaft_top + 88, z); _, gy1 = P(0, FLOOR - 52, z)
            mx = (x0 + x1) / 2; gw = wz * 0.28
            c.rect(mx - gw, gy0, mx + gw, gy1, fill=Wh, outline=K, width=.6)
            gs = gw / 3.2
            yg = gy0 + gs * 3
            while yg < gy1 - gs * 2.5:
                glyph(mx, yg, gs, random.randrange(8), K if random.random() < .8 else R)
                yg += gs * 6
        # papyrus capital: flaring bell with ribs
        _, cy0 = P(0, cap_y, z); _, cy1 = P(0, shaft_top, z)
        mx = (x0 + x1) / 2; flare = wz * 0.95
        bell = [(x0, cy1), (x1, cy1), (mx + flare, cy0), (mx - flare, cy0)]
        c.poly(bell, fill=G, outline=K, width=.7)
        for k in range(-4, 5):
            c.line([(mx + k * wz / 9, cy1), (mx + k * flare / 4.5, cy0)], Y if k % 2 else K, .6)
        c.rect(mx - flare, cy0 - 4 / z * 2, mx + flare, cy0, fill=B, outline=K, width=.5)
        # abacus + architrave to the ceiling
        _, ay = P(0, CEIL, z)
        c.rect(mx - wz * .6, ay, mx + wz * .6, cy0 - 8 / z, fill=Y, outline=K, width=.6)
# architraves along each side, with glyph friezes
for side in (-1, 1):
    X = side * XC
    a0, a1 = P(X - side * 30, CEIL, 0.9), P(X - side * 30, CEIL, 9.5)
    b0, b1 = P(X - side * 30, CEIL + 40, 0.9), P(X - side * 30, CEIL + 40, 9.5)
# cross beams at the nearest two column pairs
for z in zs[-3:]:
    l, t = P(-XC, CEIL, z); r_, b_ = P(XC, CEIL + 38, z)
    c.rect(l, t, r_, b_, fill=Y, outline=K, width=.8)
    hh = b_ - t
    c.rect(l, t + hh * .15, r_, t + hh * .3, fill=R)
    c.rect(l, t + hh * .7, r_, t + hh * .85, fill=B)
    mx = VX
    c.ell(mx, t + hh * .5, hh * .16, fill=R, outline=K, width=.5)
    for sd in (-1, 1):
        for k in range(3):
            c.poly([(mx + sd * hh * .16, t + hh * (.42 + k * .06)), (mx + sd * hh * (1.6 - k * .35), t + hh * (.38 + k * .09)), (mx + sd * hh * .16, t + hh * (.5 + k * .06))], fill=[B, G, B][k])
    n = int((r_ - l) / 14)
    for i in range(n):
        xg = l + 7 + i * (r_ - l - 14) / max(1, n - 1)
        if abs(xg - mx) > hh * 1.7: glyph(xg, t + hh * .56, hh * .11, (i * 3 + int(z)) % 8)

# two tiny travellers on the runner, heading for the light
for fx, fs, col in ((191, 1.0, R), (208, 0.9, G)):
    fy = 452
    c.ell(fx, fy - 20 * fs, 2.8 * fs, fill=K)
    c.poly([(fx - 3.4 * fs, fy - 17 * fs), (fx + 3.4 * fs, fy - 17 * fs), (fx + 4.4 * fs, fy), (fx - 4.4 * fs, fy)], fill=col if col != R else B, outline=K, width=.6)
    c.line([(fx - 2 * fs, fy), (fx - 3 * fs, fy + 6 * fs)], K, 1); c.line([(fx + 2 * fs, fy), (fx + 3 * fs, fy + 6 * fs)], K, 1)
c.line([(208 + 3.5, 440), (212, 430)], K, 0.8); c.ell(212.5, 428, 3, 2.2, fill=Y, outline=K, width=.4)   # Papageno's cage
c.rect(88, 570, 312, 596, fill=K)
c.rect(91, 573, 309, 593, fill=Y)
c.ell(91, 583, 4, fill=K); c.ell(309, 583, 4, fill=K)
c.text((200, 583), "O ISIS UND OSIRIS", K, 11, "mm", bold=True, spacing=2)
c.finish()
