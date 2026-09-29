"""Morning — 'The Last Good Blackberries'. A hedgerow bramble at sunrise on Michaelmas,
drawn as a dense botanical plate: canes, thorns, serrated leaves turning red, berries
at every stage, a wren, and a dew-strung web in the dark of the hedge."""
import math, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from ink import *

cv = Canvas(bg=WH, seed=929)
rng = cv.rng
X, Yg = cv.grid()

# ---------- sky: banded screens, pale yellow warming to the horizon ----------
HOR = 250
for i, y0 in enumerate(range(0, HOR, 10)):
    t = (y0 / HOR) ** 1.6
    cv.rect(0, y0, W, y0 + 10, mix(WH, Y, 0.05 + 0.75 * t))
# sun: rising low, left of centre, with rings of screen
sx, sy = 132, 238
for r, t in [(80, 0.55), (62, 0.35), (46, 0.18)]:
    cv.circle(sx, sy, r, mix(WH, Y, t))
cv.circle(sx, sy, 30, WH)
cv.circle(sx, sy, 30, None, outline=Y, width=2)
# long sun rays as thin yellow lines
for k in range(36):
    a = math.pi + k * math.pi / 35
    cv.line([(sx + 36 * math.cos(a), sy + 36 * math.sin(a)),
             (sx + 400 * math.cos(a), sy + 400 * math.sin(a))], mix(WH, Y, 0.6), 1.0)
# a few thin clouds
for cy, cx, ln in [(62, 290, 120), (86, 330, 70), (118, 60, 90), (150, 250, 60)]:
    for j in range(3):
        cv.line([(cx - ln / 2 + j * 8, cy + j * 4), (cx + ln / 2 - j * 10, cy + j * 4)], WH, 2.2)
        cv.line([(cx - ln / 2 + j * 8 + 4, cy + j * 4 + 2), (cx + ln / 2 - j * 10, cy + j * 4 + 2)], mix(WH, R, 0.25), 0.8)

# ---------- distant hills (blue screens) and a church tower ----------
def ridge(base, amp, freq, phase):
    return [(x, base - amp * (0.6 * math.sin(x * freq + phase) + 0.4 * math.sin(x * freq * 2.7 + phase * 1.3)))
            for x in range(-5, W + 10, 5)]
for base, amp, t, ph in [(236, 22, 0.25, 0.3), (246, 14, 0.45, 2.1), (256, 10, 0.7, 4.0)]:
    pts = ridge(base, amp, 0.018, ph)
    cv.poly(pts + [(W + 10, 300), (-5, 300)], mix(WH, B, t))
# church with spire on the far ridge (St Michael's, naturally)
cx, cy = 318, 246
cv.rect(cx - 5, cy - 26, cx + 5, cy, mix(WH, B, 0.85))
cv.poly([(cx - 6, cy - 26), (cx + 6, cy - 26), (cx, cy - 46)], mix(WH, B, 0.85))
cv.rect(cx + 5, cy - 12, cx + 26, cy, mix(WH, B, 0.85))
cv.poly([(cx + 5, cy - 12), (cx + 26, cy - 12), (cx + 22, cy - 18), (cx + 5, cy - 18)], mix(WH, B, 0.85))
cv.line([(cx, cy - 46), (cx, cy - 52)], B, 0.8)
cv.line([(cx - 2.5, cy - 50), (cx + 2.5, cy - 50)], B, 0.8)
# mist band
for y0 in range(254, 268, 2):
    cv.line([(0, y0), (W, y0 + 1)], WH, 1.0 if y0 % 4 else 0.6)

# ---------- stubble field with rows and geese ----------
cv.poly([(0, 266), (W, 262), (W, 340), (0, 340)], mix(Y, WH, 0.25))
for k in range(-30, 40):
    x0 = 200 + k * 14
    cv.line([(200 + k * 1.2, 264), (x0, 340)], mix(Y, R, 0.3), 0.8)
for j in range(14):
    y = 268 + j ** 1.5 * 1.3
    cv.line([(0, y), (W, y - 3)], mix(Y, K, 0.15), 0.6)
