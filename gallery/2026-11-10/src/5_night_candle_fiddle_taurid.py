"""Night: Candle, Fiddle, Taurid. A still life built as a tone picture (albedo x candle
falloff, plus a little moonless window light) and then *engraved*: every tone is cut as
lines whose width follows the light and whose direction follows the object. Yellow ink
where the candle reaches, blue where only the window does, on black."""
import math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from kit import W, H, K, Wh, R, Y, B, bez, scurve, save
rnd = random.Random(1112); s = 2
alb = Image.new("L", (W * s, H * s), 0); ang = Image.new("L", (W * s, H * s), 32)
da, dg = ImageDraw.Draw(alb), ImageDraw.Draw(ang)
def P(pts): return [(x * s, y * s) for x, y in pts]
def shape(pts, a, g):                       # a = albedo 0..255, g = hatch angle in degrees (0..180)
    da.polygon(P(pts), fill=a); dg.polygon(P(pts), fill=int(g / 180 * 255))
def el(x, y, rx, ry, a, g):
    box = [(x - rx) * s, (y - ry) * s, (x + rx) * s, (y + ry) * s]; da.ellipse(box, fill=a); dg.ellipse(box, fill=int(g / 180 * 255))
def ln(pts, a, w=1.0): da.line(P(pts), fill=a, width=max(1, int(w * s)), joint="curve")

FL = (262, 232)                             # the flame
TABLE = 438
# wall: plaster, vertical-ish strokes; wainscot rail
shape([(0, 0), (400, 0), (400, TABLE), (0, TABLE)], 46, 80)
for x in range(0, 400, 50): ln([(x + 6, 330), (x + 6, TABLE)], 15, 1.2)
shape([(0, 322), (400, 322), (400, 330), (0, 330)], 95, 0)
# window, upper left: frame and the night in six panes
wx0, wy0, wx1, wy1 = 28, 36, 178, 288
shape([(wx0 - 9, wy0 - 9), (wx1 + 9, wy0 - 9), (wx1 + 9, wy1 + 12), (wx0 - 9, wy1 + 12)], 215, 0)
shape([(wx0, wy0), (wx1, wy0), (wx1, wy1), (wx0, wy1)], 0, 0)
shape([(wx0 - 14, wy1 + 8), (wx1 + 14, wy1 + 8), (wx1 + 18, wy1 + 17), (wx0 - 18, wy1 + 17)], 235, 0)
# a framed print on the wall: the line itself
fx0, fy0 = 300, 70
shape([(fx0, fy0), (fx0 + 68, fy0), (fx0 + 68, fy0 + 90), (fx0, fy0 + 90)], 200, 135)
shape([(fx0 + 7, fy0 + 7), (fx0 + 61, fy0 + 7), (fx0 + 61, fy0 + 83), (fx0 + 7, fy0 + 83)], 250, 45)
ln(scurve(fx0 + 34, fy0 + 16, 58, 11, 24), 0, 3.2)
ln([(fx0 + 34, fy0), (fx0 + 34, fy0 - 26)], 40, 0.6)
# table top (seen slightly from above) and its front edge, floor below
shape([(0, TABLE), (400, TABLE), (400, 500), (0, 500)], 105, 2)
shape([(0, 500), (400, 500), (400, 518), (0, 518)], 70, 90)
shape([(0, 518), (400, 518), (400, 600), (0, 600)], 30, 20)
for x in range(-40, 440, 46): ln([(x, 518), (x - 30, 600)], 20, 1.0)
# table cloth edge pattern
for x in range(4, 400, 12): shape([(x, 506), (x + 4, 510), (x, 514), (x - 4, 510)], 240, 0)
# books: a stack of three, spines to us
bx = 26
for j, (bw, bh, a) in enumerate(((150, 22, 190), (136, 18, 240), (120, 20, 170))):
    y1 = 470 - sum(h for _, h, _ in ((150, 22, 190), (136, 18, 240), (120, 20, 170))[:j]); y0 = y1 - bh; x0 = bx + j * 9
    shape([(x0, y0), (x0 + bw, y0), (x0 + bw, y1), (x0, y1)], a, 0 if j != 1 else 90)
    shape([(x0, y0), (x0 + 8, y0 - 7), (x0 + bw + 8, y0 - 7), (x0 + bw, y0)], min(255, a + 30), 15)
    shape([(x0 + bw, y0), (x0 + bw + 8, y0 - 7), (x0 + bw + 8, y1 - 7), (x0 + bw, y1)], 250, 90)      # page block
    for k in (0.12, 0.2, 0.8, 0.88): ln([(x0 + bw * k, y0 + 1), (x0 + bw * k, y1 - 1)], 30, 1.2)
    ln([(x0 + bw * 0.3, (y0 + y1) / 2), (x0 + bw * 0.7, (y0 + y1) / 2)], 30, 2.0)
