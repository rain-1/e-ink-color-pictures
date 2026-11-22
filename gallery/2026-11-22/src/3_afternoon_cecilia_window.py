"""St Cecilia at the organ - a lancet of stained glass for her feast day.
Leaded quarries, painted folds, and stippled matting worked into the coloured glass
close to every lead (white and yellow are left clean so they glow)."""
import math, os, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from common import *

rng = random.Random(1122)
d = D(B)
LW = 1.5                                   # lead width
YS, RAD, CL, CR, X0, X1, YB = 262, 250, 128, 272, 22, 378, 580

def inside(x, y, inset=0.0):
    if y > YB - inset: return False
    if y >= YS: return X0 + inset <= x <= X1 - inset
    return math.hypot(x - CR, y - YS) <= RAD - inset and math.hypot(x - CL, y - YS) <= RAD - inset

# ---- field: blue diamond quarries, a few painted with stars
Q = 15
d.rect(0, 0, W, H, fill=B)
for k in range(-50, 80):
    d.line([(k * Q, 0), (k * Q + H, H)], K, 0.9)
    d.line([(k * Q, 0), (k * Q - H, H)], K, 0.9)
for i in range(-2, 30):
    for j in range(0, 44):
        cx, cy = i * Q + (j % 2) * Q / 2, j * Q / 2
        q = rng.random()
        if q < 0.16:
            for a in range(0, 180, 45):
                dx, dy = 3.4 * math.cos(math.radians(a)), 3.4 * math.sin(math.radians(a))
                d.line([(cx - dx, cy - dy), (cx + dx, cy + dy)], Y, 0.6)
        elif q < 0.30:
            d.ell(cx, cy, 1.5, fill=WH)
        elif q < 0.38:
            d.poly([(cx, cy - 4), (cx + 4, cy), (cx, cy + 4), (cx - 4, cy)], fill=G, outline=K, w=0.5)

# ---- tracery lights in the arch head: a rose, two stars
def rose(cx, cy, r):
    d.ell(cx, cy, r + 6, fill=Y, outline=K, w=LW)
    for i in range(24):
        a = math.radians(i * 15)
        d.line([(cx + (r + 1) * math.cos(a), cy + (r + 1) * math.sin(a)), (cx + (r + 6) * math.cos(a), cy + (r + 6) * math.sin(a))], K, 0.6)
    d.ell(cx, cy, r, fill=WH, outline=K, w=LW)
    for i in range(5):                                        # green sepals
        a = math.radians(-90 + 36 + i * 72)
        d.poly([(cx + r * 0.98 * math.cos(a), cy + r * 0.98 * math.sin(a)), (cx + r * 0.5 * math.cos(a - 0.3), cy + r * 0.5 * math.sin(a - 0.3)), (cx + r * 0.5 * math.cos(a + 0.3), cy + r * 0.5 * math.sin(a + 0.3))], fill=G, outline=K, w=0.6)
    for rr, col, off in ((0.56, R, 0), (0.30, WH, 36)):
        for i in range(5):
            a = math.radians(-90 + off + i * 72)
            d.ell(cx + r * rr * math.cos(a), cy + r * rr * math.sin(a), r * rr * 0.72, fill=col, outline=K, w=0.9)
    for i in range(5):
        a = math.radians(-90 + i * 72)
        d.arc(cx + r * 0.56 * math.cos(a), cy + r * 0.56 * math.sin(a), r * 0.28, r * 0.28, math.degrees(a) - 70, math.degrees(a) + 70, K, 0.5)
    d.ell(cx, cy, r * 0.17, fill=Y, outline=K, w=0.8)
    for i in range(8):
        a = math.radians(i * 45)
        d.ell(cx + r * 0.1 * math.cos(a), cy + r * 0.1 * math.sin(a), 0.6, fill=K)
rose(200, 92, 30)
for sx in (118, 282):
    d.ell(sx, 168, 19, fill=R, outline=K, w=LW); d.ell(sx, 168, 14.5, outline=Y, w=0.8)
    pts = []
    for i in range(16):
        a = math.radians(i * 22.5 - 90); rr = 12.5 if i % 2 == 0 else 5
        pts.append((sx + rr * math.cos(a), 168 + rr * math.sin(a)))
    d.poly(pts, fill=Y, outline=K, w=0.8); d.ell(sx, 168, 2.4, fill=WH, outline=K, w=0.5)

