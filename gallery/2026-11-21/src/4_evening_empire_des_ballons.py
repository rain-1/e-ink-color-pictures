"""Evening — 'L'empire des ballons'. After Magritte's paradox: broad daylight above, night in
the street below. The noon sky is raining balloons in a patient lattice; the house has two
lamps lit. Painted-poster style; blue in charge."""
import sys, math, os
sys.path.insert(0, os.path.dirname(__file__))
from common import *

rng = np.random.default_rng(18)
img, d = new(B)
yy, xx = np.mgrid[0:H * S, 0:W * S].astype(np.float32) / S
t = np.clip(yy / 380 + (fbm((H * S, W * S), 40, 3, 9) - .5) * .16, 0, 1) ** 1.3
paint(img, lerp_rgb([(0, mix(B, K, .12)), (.35, B), (1, mix(B, WH, .62))], t))

# far balloons — a half-drop lattice, like the men of Golconda
for r_ in range(8):
    for c_ in range(9):
        x = -10 + c_ * 52 + (26 if r_ % 2 else 0); y = 8 + r_ * 46
        balloon(img, x, y, 24, rot=.5, simple=True, figures=False, outline=False, tint=(mix(B, WH, .5), .28))
for (cx, cy, w, sd) in [(60, 96, 90, 3), (300, 60, 70, 5), (350, 190, 100, 8), (120, 250, 120, 13), (250, 300, 90, 21), (30, 320, 70, 2)]:
    cumulus(img, cx, cy, w, seed=sd, shade=mix(B, WH, .4))
# middle distance
for r_ in range(4):
    for c_ in range(4):
        x = 18 + c_ * 122 + (61 if r_ % 2 else 0); y = 22 + r_ * 98
        if abs(x - 128) < 80 and abs(y + 28 - 103) < 105: continue
        if abs(x - 318) < 66 and abs(y + 28 - 167) < 90: continue
        balloon(img, x, y, 56, rot=.9, simple=True, figures=False)
for (cx, cy, w, sd) in [(215, 172, 80, 31), (55, 205, 60, 17), (330, 290, 80, 44)]:
    cumulus(img, cx, cy, w, seed=sd, shade=mix(B, WH, .4))
# near
balloon(img, 128, 28, 150, rot=.42, simple=False)
balloon(img, 318, 108, 118, rot=1.3, simple=False)
d = ImageDraw.Draw(img); d.fontmode = "1"

# ---------------------------------------------------------------- the night below
night = Image.new("L", img.size, 0); nd = ImageDraw.Draw(night)
GY = 506
def foliage(cx, cy, rx, ry, n, seed):
    r2 = np.random.default_rng(seed)
    for i in range(n):
        an = r2.random() * math.tau; rr = math.sqrt(r2.random())
        x = cx + rx * rr * math.cos(an); y = cy + ry * rr * math.sin(an)
        r = 5 + 9 * r2.random()
        nd.ellipse(P(x - r, y - r, x + r, y + r), fill=255)
    for i in range(n * 3):             # loose leaves round the edge
        an = r2.random() * math.tau; rr = 1.0 + .16 * r2.random()
        x = cx + rx * rr * math.cos(an); y = cy + ry * rr * math.sin(an); r = 1 + 1.6 * r2.random()
        nd.ellipse(P(x - r, y - r, x + r, y + r), fill=255)
foliage(348, 300, 62, 120, 150, 1); foliage(300, 380, 50, 70, 80, 2); foliage(385, 220, 40, 90, 70, 3)
foliage(22, 360, 44, 80, 90, 4); foliage(60, 420, 40, 50, 60, 5); foliage(-5, 280, 30, 60, 40, 6)
nd.rectangle(P(0, 440, 400, 600), fill=255)
# the house: walls, hipped roof, chimneys, dormer
HX0, HX1, HY0 = 78, 292, 352
nd.rectangle(P(HX0, HY0, HX1, GY), fill=255)
nd.polygon(P((HX0 - 8, HY0), (HX1 + 8, HY0), (HX1 - 26, HY0 - 46), (HX0 + 26, HY0 - 46)), fill=255)
for cxx in (HX0 + 40, HX1 - 52):
    nd.rectangle(P(cxx, HY0 - 70, cxx + 13, HY0 - 40), fill=255); nd.rectangle(P(cxx - 2, HY0 - 73, cxx + 15, HY0 - 68), fill=255)
    nd.rectangle(P(cxx + 2, HY0 - 79, cxx + 5, HY0 - 72), fill=255); nd.rectangle(P(cxx + 8, HY0 - 79, cxx + 11, HY0 - 72), fill=255)
