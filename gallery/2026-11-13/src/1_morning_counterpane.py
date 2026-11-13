# Morning — "The Land of Counterpane" (A Child's Garden of Verses, 1885).
# "I was the giant great and still / That sits upon the pillow-hill, / And sees before him,
# dale and plain, / The pleasant land of counterpane."  A sick-bed seen from its foot: the
# quilt is a patchwork country with knees for hills; lead soldiers, a fleet, a block city.
import math, random
import numpy as np
from kit import *
random.seed(13); c = Canvas(Y)

# ---- wall and wallpaper -----------------------------------------------------------
c.fill(WH, hatch(90, 24, 2, 0))
fl = c.layer()
for j in range(12):
    for i in range(18):
        x = 12 + i * 24 + (12 if j % 2 else 0) - 12; y = 10 + j * 18
        for dx, dy in ((0, -2.4), (2.4, 0), (0, 2.4), (-2.4, 0)): fl.circle(x + dx, y + dy, 1.5)
fl.put(R)
c.put(dots(24, 1.2, False, 0, 10) & False, WH)

# ---- window: a November dawn over the chimneys --------------------------------------
wx0, wy0, wx1, wy1 = 30, 14, 132, 122
c.put(c.layer().rect(wx0 - 5, wy0 - 5, wx1 + 5, wy1 + 7).mask(), K)
c.put(c.layer().rect(wx0 - 3, wy0 - 3, wx1 + 3, wy1 + 5).mask(), WH)
win = c.layer().rect(wx0, wy0, wx1, wy1).mask()
c.put(win, B)
t = np.clip((YY - wy0) / (wy1 - wy0 - 20), 0, 1)
c.put(win, WH, tone(t ** 1.6))
c.put(win & (YY > wy1 - 42), Y, tone(np.clip((YY - (wy1 - 46)) / 26, 0, 1)))
sun = c.layer().circle(96, wy1 - 16, 13).mask() & win
ray = c.layer()
for i in range(14):
    a = math.pi + math.pi * i / 13
    ray.seg(96 + 17 * math.cos(a), wy1 - 16 + 17 * math.sin(a), 96 + 26 * math.cos(a), wy1 - 16 + 26 * math.sin(a), 1.4)
c.put(ray.mask(0.3) & win, Y); c.put(sun, R); c.put(c.layer().circle(96, wy1 - 16, 10).mask() & win, Y)
roofs = c.layer()
roofs.poly([(wx0, wy1), (wx0, wy1 - 16), (48, wy1 - 26), (66, wy1 - 16), (66, wy1 - 12), (84, wy1 - 12), (84, wy1 - 20), (100, wy1 - 9), (118, wy1 - 20), (wx1, wy1 - 14), (wx1, wy1)])
for x, hgt in ((38, 30), (60, 22), (112, 28), (124, 24)):
    roofs.rect(x, wy1 - hgt, x + 7, wy1 - 8); roofs.rect(x + 1, wy1 - hgt - 4, x + 3, wy1 - hgt); roofs.rect(x + 4, wy1 - hgt - 4, x + 6, wy1 - hgt)
c.put(roofs.mask() & win, K)
for x, y in ((41, wy1 - 40), (115, wy1 - 38)):    # chimney smoke
    c.put(c.layer().line(smooth([(x, y), (x + 4, y - 8), (x - 1, y - 16), (x + 5, y - 26)], closed=False), 1.6).mask(0.3) & win, WH)
c.put(c.layer().rect((wx0 + wx1) / 2 - 1.5, wy0, (wx0 + wx1) / 2 + 1.5, wy1).rect(wx0, 62, wx1, 65).mask(), WH)
c.hair([(wx0, wy0), (wx1, wy0), (wx1, wy1), (wx0, wy1)], K, closed=True)
for side in (0, 1):                                # red curtains, gathered
    xs = [wx0 - 12, wx0 + 12] if side == 0 else [wx1 - 12, wx1 + 12]
    cur = c.layer().poly([(xs[0], wy0 - 8), (xs[1], wy0 - 8), (xs[1] - (6 if side == 0 else -6) * 0 + (-6 if side == 0 else 6) * 0, 80),
                          ((xs[0] + xs[1]) / 2 + (-9 if side == 0 else 9), 96), (xs[1] + (-2 if side == 0 else 2) * 0, wy1 + 10), (xs[0], wy1 + 10)]).mask()
    c.put(cur, R); c.put(cur, K, hatch(90, 5, 1, side * 2)); c.put(cur & ~np.roll(cur, 1, 1) | cur & ~np.roll(cur, -1, 1), K)
    c.put(c.layer().rect(xs[0] - 1, 92, xs[1] + 1, 97).mask() & grow(cur, 1), Y)
