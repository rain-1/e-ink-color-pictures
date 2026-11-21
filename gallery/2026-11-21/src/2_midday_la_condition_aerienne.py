"""Midday — 'La condition aérienne'. For René Magritte, born 21 November 1898.
A yellow room; a canvas on an easel that continues the view exactly, so the balloon is half
painted and half real. Gouache-poster interior; yellow in charge."""
import sys, math, os
sys.path.insert(0, os.path.dirname(__file__))
from common import *
from common import _stamp_lis

rng = np.random.default_rng(1898)

# ---------------------------------------------------------------- the view (drawn full-frame)
V, vd = new(B)
HZ = 318
yy = np.arange(H * S, dtype=np.float32)[:, None] / S
t = np.clip((yy - 40) / (HZ - 40), 0, 1) ** 1.5
sky = lerp_rgb([(0, B), (1, mix(B, WH, .72))], np.repeat(t, W * S, 1))
paint(V, sky)
for (cx, cy, w, sd) in [(215, 108, 80, 2), (330, 150, 95, 7), (140, 215, 110, 4), (300, 262, 120, 9), (120, 292, 70, 12), (345, 80, 55, 1), (180, 300, 60, 6)]:
    cumulus(V, cx, cy, w, seed=sd, shade=mix(B, WH, .35))
vd = ImageDraw.Draw(V); vd.fontmode = "1"
# far hills, fields, hedgerows, poplars, a white road
pts = [(0, HZ + 4)] + [(x, HZ - 6 - 7 * math.sin(x * .021 + 1) - 3 * math.sin(x * .07)) for x in range(0, 401, 4)] + [(400, HZ + 4)]
vd.polygon(P(pts), fill=mix(B, WH, .35))
vd.rectangle(P(0, HZ, 400, 420), fill=G)
for i in range(9):                      # field strips
    y0 = HZ + i * i * 1.3 + i * 2; y1 = HZ + (i + 1) ** 2 * 1.3 + (i + 1) * 2
    c = [G, mix(G, Y, .55), mix(G, K, .3), mix(G, WH, .35)][i % 4]
    vd.polygon(P((0, y0 + 3 * math.sin(i)), (400, y0 - 4 * math.cos(i)), (400, y1 - 4 * math.cos(i + 1)), (0, y1 + 3 * math.sin(i + 1))), fill=c)
    for x in range(0, 400, max(3, 14 - i)):   # furrows
        if i % 4 in (1, 3):
            vd.line(P((x, y0 + 1), (x - 6, y1)), fill=G, width=1 if i < 4 else 2)
road = [(238, HZ + 1), (244, HZ + 14), (228, HZ + 30), (236, HZ + 52), (270, HZ + 80), (330, HZ + 110)]
for i in range(len(road) - 1):
    (xa, ya), (xb, yb) = road[i], road[i + 1]
    wa, wb = 1 + i * 2.2, 1 + (i + 1) * 2.2
    vd.polygon(P((xa - wa, ya), (xa + wa, ya), (xb + wb, yb), (xb - wb, yb)), fill=WH)
for i in range(46):                     # hedgerow trees & poplars
    x = rng.random() * 400; dy = rng.random() ** 1.6 * 78; sz = 2 + dy * .13
    y = HZ + 2 + dy
    if abs(x - 240) < 14 + dy * .2: continue
    if rng.random() < .35:
        vd.ellipse(P(x - sz * .5, y - sz * 3.2, x + sz * .5, y), fill=mix(G, K, .55))
    else:
        vd.ellipse(P(x - sz, y - sz * 1.5, x + sz, y), fill=mix(G, K, .45)); vd.ellipse(P(x - sz * .8, y - sz * 1.5, x + sz * .3, y - sz * .5), fill=G)
balloon(V, 258, 96, 168, rot=0.5, simple=False, figures=True)

# ---------------------------------------------------------------- the room
img, d = new(Y)
FL = 446   # floor line
# wallpaper: white lilies on a half-drop grid, red pips between, faint pinstripes
a = np.asarray(img).copy()
for x in range(0, W * S, 13 * S):
    a[:FL * S, x:x + 2] = mix(Y, WH, .0)
