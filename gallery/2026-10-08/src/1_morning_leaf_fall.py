# Morning — "Leaf fall". A lawn at first light, seen from directly above, with the
# night's leaves lying where they landed: ginkgo, maple (some with black tar-spot),
# oak, birch. Every blade, vein and dew drop is drawn. Full palette, green in charge.
import math, numpy as np
from PIL import Image, ImageDraw
from h import *
rng = np.random.default_rng(1008)
im = Image.new("RGB", (W, H), G); d = ImageDraw.Draw(im)

# --- lawn: dark hollows from noise, then thousands of blades
n = fbm(W, H, rng, (220, 110, 55, 25))
hollow = screen(np.clip((0.56 - n) * 3.2, 0, 1) * 0.55, 2)
a = np.array(im); a[hollow] = K; im = Image.fromarray(a); d = ImageDraw.Draw(im)
for i in range(16000):
    x, y = rng.uniform(-10, W+10), rng.uniform(-10, H+10)
    L = rng.uniform(10, 26); ang = -math.pi/2 + rng.normal(0, 0.55) + 0.25
    bend = rng.normal(0, 0.35)
    pts = []
    for t in np.linspace(0, 1, 5):
        aa = ang + bend*t
        pts.append((x + math.cos(aa)*L*t, y + math.sin(aa)*L*t))
    r = rng.random(); lit = n[int(min(max(y,0),H-1)), int(min(max(x,0),W-1))]
    col = K if r < 0.30 else (Y if r < 0.30 + 0.22*lit else G)
    d.line(pts, fill=col, width=2)
# clover patches
for i in range(14):
    cx, cy = rng.uniform(0, W), rng.uniform(0, H)
    for j in range(rng.integers(3, 8)):
        x, y = cx + rng.normal(0, 26), cy + rng.normal(0, 26); s = rng.uniform(7, 10)
        for k in range(3):
            aa = rng.uniform(0, 6.28) + k*2.094
            ex, ey = x + math.cos(aa)*s, y + math.sin(aa)*s
            d.ellipse((ex-s, ey-s, ex+s, ey+s), fill=G, outline=K, width=2)
            d.arc((ex-s*0.6, ey-s*0.6, ex+s*0.6, ey+s*0.6), 200, 340, fill=Wh, width=1)

# --- leaf outlines in local coords: stem at origin, pointing +x, length ~1
def maple():
    pts = []
    lobes = [(0, 1.0), (0.95, 0.85), (-0.95, 0.85), (1.85, 0.5), (-1.85, 0.5)]
    for th in np.linspace(-math.pi, math.pi, 260):
        r = 0.22
        for la, ll in lobes:
            dth = math.atan2(math.sin(th-la), math.cos(th-la))
            r = max(r, 0.22 + ll*0.58*math.exp(-(dth/0.42)**2) + ll*0.05*abs(math.sin(th*9))*math.exp(-(dth/0.5)**2))
        r += 0.02*math.sin(th*38)
        pts.append((0.32 + r*math.cos(th), r*math.sin(th)))
    return pts, [(0.32, 0, 0.32+0.78*math.cos(a)*l, 0.78*math.sin(a)*l) for a, l in lobes]
def oak():
    up, lo = [], []
    for x in np.linspace(0, 1, 120):
        w = 0.30*math.sin(math.pi*min(1, x*1.05))**0.7*(0.62 + 0.38*abs(math.cos(x*4.5*math.pi)))
        up.append((x, -w)); lo.append((x, w))
    v = [(0, 0, 1, 0)] + [(x, 0, x+0.12, s*0.26) for x in np.linspace(0.12, 0.78, 5) for s in (-1, 1)]
    return up + lo[::-1], v
def ginkgo():
    pts = [(0, 0)]
    for a in np.linspace(-1.05, 1.05, 90):
        r = 0.95 - 0.22*math.exp(-(a/0.07)**2) + 0.02*math.sin(a*30)
        pts.append((0.08 + r*math.cos(a), r*math.sin(a)))
    v = [(0.04, 0, 0.08 + 0.9*math.cos(a), 0.9*math.sin(a)) for a in np.linspace(-0.95, 0.95, 13)]
    return pts, v
def birch():
    up, lo = [], []
    for x in np.linspace(0, 1, 90):
        w = 0.36*math.sin(math.pi*x)**0.8*(1 - 0.3*x) + 0.015*abs(math.sin(x*60))
        up.append((x, -w)); lo.append((x, w))
    v = [(0, 0, 1, 0)] + [(x, 0, x+0.16, s*0.24*(1-x)) for x in np.linspace(0.15, 0.7, 4) for s in (-1, 1)]
    return up + lo[::-1], v
KINDS = [(maple, 70, 105, [R, R, Y, "split"]), (oak, 85, 120, [R, G, Y]), (ginkgo, 48, 66, [Y, Y, Y, G]), (birch, 38, 52, [Y, Y, G])]

