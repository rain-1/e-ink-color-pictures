# Evening — "Shōno, Driving Rain, 18:00". After Hiroshige's Shōno: Hakuu (1833): travellers and
# palanquin bearers running down a slope as a squall hits, bamboo groves bowed into grey
# silhouettes, rain cut across the whole block. Behind the bamboo, through the murk, a
# 1964 Kodama on its viaduct, windows lit yellow — the two Tōkaidōs in one frame.
# Mostly black/white screen tones; yellow for hats, straw and windows; one red cartouche.
import os, sys, math, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ukiyo import *
from PIL import Image, ImageDraw
rng = np.random.default_rng(1964)
yy, xx = np.mgrid[0:H, 0:W].astype(float)
im = Image.new("RGB", (W, H), Wh)

# --- sky: pale with a heavier band of cloud at the top (screened lightly — mid-greys speckle)
sky = np.clip(0.06 + 0.42 * np.clip(1 - yy / 200, 0, 1) ** 1.6, 0, 1)
im = blend(im, sky, Wh, K, mask=yy < 460)

def grove(base, height, density, lean, seed, x0=-30, x1=W + 30):
    """Mask of a bamboo grove silhouette: culms + feathery leaf sprays streaming leeward."""
    r = np.random.default_rng(seed)
    m = Image.new("L", (W, H), 0); g = ImageDraw.Draw(m)
    for i in range(density):
        x = r.uniform(x0, x1); h = height * r.uniform(0.6, 1.15)
        y0 = base(x)
        pts = [(x + lean * h * (k / 11) ** 2, y0 - h * k / 11) for k in range(12)]
        g.line(pts, fill=255, width=int(r.integers(2, 4)))
        for k in range(int(r.integers(10, 18))):
            t = r.uniform(0.4, 1.0)
            px, py = x + lean * h * t ** 2, y0 - h * t
            L = r.uniform(12, 34)
            for b in range(6):
                a = r.normal(0.35, 0.35)
                g.polygon([(px, py), (px + L * math.cos(a), py + L * math.sin(a) - 3), (px + L * 0.8 * math.cos(a), py + L * 0.8 * math.sin(a) + 2)], fill=255)
    g.polygon([(x, base(x)) for x in range(-5, W + 6, 5)] + [(W, base(W) + 40), (0, base(0) + 40)], fill=255)
    return np.array(m) > 0

RD = lambda x: 560 - 0.32 * x          # road centre, climbing to the right
FAR = lambda x: 360 - 0.12 * x
far = grove(FAR, 150, 30, 0.5, 1)
a = np.array(im); a[far] = B; im = Image.fromarray(a)
d = ImageDraw.Draw(im); d.fontmode = "1"
# far hill under the far grove: blue to the viaduct line
d.polygon([(x, FAR(x)) for x in range(0, W + 1, 5)] + [(W, 470), (0, 470)], fill=B)
# --- the viaduct and the lit Kodama, in front of the far grove
VY = lambda x: 382 - 0.16 * x
d.polygon([(x, VY(x)) for x in range(0, W + 1, 4)] + [(x, VY(x) + 7) for x in range(W, -1, -4)], fill=K)
for x in range(6, W, 24):
    d.rectangle((x, VY(x) + 7, x + 4, VY(x) + 60), fill=K)
TX0, TX1 = 20, 300
d.polygon([(x, VY(x) - 13) for x in range(TX0, TX1 + 1, 4)] + [(TX1 + 16, VY(TX1) - 3)] + [(x, VY(x)) for x in range(TX1, TX0 - 1, -4)], fill=K)
for x in range(TX0 + 4, TX1 - 4, 6):
    d.rectangle((x, VY(x) - 10, x + 3, VY(x) - 6), fill=Y)
d.ellipse((TX1 + 10, VY(TX1) - 7, TX1 + 15, VY(TX1) - 2), fill=Y)
for k in range(9):  # headlight beam fanning into the rain
    d.line((TX1 + 15, VY(TX1) - 5, TX1 + 90, VY(TX1) - 5 - 18 + k * 4.5), fill=Y)
# --- near bank above the road: black bamboo, bowed hard to the right
mid = grove(lambda x: RD(x) - 24, 250, 16, 0.65, 2, x0=-40, x1=250)
a = np.array(im); a[mid & (yy < RD(xx) - 20)] = K; im = Image.fromarray(a)

