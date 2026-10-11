"""Midday: 'Spoils of the Hunt' — a herbarium plate of nine autumn leaves, each turning
from green at the stalk to red/yellow at the tips, with veins, tar spots and labels."""
import os, math, random
import numpy as np
from lib import *

rnd = random.Random(1011)
PAPER = WH
img = Image.new("RGB", (W, H), WH)
d = ImageDraw.Draw(img)
noise = value_noise(W, H, 40, seed=7, octaves=3)


def rot(pts, cx, cy, a):
    c, s = math.cos(a), math.sin(a)
    return [(cx + x * c - y * s, cy + x * s + y * c) for x, y in pts]


def ovate(L, Wd, teeth=0, tooth=0.0, lobes=0, lobe=0.0, cord=0.0, n=240):
    """Leaf outline in local coords: base at (0,0), tip at (0,-L)."""
    right = []
    for i in range(n + 1):
        t = i / n
        w = Wd * math.sin(math.pi * t) ** 0.8 * (1 - 0.35 * t)
        if cord:
            w += cord * Wd * max(0, 0.25 - t) * 4 * math.sin(math.pi * t * 4) ** 2
        if lobes:
            w *= 1 - lobe * (0.5 + 0.5 * math.cos(t * lobes * 2 * math.pi)) * math.sin(math.pi * t)
        if teeth:
            w *= 1 + tooth * (abs(math.sin(t * teeth * math.pi)) - 0.5)
        y = -L * t
        if cord:
            y += cord * L * 0.12 * math.sin(math.pi * min(1, t * 3))
        right.append((w, y))
    left = [(-x, y) for x, y in reversed(right)]
    return right + left


def ginkgo(L, n=200):
    pts = [(0, 0)]
    for i in range(n + 1):
        a = math.radians(-55 + 110 * i / n)
        r = L * (1 - 0.18 * math.exp(-((a / 0.12) ** 2)))  # central notch
        r *= 1 + 0.03 * math.sin(i * 0.9)
        pts.append((r * math.sin(a), -r * math.cos(a) * 0.95))
    return pts


def colour_field(mask, base, tip, cy0, cy1, seed):
    """Per-pixel colour: base colour near the stalk blending to tip colour, with mottling."""
    ys = np.arange(H)[:, None] * np.ones((1, W))
    t = np.clip((cy0 - ys) / max(1, cy0 - cy1), 0, 1)
    t = np.clip(t + (noise - 0.5) * 0.9, 0, 1)
    b = np.array(base, float); tp = np.array(tip, float)
    col = b[None, None, :] * (1 - t[..., None]) + tp[None, None, :] * t[..., None]
    return col


def paint_leaf(outline, base, tip, veins, vein_col, spots=0, cx=0, cy=0, size=100):
    m = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m).polygon(outline, fill=255)
    ys = [p[1] for p in outline]
    col = colour_field(None, base, tip, cy, min(ys), 0)
    arr = np.asarray(img).astype(float)
    mk = (np.asarray(m) > 127)[..., None]
    arr = np.where(mk, col, arr)
    img.paste(Image.fromarray(arr.astype(np.uint8)))
    dd = ImageDraw.Draw(img)
    for ln, w in veins:
        dd.line(ln, fill=vein_col, width=w)
    # tar spots / insect holes
    xs = [p[0] for p in outline]
    for _ in range(spots):
        for _ in range(40):
            x, y = rnd.uniform(min(xs), max(xs)), rnd.uniform(min(ys), max(ys))
            if m.getpixel((int(x), int(y))) > 0:
                r = rnd.uniform(3, 7)
                dd.ellipse((x - r, y - r, x + r, y + r), fill=K)
                dd.ellipse((x - r - 3, y - r - 3, x + r + 3, y + r + 3), outline=Y, width=2)
                break
    dd.line(outline + [outline[0]], fill=K, width=3)


def pinnate_veins(cx, cy, a, L, Wd, pairs, w=2):
    vs = [(rot([(0, 0), (0, -L * 0.96)], cx, cy, a), 3)]
    for i in range(1, pairs + 1):
        t = i / (pairs + 1)
        y = -L * t * 0.95
        span = Wd * math.sin(math.pi * t) ** 0.8 * (1 - 0.35 * t) * 0.85
        for s in (-1, 1):
            vs.append((rot([(0, y), (s * span, y - span * 0.55)], cx, cy, a), w))
    return vs


def tape(x, y, a):
    pts = rot([(-22, -8), (22, -8), (22, 8), (-22, 8)], x, y, a)
    d.polygon(pts, fill=WH)
    d.line(pts + [pts[0]], fill=K, width=2)


