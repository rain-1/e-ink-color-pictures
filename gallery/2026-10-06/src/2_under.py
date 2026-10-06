"""Midday: a natural-history plate — what lived under the Kon-Tiki. Pure palette; tone by 8x8 Bayer screens."""
import os, sys, math
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(__file__))
from lib import *

rng = np.random.default_rng(1947)
img = np.zeros((H, W, 3), np.uint8); img[:] = WH

def mask_of(draw_fn):
    m = Image.new("1", (W, H), 0); draw_fn(ImageDraw.Draw(m)); return np.asarray(m)

TOP, BOT = 22, 520          # picture area inside the plate
SURF = 92                   # sea surface
pic = (YY >= TOP) & (YY < BOT) & (XX >= 14) & (XX < W - 14)

# --- sky strip: noon, white with a yellow sun
sky = pic & (YY < SURF)
img[sky] = WH
sun = (np.hypot(XX - 330, YY - 48) < 16)
img[sun & sky] = Y
for k in range(16):
    a = k * math.pi / 8
    r = np.hypot(XX - 330, YY - 48); th = np.arctan2(YY - 48, XX - 330)
    ray = (r > 20) & (r < 30) & (np.abs(((th - a + math.pi) % (2 * math.pi)) - math.pi) < 0.06)
    img[ray & sky] = Y

# --- water: light near the surface, black in the deep; god-rays fanning from the sun
water = pic & (YY >= SURF)
depth = np.clip((YY - SURF) / (BOT - SURF), 0, 1)
ang = np.arctan2(XX - 330, YY - (SURF - 160))
rays = (np.sin(ang * 38 + noise(4, 40) * 3) * 0.5 + 0.5) ** 3 * (1 - depth) ** 1.5
t_top = np.clip(1 - depth / 0.42 + rays * 0.5, 0, 1)          # 1 = white, 0 = blue
t_bot = np.clip((depth - 0.5) / 0.5 - rays * 0.3, 0, 1)        # 1 = black
upper = water & (depth < 0.5)
screen(img, upper, t_top * 0.55, B, WH)
lower = water & (depth >= 0.5)
screen(img, lower, t_bot * 0.9, B, K)

# caustic web just under the surface
cn = noise(8, 14, 3)
caust = water & (depth < 0.18) & (np.abs(cn - 0.5) < 0.025 * (1 - depth / 0.18))
img[caust] = WH

# surface line + wavelets
surf_y = SURF + 2 * np.sin(XX / 9)
img[pic & (np.abs(YY - surf_y) < 1.2)] = B

im = Image.fromarray(img); dr = ImageDraw.Draw(im)

# --- the raft from the side, below the waterline: logs, barnacles, weed
x0, x1 = 30, 300
for i, (yl, r) in enumerate([(SURF + 4, 12), (SURF + 9, 13)]):
    dr.rounded_rectangle([x0 + i * 6, yl - r, x1 - i * 5, yl + r], radius=r, fill=Y, outline=K)
for x in range(x0 + 8, x1 - 6, 5):
    dr.line([(x, SURF + 6), (x + 2, SURF + 18)], fill=K) if rng.random() < 0.3 else None
for x in range(x0 + 14, x1, 30):                                # lashings
    dr.line([(x, SURF - 8), (x + 2, SURF + 22)], fill=WH, width=2)
    dr.line([(x, SURF - 8), (x + 2, SURF + 22)], fill=K, width=1)
dr.rectangle([x0 + 40, SURF - 20, x1 - 70, SURF - 8], fill=Y, outline=K)   # deck edge above water
dr.polygon([(150, SURF - 20), (152, TOP + 2), (156, TOP + 2), (158, SURF - 20)], fill=K)   # mast foot
dr.rectangle([200, SURF - 46, 262, SURF - 20], fill=Y, outline=K)          # cabin
dr.polygon([(194, SURF - 46), (268, SURF - 46), (256, SURF - 62), (206, SURF - 62)], fill=G, outline=K)
for x in range(198, 266, 3): dr.line([(x, SURF - 46), (x + 3, SURF - 61)], fill=K)
for x in range(204, 262, 4): dr.line([(x, SURF - 44), (x, SURF - 21)], fill=K)
# centreboards (guara) hanging down between logs
for gx in (70, 118, 236):
    dr.rectangle([gx, SURF + 18, gx + 7, SURF + 64], fill=Y, outline=K)
