"""Night — the villa after dark. No moon tonight (three days past new). Tin roofs
drawn in thin blue against black; a few lit windows, each with someone inside;
a brazier; a string of bulbs; the Southern Cross low; Juanito's kite caught on a wire."""
import math, random, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from common import *

rnd = random.Random(2210)
c = C(K)

# stars: many small, few bright; Milky Way as a denser diagonal drift
for _ in range(420):
    x, y = rnd.uniform(0, W), rnd.uniform(0, 330)
    # density toward the band
    d = abs((y - 40) - (x*0.55))
    if d > 60 and rnd.random() < 0.6: continue
    c.ell(x, y, rnd.choice([0.5, 0.6, 0.7, 0.9]), fill=Wh)
def bright(x, y, r, col=Wh):
    c.ell(x, y, r, fill=col)
    c.line([(x-r*3, y), (x+r*3, y)], col, 0.7); c.line([(x, y-r*3), (x, y+r*3)], col, 0.7)
# Crux, low in the south (a small kite of stars itself) + the Pointers
crux = [(300, 170), (300, 222), (280, 196), (322, 192), (310, 205)]
for (x, y), r in zip(crux, [2.4, 2.6, 2.0, 2.2, 1.1]):
    bright(x, y, r)
bright(220, 236, 2.6, Y); bright(196, 246, 2.2)  # alpha, beta Centauri
for _ in range(9):
    bright(rnd.uniform(10, 390), rnd.uniform(10, 300), rnd.uniform(1.1, 1.7))
c.text((330, 230), "Crux", B, size=8, bold=False)

# distant city glow: blue towers outlined only, a few yellow windows
x = -5
while x < W:
    w = rnd.uniform(16, 34); h = rnd.uniform(25, 80); top = 330 - h
    c.rect(x, top, x+w, 336, fill=K, outline=B, width=0.8)
    for wy in range(int(top)+5, 330, 7):
        for wx in range(int(x)+3, int(x+w)-3, 5):
            if rnd.random() < 0.09:
                c.rect(wx, wy, wx+2, wy+3, fill=Y)
    x += w + rnd.uniform(0, 4)

def house(x0, base, w, h, sc):
    y0 = base - h
    c.rect(x0, y0, x0+w, base, fill=K)
    # wall texture: faint blue corrugation lines on some, planks on others
    if rnd.random() < 0.55:
        xx = x0 + 2
        while xx < x0 + w:
            c.line([(xx, y0+2), (xx, base)], B, 0.5); xx += 3.5*sc
    else:
        yy = y0 + 3
        while yy < base:
            c.line([(x0, yy), (x0+w, yy)], B, 0.5); yy += 5*sc
    c.rect(x0, y0, x0+w, base, outline=B, width=0.9)
    # windows: mostly dark; some lit with a scene
    for _ in range(rnd.choice([0, 1, 1, 2])):
        ww = w*rnd.uniform(0.2, 0.3); wh = ww*0.9
        wx = x0 + rnd.uniform(3, max(4, w-ww-3)); wy = y0 + h*rnd.uniform(0.2, 0.4)
        r = rnd.random()
        if r < 0.45:
            c.rect(wx, wy, wx+ww, wy+wh, fill=Y, outline=K, width=1)
            # silhouette inside: a head-and-shoulders, a pot, or a hanging bulb
            k = rnd.random()
            if k < 0.4:
                c.ell(wx+ww*0.5, wy+wh*0.45, ww*0.14, fill=K)
                c.poly([(wx+ww*0.28, wy+wh), (wx+ww*0.32, wy+wh*0.7), (wx+ww*0.68, wy+wh*0.7), (wx+ww*0.72, wy+wh)], fill=K)
            elif k < 0.7:
                c.line([(wx+ww*0.5, wy), (wx+ww*0.5, wy+wh*0.3)], K, 0.6)
                c.ell(wx+ww*0.5, wy+wh*0.36, ww*0.08, fill=Wh)
            else:
                c.rect(wx+ww*0.2, wy+wh*0.6, wx+ww*0.45, wy+wh, fill=K)
                c.line([(wx+ww*0.32, wy+wh*0.6), (wx+ww*0.3, wy+wh*0.3)], K, 0.6)
            # curtain edge
            c.poly([(wx, wy), (wx+ww*0.22, wy), (wx+ww*0.12, wy+wh)], fill=R)
            c.line([(wx+ww/2, wy), (wx+ww/2, wy+wh)], K, 0.6)
        elif r < 0.6:  # TV glow
            c.rect(wx, wy, wx+ww, wy+wh, fill=B, outline=K, width=1)
            for yy in range(int(wy)+1, int(wy+wh), 2):
                c.line([(wx+1, yy), (wx+ww-1, yy)], Wh if rnd.random() < 0.25 else B, 0.4)
        else:
            c.rect(wx, wy, wx+ww, wy+wh, fill=K, outline=B, width=0.8)
    # door with light under it
    if rnd.random() < 0.5:
        dw = w*0.22; dx = x0 + rnd.uniform(3, max(4, w-dw-3))
        c.rect(dx, base-h*0.6, dx+dw, base, fill=K, outline=B, width=0.8)
        c.line([(dx+1, base-1), (dx+dw-1, base-1)], Y, 1.2)
    # roof line
    slope = rnd.uniform(-5, 5)*sc
    rp = [(x0-3*sc, y0-1+max(0, slope)), (x0+w+3*sc, y0-1+max(0, -slope))]
    c.line(rp, Wh, 1.1)
    for t in range(0, int(w), 4):
        f = t/w
        c.line([(rp[0][0]+(rp[1][0]-rp[0][0])*f, rp[0][1]+(rp[1][1]-rp[0][1])*f), (rp[0][0]+(rp[1][0]-rp[0][0])*f, rp[0][1]+(rp[1][1]-rp[0][1])*f+3*sc)], B, 0.5)
    if rnd.random() < 0.35:
        ax = rnd.uniform(x0+3, x0+w-3); top = y0 - 22*sc
        c.line([(ax, y0), (ax, top)], B, 0.9)
        for k in range(4):
            ww = (9-k*2)*sc; c.line([(ax-ww, top+k*4*sc), (ax+ww, top+k*4*sc)], B, 0.8)

