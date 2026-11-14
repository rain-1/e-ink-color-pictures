"""Night — Nymphéas, after the painter has gone in. The pond at Giverny seen the way the
late canvases see it (no horizon, no sky) but by moonlight: the moon exists only as a
reflection among the pads. Flat inks and fine line, like the Hiroshige prints in his
dining room. Drawn at panel resolution so every line is a whole pixel."""
import math
import numpy as np
from PIL import Image, ImageDraw
from common import *

rng = np.random.default_rng(1926)
img = Image.new("RGB", (W, H), K)
d = ImageDraw.Draw(img)
MOON = (136, 318)

def persp(y):                       # 0 at the far bank, 1 at the bottom edge
    return min(1.0, max(0.0, (y - 150) / 450.0))

# ---- water: long slow ripples in blue, denser where the moon lies ----
for _ in range(1500):
    x = rng.uniform(-20, W); y = rng.uniform(150, H)
    t = persp(y)
    dm = math.hypot(x - MOON[0], (y - MOON[1]) * 1.6)
    if rng.random() > 0.20 + 0.8 * math.exp(-(dm / 150) ** 2):
        continue
    ln = rng.uniform(6, 16 + 50 * t)
    d.line([x, y, x + ln, y + rng.normal(0, .4)], fill=B, width=1 if t < .55 else 2)

# ---- reflections of the willows: hanging columns of broken dashes ----
for cx, wdt, depth_ in ((60, 46, 250), (300, 60, 300), (364, 30, 200), (200, 26, 120)):
    for _ in range(int(wdt * depth_ / 16)):
        x = cx + rng.normal(0, wdt / 2.2); y = 150 + rng.uniform(0, 1) ** 1.5 * depth_
        d.line([x, y, x + rng.normal(0, 1), y + rng.uniform(4, 13)], fill=G if rng.random() < .45 else B, width=1)

# ---- the moon in the water, cut by ripples, ringed by broken light ----
for k in range(1, 9):
    rx = 26 + k * 13; ry = rx * 0.42
    segs = 10 + k * 3
    for sgi in range(segs):
        if rng.random() < 0.42 + k * 0.03:
            continue
        a0 = sgi * 360 / segs + rng.uniform(0, 10)
        col = WH if k < 3 else (Y if k < 5 else B)
        d.arc([MOON[0] - rx, MOON[1] - ry, MOON[0] + rx, MOON[1] + ry], a0, a0 + 360 / segs * rng.uniform(.4, .8), fill=col, width=2 if k < 4 else 1)
d.ellipse([MOON[0] - 25, MOON[1] - 19, MOON[0] + 25, MOON[1] + 19], fill=Y)
d.ellipse([MOON[0] - 22, MOON[1] - 17, MOON[0] + 22, MOON[1] + 17], fill=WH)
for cx_, cy_, r_ in ((-8, -5, 5), (7, 3, 4), (-2, 8, 3), (11, -8, 2)):        # maria
    d.ellipse([MOON[0] + cx_ - r_, MOON[1] + cy_ - r_ * .75, MOON[0] + cx_ + r_, MOON[1] + cy_ + r_ * .75], fill=Y)
for yb in range(MOON[1] - 16, MOON[1] + 18, 5):                                  # ripples across the disc
    off = 6 * math.sin(yb * 0.9)
    d.line([MOON[0] - 26, yb, MOON[0] + 26, yb], fill=K, width=1)
    d.line([MOON[0] - 30 + off, yb + 2, MOON[0] - 20 + off, yb + 2], fill=WH, width=1)
    d.line([MOON[0] + 22 + off, yb + 1, MOON[0] + 34 + off, yb + 1], fill=WH, width=1)
# stars fallen in: single points, a few with a cross
for _ in range(70):
    x = int(rng.uniform(4, W - 4)); y = int(rng.uniform(170, H - 6))
    d.point((x, y), fill=WH); d.point((x + 1, y), fill=WH)
    if rng.random() < 0.2:
        d.line([x - 2, y, x + 3, y], fill=WH); d.line([x, y - 2, x, y + 2], fill=WH)

