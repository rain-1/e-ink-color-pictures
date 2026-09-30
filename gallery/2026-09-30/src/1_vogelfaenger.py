"""1 · Morning — Der Vogelfänger. Papageno's cage hung on an autumn branch at sunrise over
Vienna: an onion-domed cage full of songbirds, the door open, one bird already out,
St Stephen's zig-zag roof and spire on the skyline, the pan-pipes hanging from the hook."""
import math, random
import numpy as np
from common import *

random.seed(30)
c = Canvas(Wh)
HOR = 505
# sky: white above, screened into yellow toward the horizon, with the sun rising
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
sky = np.clip((yy - 40) / (HOR - 40), 0, 1) ** 0.9
c.tone(lambda d, s: d.rectangle([0, 0, W * s, HOR * s], fill=255), sky, Y, Wh)
c.snapshot_layer()
SX, SY = 300, HOR - 34
for i in range(38):                      # sun rays, alternating long/short
    a = math.pi + (i + 0.5) * math.pi / 38
    r1 = 600 if i % 2 == 0 else 180
    c.line([(SX + 60 * math.cos(a), SY + 60 * math.sin(a)), (SX + r1 * math.cos(a), SY + r1 * math.sin(a))], R if i % 2 == 0 else Y, 0.9)
c.ell(SX, SY, 70, fill=R); c.ell(SX, SY, 56, fill=Y)
for k in range(5): c.line([(SX - 40, SY - 8 - k * 7), (SX + 40, SY - 8 - k * 7)], R, 1)

# distant flock
for i in range(9):
    fx, fy = 262 + i * 13 + random.uniform(-4, 4), 128 + math.sin(i) * 10 + i * 3
    c.line([(fx - 4, fy - 2), (fx, fy), (fx + 4, fy - 2)], K, 0.9)

# Vienna skyline: houses, domes, and the Stephansdom with its patterned roof
c.rect(0, HOR, W, H, fill=B)
x = 0
while x < W:                           # house fronts
    w = random.choice([18, 22, 26, 30]); h = random.choice([28, 34, 40, 46])
    if 20 < x < 130: x += w; continue
    c.rect(x, HOR - h, x + w, HOR + 1, fill=B, outline=K, width=0.7)
    c.poly([(x - 1, HOR - h), (x + w / 2, HOR - h - 12), (x + w + 1, HOR - h)], fill=R, outline=K, width=0.7)
    for wy in range(HOR - h + 6, HOR - 4, 9):
        for wx in range(x + 4, x + w - 4, 7):
            c.rect(wx, wy, wx + 3, wy + 5, fill=Y if random.random() < 0.35 else K)
    x += w
for dx, dy in ((176, 58), (372, 52)):  # baroque domes
    c.rect(dx - 16, HOR - dy + 10, dx + 16, HOR, fill=B, outline=K, width=0.7)
    c.d.pieslice([(dx - 16) * 2, (HOR - dy - 6) * 2, (dx + 16) * 2, (HOR - dy + 26) * 2], 180, 360, fill=G, outline=K, width=2)
    c.line([(dx, HOR - dy - 6), (dx, HOR - dy - 18)], K, 1); c.ell(dx, HOR - dy - 19, 2, fill=Y)
# cathedral nave with diamond-tiled roof
nx0, nx1, ny = 26, 126, HOR - 36
c.rect(nx0, ny, nx1, HOR + 1, fill=Wh, outline=K, width=0.8)
for wx in range(nx0 + 8, nx1 - 6, 12):
    c.poly([(wx, HOR - 4), (wx, ny + 12), (wx + 3, ny + 7), (wx + 6, ny + 12), (wx + 6, HOR - 4)], fill=B, outline=K, width=0.5)
roof = [(nx0 - 4, ny), (nx0 + 18, ny - 46), (nx1 - 18, ny - 46), (nx1 + 4, ny)]
c.poly(roof, fill=Y, outline=K, width=0.9)
for row in range(7):                     # zig-zag tiles, the famous chevrons
    y0 = ny - 4 - row * 6
    xl = nx0 - 2 + row * 3.1; xr = nx1 + 2 - row * 3.1
    pts = []; t = 0
    xs = np.arange(xl, xr, 6)
    for i, xv in enumerate(xs): pts.append((xv, y0 - (3 if i % 2 else 0)))
    col = [R, G, K][row % 3]
    c.line(pts, col, 1.6)
# south tower: stacked tiers + spire
tx = 81
c.poly([(tx - 13, HOR), (tx - 13, HOR - 70), (tx + 13, HOR - 70), (tx + 13, HOR)], fill=Wh, outline=K, width=0.8)
for k, (w, h) in enumerate([(11, 30), (8, 32), (5, 36)]):
    yb = HOR - 70 - sum(hh for _, hh in [(11, 30), (8, 32), (5, 36)][:k])
    c.poly([(tx - w - 2, yb), (tx - w, yb - h), (tx + w, yb - h), (tx + w + 2, yb)], fill=Wh, outline=K, width=0.8)
    c.poly([(tx - 3, yb - 4), (tx - 3, yb - h + 8), (tx, yb - h + 4), (tx + 3, yb - h + 8), (tx + 3, yb - 4)], fill=B)
    for sx in (-w, w): c.poly([(tx + sx - 2, yb - h), (tx + sx, yb - h - 8), (tx + sx + 2, yb - h)], fill=K)
