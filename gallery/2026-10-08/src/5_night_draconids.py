# Night — "Draconids". Tonight (8–9 Oct 2026) the Draconid shower peaks under a moonless
# sky: dust from comet Giacobini–Zinner, not Biela, and harmless. The northern sky at
# 22:00 from latitude 45°N, real star positions (approx. J2000, from memory): Draco
# winding between the Dippers, Cassiopeia climbing in the north-east, meteors streaming
# from the dragon's head. Below: a field, a hayrick, a bare elm drawn branch by branch,
# a farmhouse with one window lit, and two people lying on a blanket, watching.
import math, numpy as np
from PIL import Image, ImageDraw
from h import *
rng = np.random.default_rng(2026_10_08)
LAT, LST = 45.0, 23.0
STARS = {
 "Eltanin": (17.94, 51.49, 2.2), "Rastaban": (17.51, 52.30, 2.8), "Grumium": (17.89, 56.87, 3.7), "nuDra": (17.53, 55.18, 4.9),
 "Altais": (19.21, 67.66, 3.1), "epsDra": (19.80, 70.27, 3.8), "chiDra": (18.35, 72.73, 3.6), "Aldhibah": (17.15, 65.71, 3.2),
 "etaDra": (16.40, 61.51, 2.7), "thetaDra": (16.03, 58.57, 4.0), "Edasich": (15.42, 58.97, 3.3), "Thuban": (14.07, 64.38, 3.7),
 "kapDra": (12.56, 69.79, 3.9), "Giausar": (11.52, 69.33, 3.8),
 "Dubhe": (11.06, 61.75, 1.8), "Merak": (11.03, 56.38, 2.4), "Phecda": (11.90, 53.69, 2.4), "Megrez": (12.26, 57.03, 3.3),
 "Alioth": (12.90, 55.96, 1.8), "Mizar": (13.40, 54.93, 2.2), "Alkaid": (13.79, 49.31, 1.9),
 "Polaris": (2.53, 89.26, 2.0), "Yildun": (17.54, 86.59, 4.4), "epsUMi": (16.77, 82.04, 4.2), "zetUMi": (15.73, 77.79, 4.3),
 "etaUMi": (16.29, 75.76, 5.0), "Kochab": (14.85, 74.16, 2.1), "Pherkad": (15.35, 71.83, 3.0),
 "Caph": (0.15, 59.15, 2.3), "Schedar": (0.68, 56.54, 2.2), "Navi": (0.95, 60.72, 2.2), "Ruchbah": (1.43, 60.24, 2.7), "Segin": (1.91, 63.67, 3.4),
 "Alderamin": (21.31, 62.59, 2.5), "Alfirk": (21.48, 70.56, 3.2), "Errai": (23.66, 77.63, 3.2), "iotCep": (22.83, 66.20, 3.5), "zetCep": (22.18, 58.20, 3.4),
 "Capella": (5.28, 46.00, 0.1), "Mirfak": (3.41, 49.86, 1.8), "Vega": (18.62, 38.78, 0.0), "Deneb": (20.69, 45.28, 1.3),
 "Sadr": (20.37, 40.26, 2.2), "Algol": (3.14, 40.96, 2.1), "Menkalinan": (6.00, 44.95, 1.9),
}
LINES = [("Rastaban", "Eltanin"), ("Eltanin", "Grumium"), ("Grumium", "nuDra"), ("nuDra", "Rastaban"), ("Grumium", "Altais"),
         ("Altais", "epsDra"), ("Altais", "chiDra"), ("chiDra", "Aldhibah"), ("Aldhibah", "etaDra"), ("etaDra", "thetaDra"),
         ("thetaDra", "Edasich"), ("Edasich", "Thuban"), ("Thuban", "kapDra"), ("kapDra", "Giausar"),
         ("Dubhe", "Merak"), ("Merak", "Phecda"), ("Phecda", "Megrez"), ("Megrez", "Dubhe"), ("Megrez", "Alioth"), ("Alioth", "Mizar"), ("Mizar", "Alkaid"),
         ("Polaris", "Yildun"), ("Yildun", "epsUMi"), ("epsUMi", "zetUMi"), ("zetUMi", "etaUMi"), ("etaUMi", "Pherkad"), ("Pherkad", "Kochab"), ("Kochab", "zetUMi"),
         ("Caph", "Schedar"), ("Schedar", "Navi"), ("Navi", "Ruchbah"), ("Ruchbah", "Segin"),
         ("Alderamin", "Alfirk"), ("Alfirk", "Errai"), ("Errai", "iotCep"), ("iotCep", "zetCep"), ("zetCep", "Alderamin"), ("iotCep", "Alfirk")]