img.paste(Image.fromarray(a))
lis = _stamp_lis(13 * S, WH + (255,))
for r_, y in enumerate(range(6, FL, 21)):
    for x in range(-4 + (13 if r_ % 2 else 0), 400, 26):
        img.paste(lis, (x * S, y * S), lis)
        d.ellipse(P(x + 17.5, y + 6, x + 21.5, y + 10), fill=R)
for x in range(0, 400, 26):
    d.line(P((x + 0.5, 0), (x + 0.5, FL)), fill=mix(Y, R, .5), width=1)

# framed picture, upper left
d.rectangle(P(12, 44, 100, 150), fill=K)
d.rectangle(P(15, 47, 97, 147), fill=mix(R, K, .25)); d.rectangle(P(21, 53, 91, 141), fill=K); d.rectangle(P(23, 55, 89, 139), fill=WH)
balloon(img, 56, 60, 48, simple=True, gallery=True, figures=False)
d = ImageDraw.Draw(img); d.fontmode = "1"
text(d, (56, 120), "Ceci n'est pas", "serif-bi", 11.5, K); text(d, (56, 131), "un ballon.", "serif-bi", 11.5, K)
d.line(P((56, 44), (56, 30)), fill=K, width=S); d.ellipse(P(54, 27, 58, 31), fill=K)

# window
WX0, WX1, WY0, WY1 = 168, 362, 46, 398
win = V.crop((WX0 * S, WY0 * S, WX1 * S, WY1 * S))
d.rectangle(P(WX0 - 12, WY0 - 12, WX1 + 12, WY1 + 14), fill=WH, outline=K, width=S + 1)
img.paste(win, (WX0 * S, WY0 * S))
d.rectangle(P(WX0, WY0, WX1, WY1), outline=K, width=S + 1)
d.rectangle(P(WX0 - 7, WY0 - 7, WX1 + 7, WY1 + 7), outline=K, width=S)
# sill, with its shadow
d.polygon(P((WX0 - 20, WY1 + 14), (WX1 + 20, WY1 + 14), (WX1 + 16, WY1 + 24), (WX0 - 16, WY1 + 24)), fill=WH, outline=K, width=S)
d.polygon(P((WX0 - 16, WY1 + 24), (WX1 + 16, WY1 + 24), (WX1 + 12, WY1 + 31), (WX0 - 8, WY1 + 31)), fill=mix(Y, K, .5))
# curtain rod and curtains
d.rectangle(P(128, 22, 400, 27), fill=K); d.ellipse(P(120, 17, 135, 32), fill=K); d.ellipse(P(124, 20, 129, 25), fill=WH)
def curtain(x0, x1, y0, y1, seed, tie=None):
    r2 = np.random.default_rng(seed)
    n = int((x1 - x0) / 5)
    xs = np.linspace(x0, x1, n + 1)
    for i in range(n):
        ph = i / n * math.pi * 3.5 + seed
        v = math.sin(ph)
        col = R if v > -.2 else mix(R, K, .45)
        if v > .8: col = mix(R, WH, .35)
        sway = lambda yy_: (3.5 * math.sin(yy_ * .012 + i * .5))
        pts = [(xs[i] + sway(y0), y0), (xs[i + 1] + sway(y0) + .4, y0)]
        yb = y1 + 5 * math.sin(i * 1.3)
        if tie:
            ty, tx = tie
            f0 = (xs[i] - x0) / (x1 - x0)
            pts += [(tx + (xs[i + 1] - x0) * .34, ty), (xs[i + 1] + sway(yb) + .4, yb), (xs[i] + sway(yb), yb), (tx + (xs[i] - x0) * .34, ty)]
        else:
            pts += [(xs[i + 1] + sway(yb) + .4, yb), (xs[i] + sway(yb), yb)]
        d.polygon(P(pts), fill=col)
        if i % 2 == 0:
            d.line(P(pts[0], pts[-1]) if not tie else P(pts[0], pts[-1], pts[-2]), fill=K, width=1)
    for i in range(n + 1):       # rings
        if i % 2 == 0:
            d.ellipse(P(xs[i] - 2.5, 21, xs[i] + 2.5, 30), outline=K, width=S)
    if tie:
        ty, tx = tie
        d.rectangle(P(tx - 2, ty - 4, tx + (x1 - x0) * .34 + 3, ty + 4), fill=Y, outline=K, width=S)
        for k in range(5):
            d.line(P((tx + (x1 - x0) * .17, ty + 4), (tx + (x1 - x0) * .17 - 6 + 3 * k, ty + 20)), fill=Y, width=S)
