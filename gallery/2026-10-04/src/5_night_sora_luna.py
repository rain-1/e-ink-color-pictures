# 5 · Night (22:00) — "Sora Luna e le Stelle"
# Laudato si', mi' Signore, per sora Luna e le stelle: in celu l'ài formate clarite
# et pretiose et belle.  The Porziuncola at night, lamp-lit, under a gibbous moon and a
# vortex of larks wheeling over the roof (Celano / Bonaventure, 3 Oct 1226).
import os, sys, math
sys.path.insert(0, os.path.dirname(__file__))
from common import *

rng = np.random.default_rng(1226)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)          # 1x grids
THR = threshold_1x()
THR_I = 1.0 - THR                                        # complementary screen


def scr(tone, inv=False):
    t = THR_I if inv else THR
    return up(tone > t)


def layer(a, region, tone, colour, inv=False):
    """paint colour into numpy image a where region & screen(tone)."""
    m = scr(tone, inv)
    if region is not None:
        m = m & region
    a[m] = colour


def P(pts):
    return [(x * S, y * S) for x, y in pts]


def poly_mask(pts):
    return mask_of(lambda d: d.polygon(P(pts), fill=255))


img, d = new(K)
a = np.asarray(img).copy()

# ---------------------------------------------------------------- sky
MX, MY, MR = 288, 112, 58                       # moon (1x)
HOR = 430
dm = np.hypot(xx - MX, yy - MY)
sky_t = 0.0 + 0.42 * np.clip(yy / HOR, 0, 1) ** 2.6
sky_t += 0.36 * np.exp(-np.clip(dm - MR, 0, None) / 26.0)
# Milky Way: band from upper-left down to the right
bx0, by0, bx1, by1 = 190, -10, -30, 430
nx, ny = by1 - by0, -(bx1 - bx0)
nl = math.hypot(nx, ny)
band_d = ((xx - bx0) * nx + (yy - by0) * ny) / nl
nz = noise(H, W, 40, seed=7)
rift = noise(H, W, 22, seed=11)
band = np.exp(-(band_d / 38.0) ** 2) * (0.55 + 0.6 * nz)
band *= np.clip(1.25 - 1.6 * np.clip(rift - 0.45, 0, 1) * np.exp(-(band_d / 14) ** 2) * 2, 0, 1)
sky_t += 0.16 * band
a[:] = K
layer(a, None, np.clip(sky_t, 0, 1), B)

# star field (2x2 minimum at 1x, aligned)
def dot(x, y, s, c):
    x, y = int(x) * S, int(y) * S
    a[y:y + s * S, x:x + s * S] = c

def plus(x, y, c, arm=1):
    x, y = int(x), int(y)
    dot(x, y, 2, c)
    a[(y) * S:(y + 2) * S, (x - arm) * S:(x + 2 + arm) * S] = c
    a[(y - arm) * S:(y + 2 + arm) * S, (x) * S:(x + 2) * S] = c

def ok_star(x, y):
    return y < HOR - 30 + 0.12 * (x - 200) * 0 and math.hypot(x - MX, y - MY) > MR + 14

# milky way dust: many 2x2 dots weighted by band density
n_mw = 0
while n_mw < 520:
    x, y = rng.uniform(0, W - 2), rng.uniform(0, HOR - 40)
    bd = ((x - bx0) * nx + (y - by0) * ny) / nl
    p = math.exp(-(bd / 34.0) ** 2) * (0.4 + 0.8 * nz[int(y), int(x)])
    if rng.random() < p * 0.9 and ok_star(x, y):
        dot(x, y, 1 if False else 2, WH if rng.random() < 0.35 else B)
        if rng.random() < 0.55:
            dot(x, y, 2, WH)
        n_mw += 1

# field stars
for i in range(260):
    x, y = rng.uniform(2, W - 4), (rng.random() ** 1.25) * (HOR - 45)
    if not ok_star(x, y):
        continue
    r = rng.random()
    if r < 0.62:
        dot(x, y, 2, WH)
    elif r < 0.80:
        dot(x, y, 2, Y if rng.random() < 0.3 else WH)
        dot(x + 2, y, 2, B)
    elif r < 0.95:
        plus(x, y, WH)
    else:
        plus(x, y, Y)
        dot(x, y, 2, WH)

