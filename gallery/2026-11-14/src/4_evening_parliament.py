"""Evening — Le Parlement, coucher de soleil. Monet's London fog set as a mosaic:
about nine thousand tesserae, laid in rings round the sun in the sky, in courses on the
stone, and in rippling rows on the Thames. Each tile is one pure ink; the fog is the mix."""
import math
import numpy as np
from PIL import Image, ImageDraw
from common import *

rng = np.random.default_rng(1904)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
HOR = 408
SUN = (292, 138)

# ---- the silhouette ----
def parliament(d):
    d.rectangle([0, 338, W, HOR], fill=255)                       # river front
    for x in range(4, W, 14):                                     # its picket of pinnacles
        d.polygon([(x - 3, 338), (x, 318 + 6 * math.sin(x)), (x + 3, 338)], fill=255)
    # Victoria Tower
    d.rectangle([78, 150, 148, HOR], fill=255)
    for x in (78, 101, 125, 148):
        d.rectangle([x - 5, 112, x + 5, 160], fill=255)
        d.polygon([(x - 6, 114), (x, 76), (x + 6, 114)], fill=255)
    d.line([113, 150, 113, 52], fill=255, width=3)                # flagstaff
    d.polygon([(114, 54), (134, 60), (114, 67)], fill=255)
    # central spire
    d.polygon([(212, 338), (220, 268), (226, 214), (232, 268), (240, 338)], fill=255)
    d.rectangle([214, 296, 238, 338], fill=255)
    # lesser turrets
    for x, top in ((176, 280), (268, 292), (300, 300), (40, 296), (14, 304)):
        d.rectangle([x - 5, top + 20, x + 5, 338], fill=255)
        d.polygon([(x - 6, top + 22), (x, top), (x + 6, top + 22)], fill=255)
    # the Clock Tower, far and small on the right
    d.rectangle([346, 236, 366, HOR], fill=255)
    d.polygon([(342, 240), (356, 180), (370, 240)], fill=255)
    d.rectangle([343, 226, 369, 242], fill=255)

bld = mask(parliament) > 0.5
sky = (yy < HOR) & ~bld
water = yy >= HOR
refl_b = np.zeros_like(bld)                                       # the building upside down in the river
k = min(H - HOR, HOR)
refl_b[HOR:HOR + k] = bld[HOR - k:HOR][::-1]
refl_soft = np.asarray(Image.fromarray((refl_b * 255).astype(np.uint8)).resize((W, H)), np.float32) / 255

# ---- the fog: weight fields (K, W, R, Y, B, G) ----
n1, n2 = fbm(80, 11), fbm(30, 12)
ds = np.hypot(xx - SUN[0], yy - SUN[1])
core = np.exp(-(ds / 50.0) ** 2)
halo = np.exp(-(ds / 150.0) ** 2)
far = 1 - halo
cloud = np.clip(np.sin(yy / 17.0 + xx / 90.0 + n1 * 6) * 0.6 + n2 - 0.62, 0, 1) * 2.0
def stack(k_, w_, r_, y_, b_, g_): return np.stack([k_, w_, r_, y_, b_, g_], -1)
z = np.zeros_like(xx)
F_sky = stack(z, 0.5 * core, 0.30 + 0.55 * (halo - core * 0.9) + 0.45 * far,
              0.10 + 1.2 * core + 0.50 * halo - 0.08 * far, 0.10 * far ** 2 + 0.9 * cloud * (0.25 + far), z)
edge = np.exp(-((xx - SUN[0]) / 130.0) ** 2)                      # fog burning through the right side
F_bld = stack(0.07 * (1 - edge), z, z, z, 1.0 + z, z)
t = np.clip((yy - HOR) / (H - HOR), 0, 1)
road = np.exp(-((xx - SUN[0] + 14 * t) / (16 + 46 * t + 10 * np.sin(yy / 6.0))) ** 2)
F_wat = stack(0.02 + 0.10 * t, 0.45 * road * (1 - t * .5),
              (0.50 - 0.15 * t) * (1 - refl_soft) + 0.25 * road, 0.16 * (1 - refl_soft) * (1 - t) + 0.75 * road,
              0.16 + 0.30 * t + 1.6 * refl_soft, 0.03 + 0.05 * t)

