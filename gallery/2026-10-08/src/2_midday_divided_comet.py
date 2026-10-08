# Midday — "The divided comet". A 19th-century astronomical plate: Biela's comet, seen to
# split in two in the winter of 1845–46, over an observatory on a hill; beneath, four
# eyepiece sketches of the pair drawing apart (the 1852 return last). In 1883 Ignatius
# Donnelly blamed its fragments for the fires of 8 October 1871. Paper white, blue sky
# engraved in white line, red for the plate's lettering.
import math, numpy as np
from PIL import Image, ImageDraw
from h import *
rng = np.random.default_rng(1846)
def s(*v): return [x*S for x in v]
im = Image.new("RGB", (W, H), Wh); d = ImageDraw.Draw(im)

# plate border: double rule, red inner
d.rectangle(s(8, 8, 392, 592), outline=K, width=4); d.rectangle(s(13, 13, 387, 587), outline=R, width=2)
ft = serif(15*S, bold=True); fi = serif(11*S, italic=True); fs = serif(10*S)
def ctext(y, t, f, col=K):
    w = d.textlength(t, font=f); d.text(((W-w)/2, y*S), t, font=f, fill=col)
ctext(22, "THE  DIVIDED  COMET", ft)
ctext(41, "Comet of Biela, as seen in two parts — Plate VIII", fi, R)

# --- main panel
X0, Y0, X1, Y1 = 26, 60, 374, 404
P = (X0*S, Y0*S, X1*S, Y1*S)
sky = Image.new("RGB", (W, H), B); sd = ImageDraw.Draw(sky)
# engraved line-sky: horizontal white rules, thicker high up (deeper sky = sparser lines, lighter low down)
for y in range(Y0*S, Y1*S, 6):
    t = (y - Y0*S)/((Y1-Y0)*S)
    if t > 0.25: sd.line((X0*S, y, X1*S, y), fill=Wh, width=1 + int(t*3.2))
# stars: several hundred, a few bright with rays
for i in range(520):
    x, y = rng.uniform(X0*S, X1*S), rng.uniform(Y0*S, (Y0+260)*S); m = rng.random()**3
    r0 = 1 + m*4
    sd.ellipse((x-r0, y-r0, x+r0, y+r0), fill=Wh if m < .7 else Y)
    if m > 0.45:
        for a in range(4):
            aa = a*math.pi/4*2 + 0.3
            sd.line((x-math.cos(aa)*r0*3, y-math.sin(aa)*r0*3, x+math.cos(aa)*r0*3, y+math.sin(aa)*r0*3), fill=Wh, width=2)
# the two comets: heads lower left, tails sweeping up-right, slightly divergent
def comet(hx, hy, length, ang, spread, nstreaks, headr, col):
    for i in range(nstreaks):
        a = ang + rng.normal(0, spread); L = length*rng.uniform(0.35, 1.0); curve = rng.normal(0.0, 0.05) + 0.08
        pts = []
        for t in np.linspace(0, 1, 30):
            aa = a + curve*t
            pts.append((hx + math.cos(aa)*L*t + rng.normal(0, 0.4), hy + math.sin(aa)*L*t + rng.normal(0, 0.4)))
        # break the streak into dashes that thin out with distance
        for j in range(len(pts)-1):
            if rng.random() < 0.85 - 0.6*j/len(pts): sd.line((pts[j], pts[j+1]), fill=col, width=2 if j < 10 else 1)
    for rr, c in [(headr*2.6, B), (headr*2.2, Wh), (headr*1.9, B), (headr*1.5, Wh), (headr*1.15, Y), (headr*0.6, Wh)]:
        if c == B: sd.ellipse((hx-rr, hy-rr, hx+rr, hy+rr), outline=Wh, width=1)
        else: sd.ellipse((hx-rr, hy-rr, hx+rr, hy+rr), fill=c)
