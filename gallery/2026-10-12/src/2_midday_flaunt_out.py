"""Flaunt out, O Sea — A Sea Symphony premiered at Leeds on Vaughan Williams' 38th
birthday, 12 Oct 1910. A barque in harbour dressed overall: the signal flags along her
dressing lines spell Whitman's words in the International Code. Key plate below."""
import math, random
from common import *

random.seed(1910)
c = Canvas(Wt)

def ring(cx, cy, r, n=20):
    return [(cx + r * math.cos(2 * math.pi * i / n), cy + r * math.sin(2 * math.pi * i / n)) for i in range(n)]
def saltire(t=0.12):
    return [[(0, 0), (t, 0), (1, 1 - t), (1, 1), (1 - t, 1), (0, t)],
            [(1, 0), (1, t), (t, 1), (0, 1), (0, 1 - t), (1 - t, 0)]]
def cross(t=0.14):
    return [[(0.5 - t, 0), (0.5 + t, 0), (0.5 + t, 1), (0.5 - t, 1)],
            [(0, 0.5 - t), (1, 0.5 - t), (1, 0.5 + t), (0, 0.5 + t)]]
def box(x0, y0, x1, y1): return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
def hstripes(cols): n = len(cols); return [(box(0, i / n, 1, (i + 1) / n), col) for i, col in enumerate(cols)]
def vstripes(cols): n = len(cols); return [(box(i / n, 0, (i + 1) / n, 1), col) for i, col in enumerate(cols)]
SW = [(0, 0), (1, 0), (0.72, 0.5), (1, 1), (0, 1)]
FLAGS = {
    "A": [(box(0, 0, 0.5, 1), Wt), ([(0.5, 0), (1, 0), (0.72, 0.5), (1, 1), (0.5, 1)], B)],
    "B": [(SW, R)],
    "C": hstripes([B, Wt, R, Wt, B]),
    "D": [(box(0, 0, 1, 1), Y), (box(0, 0.25, 1, 0.75), B)],
    "E": hstripes([B, R]),
    "F": [(box(0, 0, 1, 1), Wt), ([(0.5, 0), (1, 0.5), (0.5, 1), (0, 0.5)], R)],
    "G": vstripes([Y, B, Y, B, Y, B]),
    "H": vstripes([Wt, R]),
    "I": [(box(0, 0, 1, 1), Y), (ring(0.5, 0.5, 0.26), K)],
    "J": hstripes([B, Wt, B]),
    "K": vstripes([Y, B]),
    "L": [(box(0, 0, 1, 1), K), (box(0, 0, 0.5, 0.5), Y), (box(0.5, 0.5, 1, 1), Y)],
    "M": [(box(0, 0, 1, 1), B)] + [(p, Wt) for p in saltire()],
    "N": [(box(0, 0, 1, 1), Wt)] + [(box(i / 4, j / 4, (i + 1) / 4, (j + 1) / 4), B) for i in range(4) for j in range(4) if (i + j) % 2 == 0],
    "O": [([(0, 0), (1, 0), (1, 1)], R), ([(0, 0), (1, 1), (0, 1)], Y)],
    "P": [(box(0, 0, 1, 1), B), (box(0.32, 0.3, 0.68, 0.7), Wt)],
    "Q": [(box(0, 0, 1, 1), Y)],
    "R": [(box(0, 0, 1, 1), R)] + [(p, Y) for p in cross(0.1)],
    "S": [(box(0, 0, 1, 1), Wt), (box(0.32, 0.3, 0.68, 0.7), B)],
    "T": vstripes([R, Wt, B]),
    "U": [(box(0, 0, 1, 1), Wt), (box(0, 0, 0.5, 0.5), R), (box(0.5, 0.5, 1, 1), R)],
    "V": [(box(0, 0, 1, 1), Wt)] + [(p, R) for p in saltire()],
    "W": [(box(0, 0, 1, 1), B), (box(0.17, 0.17, 0.83, 0.83), Wt), (box(0.34, 0.34, 0.66, 0.66), R)],
    "X": [(box(0, 0, 1, 1), Wt)] + [(p, B) for p in cross(0.12)],
    "Y": [(box(0, 0, 1, 1), Y)] + [([(a, 0), (a + 0.14, 0), (a + 0.14 - 1, 1), (a - 1, 1)], R) for a in (0.2, 0.48, 0.76, 1.04, 1.32, 1.6)],
    "Z": [([(0, 0), (1, 0), (0.5, 0.5)], Y), ([(1, 0), (1, 1), (0.5, 0.5)], B),
          ([(1, 1), (0, 1), (0.5, 0.5)], R), ([(0, 1), (0, 0), (0.5, 0.5)], K)],
}

