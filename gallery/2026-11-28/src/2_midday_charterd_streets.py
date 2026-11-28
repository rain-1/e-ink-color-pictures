"""Midday — London ("I wander thro' each charter'd street").
An invented engraved plan of Blake's London: recursive-subdivision streets, the Thames,
garden squares, bridges, boats, compass rose, and a red star on Broad Street, Soho."""
import math, sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from common import *

rng = np.random.default_rng(28)
a = Art(PALE)
c = a.c

# ---- the Thames: up from the south, bending east at Charing Cross
riv = bez((118, 640), (88, 470), (160, 392), (420, 412), 160)
RV = np.array(riv)
tan = np.gradient(RV, axis=0)
def rw(i):                      # river width grows downstream
    return 30 + 14 * i / len(riv)
def rdist(x, y):
    d = np.hypot(RV[:, 0] - x, RV[:, 1] - y); i = int(d.argmin())
    side = tan[i, 0] * (y - RV[i, 1]) - tan[i, 1] * (x - RV[i, 0])   # <0: north/west bank
    return d[i] - rw(i) / 2, (-1 if side < 0 else 1), i

n_urb = fbm(4, 70, 3)
def urban(x, y):
    d, side, _ = rdist(x, y)
    nz = n_urb[int(min(H - 1, max(0, y))), int(min(W - 1, max(0, x)))]
    if side < 0:
        return math.hypot((x - 215) / 1.0, (y - 285) / 1.25) < 165 + nz * 90
    return d < 26 + nz * 70 and y < 560

def area(q):
    return .5 * abs(sum(q[i][0] * q[(i + 1) % 4][1] - q[(i + 1) % 4][0] * q[i][1] for i in range(4)))
def cen(q):
    return (sum(p[0] for p in q) / 4, sum(p[1] for p in q) / 4)
def lerp(p, q, t):
    return (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)
def inset(q, d):
    cx, cy = cen(q); out = []
    for x, y in q:
        L = math.hypot(x - cx, y - cy) or 1
        k = max(0, (L - d * 1.35)) / L
        out.append((cx + (x - cx) * k, cy + (y - cy) * k))
    return out

blocks, fields, mains = [], [], []
def split(q, depth):
    cx, cy = cen(q); A = area(q); u = urban(cx, cy)
    dc = math.hypot(cx - 250, cy - 330)
    target = (60 + dc * .55) if u else 2600
    if A < target or depth > 11:
        (blocks if u else fields).append((q, depth)); return
    e = [math.dist(q[i], q[(i + 1) % 4]) for i in range(4)]
    k = 0 if e[0] + e[2] > e[1] + e[3] else 1
    q = q[k:] + q[:k]
    t1, t2 = rng.uniform(.36, .64), rng.uniform(.36, .64)
    m1, m2 = lerp(q[0], q[1], t1), lerp(q[3], q[2], t2)
    if depth <= 3:
        mains.append((m1, m2, depth))
    split([q[0], m1, m2, q[3]], depth + 1); split([m1, q[1], q[2], m2], depth + 1)
split([(-20, -10), (430, -30), (420, 640), (-10, 620)], 0)

# ---- fields first (colour layer), with hedges, furrows and trees in ink
fk = a.ink(G); ft = a.ink(G)
FCOL = [mix(G, WH, .55), mix(Y, G, .3), CREAM, mix(G, Y, .25), mix(WH, G, .25), mix(Y, WH, .45)]
for q, dp in fields:
    cx, cy = cen(q)
    if rdist(cx, cy)[0] < 2: continue
    col = FCOL[int(rng.integers(len(FCOL)))]
    poly(c, q, col)
    poly(fk, q, 0, 255, 1.0)
    kind = rng.integers(3)
    if kind == 0:      # furrows
        for t in np.arange(.12, .95, .11):
            line(fk, [lerp(lerp(q[0], q[1], t), cen(q), .08), lerp(lerp(q[3], q[2], t), cen(q), .08)], w=.7)
    elif kind == 1:    # orchard
        for s in np.arange(.2, .9, .22):
            for t in np.arange(.2, .9, .22):
                p = lerp(lerp(q[0], q[1], s), lerp(q[3], q[2], s), t)
                disc(ft, p[0], p[1], 1.7)

