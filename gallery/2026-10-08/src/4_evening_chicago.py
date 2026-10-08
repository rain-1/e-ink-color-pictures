# Evening — "Chicago, 8 October 1871". After the Currier & Ives prints: the city seen across
# the river as the fire, driven by a south-west wind, takes the business district. Smoke
# rolls off to the north-east, sparks with it; the Water Tower stands white in front;
# schooners in the river and a swing bridge crowded with people carrying what they could.
import math, numpy as np
from PIL import Image, ImageDraw
from h import *
rng = np.random.default_rng(1871_10_08)
im = Image.new("RGB", (W, H), K)
QUAY = 372*S; HZ = 330*S

# --- smoke sky: warped fbm, blown up-and-right
n = fbm(W, H, rng, (200, 100, 50, 24, 12))
yy, xx = np.mgrid[0:H, 0:W]
warp = fbm(W, H, rng, (300, 150))
n2 = np.roll(n, 0, 1)
v = n + 0.35*(warp - 0.5) + 0.0
glow = np.clip((yy - 10*S)/(230*S), 0, 1)**1.3           # brighter near the fire
band = np.sin((xx*0.6 - yy)/ (26*S) + 6*warp)                # diagonal billow banding
t = np.clip(0.9*(v - 0.5) + 0.16*band + 0.75*glow + 0.12, 0, 1)
a = np.zeros((H, W, 3), np.uint8)
a[:] = K
a[screen(np.clip((t - 0.25)*3, 0, 1), 2)] = R
a[t > 0.58] = R
a[screen(np.clip((t - 0.62)*3.5, 0, 1), 2) & (t > 0.58)] = Y
a[t > 0.86] = Y
im = Image.fromarray(a); d = ImageDraw.Draw(im)
# billow outlines: contour of t at a few levels, drawn in black, for the engraved look
for lev in (0.42, 0.58, 0.72):
    edge = (t[:-1, :] < lev) != (t[1:, :] < lev)
    e = np.zeros((H, W), bool); e[:-1] = edge
    a = np.array(im); a[e & (yy < HZ)] = K; im = Image.fromarray(a); d = ImageDraw.Draw(im)

def flame(x, base, h, w):
    for col, sc in [(R, 1.0), (Y, 0.68), (Wh, 0.32)]:
        pts = []; hh = h*sc; ww = w*sc
        for k in range(24):
            u = k/23; y = base - hh*u
            wob = math.sin(u*9 + x*0.01)*ww*0.25
            pts.append((x - ww*(1-u)**0.8 + wob + hh*0.25*u**2, y))
        for k in range(23, -1, -1):
            u = k/23; y = base - hh*u
            wob = math.sin(u*7 + x*0.02 + 1)*ww*0.25
            pts.append((x + ww*(1-u)**0.8 + wob + hh*0.25*u**2, y))
        d.polygon(pts, fill=col)
        if col == R: d.line(pts + [pts[0]], fill=K, width=2)

# --- skyline: back row then front row, flames on most roofs
def building(x, w, h, kind):
    top = QUAY - h
    if kind == "church":
        d.rectangle((x, top, x+w, QUAY), fill=K)
        sx = x + w*0.5; d.rectangle((sx-8*S, top-50*S, sx+8*S, top), fill=K)
        d.polygon([(sx-10*S, top-50*S), (sx, top-110*S), (sx+10*S, top-50*S)], fill=K)
        d.ellipse((sx-5*S, top-36*S, sx+5*S, top-26*S), fill=Y)
        for wx in np.arange(x+8, x+w-10, 16*S): d.rectangle((wx, top+14*S, wx+8*S, top+40*S), fill=R); d.pieslice((wx, top+10*S, wx+8*S, top+18*S), 180, 360, fill=R)
    elif kind == "elevator":
        d.rectangle((x, top, x+w, QUAY), fill=K)
        d.polygon([(x, top), (x+w/2, top-20*S), (x+w, top)], fill=K)
        for k in range(1, 6): d.line((x+k*w/6, top+6*S, x+k*w/6, QUAY), fill=R, width=2)
        d.text((x+6*S, top+20*S), "ELEVATOR", font=serif(8*S, bold=True), fill=Y)
    else:
        d.rectangle((x, top, x+w, QUAY), fill=K)
        d.rectangle((x-3*S, top-6*S, x+w+3*S, top), fill=K)   # cornice
        for wy in np.arange(top+10*S, QUAY-14*S, 16*S):
            for wx in np.arange(x+5*S, x+w-8*S, 11*S):
                r = rng.random()
                if r < 0.55: d.rectangle((wx, wy, wx+6*S, wy+9*S), fill=[Y, R, R, Wh][rng.integers(4)])
    return top
