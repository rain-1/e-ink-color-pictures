"""Night — Taurids over the Mole.
Scratchboard: a black ground and nothing but scratched line — white, with yellow for lamps
and blue for the cold. The sky is tonight's, looking east at 22h from about 50 N: Orion
rising on his side, Taurus and the Pleiades above, Capella top left, and a Northern Taurid
fireball falling away from the radiant beside the Pleiades (the shower peaks tonight; the
two-day moon set hours ago). Signac's harbour, after the painter has gone to bed."""
import math, os, random
from PIL import Image, ImageDraw
from kit import *

random.seed(2211)
im, d = canvas(K)
HOR = 404
CX, CY, SC, ROT = 215, 168, 6.6, math.radians(40)
def sky(ra, dec):
    x = -(ra - 4.7) * 15 * math.cos(math.radians(dec)); y = dec - 18
    return (CX + SC * (x * math.cos(ROT) - y * math.sin(ROT)), CY - SC * (x * math.sin(ROT) + y * math.cos(ROT)))

# ---------- the Milky Way: a stippled river down the left ----------
mw = [(5.3, 48), (5.6, 36), (5.9, 26), (6.2, 15), (6.6, 4), (6.9, -6)]
for k in range(1500):
    t = random.uniform(0, len(mw) - 1.001); i = int(t); f = t - i
    ra = mw[i][0] + (mw[i + 1][0] - mw[i][0]) * f + random.gauss(0, .33); dec = mw[i][1] + (mw[i + 1][1] - mw[i][1]) * f + random.gauss(0, 3)
    x, y = sky(ra, dec)
    if 0 < x < W and 0 < y < HOR - 8: circ(d, x, y, random.choice([.45, .45, .6, .8]), fill=Wh if k % 6 else B)
for k in range(260):                                                 # field stars
    x, y = random.uniform(0, W), random.uniform(0, HOR - 6)
    circ(d, x, y, random.choice([.45, .5, .7, .9]), fill=Wh if k % 5 else B)

# ---------- constellations ----------
ST = {"Alcyone": (3.79, 24.1, 2.9), "Aldebaran": (4.60, 16.5, 0.9), "gam": (4.33, 15.6, 3.6), "del": (4.38, 17.5, 3.8), "eps": (4.48, 19.2, 3.5),
      "the": (4.48, 15.9, 3.4), "Elnath": (5.44, 28.6, 1.7), "zet": (5.63, 21.1, 3.0), "lam": (4.01, 12.5, 3.4),
      "Betelgeuse": (5.92, 7.4, 0.5), "Bellatrix": (5.42, 6.35, 1.6), "Mintaka": (5.53, -0.3, 2.2), "Alnilam": (5.60, -1.2, 1.7), "Alnitak": (5.68, -1.9, 1.8),
      "Rigel": (5.24, -8.2, 0.1), "Saiph": (5.80, -9.7, 2.1), "Meissa": (5.59, 9.9, 3.4),
      "Capella": (5.28, 46.0, 0.1), "Menkalinan": (5.99, 44.9, 1.9), "theAur": (5.99, 37.2, 2.6), "iotAur": (4.95, 33.2, 2.7),
      "Mirfak": (3.41, 49.9, 1.8), "Algol": (3.14, 41.0, 2.1), "epsPer": (3.96, 40.0, 2.9), "zetPer": (3.90, 31.9, 2.9),
      "Hamal": (2.12, 23.5, 2.0), "Sheratan": (1.91, 20.8, 2.6), "Menkar": (3.04, 4.1, 2.5),
      "Alhena": (6.63, 16.4, 1.9), "Castor": (7.58, 31.9, 1.6), "Pollux": (7.76, 28.0, 1.2), "muGem": (6.38, 22.5, 2.9)}
LINES = [("lam", "gam"), ("gam", "the"), ("the", "Aldebaran"), ("gam", "del"), ("del", "eps"), ("Aldebaran", "zet"), ("eps", "Elnath"),
         ("Betelgeuse", "Bellatrix"), ("Bellatrix", "Mintaka"), ("Betelgeuse", "Alnitak"), ("Mintaka", "Alnilam"), ("Alnilam", "Alnitak"),
         ("Mintaka", "Rigel"), ("Alnitak", "Saiph"), ("Rigel", "Saiph"), ("Betelgeuse", "Meissa"), ("Bellatrix", "Meissa"),
         ("Capella", "Menkalinan"), ("Menkalinan", "theAur"), ("theAur", "Elnath"), ("Elnath", "iotAur"), ("iotAur", "Capella"),
         ("Mirfak", "epsPer"), ("epsPer", "zetPer"), ("Mirfak", "Algol"), ("Hamal", "Sheratan"), ("Castor", "Pollux"), ("Alhena", "muGem")]