LABELS = {"Eltanin": "DRACO", "Mizar": "URSA MAJOR", "Polaris": "Polaris", "Navi": "CASSIOPEIA", "Errai": "CEPHEUS", "Capella": "Capella", "Vega": "Vega"}
def altaz(ra, dec):
    ha = math.radians((LST - ra)*15); de = math.radians(dec); la = math.radians(LAT)
    alt = math.asin(math.sin(de)*math.sin(la) + math.cos(de)*math.cos(la)*math.cos(ha))
    az = math.atan2(-math.cos(de)*math.sin(ha), math.sin(de)*math.cos(la) - math.cos(de)*math.sin(la)*math.cos(ha))
    return alt, az   # az: 0 = north, positive east
AZ0, ALT0, SC = math.radians(-8), math.radians(40), 206*S
def proj(alt, az):  # stereographic about (ALT0, AZ0); east to the right as when facing north
    dz = az - AZ0
    k = 2/(1 + math.sin(ALT0)*math.sin(alt) + math.cos(ALT0)*math.cos(alt)*math.cos(dz))
    x = k*math.cos(alt)*math.sin(dz); y = k*(math.cos(ALT0)*math.sin(alt) - math.sin(ALT0)*math.cos(alt)*math.cos(dz))
    return W/2 + x*SC, H*0.50 - y*SC
P = {n: proj(*altaz(ra, de)) for n, (ra, de, m) in STARS.items()}
GROUND = lambda x: H - 150*S + 14*S*math.sin(x/(90*S)) + 6*S*math.sin(x/(23*S) + 1)

im = Image.new("RGB", (W, H), K); d = ImageDraw.Draw(im)
# horizon skyglow: blue screened up from the ground, so silhouettes read
yy = np.arange(H)[:, None].repeat(W, 1)
glow = np.clip(1 - (H - 150*S - yy)/(120*S), 0, 1)**1.8 * 0.38
a = np.array(im); a[screen(glow, 2)] = B; im = Image.fromarray(a); d = ImageDraw.Draw(im)
# Milky Way: stipple band through Cassiopeia/Cepheus/Cygnus
mw = [P["Capella"], P["Mirfak"], P["Navi"], P["Alderamin"], P["Deneb"]]
for i in range(9000):
    k = rng.integers(len(mw)-1); t = rng.random()
    x = mw[k][0] + (mw[k+1][0]-mw[k][0])*t + rng.normal(0, 26*S); y = mw[k][1] + (mw[k+1][1]-mw[k][1])*t + rng.normal(0, 26*S)
    x, y = int(x)//2*2, int(y)//2*2
    d.rectangle((x, y, x+1, y+1), fill=Wh if rng.random() < .8 else B)
# faint field stars
for i in range(700):
    x, y = int(rng.uniform(0, W))//2*2, int(rng.uniform(0, H))//2*2
    d.rectangle((x, y, x+1, y+1), fill=Wh)
