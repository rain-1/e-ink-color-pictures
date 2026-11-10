"""Evening: Lighting-Up Time. A terrace of three houses at dusk, every window a small
scene, a lamplighter at work, and the line of beauty in the chimney smoke."""
import math, random
from kit import *
rnd = random.Random(1697)
im, d = canvas(B)

# ---------- sky: hatched dusk, stars, thin moon
for y in range(0, 150, 3):
    amp = max(0, (y - 60) / 90)
    if amp > 0:
        for x in range(0, 400, 4):
            if rnd.random() < amp * 0.55:
                line(d, [(x, y), (x + 3, y)], Y, 0.7)
for _ in range(60):
    x, y = rnd.uniform(0, 400), rnd.uniform(0, 90)
    r = rnd.choice([0.5, 0.5, 0.8, 1.1])
    circ(d, x, y, r, Wh)
circ(d, 338, 38, 13, Wh); circ(d, 333, 35, 12.5, B)          # two-day-old crescent
# a slow Taurid
line(d, [(52, 22), (96, 40)], Wh, 0.7); line(d, [(80, 33.5), (96, 40)], Y, 1.2)

def smoke(x, y, h, amp, col=Wh):
    for k in range(3):
        pts = []
        for i in range(60):
            t = i / 59
            yy = y - h * t
            xx = x + (amp * (0.3 + t)) * math.sin(t * 2 * math.pi * 1.25 + k * 0.5) + k * 2.2 * t * 3 + 14 * t * t
            pts.append((xx, yy))
        line(d, pts, col, 1.1 - 0.25 * k)

# ---------- houses
houses = [  # x0, x1, roof-eave y, style
    (0, 128, 150, "brick"), (128, 272, 118, "stucco"), (272, 400, 162, "brick2")]
GROUND = 528

def brick(x0, y0, x1, y1, base, mortar, dark=False):
    rect(d, x0, y0, x1, y1, base)
    row = 0
    y = y0
    while y < y1:
        line(d, [(x0, y), (x1, y)], mortar, 0.4)
        off = 0 if row % 2 else 5
        x = x0 + off
        while x < x1:
            line(d, [(x, y), (x, min(y + 5, y1))], mortar, 0.4)
            if rnd.random() < (0.07 if not dark else 0.2):
                rect(d, x + 0.6, y + 0.6, min(x + 9.4, x1), min(y + 4.4, y1), K if rnd.random() < .6 else Y if not dark else K)
            x += 10
        y += 5; row += 1

def roof(x0, x1, eave, pitch, col):
    ridge = eave - pitch
    poly(d, [(x0, eave), (x0 + 10, ridge), (x1 - 10, ridge), (x1, eave)], col)
    # tiles
    for j, y in enumerate(range(int(ridge) + 4, int(eave), 4)):
        t = (y - ridge) / pitch
        xa, xb = x0 + 10 * (1 - t), x1 - 10 * (1 - t)
        line(d, [(xa, y), (xb, y)], K, 0.5)
        x = xa + (2 if j % 2 else 5)
        while x < xb:
            line(d, [(x, y), (x, y + 4)], K, 0.4); x += 6
    line(d, [(x0 + 10, ridge), (x1 - 10, ridge)], K, 1.5)
    line(d, [(x0, eave), (x1, eave)], K, 2)
    return ridge

def chimney(x, top, base, n=2, lit=True):
    rect(d, x, top + 6, x + 8 * n + 4, base, R, K, 0.8)
    for y in range(int(top) + 9, int(base), 3):
        line(d, [(x, y), (x + 8 * n + 4, y)], K, 0.3)
    rect(d, x - 2, top + 3, x + 8 * n + 6, top + 7, Wh, K, 0.6)
    for i in range(n):
        rect(d, x + 3 + 8 * i, top - 4, x + 9 + 8 * i, top + 3, Y, K, 0.6)
    return [(x + 6 + 8 * i, top - 4) for i in range(n)]