c.put(c.layer().rect(wx0 - 16, wy0 - 12, wx1 + 16, wy0 - 8).mask(), K)
c.put(c.layer().circle(wx0 - 17, wy0 - 10, 3.5).circle(wx1 + 17, wy0 - 10, 3.5).mask(), K)

# ---- sampler and shelf ---------------------------------------------------------------
c.put(c.layer().rect(206, 16, 262, 60).mask(), K); c.put(c.layer().rect(209, 19, 259, 57).mask(), WH)
c.put(c.layer(1).rect(212, 22, 256, 54).mask() & ~c.layer(1).rect(214, 24, 254, 52).mask(), R, checker(2))
c.text(234, 33, "R L S", R, "dserif-b", 10); c.text(234, 45, "1850", B, "dserif", 9)
c.hair([(234, 16), (234, 8)], K)
sy = 64
c.put(c.layer().rect(274, sy, 352, sy + 5).mask(), K); c.put(c.layer().rect(276, sy + 1, 350, sy + 3).mask(), WH)
for bx in (284, 342): c.poly([(bx - 2, sy + 5), (bx + 2, sy + 5), (bx + 2, sy + 22), (bx - 2, sy + 12)], K)
# candle (the day's light)
cx = 290
glow = c.layer().circle(cx, sy - 44, 17).mask(); c.put(glow, WH, dots(4, 1.0))
c.put(c.layer().ellipse(cx, sy - 2, 12, 3).rect(cx - 3, sy - 10, cx + 3, sy - 2).ellipse(cx, sy - 10, 7, 2.5).mask(), K)
c.put(c.layer().ellipse(cx, sy - 2.5, 10.5, 2).rect(cx - 2, sy - 10, cx + 2, sy - 3).ellipse(cx, sy - 10.5, 5.5, 1.5).mask(), Y)
c.put(c.layer().ring(cx + 13, sy - 5, 4, 1.4).mask(0.3), K)
c.put(c.layer().rect(cx - 4, sy - 34, cx + 4, sy - 11).mask(), K); c.put(c.layer().rect(cx - 3, sy - 33, cx + 3, sy - 11).mask(), WH)
c.hair([(cx, sy - 34), (cx, sy - 38)], K)
c.poly(smooth([(cx, sy - 52), (cx + 4.5, sy - 42), (cx, sy - 36), (cx - 4.5, sy - 42)]), R); c.poly(smooth([(cx, sy - 47), (cx + 2.5, sy - 41), (cx, sy - 37.5), (cx - 2.5, sy - 41)]), Y)
# medicine bottle and spoon
bx = 314
c.put(c.layer().rect(bx - 8, sy - 26, bx + 8, sy).rect(bx - 3, sy - 34, bx + 3, sy - 26).rect(bx - 4, sy - 38, bx + 4, sy - 34).mask(), K)
c.put(c.layer().rect(bx - 7, sy - 25, bx + 7, sy - 1).rect(bx - 2, sy - 33, bx + 2, sy - 25).mask(), B)
c.put(c.layer().rect(bx - 7, sy - 19, bx + 7, sy - 7).mask(), WH); c.put(c.layer(1).rect(bx - 5, sy - 16, bx + 5, sy - 15).rect(bx - 5, sy - 12, bx + 3, sy - 11).mask(), K)
c.put(c.layer().rect(bx - 3, sy - 37, bx + 3, sy - 34).mask(), Y)
# books
for x, w, hgt, col in ((328, 7, 30, R), (335, 6, 26, G), (341, 8, 32, B)):
    c.put(c.layer().rect(x, sy - hgt, x + w, sy).mask(), K); c.put(c.layer().rect(x + 1, sy - hgt + 1, x + w - 1, sy).mask(), col)
    c.put(c.layer(1).rect(x + 1, sy - hgt + 5, x + w - 1, sy - hgt + 6).rect(x + 1, sy - 7, x + w - 1, sy - 6).mask(), Y)

