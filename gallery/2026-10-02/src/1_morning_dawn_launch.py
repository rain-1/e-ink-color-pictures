"""Morning — Dawn Launch. A deco city at sunrise and a rocket clearing the gantry.
Screened sky ramp, striped deco sun, two depths of towers with windows, a lattice
gantry, a riveted rocket, smoke billows with Ben-Day shading, watchers on a terrace."""
import math, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from ink import *

random.seed(1909)
cv = Canvas(WH)
HZ = 400  # horizon behind the city

# --- sky: blue → white → yellow → red, with deco ray wedges ---------------------
SX, SY = 120, 372
ang = np.arctan2(YY - SY, XX - SX)
wedge = (np.floor((ang + math.pi) / (math.pi / 18)) % 2) == 0
t = np.clip(YY / HZ, 0, 1) ** 1.35
t = t + np.where(wedge, 0.05, 0) * (YY < HZ)
cv.ramp(YY < HZ + 40, t, [B, WH, Y, R])

# streamlined deco clouds: white lozenges with a red underside line
for (cx, cy, L) in [(60, 120, 120), (250, 90, 150), (330, 190, 110), (90, 240, 160), (230, 300, 90)]:
    th = 8
    cv.draw(lambda d: d.rounded_rectangle([cx - L / 2, cy - th, cx + L / 2, cy + th], radius=th, fill=1), WH)
    cv.draw(lambda d: d.rounded_rectangle([cx - L / 2 + 14, cy - th - 7, cx + L / 2 - 30, cy], radius=7, fill=1), WH)
    cv.draw(lambda d: d.line([cx - L / 2 + 8, cy + th, cx + L / 2 - 8, cy + th], fill=1, width=2), R)
    cv.draw(lambda d: d.line([cx - L / 2 + 20, cy + th + 4, cx + L / 2 - 30, cy + th + 4], fill=1, width=1), Y)

# --- the sun: yellow disc, red bands thickening towards the horizon --------------
sun = Canvas.mask(lambda d: d.ellipse([SX - 82, SY - 82, SX + 82, SY + 82], fill=1))
cv.fill(sun, Y)
for k in range(9):
    y0 = SY - 20 + k * 12
    cv.fill(sun & (YY >= y0) & (YY < y0 + 2 + k), R)
cv.draw(lambda d: d.ellipse([SX - 82, SY - 82, SX + 82, SY + 82], outline=1, width=2), R)

# --- far mountains ---------------------------------------------------------------
pts = [(0, HZ)]
x = 0
while x < W:
    x += random.randint(14, 30)
    pts.append((x, HZ - 30 - random.randint(0, 40) * (0.5 + 0.5 * math.sin(x / 70))))
pts += [(W, HZ + 60), (0, HZ + 60)]
mnt = Canvas.mask(lambda d: d.polygon(pts, fill=1))
cv.screen(mnt, 0.25 + 0.5 * (YY - (HZ - 70)) / 110, R, B)
for p, q in zip(pts[1:-3], pts[2:-2]):  # snow-lit left faces
    cv.draw(lambda d: d.line([p, ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2 + 6)], fill=1, width=1), Y)


