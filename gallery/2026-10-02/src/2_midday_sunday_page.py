"""Midday — Sunday Page. An original five-panel space-opera Sunday strip, printed
the 1930s way: black key line, flat inks, Ben-Day dots for every tone."""
import math, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from ink import *

page = Canvas(WH)
GUT = 6


def panel(x0, y0, x1, y1, painter):
    c = Canvas(WH)
    painter(c, x0, y0, x1, y1)
    page.a[y0:y1, x0:x1] = c.a[y0:y1, x0:x1]
    page.draw(lambda d: d.rectangle([x0, y0, x1 - 1, y1 - 1], outline=1, width=3), K)


def caption(c, x, y, lines, size=12, bg=Y):
    f = font(size)
    wmax = max(f.getlength(s) for s in lines)
    h = len(lines) * (size + 2) + 6
    c.draw(lambda d: d.rectangle([x, y, x + wmax + 10, y + h], fill=1), bg)
    c.draw(lambda d: d.rectangle([x, y, x + wmax + 10, y + h], outline=1, width=2), K)
    for i, s in enumerate(lines):
        text(c, (x + 5, y + 4 + i * (size + 2)), s, size, K)


def stars(c, m, n, seed, cols=(WH, Y)):
    rnd = random.Random(seed)
    for _ in range(n):
        x, y = rnd.randrange(W), rnd.randrange(H)
        if m[y, x]:
            col = rnd.choice(cols)
            if rnd.random() < 0.12:
                c.a[max(0, y - 3):y + 4, x] = col; c.a[y, max(0, x - 3):x + 4] = col
            else:
                c.a[y:y + 2, x:x + 2] = col


def ship(c, cx, cy, s, ang, flame=True):
    """Classic finned rocket, pointing along ang (radians, 0 = right)."""
    ca, sa = math.cos(ang), math.sin(ang)
    T = lambda u, v: (cx + (u * ca - v * sa) * s, cy + (u * sa + v * ca) * s)
    body = [T(40, 0), T(26, 7), T(-6, 9), T(-28, 7), T(-28, -7), T(-6, -9), T(26, -7)]
    if flame:
        c.draw(lambda d: d.polygon([T(-28, -6), T(-28, 6), T(-62, 0)], fill=1), R)
        c.draw(lambda d: d.polygon([T(-28, -3), T(-28, 3), T(-48, 0)], fill=1), Y)
    for v in (-1, 1):
        fin = [T(-8, 8 * v), T(-30, 22 * v), T(-36, 20 * v), T(-26, 6 * v)]
        c.draw(lambda d: d.polygon(fin, fill=1), Y)
        c.draw(lambda d: d.line(fin + [fin[0]], fill=1, width=2), K)
    m = Canvas.mask(lambda d: d.polygon(body, fill=1))
    c.fill(m, WH)
    vproj = (-(XX - cx) * sa + (YY - cy) * ca) / s
    c.benday(m & (vproj > 2), R, pitch=4, r=1.4)
    c.fill(m & (vproj > 5), R)
    c.draw(lambda d: d.line(body + [body[0]], fill=1, width=2), K)
    for u in (16, 2):
        p = T(u, -1)
        c.draw(lambda d: d.ellipse([p[0] - 3 * s, p[1] - 3 * s, p[0] + 3 * s, p[1] + 3 * s], fill=1), B)
        c.draw(lambda d: d.ellipse([p[0] - 3 * s, p[1] - 3 * s, p[0] + 3 * s, p[1] + 3 * s], outline=1, width=1), K)


# --- masthead ---------------------------------------------------------------------
page.draw(lambda d: d.rectangle([0, 0, W, 78], fill=1), Y)
page.benday(YY < 78, R, pitch=6, r=1.2)
for i in range(16):  # sunburst behind title
    a0 = i * math.pi / 8
    page.draw(lambda d: d.polygon([(200, 40), (200 + 400 * math.cos(a0), 40 + 400 * math.sin(a0)),
                                   (200 + 400 * math.cos(a0 + 0.12), 40 + 400 * math.sin(a0 + 0.12))], fill=1), Y)
