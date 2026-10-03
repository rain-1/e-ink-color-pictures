"""Music for 18 Musicians (1976, fifty this year): the stage from the lighting rig at noon."""
import math, sys, os, random
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from ink import *

random.seed(18)
c = Canvas(Y)

# --- wooden stage: planks with grain ---------------------------------------
STAGE_BOTTOM = 448
for py in range(0, STAGE_BOTTOM, 13):
    off = random.randint(0, 120)
    for jx in range(-off, W, 150):
        c.line([(jx, py), (jx, py + 13)], K, 0.6)
    c.line([(0, py), (W, py)], K, 0.6)
    for g in range(1):
        gy = py + 6.5 + random.uniform(-2, 2)
        x = random.uniform(-40, 0)
        while x < W:
            ln = random.uniform(15, 60)
            wob = random.uniform(-1.2, 1.2)
            c.line([(x, gy), (x + ln / 2, gy + wob), (x + ln, gy)], R, 0.5)
            x += ln + random.uniform(25, 80)
# stage edge
c.rect(0, STAGE_BOTTOM, W, STAGE_BOTTOM + 7, fill=K)
c.line([(0, STAGE_BOTTOM + 2.5), (W, STAGE_BOTTOM + 2.5)], Y, 0.6)


def place(x0, y0, ang):
    ca, sa = math.cos(ang), math.sin(ang)
    return lambda pts: [(x0 + x * ca - y * sa, y0 + x * sa + y * ca) for x, y in pts]


def box(T, x0, y0, x1, y1):
    return T([(x0, y0), (x1, y0), (x1, y1), (x0, y1)])


def player(x, y, shirt, ang=0, hair=K, arms=None):
    """Top-down person: shoulders, head, optional arms to (dx,dy) targets in local coords."""
    T = place(x, y, ang)
    if arms:
        for ax, ay in arms:
            c.line(T([(0, 0), (ax, ay)]), shirt, 4)
            hx, hy = T([(ax, ay)])[0]
            c.ellipse(hx, hy, 2.6, 2.6, fill=Wh, outline=K, width=0.5)
    pts = [(math.cos(t) * 13, math.sin(t) * 7) for t in np.linspace(0, 2 * math.pi, 24)]
    c.poly(T(pts), fill=shirt, outline=K, width=0.7)
    c.ellipse(x, y, 6.5, 6.5, fill=hair, outline=K, width=0.6)


def shadow_poly(pts, dx=4, dy=5):
    c.poly([(x + dx, y + dy) for x, y in pts], fill=mix(Y, K, 0.5))


def marimba(x, y, ang, bars=26, bar_col=R, frame=K):
    T = place(x, y, ang)
    L = bars * 5.0
    outline = [(-L / 2 - 4, -16), (L / 2 + 4, -10), (L / 2 + 4, 10), (-L / 2 - 4, 16)]
    shadow_poly(T(outline))
    c.poly(T(outline), fill=frame)
    for i in range(bars):
        bx = -L / 2 + i * 5 + 0.6
        h = 15 - 5.5 * i / bars
        c.poly(box(T, bx, -h, bx + 3.8, h), fill=bar_col, outline=K, width=0.5)
        c.ellipse(*T([(bx + 1.9, -h + 2.5)])[0], 0.7, 0.7, fill=Y)
        c.ellipse(*T([(bx + 1.9, h - 2.5)])[0], 0.7, 0.7, fill=Y)
    # cord running through the bars
    c.line(T([(-L / 2, -12), (L / 2, -7.5)]), Wh, 0.4)
    c.line(T([(-L / 2, 12), (L / 2, 7.5)]), Wh, 0.4)
    return T


def piano(x, y, ang, lid=True):
    T = place(x, y, ang)
    Wd, L = 50, 84
    pts = [(-Wd / 2, 0), (Wd / 2, 0), (Wd / 2, L * 0.28)]
    for t in np.linspace(0, 1, 14):  # bent side swings in
        s_ = t * t * (3 - 2 * t)
        pts.append((Wd / 2 - Wd * 0.58 * s_, L * 0.28 + L * 0.5 * t))
    for t in np.linspace(0, math.pi, 12):  # rounded tail
        cx0, r0 = (Wd / 2 - Wd * 0.58 - Wd / 2) / 2, (Wd - Wd * 0.58) / 2
        pts.append((cx0 + r0 * math.cos(t), L * 0.78 + r0 * 1.1 * math.sin(t)))
    pts.append((-Wd / 2, L * 0.78))
    shadow_poly(T(pts), 6, 7)
    c.poly(T(pts), fill=K)
    if lid:  # gold plate and strings visible through the open lid
        inner = [(px * 0.74 + 1, 7 + py * 0.8) for px, py in pts]
        c.poly(T(inner), fill=Y)
        for s in range(13):
            sx = -Wd / 2 + 6 + s * 3.2
            ey = L * 0.28 + max(0, (sx - (Wd / 2 - Wd * 0.58)) / (Wd * 0.58)) * 0 + (L * 0.8 - (sx + Wd / 2) * 0.75)
            c.line(T([(sx, 7), (sx, max(14, ey))]), K, 0.45)
        c.ellipse(*T([(-4, L * 0.35)])[0], 3, 3, fill=K)
        c.ellipse(*T([(4, L * 0.22)])[0], 2.5, 2.5, fill=K)
        c.line(T([(-Wd / 2 + 4, 6), (-Wd / 2 + 4, L * 0.8)]), R, 1.2)
    # keyboard
    c.poly(box(T, -Wd / 2 - 2, -12, Wd / 2 + 2, 0), fill=K)
    for k in range(17):
        kx = -Wd / 2 + k * (Wd / 17)
        c.poly(box(T, kx + 0.3, -11, kx + Wd / 17 - 0.3, -1), fill=Wh)
    for k in range(16):
        if k % 7 in (2, 6):
            continue
        kx = -Wd / 2 + (k + 1) * (Wd / 17)
        c.poly(box(T, kx - 1, -11, kx + 1, -5), fill=K)
    return T


