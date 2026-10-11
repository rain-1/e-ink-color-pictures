"""Morning: 'Dawn at the Maple Gorge' — a Hiroshige-style woodblock landscape.
Full palette; bokashi sky gradients are left for Floyd–Steinberg, flats are pure ink."""
import os, math, random
from lib import *

rnd = random.Random(11)
img = Image.new("RGB", (W, H), WH)
d = ImageDraw.Draw(img)

# ---- sky: bokashi, deep blue at top -> paper -> warm glow at the ridge
vgrad(img, (0, 0, W, 470), [(0, B), (0.22, (60, 100, 190)), (0.5, WH), (0.78, (250, 225, 120)), (1, (245, 170, 60))])
# sun, low, half behind the far ridge
d.ellipse((520, 300, 640, 420), fill=R)
# thin cloud streaks across the sun (ukiyo-e horizontal bands)
for y, x0, x1 in [(330, 470, 700), (352, 500, 760), (250, 80, 380), (272, 40, 300)]:
    d.rounded_rectangle((x0, y, x1, y + 10), radius=5, fill=WH)
# flock of birds
for i in range(9):
    bx, by = 250 + i * 26 + rnd.randint(-6, 6), 170 + abs(i - 4) * 12 + rnd.randint(-4, 4)
    d.line([(bx - 9, by - 4), (bx, by + 2), (bx + 9, by - 4)], fill=K, width=3)

# ---- far ranges
def ridge(y0, amp, freq, seed):
    r = random.Random(seed); ph = [r.random() * 6 for _ in range(4)]
    return [(x, y0 - amp * (0.5 * math.sin(x * freq + ph[0]) + 0.3 * math.sin(x * freq * 2.3 + ph[1])
                     + 0.2 * math.sin(x * freq * 5.1 + ph[2]))) for x in range(0, W + 1, 4)]
far2 = ridge(400, 60, 0.008, 1)
d.polygon(far2 + [(W, 520), (0, 520)], fill=SKY)
far1 = ridge(450, 45, 0.011, 2)
d.polygon(far1 + [(W, 560), (0, 560)], fill=B)
# snow-dusted tops? no — autumn: tiny dark pines along the far ridge
for x, y in far1[::3]:
    if rnd.random() < 0.7:
        h = rnd.randint(8, 16)
        d.polygon([(x, y - h), (x - 4, y + 2), (x + 4, y + 2)], fill=(10, 30, 90))

