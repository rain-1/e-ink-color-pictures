"""Afternoon: a three-masted barque under full sail, drawn as a woodcut --
black line on white with blue sea, a yellow sun and red flags. The detail is
in the rigging: yards, shrouds with ratlines, stays, jibs, a spanker, gun
ports, foam at the bow, and pennants streaming from every masthead."""
import math
import os
import random

from PIL import Image, ImageDraw

S = 4
W, H = 400 * S, 600 * S
K = (0, 0, 0); Wt = (255, 255, 255); R = (0xE0, 0x1B, 0x24)
Y = (0xF5, 0xD4, 0x00); B = (0x12, 0x3D, 0xB0)
random.seed(3)

img = Image.new("RGB", (W, H), Wt)
d = ImageDraw.Draw(img)

def P(x, y): return (x * S, y * S)
def ln(pts, w=1.5, c=K): d.line([P(*p) for p in pts], fill=c, width=int(w * S), joint="curve")
def quad(p0, p1, p2, n=24):
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0],
             (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]) for t in (i / n for i in range(n + 1))]

HORIZON = 430
DECK = 398

# ------------------------------------------------------------------ sky
# sun with fine rays
sx, sy, sr = 62, 76, 26
for k in range(36):
    a = k * math.pi / 18
    L = 10 if k % 3 == 0 else 5
    ln([(sx + (sr + 4) * math.cos(a), sy + (sr + 4) * math.sin(a)),
        (sx + (sr + 4 + L) * math.cos(a), sy + (sr + 4 + L) * math.sin(a))], 1.2)
d.ellipse([*P(sx - sr, sy - sr), *P(sx + sr, sy + sr)], fill=Y, outline=K, width=int(1.8 * S))

def cloud(cx, cy, scale):
    blobs = [(-22, 4, 16), (-6, -6, 20), (14, 0, 17), (28, 6, 12), (-30, 8, 10), (4, 8, 14)]
    els = [(cx + bx * scale, cy + by * scale, r * scale) for bx, by, r in blobs]
    for x, y, r in els:
        d.ellipse([*P(x - r, y - r), *P(x + r, y + r)], fill=Wt, outline=K, width=int(1.6 * S))
    for x, y, r in els:
        r2 = r - 1.7
        d.ellipse([*P(x - r2, y - r2), *P(x + r2, y + r2)], fill=Wt)
    # flat base and shade hatch
    base = cy + 12 * scale
    ln([(cx - 34 * scale, base), (cx + 38 * scale, base)], 1.6)
    for i in range(3):
        yy = base - (3 + i * 3.2) * scale
        ln([(cx - (30 - i * 6) * scale, yy), (cx + (34 - i * 5) * scale, yy)], 0.9)
cloud(300, 70, 1.15)
cloud(120, 150, 0.8)
cloud(360, 190, 0.6)
# birds
for bx, by, s in [(150, 90, 5), (168, 100, 4), (330, 130, 4)]:
    ln(quad((bx - s, by), (bx - s / 2, by - s), (bx, by)) + quad((bx, by), (bx + s / 2, by - s), (bx + s, by)), 1.3)

# distant coast and a lighthouse on the horizon
d.polygon([P(335, HORIZON), P(345, 424), P(370, 421), P(392, 425), P(400, 423), P(400, HORIZON)], fill=K)
d.rectangle([*P(383, 406), *P(388, 424)], fill=Wt, outline=K, width=int(0.8 * S))
for yy in (409, 415, 421):
    d.rectangle([*P(383.4, yy), *P(387.6, yy + 2.5)], fill=R)
d.rectangle([*P(382, 403), *P(389, 406)], fill=K)

# ------------------------------------------------------------------ sea
d.rectangle([*P(0, HORIZON), *P(400, 600)], fill=B)
for row, yy in enumerate(range(HORIZON + 8, 600, 11)):
    n = 4 + row // 3
    for _ in range(n):
        x = random.uniform(-10, 400); L = random.uniform(10, 26 + row)
        crest = quad((x, yy), (x + L / 2, yy - 3 - row * 0.15), (x + L, yy))
        ln(crest, 1.1 + row * 0.06, Wt)
        ln([(x + L * 0.1, yy + 3), (x + L * 1.1, yy + 3)], 0.9, K)
        if row % 2 == 0:
            ln([(x - 8, yy + 6), (x + L * 0.5, yy + 6)], 0.7, K)