# ---- tiled floor and green sward with lilies
FY = 468
d.rect(0, FY, W, 500, fill=WH)
for i in range(0, 34):
    for j in range(3):
        x = i * 12 - 4 + j * 4
        d.poly([(x, FY + j * 11), (x + 12, FY + j * 11), (x + 16, FY + j * 11 + 11), (x + 4, FY + j * 11 + 11)], fill=(Y if (i + j) % 2 else WH), outline=K, w=0.7)
d.line([(0, FY), (W, FY)], K, LW)

# ---- the organ
PX0, PN = 226, 11
pipe_bot = 338
d.rect(PX0 - 8, pipe_bot - 6, PX0 + PN * 11.5 + 6, FY, fill=R, outline=K, w=LW)             # case
for i in range(PN):
    px = PX0 + i * 11.5
    top = 196 + i * 9.5 + 3 * math.sin(i * 1.3)
    d.rect(px, top, px + 9, pipe_bot, fill=Y if i % 2 == 0 else WH, outline=K, w=1.1)
    d.poly([(px, pipe_bot), (px + 9, pipe_bot), (px + 4.5, pipe_bot + 9)], fill=Y if i % 2 == 0 else WH, outline=K, w=0.9)
    d.poly([(px + 1.8, pipe_bot - 12), (px + 7.2, pipe_bot - 12), (px + 7.2, pipe_bot - 8.5), (px + 4.5, pipe_bot - 5.5), (px + 1.8, pipe_bot - 8.5)], fill=K)
    d.line([(px + 2.2, top + 3), (px + 2.2, pipe_bot - 15)], K, 0.4)
    d.ell(px + 4.5, top, 4.5, 1.6, fill=K)
# pipe-shade: carved band across the pipes
band = [(PX0 - 4, 268), (PX0 + PN * 11.5 + 2, 300), (PX0 + PN * 11.5 + 2, 308), (PX0 - 4, 276)]
d.poly(band, fill=G, outline=K, w=1)
for i in range(12):
    t = (i + 0.5) / 12
    d.ell(PX0 - 4 + t * (PN * 11.5 + 6), 272 + t * 32, 2, fill=Y, outline=K, w=0.4)
# case panels with quatrefoils
for i in range(4):
    x0 = PX0 - 3 + i * 32.5
    d.rect(x0, 362, x0 + 28, 452, fill=R, outline=K, w=1)
    d.rect(x0 + 3, 365, x0 + 25, 449, outline=Y, w=0.7)
    for cy in (386, 428):
        for (ox, oy) in ((0, -5), (5, 0), (0, 5), (-5, 0)):
            d.ell(x0 + 14 + ox, cy + oy, 4.6, fill=B if cy < 400 else G, outline=K, w=0.7)
        d.ell(x0 + 14, cy, 2.2, fill=Y, outline=K, w=0.5)
    d.poly([(x0 + 14, 400), (x0 + 19, 407), (x0 + 14, 414), (x0 + 9, 407)], fill=Y, outline=K, w=0.6)
d.rect(PX0 - 12, 452, PX0 + PN * 11.5 + 10, FY, fill=Y, outline=K, w=1.1)                    # plinth
for x in range(PX0 - 8, int(PX0 + PN * 11.5 + 8), 7):
    d.line([(x, 455), (x, FY - 2)], K, 0.4)
# keyboard
KX0, KX1, KY = 186, PX0 - 8, 344
d.poly([(KX0, KY), (KX1, KY - 4), (KX1, KY + 12), (KX0, KY + 9)], fill=WH, outline=K, w=1.1)
for i in range(1, 9):
    x = KX0 + i * (KX1 - KX0) / 9
    d.line([(x, KY - 0.4 * i), (x, KY + 9 + 0.3 * i)], K, 0.5)
    if i % 7 not in (3, 0):
        d.rect(x - 1.2, KY - 0.4 * i, x + 1.2, KY + 4.5, fill=K)
