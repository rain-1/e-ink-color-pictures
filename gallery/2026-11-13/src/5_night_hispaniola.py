# Night — "Under the wide and starry sky". The Hispaniola at anchor off the island on the
# night Jim Hawkins paddles out in Ben Gunn's coracle to cut her loose (Treasure Island,
# ch. XXIII) — rigged line by line, under tonight's real sky: a four-day moon and the first
# Leonids out of the Sickle. The couplet is from "Requiem", the poem cut on Stevenson's grave.
import math, random
import numpy as np
from kit import *
random.seed(1894); rng = np.random.default_rng(1894); c = Canvas(K)
def px(x0, y0, x1, y1, col, pat=None): c.put(c.layer(1).rect(x0, y0, x1, y1).mask(), col, pat)
HOR = 418

# ---- the sky ---------------------------------------------------------------------------
band = np.exp(-(((XX - 60) * 0.55 + (YY - 150) * 0.83) / 46.0) ** 2)          # Milky Way, upper left to lower right
c.put((YY < HOR) & (rng.random((H, W)) < 0.05 * band), WH)
c.put((YY < HOR) & (rng.random((H, W)) < 0.07 * band), B)
c.put((YY < HOR) & (rng.random((H, W)) < 0.0035), WH)
c.put((YY < HOR) & (rng.random((H, W)) < 0.002), B)
big = c.layer()
for _ in range(70):
    x, y = random.uniform(4, W - 4), random.uniform(4, HOR - 20); r = random.choice((1, 1, 1, 1.4, 1.4, 2))
    big.seg(x - r, y, x + r, y, 1); big.seg(x, y - r, x, y + r, 1)
big.put(WH, thr=0.4)
for _ in range(9):
    x, y = random.uniform(10, W - 10), random.uniform(10, HOR - 120)
    c.poly(star(x, y, 4.2, 1.2, 4), random.choice((WH, WH, Y)))
# Leo's Sickle and the radiant
sick = [(86, 74), (70, 60), (52, 58), (38, 70), (36, 90), (50, 108)]; regulus = (50, 126)
c.line(sick + [regulus], B, 1, pat=hatch(0, 3, 2) & hatch(90, 3, 2))
for x, y in sick: c.poly(star(x, y, 3.2, 1.1, 4), WH)
c.poly(star(*regulus, 5.5, 1.6, 4), WH)
c.text(64, 146, "Leo", B, "lib-i", 12, "lm")
rad = (44, 82)
for ang, d0, ln in ((18, 60, 62), (40, 96, 44), (-12, 130, 70), (63, 60, 36), (28, 190, 54), (4, 250, 38), (52, 170, 30)):
    a = math.radians(ang); x0, y0 = rad[0] + d0 * math.cos(a), rad[1] + d0 * math.sin(a); x1, y1 = x0 + ln * math.cos(a), y0 + ln * math.sin(a)
    c.put(c.layer(1).seg(x0, y0, x0 + (x1 - x0) * 0.5, y0 + (y1 - y0) * 0.5).mask(), WH, checker(1))
    c.hair([(x0 + (x1 - x0) * 0.5, y0 + (y1 - y0) * 0.5), (x1, y1)], WH)
    c.line([(x0 + (x1 - x0) * 0.8, y0 + (y1 - y0) * 0.8), (x1, y1)], WH, 1.8); c.put(c.layer().circle(x1, y1, 1.6).mask(), Y)
# the young moon, low in the west
mx, my = 344, 330
mm = c.layer().circle(mx, my, 15).mask() & ~c.layer().circle(mx - 7, my - 4, 15).mask()
c.put(c.layer().circle(mx, my, 15).mask(), B, dots(4, 0.8)); c.put(mm, Y)

# ---- the island --------------------------------------------------------------------------
ridge = [(0, 392), (22, 384), (46, 372), (70, 350), (86, 330), (98, 318), (110, 324), (124, 344), (150, 362), (176, 370), (200, 364), (226, 376),
         (262, 388), (300, 398), (340, 404), (372, 410), (400, 412)]
rp = smooth(ridge, closed=False, n=6); rp = [(x, y + random.uniform(-1.2, 1.2)) for x, y in rp]
isl = c.layer().poly(rp + [(400, HOR), (0, HOR)]).mask()
c.put(isl, B); c.put(isl, K, hatch(45, 3, 1)); c.put(isl & (YY > 396), K, hatch(135, 3, 1))
c.put(isl & ~np.roll(isl, 1, 0), B)
slope = c.layer(1)                                            # moon-side slopes catch a little light
for i in range(len(rp) - 1):
    if rp[i + 1][1] > rp[i][1] + 0.3: slope.seg(rp[i][0], rp[i][1], rp[i + 1][0], rp[i + 1][1])
