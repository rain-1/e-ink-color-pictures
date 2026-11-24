# Morning — "Moonset over the Beaver Pond". Full palette, blue in charge.
# A shin-hanga style landscape: the Beaver Moon going down over spruce ridges while the east
# (off-frame) warms the horizon. Lodge and dam in the still pond, a beaver towing a wake,
# birches on the near bank — one of them freshly felled, with its pencil-point stump and chips.
import math, random
import numpy as np
from common import *
rng = random.Random(1124); img, d = new(B)
HZ = 300                                              # far shoreline

# --- sky: night blue thinning downward, then a band of first light
sky = YY < HZ
tone(img, sky, B, Wh, np.clip((YY - 20) / 300, 0, 0.72) ** 1.25)
glow = np.clip((YY - 232) / 60, 0, 1)
tone(img, sky & (YY > 232), None, Y, glow * 0.95)
tone(img, sky & (YY > 262), None, R, np.clip((YY - 262) / 60, 0, 0.6))
for _ in range(70):                                    # last stars
    x, y = rng.randrange(W), rng.randrange(0, 150)
    if rng.random() < 0.6 * (1 - y / 150) + 0.1: d.point((x, y), fill=Wh)
vx, vy = 92, 96                                         # the morning star
d.line((vx - 6, vy, vx + 6, vy), fill=Wh); d.line((vx, vy - 6, vx, vy + 6), fill=Wh)
d.ellipse((vx - 2, vy - 2, vx + 2, vy + 2), fill=Wh)
d.ellipse((120, 131, 122, 133), fill=Wh); d.point((129, 138), fill=R); d.point((130, 138), fill=R)

# --- the moon, with its seas, and thin bars of cloud across it
mx, my, mr = 282, 158, 44
moon = ell_mask(mx, my, mr, mr)
tone(img, moon, Wh, Wh, 1)
seas = np.zeros((H, W), bool)
for (u, v, r) in [(-.25, -.5, .3), (.28, -.45, .2), (.48, -.15, .22), (.76, -.3, .11), (.7, .1, .15),
                  (-.6, -.2, .34), (-.25, .35, .22), (-.58, .4, .12), (.5, .27, .1)]:
    seas |= ell_mask(mx + u * mr, my + v * mr, r * mr, r * mr)
tone(img, moon & seas, None, B, 0.34 + 0.2 * fbm(3, 12, 2))
d.ellipse((mx - mr, my - mr, mx + mr, my + mr), outline=Y)
for (cy, x0, x1) in [(176, 215, 360), (181, 236, 400), (140, 300, 352), (187, 190, 300)]:
    for k in range(3):
        d.line((x0 + k * 9, cy + k, x1 - k * 14, cy + k), fill=Wh if k < 2 else B)

# --- three ridges of spruce, receding; mist between
def ridge(base, amp, seed, col, step, th):
    r2 = random.Random(seed); pts = [(0, HZ)]; x = -5
    while x < W + 10:
        y = base + amp * math.sin(x / 61 + seed) + amp * 0.5 * math.sin(x / 23 + seed * 2)
        t = r2.uniform(th * 0.5, th)
        pts += [(x - step / 2, y), (x, y - t), (x + step / 2, y)]; x += step * r2.uniform(0.7, 1.2)
    pts.append((W, HZ)); return pts
m1 = poly_mask(ridge(236, 12, 1, B, 7, 11)); tone(img, m1, B, Wh, 0.22)
mist = sky & (YY > 252) & (YY < 276)
tone(img, mist, None, Wh, 0.85 * np.exp(-((YY - 263) / 7) ** 2) * (0.5 + fbm(5, 90, 2)))
m2 = poly_mask(ridge(268, 7, 2, B, 9, 14)); tone(img, m2, B, K, 0.3)
mist2 = sky & (YY > 272) & (YY < 292)
tone(img, mist2, None, Wh, 0.8 * np.exp(-((YY - 283) / 5) ** 2) * (0.4 + fbm(6, 70, 2)))
m3 = poly_mask(ridge(289, 4, 3, K, 6, 15)); tone(img, m3, K, G, 0.28)
for x in range(4, W, 11):                               # a few bare aspens on the far shore
    if rng.random() < 0.5:
        d.line((x, HZ, x + rng.randint(-1, 1), HZ - rng.randint(14, 24)), fill=Wh)

