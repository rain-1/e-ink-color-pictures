"""Midday: A Plate of Figures. After the margins of Hogarth's two plates for The Analysis
of Beauty (1753): the serpentine wire on its cone, his seven waving lines with No. 4
picked out, and twenty numbered specimens of where the line lives."""
import math, random
from kit import *
rnd = random.Random(1753)
im, d = canvas(Wh)
X0, Y0, CW, CH = 10, 10, 76, 580 / 7

def num(ox, oy, n):
    circ(d, ox + 9, oy + 9, 6, Y, K, 0.6); text(d, ox + 9, oy + 9.3, str(n), 7.5, K, bold=True)
def turned(cx, y0, prof, fill=Wh, shade=True):
    """A lathe-turned profile: prof = [(radius, y)...], mirrored about cx."""
    pts = [(cx - r, y0 + y) for r, y in prof] + [(cx + r, y0 + y) for r, y in prof][::-1]
    poly(d, pts, fill, K, 0.8)
    if shade:
        hatch(im, [(cx + r * 0.25, y0 + y) for r, y in prof] + [(cx + r, y0 + y) for r, y in prof][::-1], K, 1.6, 20, 0.35)
    for r, y in prof[1:-1:2]: line(d, [(cx - r, y0 + y), (cx + r, y0 + y)], K, 0.4)
def spiral(cx, cy, r0, r1, turns, n=60, ph=0, sx=1):
    return [(cx + sx * (r0 + (r1 - r0) * i / n) * math.cos(ph + turns * 2 * math.pi * i / n), cy + (r0 + (r1 - r0) * i / n) * math.sin(ph + turns * 2 * math.pi * i / n)) for i in range(n + 1)]

def f_stays(x, y):
    L = bez((x + 22, y + 14), (x + 30, y + 30), (x + 18, y + 44), (x + 26, y + 66)); Rr = [(2 * (x + 38) - px, py) for px, py in L]
    poly(d, L + Rr[::-1], Wh, K, 0.9)
    for i in range(1, 6):
        a = bez((x + 22 + i * 2.7, y + 14), (x + 30 + i * 1.6, y + 30), (x + 18 + i * 3.3, y + 44), (x + 26 + i * 2, y + 66), 12)
        line(d, a, K, 0.4); line(d, [(2 * (x + 38) - px, py) for px, py in a], K, 0.4)
    for j in range(8):
        yy = y + 18 + j * 6; line(d, [(x + 36, yy), (x + 40, yy + 3)], K, 0.5); line(d, [(x + 40, yy), (x + 36, yy + 3)], K, 0.5)
    line(d, L, R, 1.3)
def f_chairleg(x, y):
    a = bez((x + 30, y + 12), (x + 52, y + 26), (x + 22, y + 48), (x + 40, y + 66)); b = bez((x + 42, y + 12), (x + 58, y + 30), (x + 32, y + 50), (x + 47, y + 66))
    poly(d, a + b[::-1], Wh, K, 0.8); hatch(im, a[8:] + b[8:][::-1], K, 1.5, 70, 0.35)
    rect(d, x + 22, y + 8, x + 50, y + 13, K); poly(d, [(x + 38, y + 66), (x + 50, y + 66), (x + 53, y + 70), (x + 36, y + 70)], K)
    line(d, [((p[0] + q[0]) / 2, (p[1] + q[1]) / 2) for p, q in zip(a, b)], R, 1.2)
def f_candlestick(x, y):
    turned(x + 38, y + 10, [(3, 0), (3, 6), (7, 8), (7, 11), (3, 14), (2.5, 20), (6, 27), (7, 33), (4, 40), (3, 46), (6, 50), (14, 55), (16, 59), (16, 61)])
    rect(d, x + 36.5, y + 2, x + 39.5, y + 10, Wh, K, 0.5); line(d, [(x + 38, y + 2), (x + 38, y - 0.5)], K, 0.5)
