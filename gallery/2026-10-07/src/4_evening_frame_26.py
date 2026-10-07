"""4. Evening — Frame 26. The far side as it came down the wire: film, scan lines, grain,
annotated the way the 1959 atlas annotated it, phantom mountains and all."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from common import *

rng = np.random.default_rng(26)
ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
CX, CY, RR = 206, 238, 162
LAT0, LON0 = 8, 108
m = moon(LAT0, LON0, CX, CY, RR, n=3000)
mask, h, zc = m["mask"], m["h"], m["zc"]

# --- shading: sun 20 degrees off the camera axis, from the left; strong albedo
gy_, gx_ = np.gradient(h)
x = (xs - CX) / RR; y = -(ys - CY) / RR
nx, ny, nz = x - gx_ * 2.6, y + gy_ * 2.6, zc
nn = np.sqrt(nx * nx + ny * ny + nz * nz) + 1e-6
Ls = np.array([-0.62, 0.18, 0.76]); Ls /= np.linalg.norm(Ls)
lam = np.clip((nx * Ls[0] + ny * Ls[1] + nz * Ls[2]) / nn, 0, 1)
noise = np.zeros((H, W), np.float32)
for s, a in ((3, .5), (9, .3), (27, .2)):
    small = rng.normal(0, 1, (H // s + 2, W // s + 2)).astype(np.float32)
    noise += a * np.kron(small, np.ones((s, s)))[:H, :W]
alb = 0.78 + 0.07 * noise + m["alb"] + 0.35 * np.clip(m["ray"], 0, 1)
I = np.where(mask, np.clip(alb, 0.05, 1.2) * lam ** 1.1, 0)
# the 1959 look: contrasty, bloom at the limb, grain, scan lines, a dropout
I = np.clip((I - 0.08) * 1.25, 0, 1) ** 1.25
I += 0.10 * np.exp(-((np.hypot(xs - CX, ys - CY) - RR) / 5) ** 2)
I += rng.normal(0, 0.06, I.shape) * mask + rng.normal(0, 0.025, I.shape) * ~mask
I *= 1 - 0.18 * (ys.astype(int) % 3 == 0)
for yy in rng.integers(60, 440, 6):
    I[yy:yy + rng.integers(1, 3)] *= rng.uniform(0.2, 1.6)
drop = (ys > 344) & (ys < 352) & (xs > 250)
I[drop] = 0.0
# slight horizontal smear, like a slow phosphor
I = (I + np.roll(I, 1, 1) * 0.6 + np.roll(I, 2, 1) * 0.25) / 1.85
I = np.clip(I, 0, 1)

img = np.zeros((H, W, 3), np.uint8)
ax0, ay0, ax1, ay1 = 26, 30, 374, 448     # the frame's image area
rgb = (I[..., None] * 255).repeat(3, -1)
img[ay0:ay1, ax0:ax1] = fs_dither(rgb[ay0:ay1, ax0:ax1], ["K", "B", "W"])

L = Layer()
# film: rebate, sprockets, edge printing
L.rect(0, 0, W, ay0 - 2, "K"); L.rect(0, ay1 + 2, W, H, "K")
L.rect(0, 0, ax0 - 2, H, "K"); L.rect(ax1 + 2, 0, W, H, "K")
for yy in range(4, H, 16):
    L.rect(6, yy, 17, yy + 9, "W"); L.rect(W - 17, yy, W - 6, yy + 9, "W")
L.text((ax0, 15), "ЛУНА-3", "Y", 11, "monob", "lm")
L.text((ax1, 15), "КАДР 26 · 7.X.59 · 03:3x UT", "Y", 10, "monob", "rm")
# fiducial cross-hairs
for (fx, fy) in ((ax0 + 14, ay0 + 14), (ax1 - 14, ay0 + 14), (ax0 + 14, ay1 - 14), (ax1 - 14, ay1 - 14)):
    L.line([(fx - 7, fy), (fx + 7, fy)], "W", 1); L.line([(fx, fy - 7), (fx, fy + 7)], "W", 1)

# atlas overlay
V = sph(LAT0, LON0); E = np.array([-math.sin(math.radians(LON0)), math.cos(math.radians(LON0)), 0]); N = np.cross(V, E)
def proj(la, lo):
    p = sph(la, lo); return CX + RR * p @ E, CY - RR * p @ N, p @ V
# the boundary of the visible hemisphere: meridian 90 E, dashed red, as printed in 1959
seg = [proj(la, 90)[:2] for la in np.linspace(-88, 88, 90) if proj(la, 90)[2] > 0]
for i in range(0, len(seg) - 2, 4): L.line(seg[i:i + 3], "R", 1.6)
# equator, dotted
seg = [proj(0, lo)[:2] for lo in np.linspace(10, 200, 160) if proj(0, lo)[2] > 0]
for i in range(0, len(seg) - 1, 5): L.line(seg[i:i + 2], "Y", 1.0)
# the Soviet Mountains, a range that turned out to be a ray: a dashed yellow ridge
ridge = [proj(la, lo)[:2] for la, lo in zip(np.linspace(18, -22, 30), np.linspace(108, 124, 30))]
for i in range(0, len(ridge) - 2, 3): L.line(ridge[i:i + 2], "Y", 2.2)
feats = [("I", 27, 148), ("II", 24, 135), ("III", -21, 129), ("IV", 27, 98), ("V", 3, 114),
         ("VI", -2, 116), ("VII", -20, 147), ("VIII", 17, 59), ("IX", 13, 86)]
for i, (num, la, lo) in enumerate(feats):
    x, y, z = proj(la, lo)
    if z < 0.1: continue
    if num == "VI":
        bx, by = x - 34, y + 18
    elif num == "VIII":
        bx, by = x - 6, y - 26
    else:
        bx, by = x + 18, y - 16
    L.line([(x, y), (bx, by)], "Y", 0.9)
    L.ellipse(x, y, 2, 2, "R")
    L.ellipse(bx, by, 10, 7.5, "K", "Y", 1)
    L.text((bx, by + 0.5), num, "Y", 9, "sansb", "mm")
# legend on the film rebate below
names = ["Море Москвы", "Залив Астронавтов", "Циолковский", "Ломоносов", "Жолио-Кюри",
         "Хребет Советский", "Море Мечты", "Море Кризисов", "Море Краевое"]
L.text((ax0, ay1 + 18), "ОБРАТНАЯ СТОРОНА ЛУНЫ", "W", 12, "sansb", "lm")
L.text((ax1, ay1 + 18), "the far side", "R", 11, "sans", "rm")
for i, nm in enumerate(names):
    col, row = divmod(i, 5)
    x = ax0 + col * 176; yy = ay1 + 38 + row * 15
    L.text((x + 22, yy), feats[i][0], "Y", 10, "monob", "rm")
    L.text((x + 28, yy), nm, "R" if feats[i][0] == "VI" else "W", 10, "sans", "lm")
L.text((ax0 + 176 + 28, ay1 + 38 + 4 * 15), "VI: not a range — a ray", "Y", 10, "sans", "lm")
img = L.onto(img)
save(img)
