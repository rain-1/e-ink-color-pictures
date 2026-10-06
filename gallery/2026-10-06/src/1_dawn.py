"""Morning: Kon-Tiki at first light. Painted in smooth RGB at 2x, then Floyd-Steinberg onto six colours."""
import os, math, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.dirname(__file__))
from lib import noise

S = 2; Wd, Hd = 400 * S, 600 * S
yy, xx = np.mgrid[0:Hd, 0:Wd].astype(np.float32)
HZ = 262 * S                     # horizon
SUN = (318 * S, 252 * S)

def lerp(a, b, t):
    t = np.clip(t, 0, 1)[..., None]
    return np.array(a, np.float32) * (1 - t) + np.array(b, np.float32) * t

# --- sky: deep blue -> cornflower -> pale gold -> red at the horizon line
t = yy / HZ
sky = lerp((14, 40, 120), (70, 95, 170), t / 0.45)
sky = np.where((t > 0.45)[..., None], lerp((70, 95, 170), (250, 225, 150), (t - 0.45) / 0.35), sky)
sky = np.where((t > 0.80)[..., None], lerp((250, 225, 150), (240, 120, 50), (t - 0.80) / 0.20), sky)
d = np.hypot(xx - SUN[0], (yy - SUN[1]) * 1.5)
glow = np.exp(-d / (95 * S))
sky = sky * (1 - glow[..., None] * 0.7) + np.array([255, 230, 90]) * glow[..., None] * 0.7

