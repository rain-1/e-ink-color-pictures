"""Evening: the October page of a Flemish book of hours — sowing at sunset, Scorpio above."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from ink import *

rng = np.random.default_rng(10)
img = canvas('y')
x, y = grid()
def poly(pts):
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).polygon([tuple(p) for p in pts], fill=255); return np.array(m) > 0
def ell(cx, cy, rx, ry): return ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 < 1
def rect(x0, y0, x1, y1): return (x >= x0) & (x < x1) & (y >= y0) & (y < y1)
def lines(pts, w):
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).line([tuple(p) for p in pts], fill=255, width=w); return np.array(m) > 0
def outline(m, c='k'):
    fill(img, m & (~np.roll(m, 1, 0) | ~np.roll(m, -1, 0) | ~np.roll(m, 1, 1) | ~np.roll(m, -1, 1)), c)
def text(xy, s, f, c='k', anchor='mm'):
    m = Image.new('1', (W, H), 0); d = ImageDraw.Draw(m); d.fontmode = '1'; d.text(xy, s, font=f, fill=1, anchor=anchor)
    fill(img, np.array(m) > 0, c)

# --- gold border with a little shimmer
fill(img, ((x.astype(int) % 8 == 0) & (y.astype(int) % 8 == 0)) | ((x.astype(int) % 8 == 4) & (y.astype(int) % 8 == 4)), 'w')  # gold leaf grain
# --- frames
PX0, PX1, PY0, PY1 = 40, 360, 150, 520   # miniature
LY = 128                                  # lunette baseline
# lunette: zodiac on blue
lun = ell(200, LY, 120, 96) & (y < LY)
fill(img, lun, 'b')
stars = lun & (rng.random((H, W)) < 0.012)
for sy, sx in zip(*np.nonzero(stars)):
    fill(img, ((np.abs(x - sx) < 2.5) & (np.abs(y - sy) < .6)) | ((np.abs(y - sy) < 2.5) & (np.abs(x - sx) < .6)), 'y')
# clouds rim of the lunette
for k in range(-6, 7):
    a = np.pi * (k + 6) / 12
    cx_, cy_ = 200 - 112 * np.cos(a), LY - 88 * np.sin(a)
    fill(img, ell(cx_, cy_, 14, 10) & lun, 'w'); outline(ell(cx_, cy_, 14, 10) & lun, 'b')
# Scorpio: the constellation and a gold scorpion
sc = [(150, 70), (166, 64), (182, 66), (196, 74), (206, 86), (214, 100), (230, 106), (246, 102), (256, 92), (252, 82)]
fill(img, lines(sc, 2) & lun, 'y')
for (sx, sy) in sc: fill(img, ell(sx, sy, 3, 3), 'w')
fill(img, ell(196, 74, 4.5, 4.5), 'r')  # Antares
fill(img, ell(196, 74, 2, 2), 'y')
# claws
fill(img, lines([(150, 70), (136, 58), (130, 46)], 3) | lines([(150, 70), (138, 80), (126, 82)], 3), 'y')
fill(img, lines([(256, 92), (262, 80), (256, 74)], 3), 'y'); fill(img, poly([(256, 74), (250, 70), (258, 66)]), 'y')
outline(ell(200, LY, 121, 97) & ~ell(200, LY, 118, 94) & (y < LY) | rect(78, LY, 322, LY + 2), 'k')
fill(img, ell(200, LY, 122, 98) & ~ell(200, LY, 119, 95) & (y < LY), 'r')
F = '/usr/share/fonts/truetype/'
text((200, LY + 10), 'OCTOBER  ·  SCORPIO', ImageFont.truetype(F + 'liberation/LiberationSerif-Bold.ttf', 14), 'r')

# --- miniature: sky at sunset
pic = rect(PX0, PY0, PX1, PY1)
HZ = 268
t = (y - PY0) / (HZ - PY0)
mix(img, pic & (y < HZ) & (t < 0.5), 'b', 'r', np.clip(t / 0.5, 0, 1) ** 0.9)
mix(img, pic & (y < HZ) & (t >= 0.5), 'r', 'y', np.clip((t - 0.5) / 0.5, 0, 1) ** 1.1)
# thin cloud bars, lit gold underneath
for (cy, cx, ln) in [(176, 70, 120), (190, 200, 140), (206, 60, 90), (222, 250, 90), (238, 110, 70)]:
    bar = pic & (np.abs(y - cy) < 2.5) & (x > cx) & (x < cx + ln) & (vnoise((H, W), 8, rng, 2) > .35)
    fill(img, bar, 'b' if cy < 200 else 'r'); fill(img, bar & (y > cy + 1), 'y')
# low sun
sx, sy = 286, HZ - 6
fill(img, pic & ell(sx, sy, 14, 14) & (y < HZ), 'w'); fill(img, pic & (np.abs(np.hypot(x - sx, y - sy) - 15) < 1.2) & (y < HZ), 'y')
# rooks streaming home
for _ in range(26):
    bx, by = rng.normal(150, 50), rng.normal(200, 20); s = rng.uniform(2, 3.5)
    fill(img, pic & (np.abs(y - by + s * .6 * np.abs(np.sin((x - bx) / s * 1.6))) < .8) & (np.abs(x - bx) < s * 1.9), 'k')

# --- distant city: gothic silhouette on the horizon (a Louvre-ish castle, Bruges belfry)
sil = np.zeros((H, W), bool)
sil |= rect(PX0, HZ - 10, PX1, HZ)
for (bx, bw, bh, spire) in [(60, 30, 26, 1), (92, 18, 40, 1), (112, 40, 22, 0), (152, 14, 62, 2), (168, 30, 30, 1),
                             (204, 22, 20, 0), (232, 40, 34, 1), (276, 16, 18, 0), (300, 30, 28, 1), (332, 20, 44, 1)]:
    sil |= rect(bx, HZ - bh, bx + bw, HZ)
    if spire == 1: sil |= poly([(bx - 1, HZ - bh), (bx + bw / 2, HZ - bh - bw * .9), (bx + bw + 1, HZ - bh)])
    if spire == 2:  # belfry: stacked stages and a lantern
        sil |= rect(bx + 2, HZ - bh - 14, bx + bw - 2, HZ - bh) | poly([(bx + 3, HZ - bh - 14), (bx + bw / 2, HZ - bh - 30), (bx + bw - 3, HZ - bh - 14)])
    for k in np.arange(bx, bx + bw - 2, 5):  # crenellations
        sil |= rect(k, HZ - bh - 3, k + 3, HZ - bh) if not spire else np.zeros((H, W), bool)
sil &= pic
fill(img, sil, 'k')
# lit windows
for _ in range(40):
    wx, wy = rng.uniform(PX0, PX1), rng.uniform(HZ - 40, HZ - 4)
    if sil[int(wy), int(wx)] and sil[int(wy) - 3, int(wx)]: fill(img, rect(wx, wy, wx + 1.5, wy + 3), 'y')

# --- the field: ploughed furrows in perspective, red-brown earth (red + black screen)
fld = pic & (y >= HZ)
d = (y - HZ) / (PY1 - HZ)
mix(img, fld, 'r', 'k', np.clip(0.55 - d * 0.35, 0.15, 0.6))
vx = 200
ang = (x - vx) / np.maximum(y - HZ + 2, 1)
fur = fld & (np.abs(np.sin(ang * 22)) < 0.22 + d * 0.15)
fill(img, fur, 'k')
fill(img, fld & (np.abs(np.sin(ang * 22 - .35)) < 0.12 + d * .1) & (BAYER < .6), 'y')
# a green hedge and trees along the far edge of the field
hedge = pic & (y >= HZ) & (y < HZ + 9 + 3 * np.sin(x / 7))
fill(img, hedge, 'g'); fill(img, hedge & (BAYER < .4), 'k')
for (tx, s) in [(52, 22), (78, 14), (346, 26), (322, 16)]:
    tr = pic & (((x - tx) / s) ** 2 + ((y - HZ + s * 1.1) / (s * 1.3)) ** 2 < 1)
    leaf = vnoise((H, W), 4, rng, 2)
    fill(img, tr, 'k'); fill(img, tr & (leaf > .45), 'r'); fill(img, tr & (leaf > .62), 'y')
    fill(img, pic & rect(tx - 1.5, HZ - s * .4, tx + 1.5, HZ + 8), 'k')

# --- the sower: blue tunic, seed-bag, arm flung out, seed in an arc
sx0, sy0 = 150, 470
fill(img, poly([(sx0 - 14, sy0 - 10), (sx0 - 8, sy0 - 62), (sx0 + 10, sy0 - 62), (sx0 + 16, sy0 - 10)]), 'b')   # tunic
fill(img, poly([(sx0 - 14, sy0 - 10), (sx0 - 8, sy0 - 62), (sx0 + 10, sy0 - 62), (sx0 + 16, sy0 - 10)]) & (x > sx0 + 4) & (BAYER < .5), 'k')
fill(img, rect(sx0 - 18, sy0 - 52, sx0 - 5, sy0 - 30) | ell(sx0 - 11, sy0 - 30, 7, 5), 'w')                       # seed bag
outline(rect(sx0 - 18, sy0 - 52, sx0 - 5, sy0 - 30) | ell(sx0 - 11, sy0 - 30, 7, 5))
fill(img, lines([(sx0 + 8, sy0 - 58), (sx0 + 26, sy0 - 50), (sx0 + 40, sy0 - 60)], 5), 'b')                        # flung arm
fill(img, ell(sx0 + 42, sy0 - 61, 3, 3), 'w')
fill(img, lines([(sx0 - 6, sy0 - 12), (sx0 - 12, sy0 + 22)], 5) | lines([(sx0 + 8, sy0 - 12), (sx0 + 18, sy0 + 20)], 5), 'r')  # hose
fill(img, ell(sx0 - 14, sy0 + 24, 6, 3) | ell(sx0 + 20, sy0 + 22, 6, 3), 'k')
fill(img, ell(sx0 + 1, sy0 - 70, 7, 8), 'w'); fill(img, ell(sx0 + 1, sy0 - 76, 9, 4) | rect(sx0 - 6, sy0 - 80, sx0 + 8, sy0 - 74), 'r')  # face, red hood
fill(img, ell(sx0 + 4, sy0 - 70, 1, 1), 'k')
outline(ell(sx0 + 1, sy0 - 70, 7, 8))
for k in range(28):  # seed arc
    a = k / 28
    px, py = sx0 + 44 + a * 70, sy0 - 62 + 80 * a * a - 10 * a + rng.normal(0, 3)
    fill(img, ell(px, py, 1.2, 1.2), 'y')

# --- the harrow horse, small, further back, with a rider
hx, hy = 262, 360
fill(img, ell(hx, hy, 22, 10), 'w'); outline(ell(hx, hy, 22, 10))
fill(img, poly([(hx + 16, hy - 6), (hx + 28, hy - 24), (hx + 36, hy - 20), (hx + 24, hy + 2)]), 'w')
outline(poly([(hx + 16, hy - 6), (hx + 28, hy - 24), (hx + 36, hy - 20), (hx + 24, hy + 2)]))
fill(img, poly([(hx + 20, hy - 10), (hx + 28, hy - 24), (hx + 24, hy - 26), (hx + 16, hy - 12)]), 'k')          # mane
for lx in (-16, -8, 10, 18): fill(img, rect(hx + lx, hy + 6, hx + lx + 3, hy + 26), 'k')
fill(img, lines([(hx - 22, hy - 2), (hx - 30, hy + 10)], 3), 'k')                                                # tail
fill(img, rect(hx - 4, hy - 26, hx + 6, hy - 6), 'g'); fill(img, ell(hx + 1, hy - 31, 4, 5), 'w'); fill(img, rect(hx - 4, hy - 37, hx + 6, hy - 33), 'k')
# harrow behind it: a lattice dragging dust
hr = rect(hx - 70, hy + 14, hx - 36, hy + 28); fill(img, hr & ((x.astype(int) % 5 == 0) | (y.astype(int) % 5 == 0)), 'k')
fill(img, lines([(hx - 36, hy + 18), (hx - 14, hy + 4)], 2), 'k')
fill(img, rect(hx - 74, hy + 24, hx - 30, hy + 34) & (BAYER < .25), 'y')

# --- the archer scarecrow (after the Très Riches Heures) and magpies at the seed
ax, ay = 82, 400
fill(img, rect(ax - 1.5, ay - 50, ax + 1.5, ay + 20), 'k')
fill(img, poly([(ax - 9, ay - 2), (ax - 7, ay - 40), (ax + 7, ay - 40), (ax + 9, ay - 2)]), 'w')
fill(img, poly([(ax - 9, ay - 2), (ax - 7, ay - 40), (ax + 7, ay - 40), (ax + 9, ay - 2)]) & (y.astype(int) % 6 < 2), 'r')
fill(img, ell(ax, ay - 46, 5, 6), 'y'); fill(img, rect(ax - 7, ay - 54, ax + 7, ay - 51), 'k')
bow = (np.abs(np.hypot(x - ax - 4, y - ay + 30) - 18) < 1.2) & (x > ax + 14)
fill(img, bow, 'k'); fill(img, (np.abs(x - ax - 18) < .6) & (np.abs(y - ay + 30) < 13), 'w')
fill(img, lines([(ax + 2, ay - 30), (ax + 32, ay - 30)], 2), 'k')
for (bx, by) in [(108, 488), (124, 500), (210, 492), (236, 506), (186, 410), (300, 452)]:
    s = 1 + (by - 400) / 120
    b = ell(bx, by, 6 * s, 3.5 * s); fill(img, b, 'k'); fill(img, b & (y > by) & (x < bx + 2), 'w')
    fill(img, ell(bx + 6 * s, by - 3 * s, 2.5 * s, 2.5 * s), 'k'); fill(img, lines([(bx - 5 * s, by - 1), (bx - 12 * s, by - 4 * s)], 2), 'k')

# miniature frame
frm = rect(PX0 - 3, PY0 - 3, PX1 + 3, PY1 + 3) & ~pic
fill(img, frm, 'k'); fill(img, rect(PX0 - 2, PY0 - 2, PX1 + 2, PY1 + 2) & ~rect(PX0 - 1, PY0 - 1, PX1 + 1, PY1 + 1), 'r')

# --- strewn border: flowers, a snail, a butterfly, each with a cast shadow
free = ~(rect(PX0 - 6, PY0 - 6, PX1 + 6, PY1 + 6) | ell(200, LY, 126, 102) & (y < LY + 18))
def flower(cx, cy, kind):
    sh = lambda m: np.roll(np.roll(m, 2, 0), 2, 1)
    if kind == 'pink':
        ang = np.arctan2(y - cy, x - cx); r = np.hypot(x - cx, y - cy)
        m = r < 7 + 2 * np.cos(ang * 8)
    elif kind == 'corn':
        ang = np.arctan2(y - cy, x - cx); r = np.hypot(x - cx, y - cy)
        m = (r < 8) & (np.cos(ang * 7) > -.3) | (r < 3)
    elif kind == 'daisy':
        ang = np.arctan2(y - cy, x - cx); r = np.hypot(x - cx, y - cy)
        m = (r < 8) & (np.cos(ang * 12) > 0) | (r < 3)
    else:
        m = ell(cx, cy, 9, 4) | ell(cx + 4, cy - 3, 5, 3)
    m &= free; fill(img, sh(m) & ~m & free, 'k') if False else mix(img, sh(m) & ~m & free, 'y', 'k', .5)
    col = dict(pink='r', corn='b', daisy='w', leaf='g')[kind]
    fill(img, m, col)
    if kind in ('pink', 'leaf'): outline(m)
    else: outline(m, 'b' if kind == 'corn' else 'y')
    if kind == 'pink': fill(img, (np.hypot(x - cx, y - cy) < 2.5) & m, 'w')
    if kind == 'corn': fill(img, (np.hypot(x - cx, y - cy) < 2.2) & m, 'k')
    if kind == 'daisy': fill(img, (np.hypot(x - cx, y - cy) < 2.4) & m, 'y')
    # stem
    fill(img, lines([(cx, cy + 6), (cx - 4, cy + 18)], 2) & free, 'g')

kinds = ['pink', 'corn', 'daisy', 'leaf']
pts = []
while len(pts) < 46:
    cx, cy = rng.uniform(10, 390), rng.uniform(10, 590)
    if free[int(cy), int(cx)] and all((cx - a) ** 2 + (cy - b) ** 2 > 22 ** 2 for a, b in pts):
        pts.append((cx, cy))
for i, (cx, cy) in enumerate(pts): flower(cx, cy, kinds[i % 4])
# snail
snx, sny = 372, 560
fill(img, ell(snx - 4, sny + 4, 14, 3), 'w'); outline(ell(snx - 4, sny + 4, 14, 3))
fill(img, ell(snx, sny - 2, 8, 8), 'y'); fill(img, np.abs(np.hypot(x - snx, y - sny + 2) - 4) < 1, 'r'); outline(ell(snx, sny - 2, 8, 8))
fill(img, lines([(snx - 16, sny + 2), (snx - 20, sny - 8)], 1), 'k')
# butterfly (a red admiral) in the left margin
bx, by = 20, 300
for sgn in (-1, 1):
    wing = ell(bx + sgn * 7, by - 4, 7, 9) | ell(bx + sgn * 5, by + 7, 5, 6)
    fill(img, wing, 'k'); fill(img, wing & (np.abs(y - by + 2 + sgn * 0) < 2.5), 'r'); fill(img, ell(bx + sgn * 9, by - 9, 2, 2), 'w')
fill(img, rect(bx - 1, by - 10, bx + 1, by + 10), 'k')
save(img)
