"""Evening: 'The Dragon Boat at Dusk' — a Heian leaf-viewing party on a temple pond,
in the manner of shin-hanga twilight prints: graded sky, lit windows, broken reflections."""
import os, math, random
import numpy as np
from lib import *

rnd = random.Random(1110)
img = Image.new("RGB", (W, H), K)
d = ImageDraw.Draw(img)
HZ = 560  # waterline

# ---- sky
vgrad(img, (0, 0, W, HZ), [(0, (15, 25, 90)), (0.35, (40, 60, 160)), (0.62, (70, 80, 175)),
                            (0.82, (235, 110, 60)), (1, (250, 200, 40))])
# a one-day moon: the thinnest possible arc, low in the west
d.arc((120, 330, 170, 380), 110, 200, fill=WH, width=4)
# early stars
for _ in range(40):
    x, y = rnd.uniform(20, W - 20), rnd.uniform(20, 220)
    r = rnd.choice([1.5, 1.5, 2.5])
    d.ellipse((x - r, y - r, x + r, y + r), fill=WH)
# thin long clouds lit from below
for y, x0, x1 in [(300, 380, 780), (330, 460, 820), (260, -20, 240), (410, 200, 560)]:
    d.rounded_rectangle((x0, y, x1, y + 9), radius=4, fill=(30, 30, 80))
    d.line([(x0 + 10, y + 9), (x1 - 10, y + 9)], fill=R, width=2)

# ---- far hills and the shore
def ridge(y0, amp, freq, seed):
    r = random.Random(seed); ph = [r.random() * 6 for _ in range(3)]
    return [(x, y0 - amp * (0.6 * math.sin(x * freq + ph[0]) + 0.4 * math.sin(x * freq * 2.7 + ph[1])))
            for x in range(0, W + 1, 4)]
d.polygon(ridge(470, 40, 0.009, 3) + [(W, HZ), (0, HZ)], fill=(25, 35, 100))
d.polygon(ridge(520, 22, 0.02, 5) + [(W, HZ), (0, HZ)], fill=K)

# temple hall on the far shore, right
hx, hy = 520, HZ - 10
d.rectangle((hx, hy - 70, hx + 220, hy), fill=K)
d.polygon([(hx - 40, hy - 64), (hx + 260, hy - 64), (hx + 210, hy - 110), (hx + 10, hy - 110)], fill=K)
d.polygon([(hx + 30, hy - 106), (hx + 190, hy - 106), (hx + 150, hy - 140), (hx + 70, hy - 140)], fill=K)
d.line([(hx - 40, hy - 64), (hx - 54, hy - 76)], fill=K, width=6)
d.line([(hx + 260, hy - 64), (hx + 274, hy - 76)], fill=K, width=6)
for i in range(7):
    x = hx + 12 + i * 30
    d.rectangle((x, hy - 56, x + 20, hy - 14), fill=Y)
    for k in range(1, 4):
        d.line([(x, hy - 56 + k * 10), (x + 20, hy - 56 + k * 10)], fill=ORANGE, width=1)
    d.line([(x + 10, hy - 56), (x + 10, hy - 14)], fill=ORANGE, width=1)
# stone lanterns along the shore, lit
lanterns = [(90, HZ - 6), (250, HZ - 4), (430, HZ - 6), (790, HZ - 4)]
for x, y in lanterns:
    d.rectangle((x - 4, y - 30, x + 4, y), fill=K)
    d.rectangle((x - 10, y - 46, x + 10, y - 30), fill=Y)
    d.polygon([(x - 16, y - 46), (x + 16, y - 46), (x, y - 60)], fill=K)

# maples on the shore, red canopies glowing near the lanterns
def maple_tree(x, y, s, glow):
    d.line([(x, y), (x - 6, y - s * 1.2)], fill=K, width=6)
    d.line([(x - 4, y - s * 0.8), (x + s * 0.6, y - s * 1.3)], fill=K, width=4)
    for _ in range(int(s * 1.2)):
        lx = x + rnd.gauss(0, s * 0.6); ly = y - s * 1.3 + rnd.gauss(0, s * 0.35)
        col = rnd.choices([R, ORANGE, RUST, K], [3, 2 * glow, 3, 2])[0]
        r = rnd.uniform(4, 9)
        d.ellipse((lx - r, ly - r, lx + r, ly + r), fill=col)
for x, s in [(20, 90), (150, 70), (330, 80), (480, 50), (760, 70)]:
    near = min(abs(x - lx) for lx, _ in lanterns)
    maple_tree(x, HZ - 2, s, 2 if near < 80 else 0.5)

