"""Afternoon — Opus 11.XI: the painter and the wheel.
After Signac's 1890 portrait of Feneon against a pinwheel of 'beats and angles, tones and
tints'. Here the wheel comes off the tip of the brush: eight swirling arms, each its own
repeat (some bent along the spiral in numpy, some stamped flat), and the painter in his
yachtsman's cap holds a palette that carries exactly the panel's six inks."""
import math, random
import numpy as np
from PIL import Image, ImageDraw
from kit import *

random.seed(217)
FULL = (W * S, H * S); C = (150, 252); N = 8
yy, xx = np.mgrid[0:H * S, 0:W * S].astype(np.float32)
x1, y1 = xx / S - C[0], yy / S - C[1]
r = np.hypot(x1, y1); th = np.arctan2(y1, x1)
sw = (th - 1.25 * np.log1p(r / 26.0) + 0.35) % (2 * np.pi)
sec = np.floor(sw / (2 * np.pi / N)).astype(int) % N
v = (sw / (2 * np.pi / N)) % 1.0; lr = np.log1p(r / 10.0)
INK = np.array([K, Wh, R, Y, B, G], np.uint8)
out = np.zeros((H * S, W * S, 3), np.uint8)

def layer(bg):
    L = Image.new("RGB", FULL, bg); return L, ImageDraw.Draw(L)
def star(dd, x, y, ro, ri, n, col, rot=0.0):
    poly(dd, [(x + math.cos(rot + k * math.pi / n) * (ro if k % 2 == 0 else ri), y + math.sin(rot + k * math.pi / n) * (ro if k % 2 == 0 else ri)) for k in range(2 * n)], fill=col)

# --- arm 0: red/yellow ribbons that follow the spiral, beaded
a0 = np.where(np.floor(v * 7) % 2 == 0, 3, 2)
a0 = np.where((np.abs((v * 7) % 1 - .5) < .16) & (np.floor(lr * 9) % 2 == 0), np.where(a0 == 3, 0, 1), a0)
# --- arm 1: night blue, white and yellow stars
L1, d1 = layer(B)
for k in range(520):
    x, y = random.uniform(0, W), random.uniform(0, H)
    if k % 5 == 0: star(d1, x, y, 5.5, 2.2, 5, Y, random.random())
    elif k % 5 == 1: star(d1, x, y, 4, 1.2, 4, Wh, .78)
    else: circ(d1, x, y, random.choice([.8, 1.1, 1.5]), fill=Wh)
# --- arm 2: red/white chequer bent along the spiral, a blue pip in each white
ch = (np.floor(v * 6) + np.floor(lr * 7)) % 2
pip = (np.abs((v * 6) % 1 - .5) < .14) & (np.abs((lr * 7) % 1 - .5) < .2)
a2 = np.where(ch == 0, 2, 1); a2 = np.where(pip, np.where(ch == 0, 3, 4), a2)
# --- arm 3: yellow regatta: little boats on little waves
L3, d3 = layer(Y)
for gy in range(-1, 34):
    for gx in range(-1, 18):
        x = gx * 26 + (gy % 2) * 13; y = gy * 20
        line(d3, [(x - 12 + k, y + 8 + 1.6 * math.sin(k * .9)) for k in range(0, 25)], B, 0.9)
        poly(d3, [(x - 7, y + 2), (x + 8, y + 2), (x + 5, y + 6.5), (x - 5, y + 6.5)], fill=K)
        poly(d3, [(x, y + 1), (x, y - 11), (x + 7, y + 1)], fill=R if (gx + gy) % 3 else Wh)
        poly(d3, [(x - 1.5, y + 1), (x - 1.5, y - 8), (x - 6, y + 1)], fill=Wh if (gx + gy) % 3 else R)
# --- arm 4: black with white rings, yellow studs
ring = np.floor(lr * 13) % 2
a4 = np.where(ring == 0, 0, 1)
stud = (ring == 0) & (np.abs((v * 9) % 1 - .5) < .1) & (np.abs((lr * 13) % 1 - .5) < .3)
a4 = np.where(stud, 3, a4)
# --- arm 5: green fish-scales
L5, d5 = layer(G)
for gy in range(70, -2, -1):
    for gx in range(-1, 32):
        x = gx * 14 + (gy % 2) * 7; y = gy * 9
        circ(d5, x, y, 8, fill=G if (gx + gy) % 4 else Y, outline=K, w=0.7); circ(d5, x, y + 2, 3.2, outline=K, w=0.5)
        circ(d5, x, y + 3, 1.2, fill=Wh)
