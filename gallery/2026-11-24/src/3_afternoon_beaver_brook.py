# Afternoon — "Beaver Brook: a valley re-engineered". Full palette; green in charge.
# A survey sheet of an imagined valley: a generated terrain with red-brown contours, one
# brook stepped into three ponds by three dams, lodges, canals dug out to the aspen, the
# felled patches with every stump plotted, spruce on the high ground. Border, cartouche, key.
import math, random
import numpy as np
from common import *
rng = random.Random(2026); img, d = new(Wh)
L, T, Rt, Bm = 16, 16, 384, 584                         # neatline
inside = (XX >= L) & (XX < Rt) & (YY >= T) & (YY < Bm)

# --- terrain: a valley wandering down the sheet
sx = lambda y: 200 + 62 * math.sin(y / 92 + 0.6) + 26 * math.sin(y / 37 + 1.3)
SX = np.array([sx(y) for y in range(H)], np.float32)[:, None]
n1 = fbm(11, 110, 4); n2 = fbm(12, 30, 3)
dist = np.abs(XX - SX)
hgt = (dist / 210) ** 0.9 + 0.55 * (n1 - 0.5) + 0.10 * (n2 - 0.5) + (600 - YY) / 600 * 0.55
# --- land cover
forest = inside & ((dist > 46 + 60 * n2) | (n1 > 0.62))
meadow = inside & ~forest
tone(img, meadow, Wh, Y, 0.10 + 0.10 * n2)
tone(img, forest, Wh, G, 0.5)
# --- contours
step = 0.07; q = np.floor(hgt / step)
edge = inside & ((q != np.roll(q, 1, 0)) | (q != np.roll(q, 1, 1)))
a = np.asarray(img).copy(); a[edge] = R
idx = inside & ((np.floor(hgt / (step * 5)) != np.roll(np.floor(hgt / (step * 5)), 1, 0)) | (np.floor(hgt / (step * 5)) != np.roll(np.floor(hgt / (step * 5)), 1, 1)))
idx = idx | np.roll(idx, 1, 0) | np.roll(idx, 1, 1); a[idx & inside] = R
img.paste(Image.fromarray(a))

# --- brook and tributaries
brook = [(sx(y), y) for y in range(T, Bm, 3)]
d.line(brook, fill=B, width=3)
def trib(x0, y0, y1, side):
    pts = []; x = x0
    for y in range(y0, y1, 3):
        t = (y - y0) / (y1 - y0); x = x0 + (sx(y1) - x0) * t ** 1.6 + 8 * math.sin(y / 11) * (1 - t)
        pts.append((x, y))
    d.line(pts, fill=B, width=2); return pts
trib(40, 60, 250, 1); trib(370, 210, 400, -1); trib(60, 380, 520, 1)

# --- dams and ponds
dams = [(150, 96, 44, "Upper Pond"), (318, 132, 60, "Long Pond"), (482, 104, 52, "Old Pond")]
ponds = np.zeros((H, W), bool)
for (yd, Ln, wm, name) in dams:
    for y in range(yd - Ln, yd + 1):
        t = (y - (yd - Ln)) / Ln; hw = wm * t ** 0.55 * (0.8 + 0.5 * n2[y, int(sx(y))]) + 2
        x0 = sx(y) - hw * (0.8 + 0.6 * n2[y, 40]); x1 = sx(y) + hw * (0.8 + 0.6 * n2[y, 360])
        ponds[y, int(max(x0, L)):int(min(x1, Rt))] = True
ponds &= inside
shore = ponds & ~(np.roll(ponds, 1, 0) & np.roll(ponds, -1, 0) & np.roll(ponds, 1, 1) & np.roll(ponds, -1, 1))
ring = np.zeros_like(ponds)
for sh in range(-5, 6):
    for ax in (0, 1): ring |= np.roll(ponds, sh, ax)
marsh = ring & ~ponds & inside
tone(img, marsh, Wh, G, 0.25)
a = np.asarray(img).copy(); a[ponds] = B; img.paste(Image.fromarray(a))
tone(img, ponds & ((YY % 4) == 0), None, Wh, 0.45)             # water lining
a = np.asarray(img).copy(); a[shore] = K; img.paste(Image.fromarray(a))
for _ in range(260):                                            # marsh tufts
    x, y = rng.randrange(L, Rt), rng.randrange(T, Bm)
    if marsh[y, x] or (ring[y, x] and not ponds[y, x]):
        d.line((x - 2, y, x + 2, y), fill=B); d.line((x, y - 1, x, y - 3), fill=G); d.line((x - 2, y - 1, x - 3, y - 3), fill=G); d.line((x + 2, y - 1, x + 3, y - 3), fill=G)

