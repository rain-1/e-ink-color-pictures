"""Behold, the sea itself — a rendered ocean at sunset. Analytic wave normals on a plane
(16 directional sines, damped with distance), Fresnel reflection of a banded sunset sky,
specular sun road. Every pixel's tone runs along one ramp K-B-R-Y-W and is screened with
an 8x8 Bayer matrix, so the panel sees only clean pairs. Three ships on the horizon."""
import math, os
import numpy as np
from PIL import Image, ImageDraw
from common import K, Wt, R, Y, B, G, bayer

W, H = 400, 600
rng = np.random.default_rng(1012)
HZ = 250.0                 # horizon row
f = 520.0                  # focal length (px)
cam_h = 2.2
sun_az, sun_el = -0.10, 0.045   # radians: a little left of centre, just above the horizon

yy, xx = np.mgrid[0:H, 0:W].astype(np.float64)
dx = (xx - W / 2) / f
dy = -(yy - HZ) / f        # +up
dz = np.ones_like(dx)
n = np.sqrt(dx * dx + dy * dy + 1)
dx, dy, dz = dx / n, dy / n, dz / n

def noise1(x, seed, octaves=4):
    out = np.zeros_like(x)
    r = np.random.default_rng(seed)
    for o in range(octaves):
        fr = 2 ** o
        ph, ph2 = r.uniform(0, 6.28, 2)
        out += (np.sin(x * fr * 1.7 + ph) + 0.5 * np.sin(x * fr * 3.1 + ph2)) / fr
    return out

def sky(ddx, ddy, ddz):
    el = np.arcsin(np.clip(ddy, -1, 1))
    az = np.arctan2(ddx, ddz)
    # base: zenith blue (0.25) -> red (0.5) -> yellow (0.75) at the horizon
    e = np.clip(el / 0.42, 0, 1)
    t = 0.78 - 0.55 * e ** 0.7
    # sun glow
    ang = np.sqrt((az - sun_az) ** 2 + (el - sun_el) ** 2)
    t = t + 0.30 * np.exp(-ang / 0.10) + 0.1 * np.exp(-ang / 0.35)
    t = np.where(ang < 0.032, 1.0, t)
    # cloud bands: long thin streaks, dark undersides, lit rims near the sun
    for i, (c_el, thick, dark) in enumerate([(0.06, 0.010, 0.0), (0.105, 0.016, 0.06), (0.17, 0.022, 0.18), (0.27, 0.03, 0.22), (0.36, 0.02, 0.24)]):
        edge = c_el + thick * noise1(az * (2 + i), 7 + i) * 0.3 + 0.004 * np.sin(az * 9 + i)
        band = np.abs(el - edge) < thick * (0.6 + 0.4 * np.sin(az * (5 + i * 2) + i) ** 2)
        cover = band & (np.sin(az * (2.3 + i) + i * 1.3) > -0.35)
        lit = cover & (el < edge - thick * 0.25)
        t = np.where(cover, dark + 0.08 * np.exp(-ang / 0.3), t)
        t = np.where(lit & (ang < 0.9), np.minimum(0.86, t + 0.55 * np.exp(-ang / 0.45)), t)
    return np.clip(t, 0, 1)

tone = np.zeros((H, W))
skym = dy >= -1e-4
tone[skym] = sky(dx[skym], np.maximum(dy[skym], 0), dz[skym])

# ---- sea
sea = ~skym
tt = cam_h / -dy[sea]
px, pz = dx[sea] * tt, dz[sea] * tt
dist = tt
gx = np.zeros_like(px); gz = np.zeros_like(px)
for i in range(18):
    a = rng.normal(0, 0.55) + (0.15 if i % 2 else -0.2)
    k = 0.35 * 1.32 ** i
    A = 0.11 / k ** 1.05
    ph = rng.uniform(0, 6.28)
    kx, kz = k * math.sin(a), k * math.cos(a)
    damp = np.exp(-dist * k / 180)
    c = np.cos(kx * px + kz * pz + ph) * A * k * damp
    gx += c * kx / k; gz += c * kz / k