# goose barnacles and weed on the log bottoms
for k in range(60):
    x = rng.uniform(x0 + 6, x1 - 8); y = SURF + 20
    L = rng.uniform(5, 13)
    if rng.random() < 0.5:
        dr.line([(x, y), (x + rng.uniform(-2, 2), y + L)], fill=K, width=1)
        dr.ellipse([x - 2, y + L - 1, x + 2, y + L + 4], fill=WH, outline=K)
    else:
        pts = [(x, y)]
        for j in range(5):
            pts.append((pts[-1][0] + rng.uniform(-3, 3), pts[-1][1] + L / 4))
        dr.line(pts, fill=G, width=2)
# steering oar
dr.line([(300, SURF - 30), (378, SURF + 70)], fill=K, width=4)
dr.polygon([(360, SURF + 46), (384, SURF + 60), (380, SURF + 96), (360, SURF + 84)], fill=Y, outline=K)

img = np.asarray(im).copy()

# --- the whale shark (Rhincodon typus)
def prof(x):   # body outline: top and bottom y for x in [34, 330]
    t = np.clip((x - 34) / 296, 0, 1)
    c = 350 + 10 * np.sin(t * 2.5)
    h = 52 * np.sqrt(np.clip(t * 4, 0, 1)) * (1 - t) ** 0.55 + 7
    return c - h * 1.05, c + h * 0.85, c
top_y, bot_y, cy = prof(XX)
body = (XX >= 34) & (XX <= 334) & (YY >= top_y) & (YY <= bot_y)
im = Image.fromarray(img); dr = ImageDraw.Draw(im)
# fins drawn first so the body overlaps their roots
dr.polygon([(312, 352), (350, 284), (366, 278), (356, 300), (345, 350)], fill=K)          # upper caudal lobe
dr.polygon([(316, 360), (348, 352), (370, 396), (360, 400)], fill=K)                      # lower caudal lobe
dr.polygon([(176, 312), (204, 262), (214, 262), (222, 314)], fill=K)                      # first dorsal
dr.polygon([(272, 334), (284, 314), (290, 316), (294, 338)], fill=K)                      # second dorsal
fins = mask_of(lambda d: [d.polygon([(312, 352), (350, 284), (366, 278), (356, 300), (345, 350)], fill=1),
                          d.polygon([(316, 360), (348, 352), (370, 396), (360, 400)], fill=1),
                          d.polygon([(176, 312), (204, 262), (214, 262), (222, 314)], fill=1),
                          d.polygon([(272, 334), (284, 314), (290, 316), (294, 338)], fill=1)])