# --- arm 6: blue and white waves along the spiral
wv = np.sin(lr * 26 + 2.2 * np.sin(v * 2 * np.pi * 3))
a6 = np.where(wv > 0.25, 4, 1); a6 = np.where((wv > -.2) & (wv < -.02), 3, a6)
# --- arm 7: red, sown with white cyclamen and yellow seed
L7, d7 = layer(R)
for gy in range(-1, 36):
    for gx in range(-1, 20):
        x = gx * 22 + (gy % 2) * 11; y = gy * 18
        line(d7, [(x, y + 9), (x + 2, y + 2), (x, y - 2)], K, 0.6)
        for q in range(5):
            a = -math.pi / 2 + (q - 2) * .5
            poly(d7, [(x, y - 2), (x + math.cos(a - .22) * 8, y - 2 + math.sin(a - .22) * 8), (x + math.cos(a + .22) * 8, y - 2 + math.sin(a + .22) * 8)], fill=Wh)
        circ(d7, x, y - 2, 1.5, fill=Y); circ(d7, x + 11, y + 4, 1.2, fill=Y); circ(d7, x + 11, y - 6, .8, fill=K)

flat = {1: L1, 3: L3, 5: L5, 7: L7}; bent = {0: a0, 2: a2, 4: a4, 6: a6}
for s in range(N):
    m = sec == s
    out[m] = (np.asarray(flat[s])[m] if s in flat else INK[bent[s]][m])
# seams between arms: black, with a yellow thread
edge = np.minimum(v, 1 - v) * (2 * np.pi / N) * r           # arc-distance to the seam, px
out[edge < 1.5] = K; out[(edge < 0.45) & (r > 14)] = Y
im = Image.fromarray(out); d = ImageDraw.Draw(im)
# the hub, where the brush touches
for rr_, c in [(15, K), (13.5, Wh), (10, R), (6.5, Y), (3, Wh)]: circ(d, C[0], C[1], rr_, fill=c)
for k in range(16):
    a = k * math.pi / 8; line(d, [(C[0] + math.cos(a) * 10.5, C[1] + math.sin(a) * 10.5), (C[0] + math.cos(a) * 13, C[1] + math.sin(a) * 13)], K, 0.8)

# ---------- the painter, in profile, right ----------
OX, OY = 0, 96
def T(pts): return [(x + OX, y + OY) for x, y in pts]
# trousers (white duck), then pea jacket, then jersey
poly(d, T([(288, 470), (400, 470), (400, 520), (284, 520)]), fill=Wh, outline=K, w=1)
for x in range(292, 400, 9): line(d, T([(x, 472), (x - 2, 520)]), B, 0.5)
jacket = T([(296, 224), (322, 212), (352, 214), (388, 236), (404, 300), (404, 480), (280, 480), (286, 400), (292, 330), (284, 262)])
poly(d, jacket, fill=K)
jersey = T([(296, 224), (322, 218), (316, 330), (306, 480), (282, 480), (288, 400), (294, 330), (285, 262)])
poly(d, jersey, fill=Wh)
m = Image.new("L", FULL, 0); ImageDraw.Draw(m).polygon(P(jersey), fill=255)
st, sd = layer(Wh)
for y in range(200, 620, 8): rect(sd, 250, y, 360, y + 3.4, fill=B)
im.paste(st, (0, 0), m); line(d, jersey + [jersey[0]], K, 0.9)
lap = T([(322, 214), (340, 222), (322, 300), (316, 330), (318, 262)])                 # lapel + buttons
poly(d, lap, fill=K, outline=Y, w=0.8)
for k in range(4):
    circ(d, 331 - k * 3 + OX, 300 + k * 44 + OY, 4, fill=Y, outline=K, w=0.5); circ(d, 331 - k * 3 + OX, 300 + k * 44 + OY, 1.2, fill=K)