curtain(352, 400, 27, 425, 3, tie=(300, 372))
curtain(134, 180, 27, 428, 1)

# floor: boards in perspective, with grain and joints
d.rectangle(P(0, FL, 400, 600), fill=mix(R, Y, .5))
VP = (190, 235)
k = (600 - VP[1]) / (FL - VP[1])
BOARD = [mix(R, Y, .55), mix(R, Y, .38), mix(R, Y, .68), mix(mix(R, Y, .5), K, .22)]
xt = -260; bi = 0
while xt < 660:
    wtop = 24
    x0b, x1b = VP[0] + (xt - VP[0]) * k, VP[0] + (xt + wtop - VP[0]) * k
    d.polygon(P((xt, FL), (xt + wtop, FL), (x1b, 600), (x0b, 600)), fill=BOARD[bi % 4])
    d.line(P((xt, FL), (x0b, 600)), fill=K, width=S)
    for g in range(3):                     # grain
        f = (g + 1) / 4 + (rng.random() - .5) * .1
        ya = FL + rng.random() * 100; yb = min(600, ya + 30 + rng.random() * 80)
        xa = lambda y_: VP[0] + ((xt + wtop * f) - VP[0]) * ((y_ - VP[1]) / (FL - VP[1]))
        d.line(P((xa(ya), ya), (xa(yb), yb)), fill=mix(R, K, .5), width=2)
    yj = FL + 12 + rng.random() * 130     # a joint with two nails
    xa = lambda xx_, y_: VP[0] + (xx_ - VP[0]) * ((y_ - VP[1]) / (FL - VP[1]))
    d.line(P((xa(xt, yj), yj), (xa(xt + wtop, yj), yj)), fill=K, width=S)
    d.ellipse(P(xa(xt + 6, yj) - 1, yj + 2, xa(xt + 6, yj) + 1, yj + 4), fill=K); d.ellipse(P(xa(xt + 18, yj) - 1, yj + 2, xa(xt + 18, yj) + 1, yj + 4), fill=K)
    xt += wtop; bi += 1
# skirting board
d.rectangle(P(0, FL - 20, 400, FL), fill=WH, outline=K, width=S)
d.line(P((0, FL - 15), (400, FL - 15)), fill=K, width=S); d.line(P((0, FL - 4), (400, FL - 4)), fill=K, width=1)
# light from the window lying on the floor
lm = mask_of(lambda dd: dd.polygon(P((150, FL + 18), (335, FL + 18), (420, 600), (60, 600)), fill=255))
a = np.asarray(img).astype(np.float32)
a[lm] = a[lm] * .62 + np.array(Y, np.float32) * .2 + 255 * .18
img.paste(Image.fromarray(a.astype(np.uint8))); d = ImageDraw.Draw(img); d.fontmode = "1"

# ---------------------------------------------------------------- easel & canvas
CX0, CX1, CY0, CY1 = 96, 262, 138, 376
WOOD = mix(Y, R, .25); WD = mix(mix(Y, R, .4), K, .45)
def beam(p, q, w, fill=WOOD):
    (x0, y0), (x1, y1) = p, q
    L = math.hypot(x1 - x0, y1 - y0); nx, ny = -(y1 - y0) / L * w / 2, (x1 - x0) / L * w / 2
    d.polygon(P((x0 + nx, y0 + ny), (x1 + nx, y1 + ny), (x1 - nx, y1 - ny), (x0 - nx, y0 - ny)), fill=fill, outline=K, width=S)
# shadows of the legs on the floor
for (p, q) in [((92, 566), (30, 590)), ((270, 566), (215, 596)), ((196, 500), (120, 520))]:
    sm = mask_of(lambda dd: dd.line(P(p, q), fill=255, width=7 * S))
    a = np.asarray(img).astype(np.float32); a[sm] *= .45; img.paste(Image.fromarray(a.astype(np.uint8)))