# ---- river
rk = a.ink(K); rb = a.ink(B); rwv = a.ink(WH)
for i in range(len(riv) - 1):
    line(rk, riv[i:i + 2], w=rw(i) + 2.6)
for i in range(len(riv)):
    disc(rk, riv[i][0], riv[i][1], rw(i) / 2 + 1.3)
for i in range(len(riv) - 1):
    line(rb, riv[i:i + 2], w=rw(i))
for i in range(len(riv)):
    disc(rb, riv[i][0], riv[i][1], rw(i) / 2)
for off in (-.36, -.18, 0, .18, .36):          # engraved current lines, broken
    seg = []
    for i in range(len(riv)):
        nx, ny = -tan[i, 1], tan[i, 0]; L = math.hypot(nx, ny)
        seg.append((riv[i][0] + nx / L * off * rw(i), riv[i][1] + ny / L * off * rw(i)))
    ph = int(rng.integers(9))
    for s in range(ph, len(seg) - 6, 9):
        line(rwv, seg[s:s + 6], w=.8)

# ---- city blocks
bk = a.ink(K); bw = a.ink(WH); bg = a.ink(G)
ROOF = [R, R, R, mix(R, K, .3), mix(R, WH, .3), mix(R, Y, .35), R]
squares = []
for q, dp in blocks:
    cx, cy = cen(q); d, side, _ = rdist(cx, cy)
    if min(rdist(x, y)[0] for x, y in q + [(cx, cy)]) < 2.5: continue
    qi = inset(q, 1.25)
    A = area(qi)
    if A < 14: continue
    if A > 70 and rng.random() < .035 and d > 20:       # a garden square
        poly(c, qi, mix(G, WH, .2)); poly(bk, qi, 0, 255, .9)
        ell(bg, cx, cy, math.sqrt(A) * .2, math.sqrt(A) * .2, None, 255, 1.0)
        for p in qi:
            pp = lerp(p, (cx, cy), .28); disc(bg, pp[0], pp[1], 1.6)
        squares.append((cx, cy)); continue
    poly(c, qi, ROOF[int(rng.integers(len(ROOF)))])
    poly(bk, qi, 0, 255, .9)
    if A > 95 and rng.random() < .5:                    # courtyard
        ci = inset(qi, 3.0)
        if area(ci) > 10:
            poly(bw, ci); poly(bk, ci, 0, 255, .7)
            if area(ci) > 60: disc(bg, cx, cy, 1.6)
    elif A > 30:                                        # ridge line
        line(bk, [lerp(lerp(qi[0], qi[3], .5), (cx, cy), .2), lerp(lerp(qi[1], qi[2], .5), (cx, cy), .2)], w=.7)

# main thoroughfares, kept open in paper white (only on the land)
mw = a.ink(WH)
for m1, m2, dp in mains:
    pts = [lerp(m1, m2, t) for t in np.linspace(0, 1, 80)]
    run = []
    for p in pts + [None]:
        ok = p is not None and rdist(*p)[0] > 3 and urban(*p)
        if ok: run.append(p)
        else:
            if len(run) > 1: line(mw, run, w=4.2 - dp * .6)
            run = []

# ---- bridges
def bridge(i, piers):
    nx, ny = -tan[i, 1], tan[i, 0]; L = math.hypot(nx, ny); nx, ny = nx / L, ny / L
    h = rw(i) / 2 + 5
    p, q = (riv[i][0] - nx * h, riv[i][1] - ny * h), (riv[i][0] + nx * h, riv[i][1] + ny * h)
    k1 = a.ink(K); w1 = a.ink(WH); k2 = a.ink(K)
    line(k1, [p, q], w=6.4); line(w1, [p, q], w=4.2)
    for t in np.linspace(.2, .8, piers):
        m = lerp(p, q, t); disc(k2, m[0], m[1], 1.5)
