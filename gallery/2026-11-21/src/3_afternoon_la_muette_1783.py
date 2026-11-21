"""Afternoon — 'Expérience aérostatique': hand-coloured engraving of the first free flight,
Paris, 21 November 1783, 1:54 pm. Full palette; white paper in charge."""
import sys, math, os
sys.path.insert(0, os.path.dirname(__file__))
from common import *

rng = np.random.default_rng(1783)
img, d = new(WH)
HZ = 418  # horizon

# --- clouds first (masks), then the ruled sky that avoids them
clouds = []
for (cx, cy, w, sd) in [(70, 120, 120, 3), (345, 205, 110, 8), (60, 300, 90, 5), (330, 372, 130, 11), (150, 392, 80, 2), (300, 70, 70, 4)]:
    clouds.append(cumulus(img, cx, cy, w, seed=sd, shade=mix(WH, B, .75)))
cm = np.zeros((H * S, W * S), bool)
for c in clouds: cm |= c
a = np.asarray(img).copy()
y = 16.0; gap = 2.0
while y < HZ:
    yi = int(y * S)
    row = ~cm[yi]
    # engraver's line: breaks now and then, wobbles in weight
    brk = fbm((1, W * S), scale=90, octaves=2, seed=int(y * 7))[0] > (0.30 + 0.35 * (y - 16) / (HZ - 16))
    for k in range(S if y < 250 else 2):
        a[yi + k][row & brk] = B
    gap = 2.0 + 3.2 * ((y - 16) / (HZ - 16)) ** 1.3
    y += gap
img.paste(Image.fromarray(a)); d = ImageDraw.Draw(img); d.fontmode = "1"
# cloud outlines: scalloped engraved underlines
for c in clouds:
    m = Image.fromarray((c * 255).astype(np.uint8))
    edge = np.asarray(m.filter(ImageFilter.MaxFilter(S + 2))) > 127
    a = np.asarray(img).copy(); a[edge & ~c] = K; img.paste(Image.fromarray(a))
d = ImageDraw.Draw(img); d.fontmode = "1"

# --- distant Paris -------------------------------------------------------------
# hills on the horizon (Montmartre to the left, with windmills)
pts = [(0, HZ)]
for x in range(0, 401, 4):
    hgt = 9 * math.exp(-((x - 95) / 55) ** 2) + 5 * math.exp(-((x - 330) / 80) ** 2) + 1.5 * math.sin(x * .09)
    pts.append((x, HZ - 3 - hgt))
pts.append((400, HZ))
d.polygon(P(pts), fill=mix(WH, G, .55)); d.line(P(pts[1:-1]), fill=K, width=S)
for mx in (78, 96, 112):
    my = HZ - 12 - 9 * math.exp(-((mx - 95) / 55) ** 2) + 9
    d.rectangle(P(mx - 2, my - 6, mx + 2, my), fill=K)
    for k in range(4):
        an = .5 + k * math.pi / 2
        d.line(P((mx, my - 6), (mx + 6 * math.cos(an), my - 6 + 6 * math.sin(an))), fill=K, width=S)
d.rectangle(P(0, HZ, 400, 548), fill=WH)

def seine(s):
    x = 330 - 250 * s + 55 * math.sin(s * 4.6 + .4)
    y = HZ + 2 + 112 * s ** 1.35
    return x, y, 3.5 + 34 * s
left, right = [], []
for i in range(81):
    x, y, w = seine(i / 80)
    left.append((x - w, y)); right.append((x + w, y))
river = left + right[::-1]
rm = mask_of(lambda dd: dd.polygon(P(river), fill=255))
d.polygon(P(river), fill=B)
for i in range(6, 80, 2):          # ripples
    x, y, w = seine(i / 80)
    for k in range(int(1 + w / 6)):
        xx = x - w * .8 + rng.random() * w * 1.6; ln = 2 + w * .25 * rng.random()
        d.line(P((xx, y), (xx + ln, y)), fill=WH, width=S)
d.line(P(left), fill=K, width=S); d.line(P(right), fill=K, width=S)
# rooftops, far to near
def in_river(x, y):
    xi, yi = int(x * S), int(y * S)
    return 0 <= xi < W * S and 0 <= yi < H * S and rm[yi, xi]
