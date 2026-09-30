"""4 · Evening — Wie stark ist nicht dein Zauberton. Tamino plays and the animals come, as a
millefleur tapestry: a green ground thick with small flowers, an orange tree, a lion, a stag,
a fox, hares and birds turned toward the flute, the evening star and moon woven in above,
all inside a scrolling vine border."""
import math, random
import numpy as np
from common import *

random.seed(1791)
c = Canvas(G)
BD = 20  # border width

# --- millefleur ground: poisson-ish scatter of flower types
def flower(x, y, kind, s=1.0):
    if kind == 0:   # daisy
        for k in range(8):
            a = k * math.pi / 4
            c.poly(oval(x + 3.2 * s * math.cos(a), y + 3.2 * s * math.sin(a), 2.4 * s, 1.1 * s, a, 10), fill=Wh)
        c.ell(x, y, 1.5 * s, fill=Y)
    elif kind == 1:  # red pinks on a stem
        c.line([(x, y + 7 * s), (x, y)], K, .7)
        c.line([(x, y + 4 * s), (x - 3 * s, y + 1 * s)], K, .6)
        for dx, dy in ((0, 0), (-3 * s, 1 * s)):
            c.ell(x + dx, y + dy, 2.2 * s, fill=R); c.ell(x + dx, y + dy, .8 * s, fill=Wh)
    elif kind == 2:  # bluebells
        c.line([(x, y + 8 * s), (x, y - 4 * s), (x + 3 * s, y - 6 * s)], K, .7)
        for k in range(3):
            by = y - 3 * s + k * 3.2 * s
            c.poly([(x + 1 * s, by), (x + 4 * s, by), (x + 5 * s, by + 3 * s), (x, by + 3 * s)], fill=B, outline=Wh, width=.4)
    elif kind == 3:  # strawberry plant
        for a in (-0.6, 0, 0.6):
            c.poly(oval(x + 4 * s * math.sin(a), y - 4 * s * math.cos(a), 1.6 * s, 3.2 * s, a, 10), fill=K)
        c.poly([(x - 2 * s, y + 2 * s), (x + 2 * s, y + 2 * s), (x, y + 6 * s)], fill=R); c.ell(x, y + 2 * s, 2 * s, 1.2 * s, fill=R)
        c.ell(x - .6 * s, y + 3 * s, .4 * s, fill=Y)
    elif kind == 4:  # yellow star-flower
        c.star(x, y, 4 * s, Y, 5, 0.45); c.ell(x, y, 1 * s, fill=R)
    else:            # fern sprig
        c.line([(x, y + 6 * s), (x, y - 6 * s)], K, .7)
        for k in range(5):
            yk = y + 4 * s - k * 2.4 * s
            c.line([(x, yk), (x - 3 * s, yk - 1.5 * s)], K, .6); c.line([(x, yk), (x + 3 * s, yk - 1.5 * s)], K, .6)
KEEP = [(200, 170, 80, 72), (200, 270, 12, 60), (200, 318, 36, 56), (200, 100, 168, 17), (86, 440, 66, 46),
        (300, 430, 50, 64), (78, 358, 52, 24), (318, 358, 24, 26), (160, 408, 20, 20), (250, 410, 20, 20),
        (256, 120, 24, 18), (146, 138, 24, 18), (300, 294, 22, 16), (100, 288, 24, 18), (220, 508, 24, 18),
        (176, 540, 20, 12), (325, 62, 28, 28), (80, 60, 16, 16), (262, 262, 46, 22), (160, 262, 18, 14)]
def clear(x, y): return all(((x - a) / rx) ** 2 + ((y - b) / ry) ** 2 > 1 for a, b, rx, ry in KEEP)
pts = []
tries = 0
while tries < 9000:
    tries += 1
    x, y = random.uniform(BD + 6, W - BD - 6), random.uniform(BD + 6, H - BD - 6)
    if clear(x, y) and all((x - px) ** 2 + (y - py) ** 2 > 14.5 ** 2 for px, py in pts[-400:]):
        pts.append((x, y))
for x, y in pts:
    flower(x, y, random.choices(range(6), weights=[2, 3, 2, 2, 2, 3])[0], random.uniform(0.85, 1.15))

# --- sky strip at the top: the evening star and moon, woven
c.d.chord([(300) * 2, (40) * 2, (344) * 2, (84) * 2], 0, 360, fill=Y)
c.ell(330, 56, 18, fill=G)
c.ell(322, 62, 22, fill=None)
c.star(80, 60, 12, Wh, 8, 0.35); c.star(80, 60, 5, Y, 8, 0.4)

