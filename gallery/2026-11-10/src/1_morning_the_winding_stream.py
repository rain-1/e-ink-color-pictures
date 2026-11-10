"""Morning: The Winding Stream. A November valley from a hill: a river drawn as Hogarth's
serpentine line, a patchwork of hedged fields, a village waking, mist and a low sun."""
import math, random
import numpy as np
from scipy import ndimage
from kit import *
rnd = random.Random(1110); nr = np.random.default_rng(1110)
s = S; HW, HH = W * s, H * s
HOR = 118                                   # horizon y

def river_x(y):                             # centreline, y in canvas units
    t = (y - HOR) / (H - HOR)
    return 200 + (30 + 95 * t) * math.sin(2 * math.pi * (0.05 + 1.62 * t ** 0.85)) - 6 * t
def river_w(y):
    t = (y - HOR) / (H - HOR)
    return 2 + 34 * t ** 1.4
def sc(y):                                  # object scale with depth
    return 0.32 + 0.9 * ((y - HOR) / (H - HOR)) ** 0.9

# ---------- fields: warped Voronoi patchwork, textured per cell with numpy
yy, xx = np.mgrid[0:HH, 0:HW].astype(np.float32)
cy, cx = yy / s, xx / s
depth = np.clip((cy - HOR) / (H - HOR), 0.001, 1)
n = 150
py = HOR + (H - HOR) * nr.random(n) ** 1.9; px = nr.random(n) * 440 - 20
best = np.full((HH, HW), 1e9, np.float32); lab = np.zeros((HH, HW), np.int32)
for i in range(n):
    k = 0.3 + 0.9 * ((py[i] - HOR) / (H - HOR))
    dist = np.abs(cx - px[i]) / k + np.abs(cy - py[i]) / (k * 0.55)        # squarish cells, foreshortened
    m = dist < best; best[m] = dist[m]; lab[m] = i
img = np.zeros((HH, HW, 3), np.uint8)
kinds = nr.choice(6, n, p=[.22, .2, .18, .14, .14, .12]); angs = nr.random(n) * math.pi
for i in range(n):
    m = lab == i
    if not m.any(): continue
    k = 0.35 + 0.9 * ((py[i] - HOR) / (H - HOR)); a = angs[i]
    u = (cx * math.cos(a) + cy * math.sin(a) * 2.0) / k; v = (-cx * math.sin(a) + cy * math.cos(a) * 2.0) / k
    kind = kinds[i]
    if kind == 0:      # pasture: green with dark tufts
        c = np.where(((u % 7) < 1.2) & ((v % 5) < 2.0), 0, 1); pal = [K, G]
    elif kind == 1:    # stubble: yellow with fine black rows
        c = np.where((u % 4.5) < 0.9, 0, 1); pal = [K, Y]
    elif kind == 2:    # plough: black with yellow furrows
        c = np.where((u % 5) < 1.6, 1, 0); pal = [K, Y]
    elif kind == 3:    # winter wheat: yellow dotted green
        c = np.where(((u % 5) < 2.2) & ((v % 5) < 2.2), 1, 0); pal = [Y, G]
    elif kind == 4:    # frost meadow: green with white ticks
        c = np.where(((u % 9) < 1.2) & ((v % 6) < 3), 0, 1); pal = [Wh, G]
    else:              # root crop: green rows, red-leaved
        c = np.where((u % 6) < 2.4, np.where((v % 6) < 2, 2, 0), 1); pal = [G, Y, R]
    arr = np.array(pal, np.uint8)[c]
    img[m] = arr[m]
# hedges on cell borders
edge = (lab != np.roll(lab, 1, 0)) | (lab != np.roll(lab, 1, 1))
rad = (1 + depth * 5).astype(np.float32)
thick = ndimage.maximum_filter(edge.astype(np.uint8), size=int(4 * s))
thin = ndimage.maximum_filter(edge.astype(np.uint8), size=int(1.5 * s))
hedge = np.where(depth > 0.35, thick, thin).astype(bool)
img[hedge] = K
# sky
img[cy < HOR] = Y
im = Image.fromarray(img); d = ImageDraw.Draw(im)

# ---------- sky: sun, rays, cloud bars, far hills
SX, SY = 290, 70
land = im.crop((0, HOR * s, HW, HH))
for i in range(48):
    a = math.pi * 2 * i / 48
    r0, r1 = 30 + (i % 2) * 6, 300
    poly(d, [(SX + r0 * math.cos(a - .012), SY + r0 * math.sin(a - .012)), (SX + r1 * math.cos(a - .022), SY + r1 * math.sin(a - .022)), (SX + r1 * math.cos(a + .022), SY + r1 * math.sin(a + .022))], Wh)
