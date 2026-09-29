"""Night — 'Devil's Spit Night'. The legend: cast out of heaven on Michaelmas, Lucifer fell
into a bramble and cursed it, and no one picks blackberries after. A falling star with a
trail of shed feathers, tonight's waning gibbous moon rising, the hedge smouldering."""
import math, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from ink import *

cv = Canvas(bg=K, seed=666)
rng = cv.rng
X, Yg = cv.grid()

HOR = 468
# faint glow towards the horizon: screens of blue
for y0 in range(330, HOR + 2, 6):
    t = ((y0 - 330) / (HOR - 330)) ** 2
    cv.rect(0, y0, W, y0 + 6, mix(K, B, 0.06 + 0.4 * t))

# ---------- Milky Way: a band of dense faint stars ----------
nz = vnoise((H * S, W * S), 60 * S, cv.np, octaves=4)
# band from top-left to right-middle
dist = np.abs((Yg - 60) - (X * 0.75)) / 90.0
band = np.clip(1.0 - dist, 0, 1) * (0.4 + 0.9 * nz)
cv.mask((band > 0.55) & (Yg < HOR - 10), mix(K, B, 0.125))
for py in range(0, HOR - 10):
    for px in range(0, W):
        b = band[py * S + 1, px * S + 1]
        if b > 0.2 and rng.random() < b * 0.07:
            cv.rect(px, py, px + 1, py + 1, WH if rng.random() < 0.7 else mix(K, WH, 0.5))
# dark rifts


# ---------- field stars ----------
for _ in range(420):
    x = rng.uniform(0, W); y = rng.uniform(0, HOR - 20)
    m = rng.random()
    if m < 0.75:
        cv.rect(x, y, x + 1, y + 1, WH)
    elif m < 0.95:
        cv.circle(x, y, 1.0, WH)
    else:
        cv.circle(x, y, 1.3, rng.choice([Y, WH, mix(WH, B, 0.5)]))

def bright(x, y, r, col=WH):
    cv.circle(x, y, r, col)
    cv.line([(x - r * 3.2, y), (x + r * 3.2, y)], col, 0.7)
    cv.line([(x, y - r * 3.2), (x, y + r * 3.2)], col, 0.7)

# the Great Square of Pegasus, high in the south on an autumn night, and Andromeda's chain
peg = [(250, 92), (330, 100), (322, 170), (244, 162)]
for (x, y) in peg: bright(x, y, 1.8)
for (x, y) in [(214, 80), (180, 72), (150, 58)]: bright(x, y, 1.6)   # Andromeda
cv.circle(170, 96, 3.2, mix(K, WH, 0.5))                             # M31 smudge
cv.ellipse(170, 96, 7, 2.4, mix(K, WH, 0.25))
# Cassiopeia's W, upper left
for (x, y) in [(28, 44), (46, 30), (62, 46), (80, 28), (98, 40)]: bright(x, y, 1.5)
# faint dotted guide lines, as on a star map
def dotted(a, b):
    n = int(math.hypot(b[0] - a[0], b[1] - a[1]) / 5)
    for k in range(2, n - 1):
        t = k / n
        cv.rect(a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[0] + (b[0] - a[0]) * t + 1, a[1] + (b[1] - a[1]) * t + 1, mix(K, B, 0.75))
for a, b in zip(peg, peg[1:] + peg[:1]): dotted(a, b)
dotted(peg[3], (214, 80)); dotted((214, 80), (180, 72)); dotted((180, 72), (150, 58))

# ---------- the moon: waning gibbous, 93%, low in the east ----------
mx, my, mr = 74, 392, 30
for rr, t in [(58, 0.12), (46, 0.25)]:
    cv.circle(mx, my, rr, mix(K, B, t))
cv.circle(mx, my, mr, WH)
# maria
for (dx, dy, rx, ry) in [(-8, -10, 9, 7), (4, -12, 7, 5), (-2, 2, 10, 7), (-14, 6, 6, 8), (8, 4, 6, 5), (-6, 14, 7, 4)]:
    cv.ellipse(mx + dx, my + dy, rx, ry, mix(WH, B, 0.35))
# craters: Tycho with rays, Copernicus, a scatter of pocks
cv.circle(mx + 2, my + 20, 2.4, WH, outline=mix(WH, K, 0.5), width=0.5)
for k in range(12):
    a = k * math.tau / 12 + 0.2
    cv.line([(mx + 2 + 3 * math.cos(a), my + 20 + 3 * math.sin(a)), (mx + 2 + 16 * math.cos(a), my + 20 + 16 * math.sin(a))], mix(WH, Y, 0.25), 0.5)
for (dx, dy, r) in [(-16, -2, 2.2), (10, -4, 1.6), (-4, -20, 1.4), (14, 12, 1.8), (-18, 14, 1.3), (18, -14, 1.4), (-10, 22, 1.2)]:
    cv.circle(mx + dx, my + dy, r, None, outline=mix(WH, K, 0.4), width=0.5)
