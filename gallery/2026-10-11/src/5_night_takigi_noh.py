"""Night: 'Momijigari, by Torchlight' — the Noh play's last act on an outdoor stage lit by
fire baskets: the princess unmasked as a demon among the maples. Mostly black."""
import os, math, random
from lib import *

rnd = random.Random(22)
img = Image.new("RGB", (W, H), K)
d = ImageDraw.Draw(img)
FLOOR = 900

# ---- stage architecture, barely lit
# back wall (kagami-ita) with the painted pine, very dim
d.rectangle((60, 170, 740, FLOOR - 120), fill=K)
for x in range(60, 741, 68):
    d.line([(x, 170), (x, FLOOR - 120)], fill=K, width=3)
pine = [(420, FLOOR - 120), (430, 600), (400, 480), (450, 380), (540, 330)]
d.line(pine, fill=(25, 25, 25), width=40, joint="curve")
for x, y, w in [(330, 400, 140), (540, 330, 120), (600, 470, 110), (300, 540, 100)]:
    for k in range(3):
        d.chord((x - w + k * 10, y - 40 + k * 10, x + w - k * 10, y + 30 + k * 10), 180, 360, fill=(15, 50, 25))
# pillars, lit on their inner faces
for x in (40, 720):
    d.rectangle((x, 120, x + 40, FLOOR + 40), fill=K)
    d.rectangle((x + (30 if x < 400 else 0), 120, x + (40 if x < 400 else 10), FLOOR + 40), fill=ORANGE)
# roof: deep eave and beam
d.polygon([(0, 0), (W, 0), (W, 90), (0, 90)], fill=K)
d.rectangle((0, 110, W, 140), fill=K)
d.line([(0, 110), (W, 110)], fill=RUST, width=3)
for x in range(20, W, 34):
    d.rectangle((x, 90, x + 16, 108), fill=(40, 20, 10))
# hanging stage rope with tassels, red
d.line([(60, 150), (740, 150)], fill=R, width=4)
for x in (60, 740):
    d.line([(x, 150), (x, 220)], fill=R, width=6)

# floor: polished hinoki boards, raking firelight
d.rectangle((0, FLOOR - 120, W, FLOOR + 60), fill=K)
for k in range(12):
    y = FLOOR - 116 + k * 15
    for x in range(0, W, 8):
        glow = max(0, 1 - min(abs(x - 60), abs(x - 740)) / 260)
        if rnd.random() < glow * 0.8:
            d.line([(x, y), (x + 8, y)], fill=rnd.choice([R, RUST, Y]), width=2)
d.rectangle((0, FLOOR + 60, W, FLOOR + 78), fill=K)
d.line([(0, FLOOR + 60), (W, FLOOR + 60)], fill=ORANGE, width=2)
# white gravel (shirasu) in front of the stage, catching the fire
d.rectangle((0, FLOOR + 78, W, H), fill=K)
for _ in range(1400):
    x = rnd.uniform(0, W); y = rnd.uniform(FLOOR + 82, H - 90)
    near = min(abs(x - 70), abs(x - 730)) / 300
    if rnd.random() > near:
        r = 2
        d.ellipse((x - r, y - r, x + r, y + r), fill=rnd.choice([WH, Y, ORANGE]) if near < 0.4 else R)

# ---- fire baskets (kagaribi) left and right, in the foreground
def fire(x, y):
    # tripod
    for dx in (-40, 0, 40):
        d.line([(x + dx * 0.4, y), (x + dx, y + 230)], fill=K, width=8)
        d.line([(x + dx * 0.4, y), (x + dx, y + 230)], fill=(80, 40, 10), width=2)
    # basket
    d.polygon([(x - 46, y - 40), (x + 46, y - 40), (x + 30, y + 10), (x - 30, y + 10)], fill=K)
    for k in range(-40, 41, 12):
        d.line([(x + k, y - 40), (x + k * 0.65, y + 10)], fill=RUST, width=3)
    d.line([(x - 46, y - 40), (x + 46, y - 40)], fill=RUST, width=4)
    # flames: layered tongues
    for layer, (col, sc) in enumerate([(R, 1.0), (ORANGE, 0.75), (Y, 0.5), (WH, 0.22)]):
        for k in range(7):
            fx = x + rnd.uniform(-34, 34) * sc
            h = rnd.uniform(70, 150) * sc
            w = rnd.uniform(12, 22) * sc
            d.polygon([(fx - w, y - 36), (fx + w, y - 36), (fx + rnd.uniform(-14, 14), y - 36 - h)], fill=col)
        d.ellipse((x - 44 * sc, y - 60 * sc - 20, x + 44 * sc, y - 20), fill=col)
    # sparks
    for _ in range(40):
        sx = x + rnd.gauss(0, 40); sy = y - 130 - abs(rnd.gauss(0, 140))
        r = rnd.choice([2, 2, 3])
        d.ellipse((sx - r, sy - r, sx + r, sy + r), fill=rnd.choice([Y, ORANGE, R]))
