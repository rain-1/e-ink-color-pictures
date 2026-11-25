"""Evening — curtain up. The view from the stalls: gold proscenium, red house tabs,
the Great Hall set, and somebody in the doorway."""
import math, random
import numpy as np
from common import *
random.seed(74)
im, d = new(R)
rect(im, (0, 0, W, H), R, K, p_diamond(10))                              # damask wall

# ---- the sign over the arch ---------------------------------------------------------------
d.rounded_rectangle([40, 10, 360, 74], 8, fill=K, outline=Y, width=2)
for x in range(50, 356, 10):
    for y in (17, 67): d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=Y if (x // 10) % 4 else WH)
for y in range(27, 60, 10):
    for x in (48, 352): d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=Y)
spaced(d, 200, 22, "AGATHA CHRISTIE'S", font(9, "sans", True), WH, 3)
spaced(d, 200, 33, "THE MOUSETRAP", font(24, "serif", True), Y, 2)
spaced(d, 200, 59, "", font(8, "sans"), WH)

# ---- proscenium ---------------------------------------------------------------------------
PX0, PX1, PY0, PY1 = 26, 374, 84, 446
SX0, SX1, SY0, SY1 = 52, 348, 110, 432                                   # stage opening
rect(im, (PX0, PY0, PX1, PY1), Y, K, p_diamond(6))
d.rectangle([PX0, PY0, PX1, PY1], outline=K, width=2)
d.rectangle([PX0 + 5, PY0 + 5, PX1 - 5, PY1 - 1], outline=K)
d.rectangle([SX0 - 5, SY0 - 5, SX1 + 5, SY1 + 4], fill=Y, outline=K, width=2)
# egg-and-dart along the inner moulding
for x in range(SX0, SX1, 8): d.ellipse([x, SY0 - 4, x + 5, SY0 - 0], fill=WH, outline=K)
for y in range(SY0 + 4, SY1, 8):
    d.ellipse([SX0 - 5, y, SX0 - 1, y + 5], fill=WH, outline=K); d.ellipse([SX1 + 1, y, SX1 + 5, y + 5], fill=WH, outline=K)
# cartouche: comedy/tragedy reduced to a mouse in a wreath
d.ellipse([182, 78, 218, 108], fill=K, outline=Y, width=2)
for k in range(14):
    an = k * math.tau / 14; d.ellipse([200 + 15 * math.cos(an) - 2, 93 + 12 * math.sin(an) - 2, 200 + 15 * math.cos(an) + 2, 93 + 12 * math.sin(an) + 2], fill=G)
mouse(d, 199, 98, .7, WH, eye=K)
for sx in (-1, 1):                                                       # swags either side
    for k in range(4):
        cx = 200 + sx * (44 + k * 34)
        d.arc([cx - 17, 82, cx + 17, 104], 0, 180, fill=K, width=2); d.ellipse([cx - 19, 88, cx - 15, 92], fill=R, outline=K)

# ---- the set: the Great Hall ----------------------------------------------------------------
rect(im, (SX0, SY0, SX1, SY1), G, K, p_vlines(8, 1))                       # papered wall
rect(im, (SX0, SY0, SX1, SY0 + 26), K)                                    # border flies
rect(im, (SX0, 330, SX1, 372), K, G, p_planks(11))                        # wainscot
d.line([(SX0, 330), (SX1, 330)], fill=Y)
# raked floor boards in perspective
floor = mask_rect(SX0, 372, SX1, SY1)
paint(im, floor, Y, K, p_bayer(.18))
for k in range(-14, 15):
    for yy in range(372, SY1):
        xx = 200 + k * (12 + 18 * (yy - 372) / (SY1 - 372))
        if SX0 < xx < SX1: d.point((xx, yy), fill=K)
d.line([(SX0, 372), (SX1, 372)], fill=K, width=2)
# tall mullioned window, snow going past
wx0, wx1, wy0, wy1 = 164, 244, 150, 322
d.rectangle([wx0 - 6, wy0 - 6, wx1 + 6, wy1 + 6], fill=WH, outline=K, width=2)
d.rectangle([wx0, wy0, wx1, wy1], fill=B)
for _ in range(90):
    x, y = random.randrange(wx0 + 1, wx1), random.randrange(wy0 + 1, wy1)
    d.point((x, y), fill=WH); 
    if random.random() < .3: d.rectangle([x, y, x + 1, y + 1], fill=WH)
