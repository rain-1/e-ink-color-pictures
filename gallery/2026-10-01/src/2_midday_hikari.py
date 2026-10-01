# Midday — "Hikari 1, Passing Fuji". A raymarched 3D scene: the 0-series bullet train on its
# concrete viaduct, tea terraces in front, Fuji filling the sky behind. Each surface is
# shaded, then screened through an 8x8 Bayer matrix between two or three palette inks of
# its own (sky blue→white, rock black→blue, tea black→green→yellow, body blue→white) so the
# render reads like a 1964 JNR poster rather than a dithered photo.
import os, sys, math, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ukiyo import W, H, K, Wh, R, Y, B, G, screen, font, traveller
from PIL import Image, ImageDraw
SC = int(os.environ.get("SCALE", "1"))
w, h = W // SC, H // SC

def noise(x, z, oct=4):
    v = np.zeros_like(x); a = 1.0; f = 1.0
    for i in range(oct):
        v += a * np.sin(x * f * 0.71 + 1.3 * i + np.sin(z * f * 0.53 + i)) * np.sin(z * f * 0.67 - 0.7 * i + np.sin(x * f * 0.41))
        a *= 0.5; f *= 2.1
    return v

# ---------- scene
FX, FZ = 260.0, 2400.0
def fuji_h(x, z):
    r = np.sqrt((x - FX) ** 2 + (z - FZ) ** 2)
    t = np.clip(1 - r / 1700, 0, 1)
    cone = 440 * t ** 1.9
    cone = np.minimum(cone, 405 + 5 * np.sin(np.arctan2(z - FZ, x - FX) * 9))  # flat crater rim
    return cone

def terrain(x, z):
    hills = np.where(z > 60, (3 + 30 * np.clip((z - 60) / 400, 0, 1)) * (0.6 + 0.4 * noise(x / 60, z / 60, 3)), 0)
    hills = np.maximum(hills, 0)
    tea = np.where(z < 60, 0.9 * np.abs(np.sin(z * 0.9 + 0.05 * x)) ** 0.5, 0)  # tea bush rows
    return np.maximum(fuji_h(x, z), hills + tea)

# track: straight line in xz from A heading along D (unit)
A = np.array([-160.0, 0, 20.0]); Dv = np.array([1.0, 0, 0.16]); Dv /= np.linalg.norm(Dv)
Nv = np.array([-Dv[2], 0, Dv[0]])
DECK = 9.0
def local(p):
    q = p - A
    u = q[..., 0] * Dv[0] + q[..., 2] * Dv[2]
    v = q[..., 0] * Nv[0] + q[..., 2] * Nv[2]
    return u, v, p[..., 1]

def sd_box(u, v, y, cu, cv, cy, hu, hv, hy):
    qx, qy, qz = np.abs(u - cu) - hu, np.abs(y - cy) - hy, np.abs(v - cv) - hv
    out = np.sqrt(np.maximum(qx, 0) ** 2 + np.maximum(qy, 0) ** 2 + np.maximum(qz, 0) ** 2)
    return out + np.minimum(np.maximum(qx, np.maximum(qy, qz)), 0)

NOSE_U = 166.0   # nose tip position along track
def sd_train(u, v, y):
    # body: rounded box behind the nose
    body = sd_box(u, v, y, NOSE_U - 9 - 60, 0, DECK + 2.3, 60, 1.6, 1.9) - 0.35
    # nose: ellipsoid-ish bullet
    nu = (u - (NOSE_U - 9)) / 9.0; nv = v / 1.95; ny = (y - (DECK + 2.0)) / 2.25
    nose = (np.sqrt(np.maximum(nu, 0) ** 2 + nv ** 2 + ny ** 2) - 1.0) * 1.9
    nose = np.maximum(nose, DECK + 0.4 - y)  # flat underside
    pan = sd_box(u, v, y, NOSE_U - 40, 0, DECK + 4.8, 0.8, 0.5, 0.6)  # pantograph
    return np.minimum(np.minimum(body, np.maximum(nose, u - NOSE_U - 1)), pan)

def sd_viaduct(u, v, y):
    deck = sd_box(u, v, y, 0, 0, DECK - 1.0, 400, 2.6, 1.0)
    parapet = sd_box(u, v, y, 0, 2.5, DECK + 0.3, 400, 0.15, 0.35)
    um = np.mod(u, 14.0) - 7.0
    pier = sd_box(um, v, y, 0, 0, (DECK - 2) / 2, 0.7, 1.6, (DECK - 2) / 2 + 0.2)
    beam = sd_box(um, v, y, 0, 0, DECK - 2.4, 0.9, 2.4, 0.5)
    # catenary masts on the far side every 28
    um2 = np.mod(u + 3, 28.0) - 14.0
    mast = sd_box(um2, v, y, 0, -2.6, DECK + 4, 0.18, 0.18, 4)
    arm = sd_box(um2, v, y, 0, -1.4, DECK + 7.4, 0.12, 1.3, 0.12)
    return np.minimum.reduce([deck, parapet, pier, beam, mast, arm])