# ---- floor beside the bed ------------------------------------------------------------
c.put(YY >= 204, B); c.put(YY >= 204, K, hatch(0, 9, 1)); c.put((YY >= 200) & (YY < 204), K); c.put((YY >= 196) & (YY < 200), WH)

# ---- iron bedstead --------------------------------------------------------------------
bed = c.layer()
top = lambda x: 78 + 22 * ((x - 200) / 164) ** 2
bed.line([(x, top(x)) for x in range(36, 365, 4)], 4)
bed.line([(x, 150) for x in (36, 364)], 3)
for i in range(1, 14):
    x = 36 + i * 328 / 14; bed.seg(x, top(x), x, 215, 2)
for x in (36, 364): bed.rect(x - 4, 66, x + 4, 240)
bedm = bed.put(K, thr=0.4)
scr = c.layer()                                     # scrollwork between the bars
for i in range(1, 14, 2):
    x = 36 + (i + 0.5) * 328 / 14; scr.ring(x, top(x) + 16, 7, 1.4)
scr.put(K, thr=0.3)
for x in (36, 364):
    c.put(c.layer().circle(x, 60, 9).mask(), K); c.put(c.layer().circle(x, 60, 7.5).mask(), Y); c.put(c.layer().circle(x - 2.5, 57.5, 2).mask(), WH)
    c.put(c.layer().rect(x - 2, 72, x + 2, 236).mask(), K)
for i in (3, 7, 11):
    x = 36 + i * 328 / 14; c.put(c.layer().circle(x, top(x), 4.5).mask(), K); c.put(c.layer().circle(x, top(x), 3).mask(), Y)

# ---- pillows ---------------------------------------------------------------------------
def pillow(x0, y0, x1, y1, sag=8, stripe=True):
    p = smooth([(x0, y0 + 6), (x0 + 14, y0 - 2), ((x0 + x1) / 2, y0 + sag * 0.6), (x1 - 14, y0 - 2), (x1, y0 + 6), (x1 - 5, (y0 + y1) / 2),
                (x1 + 2, y1 - 4), (x1 - 16, y1 + 2), ((x0 + x1) / 2, y1 - 3), (x0 + 16, y1 + 2), (x0 - 2, y1 - 4), (x0 + 5, (y0 + y1) / 2)], n=10)
    m = c.layer().poly(p).mask(); c.put(grow(m, 1), K); c.put(m, WH)
    if stripe: c.put(m & ~grow(~m, 4), B, hatch(90, 9, 1))
    d = depth(m, 14); c.put(m & (d < 9), K, tone(0.22 - 0.02 * d))
    return m
pillow(64, 112, 336, 196, 10)
pm = pillow(92, 134, 308, 214, 6, False)
cr = c.layer()                                      # creases radiating from the head
for a in (200, 225, 250, 290, 315, 340, 160, 20):
    cr.seg(200 + 34 * math.cos(math.radians(a)), 170 + 30 * math.sin(math.radians(a)), 200 + 62 * math.cos(math.radians(a)), 170 + 46 * math.sin(math.radians(a)), 1)
c.put(cr.mask(0.3) & pm, K)

# ---- the giant great and still ------------------------------------------------------------
hx, hy = 200, 168
# nightshirt shoulders
sh = c.layer().poly(smooth([(162, 222), (166, 198), (186, 188), (214, 188), (234, 198), (238, 222)])).mask()
c.put(grow(sh, 1), K); c.put(sh, WH); c.put(sh, B, hatch(90, 5, 1))
c.poly([(190, 189), (200, 201), (210, 189)], WH); c.line([(190, 189), (200, 201), (210, 189)], K, 1.2)
head = c.layer().ellipse(hx, hy, 21, 23).mask()
ears = c.layer().circle(hx - 21, hy + 2, 4).circle(hx + 21, hy + 2, 4).mask()
c.put(grow(head | ears, 1), K); c.put(head | ears, WH)
hair = c.layer().poly(smooth([(hx - 23, hy - 2), (hx - 20, hy - 18), (hx - 6, hy - 27), (hx + 10, hy - 26), (hx + 21, hy - 16), (hx + 23, hy - 2), (hx + 16, hy - 10),
                              (hx + 8, hy - 15), (hx - 2, hy - 10), (hx - 10, hy - 14), (hx - 17, hy - 8)])).mask()