comet(118*S, 214*S, 420, -0.72, 0.075, 170, 13, Wh)
comet(150*S, 230*S, 330, -0.62, 0.065, 120, 10, Wh)
# hill, observatory, trees, a house — black silhouettes with white engraved highlights
hill = [(X0*S, 405*S)]
for x in np.linspace(X0, X1, 120):
    hill.append((x*S, (330 - 28*math.exp(-((x-260)/70)**2) + 8*math.sin(x/17) + 3*math.sin(x/5))*S))
hill.append((X1*S, 405*S)); sd.polygon(hill, fill=K)
for i in range(70):  # contour hatching on the hill
    x = rng.uniform(X0, X1); y = rng.uniform(340, 400); L = rng.uniform(6, 20)
    sd.line(s(x, y, x+L, y-1), fill=G, width=2)
ox, oy = 262*S, 292*S   # observatory: drum + dome with open slit and the telescope tube poking out
sd.rectangle((ox-34*S, oy, ox+34*S, oy+30*S), fill=Wh, outline=K, width=3)
for yy in range(oy+6, oy+30*S, 8): sd.line((ox-32*S, yy, ox+32*S, yy), fill=K, width=1)   # clapboard
sd.pieslice((ox-38*S, oy-36*S, ox+38*S, oy+36*S), 180, 360, fill=Wh, outline=K, width=3)
for a in range(190, 360, 14):   # dome ribs
    aa = math.radians(a); sd.line((ox, oy, ox+math.cos(aa)*38*S, oy+math.sin(aa)*36*S), fill=K, width=1)
sd.polygon([(ox-6*S, oy), (ox+6*S, oy), (ox+2*S, oy-36*S), (ox-10*S, oy-35*S)], fill=K)       # slit
tl = [(ox-2*S, oy-14*S), (ox-40*S, oy-56*S)]
sd.line(tl, fill=K, width=10); sd.line(tl, fill=Y, width=4)
sd.rectangle((ox-12*S, oy+12*S, ox-2*S, oy+30*S), fill=K); sd.rectangle((ox+10*S, oy+8*S, ox+22*S, oy+18*S), fill=Y, outline=K, width=2)
sd.line((ox+16*S, oy+8*S, ox+16*S, oy+18*S), fill=K, width=2)
# keeper's house with a lit window and smoke
hx, hy = 92*S, 340*S
sd.rectangle((hx, hy, hx+44*S, hy+26*S), fill=Wh, outline=K, width=3)
sd.polygon([(hx-4*S, hy), (hx+22*S, hy-18*S), (hx+48*S, hy)], fill=R, outline=K)
for yy in range(hy-16*S, hy, 6): sd.line((hx, yy, hx+44*S, yy), fill=K, width=1)
sd.polygon([(hx-4*S, hy), (hx+22*S, hy-18*S), (hx+48*S, hy)], outline=K, width=3)
for wx in (6, 28): sd.rectangle((hx+wx*S, hy+7*S, hx+(wx+10)*S, hy+17*S), fill=Y, outline=K, width=2)
sd.rectangle((hx+32*S, hy-22*S, hx+38*S, hy-8*S), fill=K)
for i in range(16):
    t = i/15; sx, sy = hx+35*S + math.sin(t*5)*8*S + t*40*S, hy-24*S - t*60*S
    sd.ellipse((sx-(2+t*5)*S, sy-(2+t*4)*S, sx+(2+t*5)*S, sy+(2+t*4)*S), outline=Wh, width=2)
# poplars and pines along the ridge
for x in list(np.linspace(34, 80, 4)) + list(np.linspace(150, 210, 5)) + list(np.linspace(310, 368, 5)):
    base = 330 - 28*math.exp(-((x-260)/70)**2) + 8*math.sin(x/17) + 3*math.sin(x/5)
    h_ = rng.uniform(26, 50); w_ = rng.uniform(6, 10)
    if rng.random() < 0.5:
        sd.polygon(s(x, base-h_, x-w_, base+2, x+w_, base+2), fill=K)
        for k in range(5):
            yy = base - h_ + (k+1)*h_/6; ww = w_*(k+1)/6
            sd.line(s(x-ww, yy+3, x, yy, x+ww, yy+3), fill=G, width=2)
    else:
        sd.ellipse(s(x-w_*0.7, base-h_, x+w_*0.7, base+2), fill=K)
        for k in range(6): sd.line(s(x, base - h_*(k+1)/7, x + w_*0.5, base - h_*(k+1)/7 - 3), fill=G, width=2)