circ(d, SX, SY, 24, R, K, 1.2); circ(d, SX, SY, 19, None, Y, 0.6)
for (bx, by, bw) in ((60, 30, 90), (150, 52, 70), (20, 66, 60), (340, 24, 70), (100, 84, 110)):
    for k in range(4):
        w_ = bw * (1 - abs(k - 1.5) / 3)
        line(d, [(bx - w_ / 2 + k * 3, by + k * 3.2), (bx + w_ / 2 + k * 3, by + k * 3.2)], B if k % 2 else Wh, 1.6)
# birds going over
for i in range(9):
    bx, by = 60 + i * 13 + (i % 3) * 3, 18 + abs(i - 4) * 5
    line(d, [(bx - 3.5, by - 2), (bx, by), (bx + 3.5, by - 2.4)], K, 0.9)
im.paste(land, (0, HOR * s))
def hill(base, amp, f, ph, col, hcol=None, gap=3, ang=60):
    pts = [(x, base - amp * (0.5 + 0.5 * math.sin(x * f + ph)) - 0.4 * amp * math.sin(x * f * 2.7 + ph * 2)) for x in range(-5, 406, 5)]
    full = pts + [(405, HOR + 6), (-5, HOR + 6)]
    poly(d, full, col)
    if hcol: hatch(im, full, hcol, gap, ang, 0.6)
    line(d, pts, K, 0.9)
hill(HOR - 6, 34, 0.013, 1.0, B, Wh, 3, 62)
hill(HOR + 1, 22, 0.021, 4.0, B, K, 3.5, 118)
hill(HOR + 5, 10, 0.034, 2.2, G, K, 2.5, 80)
# mist bars over the far valley
for y_ in range(HOR + 8, HOR + 60, 6):
    x_ = -20 + (y_ * 37 % 60)
    while x_ < 420:
        L = 20 + (x_ * 13 + y_ * 7) % 46
        line(d, [(x_, y_), (x_ + L, y_)], Wh, 1.5); x_ += L + 14 + (x_ * 5 + y_) % 30