for i, n in ((22, 5), (86, 5), (128, 6)):
    bridge(i, n)

# ---- boats and barges
bt = a.ink(K); sail = a.ink(WH)
for i in (8, 36, 50, 66, 74, 100, 112, 140, 150, 156):
    nx, ny = -tan[i, 1], tan[i, 0]; L = math.hypot(nx, ny); o = rng.uniform(-.28, .28) * rw(i)
    x, y = riv[i][0] + nx / L * o, riv[i][1] + ny / L * o
    ang = math.atan2(tan[i, 1], tan[i, 0])
    poly(bt, leaf(x - 5 * math.cos(ang), y - 5 * math.sin(ang), ang, 10, 2.4, 6))
    if i % 2 == 0:
        poly(sail, [(x, y - 1), (x, y - 9), (x + 5, y - 2)]); line(bt, [(x, y), (x, y - 10)], w=.8)

# ---- landmarks
# St Paul's: dome seen in plan
px, py = 292, 352
lw = a.ink(WH); lk = a.ink(K); ly = a.ink(Y)
disc(lw, px, py, 13); poly(lw, [(px - 22, py - 5), (px + 16, py - 5), (px + 16, py + 5), (px - 22, py + 5)])
poly(lk, [(px - 21, py - 4), (px + 15, py - 4), (px + 15, py + 4), (px - 21, py + 4)], 0, 255, 1)
poly(lk, [(px - 4, py - 12), (px + 4, py - 12), (px + 4, py + 12), (px - 4, py + 12)], 0, 255, 1)
disc(lk, px, py, 8.5); disc(ly, px, py, 6.8); lk = a.ink(K); disc(lk, px, py, 2.2)
for k in range(8):
    th = k * math.pi / 4
    line(lk, [(px + 2 * math.cos(th), py + 2 * math.sin(th)), (px + 7 * math.cos(th), py + 7 * math.sin(th))], w=.7)
# churches: small black crosses on white dots
lk = a.ink(K); cw_ = a.ink(WH)
for (x, y) in ((70, 300), (176, 250), (236, 204), (340, 300), (150, 160), (300, 250), (96, 420), (236, 470), (350, 462)):
    if rdist(x, y)[0] > 8:
        disc(lk, x, y, 6.2); disc(cw_, x, y, 5)
        pass
lk = a.ink(K)
for (x, y) in ((70, 300), (176, 250), (236, 204), (340, 300), (150, 160), (300, 250), (96, 420), (236, 470), (350, 462)):
    if rdist(x, y)[0] > 8:
        line(lk, [(x, y - 3.6), (x, y + 3.6)], w=1.4); line(lk, [(x - 2.6, y - 1), (x + 2.6, y - 1)], w=1.4)

# ---- labels on paper slips
def label(x, y, s, f, pad=3, col=K):
    t = a.ink(WH); k = a.ink(col)
    bb = k.textbbox((x * S, y * S), s, font=f, anchor="mm")
    t.rectangle([bb[0] - pad * S, bb[1] - pad * S, bb[2] + pad * S, bb[3] + pad * S], fill=255)
    k.rectangle([bb[0] - pad * S, bb[1] - pad * S, bb[2] + pad * S, bb[3] + pad * S], outline=255, width=int(.8 * S))
    text(k, (x, y), s, f)
