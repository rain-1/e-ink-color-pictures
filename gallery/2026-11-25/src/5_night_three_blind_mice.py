"""Night — Three Blind Mice. The manor under the day-old Beaver Moon; the telephone wires
are a stave, the tune sits on them, and one wire has been cut."""
import math, random
import numpy as np
from common import *
random.seed(2250)
im, d = new(K)

# ---- sky: black, with a blue glow pooled round the moon -----------------------------------
MX, MY, MR = 286, 96, 34
a = np.array(im)
dist = np.hypot(XX - MX, YY - MY)
lv = np.clip(1.15 - dist / 210.0, 0, 1) ** 2.2 * .8
a[(BAYER[YY % 8, XX % 8] < lv) & (YY < 420)] = B
im.paste(Image.fromarray(a))
# stars: Orion rising in the east (left), Taurus above with Aldebaran, the Pleiades
def star(x, y, mag, c=WH):
    if mag >= 3:
        d.line([(x - 3, y), (x + 3, y)], fill=c); d.line([(x, y - 3), (x, y + 3)], fill=c); d.rectangle([x - 1, y - 1, x + 1, y + 1], fill=c)
    elif mag == 2:
        d.line([(x - 1, y), (x + 1, y)], fill=c); d.line([(x, y - 1), (x, y + 1)], fill=c)
    else: d.point((x, y), fill=c)
for _ in range(210):
    x, y = random.randrange(W), random.randrange(0, 330)
    if math.hypot(x - MX, y - MY) < MR + 8: continue
    star(x, y, 1 if random.random() < .86 else 2, WH if random.random() < .9 else Y)