nd.polygon(P((174, HY0 - 22), (196, HY0 - 22), (196, HY0 - 40), (185, HY0 - 50), (174, HY0 - 40)), fill=255)
nm = np.asarray(night) > 127
a = np.asarray(img).copy(); a[nm] = K; img.paste(Image.fromarray(a)); d = ImageDraw.Draw(img); d.fontmode = "1"

# tones of the dark: facade a shade of night-blue, lamp glow, everything dithered
LX, LY = 196, 428                         # the lamp
tone = np.zeros((H * S, W * S, 3), np.float32)
wall = mask_of(lambda dd: dd.rectangle(P(HX0, HY0, HX1, GY), fill=255))
roof = mask_of(lambda dd: dd.polygon(P((HX0 - 8, HY0), (HX1 + 8, HY0), (HX1 - 26, HY0 - 46), (HX0 + 26, HY0 - 46)), fill=255))
tone[wall] = np.array(mix(K, B, .42), np.float32)
tone[roof] = np.array(mix(K, B, .16), np.float32)
dist = np.hypot(xx - (LX + 30), (yy - LY) * 1.0)
glow = np.clip(1 - dist / 150, 0, 1) ** 2.0
gl = glow[..., None] * np.array(Y, np.float32) * 1.25
tone = np.clip(tone * (1 - glow[..., None] * .6) + gl, 0, 255)
# pavement and water
pav = (yy >= GY) & (yy < 532); wat = yy >= 532
tone[pav] = np.clip(np.array(mix(K, B, .12), np.float32) + gl[pav] * .9, 0, 255)
a = np.asarray(img).copy(); sel = nm & ((tone.sum(-1) > 20))
a[sel] = tone[sel].astype(np.uint8); img.paste(Image.fromarray(a)); d = ImageDraw.Draw(img); d.fontmode = "1"

