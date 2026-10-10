# Night — "Rue d'Alésia, rain". In 1961 Cartier-Bresson photographed Giacometti crossing
# the street near his studio in the rain with his raincoat pulled up over his head: the
# Walking Man, walking. Here it's night. A Paris street in one-point perspective, mostly
# black: lamp heads and a few lit windows in yellow, a red café awning, wet cobbles that
# throw every light back as a broken vertical streak, rain slanting through the halos,
# a zebra crossing, and him, hunched under the coat, coming toward us.
import math, numpy as np
from PIL import Image, ImageDraw, ImageFont
from common import *

rng = np.random.default_rng(1961)
im = Image.new("RGB", (W, H), K); d = ImageDraw.Draw(im); d.fontmode = "1"
yy, xx = np.mgrid[0:H, 0:W].astype(float)
VX, VY = 214, 300
HORIZ = VY
scr = screen(H, W)

# sky: a sliver of low cloud lit orange-ish by the city (screened red/blue on black)
skym = yy < 140
a = np.asarray(im).copy()
cl = fbm(H, W, seed=3, base=4)
a[skym & (scr < (0.02 + cl*0.08) * (1 - yy/140))] = B
a[skym & (scr < 0.03*(cl > 0.6))] = R
im = Image.fromarray(a); d = ImageDraw.Draw(im); d.fontmode = "1"

def persp(x_edge, y_edge, t):
    """point t of the way from (x_edge, y_edge) toward the vanishing point."""
    return (x_edge + (VX - x_edge)*t, y_edge + (VY - y_edge)*t)

# ---------- façades: left and right walls, receding. Cornice lines, windows in bays
lights = []   # (x, y, colour, strength) for reflections
def facade(side):
    xe = 0 if side < 0 else W
    top_e, bot_e = 40, 440                          # edge-of-frame heights
    # roofline & cornices
    for frac in (0.0, 0.18, 0.36, 0.54, 0.72):
        ye = top_e + frac*(bot_e - top_e)
        p0 = (xe, ye); p1 = persp(xe, ye, 0.86)
        d.line([p0, p1], fill=B if frac in (0.0, 0.18) else K, width=1)
    # bays (building divisions) at t positions; window columns between them
    ts = np.cumsum(rng.uniform(0.05, 0.11, 30)); ts = ts[ts < 0.85]
    tsw = np.linspace(0, 0.85, 34)
    for i in range(len(tsw)-1):
        t0, t1 = tsw[i], tsw[i+1]
        if i % 3 == 2: continue                       # pier between window pairs
        for fl in range(5):
            f0 = 0.04 + fl*0.18; f1 = f0 + 0.11
            y0e = top_e + f0*(bot_e-top_e); y1e = top_e + f1*(bot_e-top_e)
            q = [persp(xe, y0e, t0+0.006), persp(xe, y0e, t1-0.006),
                 persp(xe, y1e, t1-0.006), persp(xe, y1e, t0+0.006)]
            lit = rng.random() < 0.13
            if lit:
                d.polygon(q, fill=Y)
                # curtain / mullion
                mx = (q[0][0]+q[1][0])/2
                d.line((mx, (q[0][1]+q[1][1])/2, mx, (q[2][1]+q[3][1])/2), fill=K)
                if rng.random() < 0.3:   # someone at the window
                    cx = mx + (q[1][0]-q[0][0])*0.25; cy = (q[2][1]+q[0][1])/2
                    sz = abs(q[1][0]-q[0][0])*0.18
                    d.ellipse((cx-sz, cy-sz*2.2, cx+sz, cy-sz*0.2), fill=K)
                    d.rectangle((cx-sz*1.5, cy-sz*0.4, cx+sz*1.5, q[2][1]), fill=K)
                lights.append(((q[0][0]+q[1][0])/2, (q[2][1]+q[3][1])/2, Y, abs(q[1][0]-q[0][0])))
            elif rng.random() < 0.4:
                d.polygon(q, outline=B)
            else:
                d.line([q[3], q[2]], fill=B)      # just the sill
            # wrought-iron balcony rail on the 2nd floor: a line with tiny balusters
            if fl == 1:
                yb = q[2][1] + 1
                d.line((q[3][0], yb, q[2][0], yb), fill=Wh if lit else B)
    # ground floor: shopfronts, mostly shuttered
    y0e, y1e = top_e + 0.86*(bot_e-top_e), bot_e
    for i in range(0, len(tsw)-3, 3):
        t0, t1 = tsw[i], tsw[i+3]
        q = [persp(xe, y0e, t0+0.01), persp(xe, y0e, t1-0.01), persp(xe, y1e, t1-0.01), persp(xe, y1e, t0+0.01)]
        d.polygon(q, outline=B)
        # shutters: horizontal slats
        for s in np.linspace(0.1, 0.9, 6):
            pa = (q[0][0]*(1-s)+q[3][0]*s, q[0][1]*(1-s)+q[3][1]*s)
            pb = (q[1][0]*(1-s)+q[2][0]*s, q[1][1]*(1-s)+q[2][1]*s)
            d.line([pa, pb], fill=B)