# --- the lodge, on the far side of the pond
lx, lw, lh = 138, 62, 34
lodge = [(lx - lw, HZ)] + [(lx + lw * math.cos(a), HZ - lh * math.sin(a) ** 0.8 - rng.uniform(0, 3))
                           for a in np.linspace(math.pi, 0, 26)] + [(lx + lw, HZ)]
d.polygon(lodge, fill=K)
lm = poly_mask(lodge)
for _ in range(260):
    x = rng.uniform(lx - lw, lx + lw); y = rng.uniform(HZ - lh, HZ)
    a = math.atan2(-(y - HZ) * 1.6, -(x - lx)) + math.pi / 2 + rng.uniform(-0.5, 0.5); L = rng.uniform(4, 11)
    p = (x - math.cos(a) * L, y - math.sin(a) * L, x + math.cos(a) * L, y + math.sin(a) * L)
    if lm[int(min(max(p[1], 0), H - 1)), int(min(max(p[0], 0), W - 1))] and lm[int(min(max(p[3], 0), H - 1)), int(min(max(p[2], 0), W - 1))]:
        d.line(p, fill=rng.choice([Y, Y, Wh, R, G]))
for k in range(5):                                      # loose poles on the crown
    a = -math.pi / 2 + rng.uniform(-0.9, 0.9)
    d.line((lx + k * 5 - 10, HZ - lh + 3, lx + k * 5 - 10 + math.cos(a) * 12, HZ - lh + 3 + math.sin(a) * 12), fill=K)

# --- water: a jittered mirror of everything above, deepened with blue
a = np.asarray(img).copy()
for y in range(HZ, H):
    src = int(HZ - 1 - (y - HZ) * 0.86)
    if src < 0: src = 0
    a[y] = np.roll(a[src], int(round(2.2 * math.sin(y / 2.3) * (0.3 + (y - HZ) / 200))), axis=0)
img.paste(Image.fromarray(a))
water = YY >= HZ
tone(img, water, None, B, 0.3 + 0.25 * (YY - HZ) / 300)
band = water & (((YY - HZ) % 7) < 1)
tone(img, band, None, B, 0.8)
d.line((0, HZ, W, HZ), fill=K)
for _ in range(120):                                     # glints
    y = rng.randrange(HZ + 6, H); x = rng.randrange(W); L = rng.randint(3, 14)
    d.line((x, y, x + L, y), fill=Wh if abs(x - mx) < 60 else rng.choice([Wh, B, B]))
for y in range(HZ + 44, 470, 3):                         # the moon's road on the water
    wdt = 6 + (y - HZ) * 0.16 + rng.uniform(-4, 4); cx = mx + rng.uniform(-3, 3)
    d.line((cx - wdt, y, cx + wdt, y), fill=Wh)
    if rng.random() < 0.4: d.line((cx - wdt - 8, y + 1, cx - wdt - 2, y + 1), fill=Y)

# --- the dam: a long stitched curve of sticks, white water spilling below it
for i in range(170):
    t = i / 169; x = 205 + t * 215; y = 346 + 26 * t * t + 5 * math.sin(t * 9)
    aa = rng.uniform(-1.2, -0.2) if rng.random() < 0.5 else rng.uniform(-2.9, -1.9); L = rng.uniform(5, 13)
    d.line((x, y + 3, x + math.cos(aa) * L, y + 3 + math.sin(aa) * L), fill=K, width=2 if rng.random() < 0.3 else 1)
    if i % 3 == 0: d.line((x, y + 1, x + rng.uniform(3, 8), y - rng.uniform(1, 5)), fill=Y)
    if i % 2 == 0: d.line((x - 2, y + 6 + rng.randint(0, 2), x + 4, y + 6 + rng.randint(0, 2)), fill=Wh)

