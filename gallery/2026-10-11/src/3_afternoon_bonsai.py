"""Afternoon: 'Best in Show' — a Japanese-maple bonsai in full colour before a gold-leaf
screen, on a lacquer stand on tatami. Hundreds of tiny leaves; gold dominates."""
import os, math, random
from lib import *

rnd = random.Random(2026)
img = Image.new("RGB", (W, H), Y)
d = ImageDraw.Draw(img)

# ---- gold-leaf byobu: kinpaku squares, panel folds, painted clouds and a pine
GOLD2 = (240, 190, 30)   # slightly deeper gold, dithers in a few reds
SQ = 64
for j in range(0, 760, SQ):
    for i in range(0, W, SQ):
        if (i // SQ + j // SQ) % 4 == 0:
            d.line([(i + 6, j + 6), (i + 20, j + 6)], fill=WH, width=2)
for j in range(0, 760, SQ):
    d.line([(0, j), (W, j)], fill=ORANGE, width=1)
for i in range(0, W, SQ):
    d.line([(i, 0), (i, 760)], fill=ORANGE, width=1)
# panel folds with shaded half-panels
for k, x in enumerate(range(0, W + 1, 200)):
    if k % 2 == 1:
        d.rectangle((x - 200, 0, x, 760), fill=None)
    d.line([(x, 0), (x, 760)], fill=K, width=4)
    d.line([(x + 4, 0), (x + 4, 760)], fill=RUST, width=2)
# stylised gold clouds (suyari-gasumi), outlined
def cloud(x, y, w):
    d.rounded_rectangle((x, y, x + w, y + 40), radius=20, fill=WH, outline=ORANGE, width=3)
    for k in range(int(w // 60)):
        cx = x + 30 + k * 60
        d.arc((cx - 24, y - 18, cx + 24, y + 26), 180, 360, fill=ORANGE, width=3)
cloud(30, 80, 300); cloud(470, 150, 300); cloud(-40, 560, 260); cloud(560, 600, 280)
# painted pine on the screen (in blue-black ink and green)
def screen_pine():
    pts = [(700, 760), (690, 600), (650, 480), (600, 420), (520, 380), (430, 360)]
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        d.line([(x1, y1), (x2, y2)], fill=K, width=18)
    for (x, y, w) in [(430, 350, 110), (560, 395, 100), (660, 460, 120), (690, 560, 90), (720, 330, 80)]:
        for k in range(4):
            d.chord((x - w + k * 6, y - 40 + k * 7, x + w - k * 6, y + 30 + k * 7), 180, 360,
                    fill=G if k % 2 == 0 else (20, 110, 50))
        for k in range(14):
            xx = x - w + 10 + k * (2 * w - 20) / 13
            d.line([(xx, y - 26), (xx + 6, y - 6)], fill=K, width=2)
# gold leaf crescent moon on the screen (1% tonight — almost nothing)
d.arc((90, 230, 190, 330), 100, 230, fill=WH, width=8)

# ---- tatami floor
d.rectangle((0, 760, W, H), fill=G)
for y in range(764, H, 10):
    d.line([(0, y), (W, y)], fill=Y, width=1)
d.rectangle((0, 752, W, 770), fill=K)            # tokonoma edge, lacquered
d.rectangle((0, 1000, W, 1022), fill=K)           # tatami heri (border)
for x in range(0, W, 30):
    d.line([(x, 1004), (x + 15, 1018)], fill=B, width=3)

# ---- lacquer stand
sx0, sx1, sy = 120, 680, 900
d.polygon([(sx0, sy), (sx1, sy), (sx1 + 20, sy + 30), (sx0 - 20, sy + 30)], fill=K)
d.line([(sx0 - 20, sy + 30), (sx1 + 20, sy + 30)], fill=R, width=4)
d.line([(sx0, sy + 3), (sx1, sy + 3)], fill=R, width=2)
for x in (sx0 + 10, sx1 - 40):
    d.rectangle((x, sy + 30, x + 30, sy + 90), fill=K)
    d.arc((x - 10, sy + 70, x + 40, sy + 110), 180, 360, fill=R, width=3)
d.rectangle((sx0 - 20, sy + 30, sx1 + 20, sy + 44), fill=K)
d.line([(sx0 - 20, sy + 44), (sx1 + 20, sy + 44)], fill=R, width=2)

# ---- pot: shallow oval, blue glaze with drips
px0, px1, ptop, pbot = 200, 600, 820, 892
d.rectangle((px0 + 20, pbot - 2, px0 + 60, pbot + 10), fill=K)
d.rectangle((px1 - 60, pbot - 2, px1 - 20, pbot + 10), fill=K)
d.rounded_rectangle((px0, ptop, px1, pbot), radius=30, fill=B, outline=K, width=4)
d.ellipse((px0 - 6, ptop - 18, px1 + 6, ptop + 18), fill=B, outline=K, width=4)
d.ellipse((px0 + 10, ptop - 10, px1 - 10, ptop + 10), fill=K)
# moss + soil
for _ in range(220):
    x = rnd.uniform(px0 + 20, px1 - 20); y = ptop + rnd.uniform(-8, 6)
    r = rnd.uniform(3, 7)
    d.ellipse((x - r, y - r, x + r, y + r), fill=rnd.choice([G, G, OLIVE, (20, 80, 30)]))
# glaze drips and highlights
for k in range(0, 13):
    x = px0 + 40 + k * 26
    d.ellipse((x - 9, ptop + 34, x + 9, ptop + 52), outline=WH, width=2)
    d.line([(x - 9, ptop + 43), (x + 9, ptop + 43)], fill=WH, width=2)
d.line([(px0 + 20, ptop + 26), (px1 - 20, ptop + 26)], fill=WH, width=2)
d.line([(px0 + 24, ptop + 60), (px1 - 24, ptop + 60)], fill=WH, width=2)
d.arc((px0 + 30, ptop + 20, px0 + 120, pbot - 6), 120, 220, fill=WH, width=4)
# chop mark on pot
d.rectangle((px1 - 70, ptop + 34, px1 - 48, ptop + 56), outline=WH, width=2)

# ---- tree
leaves = []
def limb(x, y, ang, length, width, depth, pad_bias=0):
    """Draw a tapering limb as a polygon with bark lines; collect pad centres."""
    segs = 6
    pts_l, pts_r = [], []
    cx, cy, a = x, y, ang
    path = [(cx, cy, width)]
    for s in range(segs):
        a += rnd.uniform(-0.25, 0.25)
        cx += length / segs * math.cos(a); cy += length / segs * math.sin(a)
        path.append((cx, cy, width * (1 - 0.55 * (s + 1) / segs)))
    for (x1, y1, w1), (x2, y2, w2) in zip(path, path[1:]):
        nx, ny = -(y2 - y1), (x2 - x1); n = math.hypot(nx, ny) or 1; nx /= n; ny /= n
        pts_l.append((x1 + nx * w1 / 2, y1 + ny * w1 / 2)); pts_r.append((x1 - nx * w1 / 2, y1 - ny * w1 / 2))
    pts_l.append((path[-1][0], path[-1][1]))
    d.polygon(pts_l + pts_r[::-1], fill=K, outline=K)
    # bark lines
    for (x1, y1, w1), (x2, y2, w2) in zip(path, path[1:]):
        if w1 > 10:
            pass
            d.line([(x1 - 0.35 * w1, y1), (x2 - 0.35 * w2, y2)], fill=ORANGE, width=2)
    ex, ey, ew = path[-1]
    if depth == 0:
        leaves.append((ex, ey)); return
    for da in (-0.55, 0.5):
        limb(ex, ey, a + da + rnd.uniform(-0.2, 0.2), length * rnd.uniform(0.55, 0.72), ew * 0.95, depth - 1)
    if depth <= 2:
        leaves.append((ex, ey))

# nebari roots
for dx, a in [(-70, math.pi + 0.2), (-30, math.pi - 0.3), (40, -0.2), (80, 0.15)]:
    d.polygon([(400 + dx * 0.3, ptop - 30), (400 + dx * 1.8, ptop + 2), (400 + dx * 0.2, ptop + 2)], fill=K, outline=K)
# trunk: S-curve moyogi
trunk = [(400, ptop), (360, 740), (330, 660), (370, 580), (430, 520), (440, 450), (400, 390)]
widths = [80, 70, 60, 50, 40, 30, 22]
for (x1, y1), (x2, y2), w1, w2 in zip(trunk, trunk[1:], widths, widths[1:]):
    nx, ny = -(y2 - y1), (x2 - x1); n = math.hypot(nx, ny); nx /= n; ny /= n
    d.polygon([(x1 + nx * w1 / 2, y1 + ny * w1 / 2), (x2 + nx * w2 / 2, y2 + ny * w2 / 2),
               (x2 - nx * w2 / 2, y2 - ny * w2 / 2), (x1 - nx * w1 / 2, y1 - ny * w1 / 2)], fill=K)
    d.ellipse((x2 - w2 / 2, y2 - w2 / 2, x2 + w2 / 2, y2 + w2 / 2), fill=K)
    for k in (-0.1, 0.15):
        d.line([(x1 + nx * w1 * k, y1 + ny * w1 * k), (x2 + nx * w2 * k, y2 + ny * w2 * k)], fill=RUST, width=2)
    d.line([(x1 - nx * w1 * 0.38, y1 - ny * w1 * 0.38), (x2 - nx * w2 * 0.38, y2 - ny * w2 * 0.38)], fill=ORANGE, width=3)
# primary branches from the trunk
limb(335, 660, math.pi + 0.1, 120, 24, 2)
limb(370, 585, -0.05, 130, 22, 2)
limb(430, 480, math.pi + 0.3, 90, 16, 2)
limb(440, 450, -0.35, 90, 14, 2)
limb(400, 395, -math.pi / 2 - 0.1, 60, 12, 2)

# foliage pads: shadow mass, then many small leaves, lit from upper left
pads = leaves[:]
for x, y in pads:
    d.ellipse((x - 44, y - 20, x + 44, y + 26), fill=RUST, outline=K, width=2)
for x, y in pads:
    for _ in range(40):
        lx = x + rnd.gauss(0, 26); ly = y + rnd.gauss(-4, 11)
        up = (y - ly) / 40 - (lx - x) / 120
        col = rnd.choices([R, ORANGE, Y, RUST], [5, 3 + 3 * max(0, up), 1 + 3 * max(0, up), 2])[0]
        draw_maple(d, lx, ly, rnd.uniform(12, 18), rnd.uniform(-0.8, 0.8), col,
                   outline=K if rnd.random() < 0.6 else RUST, ow=1, seed=rnd.randint(0, 99999))

# fallen leaves on stand and tatami
for _ in range(16):
    x = rnd.uniform(100, 720); y = rnd.choice([rnd.uniform(895, 905), rnd.uniform(1040, 1180)])
    draw_maple(d, x, y, rnd.uniform(12, 22), rnd.uniform(0, 6.28), rnd.choice([R, ORANGE, Y]),
               outline=K, ow=2, seed=rnd.randint(0, 9999))

# ---- prize rosette + card
rx, ry = 640, 1080
for k in range(16):
    a = k * math.pi / 8
    d.polygon([(rx, ry), (rx + 56 * math.cos(a - 0.2), ry + 56 * math.sin(a - 0.2)),
               (rx + 56 * math.cos(a + 0.2), ry + 56 * math.sin(a + 0.2))], fill=B, outline=K)
d.polygon([(rx - 30, ry + 30), (rx - 50, ry + 110), (rx - 30, ry + 96), (rx - 14, ry + 112), (rx, ry + 36)], fill=B, outline=K)
d.polygon([(rx + 30, ry + 30), (rx + 50, ry + 110), (rx + 30, ry + 96), (rx + 14, ry + 112), (rx, ry + 36)], fill=B, outline=K)
d.ellipse((rx - 34, ry - 34, rx + 34, ry + 34), fill=Y, outline=K, width=3)
f = font(FONT_SERIF_B, 30)
d.text((rx - d.textlength("1st", font=f) / 2, ry - 20), "1st", font=f, fill=K)
# card
d.polygon([(80, 1060), (360, 1040), (372, 1140), (92, 1160)], fill=WH, outline=K)
d.text((110, 1062), "Acer palmatum 'Deshojo'", font=font(FONT_ITAL, 24), fill=K)
d.text((108, 1094), "est. 40 yrs · moyogi style", font=font(FONT_SC, 22), fill=K)
d.text((106, 1124), "fruit & foliage, autumn 2026", font=font(FONT_SC, 20), fill=R)

d.rectangle((0, 0, W - 1, H - 1), outline=K, width=12)
save(img, os.environ.get("OUT_RAW", "/tmp/claude-0/p3.png"))
