# Midday — "46 rue Hippolyte-Maindron". The Paris studio Giacometti kept from 1926 until
# he died: 23 square metres, a skylight, walls covered in drawings scratched straight onto
# the plaster, plaster dust everywhere. Mostly black and white screened into greys (the
# studio was grey); the skylight's noon light in yellow; one red jumper on the chair.
# Every object is placed: the big Walking Man on his stand, the tall Standing Woman on the
# turntable, tiny figures on huge bases, bottles, brushes, the stove and its pipe.
import math, numpy as np
from PIL import Image, ImageDraw
from common import *

rng = np.random.default_rng(1926)
im = Image.new("RGB", (W, H), Wh); d = ImageDraw.Draw(im)
yy, xx = np.mgrid[0:H, 0:W].astype(float)
VX, VY = 200, 250                      # vanishing point
BW = (70, 95, 330, 405)                # back wall rect
bx0, by0, bx1, by1 = BW
noise = fbm(H, W, seed=2, base=8)

# ---------- room shell
ceil = [(0, 0), (W, 0), (bx1, by0), (bx0, by0)]
lwall = [(0, 0), (bx0, by0), (bx0, by1), (0, H)]
rwall = [(W, 0), (bx1, by0), (bx1, by1), (W, H)]
floor = [(0, H), (bx0, by1), (bx1, by1), (W, H)]
tone_poly(im, ceil, 0.12 + noise*0.15, [K, Wh])
tone_poly(im, lwall, 0.36 + (noise-0.5)*0.4 + (1-yy/H)*0.1, [K, Wh])
tone_poly(im, rwall, 0.22 + (noise-0.5)*0.4, [K, Wh])
tone_poly(im, floor, 0.30 + (noise-0.5)*0.5 - (yy-400)/1200, [K, Wh])
tone_poly(im, [(bx0, by0), (bx1, by0), (bx1, by1), (bx0, by1)], 0.80 + (noise-0.5)*0.35, [K, Wh])
for a, b in (((0, 0), (bx0, by0)), ((W, 0), (bx1, by0)), ((0, H), (bx0, by1)), ((W, H), (bx1, by1))):
    d.line([a, b], fill=K, width=2)
d.rectangle(BW, outline=K, width=2)

# skylight in the ceiling: yellow noon, mullions
sky = [(120, 0), (300, 0), (265, 70), (150, 70)]
d.polygon(sky, fill=Y)
for i in range(1, 5):
    t = i/5
    d.line(((120+180*t), 0, 150+115*t, 70), fill=K, width=2)
for t in (0.33, 0.66):
    d.line((120+30*t, 70*t, 300-35*t, 70*t), fill=K, width=2)
d.polygon(sky, outline=K)
# the noon light: the skylight's image thrown onto the floor, screened yellow
patch = [(95, 470), (265, 455), (330, 590), (60, 600)]
m = polymask(patch)
a = np.asarray(im).copy()
a[m & (screen(H, W) < 0.55 + (noise-0.5)*0.4)] = Y
# faint rays in the dusty air
ray = polymask([(150, 70), (265, 70), (330, 590), (60, 600)]) & ~m
a[ray & (screen(H, W) < 0.07)] = Y
im = Image.fromarray(a); d = ImageDraw.Draw(im)

# ---------- back wall: drawings scratched into plaster
def wall_head(cx, cy, s):
    scribble(d, cx, cy, 7*s, 10*s, 9, rng, K)
    d.line((cx, cy-3*s, cx, cy+4*s), fill=K)
    d.line((cx-4*s, cy-2*s, cx+4*s, cy-2*s), fill=K)
    d.line((cx-6*s, cy+14*s, cx, cy+9*s, cx+6*s, cy+14*s), fill=K)
for (cx, cy, s) in ((112, 150, 2.6), (175, 140, 1.6), (296, 150, 2.2), (240, 190, 1.4), (100, 250, 1.3), (160, 215, 1.2)):
    wall_head(cx, cy, s)
# standing figures sketched on the wall
for x in (205, 225, 285, 300, 315):
    h = rng.uniform(45, 70); y = rng.uniform(200, 240)
    for k in range(3):
        d.line([(x+rng.normal(0, 1), y), (x+rng.normal(0, 1.5), y+h*0.45), (x+rng.normal(0, 1), y+h)], fill=K)
    d.ellipse((x-2, y-5, x+2, y), fill=K)
# a word and numbers, as he did: phone numbers and notes on the wall
from PIL import ImageFont
f = ImageFont.load_default(size=14); d.fontmode = "1"
d.text((196, 100), "1926", fill=K, font=f); d.text((150, 262), "Annette", fill=K, font=f); d.text((220, 120), "Diego", fill=K, font=f)
for _ in range(40):
    x = rng.uniform(bx0+4, bx1-4); y = rng.uniform(by0+5, 300)
    d.line((x, y, x+rng.uniform(-14, 14), y+rng.uniform(-10, 10)), fill=K)