# geese grazing the stubble: tiny but drawn
def goose(x, y, s, flip=1, head_down=False):
    cv.ellipse(x, y, 7 * s, 4 * s, WH, outline=K, width=0.6)
    cv.poly([(x - 7 * s * flip, y - 1 * s), (x - 11 * s * flip, y - 3 * s), (x - 6 * s * flip, y + 1 * s)], WH)
    if head_down:
        nk = [(x + 5 * s * flip, y - 1 * s), (x + 9 * s * flip, y + 2 * s), (x + 11 * s * flip, y + 5 * s)]
    else:
        nk = [(x + 5 * s * flip, y - 2 * s), (x + 8 * s * flip, y - 7 * s), (x + 9 * s * flip, y - 11 * s)]
    cv.line(nk, K, 1.6 * s)
    cv.circle(nk[-1][0], nk[-1][1], 1.6 * s, K)
    cv.line([(nk[-1][0], nk[-1][1]), (nk[-1][0] + 3 * s * flip, nk[-1][1] + 0.8 * s)], R, 1.0 * s)
    cv.line([(x - 1 * s, y + 4 * s), (x - 1 * s, y + 7 * s)], R, 0.7)
    cv.line([(x + 2 * s, y + 4 * s), (x + 2 * s, y + 7 * s)], R, 0.7)
for (x, y, s, f, hd) in [(236, 282, 0.8, 1, True), (262, 286, 0.85, -1, False), (282, 280, 0.75, 1, True),
                         (306, 290, 0.95, 1, False), (340, 284, 0.8, -1, True), (212, 294, 1.0, -1, True)]:
    goose(x, y, s, f, hd)

# ---------- the hedge: dark interior ----------
hedge_top = [(x, 318 + 18 * math.sin(x * 0.03) + 10 * math.sin(x * 0.11 + 1)) for x in range(-5, W + 10, 4)]
cv.poly(hedge_top + [(W + 10, H + 5), (-5, H + 5)], mix(K, G, 0.25))
# leaf-mass texture inside the hedge: many small dark leaf silhouettes
for _ in range(900):
    x = rng.uniform(-10, W + 10); y = rng.uniform(320, H + 10)
    a = rng.uniform(0, math.tau); l = rng.uniform(5, 11)
    col = rng.choice([K, K, mix(K, G, 0.6), mix(K, G, 0.75), G, mix(G, Y, 0.2)])
    pts = [(x, y), (x + l * math.cos(a + 0.5) * 0.6, y + l * math.sin(a + 0.5) * 0.6),
           (x + l * math.cos(a), y + l * math.sin(a)), (x + l * math.cos(a - 0.5) * 0.6, y + l * math.sin(a - 0.5) * 0.6)]
    cv.poly(pts, col)

# ---------- spider web, strung in the hedge dark, beaded with dew ----------
wx, wy, wr = 300, 470, 70
spokes = 19
ang = [k * math.tau / spokes + rng.uniform(-0.08, 0.08) for k in range(spokes)]
anchors = []
for a in ang:
    ex, ey = wx + wr * 1.15 * math.cos(a), wy + wr * math.sin(a)
    cv.line([(wx, wy), (ex, ey)], WH, 0.75)
    anchors.append((a, ex, ey))
for ring in range(4, 34):
    rr = 6 + ring * 2.0
    pts = []
    for k in range(spokes + 1):
        a = ang[k % spokes] + (math.tau if k == spokes else 0)
        sag = 1 - 0.06 * math.sin(k * 1.7 + ring)
        pts.append((wx + rr * 1.15 * sag * math.cos(a), wy + rr * sag * math.sin(a)))
    cv.line(pts, WH, 0.7, joint=False)
    for k in range(spokes):
        if rng.random() < 0.35:
            x, y = pts[k]
            cv.circle(x, y, rng.uniform(0.9, 1.5), WH)
# frame threads up to the canes
for (a, ex, ey) in anchors[::5]:
    cv.line([(ex, ey), (ex + 30 * math.cos(a), ey + 30 * math.sin(a))], WH, 0.5)