d.poly([(KX0 + 2, KY + 9), (KX1, KY + 12), (KX1, KY + 22), (KX0 + 12, KY + 15)], fill=R, outline=K, w=0.9)
# music desk with an open book
d.poly([(196, 316), (226, 300), (226, 330), (196, 338)], fill=WH, outline=K, w=1)
d.line([(211, 308), (211, 334)], K, 0.6)
for k in range(4):
    d.line([(198.5, 320 + k * 4 - 0), (209, 314.5 + k * 4)], K, 0.4); d.line([(213, 312.5 + k * 4), (224, 306.5 + k * 4)], K, 0.4)
for (nx, ny) in [(201, 321), (205, 323), (207, 318), (215, 314), (219, 316), (222, 309)]:
    d.ell(nx, ny, 1.1, 0.9, fill=K)

# ---- the saint
HX, HY = 146, 214
# mantle behind (green), falling from the shoulder to the floor
d.poly([(120, 246), (100, 300), (82, 380), (70, FY + 4), (128, FY + 4), (126, 380), (132, 300), (140, 246)], fill=G, outline=K, w=LW)
for k in range(5):
    d.line(bez((116 - k * 2, 262 + k * 6), (96 - k * 3 + k * 9, 360), (78 + k * 11, FY + 2), 14), K, 0.7)
d.line(bez((84, 392), (100, 400), (124, 394)), Y, 1.6)                                    # gold hem
d.line(bez((72, 458), (98, 464), (128, 458)), Y, 1.6)
# bench
d.rect(92, 372, 176, 384, fill=Y, outline=K, w=1.1)
for x in (98, 164):
    d.rect(x, 384, x + 8, FY, fill=Y, outline=K, w=1)
d.rect(96, 420, 172, 426, fill=Y, outline=K, w=0.8)
# gown: bodice + skirt
skirt = [(124, 300), (116, 372), (104, FY + 6), (212, FY + 6), (204, 420), (196, 372), (176, 318), (170, 298)]
d.poly(skirt, fill=R, outline=K, w=LW)
for k, (x0, x1, c) in enumerate([(130, 118, 8), (142, 136, 4), (154, 158, -3), (164, 180, -6), (172, 198, -10)]):
    d.line(bez((x0, 312), ((x0 + x1) / 2 + c, 390), (x1, FY + 4), 16), K, 0.9)
    d.line(bez((x0 + 3, 350), ((x0 + x1) / 2 + c + 3, 410), (x1 + 4, FY + 2), 12), K, 0.4)
d.poly([(104, FY - 4), (212, FY - 4), (212, FY + 6), (104, FY + 6)], fill=Y, outline=K, w=0.9)   # hem
for x in range(108, 212, 8):
    d.ell(x, FY + 1, 1.5, fill=R, outline=K, w=0.4)
d.poly([(196, FY + 6), (214, FY + 6), (218, FY + 12), (198, FY + 12)], fill=K)                # slipper
bod = [(126, 244), (120, 300), (172, 300), (170, 246), (158, 236), (136, 236)]
d.poly(bod, fill=R, outline=K, w=LW)
d.poly([(120, 293), (172, 293), (172, 301), (120, 301)], fill=Y, outline=K, w=0.9)            # girdle
for x in range(124, 172, 6):
    d.ell(x, 297, 1.3, fill=B)
d.poly([(138, 236), (147, 252), (157, 236)], fill=WH, outline=K, w=0.9)                       # neckline
d.line([(147, 252), (147, 292)], K, 0.6)
for yy in range(258, 290, 7):
    d.ell(147, yy, 1.3, fill=Y, outline=K, w=0.4)