# violin: built upright on its own layer, then laid against the books
vl = Image.new("L", (160 * s, 330 * s), 0); vg = Image.new("L", (160 * s, 330 * s), 0); vm = Image.new("L", (160 * s, 330 * s), 0)
dv, dvg, dvm = ImageDraw.Draw(vl), ImageDraw.Draw(vg), ImageDraw.Draw(vm)
def vshape(pts, a, g, d2=dv):
    q = [(x * s, y * s) for x, y in pts]; dv.polygon(q, fill=a); dvg.polygon(q, fill=int(g / 180 * 255)); dvm.polygon(q, fill=255)
def half(sign):
    return [(80 + sign * x, y) for x, y in bez((0, 150), (34, 150), (50, 172), (44, 198), 12) + bez((44, 198), (40, 212), (28, 214), (30, 228), 8) + bez((30, 228), (38, 240), (62, 250), (58, 286), 12) + bez((58, 286), (54, 318), (20, 322), (0, 322), 12)]
body = half(1) + half(-1)[::-1]
vshape(body, 235, 100)
vshape([(74, 20), (86, 20), (88, 152), (72, 152)], 150, 90)                       # neck + fingerboard
vshape([(74, 150), (86, 150), (90, 236), (70, 236)], 40, 90)
dv.ellipse([68 * s, 2 * s, 92 * s, 26 * s], fill=220); dvm.ellipse([68 * s, 2 * s, 92 * s, 26 * s], fill=255); dvg.ellipse([68 * s, 2 * s, 92 * s, 26 * s], fill=40)
sp = [(80 + (2 + 9 * i / 40) * math.cos(i / 40 * 4 * math.pi), 14 + (2 + 9 * i / 40) * math.sin(i / 40 * 4 * math.pi)) for i in range(41)]
dv.line([(x * s, y * s) for x, y in sp], fill=30, width=s)
for sy_ in (30, 40): 
    for sx_ in (-1, 1): dv.ellipse([(80 + sx_ * 12 - 3) * s, (sy_ - 3) * s, (80 + sx_ * 12 + 3) * s, (sy_ + 3) * s], fill=230); dvm.ellipse([(80 + sx_ * 12 - 3) * s, (sy_ - 3) * s, (80 + sx_ * 12 + 3) * s, (sy_ + 3) * s], fill=255)
for sx_ in (-1, 1):                                                               # f-holes: two more lines of beauty
    f = [(80 + sx_ * (26 + 5 * math.sin(2 * math.pi * i / 20)), 222 + i * 2.2) for i in range(21)]
    dv.line([(x * s, y * s) for x, y in f], fill=0, width=int(2.6 * s))
    for (px, py) in (f[0], f[-1]): dv.ellipse([(px - 2.6) * s, (py - 2.6) * s, (px + 2.6) * s, (py + 2.6) * s], fill=0)
dv.rectangle([64 * s, 246 * s, 96 * s, 250 * s], fill=255)                         # bridge
vshape([(72, 276), (88, 276), (86, 316), (74, 316)], 30, 90)                      # tailpiece
for k in range(4): dv.line([((77 + k * 2) * s, 22 * s), ((71 + k * 6) * s, 248 * s), ((75 + k * 3.4) * s, 278 * s)], fill=255, width=1)
dv.line([(x * s, y * s) for x, y in body + [body[0]]], fill=60, width=int(1.5 * s))
ROT = -52
vl, vg, vm = (im_.rotate(ROT, expand=True, resample=Image.BICUBIC) for im_ in (vl, vg, vm))
vg = vg.point(lambda v: int((v + (-ROT) / 180 * 255) % 255))
pos = (int(-14 * s), int(236 * s))
alb.paste(vl, pos, vm); ang.paste(vg, pos, vm)
# bow, lying on the table
ln([(150, 492), (392, 470)], 200, 1.6); ln([(152, 495), (388, 474)], 255, 0.6); shape([(380, 468), (392, 466), (393, 476), (382, 478)], 230, 0)
# candlestick and candle
cx = FL[0]
def turned(prof, a, g):
    shape([(cx - r, y) for r, y in prof] + [(cx + r, y) for r, y in prof][::-1], a, g)