fire(70, 940)
fire(730, 960)

# ---- the demon (shite) mid-transformation
cx, base = 400, FLOOR - 20
hx, hy = cx, base - 470
# wig: long red hair (akagashira) streaming down

for k in range(70):
    a = rnd.uniform(-1.3, 1.3)
    L = rnd.uniform(330, 450)
    x0 = hx + 50 * math.sin(a); y0 = hy - 60 + 30 * abs(a)
    pts = [(x0 + (math.sin(a) * 260 + 18 * math.sin(t * 4 + k)) * t ** 1.3, y0 + L * t) for t in [i / 10 for i in range(11)]]
    d.line(pts, fill=R if k % 4 else ORANGE, width=4)
# robe: karaori with scale triangles (uroko) — the demon's pattern
robe = [(cx - 150, base), (cx + 150, base), (cx + 110, base - 260), (cx + 70, base - 380), (cx - 70, base - 380), (cx - 110, base - 260)]
d.polygon(robe, fill=K)
from PIL import ImageDraw as _D
m = Image.new("L", (W, H), 0); _D.Draw(m).polygon(robe, fill=255)
tri = Image.new("RGB", (W, H), K); td = _D.Draw(tri)
s = 34
for j, y in enumerate(range(base - 400, base + 10, s)):
    for i, x in enumerate(range(cx - 180, cx + 180, s)):
        td.polygon([(x, y + s), (x + s, y + s), (x + s / 2, y)], fill=WH if (i + j) % 2 else Y)
        td.line([(x, y + s), (x + s, y + s)], fill=K, width=2)
img.paste(tri, (0, 0), m)
d = ImageDraw.Draw(img)
# shadow side of robe (firelight from both sides, dark in the middle fold)
for k in range(5):
    d.line([(cx - 10 + k * 5, base - 370), (cx - 30 + k * 12, base)], fill=K, width=6)
# outer cloak, red, flung open
d.polygon([(cx - 70, base - 380), (cx - 190, base - 200), (cx - 230, base - 30), (cx - 140, base - 60), (cx - 100, base - 260)], fill=R, outline=K)
d.polygon([(cx + 70, base - 380), (cx + 200, base - 240), (cx + 240, base - 70), (cx + 150, base - 90), (cx + 100, base - 260)], fill=R, outline=K)
for k in range(5):
    t = k / 4
    for lx, ly in ((cx - 175 + 25 * t, base - 220 + 150 * t), (cx + 175 + 20 * t, base - 230 + 140 * t)):
        draw_maple(d, lx, ly, 18, t * 2, R, outline=Y, ow=2, seed=k)
