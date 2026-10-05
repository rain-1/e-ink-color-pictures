"""Night: Patinir's Charon crossing the Styx, after dark — Saturn at opposition overhead."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from PIL import Image, ImageDraw
from ink import *

rng = np.random.default_rng(1520)
img = canvas('k')
x, y = grid()
def poly(pts):
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).polygon([tuple(p) for p in pts], fill=255); return np.array(m) > 0
def ell(cx, cy, rx, ry): return ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 < 1
def rect(x0, y0, x1, y1): return (x >= x0) & (x < x1) & (y >= y0) & (y < y1)
def lines(pts, w):
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).line([tuple(p) for p in pts], fill=255, width=w); return np.array(m) > 0

HZ = 196
# --- sky: black, a faint blue band at the horizon, stars, the Milky Way as blue dust
sky = y < HZ
mix(img, sky & (y > HZ - 40), 'k', 'b', np.clip((y - HZ + 40) / 40, 0, 1) * 0.45)
mw = vnoise((H, W), 30, rng, 4)
band = np.exp(-((y - 40 - (x - 200) * 0.45) / 38) ** 2)
fill(img, sky & (rng.random((H, W)) < band * mw ** 2 * 0.22), 'b')
fill(img, sky & (rng.random((H, W)) < band * mw ** 3 * 0.06), 'w')
for _ in range(110):
    sx, sy = rng.uniform(0, W), rng.uniform(0, HZ - 12)
    b = rng.random()
    if b > 0.93:
        c = rng.choice(['w', 'y', 'b'])
        fill(img, ((np.abs(x - sx) < 3) & (np.abs(y - sy) < .6)) | ((np.abs(y - sy) < 3) & (np.abs(x - sx) < .6)), c)
    elif b > 0.6:
        fill(img, rect(sx, sy, sx + 2, sy + 2), 'w')
    else:
        img[int(sy), int(sx)] = Wt
# Saturn, rings nearly edge-on this year
SX, SY = 96, 62
fill(img, ell(SX, SY, 22, 22) & ~ell(SX, SY, 10, 10), 'k')  # clear a patch
fill(img, ell(SX, SY, 6, 5.5), 'y'); fill(img, ell(SX, SY, 6, 5.5) & (y > SY + 2), 'r') if False else None
fill(img, ell(SX, SY, 6, 5.5) & (np.abs(y - SY - 1.5) < .7), 'r')
fill(img, (np.abs(y - SY - (x - SX) * 0.12) < .7) & (np.abs(x - SX) < 17) & ~ell(SX, SY - 1, 6, 4.5), 'y')
for k in (1, 2, 3): img[int(SY + k * 4 - 8), int(SX + 24 + k * 3)] = Wt  # moons
img[SY + 6, SX - 28] = Wt

# --- distant land: the far shore, black hills edged blue
far = HZ - 6 + 8 * vnoise((1, W), 40, rng, 3)[0] - 6
fm = (y >= far[None, :]) & (y < HZ + 6)
fill(img, fm, 'k'); fill(img, fm & ~np.roll(fm, 1, 0), 'b')

# --- the Styx: wide black water widening toward us, faint blue ripple strokes
lb = 200 - 40 - (y - HZ) * 0.75    # left bank x
rb = 200 + 40 + (y - HZ) * 0.2   # right bank x
wob = 6 * np.sin(y / 23) + 4 * np.sin(y / 9)
water = (y >= HZ) & (x > lb + wob) & (x < rb + wob * .6)
fill(img, water, 'k')
for _ in range(750):
    wx, wy = rng.uniform(0, W), rng.uniform(HZ + 2, H)
    if not water[int(wy), int(wx)]: continue
    ln = 1 + (wy - HZ) / 30 * rng.uniform(.5, 1.6)
    fill(img, rect(wx, wy, wx + ln, wy + 1), 'b' if rng.random() < .94 else 'w')
# Saturn's reflection
fill(img, water & (np.abs(x - 228 - 2 * np.sin(y)) < 2) & (y > HZ + 4) & (y < HZ + 60) & ((y.astype(int) % 4) == 0), 'y')

# --- left bank: Elysium, dim — dark green meadow, pale tiny souls, a crystal fountain
L = (y >= HZ) & (x <= lb + wob)
mix(img, L, 'k', 'g', np.clip(0.18 + vnoise((H, W), 20, rng, 3) * .35 - (y - HZ) / 900, 0, .5))
fill(img, L & ~np.roll(L, -1, 1), 'b')
for _ in range(18):  # little trees
    tx, ty = rng.uniform(0, 150), rng.uniform(HZ + 4, 330)
    if not L[int(ty), int(tx)]: continue
    s = 3 + (ty - HZ) / 22
    tr = ell(tx, ty - s * 1.6, s, s * 1.7); fill(img, tr, 'k'); fill(img, tr & (BAYER < .25), 'g')
    fill(img, rect(tx - .7, ty - s * .4, tx + .8, ty + 1), 'k')
fx, fy = 70, 262   # fountain: a white gothic spire of light
fill(img, poly([(fx - 7, fy), (fx, fy - 40), (fx + 7, fy)]), 'w')
fill(img, poly([(fx - 7, fy), (fx, fy - 40), (fx + 7, fy)]) & (x > fx) & (BAYER < .5), 'b')
fill(img, ell(fx, fy + 2, 14, 3), 'b'); fill(img, (np.abs(np.hypot((x - fx) / 14, (y - fy - 2) / 3) - 1) < .12), 'w')
for (ax, ay) in [(46, 252), (98, 270), (30, 300), (112, 300), (60, 330), (20, 270)]:  # souls with angels
    fill(img, rect(ax - 1.5, ay - 8, ax + 1.5, ay), 'w'); img[int(ay - 10), int(ax)] = Wt
    fill(img, rect(ax + 4, ay - 9, ax + 7, ay), 'w'); fill(img, poly([(ax + 7, ay - 9), (ax + 12, ay - 14), (ax + 8, ay - 5)]), 'b')

# --- right bank: Hades — black crags, a tower with red windows, the fires
R = (y >= HZ - 30) & (x >= rb + wob * .6)
cr = HZ - 20 - 70 * np.exp(-((x[0] - 350) / 40) ** 2) - 30 * np.exp(-((x[0] - 290) / 20) ** 2) + 10 * vnoise((1, W), 8, rng, 2)[0]
R = (x >= rb + wob * .6) & (y >= cr[None, :]) & (y >= HZ - 120)
fill(img, R, 'k')
rz = R & (y > HZ) & (vnoise((H, W), 10, rng, 3) > .66)
fill(img, rz & ((x + y).astype(int) % 5 == 0), 'b')                        # strata of the crags
bank = R & ~np.roll(R, 2, 1) & (y > HZ)
fill(img, bank, 'r')
edge = R & ~np.roll(R, 1, 0)
fill(img, edge, 'r')
# fire glow, the only warm thing at night
gx, gy = 330, HZ + 30
gr = np.hypot((x - gx) / 1.6, y - gy)
glow = R & (gr < 60)
mix(img, glow, 'k', 'r', np.clip(1 - gr / 60, 0, 1) ** 1.6 * .9)
fire = R & (gr < 26) & (vnoise((H, W), 5, rng, 2) > .5 - (26 - gr) / 60)
fill(img, fire, 'y'); fill(img, R & (gr < 14), 'y'); fill(img, R & (gr < 6), 'w')
# silhouettes against the fire: the gate and the dog
fill(img, rect(300, HZ + 2, 306, HZ + 50) | rect(354, HZ + 2, 360, HZ + 50) | (ell(330, HZ + 4, 30, 14) & ~ell(330, HZ + 4, 24, 9) & (y < HZ + 4)), 'k')
cb = ell(330, HZ + 46, 12, 5) | ell(318, HZ + 38, 4, 4) | ell(326, HZ + 36, 4, 4) | ell(334, HZ + 38, 4, 4)
fill(img, cb, 'k')
# tower
tx0 = 368
fill(img, rect(tx0, HZ - 150, tx0 + 18, HZ + 30), 'k')
fill(img, poly([(tx0 - 3, HZ - 150), (tx0 + 9, HZ - 176), (tx0 + 21, HZ - 150)]), 'k')
for k in range(5): fill(img, rect(tx0 + 7, HZ - 140 + k * 26, tx0 + 11, HZ - 132 + k * 26), 'r')
fill(img, (np.abs(x - tx0 - 9) < 9.5) & (np.abs(y - HZ + 150) < .6), 'r')
# a few crows over Hades
for (bx, by) in [(290, 100), (312, 88), (340, 72)]:
    fill(img, (np.abs(y - by + 2 * np.abs(np.sin((x - bx) / 2.5))) < .8) & (np.abs(x - bx) < 5), 'r')

# --- Charon's boat in the middle of the water, lantern at the bow
bx, by = 212, 450
hull = poly([(bx - 70, by - 10), (bx + 60, by - 14), (bx + 48, by + 4), (bx - 58, by + 6)])
fill(img, hull, 'k'); fill(img, (hull & ~np.roll(hull, 2, 0)), 'y'); fill(img, hull & (np.abs(y - by + 3) < .7), 'b')
# lantern on a post at the bow
lx, ly = bx - 66, by - 40
fill(img, rect(lx - .7, ly, lx + 1, by - 10), 'w')
lr = np.hypot((x - bx - 4) / 2.8, (y - by + 34) / 1.9)
mix(img, (lr < 30) & ~hull & (y < by - 10) & (img[..., 0] == 0) & (img[..., 2] == 0), 'k', 'y', np.clip(1 - lr / 30, 0, 1) ** 1.6 * .75)
fill(img, rect(lx - 3, ly, lx + 4, ly + 9), 'y'); fill(img, rect(lx - 4, ly - 1, lx + 5, ly), 'w'); fill(img, rect(lx - 1, ly + 3, lx + 2, ly + 6), 'w')
# lantern's reflection: a broken yellow column
fill(img, water & (np.abs(x - lx - 3 * np.sin(y / 3)) < 3) & (y > by + 6) & (y < by + 120) & ((y.astype(int) % 5) < 2) & (BAYER > (y - by) / 130), 'y')
# Charon: tall, hunched, pushing the pole — black against the lantern light
cx = bx + 36
ch = poly([(cx - 11, by - 12), (cx - 7, by - 56), (cx + 1, by - 66), (cx + 10, by - 58), (cx + 13, by - 30), (cx + 9, by - 12)])
fill(img, ch, 'k'); mix(img, ch & (x > cx - 4), 'k', 'r', 0.35)
fill(img, ch & ((~np.roll(ch, 1, 1)) | (~np.roll(ch, 2, 1))), 'y')
fill(img, ch & (np.abs(x - cx - 2 - (y - by + 40) * 0.12) < .7) & (y > by - 50), 'k')   # cloak fold
fill(img, ell(cx + 2, by - 70, 5, 6), 'k'); fill(img, ell(cx + 2, by - 70, 5, 6) & ~np.roll(ell(cx + 2, by - 70, 5, 6), 1, 1), 'y')
fill(img, lines([(cx - 26, by - 96), (cx + 34, by + 60)], 2), 'w'); fill(img, lines([(cx - 2, by - 48), (cx - 12, by - 60)], 3), 'k')
# the passenger: one pale soul, seated, facing the far bank
sx0 = bx - 18
fill(img, ell(sx0, by - 22, 7, 12) & (y < by - 10), 'w'); fill(img, ell(sx0 - 1, by - 38, 4.5, 5), 'w')
fill(img, ell(sx0, by - 22, 7, 12) & (y < by - 10) & (x > sx0 + 2) & (BAYER < .5), 'b')
# wake behind the boat
for k in range(8):
    fill(img, water & (np.abs(y - by - 10 - k * 6) < .7) & (np.abs(x - bx - 40 - k * 9) < 8 + k * 2), 'b')

# --- foreground: a black bank with reeds, the edge of the frame
fg = (y > 560 + 10 * np.sin(x / 30)) | ((x < 30 + (y - 470) * .4) & (y > 470))
fill(img, fg, 'k')
for rx in np.arange(0, 140, 4) + rng.uniform(-2, 2, 35):
    top = rng.uniform(470, 545); lean = rng.uniform(-.15, .15)
    fill(img, (np.abs(x - rx - (y - 600) * lean) < .7) & (y > top) & (y < 600), 'g')
    if rng.random() < .3: fill(img, ell(rx + (top - 600) * lean, top, 1.5, 4), 'r')
save(img)