# ---- reflection: flip the band above the waterline, darken, ripple
arr = np.asarray(img).astype(float)
band = arr[HZ - 400:HZ][::-1]
refl = np.zeros((H - HZ, W, 3))
for y in range(H - HZ):
    src = min(band.shape[0] - 1, int(y * 0.9))
    shift = int(6 * math.sin(y * 0.35) + 3 * math.sin(y * 0.11 + 1))
    row = np.roll(band[src], shift, axis=0)
    fade = min(1, y / 600)
    deep = np.array([10, 20, 70.0])
    refl[y] = row * (0.72 - 0.3 * fade) + deep * (0.28 + 0.3 * fade)
arr[HZ:] = refl
img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
d = ImageDraw.Draw(img)
# horizontal ripple highlights
for _ in range(240):
    y = rnd.uniform(HZ + 4, H); x = rnd.uniform(0, W)
    L = rnd.uniform(10, 50) * (1 + (y - HZ) / 400)
    d.line([(x, y), (x + L, y)], fill=rnd.choice([(20, 40, 120), K, (40, 60, 150)]), width=2)
# lantern & window reflections: broken vertical streaks
for x, y in lanterns + [(hx + 22 + i * 30, HZ) for i in range(7)]:
    for k in range(14):
        yy = HZ + 6 + k * 9 + rnd.uniform(-2, 2)
        w = rnd.uniform(4, 12) * (1 - k / 18)
        d.line([(x - w, yy), (x + w, yy)], fill=Y if k < 7 else ORANGE, width=3)

# ---- the dragon boat
bx, by = 380, 900   # hull centre at waterline
hull = [(bx - 260, by - 40), (bx + 230, by - 40), (bx + 260, by - 70), (bx + 220, by + 10), (bx - 220, by + 10)]
# boat reflection first (dark, rippled)
for k in range(10):
    yy = by + 14 + k * 9
    d.line([(bx - 220 + rnd.uniform(-10, 10), yy), (bx + 220 + rnd.uniform(-10, 10), yy)], fill=K, width=5)
    if k % 3 == 0:
        d.line([(bx - 120 + rnd.uniform(-10, 10), yy + 3), (bx + 60, yy + 3)], fill=RUST, width=3)
d.polygon(hull, fill=K)
d.line([(bx - 250, by - 32), (bx + 236, by - 32)], fill=R, width=6)
for i in range(16):
    x = bx - 220 + i * 28
    d.arc((x, by - 30, x + 28, by - 4), 0, 180, fill=Y, width=2)
# dragon head prow (left)
neck = [(bx - 260, by - 40), (bx - 300, by - 110), (bx - 290, by - 170), (bx - 250, by - 200)]
d.line(neck, fill=G, width=34, joint="curve")
for i in range(12):
    t = i / 11
    x = neck[0][0] + (neck[-1][0] - neck[0][0]) * t - 30 * math.sin(math.pi * t)
    y = neck[0][1] + (neck[-1][1] - neck[0][1]) * t
    d.arc((x - 14, y - 10, x + 14, y + 10), 200, 340, fill=Y, width=3)
hdx, hdy = bx - 250, by - 205
d.polygon([(hdx - 20, hdy - 20), (hdx + 50, hdy - 14), (hdx + 70, hdy + 6), (hdx + 40, hdy + 14),
           (hdx + 60, hdy + 30), (hdx - 10, hdy + 26)], fill=G, outline=K)
d.polygon([(hdx + 40, hdy + 14), (hdx + 72, hdy + 20), (hdx + 60, hdy + 30)], fill=R)  # open jaw
d.ellipse((hdx + 14, hdy - 12, hdx + 28, hdy + 2), fill=Y, outline=K, width=2)
d.ellipse((hdx + 19, hdy - 7, hdx + 24, hdy - 2), fill=K)
for k in range(5):   # mane
    d.line([(hdx - 18 + k * 6, hdy - 16), (hdx - 40 + k * 4, hdy - 46 - k * 4)], fill=R, width=5)
d.line([(hdx + 60, hdy + 2), (hdx + 110, hdy - 20), (hdx + 130, hdy - 4)], fill=Y, width=3)  # whisker
# stern ornament (right)
d.line([(bx + 240, by - 60), (bx + 270, by - 130)], fill=K, width=10)
for k in range(5):
    d.line([(bx + 270, by - 130), (bx + 240 + k * 18, by - 170 - (k % 2) * 16)], fill=Y, width=4)

# canopy pavilion
cx0, cx1, cy0 = bx - 150, bx + 150, by - 200
for x in (cx0 + 10, cx0 + 105, cx1 - 105, cx1 - 10):
    d.rectangle((x - 5, cy0, x + 5, by - 40), fill=R)