def window(x, y, w, h, scene, lit):
    glass = Y if lit else K
    rect(d, x - 3, y - 3, x + w + 3, y + h + 3, Wh, K, 0.7)             # surround
    rect(d, x, y, x + w, y + h, glass)
    fg = K if lit else B
    cx, by = x + w / 2, y + h
    if scene == "person":
        hx = cx + rnd.uniform(-4, 4)
        circ(d, hx, by - 20, 4.5, fg); poly(d, [(hx - 9, by), (hx - 7, by - 13), (hx + 7, by - 13), (hx + 9, by)], fg)
    elif scene == "pair":
        for dx, hh in ((-5, 21), (5, 18)):
            circ(d, cx + dx, by - hh, 3.8, fg); poly(d, [(cx + dx - 6, by), (cx + dx - 5, by - hh + 5), (cx + dx + 5, by - hh + 5), (cx + dx + 6, by)], fg)
    elif scene == "cat":
        poly(d, [(cx - 6, by), (cx - 6, by - 9), (cx - 3, by - 14), (cx + 3, by - 14), (cx + 5, by - 8), (cx + 6, by)], fg)
        circ(d, cx, by - 16, 4, fg); poly(d, [(cx - 4, by - 18), (cx - 3.5, by - 23), (cx - 1, by - 19)], fg); poly(d, [(cx + 4, by - 18), (cx + 3.5, by - 23), (cx + 1, by - 19)], fg)
        line(d, [(cx + 6, by - 1), (cx + 10, by - 3), (cx + 9, by - 8)], fg, 1.3)
    elif scene == "plant":
        poly(d, [(cx - 5, by), (cx - 6, by - 7), (cx + 6, by - 7), (cx + 5, by)], R if lit else fg, K, 0.5)
        for a in range(-70, 71, 20):
            ex, ey = cx + 14 * math.sin(math.radians(a)), by - 7 - 17 * math.cos(math.radians(a))
            line(d, bez((cx, by - 7), (cx, by - 16), (ex, ey - 4), (ex, ey), 8), G, 1.4)
            ell(d, ex, ey, 2.4, 1.6, G)
    elif scene == "candle":
        rect(d, cx - 1.5, by - 14, cx + 1.5, by, Wh if not lit else fg); ell(d, cx, by - 18, 2, 4, Y if not lit else R)
        if not lit:
            for a in range(0, 360, 30):
                line(d, [(cx + 7 * math.cos(math.radians(a)), by - 18 + 7 * math.sin(math.radians(a))), (cx + 10 * math.cos(math.radians(a)), by - 18 + 10 * math.sin(math.radians(a)))], Y, 0.6)
    elif scene == "cage":
        ell(d, cx, by - 22, 8, 9, None, fg, 0.9); rect(d, cx - 8, by - 22, cx + 8, by - 8, None, fg, 0.9)
        for dx in (-5, -2.5, 0, 2.5, 5): line(d, [(cx + dx, by - 30), (cx + dx, by - 8)], fg, 0.5)
        ell(d, cx, by - 14, 3, 2.2, R if lit else Y); line(d, [(cx, by - 31), (cx, y)], fg, 0.6)
    elif scene == "fiddler":
        circ(d, cx - 2, by - 24, 4, fg); poly(d, [(cx - 9, by), (cx - 8, by - 18), (cx + 4, by - 18), (cx + 6, by)], fg)
        line(d, [(cx + 1, by - 19), (cx + 12, by - 25)], fg, 2.4); line(d, [(cx + 3, by - 12), (cx + 13, by - 30)], fg, 0.7)
    elif scene == "easel":
        line(d, [(cx + 2, by), (cx + 6, by - 28), (cx + 11, by)], fg, 0.9); rect(d, cx, by - 26, cx + 12, by - 10, Wh, fg, 0.7)
        line(d, scurve(cx + 6, by - 24, 12, 3, 12), R, 1.0)
        circ(d, cx - 8, by - 20, 3.6, fg); poly(d, [(cx - 13, by), (cx - 12, by - 15), (cx - 4, by - 15), (cx - 3, by)], fg); line(d, [(cx - 5, by - 13), (cx + 1, by - 17)], fg, 1)
    elif scene == "curtain":
        for sx in (-1, 1):
            pts = [(cx + sx * w / 2, y)] + [(cx + sx * (w / 2 - (w * 0.42) * (1 - (i / 10) ** 0.6)), y + h * i / 10) for i in range(11)] + [(cx + sx * w / 2, by)]
            poly(d, pts, R if lit else Wh)
            for k in range(1, 4):
                line(d, [(cx + sx * (w / 2 - k * 2.2), y), (cx + sx * (w / 2 - k * 1.2), by)], K, 0.35)
    elif scene == "blind":
        rect(d, x, y, x + w, y + h * 0.7, Wh)
        for yy in range(int(y) + 2, int(y + h * 0.7), 3): line(d, [(x, yy), (x + w, yy)], fg if lit else K, 0.4)
        line(d, [(cx, y + h * 0.7), (cx, y + h * 0.7 + 5)], fg, 0.5); circ(d, cx, y + h * 0.7 + 6, 1.2, fg)
    elif scene == "bottles":
        line(d, [(x, by - 14), (x + w, by - 14)], fg, 0.8)
        for i in range(4):
            bx = x + 4 + i * (w - 8) / 3
            for yy, c in ((by, G), (by - 14, B if lit else Wh)):
                rect(d, bx - 2, yy - 9, bx + 2, yy, c if lit else fg); rect(d, bx - 0.8, yy - 13, bx + 0.8, yy - 9, c if lit else fg)
    elif scene == "reader":
        circ(d, cx - 3, by - 17, 4.2, fg); poly(d, [(cx - 10, by), (cx - 9, by - 11), (cx + 3, by - 11), (cx + 5, by)], fg)
        poly(d, [(cx + 2, by - 9), (cx + 11, by - 12), (cx + 11, by - 4), (cx + 2, by - 1)], Wh, fg, 0.6)
    # sash bars and sill
    line(d, [(x, y + h / 2), (x + w, y + h / 2)], Wh, 1.6)
    for i in (1, 2): line(d, [(x + w * i / 3, y), (x + w * i / 3, y + h)], Wh, 0.8)
    line(d, [(x, y + h / 4), (x + w, y + h / 4)], Wh, 0.6); line(d, [(x, y + 3 * h / 4), (x + w, y + 3 * h / 4)], Wh, 0.6)
    rect(d, x, y, x + w, y + h, None, K, 0.6)
    rect(d, x - 5, y + h + 3, x + w + 5, y + h + 7, Wh, K, 0.6)
    # flat brick arch
    for i in range(9):
        t = i / 8 - 0.5
        line(d, [(x - 3 + (w + 6) * i / 8, y - 3), (x - 3 + (w + 6) * i / 8 + t * 5, y - 10)], K, 0.5)