# terminator: shadow encroaching on the right-hand limb
sh = (((X - mx) ** 2 + (Yg - my) ** 2) < mr ** 2) & ((((X - (mx - 0.34 * mr)) / (mr * 1.1)) ** 2 + ((Yg - my) / mr) ** 2) > 1) & (X > mx)
cv.mask(sh, mix(K, B, 0.2))

# ---------- the fall: a meteor with shed feathers ----------
head = (256, 452)
start = (398, 230)
dx, dy = head[0] - start[0], head[1] - start[1]
Lh = math.hypot(dx, dy); ux, uy = dx / Lh, dy / Lh
nx, ny = -uy, ux
trail = [(start[0] + dx * t, start[1] + dy * t) for t in np.linspace(0, 1, 60)]
for w, col in [(30, mix(K, R, 0.5)), (20, R), (11, Y), (4.5, WH)]:
    ribbon(cv, trail, lambda t, w=w: w * t ** 1.6, col)
# sparks
for k in range(120):
    t = rng.random() ** 0.6
    px, py = start[0] + dx * t, start[1] + dy * t
    o = rng.gauss(0, 10 * t)
    cv.circle(px + nx * o, py + ny * o, rng.uniform(0.5, 1.3), rng.choice([Y, R, WH, Y]))
# head: white-hot with wings of flame
hx, hy = head
cv.circle(hx, hy, 9, R); cv.circle(hx, hy, 6.5, Y); cv.circle(hx, hy, 4, WH)
for side in (1, -1):
    wing = []
    for k in range(9):
        a = k / 8
        wing.append((hx - ux * 26 * a + side * nx * (22 * math.sin(a * math.pi) + 4),
                     hy - uy * 26 * a + side * ny * (22 * math.sin(a * math.pi) + 4)))
    wing = [(hx, hy)] + wing
    cv.poly(wing, R)
    # primaries: feather strokes
    for k in range(1, 8):
        a = k / 8
        base = (hx - ux * 10 * a, hy - uy * 10 * a)
        cv.line([base, wing[k + 1]], Y, 1.0)

def feather(x, y, a, L, col):
    ca, sa = math.cos(a), math.sin(a)
    tip = (x + L * ca, y + L * sa)
    pts_l, pts_r = [], []
    for k in range(11):
        t = k / 10
        w = L * 0.22 * math.sin(math.pi * (0.15 + 0.85 * t)) * (1 - 0.3 * t)
        px, py = x + L * t * ca, y + L * t * sa
        pts_l.append((px - sa * w, py + ca * w)); pts_r.append((px + sa * w * 0.8, py - ca * w * 0.8))
    cv.poly(pts_l + pts_r[::-1], col)
    cv.line([(x - L * 0.2 * ca, y - L * 0.2 * sa), tip], K, 0.7)
    for k in range(2, 10, 2):
        t = k / 10
        px, py = x + L * t * ca, y + L * t * sa
        cv.line([(px, py), (px - sa * L * 0.2 + ca * 3, py + ca * L * 0.2 + sa * 3)], K, 0.5)
for k in range(11):
    t = rng.uniform(0.05, 0.95)
    px, py = start[0] + dx * t, start[1] + dy * t
    o = rng.choice([-1, 1]) * rng.uniform(18, 60)
    feather(px + nx * o, py + ny * o, rng.uniform(0, math.tau), rng.uniform(8, 15),
            rng.choice([WH, WH, mix(WH, Y, 0.5), Y, mix(R, Y, 0.5)]))

# ---------- land ----------
def ridge(base, amp, f, ph):
    return [(x, base - amp * (0.6 * math.sin(x * f + ph) + 0.4 * math.sin(x * f * 2.3 + ph * 1.7))) for x in range(-5, W + 10, 4)]
cv.poly(ridge(HOR, 10, 0.02, 1.0) + [(W + 10, H), (-5, H)], mix(K, B, 0.2))
# church from the morning, now a silhouette with one lit window
cx, cy = 318, HOR - 2
cv.rect(cx - 5, cy - 26, cx + 5, cy, K)
cv.poly([(cx - 6, cy - 26), (cx + 6, cy - 26), (cx, cy - 46)], K)
cv.rect(cx + 5, cy - 12, cx + 28, cy, K)
cv.poly([(cx + 5, cy - 12), (cx + 28, cy - 12), (cx + 24, cy - 18), (cx + 5, cy - 18)], K)
cv.line([(cx, cy - 46), (cx, cy - 52)], K, 0.8); cv.line([(cx - 2.5, cy - 50), (cx + 2.5, cy - 50)], K, 0.8)
cv.rect(cx - 1.5, cy - 20, cx + 1.5, cy - 14, Y)
cv.rect(cx + 14, cy - 8, cx + 17, cy - 3, Y)
cv.poly(ridge(HOR + 12, 8, 0.03, 3.0) + [(W + 10, H), (-5, H)], mix(K, B, 0.125))
# field hedgerow trees silhouetted against the glow
for tx in (22, 120, 180):
    r = rng.uniform(12, 20)
    cv.rect(tx - 1.5, HOR - 8, tx + 1.5, HOR + 8, K)
    for k in range(14):
        a = rng.uniform(0, math.tau); d = rng.uniform(0, r * 0.7)
        cv.circle(tx + d * math.cos(a), HOR - r - 4 + d * math.sin(a) * 0.8, r * 0.45, K)

