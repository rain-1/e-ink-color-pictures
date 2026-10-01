# Night — "Line of Light, 22:00". A night chart of the Tōkaidō corridor turned on its side so
# Tokyo is at the top and Osaka at the bottom (the same orientation as the afternoon diagram).
# Real coastline (Natural Earth 1:10m, clipped to coast_tokaido.json), a blue graticule,
# city lights scattered as yellow and white points, the Shinkansen as one thin white line
# with its twelve 1964 stations, the old road's post towns as small red points, and the
# waning gibbous moon of 1 Oct 2026. Hikari 21 (dep. 20:00) is a short bright streak
# somewhere past Hamamatsu.
import os, sys, math, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ukiyo import *
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(22)
im = Image.new("RGB", (W, H), K); d = ImageDraw.Draw(im); d.fontmode = "1"

SHIN = [("東京", 139.767, 35.681), ("新横浜", 139.617, 35.507), ("小田原", 139.155, 35.256), ("熱海", 139.078, 35.104),
        ("静岡", 138.389, 34.972), ("浜松", 137.735, 34.704), ("豊橋", 137.382, 34.763), ("名古屋", 136.882, 35.171),
        ("岐阜羽島", 136.686, 35.316), ("米原", 136.291, 35.314), ("京都", 135.758, 34.985), ("新大阪", 135.500, 34.733)]
OLD = [(139.774, 35.684), (139.74, 35.62), (139.70, 35.53), (139.63, 35.47), (139.53, 35.40), (139.43, 35.34), (139.32, 35.32),
       (139.155, 35.25), (139.03, 35.19), (138.91, 35.12), (138.86, 35.10), (138.74, 35.15), (138.60, 35.12), (138.54, 35.10),
       (138.51, 35.05), (138.45, 35.01), (138.38, 34.97), (138.33, 34.94), (138.28, 34.92), (138.23, 34.88), (138.18, 34.84),
       (138.13, 34.82), (138.06, 34.80), (138.01, 34.77), (137.92, 34.73), (137.85, 34.70), (137.73, 34.71), (137.61, 34.69),
       (137.56, 34.69), (137.47, 34.71), (137.43, 34.72), (137.39, 34.77), (137.32, 34.85), (137.24, 34.91), (137.16, 34.95),
       (137.05, 35.00), (136.95, 35.08), (136.90, 35.12), (136.69, 35.07), (136.62, 34.97), (136.55, 34.91), (136.53, 34.88),
       (136.45, 34.86), (136.39, 34.85), (136.33, 34.89), (136.28, 34.93), (136.17, 34.97), (136.05, 35.01), (135.96, 35.02),
       (135.86, 35.00), (135.77, 35.009)]
CITIES = [(139.70, 35.68, 900), (139.64, 35.45, 380), (139.45, 35.55, 160), (139.36, 35.33, 60), (139.155, 35.256, 40),
          (138.389, 34.972, 120), (138.86, 35.10, 60), (138.62, 35.15, 50), (137.735, 34.704, 130), (137.382, 34.763, 70),
          (137.16, 34.95, 60), (136.90, 35.17, 420), (136.76, 35.42, 80), (136.62, 34.97, 60), (135.86, 35.00, 50),
          (135.758, 35.01, 260), (135.50, 34.69, 600), (135.19, 34.69, 230), (136.50, 34.73, 40), (136.29, 35.31, 25), (135.62, 34.50, 90)]

# projection: equirectangular km, rotated so Tokyo→Shin-Osaka points straight down
c35 = math.cos(math.radians(35))
def km(lon, lat): return np.array([lon * c35 * 111.0, lat * 111.0])
A = km(*SHIN[0][1:]); Bp = km(*SHIN[-1][1:])
v = Bp - A; ang = math.atan2(v[0], -v[1])   # angle of route from "down"
ca, sa = math.cos(ang), math.sin(ang)
def rot(p):
    q = p - A
    return np.array([q[0] * ca + q[1] * sa, -(q[0] * -sa + q[1] * ca)])
L = np.linalg.norm(v)
S = 450 / L
OX, OY = 168, 96
def P(lon, lat):
    r = rot(km(lon, lat)); return (OX + r[0] * S, OY + r[1] * S)