# facade drawing: cornice, string course, quoins, shutters, door
d.rectangle(P(HX0 - 8, HY0 - 3, HX1 + 8, HY0 + 3), fill=K)
d.line(P((HX0, HY0 + 7), (HX1, HY0 + 7)), fill=mix(K, B, .8), width=S)
d.line(P((HX0, 432), (HX1, 432)), fill=K, width=S + 1)
for y in range(HY0 + 10, GY, 12):
    for x0 in (HX0, HX1 - 9):
        d.rectangle(P(x0 + (0 if (y // 12) % 2 else 2), y, x0 + 9 - (2 if (y // 12) % 2 else 0), y + 9), outline=K, width=S)
for k in range(30):                         # roof slates
    y = HY0 - 44 + (k % 6) * 7 + 3; x0 = HX0 + 30 - (k % 6) * 5
    d.line(P((x0, y), (HX1 - 30 + (k % 6) * 5, y)), fill=mix(K, B, .5), width=1)
def window(x, y, w, h, lit=False):
    d.rectangle(P(x - 3, y - 3, x + w + 3, y + h + 3), fill=K)
    if lit:
        d.rectangle(P(x, y, x + w, y + h), fill=Y)
        d.rectangle(P(x + 2, y + 2, x + w - 2, y + h * .45), fill=mix(Y, WH, .6))
        d.line(P((x + w / 2, y), (x + w / 2, y + h)), fill=K, width=S + 1)
        for j in (1, 2): d.line(P((x, y + h * j / 3), (x + w, y + h * j / 3)), fill=K, width=S)
        d.polygon(P((x, y), (x + w * .28, y), (x + w * .18, y + h), (x, y + h)), fill=R)   # a curtain
    else:
        d.rectangle(P(x, y, x + w, y + h), fill=mix(K, B, .75))
        d.line(P((x + w / 2, y), (x + w / 2, y + h)), fill=K, width=S)
        for j in range(1, int(h / 3.2)):
            d.line(P((x + 1, y + j * 3.2), (x + w - 1, y + j * 3.2)), fill=K, width=S)
    d.rectangle(P(x - 5, y + h + 3, x + w + 5, y + h + 6), fill=mix(K, B, .9) if not lit else K)
for i, x in enumerate((96, 144, 206, 254)):
    window(x, 370, 22, 44, lit=(i in (1, 2)))
for i, x in enumerate((96, 254)):
    window(x, 446, 22, 48)
d.rectangle(P(170, 440, 204, GY), fill=K); d.rectangle(P(174, 452, 200, GY), fill=mix(K, G, .55))
d.pieslice(P(174, 440, 200, 464), 180, 360, fill=Y); 
for k in range(5):
    an = math.pi + k * math.pi / 4
    d.line(P((187, 452), (187 + 13 * math.cos(an), 452 + 12 * math.sin(an))), fill=K, width=S)
d.rectangle(P(174, 452, 200, 454), fill=K)
d.line(P((187, 454), (187, GY)), fill=K, width=S); d.ellipse(P(190, 478, 193, 481), fill=Y)
for k, (px, py) in enumerate([(176, 458), (189, 458), (176, 482), (189, 482)]):
    d.rectangle(P(px, py, px + 9, py + 20), outline=K, width=S)
d.polygon(P((164, GY), (210, GY), (214, GY + 5), (160, GY + 5)), fill=mix(K, WH, .45))

# iron railings along the pavement
for x in range(2, 400, 7):
    if 150 < x < 226: continue
    d.line(P((x, GY - 22), (x, GY + 2)), fill=K, width=S); d.polygon(P((x - 1.5, GY - 22), (x + 1.5, GY - 22), (x, GY - 27)), fill=K)
for (xa, xb) in ((0, 150), (226, 400)):
    d.line(P((xa, GY - 18), (xb, GY - 18)), fill=K, width=S); d.line(P((xa, GY - 3), (xb, GY - 3)), fill=K, width=S)

# the street lamp
d.rectangle(P(LX + 30 - 2, LY + 16, LX + 30 + 2, GY + 8), fill=K)
LPX = LX + 30
d.polygon(P((LPX - 5, GY + 8), (LPX + 5, GY + 8), (LPX + 3, GY - 6), (LPX - 3, GY - 6)), fill=K)
d.line(P((LPX - 8, LY + 34), (LPX + 8, LY + 34)), fill=K, width=S + 1)
d.polygon(P((LPX - 7, LY - 6), (LPX + 7, LY - 6), (LPX + 5, LY + 16), (LPX - 5, LY + 16)), fill=WH, outline=K, width=S + 1)
d.polygon(P((LPX - 5, LY - 3), (LPX + 5, LY - 3), (LPX + 3.5, LY + 13), (LPX - 3.5, LY + 13)), fill=mix(Y, WH, .5))
d.polygon(P((LPX - 9, LY - 6), (LPX + 9, LY - 6), (LPX, LY - 17)), fill=K); d.ellipse(P(LPX - 2, LY - 21, LPX + 2, LY - 17), fill=K)
# a man in a bowler under it, and his shadow
mx, my = LPX - 76, GY + 6
d.polygon(P((mx - 6, my), (mx + 6, my), (mx + 5, my - 30), (mx - 5, my - 30)), fill=K)
d.ellipse(P(mx - 4, my - 39, mx + 4, my - 30), fill=K); d.ellipse(P(mx - 7, my - 37, mx + 7, my - 34), fill=K)
d.pieslice(P(mx - 4.5, my - 44, mx + 4.5, my - 32), 180, 360, fill=K)
d.polygon(P((mx - 6, my), (mx + 6, my), (mx - 30, my + 18), (mx - 44, my + 18)), fill=K)

# tree trunks catching the light
for (tx, w_) in ((330, 9), (52, 7)):
    d.polygon(P((tx - w_ / 2, 440), (tx + w_ / 2, 440), (tx + w_ * .8, GY + 4), (tx - w_ * .8, GY + 4)), fill=K)
    d.line(P((tx - w_ * .3 if tx > LX else tx + w_ * .3, 446), (tx - w_ * .55 if tx > LX else tx + w_ * .55, GY)), fill=mix(K, Y, .5), width=S)

# water: reflections broken into dashes
d.rectangle(P(0, 532, 400, 600), fill=K)
d.line(P((0, 532), (400, 532)), fill=mix(K, B, .7), width=S)
def reflect(x, w, col, top=536, bot=598, p=.6, seed=0):
    r2 = np.random.default_rng(seed)
    y = top
    while y < bot:
        f = (y - top) / (bot - top)
        if r2.random() < p * (1 - f * .6):
            ww = w * (1 + f * 1.2) * (.5 + r2.random()); off = (r2.random() - .5) * 6 * (1 + f)
            d.line(P((x + off - ww / 2, y), (x + off + ww / 2, y)), fill=col, width=S + (1 if f > .5 else 0))
        y += 2.0 + f * 1.5
reflect(LPX, 7, Y, p=.95, seed=1); reflect(LPX, 3, WH, p=.5, seed=2)
reflect(155, 9, Y, p=.55, seed=3); reflect(217, 9, Y, p=.55, seed=4); reflect(187, 6, Y, p=.3, seed=5)
for i in range(70):
    x = rng.random() * 400; y = 538 + rng.random() * 60; ln = 5 + rng.random() * 18
    d.line(P((x, y), (x + ln, y)), fill=B if rng.random() < .8 else mix(B, WH, .5), width=S)
finish(img)