# ---- lily pads, in rafts, far to near ----
pads = []
rafts = [(300, 215, 70, 22), (70, 235, 55, 18), (250, 330, 85, 34), (40, 400, 60, 40),
         (330, 450, 80, 46), (150, 510, 120, 44), (360, 570, 70, 30), (20, 575, 60, 30), (205, 250, 30, 12)]
for (cx, cy, sx, sy) in rafts:
    for _ in range(60):
        x = cx + rng.normal(0, sx * .55); y = cy + rng.normal(0, sy * .6)
        if y < 172: continue
        t = persp(y)
        rx = (7 + 34 * t ** 1.2) * rng.uniform(.65, 1.15); ry = rx * (0.36 + 0.22 * t)
        if math.hypot(x - MOON[0], (y - MOON[1]) * 1.5) < 34 + rx: continue
        if any(((x - p[0]) / (rx + p[2])) ** 2 + ((y - p[1]) / (ry + p[3])) ** 2 < 0.72 for p in pads): continue
        pads.append((x, y, rx, ry, rng.uniform(0, 360)))
pads.sort(key=lambda p: p[1])

def lily(x, y, r, col):
    """A water-lily: three whorls of pointed petals round a yellow heart."""
    for whorl, (n, rr, lift) in enumerate(((9, 1.0, 0.0), (7, 0.78, 0.22), (5, 0.5, 0.42))):
        for k in range(n):
            a = math.pi * (k + 0.5 * (whorl % 2)) / (n - 1) * 1.0 + math.pi   # upper half fan
            a = math.pi + (k + 0.5) * math.pi / n
            tipx = x + r * rr * 1.25 * math.cos(a); tipy = y - r * lift + r * rr * 0.95 * math.sin(a)
            bx1 = x + r * 0.28 * math.cos(a - 0.5); by1 = y - r * lift + r * 0.12 * math.sin(a - 0.5)
            bx2 = x + r * 0.28 * math.cos(a + 0.5); by2 = y - r * lift + r * 0.12 * math.sin(a + 0.5)
            d.polygon([(bx1, by1), (tipx, tipy), (bx2, by2)], fill=col, outline=K if r > 7 else None)
    # the near petals lying on the water
    for k in range(5):
        a = (k + 0.5) * math.pi / 5
        d.polygon([(x + r * .3 * math.cos(a - .5), y), (x + r * 1.15 * math.cos(a), y + r * .34 * math.sin(a)),
                   (x + r * .3 * math.cos(a + .5), y)], fill=col, outline=K if r > 7 else None)
    d.ellipse([x - r * .22, y - r * .42, x + r * .22, y - r * .12], fill=Y)

for (x, y, rx, ry, rot) in pads:
    dm = math.hypot(x - MOON[0], (y - MOON[1]) * 1.4)
    lit = math.exp(-(dm / 250) ** 2)
    # drop shadow / thickness
    d.ellipse([x - rx, y - ry + 2, x + rx, y + ry + 2], fill=K)
    notch = rot
    d.pieslice([x - rx, y - ry, x + rx, y + ry], notch + 14, notch + 346, fill=G)
    # night: pads away from the moon sink into a black screen
    if lit < 0.75:
        x0, x1, y0, y1 = int(max(0, x - rx)), int(min(W - 1, x + rx)), int(max(0, y - ry)), int(min(H - 1, y + ry))
        px = img.load()
        for yy_ in range(y0, y1 + 1):
            for xx_ in range(x0, x1 + 1):
                if px[xx_, yy_] == G and ((xx_ - x) / rx) ** 2 + ((yy_ - y) / ry) ** 2 <= 1:
                    if lit < 0.35:
                        if (xx_ + yy_) % 2 == 0 or (yy_ % 4 == 1 and lit < 0.15): px[xx_, yy_] = K
                    elif (xx_ + 2 * yy_) % 4 == 0: px[xx_, yy_] = K
    # veins
    if rx > 11:
        nv = 9 if rx < 22 else 13
        for k in range(nv):
            a = math.radians(notch + 20 + k * 320 / (nv - 1))
            d.line([x + rx * .12 * math.cos(a), y + ry * .12 * math.sin(a), x + rx * .9 * math.cos(a), y + ry * .9 * math.sin(a)], fill=K, width=1)
    # moonlit rim on the side facing the moon; a blue rim elsewhere
    am = math.degrees(math.atan2((MOON[1] - y) * 2, MOON[0] - x))
    d.arc([x - rx, y - ry, x + rx, y + ry], am - 55, am + 55, fill=WH if lit > 0.45 else B, width=1 if rx < 20 else 2)
    if rx > 16:
        d.arc([x - rx, y - ry, x + rx, y + ry], am + 120, am + 240, fill=B, width=1)
    # dew
    if rx > 20 and rng.random() < .6:
        for _ in range(3):
            a = rng.uniform(0, 6.28); q = rng.uniform(.3, .7)
            ex, ey = x + rx * q * math.cos(a), y + ry * q * math.sin(a)
            d.ellipse([ex - 1, ey - 1, ex + 1, ey + 1], fill=WH)
    # flowers on a third of them
    if rng.random() < 0.36 and rx > 9:
        fx = x + rx * rng.uniform(-.5, .5); fy = y - ry * 0.2
        lily(fx, fy, max(6, rx * rng.uniform(.6, .8)), WH if rng.random() < 0.62 else (R if rng.random() < .7 else Y))

