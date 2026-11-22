"""The shingle beach at Aldeburgh, seen twice: Dawn (slot 1) and Moonlight (slot 5).
Same vantage, same generator, different light - and at night one boat is gone."""
import math, random
from common import *

HOR = 250           # horizon
LX = 262            # x of the sun / moon


def shore_y(x):
    return 392 + 0.07 * x + 5 * math.sin(x / 55.0 + 1.0)


def boat(d, cx, cy, L, top, mid, bot, reg, night=False, sail=R):
    h = L * 0.17
    N = 40
    tp, bt = [], []
    for i in range(N + 1):
        t = i / N
        x = cx - L / 2 + t * L
        u = 2 * t - 1
        yt = cy - h * (0.95 + 0.5 * u * u + (0.18 if u < 0 else 0) * u * u)
        yb = cy - h * (1.25 * abs(u) ** 3.2) if u < 0 else cy - h * 0.55 * abs(u) ** 4
        tp.append((x, yt)); bt.append((x, min(yb, cy)))
    bt[0] = tp[0]
    lerp = lambda f: [(a[0], a[1] + (b[1] - a[1]) * f) for a, b in zip(tp, bt)]
    ink = WH if night else K
    # props
    for px in (cx - L * 0.2, cx + L * 0.22):
        d.line([(px, cy - h * 0.5), (px + 7, cy + 5)], ink, 1.6)
    d.poly(tp + bt[::-1], fill=bot)
    d.poly(tp + lerp(0.36)[::-1], fill=mid)
    d.poly(tp + lerp(0.2)[::-1], fill=top)
    for f in (0.2, 0.36, 0.52, 0.68, 0.84):       # clinker strakes
        d.line(lerp(f), ink if f < 0.4 or not night else B, 0.7)
    for i in range(3, N, 3):                       # nail heads
        for f in (0.28, 0.6):
            p = lerp(f)[i]
            d.rect(p[0], p[1], p[0] + 0.7, p[1] + 0.7, fill=ink)
    d.line(tp + bt[::-1] + [tp[0]], ink, 1.2)
    d.line(tp, ink, 2.0)                            # gunwale
    # rudder + stem post
    d.poly([(cx + L / 2, cy - h * 1.3), (cx + L / 2 + 5, cy - h * 1.2), (cx + L / 2 + 5, cy - 2), (cx + L / 2, cy - h * 0.5)], fill=ink)
    d.line([(cx - L / 2, tp[0][1] - 4), tp[0]], ink, 1.6)
    # cuddy
    x0, x1 = cx + L * 0.14, cx + L * 0.32
    yb_ = cy - h * 1.0
    d.poly([(x0, yb_), (x0 + 2, yb_ - h * 0.75), (x1, yb_ - h * 0.75), (x1 + 1, yb_)], fill=WH if not night else K, outline=ink, w=1)
    d.rect(x0 + 5, yb_ - h * 0.6, x0 + 11, yb_ - h * 0.22, fill=(Y if night else K))
    d.rect(x0 + 14, yb_ - h * 0.6, x0 + 20, yb_ - h * 0.22, fill=(Y if night else K))
    # mast, yard, furled sail, stays
    mx = cx - L * 0.14
    my0, my1 = cy - h * 1.0, cy - h * 1.0 - L * 0.5
    d.line([(mx, my0), (mx, my1)], ink, 1.8)
    d.line([(mx, my1 + 3), tp[0]], ink, 0.5)
    d.line([(mx, my1 + 3), (cx + L / 2, cy - h * 1.3)], ink, 0.5)
    ya, yb2 = (mx - L * 0.2, my1 + L * 0.2), (mx + L * 0.3, my1 + L * 0.1)
    d.line([ya, yb2], sail, 4.2)
    d.line([ya, yb2], ink, 0.6)
    for i in range(1, 9):
        t = i / 9
        px, py = ya[0] + (yb2[0] - ya[0]) * t, ya[1] + (yb2[1] - ya[1]) * t
        d.line([(px - 0.6, py - 2.6), (px + 0.6, py + 2.6)], ink, 0.6)
    d.poly([(mx, my1), (mx + 13, my1 + 3), (mx, my1 + 6)], fill=R if not night else B)   # pennant
    # registration
    d.text(cx - L * 0.31, cy - h * 1.12 + (h * 0.2), reg, WH if top != WH else K, size=max(6.5, L * 0.055), font="sans")


