"""Morning — Juanito's villa at sunrise, as a Berni scrap collage.
Every house is a patchwork of material panels: corrugated tin, planks, brick,
flattened cans, fabric. Drawn at 3x in pure palette colours."""
import math, random, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from common import *

rnd = random.Random(1013)
c = C(Y)

# --- sky: yellow, with screenprint white bands thickening toward the horizon
for i in range(26):
    y = 20 + i*9.5
    th = (i/26)**2 * 6
    if th > 0.4:
        c.rect(0, y, W, y+th, fill=Wh)
# sun: red disc rising behind the city, with ray hatching
sx, sy = 290, 150
for k in range(48):
    a = k/48*2*math.pi
    if k % 2: continue
    c.poly([(sx, sy), (sx+300*math.cos(a), sy+300*math.sin(a)), (sx+300*math.cos(a+0.045), sy+300*math.sin(a+0.045))], fill=Y)
for k in range(48):
    a = k/48*2*math.pi + 0.065
    c.line([(sx+62*math.cos(a), sy+62*math.sin(a)), (sx+120*math.cos(a), sy+120*math.sin(a))], R if k % 3 == 0 else Y, 1.4)
c.ell(sx, sy, 56, fill=R)
for k in range(7):
    c.ell(sx, sy, 56-k*7, outline=Y if k % 2 else R, width=1.2)
c.ell(sx, sy, 50, fill=R)

# birds
for _ in range(14):
    bx, by = rnd.uniform(20, 380), rnd.uniform(40, 150)
    s = rnd.uniform(3, 6)
    c.line([(bx-s, by-s*0.5), (bx, by), (bx+s, by-s*0.5)], K, 1.1)

# --- the city: Buenos Aires towers in blue, windows lit white
x = -5
while x < W:
    w = rnd.uniform(18, 40); h = rnd.uniform(35, 105)
    top = 250 - h
    c.rect(x, top, x+w, 262, fill=B)
    if rnd.random() < 0.3:
        c.line([(x+w/2, top), (x+w/2, top-rnd.uniform(10, 30))], B, 1.5)
    for wy in range(int(top)+5, 255, 7):
        for wx in range(int(x)+3, int(x+w)-3, 5):
            if rnd.random() < 0.45:
                c.rect(wx, wy, wx+2, wy+3, fill=Wh if rnd.random() < 0.8 else Y)
    x += w + rnd.uniform(-4, 3)
# railway embankment + train
c.rect(0, 258, W, 272, fill=K)
for tx in range(0, W, 9):
    c.line([(tx, 258), (tx+4, 272)], Y, 0.8)
c.rect(30, 244, 250, 259, fill=R, outline=K, width=1)
for cx0 in range(30, 250, 55):
    c.line([(cx0, 244), (cx0, 259)], K, 1.2)
    for wx in range(cx0+5, cx0+50, 9):
        c.rect(wx, 247, wx+6, 253, fill=Y, outline=K, width=0.6)

# --- material textures
def corrugated(cc, x0, y0, x1, y1, col, vertical=True):
    cc.rect(x0, y0, x1, y1, fill=col)
    step = 3.2
    if vertical:
        xx = x0 + 1
        while xx < x1:
            cc.line([(xx, y0), (xx, y1)], K, 0.8); xx += step
    else:
        yy = y0 + 1
        while yy < y1:
            cc.line([(x0, yy), (x1, yy)], K, 0.8); yy += step
    # rust/rivets
    for _ in range(int((x1-x0)*(y1-y0)/180)):
        rx, ry = rnd.uniform(x0, x1), rnd.uniform(y0, y1)
        cc.ell(rx, ry, rnd.uniform(0.8, 2.2), fill=R if col != R else Y)

