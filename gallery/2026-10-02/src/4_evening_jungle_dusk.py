"""Evening — Jungle Moonrise. Dusk on an alien river: a huge cratered moon over
strata of red cloud, three depths of strange flora, recursive fern fronds in the
foreground with glowing pods, and a small explorer with a lantern on the bank."""
import math, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from ink import *

rnd = random.Random(1934)  # first Flash Gordon Sunday page
cv = Canvas(R)
RIV0, RIV1 = 410, 470

# --- sky: red above, screened to yellow at the horizon, cloud strata -------------
sky = YY < RIV0
cv.ramp(sky, np.clip((YY - 40) / 360, 0, 1) ** 1.2, [K, R, R, Y])
for k in range(10):
    y0 = 70 + k * 30 + rnd.randint(-6, 6)
    x0 = rnd.randint(-60, 250)
    L = rnd.randint(120, 260)
    strat = Canvas.mask(lambda d: d.rounded_rectangle([x0, y0, x0 + L, y0 + 5 + k % 3 * 2], radius=3, fill=1))
    cv.fill(strat, R if k > 4 else K)
    cv.fill(strat & (YY == y0), Y if k > 3 else R)

# --- moons -------------------------------------------------------------------------
MX, MY, MR = 262, 190, 104
moon = Canvas.mask(lambda d: d.ellipse([MX - MR, MY - MR, MX + MR, MY + MR], fill=1))
cv.fill(moon, WH)
dist = np.hypot(XX - MX + 40, YY - MY + 30)
cv.benday(moon & (dist > MR * 0.9), B, pitch=4, r=np.clip((dist - MR * 0.9) / 30, 0.4, 2.2), angle=45)
cv.benday(moon & (dist > MR * 1.25), B, pitch=4, r=2.2)
for i in range(26):  # craters: rim arc, shadowed inner floor
    a, rr = rnd.uniform(0, 2 * math.pi), MR * math.sqrt(rnd.uniform(0, 0.85))
    cx, cy, cr = MX + rr * math.cos(a), MY + rr * math.sin(a), rnd.uniform(3, 14)
    cr *= math.sqrt(max(0.2, 1 - (rr / MR) ** 2))
    box = [cx - cr, cy - cr * 0.85, cx + cr, cy + cr * 0.85]
    cv.benday(Canvas.mask(lambda d: d.ellipse(box, fill=1)) & moon, B, pitch=3, r=1.0)
    cv.fill(Canvas.mask(lambda d: d.arc(box, 200, 380, fill=1, width=2)) & moon, B)
    cv.fill(Canvas.mask(lambda d: d.arc(box, 20, 160, fill=1, width=1)) & moon, WH)
# maria
for (ax, ay, aw, ah) in [(MX - 40, MY - 30, 50, 30), (MX + 10, MY + 20, 40, 28), (MX - 10, MY - 60, 30, 18)]:
    cv.benday(Canvas.mask(lambda d: d.ellipse([ax, ay, ax + aw, ay + ah], fill=1)) & moon, B, pitch=4, r=1.5, angle=15)
cv.fill(Canvas.mask(lambda d: d.ellipse([MX - MR, MY - MR, MX + MR, MY + MR], outline=1, width=2)), Y)
# small green moon
cv.draw(lambda d: d.ellipse([60, 90, 92, 122], fill=1), G)
cv.benday(Canvas.mask(lambda d: d.ellipse([60, 90, 92, 122], fill=1)) & (XX + YY > 160), K, 4, 1.3)
cv.draw(lambda d: d.ellipse([60, 90, 92, 122], outline=1, width=1), Y)
for _ in range(60):  # first stars in the dark upper sky
    x, y = rnd.randrange(W), rnd.randrange(0, 90)
    if not moon[y, x]:
        cv.a[y, x] = rnd.choice([WH, Y])

# --- far jungle: blue lollipop trees and spires --------------------------------------
far = np.zeros((H, W), bool)
x = -10
while x < W + 10:
    kind = rnd.random()
    base = RIV0 + 2
    h = rnd.uniform(40, 120)
    if kind < 0.5:
        r = rnd.uniform(10, 22)
        far |= Canvas.mask(lambda d: d.rectangle([x - 2, base - h, x + 2, base], fill=1))
        far |= Canvas.mask(lambda d: d.ellipse([x - r, base - h - r, x + r, base - h + r], fill=1))
    elif kind < 0.8:
        w = rnd.uniform(8, 16)
        far |= Canvas.mask(lambda d: d.polygon([(x - w, base), (x + w, base), (x, base - h * 1.2)], fill=1))
    else:
        far |= Canvas.mask(lambda d: d.ellipse([x - 16, base - 30, x + 16, base + 10], fill=1))
    x += rnd.uniform(12, 26)