def label(x, y, num, latin, common):
    fi = font(FONT_ITAL, 27); fs = font(FONT_SC, 22)
    fb = font(FONT_SERIF_B, 22)
    d.text((x, y), f"{num}.", font=fb, fill=R)
    off = d.textlength(f"{num}.", font=fb) + 10
    d.text((x + off, y - 2), latin, font=fi, fill=K)
    d.text((x + off, y + 26), common, font=fs, fill=K)


# ---- header
d.rectangle((0, 0, W, H), fill=PAPER)
ft = font(FONT_SERIF_B, 40)
title = "SPOILS OF THE HUNT"
d.text(((W - d.textlength(title, font=ft)) / 2, 44), title, font=ft, fill=K)
fsub = font(FONT_ITAL, 26)
sub = "momijigari · nine leaves gathered on the eleventh of October"
d.text(((W - d.textlength(sub, font=fsub)) / 2, 96), sub, font=fsub, fill=K)
d.line([(60, 136), (W - 60, 136)], fill=K, width=3)
d.line([(60, 142), (W - 60, 142)], fill=R, width=2)

cells = [(140, 330), (400, 330), (660, 330), (140, 650), (400, 650), (660, 650), (140, 960), (400, 960), (660, 960)]
LABEL_Y = {330: 470, 650: 790, 960: 1090}
GREEN_BASE = (40, 140, 50)

# 1 Japanese maple
cx, cy = cells[0]; ROW = cells[0][1]; cy -= 40
o = maple_leaf(cx, cy - 10, 120, 0.0, lobes=7, seed=1)
v = [(ln, 3) for ln in maple_veins(cx, cy - 10, 120, 0.0, 7)]
paint_leaf(o, (210, 40, 30), R, v, RUST, spots=0, cx=cx, cy=cy + 20)
d.line(stem(cx, cy - 10, 120, 0.0), fill=K, width=4)
label(cx - 115, LABEL_Y[ROW], "I", "Acer palmatum", "Japanese maple")

# 2 Ginkgo
cx, cy = cells[1]; ROW = cells[1][1]
o = rot(ginkgo(150), cx, cy + 70, 0.15)
v = [(rot([(0, 0), (150 * math.sin(math.radians(a)) * 0.95, -150 * math.cos(math.radians(a)) * 0.9)], cx, cy + 70, 0.15), 1)
     for a in range(-52, 53, 5)]
paint_leaf(o, (200, 200, 30), Y, v, (190, 150, 0), cx=cx, cy=cy + 60)
d.line(rot([(0, 0), (6, 60)], cx, cy + 70, 0.15), fill=K, width=4)
label(cx - 115, LABEL_Y[ROW], "II", "Ginkgo biloba", "maidenhair tree")

# 3 Sweetgum (5-lobed star)
cx, cy = cells[2]; ROW = cells[2][1]; cy -= 40
o = maple_leaf(cx, cy, 105, -0.2, lobes=5, depth=0.5, jag=0.04, seed=3, spread=300)
v = [(ln, 3) for ln in maple_veins(cx, cy, 105, -0.2, 5, spread=300)]
paint_leaf(o, (140, 30, 90), (60, 30, 120), v, R, cx=cx, cy=cy + 40)
d.line(stem(cx, cy, 105, -0.2), fill=K, width=4)
label(cx - 115, LABEL_Y[ROW], "III", "Liquidambar", "sweetgum")

# 4 Oak (lobed)
cx, cy = cells[3]; ROW = cells[3][1]; cy += 95
L, Wd = 200, 70
o = rot(ovate(L, Wd, lobes=5, lobe=0.55), cx, cy, -0.25)
paint_leaf(o, (150, 110, 20), RUST, pinnate_veins(cx, cy, -0.25, L, Wd * 0.75, 5), K, spots=0, cx=cx, cy=cy)
d.line(rot([(0, 0), (0, 30)], cx, cy, -0.25), fill=K, width=5)
label(cx - 115, LABEL_Y[ROW], "IV", "Quercus rubra", "red oak")

# 5 Cherry (serrate ovate)
cx, cy = cells[4]; ROW = cells[4][1]; cy += 60
L, Wd = 200, 62
o = rot(ovate(L, Wd, teeth=34, tooth=0.08), cx, cy, 0.3)
paint_leaf(o, (60, 150, 40), (240, 110, 20), pinnate_veins(cx, cy, 0.3, L, Wd, 8), RUST, spots=3, cx=cx, cy=cy)
d.line(rot([(0, 0), (0, 40)], cx, cy, 0.3), fill=K, width=4)
label(cx - 115, LABEL_Y[ROW], "V", "Prunus serrulata", "hill cherry")