# ------------------------------------------------------------------ hull
bow, stern = 336, 68
sheer = quad((stern, 392), (200, 404), (bow, 388))
hull = [P(*p) for p in sheer] + [P(bow + 6, 412), P(bow + 2, 438), P(stern - 6, 438), P(stern - 2, 405)]
d.polygon(hull, fill=K)
# gun-port strake and boot-topping
band = [(x, y + 12) for x, y in sheer]
d.line([P(*p) for p in band], fill=Wt, width=int(5 * S), joint="curve")
for i, (x, y) in enumerate(band[2::2]):
    if i % 1 == 0:
        d.rectangle([*P(x - 2, y - 2), *P(x + 2, y + 2)], fill=K)
d.line([P(stern - 5, 433), P(bow + 3, 433)], fill=R, width=int(4 * S))
# stern gallery windows and rudder
for i in range(3):
    d.rectangle([*P(stern + 4 + i * 6, 399), *P(stern + 8 + i * 6, 403)], fill=Y)
d.rectangle([*P(stern - 10, 420), *P(stern - 5, 438)], fill=K)
# rail and a few figures for scale
ln([(x, y - 3) for x, y in sheer], 0.8, Wt)
for fx in (110, 128, 214, 292):
    fy = 388 + (fx - stern) / (bow - stern) * 0
    d.rectangle([*P(fx - 1.3, fy - 6), *P(fx + 1.3, fy)], fill=K)
    d.ellipse([*P(fx - 1.6, fy - 9.2), *P(fx + 1.6, fy - 6)], fill=K)
# bowsprit
ln([(bow - 6, 390), (396, 362)], 3)
ln([(bow + 2, 400), (372, 372)], 1.0)   # bobstay
# bow wave and wake
for i in range(6):
    x = bow + 4 + i * 5
    ln(quad((x, 436), (x + 6, 428 - i), (x + 14, 436)), 1.8, Wt)
for x in range(20, stern, 12):
    ln([(x, 437), (x + 7, 437)], 1.6, Wt)

# ------------------------------------------------------------------ masts & sails
masts = [  # x at deck, top y, rake per unit height, sails from the top: (width, height) ...
    dict(x=272, top=112, sails=[(46, 30), (64, 40), (86, 54), (112, 72)]),   # fore
    dict(x=200, top=82,  sails=[(52, 34), (72, 46), (96, 62), (124, 80)]),   # main
    dict(x=128, top=150, sails=[(44, 30), (60, 40), (80, 52)]),              # mizzen (spanker below)
]

def mast_x(m, y):
    return m["x"] + (DECK - y) * 0.035

def sail(x0, x1, yt, yb):
    mid = (yt + yb) / 2
    right = quad((x1, yt), (x1 + 7, mid), (x1 + 2, yb))
    bottom = quad((x1 + 2, yb), ((x0 + x1) / 2, yb + 9), (x0 - 2, yb))
    left = quad((x0 - 2, yb), (x0 - 7, mid), (x0, yt))
    outline = [(x0, yt), (x1, yt)] + right + bottom + left
    d.polygon([P(*p) for p in outline], fill=Wt)
    ln(outline + [(x0, yt)], 1.6)
    # billow shading: curves following the foot, tightening downward
    for k, w in ((6, 0.8), (13, 0.9), (22, 1.0), (33, 1.0)):
        if k > (yb - yt) - 6:
            break
        shrink = k * 0.25
        curve = quad((x1 + 1 - shrink, yb - k), ((x0 + x1) / 2, yb - k + 8 - k * 0.12), (x0 - 1 + shrink, yb - k))
        ln(curve, w)
    ln([(x0 - 2, yt + 1), (x0 + 3, yb - 4)], 0.8)  # leech shadow at the aft edge

# spanker on the mizzen, drawn first (it sits behind the shrouds)
mz = masts[2]
gaff_peak = (mz["x"] - 62, 268)
boom_end = (mz["x"] - 74, 392)
spanker = [(mast_x(mz, 300), 300), gaff_peak, boom_end, (mz["x"], 392)]
d.polygon([P(*p) for p in spanker], fill=Wt)
ln(spanker + [spanker[0]], 1.6)
for k in range(1, 5):
    t = k / 5
    a = (spanker[0][0] + (gaff_peak[0] - spanker[0][0]) * t, spanker[0][1] + (gaff_peak[1] - spanker[0][1]) * t)
    b = (spanker[3][0] + (boom_end[0] - spanker[3][0]) * t, spanker[3][1] + (boom_end[1] - spanker[3][1]) * t)
    ln(quad(a, ((a[0] + b[0]) / 2 - 4, (a[1] + b[1]) / 2), b), 0.8)
ln([(mast_x(mz, 300), 300), gaff_peak], 2.2)  # gaff
ln([(mz["x"], 392), boom_end], 2.2)          # boom
# ensign at the gaff peak
ex, ey = gaff_peak
d.polygon([P(ex, ey), P(ex - 22, ey - 4), P(ex - 15, ey + 4), P(ex - 22, ey + 12), P(ex, ey + 14)], fill=R, outline=K)

