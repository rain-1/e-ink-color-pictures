# Midday — "Treasure Island". A sea-chart after the one Stevenson drew for his stepson in
# 1881 and then wrote a book to explain. Coast-lines, rhumbs, hachured hills, woods tree by
# tree, the swamp, the stockade, three red crosses. Full palette on white paper.
import math, random
import numpy as np
from kit import *
random.seed(1881); rng = np.random.default_rng(1881)
c = Canvas(WH)

# ---- the island ------------------------------------------------------------------
coast = [(190,150),(214,156),(224,182),(216,204),(226,214),(242,190),(262,172),(290,190),(305,225),
         (298,262),(313,295),(320,335),(302,360),(274,366),(254,383),(250,406),(266,424),(264,450),
         (238,470),(206,463),(180,441),(150,426),(125,396),(108,360),(97,320),(112,286),(104,250),
         (125,215),(150,196),(165,166)]
pts = smooth(coast, n=10)
pts = [(x + random.uniform(-1.6, 1.6), y + random.uniform(-1.6, 1.6)) for x, y in pts]
skel = [(290 + (13 + 3 * math.sin(3 * a)) * math.cos(a), 402 + (10 + 2 * math.cos(2 * a)) * math.sin(a))
        for a in [i * math.pi / 12 for i in range(24)]]
rocks = [(84,236,4),(78,246,2.5),(330,180,3),(338,172,2),(222,488,3),(300,440,2.5)]
L = c.layer()
L.poly(pts); L.poly(skel)
for x, y, r in rocks: L.circle(x, y, r)
land = L.mask()
sea = ~land
dsea = depth(sea, 30)

# rhumb lines from two centres, dotted, kept off the land and the coast shading
CR = (80, 512)
rl = c.layer(1)
for cx, cy in (CR, (352, 262)):
    for i in range(32 if cx < 200 else 16):
        a = math.pi * i / 16
        rl.seg(cx, cy, cx + 800 * math.cos(a), cy + 800 * math.sin(a))
c.put(rl.mask() & (dsea >= 28) & ((XX - 352) ** 2 + (YY - 262) ** 2 > 144), K, checker(2))
c.poly(star(352, 262, 9, 2.5, 8), K); c.poly(star(352, 262, 5, 1.5, 4), Y)

# coast lines: closer together near the shore, like an engraver's sea
for d, col in ((2, B), (3, B), (6, B), (10, B), (15, B), (21, B), (27, B)):
    pat = None if d < 12 else (hatch(0, 5, 4) if d < 22 else hatch(0, 4, 2))
    c.put(dsea == d, col, pat)

# land: sand rim, then outline
dl = depth(land, 8)
c.put(land, WH)
c.put(land & (dl <= 4), Y)
c.put(land & (dl == 5), Y, checker(1))
c.put(land & (dl == 1), K)

# ---- labels are reserved first so the woods grow around them ----------------------
labels = [  # x, y, text, font, size, angle, colour
    (158, 300, "Spye-glass", "lib-i", 13, 0, K), (160, 313, "Hill", "lib-i", 13, 0, K),
    (247, 240, "Foremast Hill", "lib-i", 12, 0, K), (190, 438, "Mizzenmast Hill", "lib-i", 12, 0, K),
    (283, 312, "Swamp", "lib-i", 12, 0, B), (163, 226, "Bulk of treasure", "lib-i", 12, 0, R),
    (163, 238, "here", "lib-i", 12, 0, R), (279, 346, "Stockade", "lib-i", 12, 0, K),
    (128, 362, "Cape of", "lib-i", 12, 0, K), (134, 374, "ye Woods", "lib-i", 12, 0, K),
]
res = c.layer()
reserved = np.zeros((H, W), bool)
for x, y, t, f, sz, an, col in labels: reserved |= c.tmask(x, y, t, f, sz, "mm", an)
reserved = grow(reserved, 6)