scenes_lit = ["person", "pair", "cat", "plant", "cage", "fiddler", "easel", "curtain", "bottles", "reader", "person", "plant"]
scenes_dark = ["blind", "curtain", "candle", "cat", "plant", "candle"]
rnd.shuffle(scenes_lit)
si = 0
smoke_src = []
for hi, (x0, x1, eave, style) in enumerate(houses):
    # roof + chimneys (drawn first so façade overlaps)
    ridge = roof(x0, x1, eave, 34, K if style != "stucco" else B)
    if style == "stucco":
        # dormer
        for dx in (x0 + 40, x1 - 62):
            poly(d, [(dx - 3, eave - 4), (dx + 11, eave - 30), (dx + 25, eave - 4)], Wh, K, 0.8)
            rect(d, dx + 3, eave - 20, dx + 19, eave - 4, Y, K, 0.7); line(d, [(dx + 11, eave - 20), (dx + 11, eave - 4)], K, 0.6); line(d, [(dx + 3, eave - 12), (dx + 19, eave - 12)], K, 0.6)
    smoke_src += chimney(x0 + 14 + 6 * hi, ridge - 20, ridge + 4, 2 + (hi == 1))
    smoke_src += chimney(x1 - 40, ridge - 14, ridge + 4, 2)
    # wall
    if style == "brick": brick(x0, eave, x1, GROUND, R, K)
    elif style == "brick2": brick(x0, eave, x1, GROUND, R, K, dark=True)
    else:
        rect(d, x0, eave, x1, GROUND, Y)
        for _ in range(900):
            px, py = rnd.uniform(x0, x1), rnd.uniform(eave, GROUND)
            line(d, [(px, py), (px + 1.5, py)], K if rnd.random() < .7 else Wh, 0.4)
        for yy in range(int(eave) + 40, GROUND - 90, 80):   # string courses
            rect(d, x0, yy - 2, x1, yy + 2, Wh, K, 0.5)
        for k in range(12):                                   # quoins
            for qx in (x0, x1 - 9):
                rect(d, qx + (0 if k % 2 else 0), eave + 6 + k * 26, qx + 9 + (4 if k % 2 == 0 and qx == x0 else 0) - (0), eave + 18 + k * 26, Wh, K, 0.4)
    # cornice
    rect(d, x0, eave - 1, x1, eave + 5, Wh, K, 0.7)
    for x in range(int(x0) + 3, int(x1) - 2, 6): rect(d, x, eave + 5, x + 3, eave + 8, Wh, K, 0.4)
    line(d, [(x0, eave), (x0, GROUND)], K, 1.4); line(d, [(x1, eave), (x1, GROUND)], K, 1.4)
    # downpipe
    line(d, [(x1 - 4, eave + 8), (x1 - 4, GROUND)], K, 2.2); line(d, [(x1 - 4, eave + 8), (x1 - 4, GROUND)], B, 0.8)
    # windows
    wd = x1 - x0
    ncol = 3 if wd > 135 else 2 if style == "brick2" else 3
    ww = 24 if ncol == 3 else 30
    shop_top = GROUND - 96
    nrow = int((shop_top - eave - 16) // 74)
    rowh = (shop_top - eave - 14) / nrow
    for r in range(nrow):
        hh = 46 if r < nrow - 1 else 42
        for c in range(ncol):
            wx = x0 + (wd - 8) * (c + 0.5) / ncol - ww / 2 + 2
            wy = eave + 22 + r * rowh
            lit = rnd.random() < 0.66
            if lit: sc = scenes_lit[si % len(scenes_lit)]; si += 1
            else: sc = rnd.choice(scenes_dark)
            window(wx, wy, ww, hh, sc, lit)
            if style == "stucco" and r == 0:                 # iron balconette
                line(d, [(wx - 6, wy + hh + 2), (wx + ww + 6, wy + hh + 2)], K, 1.2); line(d, [(wx - 6, wy + hh - 10), (wx + ww + 6, wy + hh - 10)], K, 1.0)
                for i in range(8):
                    bx = wx - 5 + (ww + 10) * i / 7
                    line(d, scurve(bx, wy + hh - 10, 12, 1.6, 8), K, 0.6)
            if style == "brick" and c == 0 and r == 1:        # window box
                rect(d, wx - 4, wy + hh - 2, wx + ww + 4, wy + hh + 5, G, K, 0.5)
                for i in range(7): circ(d, wx - 2 + i * (ww + 4) / 6, wy + hh - 4 + (i % 2), 2.2, R if i % 2 else Y, K, 0.4)

# ---------- ground floors
st = GROUND - 96
# left: print-seller
x0, x1 = 0, 128
rect(d, x0, st, x1, GROUND, K)
rect(d, x0 + 4, st + 2, x1 - 4, st + 18, G, K, 0.6); text(d, 64, st + 10.5, "W. H. PRINTSELLER", 8.6, Y, bold=True)
rect(d, x0 + 8, st + 24, x0 + 80, GROUND - 14, Y, Wh, 1.2)
k = 0
for r in range(3):
    for c in range(4):
        fx, fy = x0 + 12 + c * 17, st + 28 + r * 18.5
        rect(d, fx, fy, fx + 13, fy + 15, Wh, K, 0.8)
        kind = k % 4; k += 1
        if kind == 0: line(d, scurve(fx + 6.5, fy + 2.5, 10, 2.6, 12), R, 0.9)
        elif kind == 1:
            circ(d, fx + 6.5, fy + 6, 3, K); poly(d, [(fx + 2.5, fy + 14), (fx + 4, fy + 9), (fx + 9, fy + 9), (fx + 10.5, fy + 14)], K)
        elif kind == 2:
            poly(d, [(fx + 1.5, fy + 12), (fx + 5, fy + 5), (fx + 8, fy + 9), (fx + 10, fy + 6), (fx + 12, fy + 12)], B); circ(d, fx + 10, fy + 3.5, 1.3, R)
        else:
            for yy in range(3, 14, 2): line(d, [(fx + 2, fy + yy), (fx + 11, fy + yy)], K, 0.4)
for i in (1, 2): line(d, [(x0 + 8 + 24 * i, st + 24), (x0 + 8 + 24 * i, GROUND - 14)], Wh, 1.0)
rect(d, x0 + 8, GROUND - 14, x0 + 80, GROUND - 2, G, Wh, 0.6)
# door
rect(d, x0 + 90, st + 24, x0 + 120, GROUND, R, Wh, 1.0)
for (a, b_, c, e) in ((94, 30, 116, 52), (94, 56, 116, 92)): rect(d, x0 + a, st + b_, x0 + c, st + e, None, K, 0.7)
circ(d, x0 + 96, st + 60, 1.5, Y)
# middle: door with fanlight, railings, steps, barber next door
x0, x1 = 128, 272
rect(d, x0 + 9, st, x1 - 9, GROUND, Wh)
for yy in range(st, GROUND, 12):
    line(d, [(x0 + 9, yy), (x1 - 9, yy)], K, 0.6)
    for xx in range(x0 + 9 + (0 if (yy // 12) % 2 else 14), x1 - 9, 28): line(d, [(xx, yy), (xx, yy + 12)], K, 0.5)
dx = 200
poly(d, [(dx - 26, GROUND - 6), (dx - 26, st + 34)] + [(dx + 26 * math.cos(math.radians(a)), st + 34 - 22 * math.sin(math.radians(a))) for a in range(180, -1, -10)] + [(dx + 26, GROUND - 6)], K)
rect(d, dx - 17, st + 36, dx + 17, GROUND - 6, B, Wh, 1.0)
for (a, b_, c, e) in ((-13, 40, -2, 62), (2, 40, 13, 62), (-13, 66, -2, 86), (2, 66, 13, 86)): rect(d, dx + a, st + b_, dx + c, st + e, None, Wh, 0.6)
circ(d, dx, st + 64, 1.8, Y)
fan = [(dx + 17 * math.cos(math.radians(a)), st + 33 - 15 * math.sin(math.radians(a))) for a in range(180, -1, -10)]
poly(d, fan, Y, Wh, 0.9)
for a in range(30, 151, 30): line(d, [(dx, st + 33), (dx + 17 * math.cos(math.radians(a)), st + 33 - 15 * math.sin(math.radians(a)))], Wh, 0.8)
for sx in (-1, 1):
    rect(d, dx + sx * 22 - 3, st + 34, dx + sx * 22 + 3, GROUND - 6, Wh, K, 0.6)
for i in range(3): rect(d, dx - 30 - i * 4, GROUND - 6 + i * 2, dx + 30 + i * 4, GROUND - 4 + i * 2, Wh, K, 0.5)
for wx in (x0 + 18, x1 - 48):
    window(wx, st + 30, 30, 44, "curtain" if wx < dx else "reader", True)
    # area railings with spear heads
    for i in range(9):
        rx = wx - 6 + i * 5.2
        line(d, [(rx, GROUND - 26), (rx, GROUND)], K, 0.9); poly(d, [(rx - 1.4, GROUND - 26), (rx, GROUND - 31), (rx + 1.4, GROUND - 26)], K)
    line(d, [(wx - 7, GROUND - 22), (wx + 37, GROUND - 22)], K, 1.0)
# barber's pole: the serpentine line, wound on a stick
bx, by = x0 + 2, st + 20
line(d, [(bx, by + 4), (bx + 12, by - 8)], K, 1.2)
pole = [(bx + 12, by - 8), (bx + 34, by - 30)]
import PIL
for i in range(22):
    t0, t1 = i / 22, (i + 1) / 22
    px0 = bx + 12 + 26 * t0; py0 = by - 8 - 26 * t0; px1 = bx + 12 + 26 * t1; py1 = by - 8 - 26 * t1
    line(d, [(px0, py0), (px1, py1)], [Wh, R, Wh, B][i % 4], 5)
circ(d, bx + 39, by - 35, 3.2, Y, K, 0.6); circ(d, bx + 11, by - 7, 3, Y, K, 0.6)
# right: tavern
x0, x1 = 272, 400
rect(d, x0, st, x1, GROUND, G)
for xx in range(x0 + 2, x1, 5): line(d, [(xx, st + 20), (xx, GROUND)], K, 0.35)
rect(d, x0 + 3, st + 2, x1 - 3, st + 18, K, Y, 0.8); text(d, 336, st + 10.5, "THE PUG & PALETTE", 8.4, Y, bold=True)
# bow window with bottle glass
rect(d, x0 + 8, st + 26, x0 + 74, GROUND - 16, Y, Wh, 1.2)
for r in range(5):
    for c in range(6):
        gx, gy = x0 + 8 + c * 11, st + 26 + r * 10.8
        rect(d, gx, gy, gx + 11, gy + 10.8, None, K, 0.6); circ(d, gx + 5.5, gy + 5.4, 2.6, None, K if (r + c) % 3 else R, 0.5)
# drinkers behind the glass
for hx in (x0 + 24, x0 + 46, x0 + 60):
    circ(d, hx, GROUND - 40, 5, K); poly(d, [(hx - 9, GROUND - 16), (hx - 7, GROUND - 33), (hx + 7, GROUND - 33), (hx + 9, GROUND - 16)], K)
poly(d, [(x0 + 31, GROUND - 30), (x0 + 37, GROUND - 30), (x0 + 36, GROUND - 20), (x0 + 32, GROUND - 20)], Wh, K, 0.5)
rect(d, x0 + 8, GROUND - 16, x0 + 74, GROUND - 2, K, Wh, 0.6)
# tavern door, open, light spilling
rect(d, x0 + 84, st + 24, x0 + 116, GROUND, Y, Wh, 1.0)
circ(d, x0 + 100, st + 44, 5.5, K); poly(d, [(x0 + 90, GROUND), (x0 + 91, st + 52), (x0 + 109, st + 52), (x0 + 111, GROUND)], K)
line(d, [(x0 + 109, st + 58), (x0 + 118, st + 50)], K, 2.5); poly(d, [(x0 + 116, st + 44), (x0 + 122, st + 44), (x0 + 121, st + 52), (x0 + 117, st + 52)], Wh, K, 0.5)
# hanging sign with the pug
sx, sy = x0 + 30, st - 34
line(d, [(x0 + 2, sy - 8), (sx + 22, sy - 8)], K, 1.8)
line(d, bez((x0 + 2, sy + 10), (x0 + 14, sy + 8), (x0 + 18, sy - 4), (sx + 6, sy - 8), 10), K, 0.9)   # scrolled bracket
for hx in (sx - 12, sx + 12): line(d, [(hx, sy - 8), (hx, sy - 2)], K, 0.7)
rect(d, sx - 17, sy - 2, sx + 17, sy + 30, Y, K, 1.2); rect(d, sx - 14, sy + 1, sx + 14, sy + 27, None, R, 0.7)
ell(d, sx - 1, sy + 17, 8, 5.5, K); circ(d, sx + 7, sy + 11, 4.6, K); poly(d, [(sx + 4, sy + 8), (sx + 4.5, sy + 4), (sx + 7, sy + 7)], K)
for lx in (sx - 6, sx - 2, sx + 3, sx + 6): line(d, [(lx, sy + 20), (lx, sy + 25)], K, 1.3)
line(d, bez((sx - 8, sy + 15), (sx - 14, sy + 14), (sx - 9, sy + 8), (sx - 12, sy + 7), 8), K, 1.1)   # the curled tail
circ(d, sx + 8.5, sy + 10.5, 0.8, Y)

# ---------- pavement and cobbles
rect(d, 0, GROUND, 400, 540, Wh, K, 0.8)
for x in range(-10, 410, 26): line(d, [(x, GROUND), (x - 6, 540)], K, 0.5)
rect(d, 0, 540, 400, 600, K)
for r, y in enumerate(range(543, 600, 7)):
    wdt = 9 + r * 1.3
    x = -(r * 5 % 9)
    while x < 400:
        poly(d, [(x + 1, y + 6 + r * .3), (x + 1.5, y + 1.5), (x + wdt / 2, y), (x + wdt - 1.5, y + 1.5), (x + wdt - 1, y + 6 + r * .3)], B if rnd.random() < .93 else Wh)
        x += wdt
# lamp glow on the cobbles
for _ in range(260):
    a, rr = rnd.uniform(0, 6.28), abs(rnd.gauss(0, 26))
    px, py = 248 + rr * 1.6 * math.cos(a), 566 + rr * 0.5 * math.sin(a)
    if py > 542: ell(d, px, py, 2.2, 1.1, Y)

# ---------- lamp post, lamplighter and ladder
lx = 248
poly(d, [(lx - 5, 552), (lx - 3, 538), (lx + 3, 538), (lx + 5, 552)], K, Wh, 0.5)
line(d, [(lx, 540), (lx, 420)], K, 3.2); line(d, [(lx - 0.8, 540), (lx - 0.8, 420)], Wh, 0.5)
for yy in (500, 460, 428): rect(d, lx - 3, yy, lx + 3, yy + 3, K, Wh, 0.4)
line(d, [(lx - 12, 432), (lx + 12, 432)], K, 1.6)                                   # ladder bar
lamp = [(lx - 6, 420), (lx - 10, 398), (lx + 10, 398), (lx + 6, 420)]
for rr, n in ((34, 26), (27, 20), (20, 14)):
    for i in range(n):
        a = 2 * math.pi * i / n + rr
        line(d, [(lx + (rr - 5) * math.cos(a), 408 + (rr - 5) * math.sin(a)), (lx + rr * math.cos(a), 408 + rr * math.sin(a))], Y, 1.0)
poly(d, lamp, Y, K, 1.1); line(d, [(lx, 420), (lx, 398)], K, 0.5)
poly(d, [(lx - 11, 398), (lx - 5, 390), (lx + 5, 390), (lx + 11, 398)], K); circ(d, lx, 388, 2, K)
ell(d, lx, 410, 2, 4.5, Wh)
# ladder
for sx_ in (0, 9):
    line(d, [(lx + 30 + sx_, 548), (lx + 5 + sx_, 432)], K, 1.5); line(d, [(lx + 30.6 + sx_, 548), (lx + 5.6 + sx_, 432)], Wh, 0.4)
for i in range(1, 13):
    t = i / 13
    line(d, [(lx + 30 - 25 * t, 548 - 116 * t), (lx + 39 - 25 * t, 548 - 116 * t)], K, 1.1)
# lamplighter on the ladder
mx, my = lx + 24, 470
poly(d, [(mx - 3, my + 34), (mx - 1, my + 10), (mx + 6, my + 10), (mx + 9, my + 40), (mx + 5, my + 40), (mx + 3, my + 20), (mx + 1, my + 34)], K, Wh, 0.4)   # legs
poly(d, [(mx - 5, my + 12), (mx - 6, my - 10), (mx + 6, my - 12), (mx + 9, my + 12)], R, K, 0.7)     # coat
circ(d, mx - 1, my - 17, 5, Wh, K, 0.7)
poly(d, [(mx - 9, my - 19), (mx + 7, my - 21), (mx + 4, my - 26), (mx - 5, my - 25)], K)              # hat
line(d, [(mx - 4, my - 6), (mx - 14, my - 24), (lx + 3, 414)], K, 2.0); line(d, [(mx - 14, my - 24), (lx + 3, 414)], Wh, 0.6)   # arm and lighting pole
# a dog watching, and a cat on the roof
gx, gy = 198, 584
ell(d, gx, gy - 9, 11, 6, Wh, K, 0.7); circ(d, gx + 12, gy - 17, 5, Wh, K, 0.7); poly(d, [(gx + 9, gy - 21), (gx + 9.5, gy - 27), (gx + 13, gy - 21)], K)
for q in (-7, -3, 5, 8): line(d, [(gx + q, gy - 5), (gx + q, gy + 2)], Wh, 1.6)
line(d, bez((gx - 10, gy - 11), (gx - 18, gy - 12), (gx - 13, gy - 20), (gx - 17, gy - 22), 8), Wh, 1.4); circ(d, gx + 14, gy - 18, 0.8, K)
cx, cy = 170, 84
ell(d, cx, cy - 5, 7, 4, K); circ(d, cx + 7, cy - 9, 3, K); poly(d, [(cx + 5, cy - 11), (cx + 5.5, cy - 15), (cx + 7.5, cy - 11.5)], K); poly(d, [(cx + 9.5, cy - 11), (cx + 9.5, cy - 15), (cx + 7.5, cy - 11.5)], K)
line(d, scurve(cx - 7, cy - 16, 12, 2.4, 10), K, 1.3); circ(d, cx + 8, cy - 9.5, 0.6, Y)
# a walker with a lantern, far left
wx_, wy_ = 40, 578
poly(d, [(wx_ - 7, wy_), (wx_ - 5, wy_ - 26), (wx_ + 5, wy_ - 26), (wx_ + 8, wy_)], B, Wh, 0.6); circ(d, wx_, wy_ - 31, 4.5, Wh, K, 0.6)
poly(d, [(wx_ - 6, wy_ - 34), (wx_ + 6, wy_ - 34), (wx_ + 3, wy_ - 41), (wx_ - 3, wy_ - 41)], K, Wh, 0.4)
line(d, [(wx_ + 5, wy_ - 20), (wx_ + 13, wy_ - 14)], Wh, 1.2); rect(d, wx_ + 11, wy_ - 14, wx_ + 16, wy_ - 7, Y, Wh, 0.5)

# smoke last, over the sky
for (sx_, sy_) in smoke_src[::2]:
    smoke(sx_, sy_, rnd.uniform(48, 80), rnd.uniform(4, 7))
save(im)
