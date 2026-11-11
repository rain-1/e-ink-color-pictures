"""Morning — The Port at Sunrise (for Paul Signac, born 11 November 1863).
Divisionism done literally: a continuous-tone picture is painted first, then rebuilt from
~30,000 small brick strokes, each one a *pure* ink. A stroke's ink is drawn by lot between
the two inks whose mixture is nearest the tone underneath, so the eye does the mixing —
which is both Signac's method and exactly how this panel works."""
import math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from kit import *

random.seed(1111); rng = np.random.default_rng(1863)
SUN = (252, 232); HOR = 306

def M(*cw):                       # mix of inks by weight: M((Y,2),(R,1))
    t = sum(w for _, w in cw)
    return tuple(int(sum(c[i] * w for c, w in cw) / t) for i in range(3))

# ---------- 1. the underpainting (continuous tone, 400x600) ----------
tgt = Image.new("RGB", (W, H)); px = np.zeros((H, W, 3), np.float32)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
r = np.hypot(xx - SUN[0], yy - SUN[1])
stops = [(0, M((Wh, 3), (Y, 2))), (34, M((Y, 4), (Wh, 1))), (80, M((Y, 3), (R, 1.3))),
         (135, M((R, 2), (Wh, 2), (Y, 1))), (200, M((Wh, 3), (R, 1), (B, .6))),
         (270, M((Wh, 2.2), (B, 1.4))), (360, M((B, 2.4), (Wh, 1.3))), (520, M((B, 3), (Wh, .6)))]
for (r0, c0), (r1, c1) in zip(stops, stops[1:]):
    m = (r >= r0) & (r < r1); t = ((r - r0) / (r1 - r0))[m][:, None]
    px[m] = np.array(c0) * (1 - t) + np.array(c1) * t
band = (np.sin(r / 9.5) > 0.55)[..., None]          # breathing rings round the sun
px = np.where(band, px * 0.86 + np.array(Wh) * 0.14, px)
# sea: sky mirrored, bluer and greener, with a broken gold road under the sun
sea = yy >= HOR
depth = np.clip((yy - HOR) / (H - HOR), 0, 1)
mirror = px[np.clip((2 * HOR - yy).astype(int), 0, H - 1), xx.astype(int)]
seacol = mirror * (0.55 - 0.3 * depth[..., None]) + np.array(M((B, 3), (G, 1.0), (Wh, 1.6))) * (0.45 + 0.3 * depth[..., None])
road = np.exp(-((xx - SUN[0]) / (10 + 46 * depth)) ** 2) * (0.5 + 0.5 * np.sin(yy * 1.9 + np.sin(xx / 7) * 2))
road = np.clip(road * 1.25, 0, 1)[..., None]
seacol = seacol * (1 - road) + np.array(M((Y, 3), (Wh, 1.6), (R, .5))) * road
px = np.where(sea[..., None], seacol, px)
tgt = Image.fromarray(px.clip(0, 255).astype(np.uint8)); d = ImageDraw.Draw(tgt)
ang = Image.new("L", (W, H), 0); da = ImageDraw.Draw(ang)       # 0 = use field; else angle code
def A(deg): return int(deg % 180) + 1

VIO = M((B, 2), (R, 1.2), (Wh, 1)); DKG = M((G, 2), (B, 1.2), (K, 1.2)); ORG = M((R, 1.5), (Y, 2))
# far hills (the Maures) in three ranges
for base, amp, col, seed in [(272, 22, M((B, 1.6), (Wh, 1.8), (R, .9)), 3), (286, 16, M((B, 3), (Wh, .8), (R, .6)), 7), (298, 9, M((B, 3), (K, 1.2)), 11)]:
    pts = [(0, HOR)] + [(x, base - amp * (0.5 + 0.5 * math.sin(x / 47 + seed) * math.cos(x / 23 + seed * 2)) - (10 if x < 150 else 0) * math.sin(x / 48) ** 2)
                        for x in range(0, W + 1, 4)] + [(W, HOR)]
    d.polygon(pts, fill=col); da.polygon(pts, fill=A(8))