# radiant (near Draco's head, RA 17.5h Dec +54) and meteors
rx_, ry_ = proj(*altaz(17.5, 54.0))
for i in range(11):
    ang = rng.uniform(0, 2*math.pi); r0 = rng.uniform(30, 160)*S; L = rng.uniform(40, 120)*S
    x0, y0 = rx_ + math.cos(ang)*r0, ry_ + math.sin(ang)*r0
    x1, y1 = x0 + math.cos(ang)*L, y0 + math.sin(ang)*L
    for k in range(20):   # tapered: thin red tail -> yellow -> white head
        t0, t1 = k/20, (k+1)/20
        col = R if k < 7 else (Y if k < 15 else Wh); wdt = 1 + int(k/4)
        d.line((x0 + (x1-x0)*t0, y0 + (y1-y0)*t0, x0 + (x1-x0)*t1, y0 + (y1-y0)*t1), fill=col, width=wdt)
    d.ellipse((x1-3*S, y1-3*S, x1+3*S, y1+3*S), fill=Wh)
d.ellipse((rx_-6*S, ry_-6*S, rx_+6*S, ry_+6*S), outline=R, width=2)
for k in range(8):
    aa = k*math.pi/4; d.line((rx_+math.cos(aa)*9*S, ry_+math.sin(aa)*9*S, rx_+math.cos(aa)*13*S, ry_+math.sin(aa)*13*S), fill=R, width=2)
# constellation lines, dotted blue
for a_, b_ in LINES:
    (x0, y0), (x1, y1) = P[a_], P[b_]; L = math.hypot(x1-x0, y1-y0); n = int(L/(7*S))
    for k in range(1, n):
        if k % 2 == 0: continue
        t0, t1 = k/n, (k+0.8)/n
        if 0.12 < t0 < 0.88: d.line((x0+(x1-x0)*t0, y0+(y1-y0)*t0, x0+(x1-x0)*t1, y0+(y1-y0)*t1), fill=B, width=3)
# named stars, sized by magnitude, a few tinted
TINT = {"Eltanin": Y, "Capella": Y, "Kochab": R, "Dubhe": Y, "Schedar": Y, "Mirfak": Wh, "Vega": Wh}
for n_, (ra, de, m) in STARS.items():
    x, y = P[n_]; r0 = max(2, (5.2 - m)*1.9)*S/2 + 1
    d.ellipse((x-r0, y-r0, x+r0, y+r0), fill=TINT.get(n_, Wh))
    if m < 2.3:
        for aa in (0, math.pi/2): d.line((x-math.cos(aa)*r0*2.4, y-math.sin(aa)*r0*2.4, x+math.cos(aa)*r0*2.4, y+math.sin(aa)*r0*2.4), fill=Wh, width=2)
f = serif(10*S, italic=True)
for n_, lab in LABELS.items():
    x, y = P[n_]; d.text((x + 8*S, y + 4*S), lab, font=f, fill=Y if lab.isupper() else Wh)

# --- ground: field of stubble in blue/black hatch, hayrick, fence, elm, house, two watchers
gpts = [(x, GROUND(x)) for x in range(0, W+8, 8)]
d.polygon(gpts + [(W, H), (0, H)], fill=K)
for i in range(800):   # stubble strokes, catching skyglow
    x = rng.uniform(0, W); y = rng.uniform(GROUND(x) + 6*S, H)
    L = (3 + (y - GROUND(x))/(150*S)*10)*S
    d.line((x, y, x + rng.normal(0, 1.5)*S, y - L), fill=B if rng.random() < .8 else G, width=2)