def hut(d, x, y, w, h, night, door=R, sign=None):
    ink = B if night else WH
    d.poly([(x, y), (x, y - h), (x + w / 2, y - h - w * 0.32), (x + w, y - h), (x + w, y)], fill=K)
    for i in range(1, int(w // 4)):
        d.line([(x + i * 4, y), (x + i * 4, y - h - w * 0.32 * (1 - abs(i * 4 - w / 2) / (w / 2)) + 2)], ink, 0.45)
    d.line([(x - 3, y - h + 2), (x + w / 2, y - h - w * 0.32 - 1), (x + w + 3, y - h + 2)], ink if night else K, 1.6)
    d.rect(x + w * 0.12, y - h * 0.62, x + w * 0.42, y, fill=door, outline=ink, w=0.6)
    wx0, wy0 = x + w * 0.56, y - h * 0.62
    d.rect(wx0, wy0, wx0 + w * 0.3, wy0 + h * 0.34, fill=Y if night else WH, outline=ink, w=0.6)
    d.line([(wx0 + w * 0.15, wy0), (wx0 + w * 0.15, wy0 + h * 0.34)], K, 0.6)
    d.line([(wx0, wy0 + h * 0.17), (wx0 + w * 0.3, wy0 + h * 0.17)], K, 0.6)
    if sign:
        d.rect(x + 3, y - h - 1, x + w - 3, y - h + 8, fill=WH, outline=K, w=0.5)
        d.text(x + w / 2, y - h + 3.6, sign, K, size=5.6, font="sans")
    # stovepipe
    d.rect(x + w * 0.78, y - h - w * 0.3, x + w * 0.84, y - h - 2, fill=K, outline=ink, w=0.4)


def pots(d, x, y, n, night, rng):
    ink = B if night else K
    for r in range(n):
        for c in range(n - r):
            px, py = x + c * 13 + r * 6.5, y - r * 8
            d.pie(px, py, 6.5, 9, 180, 360, fill=K if night else Y)
            d.arc(px, py, 6.5, 9, 180, 360, ink, 0.8)
            d.line([(px - 6.5, py), (px + 6.5, py)], ink, 1)
            for k in (-3, 0, 3):
                d.arc(px + k, py, 3.2, 9, 180, 360, ink, 0.4)
            d.line([(px - 5.6, py - 4.5), (px + 5.6, py - 4.5)], ink, 0.4)


def render(night):
    rng = random.Random(22)
    d = D(K if night else WH)
    # ------------------------------------------------------------ sky
    if not night:
        y = 0.0
        while y < HOR:                               # engraved gradient: yellow rules thickening to the horizon
            t = (y / HOR) ** 1.7
            d.rect(0, y, W, y + 0.5 + 3.6 * t, fill=Y)
            y += 4.2
        for i in range(9):                           # red rules hugging the horizon
            yy = HOR - 2 - i * 4.2
            d.rect(0, yy, W, yy + max(0.5, 2.6 - i * 0.3), fill=R)
        # sun, half risen, sliced
        d.pie(LX, HOR, 37, 37, 180, 360, fill=WH)
        d.pie(LX, HOR, 33, 33, 180, 360, fill=R)
        for i in range(5):
            d.rect(LX - 40, HOR - 4 - i * 5.5, LX + 40, HOR - 4 - i * 5.5 + 0.8 + (4 - i) * 0.35, fill=Y)
        # stratus streaks, hatched in blue
        for (cx, cy, L, hh) in [(90, 60, 150, 12), (300, 38, 170, 9), (210, 112, 230, 13), (60, 150, 140, 9), (350, 165, 150, 8), (150, 196, 190, 7), (320, 214, 120, 5), (40, 228, 100, 4)]:
            for k in range(int(hh * 2)):
                yy = cy - hh / 2 + k * 0.5 * 1.25
                f = 1 - abs((yy - cy) / (hh / 2 + 0.5)) ** 1.5
                half = L / 2 * f * rng.uniform(0.75, 1.0)
                off = rng.uniform(-10, 10)
                if k % 2 == 0:
                    d.line([(cx - half + off, yy), (cx + half + off, yy)], B, 0.75)
                elif f > 0.5:
                    d.line([(cx - half * 0.6 + off, yy), (cx + half * 0.5 + off, yy)], WH, 0.9)
        # gulls, rising like the opening violin line of 'Dawn'
        for i in range(19):
            t = i / 18
            gx = 28 + t * 215 + rng.uniform(-9, 9)
            gy = 205 - 150 * math.sin(t * math.pi * 0.62) ** 1.3 + rng.uniform(-10, 10)
            gull(d, gx, gy, 3.2 + 6.5 * (1 - t) ** 1.2 + rng.uniform(0, 1.5), K, 1.1)
    else:
        for i in range(330):                         # stars
            x, y = rng.uniform(0, W), rng.uniform(0, HOR - 6)
            m = rng.random()
            if (x - LX) ** 2 + (y - 92) ** 2 < 62 ** 2:
                continue
            if m > 0.975:
                d.line([(x - 2.4, y), (x + 2.4, y)], WH, 0.5); d.line([(x, y - 2.4), (x, y + 2.4)], WH, 0.5)
                d.ell(x, y, 0.9, fill=WH)
            else:
                d.ell(x, y, 0.35 + 0.5 * m * m, fill=WH if m > 0.25 else B)
        for (px, py, r) in [(0, 0, 1.2), (5, -3, 1.0), (9, 2, 1.1), (3, 5, 0.8), (-4, 4, 0.9), (12, -5, 0.7), (-7, -2, 0.7)]:
            d.ell(338 + px, 60 + py, r, fill=WH)     # Pleiades, which this moon is walking towards
        d.ell(70, 150, 2.0, fill=Y); d.line([(64.5, 151.5), (75.5, 148.5)], Y, 0.6)   # Saturn
        # halo rings, dotted
        for rr, n in ((52, 70), (60, 60)):
            for i in range(n):
                a = 2 * math.pi * i / n
                d.ell(LX + rr * math.cos(a), 92 + rr * math.sin(a), 0.6, fill=B)
        # the moon: waxing gibbous, 95 %
        d.ell(LX, 92, 37, fill=WH)
        mr = random.Random(5)
        for (mx, my, mrx, mry) in [(-10, -12, 13, 9), (6, -16, 9, 7), (12, -2, 8, 10), (-14, 6, 7, 9), (2, 10, 11, 6), (16, 14, 5, 4)]:
            for _ in range(int(mrx * mry * 0.55)):    # maria, stippled
                a, q = mr.uniform(0, 6.283), mr.random() ** 0.5
                d.ell(LX + mx + mrx * q * math.cos(a), 92 + my + mry * q * math.sin(a), 0.6, fill=B)
        for (cxr, cyr, rr) in [(-20, 22, 3), (20, -22, 2.4), (-2, 26, 2), (25, 8, 1.8), (-26, -8, 2)]:
            d.ell(LX + cxr, 92 + cyr, rr, outline=B, w=0.6)
        for i in range(-36, 37):                     # the 5 % still dark, on the left limb
            yy = 92 + i
            xe = math.sqrt(max(0, 37 ** 2 - i * i))
            d.line([(LX - xe - 1, yy), (LX - xe * 0.90 + 0.4, yy)], K, 1.2)
        # thin cloud bars
        for (cx, cy, L, hh) in [(110, 70, 150, 6), (60, 200, 150, 6), (330, 180, 160, 7), (200, 228, 220, 5), (330, 120, 90, 4)]:
            for k in range(int(hh)):
                yy = cy - hh / 2 + k * 1.6
                half = L / 2 * (1 - abs(k - hh / 2) / hh) * rng.uniform(0.6, 1)
                off = rng.uniform(-12, 12)
                d.line([(cx - half + off, yy), (cx + half + off, yy)], B, 0.6)
    # ------------------------------------------------------------ sea
    d.rect(0, HOR, W, 440, fill=K if night else B)
    d.line([(0, HOR), (W, HOR)], K if not night else B, 0.8)
    y = HOR + 2.0
    row = 0
    while y < 430:
        t = (y - HOR) / 170
        gap = 1.8 + 7.5 * t
        x = rng.uniform(-30, 0)
        while x < W:
            ln = rng.uniform(3, 9) + 46 * t * rng.random()
            dx = abs((x + ln / 2) - LX)
            spread = 10 + 62 * t
            inpath = dx < spread * rng.uniform(0.5, 1.15)
            if night:
                col = (WH if rng.random() > 0.22 else Y) if inpath else B
                wd = (0.9 + 1.5 * t) if inpath else 0.45 + 0.7 * t
                if not inpath and rng.random() < 0.35:
                    col = None
            else:
                col = (Y if rng.random() > 0.3 else (R if t < 0.25 else WH)) if inpath else (WH if rng.random() > 0.3 else K)
                wd = 0.6 + 1.5 * t
            if col:
                pts = [(x + k * ln / 6, y + 0.9 * t * math.sin(k * 1.1 + row)) for k in range(7)]
                d.line(pts, col, wd)
            x += ln + rng.uniform(2, 8 + 22 * t) * (0.45 if inpath else 1)
        y += gap; row += 1
    # a far trawler on the horizon, and a groyne walking into the water
    tx = 95
    d.poly([(tx - 9, HOR - 0.5), (tx - 7, HOR - 3), (tx + 8, HOR - 3), (tx + 6, HOR - 0.5)], fill=WH if night else K)
    d.rect(tx - 1, HOR - 7, tx + 3, HOR - 3, fill=WH if night else K)
    d.line([(tx - 5, HOR - 3), (tx - 5, HOR - 11)], WH if night else K, 0.5)
    if night:
        d.ell(tx - 5, HOR - 11.5, 1, fill=R)
    else:
        for k in range(5):
            d.ell(tx + 4 + k * 3, HOR - 9 - k * 1.6, 1 + k * 0.4, fill=K if k % 2 else WH, outline=K, w=0.4)
    # ------------------------------------------------------------ surf + shingle
    shore = [(x, shore_y(x)) for x in range(-4, W + 8, 4)]
    foam = [(x, yv - 9 - 3 * math.sin(x / 9.0) - 2 * math.sin(x / 23.0 + 2)) for x, yv in shore]
    d.poly(foam + [(W + 4, H), (-4, H)], fill=WH)
    for k in range(3):                               # lacework inside the foam
        for x in range(-4, W, 7):
            yy = shore_y(x) - 7 + k * 2.6
            d.arc(x + (k * 3.5) % 7, yy, 3.6, 2.2, 0, 180, B, 0.5)
    base = K if night else Y
    d.poly(shore + [(W + 4, H), (-4, H)], fill=base)
    wet = [(x, yv + 6 + 2 * math.sin(x / 17.0)) for x, yv in shore]
    if not night:
        d.poly(shore + wet[::-1], fill=K)
    # groyne posts
    for i in range(11):
        t = i / 10
        gx, gy = 352 - t * 70, 470 - t * 100
        hh = 26 - 14 * t
        ww = 5.5 - 2.5 * t
        d.rect(gx, gy - hh, gx + ww, gy, fill=K, outline=(B if night else None), w=0.5)
        d.rect(gx, gy - hh, gx + ww, gy - hh + 1.3, fill=WH if not night else B)
        if gy < shore_y(gx) - 2:
            d.arc(gx + ww / 2, gy, ww * 1.3, 1.8, 0, 360, WH, 0.6)
    # pebbles, back to front
    def pebbles(y0, y1, xfilter=None, dens=1.0):
        y = y0
        while y < y1:
            t = max(0.0, (y - 392) / 208)
            s = 1.1 + 6.2 * t ** 1.25
            x = rng.uniform(-s, 0)
            while x < W + s:
                yy = y + rng.uniform(-s * 0.5, s * 0.5)
                if yy > shore_y(x) + 1 and (xfilter is None or xfilter(x, yy)) and rng.random() < dens:
                    rx, ry = s * rng.uniform(0.7, 1.25), s * rng.uniform(0.45, 0.8)
                    q = rng.random()
                    if night:
                        fill = B if q < 0.5 else K
                        ol = B
                        if q > 0.93:
                            fill = WH
                    else:
                        wetz = yy < shore_y(x) + 8
                        fill = WH if q < 0.50 else Y if q < 0.88 else R if q < 0.93 else K if q < 0.97 else B
                        if wetz:
                            fill = B if q < 0.5 else K if q < 0.8 else WH
                        ol = K
                    d.ell(x, yy, rx, ry, fill=fill, outline=ol if s > 2.2 else None, w=0.55)
                    if s > 3.6 and fill not in (WH,) :
                        d.arc(x - rx * 0.15, yy - ry * 0.15, rx * 0.55, ry * 0.5, 190, 290, WH if not night or fill == B else B, 0.55)
                    if s > 4.5 and q < 0.2:
                        d.line([(x - rx * 0.5, yy + ry * 0.2), (x + rx * 0.6, yy - ry * 0.1)], K if not night else B, 0.45)
                x += s * rng.uniform(1.5, 2.3)
            y += s * 0.95
    pebbles(390, 540)
    # ------------------------------------------------------------ things on the beach
    hut(d, 8, 452, 54, 40, night, door=R if not night else K, sign=None if night else "FRESH FISH")
    hut(d, 66, 440, 34, 26, night, door=B if not night else K)
    # drying net on poles
    nx0, nx1, ny = 296, 392, 478
    ink = B if night else K
    for px in (nx0, (nx0 + nx1) / 2, nx1):
        d.line([(px, ny + 26), (px, ny - 30)], WH if night else K, 1.5)
    sag = lambda x, k: ny - 28 + k * 5.2 + (5 + k * 0.8) * math.sin(math.pi * ((x - nx0) / (nx1 - nx0) * 2 % 1))
    for k in range(9):
        d.line([(x, sag(x, k)) for x in range(nx0, nx1 + 1, 2)], ink, 0.5)
    for x in range(nx0, nx1 + 1, 4):
        d.line([(x, sag(x, 0)), (x + (2 if (x // 4) % 2 else -2), sag(x, 8))], ink, 0.45)
    for x in range(nx0 + 6, nx1, 12):
        d.ell(x, sag(x, 0), 1.9, fill=R if not night else WH, outline=ink, w=0.4)
    # second, smaller boat - present at dawn, gone to sea by night
    if not night:
        boat(d, 232, 428, 92, B, WH, B, "LT 13", sail=WH)
        # the fisherman, looking out
        fx, fy = 300, 420
        d.poly([(fx - 4.5, fy), (fx - 4, fy - 15), (fx - 6, fy - 22), (fx + 6, fy - 22), (fx + 4.5, fy - 12), (fx + 5, fy)], fill=K)
        d.ell(fx, fy - 26, 3.6, fill=K)
        d.poly([(fx - 7, fy - 27), (fx + 6, fy - 28.5), (fx + 2.5, fy - 31.5), (fx - 3, fy - 31)], fill=Y, outline=K, w=0.5)
        d.line([(fx - 2, fy), (fx - 2, fy + 6)], K, 2.4); d.line([(fx + 2.5, fy), (fx + 2.5, fy + 6)], K, 2.4)
        d.line([(fx + 5, fy - 20), (fx + 10, fy - 8)], K, 2)
    else:
        for k, sx in enumerate((196, 214, 232, 250, 268)):      # skids and the furrow where LT 13 stood
            d.line([(sx - 6, 431 - k * 0.6), (sx + 8, 425 - k * 0.6)], WH, 1.6)
        d.line([(182, 432), (232, 426), (290, 412), (318, 403)], B, 1.8)
        d.line([(182, 435), (232, 429), (290, 415), (320, 405)], B, 0.7)
    # main boat
    boat(d, 176, 520, 216, K if not night else B, WH, R if not night else K, "LT 22", night=night, sail=R if not night else WH)
    pots(d, 22, 540, 4, night, rng)
    # winch + chain to the boat
    wx, wy = 330, 548
    d.rect(wx - 12, wy - 16, wx + 12, wy, fill=K, outline=WH if night else K, w=0.7)
    d.ell(wx, wy - 16, 9, fill=K if night else R, outline=WH if night else K, w=1.2)
    for a in range(0, 360, 45):
        d.line([(wx, wy - 16), (wx + 9 * math.cos(math.radians(a)), wy - 16 + 9 * math.sin(math.radians(a)))], WH if night else K, 0.6)
    d.line([(wx + 9, wy - 16), (wx + 22, wy - 26)], WH if night else K, 1.4)
    for i in range(14):
        t = i / 13
        d.ell(wx - 12 - t * 34, wy - 6 - t * 14 + 5 * math.sin(t * math.pi), 1.5, outline=WH if night else K, w=0.6)
    # buoys, crate, anchor
    for (bx, by, c) in [(362, 562, R), (374, 568, Y), (352, 572, WH)]:
        d.ell(bx, by, 6, fill=(c if not night else K), outline=WH if night else K, w=0.9)
        d.line([(bx - 6, by), (bx + 6, by)], WH if night else K, 0.6)
        d.ell(bx, by - 7, 1.6, outline=WH if night else K, w=0.6)
    ax, ay = 110, 560
    aink = WH if night else K
    d.line([(ax, ay - 20), (ax, ay)], aink, 2); d.line([(ax - 7, ay - 15), (ax + 7, ay - 15)], aink, 1.6)
    d.arc(ax, ay - 9, 10, 9, 20, 160, aink, 2); d.ell(ax, ay - 22.5, 2.6, outline=aink, w=1)
    # foreground stones over the feet of things
    pebbles(540, 612)
    pebbles(500, 540, xfilter=lambda x, y: x < 60 or x > 290, dens=0.5)
    d.save()