page.fill(YY >= 78, WH)
text(page, (200, 8), "ROCKET", 40, R, anchor="ma", stroke=3, stroke_c=K)
text(page, (200, 48), "★  S U N D A Y  ★", 16, B, anchor="ma", stroke=2, stroke_c=WH)
text(page, (8, 66), "OCT. 2", 10, K)
text(page, (392, 66), "No. 1909", 10, K, anchor="ra")
page.draw(lambda d: d.rectangle([0, 0, W - 1, 77], outline=1, width=3), K)


# --- A: the cruise past the ringed planet ------------------------------------------
def pA(c, x0, y0, x1, y1):
    c.screen(np.ones((H, W), bool), np.clip((YY - y0) / (y1 - y0), 0, 1) * 0.5, K, B)
    stars(c, np.ones((H, W), bool), 500, 3)
    px, py, pr = 300, 200, 70
    ring_back = Canvas.mask(lambda d: d.ellipse([px - 130, py - 26, px + 130, py + 26], outline=1, width=9))
    c.fill(ring_back & (YY < py), Y)
    pl = Canvas.mask(lambda d: d.ellipse([px - pr, py - pr, px + pr, py + pr], fill=1))
    c.fill(pl, R)
    for k in range(-5, 6):  # bands
        c.fill(pl & (np.abs(YY - (py + k * 13 + 0.15 * (XX - px))) < 2 + (k % 3)), Y)
    lit = ((XX - px + 30) ** 2 + (YY - py + 30) ** 2) < (pr * 0.95) ** 2
    c.benday(pl & ~lit, K, pitch=4, r=1.5)
    c.fill(Canvas.mask(lambda d: d.ellipse([px - pr, py - pr, px + pr, py + pr], outline=1, width=2)), K)
    ring_front = ring_back & (YY >= py)
    c.fill(ring_front, Y)
    c.fill(Canvas.mask(lambda d: d.ellipse([px - 130, py - 26, px + 130, py + 26], outline=1, width=1)) & (YY >= py), K)
    c.fill(Canvas.mask(lambda d: d.ellipse([px - 121, py - 17, px + 121, py + 17], outline=1, width=1)) & (YY >= py), K)
    # moonlet
    c.draw(lambda d: d.ellipse([340, 96, 366, 122], fill=1), G)
    c.benday(Canvas.mask(lambda d: d.ellipse([346, 96, 372, 122], fill=1)) & Canvas.mask(lambda d: d.ellipse([340, 96, 366, 122], fill=1)), K, 4, 1.4)
    c.draw(lambda d: d.ellipse([340, 96, 366, 122], outline=1, width=2), K)
    # speed lines and the ship
    for k in range(9):
        yy = 170 + k * 7
        c.draw(lambda d: d.line([x0 + 4, yy, 70 + (k % 3) * 12, yy - 14], fill=1, width=1), WH)
    ship(c, 112, 146, 1.25, -0.28)
    caption(c, x0 + 8, y0 + 8, ["MEANWHILE, PAST THE", "RINGS OF THE RED WORLD..."], 11)


