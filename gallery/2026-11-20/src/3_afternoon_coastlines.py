"""III. Coastlines are not circles — a sea chart of an fBm island: engraved water-lines,
soundings, rhumbs, contours, towns, and the coast walked with dividers of five lengths
(the numbers in the table are measured from this very coastline). Paper and blue in charge."""
import numpy as np
from PIL import Image, ImageDraw
from common import *

rng = np.random.default_rng(1967)          # the year of "How long is the coast of Britain?"
PIC_H = H - 26
p = Plate(WH)

# --- the island ------------------------------------------------------------------
f = fbm(42, scale=150, octaves=8, gain=0.62)
cx, cy = 205, 320
rr = np.hypot((XX - cx) / 170.0, (YY - cy) / 215.0)
elev = f + 0.42 * (1 - rr ** 1.6) - 0.70
elev[(YY < 22) | (YY > PIC_H - 22) | (XX < 22) | (XX > W - 22)] = -1
land = elev > 0
m = mandel(64)                              # the islet
isl = np.zeros((H, W), bool); isl[494:494 + m.shape[0], 300:364] = m
land &= ~grow(isl, 6)
elev = np.where(isl, 0.02, elev)
land |= isl

# main island = the component under the highest point
py0, px0 = np.unravel_index(np.argmax(np.where(isl, -1, elev)), elev.shape)
im = Image.fromarray((land * 255).astype(np.uint8), "L").copy()
ImageDraw.floodfill(im, (int(px0), int(py0)), 128)
main = np.asarray(im) == 128

# distance from land, by repeated dilation (square and plus alternate: ~octagonal)
def plus(mk):
    o = mk.copy()
    o[1:, :] |= mk[:-1, :]; o[:-1, :] |= mk[1:, :]; o[:, 1:] |= mk[:, :-1]; o[:, :-1] |= mk[:, 1:]
    return o
dist = np.zeros((H, W), np.int16); cur = land.copy()
for i in range(1, 46):
    nxt = grow(cur, 1) if i % 2 else plus(cur)
    dist[nxt & ~cur] = i
    cur = nxt
dist[~cur] = 60
sea = ~land

# --- sea: shallows, water-lines, rhumbs ----------------------------------------
p.put(sea & screen(np.clip(0.62 - dist / 22.0, 0, 0.6)), B)
for dline in (2, 5, 9, 14, 20, 27, 35, 44):
    p.put(sea & (dist == dline), B)
RX, RY = 318, 108                           # compass rose
ang = np.arctan2(YY - RY, XX - RX); rad = np.hypot(XX - RX, YY - RY)
for k in range(32):
    a = k * np.pi / 16
    dd = np.abs((XX - RX) * np.sin(a) - (YY - RY) * np.cos(a))
    fwd = ((XX - RX) * np.cos(a) + (YY - RY) * np.sin(a)) > 0
    dash = (np.floor(rad) % (2 if k % 4 == 0 else 4)) == 0
    p.put(sea & (dist > 3) & (dd < 0.5) & fwd & dash, K if k % 2 == 0 else R)

# --- land: tint, forest, relief ---------------------------------------------------
p.put(land, Y)
p.put(land & screen(np.clip(0.75 - elev * 9, 0, 0.75)), WH)          # pale coastal plain
forest = land & (fbm(8, scale=38, octaves=4) > 0.53) & (elev > 0.025) & (elev < 0.17)
p.put(forest, G)
p.put(forest & screen(0.3 + 0 * elev), K)
high = land & (elev > 0.16)
p.put(high & screen(np.clip((elev - 0.16) * 7, 0, 0.7)), R)
gy, gx = np.gradient(blur(np.clip(elev * 3, 0, 1), 1.5))
shade = np.clip((gx * 0.7 + gy * 0.7) * 40, 0, 0.8)                  # light from the NW
p.put(land & (elev > 0.06) & hatch(shade, 45, 3), K)
lev = np.floor(elev / 0.03)
cont = np.zeros((H, W), bool)
cont[:, :-1] |= lev[:, :-1] != lev[:, 1:]; cont[:-1, :] |= lev[:-1, :] != lev[1:, :]
p.put(cont & land & (elev > 0.03) & ~isl, K)
p.put(grow(land, 1) & ~land, K)
p.put(edge(land), K)

