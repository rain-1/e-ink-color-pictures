"""Tierra! — dawn, 12 October 1492. The Pinta under full sail, the island on the horizon,
woodblock style: banded sky, Hokusai wave-fingers, planked hull, rigging, a lookout."""
import math, random
from common import *

random.seed(1492)
c = Canvas(B)
HZ = 318  # horizon

# --- sky: woodblock bands, dark blue at top -> yellow at horizon
bands = [(0, B), (150, Wt), (232, Y), (290, R)]
for i, (y0, col) in enumerate(bands):
    y1 = bands[i + 1][0] if i + 1 < len(bands) else HZ
    c.rect(0, y0, 400, y1, fill=col)
# ragged band edges (cut by a knife, not a ruler)
for y0, top, bot in [(150, B, Wt), (232, Wt, Y), (290, Y, R)]:
    x = 0
    while x < 400:
        w = random.uniform(8, 26); d = random.uniform(2, 7)
        c.poly([(x, y0), (x + w / 2, y0 + d), (x + w, y0)], fill=top)
        x += w
# stars fading out in the top band
for _ in range(40):
    x, y = random.uniform(0, 400), random.uniform(6, 120)
    r = random.choice([0.8, 0.8, 1.2, 1.8])
    c.circle(x, y, r, fill=Wt)
c.poly([(338, 40), (341, 50), (351, 52), (341, 54), (338, 64), (335, 54), (325, 52), (335, 50)], fill=Y)  # Venus, last star

# sun: half-risen red disc with concentric yellow rings and rays
sx, sy = 300, HZ
for i in range(26):
    a = math.radians(180 + i * 180 / 25)
    a2 = a + math.radians(2.2)
    c.poly([(sx, sy), (sx + 300 * math.cos(a), sy + 300 * math.sin(a)),
            (sx + 300 * math.cos(a2), sy + 300 * math.sin(a2))], fill=Y if i % 2 else None)
# restore the upper sky over the rays above the white band (rays only in the low sky)
c.rect(0, 0, 400, 150, fill=None)
c.circle(sx, sy - 6, 46, fill=K)
c.circle(sx, sy - 6, 44, fill=Y)
for r in (36, 28, 20):
    c.circle(sx, sy - 6, r, outline=R, width=1.3)

# long horizontal clouds, outlined
def cloud(x, y, w, h, fill=Wt):
    pts = []
    n = 14
    for i in range(n + 1):
        t = i / n
        pts.append((x + w * t, y - h * (0.5 + 0.5 * math.sin(t * math.pi)) * (0.8 + 0.4 * random.random())))
    pts += [(x + w, y), (x, y)]
    c.poly(pts, fill=fill, outline=K, width=1.2)
    for k in range(3):
        yy = y - h * 0.25 * (k + 1) * 0.6
        c.line([(x + w * 0.12 + k * 6, yy), (x + w * 0.7 - k * 9, yy)], fill=K, width=0.8)
cloud(-10, 112, 170, 22)
cloud(210, 92, 210, 18)
cloud(40, 205, 130, 14, Y)
cloud(250, 262, 150, 12, Wt)
cloud(-20, 272, 120, 10, Wt)

# --- the island: low green land, white sand line, palms
il = [(196, HZ)]
for i in range(30):
    x = 200 + i * 7
    il.append((x, HZ - 12 - 6 * math.sin(i * 0.5) - 3 * random.random() - (10 if 9 < i < 18 else 0)))
il.append((410, HZ))
c.poly(il, fill=G, outline=K, width=1)
c.rect(196, HZ - 3, 410, HZ, fill=Wt)
c.line([(196, HZ - 3), (410, HZ - 3)], fill=K, width=0.6)
def palm(x, base, h, lean):
    top = (x + lean, base - h)
    c.line([(x, base), (x + lean * 0.4, base - h * 0.5), top], fill=K, width=1.6)
    for k in range(7):
        a = math.radians(-160 + k * 23 + random.uniform(-6, 6))
        L = random.uniform(9, 13)
        ex, ey = top[0] + L * math.cos(a), top[1] + L * math.sin(a) + 3
        mx, my = top[0] + L * 0.5 * math.cos(a), top[1] + L * 0.5 * math.sin(a) - 2
        c.line([top, (mx, my), (ex, ey)], fill=K, width=1.4)
for x, h, l in [(214, 26, -4), (226, 31, 3), (262, 22, 5), (300, 34, -6), (309, 27, 4), (352, 24, 2), (380, 30, -3)]:
    palm(x, HZ - 8, h, l)