def tower(cx, w, top, base, body, win_on, win_off, lit_edge, p_lit, crown, seed):
    rnd = random.Random(seed)
    tiers = rnd.randint(2, 3)
    hs = []
    y = base
    ww = w
    span = base - top
    for i in range(tiers):
        h = span * (0.55 if i == 0 else 0.6 / tiers)
        hs.append((cx - ww / 2, y - h, cx + ww / 2, y))
        y -= h
        ww = ww * rnd.uniform(0.62, 0.78)
    for (x0, y0, x1, y1) in hs:
        cv.draw(lambda d: d.rectangle([x0, y0, x1, y1], fill=1), body)
        # windows
        for wy in range(int(y0) + 5, int(y1) - 3, 7):
            for wx in range(int(x0) + 4, int(x1) - 3, 5):
                c = win_on if rnd.random() < p_lit else win_off
                if c is not None:
                    cv.a[wy:wy + 3, wx:wx + 2] = c
        # sun-side edge and a cornice line
        cv.a[int(y0):int(y1), int(x0):int(x0) + 2] = lit_edge
        cv.a[int(y0):int(y0) + 2, int(x0):int(x1)] = lit_edge
    x0, y0, x1, _ = hs[-1]
    mid = (x0 + x1) / 2
    if crown == "needle":
        cv.draw(lambda d: d.polygon([(x0, y0), (x1, y0), (mid, y0 - 26)], fill=1), body)
        cv.draw(lambda d: d.line([mid, y0 - 26, mid, y0 - 56], fill=1, width=2), body)
        cv.a[int(y0 - 58):int(y0 - 54), int(mid) - 1:int(mid) + 2] = R
        for k in range(3):  # stepped chevrons on the crown
            yy = y0 - 6 - k * 6
            cv.draw(lambda d: d.line([mid - (x1 - x0) / 2 * (1 - k * 0.25) + 3, yy + 3, mid, yy - 3,
                                      mid + (x1 - x0) / 2 * (1 - k * 0.25) - 3, yy + 3], fill=1, width=1), lit_edge)
    elif crown == "ziggurat":
        ww = x1 - x0
        for k in range(4):
            ww *= 0.72
            cv.draw(lambda d: d.rectangle([mid - ww / 2, y0 - 7 * (k + 1), mid + ww / 2, y0 - 7 * k], fill=1), body)
            cv.a[int(y0 - 7 * (k + 1)):int(y0 - 7 * (k + 1)) + 1, int(mid - ww / 2):int(mid + ww / 2)] = lit_edge
    elif crown == "dome":
        r = (x1 - x0) / 2
        cv.draw(lambda d: d.pieslice([mid - r, y0 - r, mid + r, y0 + r], 180, 360, fill=1), body)
        cv.draw(lambda d: d.arc([mid - r, y0 - r, mid + r, y0 + r], 190, 260, fill=1, width=2), lit_edge)
        cv.draw(lambda d: d.line([mid, y0 - r, mid, y0 - r - 16], fill=1, width=1), body)
    elif crown == "mast":
        cv.draw(lambda d: d.line([mid, y0, mid, y0 - 40], fill=1, width=2), body)
        for k in range(4):
            cv.draw(lambda d: d.line([mid - 8 + k * 2, y0 - 8 - k * 8, mid + 8 - k * 2, y0 - 8 - k * 8], fill=1, width=1), body)
        cv.a[int(y0 - 42):int(y0 - 38), int(mid) - 1:int(mid) + 2] = R
    return hs


# --- far city (blue, few windows) ------------------------------------------------
x = -10
while x < W + 20:
    w = random.randint(18, 34)
    tower(x, w, random.randint(300, 370), 470, B, Y, None, WH, 0.18,
          random.choice(["needle", "ziggurat", "dome", "mast"]), x)
    x += w * random.uniform(0.7, 1.1)

# --- skyway arches between far and near ----------------------------------------
for (xa, xb, yy) in [(10, 150, 420), (190, 390, 440)]:
    cv.draw(lambda d: d.arc([xa, yy - 30, xb, yy + 30], 180, 360, fill=1, width=4), K)
    cv.draw(lambda d: d.arc([xa, yy - 30, xb, yy + 30], 180, 360, fill=1, width=1), Y)
    for k in range(1, 12):
        xx = xa + (xb - xa) * k / 12
        u = (xx - (xa + xb) / 2) / ((xb - xa) / 2)
        yv = yy - 30 * math.sqrt(max(0, 1 - u * u))
        cv.draw(lambda d: d.line([xx, yv, xx, yy], fill=1, width=1), K)
    cv.draw(lambda d: d.line([xa, yy, xb, yy], fill=1, width=3), K)

# --- the launch gantry and rocket -----------------------------------------------
GX0, GX1, GTOP, GBASE = 300, 336, 205, 500
cv.draw(lambda d: d.rectangle([GX0, GTOP, GX0 + 3, GBASE], fill=1), K)
cv.draw(lambda d: d.rectangle([GX1 - 3, GTOP, GX1, GBASE], fill=1), K)
for y in range(GTOP, GBASE, 18):
    cv.draw(lambda d: d.line([GX0, y, GX1, y + 18], fill=1, width=1), K)
    cv.draw(lambda d: d.line([GX1, y, GX0, y + 18], fill=1, width=1), K)
    cv.draw(lambda d: d.line([GX0, y, GX1, y], fill=1, width=2), K)
for y in range(GTOP + 40, GBASE - 60, 64):  # swing arms, red
    cv.draw(lambda d: d.rectangle([GX0 - 26, y, GX0, y + 4], fill=1), R)
    cv.draw(lambda d: d.line([GX0 - 26, y + 4, GX0, y + 18], fill=1, width=1), K)