d = ImageDraw.Draw(img); d.fontmode = "1"
beam((184, 120), (196, 502), 8, WD)                      # back leg
beam((150, 104), (92, 566), 9); beam((212, 104), (270, 566), 9)   # front legs
beam((104, 470), (258, 470), 8)                          # lower stretcher
d.rectangle(P(170, 92, 192, 150), fill=WOOD, outline=K, width=S)       # mast
d.rectangle(P(164, 126, 198, 140), fill=WD, outline=K, width=S)        # top clamp
canv = V.crop((CX0 * S, CY0 * S, CX1 * S, CY1 * S))
img.paste(canv, (CX0 * S, CY0 * S))
d.rectangle(P(CX0 - 7, CY0, CX0, CY1), fill=WH, outline=K, width=S)    # the tacked edge of the canvas
for y in range(CY0 + 8, CY1, 13):
    d.ellipse(P(CX0 - 5, y - 1.5, CX0 - 2, y + 1.5), fill=K)
d.line(P((CX0, CY0), (CX1, CY0)), fill=K, width=S); d.line(P((CX0, CY1), (CX1, CY1)), fill=K, width=S)
d.line(P((CX0, CY0), (CX0, CY1)), fill=K, width=S)
# the right edge is only the thinnest line where it crosses the wall and curtain, nothing over the glass
d.line(P((CX1, CY0), (CX1, WY0 - 12)), fill=K, width=S) if CY0 < WY0 - 12 else None
d.rectangle(P(82, CY1, 276, CY1 + 9), fill=WOOD, outline=K, width=S)   # shelf
d.rectangle(P(82, CY1 + 9, 276, CY1 + 13), fill=WD, outline=K, width=S)
# brushes and a tube on the shelf
for i, c in enumerate([B, R, WH]):
    bx = 222 + i * 9
    d.line(P((bx, CY1 - 1), (bx + 20, CY1 - 3 - i)), fill=K, width=S + 1); d.line(P((bx - 5, CY1 - 1), (bx, CY1 - 1)), fill=c, width=S + 2)

# ---------------------------------------------------------------- table, bowler, apple
TX, TYt = 338, 482
sm = mask_of(lambda dd: dd.ellipse(P(TX - 70, 568, TX + 20, 590), fill=255))
a = np.asarray(img).astype(np.float32); a[sm] *= .45; img.paste(Image.fromarray(a.astype(np.uint8)))
d = ImageDraw.Draw(img); d.fontmode = "1"
d.polygon(P((TX - 5, TYt), (TX + 5, TYt), (TX + 4, 560), (TX - 4, 560)), fill=K)
for sgn in (-1, 1):
    d.line(P((TX, 556), (TX + sgn * 28, 582)), fill=K, width=5 * S); d.ellipse(P(TX + sgn * 28 - 4, 579, TX + sgn * 28 + 4, 587), fill=K)
d.line(P((TX, 556), (TX - 6, 592)), fill=K, width=5 * S)
d.ellipse(P(TX - 50, TYt - 2, TX + 50, TYt + 22), fill=K)
d.ellipse(P(TX - 50, TYt - 8, TX + 50, TYt + 16), fill=WH, outline=K, width=S + 1)
d.arc(P(TX - 44, TYt - 5, TX + 44, TYt + 13), 20, 160, fill=K, width=1)
# bowler
hx, hy = TX - 12, TYt - 2
d.ellipse(P(hx - 31, hy - 7, hx + 31, hy + 9), fill=K)
d.pieslice(P(hx - 20, hy - 34, hx + 20, hy + 16), 180, 360, fill=K)
d.rectangle(P(hx - 20, hy - 10, hx + 20, hy), fill=K)
d.arc(P(hx - 15, hy - 30, hx + 5, hy - 2), 190, 260, fill=WH, width=S + 1)
d.line(P((hx - 20, hy - 6), (hx + 20, hy - 6)), fill=WH, width=1)
d.arc(P(hx - 31, hy - 7, hx + 31, hy + 9), 30, 150, fill=WH, width=S)
# apple
ax, ay = TX + 31, TYt - 4
d.ellipse(P(ax - 10, ay - 10, ax + 10, ay + 9), fill=G, outline=K, width=S)
d.ellipse(P(ax - 6, ay - 7, ax - 1, ay - 1), fill=mix(G, WH, .7))
d.line(P((ax, ay - 9), (ax + 2, ay - 15)), fill=K, width=S + 1)
d.polygon(P((ax + 2, ay - 14), (ax + 10, ay - 18), (ax + 7, ay - 11)), fill=G, outline=K)
finish(img)