# the town on the right: stacked houses, red roofs, the bell tower
random.seed(5)
x = 262
while x < W:
    w = random.randint(13, 24); h = random.randint(18, 44) + (x - 262) * 0.07
    wall = random.choice([M((Y, 2), (Wh, 2), (R, .6)), M((R, 1.3), (Wh, 2.4)), M((Y, 3), (Wh, 1)), M((Wh, 3), (Y, 1)), ORG])
    d.rectangle([x, HOR - h, x + w, HOR + 2], fill=wall); da.rectangle([x, HOR - h, x + w, HOR + 2], fill=A(90))
    d.polygon([(x - 1, HOR - h), (x + w / 2, HOR - h - 7), (x + w + 1, HOR - h)], fill=M((R, 3), (K, .5)))
    for wy in range(int(HOR - h + 5), HOR - 6, 9):
        for wx in range(int(x + 3), int(x + w - 4), 7):
            d.rectangle([wx, wy, wx + 2, wy + 4], fill=M((B, 2), (K, 1.5)))
    x += w + 1
tx = 322                                               # bell tower, ochre with a red cap
d.rectangle([tx, 212, tx + 17, HOR], fill=M((Y, 3.5), (R, 1))); da.rectangle([tx, 212, tx + 17, HOR], fill=A(90))
d.rectangle([tx + 1, 212, tx + 6, HOR], fill=M((Y, 3), (Wh, 2)))
d.rectangle([tx + 5, 222, tx + 12, 236], fill=M((B, 2), (K, 2)))
d.polygon([(tx - 2, 212), (tx + 8.5, 190), (tx + 19, 212)], fill=M((R, 3), (Y, .6)))
d.line([(tx + 8.5, 190), (tx + 8.5, 180)], fill=K, width=1)
d.rectangle([255, HOR - 4, W, HOR + 3], fill=M((Wh, 2), (Y, 1), (R, .5)))   # the quay
# town reflections
for xq in range(262, W, 3):
    c = tgt.getpixel((xq, HOR - 12))
    for yq in range(HOR + 4, HOR + 46, 2):
        if random.random() < 0.72 - (yq - HOR) / 90:
            d.line([(xq - 2, yq), (xq + 3, yq)], fill=c)

def boat(cx, wl, s, sail, sail2, hull, flip=1):
    """a tartane: lateen mainsail + jib, hull, and a shattered reflection"""
    L = 46 * s
    hullp = [(cx - L / 2, wl - 7 * s), (cx + L / 2 + 5 * s * flip, wl - 9 * s), (cx + L / 2 - 6 * s, wl), (cx - L / 2 + 5 * s, wl)]
    mast = (cx + 2 * s * flip, wl - 8 * s); top = (cx + 2 * s * flip, wl - 74 * s)
    main = [(cx - 22 * s * flip, wl - 12 * s), (cx + 10 * s * flip, wl - 92 * s), (cx + 20 * s * flip, wl - 14 * s)]
    jib = [(cx + 23 * s * flip, wl - 12 * s), (cx + 6 * s * flip, wl - 70 * s), (cx + 40 * s * flip, wl - 10 * s)]
    for k in range(int(70 * s)):                       # reflection first
        yq = wl + 2 + k * 1.6; t = k / (70 * s)
        if yq >= H: break
        wob = 5 * math.sin(k * 0.9) * (0.4 + t)
        half = (20 * s) * (1 - t) ** 0.8
        if k % 3 != 2:
            d.line([(cx - half + wob, yq), (cx + half + wob, yq)], fill=sail if k > 8 * s else hull, width=1)
    d.polygon(main, fill=sail); da.polygon(main, fill=A(100 - 12 * flip))
    stripe = [main[1], ((main[0][0] + main[2][0]) / 2 - 4 * s, main[0][1]), ((main[0][0] + main[2][0]) / 2 + 5 * s, main[2][1])]
    d.polygon(stripe, fill=sail2)
    d.polygon(jib, fill=sail2); da.polygon(jib, fill=A(70 + 12 * flip))
    d.line([mast, top], fill=K, width=max(1, int(1.6 * s)))
    d.polygon(hullp, fill=hull); da.polygon(hullp, fill=A(0))
    d.line([hullp[0], hullp[1]], fill=Wh, width=max(1, int(1.5 * s)))
    d.polygon([(top[0], top[1]), (top[0] + 9 * s * flip, top[1] + 3 * s), (top[0], top[1] + 6 * s)], fill=R)
    return mast, top