# --- sea
c.rect(0, HZ, 400, 600, fill=B)
# sun glitter road
for i in range(60):
    y = HZ + 3 + i * i * 0.07
    if y > 470: break
    w = 10 + i * 1.3
    x = sx + random.uniform(-w, w) * 0.6
    c.rect(x - w * 0.25 * random.random() - 2, y, x + w * 0.25 * random.random() + 2, y + 1 + i * 0.03, fill=Y)
# wave crest marks, small near the horizon, bigger toward us
y = HZ + 4
while y < 600:
    depth = (y - HZ) / (600 - HZ)
    step = 3 + depth * 16
    sz = 3 + depth * 22
    x = random.uniform(-sz, 0)
    while x < 400:
        c.arc(x + sz / 2, y, sz / 2, sz * 0.28, 200, 340, fill=Wt, width=0.6 + depth * 1.4)
        if depth > 0.25:
            c.arc(x + sz / 2, y + sz * 0.12, sz / 2.6, sz * 0.2, 210, 330, fill=K, width=0.6 + depth)
        x += sz * random.uniform(1.2, 2.2)
    y += step

# --- the ship (caravel Pinta, square-rigged)
def hull():
    top = [(46, 392), (70, 398), (120, 402), (190, 400), (236, 390), (252, 376)]
    bot = [(232, 428), (200, 440), (110, 442), (72, 432), (54, 412)]
    pts = top + bot
    c.poly(pts, fill=K)
    # planks
    for k in range(1, 7):
        t = k / 7
        row = [(46 + 8 * t, 392 + 20 * t + k * 0.8), (70, 398 + 34 * t), (120, 402 + 39 * t),
               (190, 400 + 40 * t), (234, 390 + 37 * t - k * 0.2)]
        c.line(row, fill=Y if k == 2 else (R if k == 3 else Wt), width=0.7 if k not in (2, 3) else 1.4)
    # stern castle & forecastle
    c.poly([(46, 392), (40, 366), (88, 368), (90, 399)], fill=R, outline=K, width=1.2)
    for i in range(6):
        c.rect(46 + i * 7, 372, 49 + i * 7, 380, fill=K)
    c.line([(40, 366), (90, 368)], fill=Y, width=1.5)
    c.poly([(214, 394), (210, 376), (250, 372), (252, 376), (236, 390)], fill=R, outline=K, width=1.2)
    c.line([(210, 376), (250, 372)], fill=Y, width=1.5)
    # bowsprit
    c.line([(246, 376), (296, 352)], fill=K, width=2.4)
    # rudder
    c.poly([(54, 412), (44, 410), (40, 438), (56, 432)], fill=K)
    # oar-ports / scuppers
    for i in range(9):
        c.rect(100 + i * 13, 413, 104 + i * 13, 416, fill=Y)
    # bow wave
    for k in range(5):
        c.arc(252 + k * 8, 432 + k * 3, 18 + k * 4, 6 + k, 180, 300, fill=Wt, width=1.6)
    for k in range(4):
        c.arc(140 - k * 30, 446 + k, 30, 5, 190, 350, fill=Wt, width=1.3)
hull()

masts = [(78, 368, 214), (148, 400, 92), (212, 376, 160)]
for x, base, top in masts:
    c.line([(x, base), (x, top)], fill=K, width=3)
# rigging: shrouds and stays
for x, base, top in masts:
    for k in range(5):
        c.line([(x, top + 10), (x - 22 + k * 3, base + 4)], fill=K, width=0.6)
        c.line([(x, top + 10), (x + 10 + k * 3, base + 4)], fill=K, width=0.6)
c.line([(148, 92), (296, 352)], fill=K, width=0.8)
c.line([(148, 92), (78, 214)], fill=K, width=0.8)
c.line([(78, 214), (40, 366)], fill=K, width=0.8)
c.line([(212, 160), (296, 352)], fill=K, width=0.7)

