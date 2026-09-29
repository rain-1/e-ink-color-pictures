"""Evening — 'Canestra, after Caravaggio'. Michelangelo Merisi was born on Michaelmas 1571
and named for the archangel. A raymarched basket of fruit on a stone ledge in one hard
raking light, everything else falling to black. Floyd–Steinberg for the paint."""
import math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 400, 600
rng = np.random.default_rng(1571)

def norm(v):
    return v / np.linalg.norm(v, axis=-1, keepdims=True)

# ---------------- scene ----------------
grapes_b = []  # black grapes spilling over the left rim
for i in range(26):
    t = i / 25
    c = np.array([-0.95 - 0.55 * t, 1.0 - 0.95 * t, -0.25 - 0.35 * t])
    spread = 0.22 * (1 - 0.6 * t)
    grapes_b.append(c + rng.normal(0, 1, 3) * np.array([spread, 0.06, spread]))
grapes_w = []  # white grapes heaped at the top right
for i in range(22):
    t = i / 21
    c = np.array([0.35 + 0.75 * t, 1.55 - 0.7 * t, -0.35 - 0.15 * t])
    spread = 0.2 * (1 - 0.5 * t)
    grapes_w.append(c + rng.normal(0, 1, 3) * np.array([spread, 0.06, spread]))
GB = np.array(grapes_b); GW = np.array(grapes_w)
RG = 0.135

def rotm(ax, ay, az):
    cx, sx, cy, sy, cz, sz = math.cos(ax), math.sin(ax), math.cos(ay), math.sin(ay), math.cos(az), math.sin(az)
    Rx = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]])
    Ry = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])
    Rz = np.array([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]])
    return Rz @ Ry @ Rx

LEAVES = [  # centre, radii, rotation
    (np.array([1.15, 1.55, 0.35]), np.array([0.62, 0.03, 0.26]), rotm(0.3, 0.4, -0.5)),
    (np.array([-0.6, 1.45, 0.6]), np.array([0.55, 0.03, 0.24]), rotm(-0.2, -0.6, 0.7)),
    (np.array([0.2, 1.75, 0.7]), np.array([0.5, 0.03, 0.22]), rotm(0.9, 0.2, 0.2)),
    (np.array([-1.35, 0.95, 0.0]), np.array([0.5, 0.03, 0.22]), rotm(0.2, 0.9, 1.1)),
    (np.array([1.3, 0.75, -0.55]), np.array([0.45, 0.03, 0.2]), rotm(-0.5, -0.3, -1.2)),
]

def sd_sphere(p, c, r):
    return np.linalg.norm(p - c, axis=-1) - r

def sd_ellipsoid(p, c, rad, R):
    q = (p - c) @ R  # into leaf space
    k0 = np.linalg.norm(q / rad, axis=-1)
    k1 = np.linalg.norm(q / (rad * rad), axis=-1)
    return k0 * (k0 - 1.0) / np.maximum(k1, 1e-6)

def smin(a, b, k):
    h = np.clip(0.5 + 0.5 * (b - a) / k, 0, 1)
    return b * (1 - h) + a * h - k * h * (1 - h)

def sd_basket(p):
    x, y, z = p[..., 0], p[..., 1], p[..., 2] - 0.25
    r = np.sqrt(x * x + z * z)
    yy = np.clip(y, 0.02, 0.72)
    rad = 1.1 + 0.25 * (yy / 0.72)
    side = np.abs(r - rad) - 0.05
    slab = np.maximum(y - 0.72, 0.02 - y)
    wall = np.maximum(side, slab)
    base = np.maximum(r - 1.1, np.abs(y - 0.04) - 0.04)
    rim = np.sqrt((r - 1.35) ** 2 + (y - 0.74) ** 2) - 0.075
    return np.minimum(np.minimum(wall, base), rim)

def sd_ledge(p):
    q = np.abs(p - np.array([0, -0.6, 0.6])) - np.array([4.0, 0.6, 1.6])
    return np.linalg.norm(np.maximum(q, 0), axis=-1) + np.minimum(q.max(-1), 0)

OBJ = ["ledge", "basket", "apple", "pear", "fig", "peach", "gb", "gw", "leaf", "stem", "pomegranate"]