def scene(p):
    u, v, y = local(p)
    dt = (p[..., 1] - terrain(p[..., 0], p[..., 2])) * 0.45
    dv = sd_viaduct(u, v, y)
    dtr = sd_train(u, v, y)
    wire = np.sqrt((y - DECK - 7.3) ** 2 + (v + 0.3) ** 2) - 0.05
    d = np.minimum.reduce([dt, dv, dtr])
    mat = np.select([d == dtr, d == dv, d == wire], [2, 1, 3], 0)
    return d, mat

# ---------- camera
cam = np.array([-10.0, 7.0, -58.0]); tgt = np.array([40.0, 120.0, 2400.0])
fwd = tgt - cam; fwd /= np.linalg.norm(fwd)
right = np.cross([0, 1, 0], fwd); right /= np.linalg.norm(right)
up = np.cross(fwd, right)
FOV = 0.30
jj, ii = np.mgrid[0:h, 0:w].astype(float)
sx = (ii + 0.5 - w / 2) / h * 2 * FOV; sy = -(jj + 0.5 - h / 2) / h * 2 * FOV
rd = fwd[None, None] + sx[..., None] * right + sy[..., None] * up
rd /= np.linalg.norm(rd, axis=-1, keepdims=True)
rd = rd.reshape(-1, 3); ro = np.broadcast_to(cam, rd.shape).copy()
t = np.full(len(rd), 0.1); hit = np.zeros(len(rd), bool); alive = np.ones(len(rd), bool)
TMAX = 6000
for step in range(600):
    idx = np.nonzero(alive)[0]
    if len(idx) == 0: break
    p = ro[idx] + rd[idx] * t[idx, None]
    d, _ = scene(p)
    hit[idx[d < 0.004 * t[idx]]] = True
    t[idx] += np.maximum(d, 0.002 * t[idx])
    alive[idx[(d < 0.004 * t[idx]) | (t[idx] > TMAX)]] = False
P = ro + rd * t[:, None]
_, mat = scene(P)
mat = np.where(hit, mat, -1)

def normal(p):
    e = 0.02 + 0.0008 * t[:, None] * 0
    n = np.zeros_like(p)
    for k in range(3):
        o = np.zeros(3); o[k] = 0.03
        n[:, k] = scene(p + o)[0] - scene(p - o)[0]
    return n / (np.linalg.norm(n, axis=1, keepdims=True) + 1e-9)
Nrm = normal(P)
SUN = np.array([-0.55, 0.62, -0.35]); SUN /= np.linalg.norm(SUN)
diff = np.clip((Nrm * SUN).sum(1), 0, 1)
# shadows: march toward sun, only for near stuff
sh = np.ones(len(P)); near = hit & (t < 500)
idx = np.nonzero(near)[0]; ts = np.full(len(idx), 0.3)
for step in range(80):
    q = P[idx] + Nrm[idx] * 0.05 + SUN * ts[:, None]
    d, _ = scene(q)
    sh[idx] = np.minimum(sh[idx], np.clip(8 * d / ts, 0, 1))
    ts += np.clip(d, 0.1, 6)
light = 0.18 + 0.82 * diff * sh

