# Morning — "Bregaglia, October". Full palette, ordered-screened inside the generator.
# Dawn in the valley where Giacometti was born (Borgonovo/Stampa): granite spires of the
# Sciora catching first light, forested shoulders flecked with turning larches, the village
# and the Maira on the valley floor, two big golden larches framing the road, and a tiny
# walking man setting out. Lots of drawn detail: every tree, roof and grass blade placed.
import math, numpy as np
from PIL import Image, ImageDraw
from common import *

rng = np.random.default_rng(1901)
im = Image.new("RGB", (W, H), Wh); d = ImageDraw.Draw(im)
yy, xx = np.mgrid[0:H, 0:W].astype(float)

# ---------- sky: deep blue -> white -> yellow glow low in the east (right)
glow = np.exp(-(((xx-300)/170)**2 + ((yy-215)/120)**2))
t = np.clip(1 - yy/240, 0, 1)*0.9 - glow*0.55
sky = ramp(np.clip(0.5 + t*0.5, 0, 1)**1.2, [Y, Wh, Wh, B])
paste_arr(im, sky)
# a few wisps of cloud, lit underneath
for i in range(9):
    cy = rng.uniform(30, 150); cx = rng.uniform(-40, 420); L = rng.uniform(60, 160)
    for k in range(4):
        y0 = cy + k*3; x0 = cx + rng.uniform(-10, 10)
        d.line((x0, y0, x0+L*(1-k*0.2), y0), fill=Wh if k < 3 else Y, width=2)
# morning star, fading
d.line((60, 52, 60, 66), fill=Wh); d.line((53, 59, 67, 59), fill=Wh); d.point((60, 59), fill=Y)

# ---------- ridge profile: midpoint displacement with deliberate spires
def ridge(n, pts, rough, seed):
    r = np.random.default_rng(seed)
    xs = np.array([p[0] for p in pts], float); ys = np.array([p[1] for p in pts], float)
    for it in range(n):
        nx, ny = [xs[0]], [ys[0]]
        for i in range(len(xs)-1):
            mx = (xs[i]+xs[i+1])/2; my = (ys[i]+ys[i+1])/2 + r.normal(0, rough*(xs[i+1]-xs[i]))
            nx += [mx, xs[i+1]]; ny += [my, ys[i+1]]
        xs, ys = np.array(nx), np.array(ny)
    return np.interp(np.arange(W), xs, ys)

far = ridge(7, [(-10, 230), (30, 175), (70, 140), (95, 98), (118, 150), (150, 118), (178, 72),
                (205, 128), (232, 110), (262, 155), (300, 145), (340, 190), (410, 205)], 0.22, 7)
mtn = yy > far[None, :]
# face orientation from the ridge slope, smoothed (lit = sloping down to the right)
slope = np.gradient(np.convolve(far, np.ones(9)/9, mode="same"))
gul = fbm(H, W, seed=3, octaves=5, base=3)
gully = np.asarray(Image.fromarray((gul*255).astype(np.uint8)).resize((W*3, H)).crop((0, 0, W, H)), float)/255
gully2 = fbm(H, W*4, seed=4, octaves=4, base=6)[:, :W]
depth = (yy - far[None, :])
sl = np.convolve(np.tanh(slope*0.6), np.ones(25)/25, mode='same')
lit = 0.55 + 0.45*sl[None, :] + (gully2 - 0.5)*1.8 + (gul-0.5)*0.4 + np.clip(depth-120, 0, None)/250
tone = np.clip(lit, 0, 1)
rock = ramp(tone, [K, B, B, Wh])
# snow in the gullies near the top
snow = mtn & (gully2 > 0.56) & (depth < 70 + gully*60)
rock[snow] = Wh
paste_arr(im, rock, mtn)
# ridge line crisp, and black couloir strokes running down the fall line
for x in range(W - 1):
    d.line((x, far[x], x+1, far[x+1]), fill=K)
for i in range(140):
    x = rng.uniform(0, W); y = far[int(x)] + rng.uniform(4, 60)
    L = rng.uniform(8, 40); a = math.pi/2 + rng.normal(0, 0.25) + slope[int(x)]*-0.2
    pts = [(x, y)]
    for s in range(6):
        x += L/6*math.cos(a) + rng.normal(0, 0.6); y += L/6*math.sin(a); pts.append((x, y))
    d.line(pts, fill=K if tone[int(min(y, H-1)), int(min(max(x, 0), W-1))] < 0.6 else B, width=1)

# ---------- forested shoulders (two bands), conifers dark, larches gold/orange
def shoulder(base_pts, seed):
    return ridge(6, base_pts, 0.08, seed)
s1 = shoulder([(-10, 265), (60, 250), (140, 285), (220, 262), (300, 290), (410, 270)], 11)
s2 = shoulder([(-10, 330), (90, 300), (180, 335), (260, 318), (330, 300), (410, 325)], 12)
VALLEY = 400