facade(-1); facade(1)

# ---------- the café on the right corner: red awning, lit window, chairs stacked
aw = [(W, 360), (300, 372), (306, 392), (W, 392)]
d.polygon(aw, fill=R)
for k in range(10):
    x = 306 + k*9.5
    d.line((x, 392, x+4, 400), fill=R, width=3)
f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 15)
d.text((318, 372), "CAFÉ", fill=Wh, font=f)
win = [(W, 400), (304, 404), (304, 438), (W, 444)]
d.polygon(win, fill=Y)
for x in (318, 338, 358, 380):  # chairs stacked on tables, silhouettes
    d.line((x, 424, x, 442), fill=K, width=2); d.line((x-7, 424, x+7, 423), fill=K, width=2)
    d.line((x-6, 424, x-8, 412), fill=K); d.line((x+6, 423, x+8, 411), fill=K)
d.line((304, 404, 304, 444), fill=K, width=3)
lights.append((350, 440, Y, 60)); lights.append((350, 392, R, 50))

# ---------- road and pavements: black, with the kerbs in blue
road_l = lambda y: VX + (0 - VX)*(y - VY)/(600 - VY)*1.25
road_r = lambda y: VX + (W - VX)*(y - VY)/(600 - VY)*1.25
for y in range(VY+2, H):
    d.point((road_l(y), y), fill=B); d.point((road_r(y), y), fill=B)
# cobbles: fan rows of arcs, faint, denser toward us
for row in range(60):
    y = VY + 6 + (row**1.6)*0.9
    if y > H: break
    sc = (y - VY)/300
    w_ = 8*sc + 1
    x = road_l(y)
    while x < road_r(y):
        if rng.random() < 0.4:
            d.arc((x, y-w_*0.35, x+w_*1.6, y+w_*0.35), 200, 340, fill=B)
        x += w_*1.6

# ---------- street lamps on the left pavement
for k, tl in enumerate((0.0, 0.32, 0.55, 0.70, 0.79)):
    bx, by = persp(30, 470, tl)
    s = 1 - tl*0.92
    top = by - 230*s
    d.line((bx, by, bx, top), fill=K, width=max(1, int(5*s)))
    d.line((bx, by, bx, top), fill=B if s > 0.4 else K, width=1)
    # lantern head
    hw = 9*s; hh = 16*s
    d.polygon([(bx-hw, top-hh*0.2), (bx+hw, top-hh*0.2), (bx+hw*0.7, top+hh*0.8), (bx-hw*0.7, top+hh*0.8)], fill=Y)
    d.polygon([(bx-hw*1.3, top-hh*0.2), (bx, top-hh*0.9), (bx+hw*1.3, top-hh*0.2)], fill=K)
    # halo: screened yellow falloff
    R_ = 60*s + 8
    m = ((xx-bx)**2 + (yy-top)**2) < R_**2
    fall = np.clip(1 - np.sqrt((xx-bx)**2 + (yy-top)**2)/R_, 0, 1)
    a = np.asarray(im).copy()
    a[m & (scr < fall**2*0.45) & (a.sum(-1) == 0)] = Y
    im = Image.fromarray(a); d = ImageDraw.Draw(im); d.fontmode = "1"
    lights.append((bx, top, Y, 18*s + 3))
    # pool of light on the pavement
    d.ellipse((bx-26*s, by-4*s, bx+30*s, by+6*s), outline=Y)