# --- orange tree behind Tamino
TX = 200
c.poly([(TX - 7, 330), (TX + 7, 330), (TX + 5, 210), (TX - 5, 210)], fill=K)
for k in range(6): c.line([(TX - 5, 320 - k * 18), (TX + 5, 314 - k * 18)], Y, .6)
crown = [(TX + 70 * math.cos(t) + 6 * math.sin(7 * t), 170 + 62 * math.sin(t) + 5 * math.cos(9 * t)) for t in np.linspace(0, 2 * math.pi, 80)]
c.poly(crown, fill=K)
crown2 = [(TX + 66 * math.cos(t) + 6 * math.sin(7 * t), 170 + 58 * math.sin(t) + 5 * math.cos(9 * t)) for t in np.linspace(0, 2 * math.pi, 80)]
c.poly(crown2, fill=G)
for i in range(70):  # leaves
    a = random.uniform(0, 2 * math.pi); r = math.sqrt(random.random())
    lx, ly = TX + 58 * r * math.cos(a), 170 + 50 * r * math.sin(a)
    c.poly(oval(lx, ly, 5, 2.2, random.uniform(0, math.pi), 10), fill=K if i % 3 else Y)
for i in range(16):  # oranges
    a = random.uniform(0, 2 * math.pi); r = math.sqrt(random.random()) * 0.85
    c.ell(TX + 56 * r * math.cos(a), 170 + 46 * r * math.sin(a), 4.5, fill=R, outline=K, width=.6)
    c.ell(TX + 56 * r * math.cos(a) - 1.3, 170 + 46 * r * math.sin(a) - 1.3, 1.1, fill=Y)

# --- Tamino, seated, playing the flute
PX, PY = 200, 350
c.poly([(PX - 26, PY + 22), (PX + 26, PY + 22), (PX + 16, PY - 12), (PX - 16, PY - 12)], fill=R, outline=K, width=1)   # cloak on the ground
for k in range(-2, 3): c.line([(PX + k * 5, PY - 8), (PX + k * 9, PY + 20)], K, .6)
c.poly([(PX - 11, PY - 12), (PX + 11, PY - 12), (PX + 9, PY - 44), (PX - 9, PY - 44)], fill=B, outline=K, width=1)      # tunic
for k in range(4): c.line([(PX - 9, PY - 40 + k * 7), (PX + 9, PY - 40 + k * 7)], Y, .6)
c.rect(PX - 10, PY - 22, PX + 10, PY - 19, fill=Y)
c.ell(PX, PY - 54, 9, 10, fill=Wh, outline=K, width=1)
c.d.chord([(PX - 10) * 2, (PY - 66) * 2, (PX + 10) * 2, (PY - 48) * 2], 180, 360, fill=Y)   # fair hair
c.poly([(PX - 10, PY - 57), (PX - 12, PY - 44), (PX - 7, PY - 50)], fill=Y)
c.ell(PX + 3, PY - 54, 1.1, fill=K); c.ell(PX - 3, PY - 54, 1.1, fill=K)
c.line([(PX - 1, PY - 48), (PX + 24, PY - 58)], Y, 2.4); c.line([(PX - 1, PY - 48), (PX + 24, PY - 58)], K, .6)       # the flute
for k in range(4): c.ell(PX + 8 + k * 4, PY - 51.5 - k * 1.6, .7, fill=K)
c.line([(PX - 9, PY - 38), (PX + 4, PY - 48)], Wh, 2); c.line([(PX + 9, PY - 38), (PX + 14, PY - 52)], Wh, 2)            # arms
# the notes drifting out
for i, (nx, ny) in enumerate([(236, 282), (256, 266), (276, 256), (298, 250), (170, 270), (150, 262)]):
    c.ell(nx, ny, 3.4, 2.5, fill=Wh, outline=K, width=.6); c.line([(nx + 3, ny), (nx + 3, ny - 12)], K, 1)
    if i % 2: c.line([(nx + 3, ny - 12), (nx + 8, ny - 8)], K, 1)

