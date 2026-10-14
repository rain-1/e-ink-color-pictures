"""ISTI MIRANT STELLA — the Great Gatehouse of Battle Abbey, under the comet.

A night engraving: black ground, everything cut in light. Stonework is drawn as
coursed lines, the shadowed faces with sparser lines; the comet's tail is a fan of
fine streamers like the stitched one in the Tapestry. Palette colours only (--dither none).
"""
import math, os, random
from PIL import Image, ImageDraw, ImageFont

W, H = 400, 600
K, Wh, Rd, Yl, Bl, Gr = (0, 0, 0), (255, 255, 255), (0xE0, 0x1B, 0x24), (0xF5, 0xD4, 0x00), (0x12, 0x3D, 0xB0), (0x1E, 0x9B, 0x3C)
R = random.Random(1066 + 960)
im = Image.new("RGB", (W, H), K)
d = ImageDraw.Draw(im)
d.fontmode = "1"

# ------------------------------------------------------------------ stars: a dense, graded field, thicker in a faint band
for i in range(1400):
    x, y = R.uniform(0, W), R.uniform(0, 420) ** 1.0
    band = math.exp(-((x * 0.6 + y - 330) / 70) ** 2)
    if R.random() > 0.25 + 0.75 * band:
        continue
    m = R.random()
    if m < 0.85:
        d.point((x, y), fill=Wh if R.random() < 0.8 else Bl)
    elif m < 0.97:
        d.rectangle([x, y, x + 1, y + 1], fill=Wh)
    else:
        d.line([x - 3, y, x + 3, y], fill=Wh); d.line([x, y - 3, x, y + 3], fill=Wh)
        d.point((x, y), fill=Yl)

# ------------------------------------------------------------------ the comet: head upper right, tail streaming up-left
CX, CY = 282, 132
for k in range(46):
    spread = (k - 23) / 23
    L = R.uniform(150, 290) * (1 - 0.45 * abs(spread))
    a0 = math.radians(205 + 16 * spread)
    pts = []
    for s in range(40):
        t = s / 39
        ang = a0 + 0.25 * t * spread + 0.05 * math.sin(t * 6 + k)
        pts.append((CX + L * t * math.cos(ang), CY + L * t * math.sin(ang) + 20 * t * t))
    col = Yl if abs(spread) < 0.3 else Wh if abs(spread) < 0.75 else Rd
    # dashed toward the end so the tail fades
    for s in range(39):
        t = s / 39
        if t > 0.35 and R.random() < t * 0.9:
            continue
        d.line([pts[s], pts[s + 1]], fill=col)
# the head: a stitched-looking star with eight rays
for k in range(8):
    a = k / 8 * 2 * math.pi + 0.2
    L = 16 if k % 2 == 0 else 9
    d.line([CX, CY, CX + L * math.cos(a), CY + L * math.sin(a)], fill=Yl, width=2)
d.ellipse([CX - 6, CY - 6, CX + 6, CY + 6], fill=Wh, outline=Yl)
d.ellipse([CX - 2, CY - 2, CX + 2, CY + 2], fill=Yl)

# ------------------------------------------------------------------ the downland horizon
HZ = 470
for x in range(W):
    y = HZ - 10 * math.sin(x / 70) - 4 * math.sin(x / 23)
    d.line([x, y, x, H], fill=K)
# distant trees along the horizon, as tiny silhouettes picked out by starlight
for x in range(0, W, 5):
    y = HZ - 10 * math.sin(x / 70) - 4 * math.sin(x / 23)
    if R.random() < 0.6:
        r = R.uniform(3, 7)
        d.arc([x - r, y - r * 1.6, x + r, y + r * 0.4], 190, 350, fill=Bl)

# ------------------------------------------------------------------ the Great Gatehouse
GX, BASE = 200, 500