# streaky clouds, lit from below
n = noise(3, 60, 5, Hd, Wd)
n2 = noise(9, 18, 3, Hd, Wd)
band = np.exp(-((yy - 150 * S) / (55 * S)) ** 2) + 0.8 * np.exp(-((yy - 225 * S) / (14 * S)) ** 2)
streak = noise(5, 200, 3, Hd // 12, Wd)
streak = np.asarray(Image.fromarray((streak * 255).astype(np.uint8)).resize((Wd, Hd), Image.BICUBIC), np.float32) / 255
cl = np.clip((streak * 0.75 + n2 * 0.35 - 0.62) * 6, 0, 1) * band
under = np.clip((yy - 120 * S) / (130 * S), 0, 1)
cloud_col = lerp((60, 50, 110), (235, 70, 50), under * 0.9 + glow * 0.6)
rim = np.clip(cl * 3 - 2.0, 0, 1) * (glow * 2.5)
sky = sky * (1 - cl[..., None]) + cloud_col * cl[..., None]
sky = sky + np.array([255, 220, 60]) * np.clip(rim, 0, 1)[..., None] * 0.6

img = sky.copy()

# --- sea
s = (yy - HZ) / (Hd - HZ)
sea = lerp((40, 70, 150), (8, 30, 95), np.clip(s, 0, 1) ** 0.6)
# waves: many octaves of directional ripples, compressed toward horizon
depth = 1 / (s + 0.04)
u = xx / S
ph = (depth * 9.0) + np.sin(u * 0.05 + depth * 0.7) * 1.4 + n * 3
w = np.sin(ph) * 0.5 + 0.5
w2 = np.sin(depth * 23 + u * 0.13 * (1 + s * 0.5) + n2 * 6) * 0.5 + 0.5
wave = (w * 0.65 + w2 * 0.35)
sea = sea * (0.75 + 0.45 * wave[..., None])
# sun path: glitter, wider near viewer
path = np.exp(-((xx - SUN[0] - (yy - HZ) * 0.05) / (S * (10 + 70 * s))) ** 2)
glit = (wave > 0.72 - 0.15 * path) * path
sea = sea * (1 - glit[..., None] * 0.9) + np.array([255, 235, 120]) * glit[..., None] * 0.95
whitecap = (w2 > 0.93) & (w > 0.7) & (s > 0.25)
sea[whitecap] = sea[whitecap] * 0.3 + 255 * 0.7
img[yy >= HZ] = sea[yy >= HZ]

# sun disc, half risen behind haze
sd = np.hypot(xx - SUN[0], yy - SUN[1])
disc = (sd < 26 * S) & (yy < HZ)
img[disc] = (255, 236, 110)
# thin haze bars across the sun
for k, (y0, th) in enumerate([(238, 2.5), (246, 2), (253, 3)]):
    m = disc & (np.abs(yy - y0 * S) < th * S)
    img[m] = (240, 120, 60)

im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
dr = ImageDraw.Draw(im)
def P(*pts): return [(x * S, y * S) for x, y in pts]

# --- the raft (seen slightly from the stern-quarter, sun behind it)
DARK = (25, 22, 30); LOG = (45, 32, 22); LOGL = (240, 200, 60); BAMB = (245, 210, 70)
cx, wl = 238, 432   # centre, waterline
# hull: nine balsa logs, centre ones longest; seen end-on-ish with perspective
logs = []
for i in range(9):
    off = i - 4
    x0 = cx - 118 + i * 0 + (abs(off) * 6)
    x1 = cx + 112 - abs(off) * 7
    y = wl - 2 + i * 3.2 - 12
    logs.append((x0, x1, y))
for i, (x0, x1, y) in enumerate(logs):
    r = 6.5
    dr.rounded_rectangle([x0 * S, (y - r) * S, x1 * S, (y + r) * S], radius=r * S, fill=LOG, outline=DARK, width=S)
    dr.line(P((x0 + 8, y - 2.5), (x1 - 8, y - 2.5)), fill=LOGL, width=S)
    # ropes lashing
    for xr in range(int(x0) + 20, int(x1) - 10, 34):
        dr.line(P((xr, y - r), (xr + 3, y + r)), fill=(230, 210, 160), width=S)
    # bow end (pointed / rounded front at left)
    dr.ellipse([(x0 - 4) * S, (y - r) * S, (x0 + 9) * S, (y + r) * S], fill=(245, 205, 60), outline=DARK, width=S)
    dr.ellipse([(x0 - 1) * S, (y - 3) * S, (x0 + 5) * S, (y + 3) * S], outline=(90, 55, 30), width=S)
# deck of split bamboo
deck_y = logs[0][2] - 9
dr.polygon(P((cx - 104, deck_y), (cx + 100, deck_y), (cx + 104, deck_y + 7), (cx - 108, deck_y + 7)), fill=BAMB, outline=DARK)
for x in range(cx - 104, cx + 100, 5):
    dr.line(P((x, deck_y), (x - 3, deck_y + 7)), fill=(60, 40, 20), width=1)

# cabin: bamboo walls, banana-leaf thatch
c0, c1, ct = cx + 8, cx + 74, deck_y - 34
dr.rectangle([c0 * S, ct * S, c1 * S, deck_y * S], fill=(240, 200, 60), outline=DARK, width=S)
for x in range(c0 + 3, c1, 4):
    dr.line(P((x, ct + 2), (x, deck_y)), fill=(60, 40, 20), width=S)
dr.rectangle([(c0 + 22) * S, (ct + 12) * S, (c0 + 36) * S, deck_y * S], fill=DARK)   # doorway
dr.polygon(P((c0 - 8, ct + 3), (c1 + 8, ct + 3), (c1 - 4, ct - 18), (c0 + 4, ct - 18)), fill=(30, 150, 60), outline=DARK)
for k in range(26):
    x = c0 - 6 + k * 3.2
    dr.line(P((x, ct + 4), (x + 5, ct - 17)), fill=(10, 60, 25), width=S)
    dr.line(P((x + 1, ct + 3), (x + 1, ct + 7)), fill=(10, 60, 25), width=S)

# steering oar off the stern (right)
dr.line(P((cx + 92, deck_y - 30), (cx + 150, wl + 34)), fill=DARK, width=4 * S)
dr.polygon(P((cx + 140, wl + 16), (cx + 160, wl + 22), (cx + 154, wl + 48), (cx + 140, wl + 44)), fill=LOG, outline=DARK)

# A-frame mast of mangrove wood
top = (cx - 36, 150)
dr.line(P((cx - 64, deck_y + 2), top), fill=DARK, width=5 * S)
dr.line(P((cx + 2, deck_y + 2), top), fill=DARK, width=5 * S)
dr.line(P((cx - 52, deck_y - 30), (cx - 8, deck_y - 30)), fill=DARK, width=2 * S)
# stays
for p in [(cx - 110, deck_y), (cx + 100, deck_y - 2), (cx + 74, ct - 18)]:
    dr.line(P(top, p), fill=(40, 30, 30), width=S)

# yard + sail (backlit: warm, translucent)
yard = 172
sl, sr = cx - 100, cx + 28
dr.line(P((sl - 8, yard), (sr + 8, yard - 6)), fill=DARK, width=4 * S)
sail_poly = P((sl, yard + 2), (sr, yard - 4), (sr + 6, deck_y - 46), (sl - 4, deck_y - 40))
mask = Image.new("L", im.size, 0); ImageDraw.Draw(mask).polygon(sail_poly, fill=255)
m = np.asarray(mask) > 0
a = np.asarray(im).astype(np.float32)
sy = (yy - yard * S) / ((deck_y - 44 - yard) * S)
sx = (xx - sl * S) / ((sr - sl) * S)
billow = np.sin(np.clip(sx, 0, 1) * math.pi) * 0.2
sail = lerp((250, 225, 160), (230, 160, 90), np.clip(sy * 0.8 + billow + (1 - glow) * 0.4, 0, 1))
canvas = (np.sin(yy / S * 1.4) > 0.85) * 0.06
sail = sail * (1 - canvas[..., None])
a[m] = sail[m]
im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)); dr = ImageDraw.Draw(im)
dr.polygon(sail_poly, outline=DARK, width=S)
# sail seams
for k in range(1, 6):
    f = k / 6
    dr.line(P((sl + (sr - sl) * f, yard - 4 * f + 2), (sl - 4 + (sr + 10 - sl) * f, deck_y - 40 - 6 * f)), fill=(200, 140, 80), width=S)