# arms reaching to the keys: blue sleeves, white cuffs, hands
for (sx, sy, ex, ey, c) in [(166, 250, 198, 338, 14), (160, 254, 190, 346, 4)]:
    pts = bez((sx, sy), (sx + c + 6, sy + 52), (ex, ey), 16)
    d.line(pts, K, 12.5); d.line(pts, B, 10)
    d.line(bez((sx + 2, sy + 10), (sx + c + 6, sy + 50), (ex - 3, ey - 6), 12), WH, 0.5)
    d.line([pts[-2], pts[-1]], K, 12.5); d.line([pts[-2], (ex + 1, ey + 1)], WH, 9.5)
    d.poly([(ex - 2, ey), (ex + 9, ey - 3), (ex + 12, ey + 1), (ex + 4, ey + 5)], fill=WH, outline=K, w=0.8)
    d.line([(ex + 5, ey - 1), (ex + 11, ey - 1)], K, 0.4)
# halo
d.ell(HX, HY, 31, fill=Y, outline=K, w=LW); d.ell(HX, HY, 26.5, outline=R, w=1.4)
for i in range(28):
    a = math.radians(i * 360 / 28)
    d.ell(HX + 28.8 * math.cos(a), HY + 28.8 * math.sin(a), 0.8, fill=K)
# hair, flowing back over the mantle
hair = bez((HX - 4, HY - 18), (HX - 30, HY - 12), (HX - 22, HY + 30), 12) + bez((HX - 22, HY + 30), (HX - 34, HY + 60), (HX - 22, HY + 86), 12) + bez((HX - 10, HY + 70), (HX - 14, HY + 40), (HX - 6, HY + 20), 10)
d.poly(hair + [(HX + 12, HY - 16)], fill=Y, outline=K, w=1.1)
for k in range(5):
    d.line(bez((HX - 6 - k * 2, HY - 14 + k), (HX - 24 - k, HY + 10), (HX - 16 - k * 1.6, HY + 74 - k * 4), 14), K, 0.5)
# neck + face (three-quarter, looking up to the right)
d.poly([(HX - 3, HY + 12), (HX + 7, HY + 12), (HX + 9, HY + 24), (HX - 6, HY + 24)], fill=WH, outline=K, w=0.9)
face = bez((HX - 10, HY - 12), (HX + 4, HY - 22), (HX + 14, HY - 10), 8) + bez((HX + 14, HY - 10), (HX + 17, HY + 4), (HX + 9, HY + 15), 8) + bez((HX + 9, HY + 15), (HX - 4, HY + 20), (HX - 11, HY + 4), 8)
d.poly(face, fill=WH, outline=K, w=1.1)
d.poly(bez((HX - 12, HY - 8), (HX - 2, HY - 26), (HX + 15, HY - 9), 10) + bez((HX + 15, HY - 9), (HX + 2, HY - 15), (HX - 9, HY - 2), 8), fill=Y, outline=K, w=0.9)
d.arc(HX + 1.5, HY - 3.5, 3.2, 2.2, 190, 350, K, 0.7); d.ell(HX + 2, HY - 3.2, 1.0, fill=K)       # eyes
d.arc(HX + 10.5, HY - 4, 2.6, 2.0, 190, 350, K, 0.7); d.ell(HX + 10.8, HY - 3.8, 0.9, fill=K)
d.line([(HX - 2, HY - 7.5), (HX + 4.5, HY - 8)], K, 0.6); d.line([(HX + 8.5, HY - 8.2), (HX + 13, HY - 7.5)], K, 0.6)
d.line([(HX + 7, HY - 3), (HX + 8.6, HY + 4), (HX + 6, HY + 4.6)], K, 0.6)                      # nose
d.line(bez((HX + 3.5, HY + 9), (HX + 6.5, HY + 10.6), (HX + 9.5, HY + 8.6), 6), R, 1.1)         # mouth
d.ell(HX - 0.5, HY + 4.5, 1.6, fill=R)                                                          # cheek
# wreath of roses and lilies
for i in range(7):
    a = math.radians(196 + i * 22)
    wx, wy = HX + 2 + 15.5 * math.cos(a), HY - 4 + 14.5 * math.sin(a)
    d.ell(wx, wy, 3.1, fill=R if i % 2 == 0 else WH, outline=K, w=0.7); d.ell(wx, wy, 0.9, fill=Y)

