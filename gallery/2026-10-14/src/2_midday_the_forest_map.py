"""A Map of the Forest — Ashdown, a hundred years on.

Hand-tinted endpaper map drawn directly at panel resolution in the six palette colours
(render with --dither none). Real places on the Pooh walks: Gills Lap, the Enchanted
Place, the Heffalump Trap, Poohsticks Bridge, Posingford Wood, Hartfield, the B2026.
"""
import math, os, random
from PIL import Image, ImageDraw, ImageFont

W, H = 400, 600
K, Wh, Rd, Yl, Bl, Gr = (0, 0, 0), (255, 255, 255), (0xE0, 0x1B, 0x24), (0xF5, 0xD4, 0x00), (0x12, 0x3D, 0xB0), (0x1E, 0x9B, 0x3C)
R = random.Random(1926)
im = Image.new("RGB", (W, H), Wh)
d = ImageDraw.Draw(im)
d.fontmode = "1"
F = "/usr/share/fonts/truetype/liberation/"
f_title = ImageFont.truetype(F + "LiberationSerif-Bold.ttf", 27)
f_sub = ImageFont.truetype(F + "LiberationSerif-Italic.ttf", 14)
f_lab = ImageFont.truetype(F + "LiberationSerif-Italic.ttf", 13)
f_labB = ImageFont.truetype(F + "LiberationSerif-Bold.ttf", 13)
f_small = ImageFont.truetype(F + "LiberationSerif-Regular.ttf", 12)

MX0, MY0, MX1, MY1 = 16, 70, 384, 516  # map field


def ctext(x, y, s, font, fill=K):
    w = d.textlength(s, font=font)
    d.text((x - w / 2, y), s, font=font, fill=fill)


def label(x, y, s, font=f_lab, fill=K):
    # knock out a white halo so labels sit on the map like hand-lettering
    w = d.textlength(s, font=font)
    bb = d.textbbox((x - w / 2, y), s, font=font)
    d.rectangle([bb[0] - 2, bb[1] - 1, bb[2] + 2, bb[3] + 1], fill=Wh)
    d.text((x - w / 2, y), s, font=font, fill=fill)


# ------------------------------------------------------------------ heath ground (yellow stipple)
for i in range(7000):
    x, y = R.uniform(MX0, MX1), R.uniform(MY0, MY1)
    d.point((x, y), fill=Yl)
    if R.random() < 0.3:
        d.point((x + 1, y), fill=Yl)


# ------------------------------------------------------------------ regions
def in_posingford(x, y):  # wood around the bridge, north
    return ((x - 140) / 120) ** 2 + ((y - 140) / 62) ** 2 < 1


def in_fivehundred(x, y):  # the big wood, west
    return x < 120 + 25 * math.sin(y / 40) and 230 < y < 500


def in_eastwood(x, y):
    return x > 330 + 15 * math.sin(y / 30) and 250 < y < 420


GL = (238, 330)  # Gills Lap


# ------------------------------------------------------------------ the stream (blue), drawn before trees
def stream(points, w0, w1):
    n = len(points)
    for i in range(n - 1):
        w = round(w0 + (w1 - w0) * i / (n - 1))
        d.line([points[i], points[i + 1]], fill=Bl, width=w)
        d.ellipse([points[i][0] - w / 2, points[i][1] - w / 2, points[i][0] + w / 2, points[i][1] + w / 2], fill=Bl)


main = []
for i in range(80):
    t = i / 79
    x = MX0 + t * (MX1 - MX0)
    y = 165 + 22 * math.sin(t * 9) + 30 * t
    main.append((x, y))
stream(main, 3, 6)
trib = [(70 + 12 * math.sin(i / 3), 196 + i * 5) for i in range(50)]
stream(trib, 2, 2)
# ripple ticks on the main stream
for x, y in main[2::5]:
    d.line([x - 2, y - 6, x + 2, y - 6], fill=Bl)

# ------------------------------------------------------------------ the road B2026, north–south
road = [(300 + 30 * math.sin(i / 14), MY0 + i * 4) for i in range(int((MY1 - MY0) / 4) + 1)]
for x, y in road:
    d.rectangle([x - 4, y - 2, x + 4, y + 2], fill=Yl)
d.line([(x - 5, y) for x, y in road], fill=K, width=1)
d.line([(x + 5, y) for x, y in road], fill=K, width=1)

# ------------------------------------------------------------------ hachured hill at Gills Lap
for ring in range(5):
    rr = 26 + ring * 13
    for k in range(int(rr * 0.9)):
        a = k / (rr * 0.9) * 2 * math.pi
        if ring > 2 and R.random() < 0.4:
            continue
        x0, y0 = GL[0] + rr * math.cos(a), GL[1] + rr * 0.7 * math.sin(a)
        x1, y1 = GL[0] + (rr + 5) * math.cos(a), GL[1] + (rr + 5) * 0.7 * math.sin(a)
        d.line([x0, y0, x1, y1], fill=K if ring < 3 else Rd)

