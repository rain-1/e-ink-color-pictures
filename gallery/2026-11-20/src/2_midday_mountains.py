"""II. Mountains are not cones — a ridged-fBm heightfield seen with a voxel-space
renderer, then inked like a survey plate: contours, hatching, a forest of tiny firs,
and one red dashed cone that fails to fit the peak. Full palette; white/blue in charge."""
import numpy as np
from common import *

rng = np.random.default_rng(1924)
N = 1024
PIC_H = H - 26

# --- the terrain ---------------------------------------------------------------
n1 = fbm(11, scale=320, octaves=7, gain=0.5, shape=(N, N))
n2 = fbm(12, scale=200, octaves=7, gain=0.5, shape=(N, N))
ridge = (1 - np.abs(2 * n2 - 1)) ** 2
my, mx = np.mgrid[0:N, 0:N].astype(np.float32)
def bump(cx, cy, r): return np.exp(-(((mx - cx) ** 2 + (my - cy) ** 2) / (2 * r * r)))
hm = 0.50 * n1 + 0.50 * ridge * (0.45 + n1)
hm += 0.55 * bump(520, 470, 120) + 0.3 * bump(250, 380, 110) + 0.28 * bump(810, 330, 120)
hm -= 0.36 * bump(500, 880, 105) + 0.15 * bump(640, 760, 70)
hm = np.clip((hm - hm.min()) / (np.percentile(hm[300:700, 250:800], 99.9) - hm.min()), 0, 1.1)
SEA = 0.25
m = mandel(150)                              # the tarn is the day's set, lying on its side
tarn = np.zeros((N, N), bool)
tarn[790:790 + m.shape[0], 420:570] = m
hm = np.where(tarn, SEA - 0.01, hm)
water = hm < SEA
hm = np.maximum(hm, SEA)
HS = 380.0
gy, gx = np.gradient(hm * HS)
nrm = np.stack([-gx, -gy, np.ones_like(gx)], -1)
nrm /= np.linalg.norm(nrm, axis=-1, keepdims=True)
sun = np.array([0.55, 0.35, 0.62]); sun /= np.linalg.norm(sun)
lightmap = np.clip(nrm @ sun, 0, 1)
slope = 1 - nrm[..., 2]

# --- voxel-space render --------------------------------------------------------
CAMX, CAMY, CAMH, HZ, S = 500.0, 1075.0, 0.60 * HS, 215.0, 265.0
alt = np.full((H, W), -1, np.float32); lit = np.zeros((H, W), np.float32)
dist = np.zeros((H, W), np.float32); slp = np.zeros((H, W), np.float32)
wat = np.zeros((H, W), bool); tex = np.zeros((H, W, 2), np.float32)
ybuf = np.full(W, float(PIC_H))
cols = (np.arange(W) - W / 2) / (W / 2)
z = 30.0
while z < 1000:
    px = (CAMX + cols * z * 0.62); py = np.full(W, CAMY - z)
    ix = np.clip(px, 0, N - 1).astype(int); iy = np.clip(py, 0, N - 1).astype(int)
    hh = hm[iy, ix] * HS
    ys = (CAMH - hh) / z * S + HZ
    mask = (YY >= ys[None, :]) & (YY < ybuf[None, :])
    if mask.any():
        cc = XX[mask]
        alt[mask] = hm[iy, ix][cc]; lit[mask] = lightmap[iy, ix][cc]
        slp[mask] = slope[iy, ix][cc]; wat[mask] = water[iy, ix][cc]
        dist[mask] = z; tex[mask, 0] = px[cc]; tex[mask, 1] = py[cc]
    ybuf = np.minimum(ybuf, ys)
    z += 0.6 + z * 0.0035
land = alt >= 0
sky = ~land & (YY < PIC_H)