c.put(hair, K)
c.put(c.layer().circle(hx - 8, hy + 1, 2.2).circle(hx + 8, hy + 1, 2.2).mask(), K)
c.put(c.layer(1).rect(hx - 9, hy, hx - 8, hy + 1).rect(hx + 7, hy, hx + 8, hy + 1).mask(), WH)
c.line(arc(hx - 8, hy - 5, 4, 2, 200, 340), K, 1); c.line(arc(hx + 8, hy - 5, 4, 2, 200, 340), K, 1)
c.line([(hx, hy + 4), (hx - 1.5, hy + 8), (hx + 1, hy + 8.5)], K, 1)
c.line(arc(hx, hy + 11, 6, 3.5, 20, 160), R, 1.5)
c.put(c.layer().circle(hx - 13, hy + 9, 3.5).circle(hx + 13, hy + 9, 3.5).mask(), R, checker(1))

# ---- the counterpane ------------------------------------------------------------------------
NU, NV = 8, 11
def hgt(u, v):
    g = lambda u0, v0, a, su, sv: a * math.exp(-((u - u0) / su) ** 2 - ((v - v0) / sv) ** 2)
    return g(0.44, 0.36, 44, 0.17, 0.13) + g(0.60, 0.40, 36, 0.15, 0.12) + g(0.52, 0.76, 30, 0.2, 0.09) + g(0.12, 0.55, 14, 0.12, 0.2) \
        + g(0.9, 0.2, 12, 0.1, 0.15) + 4 * math.sin(u * 11 + v * 5) * (0.3 + v)
def Q(u, v):
    wdt = 318 + 250 * v
    return (200 + (u - 0.5) * wdt + 5 * math.sin(v * 7 + u * 3), 224 + 392 * v ** 1.12 - hgt(u, v))
quilt = c.layer().poly([Q(0, v / 40) for v in range(41)] + [Q(1, v / 40) for v in range(40, -1, -1)]).mask()
styles = [  # base, ink, pattern
    (B, WH, dots(6, 1.2)), (WH, B, hatch(90, 6, 2)), (B, WH, cross(45, 8, 1)), (WH, B, cross(0, 6, 1)), (WH, B, dots(7, 1.6)),
    (B, Y, dots(9, 1.6)), (WH, R, hatch(45, 6, 1.5)), (R, WH, checker(3)), (Y, R, dots(8, 1.5)), (G, WH, dots(6, 1.1)),
    (WH, G, hatch(135, 5, 1.5)), (B, WH, hatch(0, 5, 1)), (R, WH, hatch(90, 7, 1.5)), (WH, B, hatch(45, 4, 1)), (Y, K, cross(45, 10, 1)),
    (G, Y, hatch(0, 6, 1.5)), (B, WH, checker(4)), (WH, R, dots(6, 1.2))]
wts = [5, 5, 4, 4, 4, 3, 3, 3, 2, 2, 3, 4, 2, 4, 2, 2, 3, 3]
grid = {}
sub = 5
for j in range(NV):
    for i in range(NU):
        while True:
            k = random.choices(range(len(styles)), wts)[0]
            if grid.get((i - 1, j)) != k and grid.get((i, j - 1)) != k and styles[k][0] not in (styles[grid[(i - 1, j)]][0] if (i - 1, j) in grid and styles[k][0] != WH and styles[k][0] != B else -1,): break
        grid[(i, j)] = k
        u0, u1, v0, v1 = i / NU, (i + 1) / NU, j / NV, (j + 1) / NV
        edge = [Q(u0 + (u1 - u0) * t / sub, v0) for t in range(sub)] + [Q(u1, v0 + (v1 - v0) * t / sub) for t in range(sub)] \
             + [Q(u1 - (u1 - u0) * t / sub, v1) for t in range(sub)] + [Q(u0, v1 - (v1 - v0) * t / sub) for t in range(sub + 1)]
        m = c.layer(2).poly(edge).mask()
        base, ink, pat = styles[k]; c.put(m, base); c.put(m, ink, pat)
