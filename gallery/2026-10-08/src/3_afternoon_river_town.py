# Afternoon — "Peshtigo, before". A naive-painting panorama of a Wisconsin mill town on a
# dry October afternoon: a river winding out of blue hills, a sawmill and its log boom,
# a white church, a railway trestle, and a thousand trees turning. Drawn far-to-near,
# every tree its own crown. Nothing is burning yet; that is the point of it.
import math, numpy as np
from PIL import Image, ImageDraw
from h import *
rng = np.random.default_rng(1871)
im = Image.new("RGB", (W, H), Wh); d = ImageDraw.Draw(im)
HZ = 170*S   # horizon

# --- sky: blue screened to white at the horizon; cumulus with screened blue undersides
yy = np.arange(H)[:, None].repeat(W, 1)
tone = np.clip(1 - (yy - 0)/(HZ*1.05), 0, 1)**0.8
a = np.array(im); a[screen(tone, 2)] = B; im = Image.fromarray(a); d = ImageDraw.Draw(im)
def cloud(cx, cy, w, h):
    blobs = [(cx + rng.uniform(-w/2, w/2), cy + rng.uniform(-h/2, 0), rng.uniform(h*0.4, h*0.8)) for _ in range(14)]
    for bx, by, r in blobs: d.ellipse((bx-r-3, by-r-3, bx+r+3, by+r+3), fill=K)
    for bx, by, r in blobs: d.ellipse((bx-r, by-r, bx+r, by+r), fill=Wh)
    for k in range(6):  # shading lines on the undersides
        y = cy - k*7; d.line((cx-w/2+k*12, y, cx+w/2-k*12, y), fill=B, width=2)
cloud(110*S, 60*S, 120*S, 30*S); cloud(300*S, 100*S, 90*S, 22*S); cloud(220*S, 30*S, 60*S, 14*S)
# sun with ray ticks
sx, sy = 340*S, 40*S
for k in range(24):
    t = k*math.pi/12; d.line((sx+math.cos(t)*30*S, sy+math.sin(t)*30*S, sx+math.cos(t)*(38 if k%2 else 46)*S, sy+math.sin(t)*(38 if k%2 else 46)*S), fill=Y, width=4)
d.ellipse((sx-24*S, sy-24*S, sx+24*S, sy+24*S), fill=Y, outline=K, width=3)
# birds
for i in range(9):
    bx, by = rng.uniform(150, 260)*S, rng.uniform(110, 150)*S; w = rng.uniform(4, 7)*S
    d.line((bx-w, by-w*0.4, bx, by, bx+w, by-w*0.4), fill=K, width=3)

# --- far hills: two ridges in blue line-screen, then green
def ridge(base, amp, f, ph):
    xs = np.arange(0, W+8, 8)
    return [(x, base - amp*(0.6*math.sin(x/f+ph) + 0.4*math.sin(x/(f*0.43)+ph*2))) for x in xs]
for base, amp, col, step in [(HZ+0, 40*S, B, 6), (HZ+30*S, 34*S, B, 4), (HZ+56*S, 26*S, G, 3)]:
    r_ = ridge(base, amp, 90*S, rng.uniform(0, 6)); poly = r_ + [(W, H), (0, H)]
    layer = Image.new("RGB", (W, H), Wh); ld = ImageDraw.Draw(layer)
    for y in range(int(base - amp), H, step*2):     # horizontal hatch inside the ridge
        ld.line((0, y, W, y), fill=col, width=step)
    m = Image.new("L", (W, H), 0); ImageDraw.Draw(m).polygon(poly, fill=255)
    im.paste(layer, (0, 0), m); d = ImageDraw.Draw(im); d.line(r_, fill=K, width=3)
    # tiny far trees along the ridge crest
    for x, y in r_[::1]:
        if rng.random() < 0.8: d.ellipse((x-5, y-8, x+5, y+2), fill=K if col == B else col)
# re-mask: later ridges cover earlier ones because we paint over; fine.