for m in masts:
    top, xd = m["top"], m["x"]
    # mast itself (behind sails), doubled in thickness toward the deck
    ln([(mast_x(m, top - 8), top - 8), (xd, DECK + 2)], 3.0)
    y = top + 4
    for i, (wdt, hgt) in enumerate(m["sails"]):
        cx = mast_x(m, y)
        yard_w = wdt / 2 + 6
        ln([(cx - yard_w, y), (cx + yard_w, y)], 2.4)                      # yard
        sail(cx - wdt / 2, cx + wdt / 2, y + 1, y + hgt)
        for sgn in (-1, 1):                                                # lifts
            ln([(mast_x(m, y - 14), y - 14), (cx + sgn * yard_w, y)], 0.8)
        y += hgt + 7
    m["lower"] = y - 7  # foot of the lowest sail
    # masthead pennant
    tx, ty = mast_x(m, top - 8), top - 8
    d.polygon([P(tx, ty), P(tx + 26, ty + 3), P(tx, ty + 7)], fill=R, outline=K)
    ln([(tx, ty - 2), (tx, ty + 8)], 1.2)

# shrouds and ratlines (over the sails), stays between mastheads
for m in masts:
    xd = m["x"]
    head_y = m["top"] + (m["sails"][0][1] + 7) + (m["sails"][1][1] + 7) + 4   # near the topsail yard
    hx = mast_x(m, head_y)
    for sgn in (-1, 1):
        feet = [xd + sgn * (12 + 7 * k) for k in range(4)]
        for fx in feet:
            ln([(hx, head_y), (fx, DECK - 2)], 0.9)
        # ratlines between outermost shroud pairs
        for yy in range(DECK - 8, int(head_y) + 30, -7):
            t = (DECK - 2 - yy) / (DECK - 2 - head_y)
            xa = feet[0] + (hx - feet[0]) * t
            xb = feet[-1] + (hx - feet[-1]) * t
            ln([(xa, yy), (xb, yy)], 0.7)
# stays
f, mn, mzn = masts
ln([(mast_x(mn, mn["top"]), mn["top"]), (mast_x(f, f["top"]), f["top"])], 1.0)
ln([(mast_x(mzn, mzn["top"]), mzn["top"]), (mast_x(mn, mn["top"] + 60), mn["top"] + 60)], 1.0)
ln([(mast_x(f, f["top"]), f["top"]), (396, 362)], 1.0)
ln([(mast_x(f, f["top"] + 80), f["top"] + 80), (384, 366)], 1.0)
ln([(mast_x(f, f["top"] + 150), f["top"] + 150), (360, 374)], 1.0)
# backstays
ln([(mast_x(mn, mn["top"]), mn["top"]), (150, DECK - 2)], 0.8)
ln([(mast_x(f, f["top"]), f["top"]), (232, DECK - 2)], 0.8)

# jibs: three triangles between the forestays and the bowsprit
jibs = [((mast_x(f, f["top"] + 6), f["top"] + 6), (392, 364), (346, 388)),
        ((mast_x(f, f["top"] + 84), f["top"] + 84), (378, 370), (338, 390)),
        ((mast_x(f, f["top"] + 154), f["top"] + 154), (352, 378), (330, 392))]
for a, b, c in jibs:
    d.polygon([P(*a), P(*b), P(*c)], fill=Wt, outline=K)
    ln([a, b, c, a], 1.5)
    for k in range(1, 4):
        t = k / 4
        p = (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
        q = (c[0] + (b[0] - c[0]) * t * 0.9, c[1] + (b[1] - c[1]) * t * 0.9)
        ln(quad(p, ((p[0] + q[0]) / 2 + 3, (p[1] + q[1]) / 2), q), 0.8)

# print border
d.rectangle([*P(6, 6), *P(394, 594)], outline=K, width=int(2 * S))

def ink_downsample(im, s):
    """Downsample so that any pixel with a fair share of ink stays black
    (hairlines survive as 1px black instead of fading to grey)."""
    import numpy as np
    a = np.asarray(im).astype(np.float32)
    h, w, _ = a.shape
    a = a.reshape(h // s, s, w // s, s, 3)
    dark = a.max(-1) < 90
    frac = dark.mean(axis=(1, 3))
    light = np.where(dark[..., None], 0, a).sum(axis=(1, 3))
    cnt = np.maximum((~dark).sum(axis=(1, 3)), 1)[..., None]
    out = light / cnt
    out[frac >= 0.28] = 0
    return Image.fromarray(out.astype(np.uint8), "RGB")

ink_downsample(img, S).save(os.environ["OUT_RAW"])
