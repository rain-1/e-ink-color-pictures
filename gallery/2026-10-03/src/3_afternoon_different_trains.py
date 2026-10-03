"""Different Trains (1988): 'from Chicago to New York, 1939' — the American side of the piece,
the boy Reich travelling between his parents. A streamliner crosses a truss bridge in afternoon light."""
import math, sys, os, random
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from ink import *

random.seed(1939)
rng = np.random.default_rng(1939)
c = Canvas(B)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)

# --- sky: deep blue thinning to paper at the horizon -------------------------
HOR = 300
c.paste_mask(ramp([B, B, Wh], np.clip(yy / HOR, 0, 1) ** 1.5), yy < HOR + 2)

# --- cumulus: metaballs, lit from the upper right, flat grey-blue bases -------
def cloud_field(blobs):
    f = np.zeros((H, W), np.float32)
    for bx, by, br in blobs:
        f += br * br / ((xx - bx) ** 2 + ((yy - by) * 1.25) ** 2 + 1)
    return f
clouds = [
    [(50 + i * 24 + rng.uniform(-6, 6), 150 - math.sin(i / 7 * math.pi) * 40 + rng.uniform(-6, 6), 18 + math.sin(i / 7 * math.pi) * 12) for i in range(8)],
    [(240 + i * 20 + rng.uniform(-5, 5), 78 - math.sin(i / 6 * math.pi) * 26 + rng.uniform(-4, 4), 13 + math.sin(i / 6 * math.pi) * 9) for i in range(7)],
    [(20 + i * 13, 252 - math.sin(i / 5 * math.pi) * 9, 6 + math.sin(i / 5 * math.pi) * 3) for i in range(6)],
    [(290 + i * 14, 240 - math.sin(i / 5 * math.pi) * 10, 6 + math.sin(i / 5 * math.pi) * 4) for i in range(6)],
]
bases = [172, 96, 258, 246]

def shade(f, base, thr=2.0, d=4):
    m = (f > thr) & (yy < base)
    g = np.tanh(f / (thr * 2.5))                      # saturating density, no hot cores
    ahead = np.roll(np.roll(g, -d, 1), d, 0)          # density toward the sun (up-right)
    occl = np.clip((ahead - g) * 3, -1, 1)
    depth = np.clip((yy - (base - 22)) / 22, 0, 1)
    tone = np.clip(0.9 - occl * 1.4 - depth * 0.5, 0, 1)
    return m, tone

for blobs, base in zip(clouds, bases):
    m, tone = shade(cloud_field(blobs), base)
    c.paste_mask(ramp([B, Wh, Wh], tone), m)

# swallows / birds
for _ in range(7):
    bx, by = random.uniform(160, 380), random.uniform(150, 200)
    c.line([(bx - 4, by - 2), (bx, by), (bx + 4, by - 2)], K, 0.8)

# --- distant land ---------------------------------------------------------
# far ridge (blue-green), fields in screened bands, shelter belts
far = HOR - 8 + 6 * np.sin(xx / 47) + 3 * np.sin(xx / 13 + 1)
c.paste_mask(mix(B, G, 0.35), (yy > far) & (yy < HOR + 40))
# field strips receding: alternating stubble yellow, green, ploughed red-brown
y = HOR + 4
k = 0
while y < 372:
    hgt = 3 + (y - HOR) * 0.12
    fill = [mix(Y, G, 0.15), G, mix(R, K, 0.35), mix(Y, R, 0.3), mix(G, Y, 0.4)][k % 5]
    tilt = 0.06 * ((k % 3) - 1)
    m = (yy >= y + tilt * (xx - 200)) & (yy < y + hgt + tilt * (xx - 200))
    c.paste_mask(fill, m)
    y += hgt; k += 1
# furrow lines on the nearer fields
for fy in range(HOR + 30, 372, 3):
    if random.random() < 0.15:
        c.line([(0, fy), (W, fy + random.uniform(-1, 1))], K, 0.25)
