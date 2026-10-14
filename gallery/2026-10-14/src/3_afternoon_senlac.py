"""Senlac, about three in the afternoon — 14 October 1066.

A bird's-eye battle plate drawn at panel resolution in palette colours (--dither none).
Hundreds of individually placed figures: the English shield wall along the ridge, Norman
horse climbing the slope, archers in the valley shooting high, arrows in the ground.
"""
import math, os, random
from PIL import Image, ImageDraw, ImageFont

W, H = 400, 600
K, Wh, Rd, Yl, Bl, Gr = (0, 0, 0), (255, 255, 255), (0xE0, 0x1B, 0x24), (0xF5, 0xD4, 0x00), (0x12, 0x3D, 0xB0), (0x1E, 0x9B, 0x3C)
R = random.Random(1066)
im = Image.new("RGB", (W, H), Gr)
d = ImageDraw.Draw(im)
d.fontmode = "1"
F = "/usr/share/fonts/truetype/liberation/"
f_t = ImageFont.truetype(F + "LiberationSerif-Bold.ttf", 22)
f_s = ImageFont.truetype(F + "LiberationSerif-Italic.ttf", 13)
f_k = ImageFont.truetype(F + "LiberationSerif-Regular.ttf", 12)
f_kb = ImageFont.truetype(F + "LiberationSerif-Bold.ttf", 12)

TOP, BOT = 56, 512  # field


def crest(x):
    return 168 + 9 * math.sin(x / 55 + 0.6) + 4 * math.sin(x / 17)


def ctext(x, y, s, font, fill=K):
    d.text((x - d.textlength(s, font=font) / 2, y), s, font=font, fill=fill)


# ------------------------------------------------------------------ beyond the ridge: the Weald
for y in range(TOP, 150, 7):
    for x in range(-4, W + 8, 9):
        xx = x + (y % 14) / 2 + R.uniform(-2, 2)
        if abs(xx - (80 + (y - TOP) * 0.5)) < 8:  # the London road
            continue
        r = R.choice([5, 6, 6])
        d.ellipse([xx - r, y - r, xx + r, y + r], fill=Gr, outline=K)
        d.arc([xx - r + 2, y - r + 2, xx + r - 2, y + r - 2], 200, 300, fill=Wh)
road = [(80 + (y - TOP) * 0.5 + 3 * math.sin(y / 9), y) for y in range(TOP, 175)]
d.line(road, fill=Yl, width=7)
d.line([(x - 4, y) for x, y in road], fill=K); d.line([(x + 4, y) for x, y in road], fill=K)

# ------------------------------------------------------------------ the slope: contours + hachures
for k in range(1, 22):
    off = 12 + k * 15 + k * k * 0.25
    pts = [(x, crest(x) + off + 6 * math.sin(x / 40 + k)) for x in range(0, W + 1, 4)]
    # hachure ticks down-slope (denser near the crest, where it is steeper)
    step = 4 if k < 8 else 7
    for x, y in pts[::max(1, step // 4)]:
        if R.random() < 0.85:
            d.line([x, y, x + R.uniform(-1, 1), y + (6 if k < 8 else 4)], fill=K)
    if k % 3 == 0:
        d.line(pts, fill=Yl)

# the marshy valley floor at both flanks
for (cx, cy, rx, ry) in [(50, 470, 80, 34), (360, 480, 70, 30)]:
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=Bl, outline=K)
    for yy in range(cy - ry + 3, cy + ry, 4):
        d.line([cx - rx, yy, cx + rx, yy], fill=Gr)
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], outline=K)
    for i in range(70):
        a, rr = R.uniform(0, 2 * math.pi), R.uniform(0, 0.85)
        x, y = cx + rx * rr * math.cos(a), cy + ry * rr * math.sin(a)
        if R.random() < 0.4:
            d.line([x - 4, y, x + 4, y], fill=Wh)
        else:
            d.line([x, y, x - 2, y - 6], fill=Gr); d.line([x, y, x + 2, y - 6], fill=Gr); d.line([x, y, x, y - 7], fill=K)

# ------------------------------------------------------------------ arrows already in the ground
for i in range(320):
    x = R.uniform(10, 390)
    y = R.uniform(crest(x) + 30, 360)
    d.line([x, y, x + 1, y - 4], fill=K)
    d.point((x + 1, y - 5), fill=Wh)
# dropped shields
for i in range(28):
    x = R.uniform(20, 380); y = R.uniform(crest(x) + 40, 380)
    if R.random() < 0.5:
        d.ellipse([x - 3, y - 2, x + 3, y + 2], fill=Rd, outline=K)
    else:
        d.polygon([(x - 3, y - 2), (x + 3, y - 2), (x, y + 4)], fill=Bl, outline=K)

