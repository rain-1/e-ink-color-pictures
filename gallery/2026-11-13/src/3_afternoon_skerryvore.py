# Afternoon — "Skerryvore". Stevenson came from a family of lighthouse engineers and named
# his house after the tallest of their towers: his uncle Alan's, 1844, twelve miles off Tiree.
# An engineer's section — cut masonry in red, nine rooms furnished — standing in a real sea.
import math, random
import numpy as np
from kit import *
random.seed(1844); c = Canvas(WH)
CX, BASE, TOP = 200, 486, 150
HOR = 428

# ---- sky: an engraver's line screen, thick where the cloud is heavy --------------------
n = (np.sin(XX / 47.0 + YY / 31.0) + np.sin(XX / 23.0 - YY / 17.0 + 2) * 0.6 + np.sin((XX + 2 * YY) / 71.0 + 4) * 0.9 + np.sin(XX / 11.0 + YY / 9.0) * 0.25)
t = np.clip(0.42 + 0.2 * n + 0.35 * (1 - YY / HOR) ** 2, 0.04, 0.8)
c.put(YY < HOR, B, ((YY % 4) / 4.0) < t)
c.put((YY < HOR) & (t > 0.72), B)

# ---- the beams ---------------------------------------------------------------------------
LY = 118
for sgn in (-1, 1):
    beam = c.layer().poly([(CX + sgn * 10, LY - 4), (CX + sgn * 230, LY - 58), (CX + sgn * 230, LY + 30), (CX + sgn * 10, LY + 4)]).mask()
    fall = np.clip(1.05 - np.abs(XX - CX) / 230.0, 0, 1)
    c.put(beam, Y, tone(fall * 0.95) | hatch(90 - sgn * 8, 7, 1))

# ---- sea ---------------------------------------------------------------------------------
c.put(YY >= HOR, B)
c.put((YY >= HOR) & (YY < HOR + 2), K)
wave = c.layer()
y = HOR + 6; k = 0
while y < 560:
    sc = 0.5 + (y - HOR) / 70.0
    step = 16 * sc; off = (k % 2) * step / 2 + random.uniform(0, 4)
    x = -step + off
    while x < W + step:
        hh = 3.2 * sc * random.uniform(0.7, 1.2)
        wave.line(bez((x, y), (x + step * 0.3, y - hh), (x + step * 0.55, y - hh), (x + step * 0.7, y + hh * 0.2)) , max(1, 0.9 * sc))
        x += step
    y += 5.5 * sc; k += 1
wave.put(WH, thr=0.3)
# deep troughs
tr = c.layer()
for _ in range(60):
    x, y = random.uniform(0, W), random.uniform(HOR + 20, 550); sc = 0.5 + (y - HOR) / 70.0
    tr.line([(x, y), (x + 9 * sc, y + 1.5)], 1.2 * sc)
tr.put(K, thr=0.3)

# ---- the rock ----------------------------------------------------------------------------
rock = smooth([(84, 520), (100, 500), (128, 494), (146, 482), (176, 486), (228, 484), (252, 478), (270, 492), (300, 498), (318, 516), (330, 540), (70, 540)], n=6)
rock = [(x + random.uniform(-2, 2), y + random.uniform(-2, 2)) for x, y in rock]
rm = c.layer().poly(rock).mask(); c.put(rm, K)
rs = c.layer()
for _ in range(46):
    x, y = random.uniform(90, 315), random.uniform(488, 532); l = random.uniform(8, 26)
    rs.line([(x, y), (x + l * 0.5, y - 2), (x + l, y + 1.5)], 1)
c.put(rs.mask(0.3) & rm, WH)
c.put(rm & (YY > 512), B, hatch(0, 3, 1))

# ---- tower profile -----------------------------------------------------------------------
def hw(y):                         # outer half-width
    tt = (BASE - y) / (BASE - TOP); return 24 + 36 * (1 - tt) ** 2.4
