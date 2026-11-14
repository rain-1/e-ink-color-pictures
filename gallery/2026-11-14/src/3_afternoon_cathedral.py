"""Afternoon — Rouen, plein soleil. The west front built procedurally (portals, gables,
rose, galleries, pinnacles) and then lit the way Monet lit it: gold stone, blue shadow,
no black anywhere. Shadows are hand-ruled hatching, not flat fill."""
import math
import numpy as np
from PIL import Image, ImageDraw
from common import *

rng = np.random.default_rng(1894)
S = 2
SW, SH = W * S, H * S
yy, xx = np.mgrid[0:SH, 0:SW].astype(np.float32)

# Three layers, each a greyscale drawing at 2x:
#   depth  : 0 = front plane of stone, 1 = deepest recess  -> blue hatching density
#   line   : drawn contours                                   -> solid blue
#   skym   : sky
depth = Image.new("L", (SW, SH), 0); dd = ImageDraw.Draw(depth)
line = Image.new("L", (SW, SH), 0); dl = ImageDraw.Draw(line)
hot = Image.new("L", (SW, SH), 0); dh = ImageDraw.Draw(hot)      # red-orange accents
skym = Image.new("L", (SW, SH), 0); ds = ImageDraw.Draw(skym)

def s(pts): return [(x * S, y * S) for x, y in pts]
def LN(pts, w=1.0, v=255): dl.line(s(pts), fill=v, width=max(1, int(round(w * S))))
def DP(pts, v): dd.polygon(s(pts), fill=v)