def forest(top, bottom_y, seed, scale):
    r = np.random.default_rng(seed)
    region = (yy > top[None, :]) & (yy < bottom_y)
    # base: dark green slope, darker in shade on the left
    tt = 0.35 + 0.25*(xx/W) + (fbm(H, W, seed=seed, base=6)-0.5)*0.6
    paste_arr(im, ramp(tt, [K, G, G]), region)
    trees = []
    for _ in range(int(1500*scale)):
        x = r.uniform(-5, W+5); xi = int(np.clip(x, 0, W-1))
        y = r.uniform(top[xi]+2, bottom_y)
        trees.append((y, x))
    trees.sort()
    for y, x in trees:
        dep = (y - 240)/200
        h = (5 + dep*11)*scale*r.uniform(0.7, 1.3); w = h*0.38
        kind = r.random()
        larch = kind < 0.32 + 0.25*(x > 200)
        if larch:
            col = Y if r.random() < 0.7 else (R if r.random() < 0.5 else Wh)
        else:
            col = K if r.random() < 0.55 else G
        d.polygon([(x, y-h), (x-w, y), (x+w, y)], fill=col)
        if larch and h > 6:
            d.line((x, y-h, x, y), fill=K if col != K else G)
forest(s1, VALLEY, 21, 0.9)
forest(s2, VALLEY, 22, 1.15)
d.line([(x, s1[x]) for x in range(W)], fill=K)
d.line([(x, s2[x]) for x in range(W)], fill=K)

# ---------- valley floor: meadows, river, village
paste_arr(im, ramp(0.3 + 0.4*fbm(H, W, seed=5, base=5) + (yy-VALLEY)/600, [G, G, Y])[VALLEY:], None, 0, VALLEY)
d.rectangle((0, VALLEY-1, W, VALLEY), fill=K)
# hedgerows / field divisions
for i in range(26):
    y = rng.uniform(VALLEY+4, 470); x = rng.uniform(-20, W)
    d.line((x, y, x+rng.uniform(30, 120), y+rng.uniform(-3, 3)), fill=K)
# river Maira: a winding white band, black banks, blue ripples
rx = lambda y: 210 + 70*math.sin((y-VALLEY)/26) - (y-VALLEY)*0.6
for y in range(VALLEY, 480):
    w = 2 + (y-VALLEY)*0.09
    c = rx(y)
    d.line((c-w, y, c+w, y), fill=Wh)
    d.point((c-w-1, y), fill=K); d.point((c+w+1, y), fill=K)
    if y % 3 == 0:
        d.line((c-w*0.5+rng.uniform(-2, 2), y, c+w*0.2, y), fill=B)
# stone bridge
by = 434; bc = rx(by)
d.rectangle((bc-16, by-4, bc+16, by+1), fill=Wh, outline=K)
d.arc((bc-8, by-3, bc+8, by+9), 180, 360, fill=K)

# village: houses along the road, white walls, stone (black/white screened) roofs
houses = []
for i in range(24):
    x = rng.uniform(30, 360); y = rng.uniform(408, 448)
    if abs(x - rx(y)) < 18: continue
    houses.append((y, x))
houses.sort()
scr = screen(H, W)
for y, x in houses:
    s = 0.6 + (y-VALLEY)/60
    w = rng.uniform(9, 15)*s; h = rng.uniform(6, 10)*s; rh = w*0.45
    d.rectangle((x, y-h, x+w, y), fill=Wh, outline=K)
    # gable-end shaded side
    d.polygon([(x+w, y-h), (x+w+w*0.35, y-h-rh*0.4), (x+w+w*0.35, y-h*0.25), (x+w, y)], fill=K)
    roof = [(x-1, y-h), (x+w*0.5, y-h-rh), (x+w+w*0.35+1, y-h-rh*0.4), (x+w, y-h)]
    d.polygon(roof, fill=K)
    d.line([(x+1, y-h-1), (x+w*0.5, y-h-rh+1)], fill=Wh)
    for wx in np.arange(x+2, x+w-2, 3.2*s):
        d.rectangle((wx, y-h*0.65, wx+1, y-h*0.65+1.5*s), fill=K)
# campanile
cx, cy = 118, 432
d.rectangle((cx, cy-38, cx+7, cy), fill=Wh, outline=K)
d.rectangle((cx+2, cy-31, cx+5, cy-26), fill=K)
d.polygon([(cx-1, cy-38), (cx+3.5, cy-54), (cx+8, cy-38)], fill=K)
d.line((cx+3.5, cy-54, cx+3.5, cy-59), fill=K); d.line((cx+1.5, cy-57, cx+5.5, cy-57), fill=K)
d.rectangle((cx-22, cy-14, cx, cy), fill=Wh, outline=K)
d.polygon([(cx-23, cy-14), (cx-11, cy-22), (cx+1, cy-14)], fill=K)
# smoke from chimneys
for sx, sy in ((170, 410), (262, 418), (88, 420)):
    for k in range(10):
        d.point((sx + k*2.2 + math.sin(k)*1.5, sy - k*3), fill=Wh)