def sail(xc, ytop, wtop, wbot, h, belly=10, cross=True):
    l0, r0 = xc - wtop / 2, xc + wtop / 2
    l1, r1 = xc - wbot / 2, xc + wbot / 2
    pts = [(l0, ytop)]
    n = 10
    for i in range(n + 1):  # right edge bulging
        t = i / n
        pts.append((r0 + (r1 - r0) * t + belly * 0.3 * math.sin(t * math.pi), ytop + h * t))
    for i in range(n + 1):  # bottom, curved (the belly)
        t = i / n
        pts.append((r1 + (l1 - r1) * t, ytop + h + belly * math.sin(t * math.pi)))
    for i in range(n + 1):
        t = 1 - i / n
        pts.append((l0 + (l1 - l0) * t - belly * 0.3 * math.sin(t * math.pi), ytop + h * t))
    c.poly(pts, fill=Wt, outline=K, width=1.4)
    # shading hatch on the left (shadow side) — sun is to the right
    for k in range(9):
        t = k / 9
        x0 = l0 + (l1 - l0) * t + 2
        yy = ytop + h * t + 3
        c.line([(x0, yy), (x0 + wtop * 0.18 * (1 - t * 0.4), yy + h * 0.1)], fill=K, width=0.6)
    # vertical seams (cloths)
    for k in range(1, 6):
        t = k / 6
        c.line([(l0 + (r0 - l0) * t, ytop + 1), (l1 + (r1 - l1) * t, ytop + h + belly * math.sin(t * math.pi) - 1)],
               fill=K, width=0.4)
    # yard
    c.line([(l0 - 6, ytop), (r0 + 6, ytop)], fill=K, width=2.2)
    if cross:
        cx, cy = xc, ytop + h * 0.52
        a = min(wtop, h) * 0.22
        c.rect(cx - a * 0.28, cy - a, cx + a * 0.28, cy + a * 1.1, fill=R)
        c.rect(cx - a * 0.8, cy - a * 0.28, cx + a * 0.8, cy + a * 0.28, fill=R)
        for (dx, dy) in [(0, -a), (0, a * 1.1), (-a * 0.8, 0), (a * 0.8, 0)]:
            c.rect(cx + dx - a * 0.32, cy + dy - a * 0.2, cx + dx + a * 0.32, cy + dy + a * 0.2, fill=R)

sail(148, 182, 96, 116, 118, belly=14)   # main course
sail(148, 112, 62, 78, 58, belly=8, cross=False)  # main topsail
sail(212, 196, 62, 72, 84, belly=10)     # foresail
# lateen mizzen (triangle)
c.poly([(56, 352), (100, 214), (104, 352)], fill=Wt, outline=K, width=1.4)
c.line([(50, 362), (104, 206)], fill=K, width=2)
for k in range(1, 5):
    c.line([(56 + k * 10, 352), (100 - k * 0.6, 214 + k * 6)], fill=K, width=0.4)
# spritsail under the bowsprit
c.poly([(258, 373), (288, 359), (291, 386), (262, 394)], fill=Wt, outline=K, width=1.2)

# crow's nest + lookout pointing at the island
c.rect(141, 100, 155, 108, fill=R, outline=K, width=1)
c.circle(150, 95, 3.2, fill=K)            # head
c.line([(150, 98), (150, 104)], fill=K, width=2)
c.line([(151, 99), (166, 92)], fill=K, width=1.4)  # arm, pointing
c.text((168, 100), "¡Tierra!", 10, fill=K, font=SERIF_BI, anchor="lm")

# pennants: Castile red/yellow
def pennant(x, y, L, col1, col2):
    pts = [(x, y), (x + L, y + 4 + 2 * math.sin(1)), (x, y + 7)]
    c.poly(pts, fill=col1, outline=K, width=0.8)
    c.poly([(x, y + 2.3), (x + L * 0.66, y + 4.4), (x, y + 4.7)], fill=col2)
pennant(148, 84, 40, R, Y)
pennant(212, 152, 26, Y, R)
pennant(78, 206, 26, R, Y)
# small gulls near the island
for gx, gy, s in [(250, 238, 6), (268, 226, 5), (232, 252, 4), (290, 246, 4.5)]:
    c.line([(gx - s, gy - s * 0.3), (gx - s * 0.4, gy - s * 0.6), (gx, gy), (gx + s * 0.4, gy - s * 0.6), (gx + s, gy - s * 0.3)], fill=K, width=1.1)

# foreground breaking wave, Hokusai-ish fingers
base = 560
pts = [(-5, 600), (-5, base)]
for i in range(41):
    x = i * 10
    pts.append((x, base - 18 * math.sin(i * 0.33) - 10))
pts += [(405, base), (405, 600)]
c.poly(pts, fill=B, outline=K, width=1.5)
for i in range(41):
    x = i * 10
    yy = base - 18 * math.sin(i * 0.33) - 10
    for k in range(3):
        c.arc(x + 4, yy + 2 + k * 4, 5 - k, 4 - k * 0.8, 180, 360, fill=Wt, width=1.4)
for k in range(4):
    yy = 575 + k * 6
    c.line([(0, yy), (400, yy)], fill=Wt if k % 2 == 0 else K, width=0.8)

# cartouche
c.rect(14, 18, 132, 50, fill=Wt, outline=K, width=1.2)
c.rect(17, 21, 129, 47, outline=R, width=0.8)
c.text((73, 29), "GUANAHANÍ", 11, fill=K, font=SERIF_B, anchor="mm", spacing=1)
c.text((73, 41), "12 · X · 1492 · alba", 8.5, fill=R, font=SERIF_I, anchor="mm")

finish(c)
