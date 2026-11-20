"""I. Clouds are not spheres — dawn sky of fBm cumulus, engraved with iso-density lines,
over a patchwork of fields. Full palette; blue/white in charge."""
import numpy as np
from common import *

rng = np.random.default_rng(1120)
p = Plate(WH)
HZ = 452                                   # horizon
t = np.clip(YY / HZ, 0, 1)

# --- sky: blue -> paper -> yellow -> a little red at the horizon -----------------
p.put(screen(np.clip(1.0 - t * 1.75, 0, 1) ** 0.9), B)
p.put(screen(np.clip((t - 0.52) / 0.42, 0, 1) ** 1.3), Y)
p.put(screen(np.clip((t - 0.9) / 0.1, 0, 1) * 0.55), R)

# --- sun and its rays ----------------------------------------------------------
SX, SY = 118, HZ + 6
dx, dy = XX - SX, YY - SY
rad = np.hypot(dx, dy)
ang = np.arctan2(dy, dx)
rays = (np.floor(ang / (np.pi / 36)) % 2 == 0) & (rad < 330) & (rad > 52)
p.put(rays & screen(np.clip(1.15 - rad / 300, 0, 1)) & (YY < HZ), Y)
p.put(rays & (rad < 120) & (YY < HZ), Y)
p.put((rad < 50), Y)
p.put((rad < 50) & (rad > 45), R)
p.put((rad < 40) & (rad > 38), R)
p.put((rad < 56) & (rad > 54), R)

# --- clouds: three decks, each its own fBm, flat-based -------------------------
decks = [  # base y, depth, noise scale, threshold, seed
    (150, 135, 110, 0.50, 7),
    (292, 95, 70, 0.52, 21),
    (392, 55, 40, 0.53, 33),
    (436, 26, 22, 0.54, 41),
]
LX, LY = -0.55, 0.83                       # direction to the light (low, left)
for base, depth, sc, thr, seed in decks:
    d = fbm(seed, scale=sc, octaves=6, gain=0.55, stretch=(0.6, 1.5))
    up = (base - YY) / depth               # 0 at base, 1 at top
    prof = np.where(up < 0, -1.0, np.clip(up * 9, 0, 1) * np.clip(1.25 - up, 0, 1) ** 0.8)
    wide = fbm(seed + 100, scale=sc * 2.2, octaves=2, stretch=(4, 1))  # gaps in the deck
    dens = (d - thr) + 0.34 * (prof - 0.72) + 0.5 * (wide - 0.5)
    dens[up < 0] = -1
    cloud = dens > 0
    gy, gx = np.gradient(blur(np.clip(dens * 3 + 0.5, 0, 1), 2.0))
    lit = (gx * LX + gy * LY)
    lit = lit / (np.abs(lit).max() + 1e-6) * 4
    body = np.clip(dens * 5, 0, 1)         # 0 at rim, 1 deep inside
    p.put(cloud, WH)
    # shadowed flanks: blue line-screen, heavier away from the sun
    sh = np.clip(-lit * 1.4 + 0.15, 0, 0.85) * cloud
    p.put(hatch(sh, angle=28, period=4) & cloud, B)
    # deep interior on the dark side goes to solid blue with white stipple
    p.put(cloud & (lit < -0.55) & screen(np.clip(body * 0.9, 0, 0.8)), B)
    # sun-facing bellies catch yellow, then red right at the base
    warm = np.clip(lit * 1.6, 0, 1) * np.clip(1.2 - up * 2.2, 0, 1) * cloud
    p.put(screen(warm * 0.95), Y)
    p.put(cloud & (up < 0.07) & screen(np.clip(warm * 1.2, 0, 0.7)), R)
    # engraved iso-density lines
    lev = np.floor(dens / 0.045)
    iso = np.zeros_like(cloud)
    iso[:, :-1] |= lev[:, :-1] != lev[:, 1:]
    iso[:-1, :] |= lev[:-1, :] != lev[1:, :]
    iso &= cloud & (dens > 0.03)
    was_blue = p.a == B
    p.put(iso & ~was_blue, B)
    p.put(iso & was_blue, WH)
    p.put(edge(cloud), B)
    p.put(edge(cloud) & (lit < -0.2), K)
    # flat base gets a firm dark line
    p.put(cloud & (up < 0.03), K)

# --- geese, a ragged V ---------------------------------------------------------
with p.draw() as d:
    for i in range(-7, 9):
        bx = 262 + i * 9
        by = 246 + abs(i) * 5 + int(rng.integers(-1, 2))
        d.line([(bx - 4, by - 2), (bx, by), (bx + 4, by - 3)], fill=K)
        d.point((bx, by + 1), fill=K)

# --- land ----------------------------------------------------------------------
land = YY >= HZ
p.put(land, G)
x = np.arange(W)
far = HZ - 10 - 14 * fbm(5, scale=90, octaves=4, shape=(1, W))[0] - 6 * np.sin(x / 70.0)
far_m = (YY >= far[None, :]) & (YY < HZ + 8)
p.put(far_m, B)
p.put(far_m & screen(0.35 + 0 * t), WH)
p.put(far_m & (np.abs(YY - far[None, :]) < 1), B)
p.put((rad < 50) & (YY < far[None, :] + 0), Y)  # sun sits behind the far ridge