# --- sky -------------------------------------------------------------------------
p = Plate(WH)
p.put(sky & screen(np.clip(0.95 - YY / 330.0, 0, 1) ** 1.1), B)
SX, SY = 322, 58
rad = np.hypot(XX - SX, YY - SY); ang = np.arctan2(YY - SY, XX - SX)
p.put(sky & (np.floor(ang / (np.pi / 24)) % 2 == 0) & (rad > 30) & (rad < 60 + 14 * np.sin(ang * 12)), Y)
p.put(sky & (rad < 25), Y); p.put(sky & (rad < 25) & (rad > 22), R)
cl = fbm(77, scale=60, octaves=5, stretch=(0.35, 1.6))
cloud = sky & (cl + 0.25 * np.exp(-((YY - 150) / 40.0) ** 2) > 0.74)
p.put(cloud, WH); p.put(cloud & hatch(0.3, 0, 3) & (cl < 0.62), B); p.put(edge(cloud), B)

# --- ground ----------------------------------------------------------------------
haze = np.clip((dist - 380) / 700.0, 0, 0.55)
tone = 1 - lit                                # 0 bright .. 1 dark
vis = alt[(alt >= 0) & ~wat]
snowline = float(np.percentile(vis, 80)) - 0.025 + 0.05 * fbm(3, scale=30, octaves=3)
treeline = float(np.percentile(vis, 50)) - 0.025 + 0.05 * fbm(4, scale=40, octaves=3)
snow = land & (alt > snowline) & (slp < 0.62)
rock = land & ~snow & ((alt > treeline) | (slp > 0.8))
veg = land & ~snow & ~rock & ~wat
# rock: paper, yellow where sunlit, black cross-hatch in shadow
p.put(rock, WH)
p.put(rock & (tone < 0.30) & screen(0.45 + 0 * tone), Y)
p.put(rock & hatch(np.clip((tone - 0.30) * 1.5, 0, 0.9), 62, 4), K)
p.put(rock & hatch(np.clip((tone - 0.55) * 1.6, 0, 0.8), -28, 4), K)
p.put(rock & (tone > 0.5) & screen(0.25 + 0 * tone), R)        # warm bounce in the shade
# snow: paper, blue shadows
p.put(snow, WH)
p.put(snow & hatch(np.clip((tone - 0.36) * 2.0, 0, 0.85), 30, 3), B)
p.put(snow & (tone > 0.72), B)
# vegetation: meadow low, forest higher
p.put(veg, G)
meadow = veg & (alt < SEA + 0.06) & (slp < 0.3)
p.put(meadow & screen(0.3 - 0.2 * tone), Y)
p.put(veg & ~meadow & screen(np.clip(tone * 0.9 - 0.15, 0, 0.8)), K)
p.put(veg & (tone < 0.2) & screen(0.25 + 0 * tone), Y)
# water: blue, white glints, the sky's light toward the far shore
p.put(wat, B)
p.put(wat & hatch(np.clip(0.15 + (PIC_H - YY) / 500.0, 0, 0.6), 90, 3) & (fbm(9, scale=14, octaves=2, stretch=(0.2, 3)) > 0.45), WH)
# contours: every 1/26 of the relief, heavier every fifth
lev = np.floor(alt * 52)
cont = np.zeros((H, W), bool)
cont[1:, :] |= (lev[1:, :] != lev[:-1, :]) & land[1:, :] & land[:-1, :]
idx5 = np.zeros((H, W), bool)
idx5[1:, :] = (np.maximum(lev[1:, :], lev[:-1, :]) % 5 == 0)
p.put(cont & ~wat & (rock | snow) & idx5, K)
p.put(cont & snow & ~idx5, B)
p.put(cont & veg & idx5, K)
# silhouettes: where distance jumps, ink the ridge
jump = np.zeros((H, W), bool)
jump[1:, :] = (dist[:-1, :] - dist[1:, :] > 14) & land[1:, :]
jump[0:1, :] = False
p.put(jump, K)
top = land.copy(); top[1:, :] &= ~land[:-1, :]
p.put(top, K)
p.put(edge(wat) & land, K)
# far haze: knock back to paper and blue
p.put(land & ~jump & screen(haze) & (np.indices((H, W))[0] % 2 == 0), WH)
p.put(land & ~jump & screen(haze * 0.6) & (np.indices((H, W))[0] % 2 == 1), B)