# sash
d.rectangle((cx - 92, base - 300, cx + 92, base - 270), fill=G)
d.line([(cx - 92, base - 286), (cx + 92, base - 286)], fill=Y, width=3)
# arms: one raising the uchizue (striking staff), one holding a maple branch
d.polygon([(cx + 70, base - 370), (cx + 160, base - 470), (cx + 190, base - 450), (cx + 100, base - 330)], fill=R, outline=K)
d.line([(cx + 175, base - 465), (cx + 260, base - 640)], fill=Y, width=8)
d.line([(cx + 175, base - 465), (cx + 260, base - 640)], fill=K, width=2)
d.polygon([(cx - 70, base - 370), (cx - 170, base - 330), (cx - 180, base - 300), (cx - 90, base - 320)], fill=R, outline=K)
def mbranch(x, y, ang, L, w, dep):
    x2, y2 = x + L * math.cos(ang), y + L * math.sin(ang)
    d.line([(x, y), (x2, y2)], fill=K, width=w)
    d.line([(x, y), (x2, y2)], fill=RUST, width=max(1, w // 3))
    if dep == 0:
        for _ in range(3):
            draw_maple(d, x2 + rnd.uniform(-10, 10), y2 + rnd.uniform(-10, 10), rnd.uniform(22, 28),
                       rnd.uniform(-0.6, 0.6), rnd.choice([R, R, ORANGE]), outline=K, vein=None, ow=2,
                       seed=rnd.randint(0, 9999))
        return
    for da in (-0.5, 0.4):
        mbranch(x2, y2, ang + da, L * 0.7, max(2, int(w * 0.7)), dep - 1)
mbranch(cx - 175, base - 315, -math.pi * 0.72, 90, 8, 3)

# hannya mask
mx, my = hx, hy
d.ellipse((mx - 62, my - 80, mx + 62, my + 86), fill=WH, outline=K, width=3)
# horns
for s_ in (-1, 1):
    d.polygon([(mx + s_ * 34, my - 66), (mx + s_ * 56, my - 70), (mx + s_ * 74, my - 150), (mx + s_ * 52, my - 110)], fill=Y, outline=K)
    for k in range(3):
        yy = my - 80 - k * 20
        d.line([(mx + s_ * (40 + k * 7), yy), (mx + s_ * (58 + k * 6), yy - 4)], fill=K, width=2)
# brows and eyes (gold, with the anguished slant)
for s_ in (-1, 1):
    d.polygon([(mx + s_ * 8, my - 26), (mx + s_ * 46, my - 50), (mx + s_ * 50, my - 36), (mx + s_ * 12, my - 16)], fill=K)
    d.polygon([(mx + s_ * 12, my - 8), (mx + s_ * 44, my - 24), (mx + s_ * 46, my - 4), (mx + s_ * 16, my + 2)], fill=Y, outline=K)
    d.ellipse((mx + s_ * 30 - 5, my - 18, mx + s_ * 30 + 5, my - 8), fill=K)
# hair parting lines on the brow
for k in range(-3, 4):
    d.line([(mx + k * 6, my - 80), (mx + k * 12, my - 56)], fill=K, width=2)
# nose
d.polygon([(mx - 10, my + 8), (mx + 10, my + 8), (mx + 14, my + 22), (mx - 14, my + 22)], fill=WH, outline=K)
# mouth: wide, red, gold fangs
d.chord((mx - 52, my + 22, mx + 52, my + 84), 0, 180, fill=R, outline=K, width=3)
d.line([(mx - 52, my + 52), (mx + 52, my + 52)], fill=K, width=3)
for s_ in (-1, 1):
    d.polygon([(mx + s_ * 38, my + 52), (mx + s_ * 30, my + 52), (mx + s_ * 34, my + 76)], fill=Y, outline=K)
    d.polygon([(mx + s_ * 22, my + 52), (mx + s_ * 14, my + 52), (mx + s_ * 18, my + 40)], fill=Y, outline=K)
for k in range(-3, 4):
    d.rectangle((mx + k * 6 - 2, my + 46, mx + k * 6 + 2, my + 52), fill=WH)
# firelight rim on the mask
d.arc((mx - 62, my - 80, mx + 62, my + 86), 140, 220, fill=ORANGE, width=4)
d.arc((mx - 62, my - 80, mx + 62, my + 86), -40, 40, fill=ORANGE, width=4)

# falling maple leaves in the dark
for _ in range(14):
    x = rnd.uniform(140, 660); y = rnd.uniform(180, 760)
    if abs(x - cx) < 130 and y > 300:
        continue
    draw_maple(d, x, y, rnd.uniform(10, 16), rnd.uniform(0, 6.28), rnd.choice([R, ORANGE]), outline=K,
               ow=2, seed=rnd.randint(0, 999))

# title, small, bottom
f = font(FONT_ITAL, 28)
t = "Momijigari  ·  takigi-noh  ·  act II"
d.text(((W - d.textlength(t, font=f)) / 2, H - 70), t, font=f, fill=R)
save(img, os.environ.get("OUT_RAW", "/tmp/claude-0/p5.png"))
