# Evening — "The Lamplighter" (A Child's Garden of Verses). "For we are very lucky, with a
# lamp before the door, / And Leerie stops to light it as he lights so many more."
# 17 Heriot Row at teatime: a New Town terrace drawn stone by stone, pane by pane; one lamp
# lit, one being lit, one still dark; a child at the first-floor window.
import math, random
import numpy as np
from kit import *
random.seed(17); c = Canvas(Y)
def px(x0, y0, x1, y1, col, pat=None): c.put(c.layer(1).rect(x0, y0, x1, y1).mask(), col, pat)

# ---- afterglow --------------------------------------------------------------------------
n = np.sin(XX / 37.0 + YY / 9.0) + 0.7 * np.sin(XX / 17.0 - YY / 13.0 + 1) + 0.5 * np.sin(XX / 61.0 + 3)
t = np.clip(0.75 - YY / 150.0 * 0.9 + 0.22 * n, 0, 0.92)
c.put(YY < 190, R, ((YY % 5) / 5.0) < t)
c.put((YY < 190) & (t < 0.12) & (n > 0.9), WH, hatch(0, 5, 2))
for x, y, s in ((300, 46, 1), (318, 38, 0.8), (282, 60, 0.9), (336, 54, 0.7), (120, 30, 0.8), (104, 40, 0.6)):   # rooks going home
    c.line([(x - 6 * s, y - 2 * s), (x - 2 * s, y - 4 * s), (x, y), (x + 3 * s, y - 4 * s), (x + 7 * s, y - 1 * s)], K, 1.5)

# ---- roof, chimneys -----------------------------------------------------------------------
EAVE, PAVE, KERB = 188, 472, 508
for x0 in (22, 186, 350):                                    # chimney stacks with cans
    px(x0 - 2, 98, x0 + 34, 160, K); px(x0, 100, x0 + 32, 160, B)
    for yy in range(108, 160, 8): c.hair([(x0, yy), (x0 + 31, yy)], K)
    px(x0 - 3, 96, x0 + 35, 100, K); px(x0 - 2, 97, x0 + 34, 98, WH)
    for k in range(4):
        px(x0 + 1 + k * 8, 82, x0 + 7 + k * 8, 96, K); px(x0 + 2 + k * 8, 83, x0 + 6 + k * 8, 96, R); c.hair([(x0 + 1 + k * 8, 86), (x0 + 6 + k * 8, 86)], K)
    for k in (0, 2):                                         # teatime smoke
        sm = smooth([(x0 + 4 + k * 8, 80), (x0 + 10 + k * 8, 66), (x0 + 3 + k * 8, 52), (x0 + 14 + k * 8, 36), (x0 + 8 + k * 8, 20)], closed=False)
        c.line(sm, K, 2.2, pat=checker(1))
px(0, 150, W, EAVE, K)
sl = c.layer(1)
for j, yy in enumerate(range(153, EAVE - 6, 6)):
    sl.seg(0, yy, W, yy)
    for x in range(-(j % 2) * 5, W, 10): sl.seg(x, yy, x, yy + 6)
sl.put(B)
px(0, EAVE - 8, W, EAVE, K); px(0, EAVE - 6, W, EAVE - 2, WH)
for x in range(2, W, 7): px(x, EAVE - 2, x + 3, EAVE + 2, WH)      # dentils
c.hair([(0, EAVE - 2), (W, EAVE - 2)], K)

# ---- ashlar front ----------------------------------------------------------------------------
c.put((YY >= EAVE) & (YY < PAVE), B)
st = c.layer(1)
for j, yy in enumerate(range(EAVE + 12, 372, 13)):
    st.seg(0, yy, W, yy)
    for x in range(-(j % 2) * 17, W, 34): st.seg(x, yy - 13, x, yy)
st.put(K)
px(0, 372, W, 378, K); px(0, 373, W, 376, WH)                 # band course
ru = c.layer(1)                                               # rusticated ground floor
for j, yy in enumerate(range(378, PAVE, 16)):
    ru.rect(0, yy, W, yy + 2)
    for x in range(-(j % 2) * 20, W, 40): ru.rect(x, yy, x + 2, yy + 16)
