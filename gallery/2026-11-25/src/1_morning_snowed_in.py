"""Morning — Monkswell Manor, snowed in. Dawn, full palette, drawn 1:1 with pattern tints."""
import math, random
import numpy as np
from PIL import Image, ImageDraw
from common import *
random.seed(1952)
im, d = new(WH)

# --- sky: blue night draining into a yellow/red dawn ---------------------------------
a = np.array(im)
HOR = 318
for y in range(HOR):
    t = y / HOR
    row = BAYER[y % 8, np.arange(W) % 8]
    if t < 0.55:                       # blue thinning to white
        lv = 1.0 - (t / 0.55) ** 0.8
        a[y] = np.where((row < lv)[:, None], B, WH)
    elif t < 0.86:                     # white warming to yellow
        lv = (t - 0.55) / 0.31
        a[y] = np.where((row < lv)[:, None], Y, WH)
    else:                              # yellow burning to red at the horizon
        lv = (t - 0.86) / 0.14 * 0.75
        a[y] = np.where((row < lv)[:, None], R, Y)
im.paste(Image.fromarray(a)); 
# last stars, thin moon-set glow
for _ in range(38):
    x, y = random.randrange(W), random.randrange(0, 120)
    d.point((x, y), fill=WH)
    if random.random() < .3: d.line([(x-1, y), (x+1, y)], fill=WH); d.line([(x, y-1), (x, y+1)], fill=WH)
# long dawn clouds
for cy, cx, L in [(196, 120, 150), (214, 290, 120), (236, 80, 110), (250, 250, 170), (176, 330, 80)]:
    for i in range(4):
        o = i * 3
        d.line([(cx - L/2 + o*4, cy + o), (cx + L/2 - o*5, cy + o)], fill=R if i % 2 == 0 else WH)

# --- far hills ------------------------------------------------------------------------
def ridge(base, amp, f, ph):
    return [(x, base + amp * math.sin(x / f + ph) + amp * .4 * math.sin(x / (f * .37) + ph * 2)) for x in range(0, W + 1, 4)]
r1 = ridge(292, 14, 60, 1.0)
poly(im, r1 + [(W, 440), (0, 440)], WH, B, p_hatch(4, 1))
d.line(r1, fill=B)
# fir wood behind the house
for i in range(70):
    x = random.randrange(-5, W + 5); h = random.randrange(26, 52); by = 345 + random.randrange(-4, 6)
    c = K if random.random() < .65 else G
    for k in range(4):
        yy = by - h + k * h / 4; w = 3 + k * 3
        d.polygon([(x, yy - 3), (x - w, yy + h / 4 + 2), (x + w, yy + h / 4 + 2)], fill=c)
        d.line([(x, yy - 3), (x - w + 1, yy + h / 4)], fill=WH)          # snow on the weather side
    d.line([(x, by), (x, by + 6)], fill=K)

# --- the manor ------------------------------------------------------------------------
GY = 428
def brick(box): rect(im, box, R, K, p_brick(10, 5))
def window(x, y, w, h, lit, panes=(2, 3)):
    c = Y if lit else B
    d.rectangle([x - 2, y - 2, x + w + 2, y + h + 2], fill=WH)
    d.rectangle([x, y, x + w, y + h], fill=c, outline=K)
    for i in range(1, panes[0]): d.line([(x + w * i / panes[0], y), (x + w * i / panes[0], y + h)], fill=K)
    for j in range(1, panes[1]): d.line([(x, y + h * j / panes[1]), (x + w, y + h * j / panes[1])], fill=K)
    if lit:  # curtain
        d.polygon([(x + 1, y + 1), (x + w * .35, y + 1), (x + 1, y + h * .8)], fill=R)
        d.polygon([(x + w - 1, y + 1), (x + w * .65, y + 1), (x + w - 1, y + h * .8)], fill=R)
    else:    # frost in the corners
        for k in range(5): d.point((x + 1 + k, y + h - 1 - (k % 2)), fill=WH)
    d.rectangle([x - 3, y + h + 2, x + w + 3, y + h + 4], fill=WH, outline=None)   # snowy sill
    d.line([(x - 3, y + h + 5), (x + w + 3, y + h + 5)], fill=K)

# chimneys first (behind roofs)
for cx, top in [(128, 214), (200, 222), (274, 214)]:
    brick((cx - 9, top, cx + 9, 300)); d.rectangle([cx - 9, top, cx + 9, 300], outline=K)
    d.rectangle([cx - 11, top - 4, cx + 11, top], fill=K)
    for px in (-5, 3): d.rectangle([cx + px, top - 11, cx + px + 3, top - 5], fill=R, outline=K)
    d.rectangle([cx - 11, top - 7, cx + 11, top - 5], fill=WH)
    # smoke: a lazy drifting column
    sx, sy = cx, top - 13
    for k in range(46):
        rr = 2 + k * .22
        ox = sx + 10 * math.sin(k / 6.0 + cx) + k * .9
        oy = sy - k * 2.6
        if oy < 4: break
        box = [ox - rr, oy - rr, ox + rr, oy + rr]
        d.arc(box, 200 + k * 20, 520 + k * 20, fill=K if k % 3 else WH)