# --- firs, far to near -------------------------------------------------------------
ys_, xs_ = np.nonzero(veg & ~meadow & (YY < PIC_H - 2))
pick = rng.choice(len(ys_), size=min(len(ys_), 2600), replace=False)
order = pick[np.argsort(ys_[pick])]
with p.draw() as d:
    for i in order:
        x, y = int(xs_[i]), int(ys_[i])
        s = float(np.clip(520.0 / dist[y, x], 2, 13))
        if s < 3 and rng.random() < 0.5:
            continue
        d.polygon([(x - s * 0.42, y), (x, y - s * 1.6), (x + s * 0.42, y)], fill=G, outline=K)
        d.polygon([(x - s * 0.42, y), (x, y - s * 1.6), (x, y)], fill=K)
        if s > 6:
            d.line([(x + 1, y - s * 0.9), (x + s * 0.3, y - s * 0.3)], fill=Y)
            d.line([(x, y), (x, y + 2)], fill=K)

# --- the cone that does not fit ------------------------------------------------------
col_top = np.where(land.any(0), land.argmax(0), H)
px0 = int(np.argmin(col_top[120:300]) + 120); py0 = int(col_top[px0])
base_y = py0 + 150
with p.draw() as d:
    for sgn in (-1, 1):
        x1 = px0 + sgn * 105
        for k in range(0, 40):
            if k % 2 == 0:
                a0, a1 = k / 40.0, (k + 1) / 40.0
                d.line([(px0 + (x1 - px0) * a0, py0 + (base_y - py0) * a0),
                        (px0 + (x1 - px0) * a1, py0 + (base_y - py0) * a1)], fill=R, width=2)
    for k in range(0, 44, 2):
        a0 = np.pi * k / 44.0; a1 = np.pi * (k + 1) / 44.0
        d.line([(px0 - 105 * np.cos(a0), base_y + 14 * np.sin(a0)), (px0 - 105 * np.cos(a1), base_y + 14 * np.sin(a1))], fill=R, width=2)
    d.line([(px0, py0 - 14), (px0, py0 - 3)], fill=R, width=1)
    d.polygon([(px0, py0 - 2), (px0 - 3, py0 - 8), (px0 + 3, py0 - 8)], fill=R)
    f = font(11)
    d.text((px0 + 8, py0 - 20), "D = 2.2", font=f, fill=K)
    # a hut by the tarn, smoke, and two walkers for scale
    cand = [(x_, y_) for y_ in range(560, 420, -4) for x_ in range(30, 330, 6)
            if (land & ~wat)[y_ - 2:y_ + 16, x_ - 4:x_ + 70].all()]
    hx, hy = cand[0] if cand else (78, 520)
    d.rectangle([hx, hy, hx + 22, hy + 13], fill=WH, outline=K)
    d.polygon([(hx - 3, hy), (hx + 11, hy - 11), (hx + 25, hy)], fill=R, outline=K)
    d.rectangle([hx + 9, hy + 5, hx + 13, hy + 13], fill=K); d.rectangle([hx + 3, hy + 3, hx + 6, hy + 6], fill=Y, outline=K)
    d.rectangle([hx + 17, hy - 12, hx + 20, hy - 5], fill=K)
    for k in range(9):
        d.ellipse([hx + 17 + k * 2 + (k % 3), hy - 18 - k * 6, hx + 22 + k * 3, hy - 13 - k * 6], outline=K, fill=WH)
    for wx, wy, c in ((hx + 46, hy + 8, R), (hx + 55, hy + 10, Y)):
        d.rectangle([wx, wy, wx + 3, wy + 7], fill=c, outline=K); d.ellipse([wx, wy - 4, wx + 3, wy - 1], fill=K)
        d.line([(wx + 5, wy - 2), (wx + 5, wy + 8)], fill=K)
    # a pair of choughs
    for bx, by in ((92, 118), (118, 96), (60, 140)):
        d.line([(bx - 6, by - 3), (bx, by), (bx + 6, by - 4)], fill=K, width=2)

p.caption("II", "MOUNTAINS ARE NOT CONES")
p.save()