def planks(cc, x0, y0, x1, y1, col):
    cc.rect(x0, y0, x1, y1, fill=col)
    yy = y0
    while yy < y1:
        h = rnd.uniform(4, 7)
        cc.line([(x0, yy), (x1, yy)], K, 1)
        for xn in (x0+2, x1-2):
            cc.ell(xn, yy+h/2, 0.9, fill=K)
        # grain
        for _ in range(2):
            gx = rnd.uniform(x0, x1); cc.line([(gx, yy+h*0.4), (gx+rnd.uniform(5, 14), yy+h*0.5)], K, 0.5)
        yy += h

def bricks(cc, x0, y0, x1, y1):
    cc.rect(x0, y0, x1, y1, fill=R)
    r_ = 0
    yy = y0
    while yy < y1:
        cc.line([(x0, yy), (x1, yy)], Wh, 0.8)
        xx = x0 + (5 if r_ % 2 else 0)
        while xx < x1:
            cc.line([(xx, yy), (xx, min(y1, yy+4))], Wh, 0.8); xx += 10
        yy += 4; r_ += 1

def cans(cc, x0, y0, x1, y1):
    xx = x0
    while xx < x1:
        yy = y0
        w = rnd.uniform(7, 11)
        while yy < y1:
            h = rnd.uniform(6, 10)
            col = rnd.choice([R, Y, B, G, Wh])
            cc.rect(xx, yy, min(xx+w, x1), min(yy+h, y1), fill=col, outline=K, width=0.7)
            if rnd.random() < 0.5:
                cc.line([(xx+1, yy+h/2), (min(xx+w, x1)-1, yy+h/2)], rnd.choice([K, Wh, R]), 1.2)
            else:
                cc.ell(xx+w/2, yy+h/2, min(w, h)/4, fill=rnd.choice([K, Wh, R, Y]))
            yy += h
        xx += w

