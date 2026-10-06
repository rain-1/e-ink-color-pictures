"""Evening: 7 August 1947 — the raft thrown onto the reef at Raroia, sun going down.
Screenprint layers in pure palette; tone between two inks by 8x8 Bayer screen."""
import os, sys, math
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(__file__))
from lib import *

rng = np.random.default_rng(807)
img = np.zeros((H, W, 3), np.uint8)
HZ = 318
SX, SY, SR = 150, HZ, 46

# sky: blue -> red -> yellow, in three screened bands
t = YY / HZ
sky = YY < HZ
n = noise(2, 50, 4)
screen(img, sky & (t < 0.42), np.clip(t / 0.42 + (n - 0.5) * 0.3, 0, 1), B, R)
# lower sky, warmed by a glow around the sun
d = np.hypot(XX - SX, (YY - SY) * 1.3)
band = np.clip((t - 0.42) / 0.58 + (n - 0.5) * 0.25, 0, 1) ** 1.3
glow = np.clip(1 - (d - SR) / 170, 0, 1) ** 1.5
screen(img, sky & (t >= 0.42), np.maximum(band, glow * np.clip((t - 0.3) * 3, 0, 1)), R, Y)
# long cloud bars: black-red, edges lit yellow
for (cy, th, x0, x1, sd) in [(70, 7, -20, 300, 1), (96, 4, 120, 430, 2), (150, 9, -40, 250, 3), (178, 5, 200, 420, 4),
                             (228, 6, 40, 380, 5), (252, 3, -10, 220, 6), (282, 4, 230, 420, 7)]:
    wob = noise(sd + 10, 30, 3)
    edge = th * (0.4 + wob * 1.2) * np.clip(np.minimum(XX - x0, x1 - XX) / 60, 0, 1)
    m = sky & (np.abs(YY - cy - 3 * np.sin(XX / 40 + sd)) < edge)
    screen(img, m, np.clip((YY - cy) / (th + 1) * 0.5 + 0.55 - (cy / HZ) * 0.5, 0, 1), K, R)
    lit = sky & (np.abs(YY - (cy + 3 * np.sin(XX / 40 + sd) + edge)) < 1.0) & (edge > 1)
    img[lit] = Y
# sun: yellow disc, sliced by thin red bars as it meets the sea
sun = sky & (np.hypot(XX - SX, YY - SY) < SR)
img[sun] = Y
for k, yb in enumerate(range(HZ - 22, HZ, 5)):
    img[sun & (np.abs(YY - yb) < 0.5 + k * 0.4)] = R

# sea beyond the reef: deep blue, sun-path broken into yellow/red dashes
sea = (YY >= HZ) & (YY < 410)
img[sea] = B
im = Image.fromarray(img); dr = ImageDraw.Draw(im)
for y in range(HZ + 2, 410, 3):
    s_ = (y - HZ) / 92
    for k in range(int(6 + s_ * 10)):
        w = rng.uniform(4, 10 + 40 * s_) * (1 - abs(rng.normal(0, 0.3)))
        x = SX + rng.normal(0, 14 + 60 * s_)
        dr.line([(x - w / 2, y), (x + w / 2, y)], fill=Y if rng.random() < 0.7 else R)
    for k in range(int(4 + s_ * 8)):
        x = rng.uniform(0, W)
        dr.line([(x, y), (x + rng.uniform(4, 16), y)], fill=K)

# distant islets of the atoll: palm silhouettes on the horizon at right
def tiny_palm(x, y, h, lean):
    dr.line([(x, y), (x + lean, y - h)], fill=K, width=2)
    for a in np.linspace(-2.8, -0.3, 6):
        dr.arc([x + lean - 8, y - h - 3, x + lean + 8, y - h + 7], math.degrees(a) + 180, math.degrees(a) + 230, fill=K)
        dr.line([(x + lean, y - h), (x + lean + 9 * math.cos(a), y - h - 4 * math.sin(-a) + 3)], fill=K, width=2)