# ------------------------------------------------------------------ trees
trees = []
for i in range(5000):
    x, y = R.uniform(MX0 + 4, MX1 - 4), R.uniform(MY0 + 8, MY1 - 4)
    if any(abs(x - rx) < 8 and abs(y - ry) < 6 for rx, ry in road[::2]):
        continue
    if any(abs(x - sx) < 7 and abs(y - sy) < 7 for sx, sy in main):
        continue
    if in_posingford(x, y) or in_fivehundred(x, y) or in_eastwood(x, y):
        trees.append((x, y, "oak" if R.random() < 0.8 else "pine"))
    elif R.random() < 0.02 and math.hypot(x - GL[0], y - GL[1]) > 80:
        trees.append((x, y, "birch"))
# thin by spacing
kept = []
for t in trees:
    if all((t[0] - k[0]) ** 2 + (t[1] - k[1]) ** 2 > 70 for k in kept):
        kept.append(t)
kept.sort(key=lambda t: t[1])
for x, y, kind in kept:
    if kind == "oak":
        d.line([x, y, x, y + 5], fill=K)
        r = R.choice([4, 4, 5])
        d.ellipse([x - r, y - r, x + r, y + r], fill=Gr, outline=K)
        d.point((x - 1, y - 2), fill=Wh)  # glint
    elif kind == "pine":
        d.line([x, y + 2, x, y + 5], fill=K)
        d.polygon([(x, y - 8), (x - 5, y + 3), (x + 5, y + 3)], fill=Gr, outline=K)
    else:
        d.line([x, y - 3, x, y + 5], fill=K)
        d.ellipse([x - 3, y - 7, x + 3, y - 1], fill=Yl, outline=K)

# the pine clump on Gills Lap: drawn bigger, flat-topped
for k in range(9):
    a = k / 9 * 2 * math.pi
    x, y = GL[0] + 14 * math.cos(a) + R.uniform(-3, 3), GL[1] - 4 + 9 * math.sin(a)
    d.line([x, y, x, y + 9], fill=K, width=1)
    d.ellipse([x - 7, y - 6, x + 7, y + 2], fill=Gr, outline=K)

# ------------------------------------------------------------------ heather tufts on open heath
for i in range(3200):
    x, y = R.uniform(MX0 + 4, MX1 - 4), R.uniform(MY0 + 4, MY1 - 4)
    if in_posingford(x, y) or in_fivehundred(x, y) or in_eastwood(x, y):
        continue
    if math.hypot(x - GL[0], (y - GL[1]) / 0.7) < 85:
        continue
    if any(abs(x - kx) < 6 and abs(y - ky) < 6 for kx, ky, _ in kept):
        continue
    if R.random() < 0.55:
        d.line([x - 2, y, x - 1, y - 2, x, y, x + 1, y - 2, x + 2, y], fill=K)
    else:
        d.point((x, y), fill=Rd); d.point((x + 1, y - 1), fill=Rd); d.point((x - 1, y - 1), fill=Rd)

# ------------------------------------------------------------------ paths (red dashes) from the car park
paths = [
    [(300, 300), (275, 318), GL],
    [GL, (210, 280), (180, 230), (150, 175), (148, 168)],  # to the bridge
    [GL, (262, 380), (285, 430)],  # to the Heffalump Trap
    [GL, (190, 360), (140, 400), (110, 450)],  # into the wood
    [(148, 168), (200, 120), (300, 95)],  # bridge to Hartfield
]
for path in paths:
    for (x0, y0), (x1, y1) in zip(path, path[1:]):
        L = math.hypot(x1 - x0, y1 - y0)
        n = int(L / 6)
        for k in range(n):
            if k % 2 == 0:
                t0, t1 = k / n, min(1, (k + 1) / n)
                d.line([x0 + (x1 - x0) * t0, y0 + (y1 - y0) * t0, x0 + (x1 - x0) * t1, y0 + (y1 - y0) * t1], fill=Rd, width=2)

# ------------------------------------------------------------------ Poohsticks Bridge (drawn)
bx, by = 148, 172
d.rectangle([bx - 13, by - 6, bx + 13, by + 6], fill=Yl, outline=K)
for k in range(-12, 13, 4):
    d.line([bx + k, by - 6, bx + k, by + 6], fill=K)
d.line([bx - 15, by - 8, bx + 15, by - 8], fill=K, width=2)
d.line([bx - 15, by + 8, bx + 15, by + 8], fill=K, width=2)
# three sticks racing downstream
for k, (sx, sy) in enumerate(main[33:42:3]):
    d.line([sx - 3, sy - 1, sx + 3, sy + 1], fill=K if k else Rd, width=2)

# ------------------------------------------------------------------ Hartfield (houses + church)
for i, (hx, hy) in enumerate([(318, 84), (334, 92), (350, 82), (366, 92), (340, 104), (360, 108)]):
    d.rectangle([hx - 5, hy - 3, hx + 5, hy + 5], fill=Wh, outline=K)
    d.polygon([(hx - 7, hy - 3), (hx, hy - 9), (hx + 7, hy - 3)], fill=Rd, outline=K)
    d.point((hx, hy + 1), fill=K)