# a door on the back wall, ajar
d.rectangle((262, 255, 312, 405), fill=K)
d.polygon([(262, 255), (286, 262), (286, 400), (262, 405)], fill=Wh, outline=K)
d.ellipse((280, 330, 284, 334), fill=K)

# ---------- right wall: easel with a portrait in progress
def quad(p, fill=None, outline=K):
    d.polygon(p, fill=fill, outline=outline)
can = [(348, 150), (392, 128), (392, 330), (348, 320)]
tone_poly(im, can, 0.6 + (noise-0.5)*0.3, [K, Wh, Y])
d.polygon(can, outline=K)
scribble(d, 371, 205, 11, 18, 12, rng, K)
for k in range(10):
    d.line((356+rng.uniform(0, 30), 250+rng.uniform(0, 30), 356+rng.uniform(0, 30), 320), fill=K)
d.line((351, 140, 362, 560), fill=K, width=3); d.line((389, 120, 380, 580), fill=K, width=3)
d.line((370, 115, 371, 550), fill=K, width=2)
d.line((345, 330, 395, 340), fill=K, width=4)

# ---------- left wall: shelves of small plaster heads, bottles, tins
for sy, sx0, sx1 in ((210, 8, 62), (280, 6, 62)):
    yb = sy + (62 - sx0)*0  # shelves recede slightly
    d.polygon([(sx0, sy+20), (sx1, sy), (sx1, sy+4), (sx0, sy+26)], fill=Wh, outline=K)
    for i in range(6):
        x = sx0 + 4 + i*9; y = sy + 20 - (x-sx0)*20/(sx1-sx0)
        kind = rng.integers(0, 3)
        if kind == 0:  # tiny head on neck
            d.rectangle((x, y-6, x+3, y), fill=Wh, outline=K)
            d.ellipse((x-1, y-14, x+4, y-5), fill=Wh, outline=K)
        elif kind == 1:  # bottle
            d.rectangle((x, y-12, x+5, y), fill=K); d.rectangle((x+1, y-17, x+3, y-12), fill=K)
            d.point((x+1, y-10), fill=Wh)
        else:  # tin of brushes
            d.rectangle((x, y-7, x+6, y), fill=R if rng.random() < 0.3 else Wh, outline=K)
            for b in range(4):
                d.line((x+1+b*1.5, y-7, x+b*2-1, y-20+rng.uniform(0, 4)), fill=K)

# ---------- stove and pipe (left back corner)
d.rectangle((86, 330, 118, 405), fill=K)
d.rectangle((90, 352, 114, 372), fill=R)
for i in range(5): d.line((90, 354+i*4, 114, 354+i*4), fill=K)
d.rectangle((96, 120, 104, 330), fill=K)
d.line((96, 120, 140, 70), fill=K, width=8)

# ---------- floor: plaster crumbs, dropped paper, footprints in dust
for _ in range(500):
    x = rng.uniform(0, W); y = rng.uniform(410, 600)
    if not polymask(floor)[int(min(y, H-1)), int(x)]: continue
    s = 1 + (y-400)/80
    c = Wh if rng.random() < 0.7 else K
    d.ellipse((x, y, x+s*rng.uniform(0.5, 1.5), y+s*0.6), fill=c)
for i in range(6):
    x = 70 + i*18 + rng.normal(0, 3); y = 590 - i*22
    d.ellipse((x, y, x+6, y+10), outline=K)

# ---------- the table, clutter of tiny figures on enormous bases
tt = [(10, 470), (150, 440), (175, 470), (30, 510)]
tone_poly(im, tt, 0.8, [K, Wh])
d.polygon(tt, outline=K)
d.polygon([(30, 510), (175, 470), (175, 478), (30, 520)], fill=K)
for lx, ly in ((34, 520), (170, 478), (14, 478)):
    d.line((lx, ly, lx, ly+70), fill=K, width=4)
items = sorted([(rng.uniform(445, 495), rng.uniform(30, 160)) for _ in range(16)])
for y, x in items:
    # keep on table top roughly
    k = rng.integers(0, 4)
    if k == 0:   # tiny figure on a big block base
        d.rectangle((x-6, y-8, x+6, y), fill=Wh, outline=K)
        d.line((x, y-8, x, y-22), fill=K, width=1); d.point((x, y-23), fill=K)
    elif k == 1:  # plaster bag slumped
        d.polygon([(x-7, y), (x-5, y-10), (x+3, y-12), (x+8, y)], fill=Wh, outline=K)
    elif k == 2:  # turpentine bottle
        d.rectangle((x-3, y-14, x+3, y), fill=K); d.rectangle((x-1, y-19, x+1, y-14), fill=K)
    else:         # rag / tube
        d.line((x-6, y, x+6, y-2), fill=R if rng.random() < 0.25 else K, width=3)

