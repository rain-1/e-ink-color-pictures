"""Morning — Impression, soleil levant. Le Havre, 1872, repainted as ~25,000 short
strokes of the six pure inks laid side by side: the panel's limit is Monet's method."""
import math
import numpy as np
from PIL import Image, ImageDraw
from common import *

rng = np.random.default_rng(18401114)
HOR = 232
SUN = (262, 158)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)

# ---- harbour ghosts: masts, cranes, chimneys, smoke (a soft mask of "more blue") ----
def harbour(d):
    # left: tall ships
    for x0, top, hull in [(18, 96, 30), (52, 70, 38), (92, 104, 28), (128, 122, 22)]:
        d.rectangle([x0 - hull // 2, HOR - 9, x0 + hull // 2, HOR], fill=200)
        for k, dx in enumerate((-hull // 4, hull // 5)):
            t = top + k * 16
            d.line([x0 + dx, t, x0 + dx, HOR - 6], fill=230, width=2)
            for j in range(3):
                yj = t + 14 + j * 22
                if yj < HOR - 14:
                    d.line([x0 + dx - 9 + j, yj, x0 + dx + 9 - j, yj], fill=170, width=1)
            d.line([x0 + dx, t, x0 + dx + 16, HOR - 8], fill=90, width=1)
            d.line([x0 + dx, t, x0 + dx - 14, HOR - 8], fill=90, width=1)
    # centre: quay, sheds
    d.rectangle([150, HOR - 6, 236, HOR], fill=150)
    for x0 in range(156, 232, 13):
        d.polygon([(x0, HOR - 6), (x0 + 6, HOR - 13), (x0 + 12, HOR - 6)], fill=140)
    # right: cranes and chimneys
    for x0, top in [(300, 120), (334, 100), (372, 132)]:
        d.line([x0, top, x0, HOR], fill=220, width=3)
        d.line([x0, top, x0 - 30, top + 22], fill=200, width=2)
        d.line([x0 - 30, top + 22, x0 - 30, top + 52], fill=120, width=1)
        d.line([x0, top + 26, x0 - 14, top + 12], fill=160, width=1)
        d.rectangle([x0 - 7, HOR - 16, x0 + 9, HOR], fill=190)
    for x0, top in [(282, 150), (352, 140), (390, 118)]:
        d.rectangle([x0 - 2, top, x0 + 2, HOR], fill=210)
    d.rectangle([270, HOR - 5, 400, HOR], fill=170)

ghost = mask(harbour, blur=1.6)
def smoke(d):
    for x0, top in [(282, 150), (352, 140), (390, 118)]:
        for i in range(26):
            t = i / 25
            d.ellipse([x0 - 40 * t - 6 - 9 * t, top - 70 * t - 6 - 8 * t,
                       x0 - 40 * t + 6 + 9 * t, top - 70 * t + 6 + 8 * t], fill=int(150 * (1 - t)))
smk = mask(smoke, blur=5)
# reflections of the ghosts in the water, smeared
refl = np.zeros_like(ghost)
span = 90
refl[HOR:HOR + span] = ghost[HOR - span:HOR][::-1] * np.linspace(0.7, 0.0, span)[:, None]

# ---- weight fields (K, W, R, Y, B, G) ----
n1, n2, n3 = fbm(90, 1), fbm(34, 2), fbm(12, 3)
dsun = np.hypot(xx - SUN[0], (yy - SUN[1]) * 1.15)
glow = np.exp(-(dsun / 78.0) ** 2)
streak = np.clip(np.sin(yy / 13.0 + n1 * 7 + xx / 140.0) * 0.5 + n2 - 0.55, 0, 1) * 2.2
sky = yy < HOR
depth = np.clip((yy - HOR) / (H - HOR), 0, 1)

wB = np.where(sky, 0.14 + 0.22 * n1 + 0.34 * (yy / HOR) ** 3, 0.74 + 0.16 * n2 + 0.06 * depth)
wB = wB + 0.5 * ghost + 0.28 * smk + 0.45 * refl
wR = np.where(sky, 0.22 * glow + 0.20 * streak * (0.5 + glow), 0.03 * glow)
wY = np.where(sky, 0.34 * glow + 0.30 * streak * (0.6 + glow), 0.02 * n3)
wB = wB * (1 - 0.45 * glow * sky)
wG = np.where(sky, 0.03 * n2, 0.10 * n3 + 0.10 * depth)
wK = np.where(sky, 0.10 * ghost, 0.02 + 0.10 * depth * n2 + 0.12 * refl)
wW = np.clip(1.0 - wB - wR - wY - wG - wK, 0.04, 1)
FIELD = np.stack([wK, wW, wR, wY, wB, wG], -1)

img = Image.new("RGB", (W, H), WH)
d = ImageDraw.Draw(img)

def stroke(x, y, ln, wd, ang, col):
    dx, dy = math.cos(ang) * ln / 2, math.sin(ang) * ln / 2
    d.line([x - dx, y - dy, x + dx, y + dy], fill=col, width=wd)

def layer(n, lmin, lmax, wd):
    xs = rng.integers(0, W, n); ys = rng.integers(0, H, n)
    for x, y in zip(xs, ys):
        if y < HOR:
            ang = -0.18 + (n2[y, x] - 0.5) * 1.3 + rng.normal(0, 0.15)
            ln = rng.uniform(lmin, lmax) * 0.8
        else:
            ang = rng.normal(0, 0.05)
            ln = rng.uniform(lmin, lmax) * (0.7 + 0.9 * depth[y, x])
        stroke(x, y, ln, wd, ang, pick(rng, FIELD[y, x]))

layer(5200, 14, 24, 4)
layer(8000, 8, 16, 2)
layer(2500, 4, 9, 1)

# ---- the harbour itself, drawn into the wet paint: blue on blue-white ----
sharp = mask(harbour)
a = np.asarray(img).copy()
sel = (sharp > 0.3) & (BAYER < 0.35 + sharp * 0.75)
a[sel] = B
sel2 = (smk > 0.18) & (BAYER < smk * 1.5) & (yy < HOR)
a[sel2] = B
img = Image.fromarray(a); d = ImageDraw.Draw(img)
for _ in range(700):          # their reflections: short blue verticals dropped in the water
    x = int(rng.integers(0, W)); k = int(rng.integers(4, 80))
    if sharp[HOR - k, x] > 0.4 and rng.random() < 1 - k / 90:
        d.line([x, HOR + k, x + rng.integers(4, 12), HOR + k], fill=B if rng.random() < .8 else K, width=2)
d.line([0, HOR, W, HOR], fill=B, width=1)

# ---- the sun, and its broken road across the water ----
for i in range(50):
    a = rng.uniform(0, 2 * math.pi); r = rng.uniform(12, 19)
    stroke(SUN[0] + r * math.cos(a), SUN[1] + r * math.sin(a), 5, 1, a + 1.57, Y if rng.random() < .6 else R)
d.ellipse([SUN[0] - 16, SUN[1] - 16, SUN[0] + 16, SUN[1] + 16], fill=Y)
d.ellipse([SUN[0] - 13, SUN[1] - 13, SUN[0] + 13, SUN[1] + 13], fill=R)
y = HOR + 6.0
while y < H - 70:
    t = (y - HOR) / (H - HOR)
    half = max(4, 6 + 34 * t + 5 * math.sin(y / 9.0))
    for _ in range(int(4 + 7 * t)):
        cx = SUN[0] - 6 * t + rng.normal(0, half * 0.5)
        ln = rng.uniform(6, 12 + 26 * t)
        col = R if rng.random() < 0.58 else Y
        stroke(cx, y + rng.normal(0, 1.5), ln, 2 if t < 0.45 else 3, rng.normal(0, .04), col)
    for _ in range(int(1 + 3 * t)):   # sparks of white light beside the road
        stroke(SUN[0] + rng.normal(0, half), y + rng.normal(0, 2), rng.uniform(4, 9), 1, 0, WH)
    y += rng.uniform(3.5, 6) * (1 + 0.7 * t)

# ---- foreground: the dark diagonal of wavelets ----
for _ in range(1500):
    x = rng.uniform(0, W); yv = rng.uniform(HOR + 40, H)
    t = (yv - HOR) / (H - HOR)
    if rng.random() > t ** 1.6 * (1.2 - 0.5 * x / W):
        continue
    col = K if rng.random() < 0.55 else (B if rng.random() < 0.6 else G)
    ln = rng.uniform(6, 10 + 24 * t)
    stroke(x, yv, ln, 2 if t < .6 else 3, rng.normal(-0.03, .05), col)
    if rng.random() < .35:
        stroke(x + 3, yv + 3, ln * .7, 1, 0, WH)

# ---- three boats, receding into the mist ----
def boat(cx, cy, s, cols, ghosty=0.0):
    hull = [(cx - 26 * s, cy), (cx - 20 * s, cy + 6 * s), (cx + 18 * s, cy + 6 * s), (cx + 27 * s, cy - 1 * s)]
    if rng.random() >= 0:
        d.polygon(hull, fill=cols[0])
    # oarsman standing at the stern, passenger seated
    d.line([cx + 12 * s, cy, cx + 12 * s, cy - 17 * s], fill=cols[0], width=max(2, int(4 * s)))
    d.ellipse([cx + 12 * s - 3 * s, cy - 23 * s, cx + 12 * s + 3 * s, cy - 17 * s], fill=cols[0])
    d.line([cx + 12 * s, cy - 12 * s, cx + 30 * s, cy + 9 * s], fill=cols[0], width=max(1, int(2 * s)))
    d.polygon([(cx - 9 * s, cy), (cx - 7 * s, cy - 9 * s), (cx - 2 * s, cy - 9 * s), (cx - 1 * s, cy)], fill=cols[0])
    d.ellipse([cx - 7 * s, cy - 14 * s, cx - 2 * s, cy - 9 * s], fill=cols[0])
    # broken reflection and wake
    for i in range(int(26 * s)):
        yy_ = cy + 7 * s + i * 1.7
        stroke(cx + rng.normal(0, 13 * s), yy_, rng.uniform(5, 20 * s), 1 if i % 3 else 2,
               rng.normal(0, .04), cols[i % len(cols)])
    for i in range(int(8 * s)):
        stroke(cx + rng.normal(0, 22 * s), cy + 5 * s + rng.uniform(0, 5), rng.uniform(4, 10), 1, 0, WH)
    if ghosty:   # mist: scumble light strokes back over the far boats
        for i in range(int(ghosty * 90)):
            px, py = cx + rng.normal(0, 16 * s), cy - 8 * s + rng.normal(0, 10 * s)
            stroke(px, py, rng.uniform(3, 7), 1, rng.normal(0, .3), B if rng.random() < .7 else WH)

boat(236, 266, 0.5, [K, B, WH])
boat(196, 316, 0.74, [K, K, B])
boat(150, 392, 1.0, [K, K, B, G])

save(img)