# shading: the quilt is lit from the window, upper left
shade = np.zeros((H, W)); cnt = c.layer(2)
S = 40
for j in range(S):
    for i in range(S):
        u, v = (i + 0.5) / S, (j + 0.5) / S
        s_ = (hgt(u + 0.03, v + 0.02) - hgt(u - 0.03, v - 0.02)) / 14.0
        if s_ < -0.08:
            val = min(0.6, -s_ * 0.55)
            pl = [Q(i / S, j / S), Q((i + 1) / S, j / S), Q((i + 1) / S, (j + 1) / S), Q(i / S, (j + 1) / S)]
            L = Image.new("L", (W, H), 0); ImageDraw.Draw(L).polygon(pl, fill=255)
            shade = np.maximum(shade, (np.asarray(L) > 0) * val)
c.put(quilt & (shade > 0.12), K, hatch(45, 4, 1)); c.put(quilt & (shade > 0.3), K, hatch(135, 4, 1)); c.put(quilt & (shade > 0.5), K, hatch(45, 2, 1))
# seams, double-stitched
seam = c.layer()
for i in range(NU + 1): seam.line([Q(i / NU, v / 60) for v in range(61)], 1.6)
for j in range(NV + 1): seam.line([Q(u / 40, j / NV) for u in range(41)], 1.6)
sm = seam.mask(0.3) & grow(quilt, 1); c.put(sm, K)
st = c.layer(1)
for i in range(NU + 1):
    for v in range(0, 120, 2): st.line([Q(i / NU + 0.012, v / 120), Q(i / NU + 0.012, (v + 1) / 120)], 1)
for j in range(1, NV + 1):
    for u in range(0, 100, 2): st.line([Q(u / 100, j / NV - 0.012), Q((u + 1) / 100, j / NV - 0.012)], 1)
c.put(st.mask() & quilt & ~sm, WH)

# sheet turned down over the quilt's top edge, with a scalloped hem
sheet = c.layer()
sheet.poly([(18, 196)] + [(x, 199 + 3 * math.sin(x / 23)) for x in range(18, 383, 4)] + [(382, 196)] + [Q(u / 30, 0.035) for u in range(30, -1, -1)])
for k in range(31):
    x, y = Q(k / 30, 0.035); sheet.circle(x, y + 1, 5.5)
shm = sheet.mask(); c.put(grow(shm, 1), K); c.put(shm, WH)
c.put(shm & ~grow(~shm, 5) & (YY > 215), B, dots(5, 0.9, False))
c.put(c.layer(1).line([(x, 207 + 3 * math.sin(x / 23)) for x in range(24, 378, 4)], 1).mask() & shm, B, hatch(90, 4, 2))
# hands on the sheet
for sx in (-1, 1):
    arm = c.layer().poly(smooth([(hx + sx * 30, 200), (hx + sx * 40, 198), (hx + sx * 66, 222), (hx + sx * 60, 232), (hx + sx * 36, 216)])).mask()
    c.put(grow(arm, 1), K); c.put(arm, WH); c.put(arm, B, hatch(90, 5, 1))
    hand = c.layer().ellipse(hx + sx * 66, 229, 7, 5.5).mask(); c.put(grow(hand, 1), K); c.put(hand, WH)
    c.hair([(hx + sx * 66, 226), (hx + sx * 71, 228)], K); c.hair([(hx + sx * 66, 229), (hx + sx * 72, 231)], K)

# ---- toys -------------------------------------------------------------------------------------
def sprite(parts, x, y, s):
    """parts: list of (colour, fn(layer)); a 1-px black keyline is drawn round the union."""
    ms = []
    for col, fn in parts:
        L = c.layer(); fn(L, lambda px, py: (x + px * s, y + py * s), s); ms.append((col, L.mask(0.45)))
    u = np.zeros((H, W), bool)
    for _, m in ms: u |= m
    c.put(grow(u, 1), K)
    for col, m in ms: c.put(m, col)