c.put(slope.mask(), WH)
palms = c.layer()
for x in (14, 30, 58, 132, 160, 186, 214, 240, 276, 312, 352, 384, 76, 116):
    y = min(py for px_, py in rp if abs(px_ - x) < 4) + 1; hh = random.uniform(7, 13); lean = random.uniform(-2, 2)
    palms.line([(x, y), (x + lean * 0.5, y - hh * 0.5), (x + lean, y - hh)], 1.1)
    for a in (195, 230, 270, 310, 345):
        palms.line(bez((x + lean, y - hh), (x + lean + 3 * math.cos(math.radians(a)), y - hh + 3 * math.sin(math.radians(a)) - 1), (x + lean + 6 * math.cos(math.radians(a)), y - hh + 5 * math.sin(math.radians(a))), (x + lean + 7 * math.cos(math.radians(a)), y - hh + 5 * math.sin(math.radians(a)) + 3), 6), 1.1)
palms.put(B, thr=0.3)
c.put(c.layer().circle(232, 400, 1.5).mask(), R); px(231, 403, 234, 404, R, checker(1))      # the pirates' fire ashore

# ---- the sea -------------------------------------------------------------------------------
c.put(YY >= HOR, K)
sw = c.layer(1)
y = HOR + 2; k = 0
while y < 556:
    sc = 1 + (y - HOR) / 40.0
    x = -random.uniform(0, 20)
    while x < W:
        ln = random.uniform(4, 12) * sc
        if random.random() < 0.72: sw.seg(x, y, x + ln, y)
        x += ln + random.uniform(3, 9) * sc
    y += 2 + sc * 1.3; k += 1
c.put(sw.mask(), B)
glint = c.layer(1)                                            # the moon's road
for yy in range(HOR + 1, 560, 3):
    spread = 5 + (yy - HOR) * 0.22
    for _ in range(3):
        x = mx + random.gauss(0, spread * 0.5); ln = random.uniform(2, 5 + (yy - HOR) * 0.06)
        glint.seg(x - ln, yy, x + ln, yy)
c.put(glint.mask() & (YY > HOR), Y)
c.put((YY == HOR) | (YY == HOR + 1), B)

# ---- the schooner ---------------------------------------------------------------------------
WL = 446
deck = lambda x: 416 + 9 * ((x - 205) / 105.0) ** 2 * (-1) + 0   # sheer: rises to bow and stern
def decky(x): return 419 - 10 * ((x - 205) / 105.0) ** 2
hull = [(96, decky(96) - 6), (104, decky(104))] + [(x, decky(x)) for x in range(110, 300, 8)] + [(306, decky(306) - 2), (296, 430), (286, WL), (112, WL), (100, 432)]
hm = c.layer().poly(hull).mask()
c.put(grow(hm, 1), WH); c.put(hm, B)
c.put(hm & (YY > 432), K, hatch(0, 2, 1)); c.put(hm & (YY >= WL - 2), R)                      # boot-topping at the waterline
wale = c.layer(1); wale.line([(x, decky(x) + 6) for x in range(98, 304, 4)], 1); c.put(wale.mask() & hm, WH)
wale2 = c.layer(1); wale2.line([(x, decky(x) + 10) for x in range(98, 304, 4)], 1); c.put(wale2.mask() & hm, K)
for x in range(128, 290, 14): px(x, int(decky(x)) + 13, x + 4, int(decky(x)) + 16, K)      # gun-ports, shut
for k in range(3):                                           # stern cabin, lit
    x = 102 + k * 7; px(x, int(decky(x)) + 2, x + 4, int(decky(x)) + 7, Y); c.hair([(x + 2, decky(x) + 2), (x + 2, decky(x) + 6)], K)
# bulwark rail and deck furniture
rail = c.layer(1); rail.line([(x, decky(x) - 4) for x in range(100, 304, 4)], 1)
for x in range(102, 304, 6): rail.seg(x, decky(x) - 4, x, decky(x))
c.put(rail.mask(), WH)
px(140, 409, 158, 416, WH); px(141, 410, 157, 416, B); px(144, 411, 147, 414, Y); px(151, 411, 154, 414, Y)    # deck-house, lamp within
px(212, 410, 226, 416, WH); px(213, 411, 225, 416, K)                                                           # galley
c.line([(120, 414), (120, 404)], WH, 1.2); c.put(c.layer().ring(120, 404, 3.5, 1).mask(0.3), WH)                 # wheel

