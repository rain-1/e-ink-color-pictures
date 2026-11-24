# Night — "Luna Plena". Black in charge; white and blue moon, yellow engraving, one red star.
# A page from a lunar atlas for tonight's perigee full moon: seas screened in blue, craters
# and ray systems, a graduated limb, numbered features with a key, the Pleiades and Uranus
# (at opposition tomorrow) beside it, and the lunation as a strip of phases along the foot.
import math, random
import numpy as np
from common import *
rng = random.Random(24); img, d = new(K)
cx, cy, r = 200, 232, 132
U = (XX - cx) / r; V = -(YY - cy) / r; disc = U * U + V * V <= 1

# --- field stars
for _ in range(260):
    x, y = rng.randrange(W), rng.randrange(0, 420)
    if (x - cx) ** 2 + (y - cy) ** 2 < (r + 16) ** 2: continue
    d.point((x, y), fill=Wh if rng.random() < 0.8 else rng.choice([Y, B]))
    if rng.random() < 0.07: d.point((x + 1, y), fill=Wh); d.point((x, y + 1), fill=Wh)

# --- the seas: blobs perturbed by noise
blobs = [(-.25, .50, .31), (.28, .46, .19), (.47, .16, .21), (.77, .30, .105), (.72, -.10, .15), (.52, -.28, .10),
         (-.22, -.36, .21), (-.57, -.41, .115), (-.62, .22, .30), (-.52, -.06, .22), (-.74, .44, .14),
         (.05, .22, .075), (-.02, .04, .06), (-.38, .0, .13), (.62, .5, .06), (-.08, -.2, .08)]
M = np.full((H, W), -9.0, np.float32)
for (u, v, s) in blobs: M = np.maximum(M, 1 - np.hypot(U - u, V - v) / s)
frig = 1 - np.hypot((U + 0.03) / 0.52, (V - 0.80 + 0.12 * U * U) / 0.045); M = np.maximum(M, frig * 0.5)
n1 = fbm(7, 26, 4); n2 = fbm(8, 9, 2)
M += 0.55 * (n1 - 0.5)
tone(img, disc, Wh, K, 0.05 + 0.10 * n2 + 0.25 * np.clip(np.hypot(U, V) - 0.86, 0, 1) * 4)      # highlands, limb
mare = disc & (M > 0)
tone(img, mare, B, K, 0.04 + 0.2 * n2)
tone(img, disc & (M > -0.07) & (M <= 0), None, B, 0.5)
tone(img, mare & (M < 0.10), None, Wh, 0.25)

# --- craters
def crater(u, v, s, bright=False, dark=False):
    x, y = cx + u * r, cy - v * r; f = math.sqrt(max(0.05, 1 - u * u - v * v))    # foreshortening
    ang = math.degrees(math.atan2(-v, u)); 
    rx, ry = s, s
    box = (x - rx, y - ry, x + rx, y + ry)
    if dark: d.ellipse(box, fill=B)
    if bright: d.ellipse(box, fill=Wh)
    d.arc(box, 200, 20, fill=K); d.arc(box, 20, 200, fill=Wh if not bright else K)
    if s >= 4 and not dark: d.point((x, y), fill=K)
    return x, y
def rays(u, v, n, lo, hi, col=Wh):
    x, y = cx + u * r, cy - v * r
    for i in range(n):
        a = 2 * math.pi * i / n + rng.uniform(-0.15, 0.15); L = rng.uniform(lo, hi); st = rng.uniform(4, 8)
        k = st
        while k < L:
            px, py = x + math.cos(a) * k, y + math.sin(a) * k
            if (px - cx) ** 2 + (py - cy) ** 2 < (r - 2) ** 2:
                on_mare = mare[int(py), int(px)]
                if on_mare: d.point((px, py), fill=col)
                elif int(k) % 3 == 0: d.point((px, py), fill=K)
            k += 1 if k < L * 0.6 else 2