turned([(4, 392), (9, 396), (9, 401), (4, 404), (3.5, 420), (8, 430), (9, 440), (5, 448), (4, 458), (10, 464), (26, 472), (30, 478), (30, 482)], 235, 90)
shape([(cx - 14, 386), (cx + 14, 386), (cx + 10, 393), (cx - 10, 393)], 245, 0)          # drip pan
shape([(cx - 6, 252), (cx + 6, 252), (cx + 6, 386), (cx - 6, 386)], 255, 90)             # candle
shape([(cx - 6, 262), (cx - 9, 290), (cx - 6, 300)], 255, 90)                             # a run of wax
el(cx + 2, 482, 44, 6, 40, 0)                                                              # its shadow pool
# wine glass
gx = 338
shape([(gx - 16, 380), (gx + 16, 380), (gx + 12, 412), (gx + 3, 424), (gx + 2, 462), (gx + 14, 470), (gx - 14, 470), (gx - 2, 462), (gx - 3, 424), (gx - 12, 412)], 170, 60)
shape([(gx - 14, 394), (gx + 14, 394), (gx + 11, 412), (gx + 3, 422), (gx - 3, 422), (gx - 11, 412)], 90, 0)
ln([(gx - 11, 384), (gx - 8, 410)], 255, 1.4)
# inkwell and quill
ix = 206
shape([(ix - 14, 452), (ix + 14, 452), (ix + 17, 478), (ix - 17, 478)], 150, 45); shape([(ix - 7, 444), (ix + 7, 444), (ix + 7, 452), (ix - 7, 452)], 200, 0)
q = bez((ix + 2, 448), (ix - 10, 400), (ix - 44, 380), (ix - 40, 330), 30)
for i in range(6, 31):
    t = i / 30; wd = 13 * math.sin(math.pi * min(1, (t - 0.15) / 0.85)) ** 0.7
    px, py = q[i]; ln([(px - wd, py - wd * 0.5), (px, py), (px + wd * 0.7, py - wd * 0.9)], 230, 1.0)
ln(q, 255, 1.4)
# a sheet of paper with a drawing half done, and the pug asleep on the floor
shape([(108, 476), (190, 470), (200, 496), (112, 500)], 255, 170)
ln([(150 + 9 * math.sin(i / 3), 474 + i * 1.1) for i in range(20)], 0, 1.6)
el(86, 566, 42, 20, 200, 30); el(128, 560, 17, 14, 215, 120); el(140, 566, 9, 7, 60, 0)
shape([(116, 550), (112, 540), (124, 547)], 50, 0); shape([(134, 546), (140, 538), (141, 550)], 50, 0)
ln([(46 + 9 * math.cos(i / 4), 552 + 7 * math.sin(i / 4)) for i in range(22)], 230, 2.4)
ln([(124, 560), (130, 561)], 30, 1.2)
for k in range(3): ln([(150 + k * 9, 546 - k * 8), (156 + k * 9, 546 - k * 8), (150 + k * 9, 552 - k * 8), (156 + k * 9, 552 - k * 8)], 180, 0.7)   # z z z

alb = alb.resize((W, H), Image.LANCZOS); ang = ang.resize((W, H), Image.NEAREST)
A = np.asarray(alb, np.float32) / 255; TH = np.asarray(ang, np.float32) / 255 * math.pi
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
dist = np.hypot(xx - FL[0], (yy - FL[1]) * 0.9)
candle = 1.0 / (1 + (dist / 92) ** 2.0)
candle *= np.where((yy > 518), 0.35, 1.0)                              # the table shades the floor
wcx, wcy = (wx0 + wx1) / 2, (wy0 + wy1) / 2
moon = 0.34 * np.exp(-(((xx - wcx) / 170) ** 2 + ((yy - wcy - 60) / 300) ** 2)) + 0.05 + 0.16 * (yy > 518) * np.exp(-((xx - 120) / 150) ** 2)
ty = np.clip(A * candle * 1.5, 0, 1); tb = np.clip(A * moon * 1.25, 0, 1)
tone = np.maximum(ty, tb); useY = ty >= tb
# the burin: one family of lines along the object's angle, a crossing family for the lights
per = 4.2
u = (xx * np.cos(TH) + yy * np.sin(TH)); v = (-xx * np.sin(TH) + yy * np.cos(TH))
wob = 0.6 * np.sin(u / 23.0 + v / 9.0)
l1 = 0.5 + 0.5 * np.cos(2 * math.pi * (v + wob) / per)
l2 = 0.5 + 0.5 * np.cos(2 * math.pi * (u * 0.82 + v * 0.57) / (per * 1.15))
ink = (l1 > 1 - tone * 1.25) | ((tone > 0.52) & (l2 > 1 - (tone - 0.52) * 2.2)) | (tone > 0.93)
ink &= tone > 0.07                                                       # let the dark be dark
gy_, gx_ = np.gradient(A); gt = np.gradient(TH)
contour = (np.hypot(gx_, gy_) > 0.06) | (np.hypot(gt[0], gt[1]) > 0.08)
ink &= ~contour                                                          # every form gets a cut black edge
out = np.zeros((H, W, 3), np.uint8)
out[ink & useY] = Y; out[ink & ~useY] = B
im = Image.fromarray(out); d = ImageDraw.Draw(im)