def dashed(a, b, c, w=0.6, on=3.0, off=3.0):
    L = math.hypot(b[0] - a[0], b[1] - a[1]); n = int(L / (on + off))
    for k in range(n + 1):
        t0 = k * (on + off) / L; t1 = min(1, t0 + on / L)
        if t0 < 1: line(d, [(a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0), (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1)], c, w)
for a, b in LINES:
    pa, pb = sky(*ST[a][:2]), sky(*ST[b][:2])
    if pa[1] < HOR - 4 and pb[1] < HOR - 4: dashed(pa, pb, B, 0.75)
def starpt(x, y, mag, tint=Wh):
    r = max(.8, 3.5 - mag * .78)
    if mag < 1.3:
        for k in range(8):
            a = k * math.pi / 4; l = r * (2.6 if k % 2 == 0 else 1.7)
            line(d, [(x + math.cos(a) * (r + .8), y + math.sin(a) * (r + .8)), (x + math.cos(a) * l * 1.3, y + math.sin(a) * l * 1.3)], tint, 0.6)
    circ(d, x, y, r, fill=Wh)
    if tint != Wh and mag < 1.3: circ(d, x, y, r * .55, fill=tint)
TINT = {"Aldebaran": R, "Betelgeuse": R, "Capella": Y, "Rigel": B, "Pollux": Y}
for n_, (ra, dec, mag) in ST.items():
    x, y = sky(ra, dec)
    if 0 < x < W and 0 < y < HOR - 5 and n_ != "Alcyone": starpt(x, y, mag, TINT.get(n_, Wh))
px_, py_ = sky(3.79, 24.1)                                           # the Pleiades, seven and a haze
for dx_, dy_, r_ in [(0, 0, 1.5), (-4, -2.5, 1.2), (-6.5, 1, 1.1), (-3, 3.5, 1.0), (3.5, 2.5, 1.1), (5.5, -1.5, .9), (1.5, -4.5, .8)]:
    circ(d, px_ + dx_, py_ + dy_, r_, fill=Wh)
for k in range(26): circ(d, px_ + random.gauss(0, 5), py_ + random.gauss(0, 4), .45, fill=B)
for (ra, dec, t) in [(3.55, 27.5, "PLEIADES"), (4.55, 12.2, "TAURUS"), (5.95, 2.6, "ORION"), (5.0, 49.5, "Capella"), (4.85, 18.2, "Aldebaran"), (6.5, 38.5, "AURIGA")]:
    x, y = sky(ra, dec); text(d, x, y, t, 8, Wh, italic=t[1].islower())