ru.put(K)

BAYS = [50, 150, 250, 350]
def window(cx, y0, y1, w=36, lit=False, rows=4, blind=0.0, drapes=None):
    x0, x1 = cx - w // 2, cx + w // 2
    px(x0 - 5, y0 - 5, x1 + 5, y1 + 2, K); px(x0 - 4, y0 - 4, x1 + 4, y1 + 1, WH)       # architrave
    px(x0 - 1, y0 - 1, x1 + 1, y1 + 1, K)
    px(x0, y0, x1, y1, Y if lit else K)
    if not lit: c.put(c.layer(1).rect(x0, y0, x1, y1).mask(), B, hatch(45, 4, 1))
    return x0, x1
def bars(cx, y0, y1, w=36, lit=False, rows=4):
    x0, x1 = cx - w // 2, cx + w // 2; col = K if lit else WH
    for k in range(1, 3): c.hair([(x0 + k * w / 3, y0), (x0 + k * w / 3, y1 - 1)], col)
    for k in range(1, rows): c.hair([(x0, y0 + k * (y1 - y0) / rows), (x1 - 1, y0 + k * (y1 - y0) / rows)], col)
    ym = y0 + (y1 - y0) / 2; px(x0, ym - 1, x1, ym + 1, col)
    px(x0 - 7, y1 + 2, x1 + 7, y1 + 6, K); px(x0 - 6, y1 + 2, x1 + 6, y1 + 5, WH)       # sill
def drape(cx, y0, y1, w, col=R):
    x0, x1 = cx - w // 2, cx + w // 2
    for sgn, xa in ((1, x0), (-1, x1)):
        m = c.layer().poly([(xa, y0), (xa + sgn * 11, y0), (xa + sgn * 9, y0 + (y1 - y0) * 0.5), (xa + sgn * 4, y0 + (y1 - y0) * 0.72), (xa + sgn * 8, y1), (xa, y1)]).mask()
        c.put(m, col); c.put(m, K, hatch(90, 3, 1))

lit2 = [False, True, False, True]; lit1 = [True, False, True, True]; lit0 = [True, None, True, False]
# second floor
for i, cx in enumerate(BAYS):
    y0, y1 = 204, 258
    window(cx, y0, y1, 34, lit2[i])
    if lit2[i]:
        if i == 1:   # a blind half down, a geranium on the sill
            px(cx - 17, y0, cx + 17, y0 + 22, WH); c.hair([(cx - 17, y0 + 22), (cx + 16, y0 + 22)], K); c.hair([(cx, y0 + 22), (cx, y0 + 27)], K)
            px(cx - 12, y1 - 6, cx - 5, y1, R); c.put(c.layer().circle(cx - 9, y1 - 11, 5).mask(), G); c.put(c.layer().circle(cx - 11, y1 - 13, 1.5).circle(cx - 6, y1 - 10, 1.5).mask(), R)
        if i == 3:   # someone dressing a lamp
            drape(cx, y0, y1, 34, G)
            c.put(c.layer().circle(cx + 2, y0 + 26, 5).poly([(cx - 5, y1), (cx - 3, y0 + 33), (cx + 7, y0 + 33), (cx + 10, y1)]).mask(), K)
    bars(cx, y0, y1, 34, lit2[i])