def th(y):                         # wall thickness
    tt = (BASE - y) / (BASE - TOP); return 6 + 25 * (1 - tt) ** 2.0
ys = list(range(TOP, BASE + 1, 4))
outer = [(CX - hw(y), y) for y in ys] + [(CX + hw(y), y) for y in reversed(ys)]
om = c.layer().poly(outer).mask()
c.put(grow(om, 1), K); c.put(om, WH)
c.put(om, R, hatch(45, 4, 1))                               # cut stone
crs = c.layer(1)                                           # courses
for y in range(TOP + 4, BASE, 6): crs.seg(CX - 70, y, CX + 70, y)
c.put(crs.mask() & om, R)

FLOORS = [436, 404, 373, 343, 314, 286, 259, 233, 208, 176]   # floor levels, bottom room first; last is watch-room ceiling
names = ["Coal & Water", "Oil Store", "Provisions", "Kitchen", "Bedroom", "Bedroom", "Library", "Store", "Watch Room"]
rooms = []
for i in range(9):
    yf, yc = FLOORS[i], FLOORS[i + 1] + 3
    xl = CX - (hw(yf) - th(yf)) + 1; xr = CX + (hw(yf) - th(yf)) - 1
    rm_ = c.layer().poly([(xl, yf), (xr, yf), (xr - 0.5, yc + 5)] + arc(CX, yc + 5, (xr - xl) / 2 - 0.5, 5, 0, -180, 12) + [(xl + 0.5, yc + 5)]).mask()
    c.put(grow(rm_, 1), K); c.put(rm_, WH)
    rooms.append((int(xl), int(xr), yf, yc))
    # window through the wall, alternating sides
    sgn = -1 if i % 2 else 1
    wy = yf - 17
    c.put(c.layer(1).rect(min(CX + sgn * (hw(wy) + 1), CX + sgn * (xr - CX)), wy - 4, max(CX + sgn * (hw(wy) + 1), CX + sgn * (xr - CX)), wy + 4).mask(), WH)
    c.put(c.layer(1).rect(CX + sgn * hw(wy) - (2 if sgn > 0 else 0), wy - 4, CX + sgn * hw(wy) + (0 if sgn > 0 else 2), wy + 4).mask(), B)
    c.hair([(CX + sgn * (xr - CX), wy - 5), (CX + sgn * hw(wy), wy - 5)], K); c.hair([(CX + sgn * (xr - CX), wy + 4), (CX + sgn * hw(wy), wy + 4)], K)