# ---------- the fireball, and two fainter Taurids from the same radiant ----------
rx, ry = sky(3.87, 22.6)
def meteor(ang, r0, r1, big):
    ca, sa = math.cos(ang), math.sin(ang)
    a = (rx + ca * r0, ry + sa * r0); b = (rx + ca * r1, ry + sa * r1)
    if big:
        for k in range(26):                                           # scratched train, widening to the head
            t = k / 25; w_ = 1.1 + 3.0 * t ** 2
            p = (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
            q = (a[0] + (b[0] - a[0]) * (t + .03), a[1] + (b[1] - a[1]) * (t + .03))
            line(d, [p, q], Wh if k % 3 else Y, w_)
            if k > 8 and k % 2 == 0:
                off = (k % 4 - 1) * 1.0
                line(d, [(p[0] - sa * (w_ + 1.5) * off, p[1] + ca * (w_ + 1.5) * off), (p[0] - sa * (w_ + 1.5) * off - ca * 9, p[1] + ca * (w_ + 1.5) * off - sa * 9)], Y, 0.6)
        circ(d, b[0], b[1], 5.5, fill=Y); circ(d, b[0], b[1], 3.2, fill=Wh)
        for k in range(12):
            aa = k * math.pi / 6; line(d, [(b[0] + math.cos(aa) * 7.5, b[1] + math.sin(aa) * 7.5), (b[0] + math.cos(aa) * (11 + 4 * (k % 2)), b[1] + math.sin(aa) * (11 + 4 * (k % 2)))], Y if k % 2 else R, 0.8)
    else:
        line(d, [a, b], Wh, 0.8); line(d, [((a[0] + b[0]) / 2, (a[1] + b[1]) / 2), b], Wh, 1.3); circ(d, b[0], b[1], 1.3, fill=Y)
meteor(math.radians(28), 34, 150, True)
meteor(math.radians(-112), 40, 86, False); meteor(math.radians(168), 60, 104, False)
dashed((rx - 5, ry), (rx + 5, ry), Y, 0.7, 2, 2); dashed((rx, ry - 5), (rx, ry + 5), Y, 0.7, 2, 2)                   # the radiant, marked

# ---------- headland and lighthouse, left ----------
head = [(0, 352), (40, 356), (84, 372), (128, 394), (160, HOR), (0, HOR)]
hatch(im, head, B, gap=3.2, ang=-28, w=0.8); line(d, head[:-1], Wh, 0.9)
lx = 46
tower = [(lx - 8, 356), (lx - 5, 286), (lx + 5, 286), (lx + 8, 356)]
poly(d, tower, fill=K, outline=Wh, w=0.9); hatch(im, tower, Wh, gap=2.2, ang=90, w=0.5)
for y0 in (298, 322, 344): rect(d, lx - 7.6, y0, lx + 7.6, y0 + 9, fill=R)
rect(d, lx - 8, 281, lx + 8, 286, fill=Wh); rect(d, lx - 5, 270, lx + 5, 281, fill=Y, outline=Wh, w=0.6)
for k in (-2, 0, 2): line(d, [(lx + k * 1.7, 270), (lx + k * 1.7, 281)], K, 0.5)
poly(d, [(lx - 6.5, 270), (lx, 261), (lx + 6.5, 270)], fill=Wh); line(d, [(lx, 261), (lx, 255)], Wh, 0.7)
rect(d, lx - 2, 346, lx + 2, 356, fill=Y)
rect(d, lx + 12, 344, lx + 34, 358, fill=K, outline=Wh, w=0.8); poly(d, [(lx + 10, 344), (lx + 23, 335), (lx + 36, 344)], fill=K, outline=Wh, w=0.8); rect(d, lx + 20, 348, lx + 25, 353, fill=Y)
for sgn, a0 in ((1, -9), (-1, 189)):                                 # the two beams
    for k in range(-4, 5):
        a = math.radians(a0 + k * 1.5 * sgn)
        dashed((lx + math.cos(a) * 9, 275 + math.sin(a) * 9), (lx + math.cos(a) * 330, 275 + math.sin(a) * 330), Y, 0.75, 5 + abs(k) * 1.5, 4 + abs(k) * 3)

# ---------- sea ----------
line(d, [(0, HOR), (W, HOR)], Wh, 0.8)
for k in range(1500):
    y = HOR + 2 + (random.random() ** 1.5) * 150; t = (y - HOR) / 150
    x = random.uniform(-10, W); L = 3 + 15 * t * random.random() + 2
    line(d, [(x, y), (x + L, y)], B if random.random() < .62 else Wh, 0.6 + .5 * t)
for k in range(60):                                                   # the lamp's road on the water
    y = HOR + 3 + k * 2.2; half = 2 + k * .22 + 3 * math.sin(k * 1.1)
    if k % 4 != 3: line(d, [(lx + 30 + k * .5 - half, y), (lx + 30 + k * .5 + half, y)], Y, 0.9)

# ---------- the mole and its houses, right ----------
mole = [(268, HOR + 2), (W, HOR - 2), (W, 474), (250, 474)]
poly(d, mole, fill=K, outline=Wh, w=0.9)
for yy in range(HOR + 44, 474, 6):                                    # stone courses
    line(d, [(254, yy), (W, yy)], Wh, 0.45)
    for xx_ in range(254 + (yy % 12), W, 13): line(d, [(xx_, yy), (xx_, yy + 6)], Wh, 0.4)
x = 282; hk = 0
while x < W - 6:
    w = random.choice([24, 28, 32]); h = random.choice([54, 66, 78, 60]); base = HOR + 42; hk += 1
    rect(d, x, base - h, x + w, base, fill=K, outline=Wh, w=0.9)
    roof = [(x - 2, base - h), (x + w / 2, base - h - 13), (x + w + 2, base - h)]
    poly(d, roof, fill=K, outline=Wh, w=0.9); hatch(im, roof, Wh, gap=2.4, ang=0, w=0.45)
    rect(d, x + w * .68, base - h - 16, x + w * .68 + 4, base - h - 5, fill=K, outline=Wh, w=0.6)
    for fl in range(int(h // 17)):
        for cx_ in (x + w * .28, x + w * .72):
            wy = base - h + 6 + fl * 17
            lit = random.random() < .3
            rect(d, cx_ - 3, wy, cx_ + 3, wy + 9, fill=Y if lit else K, outline=Wh if not lit else Y, w=0.6)
            if not lit:
                for q in range(3): line(d, [(cx_ - 3, wy + 2 + q * 2.6), (cx_ + 3, wy + 2 + q * 2.6)], B, 0.5)       # shutters
            else: line(d, [(cx_, wy), (cx_, wy + 9)], K, 0.5)
    if hk == 2:                                                       # the cafe, still open
        rect(d, x + 3, base - 15, x + w - 3, base - 1, fill=Y); line(d, [(x + w / 2, base - 15), (x + w / 2, base - 1)], K, 0.6)
        poly(d, [(x, base - 16), (x + w, base - 16), (x + w + 3, base - 11), (x - 3, base - 11)], fill=R)
        for q in range(8):
            yq = base + 34 + q * 3.2
            if q % 3 != 2: line(d, [(x + 5 - q, yq + 26), (x + w - 5 + q, yq + 26)], Y, 0.8)
    x += w + 1
line(d, [(268, HOR + 42), (W, HOR + 42)], Wh, 0.9)
for k in range(6): rect(d, 262 + k * 26, HOR + 37, 265 + k * 26, HOR + 42, fill=Wh)                                   # bollards on the mole
lampx = 272                                                           # harbour light at the mole end (green = starboard hand)
line(d, [(lampx, HOR + 42), (lampx, HOR + 10)], Wh, 1.2); circ(d, lampx, HOR + 7, 3.4, fill=G, outline=Wh, w=0.5)
for q in range(22):
    yq = 478 + q * 2.6
    if q % 3 != 2: line(d, [(lampx - 2 - q * .3 + 2 * math.sin(q), yq), (lampx + 2 + q * .3 + 2 * math.sin(q), yq)], G, 0.9)

# ---------- moored boats ----------
def boat(cx, wl, L, mast_h, lamp):
    hull = [(cx - L / 2, wl - L * .12), (cx - L * .34, wl), (cx + L * .36, wl), (cx + L / 2 + L * .06, wl - L * .16), (cx + L * .2, wl - L * .11), (cx - L * .3, wl - L * .1)]
    for q in range(int(mast_h / 3.2)):                                 # the mast shivering in the water
        yq = wl + 3 + q * 2.4
        if q % 3 != 2 and yq < 536: line(d, [(cx + 3 * math.sin(q * .8) - 1, yq), (cx + 3 * math.sin(q * .8) + 1.6 + q * .04, yq)], Wh, 0.7)
    poly(d, hull, fill=K, outline=Wh, w=1); hatch(im, hull, Wh, gap=2.3, ang=-3, w=0.5)
    line(d, [hull[0], hull[3]], Wh, 0.5)
    line(d, [(cx, wl - L * .1), (cx, wl - mast_h)], Wh, 1.3)
    boom = [(cx + 2, wl - L * .22), (cx - L * .46, wl - L * .2)]
    line(d, boom, Wh, 1.1)
    for q in range(7):                                                # furled sail, lashed
        t = q / 7; bx = boom[0][0] + (boom[1][0] - boom[0][0]) * t; by = boom[0][1] + (boom[1][1] - boom[0][1]) * t
        d.arc([(bx - L * .07) * S, (by - 5) * S, (bx) * S, (by + 1) * S], 180, 360, fill=Wh, width=2); line(d, [(bx - L * .035, by - 5), (bx - L * .035, by + 1)], Y, 0.5)
    for end, c in ((hull[3], Wh), (hull[0], Wh), ((cx + L * .2, wl - L * .11), B), ((cx - L * .3, wl - L * .1), B)):
        line(d, [(cx, wl - mast_h + 3), end], c, 0.5)
    line(d, [(cx - L * .07, wl - mast_h * .62), (cx + L * .07, wl - mast_h * .62)], Wh, 0.8)                           # spreader
    rect(d, cx - L * .14, wl - L * .2, cx + L * .1, wl - L * .11, fill=K, outline=Wh, w=0.7)                           # cabin
    for q in range(2): circ(d, cx - L * .08 + q * L * .11, wl - L * .155, 1.5, fill=Y if q == 0 and lamp == R else K, outline=Wh, w=0.5)
    circ(d, cx, wl - mast_h - 2, 2.2, fill=lamp); poly(d, [(cx, wl - mast_h + 6), (cx + 9, wl - mast_h + 8.5), (cx, wl - mast_h + 11)], fill=R)
    for q in range(10):
        yq = wl + 4 + q * 2.8; line(d, [(cx - L * .3 + q * 2 + 2 * math.sin(q), yq), (cx + L * .3 - q * 2 + 2 * math.sin(q), yq)], Wh if q % 2 else B, 0.6)
    line(d, [hull[3], (hull[3][0] + L * .3, wl + 18)], Wh, 0.4)        # mooring line
boat(226, 462, 62, 104, Wh); boat(120, 506, 118, 236, R)
# a dinghy
dh = [(28, 512), (36, 520), (72, 520), (80, 510)]; poly(d, dh, fill=K, outline=Wh, w=0.9); hatch(im, dh, Wh, gap=2.2, ang=0, w=0.45); line(d, [(40, 512), (66, 506)], Wh, 0.8)

# ---------- the near quay ----------
q0 = 540
rect(d, -2, q0, W + 2, H + 2, fill=K); line(d, [(0, q0), (W, q0)], Wh, 1.3)
for row, yy in enumerate(range(q0 + 9, H, 9)):
    line(d, [(0, yy), (W, yy)], Wh, 0.45)
    for xx_ in range((row % 2) * 13 - 6, W, 26): line(d, [(xx_, yy - 9), (xx_, yy)], Wh, 0.45)
for bx in (34, 150, 300):                                             # bollards with rope
    poly(d, [(bx - 6, q0), (bx - 4, q0 - 12), (bx + 4, q0 - 12), (bx + 6, q0)], fill=K, outline=Wh, w=0.9); ell(d, bx, q0 - 12, 6.5, 2.4, fill=K, outline=Wh, w=0.8)
    for q in range(3): line(d, [(bx - 5.4, q0 - 4 - q * 2), (bx + 5.4, q0 - 4 - q * 2)], Y, 0.6)
# lobster pots and a coil of rope
for px0 in (190, 214):
    d.pieslice([(px0 - 11) * S, (q0 - 13) * S, (px0 + 11) * S, (q0 + 13) * S], 180, 360, fill=K, outline=Wh, width=2)
    for q in range(-3, 4): line(d, [(px0 + q * 3, q0), (px0 + q * 2.6, q0 - math.sqrt(max(0, 169 - (q * 3.1) ** 2)) * .97)], Wh, 0.45)
    for q in (4, 8): line(d, [(px0 - math.sqrt(121 - q * q) , q0 - q), (px0 + math.sqrt(121 - q * q), q0 - q)], Wh, 0.45)
for r_ in (3, 6, 9): ell(d, 250, q0 + 14, r_ * 1.7, r_ * .7, outline=Y, w=0.8)
# the watcher on the quay with a flask, and the harbour cat, both looking up
wx = 352
poly(d, [(wx - 9, q0), (wx - 7, q0 - 22), (wx + 5, q0 - 24), (wx + 9, q0 - 8), (wx + 20, q0 - 6), (wx + 21, q0)], fill=K, outline=Wh, w=0.9)
hatch(im, [(wx - 9, q0), (wx - 7, q0 - 22), (wx + 5, q0 - 24), (wx + 9, q0 - 8), (wx + 9, q0)], Wh, gap=2.4, ang=70, w=0.45)
circ(d, wx - 3, q0 - 29, 5, fill=K, outline=Wh, w=0.9); d.pieslice([(wx - 9) * S, (q0 - 36) * S, (wx + 3) * S, (q0 - 26) * S], 150, 350, fill=R)
line(d, [(wx + 3, q0 - 18), (wx + 11, q0 - 26), (wx + 6, q0 - 31)], Wh, 1.6)                                           # arm raised, pointing
rect(d, wx + 26, q0 - 9, wx + 30, q0, fill=Y, outline=Wh, w=0.5)
cx_, cy_ = 96, q0
ell(d, cx_, cy_ - 6, 8, 6, fill=K, outline=Wh, w=0.9); circ(d, cx_ + 7, cy_ - 14, 4.4, fill=K, outline=Wh, w=0.9)
poly(d, [(cx_ + 3.6, cy_ - 17), (cx_ + 4.4, cy_ - 22), (cx_ + 7.6, cy_ - 18)], fill=K, outline=Wh, w=0.7); poly(d, [(cx_ + 8, cy_ - 18), (cx_ + 11, cy_ - 22), (cx_ + 11, cy_ - 16.5)], fill=K, outline=Wh, w=0.7)
circ(d, cx_ + 6, cy_ - 14.5, .9, fill=Y); circ(d, cx_ + 9.4, cy_ - 14.5, .9, fill=Y)
line(d, [(cx_ - 7, cy_ - 3), (cx_ - 15, cy_ - 2), (cx_ - 18, cy_ - 8)], Wh, 1.5)
text(d, 200, 586, "11 · XI · 2026    22 h    looking east    Northern Taurids at maximum", 7.6, Wh, italic=True)
out = os.environ.get("OUT_RAW", "out_raw.png")
vote_down(im, S, wk=0.42).save(out)                                   # favour the scratched line over the black