d.polygon([(wx0, wy1), (wx0, wy1 - 18), (wx0 + 30, wy1 - 8), (wx1 - 20, wy1 - 14), (wx1, wy1 - 24), (wx1, wy1)], fill=WH)
d.ellipse([222, 160, 238, 176], fill=WH)                                  # the moon, one day past full
for i in range(1, 4): d.line([(wx0 + i * 20, wy0), (wx0 + i * 20, wy1)], fill=K, width=2)
for j in range(1, 6): d.line([(wx0, wy0 + j * 29), (wx1, wy0 + j * 29)], fill=K)
d.rectangle([wx0 - 10, wy1 + 6, wx1 + 10, wy1 + 12], fill=WH, outline=K)   # window seat
rect(im, (wx0 - 6, wy1 + 12, wx1 + 6, 372), R, Y, p_check(4)); d.rectangle([wx0 - 6, wy1 + 12, wx1 + 6, 372], outline=K)
# fireplace, stage right
d.rectangle([100, 286, 150, 372], fill=WH, outline=K, width=2); d.rectangle([94, 278, 156, 288], fill=WH, outline=K, width=2)
d.rectangle([108, 304, 142, 372], fill=K)
for fx, fh, c in ((116, 30, R), (125, 44, R), (134, 32, R), (121, 20, Y), (130, 24, Y), (125, 12, WH)):
    d.polygon([(fx - 6, 370), (fx, 370 - fh), (fx + 6, 370)], fill=c)
d.rectangle([104, 266, 110, 278], fill=Y, outline=K); d.ellipse([118, 260, 134, 278], fill=WH, outline=K); d.line([(126, 269), (126, 263)], fill=K); d.line([(126, 269), (130, 271)], fill=K)
d.rectangle([140, 268, 146, 278], fill=R, outline=K)
d.rectangle([104, 196, 148, 246], fill=Y, outline=K, width=3); d.ellipse([116, 204, 136, 226], fill=K); d.polygon([(110, 243), (126, 222), (142, 243)], fill=K)   # ancestor
# the door, stage left, ajar — and who is that
d.rectangle([266, 214, 318, 372], fill=WH, outline=K, width=2)            # frame
d.rectangle([272, 220, 312, 372], fill=K)                                 # the dark beyond
d.polygon([(312, 220), (330, 228), (330, 380), (312, 372)], fill=R, outline=K)   # door leaf swung upstage
d.ellipse([314, 300, 318, 304], fill=Y)
fx, fy = 290, 372                                                        # figure in overcoat, hat, scarf
d.polygon([(fx - 12, fy), (fx - 13, fy - 78), (fx - 7, fy - 92), (fx + 7, fy - 92), (fx + 13, fy - 78), (fx + 12, fy)], fill=B)
d.ellipse([fx - 7, fy - 108, fx + 7, fy - 92], fill=B); d.rectangle([fx - 12, fy - 108, fx + 12, fy - 105], fill=B); d.rectangle([fx - 7, fy - 116, fx + 7, fy - 106], fill=B)
d.rectangle([fx - 7, fy - 95, fx + 7, fy - 90], fill=WH); d.line([(fx, fy - 88), (fx, fy)], fill=K)
# sofa, armchair, side table with the wireless, standard lamp
d.rounded_rectangle([196, 344, 262, 372], 6, fill=R, outline=K, width=2); d.rounded_rectangle([190, 356, 268, 396], 6, fill=R, outline=K, width=2)
rect(im, (198, 362, 260, 388), R, Y, p_dots(4)); d.line([(229, 358), (229, 394)], fill=K)
d.rectangle([194, 396, 198, 404], fill=K); d.rectangle([260, 396, 264, 404], fill=K)
d.rounded_rectangle([70, 352, 106, 400], 7, fill=B, outline=K, width=2); d.rounded_rectangle([64, 372, 112, 406], 5, fill=B, outline=K, width=2)
rect(im, (72, 378, 104, 400), B, WH, p_dots(4))
d.ellipse([80, 340, 96, 356], fill=WH, outline=K); d.pieslice([79, 338, 97, 352], 180, 360, fill=K)            # someone's head over the chair back
d.rectangle([150, 380, 180, 384], fill=K); d.line([(154, 384), (154, 410)], fill=K, width=2); d.line([(176, 384), (176, 410)], fill=K, width=2)
d.rounded_rectangle([154, 360, 176, 380], 3, fill=Y, outline=K, width=2); d.ellipse([158, 364, 168, 374], fill=K); d.line([(171, 365), (171, 375)], fill=K)
d.line([(340, 290), (340, 404)], fill=K, width=2); d.polygon([(330, 290), (350, 290), (345, 268), (335, 268)], fill=Y, outline=K); d.line([(332, 404), (348, 404)], fill=K, width=2)
a = np.array(im); m = mask_poly([(330, 291), (350, 291), (364, 330), (316, 330)]) & mask_rect(SX0, SY0, SX1, SY1) & p_bayer(.3); a[m] = Y; im.paste(Image.fromarray(a))
# rug
rect(im, (130, 408, 270, 426), R, Y, p_diamond(6)); d.rectangle([130, 408, 270, 426], outline=K)
for x in range(130, 271, 4): d.line([(x, 426), (x, 429)], fill=K)