# ---- the far bank: the bridge in moon-blue, willows over it ----
d.rectangle([0, 0, W, 146], fill=K)
def bridge_y(x, base, rise): return base - rise * (1 - ((x - 200) / 215.0) ** 2)
for base, rise, wd, col in ((142, 46, 3, B), (118, 46, 2, B), (104, 46, 3, WH)):   # deck, mid rail, top rail (catching light)
    pts = [(x, bridge_y(x, base, rise)) for x in range(-10, W + 12, 6)]
    d.line(pts, fill=col, width=wd)
for x in range(8, W, 22):
    d.line([x, bridge_y(x, 104, 46) - 3, x, bridge_y(x, 142, 46)], fill=B, width=2)
for x in range(19, W, 22):
    d.line([x, bridge_y(x, 104, 46), x, bridge_y(x, 142, 46)], fill=B, width=1)
# bridge reflected: broken
for x in range(0, W, 5):
    yb = 150 + (150 - bridge_y(x, 142, 46)) * 0.55
    if rng.random() < .6 and yb > 152:
        d.line([x, yb + rng.normal(0, 1.5), x + rng.uniform(3, 9), yb + rng.normal(0, 1.5)], fill=B, width=1)
# wisteria hanging from the top rail
for x in range(30, W - 20, 9):
    if rng.random() < .5:
        y0 = bridge_y(x, 104, 46) + 2
        for j in range(int(rng.uniform(3, 8))):
            jx = x + rng.normal(0, 1)
            d.ellipse([jx - 2, y0 + j * 3, jx + 1, y0 + j * 3 + 2], fill=WH if j % 3 == 0 else B)
# willow curtains: each frond a chain of small leaves
for cx, spread, n, drop in ((54, 60, 46, 170), (312, 78, 60, 200), (190, 30, 12, 70)):
    for _ in range(n):
        x = cx + rng.normal(0, spread / 2); y = -5.0
        ln = drop * rng.uniform(.45, 1.05); sway = rng.normal(0, .12); ph = rng.uniform(0, 6)
        col_main = G
        while y < ln:
            x += sway + 0.5 * math.sin(y / 23.0 + ph)
            lf = 3.5 + 2.5 * (y / ln)
            side = 1 if int(y / 5) % 2 else -1
            c = col_main if rng.random() < 0.7 else (Y if rng.random() < .22 else K)
            d.line([x, y, x + side * lf * .6, y + lf], fill=c, width=1)
            d.point((x, y), fill=G)
            y += 2.5
# reeds and irises at the bank foot
for _ in range(120):
    x = rng.uniform(0, W); h = rng.uniform(8, 30)
    if 110 < x < 290 and rng.random() < .7: continue
    d.line([x, 152, x + rng.normal(0, 4), 152 - h], fill=G if rng.random() < .6 else B, width=1)
    if rng.random() < .12:
        d.ellipse([x - 2, 150 - h - 4, x + 2, 150 - h], fill=Y)
d.line([0, 150, W, 150], fill=B, width=1)
# fireflies over the far water
for _ in range(16):
    x = rng.uniform(10, W - 10); y = rng.uniform(40, 190)
    d.ellipse([x - 1, y - 1, x + 1, y + 1], fill=Y)
save(img)