def f_urn(x, y):
    turned(x + 38, y + 10, [(6, 0), (8, 2), (5, 5), (6, 9), (15, 18), (17, 26), (14, 36), (7, 44), (4, 47), (4, 50), (10, 54), (11, 58)])
    for sx in (-1, 1): line(d, bez((x + 38 + sx * 6, y + 20), (x + 38 + sx * 26, y + 14), (x + 38 + sx * 26, y + 38), (x + 38 + sx * 14, y + 44), 12), R if sx < 0 else K, 1.1)
def f_scroll(x, y):
    line(d, spiral(x + 36, y + 24, 2, 14, 2.1, 70, 1.6), K, 2.2); line(d, spiral(x + 36, y + 24, 2, 14, 2.1, 70, 1.6), Wh, 0.6)
    poly(d, [(x + 44, y + 36), (x + 52, y + 34), (x + 50, y + 68), (x + 43, y + 68)], Wh, K, 0.8)
    for j in range(2): circ(d, x + 42, y + 44 + j * 10, 2, K); circ(d, x + 53, y + 48 + j * 10, 2, K)
    f = scurve(x + 20, y + 40, 26, 4, 20); line(d, f, R, 1.5); circ(d, f[0][0] + 1.5, f[0][1], 1.8, R); circ(d, f[-1][0] - 1.5, f[-1][1], 1.8, R)
def f_shell(x, y):
    sp = spiral(x + 40, y + 38, 1, 26, 2.6, 110, 0.4)
    poly(d, sp[40:] + [(x + 40, y + 38)], Wh); line(d, sp, K, 1.0)
    for i in range(12, 110, 6):
        j = max(0, i - 42); 
        if i > 42: line(d, bez(sp[i], ((sp[i][0] + sp[j][0]) / 2 + 3, (sp[i][1] + sp[j][1]) / 2), ((sp[i][0] + sp[j][0]) / 2, (sp[i][1] + sp[j][1]) / 2 + 3), sp[j], 6), K if i % 4 else R, 0.5)
def f_leaf(x, y):
    mid = bez((x + 18, y + 66), (x + 46, y + 54), (x + 26, y + 30), (x + 56, y + 8), 24)
    Lf = [(px - 14 * math.sin(math.pi * i / 24) * 0.8, py - 9 * math.sin(math.pi * i / 24)) for i, (px, py) in enumerate(mid)]; Rf = [(px + 14 * math.sin(math.pi * i / 24), py + 8 * math.sin(math.pi * i / 24)) for i, (px, py) in enumerate(mid)]
    poly(d, Lf + Rf[::-1], G, K, 0.8)
    for i in range(3, 22, 2): line(d, [Lf[i], mid[max(0, i - 2)], Rf[i]], K, 0.4)
    line(d, mid, R, 1.2)
def f_horn(x, y):
    a = bez((x + 12, y + 62), (x + 20, y + 30), (x + 50, y + 52), (x + 60, y + 16), 20); b = bez((x + 14, y + 64), (x + 34, y + 44), (x + 56, y + 62), (x + 44, y + 12), 20)
    poly(d, a + b[::-1], Y, K, 0.8)
    for i in range(2, 20, 2): line(d, [a[i], b[i]], K, 0.5)
    ell(d, x + 52, y + 14, 9, 4.5, Wh, K, 0.8)
    for (fx, fy, c) in ((48, 9, R), (55, 8, G), (51, 5, R), (58, 12, Y), (45, 13, G)): circ(d, x + fx, y + fy, 3, c, K, 0.5)
def f_flame(x, y):
    rect(d, x + 34, y + 50, x + 42, y + 70, Wh, K, 0.7); line(d, [(x + 38, y + 50), (x + 38, y + 44)], K, 0.7)
    a = bez((x + 38, y + 48), (x + 24, y + 36), (x + 44, y + 26), (x + 36, y + 8), 16); b = bez((x + 38, y + 48), (x + 52, y + 38), (x + 46, y + 24), (x + 36, y + 8), 16)
    poly(d, a + b[::-1], Y, K, 0.8); line(d, bez((x + 38, y + 46), (x + 34, y + 38), (x + 42, y + 32), (x + 38, y + 22), 10), R, 1.1)
    for i in range(10): 
        an = -math.pi * (0.1 + 0.8 * i / 9); line(d, [(x + 38 + 20 * math.cos(an), y + 30 + 24 * math.sin(an)), (x + 38 + 25 * math.cos(an), y + 30 + 30 * math.sin(an))], K, 0.4)