cx, cy = 378, 112
d.rectangle([cx - 4, cy - 6, cx + 4, cy + 6], fill=Wh, outline=K)
d.polygon([(cx - 4, cy - 6), (cx, cy - 22), (cx + 4, cy - 6)], fill=K)
d.line([cx, cy - 26, cx, cy - 22], fill=K)

# ------------------------------------------------------------------ Heffalump Trap (sandpit)
hx, hy = 290, 440
d.ellipse([hx - 18, hy - 9, hx + 18, hy + 9], fill=Yl, outline=K)
d.ellipse([hx - 11, hy - 5, hx + 11, hy + 5], fill=Wh, outline=K)
for k in range(10):
    a = k / 10 * 2 * math.pi
    d.line([hx + 18 * math.cos(a), hy + 9 * math.sin(a), hx + 22 * math.cos(a), hy + 11 * math.sin(a)], fill=K)

# ------------------------------------------------------------------ a blue balloon over Gills Lap, and bees
bx2, by2 = 258, 262
d.line([bx2, by2 + 8, bx2 - 6, by2 + 34], fill=K)
d.ellipse([bx2 - 8, by2 - 9, bx2 + 8, by2 + 9], fill=Bl, outline=K)
d.point((bx2 - 3, by2 - 4), fill=Wh); d.point((bx2 - 4, by2 - 3), fill=Wh)
for (ex, ey) in [(110, 92), (118, 86), (124, 95)]:
    d.ellipse([ex - 2, ey - 1, ex + 2, ey + 2], fill=Yl, outline=K)
    d.line([ex - 1, ey - 3, ex + 1, ey - 3], fill=K)
# dotted flight path of the bees
for k in range(14):
    d.point((70 + k * 3, 106 - 6 * math.sin(k / 2)), fill=K)
# the bees' tree
d.line([64, 102, 64, 118], fill=K, width=2)
d.ellipse([54, 88, 74, 106], fill=Gr, outline=K)

# ------------------------------------------------------------------ labels
label(176, 196, "Poohsticks Bridge", f_labB)
label(118, 118, "Posingford Wood")
label(340, 120 + 14, "Hartfield", f_labB)
label(GL[0], GL[1] + 18, "Gills Lap", f_labB, Rd)
label(GL[0] - 4, GL[1] + 33, "the Enchanted Place", f_lab)
label(hx, hy + 13, "Heffalump Trap", f_lab)
label(64, 300, "Five", f_lab); label(64, 314, "Hundred", f_lab); label(64, 328, "Acre", f_lab); label(64, 342, "Wood", f_lab)
label(330, 226, "B2026", f_small)
label(232, 486, "Ashdown Forest", f_labB, Gr)
label(60, 128 + 2, "Bees", f_small)

# compass rose
cx, cy = 360, 470
d.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], outline=K)
d.polygon([(cx, cy - 24), (cx - 5, cy), (cx + 5, cy)], fill=Rd, outline=K)
d.polygon([(cx, cy + 24), (cx - 5, cy), (cx + 5, cy)], fill=Wh, outline=K)
d.polygon([(cx - 22, cy), (cx, cy - 4), (cx, cy + 4)], fill=K)
d.polygon([(cx + 22, cy), (cx, cy - 4), (cx, cy + 4)], fill=Wh, outline=K)
ctext(cx, cy - 40, "N", f_labB)

# scale bar
sx, sy = 26, 498
for k in range(4):
    d.rectangle([sx + k * 14, sy, sx + (k + 1) * 14, sy + 4], fill=K if k % 2 == 0 else Wh, outline=K)
d.text((sx, sy + 6), "a short walk", font=f_small, fill=K)

# ------------------------------------------------------------------ frame, title, cartouche
d.rectangle([MX0 - 1, MY0 - 1, MX1 + 1, MY1 + 1], outline=K, width=2)
d.rectangle([4, 4, W - 5, H - 5], outline=K, width=3)
d.rectangle([9, 9, W - 10, H - 10], outline=Rd, width=1)
# title ribbon
d.polygon([(40, 22), (360, 22), (372, 40), (360, 58), (40, 58), (28, 40)], fill=Rd, outline=K)
d.polygon([(28, 40), (14, 30), (22, 46)], fill=Rd, outline=K)
d.polygon([(372, 40), (386, 30), (378, 46)], fill=Rd, outline=K)
ctext(W / 2, 24, "A MAP OF THE FOREST", f_title, Wh)

# cartouche
d.rectangle([40, 526, 360, 586], fill=Wh, outline=K, width=2)
d.rectangle([44, 530, 356, 582], outline=K)
ctext(W / 2, 534, "drawn on the hundredth birthday", f_sub)
ctext(W / 2, 551, "of the book, 14 October 2026", f_sub)
ctext(W / 2, 566, "1926  •  100  •  2026", f_small, Rd)
for ex in (58, 342):
    d.ellipse([ex - 7, 549, ex + 7, 563], fill=Yl, outline=K)
    d.line([ex - 5, 553, ex + 5, 553], fill=K); d.line([ex - 6, 558, ex + 6, 558], fill=K)

im.save(os.environ.get("OUT_RAW", "raw2.png"))
