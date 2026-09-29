"""Afternoon — 'Michaelmas Daisies'. A millefleur of asters in the late-September sun,
the last big nectar of the year: red admirals, bumblebees, a hoverfly. Blue in charge."""
import math, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from ink import *

cv = Canvas(bg=mix(K, G, 0.3), seed=3)
rng = cv.rng

# ---------- ground: tangle of stems and lance leaves ----------
for _ in range(700):
    x = rng.uniform(-10, W + 10); y = rng.uniform(-10, H + 10)
    a = -math.pi / 2 + rng.uniform(-0.9, 0.9)
    l = rng.uniform(12, 30); w = rng.uniform(2.5, 5)
    col = rng.choice([mix(K, G, 0.5), mix(K, G, 0.65), G, mix(G, Y, 0.25), K])
    tip = (x + l * math.cos(a), y + l * math.sin(a))
    nx, ny = -math.sin(a), math.cos(a)
    mid = (x + l * 0.45 * math.cos(a), y + l * 0.45 * math.sin(a))
    cv.poly([(x, y), (mid[0] + nx * w, mid[1] + ny * w), tip, (mid[0] - nx * w, mid[1] - ny * w)], col)
    if col == G and l > 20:
        cv.line([(x, y), tip], mix(G, Y, 0.5), 0.6)

# ---------- asters ----------
PET = [B, B, B, mix(B, WH, 0.35), mix(B, R, 0.35), mix(B, WH, 0.6), WH]

def aster(x, y, r, col, tilt=1.0, rot=0.0):
    n = int(13 + r * 0.55)
    for layer in ((0,) if r < 12 else (1, 0)):
        for k in range(n):
            a = rot + (k + 0.5 * layer) * math.tau / n
            rr = r * (1.0 if layer == 0 else 0.82)
            w = max(0.8, r * 0.075)
            ca, sa = math.cos(a), math.sin(a) * tilt
            nx, ny = -math.sin(a) * tilt, math.cos(a)
            base = (x + ca * r * 0.25, y + sa * r * 0.25)
            tip = (x + ca * rr, y + sa * rr)
            m = (x + ca * rr * 0.62, y + sa * rr * 0.62)
            c = col if layer == 0 else mix(K, B, 0.5)
            cv.poly([base, (m[0] + nx * w, m[1] + ny * w * tilt), tip, (m[0] - nx * w, m[1] - ny * w * tilt)], c)
    # disc: yellow with red-ringed florets
    cr = r * 0.3
    cv.ellipse(x, y, cr, cr * tilt, Y)
    cv.ellipse(x, y, cr, cr * tilt, None, outline=mix(Y, R, 0.5), width=0.6)
    if r > 9:
        for k in range(int(r * 0.9)):
            a = k * 2.39996
            d = cr * 0.8 * math.sqrt((k + 0.5) / (r * 0.9))
            cv.circle(x + d * math.cos(a), y + d * math.sin(a) * tilt, 0.7, mix(Y, R, 0.6))

def bud(x, y, r):
    cv.ellipse(x, y, r, r * 1.2, mix(G, K, 0.2))
    for k in range(4):
        cv.line([(x - r + k * r * 0.6, y + r), (x - r * 0.3 + k * r * 0.4, y - r * 0.9)], mix(G, Y, 0.4), 0.6)
    cv.ellipse(x, y - r * 0.9, r * 0.5, r * 0.35, mix(B, R, 0.4))

# place flowers with rejection so they tile the page
flowers = []
tries = 0
while len(flowers) < 150 and tries < 20000:
    tries += 1
    r = rng.choice([rng.uniform(7, 11), rng.uniform(10, 16), rng.uniform(14, 22)])
    x = rng.uniform(-10, W + 10); y = rng.uniform(-10, H + 10)
    if all(math.hypot(x - fx, y - fy) > (r + fr) * 0.72 for fx, fy, fr in flowers):
        flowers.append((x, y, r))
# stems first
for x, y, r in flowers:
    cv.line([(x, y), (x + rng.uniform(-8, 8), y + r * 2.5)], mix(G, R, 0.35), 1.0)
for _ in range(60):
    bud(rng.uniform(0, W), rng.uniform(0, H), rng.uniform(2.5, 4))
flowers.sort(key=lambda f: f[2])
for x, y, r in flowers:
    aster(x, y, r, rng.choices(PET, [5, 3, 3, 3, 3, 2, 1])[0], tilt=rng.uniform(0.75, 1.0), rot=rng.uniform(0, 1))