# ---- lilies growing at the left, a dove coming down on the right
for (lx, lh) in [(40, 150), (56, 110), (30, 90)]:
    stem = bez((lx, FY), (lx - 8, FY - lh * 0.5), (lx + 4, FY - lh), 14)
    d.line(stem, K, 2.6); d.line(stem, G, 1.6)
    for k in (3, 6, 9):
        px, py = stem[k]
        sgn = 1 if k % 2 else -1
        d.poly(bez((px, py), (px + sgn * 12, py - 10), (px + sgn * 20, py - 2), 6) + bez((px + sgn * 20, py - 2), (px + sgn * 10, py + 1), (px, py), 6), fill=G, outline=K, w=0.7)
    tx, ty = stem[-1]
    for a in (-150, -115, -65, -30):
        ex, ey = tx + 15 * math.cos(math.radians(a)), ty + 15 * math.sin(math.radians(a))
        n = (-(ey - ty) / 15 * 4.5, (ex - tx) / 15 * 4.5)
        d.poly([(tx, ty), ((tx + ex) / 2 + n[0], (ty + ey) / 2 + n[1]), (ex, ey), ((tx + ex) / 2 - n[0], (ty + ey) / 2 - n[1])], fill=WH, outline=K, w=0.8)
    for a in (-100, -80):
        d.line([(tx, ty), (tx + 9 * math.cos(math.radians(a)), ty + 9 * math.sin(math.radians(a)))], K, 0.5)
        d.ell(tx + 9 * math.cos(math.radians(a)), ty + 9 * math.sin(math.radians(a)), 1.2, fill=Y)
dx, dy = 322, 212
for k in range(9):                                                                            # rays
    a = math.radians(205 + k * 6)
    d.line([(dx - 6, dy + 6), (dx - 6 + 80 * math.cos(a) * -1 * -1, dy + 6 - 80 * math.sin(a))], Y, 0.7)
d.poly(bez((dx - 16, dy + 12), (dx - 6, dy - 6), (dx + 10, dy - 2), 8) + bez((dx + 10, dy - 2), (dx + 4, dy + 12), (dx - 16, dy + 12), 8), fill=WH, outline=K, w=1)
d.poly([(dx + 2, dy - 2), (dx + 12, dy - 22), (dx + 18, dy - 20), (dx + 22, dy - 14), (dx + 10, dy + 2)], fill=WH, outline=K, w=1)
d.poly([(dx - 4, dy), (dx - 14, dy - 18), (dx - 6, dy - 18), (dx + 4, dy - 4)], fill=WH, outline=K, w=1)
for k in range(3):
    d.line([(dx + 6 + k * 2, dy - 4 + k), (dx + 13 + k * 3, dy - 19 + k * 2.5)], K, 0.4)
d.poly([(dx + 8, dy + 2), (dx + 24, dy + 8), (dx + 22, dy + 14), (dx + 6, dy + 8)], fill=WH, outline=K, w=0.9)
d.ell(dx - 12, dy + 8, 0.9, fill=K); d.poly([(dx - 16, dy + 12), (dx - 21, dy + 14), (dx - 15, dy + 14.5)], fill=Y, outline=K, w=0.4)

# ---- predella: scroll with her name and a line of chant
d.rect(0, 500, W, H, fill=R)
for i in range(0, 40):
    for j in range(0, 9):
        cx, cy = i * 11 + (j % 2) * 5.5, 504 + j * 9
        d.poly([(cx, cy - 3), (cx + 3, cy), (cx, cy + 3), (cx - 3, cy)], fill=Y if (i + j) % 3 == 0 else B, outline=K, w=0.5)
d.line([(0, 500), (W, 500)], K, 2.2)
sc = [(52, 512), (348, 512), (348, 566), (52, 566)]
d.poly([(40, 520), (58, 514), (58, 560), (40, 566), (47, 543)], fill=Y, outline=K, w=1)
d.poly([(360, 520), (342, 514), (342, 560), (360, 566), (353, 543)], fill=Y, outline=K, w=1)
d.poly(sc, fill=WH, outline=K, w=LW)
for k in range(4):                                                                            # four-line chant stave
    d.line([(64, 520 + k * 3.6), (336, 520 + k * 3.6)], R, 0.5)