# --- the river: centreline x(y), widening as it comes toward us
def rx(y): t = (y - HZ - 60*S)/(H - HZ); return W*0.5 + 90*S*math.sin(t*4.2 + 0.6)*(0.4 + t)
def rw(y): t = (y - HZ - 60*S)/(H - HZ); return 6*S + 70*S*t**1.3
Y0 = HZ + 62*S
# land below the green ridge: fields
for y in range(Y0, H, 2): d.line((0, y, W, y), fill=G)
# ploughed and stubble fields in the middle distance: parallelograms of stripes
for i in range(9):
    fy = rng.uniform(Y0+4*S, Y0+70*S); fx = rng.uniform(0, W); fw = rng.uniform(40, 90)*S; fh = rng.uniform(10, 20)*S; sk = rng.uniform(-20, 20)*S
    col = [Y, Y, R, Wh][rng.integers(4)]
    d.polygon([(fx, fy), (fx+fw, fy), (fx+fw+sk, fy+fh), (fx+sk, fy+fh)], fill=col, outline=K)
    for k in range(0, int(fw), 7): d.line((fx+k, fy, fx+k+sk, fy+fh), fill=K if col != Wh else G, width=1)
pts_l, pts_r = [], []
for y in range(Y0, H+10, 6): pts_l.append((rx(y) - rw(y), y)); pts_r.append((rx(y) + rw(y), y))
d.polygon(pts_l + pts_r[::-1], fill=B)
d.line(pts_l, fill=K, width=4); d.line(pts_r, fill=K, width=4)
for i in range(260):   # ripples and sky reflections
    y = rng.uniform(Y0, H); w = rw(y)
    x = rx(y) + rng.uniform(-w*0.85, w*0.85); L = rng.uniform(3, 10)*S*(0.3 + (y-Y0)/(H-Y0))
    d.line((x-L, y, x+L, y), fill=Wh if rng.random() < .7 else Y, width=2)

# --- trees: scatter, sort far-to-near, draw. Skip the river and the town clearing.
TOWN = (W*0.28, Y0+95*S)
def in_river(x, y, pad): return abs(x - rx(y)) < rw(y) + pad
def in_town(x, y): return ((x-TOWN[0])/(95*S))**2 + ((y-TOWN[1])/(42*S))**2 < 1
def decid(x, y, s, col):
    trunk = s*0.9
    d.rectangle((x-s*0.08, y-trunk, x+s*0.08, y), fill=K)
    blobs = [(x + rng.normal(0, s*0.28), y - trunk - rng.uniform(0, s*0.5), s*rng.uniform(0.3, 0.45)) for _ in range(5)]
    for bx, by, r in blobs: d.ellipse((bx-r-3, by-r-3, bx+r+3, by+r+3), fill=K)
    for bx, by, r in blobs: d.ellipse((bx-r, by-r, bx+r, by+r), fill=col)
    second = {R: Y, Y: R, G: Y}[col]
    for k in range(int(s*0.5)):     # leaf-dabs of a second colour on the sunny (upper-right) side
        bx, by, r = blobs[rng.integers(len(blobs))]; aa = rng.uniform(-2.2, 0.3)
        px, py = bx + math.cos(aa)*r*rng.uniform(0.2, 0.85), by + math.sin(aa)*r*rng.uniform(0.2, 0.85)
        d.ellipse((px-2, py-2, px+3, py+3), fill=second)
    for k in range(int(s*0.25)):    # shadow dabs lower-left
        bx, by, r = blobs[rng.integers(len(blobs))]; aa = rng.uniform(1.6, 3.4)
        px, py = bx + math.cos(aa)*r*rng.uniform(0.4, 0.9), by + math.sin(aa)*r*rng.uniform(0.4, 0.9)
        d.ellipse((px-2, py-2, px+3, py+3), fill=K)
def conifer(x, y, s):
    h_ = s*2.2; tiers = 5
    d.rectangle((x-s*0.07, y-s*0.3, x+s*0.07, y), fill=K)
    for k in range(tiers):
        top = y - h_ + k*h_/tiers*0.85; bot = top + h_/tiers*1.5; w = s*0.25 + s*0.55*(k+1)/tiers
        d.polygon([(x, top), (x+w, bot), (x-w, bot)], fill=G, outline=K)
        d.line((x, top+4, x+w*0.7, bot-2), fill=K, width=2)
