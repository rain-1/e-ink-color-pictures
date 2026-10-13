"""Afternoon — Barriletes: a spring wind over the villa, the sky full of
homemade kites. Blue sky in charge; stitched paper clouds; every kite a different
build — hexagon, star, diamond pandorga, box kite. Strings converge on the roofs."""
import math, random, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from common import *

rnd = random.Random(7)
c = C(B)

# wind streaks: thin white dashed lines across the sky
for _ in range(60):
    x, y = rnd.uniform(-40, 400), rnd.uniform(0, 470)
    l = rnd.uniform(20, 70)
    pts = [(x + t*l/10, y + 2*math.sin(t*0.7)) for t in range(11)]
    for a, b in zip(pts[::2], pts[1::2]):
        c.line([a, b], Wh, 0.8)

def cloud(cx, cy, w, h):
    """cut-paper cloud: lumps, a stitched running line inside the edge"""
    lumps = []
    n = int(w/14)
    for i in range(n):
        x = cx - w/2 + w*(i+0.5)/n
        r = h*(0.45 + 0.4*math.sin(math.pi*(i+0.5)/n)) * rnd.uniform(0.85, 1.1)
        lumps.append((x, cy - r*0.3, r))
    for x, y, r in lumps:
        c.ell(x+3, y+3, r, fill=K)
    c.rect(cx-w/2+3, cy-h*0.2+3, cx+w/2+3, cy+h*0.35+3, fill=K)
    for x, y, r in lumps:
        c.ell(x, y, r, fill=Wh)
    c.rect(cx-w/2, cy-h*0.2, cx+w/2, cy+h*0.35, fill=Wh)
    # stitches
    for x, y, r in lumps:
        for t in range(0, 18):
            a = math.pi + t/18*math.pi
            if t % 2: continue
            p1 = (x + (r-4)*math.cos(a), y + (r-4)*math.sin(a))
            p2 = (x + (r-4)*math.cos(a+0.12), y + (r-4)*math.sin(a+0.12))
            c.line([p1, p2], B, 1)


cloud(90, 95, 150, 40); cloud(300, 210, 170, 44); cloud(120, 330, 120, 32); cloud(330, 40, 110, 28)

# sun in corner: yellow with scalloped edge
c.ell(372, 118, 34, fill=Y, outline=K, width=1.5)
for k in range(16):
    a = k/16*2*math.pi
    c.ell(372+38*math.cos(a), 118+38*math.sin(a), 5, fill=Y, outline=K, width=1)
c.ell(372, 118, 26, outline=R, width=1.5)

# --- rooftops band at the bottom, black silhouette with lit details
roofline = []
x = -10
c.rect(0, 520, W, 600, fill=K)
while x < W:
    w = rnd.uniform(30, 60); y = rnd.uniform(470, 505)
    c.poly([(x, 600), (x, y+rnd.uniform(-5, 5)), (x+w, y+rnd.uniform(-5, 5)), (x+w, 600)], fill=K)
    roofline.append((x, x+w, y))
    for k in range(int(w/3)):
        c.line([(x+k*3+1, y+4), (x+k*3+1, y+8)], Wh if k % 4 else Y, 0.5)
    if rnd.random() < 0.5:
        wx = x + rnd.uniform(4, w-14)
        c.rect(wx, y+18, wx+10, y+28, fill=rnd.choice([Y, R, Wh]))
    if rnd.random() < 0.4:
        ax = x + rnd.uniform(3, w-3); c.line([(ax, y), (ax, y-20)], K, 1.2)
        for k in range(3): c.line([(ax-8+k*2, y-18+k*5), (ax+8-k*2, y-18+k*5)], K, 1)
    x += w

# children on roofs: anchor points for strings
kids = []
for x0, x1, y in roofline:
    if rnd.random() < 0.6 and 10 < x0 < 380:
        kx = rnd.uniform(x0+6, x1-6); kids.append((kx, y))