# ---------- standing woman on the turntable (right of centre)
def plaster_figure(cx, base_y, h, w, rng, walking=False):
    # stand
    d.rectangle((cx-22, base_y, cx+22, base_y+8), fill=Wh, outline=K)
    d.polygon([(cx-22, base_y+8), (cx+22, base_y+8), (cx+18, base_y+60), (cx-18, base_y+60)], fill=K)
    d.line((cx-14, base_y+12, cx-10, base_y+56), fill=Wh)
    # the figure: rough, eroded silhouette; shaded on the right with hatching
    pts_l, pts_r = [], []
    for i in range(41):
        t = i/40; y = base_y - t*h
        prof = w*(0.55 if t < 0.04 else 0.22 + 0.25*math.exp(-((t-0.62)/0.12)**2)
                   - 0.12*math.exp(-((t-0.78)/0.03)**2) + 0.35*math.exp(-((t-0.93)/0.035)**2))
        jl = rng.normal(0, 0.7); jr = rng.normal(0, 0.7)
        pts_l.append((cx - prof + jl, y)); pts_r.append((cx + prof + jr, y))
    poly = pts_l + pts_r[::-1]
    d.polygon(poly, fill=Wh)
    for i in range(len(pts_l)-1):
        mid = (pts_l[i][0] + pts_r[i][0])/2
        for xh in np.arange(mid+1, pts_r[i][0], 1.6):
            if rng.random() < 0.8: d.line((xh, pts_r[i][1], xh, pts_r[i+1][1]), fill=K)
    d.line(pts_l, fill=K); d.line(pts_r, fill=K)
plaster_figure(300, 452, 190, 12, rng)

# ---------- the big Walking Man on his stand, centre, shaded plaster
cx, by = 182, 500
d.rectangle((cx-40, by, cx+40, by+10), fill=Wh, outline=K)
d.polygon([(cx-40, by+10), (cx+40, by+10), (cx+34, by+82), (cx-34, by+82)], fill=K)
for i in range(6): d.line((cx-30+i*3, by+16, cx-28+i*3, by+78), fill=Wh)
# plaster base slab on top of the stand
d.polygon([(cx-30, by), (cx+30, by), (cx+26, by-6), (cx-26, by-6)], fill=Wh, outline=K)
fig = Image.new("L", (W, H), 0); fd = ImageDraw.Draw(fig)
walker(fd, cx, by-6, 230, 255, stride=0.55)
fm = np.asarray(fig) > 0
# shade: hatch the right edge of each row of the figure
a = np.asarray(im).copy()
a[fm] = Wh
rows = np.where(fm.any(1))[0]
for y in rows:
    xs = np.where(fm[y])[0]
    # split into runs (legs/arms separate)
    runs = np.split(xs, np.where(np.diff(xs) > 1)[0]+1)
    for r_ in runs:
        if len(r_) == 0: continue
        n = max(1, int(len(r_)*0.5))
        sh = r_[-n:]
        a[y, sh[::2]] = K
        if len(r_) > 2:
            a[y, r_[0]] = K; a[y, r_[-1]] = K
edge = fm & ~(np.roll(fm,1,0)&np.roll(fm,-1,0)&np.roll(fm,1,1)&np.roll(fm,-1,1))
a[edge] = K
im = Image.fromarray(a); d = ImageDraw.Draw(im)
# cast shadow from the skylight, thrown down-right across the stand top/floor
d.line((cx+10, by+84, cx+120, by+96), fill=K, width=3)

# ---------- chair with a red jumper, front right
chx, chy = 300, 560
d.line((chx, chy-80, chx+4, chy+40), fill=K, width=4)
d.line((chx+60, chy-90, chx+58, chy+40), fill=K, width=4)
d.polygon([(chx-6, chy-10), (chx+70, chy-16), (chx+76, chy-2), (chx-4, chy+4)], fill=K)
for i in range(4): d.line((chx+2, chy-80+i*14, chx+60, chy-88+i*14), fill=K, width=2)
jumper = [(chx+4, chy-84), (chx+52, chy-92), (chx+66, chy-50), (chx+70, chy+20), (chx+56, chy+30),
          (chx+46, chy-6), (chx+22, chy-2), (chx+10, chy+34), (chx-6, chy+28), (chx, chy-30)]
d.polygon(jumper, fill=R)
for k in range(18):  # knit ribs
    x = chx + 6 + k*3.2
    d.line((x, chy-84 + k*0.3, x+2, chy-8), fill=K)
d.line(jumper + [jumper[0]], fill=K, width=2)

# the small walking man on the table, the one in every piece today
walker(d, 120, 452, 26, R, stride=0.9)
save(im)