def soldier(x, y, s, face=1):
    P = None
    parts = [
        (G, lambda L, P, s: L.ellipse(*P(0, 0), 8 * s, 3 * s)),
        (K, lambda L, P, s: (L.poly([P(-4, -1), P(-1, -1), P(-1, -3), P(-4, -3)]), L.poly([P(1, -1), P(5, -1), P(4, -3), P(1, -3)]))),
        (B, lambda L, P, s: (L.poly([P(-4, -3), P(-0.5, -3), P(-0.5, -12), P(-4, -12)]), L.poly([P(0.5, -3), P(4, -3), P(4, -12), P(0.5, -12)]))),
        (R, lambda L, P, s: (L.poly([P(-5, -11), P(5, -11), P(5.5, -21), P(-5.5, -21)]), L.poly([P(-7.5, -20), P(-5, -21), P(-5, -12), P(-7.5, -12)]), L.poly([P(7.5, -20), P(5, -21), P(5, -14), P(7.5, -14)]))),
        (WH, lambda L, P, s: (L.line([P(-5, -21), P(5, -12)], 1.3 * s), L.line([P(5, -21), P(-5, -12)], 1.3 * s), L.circle(*P(0, -24.5), 3.6 * s), L.circle(*P(-6.5, -11.5), 1.6 * s))),
        (K, lambda L, P, s: (L.poly([P(-4, -27), P(4, -27), P(3.5, -35), P(-3.5, -35)]), L.poly([P(-4, -27), P(6 * face, -27), P(6 * face, -26), P(-4, -26)]), L.line([P(7, -13), P(8.5, -38)], 1.2 * s))),
        (Y, lambda L, P, s: (L.circle(*P(0, -36.5), 1.8 * s), L.circle(*P(0, -16.5), 1.1 * s), L.rect(P(-3.5, -30)[0], P(0, -30)[1], P(3.5, -30)[0], P(0, -28.6)[1]))),
        (WH, lambda L, P, s: L.line([P(8.5, -38), P(9, -44)], 1.0 * s)),
    ]
    sprite(parts, x, y, s)
    c.put(c.layer(1).rect(x + 1 * s * face, y - 25 * s, x + 1 * s * face + 1, y - 24 * s + 1).mask(), K)

def tree(x, y, s, kind=0):
    if kind == 0:
        parts = [(K, lambda L, P, s: L.rect(P(-1, 0)[0], P(0, -8)[1], P(1, 0)[0], P(0, 0)[1])), (R, lambda L, P, s: L.ellipse(*P(0, 0), 5 * s, 2 * s)),
                 (G, lambda L, P, s: (L.poly([P(-7, -6), P(0, -17), P(7, -6)]), L.poly([P(-5.5, -13), P(0, -23), P(5.5, -13)]), L.poly([P(-4, -19), P(0, -28), P(4, -19)])))]
    else:
        parts = [(K, lambda L, P, s: L.rect(P(-1, 0)[0], P(0, -10)[1], P(1, 0)[0], P(0, 0)[1])), (Y, lambda L, P, s: L.ellipse(*P(0, 0), 5 * s, 2 * s)),
                 (G, lambda L, P, s: L.circle(*P(0, -16), 8 * s)), (WH, lambda L, P, s: L.circle(*P(-3, -19), 1.6 * s))]
    sprite(parts, x, y, s)

def house(x, y, s, wall=WH, roof=R, w=14, hh=12, spire=False):
    parts = [(wall, lambda L, P, s: L.poly([P(-w / 2, 0), P(w / 2, 0), P(w / 2, -hh), P(-w / 2, -hh)])),
             (B if wall == WH else WH, lambda L, P, s: L.poly([P(w / 2, 0), P(w / 2 + 6, -3), P(w / 2 + 6, -hh - 3), P(w / 2, -hh)])),
             (roof, lambda L, P, s: (L.poly([P(-w / 2 - 1, -hh), P(0, -hh - 9), P(w / 2 + 1, -hh)]), L.poly([P(0, -hh - 9), P(6, -hh - 12), P(w / 2 + 7, -hh - 3), P(w / 2 + 1, -hh)])))]
    if spire:
        parts += [(wall, lambda L, P, s: L.poly([P(-3, -hh - 4), P(3, -hh - 4), P(3, -hh - 16), P(-3, -hh - 16)])), (B, lambda L, P, s: L.poly([P(-4, -hh - 16), P(0, -hh - 32), P(4, -hh - 16)]))]
    sprite(parts, x, y, s)
    d = c.layer()
    d.rect(x - 1.5 * s, y - 5 * s, x + 1.5 * s, y)
    for wx in (-w / 2 + 2.5, w / 2 - 5):
        d.rect(x + wx * s, y - (hh - 2) * s, x + (wx + 2.5) * s, y - (hh - 5.5) * s)
    d.put(K)
    c.line([(x - (w / 2 + 1) * s, y - hh * s), (x + (w / 2 + 1) * s, y - hh * s)], K, 1)

