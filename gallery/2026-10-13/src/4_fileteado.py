"""Evening — Fileteado porteño: the scroll-and-ribbon sign painting of Buenos
Aires buses and shopfronts. Black ground, mirrored acanthus scrolls, a carnation,
a kite in the crest, and a ribbon with a dedication. Every leaf has its highlight."""
import math, random, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from common import *

c = C(K)
MX = W/2

def mirror(pts):
    return [(2*MX - x, y) for x, y in pts]

def band_poly(path, w0, w1):
    """thick tapered band along a path -> polygon"""
    L, Rr = [], []
    n = len(path)
    for i, (x, y) in enumerate(path):
        a = path[max(0, i-1)]; b = path[min(n-1, i+1)]
        dx, dy = b[0]-a[0], b[1]-a[1]; d = math.hypot(dx, dy) or 1
        nx, ny = -dy/d, dx/d
        w = w0 + (w1-w0)*i/(n-1)
        L.append((x+nx*w/2, y+ny*w/2)); Rr.append((x-nx*w/2, y-ny*w/2))
    return L + Rr[::-1], L, Rr

def spiral(cx, cy, r0, turns, a0, sign=1, n=90, decay=0.16):
    pts = []
    for i in range(n):
        t = i/(n-1)*turns*2*math.pi
        r = r0*math.exp(-decay*t)
        pts.append((cx + r*math.cos(a0 + sign*t), cy + r*math.sin(a0 + sign*t)))
    return pts