img = np.asarray(im).copy()
# body tone: dark back, pale belly
v = np.clip((YY - top_y) / (bot_y - top_y + 1e-3), 0, 1)
screen(img, body, np.clip(1.0 - v * 1.1, 0, 1) ** 0.8, B, K)
img[body & (v > 0.78)] = WH
screen(img, fins, np.full((H, W), 0.85, np.float32), B, K)
# spot pattern: vertical bars of spots behind the gills, grid of spots in front
spots = np.zeros((H, W), bool)
for x in np.arange(46, 320, 9.0):
    tb, bb, _ = prof(np.float32(x))
    for y in np.arange(tb + 5, tb + (bb - tb) * 0.72, 7.5 if x > 110 else 6):
        jx, jy = rng.normal(0, 0.8, 2)
        r = 2.0 if x < 110 else 2.4
        spots |= (np.hypot(XX - x - jx, YY - y - jy) < r)
    if x > 110 and (x // 9) % 2 == 0:
        spots |= (np.abs(XX - x - 4.5) < 0.8) & (YY > tb + 6) & (YY < tb + (bb - tb) * 0.66)
for k, f in enumerate([0.22, 0.38]):       # longitudinal ridges
    spots |= body & (np.abs(YY - (top_y + (bot_y - top_y) * f)) < 0.7) & (XX > 120)
img[spots & (body | fins)] = WH
# gills, mouth, eye
im = Image.fromarray(img); dr = ImageDraw.Draw(im); dr.fontmode = "1"
for gx in range(92, 118, 5):
    dr.arc([gx - 10, 318, gx + 4, 380], 300, 60, fill=K, width=1)
dr.line([(34, 356), (44, 362), (64, 364)], fill=K, width=3)
dr.ellipse([60, 336, 66, 342], fill=WH); dr.point((63, 339), fill=K)
dr.polygon([(104, 380), (150, 384), (176, 420), (158, 422)], fill=K)          # pectoral
# remoras riding the belly
for (rx, ry) in [(150, 391), (206, 384)]:
    dr.ellipse([rx - 12, ry - 3, rx + 12, ry + 3], fill=K, outline=WH)
# pilot fish ahead of the mouth: black and white banded
for k, (px, py) in enumerate([(18, 342), (24, 372), (12, 358)]):
    dr.ellipse([px - 9, py - 4, px + 9, py + 4], fill=WH, outline=K)
    for b in (-4, 0, 4): dr.line([(px + b, py - 4), (px + b, py + 4)], fill=K, width=2)
    dr.polygon([(px + 8, py), (px + 14, py - 4), (px + 14, py + 4)], fill=K)

# --- dorados (mahi-mahi): green-gold, blue-spotted, blunt heads
def dorado(x, y, L, flip=1):
    s = L / 100
    def T(px, py): return (x + flip * px * s, y + py * s)
    pts = [T(0, -4), T(10, -16), T(30, -20), T(70, -12), T(92, -4), T(92, 4), T(60, 12), T(20, 14), T(4, 8)]
    dr.polygon(pts, fill=G, outline=K)
    dr.polygon([T(8, -15), T(30, -27), T(80, -16), T(70, -12), T(30, -20)], fill=B, outline=K)   # dorsal
    dr.polygon([T(20, 6), T(70, 4), T(60, 12), T(20, 14)], fill=Y)                              # gold belly
    dr.polygon([T(90, 0), T(110, -14), T(102, 0), T(110, 14)], fill=Y, outline=K)              # tail
    for j in range(9):
        cxp, cyp = T(18 + j * 7.5, -7 + (j % 2) * 4)
        dr.ellipse([cxp - 1.2, cyp - 1.2, cxp + 1.2, cyp + 1.2], fill=B)
    ex, ey = T(8, -6); dr.ellipse([ex - 2, ey - 2, ex + 2, ey + 2], fill=WH, outline=K)
dorado(222, 160, 110, 1)
dorado(110, 214, 82, -1 * -1)
dorado(330, 236, 72, -1)

# school of small fish (sardines) glinting
for k in range(70):
    cx_, cy_ = 260 + rng.normal(0, 46), 440 + rng.normal(0, 18)
    if cy_ > BOT - 6 or cx_ > W - 20: continue
    dr.line([(cx_, cy_), (cx_ + 6, cy_ - 1)], fill=WH, width=2)
# a sea-turtle far down
dr.ellipse([60, 448, 96, 472], fill=G, outline=K)
for (fx, fy, gx, gy) in [(62, 452, 48, 440), (64, 468, 50, 480), (92, 452, 104, 444), (92, 468, 104, 478)]:
    dr.line([(fx, fy), (gx, gy)], fill=G, width=4)
dr.ellipse([96, 455, 108, 465], fill=G, outline=K)
for k in range(4): dr.line([(66 + k * 8, 449), (66 + k * 8, 471)], fill=K)

# key numbers on the picture
def num(x, y, n):
    dr.ellipse([x - 7, y - 7, x + 7, y + 7], fill=WH, outline=K)
    w_ = dr.textlength(str(n), font=font(11, "serifb"))
    dr.text((x - w_ / 2, y - 7), str(n), fill=K, font=font(11, "serifb"))
num(250, 300, 1); num(258, 136, 2); num(46, 382, 3); num(22, 136, 4); num(116, 444, 5); num(320, 418, 6)

# --- plate frame & caption
dr.rectangle([14, TOP, W - 15, BOT - 1], outline=K, width=2)
dr.rectangle([10, TOP - 4, W - 11, BOT + 3], outline=K, width=1)
f1, f2, f3 = font(13, "serifb"), font(12, "serifi"), font(12, "serif")
def ctext(y, s, f, c=K):
    w_ = dr.textlength(s, font=f); dr.text(((W - w_) / 2, y), s, fill=c, font=f)
ctext(4, "PLATE  II  ·  BENEATH  THE  RAFT", font(11, "serif"))
ctext(BOT + 10, "Companions of the Kon-Tiki, Pacific 1947", f2)
keys = ["1  Whale shark", "2  Dorado", "3  Pilot fish", "4  Goose barnacles", "5  Turtle", "6  Sardines"]
for i, k in enumerate(keys):
    x = 22 + (i % 3) * 128; y = BOT + 30 + (i // 3) * 17
    dr.text((x, y), k, fill=K, font=f3)
dr.line([(150, BOT + 27), (W - 150, BOT + 27)], fill=R, width=2)
im.save(os.environ.get("OUT_RAW", "under.png"))
