"""Sunday Morning - the Borough climbing to its church, bells going. Naive townscape,
red roofs in charge. Every house is drawn: tiles, sashes, chimney pots, smoke."""
import math, random
from common import *

rng = random.Random(1913)
d = D(WH)

# ---- sky: bell-rings spreading from the tower, drawn as fine yellow arcs
TX, TY = 200, 96
for r in range(14, 420, 9):
    d.arc(TX, TY, r, r * 0.92, 180, 360, Y, 1.1 + 1.6 * math.exp(-r / 120))
d.ell(338, 46, 20, fill=Y, outline=K, w=1)
for a in range(0, 360, 15):
    r0, r1 = 24, 31 if (a // 15) % 2 else 28
    d.line([(338 + r0 * math.cos(math.radians(a)), 46 + r0 * math.sin(math.radians(a))),
            (338 + r1 * math.cos(math.radians(a)), 46 + r1 * math.sin(math.radians(a)))], K, 0.8)
def cloud(cx, cy, s):
    for (ox, oy, r) in [(-1.6, 0.2, 0.8), (-0.7, -0.35, 1.0), (0.3, -0.5, 1.15), (1.3, -0.1, 0.9), (2.0, 0.3, 0.6)]:
        d.ell(cx + ox * s, cy + oy * s, r * s, r * s * 0.8, fill=WH, outline=K, w=0.9)
    d.rect(cx - 2.3 * s, cy + 0.2 * s, cx + 2.5 * s, cy + 0.9 * s, fill=WH)
    d.line([(cx - 2.4 * s, cy + 0.9 * s), (cx + 2.6 * s, cy + 0.9 * s)], K, 0.9)
    for k in range(3):
        d.line([(cx - (1.6 - k * 0.3) * s, cy + (0.2 + k * 0.22) * s), (cx + (1.9 - k * 0.5) * s, cy + (0.2 + k * 0.22) * s)], B, 0.5)
cloud(70, 44, 13); cloud(322, 118, 9); cloud(52, 150, 8)
for i in range(13):                                   # gulls wheeling
    a = i * 0.9
    gull(d, 110 + 70 * math.cos(a) + i * 9, 60 + 26 * math.sin(a * 1.3), 4 + (i % 3) * 1.6, K, 0.9)

# ---- the church of St Peter and St Paul, flint tower
def flint(x0, y0, x1, y1, s=4.0):
    d.rect(x0, y0, x1, y1, fill=WH)
    y = y0; r = 0
    while y < y1:
        x = x0 - (s / 2 if r % 2 else 0)
        while x < x1:
            if rng.random() < 0.62:
                d.rect(max(x0, x + 0.5), y + 0.5, min(x1, x + s - 0.5), min(y1, y + s - 0.6), fill=K if rng.random() < 0.8 else B)
            x += s
        y += s; r += 1
    d.rect(x0, y0, x1, y1, outline=K, w=1.2)

nave_y = 232
d.poly([(120, nave_y), (120, 196), (236, 196), (236, nave_y)], fill=WH, outline=K, w=1.2)       # nave
d.poly([(114, 198), (128, 170), (236, 170), (242, 198)], fill=B, outline=K, w=1.2)              # lead roof
for x in range(132, 236, 6):
    d.line([(x, 171), (x - 4 + (x - 132) * 0.07, 197)], WH, 0.5)
for x in range(130, 232, 21):                                                                     # nave windows
    d.poly([(x, 226), (x, 210), (x + 5, 203), (x + 10, 210), (x + 10, 226)], fill=Y, outline=K, w=0.9)
    d.line([(x + 5, 204), (x + 5, 226)], K, 0.6); d.line([(x, 215), (x + 10, 215)], K, 0.5)
    d.poly([(x + 13, 232), (x + 13, 200), (x + 17, 200), (x + 17, 232)], fill=WH, outline=K, w=0.7)   # buttress
flint(176, 98, 224, 232)
for x in range(176, 224, 8):                                                                      # battlements
    d.rect(x, 90, x + 5, 99, fill=WH, outline=K, w=0.9)
for k, yy in enumerate((132, 170, 200)):
    d.rect(173, yy, 227, yy + 3, fill=WH, outline=K, w=0.7)
# louvred bell-opening with the bell showing
d.poly([(188, 130), (188, 112), (200, 102), (212, 112), (212, 130)], fill=K, outline=WH, w=1.4)
d.poly([(195, 127), (196, 117), (200, 112), (204, 117), (205, 127)], fill=Y, outline=K, w=0.6)
d.ell(200, 128.5, 1.8, fill=Y)
# clock
d.ell(200, 152, 11, fill=B, outline=K, w=1.2); d.ell(200, 152, 8.5, outline=Y, w=0.8)
for a in range(0, 360, 30):
    d.ell(200 + 8.5 * math.cos(math.radians(a)), 152 + 8.5 * math.sin(math.radians(a)), 0.7, fill=Y)
d.line([(200, 152), (200, 144.5)], Y, 1.1); d.line([(200, 152), (194.5, 149)], Y, 1.3)            # ten o'clock
d.poly([(193, 232), (193, 214), (200, 206), (207, 214), (207, 232)], fill=R, outline=K, w=1)      # west door
d.line([(200, 207), (200, 232)], K, 0.6)
d.line([(200, 90), (200, 58)], K, 1.3)                                                            # flagstaff, St George
d.rect(201, 59, 223, 73, fill=WH, outline=K, w=0.8); d.rect(210, 59, 213.5, 73, fill=R); d.rect(201, 64.2, 223, 67.6, fill=R)
# yews and graves
for (x, s) in [(102, 1.0), (252, 1.15), (270, 0.8), (88, 0.7)]:
    d.rect(x - 1.5, nave_y - 8, x + 1.5, nave_y + 2, fill=K)
    for k in range(5):
        d.ell(x, nave_y - 8 - k * 7 * s, (11 - k * 2) * s, 7 * s, fill=G, outline=K, w=0.8)
for x in range(96, 300, 13):
    if 112 < x < 244: continue
    d.poly([(x, 236), (x, 229), (x + 2.5, 226.5), (x + 5, 229), (x + 5, 236)], fill=WH, outline=K, w=0.6)

# ---- houses
BODY = [WH, WH, WH, Y, Y, B, G, R]
def house(x, y, w, h, rh, body, roof, kind):
    # roof with tile courses
    if kind == "gable":
        d.poly([(x, y - h), (x + w / 2, y - h - rh), (x + w, y - h)], fill=body, outline=K, w=1)
        d.poly([(x - 2, y - h + 1), (x + w / 2, y - h - rh - 2), (x + w + 2, y - h + 1), (x + w + 2, y - h - 2.5), (x + w / 2, y - h - rh - 6), (x - 2, y - h - 2.5)], fill=roof, outline=K, w=0.6)
        if rh > 9:
            d.ell(x + w / 2, y - h - rh * 0.45, 2.6, fill=K, outline=WH, w=0.5)
    else:
        d.poly([(x - 2, y - h), (x + 3, y - h - rh), (x + w - 3, y - h - rh), (x + w + 2, y - h)], fill=roof, outline=K, w=1)
        tile = WH if roof in (K, B) else K
        for k in range(1, int(rh // 3.2) + 1):
            yy = y - h - rh + k * 3.2
            d.line([(x - 1 + 4 * (1 - k * 3.2 / rh), yy), (x + w + 1 - 4 * (1 - k * 3.2 / rh), yy)], tile, 0.45)
            for xx in range(int(x + 3 + (k % 2) * 2.5), int(x + w - 2), 5):
                d.line([(xx, yy), (xx, yy - 3.2)], tile, 0.4)
        if w > 30 and rng.random() < 0.6:                 # dormer
            dx = x + w * rng.choice((0.3, 0.6))
            d.poly([(dx, y - h - 2), (dx, y - h - rh * 0.6), (dx + 4.5, y - h - rh * 0.6 - 4), (dx + 9, y - h - rh * 0.6), (dx + 9, y - h - 2)], fill=WH, outline=K, w=0.7)
            d.rect(dx + 2.2, y - h - rh * 0.6 + 1, dx + 6.8, y - h - 3.5, fill=K)
    # chimney + pots + smoke
    cx = x + w * rng.choice((0.16, 0.8))
    ct = y - h - rh * (0.75 if kind != "gable" else 0.55) - 9
    d.rect(cx, ct, cx + 6, ct + 13, fill=R if roof != R else WH, outline=K, w=0.8)
    d.rect(cx - 1, ct - 1.5, cx + 7, ct + 1, fill=K)
    for px in (cx + 0.6, cx + 3.6):
        d.rect(px, ct - 5, px + 1.9, ct - 1.5, fill=Y, outline=K, w=0.4)
    if rng.random() < 0.7:
        sx, sy = cx + 3, ct - 6
        pts = [(sx + 2.5 * k * 0.5 + 3.5 * math.sin(k * 0.9), sy - k * 3.2) for k in range(9)]
        d.line(pts, K, 2.2); d.line(pts, WH, 1.2)
    # wall
    if kind != "gable":
        d.rect(x, y - h, x + w, y, fill=body, outline=K, w=1)
    else:
        d.rect(x, y - h, x + w, y, fill=body)
        d.line([(x, y - h), (x, y), (x + w, y), (x + w, y - h)], K, 1)
    ink = K if body in (WH, Y) else WH
    if body == R:                                         # brick courses
        for k in range(1, int(h // 3)):
            d.line([(x + 1, y - k * 3), (x + w - 1, y - k * 3)], K, 0.35)
    if body == WH and rng.random() < 0.35:                # weatherboard
        for k in range(1, int(h // 3.4)):
            d.line([(x + 1, y - k * 3.4), (x + w - 1, y - k * 3.4)], K, 0.3)
    # windows: sashes
    cols = max(2, int(w // 12)); floors = max(1, int(h // 17))
    cw = w / cols
    door_col = rng.randrange(cols)
    shop = floors >= 2 and w > 34 and rng.random() < 0.3
    for f in range(floors):
        for c in range(cols):
            wx, wy = x + c * cw + cw * 0.22, y - h + 4 + f * (h / floors)
            ww, wh_ = cw * 0.56, min(11, h / floors - 7)
            ground = f == floors - 1
            if ground and shop:
                continue
            if ground and c == door_col:
                dc = rng.choice([R, B, G, K]) if body != R else K
                if dc == body: dc = K
                d.rect(wx, y - 14, wx + ww, y, fill=dc, outline=K, w=0.7)
                d.rect(wx + 1.3, y - 12.5, wx + ww - 1.3, y - 8, outline=WH if dc != WH else K, w=0.4)
                d.ell(wx + ww - 1.8, y - 6.5, 0.7, fill=Y)
                d.rect(wx - 1, y - 0.5, wx + ww + 1, y + 1.5, fill=WH, outline=K, w=0.4)
                continue
            lit = rng.random() < 0.18
            d.rect(wx - 0.8, wy - 0.8, wx + ww + 0.8, wy + wh_ + 0.8, fill=WH, outline=K, w=0.5)
            d.rect(wx, wy, wx + ww, wy + wh_, fill=Y if lit else K)
            d.line([(wx + ww / 2, wy), (wx + ww / 2, wy + wh_)], WH if not lit else K, 0.5)
            d.line([(wx, wy + wh_ / 2), (wx + ww, wy + wh_ / 2)], WH if not lit else K, 0.6)
            if rng.random() < 0.3 and not lit:            # curtain
                d.poly([(wx, wy), (wx + ww * 0.45, wy), (wx, wy + wh_)], fill=rng.choice([R, WH, Y]))
            if rng.random() < 0.22:                       # window box
                d.rect(wx - 1, wy + wh_ + 0.8, wx + ww + 1, wy + wh_ + 3, fill=G, outline=K, w=0.4)
                for k in range(3):
                    d.ell(wx + 1 + k * ww / 2.4, wy + wh_ + 0.6, 1.0, fill=R)
    if shop:
        d.rect(x + 2, y - 15, x + w - 2, y - 2, fill=K, outline=K, w=0.6)
        for k in range(3):
            d.rect(x + 4 + k * (w - 6) / 3, y - 13.5, x + 2 + (k + 1) * (w - 6) / 3, y - 3.5, fill=Y if k != 1 else WH, outline=K, w=0.5)
        aw = rng.choice([R, B, G])
        for k in range(int((w + 2) // 4)):
            d.poly([(x - 1 + k * 4, y - 20), (x + 3 + k * 4, y - 20), (x + 1.5 + k * 4, y - 14), (x - 2.5 + k * 4, y - 14)], fill=aw if k % 2 else WH)
        d.line([(x - 1, y - 20), (x + w + 1, y - 20)], K, 0.8); d.line([(x - 3, y - 14), (x + w - 1, y - 14)], K, 0.6)

rows = [(262, 26, 0.74), (296, 30, 0.82), (334, 34, 0.9), (376, 38, 1.0), (424, 44, 1.12)]
for ri, (by, hh, sc) in enumerate(rows):
    x = rng.uniform(-18, -4)
    # a lane of cobbles under each terrace
    d.rect(0, by, W, by + 10, fill=WH)
    for cx in range(0, W, 5):
        d.arc(cx + (ri % 2) * 2.5, by + 6, 2.5, 2, 180, 360, K, 0.4)
    while x < W:
        w = rng.uniform(26, 50) * sc
        h = hh * rng.uniform(0.75, 1.2)
        if ri == 0 and 108 < x + w / 2 < 250:            # leave the churchyard gate open
            x += w; continue
        body = rng.choice(BODY)
        roof = rng.choice([R, R, R, R, K, B])
        if roof == body: roof = K
        house(x, by, w, h, rng.uniform(9, 15) * sc, body, roof, rng.choice(["eaves", "eaves", "gable"]))
        x += w + rng.choice([0, 0, 0, 2])
    # lamp posts and Sunday people in the lane
    for lx in range(int(rng.uniform(10, 40)), W, 96):
        d.line([(lx, by + 7), (lx, by - 16 * sc)], K, 1); d.rect(lx - 2, by - 20 * sc, lx + 2, by - 16 * sc, fill=Y, outline=K, w=0.5)

def person(x, y, s, coat, hat, child=False):
    s *= 0.72 if child else 1
    d.line([(x - 1.4 * s, y), (x - 1.4 * s, y - 6 * s)], K, 1.5 * s * 0.6 + 0.4)
    d.line([(x + 1.4 * s, y), (x + 1.4 * s, y - 6 * s)], K, 1.5 * s * 0.6 + 0.4)
    d.poly([(x - 3.6 * s, y - 4 * s), (x - 2.6 * s, y - 14 * s), (x + 2.6 * s, y - 14 * s), (x + 3.6 * s, y - 4 * s)], fill=coat, outline=K, w=0.7)
    d.ell(x, y - 16.5 * s, 2.5 * s, fill=WH, outline=K, w=0.7)
    d.rect(x - 3.6 * s, y - 18.6 * s, x + 3.6 * s, y - 17.6 * s, fill=hat); d.rect(x - 2.2 * s, y - 21 * s, x + 2.2 * s, y - 18 * s, fill=hat)
    if rng.random() < 0.3 and not child:
        d.rect(x + 3.6 * s, y - 9 * s, x + 6 * s, y - 6 * s, fill=K)       # prayer book
for ri, (by, hh, sc) in enumerate(rows):
    for _ in range(4 + ri * 2):
        px = rng.uniform(10, 390)
        coat = rng.choice([K, K, B, R, G, Y])
        person(px, by + 8.5, 0.72 * sc + 0.2, coat, K if coat != K else rng.choice([R, Y, B]))
        if rng.random() < 0.4:
            person(px + 6 * sc, by + 8.5, 0.72 * sc + 0.2, rng.choice([R, Y, B, G]), K, child=True)

# ---- five telegraph wires across the top street: a stave, with sparrows for notes
py0 = 262
for px in (14, 386):
    d.line([(px, py0 + 8), (px, py0 - 40)], K, 2)
    for k in range(5):
        d.line([(px - 7, py0 - 38 + k * 4.2), (px + 7, py0 - 38 + k * 4.2)], K, 1)
wire = lambda x, k: py0 - 38 + k * 4.2 + 9 * math.sin(math.pi * (x - 14) / 372)
for k in range(5):
    d.line([(x, wire(x, k)) for x in range(14, 387, 6)], K, 0.55)
# the bells' peal - a descending scale, twice - written in birds
scale = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5]
for i in range(16):
    bx = 34 + i * 21.5 + (6 if i >= 8 else 0)
    k = scale[i % 8] + 0.5
    yv = wire(bx, k)
    d.ell(bx, yv - 2.2, 3.1, 2.3, fill=K); d.ell(bx + 2.6, yv - 4.4, 1.5, fill=K)
    d.line([(bx - 2.6, yv - 2), (bx - 6, yv - 0.6)], K, 1); d.line([(bx + 3.8, yv - 4.4), (bx + 5.4, yv - 4)], Y, 0.7)

# ---- quay, harbour wall and the water at the bottom
qy = 480
d.rect(0, 434 + 10, W, qy, fill=WH)
for cx in range(0, W, 6):
    for k in range(4):
        d.arc(cx + (k % 2) * 3, 452 + k * 6, 3, 2.3, 180, 360, K, 0.4)
for _ in range(14):
    px = rng.uniform(8, 392); coat = rng.choice([K, B, R, G, Y, K])
    person(px, rng.uniform(462, 476), 1.25, coat, K if coat != K else rng.choice([R, Y]))
    if rng.random() < 0.5:
        person(px + 8, 476, 1.25, rng.choice([R, Y, G, B]), K, child=True)
d.rect(0, qy, W, qy + 26, fill=R, outline=K, w=1)                                # brick wall
for k in range(1, 6):
    d.line([(0, qy + k * 4.4), (W, qy + k * 4.4)], K, 0.45)
    for x in range(int((k % 2) * 5), W, 10):
        d.line([(x, qy + k * 4.4), (x, qy + (k + 1) * 4.4)], K, 0.4)
d.rect(0, qy - 2, W, qy + 2.5, fill=WH, outline=K, w=0.8)
for x in range(24, W, 58):                                                       # bollards and rings
    d.rect(x, qy - 10, x + 5, qy - 2, fill=K); d.ell(x + 2.5, qy - 10, 3.5, 2, fill=K)
    d.ell(x + 30, qy + 12, 3, outline=K, w=1)
d.rect(0, qy + 26, W, H, fill=B)
for y in range(qy + 29, H, 4):
    x = rng.uniform(-10, 0)
    while x < W:
        ln = rng.uniform(5, 26)
        d.line([(x, y), (x + ln, y)], WH if rng.random() < 0.8 else K, 0.6 + (y - qy) / 110)
        x += ln + rng.uniform(4, 22)
def skiff(cx, cy, L, col, name):
    hull = bez((cx - L / 2, cy - 9), (cx - L * 0.35, cy + 9), (cx, cy + 8), 10) + bez((cx, cy + 8), (cx + L * 0.4, cy + 8), (cx + L / 2, cy - 8), 10)
    d.poly(hull, fill=col, outline=K, w=1.1)
    d.poly(hull[:1] + [(cx - L * 0.36, cy - 4.5), (cx + L * 0.42, cy - 4), hull[-1]], fill=WH, outline=K, w=0.8)
    d.line(bez((cx - L / 2 + 5, cy - 1), (cx, cy + 5), (cx + L / 2 - 3, cy - 1), 10), WH if col != WH else K, 0.6)
    d.line([(cx - L * 0.1, cy - 6), (cx - L * 0.1, cy - 50)], K, 1.5)
    d.poly([(cx - L * 0.1 + 2, cy - 48), (cx - L * 0.1 + 2, cy - 12), (cx + L * 0.36, cy - 12)], fill=WH if col == R else R, outline=K, w=0.8)
    for k in range(1, 5):
        d.line([(cx - L * 0.1 + 2, cy - 12 - k * 7.2), (cx + L * 0.36 - k * (L * 0.46 - 2) / 5, cy - 12)], K, 0.35)
    d.line([(cx - L * 0.1, cy - 50), (cx - L / 2, cy - 9)], K, 0.45)
    d.poly([(cx - L * 0.1, cy - 50), (cx - L * 0.1 - 9, cy - 47.5), (cx - L * 0.1, cy - 45)], fill=Y, outline=K, w=0.4)
    d.text(cx + L * 0.12, cy + 1.6, name, WH if col != WH else K, size=5.6, font="sans")
    d.line([(cx - L / 2, cy - 9), (cx - L / 2 - 14, qy + 12)], K, 0.5)
    for k in range(4):                                                            # reflection
        d.line([(cx - L * 0.3 + k * 3, cy + 12 + k * 3.4), (cx + L * 0.3 - k * 4, cy + 12 + k * 3.4)], col if col != B else K, 1.3)
skiff(86, 548, 96, R, "CECILIA"); skiff(232, 560, 110, K, "LT 22"); skiff(348, 544, 74, G, "ELLEN")
for (bx, by) in [(160, 580), (296, 586), (30, 588)]:
    d.ell(bx, by, 4.5, fill=Y, outline=K, w=0.8); d.line([(bx, by - 4.5), (bx, by - 9)], K, 0.8)
d.save()
