"""Afternoon — Liberated Medallion. A quilt for Gwen Marston (b. 2 Oct 1936):
no ruler, no pattern. Wonky log cabins, liberated stars, a column of flying geese,
a sawtooth ring, and in the middle a pieced rocket for Alex Raymond (same birthday).
Every patch is a printed fabric; big-stitch hand quilting runs over the top."""
import math, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from ink import *

rnd = random.Random(1936)
cv = Canvas(WH)
COLS = [K, WH, R, Y, B, G]

FABRICS = [  # (base, accent, print)
    (R, WH, "dots"), (R, Y, "calico"), (Y, R, "stripes"), (Y, K, "check"), (B, WH, "dots"),
    (B, Y, "calico"), (G, Y, "dots"), (G, WH, "stripes"), (WH, R, "gingham"), (WH, B, "calico"),
    (K, Y, "dots"), (K, R, "calico"), (WH, G, "dots"), (Y, B, "gingham"), (R, K, "stripes"),
    (B, B, "solid"), (G, G, "solid"), (WH, K, "check"), (Y, G, "calico"),
]


def fabric(m, f):
    base, acc, pat = f
    ox, oy = rnd.randrange(8), rnd.randrange(8)
    cv.fill(m, base)
    if pat == "dots":
        cv.benday(m, acc, pitch=rnd.choice([5, 6, 7]), r=1.2, angle=rnd.choice([0, 45]), ox=ox, oy=oy)
    elif pat == "stripes":
        cv.hatch(m, acc, pitch=rnd.choice([4, 5, 6]), angle=rnd.choice([0, 90, 45, 135]), width=2, phase=ox)
    elif pat == "gingham":
        cv.hatch(m, acc, pitch=6, angle=0, width=2, phase=ox)
        cv.hatch(m, acc, pitch=6, angle=90, width=2, phase=oy)
    elif pat == "check":
        cv.fill(m & ((((XX + ox) // 4) + ((YY + oy) // 4)) % 2 == 0), acc)
    elif pat == "calico":
        h = (XX * 73856093 ^ YY * 19349663 ^ (ox * 83492791)) % 97
        sprig = m & (h < 6)
        cv.fill(sprig, acc)
        cv.fill(np.roll(sprig, 1, 1) & m, acc)
        cv.fill(np.roll(sprig, 1, 0) & m, acc)


def pick(avoid=()):
    while True:
        f = rnd.choice(FABRICS)
        if f[0] not in avoid:
            return f


def poly(pts):
    return Canvas.mask(lambda d: d.polygon(pts, fill=1))


def rectm(x0, y0, x1, y1):
    return (XX >= x0) & (XX < x1) & (YY >= y0) & (YY < y1)


def log_cabin(x0, y0, x1, y1):
    block = rectm(x0, y0, x1, y1)
    fabric(block, pick())
    cx, cy = rnd.uniform(x0 + (x1 - x0) * 0.35, x0 + (x1 - x0) * 0.6), rnd.uniform(y0 + (y1 - y0) * 0.35, y0 + (y1 - y0) * 0.6)
    s = rnd.uniform(7, 11)
    q = [[cx - s, cy - s], [cx + s, cy - s + rnd.uniform(-2, 2)], [cx + s, cy + s], [cx - s + rnd.uniform(-2, 2), cy + s]]
    fabric(poly([tuple(p) for p in q]) & block, (R, Y, "solid") if rnd.random() < 0.5 else (R, R, "solid"))  # hearth
    prev = R
    for k in range(14):
        side = k % 4
        a, b = side, (side + 1) % 4
        w1, w2 = rnd.uniform(5, 12), rnd.uniform(5, 12)
        nx = [(0, -1), (1, 0), (0, 1), (-1, 0)][side]
        na = [q[a][0] + nx[0] * w1, q[a][1] + nx[1] * w1]
        nb = [q[b][0] + nx[0] * w2, q[b][1] + nx[1] * w2]
        # extend the strip across the full new side (log cabin logs overlap the corners)
        strip = [tuple(q[a]), tuple(q[b]), tuple(nb), tuple(na)]
        f = pick(avoid=(prev,))
        prev = f[0]
        fabric(poly(strip) & block, f)
        # the neighbouring corners move outward along the new side
        q[a], q[b] = na, nb
    # seam shadow so pieces read at four inches
    cv.draw(lambda d: d.rectangle([x0, y0, x1 - 1, y1 - 1], outline=1, width=1), K)


def wonky_star(x0, y0, x1, y1):
    bgf = pick()
    block = rectm(x0, y0, x1, y1)
    fabric(block, bgf)
    sf = pick(avoid=(bgf[0],))
    w, h = x1 - x0, y1 - y0
    j = lambda: rnd.uniform(-0.06, 0.06)
    c = [(x0 + w * (0.3 + j()), y0 + h * (0.3 + j())), (x0 + w * (0.7 + j()), y0 + h * (0.3 + j())),
         (x0 + w * (0.7 + j()), y0 + h * (0.7 + j())), (x0 + w * (0.3 + j()), y0 + h * (0.7 + j()))]
    tips = [(x0 + w * (0.5 + 2 * j()), y0), (x1, y0 + h * (0.5 + 2 * j())),
            (x0 + w * (0.5 + 2 * j()), y1), (x0, y0 + h * (0.5 + 2 * j()))]
    for i in range(4):
        fabric(poly([c[i], tips[i], c[(i + 1) % 4]]) & block, sf)
    cf = pick(avoid=(sf[0],))
    fabric(poly(c), cf)
    cv.draw(lambda d: d.rectangle([x0, y0, x1 - 1, y1 - 1], outline=1, width=1), K)


# --- binding ----------------------------------------------------------------------
fabric(np.ones((H, W), bool), (R, WH, "stripes"))
INSET = 8

# --- top band: liberated stars -----------------------------------------------------
xs = [INSET, 100, 196, 300, W - INSET]
for i in range(4):
    wonky_star(xs[i], INSET, xs[i + 1], 90)

# --- side columns: flying geese, flying in opposite directions -----------------------
for (x0, x1, up) in [(INSET, 48, True), (W - 48, W - INSET, False)]:
    y = 90
    gf = (WH, WH, "solid")
    while y < 420:
        hgt = rnd.uniform(17, 24)
        sky = (B, WH, "dots") if up else (K, Y, "dots")
        fabric(rectm(x0, y, x1, y + hgt), sky)
        goose = pick(avoid=(sky[0],))
        tip = (x0 + (x1 - x0) * rnd.uniform(0.4, 0.6), y if up else y + hgt)
        basey = y + hgt if up else y
        fabric(poly([(x0, basey), (x1, basey), tip]) & rectm(x0, y, x1, y + hgt), goose)
        y += hgt
    cv.draw(lambda d: d.rectangle([x0, 90, x1 - 1, 420], outline=1, width=1), K)

# --- centre medallion: a pieced rocket over a planet -------------------------------
MX0, MY0, MX1, MY1 = 48, 90, W - 48, 420
med = rectm(MX0, MY0, MX1, MY1)
fabric(med, (B, B, "solid"))
cv.benday(med, K, pitch=6, r=1.3, angle=30)
for i in range(70):  # appliquéd star sprigs
    sx, sy = rnd.randrange(MX0 + 22, MX1 - 22), rnd.randrange(MY0 + 22, MY1 - 22)
    col = rnd.choice([Y, WH, WH])
    cv.a[sy - 2:sy + 3, sx] = col; cv.a[sy, sx - 2:sx + 3] = col
# sawtooth ring inside the medallion edge
T = 20
ring = med & ~rectm(MX0 + T, MY0 + T, MX1 - T, MY1 - T)
fabric(ring, (Y, R, "calico"))
for x in range(MX0, MX1, T):
    fabric(poly([(x, MY0), (x + T, MY0), (x + T / 2, MY0 + T)]) & med, (R, R, "solid"))
    fabric(poly([(x, MY1), (x + T, MY1), (x + T / 2, MY1 - T)]) & med, (R, R, "solid"))
for y in range(MY0 + T, MY1 - T, T):
    fabric(poly([(MX0, y), (MX0, y + T), (MX0 + T, y + T / 2)]) & ring, (K, K, "solid"))
    fabric(poly([(MX1, y), (MX1, y + T), (MX1 - T, y + T / 2)]) & ring, (K, K, "solid"))
# planet, appliquéd with blanket stitch
PX, PY, PRR = 230, 330, 58
pl = Canvas.mask(lambda d: d.ellipse([PX - PRR, PY - PRR, PX + PRR, PY + PRR], fill=1)) & rectm(MX0 + T, MY0 + T, MX1 - T, MY1 - T)
fabric(pl, (G, Y, "calico"))
fabric(pl & (np.abs(YY - PY - 0.3 * (XX - PX)) < 9), (Y, R, "stripes"))
for k in range(0, 360, 9):
    a = math.radians(k)
    x, y = PX + PRR * math.cos(a), PY + PRR * math.sin(a)
    x2, y2 = PX + (PRR - 6) * math.cos(a), PY + (PRR - 6) * math.sin(a)
    if MY0 + T < y < MY1 - T and MX0 + T < x < MX1 - T:
        cv.draw(lambda d: d.line([x, y, x2, y2], fill=1, width=1), WH)
cv.fill(Canvas.mask(lambda d: d.ellipse([PX - PRR, PY - PRR, PX + PRR, PY + PRR], outline=1, width=2)) & rectm(MX0 + T, MY0 + T, MX1 - T, MY1 - T), WH)
# rocket, pieced (straight seams, a little crooked on purpose)
rcx, rtop = 160, 128
tilt = -0.12
def rot(p):
    x, y = p[0] - rcx, p[1] - 260
    return (rcx + x * math.cos(tilt) - y * math.sin(tilt), 260 + x * math.sin(tilt) + y * math.cos(tilt))
pieces = [
    ([(rcx - 26, 190), (rcx + 26, 190), (rcx + 2, rtop)], (R, WH, "dots")),            # nose
    ([(rcx - 26, 190), (rcx + 26, 192), (rcx + 26, 236), (rcx - 26, 234)], (WH, R, "gingham")),
    ([(rcx - 26, 234), (rcx + 26, 236), (rcx + 26, 300), (rcx - 26, 300)], (Y, K, "check")),
    ([(rcx - 26, 300), (rcx + 26, 300), (rcx + 26, 330), (rcx - 26, 332)], (WH, B, "calico")),
    ([(rcx - 26, 270), (rcx - 56, 340), (rcx - 26, 332)], (R, Y, "calico")),          # fins
    ([(rcx + 26, 270), (rcx + 58, 338), (rcx + 26, 330)], (G, WH, "stripes")),
    ([(rcx - 18, 332), (rcx + 18, 330), (rcx + 4, 382)], (Y, Y, "solid")),            # flame
    ([(rcx - 10, 332), (rcx + 12, 330), (rcx + 2, 360)], (R, R, "solid")),
]
for pts, f in pieces:
    pts = [rot(p) for p in pts]
    fabric(poly(pts), f)
    cv.draw(lambda d: d.line(pts + [pts[0]], fill=1, width=1), K)
p = rot((rcx, 212))
cv.draw(lambda d: d.ellipse([p[0] - 11, p[1] - 11, p[0] + 11, p[1] + 11], fill=1), K)  # porthole, button-sewn
cv.draw(lambda d: d.ellipse([p[0] - 8, p[1] - 8, p[0] + 8, p[1] + 8], fill=1), B)
for dx, dy in [(-3, -3), (3, -3), (-3, 3), (3, 3)]:
    cv.a[int(p[1] + dy) - 1:int(p[1] + dy) + 1, int(p[0] + dx) - 1:int(p[0] + dx) + 1] = WH
cv.draw(lambda d: d.rectangle([MX0, MY0, MX1 - 1, MY1 - 1], outline=1, width=1), K)

# --- bottom: two rows of wonky log cabins ---------------------------------------
ys = [420, 506, H - INSET]
xs = [INSET, 104, 200, 298, W - INSET]
for r in range(2):
    for c in range(4):
        log_cabin(xs[c], ys[r], xs[c + 1], ys[r + 1])

# --- big-stitch hand quilting: dashes that change thread colour with the ground ----
light = np.all(cv.a == WH, -1) | np.all(cv.a == Y, -1)
stitch = np.zeros((H, W), bool)
s = Canvas.mask(lambda d: [d.line([x, 0, x + 600, 600], fill=1, width=1) for x in range(-600, 400, 26)])
stitch |= s & ~med & rectm(INSET, INSET, W - INSET, H - INSET)
# echo quilting around the planet and rocket inside the medallion
for rr in range(PRR + 10, PRR + 90, 12):
    stitch |= Canvas.mask(lambda d: d.ellipse([PX - rr, PY - rr, PX + rr, PY + rr], outline=1, width=1)) & rectm(MX0 + T + 2, MY0 + T + 2, MX1 - T - 2, MY1 - T - 2)
dash = (((XX + YY) // 4) % 2 == 0)
st = stitch & dash
cv.a[st & light] = K
cv.a[st & ~light] = WH

# a label, hand-stitched in the corner
cv.draw(lambda d: d.rectangle([292, 572, 388, 590], fill=1), WH)
cv.draw(lambda d: d.rectangle([292, 572, 388, 590], outline=1, width=1), K)
text(cv, (340, 575), "for G.M. 1936", 11, R, anchor="ma")
cv.save()