# --- rivers: walk downhill from the heights ----------------------------------------
sm = blur(np.clip(elev + 0.5, 0, 1), 3)
with p.draw() as d:
    for _ in range(9):
        ys_, xs_ = np.nonzero(main & (elev > 0.13))
        i = rng.integers(len(ys_)); x, y = float(xs_[i]), float(ys_[i]); pts = [(x, y)]
        for _ in range(400):
            xi, yi = int(x), int(y)
            if not (2 < xi < W - 3 and 2 < yi < H - 3) or not land[yi, xi]:
                break
            g = np.array([sm[yi, xi + 2] - sm[yi, xi - 2], sm[yi + 2, xi] - sm[yi - 2, xi]])
            n = np.linalg.norm(g)
            if n < 1e-5:
                break
            x -= g[0] / n * 1.5 + rng.normal(0, 0.25); y -= g[1] / n * 1.5 + rng.normal(0, 0.25)
            pts.append((x, y))
        if len(pts) > 12:
            d.line(pts, fill=B, width=1)
            d.line(pts[len(pts) * 2 // 3:], fill=B, width=2)

# --- the coast walked with dividers -------------------------------------------------
def trace(mask, start):
    nb = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
    y, x = start; out = [(x, y)]; dirn = 0
    for _ in range(40000):
        for k in range(8):
            j = (dirn + 6 + k) % 8
            ny, nx = y + nb[j][0], x + nb[j][1]
            if mask[ny, nx]:
                y, x, dirn = ny, nx, j; break
        if (y, x) == start:
            break
        out.append((x, y))
    return np.array(out, float)
ys_, xs_ = np.nonzero(main)
start = (int(ys_[0]), int(xs_[ys_ == ys_[0]][0]))
coast = trace(main, start)
def walk(r):
    pts = [coast[0]]; i = 0
    while True:
        dd = np.hypot(*(coast[i + 1:] - pts[-1]).T)
        far = np.nonzero(dd >= r)[0]
        if len(far) == 0:
            break
        i = i + 1 + far[0]; pts.append(coast[i])
    tail = np.hypot(*(pts[-1] - coast[0]))
    return np.array(pts), (len(pts) - 1) * r + tail
rulers = [64, 32, 16, 8, 4]
walks = {r: walk(r) for r in rulers}
lengths = [walks[r][1] for r in rulers]
slope = np.polyfit(np.log(rulers), np.log(lengths), 1)[0]
D = 1 - slope
MILE = 2.5                                  # miles per pixel, by decree

with p.draw() as d:
    poly = [tuple(q) for q in walks[64][0]] + [tuple(coast[0])]
    d.line(poly, fill=R, width=2)
    for q in poly:
        d.ellipse([q[0] - 3, q[1] - 3, q[0] + 3, q[1] + 3], fill=WH, outline=R)
        d.point(q, fill=R)

    # towns, a road between them, names
    f9, f10, f12 = font(9), font(10), font(12)
    names = ["Port Benoît", "Hausdorff", "Richardson", "Koch Pt", "Julia Bay", "Peano", "Cantor"]
    step = len(coast) // len(names)
    towns = []
    for k, nm in enumerate(names):
        q = coast[(k * step + step // 3) % len(coast)]
        v = np.array([cx, cy]) - q; v /= np.linalg.norm(v)
        t = q + v * 7
        towns.append(t)
    for a, b in zip(towns, towns[1:] + towns[:1]):
        n = int(np.hypot(*(b - a)) / 4)
        mid = (a + b) / 2 + (np.array([cx, cy]) - (a + b) / 2) * 0.25
        for s in range(n):
            u = s / max(1, n)
            q = (1 - u) ** 2 * a + 2 * u * (1 - u) * mid + u ** 2 * b
            if land[int(q[1]), int(q[0])] and s % 2 == 0:
                d.rectangle([q[0], q[1], q[0] + 1, q[1] + 1], fill=R)
    for t, nm in zip(towns, names):
        d.rectangle([t[0] - 3, t[1] - 3, t[0] + 3, t[1] + 3], fill=R, outline=K)
        d.point((t[0], t[1]), fill=WH)
        tw = d.textlength(nm, font=f9)
        tx = t[0] + 6 if t[0] < cx else t[0] - 6 - tw
        tx = min(max(26, tx), W - 26 - tw)
        d.rectangle([tx - 1, t[1] - 6, tx + tw, t[1] + 5], fill=WH)
        d.text((tx, t[1] - 6), nm, font=f9, fill=K)
    # summit
    d.polygon([(px0, py0 - 6), (px0 - 5, py0 + 3), (px0 + 5, py0 + 3)], fill=K)
    d.text((px0 + 7, py0 - 6), "1924", font=f9, fill=K)
    d.text((286, 482), "I. Mandelbrot", font=f9, fill=K)

    # soundings
    for _ in range(140):
        x, y = int(rng.integers(30, W - 40)), int(rng.integers(30, PIC_H - 34))
        if dist[y - 4:y + 8, x - 2:x + 14].min() < 7 or (x < 150 and y > PIC_H - 76) or (270 < x < 372 and 470 < y < 500):
            continue
        depth = int(dist[y, x] * 1.3 + rng.integers(0, 9))
        d.text((x, y), str(depth), font=font(8, "DejaVuSans"), fill=B if depth < 40 else K)

    # compass rose
    for ring, col in ((34, K), (31, K), (22, R)):
        d.ellipse([RX - ring, RY - ring, RX + ring, RY + ring], outline=col)
    for k in range(64):
        a = k * np.pi / 32
        r0 = 31 if k % 2 else 28
        d.line([(RX + r0 * np.cos(a), RY + r0 * np.sin(a)), (RX + 34 * np.cos(a), RY + 34 * np.sin(a))], fill=K)
    for k, (ln, wd) in enumerate([(44, 8)] * 4 + [(30, 6)] * 4 + [(20, 3)] * 8):
        a = (k * np.pi / 2 if k < 4 else np.pi / 4 + (k - 4) * np.pi / 2 if k < 8 else np.pi / 8 + (k - 8) * np.pi / 4) - np.pi / 2
        tip = (RX + ln * np.cos(a), RY + ln * np.sin(a))
        l = (RX + wd * np.cos(a + np.pi / 2), RY + wd * np.sin(a + np.pi / 2))
        r_ = (RX + wd * np.cos(a - np.pi / 2), RY + wd * np.sin(a - np.pi / 2))
        d.polygon([tip, l, (RX, RY)], fill=K, outline=K)
        d.polygon([tip, r_, (RX, RY)], fill=WH if k >= 4 else Y, outline=K)
    d.polygon([(RX, RY - 60), (RX - 6, RY - 46), (RX + 6, RY - 46)], fill=R, outline=K)
    d.text((RX - 4, RY - 76), "N", font=f12, fill=K)
    d.ellipse([RX - 3, RY - 3, RX + 3, RY + 3], fill=R, outline=K)

    # cartouche with the measurements
    bx, by, bw, bh = 28, 28, 172, 104
    d.rectangle([bx, by, bx + bw, by + bh], fill=WH, outline=K)
    d.rectangle([bx + 3, by + 3, bx + bw - 3, by + bh - 3], outline=K)
    d.text((bx + 10, by + 8), "HOW LONG IS", font=f12, fill=K)
    d.text((bx + 10, by + 22), "THIS COAST?", font=f12, fill=R)
    d.line([(bx + 10, by + 38), (bx + bw - 10, by + 38)], fill=K)
    d.text((bx + 10, by + 41), "dividers", font=f9, fill=K); d.text((bx + 96, by + 41), "length", font=f9, fill=K)
    for i, (r, L) in enumerate(zip(rulers, lengths)):
        yy = by + 52 + i * 9
        d.text((bx + 10, yy), f"{r * MILE:>5.0f} mi", font=f9, fill=K)
        d.line([(bx + 60, yy + 6), (bx + 60 + r // 2, yy + 6)], fill=R, width=2)
        d.text((bx + 96, yy), f"{L * MILE:,.0f} mi", font=f9, fill=K)
    # scale bar & dimension, bottom left
    sx, sy = 30, PIC_H - 44
    for k in range(5):
        d.rectangle([sx + k * 20, sy, sx + k * 20 + 20, sy + 5], fill=K if k % 2 == 0 else WH, outline=K)
    d.text((sx, sy + 7), "0", font=f9, fill=K); d.text((sx + 88, sy + 7), "250 mi", font=f9, fill=K)
    d.text((sx, sy - 14), f"D = {D:.2f}", font=f12, fill=R)

    # a ship and a whale
    def ship(x, y):
        d.polygon([(x - 12, y), (x + 13, y), (x + 9, y + 6), (x - 8, y + 6)], fill=K)
        for mx, mh in ((-6, 15), (1, 19), (8, 13)):
            d.line([(x + mx, y), (x + mx, y - mh)], fill=K)
            d.polygon([(x + mx - 5, y - 3), (x + mx + 4, y - 3), (x + mx + 3, y - mh + 2), (x + mx - 4, y - mh + 4)], fill=WH, outline=K)
        d.polygon([(x + 1, y - 19), (x + 1, y - 24), (x + 8, y - 21)], fill=R)
        for k in range(4):
            d.line([(x - 16 - k * 6, y + 7 + k % 2), (x - 13 - k * 6, y + 7 + k % 2)], fill=B)
    def spot(x0, y0):
        best_, bq = 1e9, (x0, y0)
        for yy_ in range(40, PIC_H - 50, 6):
            for xx_ in range(40, W - 40, 6):
                if dist[yy_ - 26:yy_ + 10, xx_ - 40:xx_ + 24].min() > 6 and not (xx_ < 215 and yy_ < 150):
                    dq = np.hypot(xx_ - x0, yy_ - y0)
                    if dq < best_:
                        best_, bq = dq, (xx_, yy_)
        return bq
    ship(*spot(70, 470)); ship(*spot(352, 330))
    wx, wy = spot(60, 200)
    d.chord([wx - 14, wy - 7, wx + 14, wy + 9], 180, 360, fill=K)
    d.polygon([(wx + 12, wy), (wx + 21, wy - 7), (wx + 20, wy + 1)], fill=K)
    for k in (-1, 0, 1):
        d.line([(wx - 6, wy - 8), (wx - 6 + k * 5, wy - 17)], fill=B)
    d.point((wx - 8, wy - 2), fill=WH)

# --- the neatline: a graduated border ---------------------------------------------
for i in range(10, 16):
    for sel in (YY == i, YY == PIC_H - 1 - i, XX == i, XX == W - 1 - i):
        box = (XX >= 10) & (XX <= W - 11) & (YY >= 10) & (YY <= PIC_H - 11)
        along = np.where((sel is not None) & ((YY == i) | (YY == PIC_H - 1 - i)), XX, YY)
        p.put(sel & box & ((along // 16) % 2 == 0), K)
        p.put(sel & box & ((along // 16) % 2 == 1), WH)
for o in (9, 16):
    fr = ((XX == o) | (XX == W - 1 - o)) & (YY >= o) & (YY <= PIC_H - 1 - o) | ((YY == o) | (YY == PIC_H - 1 - o)) & (XX >= o) & (XX <= W - 1 - o)
    p.put(fr, K)
outer = (XX < 9) | (XX > W - 10) | (YY < 9) | ((YY > PIC_H - 10) & (YY < PIC_H))
p.put(outer, WH)

p.caption("III", "COASTLINES ARE NOT CIRCLES")
print("rulers", rulers, "lengths", [round(l) for l in lengths], "D", round(D, 3))
p.save()