# ------------------------------------------------------------------ the English shield wall
SHIELD_COLS = [Rd, Rd, Yl, Wh, Rd, Yl, Bl]
for rank in range(7, -1, -1):  # back ranks first
    y0 = -rank * 5
    for x in range(8, W - 6, 6):
        xx = x + (rank % 2) * 3 + R.uniform(-0.7, 0.7)
        yy = crest(xx) + 6 + y0
        # spear above the head of the rear ranks
        if rank > 0 and R.random() < 0.55:
            d.line([xx + 1, yy - 4, xx + 2 + R.uniform(-1, 1), yy - 13], fill=K)
            d.point((xx + 2, yy - 14), fill=Wh)
        # helmet
        d.rectangle([xx - 1, yy - 4, xx + 1, yy - 2], fill=K)
        # shield
        c = R.choice(SHIELD_COLS)
        d.ellipse([xx - 3, yy - 2, xx + 3, yy + 4], fill=c, outline=K)
        d.point((xx, yy + 1), fill=K if c != Rd else Yl)
# front rank: kite-shaped linden shields locked, with a spear line bristling forward
for x in range(6, W - 4, 5):
    yy = crest(x) + 12
    d.line([x, yy, x + 2, yy + 9], fill=K)

# the two standards at the crest: the Dragon of Wessex and the Fighting Man
hx = 196
hy = crest(hx) - 30
d.line([hx, hy + 34, hx, hy - 30], fill=K, width=2)
d.polygon([(hx, hy - 30), (hx + 34, hy - 28), (hx + 34, hy - 6), (hx, hy - 4)], fill=Yl, outline=K)
# the fighting man: a small figure with a club, stitched in red
fx, fy = hx + 17, hy - 17
d.ellipse([fx - 2, fy - 9, fx + 2, fy - 5], fill=Rd)
d.line([fx, fy - 5, fx, fy + 3], fill=Rd, width=2)
d.line([fx, fy + 3, fx - 3, fy + 9], fill=Rd); d.line([fx, fy + 3, fx + 3, fy + 9], fill=Rd)
d.line([fx, fy - 3, fx - 6, fy - 8], fill=Rd); d.line([fx, fy - 3, fx + 7, fy - 6], fill=Rd, width=2)
for i, gx in enumerate(range(hx + 3, hx + 33, 6)):
    d.point((gx, hy - 26), fill=Rd)
# the dragon: a red windsock with jaws and a tail
dx = 238
dy = crest(dx) - 30
d.line([dx, dy + 34, dx, dy - 26], fill=K, width=2)
pts = [(dx, dy - 24)]
for k in range(1, 14):
    pts.append((dx + k * 4, dy - 22 + 6 * math.sin(k / 2.0)))
d.line(pts, fill=Rd, width=9)
d.line([(x, y - 3) for x, y in pts], fill=Yl, width=1)
d.polygon([(dx - 2, dy - 30), (dx + 7, dy - 26), (dx - 2, dy - 18)], fill=Rd, outline=K)  # head
d.point((dx + 1, dy - 26), fill=Wh)
d.polygon([pts[-1], (pts[-1][0] + 8, pts[-1][1] - 5), (pts[-1][0] + 6, pts[-1][1] + 4)], fill=Rd, outline=K)

# ------------------------------------------------------------------ Norman horse, climbing
def horseman(x, y, facing=1, shield=Bl, coat=None):
    coat = coat or R.choice([Wh, K, Rd, K])
    f = facing
    # legs (galloping)
    d.line([x - 6 * f, y + 2, x - 9 * f, y + 8], fill=K)
    d.line([x - 3 * f, y + 2, x - 1 * f, y + 8], fill=K)
    d.line([x + 4 * f, y + 2, x + 8 * f, y + 7], fill=K)
    d.line([x + 6 * f, y + 2, x + 4 * f, y + 8], fill=K)
    # body + neck + head
    d.ellipse([x - 9, y - 4, x + 9, y + 4], fill=coat, outline=K)
    d.polygon([(x + 6 * f, y - 2), (x + 11 * f, y - 10), (x + 14 * f, y - 9), (x + 9 * f, y + 1)], fill=coat, outline=K)
    d.line([x - 9 * f, y - 2, x - 13 * f, y + 4], fill=K, width=2)  # tail
    # rider: mail (black), conical helm, kite shield, couched lance
    d.rectangle([x - 2, y - 13, x + 2, y - 4], fill=K)
    d.polygon([(x - 2, y - 13), (x, y - 18), (x + 2, y - 13)], fill=K)
    d.polygon([(x - 5 * f, y - 12), (x + 1 * f, y - 12), (x - 2 * f, y - 1)], fill=shield, outline=K)
    d.line([x + 1 * f, y - 10, x + 22 * f, y - 20], fill=K)
    d.point((x + 22 * f, y - 20), fill=Wh)
    # pennon
    if R.random() < 0.3:
        d.polygon([(x + 18 * f, y - 18), (x + 14 * f, y - 22), (x + 13 * f, y - 16)], fill=R.choice([Rd, Yl]))