def scroll(path, w0, w1, col, hi, both=True, leaves=True, leafcol=None, seed=0):
    rnd = random.Random(seed)
    sides = [False, True] if both else [False]
    for mir in sides:
        p = mirror(path) if mir else path
        poly, L, Rr = band_poly(p, w0, w1)
        # acanthus lobes along the outer edge
        if leaves:
            n = len(L)
            ctr = p[-1]
            dist = lambda q: math.hypot(q[0]-ctr[0], q[1]-ctr[1])
            Lo, Ri = (L, Rr) if dist(L[n//3]) > dist(Rr[n//3]) else (Rr, L)
            for i in range(8, int(n*0.62), 9):
                j = i + 7
                # outward normal at the lobe base
                ox, oy = Lo[i][0]-Ri[i][0], Lo[i][1]-Ri[i][1]; d = math.hypot(ox, oy) or 1
                ox, oy = ox/d, oy/d
                size = (w0*(1 - i/n) + 6) * 0.95
                # tip swept back against the direction of travel, then curled
                back = Lo[max(0, i-6)]
                tip = (back[0] + ox*size, back[1] + oy*size)
                curl = (tip[0] + (Lo[i][0]-back[0])*0.5 - ox*size*0.25, tip[1] + (Lo[i][1]-back[1])*0.5 - oy*size*0.25)
                mid1 = (Lo[i][0] + ox*size*0.55, Lo[i][1] + oy*size*0.55)
                mid2 = (Lo[j][0] + ox*size*0.35, Lo[j][1] + oy*size*0.35)
                pts = [Lo[j], mid2, mid1, tip, curl, ((mid1[0]+Lo[i][0])/2, (mid1[1]+Lo[i][1])/2), Lo[i]]
                c.poly(pts, fill=leafcol or col, outline=K, width=0.9)
                c.line([((Lo[i][0]+Lo[j][0])/2, (Lo[i][1]+Lo[j][1])/2), mid1, tip], hi, 0.9)
                c.ell(curl[0], curl[1], 1.3, fill=Wh)
        c.poly(poly, fill=col, outline=K, width=1)
        # shading: a darker inner stripe and a bright highlight line
        inner = [((a[0]*0.35+b[0]*0.65), (a[1]*0.35+b[1]*0.65)) for a, b in zip(L, Rr)]
        c.line(inner[:-6], hi, 1.4)
        inner2 = [((a[0]*0.12+b[0]*0.88), (a[1]*0.12+b[1]*0.88)) for a, b in zip(L, Rr)]
        c.line(inner2[:-8], K, 0.8)
        # little white tip dot at curl centre
        c.ell(p[-1][0], p[-1][1], max(1.6, w1*0.8), fill=Wh)

# --- frame: double fillet line with corner returns
def fillet_frame(m, col, w):
    c.rect(m, m, W-m, H-m, outline=col, width=w)
fillet_frame(10, R, 2.2); fillet_frame(15, Y, 1); fillet_frame(19, Wh, 0.6)
# corner returns (small squares turned inward)
for sx in (1, -1):
    for sy in (1, -1):
        x0 = 10 if sx == 1 else W-10; y0 = 10 if sy == 1 else H-10
        c.rect(min(x0, x0+sx*22), min(y0, y0+sy*22), max(x0, x0+sx*22), max(y0, y0+sy*22), outline=R, width=2.2)
        c.ell(x0+sx*11, y0+sy*11, 3.5, fill=Y)

# --- big corner scrolls (top), mirrored
top_path = spiral(118, 132, 70, 1.25, math.pi*1.05, sign=1, n=110)
top_path = [(30 + t*0.9, 40) for t in range(0, 60, 6)][::1] and top_path
scroll(spiral(112, 118, 78, 1.3, math.pi*1.15, sign=1, n=120), 26, 4, R, Y, leafcol=R, seed=1)
scroll(spiral(80, 205, 42, 1.4, math.pi*0.55, sign=-1, n=90), 15, 3, G, Y, leafcol=G, seed=2)
# bottom scrolls
scroll(spiral(108, 498, 74, 1.3, math.pi*0.85, sign=-1, n=120), 26, 4, B, Wh, leafcol=B, seed=3)
scroll(spiral(84, 392, 40, 1.4, math.pi*1.45, sign=1, n=90), 14, 3, Y, Wh, leafcol=Y, seed=4)


# --- ribbon banner with text (white/blue, Argentine colours)
def ribbon(y, text, size):
    tw = 230; h = 30
    # tails
    for s in (1, -1):
        xo = MX + s*tw/2
        c.poly([(xo, y-h/2+5), (xo + s*34, y-h/2+10), (xo + s*24, y+h/2-2 + 8), (xo + s*40, y+h/2+14), (xo, y+h/2+6)], fill=B, outline=K, width=1)
        c.line([(xo+s*4, y-h/2+10), (xo+s*28, y-h/2+14)], Wh, 1)
    # main band, gently arched
    top = [(MX - tw/2 + tw*t/20, y - h/2 - 8*math.sin(math.pi*t/20)) for t in range(21)]
    bot = [(x, yy + h) for x, yy in top]
    c.poly(top + bot[::-1], fill=Wh, outline=K, width=1.4)
    c.line([(x, yy+4) for x, yy in top], B, 1.2)
    c.line([(x, yy-4) for x, yy in bot], B, 1.2)
    c.text((MX, y - 6), text, R, size=size, anchor="mm")

# --- centre: a carnation (clavel) between two leaves, a kite crest above
cx, cy = MX, 312
# stem leaves
for s in (1, -1):
    leaf = [(cx, cy+40)] + [(cx + s*(70*math.sin(math.pi*t/12)), cy+40 - t*5 - s*0) for t in range(1, 13)]
    leaf2 = [(cx + s*(30*math.sin(math.pi*t/12)), cy+40 - t*5) for t in range(12, -1, -1)]
    pts = [(cx + s*(60*math.sin(math.pi*t/14) + t*2), cy+70 - t*4) for t in range(15)]
    poly, L, Rr = band_poly(pts, 4, 18)
    c.poly(poly, fill=G, outline=K, width=1)
    c.line([((a[0]+b[0])/2, (a[1]+b[1])/2) for a, b in zip(L, Rr)], Y, 1)
c.line([(cx, cy+20), (cx, cy+92)], G, 4)
# petals: three rings of serrated petals
for ring, (r, col, hi) in enumerate([(44, R, Wh), (33, Wh, R), (22, R, Y)]):
    n = 14 - ring*3
    for k in range(n):
        a = -math.pi/2 + (k + 0.5*ring)/n*2*math.pi
        p0 = (cx + r*0.35*math.cos(a-0.3), cy + r*0.35*math.sin(a-0.3))
        p1 = (cx + r*math.cos(a-0.18), cy + r*math.sin(a-0.18))
        p2 = (cx + r*1.08*math.cos(a), cy + r*1.08*math.sin(a))
        p3 = (cx + r*math.cos(a+0.18), cy + r*math.sin(a+0.18))
        p4 = (cx + r*0.35*math.cos(a+0.3), cy + r*0.35*math.sin(a+0.3))
        c.poly([p0, p1, p2, p3, p4], fill=col, outline=K, width=0.9)
        c.line([(cx + r*0.5*math.cos(a), cy + r*0.5*math.sin(a)), (cx + r*0.92*math.cos(a), cy + r*0.92*math.sin(a))], hi, 0.8)
c.ell(cx, cy, 9, fill=Y, outline=K, width=1)
for k in range(8):
    a = k/8*2*math.pi; c.ell(cx+5*math.cos(a), cy+5*math.sin(a), 1.2, fill=R)

# small birds (golondrinas) either side of the flower
for s in (1, -1):
    bx, by = cx + s*112, cy - 20
    s = s*1.6
    body = [(bx - s*18, by+4), (bx - s*4, by-6), (bx + s*14, by-2), (bx + s*20, by+2), (bx + s*6, by+6)]
    c.poly(body, fill=B, outline=K, width=1)
    c.poly([(bx - s*2, by-4), (bx - s*4, by-26), (bx + s*10, by-6)], fill=B, outline=K, width=1)
    c.line([(bx - s*2, by-6), (bx - s*3, by-20)], Wh, 0.8)
    c.poly([(bx - s*18, by+4), (bx - s*34, by-2), (bx - s*26, by+6), (bx - s*36, by+12)], fill=B, outline=K, width=1)
    c.poly([(bx + s*4, by+2), (bx + s*18, by+2), (bx + s*6, by+6)], fill=Wh)
    c.ell(bx + s*12, by-2, 1.6, fill=Wh)
    c.poly([(bx + s*20, by), (bx + s*26, by+2), (bx + s*20, by+3)], fill=Y)

# kite crest at the top, between the top scrolls
kite(c, MX, 92, 34, cols=(R, Y, B, Wh, G, Y), rot=0, frame=K)
for s in (1, -1):
    c.line([(MX + s*36, 92), (MX + s*60, 92)], Y, 1.2)
    c.ell(MX + s*64, 92, 3, fill=R)

ribbon(186, "PARA JUANITO", 17)

# bottom lettering: shaded, filete style
c.text((MX+1.5, 418+1.5), "13 · X", B, size=30, anchor="mm")
c.text((MX, 418), "13 · X", Y, size=30, anchor="mm")
c.text((MX, 446), "la ciudad hecha de latas", Wh, size=11, anchor="mm", bold=False)

# dotted fillet lines around the centre panel
for t in range(0, 360, 6):
    a = math.radians(t)
    x = MX + 96*math.cos(a); y = cy + 66*math.sin(a)
    c.ell(x, y, 1.1, fill=Wh if t % 12 else Y)

c.save()