# first floor: the tall drawing-room windows with their balconies
for i, cx in enumerate(BAYS):
    y0, y1 = 280, 356
    window(cx, y0, y1, 38, lit1[i])
    px(cx - 26, y0 - 12, cx + 26, y0 - 6, K); px(cx - 25, y0 - 11, cx + 25, y0 - 8, WH)   # cornice over
    if lit1[i]:
        drape(cx, y0, y1, 38, R)
        if i == 2:   # the child: nose to the glass
            c.put(c.layer().circle(cx, y1 - 26, 7.5).poly(smooth([(cx - 12, y1), (cx - 10, y1 - 14), (cx - 4, y1 - 19), (cx + 4, y1 - 19), (cx + 10, y1 - 14), (cx + 12, y1)])).mask(), K)
            c.put(c.layer().ellipse(cx - 10, y1 - 8, 3, 4).ellipse(cx + 11, y1 - 9, 3, 4).mask(), K)     # hands on the pane
        if i == 0:   # a standard lamp and the corner of a picture
            px(cx - 4, y0 + 30, cx + 6, y0 + 42, R); px(cx, y0 + 42, cx + 2, y1, K); px(cx - 14, y0 + 8, cx - 2, y0 + 22, K); px(cx - 12, y0 + 10, cx - 4, y0 + 20, WH)
        if i == 3:   # a piano player
            c.put(c.layer().circle(cx - 4, y1 - 34, 5.5).poly([(cx - 11, y1), (cx - 9, y1 - 26), (cx + 1, y1 - 27), (cx + 4, y1 - 14), (cx + 12, y1 - 13), (cx + 12, y1)]).mask(), K)
            c.put(c.layer().circle(cx - 6, y1 - 39, 4).mask(), K)
    bars(cx, y0, y1, 38, lit1[i], 4)
    # balcony ironwork
    b = c.layer(1)
    b.rect(cx - 25, y1 + 6, cx + 25, y1 + 8); b.rect(cx - 25, y1 - 12, cx + 25, y1 - 11)
    for x in range(cx - 24, cx + 25, 4): b.seg(x, y1 - 12, x, y1 + 6)
    for x in range(cx - 20, cx + 21, 8): b.ellipse(x, y1 - 3, 3, 5, 255)
    m = b.mask(); c.put(m, K)
# ground floor
for i, cx in enumerate(BAYS):
    if lit0[i] is None: continue
    y0, y1 = 392, 446
    window(cx, y0, y1, 38, lit0[i])
    if lit0[i]:
        if i == 2:   # tea is nearly ready
            px(cx - 16, y1 - 9, cx + 16, y1 - 7, K)
            c.put(c.layer().ellipse(cx - 4, y1 - 14, 6, 5).poly([(cx + 1, y1 - 15), (cx + 8, y1 - 19), (cx + 8, y1 - 17), (cx + 2, y1 - 12)]).ring(cx - 11, y1 - 14, 3, 1.2).rect(cx - 6, y1 - 21, cx - 2, y1 - 18).mask(0.4), K)
            px(cx + 9, y1 - 12, cx + 14, y1 - 9, K)
            for sx in (cx - 2, cx + 4): c.line(smooth([(sx + 6, y1 - 21), (sx + 8, y1 - 26), (sx + 5, y1 - 30), (sx + 8, y1 - 35)], closed=False), K, 1, pat=checker(1))
            drape(cx, y0, y1, 38, R)
        if i == 0:   # a cat on the inside sill
            c.put(c.layer().ellipse(cx + 2, y1 - 6, 8, 6).circle(cx - 5, y1 - 14, 4.5).poly([(cx - 9, y1 - 16), (cx - 8, y1 - 22), (cx - 5, y1 - 17)]).poly([(cx - 4, y1 - 17), (cx - 1, y1 - 22), (cx - 1, y1 - 15)]).mask(), K)
            c.line(bez((cx + 9, y1 - 3), (cx + 15, y1 - 4), (cx + 15, y1 - 12), (cx + 12, y1 - 14)), K, 1.6)
            drape(cx, y0, y1, 38, B)
    bars(cx, y0, y1, 38, lit0[i], 4)

# ---- the door of No. 17 -------------------------------------------------------------------------
dx = BAYS[1]
px(dx - 30, 380, dx + 30, PAVE, K); px(dx - 28, 382, dx + 28, PAVE, WH)
for sx in (-1, 1):                                             # pilasters
    px(dx + sx * 24 - 4, 386, dx + sx * 24 + 4, PAVE, K); px(dx + sx * 24 - 3, 387, dx + sx * 24 + 3, PAVE - 1, WH)
    c.hair([(dx + sx * 24 - 1, 390), (dx + sx * 24 - 1, PAVE - 4)], K); c.hair([(dx + sx * 24 + 1, 390), (dx + sx * 24 + 1, PAVE - 4)], K)