def fabric(cc, x0, y0, x1, y1):
    base, ink = rnd.choice([(Wh, R), (Y, B), (G, Wh), (B, Y), (Wh, B)])
    cc.rect(x0, y0, x1, y1, fill=base)
    if rnd.random() < 0.5:  # gingham
        for xx in range(int(x0), int(x1), 5):
            cc.line([(xx, y0), (xx, y1)], ink, 1.3)
        for yy in range(int(y0), int(y1), 5):
            cc.line([(x0, yy), (x1, yy)], ink, 1.3)
    else:  # polka
        for yy in range(int(y0)+3, int(y1), 6):
            for xx in range(int(x0)+3 + (3 if (yy//6) % 2 else 0), int(x1), 6):
                cc.ell(xx, yy, 1.3, fill=ink)

MATS = [corrugated, corrugated, planks, bricks, cans, fabric]

def wall(cc, x0, y0, x1, y1):
    """patchwork wall: split into 1-3 panels of random materials"""
    n = rnd.choice([1, 2, 2, 3])
    cuts = sorted([x0] + [rnd.uniform(x0+6, x1-6) for _ in range(n-1)] + [x1])
    for a, b in zip(cuts, cuts[1:]):
        top = y0 + rnd.uniform(-2, 3)
        m = rnd.choice(MATS)
        if m is corrugated:
            m(cc, a, top, b, y1, rnd.choice([B, G, Wh, Y, R]), vertical=rnd.random() < 0.7)
        elif m is planks:
            m(cc, a, top, b, y1, rnd.choice([G, B, Y, Wh]))
        else:
            m(cc, a, top, b, y1)
        cc.line([(a, top), (a, y1)], K, 1)

def house(cc, x0, base, w, h, scale):
    y0 = base - h
    wall(cc, x0, y0, x0+w, base)
    cc.rect(x0, y0, x0+w, base, outline=K, width=1.2)
    # door or window
    if rnd.random() < 0.6:
        dw = w*rnd.uniform(0.18, 0.28); dx = x0 + rnd.uniform(3, w-dw-3)
        cc.rect(dx, base - h*0.62, dx+dw, base, fill=K)
        if rnd.random() < 0.6:  # curtain
            cc.rect(dx+1, base-h*0.62+1, dx+dw-1, base-h*0.3, fill=rnd.choice([R, Y, Wh]))
            for xx in range(int(dx+2), int(dx+dw-1), 2):
                cc.line([(xx, base-h*0.62+1), (xx, base-h*0.3)], K, 0.4)
    for _ in range(rnd.choice([0, 1, 1, 2])):
        ww = w*rnd.uniform(0.15, 0.24); wx = x0 + rnd.uniform(3, w-ww-3); wy = y0 + h*rnd.uniform(0.15, 0.35)
        cc.rect(wx, wy, wx+ww, wy+ww*0.9, fill=rnd.choice([K, K, Y]), outline=Wh, width=1.2)
        cc.line([(wx+ww/2, wy), (wx+ww/2, wy+ww*0.9)], Wh, 0.8)
        cc.line([(wx, wy+ww*0.45), (wx+ww, wy+ww*0.45)], Wh, 0.8)
    # roof: corrugated sheet sloping, overhanging
    over = 4*scale
    slope = rnd.uniform(-6, 6)*scale
    rp = [(x0-over, y0 - 2 + max(0, slope)), (x0+w+over, y0 - 2 + max(0, -slope)),
          (x0+w+over, y0 - 2 - 5*scale + max(0, -slope)), (x0-over, y0 - 2 - 5*scale + max(0, slope))]
    rc = rnd.choice([Wh, B, R, G, K])
    cc.poly(rp, fill=rc, outline=K, width=1)
    for t in range(1, int((w+2*over)/3)):
        xx = x0 - over + t*3
        f = (xx-(x0-over))/(w+2*over)
        ya = rp[0][1]*(1-f) + rp[1][1]*f; yb = rp[3][1]*(1-f) + rp[2][1]*f
        cc.line([(xx, ya), (xx, yb)], K if rc != K else Wh, 0.6)
    roof_y = (rp[2][1] + rp[3][1])/2
    # stuff on the roof: stones, tyre, water tank, antenna
    for _ in range(rnd.randint(1, 3)):
        sx_ = rnd.uniform(x0, x0+w); cc.ell(sx_, roof_y-2*scale, 2.5*scale, 2*scale, fill=rnd.choice([K, Wh]), outline=K, width=0.6)
    if rnd.random() < 0.3:
        tx = rnd.uniform(x0+4, x0+w-14); cc.ell(tx+5, roof_y-4*scale, 6*scale, 3*scale, fill=K)
        cc.ell(tx+5, roof_y-4*scale, 3*scale, 1.5*scale, fill=rc)
    if rnd.random() < 0.35:
        tx = rnd.uniform(x0+3, x0+w-16*scale)
        cc.rect(tx, roof_y-18*scale, tx+12*scale, roof_y-1, fill=B, outline=K, width=1)
        for yy in range(3):
            cc.line([(tx, roof_y-(15-yy*5)*scale), (tx+12*scale, roof_y-(15-yy*5)*scale)], K, 0.6)
    if rnd.random() < 0.4:
        ax = rnd.uniform(x0+3, x0+w-3)
        cc.line([(ax, roof_y), (ax, roof_y-24*scale)], K, 1)
        for k in range(4):
            yy = roof_y-24*scale + k*4*scale; ww = (10-k*2)*scale
            cc.line([(ax-ww, yy), (ax+ww, yy)], K, 0.8)
    return roof_y

c.rect(0, 272, W, H, fill=K)
# rows from back (small) to front (big)
rows = [(300, 0.55, 3), (338, 0.7, 2), (385, 0.85, 1), (440, 1.0, 0), (505, 1.2, 0), (590, 1.45, 0)]
poles = []
for base, sc, _ in rows:
    x0 = rnd.uniform(-30, -5)
    while x0 < W:
        w = rnd.uniform(38, 70)*sc; h = rnd.uniform(48, 66)*sc
        b = base + rnd.uniform(-5, 5)*sc
        house(c, x0, b, w, h, sc)
        if rnd.random() < 0.25:
            poles.append((x0 + w + 2, b, sc))
        x0 += w + rnd.uniform(-6, 2)*sc
    # ground strip: mud lane with puddles reflecting the sky

# laundry lines strung across rows
for _ in range(7):
    y = rnd.uniform(300, 540); x0 = rnd.uniform(-20, 200); x1 = x0 + rnd.uniform(90, 200)
    sag = rnd.uniform(6, 14)
    pts = [(x0 + (x1-x0)*t/20, y + sag*math.sin(math.pi*t/20)) for t in range(21)]
    c.line(pts, K, 0.9)
    xx = x0 + 6
    while xx < x1 - 10:
        t = (xx-x0)/(x1-x0); yy = y + sag*math.sin(math.pi*t)
        kind = rnd.random(); col = rnd.choice([R, Y, B, G, Wh])
        if kind < 0.4:  # shirt
            c.poly([(xx, yy), (xx+11, yy), (xx+14, yy+5), (xx+11, yy+6), (xx+10, yy+16), (xx+1, yy+16), (xx, yy+6), (xx-3, yy+5)], fill=col, outline=K, width=0.7)
            xx += 18
        elif kind < 0.7:  # trousers
            c.poly([(xx, yy), (xx+9, yy), (xx+10, yy+18), (xx+6, yy+18), (xx+4.5, yy+6), (xx+3, yy+18), (xx-1, yy+18)], fill=col, outline=K, width=0.7)
            xx += 14
        else:  # sheet / towel
            ww = rnd.uniform(10, 18)
            c.rect(xx, yy, xx+ww, yy+rnd.uniform(12, 20), fill=col, outline=K, width=0.7)
            if col == Wh:
                c.line([(xx+2, yy+4), (xx+ww-2, yy+4)], R, 1.2)
            xx += ww + 4
        c.line([(xx-3, yy-2), (xx-3, yy+2)], K, 1)

# electric poles and sagging wires
poles.sort()
for (x, b, sc) in poles:
    c.line([(x, b), (x, b-80*sc)], K, 2*sc)
    c.line([(x-8*sc, b-74*sc), (x+8*sc, b-74*sc)], K, 1.5*sc)
for (xa, ba, sa), (xb, bb, sb) in zip(poles, poles[1:]):
    for off in (-6, 6):
        ya, yb = ba-74*sa, bb-74*sb
        pts = [(xa+off*sa + (xb-xa)*t/16, ya + (yb-ya)*t/16 + 10*math.sin(math.pi*t/16)) for t in range(17)]
        c.line(pts, K, 0.8)

# the kite over everything, string down to a tiny Juanito on a roof
kp = kite(c, 92, 96, 30, rot=0.15, tail=tail_curve(92, 120, 120, 14, seed=3, dirx=-0.25))
jx, jy = 318, 452
# a flat roof slab for him to stand on
c.rect(286, jy, 372, jy+7, fill=Wh, outline=K, width=1.2)
for xx in range(290, 372, 6): c.line([(xx, jy+1), (xx, jy+6)], K, 0.6)
c.line([(92, 96), (200, 260), (jx+9, jy-30)], K, 0.8)
# Juanito: small, black silhouette, arm raised to the string
c.ell(jx, jy-33, 6, fill=K)
c.poly([(jx-6, jy-27), (jx+6, jy-27), (jx+8, jy-11), (jx-8, jy-11)], fill=R, outline=K, width=1)
c.line([(jx-1, jy-27), (jx-1, jy-11)], Wh, 1)
c.line([(jx+5, jy-25), (jx+9, jy-30)], K, 2.4)
c.line([(jx-5, jy-25), (jx-11, jy-18)], K, 2.4)
c.rect(jx-7, jy-12, jx+7, jy-5, fill=B, outline=K, width=0.8)
c.line([(jx-4, jy-5), (jx-6, jy)], K, 2.6); c.line([(jx+4, jy-5), (jx+6, jy)], K, 2.6)

c.save()