# --- Kon-Tiki's face, painted on the sail in red
RED = (210, 25, 30)
fx, fy = (sl + sr) / 2 + 2, (yard + deck_y - 44) / 2 + 4
F = 0.72
for k in range(22):                               # crown of rays
    ang = math.pi + k * math.pi / 21
    r0, r1 = 34 * F, (52 + (k % 2) * 7) * F
    dr.line(P((fx + r0 * math.cos(ang), fy - 6 * F + r0 * math.sin(ang)), (fx + r1 * math.cos(ang), fy - 6 * F + r1 * math.sin(ang))), fill=RED, width=3 * S)
dr.ellipse(P((fx - 32 * F, fy - 38 * F), (fx + 32 * F, fy + 26 * F)), outline=RED, width=3 * S)
dr.line(P((fx - 32 * F, fy - 12 * F), (fx + 32 * F, fy - 12 * F)), fill=RED, width=2 * S)    # band
for ex in (-13, 13):
    dr.ellipse(P((fx + (ex - 8) * F, fy - 6 * F), (fx + (ex + 8) * F, fy + 3 * F)), outline=RED, width=2 * S)
    dr.ellipse(P((fx + (ex - 3) * F, fy - 4 * F), (fx + (ex + 3) * F, fy + 2 * F)), fill=RED)
    dr.arc(P((fx + (ex - 10) * F, fy - 14 * F), (fx + (ex + 10) * F, fy - 2 * F)), 200, 340, fill=RED, width=2 * S)
dr.line(P((fx, fy - 2 * F), (fx - 4 * F, fy + 12 * F), (fx + 4 * F, fy + 12 * F)), fill=RED, width=2 * S)
dr.arc(P((fx - 12 * F, fy + 10 * F), (fx + 12 * F, fy + 22 * F)), 10, 170, fill=RED, width=2 * S)
for k in range(-4, 5):                              # beard
    dr.line(P((fx + k * 5 * F, fy + 22 * F), (fx + k * 7 * F, fy + (46 - abs(k) * 3) * F)), fill=RED, width=2 * S)

# crew: two tiny figures, one at the oar, one on deck
def figure(x, y, h=18, lean=0):
    dr.ellipse(P((x - 3, y - h), (x + 3, y - h + 6)), fill=DARK)
    dr.line(P((x, y - h + 5), (x + lean, y - 6)), fill=DARK, width=3 * S)
    dr.line(P((x + lean, y - 6), (x - 3, y)), fill=DARK, width=2 * S)
    dr.line(P((x + lean, y - 6), (x + 4, y)), fill=DARK, width=2 * S)
    return (x, y - h + 9)
sh = figure(cx + 88, deck_y, 20, 2)
dr.line(P(sh, (cx + 100, deck_y - 24)), fill=DARK, width=2 * S)
sh = figure(cx - 84, deck_y, 18, -1)
dr.line(P(sh, (cx - 92, deck_y - 18)), fill=DARK, width=2 * S)

# water around the raft: foam and reflection
for k in range(40):
    x = cx - 125 + k * 6.3
    yb = wl + 18 + math.sin(k * 1.7) * 2
    dr.arc(P((x - 6, yb - 3), (x + 6, yb + 3)), 0, 180, fill=(235, 240, 245), width=S)
for k in range(10):   # the raft's shadow on the water, toward the viewer
    y = wl + 26 + k * 5
    xl = cx - 100 + k * 4 + math.sin(k) * 6
    dr.line(P((xl, y), (xl + 150 - k * 12, y)), fill=(10, 25, 80), width=S * 3)

# flying fish, foreground, leaping out of a crest
def flyfish(x, y, sc, ang):
    ca, sa = math.cos(ang), math.sin(ang)
    def T(px, py): return ((x + (px * ca - py * sa) * sc) * S, (y + (px * sa + py * ca) * sc) * S)
    dr.polygon([T(-14, 0), T(-4, -3), T(12, -1), T(16, 0), T(12, 2), T(-4, 3)], fill=(18, 61, 176), outline=DARK)
    dr.polygon([T(-14, 0), T(-22, -5), T(-19, 0), T(-24, 5)], fill=(18, 61, 176))
    dr.polygon([T(2, -1), T(-12, -14), T(-2, -16), T(8, -2)], fill=(255, 255, 255), outline=DARK)
    dr.polygon([T(2, 1), T(-10, 12), T(-1, 13), T(8, 2)], fill=(255, 255, 255), outline=DARK)
    dr.ellipse([T(11, -1)[0] - S, T(11, -1)[1] - S, T(11, -1)[0] + S, T(11, -1)[1] + S], fill=(255, 255, 255))
flyfish(96, 500, 2.4, -0.18)
flyfish(70, 556, 1.6, -0.10)
for k in range(12):   # spray trail
    dr.ellipse(P((40 + k * 4, 520 + math.sin(k) * 3), (42 + k * 4, 522 + math.sin(k) * 3)), fill=(240, 245, 250))

# distant birds: two boobies
for (bx, by, b) in [(110, 178, 9), (134, 192, 7), (90, 200, 6)]:
    dr.line(P((bx - b, by - 3), (bx, by), (bx + b, by - 4)), fill=DARK, width=2 * S)

im = im.resize((400, 600), Image.LANCZOS)
im.save(os.environ.get("OUT_RAW", "dawn.png"))