# farmhouse right, one window lit, smoke from chimney
hx = 300*S; hy = GROUND(hx) + 6*S
d.rectangle((hx, hy-40*S, hx+70*S, hy), fill=K); d.polygon([(hx-6*S, hy-40*S), (hx+35*S, hy-70*S), (hx+76*S, hy-40*S)], fill=K)
d.rectangle((hx+48*S, hy-78*S, hx+56*S, hy-56*S), fill=K)
d.rectangle((hx+12*S, hy-30*S, hx+26*S, hy-14*S), fill=Y); d.line((hx+19*S, hy-30*S, hx+19*S, hy-14*S), fill=K, width=3); d.line((hx+12*S, hy-22*S, hx+26*S, hy-22*S), fill=K, width=3)
for k in range(30): d.line((hx+12*S + k*0.5*S, hy-14*S, hx-10*S + k*1.6*S, hy+30*S), fill=Y if k % 3 == 0 else K, width=1)   # light spill on the stubble
d.polygon([(hx+12*S, hy-14*S), (hx+26*S, hy-14*S), (hx+40*S, hy+28*S), (hx-6*S, hy+28*S)], fill=None, outline=None)
# hayrick
kx = 180*S; ky = GROUND(kx) + 30*S
d.pieslice((kx-36*S, ky-56*S, kx+36*S, ky+16*S), 180, 360, fill=K); d.rectangle((kx-36*S, ky-20*S, kx+36*S, ky), fill=K)
for k in range(10): d.arc((kx-34*S + k*2*S, ky-54*S + k*3*S, kx+34*S - k*2*S, ky+14*S), 200, 340, fill=B, width=2)
# fence posts and wire, receding
for i in range(9):
    x = (8 + i*24)*S; y = GROUND(x) + (40 + i*0)*S; h_ = (28 - i*1.8)*S
    d.rectangle((x-2*S, y-h_, x+2*S, y), fill=K)
    if i: d.line((px_, py_, x, y-h_*0.7), fill=B, width=2); d.line((px_, py_ + 8*S, x, y-h_*0.35), fill=B, width=2)
    px_, py_ = x, y-h_*0.7
# the elm: recursive branching, a few last leaves
def branch(x, y, ang, L, w, depth):
    x2, y2 = x + math.cos(ang)*L, y + math.sin(ang)*L
    d.line((x, y, x2, y2), fill=K, width=max(2, int(w)))
    if depth == 0 or L < 5*S:
        if rng.random() < 0.05: d.ellipse((x2-2*S, y2-2*S, x2+2*S, y2+2*S), fill=Y if rng.random() < .6 else R)
        return
    n = 2 if rng.random() < 0.7 else 3
    for k in range(n):
        da = rng.uniform(0.18, 0.55)*(1 if k % 2 else -1) + rng.normal(0, 0.08)
        branch(x2, y2, ang + da, L*rng.uniform(0.68, 0.82), w*0.68, depth-1)
tx = 70*S; ty = GROUND(tx) + 18*S
d.polygon([(tx-14*S, ty), (tx-6*S, ty-30*S), (tx+6*S, ty-30*S), (tx+14*S, ty)], fill=K)
branch(tx, ty-28*S, -math.pi/2 + 0.10, 58*S, 20, 9)
# watchers: two figures lying on a red blanket, faces up
bx, by = 200*S, H - 78*S
d.polygon([(bx-80*S, by), (bx+70*S, by-6*S), (bx+86*S, by+26*S), (bx-66*S, by+32*S)], fill=R)
for k in range(9): d.line((bx-76*S + k*18*S, by - k*0.6*S, bx-62*S + k*18*S, by+31*S - k*0.6*S), fill=K, width=2)
for dy in (2*S, 16*S):
    d.ellipse((bx-62*S, by+dy-2*S, bx-46*S, by+dy+12*S), fill=K)               # head
    d.rounded_rectangle((bx-48*S, by+dy, bx+50*S, by+dy+11*S), radius=5*S, fill=K)   # body
    d.ellipse((bx-58*S, by+dy+1*S, bx-54*S, by+dy+5*S), fill=B)               # a glint of face
d.line((bx-30*S, by+12*S, bx-14*S, by-24*S), fill=K, width=6)                  # one arm, pointing up
d.ellipse((bx-18*S, by-30*S, bx-10*S, by-22*S), fill=K)
# caption
f = serif(11*S, italic=True); t = "Draconids · peak tonight · no moon"
w = d.textlength(t, font=f); d.text(((W-w)/2, H - 18*S), t, font=f, fill=B)
save(im)