def scene(p, want_id=False):
    ds = []
    ds.append(sd_ledge(p))
    ds.append(sd_basket(p))
    ds.append(sd_sphere(p, np.array([-0.45, 1.0, 0.1]), 0.44))                     # apple
    pear = smin(sd_sphere(p, np.array([0.55, 1.05, 0.3]), 0.38), sd_sphere(p, np.array([0.72, 1.5, 0.32]), 0.22), 0.25)
    ds.append(pear)
    ds.append(sd_sphere(p, np.array([0.0, 0.88, -0.45]), 0.3))                     # fig
    ds.append(sd_sphere(p, np.array([-0.05, 1.28, 0.6]), 0.36))                    # peach
    dgb = np.full(p.shape[:-1], 1e9)
    for c in GB: dgb = np.minimum(dgb, sd_sphere(p, c, RG))
    ds.append(dgb)
    dgw = np.full(p.shape[:-1], 1e9)
    for c in GW: dgw = np.minimum(dgw, sd_sphere(p, c, RG * 1.05))
    ds.append(dgw)
    dl = np.full(p.shape[:-1], 1e9)
    for c, rad, R in LEAVES: dl = np.minimum(dl, sd_ellipsoid(p, c, rad, R))
    ds.append(dl)
    # apple stem and pear stem: short capsules
    def cap(p, a, b, r):
        pa, ba = p - a, b - a
        h = np.clip((pa @ ba) / (ba @ ba), 0, 1)
        return np.linalg.norm(pa - h[..., None] * ba, axis=-1) - r
    ds.append(np.minimum(cap(p, np.array([-0.45, 1.4, 0.1]), np.array([-0.38, 1.6, 0.05]), 0.025),
                         cap(p, np.array([0.72, 1.7, 0.32]), np.array([0.85, 1.9, 0.3]), 0.025)))
    ds.append(sd_sphere(p, np.array([-1.45, 0.3, -0.62]), 0.3))                      # pomegranate on ledge
    D = np.stack(ds, -1)
    if want_id:
        return D.min(-1), D.argmin(-1)
    return D.min(-1)

# ---------------- camera ----------------
ro = np.array([0.0, 1.45, -9.5])
ta = np.array([-0.1, 0.45, 0.0])
fw = norm(ta - ro); rt = norm(np.cross(np.array([0, 1, 0]), fw)); up = np.cross(fw, rt)
ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
u = (xs + 0.5 - W / 2) / H
v = -(ys + 0.5 - H / 2) / H
fov = 1.05
rd = norm(u[..., None] * rt * fov + v[..., None] * up * fov + fw * 1.9)
rd = rd.reshape(-1, 3)
N = rd.shape[0]

def march(ro_, rd_, tmax=20, steps=160):
    t = np.zeros(rd_.shape[0]); hit = np.zeros(rd_.shape[0], bool)
    active = np.arange(rd_.shape[0])
    for _ in range(steps):
        if active.size == 0: break
        p = ro_[active] + rd_[active] * t[active, None] if ro_.ndim == 2 else ro_ + rd_[active] * t[active, None]
        d = scene(p)
        t[active] += d * 0.9
        done = d < 0.0015
        hit[active[done]] = True
        far = t[active] > tmax
        active = active[~done & ~far]
    return t, hit

t, hit = march(ro, rd)
P = ro + rd * t[:, None]
Ph = P[hit]
_, ids = scene(Ph, True)
e = 0.0015
nrm = np.stack([scene(Ph + np.array([e, 0, 0])) - scene(Ph - np.array([e, 0, 0])),
                scene(Ph + np.array([0, e, 0])) - scene(Ph - np.array([0, e, 0])),
                scene(Ph + np.array([0, 0, e])) - scene(Ph - np.array([0, 0, e]))], -1)
nrm = norm(nrm)

# ---------------- lighting ----------------
L = norm(np.array([-0.8, 0.55, -0.85]))
# soft shadow
sro = Ph + nrm * 0.01
st = np.full(Ph.shape[0], 0.02); sh = np.ones(Ph.shape[0])
act = np.arange(Ph.shape[0])
for _ in range(90):
    if act.size == 0: break
    d = scene(sro[act] + L * st[act, None])
    sh[act] = np.minimum(sh[act], 10 * d / st[act])
    st[act] += np.clip(d, 0.01, 0.3)
    keep = (d > 0.001) & (st[act] < 8)
    sh[act[~keep & (d <= 0.001)]] = 0
    act = act[keep]
sh = np.clip(sh, 0, 1)

# albedo per material
alb = np.zeros_like(Ph)
spec = np.zeros(Ph.shape[0]); shin = np.full(Ph.shape[0], 20.0)
x, y, z = Ph[:, 0], Ph[:, 1], Ph[:, 2]
def put(mask, col, s=0.0, sh_=20):
    alb[mask] = col if np.ndim(col) == 1 else col[mask]
    spec[mask] = s; shin[mask] = sh_