# streams
for path in ([(170,282),(196,300),(214,330),(236,352),(252,384)], [(176,270),(196,246),(210,224),(220,208)],
             [(262,296),(280,320),(300,345),(304,360)]):
    c.line(smooth(path, closed=False), B, 1.3)

# hills: two rings of hachures falling away from a bare top
def hill(cx, cy, rx, ry, rings=3, top=None):
    Lh = c.layer()
    for k in range(rings):
        f0, f1 = 0.34 + 0.24 * k, 0.52 + 0.24 * k
        n = int(26 + 16 * k)
        for i in range(n):
            a = 2 * math.pi * (i + 0.5 * (k % 2)) / n + random.uniform(-0.05, 0.05)
            j = random.uniform(-0.04, 0.04)
            Lh.seg(cx + rx * (f0 + j) * math.cos(a), cy + ry * (f0 + j) * math.sin(a),
                   cx + rx * (f1 + j) * math.cos(a), cy + ry * (f1 + j) * math.sin(a), 1.0 if k else 1.3)
    m = Lh.mask(0.3) & land & ~reserved
    c.put(m, K)
    return m
hills = hill(160, 282, 44, 40, 3) | hill(236, 220, 30, 24, 2) | hill(204, 412, 34, 24, 2)
hillzone = c.layer().ellipse(160,282,46,42).ellipse(236,220,32,26).ellipse(204,412,36,26).mask()
# summit marks
for x, y in ((160, 276), (236, 218), (204, 410)):
    c.poly([(x - 4, y + 3), (x, y - 5), (x + 4, y + 3)], K); c.poly([(x - 1.5, y + 2), (x, y - 2), (x + 2, y + 2)], WH)

# swamp: reeds and standing water
swamp = c.layer().poly(smooth([(262,262),(292,270),(304,300),(308,338),(290,352),(270,330),(258,296)])).mask() & land & (dl > 6)
sw = c.layer(1)
for _ in range(400):
    x, y = random.randint(250, 312), random.randint(256, 356)
    sw.seg(x, y, x + random.randint(4, 8), y)
c.put(sw.mask() & swamp & ~reserved, B)
tufts = c.layer(1)
for _ in range(70):
    x, y = random.randint(252, 310), random.randint(258, 354)
    for dx in (-2, 0, 2): tufts.seg(x, y, x + dx, y - 4)
c.put(tufts.mask() & swamp & ~reserved, G)

# woods: every tree drawn. Poisson-ish scatter, sorted north to south so they overlap properly.
stock = c.layer().circle(262, 332, 15).mask()
ok = land & (dl > 6) & ~reserved & ~hillzone & ~swamp & ~stock
trees = []
tries = 0
occ = np.zeros((H, W), bool)
while len(trees) < 330 and tries < 40000:
    tries += 1
    x, y = random.randint(95, 322), random.randint(150, 472)
    if not ok[y, x] or occ[y, x]: continue
    # woods are thick in the west and south, thinner on the east shore
    dens = 0.95 if x < 215 else 0.55
    if random.random() > dens: continue
    trees.append((x, y)); occ[max(0, y - 6):y + 7, max(0, x - 6):x + 7] = True
trees.sort(key=lambda p: p[1])
tk, tg, tw_ = c.layer(), c.layer(), c.layer()
for x, y in trees:
    kind = random.random()
    if kind < 0.7:   # round broadleaf
        r = random.choice((3, 3.5, 4))
        tk.seg(x, y + 1, x, y + 4, 1.2); tk.circle(x, y - 1, r + 1); tg.circle(x, y - 1, r); tw_.circle(x - 1.2, y - 2.2, 1)
    else:            # pine
        tk.seg(x, y + 2, x, y + 4, 1.2); tk.poly([(x - 4.5, y + 2.5), (x, y - 7), (x + 4.5, y + 2.5)]); tg.poly([(x - 3, y + 1.5), (x, y - 5), (x + 3, y + 1.5)])