# a figure at the gate, looking up
fx, fy = 214*S, 318*S
sd.ellipse((fx-4*S, fy-26*S, fx+4*S, fy-18*S), fill=K); sd.polygon([(fx-6*S, fy-18*S), (fx+6*S, fy-18*S), (fx+9*S, fy+4*S), (fx-9*S, fy+4*S)], fill=K)
sd.line((fx+3*S, fy-14*S, fx+14*S, fy-28*S), fill=K, width=4)
mask = Image.new("L", (W, H), 0); ImageDraw.Draw(mask).rectangle(P, fill=255)
im.paste(sky, (0, 0), mask)
d.rectangle(P, outline=K, width=4)
# degree ticks round the panel, like a chart
for x in range(X0, X1+1, 6):
    L = 6 if (x-X0) % 30 == 0 else 3; d.line(s(x, Y0-L, x, Y0), fill=K, width=2)
for y in range(Y0, Y1+1, 6):
    L = 6 if (y-Y0) % 30 == 0 else 3; d.line(s(X1, y, X1+L, y), fill=K, width=2); d.line(s(X0-L, y, X0, y), fill=K, width=2)
d.text(s(X0+6, Y0+6), "A", font=serif(13*S, bold=True), fill=Y); d.text(s(X0+52, Y0+170), "B", font=serif(13*S, bold=True), fill=Y)

# --- four eyepiece sketches
labels = [("I", "Dec. 1845"), ("II", "Jan. 1846"), ("III", "Feb. 1846"), ("IV", "Sept. 1852")]
seps = [0.0, 6, 13, 26]
for i, ((num, lab), sep) in enumerate(zip(labels, seps)):
    cx, cy, r = (58 + i*95)*S, 460*S, 38*S
    d.ellipse((cx-r-6, cy-r-6, cx+r+6, cy+r+6), fill=K)
    d.ellipse((cx-r, cy-r, cx+r, cy+r), fill=Wh)
    for k in range(2 if sep else 1):
        hx_ = cx - (sep*S*0.5 if k == 0 else -sep*S*0.5); hy_ = cy + (k*sep*0.35*S) + 4*S
        bright = 1.0 if k == 0 else 0.7
        for j in range(int(900*bright)):   # stippled coma + tail toward upper right
            rr = abs(rng.normal(0, 4.5*S)); a = rng.normal(-0.75, 0.32)
            tail = rng.random() < 0.6
            px = hx_ + (math.cos(a)*rr*5 if tail else rng.normal(0, 3*S)); py = hy_ + (math.sin(a)*rr*5 if tail else rng.normal(0, 3*S))
            px, py = int(px)//2*2, int(py)//2*2
            if (px-cx)**2 + (py-cy)**2 < (r-3)**2: d.rectangle((px, py, px+1, py+1), fill=K)
        d.ellipse((hx_-3*S, hy_-3*S, hx_+3*S, hy_+3*S), fill=K)
    d.line((cx-r, cy, cx-r+8*S, cy), fill=R, width=2); d.line((cx+r-8*S, cy, cx+r, cy), fill=R, width=2)
    d.line((cx, cy-r, cx, cy-r+8*S), fill=R, width=2); d.line((cx, cy+r-8*S, cx, cy+r), fill=R, width=2)
    w = d.textlength(num, font=serif(12*S, bold=True)); d.text((cx-w/2, cy+r+8*S), num, font=serif(12*S, bold=True), fill=R)
    w = d.textlength(lab, font=fi); d.text((cx-w/2, cy+r+23*S), lab, font=fi, fill=K)
# --- caption
d.line(s(60, 540, 340, 540), fill=K, width=2)
ctext(546, "Fig. A, the leading nucleus; B, its companion.", fi)
ctext(561, "Blamed in 1883 for the fires of 8 October 1871.", fi, R)
save(im)
