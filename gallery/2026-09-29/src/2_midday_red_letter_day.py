"""Midday — 'A Red-Letter Day'. A Book of Hours calendar leaf for late September.
Feasts were written in red; Michaelmas is the reddest. Miniature of the goose harvest
on a diapered ground, acanthus borders, an illuminated KL, and a dragon in the margin."""
import math, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from ink import *

cv = Canvas(bg=WH, seed=2909)
rng = cv.rng
VELLUM = WH
cv.rect(0, 0, W, H, VELLUM)

# ---------- border: a gold-edged frame with acanthus vine ----------
def frame(x0, y0, x1, y1, col, w=1):
    cv.line([(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)], col, w, joint=False)

frame(14, 14, W - 14, H - 14, K, 1.2)
frame(18, 18, W - 18, H - 18, R, 0.8)

def vine(path, phase=0):
    cv.line(path, K, 1.3)
    n = len(path)
    for i in range(4, n - 4, 9):
        x, y = path[i]
        x2, y2 = path[i + 1]
        dx, dy = x2 - x, y2 - y
        l = math.hypot(dx, dy) or 1
        nx, ny = -dy / l, dx / l
        side = 1 if ((i // 9) + phase) % 2 else -1
        # acanthus leaf: curling lobed blade
        col = [B, R, G, B, R][(i // 9) % 5]
        pts = []
        for k in range(13):
            t = k / 12
            ang = t * 2.4
            rr = 15 * (1 - 0.55 * t)
            px = x + side * nx * rr * math.sin(ang) + dx / l * rr * (1 - math.cos(ang)) * 0.9
            py = y + side * ny * rr * math.sin(ang) + dy / l * rr * (1 - math.cos(ang)) * 0.9
            pts.append((px, py))
        inner = [(x + (px - x) * 0.45, y + (py - y) * 0.45) for px, py in pts]
        cv.poly(pts + inner[::-1], col)
        cv.line(pts, K, 0.7)
        cv.line(inner, mix(col, WH, 0.5), 0.7)
        # gold bezant with black outline
        bx, by = x - side * nx * 6, y - side * ny * 6
        cv.circle(bx, by, 3.0, Y, outline=K, width=0.6)
        # hairline tendril with tiny leaves
        tx, ty = x - side * nx * 3 + dx / l * 5, y - side * ny * 3 + dy / l * 5
        tp = [(tx + side * nx * 0 + dx / l * j * 1.4 - side * nx * j * 0.9 * math.sin(j * 0.5),
               ty + dy / l * j * 1.4 - side * ny * j * 0.9 * math.sin(j * 0.5)) for j in range(10)]
        cv.line(tp, K, 0.6)
        cv.circle(tp[-1][0], tp[-1][1], 1.5, G)

def wave(x0, y0, x1, y1, amp=6, per=34):
    L = math.hypot(x1 - x0, y1 - y0)
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    pts = []
    for j in range(int(L / 1.5) + 1):
        s = j * 1.5
        o = amp * math.sin(s / per * math.tau)
        pts.append((x0 + ux * s - uy * o, y0 + uy * s + ux * o))
    return pts

# vines run in the outer margin between frame lines and the text block
vine(wave(30, 30, 30, H - 30), 0)
vine(wave(W - 30, 30, W - 30, H - 30), 1)
vine(wave(44, 30, W - 44, 30, amp=5), 0)

# ---------- miniature ----------
mx0, mx1, my0, my1 = 52, W - 52, 48, 292
arch = [(mx0, my1), (mx0, my0 + 50)]
for k in range(21):
    t = k / 20
    a = math.pi + t * math.pi
    arch.append(((mx0 + mx1) / 2 + (mx1 - mx0) / 2 * math.cos(a), my0 + 50 + 50 * math.sin(a)))
arch += [(mx1, my0 + 50), (mx1, my1)]
cv.poly(arch, B)
# diaper: lozenges alternating blue/red with gold dots and white crosslets
ms = Image.new("L", (W * S, H * S), 0)
ImageDraw.Draw(ms).polygon([(x * S, y * S) for x, y in arch], fill=1)
msk = np.asarray(ms).astype(bool)
X, Yy = cv.grid()
u = (X + Yy) / 18.0; v = (X - Yy) / 18.0
cell = (np.floor(u) + np.floor(v)) % 2 == 0
cv.mask(msk & cell & (Yy < 190), R)
fu, fv = u - np.floor(u), v - np.floor(v)
edge = (np.minimum(fu, 1 - fu) < 0.06) | (np.minimum(fv, 1 - fv) < 0.06)
cv.mask(msk & edge & (Yy < 190), Y)
dot = ((fu - 0.5) ** 2 + (fv - 0.5) ** 2) < 0.018
cv.mask(msk & dot & (Yy < 190), WH)

# far hill with church and trees
hill = [(mx0, 190)] + [(x, 180 - 18 * math.sin((x - mx0) / (mx1 - mx0) * math.pi) + 4 * math.sin(x * 0.2))
                        for x in range(mx0, mx1 + 1, 3)] + [(mx1, 200), (mx1, my1), (mx0, my1)]
cv.poly(hill, G)
for x in range(mx0 + 4, mx1, 7):
    for y in range(172, 206, 6):
        if rng.random() < 0.5:
            cv.line([(x + rng.uniform(-2, 2), y), (x + 3, y - 2)], mix(G, K, 0.5), 0.7)
# church
cx, cy = 226, 172
cv.rect(cx, cy - 16, cx + 34, cy + 6, WH)
cv.poly([(cx - 3, cy - 16), (cx + 37, cy - 16), (cx + 30, cy - 28), (cx + 4, cy - 28)], R)
cv.rect(cx - 12, cy - 38, cx, cy + 6, WH)
cv.poly([(cx - 14, cy - 38), (cx + 2, cy - 38), (cx - 6, cy - 60)], B)
cv.line([(cx - 6, cy - 60), (cx - 6, cy - 68)], K, 0.8)
cv.line([(cx - 9, cy - 65), (cx - 3, cy - 65)], K, 0.8)
for k in range(4):
    cv.rect(cx + 4 + k * 8, cy - 10, cx + 7 + k * 8, cy - 3, K)
cv.rect(cx - 8, cy - 30, cx - 4, cy - 23, K)
frame(cx, cy - 16, cx + 34, cy + 6, K, 0.6); frame(cx - 12, cy - 38, cx, cy + 6, K, 0.6)
# trees: lollipop orchard
for tx, ty, r in [(82, 182, 14), (108, 176, 11), (292, 180, 13), (318, 186, 10)]:
    cv.rect(tx - 1.5, ty, tx + 1.5, ty + 20, mix(R, K, 0.5))
    cv.circle(tx, ty - 2, r, mix(G, K, 0.4), outline=K, width=0.6)
    for k in range(9):
        a = k * 2.4; d = r * 0.6 * math.sqrt(k / 9)
        cv.circle(tx + d * math.cos(a), ty - 2 + d * math.sin(a), 2.3, R if k % 3 == 0 else mix(G, Y, 0.4))

# stubble field
field = [(mx0, 214)] + [(x, 212 + 3 * math.sin(x * 0.05)) for x in range(mx0, mx1 + 1, 4)] + [(mx1, my1), (mx0, my1)]
cv.poly(field, Y)
for k in range(28):
    x0 = mx0 + k * (mx1 - mx0) / 27
    cv.line([((mx0 + mx1) / 2 + (x0 - (mx0 + mx1) / 2) * 0.3, 214), (max(mx0, min(mx1, x0 + (x0 - 200) * 0.6)), my1)], mix(Y, R, 0.4), 0.8)
for j in range(200):
    x = rng.uniform(mx0 + 2, mx1 - 2); y = rng.uniform(218, my1 - 2)
    cv.line([(x, y), (x + rng.uniform(-1, 1), y - 3 - (y - 214) * 0.03)], mix(Y, K, 0.5), 0.6)
# sheaves (stooks)
for sx, sy, s in [(84, 234, 0.9), (318, 238, 1.0)]:
    cv.poly([(sx - 10 * s, sy + 12 * s), (sx - 3 * s, sy - 16 * s), (sx + 3 * s, sy - 16 * s), (sx + 10 * s, sy + 12 * s)], mix(Y, R, 0.25), outline=K, width=0.6)
    for k in range(-4, 5):
        cv.line([(sx + k * 0.6 * s, sy - 16 * s), (sx + k * 2.2 * s, sy + 12 * s)], K, 0.4)
    cv.rect(sx - 6 * s, sy - 3 * s, sx + 6 * s, sy - 1 * s, R)

# the goose-girl
gx, gy = 148, 258
cv.poly([(gx - 13, gy + 26), (gx - 8, gy - 6), (gx + 8, gy - 6), (gx + 14, gy + 26)], B, outline=K, width=0.7)
for k in range(4):
    cv.line([(gx - 6 + k * 4, gy - 4), (gx - 10 + k * 7, gy + 25)], mix(B, K, 0.5), 0.6)
cv.poly([(gx - 6, gy - 2), (gx + 6, gy - 2), (gx + 8, gy + 20), (gx - 7, gy + 20)], WH, outline=K, width=0.6)  # apron
cv.poly([(gx - 8, gy - 6), (gx + 8, gy - 6), (gx + 6, gy - 20), (gx - 6, gy - 20)], R, outline=K, width=0.7)   # bodice
cv.circle(gx, gy - 26, 6.5, mix(WH, R, 0.2), outline=K, width=0.6)
cv.poly([(gx - 8, gy - 26), (gx - 6, gy - 34), (gx + 6, gy - 34), (gx + 8, gy - 26), (gx + 7, gy - 16), (gx - 7, gy - 16), (gx - 6, gy - 24), (gx - 5, gy - 30), (gx + 5, gy - 30), (gx + 6, gy - 24)], WH, outline=K, width=0.6)
cv.circle(gx + 2, gy - 27, 0.8, K)
cv.line([(gx + 6, gy - 14), (gx + 16, gy - 4)], mix(WH, R, 0.2), 2)  # arm
cv.line([(gx + 16, gy - 4), (gx + 46, gy - 38)], mix(R, K, 0.4), 1.2)  # switch
cv.line([(gx - 6, gy - 14), (gx - 10, gy + 2)], R, 2)
cv.rect(gx - 8, gy + 26, gx - 3, gy + 29, K); cv.rect(gx + 4, gy + 26, gx + 9, gy + 29, K)

def goose(x, y, s, flip=1, pose=0):
    cv.ellipse(x, y, 10 * s, 6 * s, WH, outline=K, width=0.7)
    cv.poly([(x - 9 * s * flip, y - 2 * s), (x - 15 * s * flip, y - 5 * s), (x - 8 * s * flip, y + 2 * s)], WH, outline=K, width=0.6)
    for k in range(3):
        cv.line([(x - 5 * s * flip + k * 3 * s * flip, y - 2 * s), (x - 7 * s * flip + k * 3 * s * flip, y + 3 * s)], K, 0.5)
    if pose == 0:
        nk = [(x + 7 * s * flip, y - 3 * s), (x + 11 * s * flip, y - 10 * s), (x + 12 * s * flip, y - 17 * s)]
    else:
        nk = [(x + 7 * s * flip, y - 2 * s), (x + 13 * s * flip, y + 1 * s), (x + 16 * s * flip, y + 6 * s)]
    cv.line(nk, WH, 3.4 * s)
    cv.line([(p[0] - 1.7 * s * flip, p[1]) for p in nk], K, 0.6)
    hx, hy = nk[-1]
    cv.circle(hx, hy, 3 * s, WH, outline=K, width=0.6)
    cv.poly([(hx + 2 * s * flip, hy - 1 * s), (hx + 8 * s * flip, hy + 0.5 * s), (hx + 2 * s * flip, hy + 1.8 * s)], R, outline=K, width=0.4)
    cv.circle(hx + 0.8 * s * flip, hy - 0.8 * s, 0.7, K)
    for dx in (-2, 2):
        cv.line([(x + dx * s, y + 5 * s), (x + dx * s, y + 11 * s)], R, 1.0)
        cv.line([(x + dx * s - 2, y + 11 * s), (x + dx * s + 2.5, y + 11 * s)], R, 1.0)
for (x, y, s, f, p) in [(198, 236, 0.9, 1, 0), (230, 250, 1.0, 1, 1), (262, 238, 0.85, 1, 0),
                        (212, 270, 1.1, 1, 0), (252, 272, 1.05, -1, 1), (290, 262, 0.95, 1, 0), (188, 282, 0.9, 1, 1)]:
    goose(x, y, s, f, p)

# miniature frame: gold with black keylines
cv.line(arch + [arch[0]], Y, 3.5)
cv.line(arch + [arch[0]], K, 0.6)
out = [(mx0 - 3, my1 + 3), (mx0 - 3, my0 + 50)] + [((mx0 + mx1) / 2 + ((mx1 - mx0) / 2 + 3) * math.cos(math.pi + k / 20 * math.pi), my0 + 50 + 53 * math.sin(math.pi + k / 20 * math.pi)) for k in range(21)] + [(mx1 + 3, my0 + 50), (mx1 + 3, my1 + 3)]
cv.line(out + [out[0]], K, 0.7)

# ---------- calendar text ----------
tx0 = 56
cv.rect(tx0, 304, tx0 + 58, 350, B)
frame(tx0, 304, tx0 + 58, 350, K, 0.8)
for k in range(14):  # white filigree in the blue field
    a = k * 0.45
    cv.circle(tx0 + 29 + 22 * math.cos(a), 327 + 18 * math.sin(a), 1.0, WH)
cv.text(tx0 + 29, 328, "KL", Y, font(34, "serifb"), anchor="mm")
cv.text(tx0 + 29, 328, "KL", None, font(34, "serifb"), anchor="mm") if False else None
cv.text(tx0 + 68, 314, "September", R, font(18, "serifb"))
cv.text(tx0 + 68, 334, "hath xxx daies. The moone xxx.", K, font(11, "serifi"))

days = [("xxiii", "d", "Tecle virginis", K), ("xxiiii", "e", "Conceptio Johannis", B),
        ("xxv", "f", "Firmini episcopi", K), ("xxvi", "g", "Cipriani & Justine", K),
        ("xxvii", "A", "Cosme & Damiani", B), ("xxviii", "b", "Wenceslai regis", K),
        ("xxix", "c", "Michaelis archangeli", R), ("xxx", "d", "Jeronimi presbiteri", K)]
y = 364
for n, (num, dom, saint, col) in enumerate(days):
    big = col == R
    f = font(15 if big else 12, "serifb" if big else "serif")
    cv.text(tx0, y, num, R if big else K, font(12 if not big else 14, "serif"))
    cv.text(tx0 + 44, y, dom, R if dom == "A" or big else K, font(12, "serifb"))
    cv.text(tx0 + 62, y - (2 if big else 0), saint, col, f)
    if big:
        # gold star and a little scroll flourish
        cv.line([(tx0 + 62, y + 18), (W - 60, y + 18)], R, 0.8)
        sx, sy = W - 66, y + 7
        pts = []
        for k in range(10):
            a = -math.pi / 2 + k * math.pi / 5
            rr = 7 if k % 2 == 0 else 3
            pts.append((sx + rr * math.cos(a), sy + rr * math.sin(a)))
        cv.poly(pts, Y, outline=K, width=0.5)
    y += 20 if not big else 24
cv.line([(tx0, 358), (W - 56, 358)], R, 0.6)
cv.line([(tx0 + 38, 358), (tx0 + 38, y - 4)], R, 0.6)
cv.line([(tx0 + 56, 358), (tx0 + 56, y - 4)], R, 0.6)

# ---------- bas-de-page: Michael's little dragon, speared, in the margin ----------
dx, dy = 170, 566
body = [(dx - 50, dy + 4)]
for k in range(30):
    t = k / 29
    body.append((dx - 50 + t * 90, dy + 4 - 10 * math.sin(t * math.pi * 1.4)))
L, Rr = offset(body, lambda t: 2 + 9 * math.sin(t * math.pi) ** 0.7)
cv.poly(L + Rr[::-1], G, outline=K, width=0.7)
for i in range(3, 28, 3):  # belly scales
    cv.circle(Rr[i][0], Rr[i][1] - 1, 1.6, Y, outline=K, width=0.4)
for i in range(2, 28, 2):  # spines
    x, y = L[i]
    cv.poly([(x - 2, y), (x + 2, y), (x, y - 4)], R)
hx, hy = body[-1]
cv.ellipse(hx + 6, hy - 2, 8, 5, G, outline=K, width=0.7)
cv.poly([(hx + 12, hy - 3), (hx + 20, hy - 1), (hx + 12, hy + 1)], R)  # tongue/flame
cv.poly([(hx + 20, hy - 1), (hx + 28, hy - 5), (hx + 25, hy), (hx + 30, hy + 3), (hx + 20, hy + 1)], mix(R, Y, 0.5))
cv.circle(hx + 7, hy - 4, 1.3, Y)
# wing
wx, wy = dx - 2, dy - 6
wing = [(wx, wy), (wx - 16, wy - 16), (wx - 5, wy - 13), (wx + 1, wy - 20), (wx + 8, wy - 13), (wx + 20, wy - 17), (wx + 14, wy - 3)]
cv.poly(wing, R, outline=K, width=0.7)
for k in (1, 3, 5):
    cv.line([(wx + 4, wy - 2), wing[k]], K, 0.6)
# tail curl
tail = [(dx - 50 + 14 * math.cos(a) - 14, dy + 4 - 14 * math.sin(a)) for a in np.linspace(0, 4.4, 30)]
cv.line(tail, G, 3); cv.line(tail, K, 0.5)
# the spear, coming in from the margin, gold-tipped
cv.line([(W - 44, 540), (hx + 12, hy - 18)], mix(R, K, 0.5), 2.0)
cv.poly([(hx + 2, hy - 8), (hx + 12, hy - 18), (hx + 9, hy - 12), (hx + 15, hy - 11)], Y, outline=K, width=0.5)
# little pennant
cv.poly([(W - 52, 543), (W - 70, 536), (W - 64, 550)], R, outline=K, width=0.5)

cv.finish()
