"""Midday — Carte de l'arc du méridien, Torne valley 1736-37 (the expedition Celsius joined)."""
import math, random
from kit import *
rnd = random.Random(1736)
img, d = canvas(WH)

def rx(y):  # the river's course
    return 212 + 26 * math.sin(y / 58 + 0.6) + 9 * math.sin(y / 21) + (y - 300) * 0.03
def coast(x):
    return 482 + 9 * math.sin(x / 47 + 1) + 4 * math.sin(x / 15) + 14 * math.exp(-((x - rx(480)) / 16) ** 2)

# ---------- sea ----------
sea = [(18, coast(18))] + [(x, coast(x)) for x in range(18, 383, 3)] + [(382, 582), (18, 582)]
land_edge = [(x, coast(x)) for x in range(18, 383, 3)]
poly(d, sea, B)
for k, off in enumerate((4, 9, 15)):       # coastal water-lining
    pts = [(x, coast(x) + off) for x in range(18, 383, 3)]
    for i in range(0, len(pts) - 1, 1 + k):
        line(d, pts[i:i + 2], WH, 0.6)
for i in range(120):                        # wave marks
    x = rnd.uniform(22, 378); y = rnd.uniform(505, 578)
    line(d, [(x, y), (x + 3, y - 1.5), (x + 6, y)], WH, 0.6)
line(d, land_edge, K, 1.2)
# yellow wash inside the coast
for off in (2.5, 4.5):
    line(d, [(x, y - off) for x, y in land_edge], Y, 1.6)
# islands
for ix, iy, a, b in [(322, 508, 10, 4), (118, 566, 9, 4), (356, 530, 8, 3.5), (290, 572, 7, 3)]:
    ell(d, ix, iy, a + 2, b + 2, fill=WH); ell(d, ix, iy, a, b, fill=Y, outline=K, w=0.8); ell(d, ix, iy, a - 3, b - 2, fill=WH)

# ---------- river and tributaries ----------
def river(pts_w, col=B):
    for (x0, y0, w0), (x1, y1, w1) in zip(pts_w, pts_w[1:]):
        line(d, [(x0, y0), (x1, y1)], K, w0 + 1.4)
    for (x0, y0, w0), (x1, y1, w1) in zip(pts_w, pts_w[1:]):
        line(d, [(x0, y0), (x1, y1)], col, w0)
    for (x, y, w) in pts_w: circ(d, x, y, w / 2, fill=col)
main = [(rx(y), y, 2.2 + (y - 18) / 480 * 6) for y in range(18, 497, 4)]
trib = lambda x0, y0, x1, n, wig: [(x0 + (x1 - x0) * i / n, y0 - abs(x1 - x0) * 0.35 * (i / n) + wig * math.sin(i * 0.9), 2.4 - 1.6 * i / n) for i in range(n + 1)]
tribs = [trib(rx(292), 292, 380, 26, 4), trib(rx(196), 196, 20, 30, 5), trib(rx(380), 380, 382, 22, 3), trib(rx(120), 120, 382, 24, 5), trib(rx(430), 430, 20, 26, 3)]
for t in tribs: river(t)
river(main)
lakes = [(322, 250, 16, 8), (70, 150, 13, 6), (330, 92, 18, 7), (64, 392, 12, 6), (318, 350, 9, 5)]
for lx, ly, a, b in lakes:
    ell(d, lx, ly, a, b, fill=B, outline=K, w=0.8); line(d, [(lx - a * 0.5, ly), (lx + a * 0.4, ly)], WH, 0.6)

# ---------- stations of the triangulation ----------
ST = {"Torneå": (rx(468) - 6, 468), "Niwa": (rx(410) - 58, 412), "Kakama": (rx(388) + 44, 386),
      "Cuitaperi": (rx(335) - 50, 334), "Avasaxa": (rx(288) + 30, 284), "Horrilakero": (rx(262) - 96, 258),
      "Pullingi": (rx(226) - 38, 222), "Niemi": (rx(170) + 46, 170), "Kittis": (rx(96) - 16, 92)}