# ---------- the river
ys = [HOR + 4 + i * 2 for i in range((H - HOR) // 2 + 4)]
left = [(river_x(y) - river_w(y), y) for y in ys]; right = [(river_x(y) + river_w(y), y) for y in ys]
bank = [(river_x(y) - river_w(y) - 1.6 - 2.6 * sc(y), y) for y in ys] + [(river_x(y) + river_w(y) + 1.6 + 2.6 * sc(y), y) for y in ys][::-1]
poly(d, bank, K)
bank2 = [(river_x(y) - river_w(y) - 0.6 - 1.3 * sc(y), y) for y in ys] + [(river_x(y) + river_w(y) + 0.6 + 1.3 * sc(y), y) for y in ys][::-1]
poly(d, bank2, Wh)
poly(d, left + right[::-1], B)
for k in (-0.62, -0.25, 0.12, 0.5):                         # current lines
    seg = []
    for y in ys:
        if river_w(y) < 4: continue
        if (int(y * 0.9 + k * 40) % 23) < 15: seg.append((river_x(y) + k * river_w(y) * 1.2, y))
        else:
            if len(seg) > 2: line(d, seg, Wh, 0.5 + 0.7 * sc(y))
            seg = []
    if len(seg) > 2: line(d, seg, Wh, 1.2)
# reeds on the banks
for y in ys[30::2]:
    for sd in (-1, 1):
        if rnd.random() < 0.55:
            bx = river_x(y) + sd * (river_w(y) + 1); k = sc(y)
            for j in range(3):
                line(d, [(bx + sd * j * 1.5 * k, y), (bx + sd * (j * 1.5 + 1.5) * k, y - (5 + 3 * j) * k)], Y if j != 1 else G, 0.7 * k + 0.3)

# ---------- things that stand on the land, back to front
items = []
def on_land(x, y, margin=6):
    return abs(x - river_x(y)) > river_w(y) + margin * sc(y) and 0 < x < 400

def tree(x, y, k, kind):
    line(d, [(x, y), (x, y - 9 * k)], K, 1.4 * k + 0.3)
    ell(d, x + 5 * k, y + 0.5 * k, 7 * k, 2 * k, K)                             # shadow
    if kind == "bare":
        for a in (-50, -25, 0, 25, 50):
            ex, ey = x + 9 * k * math.sin(math.radians(a)), y - 9 * k - 10 * k * math.cos(math.radians(a))
            line(d, [(x, y - 8 * k), (ex, ey)], K, 0.8 * k + 0.2)
            for b_ in (-28, 28):
                line(d, [(ex, ey), (ex + 5 * k * math.sin(math.radians(a + b_)), ey - 5 * k * math.cos(math.radians(a + b_)))], K, 0.5 * k + 0.2)
    elif kind == "poplar":
        ell(d, x, y - 17 * k, 4 * k, 13 * k, Y, K, 0.8)
        for j in range(4): line(d, [(x - 1.5 * k, y - (8 + j * 5) * k), (x + 1.5 * k, y - (10 + j * 5) * k)], K, 0.4 + 0.3 * k)
    else:
        col = {"red": R, "gold": Y, "green": G}[kind]
        for (ox, oy, r) in ((0, -15, 8), (-6, -12, 5.5), (6, -12, 5.5), (0, -21, 5.5)):
            circ(d, x + ox * k, y + oy * k, r * k, col, K, 0.7)
        for (ox, oy, r) in ((0, -15, 7.3), (-6, -12, 4.8), (6, -12, 4.8), (0, -21, 4.8)):
            circ(d, x + ox * k, y + oy * k, r * k, col)
        for j in range(int(5 + 6 * k)):                                         # leaf marks
            lx, ly = x + rnd.uniform(-8, 8) * k, y + rnd.uniform(-23, -9) * k
            line(d, [(lx, ly), (lx + 1.6 * k, ly + 1.2 * k)], K if j % 3 else (Y if col != Y else R), 0.5 + 0.3 * k)

def house(x, y, k, roofc=R, wall=Wh, w_=14, lit=True):
    w_ *= k; h_ = 9 * k
    poly(d, [(x + w_ / 2, y), (x + w_ / 2 + 5 * k, y - 3 * k), (x + w_ / 2 + 5 * k, y - h_ - 3 * k), (x + w_ / 2, y - h_)], K)   # shaded gable side
    rect(d, x - w_ / 2, y - h_, x + w_ / 2, y, wall, K, 0.7)
    poly(d, [(x - w_ / 2 - 1.5 * k, y - h_), (x - w_ / 2 + 3 * k, y - h_ - 7 * k), (x + w_ / 2 + 6 * k, y - h_ - 9 * k), (x + w_ / 2 + 5 * k, y - h_ - 3 * k), (x + w_ / 2 + 1 * k, y - h_)], roofc, K, 0.7)
    for j in range(1, 4): line(d, [(x - w_ / 2 + j * w_ / 4, y - h_ - 0.5 * k), (x - w_ / 2 + j * w_ / 4 + 4 * k, y - h_ - 7.2 * k)], K, 0.3 + 0.2 * k)
    rect(d, x - 1.5 * k, y - 5 * k, x + 1.5 * k, y, B if not lit else K)
    for wx in (-4.5, 4.5): rect(d, x + (wx - 1.3) * k, y - 6.5 * k, x + (wx + 1.3) * k, y - 3.5 * k, Y if lit else K)
    cxm = x + 1 * k
    rect(d, cxm, y - h_ - 11 * k, cxm + 2.6 * k, y - h_ - 6 * k, R if roofc != R else K, K, 0.5)
    if lit:
        pts = [(cxm + 1.3 * k + 3 * k * math.sin(t * 5) * t + 6 * k * t, y - h_ - 11 * k - 22 * k * t) for t in [i / 14 for i in range(15)]]
        line(d, pts, Wh, 1.0 * k + 0.3)

def church(x, y, k):
    rect(d, x - 16 * k, y - 12 * k, x + 8 * k, y, Wh, K, 0.8)
    poly(d, [(x - 17 * k, y - 12 * k), (x - 14 * k, y - 20 * k), (x + 6 * k, y - 20 * k), (x + 9 * k, y - 12 * k)], B, K, 0.8)
    for wx in (-12, -7, -2): 
        poly(d, [(x + (wx - 1.2) * k, y - 2 * k), (x + (wx - 1.2) * k, y - 7 * k), (x + wx * k, y - 9 * k), (x + (wx + 1.2) * k, y - 7 * k), (x + (wx + 1.2) * k, y - 2 * k)], Y, K, 0.4)
    rect(d, x + 6 * k, y - 26 * k, x + 15 * k, y, Wh, K, 0.8)
    poly(d, [(x + 5 * k, y - 26 * k), (x + 10.5 * k, y - 50 * k), (x + 16 * k, y - 26 * k)], B, K, 0.8)
    line(d, [(x + 10.5 * k, y - 50 * k), (x + 10.5 * k, y - 56 * k)], K, 0.8); line(d, [(x + 8.5 * k, y - 53.5 * k), (x + 12.5 * k, y - 53.5 * k)], K, 0.8)
    circ(d, x + 10.5 * k, y - 19 * k, 2.6 * k, Y, K, 0.5); line(d, [(x + 10.5 * k, y - 19 * k), (x + 10.5 * k, y - 21 * k)], K, 0.4); line(d, [(x + 10.5 * k, y - 19 * k), (x + 11.8 * k, y - 18.4 * k)], K, 0.4)
    rect(d, x + 9 * k, y - 6 * k, x + 12 * k, y, R, K, 0.4)
    for gx in range(-14, 5, 5):                                     # gravestones
        rect(d, x + gx * k, y + 3 * k, x + (gx + 1.8) * k, y + 6 * k, Wh, K, 0.4)

def sheep(x, y, k):
    ell(d, x, y - 2.6 * k, 3.6 * k, 2.4 * k, Wh, K, 0.5); circ(d, x + 3.6 * k, y - 3.4 * k, 1.5 * k, K)
    line(d, [(x - 2 * k, y - 1 * k), (x - 2 * k, y + 1 * k)], K, 0.6 * k); line(d, [(x + 2 * k, y - 1 * k), (x + 2 * k, y + 1 * k)], K, 0.6 * k)
def cow(x, y, k, col=R):
    rect(d, x - 5 * k, y - 7 * k, x + 5 * k, y - 2.5 * k, col, K, 0.5); rect(d, x + 4 * k, y - 9 * k, x + 8 * k, y - 5.5 * k, col, K, 0.5)
    rect(d, x - 2 * k, y - 7 * k, x + 1.5 * k, y - 4.4 * k, Wh)
    for lx in (-4, -2, 2.5, 4.3): line(d, [(x + lx * k, y - 2.5 * k), (x + lx * k, y + 1 * k)], K, 0.8 * k)
def stack(x, y, k):
    poly(d, [(x - 5 * k, y), (x - 5.5 * k, y - 6 * k), (x, y - 12 * k), (x + 5.5 * k, y - 6 * k), (x + 5 * k, y)], Y, K, 0.7)
    for j in (-3, -1, 1, 3): line(d, [(x + j * k, y - 1 * k), (x + j * 0.7 * k, y - 7 * k)], K, 0.4)
    ell(d, x + 5 * k, y + 0.3 * k, 5 * k, 1.5 * k, K)

# village on the near-left bank, around the bridge
BRY = 372
vx = river_x(BRY)
village = [(-70, -26, R), (-48, -34, B), (-96, -12, R), (-58, -4, K), (-32, -14, R), (-108, 14, B), (-78, 18, R), (-46, 22, R), (-124, -34, R), (52, -22, R), (78, -6, B), (60, 14, R), (98, 20, R)]
for (ox, oy, rc) in village:
    x, y = vx + ox, BRY + oy
    if on_land(x, y, 4): items.append((y, "house", x, rc))
items.append((BRY - 40, "church", vx - 92, None))
# scattered farms
for _ in range(15):
    y = rnd.uniform(HOR + 26, 590); x = rnd.uniform(8, 392)
    if on_land(x, y, 10) and abs(y - BRY) > 60: items.append((y, "house", x, rnd.choice([R, R, B])))
# trees: along hedges and riverbanks
kinds_t = ["red", "gold", "green", "bare", "bare", "poplar", "gold", "red"]
tries = 0
while sum(1 for it in items if it[1] == "tree") < 190 and tries < 6000:
    tries += 1
    y = HOR + 12 + (H - HOR - 6) * rnd.random() ** 1.3; x = rnd.uniform(-4, 404)
    if not on_land(x, y, 5): continue
    iy, ix = min(HH - 1, int(y * s)), min(HW - 1, max(0, int(x * s)))
    near_river = abs(x - river_x(y)) < river_w(y) + 16 * sc(y)
    if hedge[iy, ix] or (near_river and rnd.random() < 0.5) or rnd.random() < 0.02:
        items.append((y, "tree", x, rnd.choice(kinds_t) if not near_river else rnd.choice(["poplar", "bare", "gold"])))
# animals in pasture / frost meadow, stacks in stubble
for _ in range(900):
    y = HOR + 30 + (H - HOR - 34) * rnd.random(); x = rnd.uniform(4, 396)
    if not on_land(x, y, 5): continue
    kd = kinds[lab[min(HH - 1, int(y * s)), int(x * s)]]
    if hedge[min(HH - 1, int(y * s)), int(x * s)]: continue
    if kd == 0 and rnd.random() < 0.35: items.append((y, "sheep", x, None))
    elif kd == 4 and rnd.random() < 0.25: items.append((y, "cow", x, rnd.choice([R, K, R])))
    elif kd == 1 and rnd.random() < 0.2: items.append((y, "stack", x, None))

# road: from the bottom-left up through the village, over the bridge, off right
road = bez((40, 606), (10, 500), (60, 400), (vx - 40, BRY + 2), 30) + bez((vx - 40, BRY + 2), (vx, BRY - 6), (vx + 30, BRY - 2), (vx + 60, BRY + 2), 12)[1:] + bez((vx + 60, BRY + 2), (360, 380), (330, 300), (404, 262), 30)[1:]
for wd, col in ((3.4, K), (2.0, Wh)):
    for i in range(len(road) - 1):
        k = sc(road[i][1]); line(d, road[i:i + 2], col, wd * k + 0.6)
# bridge: three arches
bw = river_w(BRY) + 8; bk = sc(BRY)
poly(d, [(vx - bw, BRY + 2), (vx - bw, BRY - 7 * bk), (vx, BRY - 11 * bk), (vx + bw, BRY - 7 * bk), (vx + bw, BRY + 2)], Wh, K, 1.0)
for j in (-1, 0, 1):
    ax = vx + j * bw * 0.6
    poly(d, [(ax - bw * .22, BRY + 2)] + [(ax + bw * .22 * math.cos(math.radians(a)), BRY + 2 - 7.5 * bk * math.sin(math.radians(a))) for a in range(180, -1, -15)] + [(ax + bw * .22, BRY + 2)], B, K, 0.7)
for j in range(-6, 7): line(d, [(vx + j * bw / 6.5, BRY - 7.5 * bk - (1 - abs(j) / 6.5) * 3.5 * bk), (vx + j * bw / 6.5, BRY - 5 * bk - (1 - abs(j) / 6.5) * 3 * bk)], K, 0.5)
# cart on the bridge
circ(d, vx - 4, BRY - 12 * bk, 2.2, K); rect(d, vx - 8, BRY - 16.5 * bk, vx + 1, BRY - 12.5 * bk, R, K, 0.5); ell(d, vx + 6, BRY - 14 * bk, 3.4, 2, K); line(d, [(vx + 1, BRY - 14 * bk), (vx + 4, BRY - 14 * bk)], K, 0.6)

for (y, kind, x, extra) in sorted(items, key=lambda t: t[0]):
    k = sc(y)
    if kind == "tree": tree(x, y, k * 1.15, extra)
    elif kind == "house": house(x, y, k * 1.25, extra, lit=rnd.random() < 0.7)
    elif kind == "church": church(x, y, k * 1.25)
    elif kind == "sheep": sheep(x, y, k * 1.2)
    elif kind == "cow": cow(x, y, k * 1.0, extra)
    elif kind == "stack": stack(x, y, k * 1.1)

# boats and a mill, on the water
for (y, sd) in ((330, -0.3), (470, 0.35), (545, -0.2)):
    x = river_x(y) + sd * river_w(y); k = sc(y)
    poly(d, [(x - 8 * k, y - 2 * k), (x - 5 * k, y + 2 * k), (x + 5 * k, y + 2 * k), (x + 8 * k, y - 2 * k)], R if y != 470 else Y, K, 0.7)
    circ(d, x - 1 * k, y - 5.5 * k, 1.8 * k, K); line(d, [(x - 1 * k, y - 4 * k), (x - 1 * k, y - 1 * k)], K, 1.6 * k)
    line(d, [(x - 1 * k, y - 3 * k), (x + 9 * k, y + 4 * k)], K, 0.7)
    for j in (1, 2): line(d, [(x - (8 + 4 * j) * k, y + (2 + j * 2) * k), (x + (4 - 2 * j) * k, y + (2 + j * 2) * k)], Wh, 0.7)
# anglers' rings and two swans
for (y, sd) in ((420, 0.5), (505, -0.5), (585, 0.3)):
    x = river_x(y) + sd * river_w(y)
    for r in (3, 6): ell(d, x, y, r * sc(y), r * 0.4 * sc(y), None, Wh, 0.6)
for (y, sd) in ((440, -0.45), (448, -0.2)):
    x = river_x(y) + sd * river_w(y); k = sc(y)
    ell(d, x, y, 4 * k, 2 * k, Wh, K, 0.5); line(d, scurve(x + 3.5 * k, y - 7 * k, 6 * k, 1.5 * k, 8, 1, 3.14), Wh, 1.3 * k); circ(d, x + 3.5 * k, y - 7.5 * k, 1.1 * k, R)
save(im)