# --- B: the pilot, from behind, facing the alien sun -------------------------------
def pB(c, x0, y0, x1, y1):
    cx = (x0 + x1) // 2
    c.ramp(np.ones((H, W), bool), (YY - y0) / (y1 - y0), [Y, R, K])
    sun = Canvas.mask(lambda d: d.ellipse([x0 + 100, y0 + 46, x0 + 170, y0 + 116], fill=1))
    c.fill(sun, WH)
    for k in range(5):
        c.fill(sun & (np.abs(YY - (y0 + 92 + k * 6)) < 1 + k * 0.5), Y)
    # spiky alien skyline
    pts = [(x0, y1)]
    for x in range(x0, x1 + 8, 8):
        pts.append((x, y0 + 100 + 14 * math.sin(x * 0.7) + (24 if x % 24 == 0 else 0)))
    pts.append((x1, y1))
    c.draw(lambda d: d.polygon(pts, fill=1), G)
    c.hatch(Canvas.mask(lambda d: d.polygon(pts, fill=1)), K, pitch=3, angle=0, width=1)
    # helmet and shoulders
    sh = [(x0 - 4, y1), (x0 + 14, y1 - 46), (cx - 26, y1 - 62), (cx + 26, y1 - 62), (x1 - 14, y1 - 46), (x1 + 4, y1)]
    c.draw(lambda d: d.polygon(sh, fill=1), B)
    c.benday(Canvas.mask(lambda d: d.polygon(sh, fill=1)) & (XX > cx), K, 4, 1.4)
    c.draw(lambda d: d.line(sh, fill=1, width=3), K)
    c.draw(lambda d: d.line([cx, y1 - 60, cx, y1], fill=1, width=2), K)
    for k in range(4):  # harness rivets
        c.draw(lambda d: d.ellipse([cx - 16 + k * 10, y1 - 30, cx - 12 + k * 10, y1 - 26], fill=1), Y)
    hb = [cx - 38, y1 - 132, cx + 38, y1 - 52]
    c.draw(lambda d: d.ellipse(hb, fill=1), WH)
    hm = Canvas.mask(lambda d: d.ellipse(hb, fill=1))
    c.benday(hm & (XX > cx + 4), B, 4, 1.5)
    c.fill(hm & (np.abs(XX - cx) < 4), R)  # crest stripe
    c.draw(lambda d: d.arc([hb[0] + 8, hb[1] + 6, hb[2] - 8, hb[3] - 20], 200, 250, fill=1, width=3), Y)
    c.draw(lambda d: d.ellipse(hb, outline=1, width=3), K)
    c.draw(lambda d: d.line([cx + 22, y1 - 128, cx + 34, y1 - 150], fill=1, width=2), K)  # antenna
    c.draw(lambda d: d.ellipse([cx + 31, y1 - 155, cx + 38, y1 - 148], fill=1), R)
    caption(c, x0 + 6, y0 + 6, ["DAWN ON A", "STRANGE WORLD"], 11, WH)


# --- C: ZZAP! -----------------------------------------------------------------------
def pC(c, x0, y0, x1, y1):
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2 + 6
    ang = np.arctan2(YY - cy, XX - cx)
    rays = (np.floor(ang / (math.pi / 20)) % 2) == 0
    c.fill(rays, B)
    c.benday(~rays, B, 5, 1.6)
    pts = []
    for i in range(28):
        a = i * math.pi * 2 / 28
        r = 78 if i % 2 == 0 else 46 + (i % 4) * 4
        pts.append((cx + r * math.cos(a), cy + r * 0.9 * math.sin(a)))
    c.draw(lambda d: d.polygon(pts, fill=1), Y)
    inner = [(cx + (p[0] - cx) * 0.62, cy + (p[1] - cy) * 0.62) for p in pts]
    c.draw(lambda d: d.polygon(inner, fill=1), WH)
    c.draw(lambda d: d.line(pts + [pts[0]], fill=1, width=3), K)
    text(c, (cx + 2, cy + 2), "ZZAP!", 34, K, anchor="mm")
    text(c, (cx, cy), "ZZAP!", 34, R, anchor="mm", stroke=2, stroke_c=K)
    # the ray itself, entering from the corner
    c.draw(lambda d: d.line([x0, y1 - 10, cx - 50, cy + 30], fill=1, width=7), K)
    c.draw(lambda d: d.line([x0, y1 - 10, cx - 50, cy + 30], fill=1, width=3), WH)
    for k in range(5):
        c.draw(lambda d: d.line([x0 + 10 + k * 12, y1 - 18 - k * 8, x0 + 16 + k * 12, y1 - 6 - k * 8], fill=1, width=2), Y)