def flag(letter, P, ux, uy, h, clip_y=None):
    """P = hoist top; (ux,uy) = fly vector (full width); h = drop."""
    def m(u, v): return (P[0] + u * ux, P[1] + u * uy + v * h)
    for poly, col in FLAGS[letter]:
        # clip Y's stripes to the unit square roughly by clamping u
        pts = [m(min(max(u, 0), 1), v) for u, v in poly]
        c.poly(pts, fill=col)
    out = SW if letter in "AB" else box(0, 0, 1, 1)
    c.poly([m(u, v) for u, v in out], outline=K, width=0.7)

# ---------------- sky
for i in range(60):  # light blue hatched top sky, thinning downward
    y = 4 + i * 3.2
    if random.random() < i / 60: continue
    c.line([(0, y), (400, y)], fill=B, width=0.7)
# cumulus with blue engraved shading
def cumulus(cx, cy, s):
    blobs = [(-1.0, 0.1, 0.55), (-0.45, -0.35, 0.7), (0.25, -0.5, 0.8), (0.9, -0.1, 0.6), (0.2, 0.15, 0.6), (-0.4, 0.2, 0.5)]
    for bx, by, r in blobs:
        c.circle(cx + bx * s, cy + by * s, r * s + 1.4, fill=B)
    for bx, by, r in blobs:
        c.circle(cx + bx * s, cy + by * s, r * s, fill=Wt)
    c.rect(cx - 1.6 * s, cy + 0.42 * s, cx + 1.6 * s, cy + 0.8 * s, fill=Wt)
    c.line([(cx - 1.5 * s, cy + 0.42 * s), (cx + 1.5 * s, cy + 0.42 * s)], fill=B, width=1)
    for k in range(4):
        y = cy + 0.38 * s - k * 3
        c.line([(cx - 1.2 * s + k * 4, y), (cx + 1.1 * s - k * 6, y)], fill=B, width=0.6)
cumulus(70, 70, 34)
cumulus(330, 140, 26)
cumulus(200, 30, 18)

# ---------------- harbour background: distant town, lighthouse
HZ = 330
for i in range(26):
    x = 220 + i * 7
    h = random.choice([10, 14, 18, 12, 22])
    c.rect(x, HZ - h, x + 7, HZ, fill=random.choice([Wt, Y, R, Wt]), outline=K, width=0.6)
    c.poly([(x - 1, HZ - h), (x + 3.5, HZ - h - 5), (x + 8, HZ - h)], fill=R if random.random() < 0.5 else K)
    for wy in range(int(HZ - h + 3), HZ - 2, 5):
        c.rect(x + 2.5, wy, x + 4.5, wy + 2, fill=K)
c.poly([(318, HZ - 22), (322, HZ - 52), (326, HZ - 22)], fill=K)  # church spire
# lighthouse on a mole at left
c.rect(0, HZ - 6, 70, HZ, fill=K)
c.poly([(18, HZ - 6), (22, HZ - 62), (34, HZ - 62), (38, HZ - 6)], fill=Wt, outline=K, width=1)
for k in range(3):
    y0 = HZ - 16 - k * 16
    c.poly([(19 + k * 1.3, y0), (37 - k * 1.3, y0), (36.4 - k * 1.3, y0 - 7), (19.6 + k * 1.3, y0 - 7)], fill=R)