# ---- lay the tesserae ----
def seeds_sky():
    pts = [(SUN[0], SUN[1])]
    r = 7.0
    while r < 520:
        n = max(6, int(2 * math.pi * r / (6.8 + r / 90)))
        off = rng.uniform(0, 6.28)
        for i in range(n):
            a = off + i * 2 * math.pi / n
            pts.append((SUN[0] + r * math.cos(a) + rng.normal(0, .5), SUN[1] + r * math.sin(a) + rng.normal(0, .5)))
        r += 6.4 + r / 110
    return pts
def seeds_bld():
    pts = []
    for j, y in enumerate(np.arange(40, HOR + 4, 5.5)):
        for x in np.arange(-4 + (j % 2) * 3.2, W + 6, 6.4):
            pts.append((x + rng.normal(0, .35), y + rng.normal(0, .35)))
    return pts
def seeds_wat():
    pts = []
    y = HOR + 3.0; j = 0
    while y < H + 6:
        tt = (y - HOR) / (H - HOR)
        step = 7 + 9 * tt
        x = -10 + rng.uniform(0, step)
        while x < W + 10:
            pts.append((x, y + 1.8 * math.sin(x / (16 + 20 * tt) + j * 1.3) + rng.normal(0, .3)))
            x += step * rng.uniform(.8, 1.25)
        y += 5.2 + 3.2 * tt; j += 1
    return pts

out = np.zeros((H, W, 3), np.uint8)                               # grout is black
def lay(region, pts, field, grout=1.15, stretch=1.0):
    pts = np.array(pts, np.float32)
    ok = (pts[:, 0] > -12) & (pts[:, 0] < W + 12) & (pts[:, 1] > -12) & (pts[:, 1] < H + 12)
    pts = pts[ok]
    sx = np.clip(pts[:, 0].astype(int), 0, W - 1); sy = np.clip(pts[:, 1].astype(int), 0, H - 1)
    cols = np.array([pick(rng, field[y_, x_]) for x_, y_ in zip(sx, sy)], np.uint8)
    py, px = np.nonzero(region)
    for i in range(0, len(px), 3000):
        qx = px[i:i + 3000, None].astype(np.float32); qy = py[i:i + 3000, None].astype(np.float32)
        d2 = ((qx - pts[None, :, 0]) / stretch) ** 2 + (qy - pts[None, :, 1]) ** 2
        idx = np.argpartition(d2, 1, axis=1)[:, :2]
        da = np.sqrt(np.take_along_axis(d2, idx, 1))
        first = np.where(da[:, 0] <= da[:, 1], idx[:, 0], idx[:, 1])
        gap = np.abs(da[:, 0] - da[:, 1])
        c = cols[first]
        c[gap < grout] = (0, 0, 0)
        out[py[i:i + 3000], px[i:i + 3000]] = c

lay(sky, seeds_sky(), F_sky)
lay(bld, seeds_bld(), F_bld, grout=0.75)
lay(water, seeds_wat(), F_wat, grout=1.1, stretch=1.9)

img = Image.fromarray(out); d = ImageDraw.Draw(img)
# the sun itself: one round white stone in a yellow collar
d.ellipse([SUN[0] - 15, SUN[1] - 15, SUN[0] + 15, SUN[1] + 15], fill=K)
d.ellipse([SUN[0] - 13, SUN[1] - 13, SUN[0] + 13, SUN[1] + 13], fill=Y)
d.ellipse([SUN[0] - 8, SUN[1] - 8, SUN[0] + 8, SUN[1] + 8], fill=WH)
d.ellipse([350, 243, 362, 255], fill=K); d.ellipse([352, 245, 360, 253], fill=Y)   # the clock face
for gx, gy, s_ in ((60, 250, 1.2), (84, 268, .9), (188, 196, 1.1), (330, 90, 1.0), (24, 200, .8)):
    d.line([(gx - 6 * s_, gy - 3 * s_), (gx, gy), (gx + 6 * s_, gy - 4 * s_)], fill=K, width=2)
save(img)