dr.polygon([(250, HZ + 1), (262, HZ - 6), (380, HZ - 7), (400, HZ - 4), (400, HZ + 1)], fill=K)
for x in range(266, 400, 9):
    tiny_palm(x + rng.uniform(-3, 3), HZ - 5, rng.uniform(12, 24), rng.uniform(-5, 5))

# the reef: surf exploding white across the frame
img = np.asarray(im).copy()
fn = noise(21, 16, 4); fn2 = noise(22, 6, 2)
reef_y = 404 + 10 * np.sin(XX / 55) + 6 * np.sin(XX / 17 + 1)
height = 30 + 44 * noise(23, 120, 2)[0][None, :].repeat(H, 0) if False else 30 + 44 * np.clip(noise(23, 90, 2), 0, 1)
foam = (YY < reef_y + 14) & (YY > reef_y - height * (0.6 + 0.6 * fn))
img[foam] = WH
shade = foam & (fn2 > 0.62) & (YY > reef_y - height * 0.35)
img[shade] = B
spray = (YY > reef_y - height * 1.6) & (YY < reef_y - height * 0.6) & (fn2 > 0.8 - 0.1 * fn) & (YY < HZ + 90)
img[spray] = WH
# the reef flat itself: coral heads, red-black
flat = (YY >= reef_y + 14) & (YY < reef_y + 34 + 8 * fn)
screen(img, flat, np.clip(fn * 1.4 - 0.2, 0, 1), K, R, T4 := thresh(m=B4))
# lagoon: shallow, turquoise — green and blue screened, sky reflected as yellow streaks
lag = YY >= reef_y + 34 + 8 * fn
lt = np.clip((YY - 440) / 160, 0, 1)
screen(img, lag, 0.1 + 0.35 * lt, G, B)
im = Image.fromarray(img); dr = ImageDraw.Draw(im)
for k in range(140):
    y = rng.uniform(455, 600); x = rng.uniform(0, W)
    dr.line([(x, y), (x + rng.uniform(6, 22), y)], fill=Y if (abs(x - SX) < 70 and rng.random() < 0.8) else WH)

# the wreck on the reef: logs askew, cabin crushed, broken mast leaning
wx, wy = 112, 420
logs = [(-60, -4, 54, 2), (-58, 2, 58, 8), (-52, 8, 60, 13), (-48, 13, 56, 16)]
for (a, b, c, d_) in logs:
    dr.line([(wx + a, wy + b), (wx + c, wy + d_)], fill=K, width=7)
    dr.line([(wx + a + 3, wy + b - 2), (wx + c - 4, wy + d_ - 2)], fill=Y, width=1)
dr.polygon([(wx - 8, wy - 2), (wx + 30, wy + 4), (wx + 26, wy - 18), (wx - 2, wy - 26)], fill=K)
dr.line([(wx - 2, wy - 26), (wx + 26, wy - 18)], fill=Y)
dr.line([(wx - 30, wy), (wx + 8, wy - 86)], fill=K, width=4)       # one mast leg standing
dr.line([(wx - 4, wy + 4), (wx + 8, wy - 86)], fill=K, width=4)
dr.line([(wx + 8, wy - 86), (wx + 74, wy - 30)], fill=K, width=2)  # stay
dr.polygon([(wx - 50, wy - 4), (wx - 6, wy - 66), (wx + 6, wy - 60), (wx - 20, wy - 2)], fill=WH, outline=K)  # sail slumped
dr.arc([wx - 34, wy - 50, wx - 14, wy - 30], 0, 360, fill=R, width=2)
dr.line([(wx - 70, wy + 30), (wx - 30, wy + 20)], fill=K, width=3)  # loose spar in the surf