def coursed(x0, y0, x1, y1, lit=True, step=4):
    """Fill a block with coursed stone lines; joints staggered every other course."""
    for y in range(int(y0) + 2, int(y1), step):
        if not lit and (y // step) % 2:
            continue
        d.line([x0 + 1, y, x1 - 1, y], fill=Wh if lit else Bl)
        off = 6 if (y // step) % 2 else 0
        if lit:
            for jx in range(int(x0) + 3 + off, int(x1) - 1, 12):
                d.point((jx, y + 1), fill=Wh); d.point((jx, y + 2), fill=Wh)


def crenels(x0, x1, y, h=6, w=6, col=Wh):
    for cx in range(int(x0), int(x1), 2 * w):
        d.rectangle([cx, y - h, min(cx + w - 1, x1), y], fill=col)
    d.line([x0, y, x1, y], fill=col)


# side wings (lower, set back)
for (x0, x1, lit) in [(GX - 190, GX - 92, False), (GX + 92, GX + 190, True)]:
    d.rectangle([x0, BASE - 112, x1, BASE], fill=K)
    coursed(x0, BASE - 112, x1, BASE, lit)
    crenels(x0, x1, BASE - 112, col=Wh if lit else Bl)
    d.rectangle([x0, BASE - 112, x1, BASE], outline=Wh if lit else Bl)
    for wx in range(int(x0) + 14, int(x1) - 10, 28):
        d.rectangle([wx, BASE - 82, wx + 8, BASE - 58], fill=K, outline=Wh if lit else Bl)
        d.polygon([(wx, BASE - 82), (wx + 4, BASE - 90), (wx + 8, BASE - 82)], fill=K, outline=Wh if lit else Bl)
# the main block
x0, x1, top = GX - 92, GX + 92, BASE - 188
d.rectangle([x0, top, x1, BASE], fill=K)
coursed(x0, top, GX, BASE, lit=False)
coursed(GX, top, x1, BASE, lit=True)
d.rectangle([x0, top, x1, BASE], outline=Wh)
crenels(x0, x1, top)
# string course
d.line([x0, top + 46, x1, top + 46], fill=Yl, width=2)
# octagonal corner turrets, taller
for tx, lit in [(x0, False), (x1, True)]:
    ttop = top - 52
    d.rectangle([tx - 14, ttop, tx + 14, BASE], fill=K)
    coursed(tx - 14, ttop, tx, BASE, lit=False, step=4)
    coursed(tx, ttop, tx + 14, BASE, lit=True, step=4)
    d.line([tx, ttop, tx, BASE], fill=Wh)
    d.rectangle([tx - 14, ttop, tx + 14, BASE], outline=Wh)
    crenels(tx - 16, tx + 16, ttop, h=7, w=5)
    for sy in range(ttop + 22, BASE - 40, 34):  # arrow slits
        d.rectangle([tx - 2, sy, tx + 2, sy + 12], fill=K)
        d.line([tx - 4, sy + 6, tx + 4, sy + 6], fill=K)
# the great pointed arch and the small postern beside it
AW, AH = 96, 124
ax0, ax1 = GX - AW / 2 - 10, GX + AW / 2 - 10
d.rectangle([ax0, BASE - AH + 44, ax1, BASE], fill=K)
d.pieslice([ax0, BASE - AH, ax1 + AW * 0.3, BASE - AH + 96], 180, 270, fill=K)
d.pieslice([ax0 - AW * 0.3, BASE - AH, ax1, BASE - AH + 96], 270, 360, fill=K)
for r in (0, 4, 8):  # moulded orders of the arch
    d.arc([ax0 - r, BASE - AH - r, ax1 + AW * 0.3 + r, BASE - AH + 96 + r], 180, 270, fill=Wh)
    d.arc([ax0 - AW * 0.3 - r, BASE - AH - r, ax1 + r, BASE - AH + 96 + r], 270, 360, fill=Wh)
    d.line([ax0 - r, BASE - AH + 48, ax0 - r, BASE], fill=Wh)
    d.line([ax1 + r, BASE - AH + 48, ax1 + r, BASE], fill=Wh)
# through the arch: the abbey precinct, a lantern-lit window far off and the ground
d.line([ax0 + 2, BASE - 14, ax1 - 2, BASE - 14], fill=Bl)
for k in range(6):
    d.line([ax0 + 6 + k * 14, BASE - 14, GX - 10 + (k - 2.5) * 2, BASE - 46], fill=Bl)
d.rectangle([GX - 14, BASE - 64, GX - 6, BASE - 52], fill=Yl)
# postern
px = GX + 62
d.rectangle([px - 9, BASE - 52, px + 9, BASE], fill=K, outline=Wh)
d.pieslice([px - 9, BASE - 62, px + 9, BASE - 42], 180, 360, fill=K, outline=Wh)
# upper windows: three lit, tracery in black
for wx in (GX - 58, GX - 10, GX + 38):
    wy = top + 14
    d.rectangle([wx, wy + 6, wx + 20, wy + 30], fill=Yl)
    d.pieslice([wx, wy - 4, wx + 20, wy + 16], 180, 360, fill=Yl)
    d.line([wx + 10, wy, wx + 10, wy + 30], fill=K, width=2)
    d.line([wx, wy + 16, wx + 20, wy + 16], fill=K)
    d.rectangle([wx - 1, wy - 5, wx + 21, wy + 31], outline=Wh)
# lit windows cast a little light on the grass below the gate
for i in range(140):
    x = R.uniform(GX - 120, GX + 120)
    y = R.uniform(BASE + 2, BASE + 40)
    if R.random() < 1 - abs(x - GX) / 130:
        d.line([x, y, x + R.uniform(-1, 1), y - R.uniform(2, 5)], fill=Yl if R.random() < 0.3 else Gr)

# ------------------------------------------------------------------ foreground grass in starlight
for i in range(1100):
    x = R.uniform(0, W)
    y = R.uniform(BASE + 4, H - 50)
    t = (y - BASE) / (H - BASE)
    ln = 2 + 10 * t
    col = Gr if R.random() < 0.6 else Bl
    d.line([x, y, x + R.uniform(-3, 3), y - ln], fill=col)

# ------------------------------------------------------------------ inscription, as on the Tapestry
f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 17)
s = "ISTI MIRANT STELLA"
x = (W - d.textlength(s, font=f)) / 2
d.text((x, H - 46), s, font=f, fill=Yl)
f2 = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf", 13)
s2 = "these men wonder at the star  ·  1066 – 2026"
d.text(((W - d.textlength(s2, font=f2)) / 2, H - 24), s2, font=f2, fill=Wh)

im.save(os.environ.get("OUT_RAW", "raw5.png"))