boat(248, 318, 0.36, M((Wh, 3), (Y, 1)), M((Y, 2), (Wh, 1)), M((B, 2), (K, 2)), -1)
boat(196, 326, 0.5, M((Y, 3), (R, .4)), ORG, K)
boat(60, 336, 0.62, M((Wh, 3), (R, .7)), M((Wh, 2), (B, .8)), M((G, 2), (K, 2)), -1)
boat(318, 372, 0.95, M((Y, 3.2), (R, .5)), M((Wh, 2.5), (Y, 1)), M((B, 2.4), (K, 1.6)), -1)
big = boat(128, 432, 1.75, M((R, 3), (Y, 1.1)), M((R, 3.4), (K, .5)), M((K, 3), (B, 1.4)))
# gulls
for gx, gy, gs in [(92, 150, 7), (120, 128, 5), (300, 96, 6), (330, 120, 4), (212, 70, 5), (36, 222, 5), (366, 170, 5)]:
    d.line([(gx - gs, gy - gs * .5), (gx - gs * .4, gy - gs * .1), (gx, gy + gs * .35), (gx + gs * .4, gy - gs * .1), (gx + gs, gy - gs * .5)], fill=M((B, 2), (K, 2)), width=2)
# near shore, bottom: red earth, agaves, a striped mooring post
sh = [(0, 548)] + [(x, 556 + 16 * math.sin(x / 60 + 1) + 20 * (x / W) ** 2) for x in range(0, W + 1, 5)] + [(W, H), (0, H)]
d.polygon(sh, fill=M((R, 2.4), (Y, 1.4), (K, .5))); da.polygon(sh, fill=A(14))
for ax, ay, asz in [(26, 574, 20), (78, 590, 15), (236, 588, 17), (300, 596, 22), (366, 592, 16), (160, 594, 13)]:
    for k in range(-4, 5):
        a = math.radians(-90 + k * 19)
        tip = (ax + math.cos(a) * asz * (1.5 - abs(k) * .1), ay + math.sin(a) * asz * 1.25)
        d.polygon([(ax - 3, ay), tip, (ax + 3, ay)], fill=DKG if k % 2 else M((G, 3), (Y, 1.2)))
# the umbrella pine, left: trunk and a great flat canopy across the top
trunk = [(18, 560), (30, 420), (26, 300), (40, 190), (66, 108), (80, 104), (58, 196), (46, 300), (52, 420), (46, 566)]
d.polygon(trunk, fill=M((R, 1.6), (B, 1.4), (K, 1.6))); da.polygon(trunk, fill=A(86))
d.line([(42, 420), (38, 300), (50, 196), (72, 112)], fill=ORG, width=3)
for b0, b1 in [((44, 210), (118, 120)), ((60, 130), (20, 60)), ((70, 112), (150, 70)), ((36, 250), (4, 196))]:
    d.line([b0, b1], fill=M((R, 1.6), (B, 1.4), (K, 1.6)), width=5)
random.seed(8)
for cx, cy, rx, ry in [(70, 52, 96, 34), (160, 44, 74, 26), (20, 96, 46, 26), (118, 92, 50, 20), (212, 62, 40, 15), (4, 190, 26, 16), (150, 12, 110, 22)]:
    for k in range(46):
        a = random.uniform(0, 6.283); q = random.random() ** .5
        bx, by = cx + math.cos(a) * rx * q, cy + math.sin(a) * ry * q; br = random.uniform(6, 13)
        col = random.choice([DKG, DKG, M((G, 3), (K, 1)), M((G, 3), (Y, 1.4)), M((B, 2), (G, 1.5), (K, 1))])
        d.ellipse([bx - br, by - br * .7, bx + br, by + br * .7], fill=col)
        da.ellipse([bx - br, by - br * .7, bx + br, by + br * .7], fill=A(random.choice([20, 150, 60, 110])))