ROOFS = [R, R, mix(R, K, .35), mix(B, K, .35), R, mix(R, Y, .5)]
y = HZ + 3.0
while y < 520:
    sz = 2.6 + (y - HZ) * 0.085
    x = -rng.random() * sz
    while x < 400:
        w = sz * (1.0 + .9 * rng.random()); hh = sz * (.55 + .6 * rng.random())
        if in_river(x, y) or in_river(x + w, y) or in_river(x + w / 2, y - hh):
            x += w; continue
        kind = rng.random()
        lw = 1 if sz < 5 else 2 if sz < 8 else S
        if kind < .13:   # tree clump (gardens)
            for j in range(3):
                rr = sz * (.45 + .3 * rng.random())
                d.ellipse(P(x + j * w / 3, y - rr * 1.7, x + j * w / 3 + rr * 1.6, y), fill=G if rng.random() < .7 else mix(G, K, .4), outline=K, width=lw)
        elif kind < .16 and sz > 4:   # church: tower + spire
            d.rectangle(P(x, y - hh * 2.0, x + w * .35, y), fill=WH, outline=K, width=lw)
            d.polygon(P((x - .5, y - hh * 2.0), (x + w * .35 + .5, y - hh * 2.0), (x + w * .175, y - hh * 3.6)), fill=mix(B, K, .4))
            d.rectangle(P(x + w * .35, y - hh, x + w, y), fill=WH, outline=K, width=lw)
            d.polygon(P((x + w * .35, y - hh), (x + w, y - hh), (x + w * .9, y - hh * 1.5), (x + w * .45, y - hh * 1.5)), fill=R, outline=K, width=lw)
        elif kind < .175 and sz > 5:  # dome (Invalides / Val-de-Grâce)
            d.rectangle(P(x, y - hh, x + w, y), fill=WH, outline=K, width=lw)
            d.pieslice(P(x + w * .1, y - hh - w * .55, x + w * .9, y - hh + w * .55), 180, 360, fill=Y, outline=K, width=lw)
            d.line(P((x + w * .5, y - hh - w * .55), (x + w * .5, y - hh - w * .9)), fill=K, width=lw)
        else:
            d.rectangle(P(x, y - hh, x + w, y), fill=WH, outline=K, width=lw)
            rf = ROOFS[rng.integers(len(ROOFS))]
            rh = sz * (.45 + .3 * rng.random())
            d.polygon(P((x - .4, y - hh), (x + w + .4, y - hh), (x + w * .82, y - hh - rh), (x + w * .18, y - hh - rh)), fill=rf, outline=K, width=lw)
            if sz > 5.5:
                # windows, chimney, shaded gable
                nwin = max(1, int(w / 3.2))
                for j in range(nwin):
                    wx = x + (j + .5) * w / nwin
                    d.rectangle(P(wx - .7, y - hh * .72, wx + .7, y - hh * .28), fill=K)
                d.rectangle(P(x + w * .6, y - hh - rh - 2.2, x + w * .6 + 1.6, y - hh - rh + 1), fill=K)
                for j in range(3):
                    d.line(P((x + w * .86 + j * .0, y - hh + 1 + j * 2), (x + w, y - hh + 1 + j * 2)), fill=K, width=1)
        x += w + sz * .12
    y += sz * (.78 + .1 * rng.random())

# Île de la Cité, with Notre-Dame
ix, iy, iw = seine(.50)
d.polygon(P((ix - 15, iy), (ix - 5, iy - 5), (ix + 10, iy - 4), (ix + 16, iy + 2), (ix + 6, iy + 6), (ix - 8, iy + 5)), fill=WH, outline=K)
d.rectangle(P(ix - 2, iy - 15, ix + 1, iy - 2), fill=WH, outline=K); d.rectangle(P(ix + 3, iy - 15, ix + 6, iy - 2), fill=WH, outline=K)
d.polygon(P((ix + 6, iy - 9), (ix + 16, iy - 9), (ix + 16, iy - 1), (ix + 6, iy - 1)), fill=mix(B, K, .3), outline=K)
d.line(P((ix + 11, iy - 9), (ix + 11, iy - 19)), fill=K, width=S)
# bridges
for s in (.22, .36, .62, .78, .93):
    x, y, w = seine(s)
    d.rectangle(P(x - w - 2, y - 1.5, x + w + 2, y + 1.5), fill=WH, outline=K)
    na = max(2, int(w / 3.2))
    for k in range(na):
        ax = x - w + (k + .5) * 2 * w / na
        d.pieslice(P(ax - w / na * .7, y + .5, ax + w / na * .7, y + 4.5 + w * .08), 180, 360, fill=K)