mt = tk.mask(0.4); c.put(mt & land, K); c.put(tg.mask() & land, G); c.put(tw_.mask(0.6) & land, Y)
# palms along the south beaches
for x, y in ((228,458),(246,452),(196,452),(172,430),(286,398),(294,404),(258,436)):
    c.line([(x, y), (x + 1, y - 8)], K, 1.2)
    for a in (200, 240, 290, 330, 20, 160):
        c.line([(x + 1, y - 8), (x + 1 + 6 * math.cos(math.radians(a)), y - 8 + 4 * math.sin(math.radians(a)) - 1)], G, 1.4)

# stockade: palisade ring, log-house, flag
ps = c.layer()
for i in range(22):
    a = 2 * math.pi * i / 22
    ps.seg(262 + 12 * math.cos(a), 332 + 9 * math.sin(a), 262 + 12 * math.cos(a), 332 + 9 * math.sin(a) - 4, 1.2)
ps.put(K, thr=0.3)
c.poly([(256,329),(268,329),(268,336),(256,336)], K); c.poly([(257,330),(267,330),(267,335),(257,335)], WH)
c.poly([(254,329),(262,323),(270,329)], R); c.hair([(254,329),(262,323),(270,329)], K)
c.hair([(262,323),(262,313)], K); c.poly([(262,313),(270,315),(262,318)], R)
c.put(c.layer(1).rect(261,332,263,336).mask(), K)

# the track from the anchorage to the cache, and the three crosses
route = smooth([(252,392),(240,372),(246,350),(222,338),(206,318),(198,290),(206,262),(190,246),(172,246)], closed=False, n=12)
rt = c.layer()
for i in range(0, len(route) - 1, 3): rt.line(route[i:i + 2], 1.6)
c.put(grow(rt.mask(0.3), 1), WH); rt.put(R, thr=0.3)
def cross_x(x, y, s=5):
    for col, w in ((WH, 5), (R, 2.2)):
        Lx = c.layer(); Lx.seg(x - s, y - s, x + s, y + s, w); Lx.seg(x - s, y + s, x + s, y - s, w); Lx.put(col, thr=0.4)
cross_x(163, 250, 6); cross_x(226, 170, 4); cross_x(122, 338, 4)

# labels on land, with a paper halo
for x, y, t, f, sz, an, col in labels:
    c.text(x, y, t, col, f, sz, "mm", an, halo=WH, hw=2)
# labels at sea
def sealabel(x, y, t, sz=12, an=0, col=K, f="lib-i"):
    c.text(x, y, t, col, f, sz, "mm", an, halo=WH, hw=2)
sealabel(338, 404, "Skeleton I.")
sealabel(334, 432, "Capt. Kidd's"); sealabel(338, 444, "Anchorage")
sealabel(258, 148, "North Inlet"); sealabel(232, 492, "Haulbowline Head")
sealabel(52, 230, "White"); sealabel(52, 242, "Rock")
sealabel(52, 328, "Strong", 12, 0, R); sealabel(52, 340, "tide here", 12, 0, R)
sealabel(356, 208, "Foul", 12, 0, R); sealabel(356, 220, "ground", 12, 0, R)
# soundings
for x, y, n in ((304,418,"5"),(276,386,"3"),(288,426,"7"),(300,462,"12"),(236,170,"4"),(250,164,"6"),(70,290,"18"),(64,380,"22"),
                (84,420,"15"),(140,470,"9"),(340,330,"11"),(350,300,"14"),(345,370,"16"),(120,180,"20"),(180,500,"13"),(330,140,"25")):
    if sea[min(H - 1, y), x]: sealabel(x, y, n, 9, 0, K, "dserif")
# anchor in the anchorage
ax, ay = 276, 402
A = c.layer(); A.seg(ax, ay - 5, ax, ay + 5, 1.2); A.seg(ax - 3, ay - 3, ax + 3, ay - 3, 1.2); A.line(arc(ax, ay + 1, 4.5, 4.5, 10, 170), 1.2); A.ring(ax, ay - 6, 1.6, 0.8)
A.put(K, thr=0.3)

