"""IV. Bark is not smooth — an old trunk at sunset, its plates and furrows grown from
stretched Worley cells wrapped round a cylinder; lichen, ivy, brackets, a woodpecker,
and a knot-hole in the shape of the day's set. Bare fractal trees behind. Red and black."""
import numpy as np
from common import *

rng = np.random.default_rng(1982)          # The Fractal Geometry of Nature
PIC_H = H - 26
HZ = 468
p = Plate(R)

# --- sky --------------------------------------------------------------------------
t = np.clip(YY / HZ, 0, 1)
p.put(screen(np.clip(0.55 - t * 1.5, 0, 0.6)), K)                 # dusk coming down from the top
p.put(screen(np.clip((t - 0.38) / 0.55, 0, 1) ** 1.2), Y)
SX, SY = 338, 430
rad = np.hypot(XX - SX, YY - SY)
p.put(rad < 44, Y); p.put(rad < 36, WH); p.put((rad < 37) & (rad > 34), R)
bands = fbm(5, scale=50, octaves=4, stretch=(0.18, 3.0))
strat = (bands > 0.60) & (YY < HZ - 30) & (YY > 120)
p.put(strat, R); p.put(strat & hatch(0.4, 90, 3), K)
p.put((bands > 0.66) & (YY < 140), K)

# --- distant ground and bare trees ---------------------------------------------------
ground = YY >= HZ - 3 * fbm(2, scale=40, octaves=3)
p.put(ground, K)
def tree(d, x, y, ang, length, width, depth):
    if depth == 0 or length < 2:
        return
    x2 = x + np.cos(ang) * length; y2 = y - np.sin(ang) * length
    d.line([(x, y), (x2, y2)], fill=K, width=max(1, int(round(width))))
    n = 2 if rng.random() < 0.75 else 3
    for _ in range(n):
        tree(d, x2, y2, ang + rng.normal(0, 0.45), length * rng.uniform(0.62, 0.82), width * 0.62, depth - 1)
with p.draw() as d:
    for tx, sz in ((318, 62), (366, 46), (386, 30), (286, 34), (20, 44), (46, 30), (350, 24)):
        tree(d, tx, HZ + 2, np.pi / 2 + rng.normal(0, 0.08), sz, sz / 9.0, 9)
    for _ in range(11):                                       # rooks going to roost
        bx, by = rng.integers(250, 392), rng.integers(170, 330)
        d.line([(bx - 4, by - 2), (bx, by), (bx + 4, by - 2)], fill=K)

# leaf litter
lit_y, lit_x = np.nonzero(ground & (YY < PIC_H))
for c, n in ((R, 900), (Y, 500), (G, 120)):
    i = rng.choice(len(lit_y), n)
    yy, xx = lit_y[i], lit_x[i]
    p.a[yy, xx] = c; p.a[yy, np.clip(xx + 1, 0, W - 1)] = c
    big = yy > HZ + 40
    p.a[np.clip(yy[big] + 1, 0, H - 1), xx[big]] = c

# --- the trunk ------------------------------------------------------------------------
cxl = 168 + 9 * np.sin(YY / 190.0)
flare = np.clip((YY - 455) / 120.0, 0, 1) ** 2 * 70
rr = 108 + (YY - 300) * 0.03 + flare
u = (XX - cxl) / rr
trunk = (np.abs(u) < 1) & (YY < PIC_H)
theta = np.arcsin(np.clip(u, -1, 1))
s = theta * 112.0                                   # arc length round the bole
warp = (fbm(31, scale=60, octaves=4) - 0.5) * 34
def worley(a, b, ca, cb, seed, jitter=0.9):
    """F1, F2 for a jittered grid with cell size (ca, cb) over coords (a, b)."""
    ga, gb = a / ca, b / cb
    ia, ib = np.floor(ga).astype(int), np.floor(gb).astype(int)
    f1 = np.full(a.shape, 9.0, np.float32); f2 = f1.copy(); cid = np.zeros(a.shape, np.int64)
    for da in (-1, 0, 1):
        for db in (-1, 0, 1):
            ja, jb = ia + da, ib + db
            hsh = (ja * 73856093) ^ (jb * 19349663) ^ (seed * 83492791)
            r1 = ((hsh * 1103515245 + 12345) & 0x7FFFFFFF) / 0x7FFFFFFF
            r2 = ((hsh * 134775813 + 1) & 0x7FFFFFFF) / 0x7FFFFFFF
            pa = ja + 0.5 + (r1 - 0.5) * jitter; pb = jb + 0.5 + (r2 - 0.5) * jitter
            dd = np.hypot(ga - pa, gb - pb).astype(np.float32)
            closer = dd < f1
            f2 = np.where(closer, f1, np.minimum(f2, dd)); cid = np.where(closer, hsh, cid)
            f1 = np.where(closer, dd, f1)
    return f1, f2, cid
