"""Night: the middle watch. The afternoon's barque again, now drawn in white
hairline on black -- sails and hull as dark shapes edged with light -- under
the September sky: Cassiopeia, Cepheus, the Little Bear with Polaris named,
the Great Square of Pegasus and Andromeda's chain, and the Milky Way as
stipple. Her lights are the only colour: green starboard lamp, white
masthead lights, yellow ports, and the Cape Halyard light flashing far off
to the right. Each light lays its reflection on the water."""
import math
import os
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFont

S = 4
W, H = 400 * S, 600 * S
K = (0, 0, 0); Wt = (255, 255, 255); R = (0xE0, 0x1B, 0x24)
Y = (0xF5, 0xD4, 0x00); B = (0x12, 0x3D, 0xB0); G = (0x1E, 0x9B, 0x3C)
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
random.seed(2200)

img = Image.new("RGB", (W, H), K)
d = ImageDraw.Draw(img)

OX, OY, KS = 0.0, 0.0, 1.0   # a scale/offset the ship is drawn through
def P(x, y): return ((OX + x * KS) * S, (OY + y * KS) * S)
def world(x, y): return (OX + x * KS, OY + y * KS)
def ln(pts, w=1.0, c=Wt): d.line([P(*p) for p in pts], fill=c, width=int(w * S), joint="curve")
def dot(x, y, r, c=Wt): d.ellipse([*P(x - r, y - r), *P(x + r, y + r)], fill=c)
def quad(p0, p1, p2, n=24):
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0],
             (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]) for t in (i / n for i in range(n + 1))]

HORIZON = 430
DECK = 398

# ------------------------------------------------------------------ sky
# Milky Way: a broad soft band from upper left toward the right, as stipple
for _ in range(2600):
    x = random.uniform(0, 400); y = random.uniform(0, HORIZON - 4)
    # band axis: from (40, 0) to (400, 250)
    ax, ay = 40, 0; bx, by = 400, 250
    t = ((x - ax) * (bx - ax) + (y - ay) * (by - ay)) / ((bx - ax) ** 2 + (by - ay) ** 2)
    px, py = ax + t * (bx - ax), ay + t * (by - ay)
    dd = math.hypot(x - px, y - py)
    if random.random() < math.exp(-(dd / 55) ** 2) * 0.9:
        dot(x, y, 0.55)
# general field
for _ in range(700):
    x = random.uniform(0, 400); y = random.uniform(0, HORIZON - 6)
    dot(x, y, random.choice([0.5, 0.5, 0.7, 0.9]))

def star(x, y, mag):
    r = {1: 2.4, 2: 1.8, 3: 1.3, 4: 0.9}[mag]
    dot(x, y, r)
    if mag <= 2:
        f = 7 if mag == 1 else 4.5
        ln([(x - f, y), (x + f, y)], 0.7); ln([(x, y - f), (x, y + f)], 0.7)

def figure(pts, mags, closed=False, w=0.7):
    for (x, y), m in zip(pts, mags):
        star(x, y, m)
    seq = pts + [pts[0]] if closed else pts
    for a, b in zip(seq, seq[1:]):
        # leave a gap around each star
        dx, dy = b[0] - a[0], b[1] - a[1]; L = math.hypot(dx, dy)
        ux, uy = dx / L, dy / L
        ln([(a[0] + ux * 5, a[1] + uy * 5), (b[0] - ux * 5, b[1] - uy * 5)], w)

lab = ImageFont.truetype(SERIF, 10 * S)
small = ImageFont.truetype(SERIF, 8 * S)
def label(x, y, s, f=small): d.text(P(x, y), s, font=f, fill=Wt, anchor="lm")

# Little Bear, Polaris at the tail
umi = [(200, 40), (214, 62), (222, 88), (238, 108), (262, 100), (268, 122), (246, 130)]
figure(umi, [2, 3, 4, 3, 4, 3, 3])
ln([(238, 108), (246, 130)], 0.7)
star(200, 40, 1)
d.ellipse([*P(200 - 9, 40 - 9), *P(200 + 9, 40 + 9)], outline=Wt, width=int(0.7 * S))
label(212, 34, "Polaris", lab)
# Cepheus, the house
cep = [(120, 60), (146, 48), (168, 76), (148, 116), (112, 110)]
figure(cep, [3, 3, 3, 3, 2], closed=True)
label(104, 130, "Cepheus")
# Cassiopeia, the W
cas = [(42, 130), (66, 150), (84, 138), (98, 168), (126, 178)]
figure(cas, [2, 2, 3, 2, 2])
label(40, 112, "Cassiopeia")
# Great Square of Pegasus and Andromeda's chain
peg = [(300, 150), (368, 162), (374, 236), (302, 226)]
figure(peg, [2, 2, 2, 2], closed=True)
label(306, 248, "Pegasus")
andr = [(300, 150), (292, 114), (286, 78), (276, 42)]
figure(andr, [2, 3, 2, 2])
label(300, 84, "Andromeda")
dot(274, 92, 1.2); label(262, 100, "M31")
# a planet, low and steady, plus a few brighter field stars
star(60, 300, 1); label(60, 288, "Saturn")
for x, y in [(160, 300), (350, 160), (30, 40), (90, 240), (380, 400), (140, 380)]:
    star(x, y, 3)