def arch_pts(cx, base, half, rise, n=28, k=0.55):
    """Pointed two-centred arch: each side is a circular arc struck from beyond the centre."""
    r = half * (1 + k); apex = math.sqrt(r * r - (half * k) ** 2)
    left = []
    for i in range(n // 2 + 1):
        x = cx - half + half * i / (n // 2)
        yr = math.sqrt(max(0, r * r - (x - (cx + half * k)) ** 2))
        left.append((x, base - rise * yr / apex))
    return left + [(2 * cx - x, y) for x, y in reversed(left[:-1])]

def portal(cx, base, half, spring, rise, orders=5, door=True):
    # nested archivolts stepping inward and deeper
    for k in range(orders):
        f = 1 - k * 0.13
        pts = [(cx - half * f, base)] + [(x, y) for x, y in arch_pts(cx, spring, half * f, rise * f)] + [(cx + half * f, base)]
        DP(pts, int(60 + 150 * (k + 1) / orders))
        LN(pts, 0.8 if k else 1.4)
        # voussoir figures: ticks around each order
        ap = arch_pts(cx, spring, half * (f - 0.065), rise * (f - 0.065), 16 + 4 * (orders - k))
        for (x, y) in ap[1:-1]:
            dl.ellipse([x * S - 1.6, y * S - 2.6, x * S + 1.6, y * S + 2.6], fill=200)
    f = 1 - orders * 0.13
    # tympanum band and the door
    ty = spring - rise * f * 0.15
    LN([(cx - half * f, spring), (cx + half * f, spring)], 1)
    for i in range(7):
        x = cx - half * f + (i + 0.5) * 2 * half * f / 7
        dl.ellipse([x * S - 3, (spring - 9) * S - 6, x * S + 3, (spring - 9) * S + 6], fill=255)
    if door:
        LN([(cx, base), (cx, spring)], 1.5)
        for dx in (-1, 1):
            x0 = cx + dx * half * f * 0.5
            dh.rectangle([(x0 - half * f * 0.36) * S, (spring + 6) * S, (x0 + half * f * 0.36) * S, base * S], fill=255)
            for j in range(5):
                yj = spring + 10 + j * (base - spring - 10) / 5
                LN([(x0 - half * f * 0.36, yj), (x0 + half * f * 0.36, yj)], 0.5)
    # jamb statues down both sides
    for k in range(orders):
        f2 = 1 - (k + 0.5) * 0.13
        for dx in (-1, 1):
            x = cx + dx * half * f2
            for j in range(3):
                y0 = spring + 8 + j * (base - spring - 10) / 3
                dl.ellipse([x * S - 3, y0 * S, x * S + 3, (y0 + 4) * S], fill=255)
                dl.line([x * S, (y0 + 4) * S, x * S, (y0 + 20) * S], fill=255, width=3)

def gable(cx, base, half, top, crockets=9):
    pts = [(cx - half, base), (cx, top), (cx + half, base)]
    LN(pts, 1.4); LN([(cx - half + 7, base), (cx, top + 12), (cx + half - 7, base)], 0.7)
    for i in range(1, crockets):
        t = i / crockets
        for dx in (-1, 1):
            x = cx + dx * half * (1 - t); y = base + (top - base) * t
            LN([(x, y), (x + dx * 4, y - 5), (x + dx * 1, y - 7)], 0.8)
    # finial
    LN([(cx, top), (cx, top - 16)], 1.2); LN([(cx - 5, top - 9), (cx + 5, top - 9)], 1)
    dl.ellipse([cx * S - 4, (top - 19) * S - 4, cx * S + 4, (top - 19) * S + 4], fill=255)
    # pierced trefoil inside the gable
    r = half * 0.26; cy = base - (base - top) * 0.36
    dd.ellipse([(cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S], fill=235)
    dl.ellipse([(cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S], outline=255, width=2)
    for k in range(3):
        a = -math.pi / 2 + k * 2 * math.pi / 3
        px, py = cx + r * .45 * math.cos(a), cy + r * .45 * math.sin(a)
        dl.ellipse([(px - r * .42) * S, (py - r * .42) * S, (px + r * .42) * S, (py + r * .42) * S], outline=255, width=2)

def pinnacle(cx, base, top, w):
    dd.rectangle([(cx - w) * S, top * S, (cx + w * 1.9) * S, base * S], fill=0)
    LN([(cx - w, base), (cx - w, top + 26)], 1.0); LN([(cx + w, base), (cx + w, top + 26)], 1.0)
    DP([(cx + w, base), (cx + w, top + 26), (cx + w * 1.9, top + 30), (cx + w * 1.9, base)], 120)   # shaded flank
    LN([(cx - w - 2, top + 26), (cx, top), (cx + w + 2, top + 26)], 1.0)
    for i in range(1, 6):
        t = i / 6
        for dx in (-1, 1):
            LN([(cx + dx * (w + 2) * (1 - t), top + 26 * (1 - t)), (cx + dx * ((w + 2) * (1 - t) + 3), top + 26 * (1 - t) - 3)], 0.6)
    y = top + 34
    while y < base - 8:                     # blind niches up the shaft
        h = min(30, base - y - 4)
        ap = [(cx - w + 2, y + h)] + arch_pts(cx, y + 8, w - 2, 8, 10) + [(cx + w - 2, y + h)]
        DP(ap, 150); LN(ap, 0.5)
        dl.line([cx * S, (y + 10) * S, cx * S, (y + h - 2) * S], fill=255, width=2)
        y += h + 6
        LN([(cx - w - 1, y - 3), (cx + w + 1, y - 3)], 0.8)

def arcade(x0, x1, y0, y1, n, depthv=175, statues=True, glazed=False):
    LN([(x0, y0), (x1, y0)], 1.2); LN([(x0, y1), (x1, y1)], 1.2)
    bw = (x1 - x0) / n
    for i in range(n):
        cx = x0 + (i + 0.5) * bw
        ap = [(cx - bw * .4, y1)] + arch_pts(cx, y0 + (y1 - y0) * .42, bw * .4, (y1 - y0) * .36, 12) + [(cx + bw * .4, y1)]
        DP(ap, depthv); LN(ap, 0.6)
        if glazed:
            LN([(cx, y0 + (y1 - y0) * .2), (cx, y1)], 0.5)
        if statues:
            dl.ellipse([cx * S - 3, (y0 + (y1 - y0) * .38) * S, cx * S + 3, (y0 + (y1 - y0) * .38) * S + 7], fill=255)
            dl.polygon(s([(cx - 2.6, y1 - 1), (cx - 1.2, y0 + (y1 - y0) * .5), (cx + 1.2, y0 + (y1 - y0) * .5), (cx + 2.6, y1 - 1)]), fill=255)
        # little gablet over each bay
        LN([(cx - bw * .45, y0 + (y1 - y0) * .16), (cx, y0 - (y1 - y0) * .18), (cx + bw * .45, y0 + (y1 - y0) * .16)], 0.5)

def rose(cx, cy, r):
    dd.ellipse([(cx - r - 5) * S, (cy - r - 5) * S, (cx + r + 5) * S, (cy + r + 5) * S], fill=110)
    dd.ellipse([(cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S], fill=250)
    for rr, w in ((r + 5, 3), (r, 3), (r * .56, 2), (r * .2, 2)):
        dl.ellipse([(cx - rr) * S, (cy - rr) * S, (cx + rr) * S, (cy + rr) * S], outline=255, width=w)
    n = 16
    for k in range(n):
        a = k * 2 * math.pi / n
        LN([(cx + r * .2 * math.cos(a), cy + r * .2 * math.sin(a)), (cx + r * .56 * math.cos(a), cy + r * .56 * math.sin(a))], 0.8)
        a2 = a + math.pi / n
        # outer petals: two arcs meeting in a point (flamboyant mouchettes)
        p0 = (cx + r * .56 * math.cos(a), cy + r * .56 * math.sin(a))
        p1 = (cx + r * .56 * math.cos(a + 2 * math.pi / n), cy + r * .56 * math.sin(a + 2 * math.pi / n))
        tip = (cx + r * .97 * math.cos(a2), cy + r * .97 * math.sin(a2))
        mid0 = (cx + r * .82 * math.cos(a + .07), cy + r * .82 * math.sin(a + .07))
        mid1 = (cx + r * .82 * math.cos(a + 2 * math.pi / n - .07), cy + r * .82 * math.sin(a + 2 * math.pi / n - .07))
        LN([p0, mid0, tip, mid1, p1], 0.7)
        pc = (cx + r * .76 * math.cos(a2), cy + r * .76 * math.sin(a2))
        dh.ellipse([pc[0] * S - 5, pc[1] * S - 5, pc[0] * S + 5, pc[1] * S + 5], fill=255)
        pc = (cx + r * .4 * math.cos(a2), cy + r * .4 * math.sin(a2))
        dl.ellipse([pc[0] * S - 3, pc[1] * S - 3, pc[0] * S + 3, pc[1] * S + 3], outline=255, width=2)
    dh.ellipse([(cx - r * .14) * S, (cy - r * .14) * S, (cx + r * .14) * S, (cy + r * .14) * S], fill=255)

# ------------------------------------------------------------------ assemble the front
# sky: everything above the silhouette (drawn as polygons of "not building")
ds.rectangle([0, 0, SW, SH], fill=255)
sil = [(0, 600), (0, 40), (30, 40), (30, 0), (112, 0), (112, 96), (128, 96), (128, 150), (150, 150),
       (200, 58), (250, 150), (272, 150), (272, 84), (288, 84), (288, 0), (400, 0), (400, 600)]
ds.polygon(s(sil), fill=0)

# towers: left (Saint-Romain) plain and tall, right (Tour de Beurre) lacier; both cropped
for (x0, x1, y0) in ((0, 112, 0), (288, 400, 0)):
    for yb in range(18, 300, 62):
        arcade(x0 + 8, x1 - 8, yb, yb + 50, 4, depthv=215, statues=False, glazed=True)
        LN([(x0, yb - 8), (x1, yb - 8)], 1.4)
        DP([(x0, yb - 8), (x1, yb - 8), (x1, yb - 3), (x0, yb - 3)], 130)
# central screen wall
DP([(112, 150), (288, 150), (288, 430), (112, 430)], 0)
# the rose and its square frame
DP([(140, 168), (260, 168), (260, 300), (140, 300)], 60)
rose(200, 232, 54)
LN([(140, 168), (260, 168), (260, 300), (140, 300), (140, 168)], 1)
# the high gable over the rose, pierced
gable(200, 164, 62, 44, crockets=12)
arcade(150, 250, 132, 160, 7, depthv=200, statues=True)
# galleries of kings
arcade(112, 288, 304, 340, 13, depthv=190)
arcade(0, 112, 318, 350, 7, depthv=190)
arcade(288, 400, 318, 350, 7, depthv=190)
# portals
portal(200, 590, 72, 468, 96, orders=6)
portal(52, 590, 46, 492, 62, orders=4)
portal(348, 590, 46, 492, 62, orders=4)
gable(200, 404, 82, 286, crockets=13)
gable(52, 440, 52, 366, crockets=8)
gable(348, 440, 52, 366, crockets=8)
# buttress pinnacles: four big ones framing the bays, drawn last so they stand in front
for cx, top, w in ((112, 96, 11), (288, 84, 11), (4, 250, 9), (396, 250, 9)):
    pinnacle(cx, 600, top, w)
for cx, top in ((128, 300), (272, 300), (150, 130), (250, 130)):
    pinnacle(cx, 440 if top > 200 else 300, top, 5)
# steps and plinth
for i, yb in enumerate((590, 594, 598)):
    LN([(0, yb), (400, yb)], 0.8)

# ------------------------------------------------------------------ light it
# Everything from here is composed at the panel's own 400x600 so that no hatch line is
# ever averaged with the stone behind it (blue + yellow would quantise to green).
from PIL import ImageFilter
def down(im): return np.asarray(im.resize((W, H), Image.BOX), np.float32) / 255
D, Lm, Hm, SK = down(depth), down(line), down(hot), down(skym)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
ink = np.asarray(Image.fromarray((np.maximum(Lm, D * 0.5) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.3)), np.float32) / 255
cast = np.roll(np.roll(ink, 4, axis=0), 3, axis=1)        # sun high on the left
grain = fbm(26, 4, 4)
# the foot of the front falls into the shade of the houses opposite, as in the series
fall = np.clip((yy - 400) / 240 + (xx - 200) / 900, 0, 1)
shade = np.clip(0.62 * D + 0.45 * cast + 0.27 * fall + 0.22 * (grain - 0.5), 0, 1)

out = np.zeros((H, W, 3), np.uint8)
out[:] = Y
out[(shade < 0.16) & (BAYER < 0.85 - shade * 3 + 0.3 * grain)] = WH   # sunstruck faces: bare paper
p1 = (xx + yy) % 4; p2 = (xx - yy) % 4
out[(shade > 0.26) & (p1 < 1)] = B
out[(shade > 0.26) & ((xx + yy) % 8 < 1) & (shade < 0.36)] = Y        # lightest tone: every other rule
out[(shade > 0.26) & ((xx + yy) % 8 < 1) & (shade < 0.36) & (D < .05)] = Y
out[(shade > 0.50) & (p2 < 1)] = B
out[(shade > 0.72) & (yy % 2 < 1)] = B
out[(shade > 0.90)] = B
# orange heat held in the doors and in the glass of the rose
hm = Hm > 0.5
out[hm & (p1 < 2)] = R
out[hm & (p1 >= 2)] = Y
out[hm & (fall > 0.45) & (p2 < 1)] = B
out[Lm > 0.22] = B                                                    # contours
# sky: ruled blue, heavier to the right, with the sun's glare top-left
sky = SK > 0.5
out[sky] = WH
tone = 0.20 + 0.35 * xx / W + 0.3 * (grain - 0.5)
out[sky & (yy % 4 < 1)] = B
out[sky & (yy % 4 == 2) & (BAYER < tone * 1.4 - 0.2)] = B
gl = np.hypot(xx - 150, yy - 22)
out[sky & (gl < 26) & (BAYER < 1.2 - gl / 22)] = WH
out[sky & (gl < 13)] = Y
out[sky & (gl < 9)] = WH
img = Image.fromarray(out)
d = ImageDraw.Draw(img)
for bx, by, sc in ((168, 62, 1.0), (236, 40, 0.8), (228, 100, 0.7), (262, 62, 1.1), (140, 112, .7)):
    d.line([(bx - 5 * sc, by - 2 * sc), (bx, by), (bx + 5 * sc, by - 3 * sc)], fill=B, width=2)
save(img)