# ---------- 2. rebuild it out of strokes ----------
T = np.asarray(tgt.filter(ImageFilter.GaussianBlur(0.3)), np.float32); AN = np.asarray(ang)
im, dd = canvas(Wh)
PAL = PAL6
def pick(c, u):
    best = (1e18, 1, 1, 0.0)
    dark = c.max() < 105
    for i in range(6):
        for j in range(i + 1, 6):
            if i == 0 and not dark: continue        # no black unless the tone is truly dark
            p, q = PAL[i], PAL[j]; dq = q - p
            t = float(np.clip(((c - p) * dq).sum() / (dq * dq).sum(), 0, 1))
            dist = float(((c - (p + t * dq)) ** 2).sum())
            if dist < best[0]: best = (dist, i, j, t)
    _, i, j, t = best
    return j if u < t else i
STEP_X, STEP_Y = 3.5, 2.5
n = 0
rows = int(H / STEP_Y) + 2
order = []
for ry in range(rows):
    for rx in range(int(W / STEP_X) + 2):
        order.append((rx * STEP_X + (ry % 2) * STEP_X / 2 + random.uniform(-.7, .7), ry * STEP_Y + random.uniform(-.6, .6)))
random.seed(3); random.shuffle(order)
for (sx, sy) in order:
    ix, iy = min(W - 1, max(0, int(sx))), min(H - 1, max(0, int(sy)))
    c = T[iy, ix] + rng.normal(0, 8, 3)
    k = pick(c, random.random())
    u = random.random()
    if u < 0.03:                                   # the neo-impressionist spark: a contrary dab
        k = random.choice([2, 3, 4, 5, 1])
    code = AN[iy, ix]
    if code: a = math.radians(code - 1 + random.uniform(-10, 10))
    elif iy >= HOR: a = math.radians(random.uniform(-5, 5))
    else: a = math.atan2(iy - SUN[1], ix - SUN[0]) + math.pi / 2 + random.uniform(-.12, .12)
    L, Wd = random.uniform(2.0, 2.5), random.uniform(1.15, 1.4)
    ca, sa = math.cos(a), math.sin(a)
    pts = [(sx + ca * L * e - sa * Wd * f, sy + sa * L * e + ca * Wd * f) for e, f in [(-1, -1), (1, -1), (1, 1), (-1, 1)]]
    dd.polygon(P(pts), fill=tuple(int(v) for v in PAL[k])); n += 1
# a few things the dabs can't carry: masts, rigging, the sun's hard disc edge
for (mast, top), wd in [(big, 1.0)]:
    line(dd, [mast, top], K, 1.4)
    line(dd, [top, (mast[0] + 70, mast[1] - 4)], K, 0.5); line(dd, [top, (mast[0] - 42, mast[1] - 6)], K, 0.5)
circ(dd, SUN[0], SUN[1], 15, fill=Wh); circ(dd, SUN[0], SUN[1], 15, outline=Y, w=1.4)
for k in range(26):
    a = k * 2 * math.pi / 26
    line(dd, [(SUN[0] + math.cos(a) * 18, SUN[1] + math.sin(a) * 18), (SUN[0] + math.cos(a) * (22 + 3 * (k % 2)), SUN[1] + math.sin(a) * (22 + 3 * (k % 2)))], Y, 1.2)
# painted border, as Signac framed his canvases in dots
for k in range(0, 2 * (W + H), 5):
    for inset, cols in [(2.5, [B, B, R]), (6.5, [Y, R, B])]:
        t = k + (inset > 3) * 2.5
        if t < W: p = (t, inset)
        elif t < W + H: p = (W - inset, t - W)
        elif t < 2 * W + H: p = (W - (t - W - H), H - inset)
        else: p = (inset, H - (t - 2 * W - H))
        circ(dd, p[0], p[1], 1.5, fill=random.choice(cols))
print(n, "strokes"); save(im)