def f_column(x, y):
    rect(d, x + 24, y + 6, x + 52, y + 11, Wh, K, 0.7); rect(d, x + 24, y + 65, x + 52, y + 70, Wh, K, 0.7)
    L = [(x + 31 + 3.5 * math.sin(i / 3.2), y + 11 + i) for i in range(55)]; Rr = [(px + 14, py) for px, py in L]
    poly(d, L + Rr[::-1], Wh, K, 0.8)
    for k in range(-1, 6):
        s0 = [(x + 31 + 3.5 * math.sin((k * 10 + t) / 3.2) + 14 * t / 10, y + 11 + k * 10 + t * 1.4) for t in range(11)]
        s0 = [p for p in s0 if y + 11 <= p[1] <= y + 65]
        if len(s0) > 1: line(d, s0, R if k == 2 else K, 0.9)
    hatch(im, [(px + 9, py) for px, py in L] + Rr[::-1], K, 1.6, 15, 0.35)
def f_swan(x, y):
    ell(d, x + 34, y + 54, 18, 9, Wh, K, 0.8); poly(d, [(x + 16, y + 52), (x + 8, y + 44), (x + 22, y + 48)], Wh, K, 0.7)
    nk = bez((x + 46, y + 50), (x + 62, y + 40), (x + 40, y + 28), (x + 54, y + 16), 16)
    line(d, nk, K, 5.5); line(d, nk, Wh, 3.8); circ(d, x + 55, y + 15, 4, Wh, K, 0.7); poly(d, [(x + 58, y + 14), (x + 66, y + 18), (x + 58, y + 18)], R, K, 0.4); circ(d, x + 55.5, y + 14, 0.7, K)
    for j in range(3): line(d, bez((x + 22 + j * 3, y + 50 + j * 2), (x + 30, y + 46 + j * 3), (x + 40, y + 56 + j), (x + 46, y + 54 + j * 2), 8), K, 0.4)
    line(d, nk, R, 0.8)
    for j in range(3): line(d, [(x + 8 + j * 6, y + 66 + j % 2 * 2), (x + 30 + j * 14, y + 66 + j % 2 * 2)], B, 0.6)
def f_wig(x, y):
    poly(d, [(x + 22, y + 30), (x + 26, y + 10), (x + 50, y + 10), (x + 54, y + 30)], Wh, K, 0.8)
    for r in range(4):
        for c in range(4 + r % 2):
            cx_, cy_ = x + 18 + c * 12 - (r % 2) * 6, y + 26 + r * 11
            circ(d, cx_, cy_, 6, Wh, K, 0.5); line(d, spiral(cx_, cy_, 0.5, 5.5, 1.6, 22, r + c), R if (r, c) == (1, 2) else K, 0.7)
    for j in range(5): line(d, bez((x + 28 + j * 5, y + 11), (x + 26 + j * 5, y + 16), (x + 30 + j * 5, y + 18), (x + 28 + j * 5, y + 22), 6), K, 0.4)
def f_ribbon(x, y):
    top = [(x + 8 + i * 2, y + 30 + 12 * math.sin(i / 4.6)) for i in range(31)]
    for i in range(30):
        c = R if math.cos(i / 4.6) > 0 else Wh
        poly(d, [top[i], top[i + 1], (top[i + 1][0], top[i + 1][1] + 14), (top[i][0], top[i][1] + 14)], c)
    line(d, top, K, 0.8); line(d, [(px, py + 14) for px, py in top], K, 0.8)
    poly(d, [top[0], (top[0][0] + 5, top[0][1] + 7), (top[0][0], top[0][1] + 14)], Wh, K, 0.6); poly(d, [top[-1], (top[-1][0] - 5, top[-1][1] + 7), (top[-1][0], top[-1][1] + 14)], Wh, K, 0.6)
    for i in range(2, 30, 2): line(d, [(top[i][0], top[i][1] + 3), (top[i][0], top[i][1] + 11)], K, 0.3)