# ---- the house tabs ---------------------------------------------------------------------------
def curtain(side):
    s = 1 if side == "L" else -1
    e = SX0 if side == "L" else SX1
    top_in = e + s * 112
    pts = [(e, SY0)] + [(top_in - s * 84 * (t ** 1.4), SY0 + 190 * t) for t in [i / 20 for i in range(21)]]
    pts += [(e + s * 30, SY0 + 200), (e + s * 40, SY1), (e, SY1)]
    m = mask_poly(pts)
    paint(im, m, R)
    a = np.array(im)
    # folds: black lines following the sweep, plus yellow sheen
    for k in range(13):
        f = k / 12
        fold = [(e + s * (112 * f) - s * 84 * f * (t ** 1.4), SY0 + 190 * t) for t in [i / 20 for i in range(21)]]
        ImageDraw.Draw(im).line(fold, fill=K if k % 3 else Y, width=1 if k % 2 else 2)
    dd = ImageDraw.Draw(im)
    for k in range(6):
        x = e + s * (4 + k * 6.5); dd.line([(x, SY0 + 204), (x + s * k * .8, SY1)], fill=K if k % 2 else Y)
    dd.line(pts[1:22], fill=K, width=2)
    # tie-back and tassel
    dd.line([(e, SY0 + 190), (e + s * 40, SY0 + 200)], fill=Y, width=5); dd.line([(e, SY0 + 187), (e + s * 40, SY0 + 197)], fill=K)
    dd.ellipse([e + s * 22 - 5, SY0 + 200, e + s * 22 + 5, SY0 + 210], fill=Y, outline=K)
    for t in range(-4, 5, 2): dd.line([(e + s * 22 + t, SY0 + 210), (e + s * 22 + t * 1.4, SY0 + 226)], fill=Y)
    # hem fringe
    for x in range(0, 40, 3): dd.line([(e + s * x, SY1 - 5), (e + s * x, SY1)], fill=Y)
from PIL import ImageDraw
curtain("L"); curtain("R")
d = ImageDraw.Draw(im); d.fontmode = "1"
# pelmet: scalloped swags with gold fringe
for i in range(6):
    cx = SX0 + 24.7 + i * 49.3
    m = mask_ellipse([cx - 26, SY0 - 22, cx + 26, SY0 + 30]) & mask_rect(SX0, SY0, SX1, SY0 + 40)
    paint(im, m, R)
    for r in (8, 15, 22): d.arc([cx - 26, SY0 - 22 + (22 - r), cx + 26, SY0 + 8 + r], 10, 170, fill=K)
    d.arc([cx - 26, SY0 - 22, cx + 26, SY0 + 30], 0, 180, fill=Y, width=3)
    for t in range(0, 181, 12):
        x = cx + 26 * math.cos(math.radians(t)); y = SY0 + 4 + 26 * math.sin(math.radians(t))
        d.line([(x, y), (x, y + 5)], fill=Y)
    d.ellipse([cx + 21, SY0 - 2, cx + 29, SY0 + 6], fill=Y, outline=K)