placed = []
for i in range(40):
    k = rng.choice(len(KINDS), p=[0.3, 0.2, 0.32, 0.18]); f, smin, smax, cols = KINDS[k]
    cx, cy = rng.uniform(-30, W+30), rng.uniform(-30, H+30)
    sc = rng.uniform(smin, smax)*1.8; ang = rng.uniform(0, 6.28)
    outline, veins = f(); col = cols[rng.integers(len(cols))]
    P = xform(outline, cx, cy, ang, sc)
    d.polygon([(x+5, y+8) for x, y in P], fill=K)                     # shadow
    if col == "split":                                                # two-tone along the midrib
        d.polygon(P, fill=R)
        half = [p for p, q in zip(P, outline) if q[1] > 0]
        if len(half) > 2: d.polygon(xform([(0.3, 0)] + [q for q in outline if q[1] > 0], cx, cy, ang, sc), fill=Y)
        vc = K
    else:
        d.polygon(P, fill=col); vc = K if col != G else Y
    d.line(P + [P[0]], fill=K, width=2)
    for x0, y0, x1, y1 in veins:
        (a0, b0), (a1, b1) = xform([(x0, y0), (x1, y1)], cx, cy, ang, sc)
        d.line((a0, b0, a1, b1), fill=vc, width=2)
        # tertiary veins as short ticks along each primary
        for t in np.linspace(0.25, 0.85, 4):
            mx, my = a0 + (a1-a0)*t, b0 + (b1-b0)*t; L = math.hypot(a1-a0, b1-b0)*0.10
            na = math.atan2(b1-b0, a1-a0)
            for s in (-1, 1):
                d.line((mx, my, mx + math.cos(na + s*0.9)*L, my + math.sin(na + s*0.9)*L), fill=vc, width=1)
    # stem
    (s0x, s0y), (s1x, s1y) = xform([(0, 0), (-0.28, 0.04)], cx, cy, ang, sc)
    d.line((s0x, s0y, s1x, s1y), fill=K, width=4); d.line((s0x, s0y, s1x, s1y), fill=col if col in (R, Y, G) else R, width=2)
    if f is maple and rng.random() < 0.3:                             # tar spot: black blots with a yellow halo
        for j in range(rng.integers(2, 4)):
            u, v = rng.uniform(0.2, 0.8), rng.uniform(-0.35, 0.35)
            (px, py), = xform([(u, v)], cx, cy, ang, sc); r0 = rng.uniform(5, 11)
            d.ellipse((px-r0-3, py-r0-3, px+r0+3, py+r0+3), fill=Y)
            d.ellipse((px-r0, py-r0, px+r0, py+r0), fill=K)
    if f is oak and rng.random() < 0.5:                               # nibbled edge
        (px, py), = xform([(rng.uniform(0.3, 0.7), 0.24)], cx, cy, ang, sc); r0 = rng.uniform(8, 14)
        d.ellipse((px-r0, py-r0, px+r0, py+r0), fill=G, outline=K, width=2)
    placed.append((cx, cy, sc))

# --- dew: drops on leaves and grass, white with a black rim and a glint
for i in range(110):
    x, y = rng.uniform(0, W), rng.uniform(0, H); r0 = rng.choice([3, 4, 5, 7, 9], p=[.35, .3, .2, .1, .05])
    d.ellipse((x-r0, y-r0, x+r0, y+r0), fill=Wh, outline=K, width=1 if r0 < 6 else 2)
    if r0 >= 5: d.ellipse((x+r0*0.1, y+r0*0.1, x+r0*0.6, y+r0*0.6), fill=B)

# --- a ladybird, resting on the biggest leaf near the centre
cx, cy, sc = min(placed, key=lambda p: math.hypot(p[0]-W*0.52, p[1]-H*0.48))
lx, ly = cx + 6, cy + 2; r0 = 18
d.ellipse((lx-r0-2, ly-r0-2, lx+r0+2, ly+r0+2), fill=K)
d.ellipse((lx-r0, ly-r0+6, lx+r0, ly+r0), fill=R)
d.line((lx, ly-r0+6, lx, ly+r0), fill=K, width=2)
d.pieslice((lx-11, ly-r0-10, lx+11, ly-r0+12), 180, 360, fill=K)
for sx, sy in [(-8, -2), (8, -2), (-9, 9), (9, 9), (-4, 15), (4, 15)]:
    d.ellipse((lx+sx-3, ly+sy-3, lx+sx+3, ly+sy+3), fill=K)
d.ellipse((lx-7, ly-r0-4, lx-3, ly-r0), fill=Wh); d.ellipse((lx+3, ly-r0-4, lx+7, ly-r0), fill=Wh)
save(im)