# a few named-feeling bright twinkles (4-point)
def twinkle(x, y, L, c=WH):
    x2, y2 = x * S, y * S
    for k, (dx, dy) in enumerate([(1, 0), (-1, 0), (0, 1), (0, -1)]):
        ll = L if dy == 0 else int(L * 1.25)
        for j in range(ll * S):
            w = 3 if j < ll * S * 0.45 else 2
            px, py = x2 + 1 + dx * j, y2 + 1 + dy * j
            a[py - w // 2:py + (w + 1) // 2 + 1, px - w // 2:px + (w + 1) // 2 + 1] = c
    for dx, dy in [(1, 1), (-1, 1), (1, -1), (-1, -1)]:
        for j in range(int(L * 0.35) * S):
            px, py = x2 + 1 + dx * j, y2 + 1 + dy * j
            a[py:py + 2, px:px + 2] = c
    a[y2 - 3:y2 + 5, x2 - 3:x2 + 5] = WH

for (x, y, L) in [(52, 46, 11), (150, 22, 8), (370, 250, 9), (24, 210, 8),
                  (178, 150, 7), (392, 28, 6), (120, 290, 6), (330, 330, 6)]:
    if ok_star(x, y):
        twinkle(x, y, L)
plus(52, 46, Y, arm=0)

# ---------------------------------------------------------------- moon
mx2, my2, mr2 = MX * S, MY * S, MR * S
Y2, X2 = np.mgrid[0:H2, 0:W2].astype(np.float32)
u = (X2 - mx2) / mr2
v = (Y2 - my2) / mr2
disk = u * u + v * v <= 1.0
k_term = 0.55                                   # waxing gibbous: lit right of terminator
lit = disk & (u > -k_term * np.sqrt(np.clip(1 - v * v, 0, 1)))
# halo rings
ring = (np.abs(np.hypot(X2 - mx2, Y2 - my2) - (mr2 + 14)) < 1.2)
a[ring & ~disk & scr(np.full((H, W), 0.5))] = B
# dark limb: earthshine
a[disk] = K
layer(a, disk & ~lit, np.full((H, W), 0.30), B)
# lit face: white with yellow highland mottling
a[lit] = WH
u1 = (xx - MX) / MR; v1 = (yy - MY) / MR
mn = noise(H, W, 6, seed=21)
hl = 0.03 + 0.17 * mn
layer(a, lit, hl, Y)

def blob(cx, cy, rx, ry, rot=0.0, wob=0.25, seed=0):
    rr = np.hypot((u1 - cx) / rx, (v1 - cy) / ry)
    ang = np.arctan2(v1 - cy, u1 - cx)
    nb = noise(H, W, 5, seed=seed)
    return rr * (1 + wob * (nb - 0.5)) * (1 + 0.12 * np.sin(3 * ang + seed))

maria = np.full((H, W), 9.0, np.float32)
for (cx, cy, rx, ry, sd) in [(-0.36, -0.30, 0.30, 0.26, 1),     # Imbrium
                             (0.12, -0.33, 0.18, 0.16, 2),      # Serenitatis
                             (0.30, -0.04, 0.22, 0.17, 3),      # Tranquillitatis
                             (0.66, -0.24, 0.11, 0.13, 4),      # Crisium
                             (0.58, 0.15, 0.12, 0.17, 5),       # Fecunditatis
                             (0.37, 0.30, 0.09, 0.09, 6),       # Nectaris
                             (-0.62, 0.02, 0.24, 0.45, 7),      # Procellarum
                             (-0.20, 0.36, 0.16, 0.11, 8),      # Nubium
                             (-0.52, 0.40, 0.09, 0.09, 9),      # Humorum
                             (-0.05, -0.68, 0.40, 0.07, 10),    # Frigoris
                             (0.0, -0.12, 0.09, 0.08, 12)]:     # Vaporum/Medii
    maria = np.minimum(maria, blob(cx, cy, rx, ry, seed=sd))
mar_t = np.clip((1.15 - maria) * 1.6, 0, 1) * (0.42 + 0.22 * noise(H, W, 4, seed=31))
mar_region = up(mar_t > 0.02) & lit
a[mar_region] = WH
layer(a, mar_region, mar_t, B)
# terminator shading: blue screen deepening towards the shadow line
term_x = -k_term * np.sqrt(np.clip(1 - v1 * v1, 0, 1))
tdist = np.clip((u1 - term_x) / 0.35, 0, 1)
layer(a, lit, (1 - tdist) * 0.75, B, inv=True)
# limb darkening ring
layer(a, lit, np.clip((np.hypot(u1, v1) - 0.86) * 3.5, 0, 0.6), B, inv=True)

# craters: small rims (shadow on the sun-ward/left? sun is to the right, so shadow
# falls inside on the right-hand rim) + rays from Tycho and Copernicus
def crater(cx, cy, r, d_):
    x, y = mx2 + cx * mr2, my2 + cy * mr2
    rp = r * mr2
    d_.ellipse([x - rp, y - rp, x + rp, y + rp], outline=B, width=2)
    d_.arc([x - rp, y - rp, x + rp, y + rp], -110, 70, fill=WH, width=2)

base_moon = a.copy()
img = Image.fromarray(a); d = ImageDraw.Draw(img)
for (cx, cy, Lr, n) in [(-0.16, 0.72, 1.1, 14), (-0.33, -0.03, 0.55, 10), (-0.62, -0.10, 0.3, 7)]:
    x0, y0 = mx2 + cx * mr2, my2 + cy * mr2
    for j in range(n):
        th = j / n * 2 * math.pi + rng.uniform(-0.2, 0.2)
        ll = Lr * mr2 * rng.uniform(0.45, 1.0)
        x1, y1 = x0 + ll * math.cos(th), y0 + ll * math.sin(th)
        d.line([(x0, y0), (x1, y1)], fill=WH, width=2)
for (cx, cy, r) in [(-0.16, 0.72, 0.06), (-0.33, -0.03, 0.06), (0.10, 0.55, 0.05),
                    (0.45, 0.58, 0.04), (0.22, 0.75, 0.05), (0.62, 0.45, 0.04),
                    (-0.62, -0.10, 0.035), (0.05, 0.25, 0.04), (0.70, -0.50, 0.04),
                    (-0.05, 0.85, 0.035), (0.35, -0.70, 0.04), (0.82, 0.10, 0.035)]:
    crater(cx, cy, r, d)
drawn = np.asarray(img).copy()
a = base_moon
keep = lit & (u * u + v * v < 0.93)
a[keep] = drawn[keep]

# ---------------------------------------------------------------- distant hill & Assisi
ridge = lambda x: 372 + 0.055 * x + 10 * math.sin(x / 37.0) + 4 * math.sin(x / 11.0)
hill_pts = [(x, ridge(x)) for x in range(0, W + 1, 4)] + [(W, H), (0, H)]
hill = poly_mask(hill_pts)
a[hill] = K
layer(a, hill, 0.10 + 0.12 * noise(H, W, 18, seed=41), B)
img = Image.fromarray(a); d = ImageDraw.Draw(img)
# town blocks on the left ridge
tx = 6
trng = np.random.default_rng(5)
while tx < 118:
    bw = int(trng.integers(6, 14)); bh = int(trng.integers(6, 16))
    base = ridge(tx + bw / 2) + 6
    d.rectangle([tx * S, (base - bh) * S, (tx + bw) * S, base * S], fill=K)
    d.line([(tx + bw) * S - 1, (base - bh) * S, (tx + bw) * S - 1, base * S], fill=B, width=2)
    for wy in range(int(base - bh + 2), int(base - 2), 4):
        for wx in range(tx + 2, tx + bw - 2, 4):
            if trng.random() < 0.28:
                d.rectangle([wx * S, wy * S, wx * S + 3, wy * S + 3], fill=Y)
    tx += bw + int(trng.integers(0, 3))
# Basilica of San Francesco: long nave + campanile + arched substructure
bxs, bys = 20, ridge(20) + 4
d.polygon(P([(bxs, bys), (bxs, bys - 16), (bxs + 18, bys - 24), (bxs + 36, bys - 16), (bxs + 36, bys)]), fill=K)
d.rectangle([(bxs + 38) * S, (bys - 34) * S, (bxs + 44) * S, bys * S], fill=K)
d.polygon(P([(bxs + 37, bys - 34), (bxs + 41, bys - 40), (bxs + 45, bys - 34)]), fill=K)
d.line(P([(bxs + 44, bys - 34), (bxs + 44, bys)]), fill=B, width=2)
for i in range(6):
    ax = bxs - 2 + i * 7
    d.arc([ax * S, (bys + 4) * S, (ax + 6) * S, (bys + 14) * S], 180, 360, fill=Y, width=2)
d.rectangle([(bxs + 40) * S, (bys - 31) * S, (bxs + 42) * S, (bys - 28) * S], fill=Y)
# Rocca Maggiore on the summit
rx0 = 92
rb = ridge(rx0) + 2
d.rectangle([rx0 * S, (rb - 16) * S, (rx0 + 16) * S, rb * S], fill=K)
for i in range(4):
    d.rectangle([(rx0 + i * 4) * S, (rb - 19) * S, (rx0 + i * 4 + 2) * S, (rb - 16) * S], fill=K)
d.line(P([(rx0 + 16, rb - 16), (rx0 + 16, rb)]), fill=B, width=2)
a = np.asarray(img).copy()

# ---------------------------------------------------------------- ground
GY = 520
gnd = up(yy >= GY - 12 + 0 * xx) & ~poly_mask([(0, 0), (W, 0), (W, GY - 12), (0, GY - 12)])
ground_pts = [(0, 496), (120, 506), (200, 510), (300, 504), (400, 494), (400, 600), (0, 600)]
ground = poly_mask(ground_pts)
a[ground] = K
gn = noise(H, W, 10, seed=51)
layer(a, ground, 0.10 + 0.18 * gn, B)
# lamp-light pool from the door, spreading down the path
door_cx, door_cy = 200, 500
pool = np.exp(-(((xx - door_cx) / 52.0) ** 2 + ((yy - 522) / 26.0) ** 2))
path = np.exp(-((xx - (200 + (yy - 520) * 0.15)) / (16 + (yy - 520) * 0.5 + 1e-3)) ** 2) * (yy > 515)
layer(a, ground, np.clip(0.75 * pool + 0.25 * path * np.clip(1 - (yy - 520) / 70, 0, 1), 0, 0.9), Y, inv=True)

# ---------------------------------------------------------------- trees
def cypress(cx, base, top, wid, seed, lit_side=1):
    """flame-shaped cypress; black body, blue foliage texture, moonlit right edge."""
    r_ = np.random.default_rng(seed)
    hgt = base - top
    left, right = [], []
    for i in range(0, 41):
        t = i / 40
        y = top + t * hgt
        w = wid * (math.sin(min(1, t * 1.15) * math.pi * 0.5) ** 0.75) * (1 - 0.25 * t ** 3)
        jl, jr = r_.uniform(-1.5, 1.5), r_.uniform(-1.5, 1.5)
        left.append((cx - w + jl, y)); right.append((cx + w + jr, y))
    pts = [(cx, top - 4)] + right + left[::-1]
    m = poly_mask(pts)
    a[m] = K
    tex = noise(H, W, 4, seed=seed)
    edge = np.clip((xx - cx) / wid, -1, 1)
    layer(a, m, np.clip(0.12 * tex * (0.3 + 0.7 * edge * lit_side), 0, 1), B)
    im = Image.fromarray(a); dd = ImageDraw.Draw(im)
    # moonlit flicks along the lit edge
    for (x, y) in right[2:-3]:
        if r_.random() < 0.7:
            dd.line([(x - 3) * S, y * S, (x - 0.5) * S, (y - 2.5) * S], fill=WH, width=2)
        if r_.random() < 0.4:
            dd.line([(x - 7) * S, (y + 1) * S, (x - 4) * S, (y - 1.5) * S], fill=B, width=2)
    # foliage scallops inside
    for j in range(int(hgt / 3)):
        y = top + 6 + r_.random() * (hgt - 10)
        t = (y - top) / hgt
        w = wid * (math.sin(min(1, t * 1.15) * math.pi * 0.5) ** 0.75)
        x = cx + r_.uniform(-0.6, 0.9) * w
        dd.arc([(x - 3) * S, (y - 2) * S, (x + 3) * S, (y + 2) * S], 200, 340, fill=B, width=2)
    return np.asarray(im).copy()


def olive(cx, cy, rw, rh, trunk_base, seed):
    global a
    r_ = np.random.default_rng(seed)
    im = Image.fromarray(a); dd = ImageDraw.Draw(im)
    # gnarled trunk: twin twisting stems
    for off in (-4, 3):
        pts = []
        for i in range(12):
            t = i / 11
            y = trunk_base - t * (trunk_base - cy)
            x = cx + off * (1 - t) + 3 * math.sin(t * 5 + off)
            pts.append((x * S, y * S))
        dd.line(pts, fill=K, width=int(10 - 4) * S // 2 + 4)
        dd.line([(p[0] + 4, p[1]) for p in pts], fill=B, width=2)
    a = np.asarray(im).copy()
    # crown made of clustered leaf clumps
    cm = np.zeros((H2, W2), bool)
    clumps = []
    for i in range(26):
        ang = r_.uniform(0, 2 * math.pi); rr = math.sqrt(r_.random())
        x = cx + rw * rr * math.cos(ang); y = cy + rh * rr * math.sin(ang) * 0.9
        s = r_.uniform(8, 14)
        clumps.append((x, y, s))
    clumps.sort(key=lambda c: c[1])
    m = mask_of(lambda q: [q.ellipse([(x - s) * S, (y - s * 0.7) * S, (x + s) * S, (y + s * 0.7) * S], fill=255) for x, y, s in clumps])
    a[m] = K
    tex = noise(H, W, 3, seed=seed + 1)
    layer(a, m, 0.04 + 0.22 * tex * np.clip(0.5 + (xx - cx) / (2 * rw) - (yy - cy) / (2 * rh), 0, 1), B)
    im = Image.fromarray(a); dd = ImageDraw.Draw(im)
    for (x, y, s) in clumps:
        # silver leaf dabs on the moon side of each clump
        for k in range(8):
            ang = r_.uniform(-1.8, 0.4)
            lx = x + s * 0.8 * math.cos(ang) * r_.uniform(0.5, 1.0)
            ly = y + s * 0.55 * math.sin(ang) * r_.uniform(0.5, 1.0)
            col = WH if r_.random() < 0.6 else B
            dd.line([lx * S, ly * S, (lx + 2.5) * S, (ly - 1.2) * S], fill=col, width=2)
        dd.arc([(x - s) * S, (y - s * 0.7) * S, (x + s) * S, (y + s * 0.7) * S], 260, 350, fill=B, width=2)
    a = np.asarray(im).copy()


olive(52, 452, 44, 26, 505, seed=61)
a = cypress(110, 506, 318, 9, seed=71)
a = cypress(366, 506, 236, 15, seed=72)
a = cypress(342, 506, 300, 10, seed=73)
olive(390, 470, 30, 20, 508, seed=62)

# ---------------------------------------------------------------- the Porziuncola
FL, FR, EAVE, APEX, BASE = 128, 272, 392, 312, 520
AX = (FL + FR) / 2
DX, DY = 58, -14                                     # receding direction (side)
# side wall
side = poly_mask([(FR, EAVE), (FR + DX, EAVE + DY), (FR + DX, BASE + DY + 4), (FR, BASE)])
a[side] = K
layer(a, side, 0.18 + 0.1 * noise(H, W, 8, seed=81), B)
# right roof slope
roof = [(AX, APEX), (FR + 6, EAVE + 4), (FR + 6 + DX, EAVE + 4 + DY), (AX + DX, APEX + DY)]
rm = poly_mask(roof)
a[rm] = K
img = Image.fromarray(a); d = ImageDraw.Draw(img)
# coppi: columns running down the slope, staggered caps
ncol = 16
for i in range(ncol + 1):
    t = i / ncol
    top_ = (AX + DX * t, APEX + DY * t)
    bot_ = (FR + 6 + DX * t, EAVE + 4 + DY * t)
    d.line([P([top_])[0], P([bot_])[0]], fill=B, width=3)
    # tile caps: little arcs each course
    for c in range(1, 12):
        s = c / 12 + (0.04 if i % 2 else 0)
        px = top_[0] + (bot_[0] - top_[0]) * s
        py = top_[1] + (bot_[1] - top_[1]) * s
        col = WH if (i + c) % 3 == 0 else B
        d.arc([(px - 3) * S, (py - 2) * S, (px + 2) * S, (py + 2) * S], 190, 330, fill=col, width=2)
        if (i * 7 + c * 3) % 5 == 0:
            d.rectangle([(px - 1) * S, py * S, (px + 1) * S, (py + 1) * S + 1], fill=R)
# ridge line, moonlit
d.line(P([(AX, APEX - 1), (AX + DX, APEX + DY - 1)]), fill=WH, width=4)
d.line(P([(AX, APEX + 2), (AX + DX, APEX + DY + 2)]), fill=K, width=3)
# eave shadow under roof on side wall
d.line(P([(FR + 2, EAVE + 6), (FR + DX, EAVE + DY + 6)]), fill=K, width=6)
a = np.asarray(img).copy()

# side wall stones (small, foreshortened)
img = Image.fromarray(a); d = ImageDraw.Draw(img)
srng = np.random.default_rng(91)
for row in range(14):
    t0 = row / 14; t1 = (row + 1) / 14
    x = 0.0
    while x < 1.0:
        w_ = srng.uniform(0.12, 0.28)
        x1 = min(1.0, x + w_)
        def sp(px, t):
            yt = EAVE + 8 + (BASE - EAVE - 8) * t
            return (FR + DX * px, yt + DY * px * (1 - 0.0))
        q = [sp(x, t0), sp(x1, t0), sp(x1, t1), sp(x, t1)]
        d.polygon(P(q), outline=K, width=2)
        if srng.random() < 0.3:
            d.line(P([sp(x + 0.03, t0 + 0.02), sp(x1 - 0.03, t0 + 0.02)]), fill=WH, width=2)
        x = x1
a = np.asarray(img).copy()
# side window, glowing
sw = [(FR + 26, 438 - 6), (FR + 34, 438 - 8), (FR + 34, 456 - 8), (FR + 26, 456 - 6)]
img = Image.fromarray(a); d = ImageDraw.Draw(img)
d.polygon(P([(x - 1, y - 1) for x, y in sw[:2]] + [(x + 0, y + 1) for x, y in sw[2:]]), fill=K)
d.polygon(P(sw), fill=Y)
d.line(P([(FR + 30, 426), (FR + 30, 449)]), fill=R, width=2)
d.line(P([(FR + 26, 440), (FR + 34, 438)]), fill=R, width=2)
a = np.asarray(img).copy()

# facade
fac_pts = [(FL, BASE), (FL, EAVE), (AX, APEX), (FR, EAVE), (FR, BASE)]
fac = poly_mask(fac_pts)
lab = Image.new("L", (W2, H2), 0); ld = ImageDraw.Draw(lab)
glow = Image.new("L", (W2, H2), 0); gd = ImageDraw.Draw(glow)
frng = np.random.default_rng(101)
stones = []
y = BASE
while y > APEX - 2:
    hh = int(frng.integers(9, 14))
    y0 = y - hh
    x = FL - frng.integers(0, 14)
    while x < FR:
        ww = int(frng.integers(13, 30))
        x1 = x + ww
        q = [(x + frng.uniform(0.5, 2), y0 + frng.uniform(0.5, 1.8)),
             (x1 - frng.uniform(0.5, 2), y0 + frng.uniform(0.5, 1.8)),
             (x1 - frng.uniform(0.5, 1.5), y - frng.uniform(0.5, 1.5)),
             (x + frng.uniform(0.5, 1.5), y - frng.uniform(0.5, 1.5))]
        tone = frng.uniform(0.30, 0.62)
        ld.polygon(P(q), fill=int(tone * 255))
        stones.append((q, tone))
        x = x1
    y = y0
lab_a = np.asarray(lab)[::S, ::S].astype(np.float32) / 255
# warm glow on the facade around door and rose window
gx = np.exp(-(((xx - AX) / 42.0) ** 2 + ((yy - 488) / 46.0) ** 2))
gx += 0.6 * np.exp(-(((xx - AX) / 22.0) ** 2 + ((yy - 336) / 20.0) ** 2))
moonlight = 0.12 * np.clip((xx - FL) / (FR - FL), 0, 1)    # moon from upper right
a[fac] = K
stone_px = fac & up(lab_a > 0.01)
layer(a, stone_px, np.clip(lab_a + moonlight - 0.15 * gx, 0, 1), B)
layer(a, stone_px, np.clip(gx * (0.35 + lab_a * 0.5), 0, 0.85), Y, inv=True)
img = Image.fromarray(a); d = ImageDraw.Draw(img)
for q, tone in stones:
    # moonlit top edge / warm top edge near the door
    cxs = (q[0][0] + q[1][0]) / 2; cys = q[0][1]
    gl = math.exp(-(((cxs - AX) / 40) ** 2 + ((cys - 488) / 44) ** 2))
    if gl > 0.35:
        d.line(P([q[0], q[1]]), fill=Y, width=2)
    elif frng.random() < 0.45:
        d.line(P([(q[0][0] + 3, q[0][1] + 0.5), (q[1][0], q[1][1] + 0.5)]), fill=WH if frng.random() < 0.5 else B, width=2)
a2 = np.asarray(img).copy()
a2[~fac] = a[~fac]
a = a2

img = Image.fromarray(a); d = ImageDraw.Draw(img)
# gable coping, moonlit on the right slope
d.line(P([(FL - 4, EAVE + 3), (AX, APEX - 3), (FR + 5, EAVE + 3)]), fill=K, width=10)
d.line(P([(AX, APEX - 6), (FR + 6, EAVE - 1)]), fill=WH, width=2)
d.line(P([(FL - 5, EAVE - 1), (AX, APEX - 6)]), fill=B, width=2)
# plinth / step
d.rectangle([(FL - 3) * S, (BASE - 5) * S, (FR + 3) * S, (BASE + 2) * S], fill=K)
d.line(P([(FL - 3, BASE - 5), (FR + 3, BASE - 5)]), fill=B, width=2)

# bell-gable on the apex
bg_l, bg_r, bg_b, bg_t = AX - 11, AX + 11, APEX - 2, APEX - 34
d.polygon(P([(bg_l, bg_b + 6), (bg_l, bg_t + 8), (AX, bg_t), (bg_r, bg_t + 8), (bg_r, bg_b + 6)]), fill=K)
d.line(P([(AX, bg_t), (bg_r, bg_t + 8), (bg_r, bg_b + 4)]), fill=WH, width=2)
d.line(P([(bg_l, bg_b + 4), (bg_l, bg_t + 8), (AX, bg_t)]), fill=B, width=2)
# arched opening, deep blue sky seen through, with bell
d.rectangle([(AX - 6) * S, (bg_t + 12) * S, (AX + 6) * S, (bg_b - 2) * S], fill=B)
d.pieslice([(AX - 6) * S, (bg_t + 6) * S, (AX + 6) * S, (bg_t + 18) * S], 180, 360, fill=B)
d.polygon(P([(AX - 4, bg_b - 4), (AX - 3, bg_t + 16), (AX, bg_t + 13), (AX + 3, bg_t + 16), (AX + 4, bg_b - 4)]), fill=K)
d.line(P([(AX + 2, bg_t + 15), (AX + 3, bg_b - 5)]), fill=Y, width=2)
d.rectangle([(AX - 1) * S, (bg_b - 4) * S, (AX + 1) * S, (bg_b - 1) * S], fill=K)
# small iron cross on top
d.line(P([(AX, bg_t - 1), (AX, bg_t - 12)]), fill=K, width=4)
d.line(P([(AX - 4, bg_t - 8), (AX + 4, bg_t - 8)]), fill=K, width=4)
d.line(P([(AX + 1, bg_t - 1), (AX + 1, bg_t - 12)]), fill=WH, width=2)
d.line(P([(AX - 4, bg_t - 9), (AX + 4, bg_t - 9)]), fill=WH, width=2)

# small rose window in the gable, glowing
rcx, rcy, rr = AX, 343, 11
d.ellipse([(rcx - rr - 3) * S, (rcy - rr - 3) * S, (rcx + rr + 3) * S, (rcy + rr + 3) * S], fill=K)
d.ellipse([(rcx - rr - 2) * S, (rcy - rr - 2) * S, (rcx + rr + 2) * S, (rcy + rr + 2) * S], outline=WH, width=2)
d.ellipse([(rcx - rr) * S, (rcy - rr) * S, (rcx + rr) * S, (rcy + rr) * S], fill=Y)
for k in range(8):
    th = k * math.pi / 4
    d.line(P([(rcx, rcy), (rcx + rr * math.cos(th), rcy + rr * math.sin(th))]), fill=K, width=3)
    px, py = rcx + rr * 0.62 * math.cos(th + math.pi / 8), rcy + rr * 0.62 * math.sin(th + math.pi / 8)
    d.ellipse([(px - 1.6) * S, (py - 1.6) * S, (px + 1.6) * S, (py + 1.6) * S], fill=R if k % 2 else B)
d.ellipse([(rcx - 3) * S, (rcy - 3) * S, (rcx + 3) * S, (rcy + 3) * S], fill=R)
d.ellipse([(rcx - 1) * S, (rcy - 1) * S, (rcx + 1) * S, (rcy + 1) * S], fill=Y)

# gothic fresco panel above the door
pl, pr, pt, pb = AX - 38, AX + 38, 364, 452
d.polygon(P([(pl - 4, pb + 4), (pl - 4, pt + 22), (AX, pt - 8), (pr + 4, pt + 22), (pr + 4, pb + 4)]), fill=K)
fr_pts = [(pl, pb), (pl, pt + 24)] + \
         [(AX + (pl - AX) * math.cos(t) , pt + 24 - 30 * math.sin(t)) for t in np.linspace(0, math.pi / 2, 8)][::1]
# simple pointed arch outline
arch = [(pl, pb), (pl, pt + 24)]
for t in np.linspace(0, 1, 10):
    arch.append((pl + (AX - pl) * t, pt + 24 - 30 * math.sin(t * math.pi / 2) ** 0.9))
for t in np.linspace(0, 1, 10):
    arch.append((AX + (pr - AX) * t, pt - 6 + 30 * (1 - math.cos(t * math.pi / 2)) ** 1.1))
arch += [(pr, pt + 24), (pr, pb)]
d.polygon(P(arch), fill=K, outline=Y)
d.line(P(arch + [arch[0]]), fill=Y, width=2)
a = np.asarray(img).copy()
inner = poly_mask([(x + (2 if x < AX else -2 if x > AX else 0), y + 2) for x, y in arch])
# dim blue night ground of the painting with yellow stars
layer(a, inner, np.full((H, W), 0.55), B)
img = Image.fromarray(a); d = ImageDraw.Draw(img)
for (sx, sy) in [(AX - 26, pt + 26), (AX + 24, pt + 28), (AX - 8, pt + 8), (AX + 10, pt + 12),
                 (AX - 30, pt + 44), (AX + 30, pt + 46)]:
    d.rectangle([sx * S, sy * S, sx * S + 3, sy * S + 3], fill=Y)
# Christ (left) and Madonna (right) enthroned, Francis kneeling below
def figure(cx, top, robe, mantle, h=34):
    d.ellipse([(cx - 6) * S, (top - 6) * S, (cx + 6) * S, (top + 6) * S], fill=Y)          # halo
    d.ellipse([(cx - 3) * S, (top - 3) * S, (cx + 3) * S, (top + 3) * S], fill=WH)        # face
    d.polygon(P([(cx - 3, top + 3), (cx + 3, top + 3), (cx + 9, top + h), (cx - 9, top + h)]), fill=robe)
    d.polygon(P([(cx - 4, top + 2), (cx - 1, top + 4), (cx - 3, top + h), (cx - 10, top + h)]), fill=mantle)
    d.line(P([(cx - 1, top + 12), (cx + 6, top + 14)]), fill=WH, width=2)               # gesture
figure(AX - 15, pt + 22, R, B)
figure(AX + 15, pt + 24, B, WH)
d.ellipse([(AX - 10) * S, (pt + 9) * S, (AX + 10) * S, (pt + 15) * S], outline=WH, width=2)  # glory
# kneeling Francis in brown-ish (red+black stripes) with green ground
d.rectangle([(pl + 2) * S, (pb - 9) * S, (pr - 2) * S, (pb - 2) * S], fill=G)
d.polygon(P([(AX - 6, pb - 9), (AX + 6, pb - 9), (AX + 4, pb - 20), (AX - 2, pb - 22)]), fill=K)
d.line(P([(AX - 4, pb - 10), (AX - 1, pb - 20)]), fill=R, width=2)
d.ellipse([(AX + 1) * S, (pb - 28) * S, (AX + 9) * S, (pb - 20) * S], fill=Y)
d.ellipse([(AX + 3) * S, (pb - 26) * S, (AX + 7) * S, (pb - 22) * S], fill=WH)
for gx_ in range(int(pl + 4), int(pr - 3), 5):
    d.line(P([(gx_, pb - 3), (gx_ + 1, pb - 8)]), fill=Y if gx_ % 2 else K, width=2)

# round-arched door, lamp-lit interior
dl, dr, dtop, db = AX - 18, AX + 18, 462, BASE - 5
# voussoirs
for k in range(11):
    t0 = math.pi + k * math.pi / 11; t1 = t0 + math.pi / 11
    r0, r1 = 18, 27
    cx, cy = AX, dtop + 18
    q = [(cx + r0 * math.cos(t0), cy + r0 * math.sin(t0)), (cx + r1 * math.cos(t0), cy + r1 * math.sin(t0)),
         (cx + r1 * math.cos(t1), cy + r1 * math.sin(t1)), (cx + r0 * math.cos(t1), cy + r0 * math.sin(t1))]
    d.polygon(P(q), fill=Y if k % 2 else WH, outline=K)
    d.line(P([q[0], q[1]]), fill=K, width=3)
# jambs
for xj in (dl - 8, dr + 1):
    for yj in range(int(dtop + 18), int(db), 9):
        d.rectangle([xj * S, yj * S, (xj + 7) * S, (yj + 8) * S], fill=Y if (yj // 9) % 2 else WH, outline=K, width=2)
d.rectangle([dl * S, (dtop + 18) * S, dr * S, db * S], fill=Y)
d.pieslice([dl * S, dtop * S, dr * S, (dtop + 36) * S], 180, 360, fill=Y)
a = np.asarray(img).copy()
doorm = poly_mask([(dl, db), (dl, dtop + 18)] + [(AX - 18 * math.cos(t), dtop + 18 - 18 * math.sin(t)) for t in np.linspace(0, math.pi, 16)] + [(dr, db)])
# interior depth: red screen toward the edges, bright core
dd_ = np.hypot((xx - AX) / 16.0, (yy - 486) / 30.0)
layer(a, doorm, np.clip((dd_ - 0.55) * 0.9, 0, 0.7), R)
img = Image.fromarray(a); d = ImageDraw.Draw(img)
# altar with candles and hanging lamp inside
d.rectangle([(AX - 8) * S, (db - 12) * S, (AX + 8) * S, db * S], fill=K)
d.line(P([(AX - 8, db - 12), (AX + 8, db - 12)]), fill=WH, width=2)
d.rectangle([(AX - 3) * S, (db - 10) * S, (AX + 3) * S, (db - 4) * S], fill=R)
for cxp in (AX - 6, AX + 5):
    d.rectangle([cxp * S, (db - 19) * S, (cxp + 1) * S + 1, (db - 12) * S], fill=WH)
    d.ellipse([(cxp - 0.5) * S, (db - 23) * S, (cxp + 1.5) * S, (db - 19) * S], fill=R)
d.line(P([(AX, dtop + 2), (AX, dtop + 16)]), fill=K, width=2)
d.polygon(P([(AX - 4, dtop + 16), (AX + 4, dtop + 16), (AX + 2, dtop + 21), (AX - 2, dtop + 21)]), fill=K)
d.ellipse([(AX - 1) * S, (dtop + 21) * S, (AX + 1) * S, (dtop + 24) * S], fill=R)
# open door leaves (dark wood, studs)
d.polygon(P([(dl, dtop + 18), (dl + 7, dtop + 22), (dl + 7, db + 2), (dl, db)]), fill=K)
d.polygon(P([(dr, dtop + 18), (dr - 7, dtop + 22), (dr - 7, db + 2), (dr, db)]), fill=K)
for yv in range(int(dtop + 26), int(db), 8):
    d.rectangle([(dl + 2) * S, yv * S, (dl + 4) * S, yv * S + 3], fill=Y)
    d.rectangle([(dr - 4) * S, yv * S, (dr - 2) * S, yv * S + 3], fill=Y)
# light spilling down the step
d.polygon(P([(dl + 7, db + 1), (dr - 7, db + 1), (dr + 6, BASE + 6), (dl - 6, BASE + 6)]), fill=Y)
a = np.asarray(img).copy()

# lantern on a bracket, left of door
img = Image.fromarray(a); d = ImageDraw.Draw(img)
lx_, ly_ = FL + 14, 452
d.line(P([(lx_ - 4, ly_ - 8), (lx_ + 2, ly_ - 8), (lx_ + 2, ly_ - 4)]), fill=K, width=4)
d.polygon(P([(lx_ - 2, ly_ - 4), (lx_ + 6, ly_ - 4), (lx_ + 5, ly_ + 6), (lx_ - 1, ly_ + 6)]), fill=K)
d.rectangle([(lx_) * S, (ly_ - 2) * S, (lx_ + 4) * S, (ly_ + 4) * S], fill=Y)
d.line(P([(lx_ + 2, ly_ - 2), (lx_ + 2, ly_ + 4)]), fill=R, width=2)
a = np.asarray(img).copy()

# ---------------------------------------------------------------- larks (helix vortex)
def lark(dd, x, y, s, heading, flap, twist):
    """side-on lark in flight: an 'M' of bent wings, small body and tail.
    heading only sets the bank (tilt); flap in [0.5,1.1] = wing lift."""
    bank = 0.35 * math.sin(heading)
    cb, sb = math.cos(bank), math.sin(bank)
    left = math.cos(heading) < 0                     # flying leftwards -> mirror head/tail
    def T(px, py):
        if left:
            px = -px
        return ((x + (px * cb - py * sb) * s) * S, (y + (px * sb + py * cb) * s) * S)
    lift = 0.55 * flap
    down = flap < 0.7                                # down-stroke: tips droop
    tipy = 0.25 if down else -lift
    wl = [(-1.0 * twist, tipy), (-0.45, -lift * 0.75 if not down else -0.2), (0, 0.05)]
    wr = [(0, 0.05), (0.45, -lift * 0.8 if not down else -0.22), (1.0, tipy + 0.05)]
    pts = wl + wr[1:]
    dd.line([T(px, py) for px, py in pts], fill=255, width=int(max(6, s * 0.75)), joint="curve")
    # body (head forward = +x), tail
    dd.polygon([T(px, py) for px, py in [(0.32, 0.02), (0.22, -0.08), (-0.1, -0.06), (-0.42, 0.06),
                                          (-0.5, 0.18), (-0.3, 0.16), (0.0, 0.16), (0.24, 0.10)]], fill=255)
    dd.ellipse([T(0.3, 0.0)[0] - 3, T(0.3, 0.0)[1] - 3, T(0.3, 0.0)[0] + 3, T(0.3, 0.0)[1] + 3], fill=255)


bird_l = Image.new("L", (W2, H2), 0); bd_ = ImageDraw.Draw(bird_l)
N = 48
turns = 2.4
birds = []
TOP_DY = 226
def helix(t):
    th = 0.4 + t * turns * 2 * math.pi
    r = 14 + 112 * t ** 0.85
    cy = APEX - 50 - TOP_DY * t
    return th, r, AX + r * math.cos(th), cy + 0.46 * r * math.sin(th)
ts = np.linspace(0, 1, 4000)
pts_ = np.array([helix(t)[2:] for t in ts])
arc = np.concatenate([[0], np.cumsum(np.hypot(*np.diff(pts_, axis=0).T))])
for i in range(N):
    target = (i + 0.5 + rng.uniform(-0.2, 0.2)) / N * arc[-1]
    t = float(np.interp(target, arc, ts))
    th, r, x, y = helix(t)
    depth = math.sin(th)
    s = 8.0 + 4.0 * t + 2.5 * depth
    s = max(s, 7.0)
    dxdt = -r * math.sin(th)
    dydt = 0.46 * r * math.cos(th) - TOP_DY / (turns * 2 * math.pi)
    heading = math.atan2(dydt, dxdt) + rng.uniform(-0.2, 0.2)
    flap = rng.uniform(0.55, 1.1)
    twist = rng.uniform(0.65, 1.05)
    birds.append((depth, x, y, s, heading, flap, twist))
birds.sort()
for depth, x, y, s, heading, flap, twist in birds:
    if y < 6:
        continue
    bl_ = Image.new("L", (W2, H2), 0)
    lark(ImageDraw.Draw(bl_), x, y, s, heading, flap, twist)
    bm = np.asarray(bl_) > 127
    halo = bm.copy()
    for dy_, dx_ in ((-2, 0), (2, 0), (0, -2), (0, 2)):
        halo |= np.roll(np.roll(bm, dy_, 0), dx_, 1)
    on_moon = math.hypot(x - MX, y - MY) < MR + 4
    if on_moon:
        a[bm] = K
        continue
    a[halo] = K
    # moonlit top edge white, underside black: the shape minus itself shifted up
    up_ = np.zeros_like(bm); up_[2:, :] = bm[:-2, :]
    top_edge = bm & ~up_
    up2 = np.zeros_like(bm); up2[4:, :] = bm[:-4, :]
    top2 = bm & ~up2
    if depth > -0.3:
        a[bm] = K
        a[top2] = WH
    else:
        a[bm] = K
        a[top2] = B

# ---------------------------------------------------------------- foreground: dry-stone wall, grass
WT, WB = 546, 584
wrng = np.random.default_rng(131)
img = Image.fromarray(a); d = ImageDraw.Draw(img)
d.rectangle([0, (WT + 4) * S, W2, H2], fill=K)
gate_l, gate_r = 176, 232
wl = Image.new("L", (W2, H2), 0); wld = ImageDraw.Draw(wl)
later = []
for seg in ((-6, gate_l), (gate_r, W + 6)):
    y = WB
    row = 0
    while y > WT:
        hh = wrng.uniform(6, 10)
        x = seg[0] - wrng.uniform(0, 8)
        while x < seg[1]:
            ww = wrng.uniform(9, 22)
            x1 = min(seg[1], x + ww)
            yt = y - hh + wrng.uniform(-1.5, 1.5) + 0.04 * (x - 200) * 0
            q = [(x + 1, y - 1), (x + 0.5, yt + 2), (x + 3, yt), (x1 - 2, yt + wrng.uniform(-1, 1)),
                 (x1 - 0.5, yt + 2), (x1 - 1, y - 1)]
            ton = wrng.random()
            wld.polygon(P(q), fill=int(40 + 70 * ton))
            near = abs((x + x1) / 2 - 204) < 46
            col = (Y if wrng.random() < 0.6 else WH) if near else (WH if ton < 0.45 else B)
            later.append(((x + 2.5, yt + 0.8), (x1 - 2, yt + 0.8), col))
            if ton > 0.55:
                later.append(((x1 - 2, yt + 2), (x1 - 2, y - 2), K))
            x = x1
        y -= hh
        row += 1
    # (stone faces screened, then their moonlit top edges)
    a = np.asarray(img).copy()
    wl_a = np.asarray(wl)[::S, ::S].astype(np.float32) / 255
    wmask = up(wl_a > 0.01)
    layer(a, wmask, wl_a, B)
    img = Image.fromarray(a); d = ImageDraw.Draw(img)
    for p0, p1, col in later:
        d.line(P([p0, p1]), fill=col, width=2)
    later = []
    # capstones on top, upright
    x = seg[0]
    while x < seg[1] - 4:
        ww = wrng.uniform(5, 9)
        x1 = min(seg[1], x + ww)
        tp = WT - wrng.uniform(4, 9)
        d.polygon(P([(x + 0.5, WT + 2), (x + 1, tp + 1), (x + ww * 0.5, tp), (x1 - 0.5, tp + 2), (x1 - 0.5, WT + 2)]), fill=K)
        d.line(P([(x + ww * 0.5, tp + 0.5), (x1 - 0.8, tp + 2.5), (x1 - 0.8, WT - 1)]),
               fill=WH if wrng.random() < 0.5 else B, width=2)
        x = x1 + 0.6
# path between gate posts, lamp-light fading
d.polygon(P([(gate_l + 2, WT + 4), (gate_r - 2, WT + 4), (gate_r + 8, H), (gate_l - 8, H)]), fill=K)
for i in range(18):
    py = WT + 6 + i * 2.6
    px = 186 + wrng.uniform(-6, 30)
    d.ellipse([(px) * S, py * S, (px + wrng.uniform(3, 6)) * S, (py + 2) * S], fill=Y if i < 9 else B)
# gate posts
for gp in (gate_l, gate_r - 7):
    d.rectangle([gp * S, (WT - 14) * S, (gp + 7) * S, (WB + 2) * S], fill=K)
    d.line(P([(gp + 6, WT - 13), (gp + 6, WB)]), fill=WH, width=2)
    for yv in range(int(WT - 10), int(WB), 7):
        d.line(P([(gp + 1, yv), (gp + 6, yv)]), fill=B, width=2)
    d.polygon(P([(gp - 1, WT - 14), (gp + 3.5, WT - 19), (gp + 8, WT - 14)]), fill=K)
    d.line(P([(gp + 3.5, WT - 19), (gp + 8, WT - 14)]), fill=WH, width=2)

# grass tufts along the wall foot and in front of the facade line
def tuft(cx, base, hgt, n, col_tip):
    for k in range(n):
        ang = -math.pi / 2 + wrng.uniform(-0.75, 0.75)
        L = hgt * wrng.uniform(0.6, 1.0)
        x1 = cx + L * math.cos(ang) + wrng.uniform(-1, 1); y1 = base + L * math.sin(ang)
        mx_ = (cx + x1) / 2 + wrng.uniform(-2, 2); my_ = (base + y1) / 2
        d.line(P([(cx + wrng.uniform(-2, 2), base), (mx_, my_)]), fill=K, width=4)
        d.line(P([(mx_, my_), (x1, y1)]), fill=K, width=3)
        if wrng.random() < 0.6:
            d.line(P([(mx_ + 0.6, my_), (x1 + 0.6, y1)]), fill=col_tip if wrng.random() < 0.6 else B, width=2)

for i in range(26):
    cx = wrng.uniform(0, W)
    if gate_l - 6 < cx < gate_r + 6:
        continue
    tuft(cx, WT - 2, wrng.uniform(8, 16), int(wrng.integers(4, 8)), WH)
for i in range(18):
    cx = wrng.uniform(0, W)
    if gate_l - 4 < cx < gate_r + 4:
        continue
    tuft(cx, WB + 4, wrng.uniform(6, 11), int(wrng.integers(3, 6)), B)
for i in range(22):
    cx = wrng.uniform(0, W)
    if 120 < cx < 285:
        continue
    tuft(cx, 512 + wrng.uniform(0, 26), wrng.uniform(5, 9), int(wrng.integers(3, 5)), WH)
# a few in the lamp light near the step
for cx in (150, 162, 244, 256):
    tuft(cx, 522, 7, 4, Y)

# inscription
f = font("serif", 14 * S)
txt = "3 · X · 1226"
bb = d.textbbox((0, 0), txt, font=f)
tw = bb[2] - bb[0]
d.rectangle([0, 586 * S, W2, H2], fill=K)
d.text(((W2 - tw) // 2 - bb[0], 586 * S - bb[1] - 1), txt, font=f, fill=WH)

# collapse each 2x2 block to ONE of its own colours (the one nearest the block mean),
# so thin anti-aliased edges never snap to an invented colour (blue+yellow -> green).
def block_snap(im):
    q = np.asarray(im).astype(np.float32).reshape(H, 2, W, 2, 3).transpose(0, 2, 1, 3, 4).reshape(H, W, 4, 3)
    mean = q.mean(2, keepdims=True)
    best = ((q - mean) ** 2).sum(-1).argmin(2)
    pick = np.take_along_axis(q, best[..., None, None], 2)[:, :, 0]
    return Image.fromarray(up(pick.astype(np.uint8).transpose(2, 0, 1)).transpose(1, 2, 0).copy()) if False else \
        Image.fromarray(np.repeat(np.repeat(pick.astype(np.uint8), S, 0), S, 1))

finish(block_snap(img))