def birch(x, y, s):
    trunk = s*1.5
    d.rectangle((x-s*0.07, y-trunk, x+s*0.07, y), fill=Wh, outline=K, width=2)
    for k in range(4): yy = y - trunk*rng.uniform(0.1, 0.9); d.line((x-s*0.07, yy, x+s*0.03, yy), fill=K, width=3)
    for _ in range(int(s*0.6)):
        px, py = x + rng.normal(0, s*0.32), y - trunk - rng.normal(0, s*0.32); r = rng.uniform(2, 4)
        d.ellipse((px-r, py-r, px+r, py+r), fill=Y, outline=K)
trees = []
for i in range(1500):
    y = Y0 + (H - Y0 + 60*S)*rng.random()**0.85
    x = rng.uniform(-20*S, W+20*S)
    t = (y - Y0)/(H - Y0); s = (5 + 34*t**1.4)*S
    if in_river(x, y, s*0.6) or in_town(x, y): continue
    if t < 0.95 and rng.random() < 0.35: continue
    trees.append((y, x, s))
trees.sort()
TRESTLE_Y = H - 140*S + 70*S
# --- town pieces are interleaved by depth: sawmill, church, houses, log boom, trestle
def town(y_cut):
    pass
built = False
def build_town():
    tx, ty = TOWN
    # clearing ground
    d.ellipse((tx-100*S, ty-40*S, tx+100*S, ty+40*S), fill=Y)
    for k in range(-100, 100, 5): d.line((tx+k*S, ty-36*S, tx+k*S+8*S, ty+36*S), fill=G, width=1)
    d.ellipse((tx-100*S, ty-40*S, tx+100*S, ty+40*S), outline=K, width=2)
    # road
    d.line([(tx-100*S, ty+10*S), (tx-30*S, ty+4*S), (tx+40*S, ty+14*S), (rx(ty+14*S)-rw(ty+14*S), ty+14*S)], fill=Wh, width=10)
    def house(x, y, w, h, wall, roof, steeple=False):
        d.rectangle((x, y-h, x+w, y), fill=wall, outline=K, width=3)
        for yy in range(int(y-h)+5, int(y), 6): d.line((x+2, yy, x+w-2, yy), fill=K, width=1)
        d.polygon([(x-5, y-h), (x+w/2, y-h-h*0.7), (x+w+5, y-h)], fill=roof, outline=K)
        d.line([(x-5, y-h), (x+w/2, y-h-h*0.7), (x+w+5, y-h)], fill=K, width=3)
        for wx in np.arange(x+7, x+w-10, 16): d.rectangle((wx, y-h*0.7, wx+8, y-h*0.35), fill=Y if wall != Y else B, outline=K, width=2)
        if steeple:
            cx = x + w/2; d.rectangle((cx-8, y-h-h*1.5, cx+8, y-h-h*0.5), fill=Wh, outline=K, width=3)
            d.polygon([(cx-11, y-h-h*1.5), (cx, y-h-h*2.6), (cx+11, y-h-h*1.5)], fill=R, outline=K)
            d.line((cx, y-h-h*2.6, cx, y-h-h*2.9), fill=K, width=3); d.line((cx-6, y-h-h*2.75, cx+6, y-h-h*2.75), fill=K, width=3)
            d.ellipse((cx-5, y-h-h*1.25, cx+5, y-h-h*1.0), fill=K)
    house(tx-90*S, ty-6*S, 34*S, 20*S, Wh, K, steeple=True)
    house(tx-48*S, ty+2*S, 26*S, 16*S, R, K)
    house(tx-14*S, ty-8*S, 22*S, 14*S, Y, R)
    house(tx+14*S, ty+6*S, 24*S, 16*S, Wh, B)
    # sawmill on the bank: long shed + stack with a white plume drifting NE
    mx, my = tx+46*S, ty+28*S
    d.rectangle((mx, my-22*S, mx+56*S, my), fill=R, outline=K, width=3)
    for xx in range(int(mx)+6, int(mx+56*S), 8): d.line((xx, my-22*S, xx, my), fill=K, width=2)
    d.polygon([(mx-4, my-22*S), (mx+28*S, my-34*S), (mx+56*S+4, my-22*S)], fill=K)
    d.rectangle((mx+40*S, my-62*S, mx+48*S, my-26*S), fill=K)
    for k in range(14):
        t = k/13; px, py = mx+44*S + t*70*S + math.sin(t*7)*6*S, my-66*S - t*38*S; r = (4 + t*12)*S
        d.ellipse((px-r, py-r*0.7, px+r, py+r*0.7), fill=Wh, outline=K, width=2)
    # lumber stacks
    for k in range(3):
        lx, ly = tx+(-60+k*22)*S, ty+30*S
        for j in range(4):
            for i_ in range(4 - j): d.ellipse((lx+i_*9+j*4.5, ly-j*8, lx+i_*9+j*4.5+9, ly-j*8+9), fill=Y, outline=K, width=2)
    # log boom in the river: a raft of logs
    for k in range(26):
        yy = ty + rng.uniform(20, 46)*S; xx = rx(yy) + rng.uniform(-0.8, 0.8)*rw(yy); L = rng.uniform(14, 22)*S
        d.line((xx-L/2, yy, xx+L/2, yy+rng.uniform(-3, 3)), fill=K, width=9); d.line((xx-L/2, yy, xx+L/2, yy), fill=Y, width=4)
