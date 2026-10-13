"""Midday — Latas: a pyramid of tin cans with invented labels, on a woodblock
ground. Berni built Juanito's world from flattened cans; here they are whole,
stacked like a corner-shop window. Red ground in charge; labels carry the rest."""
import math, random, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from common import *

rnd = random.Random(42)
c = C(R)

# --- woodblock ground: wavy grain lines around knots, black on red
knots = [(80, 120), (320, 70), (260, 300), (60, 420)]
for y0 in range(-20, 640, 5):
    pts = []
    for x in range(-10, 420, 4):
        y = y0 + 3*math.sin(x/37 + y0/53)
        for kx, ky in knots:
            dx, dy = x-kx, y-ky
            d2 = dx*dx + dy*dy*2.5
            y += 900*dy/(d2+300)
        pts.append((x, y))
    c.line(pts, K, 0.9 if (y0//5) % 3 else 1.6)
for kx, ky in knots:
    for r in range(3, 16, 3):
        c.ell(kx, ky, r*1.6, r*0.8, outline=K, width=0.9)
# gouges: short white chisel marks
for _ in range(110):
    x, y = rnd.uniform(0, W), rnd.uniform(0, H)
    l = rnd.uniform(4, 10)
    c.line([(x, y), (x+l, y+rnd.uniform(-1, 1))], Wh, 1.1)

# shelf / counter
c.rect(0, 520, W, 600, fill=K)
c.rect(0, 516, W, 524, fill=Y, outline=K, width=1)
for x in range(0, W, 12):
    c.line([(x, 524), (x+30, 600)], R, 0.8)

def can(cx, base, w, h, label):
    rx, ry = w/2, w*0.16
    top = base - h
    # body
    c.rect(cx-rx, top, cx+rx, base, fill=Wh)
    c.ell(cx, base, rx, ry, fill=Wh, outline=K, width=1.2)
    label(cx, top + h*0.14, base - h*0.12, rx)
    # cylindrical shading: hatched shadow on the right third, highlight strip left
    for i in range(14):
        f = 0.55 + i*0.032
        x = cx - rx + 2*rx*f
        c.line([(x, top+2), (x, base+ry*math.sqrt(max(0, 1-((x-cx)/rx)**2))-1)], K, 0.5 + i*0.06)
    c.rect(cx-rx*0.62, top+3, cx-rx*0.5, base-3, fill=Wh)
    # ribs above and below label
    for yy in (top + h*0.06, top + h*0.1, base - h*0.06):
        c.line([(cx-rx + rx*(1-math.cos(t/12*math.pi)), yy + ry*0.9*math.sin(t/12*math.pi)) for t in range(13)], K, 0.7)
    # lid
    c.ell(cx, top, rx, ry, fill=Wh, outline=K, width=1.4)
    c.ell(cx, top, rx*0.86, ry*0.8, outline=K, width=0.8)
    c.ell(cx, top, rx*0.7, ry*0.6, outline=K, width=0.5)
    c.line([(cx-rx, top), (cx-rx, base)], K, 1.4)
    c.line([(cx+rx, top), (cx+rx, base)], K, 1.4)

# ---- label designs: each fills the band y0..y1 across width 2rx (front view)
def band(col, cx, y0, y1, rx):
    c.rect(cx-rx, y0, cx+rx, y1, fill=col)
def lbl_tomate(cx, y0, y1, rx):
    band(R, cx, y0, y1, rx); m = (y0+y1)/2
    c.rect(cx-rx, y0, cx+rx, y0+5, fill=G); c.rect(cx-rx, y1-5, cx+rx, y1, fill=G)
    c.ell(cx-rx*0.15, m+2, rx*0.4, fill=R, outline=K, width=1)
    c.ell(cx-rx*0.27, m-4, rx*0.08, rx*0.05, fill=Wh)
    c.poly([(cx-rx*0.15, m-rx*0.35), (cx-rx*0.4, m-rx*0.5), (cx-rx*0.1, m-rx*0.42), (cx+rx*0.1, m-rx*0.58), (cx, m-rx*0.35)], fill=G, outline=K, width=0.6)
    c.text((cx-rx*0.15, y0+7), "TOMATE", Wh, size=max(7, rx*0.26), anchor="mt")
def lbl_sardina(cx, y0, y1, rx):
    band(B, cx, y0, y1, rx); m = (y0+y1)/2
    for k in range(3):
        yy = y0 + (y1-y0)*(0.35+k*0.2); xx = cx - rx*0.55 + (k % 2)*rx*0.15
        c.ell(xx+rx*0.25, yy, rx*0.32, rx*0.09, fill=Wh, outline=K, width=0.6)
        c.poly([(xx-rx*0.07, yy), (xx-rx*0.18, yy-rx*0.08), (xx-rx*0.18, yy+rx*0.08)], fill=Wh, outline=K, width=0.6)
        c.ell(xx+rx*0.47, yy-1, 1, fill=K)
    for yy in range(int(y0)+2, int(y1), 4):
        c.line([(cx+rx*0.35, yy), (cx+rx, yy)], Y, 0.8)
    c.text((cx-rx*0.15, y0+3), "SARDINAS", Y, size=max(6, rx*0.2), anchor="mt")
def lbl_dulce(cx, y0, y1, rx):
    band(Y, cx, y0, y1, rx); m = (y0+y1)/2
    c.ell(cx-rx*0.1, m, rx*0.62, (y1-y0)*0.38, fill=Wh, outline=B, width=2)
    c.text((cx-rx*0.1, m-5), "DULCE", B, size=max(7, rx*0.24), anchor="mm")
    c.text((cx-rx*0.1, m+6), "de leche", R, size=max(6, rx*0.17), anchor="mm", bold=False)
    for t in range(9):
        a = t/9*2*math.pi; c.ell(cx-rx*0.1 + rx*0.68*math.cos(a), m + (y1-y0)*0.44*math.sin(a), 1.4, fill=R)
def lbl_yerba(cx, y0, y1, rx):
    band(G, cx, y0, y1, rx); m = (y0+y1)/2
    for k in range(7):
        a = -math.pi/2 + (k-3)*0.35
        x2, y2 = cx-rx*0.1 + rx*0.55*math.cos(a), m+6 + rx*0.55*math.sin(a)
        c.poly([(cx-rx*0.1, m+6), (x2-3, y2+2), (x2, y2-2), (x2+3, y2+2)], fill=Y, outline=K, width=0.5)
    c.rect(cx-rx, y1-9, cx+rx, y1, fill=K)
    c.text((cx-rx*0.1, y1-4.5), "YERBA", Y, size=max(6, rx*0.2), anchor="mm")
def lbl_stripe(cx, y0, y1, rx):
    band(Wh, cx, y0, y1, rx)
    cols = [R, Y, B, G]
    yy, i = y0, 0
    while yy < y1:
        c.rect(cx-rx, yy, cx+rx, min(y1, yy+4), fill=cols[i % 4]); yy += 7; i += 1
    c.ell(cx-rx*0.1, (y0+y1)/2, rx*0.36, fill=K)
    c.text((cx-rx*0.1, (y0+y1)/2), "13", Wh, size=max(7, rx*0.3), anchor="mm")
def lbl_star(cx, y0, y1, rx):
    band(K, cx, y0, y1, rx); m = (y0+y1)/2; r = (y1-y0)*0.36
    pts = [(cx-rx*0.1 + (r if k % 2 == 0 else r*0.45)*math.cos(-math.pi/2 + k*math.pi/5),
            m + (r if k % 2 == 0 else r*0.45)*math.sin(-math.pi/2 + k*math.pi/5)) for k in range(10)]
    c.poly(pts, fill=Y, outline=R, width=1)
    for xx in range(int(cx-rx), int(cx+rx), 5):
        c.ell(xx, y0+3, 1.1, fill=R); c.ell(xx, y1-3, 1.1, fill=R)
def lbl_kite(cx, y0, y1, rx):
    band(B, cx, y0, y1, rx); m = (y0+y1)/2
    kite(c, cx-rx*0.15, m-2, (y1-y0)*0.32, rot=0.2)
    c.text((cx-rx*0.1, y1-3), "LAGUNA", Wh, size=max(6, rx*0.19), anchor="mb")
def lbl_check(cx, y0, y1, rx):
    band(Wh, cx, y0, y1, rx)
    for xx in range(int(cx-rx), int(cx+rx), 6):
        for yy in range(int(y0), int(y1), 6):
            if ((xx-int(cx-rx))//6 + (yy-int(y0))//6) % 2 == 0:
                c.rect(xx, yy, xx+6, yy+6, fill=G)
    c.rect(cx-rx*0.6, (y0+y1)/2-7, cx+rx*0.4, (y0+y1)/2+7, fill=R, outline=K, width=1)
    c.text((cx-rx*0.1, (y0+y1)/2), "ARVEJAS", Wh, size=max(6, rx*0.17), anchor="mm")

LABELS = [lbl_tomate, lbl_sardina, lbl_dulce, lbl_yerba, lbl_stripe, lbl_star, lbl_check, lbl_tomate, lbl_sardina, lbl_dulce]

# pyramid 4-3-2-1, plus one big can in front-left and a fallen one
order = [lbl_tomate, lbl_sardina, lbl_dulce, lbl_yerba,
         lbl_check, lbl_stripe, lbl_star,
         lbl_sardina, lbl_dulce,
         lbl_kite]
w, h = 74, 92
idx = 0
base = 518
for row, n in enumerate([4, 3, 2, 1]):
    for i in range(n):
        cx = W/2 + (i - (n-1)/2)*(w+4) + rnd.uniform(-2, 2)
        can(cx, base - row*(h+3), w, h, order[idx]); idx += 1

# fallen can rolling at right, seen end-on: concentric ribs
fx, fy = 345, 548
c.ell(fx, fy, 30, fill=Wh, outline=K, width=1.5)
for r in range(26, 4, -4):
    c.ell(fx, fy, r, outline=K, width=0.7)
c.ell(fx, fy, 3, fill=K)
# can opener key & bent lid at left
c.poly([(28, 560), (70, 548), (73, 556), (31, 568)], fill=Y, outline=K, width=1)
c.ell(76, 552, 7, outline=K, width=2)
# price tag on a string
c.line([(W/2, 518-3*(h+3)-h-10), (W/2 + 60, 30)], K, 0.8)
c.poly([(W/2+50, 30), (W/2+92, 22), (W/2+98, 46), (W/2+56, 54)], fill=Wh, outline=K, width=1.2)
c.ell(W/2+56, 38, 2.5, fill=K)
c.text((W/2+78, 38), "$13", R, size=12, anchor="mm")

c.save()