# --- canals, felled patches, stumps
felled = []
def canal(x0, y0, ang, Ln):
    pts = [(x0, y0)]; x, y = x0, y0
    for k in range(int(Ln / 4)):
        ang2 = ang + 0.35 * math.sin(k / 2.5 + x0); x += 4 * math.cos(ang2); y += 4 * math.sin(ang2); pts.append((x, y))
    d.line(pts, fill=B); d.line([(px + 1, py) for px, py in pts], fill=B)
    felled.append((x, y))
for (yd, Ln, wm, name) in dams:
    cx0 = sx(yd - Ln * 0.45)
    canal(cx0 - wm * 0.7, yd - Ln * 0.5, math.pi + 0.3, 46); canal(cx0 + wm * 0.7, yd - Ln * 0.4, -0.35, 52)
    canal(cx0 + wm * 0.5, yd - Ln * 0.75, -0.9, 34)
for (fx, fy) in felled:
    cl = ell_mask(fx, fy, 24, 17) & inside & ~ponds
    tone(img, cl, Wh, Y, 0.3)
    for _ in range(26):
        x = fx + rng.gauss(0, 10); y = fy + rng.gauss(0, 7)
        if 0 <= int(y) < H and 0 <= int(x) < W and cl[int(y), int(x)]:
            d.ellipse((x - 2, y - 2, x + 1, y + 1), fill=Y, outline=K)
            if rng.random() < 0.4: d.line((x + 2, y, x + 8, y + rng.uniform(-3, 3)), fill=K)     # the log, where it fell

# --- trees: spruce on the heights, aspen in the valley
a0 = np.asarray(img)
for gy in range(T + 5, Bm - 4, 9):
    for gx in range(L + 5, Rt - 4, 9):
        x = gx + rng.randint(-3, 3); y = gy + rng.randint(-3, 3)
        if not (L + 4 < x < Rt - 4 and T + 6 < y < Bm - 4): continue
        if ponds[y, x] or ring[y, x] or tuple(a0[y, x]) == B: continue
        if any((x - fx) ** 2 / 576 + (y - fy) ** 2 / 289 < 1 for fx, fy in felled): continue
        if forest[y, x]:
            if hgt[y, x] > 0.62 + 0.2 * n2[y, x]:
                d.polygon([(x, y - 5), (x - 3, y + 2), (x + 3, y + 2)], fill=G, outline=K); d.point((x, y + 3), fill=K)
            else:
                c = Y if n2[y, x] > 0.45 else R
                d.ellipse((x - 3, y - 3, x + 2, y + 2), fill=c, outline=K)
        elif rng.random() < 0.10:
            d.ellipse((x - 2, y - 2, x + 1, y + 1), fill=Y, outline=K)

# --- dams, lodges, names
fi = font("DejaVu Serif:italic", 10); fs = font("DejaVu Sans", 8); fb = font("DejaVu Sans:bold", 8)
def label(x, y, s, f=fi, col=K, halo=Wh):
    w = d.textlength(s, font=f)
    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)): d.text((x - w / 2 + dx, y + dy), s, font=f, fill=halo)
    d.text((x - w / 2, y), s, font=f, fill=col)
for (yd, Ln, wm, name) in dams:
    xs = [x for x in range(L, Rt) if ponds[yd - 1, x]]; x0, x1 = min(xs) - 4, max(xs) + 4
    pts = [(x, yd + 1 + 5 * math.sin(math.pi * (x - x0) / (x1 - x0))) for x in range(x0, x1 + 1, 2)]
    d.line(pts, fill=K, width=4)
    for (x, y) in pts[::3]: d.line((x, y + 2, x, y + 6), fill=R)
    lx, ly = sx(yd - Ln * 0.35) + wm * 0.25, yd - Ln * 0.33
    d.ellipse((lx - 6, ly - 5, lx + 6, ly + 5), fill=Wh, outline=K); d.pieslice((lx - 4, ly - 4, lx + 4, ly + 6), 180, 360, fill=R, outline=K)
    label(sx(yd - Ln * 0.62), yd - Ln * 0.66, name, fi, K)