# --- a beaver crossing, towing its wake
bx, by = 196, 430
for k in range(1, 16):
    s = k * 5.2
    d.line((bx + s, by - s * 0.34, bx + s + 5, by - s * 0.34 - 1), fill=Wh)
    d.line((bx + s, by + s * 0.34, bx + s + 5, by + s * 0.34 + 1), fill=Wh)
    if k % 2: d.line((bx + s + 2, by, bx + s + 7 + k, by), fill=B)
d.ellipse((bx - 9, by - 4, bx + 5, by + 3), fill=K); d.ellipse((bx + 2, by - 2, bx + 16, by + 2), fill=K)
d.point((bx - 5, by - 2), fill=Wh); d.ellipse((bx - 2, by - 6, bx, by - 4), fill=K)
d.line((bx - 12, by + 4, bx - 2, by + 5), fill=Wh)

# --- near bank
n = fbm(9, 40, 3)
bank = [(0, 486)] + [(x, 486 + (x / 300) ** 1.6 * 120 + 10 * n[500, min(x, W - 1)]) for x in range(0, 300, 6)] + [(300, H), (0, H)]
d.polygon(bank, fill=K)
rb = [(W, 520)] + [(x, 520 + ((W - x) / 110) ** 1.5 * 80) for x in range(W, 290, -6)] + [(290, H), (W, H)]
d.polygon(rb, fill=K)
tone(img, poly_mask(bank) | poly_mask(rb), None, G, 0.16 * fbm(10, 14, 2))

def birch(x0, x1, yb, wd, lean):
    """White trunk from (x0,yb) up to (x1,-10) with lenticels, scars and fine twigs."""
    steps = 60; pl = []; pr = []
    for i in range(steps + 1):
        t = i / steps; x = x0 + (x1 - x0) * t + lean * math.sin(t * 3); y = yb + (-10 - yb) * t
        w = wd * (1 - 0.45 * t); pl.append((x - w / 2, y)); pr.append((x + w / 2, y))
    poly = pl + pr[::-1]; d.polygon(poly, fill=Wh, outline=K)
    m = poly_mask(poly)
    tone(img, m & (XX > np.interp(YY[:, 0], [p[1] for p in pr][::-1], [p[0] for p in pr][::-1])[:, None] - wd * 0.3), None, B, 0.45)
    for i in range(steps):
        (xl, y), (xr, _) = pl[i], pr[i]
        for _ in range(2):
            yy = y - rng.uniform(0, (yb + 10) / steps); a = rng.uniform(xl + 1, xr - 2); L = rng.uniform(2, (xr - xl) * 0.6)
            d.line((a, yy, min(a + L, xr - 1), yy), fill=K)
        if rng.random() < 0.10:
            cx = rng.uniform(xl + 2, xr - 2); d.polygon([(cx - 4, y), (cx + 4, y), (cx, y - 5)], fill=K)
        if rng.random() < 0.16 and y < yb - 60:
            side = rng.choice([-1, 1]); tips = []
            branch(d, xl if side < 0 else xr, y, -math.pi / 2 + side * rng.uniform(0.7, 1.2), rng.uniform(26, 50),
                   2.2, 5, K, rng, 0.5, 0.7, tips, bend=0.05 * side)
            for (tx, ty) in tips:
                if rng.random() < 0.22: d.ellipse((tx - 1, ty, tx + 1, ty + 3), fill=rng.choice([Y, Y, R]))
birch(48, 30, 560, 26, 6); birch(98, 122, 540, 15, -4); birch(372, 392, 560, 20, 3); birch(12, -2, 600, 12, 2)