def child(x, y, col):
    c.ell(x, y-17, 3.6, fill=K)
    c.poly([(x-3.5, y-13.5), (x+3.5, y-13.5), (x+4.5, y-5), (x-4.5, y-5)], fill=col, outline=K, width=0.6)
    c.line([(x+2.5, y-12), (x+6, y-18)], K, 1.6)
    c.line([(x-2, y-5), (x-3, y)], K, 1.8); c.line([(x+2, y-5), (x+3, y)], K, 1.8)

# --- kites of different builds
def star_kite(cx, cy, r, cols, rot):
    n = 8
    pts = [(cx + (r if k % 2 == 0 else r*0.55)*math.cos(rot + k*math.pi/n), cy + (r if k % 2 == 0 else r*0.55)*math.sin(rot + k*math.pi/n)) for k in range(2*n)]
    for k in range(2*n):
        c.poly([(cx, cy), pts[k], pts[(k+1) % (2*n)]], fill=cols[k % len(cols)])
    c.poly(pts, outline=K, width=1.2)
    for k in range(0, 2*n, 2): c.line([(cx, cy), pts[k]], K, 0.8)
    c.ell(cx, cy, r*0.22, fill=Wh, outline=K, width=1)
    c.ell(cx, cy, r*0.1, fill=R)
def pandorga(cx, cy, r, cols, rot):
    # diamond with quartered colours and fringe
    top = (cx + r*1.2*math.sin(rot), cy - r*1.2*math.cos(rot)); bot = (cx - r*1.5*math.sin(rot), cy + r*1.5*math.cos(rot))
    lft = (cx - r*0.9*math.cos(rot), cy - r*0.9*math.sin(rot)); rgt = (cx + r*0.9*math.cos(rot), cy + r*0.9*math.sin(rot))
    q = [(top, rgt), (rgt, bot), (bot, lft), (lft, top)]
    for i, (a, b) in enumerate(q):
        c.poly([(cx, cy), a, b], fill=cols[i % len(cols)])
        # chevrons inside each quarter
        for t in (0.35, 0.65):
            c.line([((cx*(1-t)+a[0]*t), (cy*(1-t)+a[1]*t)), ((cx*(1-t)+b[0]*t), (cy*(1-t)+b[1]*t))], K, 0.6)
    c.poly([top, rgt, bot, lft], outline=K, width=1.2)
    c.line([top, bot], K, 1); c.line([lft, rgt], K, 1)
    for t in range(1, 10):  # fringe along the lower edges
        for a, b in ((rgt, bot), (bot, lft)):
            px, py = a[0]+(b[0]-a[0])*t/10, a[1]+(b[1]-a[1])*t/10
            c.line([(px, py), (px+rnd.uniform(-2, 2), py+5)], K, 0.6)
    return bot
def box_kite(cx, cy, s, cols):
    for dy in (-s*0.9, s*0.5):
        c.poly([(cx-s*0.5, cy+dy), (cx, cy+dy-s*0.25), (cx+s*0.5, cy+dy), (cx+s*0.5, cy+dy+s*0.45), (cx, cy+dy+s*0.7), (cx-s*0.5, cy+dy+s*0.45)], fill=cols[0], outline=K, width=1)
        c.poly([(cx, cy+dy-s*0.25+0.1), (cx+s*0.5, cy+dy), (cx+s*0.5, cy+dy+s*0.45), (cx, cy+dy+s*0.7)], fill=cols[1], outline=K, width=1)
        for k in range(1, 4):
            c.line([(cx+s*0.5*k/4, cy+dy-s*0.25+s*0.25*k/4), (cx+s*0.5*k/4, cy+dy+s*0.7-s*0.25*k/4)], K, 0.5)
    for x in (cx-s*0.5, cx, cx+s*0.5):
        c.line([(x, cy-s*0.9 - (s*0.25 if x == cx else 0)), (x, cy+s*0.95+(s*0.25 if x == cx else 0))], K, 1.2)
    return (cx, cy+s*1.2)