# --- the beasts
def lion(x, y, f=1, s=1.0):
    c.line([(x - 26 * s * f, y - 14 * s), (x - 38 * s * f, y - 24 * s), (x - 42 * s * f, y - 18 * s)], K, 1.4)
    c.ell(x - 42 * s * f, y - 18 * s, 3 * s, fill=K)
    for lx in (-18, -10, 8, 16):
        c.rect(x + lx * s * f - 2.5 * s, y - 12 * s, x + lx * s * f + 2.5 * s, y, fill=Y, outline=K, width=.6)
    c.poly(oval(x - 4 * s * f, y - 18 * s, 26 * s, 11 * s), fill=Y, outline=K, width=1)
    hx, hy = x + 20 * s * f, y - 28 * s
    for k in range(16):
        a = k * math.pi / 8
        c.poly([(hx + 9 * s * math.cos(a - .25), hy + 9 * s * math.sin(a - .25)), (hx + 19 * s * math.cos(a), hy + 19 * s * math.sin(a)),
                (hx + 9 * s * math.cos(a + .25), hy + 9 * s * math.sin(a + .25))], fill=R, outline=K, width=.5)
    c.ell(hx, hy, 12 * s, fill=R, outline=K, width=.8)
    c.ell(hx + 2 * s * f, hy + 1 * s, 8.5 * s, 9 * s, fill=Y, outline=K, width=.8)
    c.ell(hx + 5 * s * f, hy - 2 * s, 1.3 * s, fill=K); c.ell(hx - .5 * s * f, hy - 2 * s, 1.3 * s, fill=K)
    c.poly([(hx + 1 * s * f, hy + 3 * s), (hx + 7 * s * f, hy + 3 * s), (hx + 4 * s * f, hy + 6 * s)], fill=K)
    c.line([(hx + 4 * s * f, hy + 6 * s), (hx + 4 * s * f, hy + 8 * s)], K, .6)
def stag(x, y, f=1, s=1.0):
    for lx in (-16, -10, 10, 16):
        c.line([(x + lx * s * f, y - 18 * s), (x + lx * s * f + 1, y)], K, 1.6 * s)
    c.poly(oval(x, y - 24 * s, 24 * s, 9 * s), fill=Wh, outline=K, width=1)
    for k in range(6): c.ell(x - 12 * s * f + k * 5 * s * f, y - 27 * s + (k % 2) * 3, 1.3 * s, fill=R)
    c.poly([(x + 14 * s * f, y - 28 * s), (x + 22 * s * f, y - 50 * s), (x + 28 * s * f, y - 48 * s), (x + 22 * s * f, y - 22 * s)], fill=Wh, outline=K, width=1)
    hx, hy = x + 26 * s * f, y - 52 * s
    c.poly([(hx - 5 * s * f, hy - 4 * s), (hx + 12 * s * f, hy + 3 * s), (hx + 10 * s * f, hy + 6 * s), (hx - 4 * s * f, hy + 5 * s)], fill=Wh, outline=K, width=1)
    c.ell(hx + 2 * s * f, hy - .5 * s, 1.2 * s, fill=K)
    c.poly([(hx - 3 * s * f, hy - 4 * s), (hx - 9 * s * f, hy - 10 * s), (hx - 5 * s * f, hy - 2 * s)], fill=Wh, outline=K, width=.6)
    for side in (0, 1):   # antlers
        bx, by = hx - (1 + side * 3) * s * f, hy - 5 * s
        stem = [(bx, by), (bx - 4 * s * f, by - 12 * s), (bx - 2 * s * f, by - 24 * s), (bx + 2 * s * f, by - 32 * s)]
        c.line(stem, Y if side else K, 1.4)
        for (ax, ay), d in zip(stem[1:], (5, 6, 4)):
            c.line([(ax, ay), (ax + d * s * f, ay - 5 * s)], Y if side else K, 1.1)
def hare(x, y, f=1, s=1.0, col=Wh):
    c.poly(oval(x, y - 7 * s, 10 * s, 7 * s), fill=col, outline=K, width=.8)
    c.ell(x - 10 * s * f, y - 8 * s, 3 * s, fill=Wh, outline=K, width=.5)
    hx, hy = x + 9 * s * f, y - 14 * s
    for a in (-.2, .15):
        c.poly(oval(hx - 2 * s * f + 10 * s * math.sin(a) * f, hy - 10 * s, 2.2 * s, 8 * s, a * f, 12), fill=col, outline=K, width=.6)
    c.ell(hx, hy, 5 * s, 4.2 * s, fill=col, outline=K, width=.8)
    c.ell(hx + 2 * s * f, hy - 1 * s, 1 * s, fill=K)
def fox(x, y, f=1, s=1.0):
    c.poly([(x - 14 * s * f, y - 12 * s), (x - 36 * s * f, y - 4 * s), (x - 40 * s * f, y - 12 * s), (x - 26 * s * f, y - 18 * s)], fill=R, outline=K, width=.8)
    c.poly([(x - 36 * s * f, y - 5 * s), (x - 41 * s * f, y - 11 * s), (x - 36 * s * f, y - 11 * s)], fill=Wh)
    for lx in (-10, -5, 8, 12): c.line([(x + lx * s * f, y - 10 * s), (x + lx * s * f, y)], K, 1.3)
    c.poly(oval(x, y - 14 * s, 17 * s, 7 * s), fill=R, outline=K, width=.9)
    hx, hy = x + 17 * s * f, y - 20 * s
    c.poly([(hx - 6 * s * f, hy - 4 * s), (hx - 4 * s * f, hy - 13 * s), (hx, hy - 5 * s), (hx + 3 * s * f, hy - 12 * s), (hx + 5 * s * f, hy - 3 * s), (hx + 14 * s * f, hy + 2 * s), (hx, hy + 6 * s), (hx - 6 * s * f, hy + 3 * s)], fill=R, outline=K, width=.9)
    c.poly([(hx, hy + 1 * s), (hx + 14 * s * f, hy + 2 * s), (hx, hy + 6 * s)], fill=Wh)
    c.ell(hx + 14 * s * f, hy + 2 * s, 1.2 * s, fill=K); c.ell(hx + 2 * s * f, hy - 2 * s, 1.1 * s, fill=K)