# ------------------------------------------------------------------ sea
ln([(0, HORIZON), (400, HORIZON)], 0.8, Wt)
for row, yy in enumerate(range(HORIZON + 10, 600, 12)):
    for _ in range(3 + row // 3):
        x = random.uniform(-10, 400); L = random.uniform(8, 20 + row)
        ln(quad((x, yy), (x + L / 2, yy - 2), (x + L, yy)), 0.9, B)

# Cape Halyard light, far to the right, on the horizon
lx, ly = 372, 424
d.polygon([P(348, HORIZON), P(360, 426), P(400, 427), P(400, HORIZON)], fill=K)
ln([(348, HORIZON), (360, 426), (400, 427)], 0.7, B)
ln([(lx, HORIZON), (lx, 410)], 1.2, Wt)
star(lx, 409, 1)
for a0 in (150, 200):   # a hint of the sweeping beam
    for k in range(14):
        a = math.radians(a0 + k * 1.2)
        rr = 20 + k * 6
        dot(lx + rr * math.cos(a), ly - 15 + rr * math.sin(a), 0.5)

# ------------------------------------------------------------------ the barque, in white line
# drawn in the afternoon piece's coordinates, scaled down and set to the right
KS = 0.55
OX, OY = 330 - 396 * KS, (HORIZON + 2) - 438 * KS
bow, stern = 336, 68
sheer = quad((stern, 392), (200, 404), (bow, 388))
hull = [P(*p) for p in sheer] + [P(bow + 6, 412), P(bow + 2, 438), P(stern - 6, 438), P(stern - 2, 405)]
d.polygon(hull, fill=K)
ln(sheer, 1.2)
ln([(bow, 388), (bow + 6, 412), (bow + 2, 438)], 1.0)
ln([(stern, 392), (stern - 2, 405), (stern - 6, 438)], 1.0)
# lit ports along the gun strake
band = [(x, y + 12) for x, y in sheer]
for x, y in band[2::2]:
    d.rectangle([*P(x - 1.6, y - 1.6), *P(x + 1.6, y + 1.6)], fill=Y)
# stern cabin windows
for i in range(3):
    d.rectangle([*P(stern + 4 + i * 6, 399), *P(stern + 8 + i * 6, 403)], fill=Y)
# rail, bowsprit
ln([(x, y - 3) for x, y in sheer], 0.7)
ln([(bow - 6, 390), (396, 362)], 1.6)
ln([(bow + 2, 400), (372, 372)], 0.7)

masts = [
    dict(x=272, top=112, sails=[(46, 30), (64, 40), (86, 54), (112, 72)]),
    dict(x=200, top=82,  sails=[(52, 34), (72, 46), (96, 62), (124, 80)]),
    dict(x=128, top=150, sails=[(44, 30), (60, 40), (80, 52)]),
]
def mast_x(m, y): return m["x"] + (DECK - y) * 0.035

def sail(x0, x1, yt, yb):
    mid = (yt + yb) / 2
    right = quad((x1, yt), (x1 + 7, mid), (x1 + 2, yb))
    bottom = quad((x1 + 2, yb), ((x0 + x1) / 2, yb + 9), (x0 - 2, yb))
    left = quad((x0 - 2, yb), (x0 - 7, mid), (x0, yt))
    outline = [(x0, yt), (x1, yt)] + right + bottom + left
    d.polygon([P(*p) for p in outline], fill=K)
    ln(outline + [(x0, yt)], 0.9)
    for k in (8, 18, 30):
        if k > (yb - yt) - 6:
            break
        shrink = k * 0.25
        ln(quad((x1 + 1 - shrink, yb - k), ((x0 + x1) / 2, yb - k + 8 - k * 0.12), (x0 - 1 + shrink, yb - k)), 0.6)

mz = masts[2]
gaff_peak = (mz["x"] - 62, 268); boom_end = (mz["x"] - 74, 392)
spanker = [(mast_x(mz, 300), 300), gaff_peak, boom_end, (mz["x"], 392)]
d.polygon([P(*p) for p in spanker], fill=K)
ln(spanker + [spanker[0]], 0.9)
ex, ey = gaff_peak
ln([(ex, ey), (ex - 22, ey - 4), (ex - 15, ey + 4), (ex - 22, ey + 12), (ex, ey + 14), (ex, ey)], 0.7)

for m in masts:
    top, xd = m["top"], m["x"]
    ln([(mast_x(m, top - 8), top - 8), (xd, DECK + 2)], 1.4)
    y = top + 4
    for wdt, hgt in m["sails"]:
        cx = mast_x(m, y)
        yard_w = wdt / 2 + 6
        ln([(cx - yard_w, y), (cx + yard_w, y)], 1.2)
        sail(cx - wdt / 2, cx + wdt / 2, y + 1, y + hgt)
        for sgn in (-1, 1):
            ln([(mast_x(m, y - 14), y - 14), (cx + sgn * yard_w, y)], 0.6)
        y += hgt + 7
    tx, ty = mast_x(m, top - 8), top - 8
    ln([(tx, ty), (tx + 26, ty + 3), (tx, ty + 7), (tx, ty)], 0.7)
for m in masts:
    xd = m["x"]
    head_y = m["top"] + (m["sails"][0][1] + 7) + (m["sails"][1][1] + 7) + 4
    hx = mast_x(m, head_y)
    for sgn in (-1, 1):
        feet = [xd + sgn * (12 + 7 * k) for k in range(4)]
        for fx in feet:
            ln([(hx, head_y), (fx, DECK - 2)], 0.6)
        for yy in range(DECK - 8, int(head_y) + 30, -7):
            t = (DECK - 2 - yy) / (DECK - 2 - head_y)
            ln([(feet[0] + (hx - feet[0]) * t, yy), (feet[-1] + (hx - feet[-1]) * t, yy)], 0.5)
f, mn, mzn = masts
ln([(mast_x(mn, mn["top"]), mn["top"]), (mast_x(f, f["top"]), f["top"])], 0.7)
ln([(mast_x(mzn, mzn["top"]), mzn["top"]), (mast_x(mn, mn["top"] + 60), mn["top"] + 60)], 0.7)
ln([(mast_x(f, f["top"]), f["top"]), (396, 362)], 0.7)
ln([(mast_x(f, f["top"] + 80), f["top"] + 80), (384, 366)], 0.7)
ln([(mast_x(f, f["top"] + 150), f["top"] + 150), (360, 374)], 0.7)
jibs = [((mast_x(f, f["top"] + 6), f["top"] + 6), (392, 364), (346, 388)),
        ((mast_x(f, f["top"] + 84), f["top"] + 84), (378, 370), (338, 390)),
        ((mast_x(f, f["top"] + 154), f["top"] + 154), (352, 378), (330, 392))]
for a, b, c in jibs:
    d.polygon([P(*a), P(*b), P(*c)], fill=K)
    ln([a, b, c, a], 0.9)

# ------------------------------------------------------------------ her lights
lights = []
def lamp(x, y, c, r=2.6):
    dot(x, y, r + 1.2, K); dot(x, y, r, c)
    for k in range(8):   # halo of dots
        a = k * math.pi / 4
        dot(x + (r + 3.5) * math.cos(a), y + (r + 3.5) * math.sin(a), 0.6, c)
    lights.append((x, c))
lamp(mast_x(f, f["top"] + 40), f["top"] + 40, Wt)      # forward masthead light
lamp(mast_x(mn, mn["top"] + 20), mn["top"] + 20, Wt)   # after masthead light, higher
lamp(bow - 30, 386, G, 2.4)                             # starboard sidelight
lamp(stern + 8, 386, Wt, 1.8)                           # stern light
port_xs = [world(px, 0)[0] for px, _ in band[2::6]]
lights = [(world(x, 0)[0], c) for x, c in lights]
OX, OY, KS = 0.0, 0.0, 1.0   # back to frame coordinates

lamp(120, 470, R, 1.6)                                  # a red buoy, closer in
label(126, 478, "Fl R")

# reflections: broken vertical columns of dashes under every light
for x, c in lights + [(lx, Wt)] + [(px, Y) for px in port_xs]:
    y = HORIZON + 6
    while y < 596:
        if random.random() < 0.7:
            w = random.uniform(2, 7) + (y - HORIZON) * 0.02
            ln([(x - w + random.uniform(-2, 2), y), (x + w + random.uniform(-2, 2), y)], 0.9, c)
        y += random.uniform(4, 9)
        if random.random() < (y - HORIZON) / 520:
            break

# print border
d.rectangle([*P(0, 0), *P(400, 600)], outline=Wt, width=int(1.5 * S))

def light_downsample(im, s):
    """Downsample keeping any pixel with a fair share of light lit
    (hairlines and stars survive as 1px instead of fading into the black)."""
    a = np.asarray(im).astype(np.float32)
    h, w, _ = a.shape
    a = a.reshape(h // s, s, w // s, s, 3)
    lit = a.max(-1) > 60
    frac = lit.mean(axis=(1, 3))
    tot = np.where(lit[..., None], a, 0).sum(axis=(1, 3))
    cnt = np.maximum(lit.sum(axis=(1, 3)), 1)[..., None]
    out = tot / cnt
    out[frac < 0.22] = 0
    return Image.fromarray(out.astype(np.uint8), "RGB")

light_downsample(img, S).save(os.environ["OUT_RAW"])