c.rect(21, HZ - 72, 35, HZ - 62, fill=Y, outline=K, width=1)
c.poly([(19, HZ - 72), (28, HZ - 82), (37, HZ - 72)], fill=K)

# ---------------- sea
c.rect(0, HZ, 400, 448, fill=B)
y = HZ + 3
while y < 446:
    d = (y - HZ) / 118
    x = random.uniform(-10, 0)
    while x < 400:
        L = 3 + d * 14
        c.line([(x, y), (x + L, y)], fill=Wt, width=0.6 + d * 0.8)
        x += L + random.uniform(4, 14) * (1 + d)
    y += 2.5 + d * 6

# ---------------- the barque
deck = 360
hull_top = [(52, 344), (90, 350), (200, 352), (300, 348), (338, 338)]
hull_bot = [(326, 380), (290, 392), (110, 394), (66, 384)]
c.poly(hull_top + hull_bot, fill=K)
c.line([(54, 354), (90, 360), (200, 362), (300, 358), (334, 350)], fill=Wt, width=5)  # painted band
for i in range(14):  # painted gunports
    x = 92 + i * 16
    c.rect(x, 359.5, x + 6, 364, fill=K)
c.line([(60, 376), (110, 386), (290, 384), (322, 372)], fill=R, width=1.6)  # boot-top
c.line([(52, 344), (90, 350), (200, 352), (300, 348), (338, 338)], fill=Y, width=1.2)  # rail
# reflection of the hull, broken
for k in range(10):
    yy = 398 + k * 4.5
    x0 = 70 + random.uniform(-6, 6) + k * 2; x1 = 320 + random.uniform(-6, 6) - k * 3
    xx = x0
    while xx < x1:
        L = random.uniform(10, 34)
        c.line([(xx, yy), (min(xx + L, x1), yy)], fill=K, width=2.2 - k * 0.15)
        xx += L + random.uniform(3, 8)
# bowsprit + jib-boom, figurehead
c.line([(330, 340), (392, 300)], fill=K, width=3)
c.poly([(334, 340), (344, 336), (342, 348)], fill=Y)
# masts
masts = [(270, 70), (190, 54), (112, 88)]
for x, top in masts:
    c.line([(x, deck - 8), (x, top)], fill=K, width=3.2)
    c.line([(x, top), (x, top - 10)], fill=K, width=1.6)   # pole
    c.rect(x - 1.5, top - 15, x + 1.5, top - 10, fill=Y)     # truck
# shrouds with ratlines
for x, top in masts:
    for side in (-1, 1):
        for k in range(4):
            c.line([(x, top + 40), (x + side * (14 + k * 3), deck - 10)], fill=K, width=0.5)
        for j in range(18):
            yy = top + 48 + j * (deck - 18 - top - 48) / 18
            t = (yy - top - 40) / (deck - 10 - top - 40)
            c.line([(x + side * 2, yy), (x + side * (14 + 9) * t, yy)], fill=K, width=0.4)
# yards with furled sails (white sausages lashed)
for x, top in masts[:2]:
    for k, (yy, half) in enumerate([(top + 22, 30), (top + 58, 42), (top + 104, 54), (top + 160, 62)]):
        c.line([(x - half, yy), (x + half, yy)], fill=K, width=2)
        c.ellipse(x, yy + 3.2, half - 4, 3.2, fill=Wt, outline=K, width=0.8)
        for g in range(-half + 8, half - 4, 8):
            c.line([(x + g, yy), (x + g, yy + 6)], fill=K, width=0.5)
        c.line([(x - half, yy), (x, top + 2)], fill=K, width=0.4)  # lifts
        c.line([(x + half, yy), (x, top + 2)], fill=K, width=0.4)