# ---------- foreground: dry meadow sloping up, a dry-stone wall, the road, two big larches
fg_top = lambda x: 478 + 20*math.sin(x/70) - x*0.03
fgm = yy > np.array([fg_top(x) for x in range(W)])[None, :]
paste_arr(im, ramp(0.55 + 0.35*fbm(H, W, seed=8, base=7) - (yy-480)/500, [K, G, Y, Y]), fgm)
# road: a pale band curving from bottom-left into the valley
road_pts = []
for i in range(60):
    t = i/59
    x = 120 + 140*t + 60*math.sin(t*2.5); y = 600 - t*125
    road_pts.append((x, y, 34*(1-t)+3))
for i in range(len(road_pts)-1):
    x0, y0, w0 = road_pts[i]; x1, y1, w1 = road_pts[i+1]
    d.polygon([(x0-w0, y0), (x0+w0, y0), (x1+w1, y1), (x1-w1, y1)], fill=Wh)
for i in range(0, len(road_pts)-1):
    x0, y0, w0 = road_pts[i]; x1, y1, w1 = road_pts[i+1]
    d.line((x0-w0, y0, x1-w1, y1), fill=K); d.line((x0+w0, y0, x1+w1, y1), fill=K)
    if i % 2 == 0:  # wheel ruts and pebbles
        d.point((x0-w0*0.4+rng.uniform(-2, 2), y0), fill=K); d.point((x0+w0*0.4, y0), fill=Y)
# grass blades over the meadow
for _ in range(2600):
    x = rng.uniform(0, W); y = rng.uniform(485, 600)
    if y < fg_top(x) + 2: continue
    on_road = any(abs(x - rx_) < w_ and abs(y - ry_) < 3 for rx_, ry_, w_ in road_pts[::3])
    if on_road: continue
    dep = (y-480)/120; L = 2 + dep*9
    a = -math.pi/2 + rng.normal(0, 0.35)
    col = [K, Y, G, Y, K, Y][rng.integers(0, 6)] if dep > 0.3 else [K, Y, G][rng.integers(0, 3)]
    d.line((x, y, x+L*math.cos(a), y+L*math.sin(a)), fill=col)
# dry-stone wall along the right of the road
for i in range(80):
    t = i/80
    x = 250 + t*160; y = 545 - t*55 + 6*math.sin(t*9)
    sw = 9 - t*5; sh = 6 - t*3
    d.ellipse((x, y-sh, x+sw, y), fill=Wh if (i % 3) else Y, outline=K)

def larch(bx, by, h, seed, lean=0):
    r = np.random.default_rng(seed)
    top = (bx + lean, by - h)
    # trunk
    d.polygon([(bx-6, by), (bx+6, by), (top[0]+1, top[1]+10), (top[0]-1, top[1]+10)], fill=K)
    # tiers of drooping branches with gold needles
    n = 20
    for i in range(n):
        t = i/n
        y = by - h*0.15 - t*h*0.83
        cx = bx + lean*t*(1.0)
        span = (1-t)**1.1 * h*0.24 + 5
        for side in (-1, 1):
            L = span*r.uniform(0.6, 1.1)
            ex = cx + side*L; ey = y + L*0.35 + r.uniform(-4, 6)
            mx = cx + side*L*0.5; my = y - L*0.05
            pts = [(cx, y), (mx, my), (ex, ey)]
            d.line(pts, fill=K, width=1)
            # needle tufts along the branch: short yellow/orange strokes hanging down
            for k in range(int(L/2.6)):
                u = k/(L/2.6)
                px = (1-u)**2*cx + 2*(1-u)*u*mx + u*u*ex
                py = (1-u)**2*y + 2*(1-u)*u*my + u*u*ey
                c = Y if r.random() < 0.72 else (R if r.random() < 0.55 else Wh)
                for j in range(2):
                    ox = r.uniform(-2, 2); ll = r.uniform(2, 6)
                    d.line((px+ox, py-2, px+ox+r.uniform(-1, 1), py+ll), fill=c)
larch(28, 600, 380, 31, lean=10)
larch(380, 600, 300, 32, lean=-8)
larch(330, 548, 120, 33, lean=-3)

# the walking man, setting out on the road
walker(d, 220, 548, 46, K, stride=0.8)
d.line((220, 549, 252, 551), fill=K, width=2)  # his shadow, long and thin in low sun
save(im)