# --- the road ribbon and the earth bank below it
road = (yy > RD(xx) - 22) & (yy < RD(xx) + 12)
earth = yy >= RD(xx) + 12
a = np.array(im); a[road] = Wh; a[earth] = Y; im = Image.fromarray(a)
d = ImageDraw.Draw(im); d.fontmode = "1"
d.line([(x, RD(x) - 22) for x in range(0, W + 1, 4)], fill=K, width=2)
d.line([(x, RD(x) + 12) for x in range(0, W + 1, 4)], fill=K, width=3)
for k in range(300):  # earth hatching, slanting with the slope
    x = rng.uniform(0, W); y = rng.uniform(RD(x) + 16, H)
    d.line((x, y, x + 8, y - 3), fill=K)
for px in (60, 196, 352):  # puddles holding the train's windows
    d.ellipse((px - 20, RD(px) - 7, px + 20, RD(px) + 3), fill=B, outline=K)
    for k in range(4): d.line((px - 13 + k * 7, RD(px) - 3, px - 9 + k * 7, RD(px) - 3), fill=Y)

# --- figures. kago (palanquin) carried at a run down to the left by two bearers
def kago(x, y, s):
    for bx, st in ((x - 30 * s, 1), (x + 30 * s, -1)):
        traveller(d, bx, y, 52 * s, robe=B, hat=Y, facing=-1, stride=0.9 * st)
    by = y - 33 * s
    d.line((x - 44 * s, by, x + 44 * s, by - 2 * s), fill=K, width=max(2, int(2 * s)))
    d.polygon([(x - 18 * s, by), (x + 18 * s, by), (x + 15 * s, by + 22 * s), (x - 15 * s, by + 22 * s)], fill=Y, outline=K)
    for k in range(-15, 16, 3): d.line((x + k * s, by + 1, x + k * s * 0.85, by + 21 * s), fill=K)
    d.polygon([(x - 22 * s, by - 2 * s), (x + 22 * s, by - 4 * s), (x + 18 * s, by + 4 * s), (x - 18 * s, by + 5 * s)], fill=K)  # straw cover
    for k in range(-20, 21, 3): d.line((x + k * s, by - 3 * s, x + k * s - 2, by + 4 * s), fill=Y)
kago(100, RD(100) + 8, 1.6)
# a man running uphill under an umbrella, bent into the wind; umbrella has a red name on it
ux, uy = 318, RD(318) + 6
traveller(d, ux, uy, 62, robe=B, hat=None, facing=1, stride=1.0)
cx, cy = ux - 12, uy - 64
d.line((ux + 2, uy - 36, cx, cy), fill=K, width=2)
d.pieslice((cx - 36, cy - 26, cx + 36, cy + 26), 185, 335, fill=Y, outline=K, width=2)
for k in range(7):
    a = math.radians(185 + k * 25)
    d.line((cx, cy, cx + 36 * math.cos(a), cy + 26 * math.sin(a)), fill=K)
d.text((cx - 22, cy - 22), "竹", font=font(12, jp=True), fill=R)
# a traveller in a straw mino cape and kasa, hunched, climbing behind
mx, my = 240, RD(240) + 2
traveller(d, mx, my, 50, robe=K, hat=Y, facing=1, stride=0.6, staff=True)
d.polygon([(mx - 8, my - 33), (mx + 7, my - 33), (mx + 13, my - 12), (mx - 13, my - 12)], fill=Y, outline=K)
for k in range(-12, 13, 2): d.line((mx + k * 0.4, my - 31, mx + k, my - 13), fill=K)

# --- rain: long thin strokes everywhere, black over light, white over dark
rain = Image.new("L", (W, H), 0); rd = ImageDraw.Draw(rain)
ang = math.radians(74)
for i in range(900):
    x, y = rng.uniform(-200, W), rng.uniform(-50, H)
    L = rng.uniform(18, 70)
    rd.line((x, y, x + L * math.cos(ang), y + L * math.sin(ang)), fill=255)
r = np.array(rain) > 0
a = np.array(im).astype(int)
lum = a.sum(2)
dark = lum < 300
out = a.copy()
out[r & ~dark] = K
out[r & dark] = Wh
im = Image.fromarray(out.astype(np.uint8)); d = ImageDraw.Draw(im); d.fontmode = "1"
# splashes on the road
for i in range(160):
    x = rng.uniform(0, W); y = RD(x) + rng.uniform(-20, 8)
    d.line((x - 2, y, x, y - 3, x + 2, y), fill=K)

# --- cartouches
cartouche(d, 360, 18, "庄野", font(15, jp=True), R, Wh)
cartouche(d, 336, 18, "白雨", font(12, jp=True), Wh, K, pad=3)
d.rectangle((0, 586, W, H), fill=K)
d.text((8, 587), "TŌKAIDŌ 46/53 · SHŌNO · DRIVING RAIN · KODAMA 18:00", font=font(9, serif=False), fill=Wh)
im.save(os.environ.get("OUT_RAW", "/tmp/4.png"))