# mizzen gaff & boom with furled spanker
mx, mt = masts[2]
c.line([(mx, mt + 40), (60, mt + 76)], fill=K, width=1.8)
c.line([(mx, deck - 30), (40, deck - 18)], fill=K, width=1.8)
c.ellipse(76, deck - 21, 34, 3.2, fill=Wt, outline=K, width=0.8)
c.line([(mx, mt + 70), (mx - 28, mt + 70)], fill=K, width=1.6)
# stays
c.line([(270, 70), (392, 300)], fill=K, width=0.7)
c.line([(270, 110), (362, 320)], fill=K, width=0.7)
c.line([(190, 54), (270, 100)], fill=K, width=0.6)
c.line([(112, 88), (190, 84)], fill=K, width=0.6)
# a long house pennant at the gaff (no nation)
c.poly([(66, mt + 70), (22, mt + 76), (66, mt + 84)], fill=R, outline=K, width=0.8)
c.poly([(66, mt + 74.5), (40, mt + 77), (66, mt + 79.5)], fill=Y)

# ---------------- dressing lines: Whitman, in the International Code
MSG = "FLAUNTOUTOSEA" + "BEHOLDTHESEAITSELF"
route = [(392, 302), (270, 62), (190, 46), (112, 80), (36, 342)]
segs = [(route[i], route[i + 1]) for i in range(4)]
lens = [math.dist(a, b) for a, b in segs]
total = sum(lens)
fw = 13
pos = 6
for k, ch in enumerate(MSG):
    # place flag k at arc length s
    s = 10 + k * (total - 20) / len(MSG)
    acc = 0
    for (a, b), L in zip(segs, lens):
        if s <= acc + L:
            t = (s - acc) / L
            P = (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
            ux, uy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
            break
        acc += L
    # flags on steep legs hang from the line — keep a minimum horizontal fly
    if abs(ux) < 0.5:
        ux, uy = math.copysign(0.5, ux), uy * 0.5 / max(abs(uy), 1e-6) * (1 if uy > 0 else -1) if False else uy * 0.6
    n = math.hypot(ux, uy); ux, uy = ux / n * fw, uy / n * fw
    if ux < 0: ux, uy = -ux, -uy
    flag(ch, P, ux, uy, 10)
for a, b in segs:
    c.line([a, b], fill=K, width=0.6)

# rowing boat
c.poly([(130, 430), (176, 430), (170, 438), (138, 438)], fill=R, outline=K, width=1)
c.circle(152, 425, 2.4, fill=K); c.line([(152, 427), (152, 431)], fill=K, width=2)
c.line([(140, 424), (166, 440)], fill=Y, width=1.2)
# gulls
for gx, gy, s in [(150, 150, 6), (168, 168, 5), (350, 230, 5), (24, 200, 4)]:
    c.line([(gx - s, gy - s * 0.3), (gx - s * 0.4, gy - s * 0.6), (gx, gy), (gx + s * 0.4, gy - s * 0.6), (gx + s, gy - s * 0.3)], fill=K, width=1.1)

# ---------------- key plate
c.rect(0, 448, 400, 600, fill=Wt)
c.line([(0, 448), (400, 448)], fill=K, width=2)
c.line([(0, 451.5), (400, 451.5)], fill=K, width=0.6)
c.text((200, 466), "“Flaunt out, O Sea, your separate flags of nations!”", 12.5, fill=K, font=SERIF_BI, anchor="mm")
c.text((200, 482), "WHITMAN · VAUGHAN WILLIAMS, A SEA SYMPHONY · LEEDS, 12 OCTOBER 1910", 7, fill=R, font=SERIF_B, anchor="mm")
letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
for i, ch in enumerate(letters):
    row, col = divmod(i, 13)
    x = 14 + col * 29.3
    y = 496 + row * 50
    flag(ch, (x, y), 22, 0, 16)
    c.text((x + 11, y + 26), ch, 11, fill=K, font=SERIF_B, anchor="mm")
c.line([(14, 592), (386, 592)], fill=K, width=0.6)

finish(c)