ori = {"bet": (62, 150), "bel": (118, 138), "rig": (120, 258), "sai": (70, 268), "a1": (84, 206), "a2": (93, 201), "a3": (102, 196), "mei": (88, 120)}
for a_, b_ in (("bet", "bel"), ("bet", "a1"), ("bel", "a3"), ("a1", "sai"), ("a3", "rig"), ("a1", "a2"), ("a2", "a3"), ("bet", "mei"), ("bel", "mei"), ("sai", "rig")):
    (x0, y0), (x1, y1) = ori[a_], ori[b_]
    n = int(math.hypot(x1 - x0, y1 - y0) // 5)
    for i in range(2, n - 1): 
        if i % 2: d.point((x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n), fill=B)
star(*ori["bet"], 3, R); star(*ori["rig"], 3, WH); star(*ori["bel"], 2); star(*ori["sai"], 2); star(*ori["mei"], 2)
for k in ("a1", "a2", "a3"): star(*ori[k], 2)
for k in range(3): d.point((98 + k, 222 + k * 5), fill=WH)                                # the sword
star(196, 62, 3, Y)                                                                   # Aldebaran
for x, y in ((182, 50), (172, 44), (186, 70), (176, 62), (206, 40)): star(x, y, 1 if x != 206 else 2)
for x, y in ((148, 22), (152, 18), (156, 23), (151, 26), (158, 17), (145, 17)): d.point((x, y), fill=WH)   # Pleiades
fl = font(9, "sans")
d.text((8, 132), "Betelgeuse", font=fl, fill=WH); d.text((206, 66), "Aldebaran", font=fl, fill=WH)

# ---- the moon, waning gibbous, 99% ------------------------------------------------------------
for r, c in ((MR + 9, B),):
    for an in range(0, 360, 6):
        d.point((MX + r * math.cos(math.radians(an)), MY + r * math.sin(math.radians(an))), fill=WH)
d.ellipse([MX - MR, MY - MR, MX + MR, MY + MR], fill=WH)
a = np.array(im)
moon = mask_ellipse([MX - MR, MY - MR, MX + MR, MY + MR])
# the faintest shaved edge on the right-hand limb
shade = moon & (((XX - MX + 5) / (MR - 1.0)) ** 2 + ((YY - MY) / (MR + 1.0)) ** 2 > 1.0) & (XX > MX)
a[shade & p_check(1)] = K
for (cx, cy, rx, ry, lvl) in ((-12, -10, 12, 9, .5), (4, -16, 9, 6, .45), (-6, 8, 10, 8, .4), (12, 4, 7, 9, .35), (-18, 4, 5, 6, .4), (6, 20, 6, 4, .3)):
    m = mask_ellipse([MX + cx - rx, MY + cy - ry, MX + cx + rx, MY + cy + ry]) & moon
    a[m & p_bayer(lvl)] = B
im.paste(Image.fromarray(a))
for (cx, cy, r) in ((16, -20, 3), (-22, -18, 2), (20, 16, 2), (-4, 24, 3)):
    d.arc([MX + cx - r, MY + cy - r, MX + cx + r, MY + cy + r], 0, 360, fill=B)
d.line([(MX - 4, MY + 24), (MX - 16, MY + 6)], fill=WH)                                  # Tycho's ray

# ---- hills and the manor ------------------------------------------------------------------------
def ridge(base, amp, f, ph): return [(x, base + amp * math.sin(x / f + ph) + amp * .35 * math.sin(x / (f * .31) + ph * 3)) for x in range(0, W + 1, 2)]
r_far = ridge(352, 14, 70, 2.0)
poly(im, r_far + [(W, H), (0, H)], K, B, p_bayer(.5)); d.line(r_far, fill=WH)
for i in range(46):                                                                    # firs on the far ridge
    x = random.randrange(0, W); y = 352 + 14 * math.sin(x / 70 + 2.0) + 14 * .35 * math.sin(x / 21.7 + 6.0); h = random.randrange(10, 22)
    if 228 < x < 372: continue
    d.polygon([(x, y - h), (x - 4, y + 1), (x + 4, y + 1)], fill=K, outline=B); d.line([(x, y - h), (x - 4, y + 1)], fill=WH)
# house silhouette, moonlit roofs
hx, hy = 300, 372
body = [(236, hy), (236, 330), (258, 302), (280, 330), (280, 322), (320, 322), (320, 330), (342, 302), (364, 330), (364, hy)]
poly(im, body, K)
for ax in (258, 342):
    d.line([(ax - 25, 333), (ax, 301), (ax + 25, 333)], fill=WH, width=3)
    d.line([(ax, 304), (ax + 24, 334)], fill=B)
poly(im, [(278, 322), (284, 310), (316, 310), (322, 322)], WH, B, p_hatch(4, 1, -1))
for cx in (270, 300, 330):
    d.rectangle([cx - 4, 292 if cx != 300 else 298, cx + 4, 312], fill=K); d.rectangle([cx - 5, (292 if cx != 300 else 298) - 2, cx + 5, (292 if cx != 300 else 298)], fill=WH)
for (wx, wy, lit) in ((246, 340, 0), (262, 340, 0), (290, 334, 0), (304, 334, 0), (334, 340, 0), (350, 340, 0), (246, 356, 0), (262, 356, 0), (334, 356, 0), (350, 356, 1), (256, 316, 0), (340, 316, 0)):
    d.rectangle([wx - 4, wy - 5, wx + 4, wy + 5], fill=Y if lit else K, outline=B if not lit else K)
    d.line([(wx, wy - 5), (wx, wy + 5)], fill=K if lit else B)
d.rectangle([296, 356, 304, hy], fill=K, outline=B)
# the one lit window throws a long yellow lozenge on the snow
a = np.array(im); m = mask_poly([(346, 374), (356, 374), (372, 410), (318, 410)]) & p_bayer(.5); a[m] = Y; im.paste(Image.fromarray(a))
# chimney smoke, only from one stack now
for k in range(26):
    ox = 330 + 7 * math.sin(k / 4.0) - k * 1.6; oy = 286 - k * 3.2
    d.arc([ox - 3 - k * .2, oy - 3, ox + 3 + k * .2, oy + 3], 180 + k * 25, 400 + k * 25, fill=WH if k % 2 else B)

# near snowfield: white where the moon lands, blue-black in the hollows
r_near = ridge(396, 10, 95, .4)
a = np.array(im)
near = mask_poly(r_near + [(W, H), (0, H)])
t = np.clip((YY - 390) / 210.0, 0, 1)
glow = np.clip(1 - np.abs(XX - 250) / 260.0, 0, 1)
lvl = .06 + .42 * glow * (1 - t * .6) + .06 * np.sin(YY / 9.0 + XX / 60.0)
a[near] = B
a[near & (BAYER[YY % 8, XX % 8] < lvl)] = WH
a[near & (BAYER[(YY + 3) % 8, (XX + 5) % 8] < .18 + t * .5 - .3 * glow)] = K
im.paste(Image.fromarray(a)); d.line(r_near, fill=WH, width=2)
# wind-carved sastrugi
for _ in range(34):
    x, y = random.randrange(-20, W), random.randrange(410, 590); L = random.randrange(20, 70)
    d.line([(x, y), (x + L, y - 2)], fill=WH if random.random() < .5 else B)
# buried lane: fence posts marching to the house
for i in range(9):
    t_ = i / 8; x = 60 + t_ * 190 + 30 * math.sin(t_ * 3); y = 586 - t_ * 200; h = 30 - t_ * 22
    d.rectangle([x, y - h, x + max(1, 4 - t_ * 3), y], fill=K); d.rectangle([x - 1, y - h - 2, x + max(2, 5 - t_ * 3), y - h], fill=WH)
    d.line([(x + 4, y), (x + 4 + h * 1.6, y + h * .35)], fill=K)                         # moon shadow

# ---- telegraph poles and the stave ---------------------------------------------------------------
P1, P2 = (38, 600), (398, 300)
def pole(x, base, top, arm):
    d.rectangle([x - 3, top, x + 3, base], fill=K); d.line([(x - 4, top), (x - 4, base)], fill=WH)
    for j in range(2):
        yy = top + 10 + j * 22
        d.rectangle([x - arm, yy, x + arm, yy + 3], fill=K); d.line([(x - arm, yy - 1), (x + arm, yy - 1)], fill=WH)
        for sx in (-arm + 2, -arm // 2, arm // 2, arm - 2): d.rectangle([x + sx - 1, yy - 5, x + sx + 1, yy - 1], fill=WH)
    d.rectangle([x - 5, top - 3, x + 5, top], fill=WH)
LX, RX = 44, 372
ltop, rtop = 176, 232
# five wires = five lines of the stave, sagging between poles
def wire(i, x):
    t_ = (x - LX) / (RX - LX)
    y0 = ltop + 8 + i * 11; y1 = rtop + 6 + i * 6
    return y0 + (y1 - y0) * t_ + 26 * math.sin(math.pi * t_) * (1 - .25 * t_)
for i in range(5):
    if i == 4:      # the cut wire: runs a little way from each pole, then hangs
        d.line([(x, wire(i, x)) for x in range(LX, 150, 4)], fill=WH)
        d.line([(146, wire(i, 146)), (150, wire(i, 146) + 24), (147, wire(i, 146) + 52), (152, wire(i, 146) + 70)], fill=WH)
        d.line([(x, wire(i, x)) for x in range(318, RX + 1, 4)], fill=WH)
        d.line([(318, wire(i, 318)), (315, wire(i, 318) + 20), (318, wire(i, 318) + 38)], fill=WH)
        for s_ in range(3): d.line([(152, wire(i, 146) + 70), (152 + (s_ - 1) * 4, wire(i, 146) + 76)], fill=Y)   # frayed copper
    else:
        d.line([(x, wire(i, x)) for x in range(LX, RX + 1, 4)], fill=WH)
pole(LX, 560, ltop - 6, 22); pole(RX, 404, rtop - 4, 13)
# treble clef, hand-drawn on the wires
cx = 78; cy = wire(2, cx)
clef = [(cx + 2, cy + 22), (cx - 2, cy + 26), (cx - 6, cy + 22), (cx - 2, cy + 18), (cx + 3, cy + 22), (cx + 1, cy - 26), (cx + 6, cy - 34), (cx + 8, cy - 26), (cx - 6, cy - 8), (cx - 9, cy + 2), (cx - 4, cy + 10), (cx + 5, cy + 10), (cx + 9, cy + 3), (cx + 5, cy - 4), (cx - 1, cy - 3), (cx - 3, cy + 3), (cx + 1, cy + 6)]
d.line(clef, fill=Y, width=2)
# "Three blind mice, three blind mice": E D C — E D C  (in C: 1st line E, below-line D, ledger C)
def ypos(step, x):
    """step 0 = bottom line (E4), +1 per staff step upward."""
    lo = wire(3, x) if True else 0     # bottom *intact* line is wire 3; treat wire 3 as E
    gap_ = (wire(3, x) - wire(2, x))
    return wire(3, x) - step * gap_ / 2
notes = [(112, 0, 1), (138, -1, 1), (166, -2, 2), (214, 0, 1), (240, -1, 1), (268, -2, 2)]
for (x, step, dur) in notes:
    y = ypos(step, x)
    if step == -2: d.line([(x - 9, y), (x + 9, y)], fill=WH)                                   # ledger line
    # each note is a mouse: round body as the note-head, tail as the stem
    d.ellipse([x - 6, y - 4, x + 6, y + 4], fill=WH if dur == 1 else K, outline=WH)
    d.ellipse([x - 8, y - 7, x - 3, y - 2], fill=WH); d.ellipse([x - 2, y - 8, x + 3, y - 3], fill=WH)   # ears
    d.point((x - 5, y), fill=K if dur == 1 else WH)
    stem = [(x + 6, y - 1), (x + 7, y - 14), (x + 6, y - 26), (x + 9, y - 32)]
    d.line(stem, fill=WH)
d.line([(192, wire(0, 192)), (192, wire(3, 192))], fill=WH)                                  # bar line
d.line([(296, wire(0, 296)), (296, wire(3, 296))], fill=WH); d.line([(299, wire(0, 299)), (299, wire(3, 299))], fill=WH, width=2)

# ---- three real ones, crossing the moonlit snow in a line --------------------------------------
for i, (x, y, s) in enumerate(((208, 520, 1.5), (164, 532, 1.3), (124, 540, 1.1))):
    d.ellipse([x - 9 * s, y - 1, x + 14 * s, y + 3], fill=K)                                  # shadow
    mouse(d, x, y, s, WH, eye=K)
    for k in range(6): d.point((x - 22 * s - k * 6, y + 1 + (k % 2) * 2), fill=WH)
# title, small, bottom right
d.rectangle([222, 560, 378, 594], fill=K, outline=B)
spaced(d, 300, 566, "THREE BLIND MICE", font(11, "serif", True), WH, 2)
ctext(d, 300, 580, "see how they run", font(10, "serif", italic=True), Y)

# ---- snow still coming down --------------------------------------------------------------------
for _ in range(150):
    x, y = random.randrange(W), random.randrange(120, 560)
    d.point((x, y), fill=WH)
    if random.random() < .2: d.rectangle([x, y, x + 1, y + 1], fill=WH)
save(im)