neumes = [2, 2, 1, 2, 3, 2, 1, 0, 1, 2, 2, 3, 1, 2, 1, 0, 1, 1, 2, 3, 2, 1, 2, 2]
for i, n in enumerate(neumes):
    nx, ny = 76 + i * 10.8, 520 + (3 - n) * 3.6 - 1.8 + 1.8
    d.rect(nx - 1.7, ny - 1.6, nx + 1.7, ny + 1.6, fill=K)
    if i % 5 == 4: d.line([(nx + 1.7, ny), (nx + 1.7, ny + 6)], K, 0.5)
d.poly([(66, 519), (69, 519), (69, 526), (66, 526)], fill=K)
d.text(200, 541, "SANCTA CAECILIA", K, size=13.5, font="serif", spacing=1.6)
d.text(200, 557, "CANTANTIBVS ORGANIS · XXII NOV", R, size=6.6, font="sans", spacing=0.9)

# ---- ferramenta (saddle bars)
for yy in (150, 262, 380, 500):
    d.rect(0, yy - 1.3, W, yy + 1.3, fill=K)

# ---- border of jewels following the arch, then the stone
im = d.im
px = im.load()
BW = 11
stone = Image.new("RGB", im.size, WH)
sd = ImageDraw.Draw(stone)
for j in range(0, 62):                                                                         # ashlar
    y = j * 20 * S
    sd.line([(0, y), (W * S, y)], fill=K, width=2)
    for x in range(-(j % 2) * 30, W + 60, 60):
        sd.line([(x * S, y), (x * S, y + 20 * S)], fill=K, width=2)
        for _ in range(5):
            qx, qy = x + rng.uniform(4, 56), j * 20 + rng.uniform(3, 17)
            sd.line([(qx * S, qy * S), ((qx + rng.uniform(2, 7)) * S, qy * S)], fill=K, width=1 * S // 2)
mask = Image.new("L", im.size, 0)
mp = mask.load()
out = im.copy(); op = out.load(); sp = stone.load()
for Yp in range(H * S):
    y = (Yp + 0.5) / S
    for Xp in range(W * S):
        x = (Xp + 0.5) / S
        if inside(x, y, BW):
            if not inside(x, y, BW + LW): op[Xp, Yp] = K
            continue
        if inside(x, y, 0):
            if not inside(x, y, 1.8) or not inside(x, y, BW - 0.0) and inside(x, y, BW - 0.0 - 0) is None:
                op[Xp, Yp] = K; continue
            # jewel pattern, indexed along the border
            if y >= YS:
                t = y if (x < X0 + BW or x > X1 - BW) else x
            else:
                c = CR if x < 200 else CL
                t = math.degrees(math.atan2(YS - y, abs(x - c))) * 4.1
            seg = int(t // 11)
            f = t / 11 - seg
            if f < 0.1: op[Xp, Yp] = K
            else: op[Xp, Yp] = (R, WH, B, Y)[seg % 4] if not (seg % 4 == 1 and 0.4 < f < 0.72) else Y
            continue
        if inside(x, y, -5) and not inside(x, y, -3.4):
            op[Xp, Yp] = K
        elif inside(x, y, -9) and not inside(x, y, -8.2):
            op[Xp, Yp] = K
        else:
            op[Xp, Yp] = sp[Xp, Yp]
d.im = out
d.save()

# ---- matting: stipple the coloured glass dark close to the leads (at panel resolution)
path = os.environ.get("OUT_RAW", "out.png")
a = np.asarray(Image.open(path).convert("RGB")).copy()
isK = (a.sum(-1) == 0)
blur = np.asarray(Image.fromarray((isK * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2.4))).astype(float) / 255
bayer = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16 + 1 / 32
thr = np.tile(bayer, (150, 100))
col = np.zeros(a.shape[:2], bool)
for c in (R, B, G):
    col |= (a == np.array(c)).all(-1)
glass = np.zeros(a.shape[:2], bool)
for yy in range(600):
    for xx in range(400):
        glass[yy, xx] = inside(xx + 0.5, yy + 0.5, 0)
dark = col & glass & ((blur - 0.16) * 1.15 > thr)
a[dark] = 0
Image.fromarray(a).save(path)