# central block
brick((150, 300, 250, GY)); 
roofc = [(140, 304), (160, 262), (240, 262), (260, 304)]
poly(im, roofc, WH, B, p_hatch(6, 1, -1)); d.line(roofc + [roofc[0]], fill=K)
d.line([(140, 305), (260, 305)], fill=K, width=2)
# wings with half-timbered gables
for x0 in (58, 248):
    x1 = x0 + 94; ax = (x0 + x1) / 2
    brick((x0, 318, x1, GY)); d.rectangle([x0, 318, x1, GY], outline=K)
    gable = [(x0, 318), (ax, 246), (x1, 318)]
    poly(im, gable, WH)
    for k in range(-4, 5):                                # timber studs
        xx = ax + k * 10; top = 246 + abs(k * 10) * (72 / 47)
        d.line([(xx, top + 2), (xx, 318)], fill=K, width=2)
    d.line([(x0 + 14, 300), (x1 - 14, 300)], fill=K, width=2)
    d.line([(ax - 30, 318), (ax, 272), (ax + 30, 318)], fill=K, width=2)
    # snow-loaded barge boards
    d.line([(x0 - 8, 324), (ax, 240), (x1 + 8, 324)], fill=K, width=5)
    d.line([(x0 - 9, 320), (ax, 236), (x1 + 9, 320)], fill=WH, width=5)
    d.line([(x0 - 9, 316), (ax, 232), (x1 + 9, 316)], fill=B, width=1)
    for k in range(9):                                    # icicles
        ix = x0 - 4 + k * 3 if k < 4 else x1 + 4 - (k - 4) * 3
    window(ax - 9, 276, 18, 20, lit=(x0 == 58), panes=(2, 2))
    window(x0 + 12, 336, 24, 34, lit=(x0 != 58)); window(x1 - 36, 336, 24, 34, lit=False)
    window(x0 + 12, 386, 24, 30, lit=True); window(x1 - 36, 386, 24, 30, lit=(x0 == 58))
d.rectangle([150, 300, 250, GY], outline=K)
for wx in (160, 190, 220): window(wx, 316, 20, 30, lit=(wx == 190))
window(158, 376, 20, 36, lit=True); window(222, 376, 20, 36, lit=False)
# icicles under every eave
for x in list(range(142, 259, 5)) + list(range(52, 150, 6)) + list(range(252, 348, 6)):
    if 150 <= x <= 250: y0 = 306
    else:
        x0 = 58 if x < 200 else 248; ax = x0 + 47; y0 = 322 if abs(x - ax) > 44 else None
    if y0: d.line([(x, y0), (x, y0 + random.randrange(3, 9))], fill=WH)
# porch + door
poly(im, [(180, 372), (200, 350), (220, 372)], WH); d.line([(178, 374), (200, 350), (222, 374)], fill=K, width=2)
d.line([(177, 371), (200, 346), (223, 371)], fill=WH, width=3)
d.rectangle([188, 378, 212, GY], fill=G, outline=K); d.line([(200, 378), (200, GY)], fill=K)
d.ellipse([203, 402, 206, 405], fill=Y); d.rectangle([184, 374, 187, GY], fill=K); d.rectangle([213, 374, 216, GY], fill=K)
d.ellipse([196, 358, 204, 366], fill=Y, outline=K)                      # porch lamp
# ivy up the right wing
for k in range(260):
    t = random.random(); x = 336 - t * 26 * random.random(); y = GY - t * 100 + random.randrange(-3, 4)
    d.point((x, y), fill=G); d.point((x + 1, y), fill=G if random.random() < .7 else K); d.point((x, y + 1), fill=G)

# --- snow field -----------------------------------------------------------------------
snow_top = [(x, GY + 3 * math.sin(x / 31) + 2 * math.sin(x / 9 + 1)) for x in range(0, W + 1, 4)]
poly(im, snow_top + [(W, H), (0, H)], WH)
d.line(snow_top, fill=B)
# drift shadows: long blue-hatched lozenges
for (cx, cy, rx, ry) in [(90, 470, 120, 9), (310, 492, 130, 11), (150, 528, 170, 12), (330, 560, 110, 10), (60, 578, 90, 9), (250, 452, 80, 5)]:
    m = mask_ellipse([cx - rx, cy - ry, cx + rx, cy + ry]) & (YY > cy - 1)
    paint(im, m, WH, B, p_hlines(3, 1))
    d.arc([cx - rx, cy - ry, cx + rx, cy + ry], 180, 360, fill=B)