# ---------- things that are light itself, drawn straight in ink
# window panes: glazing bars, stars, the Pleiades, a slow Taurid, the two-day moon low down
for i in range(1, 2): d.line([( (wx0 + wx1) // 2, wy0), ((wx0 + wx1) // 2, wy1)], fill=B, width=5)
for j in range(1, 3): d.line([(wx0, wy0 + (wy1 - wy0) * j // 3), (wx1, wy0 + (wy1 - wy0) * j // 3)], fill=B, width=5)
def star(x, y, r=0):
    d.point((x, y), fill=Wh)
    if r >= 1: d.line([(x - r, y), (x + r, y)], fill=Wh); d.line([(x, y - r), (x, y + r)], fill=Wh)
for _ in range(70):
    x, y = rnd.randint(wx0 + 2, wx1 - 2), rnd.randint(wy0 + 2, wy1 - 2)
    if abs(x - (wx0 + wx1) // 2) > 4 and min(abs(y - wy0 - 84), abs(y - wy0 - 168)) > 4: star(x, y, rnd.choice([0, 0, 0, 1]))
for (px, py) in ((0, 0), (4, -2), (7, 1), (3, 3), (9, -3), (11, 2), (6, -5)): star(120 + px, 70 + py, 0)      # Pleiades
for (px, py, r) in ((0, 0, 2), (-13, -9, 1), (-22, -17, 1), (12, -12, 1), (22, -22, 1), (-6, 6, 0), (4, 9, 0)): star(118 + px, 118 + py, r)   # Taurus: Aldebaran and the V
d.point((118, 118), fill=R); d.point((117, 118), fill=R); d.point((119, 118), fill=R); d.point((118, 117), fill=R); d.point((118, 119), fill=R)
d.line([(56, 150), (100, 196)], fill=Wh, width=1); d.line([(84, 179), (100, 196)], fill=Y, width=2); d.line([(96, 192), (100, 196)], fill=Wh, width=3)   # the Taurid
# flame and its glow rings
for r, n in ((16, 20), (24, 28), (33, 36), (43, 44)):
    for i in range(n):
        a = 2 * math.pi * i / n + r
        d.line([(FL[0] + (r - 3) * math.cos(a), FL[1] + (r - 3) * math.sin(a)), (FL[0] + r * math.cos(a), FL[1] + r * math.sin(a))], fill=Y, width=1)
fl = bez((cx, 252), (cx - 9, 240), (cx + 3, 226), (cx - 1, 208), 14) + bez((cx - 1, 208), (cx + 9, 226), (cx + 8, 242), (cx, 252), 14)
d.polygon(fl, fill=Y); d.polygon([(cx + (x - cx) * 0.5, 252 + (y - 252) * 0.72) for x, y in fl], fill=Wh)
d.line([(cx, 252), (cx, 246)], fill=K, width=1)
# smoke: the line of beauty, three strands unwinding to the ceiling
for k in range(3):
    pts = []
    for i in range(90):
        t = i / 89
        pts.append((cx - 1 + (4 + 30 * t) * math.sin(t * 2 * math.pi * 1.4 + k * 0.35) * (0.4 + t) + k * 5 * t - 26 * t * t, 206 - 200 * t))
    for i in range(len(pts) - 1):
        if (i + k * 2) % 9 < 7 - k: d.line(pts[i:i + 2], fill=Wh, width=2 if (k == 0 and i < 60) else 1)
# glints: glass rim, candlestick, strings catch white
d.arc([gx - 16, 376, gx + 16, 384], 180, 360, fill=Wh); d.line([(gx - 11, 386), (gx - 9, 404)], fill=Wh)
d.line([(cx - 3, 400), (cx - 3, 418)], fill=Wh); d.line([(cx - 7, 262), (cx - 7, 380)], fill=Wh)
d.line([(fx0 + 34 + 11 * math.sin(2 * math.pi * i / 24), fy0 + 16 + 58 * i / 24) for i in range(25)], fill=R, width=3)
save(im)