f1, f2, cid = worley(s + warp, YY + warp * 0.6, 21.0, 74.0, 4)
e = f2 - f1                                          # 0 in the furrows
g1, g2, _ = worley(s + warp * 1.4 + 300, YY + 900, 8.0, 27.0, 9)
e2 = g2 - g1
furrow = e < (0.07 + 0.09 * fbm(6, scale=24, octaves=3))
crack = (e2 < 0.07) & ~furrow
plate_r = ((cid * 2654435761) & 0xFFFF) / 65535.0     # each plate its own lean
TL = 0.95                                            # light comes round from the right
lam = np.cos(theta - TL)
des = np.gradient(e, axis=1)                         # plate edge facing the light
lightv = np.clip(lam * 0.55 + des * 3.5 + (plate_r - 0.5) * 0.30 + 0.30, 0, 1)
fib = fbm(12, scale=10, octaves=3, stretch=(6.0, 0.35))  # vertical fibre

p.put(trunk, K)
tops = trunk & ~furrow
p.put(tops & screen(np.clip(lightv * 1.9 - 0.12, 0, 1)), R)
p.put(tops & screen(np.clip((lightv - 0.50) * 2.6, 0, 1)), Y)
p.put(tops & (lightv > 0.9) & screen(0.35 + 0 * lightv), WH)
p.put(tops & (fib > 0.60) & (lightv > 0.25), K)                       # fibre lines
p.put(tops & (fib < 0.36) & (lightv > 0.45) & (lightv < 0.8), R)
p.put(trunk & crack, K)
p.put(trunk & furrow, K)
p.put(trunk & furrow & (e < 0.03) & (lam > 0.75) & screen(0.4 + 0 * e), R)   # light gets into the deep ones
# cold skylight on the far left flank
p.put(tops & (u < -0.62) & screen(np.clip((-u - 0.62) * 2.2, 0, 0.75)), B)
# lichen on the shaded side, moss at the foot
lich = tops & (fbm(13, scale=26, octaves=4) > 0.60) & (u < 0.25) & (u > -0.9)
p.put(lich, G); p.put(lich & screen(0.3 + 0 * e), WH); p.put(edge(lich), K)
moss = trunk & (YY > 500 - 30 * fbm(14, scale=30, octaves=3)) & (fbm(15, scale=18, octaves=3) > 0.42)
p.put(moss & ~furrow, G); p.put(moss & ~furrow & screen(0.35 + 0 * e), K); p.put(moss & ~furrow & (fib > 0.66) & (lam > 0.5), Y)
# trunk outline
p.put(trunk & ~np.roll(trunk, 1, axis=1), K); p.put(trunk & ~np.roll(trunk, -1, axis=1), Y)
p.put(trunk & ~np.roll(trunk, -2, axis=1), Y)

# --- knot-hole: the set, head up ---------------------------------------------------------
m = np.rot90(mandel(78), -1)
kx, ky = 118, 262
for g_, col in ((9, K), (7, Y), (5, R), (3, K)):
    p.stamp(grow(np.pad(m, 10), g_), kx - 10, ky - 10, col)