for _ in range(210):                                        # the anonymous hundreds, thick in the south
    a = rng.uniform(0, 2 * math.pi); q = math.sqrt(rng.random()) * 0.97; u, v = q * math.cos(a), q * math.sin(a)
    x, y = int(cx + u * r), int(cy - v * r)
    if mare[y, x] and rng.random() < 0.8: continue
    if v > 0.1 and rng.random() < 0.5: continue
    crater(u, v, rng.choice([1.5, 2, 2, 3, 3, 4, 5]))
named = {"Tycho": (-.10, -.68, 5), "Copernicus": (-.33, .17, 6), "Kepler": (-.60, .14, 3), "Aristarchus": (-.68, .40, 3),
         "Plato": (-.10, .78, 6), "Grimaldi": (-.92, -.09, 5), "Langrenus": (.86, -.15, 5), "Proclus": (.70, .28, 2.5),
         "Clavius": (-.12, -.85, 8), "Ptolemaeus": (-.03, -.16, 6), "Theophilus": (.42, -.20, 5)}
rays(-.10, -.68, 22, 50, 150); rays(-.33, .17, 14, 16, 44); rays(-.60, .14, 10, 10, 26); rays(-.68, .40, 8, 8, 20); rays(.70, .28, 7, 8, 22)
pos = {}
for k, (u, v, s) in named.items():
    pos[k] = crater(u, v, s, bright=k in ("Tycho", "Copernicus", "Kepler", "Aristarchus", "Proclus"), dark=k in ("Plato", "Grimaldi"))

# --- graduated limb
for i in range(360):
    a = math.radians(i); L = 8 if i % 30 == 0 else (5 if i % 10 == 0 else (3 if i % 2 == 0 else 0))
    if L: d.line((cx + (r + 5) * math.cos(a), cy + (r + 5) * math.sin(a), cx + (r + 5 + L) * math.cos(a), cy + (r + 5 + L) * math.sin(a)), fill=Y)
d.ellipse((cx - r - 5, cy - r - 5, cx + r + 5, cy + r + 5), outline=Y); d.ellipse((cx - r - 14, cy - r - 14, cx + r + 14, cy + r + 14), outline=Y)
fs = font("DejaVu Sans:bold", 9); fl = font("DejaVu Sans", 8); fi = font("DejaVu Serif:italic", 9)
for (t, a) in [("N", -90), ("E", 0), ("S", 90), ("W", 180)]:
    x = cx + (r + 23) * math.cos(math.radians(a)); y = cy + (r + 23) * math.sin(math.radians(a))
    d.rectangle((x - 5, y - 6, x + 5, y + 6), fill=K); d.text((x - 3, y - 6), t, font=fs, fill=Y)

# --- numbered features and key
feats = [("Mare Imbrium", -.25, .50), ("Mare Serenitatis", .28, .46), ("Mare Tranquillitatis", .47, .14), ("Mare Crisium", .77, .30),
         ("Mare Fecunditatis", .72, -.10), ("Mare Nectaris", .52, -.30), ("Mare Nubium", -.22, -.38), ("Mare Humorum", -.57, -.41),
         ("Oceanus Procellarum", -.66, .24), ("Mare Frigoris", .16, .80), ("Tycho", -.10 + .07, -.68), ("Copernicus", -.33 + .08, .17),
         ("Plato", -.10 + .08, .78 - .03), ("Aristarchus", -.68 + .06, .40 + .03), ("Kepler", -.60, .14 - .06), ("Clavius", -.12 + .10, -.85)]
fn = font("DejaVu Sans:bold", 8)
for i, (name, u, v) in enumerate(feats, 1):
    x, y = cx + u * r, cy - v * r; s = str(i); w = 6 if i < 10 else 8
    d.ellipse((x - w, y - 6, x + w, y + 6), fill=Y, outline=K)
    d.text((x - d.textlength(s, font=fn) / 2 + 0.5, y - 5), s, font=fn, fill=K)