# 6 Katsura (heart)
cx, cy = cells[5]; ROW = cells[5][1]; cy += 20
L, Wd = 150, 90
heart = []
for i in range(361):
    tt = math.radians(i)
    hx = 16 * math.sin(tt) ** 3
    hy = 13 * math.cos(tt) - 5 * math.cos(2 * tt) - 2 * math.cos(3 * tt) - math.cos(4 * tt)
    k = 1 + 0.025 * abs(math.sin(i * math.pi / 9))
    heart.append((hx * 6.2 * k, hy * 6.2 * k - 31))
o = rot(heart, cx, cy, -0.1)
vs = [(rot([(0, 0), (s * 55, -90 + abs(s) * 10)], cx, cy, -0.1), 2) for s in (-1, -0.5, 0, 0.5, 1)]
paint_leaf(o, (230, 200, 20), (240, 120, 40), vs, (180, 110, 0), cx=cx, cy=cy)
d.line(rot([(0, 0), (0, 50)], cx, cy, -0.1), fill=K, width=4)
label(cx - 115, LABEL_Y[ROW], "VI", "Cercidiphyllum", "katsura · caramel")

# 7 Maple samaras
cx, cy = cells[6]; ROW = cells[6][1]; cy -= 20
for s in (-1, 1):
    wing = rot([(0, 0), (s * 30, -30), (s * 100, -80), (s * 125, -70), (s * 110, -40), (s * 40, 10)], cx, cy, 0)
    d.polygon(wing, fill=(240, 200, 120))
    for k in range(8):
        t = k / 8
        d.line(rot([(s * 24, -4), (s * (92 + 14 * t), -70 + 28 * t)], cx, cy, 0), fill=RUST, width=2)
    d.line(wing + [wing[0]], fill=K, width=3)
    d.ellipse((cx + s * 22 - 16, cy - 14, cx + s * 22 + 16, cy + 14), fill=RUST, outline=K, width=3)
d.line([(cx, cy), (cx + 10, cy + 60)], fill=K, width=3)
label(cx - 115, LABEL_Y[ROW], "VII", "samarae", "keys, still paired")

# 8 Birch (small, yellow)
cx, cy = cells[7]; ROW = cells[7][1]; cy += 40
L, Wd = 170, 70
o = rot(ovate(L, Wd, teeth=26, tooth=0.1), cx, cy, -0.5)
paint_leaf(o, (200, 190, 40), Y, pinnate_veins(cx, cy, -0.5, L, Wd, 6), (170, 130, 0), cx=cx, cy=cy)
d.line(rot([(0, 0), (0, 40)], cx, cy, -0.5), fill=K, width=4)
label(cx - 115, LABEL_Y[ROW], "VIII", "Betula", "birch, gold")

# 9 Sumac (compound leaflet spray)
cx, cy = cells[8]; ROW = cells[8][1]; cy += 95
a0 = 0.25
rach = rot([(0, 0), (0, -170)], cx, cy, a0)
d.line(rach, fill=R, width=5)
for i in range(6):
    t = 0.18 + i * 0.15
    for s in ((-1, 1) if i < 5 else (0,)):
        bx, by = rot([(0, -170 * t)], cx, cy, a0)[0]
        aa = a0 + s * 1.1 if s else a0
        lo = rot(ovate(54, 15, teeth=12, tooth=0.15), bx, by, aa)
        paint_leaf(lo, (230, 60, 30), (150, 20, 20), [(rot([(0, 0), (0, -50)], bx, by, aa), 2)], RUST, cx=bx, cy=by)
d.line(rot([(0, 0), (0, 30)], cx, cy, a0), fill=K, width=5)
label(cx - 115, LABEL_Y[ROW], "IX", "Rhus typhina", "stag's-horn sumac")

# tape strips on a few stalks
for (x, y), a in [((150, 395), 0.2), ((412, 430), -0.3), ((132, 735), 0.1), ((392, 730), 0.4), ((660, 990), -0.2)]:
    tape(x, y, a)

# scale bar + footer
d.line([(60, H - 62), (W - 60, H - 62)], fill=K, width=2)
for i in range(6):
    x = 60 + i * 40
    d.rectangle((x, H - 50, x + 40, H - 42), fill=K if i % 2 == 0 else PAPER, outline=K)
d.text((60, H - 38), "0        5 cm", font=font(FONT_SC, 18), fill=K)
d.text((W - 300, H - 48), "herb. papercolor, sheet 3", font=font(FONT_ITAL, 22), fill=K)
d.rectangle((14, 14, W - 15, H - 15), outline=K, width=4)
save(img, os.environ.get("OUT_RAW", "/tmp/claude-0/p2.png"))
