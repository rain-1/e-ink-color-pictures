"""Afternoon: a survey sheet of the morning's world, seen straight down — for Maya Lin (b. 5 Oct 1959)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from ink import *

rng = np.random.default_rng(1959)
img = canvas('w')
x, y = grid()
FD = '/usr/share/fonts/truetype/'
def font(name, size): return ImageFont.truetype(FD + name, size)
SERIF_I = 'liberation/LiberationSerif-Italic.ttf'; SERIF = 'liberation/LiberationSerif-Regular.ttf'
SERIF_B = 'liberation/LiberationSerif-Bold.ttf'; SANS = 'dejavu/DejaVuSans.ttf'
def text_mask(xy, s, f, anchor='mm', spacing=0, angle=0):
    m = Image.new('1', (W, H), 0); d = ImageDraw.Draw(m); d.fontmode = '1'
    if spacing:
        tw = sum(d.textlength(c, font=f) + spacing for c in s) - spacing
        cx = xy[0] - tw / 2
        for c in s:
            d.text((cx, xy[1]), c, font=f, fill=1, anchor='lm'); cx += d.textlength(c, font=f) + spacing
    else:
        d.text(xy, s, font=f, fill=1, anchor=anchor)
    if angle: m = m.rotate(angle, center=xy, resample=Image.NEAREST)
    return np.array(m) > 0
def label(xy, s, f, c='k', halo=True, **kw):
    m = text_mask(xy, s, f, **kw)
    if halo:
        hm = m.copy()
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1): hm |= np.roll(np.roll(m, dx, 1), dy, 0)
        fill(img, hm & ~m, 'w')
    fill(img, m, c)
def lines_mask(pts, width):
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).line([tuple(p) for p in pts], fill=255, width=width, joint='curve'); return np.array(m) > 0

M0, M1, MT, MB = 14, 386, 14, 512   # neatline
inside = (x >= M0) & (x < M1) & (y >= MT) & (y < MB)

# --- terrain: sea to the north, river valley winding up the middle, crag ridge east
tt = np.linspace(0, 1, 300)
rvx = 180 + 95 * np.sin(tt * 9.0 + 0.3) * (1 - tt * .35) - 10 * tt
rvy = MB + 10 - tt * (MB - 90)
from math import inf
dist = np.full((H, W), 1e9)
for i in range(0, 300, 2):
    dist = np.minimum(dist, (x - rvx[i]) ** 2 + (y - rvy[i]) ** 2)
dist = np.sqrt(dist)
h = vnoise((H, W), 120, rng, 5) * 0.9
h += np.clip(dist / 140, 0, 1) ** 1.3 * 0.9                      # valley
ridge = np.exp(-((x - 318 - 15 * np.sin(y / 50)) / 26) ** 2) * np.clip((y - 110) / 80, 0, 1)
h += ridge * (0.9 + 0.6 * vnoise((H, W), 18, rng, 3))           # crags
h -= np.clip((150 - y) / 70, 0, 1.5) * 1.2                       # sea to the north
h = h - 0.35
sea = h < 0

# hillshade, light from the north-west
gy_, gx_ = np.gradient(h)
g_s = np.percentile(np.hypot(gx_, gy_)[~sea & inside], 90)
gx_ /= g_s; gy_ /= g_s
shade = np.clip((gx_ * 0.7 + gy_ * 0.7) * 0.45 + 0.2, 0, 1)
land = inside & ~sea
lowland = land & (h < 0.22)
mix(img, land, 'w', 'b', np.clip(shade * 0.65, 0, 0.6))
mix(img, lowland & (shade < 0.25), 'w', 'y', 0.38)
mix(img, land & (h >= 0.22) & (shade < 0.12), 'w', 'y', 0.12)

# sea: blue, with coastal ripple lines and deeper tint
sm = inside & sea
mix(img, sm, 'w', 'b', np.clip(0.45 + (-h) * 0.6, 0, 0.85))
for k in range(1, 7):
    fill(img, sm & (np.abs(h + k * 0.035) < 0.004 + 0.002 * (k == 1)), 'w')
fill(img, inside & sea & ~np.roll(sea, 1, 0) | inside & sea & ~np.roll(sea, -1, 1) | inside & sea & ~np.roll(sea, 1, 1) | inside & sea & ~np.roll(sea, -1, 0), 'k')

# forests: patches on mid slopes, green screen + tree symbols
fz = vnoise((H, W), 45, rng, 3)
forest = land & (fz > 0.56) & (h > 0.08) & (h < 0.75) & (dist > 14)
mix(img, forest, 'w', 'g', 0.45)
fill(img, forest & ~np.roll(forest, 1, 0) | forest & ~np.roll(forest, 1, 1), 'g')
for _ in range(1600):
    tx, ty = rng.uniform(M0, M1), rng.uniform(MT, MB)
    if forest[int(ty), int(tx)]:
        r = ((x - tx) ** 2 + (y - ty) ** 2)
        if rng.random() < .5:
            fill(img, (r < 6.5) & (r > 2.2), 'g'); img[int(ty) + 3, int(tx)] = G
        else:
            fill(img, poly_m := ((np.abs(x - tx) < (y - ty + 4) * 0.6) & (y > ty - 4) & (y < ty + 2)), 'g')
# vineyards on south-facing low slopes: ranks of dots
vine = land & (fz < 0.3) & (h > 0.05) & (h < 0.4) & (gy_ < -0.2) & (dist > 12)
fill(img, vine & (y.astype(int) % 4 == 0) & (x.astype(int) % 3 == 0), 'g')
fill(img, vine & ~np.roll(vine, 1, 1) & (y.astype(int) % 2 == 0), 'k')

# crags: black hachures down the steep faces
steep = np.hypot(gx_, gy_)
crag = land & (steep > 1.25) & (h > 0.55) & (ridge > 0.3)
hx = (x + 0.6 * y).astype(int) % 3 == 0
fill(img, crag & hx, 'k')
fill(img, crag & (steep > 2.2) & (BAYER < .5), 'k')

# contours: every 0.05, index every 0.25
def iso(step):
    q = np.floor(h / step)
    return (q != np.roll(q, 1, 0)) | (q != np.roll(q, 1, 1))
cont = land & iso(0.075)
idx = land & iso(0.30); idx |= np.roll(idx, 1, 1) & land
fill(img, cont & ~crag, 'k')
fill(img, idx, 'k')
# spot heights
placed = []
for _ in range(14):
    sx, sy = rng.integers(M0 + 20, M1 - 20), rng.integers(140, MB - 20)
    win = h[sy - 15:sy + 15, sx - 15:sx + 15]
    j, i = np.unravel_index(win.argmax(), win.shape); px, py = sx - 15 + i, sy - 15 + j
    if sea[py, px] or h[py, px] < 0.3 or any(abs(px - a) < 40 and abs(py - b) < 30 for a, b in placed) or abs(px - 314) < 30 and py < 180: continue
    placed.append((px, py))
    fill(img, ((x - px) ** 2 + (y - py) ** 2 < 3), 'k')
    label((px + 4, py - 6), f"{int(h[py, px] * 600)}", font(SERIF, 11), anchor='lm')

# --- the river Meuse, with tributaries
pts = list(zip(rvx, rvy))
riv = lines_mask(pts[:200], 7) | lines_mask(pts[150:], 5) | lines_mask(pts[230:], 4)
riv &= inside
fill(img, riv, 'b')
edge = riv & (~np.roll(riv, 1, 0) | ~np.roll(riv, -1, 0) | ~np.roll(riv, 1, 1) | ~np.roll(riv, -1, 1))
fill(img, edge, 'k')
for (sx, sy, n) in [(40, 300, 1), (90, 470, 2), (370, 380, 3), (30, 180, 4)]:
    r2 = np.random.default_rng(n); px, py = sx, sy; tp = [(px, py)]
    for _ in range(40):
        i = np.argmin((rvx - px) ** 2 + (rvy - py) ** 2)
        dx, dy = rvx[i] - px, rvy[i] - py; d = np.hypot(dx, dy) + 1e-6
        if d < 5: break
        px += dx / d * 5 + r2.normal(0, 2.5); py += dy / d * 5 + r2.normal(0, 2.5); tp.append((px, py))
    tm = lines_mask(tp, 2) & inside & ~sea
    fill(img, tm, 'b')

# --- roads: red with black casing, one along each bank, one up to the castle
def road(p, w=3):
    cas = lines_mask(p, w + 2) & inside & ~sea; core = lines_mask(p, w) & inside & ~sea
    fill(img, cas & ~riv, 'k'); fill(img, core & ~riv, 'r')
off = 16
road([(rvx[i] - off, rvy[i]) for i in range(0, 300, 5)])
road([(rvx[175] + off * 1.4, rvy[175] + 2), (rvx[150] + 40, rvy[150]), (280, rvy[120] - 30), (300, rvy[120] - 60), (316, 150)], 2)
# bridges
for i in (60, 175):
    fill(img, lines_mask([(rvx[i] - off, rvy[i]), (rvx[i] + off * 1.4, rvy[i] + 2)], 5) & inside, 'k')
    fill(img, lines_mask([(rvx[i] - off + 2, rvy[i]), (rvx[i] + off * 1.4 - 2, rvy[i] + 2)], 2) & inside, 'w')
# railway: black ticked line along the west
rp = [(M0 + 6 + 8 * np.sin(k / 30), k) for k in range(MB, 150, -4)]
rm = lines_mask(rp, 2) & inside; fill(img, rm, 'k')
for (px, py) in rp[::3]: fill(img, (np.abs(y - py) < .8) & (np.abs(x - px) < 3.5), 'k')

# --- settlements: black blocks, churches, a castle
def town(cx, cy, n, r, name, side=1, big=False):
    r2 = np.random.default_rng(int(cx * cy))
    for _ in range(n):
        bx, by = cx + r2.normal(0, r), cy + r2.normal(0, r * .7)
        bw, bh = r2.uniform(2, 5), r2.uniform(2, 4)
        if not riv[int(by), int(bx)] and not sea[int(by), int(bx)]:
            fill(img, (np.abs(x - bx) < bw / 2) & (np.abs(y - by) < bh / 2), 'k')
    # church: circle + cross
    fill(img, (np.abs(np.hypot(x - cx, y - cy) - 3) < .9), 'k'); fill(img, (np.hypot(x - cx, y - cy) < 2.2), 'w')
    fill(img, ((np.abs(x - cx) < .6) & (np.abs(y - cy + 6) < 3)) | ((np.abs(y - cy + 6.5) < .6) & (np.abs(x - cx) < 2)), 'k')
    f = font(SERIF_B if big else SERIF, 14 if big else 12)
    label((cx + side * (r + 6), cy + 1), name, f, anchor='lm' if side > 0 else 'rm')

town(rvx[60] - 34, rvy[60] + 2, 40, 11, 'Dinant', side=-1, big=True)
town(rvx[175] + 32, rvy[175] - 6, 26, 8, 'Bouvignes', side=1)
town(rvx[262] - 30, rvy[262] + 14, 14, 6, 'Anseremme', side=-1)
town(84, 230, 10, 6, 'Falmignoul', side=1)
# castle on the crag
ccx, ccy = 314, 152
fill(img, (np.abs(x - ccx) < 9) & (np.abs(y - ccy) < 6), 'k'); fill(img, (np.abs(x - ccx) < 6) & (np.abs(y - ccy) < 3), 'r')
for dx in (-9, 9):
    for dy in (-6, 6): fill(img, (x - ccx - dx) ** 2 + (y - ccy - dy) ** 2 < 6, 'k')
label((ccx - 22, ccy), 'Ruine', font(SERIF_I, 11), anchor='rm')
# the hermit's cave
cvx, cvy = 64, 478
fill(img, ((x - cvx) ** 2 + (y - cvy) ** 2 < 16) & (y < cvy), 'k'); fill(img, (np.abs(y - cvy) < 1) & (np.abs(x - cvx) < 5), 'k')
label((cvx + 9, cvy - 1), 'Grotte S. Jérôme', font(SERIF_I, 11), anchor='lm')

# water names, spaced italic
label((200, 62), 'MER  DU  NORD', font(SERIF_I, 15), c='w', halo=False, spacing=4)
label((200, 86), '( l’horizon de Patinir )', font(SERIF_I, 11), c='w', halo=False)
label((210, 497), 'la Meuse', font(SERIF_I, 13), c='b')
label((330, 330), 'ROCHERS', font(SERIF_I, 12), angle=80, spacing=2)
label((80, 410), 'Bois de Freyr', font(SERIF_I, 11), c='g')

# grid ticks and neatline
fill(img, ~inside, 'w')
for k in range(M0, M1 + 1, 31):
    fill(img, (np.abs(x - k) < .6) & (((y >= MT - 6) & (y < MT)) | ((y >= MB) & (y < MB + 6))), 'k')
for k in range(MT, MB + 1, 31):
    fill(img, (np.abs(y - k) < .6) & (((x >= M0 - 6) & (x < M0)) | ((x >= M1) & (x < M1 + 6))), 'k')
nl = (((np.abs(x - M0 + .5) < 1) | (np.abs(x - M1 + .5) < 1)) & (y >= MT) & (y <= MB)) | (((np.abs(y - MT + .5) < 1) | (np.abs(y - MB + .5) < 1)) & (x >= M0) & (x <= M1))
fill(img, nl, 'k')
# grid lines faint inside the map
fill(img, inside & ~sea & (((x - M0) % 62 == 0) | ((y - MT) % 62 == 0)) & (BAYER < .35), 'k')

# north arrow
nx, ny = 356, 470
fill(img, (np.abs(np.hypot(x - nx, y - ny) - 15) < .8), 'k')
fill(img, (np.abs(x - nx) < (y - ny + 15) * 0.25) & (y > ny - 15) & (y < ny + 4) & (x <= nx), 'k')
fill(img, (np.abs(x - nx) < (y - ny + 15) * 0.25) & (y > ny - 15) & (y < ny + 4) & (x > nx), 'r')
label((nx, ny - 24), 'N', font(SERIF_B, 12))

# title block
label((200, 535), 'CARTE  DU  PAYS  DE  PATINIR', font(SERIF_B, 17), halo=False, spacing=1)
label((200, 556), 'la Meuse à Dinant, levée d’en haut  ·  5 octobre', font(SERIF_I, 12), halo=False)
# scale bar
for i in range(5):
    fill(img, (x >= 120 + i * 32) & (x < 152 + i * 32) & (y >= 574) & (y < 580), 'k' if i % 2 == 0 else 'w')
fill(img, (((y == 574) | (y == 579)) & (x >= 120) & (x < 280)) | (((x == 120) | (x == 279)) & (y >= 574) & (y < 580)), 'k')
for i, s in enumerate(['0', '1', '2', '3', '4', '5']):
    label((120 + i * 32, 590), s, font(SERIF, 11), halo=False, anchor='lm' if i == 5 else 'mm')
# legend swatches at left and right of the scale bar
for (lx, c, name) in [(22, 'r', 'route'), (22, 'b', 'rivière'), (300, 'g', 'bois'), (300, 'y', 'prés')]:
    ly = 576 if name in ('route', 'bois') else 590
    fill(img, (x >= lx) & (x < lx + 14) & (np.abs(y - ly) < 3), c); fill(img, ((x == lx) | (x == lx + 13)) & (np.abs(y - ly) < 3), 'k')
    label((lx + 18, ly), name, font(SERIF_I, 11), halo=False, anchor='lm')
save(img)