def boat(x, y, s, sail=WH):
    parts = [(B, lambda L, P, s: [L.line([P(-20 + i * 4, 3 + k * 3 + (1.2 if (i + k) % 2 else 0)) for i in range(11)], 1.2 * s) for k in range(2)] and None),
             (R, lambda L, P, s: L.poly([P(-15, -5), P(15, -5), P(10, 2), P(-11, 2)])),
             (K, lambda L, P, s: (L.line([P(0, -5), P(0, -34)], 1.4 * s), L.line([P(15, -5), P(22, -9)], 1.2 * s))),
             (sail, lambda L, P, s: (L.poly(smooth([P(2, -8), P(13, -9), P(11, -20), P(2, -31)], n=4)), L.poly(smooth([P(-2, -8), P(-13, -8), P(-9, -18), P(-2, -27)], n=4)))),
             (Y, lambda L, P, s: L.poly([P(0, -34), P(-7, -32), P(0, -30)]))]
    sprite(parts, x, y, s)
    c.line([(x - 13 * s, y - 3 * s), (x + 13 * s, y - 3 * s)], WH, 1)

things = []
# the column marches over the knees
col = [(0.10 + 0.56 * t + 0.03 * math.sin(t * 6), 0.60 - 0.42 * t) for t in [i / 8 for i in range(9)]]
for (u, v) in col: things.append((Q(u, v), 0.62 + 0.55 * v, "soldier", {}))
things.append((Q(0.72, 0.2), 0.75, "soldier", {"face": -1}))        # the officer, facing them
# woods on the heights
for (u, v, k) in ((0.34, 0.26, 0), (0.28, 0.33, 1), (0.74, 0.34, 1), (0.82, 0.29, 0), (0.9, 0.42, 0), (0.06, 0.3, 1), (0.93, 0.74, 1), (0.06, 0.78, 0)):
    things.append((Q(u, v), 0.6 + 0.5 * v, "tree", {"kind": k}))
# the fleet in the valley between knees and feet
for (u, v, sl) in ((0.62, 0.585, WH), (0.80, 0.63, Y), (0.93, 0.575, WH)):
    things.append((Q(u, v), 0.62 + 0.5 * v, "boat", {"sail": sl}))
# the city on the plain
for (u, v, kw) in ((0.17, 0.86, dict(spire=True, w=13, hh=15)), (0.30, 0.84, dict(wall=Y, roof=R)), (0.08, 0.92, dict(wall=WH, roof=B, w=16)),
                   (0.25, 0.94, dict(wall=WH, roof=R, w=15, hh=14)), (0.38, 0.93, dict(wall=Y, roof=G, w=12)), (0.42, 0.85, dict(wall=WH, roof=R, w=11, hh=10))):
    things.append((Q(u, v), 0.75 + 0.55 * v, "house", kw))
for (u, v) in ((0.34, 0.98), (0.02, 0.86)): things.append((Q(u, v), 1.25, "tree", {"kind": 1}))
# reserve soldiers by the feet
for (u, v) in ((0.62, 0.9), (0.72, 0.93), (0.82, 0.9), (0.92, 0.94)): things.append((Q(u, v), 1.2, "soldier", {}))
things.sort(key=lambda t: t[0][1])
for (x, y), s, kind, kw in things:
    sh = c.layer().ellipse(x + 5 * s, y + 1.5 * s, 9 * s, 3 * s).mask()      # cast shadow, away from the window
    if kind != "boat": c.put(sh & quilt, K, checker(1))
    {"soldier": soldier, "tree": tree, "house": house, "boat": boat}[kind](x, y, s, **kw)
c.save("p1.png")
