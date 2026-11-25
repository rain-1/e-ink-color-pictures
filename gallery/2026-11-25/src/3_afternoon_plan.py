"""Afternoon — the ground-floor plan as a blueprint, with the sergeant's pencil on it."""
import math, random
import numpy as np
from common import *
random.seed(3)
im, d = new(B)
T = 4                                    # wall thickness

# paper: faint mottling and two fold creases
a = np.array(im)
rng = np.random.default_rng(3)
a[(rng.random((H, W)) < .012)] = WH
im.paste(Image.fromarray(a))
for y in (200, 400): 
    for x in range(0, W, 3): d.point((x, y + (x // 37) % 2), fill=WH)
for x in range(0, H, 3): d.point((200 + (x // 41) % 2, x), fill=WH)

# border with grid references
d.rectangle([8, 8, W - 9, H - 9], outline=WH, width=2); d.rectangle([20, 20, W - 21, H - 21], outline=WH)
f8 = font(9, "sans", True)
for i, ch in enumerate("ABCDEF"):
    x = 20 + (i + .5) * 60; ctext(d, x, 9, ch, f8, WH); ctext(d, x, H - 20, ch, f8, WH)
    d.line([(20 + i * 60, 8), (20 + i * 60, 20)], fill=WH); d.line([(20 + i * 60, H - 21), (20 + i * 60, H - 9)], fill=WH)
for j in range(8):
    y = 20 + (j + .5) * 70; d.text((11, y - 5), str(j + 1), font=f8, fill=WH); d.text((W - 17, y - 5), str(j + 1), font=f8, fill=WH)
    d.line([(8, 20 + j * 70), (20, 20 + j * 70)], fill=WH); d.line([(W - 21, 20 + j * 70), (W - 9, 20 + j * 70)], fill=WH)

# ---- walls ----------------------------------------------------------------------------
def hw(x0, x1, y): d.rectangle([x0, y - T // 2, x1, y + T // 2], fill=WH)
def vw(x, y0, y1): d.rectangle([x - T // 2, y0, x + T // 2, y1], fill=WH)
X0, X1, Y0, Y1 = 44, 356, 70, 452
# outer shell drawn double with hatching between, like a proper cavity wall
d.rectangle([X0 - 5, Y0 - 5, X1 + 5, Y1 + 5], fill=WH)
rect(im, (X0 - 3, Y0 - 3, X1 + 4, Y1 + 4), B, WH, p_hatch(3, 1))
rect(im, (X0 + 3, Y0 + 3, X1 - 2, Y1 - 2), B)
d.rectangle([X0 + 2, Y0 + 2, X1 - 2, Y1 - 2], outline=WH)
hw(X0, X1, 196); hw(X0, 250, 380); hw(250, X1, 320)
vw(150, Y0, 196); vw(266, Y0, 196); vw(250, 196, Y1); vw(120, 380, Y1); vw(184, 380, Y1); vw(304, 320, Y1)
# porch
d.rectangle([126, Y1 + 5, 178, Y1 + 30], outline=WH, width=2)
for i in range(1, 4): d.line([(126, Y1 + 30 + i * 4), (178, Y1 + 30 + i * 4)], fill=WH)

def gap(x0, y0, x1, y1): d.rectangle([x0, y0, x1, y1], fill=B)
def door_h(x, y, w=22, up=True, left=True):
    """door in a horizontal wall at (x..x+w, y)"""
    gap(x, y - 4, x + w, y + 4)
    hx = x if left else x + w
    ey = y - w if up else y + w
    d.line([(hx, y), (hx, ey)], fill=WH, width=2)
    box = [hx - w, y - w, hx + w, y + w]
    if left: d.arc(box, 270 if up else 0, 360 if up else 90, fill=WH)
    else:    d.arc(box, 180 if up else 90, 270 if up else 180, fill=WH)
def door_v(x, y, w=22, right=True, top=True):
    gap(x - 4, y, x + 4, y + w)
    hy = y if top else y + w
    ex = x + w if right else x - w
    d.line([(x, hy), (ex, hy)], fill=WH, width=2)
    box = [x - w, hy - w, x + w, hy + w]
    if right: d.arc(box, 0 if top else 270, 90 if top else 360, fill=WH)
    else:     d.arc(box, 90 if top else 180, 180 if top else 270, fill=WH)
def win_h(x0, x1, y):
    gap(x0, y - 6, x1, y + 6)
    for o in (-4, 0, 4): d.line([(x0, y + o), (x1, y + o)], fill=WH)
    d.line([(x0, y - 5), (x0, y + 5)], fill=WH, width=2); d.line([(x1, y - 5), (x1, y + 5)], fill=WH, width=2)
def win_v(x, y0, y1):
    gap(x - 6, y0, x + 6, y1)
    for o in (-4, 0, 4): d.line([(x + o, y0), (x + o, y1)], fill=WH)
    d.line([(x - 5, y0), (x + 5, y0)], fill=WH, width=2); d.line([(x - 5, y1), (x + 5, y1)], fill=WH, width=2)

door_h(100, 196, up=False); door_h(196, 196, up=False, left=False); door_h(284, 196, up=False)
door_v(250, 232, right=False); door_h(60, 380, up=True); door_h(210, 380, up=True, left=False)
door_h(140, Y1, 24, up=True); door_h(140, 380, 24, up=True, left=False); door_v(304, 400, right=True); door_h(270, 320, up=False)
door_v(X1, 348, 20, right=False)                 # back door
win_h(70, 124, Y0); win_h(180, 236, Y0); win_h(288, 338, Y0)
win_v(X0, 100, 160); win_v(X0, 240, 330); win_v(X1, 100, 160); win_v(X1, 220, 290); win_h(60, 100, Y1); win_h(200, 236, Y1); win_h(316, 344, Y1)
win_v(X0, 400, 436)

# ---- fittings -----------------------------------------------------------------------------
def chair(x, y, s=9): d.rectangle([x, y, x + s, y + s], outline=WH); d.line([(x, y), (x + s, y)], fill=WH, width=2)
def armchair(x, y): d.rounded_rectangle([x, y, x + 18, y + 18], 4, outline=WH); d.rectangle([x + 4, y + 5, x + 14, y + 18], outline=WH)
def fireplace_h(x, y, w=40, down=True):
    s = 1 if down else -1
    d.rectangle([x, min(y, y + s * 8), x + w, max(y, y + s * 8)], fill=WH)
    d.rectangle([x + 6, min(y, y + s * 6), x + w - 6, max(y, y + s * 6)], fill=B)
    rect(im, (x + 2, min(y + s * 9, y + s * 16), x + w - 2, max(y + s * 9, y + s * 16)), B, WH, p_check(3))  # hearth
    d.rectangle([x + 2, min(y + s * 9, y + s * 16), x + w - 2, max(y + s * 9, y + s * 16)], outline=WH)

# Library (top left)
for i in range(0, 92, 6): d.line([(52 + i, Y0 + 6), (52 + i, Y0 + 15)], fill=WH)
d.rectangle([50, Y0 + 5, 66, Y0 + 16], outline=WH); d.rectangle([128, Y0 + 5, 144, Y0 + 16], outline=WH)   # shelves either side of window
for j in range(0, 80, 6): d.line([(134, 90 + j), (145, 90 + j)], fill=WH)
d.rectangle([133, 88, 146, 172], outline=WH)
d.rectangle([78, 118, 116, 144], outline=WH, width=2); chair(92, 148); d.ellipse([82, 122, 90, 130], outline=WH)       # desk + lamp
armchair(56, 160); d.rectangle([52, 96, 70, 110], outline=WH)
# Drawing room (top middle): piano, sofa, fireplace on the far wall
fireplace_h(188, Y0 + 3, 40, down=True)
pts = [(160, 150), (160, 108), (176, 104), (190, 112), (194, 128), (206, 136), (206, 150)]
d.polygon(pts, outline=WH); d.rectangle([160, 150, 206, 158], outline=WH)
for k in range(162, 206, 3): d.line([(k, 152), (k, 157)], fill=WH)
d.rectangle([172, 162, 192, 170], outline=WH)                                         # stool
d.rounded_rectangle([216, 124, 258, 144], 5, outline=WH); d.line([(216, 130), (258, 130)], fill=WH); armchair(232, 162)
d.ellipse([222, 102, 242, 118], outline=WH)
# Dining room (top right)
d.rounded_rectangle([288, 100, 336, 166], 8, outline=WH, width=2)
for y in (106, 126, 146): chair(276, y); 
for y in (106, 126, 146): d.rectangle([339, y, 348, y + 9], outline=WH)
chair(306, 88); d.rectangle([306, 169, 315, 178], outline=WH)
for cy in (112, 133, 154):
    for cx in (298, 326): d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], outline=WH)
d.rectangle([274, 180, 330, 190], outline=WH)                                          # sideboard
# Great Hall
fireplace_h(X0 + 3, 0, 0) if False else None
d.rectangle([X0 + 3, 342, X0 + 11, 376], fill=WH); d.rectangle([X0 + 3, 348, X0 + 9, 370], fill=B)   # hall fireplace, west wall... 
rect(im, (X0 + 12, 344, X0 + 20, 374), B, WH, p_check(3)); d.rectangle([X0 + 12, 344, X0 + 20, 374], outline=WH)
for k in range(0, 100, 8):                                                             # rug, dashed
    d.line([(86 + k, 246), (90 + k, 246)], fill=WH); d.line([(86 + k, 330), (90 + k, 330)], fill=WH)
for k in range(0, 84, 8):
    d.line([(84, 248 + k), (84, 252 + k)], fill=WH); d.line([(186, 248 + k), (186, 252 + k)], fill=WH)
d.rounded_rectangle([104, 262, 150, 282], 5, outline=WH); d.line([(104, 268), (150, 268)], fill=WH)          # sofa
armchair(70, 300); armchair(158, 300); d.ellipse([112, 296, 140, 320], outline=WH)                           # table
d.rectangle([56, 214, 76, 228], outline=WH); d.ellipse([60, 217, 70, 225], outline=WH)                        # wireless
# stairs along the north-east of the hall
for k in range(11):
    d.line([(200, 206 + k * 8), (244, 206 + k * 8)], fill=WH)
d.rectangle([200, 200, 244, 290], outline=WH); d.line([(222, 284), (222, 212)], fill=WH); d.polygon([(222, 206), (218, 214), (226, 214)], fill=WH)
d.text((228, 276), "UP", font=font(8, "sans", True), fill=WH) if False else None
# telephone table by the stairs
d.rectangle([222, 300, 242, 316], outline=WH); d.ellipse([228, 303, 238, 313], fill=WH)
# Kitchen
d.rectangle([330, 204, 352, 250], outline=WH, width=2)
for cy in (214, 228, 242):
    d.ellipse([335, cy - 5, 345, cy + 5], outline=WH)
d.rectangle([262, 204, 300, 220], outline=WH); d.rectangle([266, 207, 282, 217], outline=WH); d.line([(286, 206), (286, 218)], fill=WH); d.line([(290, 206), (290, 218)], fill=WH); d.line([(294, 206), (294, 218)], fill=WH)   # sink+drainer
d.rectangle([278, 250, 322, 288], outline=WH, width=2); chair(264, 262); chair(292, 292); d.rectangle([326, 262, 335, 271], outline=WH)
rect(im, (260, 300, 300, 316), B, WH, p_hlines(3, 1)); d.rectangle([260, 300, 300, 316], outline=WH)          # dresser
# Scullery / larder / study / cloaks
for j in range(0, 110, 7): d.line([(X1 - 14, 332 + j), (X1 - 4, 332 + j)], fill=WH) if not (345 < 332 + j < 372) else None
d.rectangle([258, 420, 296, 444], outline=WH); d.ellipse([264, 424, 280, 440], outline=WH)                     # copper
d.rectangle([56, 400, 100, 420], outline=WH, width=2); chair(72, 424)                                         # study desk
for k in range(0, 56, 5): d.line([(190 + k, 440), (192 + k, 446)], fill=WH)                                    # coat pegs
d.line([(190, 446), (246, 446)], fill=WH)
d.ellipse([230, 392, 242, 404], outline=WH); d.ellipse([234, 396, 238, 400], fill=WH)                          # umbrella stand

# ---- labels -----------------------------------------------------------------------------
fl = font(10, "sans", True); fs = font(8, "sans")
def label(cx, y, s, dims=None):
    w = d.textlength(s, font=fl); d.rectangle([cx - w / 2 - 2, y - 1, cx + w / 2 + 2, y + 11], fill=B)
    ctext(d, cx, y, s, fl, WH)
    if dims: 
        w2 = d.textlength(dims, font=fs); d.rectangle([cx - w2 / 2 - 1, y + 11, cx + w2 / 2 + 1, y + 20], fill=B); ctext(d, cx, y + 11, dims, fs, WH)
label(98, 174, "LIBRARY"); label(208, 176, "DRAWING RM", None); label(310, 76, "DINING"); 
label(134, 222, "GREAT HALL", "24'0\" × 21'6\""); label(302, 228, "KITCHEN"); label(84, 436, "STUDY") if False else None
label(152, 404, "LOBBY"); label(218, 416, "CLOAKS"); label(277, 398, "SCULL."); label(330, 426, "LARDER"); label(86, 388, "STUDY")
label(152, Y1 + 12, "PORCH")
# dimension line across the top
d.line([(X0, 52), (X1, 52)], fill=WH)
for x in (X0, 150, 266, X1):
    d.line([(x, 46), (x, 58)], fill=WH); d.line([(x - 3, 55), (x + 3, 49)], fill=WH)
for cx, s in ((97, "17'8\""), (208, "19'4\""), (311, "15'0\"")):
    w = d.textlength(s, font=fs); d.rectangle([cx - w / 2 - 2, 47, cx + w / 2 + 2, 57], fill=B); ctext(d, cx, 47, s, fs, WH)
d.line([(32, Y0), (32, Y1)], fill=WH)
for y in (Y0, 196, 380, Y1): d.line([(26, y), (38, y)], fill=WH); d.line([(29, y + 3), (35, y - 3)], fill=WH)

# ---- the sergeant's pencil: yellow notes, red marks ------------------------------------------
def dashed(pts, c, dash=5, gap_=4, w=2):
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        L = math.hypot(x1 - x0, y1 - y0); n = int(L // (dash + gap_)) + 1
        for i in range(n):
            t0 = i * (dash + gap_) / L; t1 = min(1, t0 + dash / L)
            if t0 >= 1: break
            d.line([(x0 + (x1 - x0) * t0, y0 + (y1 - y0) * t0), (x0 + (x1 - x0) * t1, y0 + (y1 - y0) * t1)], fill=c, width=w)
route = [(152, Y1 + 40), (152, 420), (152, 366), (176, 340), (190, 300), (208, 214), (208, 190)]
dashed(route, Y)
d.polygon([(208, 182), (203, 192), (213, 192)], fill=Y)
fi = font(11, "serif", italic=True, bold=True)
# X where it happened — drawing room, behind the sofa
cx, cy = 238, 134
d.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], outline=WH, width=4); d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], outline=R, width=3)
d.line([(cx - 7, cy - 7), (cx + 7, cy + 7)], fill=R, width=3); d.line([(cx - 7, cy + 7), (cx + 7, cy - 7)], fill=R, width=3)
d.text((246, 86), "here.", font=fi, fill=Y); d.line([(256, 100), (246, 118)], fill=Y)
# the cut telephone wire
d.ellipse([214, 292, 250, 324], outline=Y, width=2); d.text((194, 330), "wire cut", font=fi, fill=Y)
# who was where
notes = [((60, 100), "?"), ((300, 262), "Mrs R."), ((64, 404), "?") , ((330, 180), "?")]
d.text((58, 232), "wireless", font=fi, fill=Y) ; d.text((60, 244), "on LOUD", font=fi, fill=Y)
d.text((282, 266), "Mrs R.", font=fi, fill=Y); d.text((210, 232), "Maj.?", font=fi, fill=Y) if False else None
for (x, y) in ((100, 98), (318, 136), (76, 410), (330, 380), (222, 250)):
    d.text((x, y), "?", font=font(16, "serif", True), fill=Y)
# skis left outside
d.line([(184, Y1 + 8), (184, Y1 + 34)], fill=Y, width=2); d.line([(189, Y1 + 8), (189, Y1 + 34)], fill=Y, width=2)
d.text((196, Y1 + 20), "skis (mine)", font=fi, fill=Y)
# and the mouse, in the larder, surveyed like everything else
mouse(d, 326, 412, .8, WH, eye=B)
d.polygon([(338, 404), (348, 400), (348, 408)], fill=Y, outline=WH)
for k in range(9): d.point((312 - k * 4, 414 + (k % 2) * 2 - k), fill=WH)

# ---- title block ----------------------------------------------------------------------------
TY = 508
d.rectangle([28, TY, W - 29, H - 28], outline=WH, width=2)
d.line([(120, TY), (120, H - 28)], fill=WH); d.line([(290, TY), (290, H - 28)], fill=WH); d.line([(120, TY + 34), (W - 29, TY + 34)], fill=WH)
# compass
cx, cy, r = 74, TY + 33, 24
d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=WH)
for k in range(16):
    an = k * math.pi / 8; r0 = r - (5 if k % 4 == 0 else 2)
    d.line([(cx + r0 * math.sin(an), cy - r0 * math.cos(an)), (cx + r * math.sin(an), cy - r * math.cos(an))], fill=WH)
d.polygon([(cx, cy - r + 4), (cx - 5, cy), (cx, cy - 4)], fill=WH); d.polygon([(cx, cy - r + 4), (cx + 5, cy), (cx, cy - 4)], fill=Y)
d.polygon([(cx, cy + r - 6), (cx - 4, cy), (cx + 4, cy)], outline=WH)
ctext(d, cx, cy - r - 11, "N", font(9, "sans", True), WH) if False else None
spaced(d, 205, TY + 5, "MONKSWELL MANOR", font(13, "serif", True), WH, 2)
ctext(d, 205, TY + 20, "GROUND FLOOR PLAN", font(9, "sans", True), WH)
ctext(d, 205, TY + 38, "Scale: ⅛ inch to one foot", fs, WH) if False else ctext(d, 205, TY + 38, "Scale: 1/8 inch to one foot", fs, WH)
for i in range(8):
    x = 150 + i * 14; d.rectangle([x, TY + 51, x + 14, TY + 56], fill=WH if i % 2 == 0 else B, outline=WH)
for i, s in ((0, "0"), (4, "20"), (8, "40 ft")): d.text((148 + i * 14, TY + 57), s, font=font(7, "sans"), fill=WH) if False else None
ctext(d, 330, TY + 4, "DRG. No.", fs, WH); ctext(d, 330, TY + 15, "25 / 11 / 52", font(11, "sans", True), WH)
ctext(d, 330, TY + 38, "SHEET 1 of 3", fs, WH); ctext(d, 330, TY + 49, "Berks.", fs, WH)
# rubber stamp
d.rectangle([296, 474, 368, 496], fill=WH, outline=R, width=2); ctext(d, 332, 479, "EVIDENCE", font(11, "sans", True), R)
save(im)