# ---- footlights, apron, pit rail ------------------------------------------------------------------
rect(im, (PX0, SY1 + 2, PX1, 462), K)
for x in range(SX0 + 8, SX1 - 4, 14):
    d.pieslice([x - 6, SY1 - 4, x + 6, SY1 + 10], 180, 360, fill=Y, outline=K); d.line([(x, SY1 - 8), (x, SY1 - 6)], fill=Y)
    d.point((x - 8, SY1 - 7), fill=Y); d.point((x + 8, SY1 - 7), fill=Y)
d.line([(PX0, 462), (PX1, 462)], fill=Y, width=2)
mouse(d, 322, 461, 1.0, WH, eye=K, flip=True)                               # late, and crossing the apron
# wall sconces
for sx in (12, 388):
    d.rectangle([sx - 2, 250, sx + 2, 270], fill=Y, outline=K); d.ellipse([sx - 7, 236, sx + 7, 252], fill=WH, outline=K)
    for an in range(200, 350, 25):
        d.line([(sx + 10 * math.cos(math.radians(an)), 244 + 10 * math.sin(math.radians(an))), (sx + 15 * math.cos(math.radians(an)), 244 + 15 * math.sin(math.radians(an)))], fill=Y)

# ---- the stalls -------------------------------------------------------------------------------------
rect(im, (0, 464, W, H), K, R, p_bayer(.2))
def head(x, y, s, kind):
    d.ellipse([x - 9 * s, y - 22 * s, x + 9 * s, y], fill=K)                                  # head
    d.polygon([(x - 22 * s, y + 30 * s), (x - 18 * s, y + 6 * s), (x - 6 * s, y - 2 * s), (x + 6 * s, y - 2 * s), (x + 18 * s, y + 6 * s), (x + 22 * s, y + 30 * s)], fill=K)
    if kind == 1:   # hat with a feather
        d.ellipse([x - 13 * s, y - 24 * s, x + 13 * s, y - 16 * s], fill=K); d.rectangle([x - 7 * s, y - 30 * s, x + 7 * s, y - 20 * s], fill=K)
        d.line([(x + 6 * s, y - 28 * s), (x + 14 * s, y - 40 * s)], fill=Y, width=2)
    elif kind == 2: # bun
        d.ellipse([x - 5 * s, y - 30 * s, x + 5 * s, y - 20 * s], fill=K)
    elif kind == 3: # bald, catching the light
        d.arc([x - 8 * s, y - 21 * s, x + 8 * s, y - 5 * s], 200, 300, fill=WH, width=2)
    elif kind == 4: # white collar
        d.line([(x - 6 * s, y), (x + 6 * s, y)], fill=WH, width=2)
    elif kind == 5: # pearls
        for t in range(-5, 6, 2): d.point((x + t * s, y + 2 * s + abs(t) * -.3), fill=WH)
    # rim light from the stage
    d.arc([x - 9 * s, y - 22 * s, x + 9 * s, y], 215, 325, fill=Y)
for row, (y, s, n, off) in enumerate([(486, .7, 12, 0), (512, .9, 10, 18), (544, 1.15, 8, -4), (584, 1.5, 6, 24)]):
    # seat backs
    for i in range(n + 1):
        x = off + (i + .5) * W / n
        d.rounded_rectangle([x - 20 * s, y + 4 * s, x + 20 * s, y + 44 * s], 6, fill=R, outline=K, width=2)
    for i in range(n + 1):
        x = off + (i + .5) * W / n + random.randrange(-3, 4)
        if random.random() < .12: continue                                                 # an empty seat
        head(x, y + random.randrange(-2, 3), s, random.choice([0, 0, 1, 2, 3, 4, 5]))
save(im)