fan = c.layer().poly([(dx - 17, 410)] + arc(dx, 410, 17, 16, 180, 360) + [(dx + 17, 410)]).mask()
c.put(grow(fan, 1), K); c.put(fan, Y)
fb = c.layer(1)
for a in range(210, 340, 30): fb.seg(dx, 410, dx + 18 * math.cos(math.radians(a)), 410 + 17 * math.sin(math.radians(a)))
fb.line(arc(dx, 410, 8, 7.5, 180, 360), 1)
c.put(fb.mask() & fan, K)
px(dx - 18, 411, dx + 18, 414, K)
px(dx - 17, 414, dx + 17, PAVE - 2, K); px(dx - 15, 416, dx + 15, PAVE - 2, R)
for (a, b_, cc, d) in ((dx - 12, 420, dx - 2, 438), (dx + 2, 420, dx + 12, 438), (dx - 12, 442, dx - 2, 464), (dx + 2, 442, dx + 12, 464)):
    c.hair([(a, b_), (cc, b_), (cc, d), (a, d)], K, closed=True)
c.put(c.layer().circle(dx + 10, 440, 2.2).mask(), Y); px(dx - 5, 439, dx + 3, 441, Y)       # knob, letter-box
c.text(dx, 403, "17", K, "dserif-b", 9)
# steps and area railings
for k in range(3):
    px(dx - 30 - k * 3, PAVE - 9 + k * 3 + 3, dx + 30 + k * 3, PAVE - 9 + k * 3 + 6, K); px(dx - 29 - k * 3, PAVE - 9 + k * 3 + 3, dx + 29 + k * 3, PAVE - 9 + k * 3 + 5, WH)
rl = c.layer(1)
for x in list(range(2, dx - 36, 6)) + list(range(dx + 40, W, 6)):
    rl.seg(x, 430, x, PAVE); rl.poly([(x - 1.5, 430), (x, 425), (x + 1.5, 430)])
rl.rect(0, 432, dx - 34, 434); rl.rect(dx + 38, 432, W, 434); rl.rect(0, PAVE - 5, dx - 34, PAVE - 3); rl.rect(dx + 38, PAVE - 5, W, PAVE - 3)
rm = rl.mask(); c.put(grow(rm, 1) & (YY < PAVE) & (YY > 428), B, checker(1)); c.put(rm, K)

# ---- pavement, kerb, setts ------------------------------------------------------------------------
c.put((YY >= PAVE) & (YY < KERB), WH)
pv = c.layer(1)
for j, yy in enumerate((PAVE, PAVE + 10, PAVE + 22)):
    pv.seg(0, yy, W, yy)
    for x in range(-(j % 2) * 22, W, 44): pv.seg(x, yy, x - 3, (PAVE + 10, PAVE + 22, KERB)[j])
pv.put(K)
px(0, KERB - 2, W, KERB + 3, K); px(0, KERB - 1, W, KERB + 1, WH)
c.put(YY >= KERB + 3, K)
LAMPS = [(100, True), (206, None), (300, False)]
sett = np.zeros((H, W), bool); warm = np.zeros((H, W), bool)
row = 0; y = KERB + 6
setts = c.layer(2); settw = c.layer(2)
while y < H:
    hh = 5 + row * 0.9; wdt = 9 + row * 1.7
    x = -wdt * (0.5 if row % 2 else 0) - random.uniform(0, 2)
    while x < W:
        w_ = wdt * random.uniform(0.8, 1.15)
        d = min(abs(x + w_ / 2 - lx) + (y - KERB) * 0.9 for lx, s_ in LAMPS if s_)
        tgt = settw if d < 62 and random.random() < 1.25 - d / 62 else setts
        tgt.poly(smooth([(x + 1, y + 1), (x + w_ - 1, y + 1), (x + w_ - 1, y + hh - 1), (x + 1, y + hh - 1)], n=3))
        x += w_ + 1.2
    y += hh + 1.5; row += 1
setts.put(B); settw.put(Y)