palettes = [(R, Y, Wh, G), (Y, R, B, Wh), (G, Wh, R, Y), (Wh, R, Y, B), (R, Wh, G, Y), (Y, G, R, Wh)]
specs = [  # type, x, y, size
    ("hex", 210, 120, 46), ("star", 72, 205, 34), ("pand", 300, 330, 30), ("box", 345, 165, 32),
    ("hex", 60, 400, 22), ("star", 235, 300, 22), ("pand", 160, 245, 20), ("hex", 270, 425, 16),
    ("star", 150, 40, 18), ("hex", 380, 270, 14), ("pand", 40, 70, 14), ("hex", 115, 470, 12),
]
anchors = []
for i, (t, x, y, s) in enumerate(specs):
    cols = palettes[i % len(palettes)]
    rot = rnd.uniform(-0.35, 0.35)
    # tail first so kite sits on top
    tl = tail_curve(x, y+s*0.8, s*3.2, s*0.4, n=24, seed=i, dirx=-0.35)
    if t == "hex":
        kite(c, x, y, s, cols=cols + cols[:2], rot=rot, tail=tl)
    elif t == "star":
        c.line(tl, K, 1)
        for j, (tx, ty) in enumerate(tl[3::4]):
            c.ell(tx, ty, max(2, s/9), fill=cols[j % 4], outline=K, width=0.6)
        star_kite(x, y, s, cols, rot)
    elif t == "pand":
        bot = pandorga(x, y, s, cols, rot)
        tl = tail_curve(bot[0], bot[1], s*3, s*0.35, n=24, seed=i+50, dirx=-0.3)
        c.line(tl, K, 1)
        for j, (tx, ty) in enumerate(tl[2::3]):
            c.poly([(tx-4, ty-3), (tx, ty), (tx-4, ty+3)], fill=cols[j % 4], outline=K, width=0.5)
            c.poly([(tx+4, ty-3), (tx, ty), (tx+4, ty+3)], fill=cols[j % 4], outline=K, width=0.5)
    else:
        box_kite(x, y, s, cols)
    anchors.append((x, y + s*0.2))

# strings: sagging curves from each kite to a child
kids.sort()
for i, (ax, ay) in enumerate(sorted(anchors, key=lambda a: a[0])):
    kx, ky = kids[min(len(kids)-1, int(i*len(kids)/len(anchors)))]
    pts = []
    for t in range(21):
        f = t/20
        pts.append((ax + (kx+6-ax)*f, ay + (ky-18-ay)*f + 30*math.sin(math.pi*f)*(1 - abs(ax-kx)/600)))
    c.line(pts, K, 0.7)
for i, (kx, ky) in enumerate(kids):
    child(kx, ky, [R, Y, Wh, G][i % 4])

# house fronts in the black band: windows, doors, a painted sign, caption
for x in range(6, 394, 22):
    if rnd.random() < 0.55:
        y = rnd.uniform(522, 540); col = rnd.choice([Y, Wh, R, G, B])
        c.rect(x, y, x+12, y+11, fill=col, outline=Wh if col == B else K, width=0.8)
        c.line([(x+6, y), (x+6, y+11)], K, 0.8); c.line([(x, y+5.5), (x+12, y+5.5)], K, 0.8)
c.line([(14, 556), (386, 556)], Y, 0.8)
c.text((200, 564), "JUANITO LAGUNA", Wh, size=13, anchor="mt")
c.text((200, 580), "remontando su barrilete  ·  A. Berni 1905–1981", Y, size=8.5, anchor="mt", bold=False)

# birds threading between kites
for _ in range(10):
    bx, by = rnd.uniform(20, 380), rnd.uniform(20, 440); s = rnd.uniform(3, 5)
    c.line([(bx-s, by-s*0.5), (bx, by), (bx+s, by-s*0.5)], K, 1.1)

c.save()