p.stamp(m, kx, ky, K)
with p.draw() as d:
    ox, oy = kx + m.shape[1] // 2, ky + int(m.shape[0] * 0.62)        # someone lives here
    for sx_ in (-9, 9):
        d.ellipse([ox + sx_ - 6, oy - 6, ox + sx_ + 6, oy + 6], fill=Y)
        d.ellipse([ox + sx_ - 3, oy - 3, ox + sx_ + 3, oy + 3], fill=K)
        d.point((ox + sx_ + 1, oy - 1), fill=WH)
    d.polygon([(ox - 2, oy + 5), (ox + 2, oy + 5), (ox, oy + 10)], fill=Y)

    # bracket fungi up the left flank
    for i, (fy, fw) in enumerate(((392, 34), (408, 44), (426, 38), (441, 26))):
        fx = int(cxl[fy, 0] - rr[fy, 0] * 0.78) - i * 2
        d.pieslice([fx - fw, fy - 9, fx + fw // 3, fy + 9], 180, 360, fill=Y, outline=K)
        d.arc([fx - fw + 4, fy - 6, fx + fw // 3 - 4, fy + 6], 180, 360, fill=R)
        d.arc([fx - fw + 9, fy - 3, fx + fw // 3 - 9, fy + 3], 180, 360, fill=R)
        d.line([(fx - fw, fy), (fx + fw // 3, fy)], fill=K)
        d.line([(fx - fw + 2, fy + 1), (fx + fw // 3 - 2, fy + 1)], fill=WH)

    # ivy climbing the right side
    pts = [(256 + 12 * np.sin(yy / 31.0) + (yy - 300) * 0.03, yy) for yy in range(PIC_H - 2, 70, -3)]
    d.line(pts, fill=K, width=2)
    for i, (ix, iy) in enumerate(pts[::4]):
        sgn = 1 if i % 2 else -1; sz = 7 + (i * 5) % 4
        lx, ly = ix + sgn * (sz + 3), iy - 3
        d.line([(ix, iy), (lx, ly)], fill=K)
        d.polygon([(lx, ly - sz), (lx + sz, ly - sz // 3), (lx + sz // 2, ly + sz // 2), (lx, ly + sz),
                   (lx - sz // 2, ly + sz // 2), (lx - sz, ly - sz // 3)], fill=G, outline=K)
        d.line([(lx, ly - sz + 2), (lx, ly + sz - 2)], fill=Y)
        d.line([(lx - sz + 3, ly - sz // 3 + 1), (lx, ly + 1), (lx + sz - 3, ly - sz // 3 + 1)], fill=Y)

    # great spotted woodpecker, propped on its tail
    wx, wy = 196, 96
    d.ellipse([wx - 12, wy - 12, wx + 32, wy + 58], fill=Y)                                            # a patch of late sun behind it
    d.polygon([(wx + 8, wy + 44), (wx + 2, wy + 70), (wx + 10, wy + 68), (wx + 16, wy + 46)], fill=K)      # tail
    d.ellipse([wx, wy + 8, wx + 26, wy + 52], fill=K)                                                  # back
    d.ellipse([wx - 6, wy + 12, wx + 12, wy + 46], fill=WH, outline=K)                                 # breast
    d.ellipse([wx - 2, wy + 38, wx + 12, wy + 52], fill=R, outline=K)                                  # vent
    d.ellipse([wx + 12, wy + 16, wx + 22, wy + 36], fill=WH)                                           # shoulder patch
    for k in range(4):
        d.line([(wx + 14, wy + 38 + k * 4), (wx + 24, wy + 36 + k * 4)], fill=WH)                      # barred wing
    d.ellipse([wx - 4, wy - 6, wx + 18, wy + 14], fill=K)                                              # head
    d.ellipse([wx - 3, wy + 1, wx + 9, wy + 11], fill=WH)                                              # cheek
    d.rectangle([wx + 10, wy - 5, wx + 17, wy + 1], fill=R)                                            # nape
    d.polygon([(wx - 3, wy + 2), (wx - 17, wy + 5), (wx - 3, wy + 7)], fill=K)                         # bill
    d.ellipse([wx + 1, wy + 1, wx + 4, wy + 4], fill=K); d.point((wx + 2, wy + 2), fill=WH)
    d.line([(wx - 2, wy + 46), (wx - 9, wy + 50)], fill=K, width=2); d.line([(wx - 2, wy + 40), (wx - 9, wy + 43)], fill=K, width=2)
    for k in range(5):                                                                                # chips
        d.point((wx - 20 - k * 3, wy + 10 + k * k), fill=Y)

# --- a limb leaving top right, rim-lit ---------------------------------------------------
limb = Plate(0)
with limb.draw() as d:
    def branch(x, y, ang, length, width, depth):
        if depth == 0 or width < 0.6:
            return
        x2 = x + np.cos(ang) * length; y2 = y - np.sin(ang) * length
        d.line([(x, y), (x2, y2)], fill=1, width=max(1, int(round(width))))
        d.ellipse([x2 - width / 2, y2 - width / 2, x2 + width / 2, y2 + width / 2], fill=1)
        branch(x2, y2, ang + rng.normal(0.02, 0.16), length * 0.86, width * 0.80, depth - 1)
        if rng.random() < 0.72:
            branch(x2, y2, ang + rng.choice([-1, 1]) * rng.uniform(0.5, 1.0), length * 0.7, width * 0.45, depth - 2)
    branch(262, 150, 0.70, 46, 34, 12)
lm = (limb.a == 1) & ~trunk & (YY < HZ)
p.put(lm, K)
under = lm & ~np.roll(lm, -2, axis=0) | lm & ~np.roll(lm, -2, axis=1)
p.put(grow(under, 1) & lm, R); p.put(under, Y)
thick = lm & np.roll(lm, 6, axis=0) & np.roll(lm, -6, axis=0)
p.put(thick & hatch(0.3, 35, 5) & (fbm(19, scale=9, octaves=2) > 0.5), R)
# the last leaves
ys_, xs_ = np.nonzero(edge(lm) & (XX > 290))
with p.draw() as d:
    for i in rng.choice(len(ys_), 46):
        x, y = int(xs_[i]), int(ys_[i]); c = [Y, Y, R, G][rng.integers(4)]
        d.polygon([(x, y), (x + 3, y + 4), (x, y + 9), (x - 3, y + 4)], fill=c, outline=K)

p.caption("IV", "BARK IS NOT SMOOTH")
p.save()