cv.draw(lambda d: d.polygon([(GX0 - 4, GTOP), (GX1 + 4, GTOP), ((GX0 + GX1) / 2, GTOP - 16)], fill=1), K)
cv.a[GTOP - 22:GTOP - 16, (GX0 + GX1) // 2 - 1:(GX0 + GX1) // 2 + 2] = R

# smoke column and billows (white puffs, black ink line, blue dot shading below)
RX = 252
column = Canvas.mask(lambda d: d.polygon([(RX - 8, 268), (RX + 8, 268), (RX + 34, 500), (RX - 34, 500)], fill=1))
cv.ramp(column, (YY - 268) / 60, [WH, Y, WH])
random.seed(7)
puffs = []
for i in range(46):
    py = random.uniform(330, 530)
    spread = 20 + (py - 330) * 0.9
    px = RX + random.uniform(-spread, spread)
    r = 10 + (py - 330) / 200 * 26 * random.uniform(0.6, 1.2)
    puffs.append((py, px, r))
puffs.sort()
for py, px, r in puffs:
    box = [px - r, py - r, px + r, py + r]
    m = Canvas.mask(lambda d: d.ellipse(box, fill=1))
    cv.fill(m, WH)
    shade = m & ((XX - px) * 0.5 + (YY - py) > r * 0.25)
    cv.benday(shade, B, pitch=4, r=1.1)
    cv.draw(lambda d: d.arc(box, 200, 330, fill=1, width=1), R)
    cv.draw(lambda d: d.ellipse(box, outline=1, width=2), K)

# flame
flame = [(RX - 11, 262), (RX + 11, 262), (RX + 5, 300), (RX + 2, 340), (RX, 365), (RX - 2, 340), (RX - 5, 300)]
cv.draw(lambda d: d.polygon(flame, fill=1), R)
cv.draw(lambda d: d.polygon([(RX - 7, 262), (RX + 7, 262), (RX + 2, 310), (RX, 328), (RX - 2, 310)], fill=1), Y)
cv.draw(lambda d: d.polygon([(RX - 3, 262), (RX + 3, 262), (RX, 290)], fill=1), WH)
for k in range(6):  # speed streaks
    xx = RX - 22 + k * 9
    cv.draw(lambda d: d.line([xx, 280 + (k % 2) * 10, xx, 320 + (k % 3) * 8], fill=1, width=1), K)

# rocket body
NOSE, TAIL = 70, 262
body = Canvas.mask(lambda d: d.polygon(
    [(RX, NOSE), (RX + 9, NOSE + 30), (RX + 15, NOSE + 70), (RX + 16, 210), (RX + 12, TAIL),
     (RX - 12, TAIL), (RX - 16, 210), (RX - 15, NOSE + 70), (RX - 9, NOSE + 30)], fill=1))
cv.fill(body, R)
cv.hatch(body & (XX < RX - 8), WH, pitch=3, angle=90, width=1)  # lit flank
cv.benday(body & (XX > RX + 5), K, pitch=4, r=1.2)               # shadow flank
cv.fill(body & (YY > 150) & (YY < 160), WH)                      # band
cv.fill(body & (YY > 160) & (YY < 163), K)
cv.fill(body & (YY < NOSE + 26), Y)                               # nose cone
# fins
for side in (-1, 1):
    fin = [(RX + side * 14, 200), (RX + side * 36, 250), (RX + side * 36, 278), (RX + side * 12, 258)]
    cv.draw(lambda d: d.polygon(fin, fill=1), Y if side < 0 else R)
    if side > 0:
        cv.benday(Canvas.mask(lambda d: d.polygon(fin, fill=1)), K, pitch=4, r=1.2)
    cv.draw(lambda d: d.line(fin + [fin[0]], fill=1, width=2), K)
cv.draw(lambda d: d.polygon([(RX - 3, 205), (RX + 3, 205), (RX + 3, 276), (RX - 3, 276)], fill=1), K)
outline = Canvas.mask(lambda d: d.polygon(
    [(RX, NOSE), (RX + 9, NOSE + 30), (RX + 15, NOSE + 70), (RX + 16, 210), (RX + 12, TAIL),
     (RX - 12, TAIL), (RX - 16, 210), (RX - 15, NOSE + 70), (RX - 9, NOSE + 30)], outline=1))
cv.fill(outline, K)
cv.draw(lambda d: d.line([RX - 12, TAIL, RX + 12, TAIL], fill=1, width=2), K)
for py in (118, 180):  # portholes
    cv.draw(lambda d: d.ellipse([RX - 6, py - 6, RX + 6, py + 6], fill=1), K)
    cv.draw(lambda d: d.ellipse([RX - 4, py - 4, RX + 4, py + 4], fill=1), Y)
    cv.a[py - 3:py - 1, RX - 3:RX - 1] = WH
for py in range(NOSE + 40, TAIL, 9):  # rivets
    cv.a[py, RX - 11] = K; cv.a[py, RX + 11] = K

# --- near city: black towers, lots of lit windows ---------------------------------
random.seed(42)
near = [(-4, 52, 330), (50, 40, 380), (92, 58, 300), (150, 36, 410), (190, 44, 360), (360, 50, 330), (395, 40, 300)]
for i, (cx, w, top) in enumerate(near):
    tower(cx + w / 2, w, top, 560, K, Y, B, R, 0.35, ["ziggurat", "needle", "dome", "mast", "needle", "dome", "ziggurat"][i], 100 + i)

# launch pad deck
cv.draw(lambda d: d.rectangle([200, 500, 360, 560], fill=1), K)
for x in range(204, 360, 10):
    cv.draw(lambda d: d.rectangle([x, 506, x + 5, 512], fill=1), Y if (x // 10) % 3 else R)
cv.draw(lambda d: d.line([200, 500, 360, 500], fill=1, width=2), R)
# searchlights from the pad, crossing behind the rocket
for (x0, x1) in [(214, 160), (350, 400)]:
    beam = Canvas.mask(lambda d: d.polygon([(x0 - 2, 500), (x0 + 2, 500), (x1 + 16, 330), (x1 - 16, 330)], fill=1))
    cv.benday(beam & ~body, WH, pitch=3, r=0.8)

# --- foreground terrace with watchers ----------------------------------------------
cv.draw(lambda d: d.rectangle([0, 548, W, H], fill=1), K)
cv.draw(lambda d: d.rectangle([0, 548, W, 552], fill=1), Y)
for x in range(6, W, 16):  # balustrade with deco fans
    cv.draw(lambda d: d.rectangle([x, 556, x + 9, 596], fill=1), G)
    cv.draw(lambda d: d.pieslice([x - 2, 556, x + 11, 570], 0, 180, fill=1), Y)
    cv.draw(lambda d: d.line([x + 4, 572, x + 4, 594], fill=1, width=1), K)
cv.draw(lambda d: d.rectangle([0, 594, W, H], fill=1), R)


def figure(x, y, s=1.0, arm=False, hat=False, c=K):
    h = 34 * s
    cv.draw(lambda d: d.ellipse([x - 4 * s, y - h, x + 4 * s, y - h + 8 * s], fill=1), c)  # head
    cv.draw(lambda d: d.polygon([(x - 6 * s, y - h + 9 * s), (x + 6 * s, y - h + 9 * s),
                                 (x + 8 * s, y - 2), (x - 8 * s, y - 2)], fill=1), c)    # coat
    if hat:
        cv.draw(lambda d: d.rectangle([x - 6 * s, y - h - 1, x + 6 * s, y - h + 1], fill=1), c)
        cv.draw(lambda d: d.rectangle([x - 3 * s, y - h - 4, x + 3 * s, y - h], fill=1), c)
    if arm:
        cv.draw(lambda d: d.line([x + 4 * s, y - h + 11 * s, x + 18 * s, y - h - 6 * s], fill=1, width=3), c)


cv.draw(lambda d: d.rectangle([0, 520, 170, 548], fill=1), K)  # observation balcony
cv.draw(lambda d: d.line([0, 520, 170, 520], fill=1, width=2), Y)
for i, (x, s, arm, hat) in enumerate([(24, 1.0, False, True), (44, 0.85, False, False), (70, 1.1, True, False),
                                      (96, 0.7, False, False), (120, 1.0, False, True), (146, 0.9, True, False)]):
    s *= 1.15
    for dx, dy in [(-2, 0), (2, 0), (0, -2), (-1, -1), (1, -1)]:  # inked yellow halo so they read on black
        figure(x + dx, 520 + dy, s, arm, hat, Y)
    figure(x, 520, s, arm, hat, K)
    cv.draw(lambda d: d.line([x - 6 * s, 520 - 30 * s, x - 7 * s, 518], fill=1, width=2), R)  # rim light

text(cv, (390, 588), "DAWN LAUNCH · 2 OCT", 11, Y, anchor="rs")
cv.save()