# ---------- per-material inks
tone = np.zeros(len(P)); ink = np.zeros(len(P), int)   # ink index into ramps
ramps = {0: [K, B, Wh], 1: [K, G, Wh], 2: [K, G, Y], 3: [K, Wh, Wh], 4: [K, B, B], 5: [B, Wh, Wh], 6: [K, Wh, Wh], 7: [B, B, Wh], 8: [K, K, K], 9: [K, R, Y]}
x, y, z = P[:, 0], P[:, 1], P[:, 2]
u, v, yy = local(P)
fh = fuji_h(x, z)
on_fuji = (mat == 0) & (fh > 45) & (y > 40) & (z > 700)
gully = np.sin(np.arctan2(z - FZ, x - FX) * 70 + noise(x / 30, z / 30, 2) * 2)
snowline = 255 + 30 * gully + 15 * noise(x / 25, z / 25, 3)
snow = on_fuji & (y > snowline)
rock = on_fuji & ~snow
fieldsN = (mat == 0) & ~on_fuji
sky = mat == -1
# sky: blue at top → white near horizon, with screen-printed cloud bands
dirY = rd[:, 1]
cl = noise(rd[:, 0] * 18, rd[:, 1] * 50, 3)
tone[sky] = np.clip(1.0 - (dirY[sky] - 0.13) * 4.2, 0, 1)
cloud = sky & (cl > 0.62) & (dirY > 0.17)
ink[sky] = 7; tone[cloud] = 1.0
ink[rock] = 0; tone[rock] = np.clip(0.05 + 0.5 * light[rock] + 0.1 * gully[rock], 0, .62)
ink[snow] = 5; tone[snow] = np.clip(0.25 + 0.9 * light[snow], 0, 1)
# fields: aerial perspective — far hills go blue, near go green/yellow
far = fieldsN & (z > 300)
rows = (np.sin(z * 0.9 + 0.05 * x) > -0.2)
ink[fieldsN] = 2; tone[fieldsN] = np.clip(0.3 + 0.55 * light[fieldsN] * rows[fieldsN] + 0.1 * rows[fieldsN], 0, 1)
ink[far] = 4; tone[far] = np.clip(0.3 + 0.6 * light[far], 0, 1)
# village roofs scattered in the middle distance
vill = fieldsN & (z > 90) & (z < 300) & (noise(x / 4, z / 4, 2) > 0.62)
ink[vill] = 8
via = mat == 1
ink[via] = 6; tone[via] = np.clip(0.1 + 0.95 * light[via], 0, 1)
tr = mat == 2
ink[tr] = 3; tone[tr] = np.clip(0.25 + 0.95 * light[tr], 0, 1)
band = tr & (yy > DECK + 1.9) & (yy < DECK + 3.0)
win = band & (np.mod(u, 2.4) < 1.5) & (u < NOSE_U - 12)
skirt = tr & (yy < DECK + 0.9)
ink[band | skirt] = 4; tone[band | skirt] = np.clip(0.35 + 0.8 * light[band | skirt], 0, 1)
ink[win] = 8
tip = tr & (u > NOSE_U - 1.6)
ink[tip] = 3; tone[tip] = 1.0
ink[mat == 3] = 8

# map tone → 3-stop ramp via Bayer
th = screen((h, w)).reshape(-1)
out = np.zeros((len(P), 3), np.uint8)
for k, ramp in ramps.items():
    m = ink == k
    if not m.any(): continue
    tt = np.clip(tone[m], 0, 1) * 2
    seg = np.minimum(tt.astype(int), 1); frac = tt - seg
    lo = np.array(ramp)[seg]; hi = np.array(ramp)[seg + 1]
    out[m] = np.where((frac > th[m])[:, None], hi, lo)
img = Image.fromarray(out.reshape(h, w, 3))
if SC > 1: img = img.resize((W, H), Image.NEAREST)
d = ImageDraw.Draw(img); d.fontmode = "1"
# tea pickers among the rows, kasa hats, baskets on their backs — drawn over the render
for (px, py, hh, robe) in ((60, 470, 46, B), (150, 498, 58, Wh), (300, 452, 38, R), (352, 522, 66, B)):
    traveller(d, px, py, hh, robe=robe, hat=Y, facing=-1 if px > 200 else 1)
    s_ = hh / 30
    d.polygon([(px - 6 * s_, py - 20 * s_), (px - 1 * s_, py - 20 * s_), (px - 2 * s_, py - 11 * s_), (px - 6 * s_, py - 12 * s_)], fill=Y, outline=K)
    for k in range(3): d.line((px - 6 * s_, py - (18 - 3 * k) * s_, px - 1.5 * s_, py - (18 - 3 * k) * s_), fill=K)
    d.chord((px - 16 * s_, py - 9 * s_, px + 16 * s_, py + 7 * s_), 180, 360, fill=G, outline=K)  # legs vanish into the tea bush
    for k in range(-6, 7, 2): d.line((px + k * 2 * s_, py - 6 * s_ + abs(k) * 0.6 * s_, px + k * 2 * s_ + s_, py - 4 * s_ + abs(k) * 0.6 * s_), fill=Y)
# poster lettering, 1964 JNR style
d.rectangle((0, 548, W, H), fill=R)
d.text((16, 553), "東海道新幹線", font=font(22, jp=True), fill=Wh)
d.text((16, 579), "HIKARI 1 · TOKYO 06:00 → SHIN-OSAKA 10:00", font=font(10, serif=False, bold=True), fill=Y)
d.text((302, 554), "1964", font=font(24, serif=False, bold=True), fill=Y)
d.text((310, 581), "10·1", font=font(12, serif=False, bold=True), fill=Wh)
img.save(os.environ.get("OUT_RAW", "/tmp/2.png"))