rows = [(372, 0.6), (408, 0.75), (452, 0.9), (505, 1.1), (575, 1.35), (640, 1.6)]
poles = []
for base, sc in rows:
    x0 = rnd.uniform(-30, -5)
    while x0 < W:
        w = rnd.uniform(40, 70)*sc; h = rnd.uniform(46, 62)*sc
        house(x0, base + rnd.uniform(-4, 4)*sc, w, h, sc)
        if rnd.random() < 0.22:
            poles.append((x0+w+1, base, sc))
        x0 += w + rnd.uniform(-4, 1)*sc

# string of bulbs across the lane
pts = [(30 + 340*t/30, 470 + 26*math.sin(math.pi*t/30)) for t in range(31)]
c.line(pts, Wh, 0.7)
for i, (x, y) in enumerate(pts[1:-1:3]):
    col = [Y, R, Wh, G, Y][i % 5]
    c.line([(x, y), (x, y+4)], Wh, 0.6); c.ell(x, y+6.5, 2.6, fill=col)

# brazier in the lane, with a few figures around it
bx, by = 120, 560
c.poly([(bx-14, by), (bx+14, by), (bx+10, by+16), (bx-10, by+16)], fill=K, outline=B, width=1)
for k in range(-12, 13, 4):
    c.ell(bx+k*0.9, by+6, 1.3, fill=R)
flames = [(bx-9, by), (bx-6, by-14), (bx-2, by-5), (bx+1, by-22), (bx+4, by-6), (bx+8, by-15), (bx+10, by)]
c.poly(flames, fill=R)
c.poly([(bx-5, by), (bx-2, by-9), (bx+1, by-15), (bx+3, by-6), (bx+6, by)], fill=Y)
for k in range(8):
    c.ell(bx + rnd.uniform(-10, 10), by - rnd.uniform(25, 60), 0.8, fill=rnd.choice([Y, R]))
for fx, s in ((bx-34, 1), (bx+32, -1), (bx+52, -1)):
    c.ell(fx, by-14, 4.5, fill=K, outline=R, width=0.8)
    c.poly([(fx-5, by-10), (fx+5, by-10), (fx+7, by+16), (fx-7, by+16)], fill=K)
    c.line([(fx + s*4, by-9), (fx + s*5, by-9), (fx + s*8, by-6)], R, 1.0)  # rim light
    c.line([(fx + s*5, by-9), (fx + s*7, by+14)], R, 1.0)
# a dog
dx, dy = 300, 585
c.poly([(dx, dy), (dx+22, dy), (dx+24, dy-10), (dx+30, dy-14), (dx+33, dy-11), (dx+28, dy-5), (dx+24, dy+2), (dx+22, dy+10), (dx+19, dy+10), (dx+18, dy+3), (dx+5, dy+3), (dx+3, dy+10), (dx, dy+10), (dx-2, dy-2), (dx-8, dy-8)], fill=K, outline=B, width=0.9)

# poles and wires; Juanito's kite caught on the top wire, string dangling
poles.sort()
for (x, b, sc) in poles:
    c.line([(x, b), (x, b - 95*sc)], B, 1.6*sc)
    c.line([(x-7*sc, b-88*sc), (x+7*sc, b-88*sc)], B, 1.2*sc)
wire = [(-10, 300), (130, 345), (260, 328), (410, 352)]
for (xa, ya), (xb, yb) in zip(wire, wire[1:]):
    c.line([(xa + (xb-xa)*t/16, ya + (yb-ya)*t/16 + 9*math.sin(math.pi*t/16)) for t in range(17)], B, 1)
kx, ky = 186, 322
kite(c, kx, ky, 15, cols=(R, Y, B, Wh, G, R), rot=0.6, frame=K)
c.line(tail_curve(kx+3, ky+14, 70, 6, n=20, seed=9, dirx=0.08), Wh, 0.6)

c.save()