# ---- lamps ------------------------------------------------------------------------------------------------
def lamp(x, state):
    top = 372
    if state:                                                # light falling on the stone and the flags
        d = np.hypot(XX - x, (YY - (top + 14)) * 0.9)
        ringp = ((d % 7) < 6.2 * np.clip(1 - d / 84.0, 0, 1) ** 1.3) & (d < 84)
        c.put(ringp & (c.a == B), Y)
        c.put(ringp & (c.a == K) & (YY < PAVE) & (d < 50), Y, checker(1))
    post = c.layer()
    post.poly([(x - 2, top + 30), (x + 2, top + 30), (x + 2.6, KERB - 14), (x - 2.6, KERB - 14)])
    post.poly([(x - 5, KERB - 14), (x + 5, KERB - 14), (x + 6, KERB), (x - 6, KERB)])
    post.rect(x - 13, top + 37, x + 13, top + 40); post.circle(x - 13, top + 38.5, 2.2); post.circle(x + 13, top + 38.5, 2.2)   # ladder bar
    post.ellipse(x, top + 30, 5, 2.5); post.ellipse(x, top + 50, 4, 2)
    post.poly([(x - 6, top + 27), (x - 11, top + 4), (x + 11, top + 4), (x + 6, top + 27)])
    post.poly([(x - 12, top + 4), (x, top - 6), (x + 12, top + 4)]); post.rect(x - 2, top - 11, x + 2, top - 5); post.circle(x, top - 13, 2.6)
    pm = post.mask(); c.put(grow(pm, 1) & (YY < KERB + 1), WH if state is not True else K); c.put(pm, K)
    glass = c.layer().poly([(x - 4.5, top + 25), (x - 8.5, top + 6), (x + 8.5, top + 6), (x + 4.5, top + 25)]).mask()
    if state is True:
        c.put(glass, Y); c.put(c.layer().ellipse(x, top + 16, 2.5, 6).mask(), WH); c.put(c.layer().ellipse(x, top + 18, 1.2, 3).mask(), R)
    elif state is None:
        c.put(glass, WH); c.put(c.layer().ellipse(x, top + 18, 1.6, 3.5).mask(), Y)
    else:
        c.put(glass, B); c.put(glass, WH, hatch(45, 4, 1))
    c.hair([(x, top + 6), (x, top + 25)], K)
    c.put(c.layer(1).seg(x - 1, top + 60, x - 1, KERB - 16).mask(), WH)       # a highlight down the post
for x, s_ in LAMPS: lamp(x, s_)

# ---- Leerie on his ladder ---------------------------------------------------------------------------------
lx = 206; top = 372
la, lb = (lx + 30, KERB - 1), (lx + 9, top + 38)
lad = c.layer()
off = 7
lad.seg(la[0], la[1], lb[0], lb[1], 1.6); lad.seg(la[0] + off, la[1], lb[0] + off, lb[1] - 2, 1.6)
for k in range(1, 12):
    f = k / 12; lad.seg(la[0] + (lb[0] - la[0]) * f, la[1] + (lb[1] - la[1]) * f, la[0] + off + (lb[0] - la[0]) * f, la[1] + (lb[1] - 2 - la[1]) * f, 1.2)