c.poly([(tx - 4, HOR - 168), (tx, HOR - 214), (tx + 4, HOR - 168)], fill=Wh, outline=K, width=0.8)
for k in range(6): c.line([(tx - 3 + k * .5, HOR - 172 - k * 7), (tx + 3 - k * .5, HOR - 172 - k * 7)], K, 0.6)
c.ell(tx, HOR - 216, 2, fill=Y, outline=K, width=0.5)
# the Danube glint + foreground roofs
for i in range(14):
    y = 530 + i * 5
    for j in range(8):
        xx0 = random.uniform(0, W); c.line([(xx0, y), (xx0 + random.uniform(8, 26), y)], Wh if i < 6 else Y, 0.9)
for k in range(9):
    x0 = -20 + k * 52
    c.poly([(x0, H), (x0 + 26, 568 + (k % 3) * 6), (x0 + 52, H)], fill=R, outline=K, width=0.8)
    for j in range(4): c.line([(x0 + 8 + j * 4, H - 6 - j * 5), (x0 + 44 - j * 4, H - 6 - j * 5)], K, 0.6)
    c.rect(x0 + 34, 572 + (k % 3) * 6, x0 + 40, 590, fill=K)

# branch across the top, with late-September leaves
br = [(-10, 58), (60, 48), (130, 56), (200, 44), (280, 50), (350, 38), (410, 46)]
c.line(br, K, 7); c.line([(p[0], p[1] - 2) for p in br], R, 1.2)
for t in (80, 250, 330):
    c.line([(t, 50), (t + 16, 22), (t + 30, 14)], K, 3)
for i in range(52):
    px = -6 + i * 8.2 + random.uniform(-4, 4); py = 48 + random.uniform(-30, 22)
    if abs(px - 196) < 10: continue
    ang = random.uniform(0, math.pi * 2)
    col = random.choice([G, G, R, Y, R, G])
    L = random.uniform(15, 23)
    tip = (px + L * math.cos(ang), py + L * math.sin(ang))
    lf = [(px, py), (px + L * .5 * math.cos(ang) - 6.5 * math.sin(ang), py + L * .5 * math.sin(ang) + 6.5 * math.cos(ang)), tip,
          (px + L * .5 * math.cos(ang) + 6.5 * math.sin(ang), py + L * .5 * math.sin(ang) - 6.5 * math.cos(ang))]
    c.poly(lf, fill=col, outline=K, width=0.8); c.line([(px, py), tip], K, 0.5)
# hanging hook + pan-pipes
CX = 196
c.line([(CX, 50), (CX, 88)], K, 1.6); c.d.arc([(CX - 6) * 2, 44 * 2, (CX + 6) * 2, 56 * 2], 180, 360, fill=K, width=3)
pp_x = 250
c.line([(CX + 2, 70), (pp_x + 10, 94)], K, 0.8); c.line([(CX + 2, 70), (pp_x + 44, 94)], K, 0.8)
for k in range(7):
    c.rect(pp_x + k * 7, 94, pp_x + k * 7 + 6, 150 - k * 6, fill=Y, outline=K, width=0.8)
    c.ell(pp_x + k * 7 + 3, 96, 1.6, fill=K)
c.rect(pp_x - 2, 108, pp_x + 51, 114, fill=R, outline=K, width=0.8)

# the cage: surface of revolution, perspective ellipses; back bars, birds, front bars
top, dome_b, body_b = 100, 212, 398
RAD = 118
def radius(y):
    if y < dome_b:     # onion dome
        t = (y - top) / (dome_b - top)
        return RAD * (math.sin(t * math.pi * 0.5) ** 1.3) * (1 + 0.16 * math.sin(t * math.pi * 1.4))
    return RAD
TILT = 0.16
ys = np.linspace(top, body_b, 90)
NB = 30
def bar_pts(th):
    return [(CX + radius(y) * math.sin(th), y + radius(y) * TILT * math.cos(th)) for y in ys]
for i in range(NB):
    th = 2 * math.pi * i / NB
    if math.cos(th) < 0: c.line(bar_pts(th), B, 1.0)