# tree lines
for tx in list(range(0, 140, 6)) + list(range(250, 400, 7)):
    ty = HOR + 14 + (12 if tx > 200 else 0)
    c.ellipse(tx + random.uniform(-2, 2), ty, 4.5, 5 + random.uniform(0, 2), fill=G, outline=K, width=0.5)
# grain elevator and farm
c.rect(312, 250, 340, 318, fill=Wh, outline=K, width=0.8)
for i in range(4):
    c.rect(314 + i * 6.5, 256, 318 + i * 6.5, 318, fill=mix(Wh, K, 0.15))
c.rect(322, 236, 334, 252, fill=R, outline=K, width=0.8)
c.poly([(320, 236), (328, 228), (336, 236)], fill=K)
c.text((326, 290), "CO-OP", R, 4.5, anchor="mm")
c.rect(60, 302, 86, 318, fill=R, outline=K, width=0.7)
c.poly([(56, 303), (73, 292), (90, 303)], fill=K)
c.rect(70, 309, 76, 318, fill=K)
c.rect(96, 306, 112, 318, fill=Wh, outline=K, width=0.7)
c.poly([(94, 307), (104, 299), (114, 307)], fill=R, outline=K, width=0.6)
for wx in (100, 108):
    c.rect(wx - 1.5, 310, wx + 1.5, 313, fill=K)
# windmill
c.line([(140, 318), (144, 280), (148, 318)], K, 0.7)
c.line([(142, 300), (146, 300)], K, 0.5)
for a in range(12):
    ang = a * math.pi / 6
    c.line([(144, 280), (144 + 8 * math.cos(ang), 280 + 8 * math.sin(ang))], K, 0.6)

# telegraph line along the track
WIRE_Y = 336
for px in range(-10, W + 40, 46):
    c.line([(px, WIRE_Y - 32), (px, 384)], K, 1.4)
    c.line([(px - 7, WIRE_Y - 30), (px + 7, WIRE_Y - 30)], K, 1.1)
    c.line([(px - 5, WIRE_Y - 25), (px + 5, WIRE_Y - 25)], K, 1.0)
for wy in (WIRE_Y - 30, WIRE_Y - 25):
    for side in (-6, 6, -3, 3):
        pts = []
        for px in range(-10, W + 40, 46):
            for t in np.linspace(0, 1, 8)[:-1]:
                pts.append((px + side + 46 * t, wy + 1 + 4.5 * math.sin(math.pi * t)))
        c.line(pts, K, 0.35)

# --- river ----------------------------------------------------------------
RIV = 430
c.rect(0, 392, W, H, fill=B)
ry = np.clip((yy - 392) / 200, 0, 1)
c.paste_mask(ramp([Wh, B, B, K], ry * 0.9 + 0.08), yy > 392)
for i in range(140):  # glints
    gx, gy = random.uniform(0, W), random.uniform(396, 560)
    L = random.uniform(4, 16) * (1.2 - (gy - 396) / 200)
    c.line([(gx, gy), (gx + L, gy)], Wh, 0.5)