line(d, T([(388, 236), (396, 300), (398, 480)]), Y, 0.6)
for k in range(9): line(d, T([(350 + k * 5, 250 + k * 3), (352 + k * 5, 470)]), B, 0.4)            # nap of the cloth
# brush arm: sleeve to the left, cuff, hand, the long brush to the hub
sleeve = T([(306, 240), (332, 262), (276, 312), (232, 300), (236, 276), (270, 282)])
poly(d, sleeve, fill=K, outline=Y, w=0.8)
for k in range(3): line(d, T([(246 + k * 5, 279 + k), (243 + k * 5, 301 + k)]), Y, 0.9)             # cuff braid
hand = T([(236, 276), (232, 300), (218, 296), (210, 286), (216, 276)])
poly(d, hand, fill=Wh, outline=K, w=0.9); line(d, T([(214, 282), (226, 284)]), K, 0.5); line(d, T([(215, 288), (226, 290)]), K, 0.5)
hx, hy = 216 + OX, 284 + OY
bx, by = C[0] + 9, C[1] + 5
line(d, [(hx + 22, hy + 11), (bx + 12, by + 6)], K, 3.2); line(d, [(hx + 22, hy + 11), (bx + 12, by + 6)], Y, 1.6)
line(d, [(bx + 14, by + 7), (bx + 6, by + 3)], Wh, 3); poly(d, [(bx + 7, by + 6), (bx + 8, by), (bx - 8, by - 5)], fill=R, outline=K, w=0.5)
# palette arm and the palette of six inks
arm2 = T([(366, 250), (396, 262), (392, 372), (352, 396), (336, 378), (366, 352)])
poly(d, arm2, fill=K, outline=Y, w=0.8)
pcx, pcy = 318 + OX, 408 + OY
pal = [(pcx + math.cos(a) * (56 + 7 * math.sin(2 * a + 1)), pcy + math.sin(a) * (34 + 4 * math.cos(3 * a))) for a in [k * math.pi / 30 for k in range(60)]]
poly(d, pal, fill=Wh, outline=K, w=1.4)
hatch(im, pal, K, gap=5, ang=12, w=0.3)
ell(d, pcx + 32, pcy + 6, 8, 6, fill=K); poly(d, T([(346, 400), (358, 396), (364, 412), (350, 418)]), fill=Wh, outline=K, w=0.8)   # thumb
for k, c in enumerate([K, Wh, R, Y, B, G]):
    a = math.pi * (0.62 + k * 0.2); px_, py_ = pcx + math.cos(a) * 38, pcy + math.sin(a) * 21
    ell(d, px_, py_, 8.5, 6.5, fill=c, outline=K, w=0.8); ell(d, px_ - 2, py_ - 2, 2.4, 1.5, fill=Wh if c != Wh else Y)
for k in range(3): line(d, [(pcx + 20 + k * 5, pcy + 16), (pcx + 62 + k * 6, pcy - 30 - k * 4)], K, 1.6)            # spare brushes
for k, c in enumerate([B, G, R]): circ(d, pcx + 62 + k * 6, pcy - 30 - k * 4, 2.6, fill=c, outline=K, w=0.5)
# head: neck, face, beard, cap
poly(d, T([(308, 196), (332, 190), (336, 222), (304, 226)]), fill=Wh, outline=K, w=0.8)
poly(d, T([(300, 218), (338, 210), (340, 226), (298, 232)]), fill=R, outline=K, w=0.7)                                # neckerchief
poly(d, T([(300, 230), (296, 248), (306, 244), (310, 232)]), fill=R, outline=K, w=0.7)
for k in range(5): circ(d, 306 + k * 7 + OX, 222 - k * 1.6 + OY, 1.1, fill=Wh)
face = T([(304, 146), (298, 160), (288, 173), (294, 178), (293, 184), (296, 188), (294, 196), (306, 204), (328, 198), (338, 176), (336, 150)])
poly(d, face, fill=Wh, outline=K, w=1)
beard = T([(295, 186), (286, 214), (300, 210), (312, 214), (330, 200), (338, 174), (328, 170), (322, 186), (308, 190)])
poly(d, beard, fill=K)
for k in range(7): line(d, T([(298 + k * 4, 194), (290 + k * 4.5, 210 + (k % 2) * 2)]), Wh, 0.4)
poly(d, T([(292, 180), (304, 177), (312, 184), (300, 185)]), fill=K)                                                  # moustache
poly(d, T([(326, 150), (340, 150), (340, 178), (330, 172)]), fill=K)                                                  # hair
ell(d, 329 + OX, 172 + OY, 4, 6, fill=Wh, outline=K, w=0.7)                                                           # ear
line(d, T([(300, 160), (309, 158)]), K, 1.4); circ(d, 304 + OX, 163.5 + OY, 1.7, fill=K); line(d, T([(300, 166), (308, 166.5)]), K, 0.5)
cap = T([(298, 148), (302, 132), (322, 124), (344, 128), (350, 142), (342, 152)])
poly(d, cap, fill=B, outline=K, w=1); poly(d, T([(298, 148), (342, 152), (342, 146), (299, 142)]), fill=K)
poly(d, T([(300, 146), (280, 154), (284, 158), (304, 152)]), fill=K)                                                  # peak
circ(d, 312 + OX, 136 + OY, 4.2, fill=Y, outline=K, w=0.5); line(d, T([(312, 133), (312, 139)]), K, 0.7); line(d, T([(309.5, 137.5), (314.5, 137.5)]), K, 0.7)
# opus cartouche
rect(d, 14, 556, 150, 586, fill=Wh, outline=K, w=1.2); rect(d, 17, 559, 147, 583, outline=R, w=0.6)
text(d, 82, 566.5, "OPUS 11 · XI", 10.5, K, bold=True); text(d, 82, 577.5, "P. Signac, né le 11 novembre 1863", 6.6, K, italic=True)
save(im)