c.d.chord([(CX - RAD) * 2, (body_b - RAD * TILT) * 2, (CX + RAD) * 2, (body_b + RAD * TILT) * 2], 180, 360, fill=None, outline=B, width=2)
c.poly(oval(CX, body_b, RAD, RAD * TILT, 0, 60), fill=Y, outline=K, width=1)   # floor of cage
for k in range(1, 6): c.poly(oval(CX, body_b, RAD * k / 6, RAD * TILT * k / 6, 0, 48), outline=R, width=0.7)
# seed cup + water dish
c.poly(oval(CX - 50, body_b - 2, 14, 4), fill=B, outline=K); c.poly(oval(CX + 56, body_b + 4, 12, 3.5), fill=R, outline=K)
for k in range(6): c.ell(CX - 56 + k * 2.5, body_b - 4, 0.9, fill=Y)
# perches
perches = [(250, CX - 96, CX + 64), (312, CX - 70, CX + 100), (372, CX - 104, CX + 44)]
for py, x0, x1 in perches:
    c.line([(x0, py), (x1, py)], K, 3.4); c.line([(x0, py - 1), (x1, py - 1)], R, 1)
# swing ring
c.line([(CX + 30, 140), (CX + 18, 196)], K, 0.8); c.line([(CX + 30, 140), (CX + 46, 196)], K, 0.8)
c.line([(CX + 16, 196), (CX + 48, 196)], K, 2.6)
birds = [((CX - 66, 250), 1.3, 1, R, B, Y, None, False), ((CX - 12, 250), 1.15, -1, Y, G, Wh, R, True),
         ((CX + 40, 250), 1.2, 1, B, R, Wh, None, False), ((CX - 36, 312), 1.35, 1, G, Y, Y, R, False),
         ((CX + 22, 312), 1.2, -1, Y, R, Wh, B, True), ((CX + 76, 312), 1.05, -1, R, K, Wh, K, False),
         ((CX - 78, 372), 1.3, 1, B, Y, Wh, None, True), ((CX - 22, 372), 1.15, -1, R, G, Y, Y, False),
         ((CX + 32, 196), 1.05, 1, G, R, Y, None, False), ((CX + 30, body_b - 2), 1.1, -1, Y, B, Wh, R, False)]
for (bx, by), s, f, bo, wi, be, he, cr in birds:
    bird(c, bx, by, s, f, bo, wi, be, he, crest=cr)
# front bars and rings
for i in range(NB):
    th = 2 * math.pi * i / NB
    if math.cos(th) >= 0: c.line(bar_pts(th), K, 1.2)
for y in (dome_b, 300, 370, body_b):
    c.poly(oval(CX, y, radius(y), radius(y) * TILT, 0, 72), outline=K, width=1.4 if y in (dome_b, body_b) else 1)
for y in np.linspace(top + 20, dome_b - 18, 4):
    pts = [(CX + radius(y) * math.sin(t), y + radius(y) * TILT * math.cos(t)) for t in np.linspace(-math.pi / 2, math.pi / 2, 30)]
    c.line(pts, K, 0.9)
# the open door, swung outward on the right
dx0, dy0, dy1 = CX + 64, 300, 384
c.poly([(dx0, dy0), (dx0 + 44, dy0 + 8), (dx0 + 44, dy1 + 8), (dx0, dy1)], outline=K, width=1.3)
for k in range(1, 6): c.line([(dx0 + k * 7.3, dy0 + k * 1.33), (dx0 + k * 7.3, dy1 + k * 1.33)], K, 0.9)
# base: scalloped plinth with bands
c.poly(oval(CX, body_b + 6, RAD + 6, (RAD + 6) * TILT, 0, 72), fill=R, outline=K, width=1.2)
c.rect(CX - RAD - 6, body_b + 6, CX + RAD + 7, body_b + 24, fill=R)
c.poly(oval(CX, body_b + 24, RAD + 6, (RAD + 6) * TILT, 0, 72), fill=R, outline=K, width=1.2)
c.line([(CX - RAD - 6, body_b + 6), (CX - RAD - 6, body_b + 24)], K, 1.2); c.line([(CX + RAD + 6, body_b + 6), (CX + RAD + 6, body_b + 24)], K, 1.2)
for t in np.linspace(-math.pi / 2 + 0.1, math.pi / 2 - 0.1, 22):   # scallops on the band
    x = CX + (RAD + 6) * math.sin(t); y = body_b + 15 + (RAD + 6) * TILT * math.cos(t)
    c.ell(x, y, 3.6, 4.4, fill=Y, outline=K, width=0.6)
# finial: ball, ring
c.ell(CX, top - 6, 7, fill=Y, outline=K, width=1); c.ell(CX, top - 6, 2.5, fill=R)
c.ell(CX, 90, 4, outline=K, width=1.4)

# escaped: one on the door, two flying off to the sun
bird(c, dx0 + 42, dy0 + 8, 1.0, 1, G, R, Y, None, crest=True)
bird(c, 330, 250, 0.9, 1, R, Y, Wh, None, flying=True, legs=False)
bird(c, 360, 205, 0.7, 1, B, G, Y, None, flying=True, legs=False)
c.text((14, 100), "Der Vogelfänger", K, 13, "lm", bold=True)
c.text((14, 118), "bin ich ja", R, 12, "lm", bold=True)
c.finish()