ty_ = H - 140*S
def trestle():
    d.rectangle((0, ty_-10*S, W, ty_), fill=K)
    for x in range(0, W, 14*S):
        d.line((x, ty_, x+14*S, ty_+70*S), fill=K, width=5); d.line((x+14*S, ty_, x, ty_+70*S), fill=K, width=5)
        d.line((x, ty_, x, ty_+90*S), fill=K, width=6)
    for x in range(0, W, 8): d.line((x, ty_-14*S, x, ty_-10*S), fill=K, width=3)
    d.line((0, ty_-14*S, W, ty_-14*S), fill=K, width=3)
    # a little locomotive and two cars on it
    lx = 70*S; ly = ty_-14*S
    d.rectangle((lx, ly-24*S, lx+56*S, ly-6*S), fill=G, outline=K, width=3)
    d.rectangle((lx+38*S, ly-40*S, lx+56*S, ly-20*S), fill=R, outline=K, width=3)
    d.rectangle((lx+42*S, ly-36*S, lx+52*S, ly-28*S), fill=Y, outline=K, width=2)
    d.polygon([(lx+6*S, ly-24*S), (lx+2*S, ly-46*S), (lx+18*S, ly-46*S), (lx+14*S, ly-24*S)], fill=K)
    d.polygon([(lx-12*S, ly-6*S), (lx, ly-18*S), (lx, ly-6*S)], fill=R, outline=K)
    for wx in (10, 26, 46): d.ellipse((lx+wx*S-7*S, ly-14*S, lx+wx*S+7*S, ly), fill=R, outline=K, width=3)
    for k in range(10):
        t = k/9; px, py = lx+10*S + t*60*S, ly-50*S - t*30*S - math.sin(t*5)*6*S; r = (5+t*12)*S
        d.ellipse((px-r, py-r*0.7, px+r, py+r*0.7), fill=Wh, outline=K, width=2)
    for c in range(2):
        cx = lx + (62 + c*58)*S
        d.rectangle((cx, ly-22*S, cx+52*S, ly-6*S), fill=[Y, R][c], outline=K, width=3)
        for k in range(5): d.line((cx+k*10*S+6, ly-22*S, cx+k*10*S+6, ly-6*S), fill=K, width=2)
        for wx in (10, 42): d.ellipse((cx+wx*S-6*S, ly-12*S, cx+wx*S+6*S, ly), fill=K)

done = tdone = False
for (y, x, s) in trees:
    if not done and y > TOWN[1] + 46*S: build_town(); done = True
    if not tdone and y > TRESTLE_Y: trestle(); tdone = True
    if y > TRESTLE_Y and abs(x - W*0.4) < 120*S: continue   # keep the train in view
    r = rng.random()
    if r < 0.18: conifer(x, y, s*0.8)
    elif r < 0.30: birch(x, y, s*0.8)
    else: decid(x, y, s, [R, Y, Y, R, G][rng.integers(5)])
if not done: build_town()
if not tdone: trestle()
save(im)