# --- bridge ---------------------------------------------------------------
DECK = 386
TOP = 318
# piers
for px in (40, 200, 360):
    c.poly([(px - 13, DECK + 6), (px + 13, DECK + 6), (px + 17, 480), (px - 17, 480)], fill=mix(Wh, K, 0.25), outline=K, width=0.8)
    for sy in range(DECK + 12, 480, 7):
        c.line([(px - 16, sy), (px + 16, sy)], K, 0.4)
        off = 0 if (sy // 7) % 2 else 6
        for sx in range(int(px - 14 + off), int(px + 14), 12):
            c.line([(sx, sy), (sx, sy + 7)], K, 0.4)
    # reflection
    c.paste_mask(mix(B, K, 0.6), (xx > px - 15) & (xx < px + 15) & (yy > 480) & (yy < 540) & (BAYER > (yy - 480) / 60))
# deck girder
c.rect(0, DECK, W, DECK + 7, fill=K)
c.line([(0, DECK + 3), (W, DECK + 3)], R, 0.8)
def truss(width_main, width_web):
    for x0, x1 in ((40, 200), (200, 360), (-120, 40), (360, 520)):
        n = 8
        c.line([(x0, DECK), (x0 + 18, TOP), (x1 - 18, TOP), (x1, DECK)], R, width_main)
        for i in range(1, n):
            x = x0 + (x1 - x0) * i / n
            c.line([(x, TOP), (x, DECK)], R, width_web)
        for i in range(n):
            xa = x0 + (x1 - x0) * i / n
            xb = x0 + (x1 - x0) * (i + 1) / n
            if i < n / 2:
                c.line([(xb, TOP), (xa, DECK)], R, width_web * 0.7)
            else:
                c.line([(xa, TOP), (xb, DECK)], R, width_web * 0.7)
        for i in range(n + 1):
            x = x0 + (x1 - x0) * i / n
            c.ellipse(x, TOP, 1.4, 1.4, fill=K)
            c.ellipse(x, DECK, 1.4, 1.4, fill=K)
        # portal bracing across the top
        for i in range(n):
            xa = x0 + (x1 - x0) * i / n
            c.line([(xa, TOP), (xa + (x1 - x0) / n, TOP + 6)], K, 0.4)

# far truss, seen through: thinner and darker
truss(1.2, 0.6)
# --- the train ------------------------------------------------------------
RAIL = DECK - 1
GREY = mix(Wh, K, 0.3)
LIGHT = mix(Wh, K, 0.12)
# coaches running back off the left edge
cx_ = 214
for car in range(3):
    x1 = cx_ - car * 98 - 6
    x0 = x1 - 92
    c.rect(x0, RAIL - 30, x1, RAIL - 6, fill=GREY, outline=K, width=0.8)
    c.rect(x0, RAIL - 30, x1, RAIL - 27, fill=K)
    c.rect(x0, RAIL - 14, x1, RAIL - 11, fill=B)
    for wx in range(int(x0) + 6, int(x1) - 6, 9):
        c.rect(wx, RAIL - 24, wx + 6, RAIL - 17, fill=K)
        c.rect(wx + 0.5, RAIL - 23.5, wx + 2.5, RAIL - 21.5, fill=Wh)
        if random.random() < 0.5:
            c.ellipse(wx + 3.5, RAIL - 18.5, 1.6, 1.6, fill=random.choice([Y, R, Wh]))
    for bx in (x0 + 12, x0 + 22, x1 - 22, x1 - 12):
        c.ellipse(bx, RAIL - 4, 4, 4, fill=K)
        c.ellipse(bx, RAIL - 4, 1.4, 1.4, fill=Wh)
    c.rect(x1, RAIL - 25, x1 + 6, RAIL - 10, fill=K)
# tender
c.rect(cx_, RAIL - 30, cx_ + 34, RAIL - 6, fill=GREY, outline=K, width=0.8)
c.rect(cx_, RAIL - 14, cx_ + 34, RAIL - 11, fill=B)
for bx in (cx_ + 8, cx_ + 17, cx_ + 26):
    c.ellipse(bx, RAIL - 4, 4, 4, fill=K)
# locomotive: a 1938 streamlined Hudson, shrouded, with the finned nose
lx = cx_ + 38
body = [(lx, RAIL - 34), (lx + 96, RAIL - 34)]
for t in np.linspace(0, math.pi / 2, 10):
    body.append((lx + 96 + 22 * math.sin(t), RAIL - 34 + 26 * (1 - math.cos(t))))
body += [(lx + 118, RAIL - 8), (lx, RAIL - 8)]
c.poly(body, fill=LIGHT, outline=K, width=1)
c.rect(lx, RAIL - 34, lx + 26, RAIL - 46, fill=LIGHT, outline=K, width=0.9)  # cab roof
c.rect(lx + 6, RAIL - 30, lx + 18, RAIL - 22, fill=K)
c.rect(lx + 7, RAIL - 29, lx + 11, RAIL - 25, fill=Wh)
c.rect(lx + 60, RAIL - 40, lx + 70, RAIL - 34, fill=K)  # stack
# the blue speed stripe and the finned prow
c.poly([(lx, RAIL - 18), (lx + 112, RAIL - 18), (lx + 117, RAIL - 15), (lx, RAIL - 15)], fill=B)
c.line([(lx + 100, RAIL - 30), (lx + 115, RAIL - 18)], K, 1.2)
c.ellipse(lx + 109, RAIL - 26, 3.2, 3.2, fill=Y, outline=K, width=0.7)  # headlamp
for f in range(3):
    c.line([(lx + 98 - f * 4, RAIL - 33 + f * 2), (lx + 112 - f * 2, RAIL - 33 + f * 2 + 8)], Wh, 0.5)
# skirt and driving wheels, red spoked, with side rods
c.rect(lx + 2, RAIL - 12, lx + 116, RAIL - 8, fill=K)
for i, wx in enumerate([lx + 36, lx + 54, lx + 72]):
    c.ellipse(wx, RAIL - 9, 8.5, 8.5, fill=K)
    c.ellipse(wx, RAIL - 9, 7, 7, fill=R)
    for s in range(10):
        a = s * math.pi / 5 + 0.3
        c.line([(wx, RAIL - 9), (wx + 6.5 * math.cos(a), RAIL - 9 + 6.5 * math.sin(a))], K, 0.5)
    c.ellipse(wx, RAIL - 9, 2, 2, fill=Wh, outline=K, width=0.4)
c.line([(lx + 34, RAIL - 6), (lx + 74, RAIL - 6)], Wh, 1.4)
for wx in (lx + 92, lx + 104, lx + 14, lx + 22):
    c.ellipse(wx, RAIL - 5, 4.5, 4.5, fill=K)
    c.ellipse(wx, RAIL - 5, 1.5, 1.5, fill=Wh)
c.text((lx + 44, RAIL - 26), "NEW YORK CENTRAL", K, 4.2, anchor="lm")

# steam: a long plume blown back over the train, lit from the right
f = np.zeros((H, W), np.float32)
px, py = lx + 65, RAIL - 42
for i in range(28):
    t = i / 27
    bx = px - t * 300 + math.sin(i * 1.7) * 6
    by = py - 30 * math.sqrt(t) + math.sin(i * 0.9) * 4
    br = 5 + t * 11
    f += br * br / ((xx - bx) ** 2 + ((yy - by) * 1.3) ** 2 + 1)
m, tone = shade(f, RAIL - 36, thr=2.0, d=3)
c.paste_mask(ramp([B, Wh, Wh], tone - np.clip((px - xx) / 900, 0, 0.3)), m)

# near truss, in front of the train
truss(2.6, 1.2)

# reeds and a foreground bank, lower left
c.poly([(0, 560), (60, 548), (120, 572), (150, 600), (0, 600)], fill=G)
c.poly([(400, 575), (330, 585), (300, 600), (400, 600)], fill=G)
for i in range(70):
    rx = random.uniform(0, 140) if i < 50 else random.uniform(310, 400)
    base = 600
    top = random.uniform(500, 560)
    bend = random.uniform(-10, 10)
    c.line([(rx, base), (rx + bend * 0.4, (base + top) / 2), (rx + bend, top)], random.choice([K, G, G, Y]), 0.9)
    if random.random() < 0.25:
        c.ellipse(rx + bend, top - 4, 1.8, 5, fill=R, outline=K, width=0.4)

c.rect(0, 0, W, 16, fill=K)
c.text((200, 8.5), "DIFFERENT TRAINS · FROM CHICAGO TO NEW YORK · 1939", Wh, 6.8, anchor="mm")
c.save()