# ---------- red admiral ----------
def admiral(cx, cy, s, ang):
    ca, sa = math.cos(ang), math.sin(ang)
    def T(pts):
        return [(cx + (px * ca - py * sa) * s, cy + (px * sa + py * ca) * s) for px, py in pts]
    for side in (1, -1):
        fw = [(0, -4), (side * 10, -26), (side * 30, -44), (side * 50, -46), (side * 56, -38), (side * 50, -26), (side * 46, -14), (side * 28, -4), (side * 4, 2)]
        hw = [(side * 2, 0), (side * 22, -4), (side * 33, 4), (side * 36, 16), (side * 31, 27), (side * 18, 31), (side * 6, 24), (0, 10)]
        cv.poly(T(hw), K)
        # hindwing red border with black dots and a blue eye
        band = [(side * 12, 27), (side * 26, 24), (side * 32, 12), (side * 36, 16), (side * 31, 27), (side * 18, 31), (side * 10, 29)]
        cv.poly(T(band), R)
        for k, (px, py) in enumerate([(17, 28), (24, 26.5), (30, 21)]):
            p = T([(side * px, py)])[0]
            cv.circle(p[0], p[1], 1.2 * s, K)
        p = T([(side * 12, 29)])[0]; cv.circle(p[0], p[1], 1.6 * s, B)
        cv.poly(T(fw), K)
        # forewing red band
        fb = [(side * 18, -20), (side * 34, -38), (side * 40, -34), (side * 44, -16), (side * 36, -12), (side * 28, -20)]
        cv.poly(T(fb), R)
        # white apical spots
        for (px, py, rr) in [(44, -40, 2.6), (50, -36, 2.0), (48, -30, 1.6), (38, -42, 1.8), (52, -41, 1.3)]:
            p = T([(side * px, py)])[0]
            cv.circle(p[0], p[1], rr * s, WH)
        # scaly fringe
        for k in range(len(fw) - 1):
            a, b = T([fw[k]])[0], T([fw[k + 1]])[0]
            for j in range(0, 6):
                t = j / 6
                cv.circle(a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, 0.6 * s, WH if j % 2 else K)
        # veins
        for (px, py) in [(40, -40), (46, -26), (36, -10)]:
            cv.line(T([(side * 4, -2), (side * px, py)]), mix(K, R, 0.3), 0.5)
    body = T([(0, -10), (2.5, 0), (2, 24), (0, 28), (-2, 24), (-2.5, 0)])
    cv.poly(body, K)
    cv.line(T([(0, -2), (0, 22)]), mix(K, WH, 0.3), 0.5)
    hd = T([(0, -12)])[0]; cv.circle(hd[0], hd[1], 3 * s, K)
    for side in (1, -1):
        ant = T([(side * 1, -14), (side * 8, -30), (side * 12, -40)])
        cv.line(ant, K, 0.8)
        cv.circle(ant[-1][0], ant[-1][1], 1.3 * s, WH)
admiral(250, 170, 1.55, 0.35)
admiral(98, 430, 1.0, -0.4)

# ---------- bumblebees ----------
def bee(x, y, s, ang):
    ca, sa = math.cos(ang), math.sin(ang)
    def T(px, py): return (x + (px * ca - py * sa) * s, y + (px * sa + py * ca) * s)
    # wings
    for side in (1, -1):
        p = T(side * 8, -6)
        cv.ellipse(p[0], p[1], 7 * s, 4 * s, mix(WH, B, 0.2), outline=K, width=0.5)
    bands = [(0, K), (-5, Y), (-10, K), (-15, K), (-19, Y), (-24, WH)]
    for dy, c in bands[::-1]:
        p = T(0, 6 + dy * -0.6 - 8)
    # body as stacked discs (tail white, then black/yellow)
    for k, c in enumerate([WH, WH, K, K, Y, Y, K, K, Y, Y]):
        p = T(0, 12 - k * 2.2)
        cv.circle(p[0], p[1], (5.5 - abs(k - 5) * 0.25) * s, c)
    h = T(0, -12); cv.circle(h[0], h[1], 3.6 * s, K)
    for side in (1, -1):
        a = T(side * 2, -14); b = T(side * 6, -20)
        cv.line([a, b], K, 0.7)
        for j in range(3):
            l1 = T(side * 4, -4 + j * 4); l2 = T(side * 9, -2 + j * 5)
            cv.line([l1, l2], K, 0.7)
    # fuzz
    for k in range(20):
        a = k * math.tau / 20
        p = T(6.2 * math.cos(a), 1 + 11 * math.sin(a))
        cv.circle(p[0], p[1], 0.5 * s, K)
for (x, y, s, a) in [(330, 330, 1.3, 0.6), (140, 250, 1.0, -0.3), (300, 520, 1.1, 2.4), (60, 90, 0.9, 0.9)]:
    bee(x, y, s, a)

# a hoverfly, hovering
hx, hy = 212, 372
for side in (1, -1):
    cv.ellipse(hx + side * 7, hy - 3, 7, 3, mix(WH, B, 0.15), outline=K, width=0.4)
cv.ellipse(hx, hy + 4, 3, 8, Y)
for k in range(3):
    cv.line([(hx - 3, hy + k * 4), (hx + 3, hy + k * 4)], K, 1.2)
cv.circle(hx, hy - 5, 3, mix(R, K, 0.4))
for k in range(4):  # motion lines
    cv.line([(hx - 22, hy - 8 + k * 5), (hx - 14, hy - 8 + k * 5)], WH, 0.6)

# ---------- botanical label ----------
lx0, ly0, lx1, ly1 = 222, 544, 384, 584
cv.rect(lx0 + 3, ly0 + 3, lx1 + 3, ly1 + 3, K)
cv.rect(lx0, ly0, lx1, ly1, WH)
cv.line([(lx0 + 3, ly0 + 3), (lx1 - 3, ly0 + 3), (lx1 - 3, ly1 - 3), (lx0 + 3, ly1 - 3), (lx0 + 3, ly0 + 3)], K, 0.6, joint=False)
cv.text((lx0 + lx1) / 2, ly0 + 13, "Michaelmas Daisy", K, font(13, "serifb"), anchor="mm")
cv.text((lx0 + lx1) / 2, ly0 + 28, "Symphyotrichum novi-belgii", B, font(12, "serifi"), anchor="mm")

cv.finish()