def f_pug(x, y):
    ell(d, x + 34, y + 50, 16, 11, Y, K, 0.8); circ(d, x + 52, y + 36, 9, Y, K, 0.8); ell(d, x + 57, y + 39, 5, 4.5, K)
    poly(d, [(x + 44, y + 32), (x + 44, y + 24), (x + 50, y + 28)], K); poly(d, [(x + 56, y + 28), (x + 60, y + 23), (x + 61, y + 31)], K)
    circ(d, x + 50, y + 34, 1.2, K); circ(d, x + 56, y + 33.5, 1.2, K)
    for lx in (24, 30, 40, 46): rect(d, x + lx, y + 58, x + lx + 4, y + 68, Y, K, 0.6)
    line(d, spiral(x + 16, y + 40, 1, 6.5, 1.4, 24, 1.2), R, 1.6)
    for j in range(3): line(d, bez((x + 40 + j * 2, y + 42 + j * 3), (x + 44, y + 44 + j * 3), (x + 44, y + 48 + j * 3), (x + 48, y + 48 + j * 3), 5), K, 0.4)
def f_tulip(x, y):
    st = bez((x + 34, y + 70), (x + 48, y + 54), (x + 26, y + 40), (x + 40, y + 24), 16); line(d, st, G, 1.6)
    for sx, yy in ((-1, 56), (1, 46)):
        lf = bez(st[5 if sx < 0 else 9], (x + 38 + sx * 20, y + yy), (x + 38 + sx * 22, y + yy - 14), (x + 38 + sx * 26, y + yy - 22), 10)
        poly(d, lf + bez((x + 38 + sx * 26, y + yy - 22), (x + 38 + sx * 12, y + yy - 12), (x + 38 + sx * 12, y + yy - 2), st[5 if sx < 0 else 9], 10), G, K, 0.5)
    for a, c in ((-0.5, R), (0.5, R), (0, Y)):
        poly(d, bez((x + 40, y + 26), (x + 40 + a * 22 - 8, y + 18), (x + 40 + a * 26 - 4, y + 8), (x + 40 + a * 16, y + 4), 8) + bez((x + 40 + a * 16, y + 4), (x + 40 + a * 26 + 4, y + 8), (x + 40 + a * 22 + 8, y + 18), (x + 40, y + 26), 8), c, K, 0.6)
def f_waves(x, y):
    for r in range(5):
        yy = y + 16 + r * 12
        for c in range(-1, 4):
            cx_ = x + 12 + c * 20 + (r % 2) * 10
            pts = [(px, py) for px, py in bez((cx_ - 10, yy + 6), (cx_ - 2, yy + 6), (cx_ + 2, yy - 6), (cx_ + 8, yy - 2), 8) + spiral(cx_ + 6, yy + 1, 3, 0.5, 0.8, 8, -1.2) if x + 4 <= px <= x + 72]
            if len(pts) > 1: line(d, pts, B if r != 2 else R, 1.0)