def stand(x, y, ang):
    T = place(x, y, ang)
    c.line(T([(0, 0), (0, 6)]), K, 0.8)
    c.poly(box(T, -9, -2, 9, 2), fill=K)
    c.poly(box(T, -8, -1.5, 0, 1.5), fill=Wh)
    c.poly(box(T, 0.4, -1.5, 8, 1.5), fill=Wh)


def mic(x, y, tx, ty):
    c.line([(x, y), (tx, ty)], K, 1)
    c.ellipse(tx, ty, 2.2, 2.2, fill=K)
    c.ellipse(x, y, 4, 4, outline=K, width=0.8)


# cables first, so everything sits on them
for _ in range(6):
    x, y = random.uniform(40, 360), random.uniform(60, 400)
    vx, vy = random.uniform(-2, 2), random.uniform(-2, 2)
    pts = [(x, y)]
    for s in range(80):
        vx += random.uniform(-0.35, 0.35); vy += random.uniform(-0.35, 0.35)
        n = math.hypot(vx, vy) or 1
        vx, vy = vx / n * 2.2, vy / n * 2.2
        x += vx; y += vy
        pts.append((x, y))
    c.line(pts, K, 1.4)

# back: four voices on mics, violin, cello, two clarinets
for i, sx in enumerate([42, 82, 122, 162]):
    mic(sx, 40, sx, 58)
    stand(sx, 75, 0)
    player(sx, 92, [B, G, R, B][i], hair=[K, R, K, Y][i])
mic(250, 42, 247, 56)
player(250, 80, G, ang=0.2, arms=[(-14, -12), (12, -6)])
c.line(place(250, 80, 0.2)([(-15, -12), (14, -18)]), R, 2.2)  # violin
player(300, 84, R, ang=-0.1, arms=[(-8, -12), (12, -4)])
c.poly(place(300, 70, -0.5)([(-5, -9), (5, -9), (6, 5), (-6, 5)]), fill=R, outline=K, width=0.6)  # cello
c.line([(300, 62), (300, 52)], K, 1)
for cx_, col in [(345, B), (378, Wh)]:
    stand(cx_, 62, 0)
    player(cx_, 84, col, arms=[(-3, -14), (3, -14)])
    c.line([(cx_, 72), (cx_, 64)], K, 2)

# four pianos in two facing pairs
piano(95, 182, 0.0)
player(95, 156, Wh, arms=[(-14, 10), (14, 10)])
piano(305, 182, 0.0)
player(305, 156, R, arms=[(-14, 10), (14, 10)])
piano(165, 300, math.pi - 0.15)
player(169, 328, G, ang=math.pi - 0.15, arms=[(-14, 10), (14, 10)])
piano(250, 300, math.pi + 0.15)
player(246, 328, B, ang=math.pi + 0.15, arms=[(-14, 10), (14, 10)])

# vibraphone (metallophone) centre, silver bars with blue frame & resonator dots
T = marimba(205, 222, 0.0, bars=19, bar_col=Wh, frame=B)
player(205, 246, Y, hair=K, arms=[(-16, -12), (16, -12)])

# three marimbas and two xylophones at the front
mx = [(70, 372, -0.25), (200, 392, 0.0), (330, 372, 0.25)]
for (x, y, a), sh in zip(mx, [B, R, G]):
    marimba(x, y, a)
    T = place(x, y, a)
    for px in (-30, 30):  # two players per marimba
        hx, hy = T([(px, 30)])[0]
        player(hx, hy, sh, ang=a, arms=[(-10, -18), (10, -18)])
        for side in (-10, 10):
            ex, ey = T([(px + side * 1.2, 30 - 26)])[0]
            c.line([T([(px + side, 30 - 18)])[0], (ex, ey)], K, 0.6)
            c.ellipse(ex, ey, 1.6, 1.6, fill=Y if sh != Y else R, outline=K, width=0.4)
for x, y, a in [(28, 262, 1.3), (372, 262, -1.3)]:
    marimba(x, y, a, bars=17, bar_col=R)
    T = place(x, y, a)
    hx, hy = T([(0, 26)])[0]
    player(hx, hy, Wh, ang=a, arms=[(-8, -16), (8, -16)])
# maracas player
player(205, 432, R, arms=[(-12, -6), (12, -6)])
for s in (-1, 1):
    c.ellipse(205 + s * 15, 424, 3, 3, fill=Y, outline=K, width=0.6)

# --- house: rows of seats and heads ----------------------------------------
c.rect(0, STAGE_BOTTOM + 7, W, H, fill=K)
for r_ in range(6):
    y = STAGE_BOTTOM + 20 + r_ * 22
    c.line([(0, y + 12), (W, y + 12)], B, 0.8)
    for s in range(17):
        x = 8 + s * 23.5 + (r_ % 2) * 11
        c.rect(x - 9, y - 2, x + 9, y + 10, fill=R, outline=K, width=0.6)
        c.rect(x - 9, y + 7, x + 9, y + 10, fill=mix(R, K, 0.5))
        if random.random() < 0.82:
            hc = random.choice([K, K, Y, R, Wh])
            c.ellipse(x, y + 2, 5, 5, fill=hc if hc != K else B, outline=K, width=0.5)
# title plate on the stage lip
c.rect(110, 452, 290, 470, fill=K)
c.text((200, 461), "MUSIC FOR 18 MUSICIANS · 1976", Y, 7.5, anchor="mm")
c.save()