# crew wading across the lagoon toward the islet, carrying things
def wader(x, y, h=26, load=False):
    dr.ellipse([x - 3, y - h, x + 3, y - h + 7], fill=K)
    dr.line([(x, y - h + 6), (x, y - 8)], fill=K, width=4)
    dr.line([(x, y - 8), (x - 3, y)], fill=K, width=3); dr.line([(x, y - 8), (x + 3, y)], fill=K, width=3)
    if load:
        dr.rectangle([x - 6, y - h - 6, x + 8, y - h - 1], fill=K)
        dr.line([(x - 3, y - h + 8), (x - 5, y - h - 2)], fill=K, width=2); dr.line([(x + 3, y - h + 8), (x + 6, y - h - 2)], fill=K, width=2)
    else:
        dr.line([(x, y - h + 10), (x + 8, y - h + 16)], fill=K, width=2); dr.line([(x, y - h + 10), (x - 7, y - h + 17)], fill=K, width=2)
    dr.arc([x - 9, y - 3, x + 9, y + 3], 0, 180, fill=WH)
for i, (x, y) in enumerate([(176, 500), (196, 506), (214, 498), (236, 512), (152, 520), (256, 504)]):
    wader(x, y, 24 + (y - 495) * 0.5, load=i % 2 == 0)

# the big palm, foreground right, arching over
def bez(p0, p1, p2, n=60):
    t = np.linspace(0, 1, n)[:, None]
    return (1 - t) ** 2 * np.array(p0) + 2 * (1 - t) * t * np.array(p1) + t ** 2 * np.array(p2)
trunk = bez((392, 610), (402, 360), (300, 214), 80)
for i in range(len(trunk) - 1):
    w = 18 - 11 * i / len(trunk)
    dr.line([tuple(trunk[i]), tuple(trunk[i + 1])], fill=K, width=int(w))
    if i % 4 == 0:   # ring scars, lit on the sun side
        x, y = trunk[i]
        dr.line([(x - w / 2, y), (x - w / 2 + 3, y + 1)], fill=Y, width=1)
cx, cy = trunk[-1]
for k in range(8):                                     # coconuts
    a = k * 0.8
    dr.ellipse([cx - 4 + 7 * math.cos(a), cy + 4 + 4 * math.sin(a), cx + 4 + 7 * math.cos(a), cy + 12 + 4 * math.sin(a)], fill=K, outline=R if k % 3 == 0 else K)
for f in range(11):
    ang = -math.pi + f * (2 * math.pi / 11) + rng.normal(0, 0.12)
    L = rng.uniform(80, 150) * (0.75 if math.sin(ang) < -0.5 else 1)
    end = (cx + L * math.cos(ang), cy + L * 0.55 * math.sin(ang) + L * 0.45)   # droop
    mid = (cx + L * 0.55 * math.cos(ang), cy + L * 0.45 * math.sin(ang) - 22)
    sp = bez((cx, cy), mid, end, 40)
    dr.line([tuple(p) for p in sp], fill=K, width=3)
    for i in range(2, len(sp) - 1, 2):
        p, q = sp[i], sp[i + 1]
        dx, dy = q - p; nrm = math.hypot(dx, dy) + 1e-6
        nx, ny = -dy / nrm, dx / nrm
        ll = 20 * math.sin(math.pi * i / len(sp)) + 4
        for side in (-1, 1):
            tip = (p[0] + side * nx * ll + dx / nrm * 6, p[1] + side * ny * ll + abs(ll) * 0.7)
            dr.line([tuple(p), tip], fill=K, width=1)
# beach under the palm, a crab
dr.polygon([(250, 600), (290, 548), (400, 530), (400, 600)], fill=Y)
for k in range(60):
    x, y = rng.uniform(290, 400), rng.uniform(548, 600)
    if y > 548 + (400 - x) * -0.1: dr.point((x, y), fill=K)
dr.ellipse([326, 566, 342, 576], fill=R, outline=K)
for s_ in (-1, 1):
    for j in range(3):
        dr.line([(334 + s_ * 6, 572), (334 + s_ * (12 + j * 2), 576 + j * 2)], fill=K)
    dr.line([(334 + s_ * 6, 568), (334 + s_ * 12, 561)], fill=K, width=2)
dr.line([(392, 610), (380, 540)], fill=K, width=18)
im.save(os.environ.get("OUT_RAW", "reef.png"))