label(84, 300, "Aspen Flat"); label(318, 96, "Spruce Knoll"); label(322, 430, "Alder Carr"); label(70, 560, "to the river", fi, B)
# --- a footpath and the watcher's hide
path = [(L, 262 + 10 * math.sin(L / 30))] + [(x, 262 + 14 * math.sin(x / 34) + 0.05 * (x - 200)) for x in range(L, Rt, 6)]
for i in range(0, len(path) - 1, 2):
    (x0, y0), (x1, y1) = path[i], path[i + 1]
    if not ponds[int(y0), int(x0)]: d.line((x0, y0, x1, y1), fill=K, width=2)
d.rectangle((300, 268, 307, 275), fill=K); d.line((298, 268, 303.5, 263, 309, 268), fill=K); label(322, 277, "hide", fs)

# --- sheet furniture: chequered border, cartouche, key, scale, north
a = np.asarray(img).copy(); a[~inside] = Wh; img.paste(Image.fromarray(a))
d.rectangle((L, T, Rt - 1, Bm - 1), outline=K); d.rectangle((L - 6, T - 6, Rt + 5, Bm + 5), outline=K); d.rectangle((L - 9, T - 9, Rt + 8, Bm + 8), outline=K)
for i, x in enumerate(range(L, Rt, 23)):
    if i % 2 == 0: d.rectangle((x, T - 5, min(x + 22, Rt - 1), T - 1), fill=K); d.rectangle((x, Bm, min(x + 22, Rt - 1), Bm + 4), fill=K)
for i, y in enumerate(range(T, Bm, 23)):
    if i % 2 == 0: d.rectangle((L - 5, y, L - 1, min(y + 22, Bm - 1)), fill=K); d.rectangle((Rt, y, Rt + 4, min(y + 22, Bm - 1)), fill=K)
d.rectangle((24, 24, 190, 76), fill=Wh, outline=K); d.rectangle((27, 27, 187, 73), outline=K)
spaced(d, 107, 30, "BEAVER BROOK", font("DejaVu Serif:bold", 13), K, gap=2)
s = "a valley re-engineered"; d.text((107 - d.textlength(s, font=fi) / 2, 46), s, font=fi, fill=R)
s = "surveyed at the full moon, 24 XI"; d.text((107 - d.textlength(s, font=fs) / 2, 60), s, font=fs, fill=K)
kx, ky = 262, 478
d.rectangle((kx, ky, 376, 576), fill=Wh, outline=K); d.text((kx + 6, ky + 4), "KEY", font=fb, fill=K); d.line((kx + 6, ky + 15, 370, ky + 15), fill=K)
rows = ["dam", "lodge", "canal", "stump", "aspen", "spruce"]
for i, t in enumerate(rows):
    y = ky + 20 + i * 12; x = kx + 14
    if i == 0: d.line((x - 7, y + 4, x + 7, y + 4), fill=K, width=3); d.line((x - 4, y + 6, x - 4, y + 8), fill=R); d.line((x + 3, y + 6, x + 3, y + 8), fill=R)
    if i == 1: d.pieslice((x - 4, y, x + 4, y + 10), 180, 360, fill=R, outline=K)
    if i == 2: d.line((x - 7, y + 6, x - 2, y + 3, x + 3, y + 6, x + 7, y + 4), fill=B, width=2)
    if i == 3: d.ellipse((x - 2, y + 2, x + 1, y + 5), fill=Y, outline=K); d.line((x + 2, y + 4, x + 7, y + 3), fill=K)
    if i == 4: d.ellipse((x - 3, y + 1, x + 2, y + 6), fill=Y, outline=K)
    if i == 5: d.polygon([(x, y), (x - 3, y + 7), (x + 3, y + 7)], fill=G, outline=K)
    d.text((kx + 30, y), t, font=fs, fill=K)
d.rectangle((24, 548, 150, 576), fill=Wh, outline=K)
for i in range(4): d.rectangle((32 + i * 20, 566, 52 + i * 20, 570), fill=K if i % 2 == 0 else Wh, outline=K)
d.text((32, 553), "0", font=fs, fill=K); d.text((101, 553), "200 m", font=fs, fill=K)
nx, ny = 136, 562
d.polygon([(nx, ny - 11), (nx - 5, ny + 9), (nx, ny + 5)], fill=K); d.polygon([(nx, ny - 11), (nx + 5, ny + 9), (nx, ny + 5)], fill=Wh, outline=K)
save(img)