MAIN, FORE = 168, 248
rig = c.layer(1)       # standing rigging — hairlines
spars = c.layer()      # masts and spars — solid
furl = c.layer()       # furled canvas
def mast(x, top, cross, rake=-0.04):
    X = lambda y: x + (decky(x) - y) * rake
    spars.poly([(X(decky(x)) - 2, decky(x)), (X(decky(x)) + 2, decky(x)), (X(cross) + 1.4, cross), (X(cross) - 1.4, cross)])
    spars.poly([(X(cross + 10) + 2.2, cross + 10), (X(cross + 10) + 3.6, cross + 10), (X(top) + 2.4, top), (X(top) + 1.6, top)])
    spars.rect(X(cross) - 7, cross, X(cross) + 8, cross + 2); spars.rect(X(cross + 10) - 5, cross + 10, X(cross + 10) + 6, cross + 11.5)
    spars.circle(X(top) + 2, top - 1.5, 1.8)
    # lower shrouds with ratlines, both sides
    for sgn in (-1, 1):
        feet = [x + sgn * (10 + k * 5) for k in range(3)]
        for fxx in feet: rig.seg(X(cross) + sgn * 2, cross + 2, fxx, decky(fxx) - 4)
        for yy in range(int(cross) + 12, int(decky(x)) - 6, 6):
            f = (yy - cross - 2) / (decky(x) - 6 - cross)
            rig.seg(X(cross) + sgn * 2 + (feet[0] - X(cross) - sgn * 2) * f, yy, X(cross) + sgn * 2 + (feet[2] - X(cross) - sgn * 2) * f, yy)
        # topmast shrouds to the crosstrees, and a backstay to the rail
        rig.seg(X(top) + 2, top + 4, X(cross) + sgn * 7, cross)
        rig.seg(X(top) + 2, top + 8, x + sgn * 30 - 6, decky(x + sgn * 30 - 6) - 4)
    return X
XM = mast(MAIN, 138, 236); XF = mast(FORE, 156, 244)
# booms and gaffs lowered, canvas furled along them
for x, X, ln, gy in ((MAIN, XM, 86, 388), (FORE, XF, 62, 392)):
    x0 = X(gy)
    spars.poly([(x0, gy - 1), (x0 - ln, gy + 4), (x0 - ln, gy + 6), (x0, gy + 2)])                 # boom
    pts = [(x0 - 2 - i * (ln - 8) / 9, gy - 3 + i * 0.5 - (3.2 if i % 2 else 1.6)) for i in range(10)]
    furl.poly(pts + [(x0 - ln + 6, gy + 2), (x0 - 2, gy - 1)])
    spars.seg(x0, gy - 8, x0 - ln * 0.8, gy - 5, 1.2)                                               # gaff on top
    rig.seg(x0 - ln, gy + 4, X(236 if x == MAIN else 244), (236 if x == MAIN else 244) + 2)        # topping lift
    rig.seg(x0 - ln * 0.6, gy + 6, x - ln * 0.6 + 8, decky(x - ln * 0.6 + 8) - 4)                  # sheet
# bowsprit, jib-boom, head-stays with stowed jibs, bobstay
bx0, by0, bx1, by1 = 300, decky(300) - 4, 366, 392
spars.poly([(bx0, by0 - 1.5), (bx1, by1 - 0.6), (bx1, by1 + 0.6), (bx0, by0 + 1.5)])
rig.seg(XF(156) + 2, 158, bx1, by1); rig.seg(XF(244), 246, 336, by0 + (by1 - by0) * 0.55); rig.seg(XF(200), 200, 352, by0 + (by1 - by0) * 0.8)
rig.seg(bx1, by1, 292, 436); rig.seg(336, 401, 296, 428)
furl.poly([(304, by0 - 3), (318, by0 - 9), (332, by0 - 10), (350, by0 - 14), (358, by1 - 2), (304, by0)])
# stays between the masts, flag halyard
rig.seg(XM(138) + 2, 140, XF(156) + 2, 158); rig.seg(XM(236), 238, XF(156) + 2, 160); rig.seg(XM(138) + 2, 140, 98, decky(98) - 8)
rgm = rig.mask(); c.put(rgm & (YY < WL), WH, checker(1) | (YY % 6 == 0)); 
fm = furl.mask(); c.put(grow(fm, 1), WH); c.put(fm, B); c.put(fm, WH, hatch(100, 9, 1))            # gaskets
spm = spars.mask(0.4); c.put(spm, WH)
# the black flag at the main truck
fx, fy = XM(138) + 3, 122
c.hair([(fx, 138), (fx, fy - 2)], WH)
flag = c.layer().poly(smooth([(fx, fy), (fx + 9, fy + 2), (fx + 18, fy - 1), (fx + 18, fy + 11), (fx + 9, fy + 14), (fx, fy + 12)], n=4)).mask()
c.put(grow(flag, 1), WH); c.put(flag, K); c.put(c.layer().circle(fx + 9, fy + 5, 2.6).mask(), WH); px(fx + 7, fy + 9, fx + 12, fy + 10, WH)
px(int(fx + 8), fy + 4, int(fx + 9), fy + 5, K); px(int(fx + 10), fy + 4, int(fx + 11), fy + 5, K)
# riding light on the forestay, and the watch's lantern on deck
for lx, ly, r in ((292, 330, 26), (196, 408, 16)):
    d = np.hypot(XX - lx, YY - ly)
    c.put(((d % 6) < 4.5 * np.clip(1 - d / r, 0, 1) ** 1.2) & (d < r) & (c.a == K), Y, checker(1))
    px(lx - 2, ly - 3, lx + 3, ly + 4, Y); px(lx - 1, ly - 1, lx + 2, ly + 2, WH); c.hair([(lx - 2, ly - 4), (lx + 2, ly - 4)], WH)