lion(96, 470, 1, 1.35)
stag(305, 468, -1, 1.25)
fox(90, 372, 1, 1.0)
hare(318, 372, -1, 1.1)
hare(160, 420, 1, 0.9, Y)
hare(250, 422, -1, 0.85)
bird(c, 256, 132, 1.1, -1, B, Y, Wh, None, crest=True)
bird(c, 146, 150, 1.0, 1, R, K, Y, None)
bird(c, 300, 305, 0.9, -1, Y, R, Wh, None)
bird(c, 100, 300, 0.95, 1, Wh, B, Y, R, crest=True)
bird(c, 220, 520, 1.0, -1, Y, B, Wh, R)
# a snail, because tapestries always have one
c.ell(170, 540, 7, fill=Y, outline=K, width=.8)
c.d.arc([(170 - 4) * 2, (540 - 4) * 2, (170 + 4) * 2, (540 + 4) * 2], 0, 300, fill=K, width=2)
c.poly([(162, 547), (186, 547), (190, 541), (184, 544), (162, 544)], fill=Wh, outline=K, width=.6)

# --- banderole across the top
bl = [(58 + t * 284, 100 + 6 * math.sin(t * math.pi * 2)) for t in np.linspace(0, 1, 40)]
c.poly([(x, y - 10) for x, y in bl] + [(x, y + 10) for x, y in bl[::-1]], fill=Wh, outline=K, width=1)
c.poly([(58, 90), (40, 88), (48, 100), (40, 112), (58, 110)], fill=Wh, outline=K, width=1)
c.poly([(342, 90), (360, 88), (352, 100), (360, 112), (342, 110)], fill=Wh, outline=K, width=1)
c.text((200, 100), "WIE STARK IST NICHT DEIN ZAUBERTON", R, 9.2, "mm", bold=True, spacing=0.4)

# --- border: blue band, a yellow vine with red flowers, corner blocks
for (x0, y0, x1, y1) in ((0, 0, W, BD), (0, H - BD, W, H), (0, 0, BD, H), (W - BD, 0, W, H)):
    c.rect(x0, y0, x1, y1, fill=B)
c.rect(BD - 2, BD - 2, W - BD + 2, H - BD + 2, outline=Y, width=1.5)
def vine(p0, p1, n):
    (x0, y0), (x1, y1) = p0, p1
    L = math.hypot(x1 - x0, y1 - y0); ux, uy = (x1 - x0) / L, (y1 - y0) / L
    pts = []
    for t in np.linspace(0, 1, int(L / 3)):
        o = 4.5 * math.sin(t * n * 2 * math.pi)
        pts.append((x0 + ux * L * t - uy * o, y0 + uy * L * t + ux * o))
    c.line(pts, Y, 1.1)
    for k in range(n):
        t = (k + 0.25) / n
        x, y = x0 + ux * L * t, y0 + uy * L * t
        c.ell(x - uy * 4.5, y + ux * 4.5, 2.6, fill=R); c.ell(x - uy * 4.5, y + ux * 4.5, .9, fill=Y)
        t2 = (k + .75) / n
        c.poly(oval(x0 + ux * L * t2 + uy * 4.5, y0 + uy * L * t2 - ux * 4.5, 2.8, 1.4, math.atan2(uy, ux) + .8, 8), fill=G)
vine((BD, BD / 2), (W - BD, BD / 2), 14); vine((BD, H - BD / 2), (W - BD, H - BD / 2), 14)
vine((BD / 2, BD), (BD / 2, H - BD), 22); vine((W - BD / 2, BD), (W - BD / 2, H - BD), 22)
for x, y in ((BD / 2, BD / 2), (W - BD / 2, BD / 2), (BD / 2, H - BD / 2), (W - BD / 2, H - BD / 2)):
    c.rect(x - 10, y - 10, x + 10, y + 10, fill=R, outline=Y, width=1); c.star(x, y, 7, Y, 4, 0.35)
c.finish()