squadrons = [(70, 262, 9), (200, 240, 11), (320, 262, 8), (130, 318, 7), (270, 316, 7)]
riders = []
for (sx, sy, n) in squadrons:
    for i in range(n):
        riders.append((sx + R.uniform(-48, 48), sy + R.uniform(-22, 22)))
riders.sort(key=lambda p: p[1])
for k, (x, y) in enumerate(riders):
    # most face the hill (up-slope is "up" here, so draw them three-quarter facing right/left at random)
    horseman(x, y, facing=R.choice([1, -1]), shield=R.choice([Bl, Bl, Yl, Rd]))

# the feigned retreat: a knot of riders turned back down-hill, chased by a few English
for (x, y) in [(338, 360), (352, 372), (324, 378)]:
    horseman(x, y, facing=1, shield=Bl)
for (x, y) in [(300, 352), (290, 362), (306, 368)]:
    d.rectangle([x - 1, y - 7, x + 1, y - 2], fill=K)
    d.ellipse([x - 3, y - 2, x + 3, y + 4], fill=Rd, outline=K)
    d.line([x + 2, y - 4, x + 9, y - 10], fill=K)

# ------------------------------------------------------------------ archers in the valley, shooting high
arch_y = 418
archers = [(x + R.uniform(-2, 2), arch_y + (i % 2) * 9 + R.uniform(-2, 2)) for i, x in enumerate(range(110, 300, 7))]
for x, y in archers:
    d.ellipse([x - 2, y - 9, x + 2, y - 5], fill=K)
    d.line([x, y - 5, x, y + 2], fill=K, width=2)
    d.line([x, y + 2, x - 2, y + 7], fill=K); d.line([x, y + 2, x + 2, y + 7], fill=K)
    d.arc([x - 5, y - 12, x + 3, y + 2], 280, 80, fill=Wh)  # bow, raised
    d.line([x, y - 4, x + 3, y - 10], fill=K)
# high arcs of arrows over the horse, falling behind the wall
for i in range(18):
    x0, y0 = archers[R.randrange(len(archers))]
    x1 = R.uniform(30, 370); y1 = crest(x1) - 10 - R.uniform(0, 20)
    cx, cy = (x0 + x1) / 2 + R.uniform(-30, 30), R.uniform(-60, 10)
    pts = []
    for k in range(40):
        t = k / 39
        pts.append(((1 - t) ** 2 * x0 + 2 * t * (1 - t) * cx + t * t * x1,
                    (1 - t) ** 2 * (y0 - 10) + 2 * t * (1 - t) * cy + t * t * y1))
    for k in range(0, 39, 3):
        d.line([pts[k], pts[k + 1]], fill=Wh)
    # the arrow at the end of its flight
    (ax, ay), (bx, by) = pts[-3], pts[-1]
    d.line([ax, ay, bx, by], fill=K, width=2)

# ------------------------------------------------------------------ William's knot, on the valley floor
wx, wy = 200, 470
for (x, y) in [(186, 474), (214, 474), (200, 482)]:
    horseman(x, y, facing=1, shield=Bl)
d.line([wx, wy + 8, wx, wy - 34], fill=K, width=2)
d.rectangle([wx, wy - 34, wx + 22, wy - 18], fill=Wh, outline=K)
d.line([wx + 11, wy - 33, wx + 11, wy - 19], fill=Rd, width=3)
d.line([wx + 1, wy - 26, wx + 21, wy - 26], fill=Rd, width=3)  # papal banner

# ------------------------------------------------------------------ title and key
d.rectangle([0, 0, W, TOP - 4], fill=Yl)
d.line([0, TOP - 4, W, TOP - 4], fill=K, width=2)
ctext(W / 2, 6, "SENLAC  ·  14 OCTOBER 1066", f_t)
ctext(W / 2, 32, "about three in the afternoon", f_s)

d.rectangle([0, BOT, W, H], fill=Wh)
d.line([0, BOT, W, BOT], fill=K, width=2)
kx, ky = 18, BOT + 10
d.ellipse([kx - 4, ky + 2, kx + 4, ky + 10], fill=Rd, outline=K)
d.text((kx + 10, ky), "Harold's housecarls & fyrd, on the ridge", font=f_k, fill=K)
ky += 18
d.polygon([(kx - 4, ky + 1), (kx + 4, ky + 1), (kx, ky + 12)], fill=Bl, outline=K)
d.text((kx + 10, ky), "Norman, Breton & Flemish horse", font=f_k, fill=K)
ky += 18
d.line([kx - 5, ky + 10, kx + 5, ky + 2], fill=K, width=2)
d.text((kx + 10, ky), "archers, shooting high over the wall", font=f_k, fill=K)
ky += 18
d.rectangle([kx - 4, ky + 2, kx + 4, ky + 10], fill=Yl, outline=K)
d.text((kx + 10, ky), "the Fighting Man & the Dragon: Harold", font=f_kb, fill=K)
d.rectangle([3, 3, W - 4, H - 4], outline=K, width=2)

im.save(os.environ.get("OUT_RAW", "raw3.png"))
