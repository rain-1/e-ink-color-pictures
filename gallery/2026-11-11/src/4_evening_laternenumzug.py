"""Evening — Laternenumzug (St Martin's Eve lantern walk, 11 November).
A flat dusk-blue picture-map of a half-timbered hill town. The one big shape is the white
zigzag of the lane; on it about a hundred walkers carry paper lanterns up to the bonfire
behind St Martin on his white horse. A two-day-old moon follows the sunset down."""
import math, random
from PIL import Image, ImageDraw
from kit import *

random.seed(1111)
im, d = canvas(B)
FULL = (W * S, H * S)
def prof(x): return 150 + 84 * ((x - 215) / 215.0) ** 2            # the hill's skyline

# ---------- sky ----------
for k, (y, c, w) in enumerate([(238, Y, 9), (228, Y, 6), (219, R, 5), (211, R, 3.4), (203, R, 2.2), (196, R, 1.3), (190, R, .7)]):
    line(d, [(0, y), (W, y)], c, w)
for y in range(8, 186, 6):                                          # combed air, thinning upward
    line(d, [(0, y), (W, y)], K, 0.35 + 0.9 * (1 - y / 186))
random.seed(4)
for k in range(70):
    x, y = random.uniform(4, W - 4), random.uniform(4, 150) ** 1.0
    if y < prof(x) - 26: circ(d, x, y, random.choice([.6, .6, .9, 1.3]), fill=Wh)
mx, my = 58, 118                                                    # the young moon: earthshine + thin lit limb
circ(d, mx, my, 13, fill=K); circ(d, mx, my, 13, outline=Wh, w=0.4)
circ(d, mx, my, 13, fill=Y); circ(d, mx - 3.6, my - 3.0, 12.2, fill=K)
for gx, gy in [(300, 44), (0, 0)][:1]:                              # geese going over, a ragged V
    for k in range(-6, 7):
        x, y = gx + k * 9, gy + abs(k) * 5 + (k % 2)
        line(d, [(x - 4, y - 2), (x, y), (x + 4, y - 2.5)], Wh, 1.0)
# ---------- the hill ----------
hill = [(0, H), (0, prof(0))] + [(x, prof(x)) for x in range(0, W + 1, 8)] + [(W, H)]
poly(d, hill, fill=B); line(d, hill[1:-1], K, 1.2)
gl, gd = Image.new("L", FULL, 0), None; gd = ImageDraw.Draw(gl)     # ground texture: slanting grass strokes
for k in range(2600):
    x, y = random.uniform(0, W), random.uniform(150, H)
    gd.line(P([(x, y), (x + 2.2, y - 4)]), fill=255, width=2)
hm = Image.new("L", FULL, 0); ImageDraw.Draw(hm).polygon(P(hill), fill=255)
im.paste(K, (0, 0), Image.composite(gl, Image.new("L", FULL, 0), hm))

PATH = [(-12, 590), (352, 542), (48, 470), (344, 402), (64, 334), (326, 272), (140, 218), (228, 192)]
def seg_y(i, x):
    (xa, ya), (xb, yb) = PATH[i], PATH[i + 1]
    return ya + (yb - ya) * (x - xa) / (xb - xa)

def bare_tree(x, y, h, c=K):
    def br(x, y, a, l, w, n):
        x2, y2 = x + math.cos(a) * l, y + math.sin(a) * l; line(d, [(x, y), (x2, y2)], c, w)
        if n: [br(x2, y2, a + t + random.uniform(-.12, .12), l * .68, max(.45, w * .65), n - 1) for t in (-.55, .5)]
    br(x, y, -math.pi / 2, h * .42, max(.9, h / 16), 4)
def fir(x, y, h):
    for k in range(4):
        yy = y - h * k / 4.6; ww = h * .34 * (1 - k / 5.2)
        poly(d, [(x - ww, yy), (x, yy - h * .42), (x + ww, yy)], fill=G, outline=K, w=0.5)
    line(d, [(x, y), (x, y + 3)], K, 1.2)