# ---- the Hispaniola, standing in from the north-east -------------------------------
def ship(x, y, s=1.0, flip=1):
    P = lambda px, py: (x + flip * px * s, y + py * s)
    wv = c.layer()
    for k in range(3): wv.line([P(-26 + i * 4, 9 + k * 3 + (1.2 if i % 2 else 0)) for i in range(14 - k * 2)], 1.0)
    wv.put(B, thr=0.3)
    hull = [P(-20, 0), P(22, 0), P(28, -4), P(19, 6), P(-16, 6), P(-22, -5)]
    c.poly(hull, K); c.line([P(-19, 1.5), P(21, 1.5)], Y, 1.2)
    c.line([P(22, -1), P(38, -7)], K, 1.2)                                  # bowsprit
    for mx, top in ((-9, -44), (9, -48)):
        c.line([P(mx, 0), P(mx, top)], K, 1.3)
    sails = [([P(-8, -6), P(-8, -30), P(-24, -8)], WH), ([P(-8, -32), P(-8, -42), P(-19, -32)], WH),   # main gaff + top
             ([P(10, -6), P(10, -32), P(-5, -9)], WH), ([P(10, -34), P(10, -46), P(0, -34)], WH),
             ([P(12, -8), P(11, -40), P(36, -7)], WH), ([P(12, -30), P(11, -46), P(30, -12)], WH)]
    for pl, col in sails:
        c.poly(pl, col); c.line(pl, K, 1.0, closed=True)
    hs = c.layer(1)
    for pl, _ in sails[:4]:
        for t in (0.35, 0.65):
            hs.seg(*(pl[0][0] + (pl[2][0] - pl[0][0]) * t, pl[0][1] + (pl[2][1]-pl[0][1]) * t), *(pl[1][0] + (pl[2][0] - pl[1][0]) * t, pl[1][1] + (pl[2][1]-pl[1][1]) * t))
    hs.put(K, hatch(0, 2, 1))
    c.poly([P(9, -48), P(9, -54), P(0, -51)], R)                             # pennant
    c.hair([P(9, -48), P(9, -55)], K)
ship(338, 118, 0.95, -1)

# a whale, because every old chart keeps one
wx, wy = 330, 506
c.poly(smooth([(wx-24,wy+2),(wx-14,wy-8),(wx+4,wy-9),(wx+16,wy-3),(wx+24,wy-9),(wx+29,wy-13),(wx+27,wy-4),(wx+31,wy+2),(wx+22,wy+1),(wx+8,wy+6),(wx-10,wy+7)]), B)
c.put(c.layer().circle(wx - 15, wy - 2, 1.4).mask(), WH)
c.line([(wx-22,wy+3),(wx-8,wy+4)], WH, 1)
for dx, hgt in ((-4, 12), (0, 16), (4, 11)):
    c.line(bez((wx-10, wy-9), (wx-10, wy-16), (wx-10+dx, wy-9-hgt), (wx-10+dx*2.5, wy-6-hgt*0.6)), B, 1.1)
wv = c.layer()
for k in range(3): wv.line([(wx - 34 + i * 5, wy + 9 + k * 3.5 + (1.5 if i % 2 else 0)) for i in range(14)], 1.0)
wv.put(B, thr=0.3)

# ---- compass rose ------------------------------------------------------------------
cx, cy = CR
c.put(c.layer().circle(cx, cy, 52).mask(), WH)
c.put(c.layer().ring(cx, cy, 46, 1.2).ring(cx, cy, 40, 1).mask(0.3), K)
tk = c.layer()
for i in range(64):
    a = math.pi * i / 32
    tk.seg(cx + 40 * math.cos(a), cy + 40 * math.sin(a), cx + (46 if i % 2 == 0 else 43) * math.cos(a), cy + (46 if i % 2 == 0 else 43) * math.sin(a), 1)