# patchwork: Voronoi fields in a perspective-warped plane
depthv = 1.0 / (YY - HZ + 9.0)             # big near the horizon
u = (XX - 200) * depthv * 9.0
v = depthv * 620.0
n = 240
pu = rng.uniform(u[land].min(), u[land].max(), n)
pv = rng.uniform(v[land].min() * 0.9, v[land].max(), n)
best = np.full((H, W), 1e9, np.float32); second = best.copy(); owner = np.zeros((H, W), np.int32)
for i in range(n):
    dd = np.hypot(u - pu[i], (v - pv[i]) * 1.6).astype(np.float32)
    closer = dd < best
    second = np.where(closer, best, np.minimum(second, dd))
    owner = np.where(closer, i, owner)
    best = np.where(closer, dd, best)
kind = rng.integers(0, 7, n)[owner]
angf = rng.choice([20, 65, 110, 155], n)[owner]
near = np.clip((YY - HZ) / 120.0, 0, 1)
per = 3 + np.round(near * 3)
for a in (20, 65, 110, 155):
    for pr in (3, 4, 5, 6):
        sel = land & (angf == a) & (per == pr)
        p.put(sel & (kind == 0) & hatch(0.5, a, pr), Y)          # stubble
        p.put(sel & (kind == 1), Y)
        p.put(sel & (kind == 1) & hatch(0.3, a, pr), K)          # ploughed, lit
        p.put(sel & (kind == 2) & hatch(0.34, a, pr), K)         # dark pasture
        p.put(sel & (kind == 3), Y)                              # ripe
        p.put(sel & (kind == 3) & hatch(0.25, a, pr + 1), R)
p.put(land & (kind == 4) & screen(0.3 + 0 * t), Y)               # meadow stipple
p.put(land & (kind == 5) & screen(0.22 + 0 * t), K)
hedge = land & ((second - best) < (0.02 + 0.10 * depthv * 9)) & ~far_m
p.put(hedge, K)

# river: a white ribbon with blue ripples, winding to the horizon
ys = np.arange(HZ + 6, H)
cx = 250 + 70 * np.sin((ys - HZ) / 26.0) * np.clip((ys - HZ) / 60.0, 0.15, 1) - (ys - HZ) * 0.5
hw = 1.5 + (ys - HZ) * 0.16
riv = np.zeros((H, W), bool)
for yy, c, h_ in zip(ys, cx, hw):
    riv[yy, max(0, int(c - h_)):min(W, int(c + h_) + 1)] = True
p.put(grow(riv, 1) & land, K)
p.put(riv, WH)
p.put(riv & hatch(0.3, 90, 4), B)

# the pond (the day's small set), in a near field
m = mandel(58)
p.stamp(grow(m, 1), 300, 522, K)
p.stamp(m, 300, 522, B)
p.stamp(m & (np.indices(m.shape)[0] % 3 == 0), 300, 522, WH)

# trees along hedges and a village with a spire
with p.draw() as d:
    for _ in range(170):
        ty = int(rng.integers(HZ + 12, 572)); tx = int(rng.integers(0, W))
        if riv[ty, tx] or (296 < tx < 362 and 516 < ty < 574):
            continue
        r = 1 + (ty - HZ) / 22.0
        d.ellipse([tx - r, ty - 2 * r, tx + r, ty], fill=K)
        d.ellipse([tx - r + 1, ty - 2 * r + 1, tx + r - 1, ty - 1], fill=G)
        d.point((tx - r / 2, ty - 1.4 * r), fill=Y)
        d.line([(tx + r, ty), (tx + 2.5 * r, ty + r / 2)], fill=K)   # long dawn shadow
    for i in range(13):
        hx = 34 + int(rng.integers(0, 78)); hy = 492 + int(rng.integers(0, 22))
        s = 5 + (hy - 488) // 6
        d.rectangle([hx, hy, hx + s + 3, hy + s], fill=WH, outline=K)
        d.polygon([(hx - 2, hy), (hx + (s + 3) / 2, hy - s + 1), (hx + s + 5, hy)], fill=R, outline=K)
        d.point((hx + 2, hy + 2), fill=Y); d.point((hx + s, hy + 2), fill=K)
    d.rectangle([70, 474, 78, 500], fill=WH, outline=K)                # church tower
    d.polygon([(69, 474), (74, 452), (79, 474)], fill=R, outline=K)
    d.rectangle([78, 488, 98, 500], fill=WH, outline=K)
    d.polygon([(78, 488), (88, 480), (98, 488)], fill=R, outline=K)
    d.line([(74, 452), (74, 447)], fill=K); d.line([(72, 449), (76, 449)], fill=K)

p.caption("I", "CLOUDS ARE NOT SPHERES")
p.save()