# ---------- reflections: broken vertical streaks on the wet road under every light
for (lx, ly, col, sz) in lights:
    # mirror about the road line under the light
    base = max(VY + 4, min(H, ly + (ly < 440)*0 ))
    y_road = 445 if lx > 300 else max(ly + 10, VY + 10)
    ref_len = min(H - y_road, 40 + sz*4)
    for k in range(int(ref_len/2)):
        y = y_road + k*2 + rng.integers(0, 2)
        if y >= H: break
        wob = rng.normal(0, 1.5 + k*0.06)
        w_ = sz*0.35*(1 - k/(ref_len/2))*rng.uniform(0.3, 1.2)
        if rng.random() < 0.75:
            d.line((lx + wob - w_, y, lx + wob + w_, y), fill=col if rng.random() < 0.85 else Wh)

# ---------- zebra crossing in the foreground, its white bars reflecting the lamps
for i in range(7):
    y0 = 520 + i*0  # bars run toward the vanishing point
for i in range(-4, 5):
    x0 = 200 + i*44; x1 = x0 + 26
    y0, y1 = 512, 560
    q = [(VX + (x0-VX)*0.93, y0), (VX + (x1-VX)*0.93, y0), (x1 + (x1-VX)*0.18, y1), (x0 + (x0-VX)*0.18, y1)]
    m = polymask(q)
    a = np.asarray(im).copy()
    a[m & (scr < 0.42)] = Wh
    im = Image.fromarray(a); d = ImageDraw.Draw(im); d.fontmode = "1"

# ---------- him: hunched under the raincoat, striding toward us
fx, fy = 176, 548
fig = Image.new("L", (W, H), 0); fd = ImageDraw.Draw(fig)
walker(fd, fx, fy, 170, 255, stride=0.65)
# the coat pulled up over the head: a tented shape from the shoulders to above the head
coat = [(fx-24, fy-60), (fx-30, fy-128), (fx-18, fy-168), (fx+4, fy-182), (fx+20, fy-170),
        (fx+30, fy-132), (fx+26, fy-60), (fx+10, fy-52), (fx-10, fy-54)]
fd.polygon(coat, fill=255)
fm = np.asarray(fig) > 0
a = np.asarray(im).copy()
a[fm] = K
# rim light from the lamps behind-left: the left edge of the silhouette in yellow, the right in blue
le = fm & ~np.roll(fm, 1, 1); re_ = fm & ~np.roll(fm, -1, 1)
a[le | np.roll(le, 1, 1)] = Y; a[re_] = B
te = fm & ~np.roll(fm, 1, 0); a[te] = Y
im = Image.fromarray(a); d = ImageDraw.Draw(im); d.fontmode = "1"
# folds in the coat
for k in range(5):
    x0 = fx - 16 + k*8
    d.line((x0, fy-160 + abs(k-2)*6, x0 + rng.normal(0, 2), fy-64), fill=B)
# his reflection, broken, beneath him
for k in range(26):
    y = fy + 3 + k*2
    if y >= H: break
    xs_ = np.where(fm[max(0, fy - 3 - k*2*3)])[0]
    if len(xs_) and rng.random() < 0.7:
        d.line((xs_.min() + rng.normal(0, 1.5), y, xs_.max() + rng.normal(0, 1.5), y), fill=B)

# ---------- rain: slanting strokes everywhere, brighter (white/yellow) inside the halos
for _ in range(1500):
    x = rng.uniform(-30, W); y = rng.uniform(0, H)
    L_ = rng.uniform(6, 16)
    pix = np.asarray(im)[int(min(y, H-1)), int(max(0, min(x, W-1)))]
    inhalo = tuple(pix) == Y
    col = Wh if inhalo else (B if rng.random() < 0.8 else Wh)
    if not inhalo and rng.random() < 0.78: continue
    d.line((x, y, x + L_*0.28, y + L_), fill=col)
# splashes on the road
for _ in range(220):
    x = rng.uniform(0, W); y = rng.uniform(VY + 40, H)
    s = (y - VY)/120
    d.arc((x, y, x + 3*s + 2, y + s + 1), 180, 360, fill=B if rng.random() < 0.8 else Wh)
save(im)