TRI = [("Torneå", "Niwa", "Kakama"), ("Niwa", "Kakama", "Cuitaperi"), ("Kakama", "Cuitaperi", "Avasaxa"),
       ("Cuitaperi", "Avasaxa", "Pullingi"), ("Cuitaperi", "Horrilakero", "Pullingi"), ("Avasaxa", "Pullingi", "Niemi"),
       ("Pullingi", "Niemi", "Kittis")]

occupied = []   # (x, y, r) circles trees must avoid
def hill(x, y, r, shade=True):
    occupied.append((x, y, r + 5))
    arc = [(x - r + 2 * r * i / 16, y - r * 0.75 * math.sin(math.pi * i / 16) ** 0.8) for i in range(17)]
    poly(d, arc, WH); poly(d, arc[2:9] + [(x, y)], Y)
    line(d, arc, K, 1)
    for i in range(1, 16):
        ax, ay = arc[i]; f = i / 16
        ln = (2.5 + 5 * f) if shade else 3
        line(d, [(ax, ay + 1), (ax + (f - 0.5) * 3, ay + 1 + ln)], K, 0.5 if f < 0.5 else 0.8)
# background hills (east and west fells)
for _ in range(70):
    x = rnd.choice([rnd.uniform(26, 120), rnd.uniform(290, 374)]); y = rnd.uniform(40, 450)
    if abs(x - rx(y)) < 40 or any(abs(x - sx) < 22 and abs(y - sy) < 16 for sx, sy in ST.values()): continue
    if x < 160 and y < 130: continue
    if x > 300 and 380 < y < 470: continue
    if any((x - ox) ** 2 + (y - oy) ** 2 < (orad + 9) ** 2 for ox, oy, orad in occupied): continue
    hill(x, y, rnd.uniform(9, 15))
for n, (x, y) in ST.items():
    if n != "Torneå": hill(x, y + 6, 15)

# forest: little spruces, kept clear of water, hills, cartouche
def clear(x, y):
    if abs(x - rx(y)) < 9 or y > coast(x) - 9: return False
    if x < 164 and y < 126: return False
    if x > 318 and 372 < y < 476: return False
    if any((x - ox) ** 2 + (y - oy) ** 2 < orad ** 2 for ox, oy, orad in occupied): return False
    if any(((x - lx) / (a + 5)) ** 2 + ((y - ly) / (b + 5)) ** 2 < 1 for lx, ly, a, b in lakes): return False
    return True
pts = []
for _ in range(9000):
    x = rnd.uniform(24, 376); y = rnd.uniform(24, 478)
    dens = 0.5 + 0.5 * math.sin(x / 40 + 1) * math.sin(y / 55)
    if rnd.random() > 0.35 + 0.65 * dens: continue
    if clear(x, y) and all((x - px) ** 2 + (y - py) ** 2 > 60 for px, py in pts): pts.append((x, y))
for x, y in sorted(pts, key=lambda p: p[1]):
    line(d, [(x, y), (x, y - 2)], K, 0.7)
    poly(d, [(x - 2.2, y - 1.5), (x, y - 6.5), (x + 2.2, y - 1.5)], G)
# marsh marks
for _ in range(46):
    x = rnd.uniform(30, 370); y = rnd.uniform(130, 470)
    if clear(x, y) and clear(x + 8, y):
        for k in range(3): line(d, [(x + k, y + k * 2), (x + 8 - k, y + k * 2)], B, 0.6)

# ---------- Arctic Circle, meridian ----------
for x in range(20, 380, 9):
    y = 208 + 4 * math.sin(x / 120)
    line(d, [(x, y), (x + 5, y + 0.1)], K, 1)
mx = ST["Torneå"][0]
for y in range(20, 580, 10):
    line(d, [(mx, y), (mx, y + 6)], K, 0.6); circ(d, mx, y + 8, 0.5, fill=K)

# ---------- triangles ----------
for a, b, c in TRI:
    for p, q in ((a, b), (b, c), (c, a)):
        line(d, [ST[p], ST[q]], R, 1.5)
for n, (x, y) in ST.items():
    poly(d, [(x - 4.5, y + 3.5), (x, y - 5), (x + 4.5, y + 3.5)], WH, R, 1.2); circ(d, x, y + 0.5, 1.1, fill=K)