# yellow light spilling from the windows onto the snow
for lx in (82, 168, 200, 298):
    m = mask_poly([(lx - 10, GY + 4), (lx + 14, GY + 4), (lx + 30, GY + 30), (lx - 22, GY + 30)])
    paint(im, m, WH, Y, p_bayer(.45))
# buried fence along the drive
for i in range(13):
    x = 14 + i * 31; y = 474 + 10 * math.sin(i / 2.0) + i * 1.5; hgt = 16 + (i % 3) * 3
    d.rectangle([x, y - hgt, x + 3, y], fill=K); d.rectangle([x - 1, y - hgt - 3, x + 4, y - hgt], fill=WH, outline=B)
    if i < 12:
        x2 = 14 + (i + 1) * 31; y2 = 474 + 10 * math.sin((i + 1) / 2.0) + (i + 1) * 1.5
        d.line([(x + 3, y - hgt + 6), (x2, y2 - 16 - ((i + 1) % 3) * 3 + 6)], fill=K)
# ski tracks: the sergeant came across the fields
def track(off):
    return [(250 + off + 120 * math.sin((y - 430) / 95.0) * ((y - 430) / 170.0), y) for y in range(600, 434, -3)]
for off in (0, 7):
    pts = track(off); d.line(pts, fill=B, width=2)
for i, y in enumerate(range(596, 440, -14)):
    x = 250 + 120 * math.sin((y - 430) / 95.0) * ((y - 430) / 170.0)
    sx = x - 9 if i % 2 else x + 16
    d.ellipse([sx - 2, y - 2, sx + 2, y + 2], outline=B); d.point((sx, y), fill=K)
# the skis themselves, leaning by the door
d.line([(226, GY), (230, 380)], fill=K, width=2); d.line([(231, GY), (234, 382)], fill=K, width=2)
d.line([(230, 380), (232, 376)], fill=K); d.line([(234, 382), (236, 378)], fill=K)

# --- signpost ---------------------------------------------------------------------------
d.rectangle([318, 470, 322, 548], fill=K)
d.rectangle([272, 476, 372, 512], fill=WH, outline=K, width=2)
d.rectangle([270, 471, 374, 475], fill=WH, outline=B)
spaced(d, 322, 479, "MONKSWELL", font(11, "serif", True), K, 1)
spaced(d, 322, 492, "MANOR", font(11, "serif", True), R, 3)
d.line([(280, 507), (364, 507)], fill=K)
d.rectangle([284, 514, 360, 528], fill=G, outline=K); ctext(d, 322, 515, "GUEST HOUSE", font(9, "sans", True), WH)
d.polygon([(310, 548), (330, 548), (336, 556), (304, 556)], fill=WH, outline=B)

# --- the old tree in front ------------------------------------------------------------
def branch(x, y, ang, L, w, depth):
    x2 = x + L * math.cos(ang); y2 = y - L * math.sin(ang)
    d.line([(x, y), (x2, y2)], fill=K, width=max(1, int(w)))
    if w >= 2 and abs(math.cos(ang)) > .35:                    # snow lying on the upper side
        d.line([(x, y - w / 2 - 1), (x2, y2 - w / 2 - 1)], fill=WH, width=2)
    if depth == 0 or L < 5: return
    n = 2 if depth > 1 else 3
    for i in range(n):
        branch(x2, y2, ang + random.uniform(-.75, .75), L * random.uniform(.62, .8), w * .66, depth - 1)
poly(im, [(28, 590), (38, 500), (50, 500), (62, 590)], K)
branch(44, 505, math.pi / 2 + .08, 70, 11, 7)
branch(44, 470, math.pi / 2 + .9, 46, 6, 5)
branch(46, 440, math.pi / 2 - .8, 52, 6, 6)
ell(im, (14, 580, 80, 600), WH); d.arc([14, 580, 80, 606], 180, 360, fill=B)
# a robin, because someone has to be warm
d.ellipse([96, 372, 104, 379], fill=K); d.ellipse([99, 374, 104, 379], fill=R); d.line([(96, 376), (92, 378)], fill=K)

# --- the mouse, and where it has been ----------------------------------------------------
mx, my = 150, 572
for k in range(22):
    px = 60 + k * 4.2; py = 590 - k * .9 + 3 * math.sin(k / 2.5)
    d.point((px, py), fill=K); d.point((px + 1, py + 2), fill=K)
mouse(d, mx, my, 1.0, K, eye=WH)

# --- falling snow -------------------------------------------------------------------------
a = np.array(im)
for _ in range(520):
    x, y = random.randrange(W), random.randrange(H - 60)
    big = random.random() < .28
    if tuple(a[y, x]) == WH and not big: continue
    d.point((x, y), fill=WH)
    if big:
        d.point((x + 1, y), fill=WH); d.point((x, y + 1), fill=WH); d.point((x + 1, y + 1), fill=WH)
save(im)
