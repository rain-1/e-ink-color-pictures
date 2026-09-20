# Afternoon — "The Strait". A raymarched fjord: the channel Magellan threaded in
# October–November 1520, seen from the water. Two ranges of ridged rock either side,
# snow above the treeline, dark Nothofagus forest at the shore, mist with distance, and
# the whole thing reflected in the water. Printed as a screenprint: each material is
# screened between two palette inks with an 8x8 Bayer matrix (rock K/W, forest K/G,
# snow B/W, water K/B/W), so nothing speckles. Render with --dither none.
import os, math, numpy as np
from PIL import Image, ImageDraw, ImageFont
W, H = 400, 600

# ---------------- terrain ------------------------------------------------------------
def fbm(x, z, octaves=6, f0=0.55):
    v = np.zeros_like(x); amp = 1.0; f = f0
    for i in range(octaves):
        c, s = math.cos(0.7 * i + 0.4), math.sin(0.7 * i + 0.4)
        u = c * x - s * z; w = s * x + c * z
        v += amp * (np.sin(u * f + 1.7 * i) * np.cos(w * f * 0.83 + 0.9 * i) + 0.5 * np.sin((u + w) * f * 1.9 + i))
        amp *= 0.5; f *= 2.05
    return v
def centre(z):    return 3.4 * np.sin(0.085 * z + 0.15) + 0.7 * np.sin(0.21 * z + 2.0)
def halfwidth(z): return 2.4 + 0.7 * np.sin(0.19 * z + 1.1)
def height(x, z):
    d = np.abs(x - centre(z)) - halfwidth(z)
    dd = np.clip(d, 0, None)
    base = np.where(d < 0, -0.6, dd ** 1.15 * 1.35)
    ridged = (1.0 - np.abs(fbm(x * 0.7 + 3, z * 0.7 - 5, 5, 0.6)) * 0.55)      # sharp crests
    ridge = ridged ** 2 * 2.6 * np.clip(dd / 2.0, 0, 1)
    fine = fbm(x * 2.8 + 7, z * 2.8 + 3, 4, 1.0) * 0.28 * np.clip(dd, 0, 1)
    return np.minimum(base + np.where(d < 0, 0.0, ridge + fine), 9.5)

def march(o, d, steps=240, tmax=95.0):
    t = np.full(d.shape[:-1], 0.02); hit = np.zeros(d.shape[:-1], bool)
    for _ in range(steps):
        p = o + d * t[..., None]
        h = height(p[..., 0], p[..., 2])
        hit |= (p[..., 1] < h) & (t < tmax)
        dt = np.clip(0.4 * (p[..., 1] - h), 0.03, 0.9)
        t = np.where(hit, t, t + dt)
    p = o + d * t[..., None]
    return p, hit & (t < tmax), t

def normal(p, e=0.03):
    hx = height(p[..., 0] + e, p[..., 2]) - height(p[..., 0] - e, p[..., 2])
    hz = height(p[..., 0], p[..., 2] + e) - height(p[..., 0], p[..., 2] - e)
    n = np.stack([-hx, 2 * e * np.ones_like(hx), -hz], -1)
    return n / np.linalg.norm(n, axis=-1, keepdims=True)

LIGHT = np.array([-0.62, 0.40, 0.30]); LIGHT /= np.linalg.norm(LIGHT)
SKY, ROCK, SNOW, FOREST, WATER = 0, 1, 2, 3, 4

def shade(p, hit, t):
    """returns (material, tone 0..1, fog 0..1) for terrain hits"""
    n = normal(p)
    diff = np.clip((n * LIGHT).sum(-1), 0, 1)
    _, hs, _ = march(p + n * 0.08, np.broadcast_to(LIGHT, p.shape), steps=70, tmax=30.0)
    lit = np.where(hs, 0.0, 1.0)
    y = p[..., 1]; slope = n[..., 1]
    snow = (y > 5.2 + 0.7 * np.sin(p[..., 2] * 0.7 + p[..., 0])) & (slope > 0.42)
    forest = (y < 2.1 + 0.5 * np.sin(p[..., 0] * 1.3)) & (slope > 0.30)
    mat = np.where(snow, SNOW, np.where(forest, FOREST, ROCK))
    tone = 0.08 + 0.74 * diff * lit
    tone = np.where(snow, 0.35 + 0.65 * diff * lit, tone)
    fog = 1 - np.exp(-t * 0.019)
    return mat, tone, fog