# sanity: Tokyo at (OX,OY), Osaka straight below
# --- sea: sparse blue ripple dashes across the whole sheet; land is masked black afterwards
for y in range(0, H, 6):
    x = rng.uniform(-10, 0)
    while x < W:
        Ld = rng.uniform(3, 9)
        if rng.random() < 0.55: d.line((x, y, x + Ld, y), fill=B)
        x += Ld + rng.uniform(6, 16)
# --- graticule: every half degree, dotted blue
for lon in np.arange(134.5, 141.01, 0.5):
    pts = [P(lon, lat) for lat in np.linspace(32.5, 37.5, 120)]
    for i, p in enumerate(pts):
        if i % 2 == 0: d.point(p, fill=B)
for lat in np.arange(33.0, 37.01, 0.5):
    pts = [P(lon, lat) for lon in np.linspace(133.5, 141.5, 200)]
    for i, p in enumerate(pts):
        if i % 2 == 0: d.point(p, fill=B)
# --- coast: blue line, land filled black by flood from inland seeds
coast = json.load(open(os.path.join(HERE, "coast_tokaido.json")))
mask = Image.new("L", (W, H), 0); md = ImageDraw.Draw(mask)
segs = []
for line in coast:
    seg = [line[0]]
    for a, b in zip(line, line[1:]):
        if abs(a[0] - b[0]) + abs(a[1] - b[1]) > 0.3:
            segs.append(seg); seg = []
        seg.append(b)
    segs.append(seg)
for seg in segs:
    if len(seg) > 1:
        md.line([P(*p) for p in seg], fill=255, width=1)
from PIL import ImageDraw as _D
land = mask.copy()
for lon, lat in ((138.0, 35.4), (136.9, 35.4), (139.4, 35.6), (136.2, 34.95), (139.0, 35.3)):
    x, y = P(lon, lat)
    if 0 <= x < W and 0 <= y < H and land.getpixel((int(x), int(y))) == 0:
        _D.floodfill(land, (int(x), int(y)), 128)
la = np.array(land) == 128
a = np.array(im); a[la] = K; im = Image.fromarray(a); d = ImageDraw.Draw(im); d.fontmode = "1"
for seg in segs:
    if len(seg) > 1:
        d.line([P(*p) for p in seg], fill=B, width=2)
        d.line([P(*p) for p in seg], fill=Wh if False else B, width=1)
# --- lights: each city a gaussian swarm of points; a faint dust along the corridor
for lon, lat, pop in CITIES:
    cx, cy = P(lon, lat)
    n = int(pop * 1.1); sd = 2 + math.sqrt(pop) * 0.55
    xs = rng.normal(cx, sd, n); ys = rng.normal(cy, sd, n)
    for x, y in zip(xs, ys):
        if 0 <= x < W and 0 <= y < H and la[int(y), int(x)]:
            r2 = ((x - cx) ** 2 + (y - cy) ** 2) / sd ** 2
            if r2 < 0.3: d.point((x, y), fill=Wh)
            elif r2 < 2.5: d.point((x, y), fill=Y)
            elif rng.random() < 0.25: d.point((x, y), fill=R)
for i in range(1, len(SHIN)):
    (x0, y0), (x1, y1) = P(*SHIN[i - 1][1:]), P(*SHIN[i][1:])
    for k in range(40):
        t = rng.random(); x = x0 + (x1 - x0) * t + rng.normal(0, 7); y = y0 + (y1 - y0) * t + rng.normal(0, 7)
        if 0 <= x < W and 0 <= y < H and la[int(y), int(x)]:
            d.point((x, y), fill=Y)
# --- the old road: red dotted path through the post towns
op = [P(*p) for p in OLD]
for (x0, y0), (x1, y1) in zip(op, op[1:]):
    n = max(1, int(math.hypot(x1 - x0, y1 - y0) / 3))
    for k in range(n):
        if k % 2 == 0: d.point((x0 + (x1 - x0) * k / n, y0 + (y1 - y0) * k / n), fill=R)
for x, y in op:
    d.rectangle((x - 1, y - 1, x + 1, y + 1), fill=R)
