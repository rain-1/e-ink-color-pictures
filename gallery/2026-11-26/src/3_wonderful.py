"""Afternoon — "Yes, wonderful things." The breach in the sealed doorway, one candle,
and the antechamber heaped with gold. Candlelight is an 8x8 Bayer screen on distance."""
import math, random
from common import *
from PIL import Image, ImageDraw

random.seed(1126)
FX, FY = 200, 462           # the flame
c = C(K)                    # the room
FLOOR, RAIL = 398, 292


def gold(pts, w=1.0):
    c.poly(pts, Y, K, w)


def couch(hx, kind, length=96):
    x1 = hx + length
    # tail
    tail = bez((x1 + 4, RAIL + 2), (x1 + 20, RAIL - 6), (x1 + 4, RAIL - 40), (x1 + 16, RAIL - 62), 16)
    c.line(tail, K, 6); c.line(tail, Y, 3.6)
    if kind == "lion": c.circ(x1 + 16, RAIL - 64, 5, fill=Y, outline=K)
    # legs
    for lx in (hx + 12, x1 - 16):
        leg = [(lx, RAIL + 6), (lx + 13, RAIL + 6), (lx + 11, RAIL + 44), (lx + 15, RAIL + 60), (lx + 10, FLOOR - 8),
               (lx + 13, FLOOR - 2), (lx - 5, FLOOR - 2), (lx + 1, FLOOR - 12), (lx + 3, RAIL + 60), (lx - 2, RAIL + 40)]
        gold(leg)
        for j in range(3): c.line([(lx - 3 + j * 4, FLOOR - 7), (lx - 3 + j * 4, FLOOR - 3)], K, .8)
        c.line([(lx + 5, RAIL + 14), (lx + 6, RAIL + 54)], K, .8)
    c.rect(hx + 2, FLOOR - 2, x1 + 6, FLOOR + 4, fill=Y, outline=K, w=1)
    # rail and mattress
    c.rect(hx + 4, RAIL - 4, x1 + 6, RAIL + 7, fill=Y, outline=K, w=1)
    for x in range(int(hx) + 8, int(x1) + 4, 5):
        if kind == "cow": c.circ(x, RAIL + 1.5, 1.4, fill=K)
        else: c.line([(x, RAIL - 1), (x + 3, RAIL + 4)], K, .8)
    # neck
    gold([(hx + 2, RAIL - 4), (hx + 26, RAIL - 4), (hx + 23, RAIL - 62), (hx + 3, RAIL - 66)])
    if kind == "cow":
        for (sx, sy) in ((10, -16), (17, -30), (9, -44), (18, -54), (16, -10)):
            for (ox, oy) in ((0, 0), (3, 2.5), (-3, 2.5)): c.circ(hx + sx + ox, RAIL + sy + oy, 1.8, fill=K)
    elif kind == "lion":
        for j in range(7):
            c.arc(hx + 12, RAIL - 60 + j * 8, 12, 20, 160, K, .9, ry=6)
    else:
        for j in range(6):
            for i in range(3): c.line([(hx + 6 + i * 6 + (j % 2) * 3, RAIL - 56 + j * 9), (hx + 9 + i * 6 + (j % 2) * 3, RAIL - 52 + j * 9)], K, .9)
    hy = RAIL - 66
    if kind == "lion":
        c.circ(hx + 20, hy - 12, 6, fill=Y, outline=K)                       # ear
        c.circ(hx + 10, hy - 2, 16, fill=Y, outline=K, w=1.2)
        c.ell(hx - 14, hy - 4, hx + 8, hy + 14, fill=Y, outline=K, w=1.2)     # muzzle
        c.poly([(hx - 14, hy + 2), (hx - 9, hy - 1), (hx - 8, hy + 6)], B, K, .8)  # nose
        c.line([(hx - 12, hy + 8), (hx - 2, hy + 10)], K, 1)
        c.ell(hx + 2, hy - 9, hx + 11, hy - 3, fill=WH, outline=K, w=1); c.circ(hx + 6, hy - 6, 1.8, fill=K)
        c.line([(hx + 12, hy - 4), (hx + 20, hy + 4)], B, 1.4)                # tear line, blue glass
        for j in range(3): c.circ(hx - 6 + j * 3, hy + 4.5, .8, fill=K)
    elif kind == "cow":
        for s in (-1, 1):                                                     # lyre horns
            horn = bez((hx + 12 + s * 5, hy - 10), (hx + 12 + s * 26, hy - 26), (hx + 12 + s * 22, hy - 52), (hx + 12 + s * 9, hy - 62), 14)
            c.line(horn, K, 5.5); c.line(horn, Y, 3.2)
        c.circ(hx + 12, hy - 36, 13.5, fill=K); c.circ(hx + 12, hy - 36, 12, fill=Y); c.circ(hx + 12, hy - 36, 9.5, fill=R)
        gold([(hx + 24, hy - 12), (hx + 2, hy - 10), (hx - 18, hy + 12), (hx - 17, hy + 22), (hx - 4, hy + 23), (hx + 12, hy + 10), (hx + 25, hy + 8)], 1.2)
        gold([(hx + 20, hy - 6), (hx + 36, hy - 12), (hx + 34, hy - 3), (hx + 22, hy + 1)])   # ear
        c.ell(hx + 3, hy - 5, hx + 12, hy + 2, fill=WH, outline=K, w=1); c.circ(hx + 7, hy - 1.5, 2, fill=K)
        c.circ(hx - 13, hy + 15, 1.5, fill=K); c.line([(hx - 15, hy + 19), (hx - 6, hy + 20)], K, .9)
        for (sx, sy) in ((16, 2), (6, 8)):
            for (ox, oy) in ((0, 0), (3, 2.5), (-3, 2.5)): c.circ(hx + sx + ox, hy + sy + oy, 1.6, fill=K)
    else:                                                                     # Ammut: hippo head, jaws open
        c.circ(hx + 22, hy - 10, 5, fill=Y, outline=K)
        gold([(hx + 26, hy - 8), (hx + 4, hy - 12), (hx - 20, hy - 6), (hx - 27, hy + 6), (hx - 22, hy + 12), (hx - 2, hy + 12), (hx + 8, hy + 6), (hx + 26, hy + 10)], 1.2)
        c.poly([(hx - 22, hy + 12), (hx - 2, hy + 12), (hx + 8, hy + 20), (hx - 18, hy + 22)], R, K, 1)   # mouth
        gold([(hx - 20, hy + 22), (hx + 8, hy + 20), (hx + 14, hy + 28), (hx - 14, hy + 31)], 1.2)
        for j in range(4):
            tx = hx - 19 + j * 5.5
            c.poly([(tx, hy + 12), (tx + 4, hy + 12), (tx + 2, hy + 18)], WH, K, .6)
            c.poly([(tx + 1, hy + 22), (tx + 5, hy + 22), (tx + 3, hy + 16)], WH, K, .6)
        c.ell(hx + 4, hy - 8, hx + 13, hy - 1, fill=WH, outline=K, w=1); c.circ(hx + 8, hy - 4.5, 2, fill=K)
        c.circ(hx - 21, hy + 2, 1.6, fill=K)