roof = [(cx0 - 50, cy0 + 4), (cx1 + 50, cy0 + 4), (cx1 + 20, cy0 - 30), (cx0 - 20, cy0 - 30)]
d.polygon(roof, fill=K)
d.line([(cx0 - 50, cy0 + 4), (cx1 + 50, cy0 + 4)], fill=Y, width=4)
d.line([(cx0 - 50, cy0 + 4), (cx0 - 66, cy0 - 12)], fill=K, width=6)
d.line([(cx1 + 50, cy0 + 4), (cx1 + 66, cy0 - 12)], fill=K, width=6)
d.polygon([(bx - 12, cy0 - 30), (bx + 12, cy0 - 30), (bx, cy0 - 52)], fill=Y)
# hanging blinds (sudare), rolled half up, with red tassels
for x0 in (cx0 + 15, cx1 - 100):
    d.rectangle((x0, cy0 + 6, x0 + 85, cy0 + 60), fill=(200, 170, 60))
    for k in range(0, 54, 6):
        d.line([(x0, cy0 + 8 + k), (x0 + 85, cy0 + 8 + k)], fill=ORANGE, width=2)
    d.line([(x0 + 42, cy0 + 60), (x0 + 42, cy0 + 90)], fill=R, width=4)
    d.ellipse((x0 + 36, cy0 + 86, x0 + 48, cy0 + 100), fill=R)

# courtiers in layered robes (juni-hitoe: visible bands of colour at the hem and sleeves)
def courtier(x, y, layers, hair=True, flute=False, fan=False):
    for i, c in enumerate(layers):
        w = 46 - i * 6
        d.polygon([(x - w, y), (x + w, y), (x + w * 0.5, y - 70 + i * 4), (x - w * 0.5, y - 70 + i * 4)], fill=c)
        d.line([(x - w, y), (x + w, y)], fill=K, width=1)
    d.ellipse((x - 13, y - 98, x + 13, y - 70), fill=WH, outline=K, width=2)
    if hair:
        d.polygon([(x - 14, y - 90), (x - 6, y - 100), (x + 10, y - 98), (x + 16, y - 86), (x + 30, y - 10), (x + 16, y)], fill=K)
    else:
        d.rectangle((x - 9, y - 124, x + 9, y - 96), fill=K)   # eboshi cap
    if flute:
        d.line([(x - 4, y - 78), (x - 50, y - 70)], fill=Y, width=4)
        d.ellipse((x - 26, y - 82, x - 10, y - 66), fill=layers[0])
    if fan:
        d.pieslice((x - 60, y - 110, x + 10, y - 40), 200, 290, fill=R, outline=K)
        for a in range(200, 291, 15):
            r = math.radians(a)
            d.line([(x - 25, y - 75), (x - 25 + 35 * math.cos(r), y - 75 + 35 * math.sin(r))], fill=Y, width=1)
courtier(bx - 70, by - 42, [R, Y, G, B, WH], fan=True)
courtier(bx + 10, by - 42, [B, WH, R, Y], hair=False, flute=True)
courtier(bx + 90, by - 42, [G, Y, R, WH, R])
# boatman at the stern with pole
d.line([(bx + 200, by - 160), (bx + 140, by + 120)], fill=K, width=5)
d.polygon([(bx + 170, by - 40), (bx + 200, by - 40), (bx + 192, by - 100), (bx + 176, by - 100)], fill=K)
d.ellipse((bx + 174, by - 120, bx + 194, by - 100), fill=K)
d.polygon([(bx + 162, by - 112), (bx + 206, by - 112), (bx + 184, by - 128)], fill=Y)

# ---- floating leaves, foreground, catching the last light
for _ in range(36):
    x = rnd.uniform(10, W - 10); y = rnd.uniform(960, H - 20)
    s = 10 + (y - 960) / 14
    draw_maple(d, x, y, s, rnd.uniform(0, 6.28), rnd.choices([R, ORANGE, Y], [5, 2, 1])[0],
               outline=K, ow=2, seed=rnd.randint(0, 9999))
    d.arc((x - s * 1.6, y - s * 0.4, x + s * 1.6, y + s * 0.8), 20, 160, fill=(40, 60, 150), width=2)

# ---- overhanging branch, top right, in silhouette with backlit leaves
def branch(x, y, ang, length, width, depth):
    x2 = x + length * math.cos(ang); y2 = y + length * math.sin(ang)
    d.line([(x, y), (x2, y2)], fill=K, width=int(width))
    if depth == 0:
        for _ in range(4):
            draw_maple(d, x2 + rnd.uniform(-14, 14), y2 + rnd.uniform(-6, 18), rnd.uniform(18, 26),
                       rnd.uniform(-0.5, 0.5), rnd.choice([R, R, RUST]), outline=K, vein=K, ow=2,
                       seed=rnd.randint(0, 9999))
        return
    for da in (-0.4, 0.45):
        branch(x2, y2, ang + da + rnd.uniform(-0.1, 0.1), length * 0.7, max(2, width * 0.65), depth - 1)
rnd.seed(8)
branch(W + 20, 40, math.pi - 0.25, 150, 20, 4)

d.rectangle((0, 0, W - 1, H - 1), outline=K, width=12)
save(img, os.environ.get("OUT_RAW", "/tmp/claude-0/p4.png"))
