"""Chaekgeori — a scholar's bookshelf screen. Twelve compartments, each a little still life:
tied books, a celadon vase of chrysanthemums, persimmons, brushes, a scroll, a coral branch,
spectacles, a peacock feather. Wood in yellow with drawn grain; tones by Bayer screen."""
import math, random
import numpy as np
from PIL import Image, ImageDraw
from kit import *

random.seed(1009)
img = Image.new("RGB", (W, H), K)
a = to_arr(img)

X0, Y0, CW, CH, COLS, ROWS = 14, 22, 124, 136, 3, 4
WALL = 7

def cell(c, r):
    x, y = X0 + c * CW, Y0 + r * CH
    return x + WALL, y + WALL, x + CW - WALL, y + CH - WALL

# compartment interiors: back wall white, left wall + floor screened yellow (reverse perspective)
for r in range(ROWS):
    for c in range(COLS):
        x0, y0, x1, y1 = cell(c, r)
        a[y0:y1, x0:x1] = WH
        # papered back wall: a small diamond lattice of blue points
        for yy in range(y0 + 4, y1 - 14, 8):
            for xx in range(x0 + 16 + ((yy - y0) // 8 % 2) * 4, x1 - 2, 8):
                a[yy, xx] = B
        side = mask_of(lambda m: m.polygon([(x0, y0), (x0 + 12, y0 + 10), (x0 + 12, y1 - 14), (x0, y1)], fill=255))
        screen(a, side, WH, Y, 0.5)
        floor = mask_of(lambda m: m.polygon([(x0, y1), (x0 + 12, y1 - 14), (x1, y1 - 14), (x1, y1)], fill=255))
        screen(a, floor, Y, K, 0.18)
img = Image.fromarray(a); d = ImageDraw.Draw(img)

# frame wood with grain
for r in range(ROWS + 1):
    y = Y0 + r * CH
    d.rectangle([X0, y - WALL, X0 + COLS * CW, y + WALL], fill=Y)
for c in range(COLS + 1):
    x = X0 + c * CW
    d.rectangle([x - WALL, Y0 - WALL, x + WALL, Y0 + ROWS * CH + WALL], fill=Y)
for r in range(ROWS + 1):
    y = Y0 + r * CH
    for k in range(3):
        yy = y - 4 + k * 4
        pts = [(x, yy + math.sin(x / 9 + r + k) * 1.2) for x in range(X0 - WALL, X0 + COLS * CW + WALL, 3)]
        d.line(pts, fill=K, width=1)
for c in range(COLS + 1):
    x = X0 + c * CW
    for k in range(2):
        xx = x - 3 + k * 6
        pts = [(xx + math.sin(y / 11 + c + k) * 1.3, y) for y in range(Y0 - WALL, Y0 + ROWS * CH + WALL, 3)]
        d.line(pts, fill=K, width=1)
for r in range(ROWS):
    for c in range(COLS):
        x0, y0, x1, y1 = cell(c, r)
        d.rectangle([x0, y0, x1, y1], outline=K, width=2)
        # brass corner fittings
        for (px, py) in ((x0, y0), (x1, y0), (x0, y1), (x1, y1)):
            d.rectangle([px - 4, py - 4, px + 4, py + 4], fill=Y, outline=K)
            d.point((px, py), fill=K)

# ---------- objects ----------
COVERS = [B, G, R, Y, B, G, WH]

def book_flat(x, y, w, h, col, tie=R, depth=10):
    """A book lying flat, front edge at y (bottom). Seen slightly from above-left."""
    d.polygon([(x, y - h), (x + depth, y - h - depth * .6), (x + w + depth, y - h - depth * .6), (x + w, y - h)], fill=col, outline=K)
    d.rectangle([x, y - h, x + w, y], fill=WH, outline=K)
    for k in range(1, h - 1, 2):  # page edges
        d.line([(x + 2, y - h + k), (x + w - 2, y - h + k)], fill=K if k % 4 == 1 else WH, width=1)
    d.rectangle([x, y - h, x + w, y - h + 2], fill=col)
    d.rectangle([x, y - 2, x + w, y], fill=col)
    d.line([(x + w * .3, y - h - depth * .6 + 1), (x + w * .3, y)], fill=tie, width=2)
    d.line([(x + w * .7, y - h - depth * .6 + 1), (x + w * .7, y)], fill=tie, width=2)

def stack(x, y, n, w, seed):
    rnd = random.Random(seed)
    for i in range(n):
        h = rnd.choice([7, 8, 9, 10])
        dx = rnd.randint(-4, 4)
        book_flat(x + dx, y, w + rnd.randint(-6, 4), h, rnd.choice(COVERS), tie=rnd.choice([R, K, Y]))
        y -= h + 1
    return y

def upright(x, y, n, seed):
    rnd = random.Random(seed)
    for i in range(n):
        w, h = rnd.randint(7, 11), rnd.randint(46, 62)
        col = rnd.choice(COVERS)
        d.rectangle([x, y - h, x + w, y], fill=col, outline=K)
        d.rectangle([x + 1, y - h + 6, x + w - 1, y - h + 16], fill=WH, outline=K)  # title slip
        d.line([(x + 3, y - h + 9), (x + 3, y - h + 13)], fill=K)
        for k in (0.35, 0.65):
            d.line([(x, y - h * k), (x + w, y - h * k)], fill=Y if col != Y else K, width=1)
        x += w + 1
    return x

def vase(cx, y, h, wmax, body=G, band=WH, flowers=None):
    prof = lambda t: (0.28 + 0.72 * math.sin(math.pi * min(1, t * 1.15)) ** 1.4) * (1 - 0.55 * max(0, t - .75) / .25)
    left, right = [], []
    for i in range(41):
        t = i / 40
        r = wmax / 2 * max(0.22, prof(t))
        left.append((cx - r, y - t * h)); right.append((cx + r, y - t * h))
    poly = left + right[::-1]
    if flowers:
        flowers(cx, y - h)
    d.polygon(poly, fill=body, outline=K)
    for t, col in ((0.18, band), (0.62, band), (0.64, K)):
        r = wmax / 2 * max(0.22, prof(t))
        d.line([(cx - r + 1, y - t * h), (cx + r - 1, y - t * h)], fill=col, width=2)
    # crane-and-cloud inlay suggested by small white marks
    for k in range(5):
        t = .3 + k * .06
        r = wmax / 2 * prof(t) * .6
        d.arc([cx - r, y - t * h - 3, cx + r * .2, y - t * h + 3], 180, 360, fill=WH)
    d.line([(cx - wmax * .14, y - h * .35), (cx - wmax * .14, y - h * .55)], fill=WH)
    d.rectangle([cx - wmax * .2, y - 3, cx + wmax * .2, y], fill=K)

def chrysanth(cx, cy, r, col=Y):
    for i in range(16):
        t = i / 16 * 2 * math.pi
        d.line([(cx, cy), (cx + r * math.cos(t), cy + r * math.sin(t) * .8)], fill=col, width=3)
    for i in range(16):
        t = (i + .5) / 16 * 2 * math.pi
        d.line([(cx + r * .3 * math.cos(t), cy + r * .3 * math.sin(t)), (cx + r * math.cos(t), cy + r * .8 * math.sin(t))], fill=K, width=1)
    d.ellipse([cx - r * .3, cy - r * .3, cx + r * .3, cy + r * .3], fill=R, outline=K)

def mums(top_x, top_y):
    pts = [(-30, -40, 11), (-6, -58, 13), (20, -44, 11), (34, -18, 9), (-36, -10, 9), (6, -28, 10)]
    for dx, dy, r in pts:
        d.line([(top_x, top_y + 6), (top_x + dx, top_y + dy)], fill=G, width=2)
        d.line([(top_x + dx * .5, top_y + dy * .5), (top_x + dx * .5 - 7, top_y + dy * .5 - 2)], fill=G, width=4)
    for i, (dx, dy, r) in enumerate(pts):
        chrysanth(top_x + dx, top_y + dy, r, WH if i in (2, 4) else Y)

def persimmons(cx, y, n=5):
    d.ellipse([cx - 40, y - 10, cx + 40, y + 2], fill=WH, outline=K)
    d.rectangle([cx - 14, y - 4, cx + 14, y], fill=B)
    d.ellipse([cx - 32, y - 14, cx + 32, y - 4], fill=B, outline=K)
    spots = [(-18, -24), (0, -26), (18, -24), (-9, -42), (9, -42)][:n]
    for dx, dy in spots:
        x0, y0 = cx + dx, y + dy
        m = mask_of(lambda mm: mm.ellipse([x0 - 12, y0 - 10, x0 + 12, y0 + 11], fill=255))
        arr = np.array(img)
        yy, xx = np.mgrid[0:H, 0:W]
        shade = np.clip(0.12 + 0.45 * ((xx - x0 + 5) ** 2 + (yy - y0 + 5) ** 2) / 200, 0, 0.95)
        screen(arr, m, Y, R, shade)
        img.paste(Image.fromarray(arr))
        d.ellipse([x0 - 12, y0 - 10, x0 + 12, y0 + 11], outline=K)
        for k in range(4):
            t = k * math.pi / 2 + .4
            d.line([(x0, y0 - 9), (x0 + 6 * math.cos(t), y0 - 9 + 3 * math.sin(t))], fill=G, width=3)
        d.line([(x0, y0 - 10), (x0 + 1, y0 - 15)], fill=K, width=2)
        d.point((x0 - 5, y0 - 3), fill=WH); d.point((x0 - 4, y0 - 4), fill=WH)

def brushpot(cx, y):
    for i, (dx, tip) in enumerate([(-10, -78), (-3, -88), (5, -82), (12, -72), (-15, -66)]):
        x1 = cx + dx * 1.8
        d.line([(cx + dx * .5, y - 20), (x1, y + tip)], fill=Y if i % 2 else R, width=3)
        d.line([(cx + dx * .5, y - 20), (x1, y + tip)], fill=K, width=1)
        d.polygon([(x1 - 3, y + tip), (x1 + 3, y + tip), (x1 + dx * .1, y + tip - 12)], fill=K)
    d.rectangle([cx - 16, y - 46, cx + 16, y], fill=B, outline=K, width=2)
    d.ellipse([cx - 16, y - 50, cx + 16, y - 42], fill=K, outline=K)
    for k in range(6):  # bamboo pattern
        d.line([(cx - 12 + k * 5, y - 40), (cx - 12 + k * 5, y - 6)], fill=WH if k % 2 else B, width=1)
    d.line([(cx - 16, y - 24), (cx + 16, y - 24)], fill=WH, width=2)

def scroll(x, y, L, col=R):
    d.rectangle([x, y - 12, x + L, y], fill=WH, outline=K)
    d.ellipse([x + L - 6, y - 13, x + L + 6, y + 1], fill=col, outline=K)
    d.ellipse([x - 6, y - 13, x + 6, y + 1], fill=col, outline=K)
    d.line([(x + 10, y - 6), (x + L - 10, y - 6)], fill=K)
    d.line([(x + L * .5, y - 12), (x + L * .5 + 6, y + 6)], fill=Y, width=2)

def coral(x, y, depth=0, ang=-math.pi / 2, L=26):
    if depth > 4: return
    x1, y1 = x + L * math.cos(ang), y + L * math.sin(ang)
    d.line([(x, y), (x1, y1)], fill=R, width=max(1, 5 - depth))
    coral(x1, y1, depth + 1, ang - .45, L * .72)
    coral(x1, y1, depth + 1, ang + .5, L * .68)

def spectacles(cx, y):
    for dx in (-11, 11):
        d.ellipse([cx + dx - 9, y - 16, cx + dx + 9, y], outline=K, width=2)
        d.arc([cx + dx - 6, y - 13, cx + dx + 2, y - 5], 180, 270, fill=B, width=1)
    d.arc([cx - 4, y - 12, cx + 4, y - 4], 180, 360, fill=K, width=2)

def feather_vase(cx, y):
    for k, ang in enumerate((-.25, .1, .35)):
        x1, y1 = cx + 70 * math.sin(ang), y - 40 - 70 * math.cos(ang)
        d.line([(cx, y - 30), (x1, y1)], fill=K, width=1)
        for j in range(12):
            t = j / 12
            px, py = cx + (x1 - cx) * t, y - 30 + (y1 - y + 30) * t
            d.line([(px - 5, py + 3), (px, py)], fill=G); d.line([(px + 5, py + 3), (px, py)], fill=G)
        d.ellipse([x1 - 7, y1 - 9, x1 + 7, y1 + 7], fill=G, outline=K)
        d.ellipse([x1 - 4, y1 - 5, x1 + 4, y1 + 3], fill=B)
        d.ellipse([x1 - 2, y1 - 3, x1 + 2, y1 + 1], fill=Y)
    vase(cx, y, 40, 26, body=WH, band=B)

def inkstone(x, y):
    d.rectangle([x, y - 8, x + 34, y], fill=K, outline=K)
    d.polygon([(x, y - 8), (x + 6, y - 13), (x + 40, y - 13), (x + 34, y - 8)], fill=B, outline=K)
    d.ellipse([x + 22, y - 12, x + 32, y - 9], fill=K)
    d.rectangle([x + 40, y - 24, x + 46, y], fill=K)  # ink stick
    d.text((x + 40, y - 22), "", fill=Y)
    d.line([(x + 43, y - 22), (x + 43, y - 4)], fill=Y)

def watch(cx, y):
    d.ellipse([cx - 13, y - 28, cx + 13, y - 2], fill=Y, outline=K, width=2)
    d.ellipse([cx - 9, y - 24, cx + 9, y - 6], fill=WH, outline=K)
    for i in range(12):
        t = i / 12 * 2 * math.pi
        d.point((cx + 7 * math.cos(t), y - 15 + 7 * math.sin(t)), fill=K)
    d.line([(cx, y - 15), (cx + 4, y - 20)], fill=K); d.line([(cx, y - 15), (cx - 2, y - 11)], fill=R)
    d.ellipse([cx - 3, y - 34, cx + 3, y - 28], outline=K, width=2)

def floor(c, r):
    x0, y0, x1, y1 = cell(c, r)
    return x0, y1 - 6, x1

# row 0: chrysanthemum vase | books + spectacles | coral in a pot
x0, fy, x1 = floor(0, 0); vase(x0 + 58, fy, 58, 44, flowers=mums)
x0, fy, x1 = floor(1, 0); t = stack(x0 + 14, fy, 5, 58, 1); upright(x0 + 82, fy, 2, 3); spectacles(x0 + 44, t)
x0, fy, x1 = floor(2, 0); coral(x0 + 56, fy - 26); d.rectangle([x0 + 38, fy - 26, x0 + 74, fy], fill=WH, outline=K, width=2)
for k in range(4): d.line([(x0 + 40 + k * 9, fy - 22), (x0 + 44 + k * 9, fy - 4)], fill=B, width=2)
# row 1: tall stack | persimmons | upright books + scroll
x0, fy, x1 = floor(0, 1); t = stack(x0 + 18, fy, 9, 62, 7); watch(x0 + 50, t)
x0, fy, x1 = floor(1, 1); persimmons(x0 + 56, fy)
x0, fy, x1 = floor(2, 1); upright(x0 + 14, fy, 7, 5); scroll(x0 + 18, fy - 64, 76)
# row 2: brush pot + inkstone | peacock feathers | books
x0, fy, x1 = floor(0, 2); brushpot(x0 + 36, fy); inkstone(x0 + 58, fy)
x0, fy, x1 = floor(1, 2); feather_vase(x0 + 56, fy)
x0, fy, x1 = floor(2, 2); t = stack(x0 + 12, fy, 4, 50, 11); t = stack(x0 + 52, fy, 6, 40, 13)
# row 3: scrolls in a jar | books + persimmon | chrysanthemum pot (white)
x0, fy, x1 = floor(0, 3)
for k in range(4):
    d.line([(x0 + 40 + k * 8, fy - 30), (x0 + 28 + k * 14, fy - 92 + k * 6)], fill=WH, width=6)
    d.line([(x0 + 40 + k * 8, fy - 30), (x0 + 28 + k * 14, fy - 92 + k * 6)], fill=K, width=1)
    d.ellipse([x0 + 24 + k * 14, fy - 96 + k * 6, x0 + 32 + k * 14, fy - 88 + k * 6], fill=[R, Y, B, G][k], outline=K)
vase(x0 + 58, fy, 46, 60, body=B, band=Y)
x0, fy, x1 = floor(1, 3); t = stack(x0 + 10, fy, 3, 54, 17); upright(x0 + 70, fy, 3, 19); persimmons(x0 + 38, t + 4, n=1)
x0, fy, x1 = floor(2, 3); vase(x0 + 58, fy, 52, 40, body=WH, band=R, flowers=mums)

d.rectangle([0, 0, W - 1, H - 1], outline=K, width=4)
save(img)