def px(x0, y0, x1, y1, col, pat=None): c.put(c.layer(1).rect(x0, y0, x1, y1).mask(), col, pat)
def ladder(xa, ya, xb, yb):
    c.hair([(xa, ya), (xb, yb)], K); c.hair([(xa + 4, ya), (xb + 4, yb)], K)
    nn = int(abs(ya - yb) // 4)
    for k in range(1, nn): 
        f = k / nn; c.hair([(xa + (xb - xa) * f, ya + (yb - ya) * f), (xa + 4 + (xb - xa) * f, ya + (yb - ya) * f)], K)
def keeper(x, y, coat=B, sit=False):
    px(x - 1, y - 12, x + 2, y - 9, WH); c.hair([(x - 2, y - 13), (x + 2, y - 13)], K); px(x - 2, y - 14, x + 3, y - 12, K)   # cap
    px(x - 2, y - 9, x + 3, y - 4, coat)
    if sit: px(x - 2, y - 4, x + 5, y - 2, K); px(x + 3, y - 2, x + 5, y, K)
    else: px(x - 2, y - 4, x, y, K); px(x + 1, y - 4, x + 3, y, K)
def barrel(x, y, col, w=8, hh=10):
    px(x, y - hh, x + w, y, K); px(x + 1, y - hh + 1, x + w - 1, y - 1, col); c.hair([(x, y - hh + 3), (x + w - 1, y - hh + 3)], K); c.hair([(x, y - 4), (x + w - 1, y - 4)], K)

for i, (xl, xr, yf, yc) in enumerate(rooms):
    # ladders alternate
    if i < 8:
        if i % 2 == 0: ladder(xr - 12, yf - 1, xr - 6, yc - 2)
        else: ladder(xl + 8, yf - 1, xl + 2, yc - 2)
    if i == 0:      # coal and water
        c.poly([(xl + 1, yf), (xl + 8, yf - 9), (xl + 15, yf - 5), (xl + 20, yf)], K)
        px(xl + 22, yf - 14, xl + 34, yf, K); px(xl + 23, yf - 13, xl + 33, yf - 1, B); px(xl + 23, yf - 13, xl + 33, yf - 11, WH); c.hair([(xl + 28, yf - 14), (xl + 28, yf - 19), (xl + 31, yf - 19)], K)
    if i == 1:      # oil
        for k in range(3): barrel(xl + 3 + k * 10, yf, Y, 9, 12)
        barrel(xl + 8, yf - 12, Y, 9, 9)
    if i == 2:      # provisions: shelves, sacks, a ham
        for sy_ in (yf - 9, yf - 17): c.hair([(xl + 1, sy_), (xl + 22, sy_)], K)
        for k, col in enumerate((R, G, Y, B, R)): px(xl + 2 + k * 4, yf - 15, xl + 5 + k * 4, yf - 9, col)
        for k, col in enumerate((G, Y, R, B)): px(xl + 3 + k * 5, yf - 22, xl + 6 + k * 5, yf - 17, col)
        c.put(c.layer().ellipse(xl + 8, yf - 4, 5, 4).ellipse(xl + 17, yf - 3.5, 4.5, 3.5).mask(), K); c.put(c.layer().ellipse(xl + 8, yf - 4, 4, 3).ellipse(xl + 17, yf - 3.5, 3.5, 2.5).mask(), WH)
        barrel(xl + 24, yf, G, 7, 9)
    if i == 3:      # kitchen: range with fire and flue, table, kettle, keeper
        px(xl + 2, yf - 11, xl + 14, yf, K); px(xl + 4, yf - 7, xl + 10, yf - 2, R); px(xl + 6, yf - 5, xl + 8, yf - 3, Y)
        px(xl + 3, yf - 26, xl + 6, yf - 11, K)
        px(xl + 9, yf - 15, xl + 14, yf - 11, K); c.hair([(xl + 14, yf - 13), (xl + 16, yf - 15)], K)
        px(xl + 20, yf - 8, xl + 32, yf - 7, K); px(xl + 21, yf - 7, xl + 22, yf, K); px(xl + 30, yf - 7, xl + 31, yf, K)
        px(xl + 23, yf - 10, xl + 26, yf - 8, B); px(xl + 27, yf - 11, xl + 29, yf - 8, Y)
        keeper(xl + 17, yf, R)
    if i in (4, 5): # bunks
        for by in (yf - 3, yf - 14):
            px(xl + 2, by - 1, xl + 26, by, K); px(xl + 2, by - 5, xl + 26, by - 1, R if i == 4 else B); px(xl + 2, by - 5, xl + 8, by - 1, WH)
            c.put(c.layer(1).rect(xl + 9, by - 5, xl + 26, by - 1).mask(), WH, hatch(90, 4, 1))
        px(xl + 1, yf - 22, xl + 2, yf, K); px(xl + 26, yf - 22, xl + 27, yf, K)
        if i == 4: px(xl + 4, yf - 8, xl + 7, yf - 5, K)   # a sleeper's head
        px(xl + 30, yf - 6, xl + 35, yf, K); px(xl + 31, yf - 5, xl + 34, yf - 1, Y)     # sea-chest
    if i == 6:      # library: books, armchair, reader, lamp
        for sy_ in (yf - 8, yf - 15, yf - 22):
            c.hair([(xl + 1, sy_), (xl + 15, sy_)], K)
            for k in range(7): px(xl + 1 + k * 2, sy_ - 6, xl + 3 + k * 2, sy_, random.choice((R, B, G, Y, K, R, B)))
        px(xl + 20, yf - 9, xl + 22, yf, K); px(xl + 20, yf - 4, xl + 29, yf - 2, G); px(xl + 20, yf - 10, xl + 23, yf - 3, G)
        keeper(xl + 25, yf - 2, B, True)
        px(xl + 31, yf - 16, xl + 34, yf - 12, Y); c.hair([(xl + 32, yf - 12), (xl + 32, yf - 20)], K)
    if i == 7:      # store: coiled rope, spare lamp glasses, flags
        c.put(c.layer().ring(xl + 8, yf - 5, 5, 1.2).ring(xl + 8, yf - 5, 2.5, 1).mask(0.3), K)
        for k, col in enumerate((R, Y, B, WH)): px(xl + 16 + k * 5, yf - 18, xl + 20 + k * 5, yf - 13, col); c.hair([(xl + 16 + k * 5, yf - 19), (xl + 20 + k * 5, yf - 19)], K)
        barrel(xl + 16, yf, R, 7, 8); barrel(xl + 24, yf, WH, 7, 8)
    if i == 8:      # watch room: the clockwork that turns the lens, and the man who winds it
        mx = CX - 4
        px(mx - 6, yf - 12, mx + 8, yf, K); px(mx - 5, yf - 11, mx + 7, yf - 1, WH)
        c.put(c.layer().ring(mx - 1, yf - 6, 3.5, 1).ring(mx + 4, yf - 4, 2, 1).mask(0.3), K); px(mx - 2, yf - 7, mx, yf - 5, Y)
        px(mx, yf - 28, mx + 2, yf - 12, K)                               # drive shaft up to the lens
        c.hair([(mx + 10, yf - 14), (mx + 10, yf - 2)], K); px(mx + 9, yf - 3, mx + 12, yf, Y)   # weight
        keeper(xl + 6, yf, B)

# entrance door and the gun-metal ladder down to the rock
dy = FLOORS[0]
px(CX - hw(dy) - 1, dy - 14, CX - (hw(dy) - th(dy)) + 1, dy, WH)
px(CX - hw(dy) - 1, dy - 14, CX - hw(dy) + 3, dy, R); c.hair([(CX - hw(dy) - 2, dy), (CX - (hw(dy) - th(dy)), dy)], K); c.hair([(CX - hw(dy) - 2, dy - 15), (CX - (hw(dy) - th(dy)), dy - 15)], K)
lx = CX - hw(dy) - 6
for yy in range(dy, BASE + 4, 4): c.hair([(lx - (yy - dy) * 0.19, yy), (lx + 4 - (yy - dy) * 0.19, yy)], K)
c.hair([(lx, dy), (lx - (BASE + 4 - dy) * 0.19, BASE + 4)], K); c.hair([(lx + 4, dy), (lx + 4 - (BASE + 4 - dy) * 0.19, BASE + 4)], K)

# ---- gallery and lantern -------------------------------------------------------------------
gy = TOP
c.poly([(CX - 24, gy + 8), (CX - 34, gy), (CX + 34, gy), (CX + 24, gy + 8)], K)
px(CX - 36, gy - 3, CX + 36, gy, K); px(CX - 35, gy - 2, CX + 35, gy - 1, WH)
for x in range(CX - 35, CX + 36, 5): c.hair([(x, gy - 3), (x, gy - 14)], K)
c.hair([(CX - 36, gy - 14), (CX + 35, gy - 14)], K); c.hair([(CX - 36, gy - 9), (CX + 35, gy - 9)], K)
# lantern glazing
lx0, lx1, ly0, ly1 = CX - 19, CX + 19, gy - 48, gy - 3
px(lx0 - 1, ly0, lx1 + 1, ly1, K); px(lx0, ly0 + 1, lx1, ly1, WH)
px(lx0, ly1 - 9, lx1, ly1, K); px(lx0 + 1, ly1 - 8, lx1 - 1, ly1 - 1, WH); c.put(c.layer(1).rect(lx0 + 1, ly1 - 8, lx1 - 1, ly1 - 1).mask(), K, hatch(90, 4, 1))
glz = c.layer(1)
for k in range(-6, 7): 
    glz.seg(CX + k * 9.5 - 30, ly1 - 9, CX + k * 9.5 + 30, ly0); glz.seg(CX + k * 9.5 + 30, ly1 - 9, CX + k * 9.5 - 30, ly0)
c.put(glz.mask() & c.layer(1).rect(lx0, ly0 + 1, lx1, ly1 - 9).mask(), K)
# the lens: a beehive of prisms
lens = c.layer().ellipse(CX, LY, 11, 15).mask()
c.put(grow(lens, 1), K); c.put(lens, Y); c.put(lens, WH, hatch(0, 3, 1)); c.put(c.layer().ellipse(CX, LY, 4, 5).mask(), WH); c.put(c.layer().ellipse(CX, LY, 2, 3).mask(), R)
c.hair([(CX - 11, LY), (CX + 11, LY)], K)
px(CX - 4, LY + 15, CX + 4, ly1 - 9, K)
# dome, ball, vane
dome = c.layer().poly([(lx0 - 3, ly0 + 1)] + arc(CX, ly0 + 1, 22, 20, 180, 360, 20) + [(lx1 + 3, ly0 + 1)]).mask()
c.put(grow(dome, 1), K); c.put(dome, R); c.put(dome & (XX > CX + 6), K, hatch(90, 3, 1))
dl_ = c.layer(1)
for k in (-12, -4, 4, 12): dl_.line(arc(CX, ly0 + 1, abs(k) + 0.01, 20, 180 if k < 0 else 360, 270, 10), 1)
c.put(dl_.mask() & dome, K)
c.put(c.layer().circle(CX, ly0 - 23, 4).mask(), K); c.put(c.layer().circle(CX, ly0 - 23, 2.6).mask(), Y)
c.hair([(CX, ly0 - 27), (CX, ly0 - 44)], K); c.poly([(CX, ly0 - 42), (CX + 12, ly0 - 39), (CX, ly0 - 36)], K); c.hair([(CX - 5, ly0 - 34), (CX + 5, ly0 - 34)], K)
keeper(CX + 27, gy - 3, K)        # a keeper on the gallery, looking west

# ---- surf breaking on the rock, spray up the weather side ------------------------------------
foam = c.layer()
random.seed(7)
for (fx, fy, r) in ((92, 508, 13), (78, 520, 12), (110, 498, 10), (126, 488, 8), (64, 530, 11), (104, 520, 9), (308, 512, 10), (322, 524, 10), (292, 502, 7), (140, 476, 6), (120, 470, 5)):
    for _ in range(7):
        a = random.uniform(0, 6.28); d = random.uniform(0, r * 0.7)
        foam.circle(fx + d * math.cos(a), fy + d * math.sin(a) * 0.7, random.uniform(r * 0.3, r * 0.6))
fm = foam.mask(); c.put(grow(fm, 1), K); c.put(fm, WH); c.put(fm & ~grow(~fm, 2) & (dots(5, 1.1)), B)
spray = c.layer()
for _ in range(190):
    a = random.uniform(-2.5, -1.0); d = random.uniform(10, 95) * random.random() ** 0.6
    spray.circle(112 + d * math.cos(a) * 0.8, 492 + d * math.sin(a), random.choice((0.8, 1, 1.4, 2)))
sp = spray.mask(0.4) & ~om; c.put(grow(sp, 1) & ~om & (YY > HOR - 60), K, checker(1)); c.put(sp, WH)

# ---- the relief boat, reefed down ---------------------------------------------------------------
bx, by = 46, 462
c.poly([(bx - 16, by - 4), (bx + 17, by - 5), (bx + 12, by + 2), (bx - 12, by + 2)], K)
c.line([(bx, by - 4), (bx + 2, by - 34)], K, 1.3)
c.poly([(bx + 3, by - 32), (bx + 16, by - 8), (bx + 3, by - 7)], R); c.poly([(bx, by - 28), (bx - 12, by - 8), (bx, by - 7)], R)
c.line([(bx + 3, by - 32), (bx + 16, by - 8), (bx + 3, by - 7)], K, 1, closed=True); c.line([(bx, by - 28), (bx - 12, by - 8), (bx, by - 7)], K, 1, closed=True)
px(bx - 9, by - 8, bx - 7, by - 5, WH); px(bx + 8, by - 8, bx + 10, by - 5, WH)
c.line([(bx - 20, by + 4), (bx - 10, by + 2), (bx, by + 5), (bx + 10, by + 2), (bx + 22, by + 4)], WH, 1.5)

# ---- gulls ----------------------------------------------------------------------------------------
def gull(x, y, s=1.0):
    g = c.layer(); g.line(bez((x - 9 * s, y - 1), (x - 5 * s, y - 6 * s), (x - 2 * s, y - 4 * s), (x, y)), 1.5); g.line(bez((x, y), (x + 2 * s, y - 5 * s), (x + 6 * s, y - 6 * s), (x + 10 * s, y - 2 * s)), 1.5)
    m = g.mask(0.3); c.put(grow(m, 1), WH); c.put(m, K)
for x, y, s in ((60, 250, 1.2), (86, 232, 0.9), (330, 300, 1.1), (350, 322, 0.8), (300, 216, 0.9), (40, 330, 0.8), (118, 300, 0.7)): gull(x, y, s)

# ---- annotation: room names on paper tags, dimension line ----------------------------------------
def tag(x, y, t, anchor="lm"):
    m = c.tmask(x, y, t, "lib-i", 12, anchor)
    ys_, xs_ = np.nonzero(m)
    px(xs_.min() - 4, ys_.min() - 3, xs_.max() + 5, ys_.max() + 4, K); px(xs_.min() - 3, ys_.min() - 2, xs_.max() + 4, ys_.max() + 3, WH)
    c.put(m, K)
for i, (xl, xr, yf, yc) in enumerate(rooms):
    yy = yf - 12; x0 = CX + hw(yy) + 3; x1 = 272
    c.put(grow(c.layer(1).seg(x0, yy, x1, yy).mask(), 1), WH); c.hair([(x0, yy), (x1, yy)], K); px(x0 - 1, yy - 1, x0 + 2, yy + 2, K)
    tag(x1 + 4, yy, names[i])
c.hair([(CX + 20, LY - 26), (252, LY - 40)], K); tag(256, LY - 40, "Light Room")
dx = 122
c.put(grow(c.layer(1).seg(dx, TOP, dx, BASE - 30).mask(), 2), WH)
c.hair([(dx, TOP), (dx, BASE - 30)], K)
for yy in (TOP, BASE - 30): c.hair([(dx - 4, yy), (dx + 4, yy)], K)
for yy in range(TOP, BASE - 30, 20): c.hair([(dx - 2, yy), (dx + 1, yy)], K)
tag(dx - 6, 372, "138 feet", "rm"); tag(dx - 6, 388, "rock to lantern", "rm")

# ---- title block --------------------------------------------------------------------------------------
c.put(YY >= 548, WH); c.put((YY >= 548) & (YY < 550), K); c.put((YY >= 552) & (YY < 553), K)
c.text(200, 566, "SKERRYVORE", K, "serif-b", 19, track=5)
c.text(200, 586, "Section · Alan Stevenson, Engineer · 1844", K, "lib-i", 12)
c.poly(star(52, 568, 7, 3, 4), R); c.poly(star(348, 568, 7, 3, 4), R)
c.save("p3.png")