def chest(x, y, w, h, style=0):
    c.rect(x, y - h, x + w, y, fill=Y, outline=K, w=1)
    if style == 0:                                    # painted casket: panels
        c.rect(x + 3, y - h + 3, x + w - 3, y - 3, fill=WH, outline=K, w=.8)
        for i in range(int(w // 8)):
            c.rect(x + 5 + i * 8, y - h + 5, x + 9 + i * 8, y - 5, fill=[R, B, G][i % 3])
    else:                                             # ebony and gold: ankh-like slats
        c.rect(x + 3, y - h + 3, x + w - 3, y - 3, fill=K)
        for i in range(int((w - 6) // 6)):
            c.line([(x + 6 + i * 6, y - h + 5), (x + 6 + i * 6, y - 5)], Y, 1.4)
    c.poly([(x - 2, y - h), (x + w / 2, y - h - 7), (x + w + 2, y - h)], Y, K, 1)   # gabled lid
    c.circ(x + w / 2, y - h + 1, 2, fill=R, outline=K, w=.6)
    c.line([(x + 1, y), (x + 1, y + 4)], Y, 1.6); c.line([(x + w - 1, y), (x + w - 1, y + 4)], Y, 1.6)


def egg_box(x, y, w=26, h=15):
    c.ell(x, y - h, x + w, y, fill=WH, outline=K, w=1)
    c.line([(x + 2, y - h / 2), (x + w - 2, y - h / 2)], K, .8)
    c.line([(x + w / 2, y - h + 1), (x + w / 2, y - 1)], K, .8)


def wheel(x, y, r):
    c.circ(x, y, r + 1.5, fill=K); c.circ(x, y, r, fill=Y); c.circ(x, y, r - 4.5, fill=K)
    for k in range(6):
        a = k * math.pi / 3 + .2
        c.line([(x, y), (x + (r - 3) * math.cos(a), y + (r - 3) * math.sin(a))], Y, 2.6)
    c.circ(x, y, 5.5, fill=Y, outline=K, w=1); c.circ(x, y, 2, fill=R)
    for k in range(18):
        a = k * math.pi / 9
        c.circ(x + (r - 2.2) * math.cos(a), y + (r - 2.2) * math.sin(a), .8, fill=K)


def vase(x, y, s=1.0):
    """Alabaster unguent jar with openwork handles."""
    pts = [(-5, 0), (-9, -4), (-11, -22), (-6, -34), (-4, -52), (-8, -56), (8, -56), (4, -52), (6, -34), (11, -22), (9, -4), (5, 0)]
    for sd in (-1, 1):
        h = bez((sd * 5 * s + x, y - 50 * s), (x + sd * 24 * s, y - 52 * s), (x + sd * 26 * s, y - 20 * s), (x + sd * 10 * s, y - 14 * s), 12)
        c.line(h, K, 4.4); c.line(h, WH, 2.4)
        c.circ(x + sd * 19 * s, y - 36 * s, 3 * s, fill=WH, outline=K, w=.8)
    c.poly([(x + px * s, y + py * s) for px, py in pts], WH, K, 1.1)
    c.line([(x - 9 * s, y - 14 * s), (x + 9 * s, y - 14 * s)], Y, 1.2); c.line([(x - 6 * s, y - 34 * s), (x + 6 * s, y - 34 * s)], B, 1.4)
    c.rect(x - 13 * s, y, x + 13 * s, y + 4 * s, fill=WH, outline=K, w=.9)


# ---- back wall furniture, far to near ----
# things heaped on the couches
chest(74, RAIL - 4, 54, 26, 0); chest(96, RAIL - 34, 40, 18, 1)
c.rect(176, RAIL - 12, 262, RAIL - 4, fill=Y, outline=K, w=1)                # a bed frame
for x in range(180, 260, 4): c.line([(x, RAIL - 11), (x + 3, RAIL - 5)], K, .7)
c.poly([(250, RAIL - 12), (262, RAIL - 12), (262, RAIL - 44), (256, RAIL - 44)], Y, K, 1)
for i in range(3): egg_box(196 + i * 19, RAIL - 12, 20, 12)
egg_box(206, RAIL - 23, 20, 12)
chest(292, RAIL - 4, 52, 32, 1)
c.rect(300, RAIL - 62, 336, RAIL - 46, fill=WH, outline=K, w=1); c.line([(300, RAIL - 54), (336, RAIL - 54)], R, 1.4)
# the guardian statue, far right: black skin, gold kilt and headcloth
gx = 334
c.poly([(gx - 9, 180), (gx + 9, 180), (gx + 14, 204), (gx - 14, 204)], Y, K, 1)      # nemes
c.line([(gx, 176), (gx - 5, 170), (gx - 2, 166)], Y, 1.6)                             # uraeus
c.ell(gx - 7, 184, gx + 7, 202, fill=K, outline=Y, w=1)
c.ell(gx - 5, 190, gx - 1, 193, fill=WH)
c.poly([(gx - 15, 206), (gx + 15, 206), (gx + 11, 250), (gx - 11, 250)], K, Y, 1)
for j in range(4): c.arc(gx, 206, 14, 20, 160, Y, 1.2, ry=4 + j * 3)                  # collar
c.poly([(gx - 12, 250), (gx + 12, 250), (gx + 18, 300), (gx - 24, 300), (gx - 14, 268)], Y, K, 1)   # kilt
for j in range(6): c.line([(gx - 10 + j * 4, 254), (gx - 16 + j * 6, 298)], K, .7)
c.line([(gx - 22, 216), (gx - 26, 398)], Y, 2.2)                                      # staff
c.line([(gx - 13, 210), (gx - 22, 250)], Y, 1.2)

couch(70, "lion"); couch(172, "cow"); couch(272, "hippo", 110)

# under the couches
chest(92, FLOOR - 4, 50, 30, 1)
for r_ in range(3):
    for i in range(3 - (r_ > 1)):
        egg_box(196 + i * 24 + r_ * 6, FLOOR - 4 - r_ * 14, 24, 14)
# the throne, tucked under Ammut
tx, ty = 300, FLOOR - 4
c.poly([(tx + 34, ty - 30), (tx + 44, ty - 30), (tx + 50, ty - 84), (tx + 40, ty - 84)], Y, K, 1)
c.rect(tx + 37, ty - 78, tx + 47, ty - 36, fill=R, outline=K, w=.8)
c.rect(tx, ty - 34, tx + 44, ty - 27, fill=Y, outline=K, w=1)
for lx in (tx + 2, tx + 36):
    c.poly([(lx, ty - 27), (lx + 7, ty - 27), (lx + 6, ty - 6), (lx + 9, ty), (lx - 2, ty), (lx + 1, ty - 6)], Y, K, .9)
c.circ(tx + 2, ty - 37, 5.5, fill=Y, outline=K, w=1); c.circ(tx, ty - 37, 1, fill=K)
c.line([(tx + 9, ty - 16), (tx + 36, ty - 16)], Y, 1.6)
for i in range(4): c.line([(tx + 12 + i * 7, ty - 26), (tx + 12 + i * 7, ty - 17)], Y, 1.2)

# floor, receding
for j in range(9):
    yy = FLOOR + 6 + j * j * .9 + j * 3
    c.line([(40, yy), (360, yy)], Y, .9)
for i in range(-10, 11):
    c.line([(200 + i * 22, FLOOR + 6), (200 + i * 52, 480)], Y, .7)

# near things
wheel(318, 402, 36); wheel(282, 424, 30)
c.line([(250, 446), (346, 380)], K, 5); c.line([(250, 446), (346, 380)], Y, 2.6)       # a chariot pole
chest(62, 446, 66, 34, 0)
vase(160, 440, .95); vase(196, 448, 1.1); vase(232, 438, .85)
# a stool and a bouquet
c.rect(120, 404, 150, 409, fill=WH, outline=K, w=.9)
for lx in (123, 146): c.line([(lx, 409), (lx + (2 if lx < 130 else -2), 432)], WH, 2)
c.line([(124, 422), (146, 422)], WH, 1.2)
for i in range(7):
    a = math.radians(-120 + i * 10)
    c.line([(52, 404), (52 + 46 * math.cos(a), 404 + 46 * math.sin(a))], G, 1.3)
    c.circ(52 + 48 * math.cos(a), 404 + 48 * math.sin(a), 2.6, fill=[R, WH, B][i % 3])

room = c.array().astype(np.int32)

# ---------- light ----------
yy, xx = np.mgrid[0:H, 0:W]
dist = np.hypot(xx - FX, (yy - FY) * 0.82)
light = np.clip(1.18 - dist / 300.0, 0, 1) ** 1.35
thr = np.tile(BAYER, (H // 8 + 1, W // 8 + 1))[:H, :W]
isK = (room == 0).all(-1)
lit = thr < np.clip(light * 2.1 + 0.12, 0, 1)
out = np.where(lit[..., None], room, 0)
haze = isK & (thr < light * 0.13 - 0.03) & (yy < FLOOR + 4)            # the back wall catching a little
out[haze] = Y
core = (~isK) & (dist < 70) & (room == np.array(Y)).all(-1) & (thr < (1 - dist / 70) * .5)
out[core] = WH                                                          # gold burning white near the flame

# ---------- the plastered doorway and its breach ----------
w = C(WH)
for _ in range(520):                                                    # trowel marks
    x, y_ = random.uniform(0, 400), random.uniform(0, 600)
    a = random.uniform(-.5, .5); ln = random.uniform(8, 26)
    w.line([(x, y_), (x + ln * math.cos(a), y_ + ln * math.sin(a))], Y, 1)
for _ in range(240):
    x, y_ = random.uniform(0, 400), random.uniform(0, 600)
    w.line([(x, y_), (x + random.uniform(2, 6), y_ + random.uniform(-1, 1))], K, .8)


def seal(x, y_, rot):
    """Necropolis seal: the jackal couchant over nine bound captives."""
    def T(px, py):
        ca, sa = math.cos(rot), math.sin(rot)
        return (x + px * ca - py * sa, y_ + px * sa + py * ca)
    oval = [T(15 * math.cos(t) * (1 if abs(math.sin(t)) < .8 else .92), 27 * math.sin(t)) for t in np.linspace(0, 2 * math.pi, 40)]
    w.poly(oval, WH, R, 1.6)
    w.poly([T(-10, -13), (T(-4, -17)), T(6, -17), T(10, -20), T(11, -15), T(8, -11), T(-10, -11)], R)     # jackal
    w.line([T(9, -19), T(8, -24)], R, 1.2); w.line([T(-10, -12), T(-12, -6)], R, 1.2)
    for r_ in range(3):
        for i in range(3):
            px, py = -8 + i * 8, -3 + r_ * 9
            w.circ(*T(px, py), 1.6, fill=R); w.line([T(px, py + 1), T(px - 1, py + 6), T(px + 3, py + 6)], R, 1.1)


for (x, y_, rot) in ((40, 60, .15), (92, 38, -.3), (322, 50, .4), (366, 108, -.1), (30, 190, -.2), (372, 250, .25),
                     (28, 330, .1), (374, 392, -.35), (36, 470, .3), (88, 545, -.15), (318, 548, .2), (366, 498, -.2),
                     (212, 34, .05), (150, 566, .35), (268, 572, -.3)):
    seal(x, y_, rot)
wall = w.array().astype(np.int32)

# the hole: a ragged oval
hole = []
N = 90
for i in range(N):
    t = 2 * math.pi * i / N
    rr = 1 + .07 * math.sin(3 * t + 1) + .05 * math.sin(7 * t) + random.uniform(-.045, .045)
    hole.append((200 + 150 * rr * math.cos(t), 286 + 196 * rr * math.sin(t) * (1 if math.sin(t) < 0 else .93)))
m = Image.new("L", (W, H), 0); md = ImageDraw.Draw(m)
md.polygon(hole, fill=255)
mask = np.asarray(m) > 0
rim = Image.new("L", (W, H), 0); rd = ImageDraw.Draw(rim)
rd.polygon([(200 + (x - 200) * 1.06, 286 + (y_ - 286) * 1.05) for x, y_ in hole], fill=255)
rimm = (np.asarray(rim) > 0) & ~mask

# shade the plaster by candle distance: white -> gold screen -> black screen
dw = np.hypot(xx - FX, (yy - FY) * 0.9)
lw = np.clip(1.3 - dw / 285.0, 0, 1)
wl = wall.copy()
isW = (wall == 255).all(-1)
wl[isW & (thr > lw * 1.7)] = Y
dark = thr > lw * 2.6 + .12
wl[dark] = K
wl[rimm] = np.where((thr[rimm] < lw[rimm] * 1.2)[:, None], np.array(Y), np.array(K))   # broken edge, in section
final = np.where(mask[..., None], out, wl).astype(np.uint8)

img = Image.fromarray(final, "RGB"); d = ImageDraw.Draw(img); d.fontmode = "1"
d.line(hole + [hole[0]], fill=K, width=2)
for i in range(0, N, 3):                                                # cracks running out from the breach
    x, y_ = hole[i]; a = math.atan2(y_ - 286, x - 200) + random.uniform(-.5, .5)
    pts = [(x, y_)]
    for _ in range(random.randint(2, 5)):
        a += random.uniform(-.6, .6); ln = random.uniform(5, 13)
        pts.append((pts[-1][0] + ln * math.cos(a), pts[-1][1] + ln * math.sin(a)))
    d.line(pts, fill=K, width=1)

# ---------- the candle, and the hand that holds it ----------
d.polygon([(400, 600), (400, 548), (300, 530), (252, 520), (246, 552), (300, 600)], fill=K)             # sleeve
d.polygon([(256, 518), (246, 520), (240, 556), (250, 558)], fill=WH, outline=K)                         # cuff
d.polygon([(246, 522), (226, 512), (206, 508), (190, 512), (186, 526), (190, 546), (206, 556), (240, 554)], fill=Y, outline=K)   # hand
for i in range(4):
    d.line([(196 + i * 9, 514 + i * 1), (192 + i * 9, 548 + i * 2)], fill=K, width=1)
d.rectangle([193, 478, 207, 512], fill=WH, outline=K)
d.polygon([(193, 478), (190, 486), (194, 492)], fill=WH, outline=K)                                     # a run of wax
d.line([(200, 478), (200, 470)], fill=K, width=1)
flame = [(200, 436), (206, 452), (208, 463), (204, 471), (196, 471), (192, 463), (194, 452)]
d.polygon([(200, 430), (209, 450), (212, 464), (206, 475), (194, 475), (188, 464), (191, 450)], fill=R)
d.polygon(flame, fill=Y); d.polygon([(200, 452), (203, 462), (200, 469), (197, 462)], fill=WH)
f = ImageFont.truetype("DejaVuSerif-Bold.ttf", 13)
d.rectangle([64, 572, 236, 592], fill=K)
d.text((150, 582), "“Yes, wonderful things.”", fill=Y, font=f, anchor="mm")
c.save(np.asarray(img))