nx, ny, nz = -gx, np.ones_like(gx), -gz
nn = np.sqrt(nx * nx + ny * ny + nz * nz); nx, ny, nz = nx / nn, ny / nn, nz / nn
vx, vy, vz = dx[sea], dy[sea], dz[sea]
dn = vx * nx + vy * ny + vz * nz
rx, ry, rz = vx - 2 * dn * nx, vy - 2 * dn * ny, vz - 2 * dn * nz
ry = np.abs(ry) + 1e-3
fres = 0.04 + 0.96 * (1 - np.clip(-dn, 0, 1)) ** 5
fres = np.clip(fres * 1.35, 0, 1)
refl = sky(rx, ry, rz)
slope = np.clip(0.5 + 2.2 * (nz * 0.8 - nx * 0.3), 0, 1)
body = 0.03 + 0.24 * slope * np.exp(-dist / 60)
tsea = fres * refl * 0.95 + (1 - fres) * body
# sun glitter
sdx, sdy, sdz = math.sin(sun_az) * math.cos(sun_el), math.sin(sun_el), math.cos(sun_az) * math.cos(sun_el)
spec = np.clip(rx * sdx + ry * sdy + rz * sdz, 0, 1) ** 900
tsea = np.clip(tsea + spec * 3.0, 0, 1)
tone[sea] = tsea

# ---- ramp-dither: K -> B -> R -> Y -> W
ramp = [K, B, R, Y, Wt]
nseg = len(ramp) - 1
v = np.clip(tone, 0, 0.9999) * nseg
i0 = np.floor(v).astype(int); fr = v - i0
th = np.tile(bayer(8), (H // 8 + 1, W // 8 + 1))[:H, :W]
idx = np.where(fr > th, i0 + 1, i0)
img = np.array(ramp, dtype=np.uint8)[idx]
out = Image.fromarray(img)
d = ImageDraw.Draw(out)

# ---- ships on the horizon (silhouettes) with broken reflections
def ship(x, s, lateen=False):
    base = HZ + 1
    d.polygon([(x - 18 * s, base - 5 * s), (x + 20 * s, base - 6 * s), (x + 14 * s, base + 1), (x - 14 * s, base + 1)], fill=K)
    d.polygon([(x - 18 * s, base - 5 * s), (x - 19 * s, base - 11 * s), (x - 9 * s, base - 10 * s), (x - 9 * s, base - 5 * s)], fill=K)
    for mx, mh, sw in [(-11, 30, 0), (2, 42, 12), (13, 32, 9)]:
        X = x + mx * s
        d.line([(X, base - 5 * s), (X, base - mh * s)], fill=K, width=max(1, round(s)))
        if sw:
            d.polygon([(X - sw * s, base - (mh - 4) * s), (X + sw * s, base - (mh - 4) * s), (X + (sw + 1) * s, base - 12 * s), (X - (sw - 2) * s, base - 12 * s)], fill=K)
            d.polygon([(X - sw * 0.7 * s, base - (mh - 1) * s), (X + sw * 0.7 * s, base - (mh - 1) * s), (X + sw * 0.75 * s, base - (mh - 5) * s), (X - sw * 0.6 * s, base - (mh - 5) * s)], fill=K)
    X = x - 11 * s
    d.polygon([(X - 9 * s, base - 8 * s), (X + 1, base - 30 * s), (X + 2, base - 8 * s)], fill=K)
    d.line([(x + 20 * s, base - 6 * s), (x + 32 * s, base - 14 * s)], fill=K, width=max(1, round(s * 0.8)))
    for k in range(int(10 * s)):
        y = base + 2 + k * 2
        w = (18 - k * 0.6 / s) * s
        jit = rng.uniform(-3, 3)
        if w > 2:
            d.line([(x - w + jit, y), (x + w * 0.6 + jit, y)], fill=K, width=1)
ship(262, 1.25)   # Santa María
ship(318, 0.85)   # Pinta
ship(352, 0.7)    # Niña
# birds
for bx, by, s in [(120, 150, 5), (134, 160, 4), (108, 166, 4), (150, 140, 3)]:
    d.line([(bx - s, by - s * 0.3), (bx - s * 0.4, by - s * 0.7), (bx, by), (bx + s * 0.4, by - s * 0.7), (bx + s, by - s * 0.3)], fill=K, width=1)
out.save(os.environ.get("OUT_RAW", "out.png"))