label(205, 132, "S O H O", font(11, "Bold"))
label(318, 300, "THE CITY", font(11, "Bold"))
label(272, 492, "SOUTHWARK", font(11, "Bold"))
label(46, 372, "WESTMINSTER", font(9.5, "Bold"), 2)
# Thames lettering down the current
tl = a.ink(WH)
for ch, i in zip("THAMES", (92, 100, 108, 116, 124, 132)):
    text(tl, (riv[i][0] + 0, riv[i][1] - 20 + 0), "", font(12, "BoldItalic"))
for ch, i in zip("THAMES", (96, 104, 111, 118, 126, 133)):
    text(tl, riv[i], ch, font(13, "BoldItalic"))

# Broad Street: the star
sx, sy = 122, 196
sw = a.ink(WH); sk = a.ink(K); sr = a.ink(R)
disc(sw, sx, sy, 13); disc(sk, sx, sy, 13, None, 255, 1.2)
star = [(sx + (10.5 if k % 2 == 0 else 4.3) * math.sin(k * math.pi / 5), sy - (10.5 if k % 2 == 0 else 4.3) * math.cos(k * math.pi / 5)) for k in range(10)]
poly(sr, star); poly(sk, star, 0, 255, .8)
label(122, 221, "28 Broad Street", font(11, "Italic"), 2)

# ---- compass rose (the day's orb)
ox, oy, r = 348, 62, 34
cw = a.ink(WH); ck = a.ink(K); cy_ = a.ink(Y); cr = a.ink(R); ck2 = a.ink(K)
disc(cw, ox, oy, r + 5); disc(ck, ox, oy, r + 5, None, 255, 1.2); disc(ck, ox, oy, r - 3, None, 255, .8)
for k in range(32):
    th = k * math.pi / 16
    line(ck, [(ox + (r - 3) * math.cos(th), oy + (r - 3) * math.sin(th)), (ox + (r + 1) * math.cos(th), oy + (r + 1) * math.sin(th))], w=.7)
for k, (L, col) in enumerate([(r - 10, cy_)] * 4):
    th = math.pi / 4 + k * math.pi / 2
    pts = [(ox + L * math.cos(th), oy + L * math.sin(th)), (ox + 5 * math.cos(th + 1.57), oy + 5 * math.sin(th + 1.57)), (ox - 5 * math.cos(th + 1.57), oy - 5 * math.sin(th + 1.57))]
    poly(col, pts); poly(ck, pts, 0, 255, .7)
for k in range(4):
    th = k * math.pi / 2 - math.pi / 2; L = r - 4
    tip = (ox + L * math.cos(th), oy + L * math.sin(th))
    l_ = (ox + 6 * math.cos(th + math.pi / 4 * 1), oy + 6 * math.sin(th + math.pi / 4))
    r_ = (ox + 6 * math.cos(th - math.pi / 4), oy + 6 * math.sin(th - math.pi / 4))
    poly(cr, [tip, l_, (ox, oy)]); poly(ck2, [tip, r_, (ox, oy)]); poly(ck2, [tip, l_, (ox, oy)], 0, 255, .7)
text(ck2, (ox, oy - r - 12), "N", font(11, "Bold"))

# ---- cartouche
x0, y0, x1, y1 = 108, 536, 388, 590
kw = a.ink(WH); kk = a.ink(K); kr = a.ink(R)
kw.rectangle([x0 * S, y0 * S, x1 * S, y1 * S], fill=255)
kk.rectangle([x0 * S, y0 * S, x1 * S, y1 * S], outline=255, width=int(1.6 * S))
kk.rectangle([(x0 + 3) * S, (y0 + 3) * S, (x1 - 3) * S, (y1 - 3) * S], outline=255, width=int(.7 * S))
text(kr, ((x0 + x1) / 2, y0 + 17), "L O N D O N", font(19, "Bold"))
text(kk, ((x0 + x1) / 2, y0 + 35), "I wander thro' each charter'd street,", font(11.5))
text(kk, ((x0 + x1) / 2, y0 + 47), "near where the charter'd Thames does flow", font(11.5))
border(a, K, 4, 1.6, 3)
a.finish()