# ---------------- camera ---------------------------------------------------------------
cam = np.array([float(centre(0.0)) - 0.6, 1.0, 0.0])
target = np.array([float(centre(24.0)) + 0.4, 4.6, 24.0])
fwd = target - cam; fwd /= np.linalg.norm(fwd)
right = np.cross(fwd, [0, 1, 0]); right /= np.linalg.norm(right); up = np.cross(right, fwd)
FOV = 0.95
def project(pt):
    q = np.asarray(pt, float) - cam
    zc = q @ fwd; xc = q @ right; yc = q @ up
    u = xc / zc / (FOV * W / H); v = yc / zc / FOV
    return ((u + 1) / 2 * W, (1 - v) / 2 * H, zc)
ys, xs = np.mgrid[0:H, 0:W]
u = (xs + 0.5) / W * 2 - 1; v = 1 - (ys + 0.5) / H * 2
d = fwd[None, None, :] + (u * (W / H) * FOV)[..., None] * right + (v * FOV)[..., None] * up
d /= np.linalg.norm(d, axis=-1, keepdims=True)

P, hit, t = march(cam[None, None, :], d)
mat = np.full((H, W), SKY); tone = np.ones((H, W)); fog = np.zeros((H, W))
m, tn, fg = shade(P, hit, t)
mat = np.where(hit, m, mat); tone = np.where(hit, tn, tone); fog = np.where(hit, fg, fog)

# water: the ray crosses y=0 inside the channel before it hits rock
down = d[..., 1] < -1e-4
dy = np.where(down, d[..., 1], -1.0)
tw = np.where(down, -cam[1] / dy, np.inf)
pw = cam[None, None, :] + d * np.where(down, tw, 0.0)[..., None]
inside = (np.abs(pw[..., 0] - centre(pw[..., 2])) - halfwidth(pw[..., 2])) < 0
water = down & (tw < t) & inside
rip = 0.014 * np.sin(pw[..., 2] * 8.0 + pw[..., 0] * 3.0) + 0.009 * np.sin(pw[..., 2] * 21.0 - pw[..., 0] * 5.0)
rd = d.copy(); rd[..., 1] = -rd[..., 1] + rip * 2; rd[..., 0] += rip
rd /= np.linalg.norm(rd, axis=-1, keepdims=True)
Pr, hitr, tr = march(pw + np.array([0, 0.02, 0]), rd, steps=200)
mr, tnr, fgr = shade(Pr, hitr, tr)
# brightness of what the water reflects: sky = 1, materials by tone, lifted by fog
refl_b = np.where(hitr, np.where(mr == SNOW, 0.55 + 0.45 * tnr, np.where(mr == FOREST, 0.05 + 0.25 * tnr, 0.05 + 0.5 * tnr)), 1.0)
refl_b = refl_b * (1 - fgr) + 1.0 * fgr
fres = 0.45 + 0.55 * (1 - np.clip(-d[..., 1] * 2.4, 0, 1)) ** 2
wtone = np.clip((refl_b * fres - 0.04) * 1.35, 0, 1)
fogw = 1 - np.exp(-tw * 0.019)
wtone = np.where(water, wtone * (1 - fogw) + fogw, 0)
mat = np.where(water, WATER, mat); tone = np.where(water, wtone, tone); fog = np.where(water, fogw, fog)

# ---------------- screenprint: two inks per material through an 8x8 Bayer screen -------
b8 = np.array([[0, 32, 8, 40, 2, 34, 10, 42], [48, 16, 56, 24, 50, 18, 58, 26], [12, 44, 4, 36, 14, 46, 6, 38],
               [60, 28, 52, 20, 62, 30, 54, 22], [3, 35, 11, 43, 1, 33, 9, 41], [51, 19, 59, 27, 49, 17, 57, 25],
               [15, 47, 7, 39, 13, 45, 5, 37], [63, 31, 55, 23, 61, 29, 53, 21]]) / 64.0 + 1 / 128