# --- the Shinkansen: white line, station ticks and names
sp = [P(*s[1:]) for s in SHIN]
d.line(sp, fill=Wh, width=1)
f = font(10, jp=True)
for (name, lon, lat), (x, y) in zip(SHIN, sp):
    d.ellipse((x - 3, y - 3, x + 3, y + 3), fill=K, outline=Wh)
    side = 1 if name not in ("岐阜羽島", "新横浜", "熱海") else -1
    tx = x + 8 if side > 0 else x - 8 - f.getlength(name)
    d.text((tx, y - 6), name, font=f, fill=Wh, stroke_width=2, stroke_fill=K)
# Hikari 21 at 22:00: two hours out of Tokyo → between Hamamatsu and Toyohashi, a bright dash
(hx0, hy0), (hx1, hy1) = sp[5], sp[6]
mx, my = hx0 + (hx1 - hx0) * 0.55, hy0 + (hy1 - hy0) * 0.55
ux, uy = (hx1 - hx0), (hy1 - hy0); n = math.hypot(ux, uy); ux, uy = ux / n, uy / n
d.line((mx - ux * 14, my - uy * 14, mx, my), fill=Y, width=3)
d.line((mx - ux * 26, my - uy * 26, mx - ux * 14, my - uy * 14), fill=Y, width=1)
d.ellipse((mx - 2, my - 2, mx + 2, my + 2), fill=Wh)
# --- moon: waning gibbous, ~78% lit, low in the east (top right of this rotated sheet)
MX, MY, MR = 340, 62, 30
moon = Image.new("L", (W, H), 0); mdd = ImageDraw.Draw(moon)
mdd.ellipse((MX - MR, MY - MR, MX + MR, MY + MR), fill=255)
mdd.ellipse((MX - MR - 0.56 * 2 * MR * 0.8, MY - MR, MX + MR - 0.56 * 2 * MR * 0.8 - 6, MY + MR), fill=0)
mm = np.array(moon) > 0
a = np.array(im); a[mm] = Wh; im = Image.fromarray(a); d = ImageDraw.Draw(im); d.fontmode = "1"
d.ellipse((MX - MR, MY - MR, MX + MR, MY + MR), outline=B)
for cx, cy, r in ((MX + 8, MY - 10, 6), (MX + 16, MY + 6, 4), (MX + 2, MY + 14, 7), (MX + 20, MY - 2, 3), (MX - 2, MY - 2, 3)):
    for yy_ in range(int(cy - r), int(cy + r) + 1):
        for xx_ in range(int(cx - r), int(cx + r) + 1):
            if (xx_ - cx) ** 2 + (yy_ - cy) ** 2 <= r * r and mm[yy_, xx_] and (xx_ + 2 * yy_) % 4 == 0:
                d.point((xx_, yy_), fill=Y)
# --- compass: north arrow, rotated with the map
nx, ny = 40, 60
p0 = rot(km(137, 35)); p1 = rot(km(137, 35.3)); dv = (p1 - p0) / np.linalg.norm(p1 - p0)
dv = np.array([dv[0], dv[1]])
d.line((nx - dv[0] * 18, ny - dv[1] * 18, nx + dv[0] * 18, ny + dv[1] * 18), fill=Wh)
tip = (nx + dv[0] * 20, ny + dv[1] * 20); pr = np.array([-dv[1], dv[0]])
d.polygon([tip, (nx + dv[0] * 8 + pr[0] * 5, ny + dv[1] * 8 + pr[1] * 5), (nx + dv[0] * 8 - pr[0] * 5, ny + dv[1] * 8 - pr[1] * 5)], fill=R)
d.text((tip[0] + dv[0] * 6 - 4, tip[1] + dv[1] * 6 - 6), "N", font=font(10, serif=False, bold=True), fill=Wh)
# --- scale bar and title
d.line((20, 560, 20 + 100 * S, 560), fill=Wh); d.line((20, 556, 20, 564), fill=Wh); d.line((20 + 100 * S, 556, 20 + 100 * S, 564), fill=Wh)
d.text((24 + 100 * S, 554), "100 km", font=font(9, serif=False), fill=Wh)
d.text((20, 572), "22:00 · 東海道 · 1964 / 1833", font=font(11, jp=True), fill=Y)
d.text((240, 556), "— 新幹線", font=font(9, jp=True), fill=Wh)
d.text((240, 568), "·· 旧東海道", font=font(9, jp=True), fill=R)
im.save(os.environ.get("OUT_RAW", "/tmp/5.png"))