fires = []
x = -10*S
while x < W:
    w = rng.uniform(34, 70)*S; h = rng.uniform(120, 200)*S
    kind = rng.choice(["block", "block", "block", "church", "elevator"])
    top = building(x, w, h*0.85, kind); 
    if rng.random() < 0.8: fires.append((x + w/2, top, rng.uniform(70, 180)*S, w*0.6))
    x += w + rng.uniform(-6, 4)*S
for f in fires: flame(*f)
x = -20*S
while x < W:
    w = rng.uniform(40, 80)*S; h = rng.uniform(60, 120)*S
    top = building(x, w, h, rng.choice(["block", "block", "church"]) if rng.random() < .9 else "block")
    if rng.random() < 0.55: flame(x + w*0.5, top, rng.uniform(40, 110)*S, w*0.55)
    x += w + rng.uniform(4, 30)*S
# sparks and embers blowing right
for i in range(500):
    px, py = rng.uniform(0, W), rng.uniform(0, HZ + 20*S)
    L = rng.uniform(2, 8)*S
    d.line((px, py, px + L, py - L*0.6), fill=Y if rng.random() < .7 else Wh, width=2 if rng.random() < .5 else 3)
# --- the Water Tower, white limestone, castellated — standing in front
wx, wy = 300*S, QUAY + 8*S
def wt():
    base_w, mid_w, top_w = 40*S, 18*S, 12*S
    d.rectangle((wx-base_w/2, wy-64*S, wx+base_w/2, wy), fill=Wh, outline=K, width=3)
    for cx in (wx-base_w/2, wx+base_w/2):   # corner turrets
        d.rectangle((cx-5*S, wy-80*S, cx+5*S, wy), fill=Wh, outline=K, width=3)
        d.polygon([(cx-6*S, wy-80*S), (cx, wy-94*S), (cx+6*S, wy-80*S)], fill=Wh, outline=K)
    d.rectangle((wx-mid_w/2, wy-150*S, wx+mid_w/2, wy-64*S), fill=Wh, outline=K, width=3)
    d.rectangle((wx-top_w/2-3*S, wy-162*S, wx+top_w/2+3*S, wy-150*S), fill=Wh, outline=K, width=3)
    d.polygon([(wx-top_w/2, wy-162*S), (wx, wy-196*S), (wx+top_w/2, wy-162*S)], fill=Wh, outline=K)
    d.line([(wx-top_w/2, wy-162*S), (wx, wy-196*S), (wx+top_w/2, wy-162*S)], fill=K, width=3)
    for yy_ in range(int(wy-148*S), int(wy-66*S), 10*S): d.line((wx-mid_w/2, yy_, wx+mid_w/2, yy_), fill=K, width=1)
    d.rectangle((wx-3*S, wy-130*S, wx+3*S, wy-110*S), fill=K); d.rectangle((wx-3*S, wy-100*S, wx+3*S, wy-80*S), fill=K)
    d.pieslice((wx-9*S, wy-36*S, wx+9*S, wy-18*S), 180, 360, fill=K); d.rectangle((wx-9*S, wy-27*S, wx+9*S, wy), fill=K)
    for cx in np.arange(wx-base_w/2, wx+base_w/2, 6*S): d.rectangle((cx, wy-68*S, cx+3*S, wy-64*S), fill=K)
    # red glow on the fire side
    for k in range(18): yk = wy - rng.uniform(4, 190)*S; d.line((wx-mid_w/2+2, yk, wx-mid_w/2+5*S, yk), fill=R, width=2)