# base measured on the river ice
b0 = (rx(318) , 318); b1 = (rx(262), 262)
line(d, [b0, b1], K, 3.2)
for i in range(6):
    if i % 2 == 0:
        p = (b0[0] + (b1[0] - b0[0]) * i / 6, b0[1] + (b1[1] - b0[1]) * i / 6); q = (b0[0] + (b1[0] - b0[0]) * (i + 1) / 6, b0[1] + (b1[1] - b0[1]) * (i + 1) / 6)
        line(d, [p, q], WH, 1.6)
# Torneå: church and town
tx, ty = ST["Torneå"]
for k in range(7):
    hx = tx + 10 + (k % 4) * 6; hy = ty - 6 + (k // 4) * 7
    rect(d, hx, hy, hx + 4, hy + 4, fill=R, outline=K, w=0.5)
rect(d, tx - 16, ty - 5, tx - 6, ty + 3, fill=R, outline=K, w=0.6); poly(d, [(tx - 17, ty - 5), (tx - 11, ty - 10), (tx - 5, ty - 5)], K)
rect(d, tx - 19, ty - 11, tx - 15, ty + 3, fill=WH, outline=K, w=0.6); poly(d, [(tx - 20, ty - 11), (tx - 17, ty - 22), (tx - 14, ty - 11)], K)
# hamlets along the river
for y in (430, 356, 300, 240, 190, 140, 60):
    x = rx(y) + rnd.choice([-12, 12])
    for k in range(3): rect(d, x + k * 5 - 6, y + (k % 2) * 3, x + k * 5 - 3, y + 3 + (k % 2) * 3, fill=R, outline=K, w=0.4)
# Sami tents + reindeer & pulka
def kata(x, y):
    poly(d, [(x - 6, y), (x, y - 10), (x + 6, y)], Y, K, 0.8); line(d, [(x - 2, y - 12), (x + 2, y - 7)], K, 0.6); line(d, [(x + 2, y - 12), (x - 2, y - 7)], K, 0.6)
    poly(d, [(x - 1.5, y), (x, y - 4), (x + 1.5, y)], K)
for kx, ky in [(52, 262), (64, 268), (340, 180)]:
    occupied.append((kx, ky, 8)); kata(kx, ky)
def reindeer(x, y, sc=1.0):
    ell(d, x, y, 7 * sc, 3.2 * sc, fill=K)
    for lx in (-5, -3, 3.5, 5.5): line(d, [(x + lx * sc, y + 2), (x + (lx + (0.8 if lx > 0 else -0.8)) * sc, y + 8 * sc)], K, 0.9)
    line(d, [(x + 6 * sc, y - 1), (x + 9 * sc, y - 6 * sc)], K, 2); ell(d, x + 10.5 * sc, y - 6.5 * sc, 2.6 * sc, 1.6 * sc, fill=K)
    for a in (-0.3, 0.4):
        bx, by = x + 9.5 * sc, y - 8 * sc
        line(d, [(bx, by), (bx - 2 + a * 4, by - 5 * sc), (bx - 4 + a * 6, by - 8 * sc)], K, 0.7); line(d, [(bx - 2 + a * 4, by - 5 * sc), (bx + 1 + a * 4, by - 8 * sc)], K, 0.7)
rex, rey = 86, 462
reindeer(rex, rey)
line(d, [(rex - 7, rey), (rex - 22, rey + 4)], K, 0.6)
poly(d, [(rex - 38, rey + 2), (rex - 22, rey + 2), (rex - 19, rey + 6), (rex - 36, rey + 7)], R, K, 0.7); circ(d, rex - 31, rey - 1, 2.5, fill=K); rect(d, rex - 33, rey + 1, rex - 29, rey + 4, fill=B)

# ---------- ship ----------
sx, sy = 316, 548
poly(d, [(sx - 16, sy), (sx + 18, sy), (sx + 13, sy + 7), (sx - 12, sy + 7)], K, WH, 0.6)
line(d, [(sx - 4, sy), (sx - 4, sy - 26)], WH, 1); line(d, [(sx + 8, sy), (sx + 8, sy - 20)], WH, 1)
poly(d, [(sx - 13, sy - 5), (sx - 5, sy - 24), (sx - 5, sy - 5)], WH); poly(d, [(sx - 3, sy - 4), (sx - 3, sy - 22), (sx + 6, sy - 13), (sx + 6, sy - 4)], WH)
poly(d, [(sx + 9, sy - 4), (sx + 9, sy - 18), (sx + 17, sy - 4)], WH); poly(d, [(sx - 4, sy - 26), (sx + 3, sy - 28), (sx - 4, sy - 30)], Y)

# ---------- compass rose ----------
cx, cy = 62, 540
circ(d, cx, cy, 25, fill=WH, outline=K, w=1); circ(d, cx, cy, 21, outline=K, w=0.6)
for i in range(32):
    a = i * math.pi / 16; line(d, [(cx + 21 * math.cos(a), cy + 21 * math.sin(a)), (cx + 25 * math.cos(a), cy + 25 * math.sin(a))], K, 0.6)
for i in range(8):
    a = i * math.pi / 4 + math.pi / 8; r = 13
    poly(d, [(cx, cy), (cx + 3 * math.cos(a - 1.2), cy + 3 * math.sin(a - 1.2)), (cx + r * math.cos(a), cy + r * math.sin(a))], K)
for i in range(4):
    a = i * math.pi / 2 + math.pi / 4; r = 17
    tip = (cx + r * math.cos(a), cy + r * math.sin(a))
    poly(d, [(cx, cy), (cx + 4 * math.cos(a - 1.3), cy + 4 * math.sin(a - 1.3)), tip], Y, K, 0.5); poly(d, [(cx, cy), (cx + 4 * math.cos(a + 1.3), cy + 4 * math.sin(a + 1.3)), tip], K)
for i in range(4):
    a = i * math.pi / 2 - math.pi / 2; r = 30 if i == 0 else 23
    tip = (cx + r * math.cos(a), cy + r * math.sin(a))
    poly(d, [(cx, cy), (cx + 5 * math.cos(a - 1.25), cy + 5 * math.sin(a - 1.25)), tip], R if i == 0 else WH, K, 0.6); poly(d, [(cx, cy), (cx + 5 * math.cos(a + 1.25), cy + 5 * math.sin(a + 1.25)), tip], K)
circ(d, cx, cy, 2, fill=Y, outline=K, w=0.5)

# ---------- cartouche ----------
rect(d, 24, 24, 162, 124, fill=WH, outline=K, w=1.2); rect(d, 27, 27, 159, 121, outline=R, w=0.8); rect(d, 30, 30, 156, 118, outline=K, w=0.5)
for (qx, qy) in [(27, 27), (159, 27), (27, 121), (159, 121)]:
    circ(d, qx, qy, 5, fill=Y, outline=K, w=0.8); circ(d, qx, qy, 1.5, fill=K)

# ---------- thermometer as the scale ("échelle"), Celsius' own: 0 boils, 100 freezes ----------
ex, ey = 326, 380
rect(d, ex, ey, ex + 50, ey + 88, fill=WH, outline=K, w=1); rect(d, ex + 2.5, ey + 2.5, ex + 47.5, ey + 85.5, outline=B, w=0.6)
tcx = ex + 16; top, bot = ey + 16, ey + 68
rect(d, tcx - 2, top - 4, tcx + 2, bot + 3, fill=WH, outline=K, w=0.7)
rect(d, tcx - 1, bot - 0.0 - (bot - top) * 0.0, tcx + 1, bot + 3, fill=R)
rect(d, tcx - 1, top + (bot - top) * 1.08 - 6, tcx + 1, bot + 3, fill=R)
circ(d, tcx, bot + 8, 5, fill=R, outline=K, w=0.8)
for i in range(21):
    yv = top + (bot - top) * i / 20
    line(d, [(tcx + 3.5, yv), (tcx + (8 if i % 5 == 0 else 5.5), yv)], K, 0.6)

# ---------- scale bar in toises ----------
bx, by = 150, 566
for i in range(5):
    rect(d, bx + i * 22, by, bx + (i + 1) * 22, by + 5, fill=K if i % 2 == 0 else WH, outline=K, w=0.6)
rect(d, bx - 4, by - 14, bx + 114, by + 9, outline=None)

# ---------- neatline ----------
rect(d, 0, 0, 400, 18, fill=WH); rect(d, 0, 582, 400, 600, fill=WH); rect(d, 0, 0, 18, 600, fill=WH); rect(d, 382, 0, 400, 600, fill=WH)
rect(d, 6, 6, 394, 594, outline=K, w=1.6); rect(d, 10, 10, 390, 590, outline=K, w=0.6); rect(d, 17, 17, 383, 583, outline=K, w=1)
n = 0
for x in range(17, 383, 12):
    if n % 2 == 0: rect(d, x, 10.5, min(x + 12, 383), 16.5, fill=K); rect(d, x, 583.5, min(x + 12, 383), 589.5, fill=K)
    n += 1
n = 0
for y in range(17, 583, 12):
    if n % 2 == 1: rect(d, 10.5, y, 16.5, min(y + 12, 583), fill=K); rect(d, 383.5, y, 389.5, min(y + 12, 583), fill=K)
    n += 1
for (qx, qy) in [(13.5, 13.5), (386.5, 13.5), (13.5, 586.5), (386.5, 586.5)]:
    rect(d, qx - 3.5, qy - 3.5, qx + 3.5, qy + 3.5, fill=R, outline=K, w=0.6)

# ---------- lettering at 1x ----------
def post(p, out):
    def lab(x, y, t, f, fill=K, anchor="la", halo=WH):
        if halo:
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    p.text((x + dx, y + dy), t, font=f, fill=halo, anchor=anchor)
        p.text((x, y), t, font=f, fill=fill, anchor=anchor)
    fi = font("serifi", 12); fb = font("serifb", 11); fs = font("sans", 8); fsb = font("serifb", 9)
    lab(93, 36, "CARTE", font("serifb", 15), anchor="ma", halo=None)
    lab(93, 54, "de l'Arc du Méridien", font("serifi", 13), anchor="ma", halo=None)
    lab(93, 67, "mesuré au Cercle Polaire", font("serifi", 12), anchor="ma", halo=None)
    lab(93, 80, "par MM. de Maupertuis,", font("serifi", 11), anchor="ma", halo=None)
    lab(93, 92, "Celsius, Clairaut &c.", font("serifi", 11), anchor="ma", halo=None)
    lab(93, 106, "1736 – 1737", font("serifb", 9), fill=R, anchor="ma", halo=None)
    off = {"Torneå": (-22, 6, "ra"), "Niwa": (-7, -4, "ra"), "Kakama": (7, -4, "la"), "Cuitaperi": (-7, -5, "ra"), "Avasaxa": (7, -6, "la"),
           "Horrilakero": (-2, -18, "ma"), "Pullingi": (-7, -14, "ra"), "Niemi": (7, -5, "la"), "Kittis": (8, -12, "la")}
    for n, (x, y) in ST.items():
        dx, dy, an = off[n]
        lab(round(x + dx), round(y + dy), n.upper() if n == "Torneå" else n, fb if n == "Torneå" else fi, anchor=an)
    lab(374, 196, "CERCLE POLAIRE", fsb, anchor="ra")
    lab(40, 196, "66° 32'", fs)
    lab(200, 508, "GOLFE  DE  BOTHNIE", font("serifb", 11), fill=WH, anchor="ma", halo=B)
    lab(205, 530, "1° = 57 437 toises", font("serifi", 11), fill=Y, anchor="ma", halo=B)
    lab(205, 543, "la Terre est aplatie aux pôles", font("serifi", 11), fill=WH, anchor="ma", halo=B)
    lab(205, 555, "Échelle de 10 000 toises", fs, fill=WH, anchor="ma", halo=B)
    lab(62, 500, "N", font("serifb", 10), fill=WH, anchor="ma", halo=B)
    lab(ex + 26, ey + 5, "0", fs, halo=None); lab(ex + 26, ey + 37, "50", fs, halo=None); lab(ex + 26, ey + 63, "100", fs, halo=None)
    lab(round(rx(150)) + 8, 146, "Torne", font("serifi", 11), fill=B)
    lab(round(b0[0]) + 6, 304, "Base", font("serifi", 11))
finish(img, post, ink=(K, R))