ky = 420
d.line((24, ky - 8, 376, ky - 8), fill=Y); d.line((24, ky - 6, 376, ky - 6), fill=Y)
for i, (name, u, v) in enumerate(feats):
    col, row = divmod(i, 6); x = 26 + col * 124; y = ky + row * 12
    d.text((x, y), f"{i + 1}", font=fn, fill=Y); d.text((x + 13, y), name, font=fl, fill=Wh)

# --- title
ft = font("DejaVu Serif:bold", 17)
spaced(d, 200, 14, "LUNA PLENA", ft, Y, gap=7)
spaced(d, 200, 40, "XXIV · XI · MMXXVI", font("DejaVu Serif", 9), Wh, gap=2)
d.line((60, 36, 340, 36), fill=Y)

# --- neighbours: Pleiades, Uranus, Aldebaran
px, py = 352, 78
for (dx, dy, s) in [(0, 0, 2), (7, -3, 1), (-6, 2, 1), (3, 6, 1), (-3, -6, 1), (11, 3, 1), (-10, -3, 0), (5, -9, 0), (14, -6, 0)]:
    if s == 2: d.ellipse((px + dx - 1, py + dy - 1, px + dx + 1, py + dy + 1), fill=Wh)
    elif s == 1: d.rectangle((px + dx, py + dy, px + dx + 1, py + dy + 1), fill=Wh)
    else: d.point((px + dx, py + dy), fill=Wh)
d.text((330, 90), "Pleiades", font=fi, fill=Wh)
d.ellipse((30, 76, 34, 80), fill=G); d.ellipse((27, 73, 37, 83), outline=G); d.text((42, 71), "Uranus", font=fi, fill=Wh); d.text((42, 82), "☍ 25 XI", font=fl, fill=G)
d.ellipse((357, 376, 363, 382), fill=R); d.line((353, 379, 367, 379), fill=R); d.line((360, 372, 360, 386), fill=R)
d.text((306, 386), "Aldebaran", font=fi, fill=Wh)
d.text((22, 380), "Full 14:53 UT", font=fi, fill=Wh); d.text((22, 391), "perigee · +6.5% · +13.5% lux", font=fl, fill=Y)

# --- the lunation along the foot
d.line((24, 500, 376, 500), fill=Y)
spaced(d, 200, 506, "THE BEAVER MOON · LUNATION OF NOVEMBER", font("DejaVu Sans", 8), Y, gap=2)
N = 15
for i in range(N):
    x = 32 + i * 24; y = 548; rr = 9; ph = i / (N - 1)            # 0 new .. 0.5 full .. 1 new
    for yy in range(-rr, rr + 1):
        hw = math.sqrt(rr * rr - yy * yy); k = math.cos(2 * math.pi * ph)        # 1 new, -1 full
        if ph <= 0.5: x0, x1 = k * hw, hw
        else: x0, x1 = -hw, -k * hw
        if x1 - x0 > 0.6: d.line((x + x0, y + yy, x + x1, y + yy), fill=Wh)
    d.ellipse((x - rr, y - rr, x + rr, y + rr), outline=B if i != 7 else Wh)
    if i == 7:
        d.ellipse((x - rr - 4, y - rr - 4, x + rr + 4, y + rr + 4), outline=Y); d.polygon([(x, y + rr + 7), (x - 4, y + rr + 13), (x + 4, y + rr + 13)], fill=Y)
    lab = ["9", "", "", "17", "", "", "", "24", "", "", "", "1", "", "", "9"][i]
    if lab and i != 7: d.text((x - d.textlength(lab, font=fl) / 2, y + rr + 5), lab, font=fl, fill=Wh)
d.text((200 - d.textlength("24", font=fs) / 2, 578), "24", font=fs, fill=Y)
d.rectangle((6, 6, W - 7, H - 7), outline=Y)
save(img)