far &= YY < RIV0 + 4
cv.fill(far, B)
cv.hatch(far, K, pitch=3, angle=0, width=1)
cv.fill(far & ~np.roll(far, 2, 1) & ~np.roll(far, 2, 0), Y)  # rim light from the moon side

# --- the river: reflections of sky, moon and far trees ----------------------------------
riv = (YY >= RIV0) & (YY < RIV1)
cv.fill(riv, K)
for y in range(RIV0, RIV1, 3):
    src_y = 2 * RIV0 - y - 30
    row = cv.a[max(0, src_y)].copy()
    shift = int(3 * math.sin(y * 1.7))
    row = np.roll(row, shift, 0)
    keep = (np.arange(W) // (6 + (y - RIV0) // 6)) % 2 == 0
    cv.a[y, keep] = row[keep]
for k in range(14):  # moon path dashes
    y = RIV0 + 4 + k * 4
    w = 30 - k
    cv.a[y, MX - w + rnd.randint(-4, 4):MX + w + rnd.randint(-4, 4)] = WH

# --- mid flora: green bottle trees, fiddleheads, pitcher plants ------------------------
def bottle(x, base, h, w):
    pts = [(x - w * 0.3, base)]
    for i in range(21):
        t = i / 20
        bulge = w * (0.3 + 0.7 * math.sin(math.pi * min(1, t * 1.4)) ** 2) * (1 - t * 0.5)
        pts.append((x - bulge, base - h * t))
    pts += [(x + w * 0.1, base - h - 14), (x + w * 0.2, base - h)]
    right = [(2 * x - p[0], p[1]) for p in pts[1:22]][::-1]
    pts += right + [(x + w * 0.3, base)]
    m = Canvas.mask(lambda d: d.polygon(pts, fill=1))
    cv.fill(m, G)
    cv.hatch(m & (XX > x + w * 0.15), K, pitch=3, angle=60, width=1)
    cv.hatch(m & (XX > x + w * 0.45), K, pitch=3, angle=120, width=1)
    for k in range(4, int(h), 9):  # bark rings
        cv.fill(m & (np.abs(YY - (base - k)) < 1) & (XX < x), Y if k % 2 else K)
    cv.draw(lambda d: d.line(pts + [pts[0]], fill=1, width=2), K)
    for k in range(5):  # leafy crown spikes
        a = -math.pi / 2 + (k - 2) * 0.5
        cv.draw(lambda d: d.line([x, base - h - 10, x + 30 * math.cos(a), base - h - 10 + 30 * math.sin(a)], fill=1, width=3), G)
        cv.draw(lambda d: d.line([x, base - h - 10, x + 30 * math.cos(a), base - h - 10 + 30 * math.sin(a)], fill=1, width=1), K)


def pitcher(x, base, h):
    pts = [(x - 4, base), (x - 12, base - h * 0.4), (x - 9, base - h), (x + 9, base - h), (x + 12, base - h * 0.4), (x + 4, base)]
    m = Canvas.mask(lambda d: d.polygon(pts, fill=1))
    cv.fill(m, R)
    cv.hatch(m, Y, pitch=4, angle=90, width=1)
    cv.draw(lambda d: d.line(pts + [pts[0]], fill=1, width=2), K)
    cv.draw(lambda d: d.ellipse([x - 10, base - h - 4, x + 10, base - h + 4], fill=1), K)
    cv.draw(lambda d: d.ellipse([x - 10, base - h - 4, x + 10, base - h + 4], outline=1, width=1), Y)


bank = [(0, RIV1 + 8)]
for x in range(0, W + 20, 20):
    bank.append((x, RIV1 - 4 + 6 * math.sin(x / 31)))
bank += [(W, H), (0, H)]
cv.draw(lambda d: d.polygon(bank, fill=1), G)
cv.hatch(Canvas.mask(lambda d: d.polygon(bank, fill=1)), K, pitch=6, angle=10, width=1)
bottle(70, RIV1 + 20, 150, 30)
bottle(345, RIV1 + 30, 190, 36)
for (px, ph) in [(120, 50), (138, 34), (300, 44), (280, 30)]:
    pitcher(px, RIV1 + 24, ph)

# --- foreground: recursive black fern fronds with glowing pods -------------------------
ink = np.zeros((H, W), bool)
glow = []


def frond(x, y, ang, L, curl, depth, width):
    pts = []
    n = 26
    a = ang
    for i in range(n):
        pts.append((x, y))
        step = L / n
        x += step * math.cos(a); y += step * math.sin(a)
        a += curl * (0.4 + i / n)
        t = i / n
        if depth > 0 and i > 2 and i < n - 3 and i % 2 == 0:
            for side in (-1, 1):
                ll = L * 0.32 * (1 - t) ** 0.8
                if ll > 5:
                    frond(x, y, a + side * 1.05, ll, -side * 0.05 + curl * 0.3, depth - 1, max(2, width - 1))
    # fiddlehead spiral at the tip
    r = L * 0.05
    for i in range(18):
        pts.append((x, y))
        a += 0.5
        r *= 0.88
        x += r * math.cos(a); y += r * math.sin(a)
    m = Canvas.mask(lambda d: d.line(pts, fill=1, width=width, joint="curve"))
    ink[:] |= m
    if depth == 2 and rnd.random() < 0.8:
        glow.append((pts[n // 2][0], pts[n // 2][1]))


frond(-10, 610, -1.2, 260, 0.045, 2, 4)
frond(30, 620, -1.45, 210, 0.06, 2, 3)
frond(410, 600, -1.95, 280, -0.05, 2, 4)
frond(380, 630, -1.7, 200, -0.07, 2, 3)
frond(200, 640, -1.5, 120, 0.03, 1, 2)
# hanging vines from the top-left
for k in range(6):
    vx = 6 + k * 18
    L = rnd.uniform(80, 220)
    vpts = [(vx + 6 * math.sin(t / 9 + k), t) for t in range(0, int(L), 3)]
    ink |= Canvas.mask(lambda d: d.line(vpts, fill=1, width=2))
    for t in range(10, int(L), 14):
        lx, ly = vx + 6 * math.sin(t / 9 + k), t
        ink |= Canvas.mask(lambda d: d.polygon([(lx, ly), (lx + 9, ly + 3), (lx, ly + 7)], fill=1))
ink |= (YY < 8) & (XX < 130)
# outline the ink in red so the fronds read against the black water
edge = ink & ~np.roll(ink, 1, 0) | ink & ~np.roll(ink, -1, 1)
halo = (np.roll(ink, 1, 0) | np.roll(ink, -1, 0) | np.roll(ink, 1, 1) | np.roll(ink, -1, 1)) & ~ink
cv.fill(halo & (YY > RIV0 - 2), R)
cv.fill(ink, K)
for (gx, gy) in glow + [(60, 230), (110, 160)]:
    cv.draw(lambda d: d.ellipse([gx - 6, gy - 6, gx + 6, gy + 6], fill=1), R)
    cv.draw(lambda d: d.ellipse([gx - 3, gy - 3, gx + 3, gy + 3], fill=1), Y)
    cv.a[int(gy) - 1:int(gy) + 1, int(gx) - 1:int(gx) + 1] = WH

# --- the explorer with a lantern, small on the bank ---------------------------------------
ex, ey = 214, RIV1 + 14
lg = Canvas.mask(lambda d: d.ellipse([ex + 4, ey - 52, ex + 44, ey - 12], fill=1))
cv.benday(lg & ~ink, Y, pitch=3, r=1.0)
cv.draw(lambda d: d.ellipse([ex - 5, ey - 40, ex + 5, ey - 30], fill=1), WH)     # helmet
cv.draw(lambda d: d.ellipse([ex - 5, ey - 40, ex + 5, ey - 30], outline=1, width=1), K)
cv.draw(lambda d: d.polygon([(ex - 6, ey - 29), (ex + 6, ey - 29), (ex + 7, ey - 12), (ex - 7, ey - 12)], fill=1), B)
cv.draw(lambda d: d.line([ex - 4, ey - 12, ex - 5, ey], fill=1, width=3), K)
cv.draw(lambda d: d.line([ex + 4, ey - 12, ex + 5, ey], fill=1, width=3), K)
cv.draw(lambda d: d.line([ex + 6, ey - 26, ex + 22, ey - 32], fill=1, width=2), K)    # arm with lantern
cv.draw(lambda d: d.rectangle([ex + 20, ey - 36, ex + 28, ey - 26], fill=1), Y)
cv.draw(lambda d: d.rectangle([ex + 20, ey - 36, ex + 28, ey - 26], outline=1, width=1), K)
cv.draw(lambda d: d.line([ex - 2, ey - 40, ex - 6, ey - 50], fill=1, width=1), K)     # antenna
cv.a[ey - 52:ey - 49, ex - 7:ex - 4] = R
cv.save()