# --- the felled birch: stump, chips, and the trunk lying out into the pond
sx, sy = 190, 548
d.polygon([(sx - 11, sy + 14), (sx - 10, sy - 8), (sx - 2, sy - 26), (sx + 3, sy - 26), (sx + 10, sy - 8), (sx + 11, sy + 14)], fill=Wh, outline=K)
d.polygon([(sx - 9, sy - 9), (sx - 2, sy - 26), (sx + 3, sy - 26), (sx + 9, sy - 9)], fill=Y, outline=K)
for k in range(5): d.line((sx - 6 + k * 3, sy - 10, sx - 1 + k, sy - 24), fill=R)
for k in range(4): d.line((sx - 9, sy + k * 5 - 4, sx - 2 + k, sy + k * 5 - 4), fill=K)
for _ in range(46):
    x = sx + rng.gauss(0, 22); y = sy + 12 + rng.uniform(-4, 22)
    d.line((x, y, x + rng.uniform(2, 5), y + rng.uniform(-2, 1)), fill=rng.choice([Y, Y, Wh]))
log = [(sx + 16, sy - 8), (sx + 22, sy - 20), (330, 462), (327, 455)]
d.polygon(log, fill=Wh, outline=K)
for k in range(16):
    t = k / 16; x = sx + 20 + t * 135; y = sy - 14 - t * 86
    d.line((x, y, x + 3, y + 5), fill=K)
    if k > 5 and k % 2:
        branch(d, x, y, -math.pi / 2 + rng.choice([-1, 1]) * 0.9 - 0.5, 22, 1.5, 3, K, rng, 0.5, 0.7)
d.polygon([(sx + 12, sy - 10), (sx + 22, sy - 20), (sx + 20, sy - 6)], fill=Y, outline=K)

# --- sedge, cattails, and a heron standing in the shallows
for _ in range(240):
    x = rng.uniform(0, W); 
    if 205 < x < 300 and rng.random() < 0.8: continue
    y = 600 - rng.uniform(0, 40) if x > 150 else 500 + (x / 300) ** 1.6 * 120 + rng.uniform(-4, 30)
    L = rng.uniform(14, 44); a = -math.pi / 2 + rng.gauss(0, 0.28)
    c = rng.choice([K, K, K, G, Y])
    d.line((x, y, x + math.cos(a) * L * 0.6, y + math.sin(a) * L * 0.6, x + math.cos(a + 0.3) * L, y + math.sin(a + 0.1) * L), fill=c)
for (x, y, L) in [(306, 600, 96), (318, 600, 74), (296, 600, 60), (334, 600, 110), (347, 600, 82), (262, 600, 52), (275, 600, 70)]:
    x2 = x + rng.uniform(-8, 8); d.line((x, y, x2, y - L), fill=K, width=2)
    d.rounded_rectangle((x2 - 3, y - L - 2, x2 + 2, y - L + 18), 2, fill=K); d.line((x2 - 1, y - L, x2 - 1, y - L + 15), fill=R)
    d.line((x2, y - L - 2, x2, y - L - 10), fill=K)
hx, hy = 246, 506
d.line((hx, hy, hx - 1, hy + 30), fill=K); d.line((hx + 5, hy, hx + 7, hy + 30), fill=K)
d.ellipse((hx - 10, hy - 16, hx + 14, hy + 2), fill=Wh, outline=K); d.polygon([(hx + 6, hy - 6), (hx + 22, hy + 4), (hx + 8, hy + 2)], fill=K)
d.line((hx - 6, hy - 12, hx - 12, hy - 26, hx - 5, hy - 36, hx - 10, hy - 46), fill=Wh, width=3)
d.line((hx - 8, hy - 12, hx - 14, hy - 26, hx - 7, hy - 36, hx - 12, hy - 46), fill=K)
d.ellipse((hx - 14, hy - 51, hx - 6, hy - 44), fill=Wh, outline=K); d.line((hx - 14, hy - 48, hx - 28, hy - 45), fill=Y, width=2)
d.line((hx - 7, hy - 50, hx + 2, hy - 54), fill=K); d.point((hx - 11, hy - 48), fill=K)
d.ellipse((hx - 8, hy + 28, hx + 12, hy + 32), outline=Wh)

# --- seal: 霜月, "frost month"
d.rectangle((356, 20, 380, 68), fill=R); f = font("WenQuanYi Zen Hei", 18)
d.text((359, 22), "霜", font=f, fill=Wh); d.text((359, 44), "月", font=f, fill=Wh)
save(img)