# --- the balloon -----------------------------------------------------------------
BCX, BY, BH = 205, 36, 318
# smoke drifting down-wind from the brazier
for i in range(420):
    f = rng.random()
    sx = BCX + 14 + f * 150 + rng.normal(0, 3 + 12 * f); sy = BY + BH * 1.0 + 4 + 16 * f ** .7 + rng.normal(0, 2 + 9 * f)
    r = .5 + 1.4 * rng.random() * (1 - f * .5)
    d.ellipse(P(sx - r, sy - r, sx + r, sy + r), fill=K if rng.random() < .75 else mix(K, WH, .5))
balloon(img, BCX, BY, BH, rot=0.42, fire=True)
d = ImageDraw.Draw(img); d.fontmode = "1"
# birds for scale
for (bx, by, bs) in [(52, 210, 5), (66, 222, 4), (40, 228, 4), (352, 128, 5), (368, 138, 4), (330, 300, 3.5), (88, 352, 3.5)]:
    d.line(P((bx - bs, by - bs * .5), (bx - bs * .3, by - bs * .7), (bx, by), (bx + bs * .3, by - bs * .7), (bx + bs, by - bs * .5)), fill=K, width=S + 1)

# --- the crowd on the terrace ----------------------------------------------------
TY = 522
d.rectangle(P(0, TY, 400, 552), fill=WH)
d.line(P((0, TY), (400, TY)), fill=K, width=S + 1)
d.rectangle(P(0, TY + 12, 400, TY + 14), fill=K)
COATS = [K, K, R, B, K, G, mix(R, K, .4), K, B]
x = 5.0
while x < 396:
    fh = 17 + 7 * rng.random(); col = COATS[rng.integers(len(COATS))]
    by = 552; lady = rng.random() < .3
    if lady:
        d.polygon(P((x - 5.5, by), (x + 5.5, by), (x + 2, by - fh * .55), (x - 2, by - fh * .55)), fill=col)
        d.polygon(P((x - 2.6, by - fh * .5), (x + 2.6, by - fh * .5), (x + 2, by - fh * .8), (x - 2, by - fh * .8)), fill=col)
        d.ellipse(P(x - 2, by - fh, x + 2, by - fh * .78), fill=WH, outline=K, width=S)
        d.ellipse(P(x - 4.5, by - fh * 1.06, x + 4.5, by - fh * .93), fill=K)   # wide hat
        if rng.random() < .5:   # parasol
            d.line(P((x + 3, by - fh * .6), (x + 7, by - fh * 1.35)), fill=K, width=S)
            d.pieslice(P(x + 1, by - fh * 1.6, x + 13, by - fh * 1.1), 180, 360, fill=Y if rng.random() < .5 else R, outline=K)
    else:
        d.polygon(P((x - 3.2, by), (x + 3.2, by), (x + 2.8, by - fh * .78), (x - 2.8, by - fh * .78)), fill=col)
        d.ellipse(P(x - 2, by - fh, x + 2, by - fh * .78), fill=WH, outline=K, width=S)
        d.polygon(P((x - 3.6, by - fh * .95), (x + 3.6, by - fh * .95), (x, by - fh * 1.12)), fill=K)  # tricorne
        g = rng.random()
        if g < .45:  # arm up, hat or handkerchief
            sgn = 1 if rng.random() < .5 else -1
            d.line(P((x + sgn * 2.5, by - fh * .7), (x + sgn * 6, by - fh * 1.15)), fill=col, width=S + 1)
            if rng.random() < .5:
                d.polygon(P((x + sgn * 4, by - fh * 1.15), (x + sgn * 8.5, by - fh * 1.15), (x + sgn * 6.2, by - fh * 1.32)), fill=K)
            else:
                d.rectangle(BX(x + sgn * 5, by - fh * 1.32, x + sgn * 8, by - fh * 1.15), fill=WH, outline=K)
        elif g < .6:  # telescope
            d.line(P((x + 1, by - fh * .86), (x + 8, by - fh * 1.2)), fill=K, width=S + 1)
    x += 9 + 6 * rng.random()

# --- plate border and lettering ---------------------------------------------------
d.rectangle(P(0, 552, 400, 600), fill=WH)
d.line(P((0, 552), (400, 552)), fill=K, width=S + 1)
text(d, (200, 566), "EXPÉRIENCE AÉROSTATIQUE", "serif-b", 15, K, spacing=1.6)
text(d, (200, 582), "faite au Château de la Muette, le 21 Novembre 1783", "serif", 13, K, spacing=.4)
for inset, wd in ((3, S + 1), (7, S)):
    d.rectangle(P(inset, inset, 400 - inset - .34, 600 - inset - .34), outline=K, width=wd)
finish(img)