lm = lad.mask(0.35); c.put(grow(lm, 1), K); c.put(lm, WH)
fx, fy = lx + 23, 452                                       # his feet on the fourth rung
body = c.layer()
body.poly([(fx - 1, fy), (fx + 6, fy), (fx + 4, fy - 20), (fx - 4, fy - 20)])            # legs
body.poly([(fx - 4, fy), (fx + 9, fy), (fx + 9, fy + 3), (fx - 4, fy + 3)])               # boots
body.poly(smooth([(fx - 7, fy - 18), (fx - 9, fy - 40), (fx - 3, fy - 47), (fx + 5, fy - 45), (fx + 8, fy - 30), (fx + 7, fy - 16)]))   # greatcoat
body.line([(fx - 6, fy - 42), (fx - 13, fy - 52), (lx + 2, top + 22)], 3.2)             # the reaching arm
body.line([(fx + 5, fy - 40), (fx + 6, fy - 30), (fx + 1, fy - 24)], 3)                 # the arm that holds on
body.circle(fx - 2, fy - 52, 5.2)
body.poly([(fx - 8, fy - 55), (fx + 4, fy - 55), (fx + 3, fy - 60), (fx - 6, fy - 60)]); body.poly([(fx - 12, fy - 54), (fx - 6, fy - 56), (fx - 6, fy - 54)])   # cap and peak
bm = body.mask(0.45); c.put(grow(bm, 1), WH); c.put(bm, K)
c.put(c.layer().poly([(fx - 6, fy - 49), (fx - 1, fy - 50), (fx - 4, fy - 46)]).mask(), WH)                    # a lit cheek
c.put(c.layer().line([(fx - 5, fy - 46), (fx + 3, fy - 45), (fx + 6, fy - 38)], 2.4).mask(0.4), R)             # muffler
c.put(c.layer(1).seg(fx - 5, fy - 36, fx - 4, fy - 20).seg(fx + 1, fy - 40, fx + 1, fy - 22).mask(), WH, hatch(0, 3, 2))  # coat seam, buttons
c.put(c.layer().circle(lx + 2, top + 21, 2.4).mask(), Y); c.put(c.layer(1).rect(lx + 1, top + 20, lx + 3, top + 22).mask(), R)  # the taper's spark
sp = c.layer(1)
for a in range(0, 360, 45): sp.seg(lx + 2 + 5 * math.cos(math.radians(a)), top + 21 + 5 * math.sin(math.radians(a)), lx + 2 + 8 * math.cos(math.radians(a)), top + 21 + 8 * math.sin(math.radians(a)))
c.put(sp.mask() & ~bm, Y)
# his lantern, hung on the ladder
px(la[0] - 8, KERB - 30, la[0] - 1, KERB - 19, K); px(la[0] - 7, KERB - 28, la[0] - 2, KERB - 20, Y); c.hair([(la[0] - 5, KERB - 30), (la[0] - 5, KERB - 34)], K)

# ---- passers-by -----------------------------------------------------------------------------------------------
gx, gy = 344, KERB - 3                                      # a gentleman going home to his tea
g = c.layer()
g.rect(gx - 4, gy - 44, gx + 4, gy - 34); g.rect(gx - 6, gy - 35, gx + 6, gy - 33); g.circle(gx, gy - 29, 4)
g.poly(smooth([(gx - 6, gy - 24), (gx + 6, gy - 24), (gx + 8, gy - 6), (gx - 8, gy - 6)], n=4)); g.poly([(gx - 5, gy - 7), (gx - 1, gy - 7), (gx - 2, gy), (gx - 7, gy)]); g.poly([(gx + 1, gy - 7), (gx + 5, gy - 7), (gx + 8, gy), (gx + 3, gy)])
g.seg(gx + 9, gy - 18, gx + 13, gy, 1.2)
gm = g.mask(0.45); c.put(grow(gm, 1), WH); c.put(gm, K)
kx, ky = 40, KERB - 4                                      # the street cat
k_ = c.layer(); k_.ellipse(kx, ky - 5, 8, 4.5); k_.circle(kx - 8, ky - 9, 3.5); k_.poly([(kx - 11, ky - 10), (kx - 11, ky - 15), (kx - 8, ky - 12)]); k_.poly([(kx - 7, ky - 12), (kx - 5, ky - 15), (kx - 5, ky - 10)])
k_.line(bez((kx + 7, ky - 5), (kx + 14, ky - 6), (kx + 13, ky - 14), (kx + 16, ky - 17)), 1.6)
for lx_ in (-5, -2, 4, 6): k_.seg(kx + lx_, ky - 3, kx + lx_, ky + 2, 1.5)
km = k_.mask(0.4); c.put(km, K); px(kx - 10, ky - 10, kx - 9, ky - 9, Y)

# ---- the line itself ---------------------------------------------------------------------------------------------
c.put(YY >= 580, WH); c.put((YY >= 578) & (YY < 580), K)
c.text(200, 590, "And O! before you hurry by with ladder and with light", K, "lib-i", 12)
c.save("p4.png")