m = ids == 0  # ledge: warm ochre stone, faint grain
grain = 0.85 + 0.15 * np.sin(x * 9 + np.sin(z * 3) * 2)
put(m, (np.array([0.5, 0.35, 0.13])[None] * grain[:, None]))
alb[(ids == 0) & (nrm[:, 2] < -0.9)] *= 0.4  # ledge front falls into shadow
m = ids == 1  # basket weave
ang = np.arctan2(z - 0.25, x)
weave = np.sign(np.sin(ang * 22)) * np.sign(np.sin(y * 36))
straw = 0.7 + 0.3 * weave
rimband = (y > 0.66)
col = np.array([0.85, 0.62, 0.25])[None] * straw[:, None]
col[rimband] = np.array([0.7, 0.48, 0.2]) * (0.8 + 0.2 * np.sin(ang[rimband] * 60))[:, None]
put(m, col, 0.1, 8)
m = ids == 2  # apple: red with yellow streaks
streak = 0.5 + 0.5 * np.sin(np.arctan2(z - 0.1, x + 0.45) * 14 + y * 3)
col = np.array([0.85, 0.08, 0.06])[None] * (1 - 0.35 * streak[:, None]) + np.array([0.9, 0.75, 0.0])[None] * 0.35 * streak[:, None]
put(m, col, 0.6, 50)
m = ids == 3; put(m, np.array([0.78, 0.8, 0.12]), 0.35, 30)   # pear
m = ids == 4; put(m, np.array([0.12, 0.1, 0.35]), 0.3, 25)    # fig
m = ids == 5  # peach: yellow to red blush
blush = np.clip((-x + 0.2) * 1.5, 0, 1)
col = np.array([0.95, 0.72, 0.1])[None] * (1 - blush[:, None]) + np.array([0.9, 0.2, 0.08])[None] * blush[:, None]
put(m, col, 0.15, 10)
m = ids == 6; put(m, np.array([0.06, 0.06, 0.18]), 1.0, 60)   # black grapes
m = ids == 7; put(m, np.array([0.7, 0.85, 0.45]), 0.9, 60)    # white grapes
m = ids == 8  # leaves: green with yellowing and dark blight spots
spots = (np.sin(x * 23) * np.sin(y * 19) * np.sin(z * 29)) > 0.55
col = np.tile(np.array([0.15, 0.55, 0.18]), (Ph.shape[0], 1))
yel = np.sin(x * 4 + y * 2) > 0.4
col[yel] = [0.6, 0.62, 0.1]
col[spots] = [0.25, 0.12, 0.05]
put(m, col, 0.25, 15)
m = ids == 9; put(m, np.array([0.3, 0.18, 0.05]))
m = ids == 10; put(m, np.array([0.8, 0.1, 0.1]), 0.4, 30)     # pomegranate

diff = np.clip((nrm * L).sum(-1), 0, 1)
hv = norm(L - rd[hit])
sp = np.clip((nrm * hv).sum(-1), 0, 1) ** shin * spec
amb = 0.06 + 0.04 * np.clip(nrm[:, 1], 0, 1)
# light falloff across the scene: brightest upper-left, the right side sinks into shade
fall = np.clip(1.25 - 0.35 * (x + 0.8) - 0.15 * np.abs(z), 0.25, 1.2)
col = alb * (amb[:, None] + 1.25 * diff[:, None] * sh[:, None] * fall[:, None]) + sp[:, None] * sh[:, None] * 1.2
# gentle vignette into the black background
img = np.zeros((N, 3))
img[hit] = col
img = img.reshape(H, W, 3)
vig = np.clip(1.25 - 0.9 * np.sqrt(((xs - 150) / 400) ** 2 + ((ys - 250) / 520) ** 2), 0, 1)
img *= vig[..., None]
# crush darks so the background and deep shadows stay pure black (no FS speckle)
lum = img.mean(-1, keepdims=True)
img = np.where(lum < 0.07, 0, img)
img = np.clip(img, 0, 1) ** 0.9

# ledge front: find the band of lit front-face pixels for the inscription
front = (np.abs(nrm[:, 2] + 1) < 0.05) & (ids == 0)
rows = np.nonzero(hit)[0][front] // W
TXT_Y = int(np.median(rows)) if rows.size else 560
out = Image.fromarray((img * 255).astype(np.uint8), "RGB")
# carved inscription on the ledge front, like a painter's signature
d = ImageDraw.Draw(out)
f = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf", 17)
d.text((200, TXT_Y + 1), "MICHAEL ANGELVS · MDLXXI", fill=(0, 0, 0), font=f, anchor="mm")
d.text((200, TXT_Y), "MICHAEL ANGELVS · MDLXXI", fill=(215, 170, 40), font=f, anchor="mm")
# a fly on the ledge — memento mori
top = (nrm[:, 1] > 0.95) & (ids == 0)
trows = np.nonzero(hit)[0][top]
tr = trows[(trows % W > 280) & (trows % W < 330)] // W
fx, fy = 305, (int(np.median(tr)) if tr.size else TXT_Y - 80)
d.ellipse([fx - 4, fy - 2, fx + 4, fy + 2], fill=(0, 0, 0))
d.ellipse([fx + 3, fy - 2, fx + 7, fy + 2], fill=(0, 0, 0))
d.ellipse([fx - 7, fy - 6, fx + 1, fy - 1], fill=(200, 200, 210))
d.ellipse([fx - 7, fy + 1, fx + 1, fy + 6], fill=(200, 200, 210))
for k in (-3, 0, 3):
    d.line([fx + k, fy + 2, fx + k - 2, fy + 6], fill=(0, 0, 0))
out.save(os.environ.get("OUT_RAW", "out.png"))
