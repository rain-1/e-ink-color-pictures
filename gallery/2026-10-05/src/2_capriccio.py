"""Midday: a Venetian capriccio for Francesco Guardi's birthday (b. 5 Oct 1712)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from PIL import Image, ImageDraw
from ink import *

rng = np.random.default_rng(1712)
img = canvas('w')
x, y = grid()
def poly(pts):
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).polygon([tuple(p) for p in pts], fill=255); return np.array(m) > 0
def rect(x0, y0, x1, y1):
    return (x >= x0) & (x < x1) & (y >= y0) & (y < y1)
def ell(cx, cy, rx, ry):
    return ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 < 1

QY = 318  # quay line / waterline
# --- sky: blue above, Guardi's heaped cloud, warm yellow underlit
sky = y < QY
cb = vnoise((H, W), 90, rng, 3) + (y / QY) * 0.22
cl = cb * 0.85 + vnoise((H, W), 14, rng, 2) * 0.15 + 0.07
blue = sky & (cl < 0.55)
mix(img, blue, 'w', 'b', np.clip(0.9 - y / QY * 0.75, 0.2, 0.85))
cloud = sky & (cl >= 0.55)
under = np.clip((cb - np.roll(cb, -10, 0)) * 12 + (cl - 0.55) * -3, 0, 1)
mix(img, cloud, 'w', 'y', np.clip(under * 0.7, 0, 0.6))
mix(img, cloud & (under > 0.6), 'y', 'r', 0.12)
fill(img, cloud & (np.abs(cl - 0.55) < 0.004) & (y > 20), 'b')
# birds
for _ in range(9):
    bx, by = rng.uniform(40, 360), rng.uniform(30, 160); s = rng.uniform(2.5, 4.5)
    fill(img, (np.abs(y - by + s * 0.6 * np.abs(np.sin((x - bx) / s * 1.6))) < 0.8) & (np.abs(x - bx) < s * 1.9), 'k')

scene = np.zeros((H, W), bool)  # architecture mask, for reflection

def windows(x0, y0, x1, y1, cols, rows, arch=True, col='k', sill='w'):
    cw = (x1 - x0) / cols; rh = (y1 - y0) / rows
    for i in range(cols):
        for j in range(rows):
            wx = x0 + cw * (i + .3); wy = y0 + rh * (j + .25); ww = cw * .4; wh = rh * .55
            m = rect(wx, wy, wx + ww, wy + wh)
            if arch: m |= ell(wx + ww / 2, wy, ww / 2, ww / 2 * 1.3)
            fill(img, m, col)
            fill(img, rect(wx - 1, wy + wh, wx + ww + 1, wy + wh + 1), sill)

def palazzo(x0, x1, top, wall, seed):
    r2 = np.random.default_rng(seed)
    m = rect(x0, top, x1, QY); global scene; scene |= m
    if wall == 'r': mix(img, m, 'r', 'k', 0.12)
    elif wall == 'y': mix(img, m, 'y', 'r', 0.18)
    elif wall == 'w': mix(img, m, 'w', 'y', 0.12)
    else: mix(img, m, 'w', 'b', 0.25)
    fill(img, rect(x0, top, x1, top + 2), 'k')                # cornice
    fill(img, rect(x0, top + 2, x1, top + 3), 'w')
    fill(img, rect(x0, top, x0 + 1, QY) | rect(x1 - 1, top, x1, QY), 'k')
    floors = max(2, int((QY - top) / 22))
    cols = max(2, int((x1 - x0) / 11))
    windows(x0 + 2, top + 6, x1 - 2, QY - 16, cols, floors, arch=r2.random() < .7)
    # a gothic loggia in the middle of the piano nobile on some
    if r2.random() < .5 and x1 - x0 > 40:
        lx0 = x0 + (x1 - x0) * .25; lx1 = x1 - (x1 - x0) * .25; ly = top + (QY - top) * .3
        fill(img, rect(lx0, ly, lx1, ly + 14), 'k')
        for k in np.arange(lx0 + 3, lx1 - 2, 5):
            fill(img, rect(k, ly + 3, k + 1.5, ly + 14), 'w')
        fill(img, rect(lx0 - 2, ly + 14, lx1 + 2, ly + 16), 'w')
        fill(img, rect(lx0 - 2, ly + 16, lx1 + 2, ly + 17), 'k')
    # water door
    dx = (x0 + x1) / 2
    fill(img, rect(dx - 4, QY - 13, dx + 4, QY) | ell(dx, QY - 13, 4, 5), 'k')
    # roof & funnel chimneys
    fill(img, rect(x0 + 1, top - 3, x1 - 1, top), 'r')
    for cx in r2.uniform(x0 + 4, x1 - 4, r2.integers(1, 4)):
        ch = r2.uniform(8, 14)
        fill(img, rect(cx - 1.5, top - ch, cx + 1.5, top), 'r')
        fill(img, poly([(cx - 4, top - ch - 4), (cx + 4, top - ch - 4), (cx + 1.5, top - ch), (cx - 1.5, top - ch)]), 'w')
        fill(img, rect(cx - 4, top - ch - 5, cx + 4, top - ch - 4), 'k')
        scene |= rect(cx - 4, top - ch - 5, cx + 4, top)

# --- campanile (left), brick with white belfry and green spire
cx0 = 62
palazzo(0, 44, 214, 'y', 1)
m = rect(cx0 - 15, 92, cx0 + 15, QY); scene |= m
mix(img, m, 'r', 'k', 0.1)
for k in range(cx0 - 12, cx0 + 13, 6): fill(img, rect(k, 104, k + 2, QY - 4), 'k')   # pilaster strips
mix(img, m & (np.abs(x - cx0) < 15) & (x > cx0 + 5), 'r', 'k', 0.35)
bel = rect(cx0 - 17, 64, cx0 + 17, 92); scene |= bel; fill(img, bel, 'w')
for k in range(4): fill(img, rect(cx0 - 14 + k * 8, 70, cx0 - 9 + k * 8, 90) | ell(cx0 - 11.5 + k * 8, 70, 2.5, 3), 'k')
fill(img, rect(cx0 - 19, 62, cx0 + 19, 65) | rect(cx0 - 19, 90, cx0 + 19, 93), 'k')
att = rect(cx0 - 14, 48, cx0 + 14, 62); fill(img, att, 'w'); scene |= att
fill(img, rect(cx0 - 10, 51, cx0 + 10, 59) & ((x.astype(int) % 5) == 0), 'k')
sp = poly([(cx0 - 15, 48), (cx0, 6), (cx0 + 15, 48)]); scene |= sp
mix(img, sp, 'g', 'k', np.clip((x - cx0 + 4) / 30, 0, .6))
fill(img, ell(cx0, 5, 3, 4), 'y'); fill(img, rect(cx0 - .5, 0, cx0 + 1, 3), 'k')

# --- palazzi along the quay
palazzo(78, 128, 230, 'w', 2)
palazzo(128, 160, 246, 'r', 3)
# --- domed church (Salute-ish), right of centre
dcx = 240
base = rect(dcx - 58, 214, dcx + 58, QY); scene |= base
mix(img, base, 'w', 'y', 0.1)
for k in [-50, -30, 30, 50]: fill(img, rect(dcx + k - 2, 222, dcx + k + 2, QY - 10), 'k') if False else mix(img, rect(dcx + k - 3, 222, dcx + k + 3, QY - 12), 'w', 'b', .4)
pd = poly([(dcx - 26, 222), (dcx, 196), (dcx + 26, 222)]); fill(img, pd, 'w'); scene |= pd
fill(img, poly([(dcx - 26, 222), (dcx, 196), (dcx + 26, 222)]) & ~poly([(dcx - 21, 220), (dcx, 200), (dcx + 21, 220)]), 'k')
fill(img, rect(dcx - 12, 262, dcx + 12, QY) | ell(dcx, 262, 12, 13), 'k')               # great door
fill(img, rect(dcx - 60, 212, dcx + 60, 215) | rect(dcx - 60, 290, dcx + 60, 292), 'k')
windows(dcx - 56, 224, dcx - 30, 286, 1, 2); windows(dcx + 30, 224, dcx + 56, 286, 1, 2)
steps = rect(dcx - 50, QY - 8, dcx + 50, QY)
fill(img, steps, 'w'); fill(img, steps & (y.astype(int) % 3 == 0), 'k')
# drum + dome
drum = rect(dcx - 40, 150, dcx + 40, 214); scene |= drum; mix(img, drum, 'w', 'y', .15)
for k in range(-36, 37, 9): fill(img, rect(dcx + k - 1, 156, dcx + k + 1, 212), 'k')
for k in range(-32, 33, 9): fill(img, rect(dcx + k - 1.5, 168, dcx + k + 2.5, 194) | ell(dcx + k + .5, 168, 2, 3), 'b')
# volutes
for sgn in (-1, 1):
    for j in range(4):
        vx = dcx + sgn * (44 + j * 2); vy = 186 + j * 8
        fill(img, (np.abs(np.hypot(x - vx, y - vy) - 5) < 1.2), 'k'); scene |= ell(vx, vy, 6, 6)
        fill(img, ell(vx, vy, 3.8, 3.8), 'w')
dome = ell(dcx, 150, 44, 46) & (y < 150); scene |= dome
mix(img, dome, 'w', 'b', np.clip(0.2 + (x - dcx + 20) / 80 + (150 - y) / 200, 0, .9))
for k in range(-4, 5):  # ribs
    fill(img, dome & (np.abs((x - dcx) - k * 10 * np.sqrt(np.clip(1 - ((150 - y) / 46) ** 2, 0, 1))) < .7), 'w' if k < 1 else 'k')
fill(img, rect(dcx - 46, 148, dcx + 46, 152), 'k')
lan = rect(dcx - 9, 92, dcx + 9, 108); scene |= lan; fill(img, lan, 'w'); fill(img, rect(dcx - 5, 95, dcx - 2, 105) | rect(dcx + 2, 95, dcx + 5, 105), 'k')
ld = ell(dcx, 92, 10, 10) & (y < 92); scene |= ld; mix(img, ld, 'w', 'b', .5)
fill(img, rect(dcx - 1, 66, dcx + 1, 84) | rect(dcx - 5, 72, dcx + 5, 74), 'k'); fill(img, ell(dcx, 64, 3, 3), 'y')
# right-side palazzi and a distant low island
palazzo(300, 342, 226, 'y', 5)
palazzo(342, 400, 240, 'b', 6)
isl = rect(160, 290, 182, QY); scene |= isl; mix(img, isl, 'w', 'b', .5)
# quay edge
quay = rect(0, QY - 4, W, QY); fill(img, quay, 'w'); fill(img, rect(0, QY - 1, W, QY), 'k'); scene |= quay
# macchiette on the quay: tiny figures, Guardi's flicks
for _ in range(34):
    fx = rng.uniform(4, 396); col = rng.choice(['k', 'k', 'r', 'b', 'y', 'w'])
    fh = rng.uniform(9, 13)
    fill(img, poly([(fx - 2.5, QY - 3), (fx - 1, QY - fh + 3), (fx + 1, QY - fh + 3), (fx + 2.5, QY - 3)]), col)
    fill(img, ell(fx, QY - fh + 1.5, 1.6, 1.8), 'k' if col == 'w' else 'w')
    if rng.random() < .3: fill(img, rect(fx - 2.5, QY - fh - .5, fx + 2.5, QY - fh + 1), 'k')  # tricorn

# --- water: reflections of the scene, broken into wavelets
wat = y >= QY
mix(img, wat, 'w', 'b', np.clip(0.35 + (y - QY) / 400, 0, .85))
src = img.copy()
wob = (3.5 * np.sin(y / 3.1 + x / 23) + 2 * np.sin(y / 1.7 - x / 11)).astype(int)
ry = (2 * QY - y).astype(int); rx = (x + wob * np.clip((y - QY) / 40, 0.2, 1.5)).astype(int).clip(0, W - 1)
ok = wat & (ry >= 0) & (ry < QY)
refl = np.zeros_like(img); refl[ok] = src[ry[ok], rx[ok]]
inscene = np.zeros((H, W), bool); inscene[ok] = scene[ry[ok], rx[ok]]
fade = (y - QY) / 160
keep = ok & inscene & (BAYER > fade + 0.1) & ((y.astype(int) % 4) != 0)
img[keep] = refl[keep]
# wavelets: short horizontal strokes, white and dark blue
for _ in range(1800):
    wx, wy = rng.uniform(0, W), rng.uniform(QY + 2, H)
    ln = 2 + (wy - QY) / 25 * rng.uniform(.5, 1.5)
    c = 'w' if rng.random() < .5 else ('b' if rng.random() < .7 else 'k')
    fill(img, rect(wx, wy, wx + ln, wy + 1 + (wy > 470)), c)

# --- foreground: striped mooring poles, a bragozzo with a painted sail, a gondola
for (px, c) in [(318, 'r'), (330, 'r'), (352, 'b'), (370, 'b')]:
    pm = rect(px, 330 + (px - 300) * .5, px + 4, 470 + (px - 300))
    fill(img, pm, 'w'); fill(img, pm & (((y + x * 0.0) // 8).astype(int) % 2 == 0), c)
    fill(img, pm & (x >= px + 3), 'k')
    fill(img, ell(px + 2, 330 + (px - 300) * .5, 3, 2), 'k')
    rr = rect(px, 470 + (px - 300), px + 4, 500 + (px - 300)) & (BAYER < .5) & (y.astype(int) % 3 != 0)
    fill(img, rr, c)
# bragozzo, left
bx, by = 96, 470
hull = poly([(bx - 70, by - 8), (bx + 70, by - 12), (bx + 56, by + 14), (bx - 58, by + 12)])
fill(img, hull, 'k'); fill(img, hull & (y < by - 3), 'r'); fill(img, hull & (np.abs(y - by + 3) < 1.2), 'y')
fill(img, ell(bx + 54, by - 4, 3, 3), 'w'); fill(img, ell(bx + 54, by - 4, 1.5, 1.5), 'k')  # the painted eye
fill(img, rect(bx - 1, 330, bx + 2, by - 8), 'k')
sail = poly([(bx + 2, 340), (bx + 70, 362), (bx + 66, by - 18), (bx + 2, by - 16)])
fill(img, sail, 'y'); fill(img, sail & (x > bx + 40), 'r')
ang = np.arctan2(y - 410, x - bx - 22); rr_ = np.hypot(x - bx - 22, y - 410)   # sun emblem
fill(img, sail & ((rr_ < 8) | ((rr_ < 15) & (np.cos(ang * 10) > 0.4))), 'r')
fill(img, sail & (rr_ < 4), 'y')
for k in range(5): fill(img, sail & (np.abs(y - 345 - k * 25 - (x - bx) * 0.3) < .6), 'k')
fill(img, poly([(bx - 2, 350), (bx - 50, by - 14), (bx - 2, by - 14)]), 'w')
fill(img, poly([(bx - 2, 350), (bx - 50, by - 14), (bx - 2, by - 14)]) & (np.abs(x - bx + 20) < 1), 'k')
fill(img, rect(bx + 2, by - 18, bx + 70, by - 16), 'k')
for (fx, c) in [(bx - 30, 'b'), (bx + 20, 'r')]:  # two sailors
    fill(img, rect(fx - 3, by - 26, fx + 3, by - 10), c); fill(img, ell(fx, by - 29, 2.6, 3), 'w')
    fill(img, rect(fx - 3, by - 33, fx + 3, by - 30), 'r')
# reflection of hull/sail
rs = (y > by + 14) & (y < by + 70) & (BAYER > (y - by) / 70) & (y.astype(int) % 3 != 0)
fill(img, rs & (np.abs(x - bx - 30 - 3 * np.sin(y / 2)) < 30), 'y')
fill(img, rs & (np.abs(x - bx + 5 - 3 * np.sin(y / 2)) < 50) & (y < by + 26), 'k')

# gondola, centre-right, long and black with ferro and gondolier
gx, gy = 236, 548
g = poly([(gx - 90, gy - 22), (gx - 70, gy - 2), (gx + 70, gy - 2), (gx + 96, gy - 26), (gx + 80, gy + 6), (gx - 74, gy + 6)])
fill(img, g, 'k'); fill(img, g & (np.abs(y - gy + 1) < .8) & (x > gx - 70) & (x < gx + 70), 'y')
ferro = rect(gx - 98, gy - 34, gx - 92, gy - 20); fill(img, ferro, 'w')
for k in range(5): fill(img, rect(gx - 98, gy - 32 + k * 3, gx - 88, gy - 31 + k * 3), 'w')
fill(img, ferro & (x > gx - 93), 'k')
felze = rect(gx - 30, gy - 24, gx + 10, gy - 2) | ell(gx - 10, gy - 24, 20, 8) & (y < gy - 24)
fill(img, felze, 'k'); fill(img, rect(gx - 22, gy - 18, gx - 14, gy - 8), 'y'); fill(img, rect(gx - 6, gy - 18, gx + 2, gy - 8), 'y')
fill(img, ell(gx - 10, gy - 30, 3, 1.5), 'r')
# gondolier, standing aft, oar raked to the water
ox = gx + 58
fill(img, rect(ox - 4, gy - 40, ox + 4, gy - 22), 'w'); fill(img, rect(ox - 4, gy - 40, ox + 4, gy - 22) & (y.astype(int) % 4 < 2), 'r')
fill(img, rect(ox - 4, gy - 22, ox + 4, gy - 4), 'k')
fill(img, ell(ox, gy - 45, 3.5, 4), 'w'); fill(img, rect(ox - 6, gy - 51, ox + 6, gy - 49) | rect(ox - 3.5, gy - 55, ox + 3.5, gy - 50), 'y')
fill(img, rect(ox - 3.5, gy - 51.5, ox + 3.5, gy - 50), 'r')
oar = (np.abs((y - (gy - 38)) - (x - ox) * 1.6) < 1.6) & (y > gy - 38) & (y < gy + 30)
fill(img, oar, 'k')
fill(img, poly([(gx + 82, gy - 12), (gx + 90, gy - 22), (gx + 96, gy - 14)]), 'k')  # forcola
# gondola shadow in water
gs = (y > gy + 6) & (y < gy + 36) & (np.abs(x - gx) < 90 - (y - gy) * 1.5) & (y.astype(int) % 3 != 2) & (BAYER < .7)
fill(img, gs, 'k')
save(img)
