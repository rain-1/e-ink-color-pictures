"""Evening: sunset colours at the light. A banded lighthouse on a black
headland, its beams just lit, the keeper at the flagstaff hauling the
ensign down for the night. The sky is an ordered-dither gradient through
yellow, red, blue and black; the line work is woodcut black with white
hatching on the rock. All six inks."""
import math
import os
import random

import numpy as np
from PIL import Image, ImageDraw

S = 4
W1, H1 = 400, 600
W, H = W1 * S, H1 * S
K = (0, 0, 0); Wt = (255, 255, 255); R = (0xE0, 0x1B, 0x24)
Y = (0xF5, 0xD4, 0x00); B = (0x12, 0x3D, 0xB0); G = (0x1E, 0x9B, 0x3C)
random.seed(1821)
HORIZON = 436
LIGHT = (118, 226)   # lantern focus

# ------------------------------------------------- sky & sea, dithered at 1x
bayer = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]], dtype=np.float32) / 16
B8 = np.tile(bayer, (H1 // 4 + 1, W1 // 4 + 1))[:H1, :W1]
yy, xx = np.mgrid[0:H1, 0:W1].astype(np.float32)

def ramp(t, stops):
    """Ordered-dither a scalar field t (0..1) through colour stops."""
    out = np.zeros((H1, W1, 3), np.uint8)
    for i in range(len(stops) - 1):
        t0, c0 = stops[i]; t1, c1 = stops[i + 1]
        sel = (t >= t0) & (t < t1) if i < len(stops) - 2 else (t >= t0)
        f = np.clip((t - t0) / (t1 - t0), 0, 1)
        pick = f > B8
        out[sel & ~pick] = c0
        out[sel & pick] = c1
    return out

sky_t = np.clip((HORIZON - yy) / HORIZON, 0, 1)            # 0 at horizon, 1 at top
# a glow centred on the setting sun
sun_x, sun_y = 250, HORIZON
glow = np.exp(-(((xx - sun_x) / 150) ** 2 + ((yy - sun_y) / 90) ** 2))
sky_t = np.clip(sky_t - 0.35 * glow, 0, 1)
sky = ramp(sky_t, [(0.0, Y), (0.2, R), (0.52, B), (1.01, B)])

sea_t = np.clip((yy - HORIZON) / (H1 - HORIZON), 0, 1)
sea = ramp(sea_t, [(0.0, B), (0.6, K), (1.01, K)])
# the sun's reflection: a broken column of yellow and red flecks
refl = np.exp(-(((xx - sun_x) / np.maximum(18 + (yy - HORIZON) * 0.25, 4)) ** 2))
streak = ((yy.astype(int) // 3) % 2 == 0) & (np.random.RandomState(5).rand(H1, W1) < refl * 0.9)
near = (yy - HORIZON) < 60
sea[streak & near & (B8 < 0.55)] = Y
sea[streak & ~near & (B8 < 0.35)] = R
sea[streak & near & (B8 >= 0.55) & (B8 < 0.85)] = R

base = np.where((yy < HORIZON)[..., None], sky, sea).astype(np.uint8)

# light beams: two wedges from the lantern, dithered to half so the sky shows through
beam = Image.new("L", (W1, H1), 0)
bd = ImageDraw.Draw(beam)
lx, ly = LIGHT
for ang, spread in ((-8, 6), (176, 6)):
    a0, a1 = math.radians(ang - spread), math.radians(ang + spread)
    far = 420
    bd.polygon([(lx, ly), (lx + far * math.cos(a0), ly + far * math.sin(a0)),
                (lx + far * math.cos(a1), ly + far * math.sin(a1))], fill=255)
bm = np.asarray(beam) > 0
dist_l = np.hypot(xx - lx, yy - ly)
strength = np.clip(1 - dist_l / 330, 0, 1) ** 1.5 * 0.6
base[bm & (B8 < strength) & (yy < HORIZON)] = Y
# a half-set sun on the horizon
sun = (np.hypot(xx - sun_x, (yy - sun_y) * 1.0) < 34) & (yy < HORIZON)
base[sun] = R
base[sun & (np.hypot(xx - sun_x, yy - sun_y) < 26)] = Y

img = Image.fromarray(base).resize((W, H), Image.NEAREST)
d = ImageDraw.Draw(img)

def P(x, y): return (x * S, y * S)
def ln(pts, w=1.5, c=K): d.line([P(*p) for p in pts], fill=c, width=int(w * S), joint="curve")

# horizon line
ln([(0, HORIZON), (400, HORIZON)], 1.2)

# ------------------------------------------------- headland & rocks
head = [(0, 300), (30, 292), (60, 296), (90, 288), (130, 290), (160, 298), (186, 312),
        (200, 340), (214, 372), (226, 400), (236, 430), (250, 470), (262, 520), (280, 560),
        (300, 600), (0, 600)]
d.polygon([P(*p) for p in head], fill=K)
# green turf cap on the headland
turf = [(0, 300), (30, 292), (60, 296), (90, 288), (130, 290), (160, 298), (186, 312),
        (176, 318), (140, 306), (100, 302), (60, 306), (30, 304), (0, 310)]
d.polygon([P(*p) for p in turf], fill=G)
for tx in range(6, 180, 9):   # grass tufts
    ty = 300 + 4 * math.sin(tx / 13)
    ln([(tx, ty + 5), (tx - 2, ty - 3)], 1.0)
    ln([(tx, ty + 5), (tx + 2.5, ty - 2)], 1.0)
# white hatching for the rock faces, strata sloping seaward
def face_x(y):
    """x of the headland's seaward face at height y."""
    edge = head[6:15]
    for (xa, ya), (xb, yb) in zip(edge, edge[1:]):
        if ya <= y <= yb:
            return xa + (xb - xa) * (y - ya) / (yb - ya)
    return 186 if y < 312 else 300
for i in range(58):
    y0 = 318 + i * 4.8
    face = face_x(y0) - 4
    if face < 12:
        continue
    seg_len = random.uniform(0.3, 0.8) * face
    xa = random.uniform(0, face - seg_len)
    ln([(xa, y0 + xa * 0.12), (xa + seg_len, y0 + (xa + seg_len) * 0.12)], 1.25, Wt)
for x in range(0, 300, 30):   # a few vertical cracks
    x0 = x + random.uniform(0, 20)
    y0 = 330 + x0 * 0.9
    ln([(x0, y0), (x0 + 3, y0 + 20), (x0 - 1, y0 + 40)], 1.25, Wt)
# foam where sea meets rock
for x, y in [(226, 436), (240, 450), (252, 476), (266, 528), (286, 568)]:
    for k in range(3):
        ln([(x + 4 + k * 3, y + k * 3), (x + 26 + k * 6, y + 2 + k * 3)], 1.6, Wt)
# foreground rock, bottom right, with its own foam
d.polygon([P(320, 600), P(336, 574), P(362, 566), P(388, 578), P(400, 572), P(400, 600)], fill=K)
ln([(330, 586), (352, 580)], 1.25, Wt); ln([(360, 574), (386, 582)], 1.25, Wt)
ln([(300, 566), (334, 570)], 1.6, Wt); ln([(390, 570), (400, 566)], 1.6, Wt)

# ------------------------------------------------- lighthouse
bx, top = 118, 226
base_y = 296
d.polygon([P(bx - 20, base_y), P(bx + 20, base_y), P(bx + 13, top + 14), P(bx - 13, top + 14)], fill=Wt, outline=K)
for i, yb in enumerate(range(top + 14, base_y, 14)):
    if i % 2 == 0:
        w0 = 13 + (yb - top - 14) / (base_y - top - 14) * 7
        w1 = 13 + (yb + 14 - top - 14) / (base_y - top - 14) * 7
        d.polygon([P(bx - w0, yb), P(bx + w0, yb), P(bx + w1, min(yb + 14, base_y)), P(bx - w1, min(yb + 14, base_y))], fill=R)
ln([(bx - 13, top + 14), (bx - 20, base_y)], 1.6); ln([(bx + 13, top + 14), (bx + 20, base_y)], 1.6)
# gallery, lantern, dome
d.rectangle([*P(bx - 18, top + 10), *P(bx + 18, top + 14)], fill=K)
for rx in range(-16, 17, 4):
    ln([(bx + rx, top + 4), (bx + rx, top + 10)], 0.9)
ln([(bx - 17, top + 4), (bx + 17, top + 4)], 1.2)
d.rectangle([*P(bx - 10, top - 10), *P(bx + 10, top + 10)], fill=Y, outline=K, width=int(1.4 * S))
ln([(bx - 3, top - 10), (bx - 3, top + 10)], 1.0); ln([(bx + 3, top - 10), (bx + 3, top + 10)], 1.0)
d.ellipse([*P(bx - 3, top - 3), *P(bx + 3, top + 3)], fill=Wt)
d.pieslice([*P(bx - 11, top - 20), *P(bx + 11, top - 2)], 180, 360, fill=K)
ln([(bx, top - 20), (bx, top - 27)], 1.6)
d.rectangle([*P(bx - 3, base_y - 12), *P(bx + 3, base_y)], fill=K)  # door
d.rectangle([*P(bx - 2, top + 40), *P(bx + 2, top + 46)], fill=K)     # window
d.rectangle([*P(bx - 2, top + 70), *P(bx + 2, top + 76)], fill=K)

# ------------------------------------------------- keeper's cottage
cx0, cy0 = 30, 296
d.polygon([P(cx0, cy0), P(cx0 + 44, cy0), P(cx0 + 44, cy0 - 22), P(cx0, cy0 - 22)], fill=Wt, outline=K)
d.polygon([P(cx0 - 4, cy0 - 22), P(cx0 + 48, cy0 - 22), P(cx0 + 22, cy0 - 40)], fill=K)
d.rectangle([*P(cx0 + 32, cy0 - 40), *P(cx0 + 37, cy0 - 28)], fill=K)   # chimney
for k in range(3):   # smoke
    ln([(cx0 + 34 + k * 3, cy0 - 42 - k * 8), (cx0 + 38 + k * 4, cy0 - 47 - k * 8), (cx0 + 34 + k * 5, cy0 - 51 - k * 8)], 0.9)
d.rectangle([*P(cx0 + 6, cy0 - 16), *P(cx0 + 14, cy0 - 8)], fill=Y, outline=K)
d.rectangle([*P(cx0 + 28, cy0 - 16), *P(cx0 + 36, cy0 - 8)], fill=Y, outline=K)
d.rectangle([*P(cx0 + 18, cy0 - 14), *P(cx0 + 24, cy0)], fill=K)
ln([(cx0 + 46, cy0), (cx0 + 46, cy0 - 20)], 1.0)
# picket fence
for fx in range(cx0 - 14, cx0 - 2, 4):
    ln([(fx, cy0), (fx, cy0 - 7)], 1.0)
ln([(cx0 - 16, cy0 - 4), (cx0 - 1, cy0 - 4)], 0.9)

# ------------------------------------------------- flagstaff & keeper
fx, fy = 168, 300
ln([(fx, fy), (fx, fy - 70)], 2.0)
d.ellipse([*P(fx - 2, fy - 73), *P(fx + 2, fy - 69)], fill=K)
ln([(fx + 1, fy - 70), (fx + 1, fy - 4)], 0.7)   # halyard
# the ensign, part-way down, streaming aft
ey = fy - 44
d.polygon([P(fx, ey), P(fx + 30, ey - 2), P(fx + 22, ey + 8), P(fx + 30, ey + 18), P(fx, ey + 16)], fill=R, outline=K)
d.polygon([P(fx + 2, ey + 2), P(fx + 12, ey + 3), P(fx + 12, ey + 8), P(fx + 2, ey + 8)], fill=Wt, outline=K)
# the keeper, hauling
kx, ky = fx + 9, fy
d.ellipse([*P(kx - 2.5, ky - 22), *P(kx + 2.5, ky - 17)], fill=K)
d.polygon([P(kx - 3, ky - 17), P(kx + 3, ky - 17), P(kx + 4, ky - 6), P(kx - 4, ky - 6)], fill=K)
ln([(kx - 1, ky - 6), (kx - 3, ky)], 1.8); ln([(kx + 1, ky - 6), (kx + 4, ky)], 1.8)
ln([(kx - 2, ky - 15), (kx - 8, ky - 22)], 1.6); ln([(kx + 2, ky - 14), (kx - 7, ky - 12)], 1.6)

# ------------------------------------------------- first stars and a young moon
for _ in range(34):
    x, y = random.uniform(12, 388), random.uniform(12, 200)
    r = random.choice([0.7, 0.7, 1.0, 1.3])
    d.ellipse([*P(x - r, y - r), *P(x + r, y + r)], fill=Wt)
mx, my = 318, 72
d.ellipse([*P(mx - 16, my - 16), *P(mx + 16, my + 16)], fill=Wt)
d.ellipse([*P(mx - 22, my - 17), *P(mx + 8, my + 13)], fill=B)   # earth's shadow, off-centre
d.ellipse([*P(mx - 22, my - 17), *P(mx + 8, my + 13)], outline=B, width=int(1.5 * S))

# ------------------------------------------------- gulls, home late
for gx, gy, s in [(300, 150, 6), (322, 162, 5), (340, 148, 4)]:
    ln([(gx - s, gy), (gx - s / 2, gy - s * 0.6), (gx, gy), (gx + s / 2, gy - s * 0.6), (gx + s, gy)], 1.3)

# print border
d.rectangle([*P(0, 0), *P(400, 600)], outline=K, width=int(4 * S))

def ink_downsample(im, s):
    a = np.asarray(im).astype(np.float32)
    h, w, _ = a.shape
    a = a.reshape(h // s, s, w // s, s, 3)
    dark = a.max(-1) < 90
    frac = dark.mean(axis=(1, 3))
    light = np.where(dark[..., None], 0, a).sum(axis=(1, 3))
    cnt = np.maximum((~dark).sum(axis=(1, 3)), 1)[..., None]
    out = light / cnt
    out[frac >= 0.28] = 0
    return Image.fromarray(out.astype(np.uint8), "RGB")

ink_downsample(img, S).save(os.environ["OUT_RAW"])
