"""Morning: a world landscape after Patinir — dawn, seen from a height."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from PIL import Image, ImageDraw
from ink import *

rng = np.random.default_rng(1524)
img = canvas('w')
x, y = grid()

def poly_mask(pts):
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).polygon([tuple(p) for p in pts], fill=255)
    return np.array(m) > 0

def draw_on(fn):
    m = Image.new('L', (W, H), 0); fn(ImageDraw.Draw(m)); return np.array(m) > 0

HZ = 150  # sea horizon
# --- sky: blue at top through white to yellow at the horizon
sky = y < HZ
t = np.clip(y / HZ, 0, 1)
mix(img, sky & (t < 0.45), 'b', 'w', np.clip(t / 0.45, 0, 1) ** 0.8)
mix(img, sky & (t >= 0.45), 'w', 'y', np.clip((t - 0.45) / 0.55, 0, 1) ** 1.3)
# streaks of cloud: thin red/blue bands lit from below
for i in range(9):
    cy = rng.uniform(30, HZ - 25); cx = rng.uniform(-40, W); ln = rng.uniform(60, 180)
    th = rng.uniform(1.5, 4)
    band = (np.abs(y - cy - 0.02 * (x - cx)) < th) & (x > cx) & (x < cx + ln)
    band &= vnoise((H, W), 12, rng, 2) > 0.42
    fill(img, band, 'r' if cy > HZ * 0.55 else 'b')
    fill(img, band & (np.abs(y - cy - th + 1 - 0.02 * (x - cx)) < 0.8), 'y' if cy > HZ*0.55 else 'w')
# sun, half risen, with rays
sx, sy = 120, HZ
r = np.hypot(x - sx, y - sy)
ang = np.arctan2(y - sy, x - sx)
rays = (np.sin(ang * 36) > 0.6) & (r > 26) & (r < 120) & (y < HZ) & (BAYER < np.clip(1 - (r - 26) / 94, 0, 1) * 0.8)
fill(img, rays, 'y')
fill(img, (r < 22) & (y < HZ), 'y')
fill(img, (np.abs(r - 23) < 1.2) & (y < HZ), 'r')

# --- far sea and plain
sea = (y >= HZ) & (y < 245)
mix(img, sea, 'w', 'b', np.clip((y - HZ) / 95, 0, 1) * 0.6 + 0.12)
# sun glitter column on the sea
gl = sea & (np.abs(x - sx) < 6 + (y - HZ) * 0.35) & ((y.astype(int) % 3) == 0) & (rng.random((H, W)) < 0.6)
fill(img, gl, 'y')

# distant blue mountains & islands
for (cx, w0, h0, base) in [(330, 90, 40, HZ + 4), (20, 70, 22, HZ + 6), (230, 50, 14, HZ + 10), (380, 60, 28, HZ + 18)]:
    prof = base - h0 * np.exp(-((x[0] - cx) / w0) ** 2 * 3) * (0.8 + 0.4 * noise1(W, 10, rng))
    m = (y < base) & (y >= prof[None, :]) & (np.abs(x - cx) < w0 * 1.3)
    mix(img, m, 'w', 'b', 0.55 + 0.25 * (y - prof[None, :]) / max(h0, 1))
    fill(img, m & (np.abs(y - prof[None, :]) < 1), 'b')
# tiny sails on the sea
for _ in range(14):
    bx, by = rng.uniform(160, 390), rng.uniform(HZ + 12, 238)
    s = 2 + (by - HZ) / 30
    img[int(by - s * 1.6):int(by), int(bx):int(bx + s)] = Wt
    img[int(by):int(by + 1 + s / 3), int(bx - s * .6):int(bx + s * 1.6)] = K

# --- middle land: green plain with a winding river to the sea
land = y >= 205
shore = 205 + 18 * noise1(W, 60, rng, 3) + 0.05 * (x[0] - 200)
landm = y >= shore[None, :]
lt = np.clip((y - 205) / 260, 0, 1)
nz = vnoise((H, W), 22, rng, 4)
mix(img, landm, 'b', 'g', np.clip(0.3 + lt * 0.9 + (nz - .5) * .6, 0, 1))
fields = np.zeros((H, W), bool)
# fields: patchwork of yellow and green parcels in the near plain
for _ in range(60):
    fx, fy = rng.uniform(0, 300), rng.uniform(270, 430)
    sc = 0.4 + (fy - 250) / 200
    fw, fh = rng.uniform(14, 34) * sc, rng.uniform(5, 10) * sc
    a = rng.uniform(-.25, .25)
    pts = [(fx, fy), (fx + fw, fy + fw * a), (fx + fw + 3, fy + fh + fw * a), (fx + 3, fy + fh)]
    m = poly_mask(pts) & landm
    fields |= m
    c = rng.choice(['y', 'y', 'g', 'w'])
    if c == 'y':
        mix(img, m, 'g', 'y', 0.75)
        fill(img, m & ((x + y * 2).astype(int) % 4 == 0), 'g')  # furrows
    elif c == 'w':
        mix(img, m, 'y', 'r', 0.25)
    else:
        fill(img, m & ((x - y).astype(int) % 3 == 0), 'k')
# river
tt = np.linspace(0, 1, 400)
rx = 150 + 70 * np.sin(tt * 7.5) * (1 - tt * 0.3) + 60 * tt
ry = 222 + tt * 360
rw = 3 + tt * 22
riv = np.zeros((H, W), bool)
for i in range(len(tt)):
    riv |= (np.abs(y - ry[i]) < 1.2) & (np.abs(x - rx[i]) < rw[i])
riv = draw_on(lambda d: [d.ellipse([rx[i] - rw[i], ry[i] - rw[i] * .35, rx[i] + rw[i], ry[i] + rw[i] * .35], fill=255) for i in range(len(tt))])
mix(img, riv, 'w', 'b', np.clip(0.35 + (y - 220) / 500, 0, 1))
edge = riv & ~np.roll(riv, 2, 0)
fill(img, edge, 'k')
fill(img, riv & (rng.random((H, W)) < 0.05) & (BAYER > .5), 'w')

# trees: thousands of small dark-green dabs, bigger toward the viewer
for _ in range(1100):
    tx, ty = rng.uniform(0, W), rng.uniform(220, 520)
    iy = int(min(ty, H - 1)); ix = int(tx)
    if not landm[iy, ix] or riv[iy, ix] or fields[iy, ix]:
        continue
    s = 1.3 + (ty - 210) / 85
    if rng.random() < 0.6 and ty < 470:  # clump in hedgerow lines
        ty = round(ty / (6 + s * 3)) * (6 + s * 3)
    d = (x - tx) ** 2 + ((y - ty) * 1.2) ** 2
    blob = d < s * s * 2.2
    fill(img, blob, 'g')
    fill(img, blob & (x > tx + s * .1) & (BAYER < .55), 'k')
    fill(img, (d < (s * .5) ** 2) & (x < tx) & (y < ty), 'y' if ty < 400 else 'g')

# villages: clustered houses with red roofs, a church spire each
def house(d_img, hx, hy, s, roof='r'):
    s = max(s, 2)
    wall = [hx, hy - s, hx + s * 1.4, hy]
    img[int(wall[1]):int(wall[3]), int(wall[0]):int(wall[2])] = Wt
    img[int(hy - s * .5):int(hy), int(hx + s * .25):int(hx + s * .25) + 1] = K  # door/window
    pts = [(hx - 1, hy - s), (hx + s * .7, hy - s * 1.8), (hx + s * 1.4 + 1, hy - s)]
    fill(img, poly_mask(pts), roof)
    img[int(hy):int(hy) + 1, int(hx):int(hx + s * 1.4)] = K

for (vx, vy, n) in [(60, 300, 14), (250, 262, 10), (300, 360, 9), (110, 420, 8), (205, 235, 7)]:
    sc = 1.5 + (vy - 230) / 45
    for _ in range(n):
        house(img, vx + rng.normal(0, 9 * sc / 2), vy + rng.normal(0, 3 * sc / 2), sc * rng.uniform(1.6, 2.4))
    # church
    cx_, cy_ = vx + 4, vy - 2
    s = sc * 2.4
    img[int(cy_ - s * 4):int(cy_), int(cx_):int(cx_ + s)] = Wt
    fill(img, poly_mask([(cx_ - 1, cy_ - s * 4), (cx_ + s / 2, cy_ - s * 7), (cx_ + s + 1, cy_ - s * 4)]), 'b')
    img[int(cy_ - s * 4):int(cy_), int(cx_ + s):int(cx_ + s) + 1] = K

# --- the great rocks: Patinir's pinnacles, right side
def pinnacle(cx, base, top, wid, seed):
    r2 = np.random.default_rng(seed)
    ys = np.linspace(top, base, 60)
    pr = (ys - top) / (base - top)
    lw = wid * (0.45 + 0.55 * pr ** 0.6) * (1 + 0.28 * np.sin(pr * r2.uniform(9, 14) + r2.uniform(0, 6)))
    sm = lambda a: np.convolve(np.pad(a, 3, mode='edge'), np.ones(7) / 7, 'valid')
    jag_l = sm((r2.random(60) - .5) * wid * .5) + (r2.random(60) - .5) * 3
    jag_r = sm((r2.random(60) - .5) * wid * .5) + (r2.random(60) - .5) * 3
    lean = 12 * np.sin((ys - top) / (base - top) * 2.4) * r2.choice([-1, 1])
    L = [(cx - lw[i] / 2 + jag_l[i] + lean[i], ys[i]) for i in range(60)]
    Rr = [(cx + lw[i] / 2 + jag_r[i] + lean[i], ys[i]) for i in range(60)][::-1]
    m = poly_mask(L + Rr)
    xc = np.interp(y, ys, cx + lean)
    rel = (x - xc) / (wid / 2)
    strata = (np.sin(y * 0.55 + 4 * vnoise((H, W), 9, r2, 2)) > 0.55)
    # lit side: white with pale blue screen; shadow side: blue into black
    lit = m & (rel < 0.15)
    mix(img, lit, 'w', 'b', np.clip(0.08 + (rel + 1) * 0.18 + strata * 0.25, 0, 1))
    sh = m & (rel >= 0.15)
    mix(img, sh, 'b', 'k', np.clip(0.3 + rel * 0.5 + strata * 0.2, 0, 1))
    fill(img, m & ~np.roll(m, 1, 1) | m & ~np.roll(m, -1, 1), 'k')
    fill(img, m & ~np.roll(m, 1, 0), 'k')
    # cracks
    for _ in range(int(wid / 3)):
        cy0 = r2.uniform(top + 10, base); cx0 = np.interp(cy0, ys, cx + lean) + r2.uniform(-wid / 3, wid / 3)
        ln = r2.uniform(6, 22)
        crack = (np.abs(x - cx0 - (y - cy0) * r2.uniform(-.3, .3)) < .7) & (y > cy0) & (y < cy0 + ln) & m
        fill(img, crack, 'k')
    # bushes clinging to ledges
    for _ in range(int(wid / 2)):
        by = r2.uniform(top + 15, base); bx = np.interp(by, ys, cx + lean) + r2.uniform(-wid / 2.5, wid / 2.5)
        bl = ((x - bx) ** 2 + (y - by) ** 2 * 2 < r2.uniform(3, 9)) & m
        fill(img, bl, 'g'); fill(img, bl & (y > by) , 'k')
    return m, xc

m1, _ = pinnacle(332, 470, 60, 70, 7)
m2, _ = pinnacle(272, 430, 130, 40, 11)
m3, _ = pinnacle(378, 500, 110, 50, 3)
# castle on the tallest rock
cx0, cy0 = 333, 64
for dx, hh in [(-14, 14), (-5, 22), (5, 16), (12, 10)]:
    img[cy0 - hh:cy0 + 2, cx0 + dx:cx0 + dx + 7] = Wt
    img[cy0 - hh:cy0 + 2, cx0 + dx + 5:cx0 + dx + 7] = B
    fill(img, poly_mask([(cx0 + dx - 1, cy0 - hh), (cx0 + dx + 3.5, cy0 - hh - 9), (cx0 + dx + 8, cy0 - hh)]), 'r')
    img[cy0 - hh + 4:cy0 - hh + 7, cx0 + dx + 2] = K
# a tiny flag
img[cy0 - 40:cy0 - 31, cx0 - 1] = K; img[cy0 - 40:cy0 - 36, cx0:cx0 + 5] = R

# --- foreground ledge: dark rock with a hermit in red at a cave mouth
fg = 500 + 25 * noise1(W, 40, rng, 3) - 0.18 * (x[0] - 40).clip(0) * (x[0] < 200)
fgm = y >= fg[None, :]
fgt = vnoise((H, W), 14, rng, 4)
mix(img, fgm, 'g', 'k', np.clip(0.35 + (fgt - .5) * 1.2 + (y - 520) / 150, 0, 1))
fill(img, fgm & ~np.roll(fgm, 2, 0), 'k')
# grass tufts along the edge
for gx in range(0, W, 3):
    gy = int(fg[gx]); hh = rng.integers(3, 10)
    for k in range(hh):
        xx = int(gx + k * rng.uniform(-.4, .4))
        if 0 <= xx < W and gy - k >= 0: img[gy - k, xx] = G if k > 2 else K
# cave mouth and hermit
cave = ((x - 80) / 34) ** 2 + ((y - 590) / 52) ** 2 < 1
fill(img, cave & fgm, 'k')
hx, hy = 112, 560
fill(img, poly_mask([(hx - 9, hy + 26), (hx - 5, hy - 4), (hx + 6, hy - 4), (hx + 12, hy + 26)]), 'r')
fill(img, poly_mask([(hx - 2, hy + 4), (hx + 5, hy + 2), (hx + 9, hy + 26), (hx + 4, hy + 26)]), 'k')
fill(img, (x - hx) ** 2 + (y - hy + 10) ** 2 < 25, 'w')  # head
fill(img, ((x - hx) ** 2 + (y - hy + 10) ** 2 < 25) & (y > hy - 9), 'y')  # beard/halo glow
fill(img, (np.abs(np.hypot(x - hx, y - hy + 11) - 8) < .9) & (y < hy - 9), 'y')  # halo
# open book on a rock
fill(img, poly_mask([(hx + 14, hy + 12), (hx + 24, hy + 9), (hx + 34, hy + 12), (hx + 24, hy + 15)]), 'w')
img[hy + 9:hy + 15, hx + 24] = K
# lion, small, lying by the cave
lx, ly = 160, 584
fill(img, ((x - lx) / 22) ** 2 + ((y - ly) / 8) ** 2 < 1, 'y')
fill(img, (np.abs(np.hypot(x - lx + 20, y - ly + 9) - 9) < 3), 'r')
fill(img, (x - lx + 20) ** 2 + (y - ly + 9) ** 2 < 49, 'y')
img[ly - 11, lx - 23] = K; img[ly - 11, lx - 18] = K
fill(img, (np.abs(y - ly + 4 + 6 * np.sin((x - lx - 22) / 5)) < 1.2) & (x > lx + 20) & (x < lx + 34), 'y')
img[ly + 4:ly + 7, lx - 12:lx + 12:6] = K

save(img)