px(292, 318, 293, 327, WH)
# two of the watch, drunk and quarrelling by the lantern
for x, lean in ((186, 1), (206, -1)):
    yb = int(decky(x)) - 4
    px(x - 2, yb - 9, x + 2, yb, K); px(x - 2, yb - 9, x + 2, yb - 4, R if lean > 0 else WH); px(x - 1, yb - 13, x + 2, yb - 10, WH); px(x - 2, yb - 15, x + 3, yb - 13, R if lean < 0 else K)
# anchor cable
cab = c.layer(1); cab.line(bez((298, 424), (310, 432), (322, 440), (334, WL + 4)), 1); c.put(cab.mask(), WH, checker(1) | hatch(0, 2, 1))

# reflections: hull as broken bars, masts as shivered lines, lights as dashes
for yy in range(WL + 2, WL + 34, 2):
    f = (yy - WL) / 34.0
    for _ in range(int(9 * (1 - f)) + 1):
        x = random.uniform(112 + 30 * f, 286 - 30 * f); ln = random.uniform(4, 14)
        px(int(x), yy, int(x + ln), yy + 1, B)
for x in (MAIN, FORE):
    for yy in range(WL + 4, WL + 110, 3):
        if random.random() < 0.8 - (yy - WL) / 160.0: px(int(x + 4 * math.sin(yy * 0.35) + random.uniform(-1, 1)), yy, int(x + 4 * math.sin(yy * 0.35)) + 3, yy + 1, WH)
for x, col in ((108, Y), (196, Y), (292, Y)):
    for yy in range(WL + 3, WL + 40, 3):
        if random.random() < 0.75: px(int(x + random.uniform(-3, 1)), yy, int(x + random.uniform(2, 5)), yy + 1, col)
c.put((YY == WL) & hm, WH)

# ---- Jim in the coracle --------------------------------------------------------------------------
jx, jy = 58, 500
cor = c.layer().poly(smooth([(jx - 15, jy - 4), (jx + 15, jy - 4), (jx + 11, jy + 5), (jx - 11, jy + 5)], n=5)).mask()
c.put(grow(cor, 1), WH); c.put(cor, K); c.put(cor, WH, cross(45, 4, 1))
c.put(c.layer().circle(jx - 1, jy - 15, 3.6).poly([(jx - 5, jy - 4), (jx - 4, jy - 12), (jx + 3, jy - 12), (jx + 5, jy - 4)]).mask(), WH)
px(jx - 5, jy - 19, jx + 3, jy - 17, B)
c.line([(jx + 3, jy - 10), (jx + 14, jy - 6), (jx + 22, jy + 6)], WH, 1.4); c.put(c.layer().ellipse(jx + 23, jy + 8, 2.2, 4).mask(), WH)
rp_ = c.layer(1)
for k, r in enumerate((20, 27, 35)): rp_.line(arc(jx, jy + 6, r, r * 0.22, 10 + k * 8, 170 - k * 8), 1)
c.put(rp_.mask(), WH, hatch(90, 4, 3))

# ---- Requiem ------------------------------------------------------------------------------------------
c.put((YY >= 562), K); c.put((YY == 562), B)
c.text(200, 574, "Home is the sailor, home from sea,", WH, "lib-i", 12)
c.text(200, 589, "And the hunter home from the hill.", WH, "lib-i", 12)
c.save("p5.png")