def f_snake(x, y):
    pts = [(x + 10 + i * 1.1, y + 40 + (18 - i * 0.2) * math.sin(i / 5.2)) for i in range(52)]
    for i in range(len(pts) - 1): line(d, pts[i:i + 2], K, 5.5 - i * 0.06)
    for i in range(len(pts) - 1): line(d, pts[i:i + 2], G if (i // 3) % 2 else Y, 3.6 - i * 0.05)
    hx, hy = pts[0]; ell(d, hx, hy - 1, 4.5, 3.4, G, K, 0.7); circ(d, hx - 1, hy - 2, 0.8, K); line(d, [(hx - 4, hy), (hx - 8, hy + 2), (hx - 10, hy + 1)], R, 0.6); line(d, [(hx - 8, hy + 2), (hx - 10, hy + 4)], R, 0.6)
def f_dance(x, y):
    for k, c in ((0, K), (1, R)):
        pts = [(x + 38 + (1 - 2 * k) * 20 * math.sin(i / 40 * 2 * math.pi), y + 8 + i * 1.5) for i in range(41)]
        for i in range(0, 40, 2): line(d, pts[i:i + 2], c, 0.9)
        for i in (4, 14, 24, 34):
            px, py = pts[i]; ell(d, px + 2.5, py, 1.5, 2.6, c); ell(d, px - 2.5, py + 4, 1.5, 2.6, c)
def f_teapot(x, y):
    ell(d, x + 36, y + 46, 17, 15, B, K, 0.8); hatch(im, [(x + 36 + 17 * math.cos(a / 10 * math.pi) * (1 if math.cos(a / 10 * math.pi) > 0.2 else 0.2), y + 46 + 15 * math.sin(a / 10 * math.pi)) for a in range(20)], Wh, 1.6, 30, 0.4)
    sp = bez((x + 50, y + 52), (x + 64, y + 50), (x + 56, y + 34), (x + 68, y + 30), 12); line(d, sp, K, 5); line(d, sp, B, 3.4); line(d, sp, R, 0.8)
    line(d, bez((x + 20, y + 38), (x + 6, y + 36), (x + 6, y + 56), (x + 21, y + 54), 12), K, 2.2)
    ell(d, x + 36, y + 31, 9, 2.6, Wh, K, 0.7); circ(d, x + 36, y + 27, 2.5, Wh, K, 0.7); rect(d, x + 26, y + 60, x + 46, y + 63, K)
    for k in range(2): line(d, scurve(x + 68 + k * 3, y + 8, 18, 2, 10), K, 0.5)
def f_river(x, y):
    Lr = [(x + 38 + 16 * math.sin(i / 9) - 2 - i * 0.07, y + 8 + i) for i in range(62)]; Rr = [(px + 5 + i * 0.14, py) for i, (px, py) in enumerate(Lr)]
    poly(d, Lr + Rr[::-1], B, K, 0.6)
    for i in range(4, 60, 5):
        for sx, pts in ((-1, Lr), (1, Rr)):
            px, py = pts[i]; px += sx * 6
            line(d, [(px, py), (px, py - 4)], K, 0.5); circ(d, px, py - 5.5, 2.2, G if i % 2 else Y, K, 0.4)
    rect(d, Lr[34][0] - 3, Lr[34][1] - 2, Rr[34][0] + 3, Lr[34][1] + 1.5, Wh, K, 0.5)
    line(d, [((p[0] + q[0]) / 2, p[1]) for p, q in zip(Lr, Rr)], R, 0.7)

figs = [f_stays, f_chairleg, f_candlestick, f_urn, f_scroll, f_shell, f_leaf, f_horn, f_flame, f_column,
        f_swan, f_wig, f_ribbon, f_pug, f_tulip, f_waves, f_snake, f_dance, f_teapot, f_river]
cells = [(c, 0) for c in range(5)] + [(4, r) for r in range(1, 6)] + [(c, 6) for c in range(4, -1, -1)] + [(0, r) for r in range(5, 0, -1)]
for n, ((c, r), f) in enumerate(zip(cells, figs), 1):
    ox, oy = X0 + c * CW, Y0 + r * CH
    f(ox, oy + 2)
    rect(d, ox, oy, ox + CW, oy + CH, None, K, 0.8); num(ox, oy, n)

# ---------- the centre plate
cx0, cy0, cx1, cy1 = X0 + CW, Y0 + CH, X0 + 4 * CW, Y0 + 6 * CH
rect(d, cx0 + 4, cy0 + 4, cx1 - 4, cy1 - 4, Y, K, 0.6)
text(d, 200, cy0 + 20, "THE LINE", 21, K, bold=True); text(d, 200, cy0 + 38, "of", 12, K, italic=True); text(d, 200, cy0 + 56, "BEAUTY", 21, R, bold=True)
line(d, [(120, cy0 + 70), (280, cy0 + 70)], K, 0.6); line(d, scurve(200, cy0 + 66, 8, 2.5, 10), K, 0.8)
# the cone and its wire
AX, AY, BYc, BRx, BRy = 200, cy0 + 82, cy0 + 236, 70, 14
cone = [(AX, AY)] + [(AX + BRx * math.cos(a / 30 * math.pi), BYc + BRy * math.sin(a / 30 * math.pi)) for a in range(0, 31)]
poly(d, cone, Wh)
for i in range(1, 40):                                   # engraved shading, denser to the right
    t = i / 40; bx = AX - BRx + 2 * BRx * t; by = BYc + BRy * math.sqrt(max(0, 1 - (2 * t - 1) ** 2))
    if t > 0.42 or i % 4 == 0: line(d, [(AX, AY), (bx, by)], K, 0.35 + 0.5 * max(0, t - 0.45))
ell(d, AX, BYc, BRx, BRy, None, K, 0.9); line(d, [(AX - BRx, BYc), (AX, AY), (AX + BRx, BYc)], K, 1.0)
hatch(im, [(AX + 20 + 76 * math.cos(a / 12 * math.pi), BYc + 6 + 9 * math.sin(a / 12 * math.pi)) for a in range(24)], K, 2.0, 20, 0.4)   # cast shadow
poly(d, [(AX + BRx * math.cos(a / 30 * math.pi), BYc + BRy * math.sin(a / 30 * math.pi)) for a in range(0, 31)], Wh)
ell(d, AX, BYc, BRx, BRy, None, K, 0.9)
turnsN = 3.25; prev = None
for i in range(241):
    t = i / 240; a = t * turnsN * 2 * math.pi + 2.6; rr = 1 - t * 0.96
    p = (AX + BRx * rr * math.cos(a), AY + (BYc - AY) * rr + BRy * rr * math.sin(a))
    front = math.sin(a) > -0.05
    if prev:
        if front: line(d, [prev, p], K, 3.6); 
        elif i % 4 < 2: line(d, [prev, p], K, 0.6)
    prev = p
prev = None
for i in range(241):
    t = i / 240; a = t * turnsN * 2 * math.pi + 2.6; rr = 1 - t * 0.96
    p = (AX + BRx * rr * math.cos(a), AY + (BYc - AY) * rr + BRy * rr * math.sin(a))
    if prev and math.sin(a) > -0.05: line(d, [prev, p], R, 2.2)
    prev = p
text(d, 200, BYc + 28, "the Serpentine Line, or Line of Grace,", 8.5, K, italic=True); text(d, 200, BYc + 38, "as a wire twisted round a Cone", 8.5, K, italic=True)
# the seven waving lines
ly = BYc + 50
for i in range(7):
    lx = 110 + i * 30; amp = 0.6 + i * 2.1
    pts = [(lx + amp * math.sin(2 * math.pi * k / 30) * (1 + 0.04 * i), ly + k * 2.1) for k in range(31)]
    line(d, pts, R if i == 3 else K, 2.4 if i == 3 else 1.1)
    text(d, lx, ly + 72, str(i + 1), 10, R if i == 3 else K, bold=(i == 3))
rect(d, 186, ly - 5, 214, ly + 80, None, R, 0.7)
text(d, 200, cy1 - 27, "No. 4 — neither mean nor bulging", 8.2, K, italic=True)
text(d, 200, cy1 - 14, "W. HOGARTH  b. 10 Nov. 1697", 7.6, K)
rect(d, X0, Y0, X0 + 5 * CW, Y0 + 7 * CH, None, K, 1.6); rect(d, X0 - 4, Y0 - 4, X0 + 5 * CW + 4, Y0 + 7 * CH + 4, None, K, 0.5)
save(im)