def house(x, base, w, h, kind):
    """a half-timbered house: plinth, two framed storeys with braces, lit windows, tiled roof"""
    wall = [Wh, Wh, Y, Wh][kind % 4]; roofc = [R, K, R, K, R][kind % 5]
    gable = kind % 3 == 0
    rh = h * (0.62 if gable else 0.42); top = base - h
    rect(d, x, top, x + w, base, fill=wall, outline=K, w=0.9)
    if kind % 4 != 2:                                                 # dusk falls on the walls: blue wash lines
        for yy in range(int(top) + 2, int(base), 3): line(d, [(x + 1, yy), (x + w - 1, yy)], B, 0.5)
    rect(d, x, base - 4, x + w, base, fill=K)
    fl = top + (h - 4) / 2
    line(d, [(x, fl), (x + w, fl)], K, 1.5)
    n = max(2, int(w // 9))
    for k in range(n + 1):
        px_ = x + w * k / n; line(d, [(px_, top), (px_, base)], K, 0.9)
    for k in range(n):
        x0, x1_ = x + w * k / n, x + w * (k + 1) / n
        for y0, y1_ in ((top, fl), (fl, base - 4)):
            if (k + kind) % 2 == 0 and x1_ - x0 > 5:                  # window, lit or shuttered
                lit = random.random() < .72
                rect(d, x0 + 1.6, y0 + 3, x1_ - 1.6, y1_ - 3.5, fill=Y if lit else K, outline=K, w=0.7)
                line(d, [((x0 + x1_) / 2, y0 + 3), ((x0 + x1_) / 2, y1_ - 3.5)], K, 0.5); line(d, [(x0 + 1.6, (y0 + y1_) / 2 - .5), (x1_ - 1.6, (y0 + y1_) / 2 - .5)], K, 0.5)
                if lit and random.random() < .3: circ(d, (x0 + x1_) / 2 - 1.5, y1_ - 6.5, 1.5, fill=K)       # somebody watching
                rect(d, x0 + .8, y1_ - 3.6, x1_ - .8, y1_ - 2.4, fill=R)                                     # window box
            else:                                                      # St Andrew's brace
                line(d, [(x0, y0), (x1_, y1_)], K, 0.7)
                if (k + kind) % 3 == 0: line(d, [(x1_, y0), (x0, y1_)], K, 0.7)
    dk = (kind * 7) % n; x0 = x + w * dk / n + 1.5; x1_ = x + w * (dk + 1) / n - 1.5                         # door
    rect(d, x0, fl + 3, x1_, base, fill=[G, R, K][kind % 3], outline=K, w=0.7); circ(d, x1_ - 1.6, (fl + base) / 2 + 2, .7, fill=Y)
    if gable:
        g = [(x - 3, top), (x + w / 2, top - rh), (x + w + 3, top)]
        poly(d, g, fill=wall, outline=K, w=0.9)
        for t in (.3, .5, .7): line(d, [(x + w * t, top), (x + w * t, top - rh * (1 - abs(t - .5) * 2) + 1)], K, 0.7)
        line(d, [(x + w * .22, top - rh * .42), (x + w * .78, top - rh * .42)], K, 0.8)
        rect(d, x + w / 2 - 2.6, top - rh * .36, x + w / 2 + 2.6, top - rh * .08, fill=Y, outline=K, w=0.6)
        line(d, [g[0], g[1]], roofc, 3.2); line(d, [g[1], g[2]], roofc, 3.2); line(d, g, K, 0.6)
        ridge = (x + w / 2, top - rh)
    else:
        rf = [(x - 3, top), (x + 4, top - rh), (x + w - 4, top - rh), (x + w + 3, top)]
        poly(d, rf, fill=roofc, outline=K, w=0.9)
        tc = K if roofc == R else Wh
        for q in range(1, 4):
            yy = top - rh * q / 4; line(d, [(x - 3 + 7 * q / 4, yy), (x + w + 3 - 7 * q / 4, yy)], tc, 0.45)
        for q in range(int(w // 4)): line(d, [(x + 2 + q * 4 + (2 if q % 2 else 0), top - 1), (x + 3 + q * 4, top - rh + 1)], tc, 0.3)
        if w > 30: poly(d, [(x + w / 2 - 5, top - rh * .2), (x + w / 2, top - rh * .75), (x + w / 2 + 5, top - rh * .2)], fill=Y, outline=K, w=0.6)    # dormer
        ridge = (x + w * .7, top - rh)
    cx = ridge[0] + (6 if gable else 0); cy = ridge[1] + (8 if gable else 0)
    rect(d, cx - 2, cy - 7, cx + 2, cy + 1, fill=R, outline=K, w=0.5)
    pts = [(cx + 5 * math.sin(t * .9) + t * 1.2, cy - 8 - t * 3.2) for t in range(0, 9)]; line(d, pts, Wh, 0.9)      # smoke

def lantern(x, y, r, kind):
    for k in range(10):                                                # halo of light on the dark
        a = k * math.pi / 5 + kind; circ(d, x + math.cos(a) * (r + 2.8), y + math.sin(a) * (r + 2.8), .55, fill=Y)
    k5 = kind % 6
    if k5 == 0:   circ(d, x, y, r, fill=Y, outline=K, w=0.5); line(d, [(x - r, y), (x + r, y)], R, 0.9); line(d, [(x - r * .8, y - r * .55), (x + r * .8, y - r * .55)], R, 0.6); line(d, [(x - r * .8, y + r * .55), (x + r * .8, y + r * .55)], R, 0.6)
    elif k5 == 1: circ(d, x, y, r, fill=R, outline=K, w=0.5); circ(d, x, y, r * .5, fill=Y)
    elif k5 == 2:                                                      # a star
        poly(d, [(x + math.cos(q * math.pi / 5 - 1.57) * (r * 1.35 if q % 2 == 0 else r * .55), y + math.sin(q * math.pi / 5 - 1.57) * (r * 1.35 if q % 2 == 0 else r * .55)) for q in range(10)], fill=Y, outline=K, w=0.4)
    elif k5 == 3:                                                      # a paper boat, for Signac
        poly(d, [(x - r * 1.3, y), (x + r * 1.3, y), (x + r * .8, y + r * .8), (x - r * .8, y + r * .8)], fill=Y, outline=K, w=0.4)
        poly(d, [(x, y - 1), (x, y - r * 1.5), (x + r, y - 1)], fill=Wh, outline=K, w=0.4); poly(d, [(x - 1, y - 1), (x - 1, y - r * 1.1), (x - r * .8, y - 1)], fill=R)
    elif k5 == 4: rect(d, x - r * .8, y - r, x + r * .8, y + r, fill=Wh, outline=K, w=0.5); rect(d, x - r * .8, y - r * .3, x + r * .8, y + r * .3, fill=Y); line(d, [(x, y - r), (x, y + r)], R, 0.6)
    else:                                                              # a moon face
        circ(d, x, y, r, fill=Y, outline=K, w=0.5); circ(d, x + r * .5, y - r * .2, r * .8, fill=Wh); circ(d, x - r * .3, y - r * .2, .5, fill=K)

def walker(x, y, s, dr, kind, lit=True):
    tall = 1.45 if kind % 4 == 0 else 1.0; u = s * tall
    coat = [K, K, R, K, G, K, Wh][kind % 7] if s > 1.0 else K
    line(d, [(x - 1.4 * u, y - 4 * u), (x - 2 * u + dr * (kind % 2) * u, y)], K, 1.1 * u); line(d, [(x + 1.4 * u, y - 4 * u), (x + 2 * u - dr * (kind % 2) * u, y)], K, 1.1 * u)
    poly(d, [(x - 2.4 * u, y - 11 * u), (x + 2.4 * u, y - 11 * u), (x + 3.8 * u, y - 3.5 * u), (x - 3.8 * u, y - 3.5 * u)], fill=coat, outline=K, w=0.5)
    circ(d, x, y - 13.4 * u, 2.3 * u, fill=Wh, outline=K, w=0.5)
    hat = [R, Y, Wh, G, R, K][kind % 6]
    if kind % 3 == 0: poly(d, [(x - 2.5 * u, y - 14.6 * u), (x + dr * -1 * u, y - 19.5 * u), (x + 2.5 * u, y - 14.6 * u)], fill=hat, outline=K, w=0.4); circ(d, x + dr * -1 * u, y - 19.8 * u, .9 * u, fill=Wh)
    else: d.pieslice([(x - 2.6 * u) * S, (y - 16.4 * u) * S, (x + 2.6 * u) * S, (y - 11 * u) * S], 180, 360, fill=hat, outline=K)
    line(d, [(x - 2 * u, y - 10.4 * u), (x + 2 * u, y - 10.4 * u)], [Y, R, Wh][kind % 3], 1.0 * u)                    # scarf
    if lit:
        tip = (x + dr * 8.5 * u, y - (20 + (kind % 3) * 2.5) * u)
        line(d, [(x + dr * 2.5 * u, y - 8 * u), tip], K, 0.6); line(d, [tip, (tip[0], tip[1] + 2.2 * u)], K, 0.4)
        lantern(tip[0], tip[1] + (2.2 + 3.4) * u, 3.4 * u, kind)

def goose(x, y, s, dr):
    ell(d, x, y - 5 * s, 6 * s, 4 * s, fill=Wh, outline=K, w=0.5); line(d, [(x + dr * 4 * s, y - 7 * s), (x + dr * 7 * s, y - 13 * s)], K, 3.0 * s); line(d, [(x + dr * 4 * s, y - 7 * s), (x + dr * 7 * s, y - 13 * s)], Wh, 1.9 * s)
    circ(d, x + dr * 7.4 * s, y - 14 * s, 2 * s, fill=Wh, outline=K, w=0.4); poly(d, [(x + dr * 9 * s, y - 15 * s), (x + dr * 12.5 * s, y - 13.6 * s), (x + dr * 9 * s, y - 13 * s)], fill=Y)
    line(d, [(x - 1 * s, y - 1.5 * s), (x - 1 * s, y)], Y, 1); line(d, [(x + 2 * s, y - 1.5 * s), (x + 2 * s, y)], Y, 1)
    poly(d, [(x - dr * 5 * s, y - 7 * s), (x - dr * 9 * s, y - 9 * s), (x - dr * 6 * s, y - 4 * s)], fill=Wh, outline=K, w=0.4)

# ---------- the church on the crown, the bonfire in the square ----------
cb = 180
rect(d, 252, cb - 34, 322, cb, fill=Wh, outline=K, w=1)
for yy in range(cb - 32, cb, 3): line(d, [(253, yy), (321, yy)], B, 0.5)
poly(d, [(248, cb - 34), (258, cb - 58), (322, cb - 58), (326, cb - 34)], fill=R, outline=K, w=1)
for q in range(1, 5): line(d, [(250 + q * 2, cb - 34 - q * 5), (325 - q * .8, cb - 34 - q * 5)], K, 0.4)
for k in range(4):
    x = 262 + k * 15
    poly(d, [(x - 3.5, cb - 5), (x - 3.5, cb - 22), (x, cb - 27), (x + 3.5, cb - 22), (x + 3.5, cb - 5)], fill=Y, outline=K, w=0.7); line(d, [(x, cb - 27), (x, cb - 5)], K, 0.5); line(d, [(x - 3.5, cb - 15), (x + 3.5, cb - 15)], R, 0.6)
rect(d, 226, cb - 76, 254, cb, fill=Wh, outline=K, w=1)
for yy in range(cb - 74, cb, 3): line(d, [(227, yy), (253, yy)], B, 0.5)
for yy in (cb - 52, cb - 28): line(d, [(226, yy), (254, yy)], K, 1)
poly(d, [(222, cb - 76), (240, cb - 132), (258, cb - 76)], fill=K, outline=K, w=1)
for q in range(1, 7): line(d, [(224 + q * 2.4, cb - 76 - q * 7.6), (256 - q * 2.4, cb - 76 - q * 7.6)], B, 0.5)
line(d, [(240, cb - 132), (240, cb - 146)], K, 1); line(d, [(236, cb - 141), (244, cb - 141)], K, 1); circ(d, 240, cb - 133, 1.8, fill=Y)
circ(d, 240, cb - 64, 7, fill=Wh, outline=K, w=0.8); line(d, [(240, cb - 64), (240, cb - 69)], K, 0.8); line(d, [(240, cb - 64), (243, cb - 64)], K, 0.8)   # clock: six
for x in (234, 246): rect(d, x - 2, cb - 46, x + 2, cb - 34, fill=K)
poly(d, [(234, cb), (234, cb - 16), (240, cb - 22), (246, cb - 16), (246, cb)], fill=Y, outline=K, w=0.8)
# bonfire
fx, fy = 176, 196
for k in range(60):
    t = random.random(); a = random.uniform(-.5, .5)
    circ(d, fx + a * 60 * t + 10 * math.sin(t * 9 + k), fy - 24 - t * 120, random.choice([.6, .9, 1.2]), fill=random.choice([Y, Y, R]))
for k, (dx_, hh, c) in enumerate([(-9, 22, R), (8, 24, R), (0, 34, R), (-5, 18, Y), (5, 20, Y), (0, 25, Y), (0, 13, Wh)]):
    poly(d, [(fx + dx_ - 7, fy), (fx + dx_ - 3 + 3 * math.sin(k), fy - hh * .55), (fx + dx_ + 2 * math.cos(k * 2), fy - hh), (fx + dx_ + 4, fy - hh * .5), (fx + dx_ + 7, fy)], fill=c)
for a in (-.9, -.3, .3, .9): line(d, [(fx - 14 * math.sin(a) - 9 * math.cos(a), fy + 2), (fx + 11 * math.sin(a) * 0 + 9 * math.cos(a) + 4 * a, fy - 7)], K, 1.8)
for k in range(8): walker(fx - 40 + k * 12 + (18 if k > 3 else 0), fy + 6 + (k % 2) * 3, .62, 1 if k < 4 else -1, k + 2, lit=False)
bare_tree(206, 178, 46); bare_tree(120, 186, 40); bare_tree(350, 190, 50); bare_tree(86, 204, 34); fir(376, 206, 30); fir(30, 236, 34); fir(392, 232, 26)

# ---------- terraces: houses, lane, walkers — painted from the top down ----------
hk = 0
for i in range(len(PATH) - 2, -1, -1):
    (xa, ya), (xb, yb) = PATH[i], PATH[i + 1]
    if i < len(PATH) - 2:                                              # houses stand above this stretch of lane
        x = 6.0
        while x < W - 20:
            w = random.choice([28, 32, 36, 42, 46])
            xm = x + w / 2
            if not (min(xa, xb) - 6 < xm < max(xa, xb) + 6): x += 14; continue
            base = seg_y(i, xm) - 15
            up = seg_y(i + 1, min(max(xm, min(PATH[i + 1][0], PATH[i + 2][0])), max(PATH[i + 1][0], PATH[i + 2][0])))
            gap = base - up - 9
            if gap > 30:
                h = min(34, gap * 0.56); hk += 1
                house(x, base, w, h, hk)
                if random.random() < .5: bare_tree(x + w + 5, base, random.uniform(20, 30))
                x += w + random.choice([3, 5, 12])
            else:
                if gap > 14 and random.random() < .7: (fir if random.random() < .5 else bare_tree)(xm, base, min(26, gap + 6))
                elif gap > 6:
                    for q in range(4): circ(d, xm - 9 + q * 6, base - 2, 2.2, fill=G, outline=K, w=0.4)                 # cabbages
                x += 18
    wd = 7 + 4.5 * (ya / H)
    line(d, [(xa, ya), (xb, yb)], K, wd + 1.6); line(d, [(xa, ya), (xb, yb)], Wh, wd)
    circ(d, xb, yb, wd / 2 + .8, fill=K); circ(d, xb, yb, wd / 2, fill=Wh)
    L = math.hypot(xb - xa, yb - ya); n = int(L / 9)
    for k in range(n):                                                 # cobbles
        t = (k + .5) / n; line(d, [(xa + (xb - xa) * t - 1.5, ya + (yb - ya) * t + ((k % 3) - 1) * wd * .28), (xa + (xb - xa) * t + 1.5, ya + (yb - ya) * t + ((k % 3) - 1) * wd * .28)], B, 0.5)
    for k in range(int(L / 26)):                                       # fence posts on the downhill side
        t = (k + .5) / int(L / 26); px_, py_ = xa + (xb - xa) * t, ya + (yb - ya) * t + wd / 2 + 1
        line(d, [(px_, py_), (px_, py_ + 5)], K, 0.8)
    dr = 1 if xb > xa else -1
    s = 0.62 + 0.62 * ((ya + yb) / 2 / H)
    step = 20 * s
    if i <= 4:
        stop = 0.62 if i == 4 else 1.0
        m = int(L * stop / step)
        for k in range(m):
            t = (k + .6) * step / L
            hk += 1; walker(xa + (xb - xa) * t, ya + (yb - ya) * t + random.uniform(-1.2, 1.6), s, dr, hk + k * 3)
        if i == 4:                                                     # St Martin on the white horse, and the beggar
            t = 0.74; hx, hy = xa + (xb - xa) * t, ya + (yb - ya) * t + 1; q = 1.0
            for lx_ in (-8, -5, 6, 9): line(d, [(hx + lx_, hy - 10), (hx + lx_ + (1 if lx_ % 2 else -1), hy)], K, 2.4); line(d, [(hx + lx_, hy - 10), (hx + lx_ + (1 if lx_ % 2 else -1), hy - .6)], Wh, 1.4)
            ell(d, hx, hy - 13, 12, 6, fill=Wh, outline=K, w=0.7)
            poly(d, [(hx + 8, hy - 16), (hx + 15, hy - 28), (hx + 20, hy - 26), (hx + 13, hy - 11)], fill=Wh, outline=K, w=0.7)
            poly(d, [(hx + 14, hy - 29), (hx + 24, hy - 25), (hx + 23, hy - 21), (hx + 16, hy - 23)], fill=Wh, outline=K, w=0.7); poly(d, [(hx + 14, hy - 29), (hx + 15, hy - 33), (hx + 17.5, hy - 28)], fill=Wh, outline=K, w=0.5)
            circ(d, hx + 18.6, hy - 26, .7, fill=K); line(d, [(hx + 9, hy - 18), (hx + 14, hy - 28)], K, 1.4)
            line(d, [(hx - 12, hy - 14), (hx - 18, hy - 6)], K, 2.2); line(d, [(hx + 22, hy - 23), (hx + 4, hy - 20)], R, 0.6)
            poly(d, [(hx - 4, hy - 30), (hx + 4, hy - 30), (hx + 7, hy - 14), (hx - 12, hy - 9), (hx - 8, hy - 20)], fill=R, outline=K, w=0.7)       # the cloak
            circ(d, hx, hy - 33.5, 3, fill=Wh, outline=K, w=0.5); d.pieslice([(hx - 3.6) * S, (hy - 38) * S, (hx + 3.6) * S, (hy - 31) * S], 180, 360, fill=Y, outline=K)
            poly(d, [(hx - 1, hy - 37.5), (hx, hy - 42), (hx + 2, hy - 37.5)], fill=R)
            line(d, [(hx + 3, hy - 27), (hx + 9, hy - 35)], K, 0.8); line(d, [(hx + 9, hy - 35), (hx + 11, hy - 44)], Wh, 1.1)                       # sword raised to cut the cloak
            bx_, by_ = hx + 40, hy - 6 + (yb - ya) / (xb - xa) * 40
            poly(d, [(bx_ - 5, by_), (bx_ - 3, by_ - 9), (bx_ + 3, by_ - 9), (bx_ + 7, by_)], fill=K); circ(d, bx_, by_ - 11.5, 2.4, fill=Wh, outline=K, w=0.5); line(d, [(bx_ - 2, by_ - 6), (bx_ - 9, by_ - 11)], Wh, 1.2)
    if i == 0:                                                         # geese bringing up the rear, and a dog
        for k in range(5): goose(26 + k * 17, seg_y(0, 26 + k * 17) + 2 - (k % 2) * 2, 1.25, 1)
# foreground: garden fence, cabbages, a row of pollards
for x in range(0, W + 6, 7):
    yb_ = 598; line(d, [(x, yb_), (x, yb_ - 13 - (x % 14 == 0) * 2)], Wh, 1.6); poly(d, [(x - 1, yb_ - 13), (x, yb_ - 16), (x + 1, yb_ - 13)], fill=Wh)
line(d, [(0, 590), (W, 590)], Wh, 1.1)
for k in range(14): circ(d, 150 + k * 18, 580 - (k % 2) * 3, 4, fill=G, outline=K, w=0.5); circ(d, 150 + k * 18, 580 - (k % 2) * 3, 1.6, fill=Wh)
save(im)