# --- D: landing in the fungus jungle ---------------------------------------------------
def pD(c, x0, y0, x1, y1):
    c.ramp(np.ones((H, W), bool), np.clip((YY - y0) / (y1 - y0) * 1.3, 0, 1), [R, Y, WH])
    rnd = random.Random(5)
    # back row of giant mushrooms, green with black dots; front row darker
    for layer, (col, base, scale) in enumerate([(G, y1 - 40, 0.7), (B, y1 - 10, 1.0)]):
        for k in range(7):
            mx = x0 + rnd.uniform(-10, x1 - x0 + 10)
            h = rnd.uniform(50, 110) * scale
            cw = rnd.uniform(26, 50) * scale
            stem = [(mx - 4 * scale, base), (mx + 4 * scale, base), (mx + 3, base - h), (mx - 3, base - h)]
            c.draw(lambda d: d.polygon(stem, fill=1), WH if layer else Y)
            c.draw(lambda d: d.line(stem + [stem[0]], fill=1, width=1), K)
            cap = [mx - cw, base - h + 6, mx + cw, base - h - cw * 0.9]
            capm = Canvas.mask(lambda d: d.pieslice([cap[0], cap[3], cap[2], base - h + cw * 0.9], 180, 360, fill=1))
            c.fill(capm, col)
            c.benday(capm & (XX > mx), K, 4, 1.3)
            for s in range(5):
                sx, sy = mx + rnd.uniform(-cw * 0.6, cw * 0.6), base - h - rnd.uniform(4, cw * 0.6)
                if capm[int(min(sy, H - 1)), int(min(max(sx, 0), W - 1))]:
                    c.draw(lambda d: d.ellipse([sx - 3, sy - 2, sx + 3, sy + 2], fill=1), WH)
            c.draw(lambda d: d.arc([cap[0], cap[3], cap[2], base - h + cw * 0.9], 180, 360, fill=1, width=2), K)
            c.draw(lambda d: d.line([cap[0], base - h, cap[2], base - h], fill=1, width=2), K)
    # ground
    c.draw(lambda d: d.rectangle([x0, y1 - 12, x1, y1], fill=1), K)
    # the rocket, landed on its fins
    rx, rb = x0 + 150, y1 - 12
    ship(c, rx, rb - 60, 1.3, -math.pi / 2, flame=False)
    for k in range(5):  # landing dust
        c.draw(lambda d: d.ellipse([rx - 50 + k * 22, rb - 10, rx - 30 + k * 22, rb + 2], fill=1), WH)
        c.draw(lambda d: d.ellipse([rx - 50 + k * 22, rb - 10, rx - 30 + k * 22, rb + 2], outline=1, width=1), K)
    caption(c, x0 + 6, y0 + 6, ["DOWN AMONG THE", "TOWERING FUNGI!"], 11)


# --- E: next week -----------------------------------------------------------------------
def pE(c, x0, y0, x1, y1):
    c.fill(np.ones((H, W), bool), R)
    c.benday(np.ones((H, W), bool), Y, 5, 1.2, angle=15)
    cx = (x0 + x1) // 2
    c.draw(lambda d: d.rectangle([x0 + 8, y0 + 10, x1 - 8, y1 - 10], fill=1), WH)
    c.draw(lambda d: d.rectangle([x0 + 8, y0 + 10, x1 - 8, y1 - 10], outline=1, width=2), K)
    text(c, (cx, y0 + 18), "NEXT", 18, B, anchor="ma")
    text(c, (cx, y0 + 38), "WEEK:", 18, B, anchor="ma")
    # a small crystal cave mouth
    pts = [(x0 + 18, y1 - 16), (x0 + 28, y0 + 104), (cx - 6, y0 + 96), (cx + 6, y0 + 102),
           (x1 - 26, y0 + 94), (x1 - 18, y1 - 16)]
    c.draw(lambda d: d.polygon(pts, fill=1), K)
    for k in range(6):
        bx = x0 + 26 + k * 13
        c.draw(lambda d: d.polygon([(bx, y1 - 22), (bx + 5, y1 - 34 - (k % 3) * 8), (bx + 10, y1 - 22)], fill=1),
               [B, G, Y][k % 3])
        c.draw(lambda d: d.line([bx + 5, y1 - 32 - (k % 3) * 8, bx + 5, y1 - 26], fill=1, width=1), WH)
    text(c, (cx, y0 + 62), "THE CRYSTAL", 11, K, anchor="ma")
    text(c, (cx, y0 + 76), "CAVES!", 14, R, anchor="ma")


TOP = 84
panel(GUT, TOP, W - GUT, 246, pA)
panel(GUT, 252, 196, 420, pB)
panel(202, 252, W - GUT, 420, pC)
panel(GUT, 426, 270, H - GUT, pD)
panel(276, 426, W - GUT, H - GUT, pE)
page.save()