# ---- kasumi mist band
def mist(y, x0, x1, h=36):
    d.rounded_rectangle((x0, y, x1, y + h), radius=h // 2, fill=WH)
mist(500, -40, 520, 40); mist(530, 300, 860, 34)

# ---- middle slopes: green hills carrying maple canopies
noise = value_noise(W, H, 80, seed=4)
left_slope = [(0, 560), (120, 545), (260, 590), (380, 680), (430, 760), (380, 900), (300, 1200), (0, 1200)]
right_slope = [(W, 520), (700, 535), (590, 600), (500, 700), (470, 800), (560, 900), (520, 1000), (400, 1200), (W, 1200)]
# distant inner valley wall + waterfall between the slopes
d.polygon([(200, 600), (400, 560), (600, 590), (560, 820), (380, 820)], fill=(30, 90, 110))
for k in range(40):
    y = 600 + k * 5
    d.line([(rnd.uniform(300, 560), y), (rnd.uniform(300, 560), y)], fill=B, width=2)
d.rectangle((462, 566, 500, 790), fill=WH)
for k in range(6):
    x = 466 + k * 6
    d.line([(x, 570 + (k % 2) * 30), (x, 780)], fill=SKY if k % 2 else B, width=2)
d.ellipse((430, 760, 540, 800), fill=WH)
for poly in (left_slope, right_slope):
    d.polygon(poly, fill=G)

def inside(poly, x, y):
    c = False; n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]; x2, y2 = poly[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            c = not c
    return c

def pine(x, y, h):
    dark = (10, 60, 30)
    d.line([(x, y), (x, y - h)], fill=K, width=3)
    for t in range(5):
        yy = y - h * (0.25 + 0.17 * t); w = h * (0.45 - 0.07 * t)
        d.polygon([(x - w, yy + 6), (x + w, yy + 6), (x + w * 0.5, yy - 6), (x - w * 0.5, yy - 6)], fill=dark)
        d.line([(x - w, yy + 6), (x + w, yy + 6)], fill=K, width=2)

def canopy(x, y, s):
    col = rnd.choices([R, ORANGE, Y, RUST], [5, 3, 2, 1])[0]
    # shadow side, then lit puffs, then edge dabs
    d.ellipse((x - s, y - s * 0.6, x + s, y + s * 0.8), fill=RUST if col != RUST else K)
    for _ in range(5):
        ox, oy = rnd.uniform(-s * .7, s * .7), rnd.uniform(-s * .6, s * .2)
        r = s * rnd.uniform(.35, .6)
        d.ellipse((x + ox - r, y + oy - r, x + ox + r, y + oy + r), fill=col)
    for _ in range(4):
        ox, oy = rnd.uniform(-s * .6, s * .6), rnd.uniform(-s * .7, -s * .1)
        r = s * .15
        d.ellipse((x + ox - r, y + oy - r, x + ox + r, y + oy + r), fill=Y if col != Y else WH)
    d.line([(x, y + s * 0.5), (x, y + s * 1.1)], fill=K, width=3)

items = []
for _ in range(1400):
    x, y = rnd.uniform(0, W), rnd.uniform(520, 1200)
    for poly in (left_slope, right_slope):
        if inside(poly, x, y):
            depth = min(1, (y - 520) / 440)
            items.append((y, x, depth)); break
items.sort()
for y, x, depth in items[::3]:
    s = 7 + depth * 20
    if rnd.random() < 0.18:
        pine(x, y, s * 3)
    else:
        canopy(x, y, s)

# ---- five-storey pagoda on the right slope
px, py = 640, 640
d.rectangle((px - 6, py - 250, px + 6, py), fill=K)
for i in range(5):
    yb = py - 30 - i * 44; w = 70 - i * 9
    d.rectangle((px - w * 0.55, yb - 26, px + w * 0.55, yb), fill=R)
    for k in range(-2, 3):
        d.line([(px + k * w * 0.2, yb - 26), (px + k * w * 0.2, yb)], fill=K, width=2)
    d.polygon([(px - w, yb - 22), (px - w * 0.5, yb - 38), (px + w * 0.5, yb - 38), (px + w, yb - 22),
               (px + w * 1.05, yb - 27)], fill=K)
    d.polygon([(px - w * 1.05, yb - 27), (px - w, yb - 22), (px - w * 0.6, yb - 30)], fill=K)
# sorin spire with rings
d.line([(px, py - 250), (px, py - 320)], fill=K, width=4)
for k in range(9):
    yy = py - 258 - k * 6
    d.line([(px - 7, yy), (px + 7, yy)], fill=Y, width=2)
d.ellipse((px - 6, py - 330, px + 6, py - 318), fill=Y)
# some canopies in front of the pagoda base
for _ in range(10):
    canopy(px + rnd.uniform(-80, 80), py + rnd.uniform(-10, 30), rnd.uniform(16, 24))

# ---- river through the gorge
river = [(470, 760), (430, 800), (380, 880), (330, 960), (250, 1040), (140, 1110), (0, 1150), (0, 1200),
         (330, 1200), (430, 1100), (500, 1000), (540, 900), (530, 820), (500, 770)]
d.polygon(river, fill=B)
# woodblock wave lines
for i in range(26):
    t = i / 25
    y = 790 + t * 400
    xl = 480 - t * 470; xr = 520 - t * 180 + 60 * t
    for j in range(5):
        x = xl + (xr - xl) * (j + rnd.random() * 0.6) / 5
        if inside(river, x, y):
            w = 12 + t * 26
            d.arc((x - w, y - w * 0.4, x + w, y + w * 0.4), 200, 340, fill=WH, width=3)
# fallen leaves on the water
for _ in range(40):
    x, y = rnd.uniform(0, 540), rnd.uniform(800, 1200)
    if inside(river, x, y):
        s = 7 + (y - 800) / 30
        draw_maple(d, x, y, s, rnd.uniform(0, 6.28), rnd.choice([R, Y, ORANGE]), outline=K, ow=2,
                   seed=rnd.randint(0, 999))

# ---- arched bridge (taikobashi)
bx0, bx1, by = 330, 590, 905
arch = [(bx0 + (bx1 - bx0) * t, by - 60 * math.sin(math.pi * t)) for t in [i / 40 for i in range(41)]]
d.line(arch, fill=R, width=18)
d.line([(x, y + 9) for x, y in arch], fill=K, width=3)
# posts + rail
for i in range(0, 41, 5):
    x, y = arch[i]
    d.line([(x, y), (x, y - 34)], fill=R, width=7)
    d.ellipse((x - 6, y - 42, x + 6, y - 30), fill=Y)
d.line([(x, y - 30) for x, y in arch], fill=R, width=6)
# piers into the water
for i in (6, 16, 24, 34):
    x, y = arch[i]
    d.rectangle((x - 5, y + 10, x + 5, by + 40), fill=K)

# tiny travellers on the bridge
def figure(x, y, coat, hat=None, umbrella=None, basket=False):
    d.polygon([(x - 9, y), (x + 9, y), (x + 5, y - 30), (x - 5, y - 30)], fill=coat)
    d.line([(x - 9, y), (x + 9, y)], fill=K, width=2)
    d.ellipse((x - 6, y - 42, x + 6, y - 30), fill=WH, outline=K, width=2)
    if hat:
        d.polygon([(x - 16, y - 38), (x + 16, y - 38), (x, y - 52)], fill=hat, outline=K)
    if umbrella:
        d.line([(x + 4, y - 20), (x + 4, y - 70)], fill=K, width=2)
        d.pieslice((x - 26, y - 92, x + 34, y - 52), 180, 360, fill=umbrella, outline=K, width=2)
        for k in range(1, 6):
            a = math.pi + k * math.pi / 6
            d.line([(x + 4, y - 72), (x + 4 + 30 * math.cos(a), y - 72 + 20 * math.sin(a))], fill=K, width=1)
    if basket:
        d.rectangle((x + 8, y - 26, x + 22, y - 12), fill=Y, outline=K)
        for k in range(3):
            d.ellipse((x + 10 + k * 4, y - 32, x + 16 + k * 4, y - 26), fill=R)
figure(*arch[14], coat=B, umbrella=R)
figure(arch[20][0] + 6, arch[20][1], coat=K, hat=Y)
figure(*arch[26], coat=G, hat=Y, basket=True)

# ---- foreground bank, bottom right
bank = [(W, 960), (680, 980), (560, 1060), (470, 1130), (420, 1200), (W, 1200)]
d.polygon(bank, fill=K)
for _ in range(90):
    x = rnd.uniform(440, W); y = rnd.uniform(990, 1200)
    if inside(bank, x, y):
        h = rnd.uniform(14, 40)
        d.line([(x, y), (x + rnd.uniform(-10, 10), y - h)], fill=rnd.choice([Y, OLIVE, G]), width=3)
# rocks with highlights
for x, y, r in [(600, 1110, 40), (700, 1060, 30), (740, 1150, 50)]:
    d.ellipse((x - r, y - r * 0.6, x + r, y + r * 0.6), fill=B, outline=K, width=3)
    d.arc((x - r * 0.8, y - r * 0.5, x + r * 0.6, y + r * 0.3), 190, 290, fill=WH, width=3)

# ---- overhanging maple branch from top-left
def branch(x, y, ang, length, width, depth):
    x2 = x + length * math.cos(ang); y2 = y + length * math.sin(ang)
    d.line([(x, y), (x2, y2)], fill=K, width=int(width))
    if depth == 0 or length < 18:
        for _ in range(3):
            draw_maple(d, x2 + rnd.uniform(-12, 12), y2 + rnd.uniform(-8, 14), rnd.uniform(22, 32),
                       rnd.uniform(-0.6, 0.6), rnd.choices([R, ORANGE, Y], [6, 3, 2])[0],
                       outline=K, vein=RUST, ow=2, seed=rnd.randint(0, 9999))
        return
    for da in (-0.4, 0.4):
        branch(x2, y2, ang + da + rnd.uniform(-0.15, 0.15), length * rnd.uniform(0.62, 0.75),
               max(2, width * 0.66), depth - 1)
rnd.seed(3)
branch(-20, 60, 0.12, 170, 22, 5)
branch(-20, 200, -0.05, 120, 14, 4)

# ---- cartouche, top right: vertical title strip
cx0, cy0 = 712, 40
d.rectangle((cx0, cy0, cx0 + 50, cy0 + 300), fill=Y, outline=K, width=3)
d.rectangle((cx0 + 5, cy0 + 5, cx0 + 45, cy0 + 295), outline=K, width=1)
f = font(FONT_SERIF_B, 28)
for i, ch in enumerate("MOMIJI"):
    tw = d.textlength(ch, font=f)
    d.text((cx0 + 25 - tw / 2, cy0 + 14 + i * 46), ch, font=f, fill=K)
# red seal
d.rectangle((cx0 + 8, cy0 + 312, cx0 + 42, cy0 + 346), fill=R)
d.rectangle((cx0 + 13, cy0 + 317, cx0 + 37, cy0 + 341), outline=WH, width=2)
d.line([(cx0 + 25, cy0 + 319), (cx0 + 25, cy0 + 339)], fill=WH, width=2)
d.line([(cx0 + 15, cy0 + 329), (cx0 + 35, cy0 + 329)], fill=WH, width=2)

# ---- frame
d.rectangle((0, 0, W - 1, H - 1), outline=K, width=14)
d.rectangle((14, 14, W - 15, H - 15), outline=WH, width=3)
save(img, os.environ.get("OUT_RAW", "/tmp/claude-0/p1.png"))