# ---------- bramble canes ----------
canes = [
    bez((-20, 600), (40, 330), (230, 220), (420, 330), 120),
    bez((440, 610), (330, 380), (120, 300), (-30, 420), 120),
    bez((60, 620), (90, 470), (200, 420), (260, 520), 80),
    bez((180, 610), (230, 400), (360, 370), (430, 470), 90),
]
def draw_cane(path, w):
    L, Rr = ribbon(cv, path, lambda t: w * (1 - 0.55 * t), mix(R, K, 0.35))
    # lit edge
    cv.line(L, R, 1.0)
    cv.line(Rr, K, 0.8)
    # thorns, curved back
    for i in range(3, len(path) - 2, 3):
        x, y = path[i]
        x2, y2 = path[i + 1]
        dx, dy = x2 - x, y2 - y
        l = math.hypot(dx, dy) or 1
        nx, ny = -dy / l, dx / l
        side = 1 if (i // 3) % 2 else -1
        ww = w * (1 - 0.55 * i / len(path)) / 2
        bx, by = x + side * nx * ww, y + side * ny * ww
        tip = (bx + side * nx * 5 - dx / l * 3.5, by + side * ny * 5 - dy / l * 3.5)
        cv.poly([(bx - dx / l * 2.5, by - dy / l * 2.5), (bx + dx / l * 2.5, by + dy / l * 2.5), tip], mix(R, Y, 0.3))
for c, w in zip(canes, (7, 7, 5, 5)):
    draw_cane(c, w)

# ---------- leaves ----------
def leaflet(x, y, a, L, Wd, col, vein):
    pts_l, pts_r = [], []
    n = 22
    for i in range(n + 1):
        t = i / n
        hw = Wd * math.sin(math.pi * t ** 0.75) * (1 - 0.15 * t)
        tooth = 0.0 if i % 2 else 1.4 * (0.3 + t)
        hw = max(0, hw + tooth * (0 < t < 0.97))
        px, py = x + L * t * math.cos(a), y + L * t * math.sin(a)
        nx, ny = -math.sin(a), math.cos(a)
        pts_l.append((px + nx * hw, py + ny * hw))
        pts_r.append((px - nx * hw, py - ny * hw))
    cv.poly(pts_l + pts_r[::-1], col)
    # midrib + pinnate veins
    tip = (x + L * math.cos(a), y + L * math.sin(a))
    cv.line([(x, y), tip], vein, 0.8)
    for j in range(1, 8):
        t = j / 8.5
        px, py = x + L * t * math.cos(a), y + L * t * math.sin(a)
        hw = Wd * math.sin(math.pi * t ** 0.75) * 0.85
        for sgn in (1, -1):
            b = a + sgn * 0.75
            cv.line([(px, py), (px + hw * 1.1 * math.cos(b), py + hw * 1.1 * math.sin(b))], vein, 0.55)

def leaf(x, y, a, s, palette):
    col, vein = palette
    # petiole
    ex, ey = x + 10 * s * math.cos(a), y + 10 * s * math.sin(a)
    cv.line([(x, y), (ex, ey)], mix(R, K, 0.3), 1.4 * s)
    # three or five leaflets
    spec = [(0, 1.0), (-1.05, 0.78), (1.05, 0.78)]
    if s > 1.05:
        spec += [(-1.7, 0.55), (1.7, 0.55)]
    for da, k in spec[::-1]:
        leaflet(ex + 4 * s * math.cos(a + da), ey + 4 * s * math.sin(a + da), a + da, 24 * s * k, 7.5 * s * k, col, vein)
        cv.line([(ex, ey), (ex + 4 * s * math.cos(a + da), ey + 4 * s * math.sin(a + da))], vein, 0.8)

LEAF_COLS = [(G, mix(G, Y, 0.5)), (G, mix(G, K, 0.5)), (mix(G, Y, 0.3), G), (R, mix(R, Y, 0.5)),
             (mix(R, K, 0.3), R), (Y, mix(Y, R, 0.5)), (mix(G, R, 0.5), R)]
placed = []
for ci, c in enumerate(canes):
    for i in range(8, len(c) - 4, 11 + ci):
        x, y = c[i]
        if y < 200: continue
        a = rng.uniform(-math.pi, math.pi)
        s = rng.uniform(0.8, 1.3)
        weights = [3, 2, 2, 2, 1, 1, 1] if y > 360 else [3, 3, 2, 1, 1, 1, 1]
        pal = rng.choices(LEAF_COLS, weights)[0]
        leaf(x, y, a, s, pal)

# ---------- blackberries ----------
def berry(x, y, r, stage):
    # sepals
    for k in range(5):
        a = -math.pi / 2 + k * math.tau / 5 + 0.3
        cv.poly([(x, y - r * 0.9), (x + r * 0.9 * math.cos(a), y - r * 0.9 + r * 0.9 * math.sin(a) * 0.5),
                 (x + r * 0.4 * math.cos(a + 0.4), y - r * 0.9 + r * 0.4 * math.sin(a + 0.4) * 0.5)], G)
    body, shade, hi = {"ripe": (K, K, WH), "turning": (R, mix(R, K, 0.5), WH),
                       "red": (R, R, Y), "green": (G, mix(G, K, 0.4), Y)}[stage]
    cv.ellipse(x, y, r, r * 1.1, shade)
    # drupelets in rings
    for ring, (rr, n) in enumerate([(0, 1), (0.42, 7), (0.78, 12)]):
        for k in range(n):
            a = k * math.tau / n + ring * 0.3
            dx, dy = x + rr * r * math.cos(a), y + rr * r * 1.1 * math.sin(a)
            dr = r * (0.34 if ring < 2 else 0.28)
            c = body if stage != "turning" or (k + ring) % 3 else K
            cv.circle(dx, dy, dr, c, outline=K if stage != "ripe" else None, width=0.4)
            cv.circle(dx - dr * 0.35, dy - dr * 0.35, max(0.6, dr * 0.3), hi)

def flower(x, y, r):
    for k in range(5):
        a = k * math.tau / 5 + 0.2
        cv.ellipse(x + r * 0.55 * math.cos(a), y + r * 0.55 * math.sin(a), r * 0.5, r * 0.5, WH, outline=mix(WH, R, 0.4), width=0.5)
    cv.circle(x, y, r * 0.35, Y)
    for k in range(10):
        a = k * math.tau / 10
        cv.circle(x + r * 0.3 * math.cos(a), y + r * 0.3 * math.sin(a), 0.6, G)

clusters = [(70, 420), (150, 350), (238, 300), (330, 350), (385, 330), (110, 520), (205, 470),
            (360, 420), (40, 330), (270, 560), (180, 560)]
for (cx, cy) in clusters:
    n = rng.randint(4, 7)
    for j in range(n):
        a = rng.uniform(0, math.tau); d = rng.uniform(0, 26)
        x, y = cx + d * math.cos(a), cy + d * math.sin(a) + 8
        cv.line([(cx, cy - 10), (x, y - 9)], mix(G, R, 0.5), 1.0)
    for j in range(n):
        a = rng.uniform(0, math.tau); d = rng.uniform(0, 26)
        x, y = cx + d * math.cos(a), cy + d * math.sin(a) + 8
        stage = rng.choices(["ripe", "turning", "red", "green"], [5, 2, 2, 1])[0]
        berry(x, y, rng.uniform(8, 11), stage)
    if rng.random() < 0.4:
        flower(cx + 22, cy - 12, 7)

# ---------- a wren on the high cane ----------
def wren(x, y):
    body = mix(R, K, 0.45)
    cv.ellipse(x, y, 16, 12, body)
    # barred wings
    cv.ellipse(x - 2, y + 1, 11, 7, mix(R, Y, 0.35))
    for k in range(6):
        cv.line([(x - 10 + k * 3.5, y - 4), (x - 12 + k * 3.5, y + 6)], K, 0.8)
    # cocked tail
    cv.poly([(x - 12, y - 4), (x - 22, y - 26), (x - 16, y - 28), (x - 7, y - 6)], body)
    for k in range(5):
        cv.line([(x - 13 - k * 1.7, y - 9 - k * 3.6), (x - 9 - k * 1.7, y - 10 - k * 3.6)], K, 0.8)
    # head
    cv.circle(x + 13, y - 7, 8, body)
    cv.line([(x + 8, y - 11), (x + 20, y - 10)], mix(WH, Y, 0.3), 1.4)   # pale supercilium
    cv.circle(x + 16, y - 7, 1.7, K)
    cv.circle(x + 16.5, y - 7.5, 0.6, WH)
    cv.poly([(x + 20, y - 7), (x + 28, y - 5), (x + 20, y - 4)], K)
    # breast
    cv.ellipse(x + 8, y + 3, 7, 6, mix(Y, R, 0.25))
    # legs gripping the cane
    for dx in (0, 5):
        cv.line([(x + dx, y + 10), (x + dx + 2, y + 17)], mix(R, Y, 0.4), 1.1)
        cv.line([(x + dx - 2, y + 18), (x + dx + 5, y + 17)], mix(R, Y, 0.4), 0.9)
    # song: three notes rising
    for k, (nx, ny) in enumerate([(x + 34, y - 20), (x + 44, y - 32), (x + 56, y - 40)]):
        cv.line([(nx, ny), (nx + 5, ny - 3)], K, 0.8)
_c = min(canes[0], key=lambda p: abs(p[0] - 262))
wren(_c[0], _c[1] - 17)

# ---------- border & caption ----------
cv.rect(0, 0, W, 4, K); cv.rect(0, H - 4, W, H, K); cv.rect(0, 0, 4, H, K); cv.rect(W - 4, 0, W, H, K)
cv.rect(4, 4, W - 4, 5, WH)
cv.finish()