thr = np.tile(b8, (H // 8 + 1, W // 8 + 1))[:H, :W]
K, Wt, R, Y, B, G = (0, 0, 0), (255, 255, 255), (224, 27, 36), (245, 212, 0), (18, 61, 176), (30, 155, 60)
img = np.zeros((H, W, 3), np.uint8); img[:] = Wt
# terrain tone is lifted toward white by mist; far things dissolve
tone_f = tone * (1 - fog) + fog
def screen(mask, lo, hi, tv):
    on = mask & (tv >= thr)
    off = mask & (tv < thr)
    img[on] = hi; img[off] = lo
screen(mat == ROCK, K, Wt, tone_f)
screen(mat == FOREST, K, G, np.clip(tone_f * 1.15, 0, 1))
# forest dissolves to white in the mist too
screen((mat == FOREST) & (fog > 0.55), G, Wt, np.clip((fog - 0.55) / 0.45, 0, 1))
screen(mat == SNOW, B, Wt, np.clip(tone_f, 0, 1))
# water: three levels — black→blue on the dark half, blue→white on the light half
wl = (mat == WATER) & (tone < 0.5); wh = (mat == WATER) & (tone >= 0.5)
screen(wl, K, B, np.clip(tone * 2, 0, 1)); screen(wh, B, Wt, np.clip((tone - 0.5) * 2, 0, 1))
img[mat == SKY] = Wt
im = Image.fromarray(img, "RGB")

# ---------------- the naos, mid-channel, and their reflections ------------------------
dr = ImageDraw.Draw(im)
hull = [(-62, -36), (-40, -36), (-40, -23), (20, -21), (20, -31), (52, -31), (61, -19), (58, 0), (-58, 0), (-65, -12)]
def nao(sx, sy, s, flip=1):
    def T(x, y): return (sx + flip * x * s, sy + y * s)
    for k in range(1, 9):   # reflection first
        yy = sy + k * 4 * s * 2.2
        dr.line([(sx - 55 * s + k * 2, yy), (sx + 55 * s - k * 2, yy)], fill=K, width=max(1, int(2 * s * 2)))
    dr.polygon([T(*p) for p in hull], fill=K)
    for (mx, top) in [(28, -108), (-2, -142), (-42, -96)]:
        dr.line([T(mx, -22), T(mx, top)], fill=K, width=max(1, int(2.5 * s)))
    for (mx, yy, hw, foot) in [(-2, -96, 40, -44), (-2, -134, 22, -102), (28, -80, 28, -38), (28, -105, 14, -84)]:
        dr.polygon([T(mx - hw, yy), T(mx + hw, yy), T(mx + hw - 3, foot), T(mx - hw + 3, foot)], fill=Wt, outline=K)
        dr.line([T(mx - hw - 5, yy), T(mx + hw + 5, yy)], fill=K, width=max(1, int(2 * s)))
    dr.polygon([T(-70, -42), T(-16, -100), T(-30, -40)], fill=Wt, outline=K)
    dr.line([T(48, -31), T(96, -60)], fill=K, width=max(1, int(2 * s)))
    dr.polygon([T(-2, -142), T(-20, -140), T(-2, -136)], fill=R)
    for (mx, top) in [(28, -108), (-42, -96)]:
        dr.polygon([T(mx, top), T(mx - 12, top + 1), T(mx, top + 5)], fill=R)
ships = []
for zz, off, flip in [(9.0, -0.5, 1), (15.5, 0.9, 1), (22.0, -0.3, -1)]:
    x, y, zc = project((float(centre(zz)) + off, 0.0, zz))
    ships.append((x, y, 1.15 / zc * 3.2, flip))
for (x, y, s, flip) in sorted(ships, key=lambda q: -q[2]) [::-1]:
    nao(x, y, s, flip)
# a few birds over the water
for (gx, gy, gs) in [(150, 300, 5), (170, 292, 4), (188, 305, 3), (300, 250, 4)]:
    dr.arc([gx - gs, gy - gs, gx, gy + gs], 200, 340, fill=K, width=1)
    dr.arc([gx, gy - gs, gx + gs, gy + gs], 200, 340, fill=K, width=1)

# ---------------- plate line at the foot ----------------------------------------------
dr.rectangle([0, 566, W, H], fill=Wt)
dr.line([(0, 566), (W, 566)], fill=K, width=2)
try:
    f1 = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf", 12)
    f2 = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSerifItalic.ttf", 10)
except OSError:
    f1 = f2 = ImageFont.load_default()
dr.text((200, 572), "E S T R E C H O   D E   T O D O S   L O S   S A N T O S", fill=K, font=f1, anchor="mt")
dr.text((200, 587), "the strait · 21 October – 28 November 1520 · three ships of five", fill=K, font=f2, anchor="mt")
im.save(os.environ["OUT_RAW"])