# ---------- the cursed bramble, foreground, catching the fire ----------
canes = [bez((-20, 600), (40, 470), (180, 420), (300, 480), 90),
         bez((420, 610), (340, 470), (240, 430), (160, 500), 90),
         bez((120, 610), (170, 520), (250, 470), (330, 530), 70),
         bez((260, 610), (300, 520), (380, 500), (420, 560), 60)]
for c in canes:
    L_, R_ = ribbon(cv, c, lambda t: 6 * (1 - 0.6 * t), K)
    # rim-light from the fire, on the side facing the impact
    lit = [p for p in L_]
    for i in range(1, len(lit)):
        (x0, y0), (x1, y1) = lit[i - 1], lit[i]
        dd = math.hypot(x1 - hx, y1 - hy)
        if dd < 210:
            cv.line([(x0, y0), (x1, y1)], R if dd > 80 else Y, 1.3)
    for i in range(2, len(c) - 1, 3):
        x, y = c[i]; x2, y2 = c[i + 1]
        ddx, ddy = x2 - x, y2 - y; l = math.hypot(ddx, ddy) or 1
        nnx, nny = -ddy / l, ddx / l
        s = 1 if (i // 3) % 2 else -1
        ww = 6 * (1 - 0.6 * i / len(c)) / 2
        bx, by = x + s * nnx * ww, y + s * nny * ww
        cv.poly([(bx - ddx / l * 2, by - ddy / l * 2), (bx + ddx / l * 2, by + ddy / l * 2), (bx + s * nnx * 5 - ddx / l * 3, by + s * nny * 5 - ddy / l * 3)], K)
# leaves in silhouette along the canes
for c in canes:
    for i in range(6, len(c) - 3, 9):
        x, y = c[i]
        a = rng.uniform(0, math.tau)
        for da in (-1.0, 0, 1.0):
            aa = a + da; Lf = rng.uniform(12, 18)
            tip = (x + Lf * math.cos(aa), y + Lf * math.sin(aa))
            mid = (x + Lf * 0.5 * math.cos(aa), y + Lf * 0.5 * math.sin(aa))
            w = Lf * 0.3
            pts = [(x, y), (mid[0] - math.sin(aa) * w, mid[1] + math.cos(aa) * w), tip, (mid[0] + math.sin(aa) * w, mid[1] - math.cos(aa) * w)]
            dd = math.hypot(tip[0] - hx, tip[1] - hy)
            cv.poly(pts, K)
            if dd < 170:
                cv.line(pts[1:3], R if dd > 70 else Y, 1.0)
# blackberries glinting red
for c in canes:
    for i in range(10, len(c) - 5, 13):
        x, y = c[i]
        x += rng.uniform(-8, 8); y += rng.uniform(4, 12)
        cv.circle(x, y, 6, K)
        dd = math.hypot(x - hx, y - hy)
        for k in range(7):
            a = k * math.tau / 7
            cv.circle(x + 3.5 * math.cos(a), y + 3.5 * math.sin(a), 1.1 if dd < 150 else 0.7, R if dd < 150 else mix(K, B, 0.5))
        cv.circle(x, y, 1.1, R if dd < 150 else mix(K, B, 0.5))

# impact: smoke and embers where it lands
for k in range(9):
    sx = hx - 10 + k * 3 + 8 * math.sin(k)
    pts = [(sx + 6 * math.sin(j * 0.5 + k), hy - 8 - j * 5) for j in range(14)]
    cv.line(pts, mix(K, WH, 0.25), 2.4)
for k in range(40):
    a = rng.uniform(-math.pi, 0); d = rng.uniform(10, 45)
    cv.circle(hx + d * math.cos(a), hy + 12 + d * math.sin(a) * 0.6, rng.uniform(0.6, 1.4), rng.choice([Y, R, R]))

# a barn owl on a fence post, watching
ox, oy = 44, 520
cv.rect(ox - 4, oy + 14, ox + 4, H, mix(K, B, 0.3))
cv.ellipse(ox, oy, 10, 15, mix(K, WH, 0.35))
cv.ellipse(ox, oy - 12, 9, 8, mix(K, WH, 0.35))
cv.ellipse(ox, oy - 12, 6.5, 6, WH)
cv.circle(ox - 2.5, oy - 12, 1.4, K); cv.circle(ox + 2.5, oy - 12, 1.4, K)
cv.poly([(ox - 0.8, oy - 10), (ox + 0.8, oy - 10), (ox, oy - 7.5)], mix(R, Y, 0.5))
for k in range(5):
    cv.circle(ox - 4 + k * 2, oy + 2 + (k % 2) * 3, 0.5, K)

cv.finish()