wt()

# --- quay and river
d.rectangle((0, QUAY, W, QUAY + 14*S), fill=K)
for x in range(0, W, 10*S): d.line((x, QUAY+2*S, x, QUAY+14*S), fill=R, width=2)
RIV = QUAY + 14*S
a = np.array(im)
ry = np.arange(RIV, H)
for y in ry:   # reflections: mirror of the sky/fire rows, broken into horizontal dashes
    src = max(0, int(RIV - (y - RIV)*1.3) - 1)
    row = a[src].copy()
    keep = (np.sin(np.arange(W)/(4 + (y-RIV)/40) + rng.uniform(0, 6)) > -0.2) & (rng.random(W) > 0.15)
    out = np.where(keep[:, None], row, np.array(B))
    out[(row == K).all(-1)] = B
    a[y] = out
im = Image.fromarray(a); d = ImageDraw.Draw(im)
for y in range(RIV, H, 6): d.line((0, y, W, y), fill=B, width=2)   # water lines

# schooners: hulls, two masts, rigging, furled sails — black against the reflections
def schooner(x, y, sc, flip=1):
    L = 110*sc*S
    d.polygon([(x - L/2*flip, y - 10*sc*S), (x + L/2*flip, y - 14*sc*S), (x + L*0.42*flip, y + 4*sc*S), (x - L*0.40*flip, y + 4*sc*S)], fill=K)
    d.line((x - L*0.42*flip, y - 4*sc*S, x + L*0.45*flip, y - 7*sc*S), fill=Y, width=2)
    masts = [x - L*0.15*flip, x + L*0.2*flip]
    for m in masts:
        d.line((m, y - 10*sc*S, m, y - 120*sc*S), fill=K, width=int(4*sc)+2)
        for k in range(3): d.line((m - 22*sc*S, y - (40 + k*26)*sc*S, m + 22*sc*S, y - (40 + k*26)*sc*S), fill=K, width=3)
        d.line((m, y - 120*sc*S, x + L/2*flip, y - 14*sc*S), fill=K, width=2)
        d.line((m, y - 120*sc*S, x - L/2*flip, y - 10*sc*S), fill=K, width=2)
    d.line((masts[1], y-110*sc*S, x + L*0.75*flip, y - 18*sc*S), fill=K, width=2)   # bowsprit stay
    d.line((x + L/2*flip, y - 14*sc*S, x + L*0.75*flip, y - 18*sc*S), fill=K, width=4)
schooner(90*S, 470*S, 1.0); schooner(330*S, 560*S, 1.25, -1)
# swing bridge with the crowd crossing toward us (left side)
by = 430*S
d.rectangle((0, by, 170*S, by + 8*S), fill=K)
for x in range(0, 170*S, 12*S): d.line((x, by, x + 12*S, by - 20*S), fill=K, width=3); d.line((x+12*S, by, x, by - 20*S), fill=K, width=3)
d.line((0, by - 20*S, 170*S, by - 20*S), fill=K, width=4)
d.rectangle((150*S, by, 166*S, by + 40*S), fill=K)
for i in range(34):  # people: head, body, sometimes a bundle on the back
    px = rng.uniform(4, 160)*S; ph = rng.uniform(22, 30)*S
    d.ellipse((px-4*S, by-ph-9*S, px+4*S, by-ph-1*S), fill=K)
    d.polygon([(px-5*S, by-ph), (px+5*S, by-ph), (px+7*S, by), (px-7*S, by)], fill=K)
    if rng.random() < 0.4: d.rectangle((px+2*S, by-ph-2*S, px+10*S, by-ph+6*S), fill=[Wh, Y, R][rng.integers(3)], outline=K, width=2)
# date line
f = serif(14*S, bold=True)
txt = "CHICAGO  ·  8 OCTOBER 1871"
w = d.textlength(txt, font=f); d.rectangle(((W-w)/2-8*S, 14*S, (W+w)/2+8*S, 36*S), fill=K)
d.text(((W-w)/2, 16*S), txt, font=f, fill=Y)
save(im)