tk.put(K, thr=0.3)
def point(a, r, rb, half, dark, light):
    a = math.radians(a); tip = (cx + r * math.cos(a), cy + r * math.sin(a))
    b1 = (cx + rb * math.cos(a - half), cy + rb * math.sin(a - half)); b2 = (cx + rb * math.cos(a + half), cy + rb * math.sin(a + half))
    c.poly([(cx, cy), b1, tip], dark); c.poly([(cx, cy), b2, tip], light); c.line([(cx, cy), b1, tip, b2], K, 1.0, closed=True)
for i in range(16):
    if i % 2: point(-90 + i * 22.5, 24, 9, math.radians(11.25), B, WH)
for i in range(4): point(-45 + i * 90, 33, 10, math.radians(22.5), Y, WH)
for i in range(4): point(-90 + i * 90, 42, 10, math.radians(45), K if i else R, WH)
c.put(c.layer().circle(cx, cy, 3.2).mask(), K); c.put(c.layer().circle(cx, cy, 1.5).mask(), Y)
for t, a in (("N", -90), ("E", 0), ("S", 90), ("W", 180)):
    rr = 53 if a else 51
    c.text(cx + rr * math.cos(math.radians(a)), cy + rr * math.sin(math.radians(a)), t, K, "lib-b", 12, halo=WH, hw=2)

# ---- cartouche ---------------------------------------------------------------------
x0, y0, x1, y1 = 26, 30, 222, 112
c.put(c.layer().rect(x0 + 3, y0 + 3, x1 + 3, y1 + 3).mask(), K, hatch(45, 3, 1))
c.put(c.layer().rect(x0, y0, x1, y1).mask(), WH)
c.hair([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], K, closed=True)
c.hair([(x0 + 3, y0 + 3), (x1 - 3, y0 + 3), (x1 - 3, y1 - 3), (x0 + 3, y1 - 3)], R, closed=True)
c.text((x0 + x1) / 2, y0 + 20, "Treasure Island", K, "serif-bi", 23)
c.line([(x0 + 22, y0 + 35), (x1 - 22, y0 + 35)], K, 1); c.poly(star((x0 + x1) / 2, y0 + 35, 5, 2, 4), R)
c.text((x0 + x1) / 2, y0 + 48, "Given by above J. F. to Mr W. Bones", K, "lib-i", 12)
c.text((x0 + x1) / 2, y0 + 60, "Maste of ye Walrus, Savannah", K, "lib-i", 12)
c.text((x0 + x1) / 2, y0 + 72, "this twenty July 1754   W. B.", R, "lib-i", 12)

# ---- scale of miles ----------------------------------------------------------------
sx, sy = 236, 548
for i in range(6):
    c.put(c.layer(1).rect(sx + i * 20, sy, sx + i * 20 + 20, sy + 5).mask(), K if i % 2 == 0 else WH)
c.hair([(sx, sy), (sx + 120, sy), (sx + 120, sy + 5), (sx, sy + 5)], K, closed=True)
for i, t in enumerate(("0", "1", "2", "3")): c.text(sx + i * 40, sy - 8, t, K, "dserif", 9)
c.text(sx + 60, sy + 15, "Scale of 3 English Miles", K, "lib-i", 12, halo=WH, hw=2)

# ---- neat-line border with a graduated edge ----------------------------------------
c.put((XX < 8) | (XX >= W - 8) | (YY < 8) | (YY >= H - 8), WH)
inner = (XX >= 14) & (XX < W - 14) & (YY >= 14) & (YY < H - 14)
band = ~inner & (XX >= 8) & (XX < W - 8) & (YY >= 8) & (YY < H - 8)
c.put(band, Y)
grad = ~((XX >= 18) & (XX < W - 18) & (YY >= 18) & (YY < H - 18)) & inner
seg = np.where((YY < 18) | (YY >= H - 18), (XX - 14) // 12, (YY - 14) // 12) % 2 == 0
c.put(grad, WH); c.put(grad & seg, K)
for d in (8, 13, 18):
    c.hair([(d, d), (W - 1 - d, d), (W - 1 - d, H - 1 - d), (d, H - 1 - d)], K, closed=True)
c.save("p2.png")
