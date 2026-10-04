# 2 · midday — "Sora Nostra Matre Terra"
# "Laudato si', mi' Signore, per sora nostra matre Terra, la quale ne sustenta et governa,
#  et produce diversi fructi con coloriti fiori et herba."
# A millefleur tapestry: deep green ground sown with a library of small drawn plants
# (Poisson-disk placed), two fruiting trees, and the creatures of the field at peace:
# the tamed Wolf of Gubbio sitting beside a lamb, a hare, a goldfinch, a blue bird, a snail.
# A woven selvedge border and a banderole carry the first words of the Canticle.
import os, sys, math
sys.path.insert(0, os.path.dirname(__file__))
from common import *
from PIL import ImageFilter

rng = np.random.default_rng(80026)

def P(x, y):
    return (x * S, y * S)

# ------------------------------------------------------------------ primitives (2x coords)

def bez(p0, p1, p2, n=10):
    out = []
    for i in range(n + 1):
        t = i / n
        a, b, c = (1 - t) ** 2, 2 * (1 - t) * t, t * t
        out.append((a * p0[0] + b * p1[0] + c * p2[0], a * p0[1] + b * p1[1] + c * p2[1]))
    return out

def leaf_pts(x, y, ang, L, Wd, n=12, power=0.75, skew=0.8):
    """Pointed leaf from base (x,y) along angle ang (radians, y down)."""
    dx, dy = math.cos(ang), math.sin(ang)
    px, py = -dy, dx
    left, right = [], []
    for i in range(n + 1):
        t = i / n
        h = Wd / 2 * math.sin(math.pi * (t ** skew)) ** power
        cx, cy = x + dx * L * t, y + dy * L * t
        left.append((cx + px * h, cy + py * h))
        right.append((cx - px * h, cy - py * h))
    return left + right[::-1]

def opoly(d, pts, fill, w=3):
    d.polygon(pts, fill=fill)
    d.line(list(pts) + [pts[0], pts[1]], fill=K, width=w, joint="curve")

def leaf(d, x, y, ang, L, Wd, fill=G, w=3, vein=True, **kw):
    pts = leaf_pts(x, y, ang, L, Wd, **kw)
    opoly(d, pts, fill, w)
    if vein and Wd > 9:
        d.line([(x, y), (x + math.cos(ang) * L * 0.8, y + math.sin(ang) * L * 0.8)], fill=K, width=2)

def disk(d, x, y, r, fill, w=3):
    d.ellipse((x - r, y - r, x + r, y + r), fill=fill, outline=K if w else None, width=w)

def stem(d, pts, w=4):
    d.line(pts, fill=K, width=w, joint="curve")

def flower(d, x, y, n, R, pw, col, ccol, cr, rot=0.0, w=3, cdot=None):
    # black backing so petals read as a single blossom
    for i in range(n):
        a = rot + 2 * math.pi * i / n
        opoly(d, leaf_pts(x, y, a, R, pw, n=8, power=0.6, skew=1.0), col, w)
    disk(d, x, y, cr, ccol, 2 if cr > 4 else 0)
    if cdot:
        disk(d, x, y, max(2, cr * 0.45), cdot, 0)

UP = -math.pi / 2
def deg(a):
    return math.radians(a)

# ------------------------------------------------------------------ the plant library
# each takes (d, x, y, r): footprint centre and radius in 2x px; base at y + 0.9r

def p_daisy(d, x, y, r):
    by = y + r * 0.9
    for a in (-165, -130, -50, -15):
        leaf(d, x, by, deg(a + rng.uniform(-8, 8)), r * 0.55, r * 0.26)
    n = rng.integers(1, 4)
    for i in range(n):
        hx = x + (i - (n - 1) / 2) * r * 0.6 + rng.uniform(-3, 3)
        hy = y - r * 0.35 + rng.uniform(-r * 0.25, r * 0.15)
        stem(d, bez((x, by), ((x + hx) / 2, by - r * 0.4), (hx, hy)))
    for i in range(n):
        hx = x + (i - (n - 1) / 2) * r * 0.6
        hy = y - r * 0.35 + rng.uniform(-r * 0.2, r * 0.1)
        hr = r * rng.uniform(0.34, 0.42)
        col = WH if rng.random() < 0.7 else (R if rng.random() < 0.5 else Y)
        flower(d, hx, hy, 9, hr, hr * 0.62, col, Y if col != Y else R, hr * 0.36, rot=rng.uniform(0, 1))

def p_violet(d, x, y, r):
    by = y + r * 0.9
    for a in (-160, -110, -70, -20):
        leaf(d, x, by, deg(a + rng.uniform(-10, 10)), r * 0.55, r * 0.5, power=0.5, skew=0.6)
    n = rng.integers(2, 4)
    for i in range(n):
        hx = x + (i - (n - 1) / 2) * r * 0.62
        hy = y - r * 0.25 + rng.uniform(-r * 0.25, r * 0.1)
        stem(d, bez((x, by), (hx, by - r * 0.2), (hx, hy)), 3)
        hr = r * 0.34
        col = B if rng.random() < 0.8 else WH
        for a, L in ((-115, 1.0), (-65, 1.0), (170, 0.85), (10, 0.85), (90, 1.05)):
            opoly(d, leaf_pts(hx, hy, deg(a), hr * L, hr * 0.8, n=8, power=0.5, skew=1.0), col, 3)
        disk(d, hx, hy, hr * 0.32, WH if col == B else B, 2)
        disk(d, hx, hy, 2.5, Y, 0)

def trefoil(d, x, y, ang, L, fill=G, mark=False):
    for da in (-55, 0, 55):
        a = ang + deg(da)
        pts = leaf_pts(x, y, a, L, L * 0.75, power=0.45, skew=0.7)
        opoly(d, pts, fill, 3)
        if mark:
            mx, my = x + math.cos(a) * L * 0.45, y + math.sin(a) * L * 0.45
            d.line([(mx - 3, my - 3), (mx, my), (mx + 3, my - 3)], fill=WH, width=3)

def p_strawberry(d, x, y, r):
    by = y + r * 0.9
    for side in (-1, 1):
        ex, ey = x + side * r * 0.5, by - r * 0.35
        stem(d, [(x, by), (ex, ey)], 3)
        trefoil(d, ex, ey, UP + side * deg(25), r * 0.38)
    # flower
    fx, fy = x + rng.uniform(-r * 0.15, r * 0.15), y - r * 0.55
    stem(d, bez((x, by), (x, y), (fx, fy)), 3)
    flower(d, fx, fy, 5, r * 0.3, r * 0.3, WH, Y, r * 0.11)
    # berries
    for k in range(rng.integers(1, 3)):
        side = 1 if k == 0 else -1
        sx, sy = x + side * r * 0.25, y - r * 0.1
        bx, byy = x + side * r * 0.6, y + r * 0.08
        stem(d, bez((x, y + r * 0.3), (sx, sy), (bx, byy - r * 0.15)), 3)
        br = r * 0.2
        pts = [(bx - br, byy - br * 0.4), (bx + br, byy - br * 0.4), (bx + br * 0.75, byy + br * 0.6),
               (bx, byy + br * 1.4), (bx - br * 0.75, byy + br * 0.6)]
        d.polygon(pts, fill=R)
        d.line(pts + [pts[0], pts[1]], fill=K, width=3, joint="curve")
        for (u, v) in ((-0.4, 0.1), (0.4, 0.1), (0, 0.65)):
            disk(d, bx + u * br, byy + v * br, 2.2, Y, 0)
        for a in (-150, -90, -30):
            d.line([(bx, byy - br * 0.45), (bx + math.cos(deg(a)) * br * 0.8, byy - br * 0.45 + math.sin(deg(a)) * br * 0.5)],
                   fill=K, width=3)

def p_carnation(d, x, y, r):
    by = y + r * 0.9
    for a in (-160, -135, -45, -20):
        leaf(d, x, by, deg(a), r * 0.6, r * 0.1, vein=False)
    n = rng.integers(1, 3)
    col = [R, R, WH, Y][rng.integers(0, 4)]
    for i in range(n):
        hx = x + (i - (n - 1) / 2) * r * 0.75
        hy = y - r * 0.3 + rng.uniform(-r * 0.2, r * 0.1)
        stem(d, bez((x, by), ((x + hx) / 2, y + r * 0.2), (hx, hy + r * 0.2)), 3)
        for s in (-1, 1):
            leaf(d, hx + (x - hx) * 0.4, y + r * 0.35, UP + s * deg(55), r * 0.3, r * 0.08, vein=False)
        # calyx
        cw = r * 0.11
        opoly(d, [(hx - cw, hy), (hx + cw, hy), (hx + cw * 0.7, hy + r * 0.3), (hx - cw * 0.7, hy + r * 0.3)], G, 3)
        # fringed fan
        R0 = r * 0.42
        pts = [(hx - cw, hy + 1)]
        m = 9
        for k in range(m + 1):
            a = deg(-160 + 140 * k / m)
            rr = R0 if k % 2 == 0 else R0 * 0.72
            pts.append((hx + math.cos(a) * rr, hy + 2 + math.sin(a) * rr * 0.85))
        pts.append((hx + cw, hy + 1))
        opoly(d, pts, col, 3)
        inner = WH if col == R else R
        if col != Y:
            d.line([(hx, hy), (hx, hy - R0 * 0.5)], fill=inner, width=4)
            d.line([(hx, hy), (hx - R0 * 0.38, hy - R0 * 0.38)], fill=inner, width=3)
            d.line([(hx, hy), (hx + R0 * 0.38, hy - R0 * 0.38)], fill=inner, width=3)
        else:
            d.line([(hx, hy), (hx, hy - R0 * 0.5)], fill=R, width=4)

def p_columbine(d, x, y, r):
    by = y + r * 0.9
    for side in (-1, 1):
        ex, ey = x + side * r * 0.42, by - r * 0.25
        stem(d, [(x, by), (ex, ey)], 3)
        for da in (-50, 0, 50):
            a = UP + side * deg(30) + deg(da)
            opoly(d, leaf_pts(ex, ey, a, r * 0.26, r * 0.26, power=0.4, skew=0.7), G, 3)
    col = [B, B, R, WH][rng.integers(0, 4)]
    n = rng.integers(1, 3)
    for i in range(n):
        side = 1 if (i == 0) ^ (rng.random() < 0.5) else -1
        top = (x + side * r * 0.1, y - r * 0.95)
        hx, hy = x + side * r * 0.45, y - r * 0.35 + i * r * 0.15
        stem(d, bez((x, by), top, (hx, hy - r * 0.18)), 3)
        # spurs (up, curled)
        for k in (-1, 0, 1):
            sx = hx + k * r * 0.13
            pts = bez((sx, hy - r * 0.02), (sx + k * r * 0.12, hy - r * 0.3), (sx + k * r * 0.03 + r * 0.06, hy - r * 0.22), 5)
            d.line(pts, fill=K, width=7, joint="curve")
            d.line(pts, fill=col, width=3, joint="curve")
            disk(d, pts[-1][0], pts[-1][1], 3, K, 0)
        # bell hanging down
        bw = r * 0.22
        bell = [(hx - bw, hy), (hx + bw, hy), (hx + bw * 0.9, hy + r * 0.22), (hx + bw * 0.4, hy + r * 0.32),
                (hx, hy + r * 0.24), (hx - bw * 0.4, hy + r * 0.32), (hx - bw * 0.9, hy + r * 0.22)]
        opoly(d, bell, col, 3)
        inner = WH if col != WH else Y
        d.line([(hx - bw * 0.5, hy + r * 0.12), (hx + bw * 0.5, hy + r * 0.12)], fill=inner, width=4)

def p_bluebell(d, x, y, r):
    by = y + r * 0.9
    side = 1 if rng.random() < 0.5 else -1
    for a in (-120, -95, -70):
        leaf(d, x, by, deg(a) + side * deg(10), r * 1.0, r * 0.14, vein=False)
    tip = (x + side * r * 0.65, y - r * 0.55)
    pts = bez((x, by), (x - side * r * 0.1, y - r * 1.05), tip, 14)
    stem(d, pts, 3)
    col = B if rng.random() < 0.85 else WH
    idx = [5, 7, 9, 11, 13]
    for j, k in enumerate(idx):
        sx, sy = pts[k]
        bl = r * (0.24 - 0.02 * j)
        bx, byy = sx + side * r * 0.08, sy + r * 0.08
        d.line([(sx, sy), (bx, byy)], fill=K, width=3)
        bw = bl * 0.5
        bell = [(bx - bw * 0.6, byy), (bx + bw * 0.6, byy), (bx + bw, byy + bl * 0.8), (bx + bw * 1.25, byy + bl),
                (bx + bw * 0.35, byy + bl * 0.9), (bx, byy + bl * 1.05), (bx - bw * 0.35, byy + bl * 0.9),
                (bx - bw * 1.25, byy + bl), (bx - bw, byy + bl * 0.8)]
        opoly(d, bell, col, 3)

def toothed_leaf(d, x, y, ang, L, Wd):
    dx, dy = math.cos(ang), math.sin(ang)
    px, py = -dy, dx
    n = 7
    left, right = [], []
    for i in range(n + 1):
        t = i / n
        h = Wd / 2 * math.sin(math.pi * t ** 0.8) ** 0.6 * (1.0 if i % 2 else 0.45)
        cx, cy = x + dx * L * t, y + dy * L * t
        left.append((cx + px * h, cy + py * h))
        right.append((cx - px * h, cy - py * h))
    opoly(d, left + right[::-1], G, 3)
    d.line([(x, y), (x + dx * L * 0.85, y + dy * L * 0.85)], fill=K, width=2)

def p_dandelion(d, x, y, r):
    by = y + r * 0.9
    for a in (-170, -140, -40, -10):
        toothed_leaf(d, x, by, deg(a + rng.uniform(-6, 6)), r * 0.65, r * 0.3)
    # clock
    cx, cy = x - r * 0.25, y - r * 0.45
    stem(d, bez((x, by), (x - r * 0.2, y), (cx, cy)), 3)
    cr = r * 0.36
    disk(d, cx, cy, cr, WH, 3)
    for k in range(12):
        a = 2 * math.pi * k / 12
        d.line([(cx, cy), (cx + math.cos(a) * cr * 0.75, cy + math.sin(a) * cr * 0.75)], fill=K, width=2)
    disk(d, cx, cy, 3, K, 0)
    # yellow flower
    fx, fy = x + r * 0.4, y - r * 0.1
    stem(d, bez((x, by), (x + r * 0.2, y + r * 0.3), (fx, fy)), 3)
    flower(d, fx, fy, 12, r * 0.27, r * 0.14, Y, Y, r * 0.1, rot=0.2)

def p_wheat(d, x, y, r):
    by = y + r * 0.95
    n = rng.integers(2, 4)
    leaf(d, x, by, deg(-125), r * 0.7, r * 0.1, vein=False)
    leaf(d, x, by, deg(-55), r * 0.7, r * 0.1, vein=False)
    for i in range(n):
        a = UP + (i - (n - 1) / 2) * deg(16) + deg(rng.uniform(-4, 4))
        L = r * rng.uniform(1.1, 1.35)
        tx, ty = x + math.cos(a) * L, by + math.sin(a) * L
        ex, ey = x + math.cos(a) * L * 0.45, by + math.sin(a) * L * 0.45
        stem(d, [(x, by), (ex, ey)], 3)
        # ear: grains alternating along axis from (ex,ey) to (tx,ty)
        rows = 5
        dx, dy = (tx - ex) / rows, (ty - ey) / rows
        gl = r * 0.2
        for k in range(rows):
            for s in (-1, 1):
                gx, gy = ex + dx * (k + 0.3), ey + dy * (k + 0.3)
                ga = a + s * deg(28)
                # awn
                ax, ay = gx + math.cos(ga) * gl * 1.9, gy + math.sin(ga) * gl * 1.9
                d.line([(gx, gy), (ax, ay)], fill=K, width=2)
                opoly(d, leaf_pts(gx, gy, ga, gl, gl * 0.62, n=8, power=0.5, skew=1.0), Y, 3)
        opoly(d, leaf_pts(tx - dx * 0.4, ty - dy * 0.4, a, gl * 0.9, gl * 0.55, n=8, power=0.5, skew=1.0), Y, 3)

def p_plantain(d, x, y, r):
    by = y + r * 0.9
    for a in (-165, -125, -55, -15):
        a = deg(a + rng.uniform(-6, 6))
        L, Wd = r * 0.62, r * 0.36
        pts = leaf_pts(x, by, a, L, Wd, power=0.6, skew=0.8)
        opoly(d, pts, G, 3)
        px, py = -math.sin(a), math.cos(a)
        for o in (-0.18, 0.18):
            d.line(bez((x, by), (x + math.cos(a) * L * 0.5 + px * Wd * o * 1.4, by + math.sin(a) * L * 0.5 + py * Wd * o * 1.4),
                       (x + math.cos(a) * L * 0.9, by + math.sin(a) * L * 0.9), 6), fill=K, width=2)
    n = rng.integers(2, 4)
    for i in range(n):
        a = UP + (i - (n - 1) / 2) * deg(22)
        L = r * rng.uniform(1.1, 1.4)
        tx, ty = x + math.cos(a) * L, by + math.sin(a) * L
        sx, sy = x + math.cos(a) * L * 0.62, by + math.sin(a) * L * 0.62
        stem(d, [(x, by), (sx, sy)], 3)
        opoly(d, leaf_pts(sx, sy, a, L * 0.4, r * 0.15, n=8, power=0.4, skew=1.0), K, 2)
        # ring of white anthers
        mx, my = sx + math.cos(a) * L * 0.12, sy + math.sin(a) * L * 0.12
        px, py = -math.sin(a), math.cos(a)
        for s in (-1, 1):
            disk(d, mx + px * s * r * 0.12, my + py * s * r * 0.12, 2.6, WH, 0)
            disk(d, mx + px * s * r * 0.11 + math.cos(a) * 6, my + py * s * r * 0.11 + math.sin(a) * 6, 2.6, WH, 0)

def p_clover(d, x, y, r):
    by = y + r * 0.9
    for side in (-1, 1):
        ex, ey = x + side * r * 0.5, by - r * 0.3
        stem(d, [(x, by), (ex, ey)], 3)
        trefoil(d, ex, ey, UP + side * deg(15), r * 0.36, mark=True)
    col = R if rng.random() < 0.6 else WH
    n = rng.integers(1, 3)
    for i in range(n):
        hx = x + (i - (n - 1) / 2) * r * 0.5
        hy = y - r * 0.45 + i * r * 0.1
        stem(d, [(x, by), (hx, hy)], 3)
        hr = r * 0.26
        disk(d, hx, hy, hr, col, 3)
        for k in range(6):
            a = -math.pi / 2 + 2 * math.pi * k / 6
            u, v = hx + math.cos(a) * hr * 0.55, hy + math.sin(a) * hr * 0.55
            d.line([(u, v + 3), (u - 3, v - 2)], fill=K, width=2)
        d.line([(hx - 3, hy + hr * 0.3), (hx + 3, hy - hr * 0.3)], fill=K, width=2)

def p_fern(d, x, y, r):
    by = y + r * 0.95
    side = 1 if rng.random() < 0.5 else -1
    tip = (x + side * r * 0.6, y - r * 0.8)
    pts = bez((x, by), (x - side * r * 0.3, y - r * 0.6), tip, 12)
    stem(d, pts, 4)
    solid = rng.random() < 0.4
    for k in range(1, 12):
        (x0, y0), (x1, y1) = pts[k], pts[k + 1] if k + 1 < len(pts) else pts[k]
        a = math.atan2(y1 - y0, x1 - x0)
        L = r * 0.42 * (1 - k / 13) ** 0.7
        for s in (-1, 1):
            la = a + s * deg(70)
            if solid:
                opoly(d, leaf_pts(x0, y0, la, L, L * 0.38, n=8), K, 2)
            else:
                leaf(d, x0, y0, la, L, L * 0.42, vein=False)
    # crozier
    cx, cy = tip
    d.arc((cx - 7, cy - 7, cx + 7, cy + 7), 90, 400, fill=K, width=4)

def p_myosotis(d, x, y, r):
    by = y + r * 0.9
    for a in (-150, -30):
        leaf(d, x, by, deg(a), r * 0.5, r * 0.22)
    n = rng.integers(2, 4)
    for i in range(n):
        a = UP + (i - (n - 1) / 2) * deg(35)
        hx, hy = x + math.cos(a) * r * 1.2, by + math.sin(a) * r * 1.2
        stem(d, [(x, by), (hx, hy)], 3)
        for k in range(3):
            fa = a + deg(-70 + 70 * k)
            fx, fy = hx + math.cos(fa) * r * 0.2, hy + math.sin(fa) * r * 0.2
            disk(d, fx, fy, r * 0.15, B, 3)
            disk(d, fx, fy, 2.6, Y, 0)

def p_rose(d, x, y, r):
    by = y + r * 0.9
    stem(d, bez((x, by), (x - r * 0.2, y), (x, y - r * 0.35)), 4)
    for (u, v, a) in ((-0.1, 0.5, -150), (0.0, 0.35, -30), (-0.15, 0.1, -160)):
        lx, ly = x + u * r, y + v * r
        for s in (0, 1):
            leaf(d, lx, ly, deg(a + s * 30), r * 0.33, r * 0.2, vein=False)
    col = R if rng.random() < 0.75 else WH
    hx, hy = x, y - r * 0.35
    flower(d, hx, hy, 5, r * 0.48, r * 0.5, col, WH if col == R else R, r * 0.17, rot=rng.uniform(0, 1))
    disk(d, hx, hy, r * 0.08, Y, 0)
    # a bud
    bx, bym = x + r * 0.5, y + r * 0.05
    stem(d, [(x - r * 0.1, y + r * 0.2), (bx, bym)], 3)
    opoly(d, leaf_pts(bx, bym + 2, UP + deg(20), r * 0.25, r * 0.2, power=0.5, skew=1), col, 3)

def p_sprig(d, x, y, r):
    """filler: a little three-leaved sprig, sometimes with a bud or a four-petalled blossom"""
    by = y + r * 0.8
    a0 = UP + deg(rng.uniform(-25, 25))
    tx, ty = x + math.cos(a0) * r * 1.1, by + math.sin(a0) * r * 1.1
    stem(d, [(x, by), (tx, ty)], 3)
    for t, s_ in ((0.35, -1), (0.55, 1)):
        lx, ly = x + (tx - x) * t, by + (ty - by) * t
        leaf(d, lx, ly, a0 + s_ * deg(60), r * 0.6, r * 0.32, vein=False)
    c = rng.random()
    if c < 0.5:
        col = [Y, R, WH, B, WH, Y][rng.integers(0, 6)]
        flower(d, tx, ty, 4, r * 0.38, r * 0.36, col, R if col in (WH, Y) else Y, 3, rot=rng.uniform(0, 1))
    else:
        leaf(d, tx + (tx - x) * -0.05, ty + 3, a0, r * 0.45, r * 0.3, vein=False)

LIB = {
    "daisy": (p_daisy, 42, 62, 4), "violet": (p_violet, 38, 52, 3), "strawberry": (p_strawberry, 50, 66, 3),
    "carnation": (p_carnation, 52, 70, 3), "columbine": (p_columbine, 56, 72, 2), "bluebell": (p_bluebell, 52, 72, 2),
    "dandelion": (p_dandelion, 50, 66, 2), "wheat": (p_wheat, 50, 68, 2), "plantain": (p_plantain, 50, 66, 2),
    "clover": (p_clover, 38, 52, 3), "fern": (p_fern, 52, 72, 2), "myosotis": (p_myosotis, 38, 50, 3),
    "rose": (p_rose, 50, 66, 2),
}

# ------------------------------------------------------------------ silhouettes for creatures

def dilate(m, w):
    im = Image.fromarray((m * 255).astype(np.uint8))
    return np.asarray(im.filter(ImageFilter.MaxFilter(2 * w + 1))) > 127

def erode(m, w):
    im = Image.fromarray((m * 255).astype(np.uint8))
    return np.asarray(im.filter(ImageFilter.MinFilter(2 * w + 1))) > 127

def body(img, fn, fill, w=4):
    m = mask_of(fn)
    img = paint(img, dilate(m, w), K)
    img = paint(img, m, fill)
    return img, m

def clipped(img, region, fn, colour):
    m = mask_of(fn)
    return paint(img, m & region, colour)

def L2(pts):
    return [P(*p) for p in pts]

# ------------------------------------------------------------------ composition (1x coords)

BORDER = 12
img, d = new(G)

# reserved areas for creatures/trees (filled before plants are scattered)
reserve = np.zeros((H2, W2), bool)

def reserve_poly(pts, pad=6):
    global reserve
    m = mask_of(lambda dd: dd.polygon(L2(pts), fill=255))
    reserve |= dilate(m, pad * S // 2)

def reserve_ellipse(b, pad=6):
    global reserve
    m = mask_of(lambda dd: dd.ellipse([b[0] * S, b[1] * S, b[2] * S, b[3] * S], fill=255))
    reserve |= dilate(m, pad * S // 2)

TREES = [  # (cx, crown cy, crown r, trunk bottom, kind)
    (100, 92, 60, 200, "orange"),
    (302, 100, 54, 205, "pomegranate"),
]
for cx, cy, cr, tb, kind in TREES:
    reserve_ellipse((cx - cr, cy - cr * 0.95, cx + cr, cy + cr * 0.95))
    reserve_poly([(cx - 9, cy), (cx + 9, cy), (cx + 12, tb), (cx - 12, tb)])

# creatures' rough footprints
reserve_ellipse((230, 182, 318, 272))       # hare
reserve_poly([(56, 336), (116, 300), (128, 258), (170, 258), (200, 292), (164, 322), (166, 384), (174, 456), (40, 462), (40, 420)])  # wolf
reserve_ellipse((204, 362, 330, 440))       # lamb
reserve_ellipse((176, 52, 230, 92))          # flying goldfinch
reserve_ellipse((184, 428, 236, 470))        # ground bird
reserve_ellipse((262, 470, 330, 512))        # snail
reserve_poly([(26, 532), (374, 532), (374, 578), (26, 578)])  # banderole

field = np.zeros((H2, W2), bool)
field[BORDER * S:H2 - BORDER * S, BORDER * S:W2 - BORDER * S] = True

# ------------------------------------------------------------------ Poisson-disk sowing
SMALL = ["violet", "clover", "myosotis", "daisy", "strawberry", "sprig"]

def sow():
    pts = []
    grid = {}
    cell = 80
    def fits(x, y, r, name, k, same):
        for a in range(0, 360, 45):
            u = int(x + math.cos(math.radians(a)) * r * 0.45); v = int(y + math.sin(math.radians(a)) * r * 0.45)
            if reserve[v, u]:
                return False
        if reserve[int(y), int(x)]:
            return False
        gx, gy = int(x // cell), int(y // cell)
        for i in range(gx - 2, gx + 3):
            for j in range(gy - 2, gy + 3):
                for (px, py, pr, pn) in grid.get((i, j), []):
                    dd = math.hypot(px - x, py - y)
                    if dd < (pr + r) * k or (pn == name and dd < (pr + r) * same):
                        return False
        return True
    def add(p):
        pts.append(p); grid.setdefault((int(p[0] // cell), int(p[1] // cell)), []).append(p)
    def run(names, rscale, k, same, tries):
        for _ in range(tries):
            name = names[rng.integers(0, len(names))]
            if name == "sprig":
                rmin, rmax, wgt = 26, 36, 4
            else:
                _, rmin, rmax, wgt = LIB[name]
            if rng.random() > wgt / 4:
                continue
            r = rng.uniform(rmin, rmax) * rscale
            x = rng.uniform(BORDER * S + r * 0.8, W2 - BORDER * S - r * 0.8)
            y = rng.uniform(BORDER * S + r * 0.9, H2 - BORDER * S - r * 0.9)
            if fits(x, y, r, name, k, same):
                add((x, y, r, name))
    BIG = ["columbine", "bluebell", "fern", "carnation", "wheat", "dandelion", "plantain", "rose", "strawberry"]
    run(BIG, 1.0, 0.66, 1.1, 30000)
    run(list(LIB), 1.0, 0.64, 1.1, 30000)
    run(SMALL[:-1], 0.75, 0.66, 1.0, 40000)
    run(["sprig"], 1.0, 0.68, 0.0, 30000)
    run(["sprig"], 0.75, 0.66, 0.0, 30000)
    return pts

plants = sow()
print("plants:", len(plants), {n: sum(p[3] == n for p in plants) for n in set(p[3] for p in plants)})
plants.sort(key=lambda p: p[1])
for (x, y, r, name) in plants:
    if name == "sprig":
        p_sprig(d, x, y, r)
    else:
        LIB[name][0](d, x, y, r)

# ------------------------------------------------------------------ trees
def tree(img, cx, cy, cr, tb, kind):
    d = ImageDraw.Draw(img)
    # trunk
    trunk = L2([(cx - 7, cy + 10), (cx + 7, cy + 10), (cx + 10, tb - 6), (cx + 16, tb), (cx - 16, tb), (cx - 10, tb - 6)])
    img, tm = body(img, lambda dd: dd.polygon(trunk, fill=255), R if kind == "pomegranate" else Y, 3)
    d = ImageDraw.Draw(img)
    for k in range(5):  # bark hatching
        yy = cy + 22 + k * (tb - cy - 30) / 5
        d.line([P(cx - 6, yy), P(cx + 2, yy + 5)], fill=Y if kind == "pomegranate" else R, width=4)
    # dark crown mass
    box = [P(cx - cr, cy - cr * 0.92), P(cx + cr, cy + cr * 0.92)]
    img, cm = body(img, lambda dd: dd.ellipse([box[0], box[1]], fill=255), K, 3)
    d = ImageDraw.Draw(img)
    # leaves in rings, pointing outward from centre
    lr = np.random.default_rng(int(cx))
    leaves = []
    for ring in np.linspace(0.15, 0.88, 6):
        n = int(6 + ring * 26)
        off = lr.uniform(0, 1)
        for i in range(n):
            a = 2 * math.pi * (i + off) / n
            leaves.append((ring, a))
    for ring, a in leaves:
        bx = cx + math.cos(a) * cr * ring * 0.85
        by = cy + math.sin(a) * cr * ring * 0.8
        la = a + lr.uniform(-0.5, 0.5) if ring > 0.3 else lr.uniform(0, 6.3)
        L = cr * 0.28 * S
        leaf(d, bx * S, by * S, la, L, L * 0.45, w=3)
    # fruit
    fr = np.random.default_rng(int(cy))
    fruits = []
    for _ in range(400):
        a = fr.uniform(0, 2 * math.pi); rr = math.sqrt(fr.uniform(0.02, 0.8)) * cr * 0.85
        fx, fy = cx + math.cos(a) * rr, cy + math.sin(a) * rr * 0.9
        if all(math.hypot(fx - u, fy - v) > 17 for u, v in fruits):
            fruits.append((fx, fy))
        if len(fruits) >= (13 if kind == "orange" else 10):
            break
    for fx, fy in fruits:
        if kind == "orange":
            disk(d, fx * S, fy * S, 13, Y, 4)
            d.arc((fx * S - 8, fy * S - 8, fx * S + 6, fy * S + 6), 200, 280, fill=WH, width=3)
            leaf(d, fx * S, fy * S - 12, deg(-50), 12, 7, w=2, vein=False)
            disk(d, fx * S, fy * S - 12, 2.5, K, 0)
        else:
            disk(d, fx * S, fy * S, 14, R, 4)
            crown = [P(fx - 5, fy - 5), P(fx - 6, fy - 11), P(fx - 2, fy - 8), P(fx, fy - 12), P(fx + 2, fy - 8),
                     P(fx + 6, fy - 11), P(fx + 5, fy - 5)]
            opoly(d, crown, Y, 3)
            d.arc((fx * S - 8, fy * S - 8, fx * S + 6, fy * S + 6), 200, 270, fill=WH, width=3)
    # blossom on the pomegranate (red-orange flowers) / orange (white)
    for _ in range(6):
        a = fr.uniform(0, 2 * math.pi); rr = cr * fr.uniform(0.3, 0.8)
        fx, fy = cx + math.cos(a) * rr, cy + math.sin(a) * rr * 0.9
        if min(math.hypot(fx - u, fy - v) for u, v in fruits) > 14:
            flower(d, fx * S, fy * S, 5, 10, 9, WH if kind == "orange" else R, Y, 3)
    return img

for t in TREES:
    img = tree(img, *t)
d = ImageDraw.Draw(img)

# ------------------------------------------------------------------ the Wolf of Gubbio, sitting, tamed
def wolf(img):
    def sil(dd):
        dd.ellipse([P(56, 360), P(128, 440)], fill=255)                         # haunch
        dd.polygon(L2([(70, 372), (118, 316), (154, 322), (158, 392), (126, 440), (80, 440)]), fill=255)
        dd.ellipse([P(114, 312), P(164, 396)], fill=255)                          # chest
        dd.polygon(L2([(130, 380), (144, 380), (143, 446), (130, 446)]), fill=255)
        dd.polygon(L2([(148, 384), (161, 384), (160, 446), (148, 446)]), fill=255)
        dd.ellipse([P(126, 438), P(152, 452)], fill=255)
        dd.ellipse([P(146, 438), P(172, 452)], fill=255)
        dd.ellipse([P(78, 428), P(130, 452)], fill=255)                           # hind foot
        dd.polygon(L2([(118, 330), (128, 296), (160, 290), (162, 330)]), fill=255)  # neck
        dd.ellipse([P(128, 270), P(176, 314)], fill=255)                          # skull
        dd.polygon(L2([(164, 282), (196, 294), (198, 304), (190, 312), (162, 314)]), fill=255)  # muzzle
        dd.polygon(L2([(134, 284), (136, 252), (152, 278)]), fill=255)            # ears
        dd.polygon(L2([(148, 278), (158, 250), (166, 280)]), fill=255)
        # tail curled round the feet
        dd.line(L2(bez((64, 412), (34, 452), (96, 456), 12)), fill=255, width=26)
        dd.ellipse([P(88, 444), P(124, 462)], fill=255)
        # ruff
        for k in range(5):
            y0 = 312 + k * 9
            dd.polygon(L2([(118 - k, y0), (110 - k * 2, y0 + 6), (120 - k, y0 + 10)]), fill=255)
    img, m = body(img, sil, WH, 4)
    inner = erode(m, 3)
    # tapestry hatching: blue comb strokes along the back, haunch and tail
    def hatch(dd):
        for k in range(14):  # back
            t = k / 13
            x0 = 70 + t * 50; y0 = 372 - t * 58
            dd.line([P(x0, y0), P(x0 + 9, y0 + 7)], fill=255, width=5)
        for k in range(10):  # haunch rim
            a = deg(150 + k * 14)
            x0 = 92 + math.cos(a) * 34; y0 = 400 + math.sin(a) * 38
            dd.line([P(x0, y0), P(92 + math.cos(a) * 24, 400 + math.sin(a) * 28)], fill=255, width=5)
        for k in range(8):   # skull top
            x0 = 136 + k * 5
            dd.line([P(x0, 270), P(x0 + 2, 280)], fill=255, width=4)
        for k in range(9):   # tail
            x0 = 44 + k * 7
            dd.line([P(x0, 438), P(x0 + 5, 448)], fill=255, width=5)
        for k in range(9):   # front of chest / ruff
            y0 = 318 + k * 8
            dd.line([P(160 - (k > 5) * 2, y0), P(151 - (k > 5) * 2, y0 + 4)], fill=255, width=5)
        for k in range(5):   # forelegs, behind
            dd.line([P(131, 392 + k * 10), P(136, 396 + k * 10)], fill=255, width=4)
        for k in range(6):   # cheek ruff
            dd.line([P(132 + k * 4, 312 - k), P(134 + k * 4, 304 - k)], fill=255, width=4)
        dd.ellipse([P(38, 430), P(58, 450)], fill=255)  # tail tip
        dd.polygon(L2([(138, 282), (138, 262), (148, 278)]), fill=255)  # inner ears
        dd.polygon(L2([(152, 278), (157, 262), (162, 280)]), fill=255)
    img = clipped(img, inner, hatch, B)
    d = ImageDraw.Draw(img)
    # details
    d.arc([P(150, 284), P(164, 296)], 20, 160, fill=K, width=4)          # closed, peaceful eye
    d.line([P(160, 290), P(166, 286)], fill=K, width=3)
    disk(d, *P(196, 299), 6, K, 0)                                         # nose
    d.line(L2([(194, 306), (184, 308), (174, 306)]), fill=K, width=4)     # mouth
    d.line(L2(bez((126, 400), (110, 360), (122, 330), 8)), fill=K, width=4)  # shoulder
    d.line(L2([(144, 392), (145, 440)]), fill=K, width=4)                 # leg division
    d.line(L2(bez((60, 405), (90, 368), (124, 400), 8)), fill=K, width=4) # haunch
    for px in (132, 138, 152, 158, 164):
        d.line([P(px, 446), P(px, 451)], fill=K, width=3)                 # toes
    # red collar? No — the wolf is free. Instead, a little blue-red pact: Francis' cord knot
    return img

img = wolf(img)

# ------------------------------------------------------------------ lamb, couchant, facing the wolf
def lamb(img):
    cx, cy, rx, ry = 278, 408, 44, 24
    def sil(dd):
        dd.ellipse([P(cx - rx, cy - ry), P(cx + rx, cy + ry)], fill=255)
        for k in range(15):                        # scalloped fleece rim
            a = deg(180 + k * 180 / 14)
            u, v = cx + math.cos(a) * rx, cy + math.sin(a) * ry
            dd.ellipse([P(u - 7, v - 7), P(u + 7, v + 7)], fill=255)
        dd.ellipse([P(cx + rx - 10, cy - 2), P(cx + rx + 6, cy + 14)], fill=255)  # rump curl / tail
        dd.ellipse([P(222, 384), P(254, 426)], fill=255)          # chest
        dd.ellipse([P(220, 360), P(248, 390)], fill=255)          # poll
        dd.polygon(L2([(222, 372), (204, 390), (206, 400), (218, 402), (238, 388)]), fill=255)  # long face
        dd.ellipse([P(203, 386), P(219, 403)], fill=255)          # muzzle
        dd.polygon(L2(leaf_pts(238, 372, deg(-10), 20, 9)), fill=255)          # ear, sticking back
        dd.polygon(L2([(234, 420), (206, 420), (202, 428), (236, 430)]), fill=255)  # folded foreleg
        dd.polygon(L2([(290, 426), (318, 426), (320, 434), (288, 434)]), fill=255)  # hind leg
    img, m = body(img, sil, WH, 4)
    d = ImageDraw.Draw(img)
    # fleece curls: little c-scrolls in rows
    lr = np.random.default_rng(7)
    for row, y in enumerate(range(390, 432, 8)):
        for x in range(244 + (row % 2) * 6, 324, 11):
            u, v = x + lr.uniform(-2, 2), y + lr.uniform(-1.5, 1.5)
            if m[int((v + 7) * S), int(u * S)] and m[int((v - 7) * S), int((u + 7) * S)] and m[int(v * S), int((u + 9) * S)]:
                a0 = lr.uniform(0, 360)
                pts = []
                for i in range(14):           # a little curl: shrinking spiral, ~1.3 turns
                    t = i / 13
                    a = math.radians(a0) + t * 8.0
                    rr = 4.2 * (1 - 0.65 * t)
                    pts.append(P(u + 4 + math.cos(a) * rr, v + math.sin(a) * rr))
                d.line(pts, fill=K, width=3, joint="curve")
    d.line(L2(bez((250, 388), (236, 404), (246, 424), 8)), fill=K, width=3)   # chest / body seam
    # face
    d.polygon(L2(leaf_pts(239, 372, deg(-10), 15, 4)), fill=R)              # inner ear
    d.arc([P(220, 374), P(230, 384)], 200, 340, fill=K, width=4)           # mild eye
    disk(d, *P(209, 392), 3, K, 0)                                          # nostril
    d.line(L2([(205, 399), (213, 399)]), fill=K, width=3)
    # hooves
    opoly(d, L2([(202, 421), (209, 421), (209, 429), (201, 429)]), K, 2)
    opoly(d, L2([(316, 427), (322, 427), (322, 434), (316, 434)]), K, 2)
    # a garland of small flowers round the neck (the feast day)
    for k in range(5):
        x, y = 244 - k * 1.2, 380 + k * 8
        flower(d, x * S, y * S, 5, 8, 8, R if k % 2 == 0 else Y, Y if k % 2 == 0 else R, 3)
    return img

img = lamb(img)

# ------------------------------------------------------------------ hare, sitting up alert
def hare(img):
    def sil(dd):
        dd.ellipse([P(258, 214), P(318, 270)], fill=255)      # body/haunch
        dd.ellipse([P(246, 206), P(282, 252)], fill=255)      # chest
        dd.ellipse([P(234, 192), P(266, 220)], fill=255)      # head
        dd.polygon(L2([(234, 204), (228, 212), (236, 216)]), fill=255)
        dd.polygon(L2(leaf_pts(250, 198, deg(-70), 46, 12)), fill=255)   # ears
        dd.polygon(L2(leaf_pts(258, 200, deg(-48), 44, 12)), fill=255)
        dd.ellipse([P(246, 252), P(268, 264)], fill=255)      # forepaws
        dd.ellipse([P(264, 258), P(312, 274)], fill=255)      # hind foot
        dd.ellipse([P(310, 236), P(326, 254)], fill=255)      # scut
    img, m = body(img, sil, Y, 4)
    inner = erode(m, 3)
    def hatch(dd):
        for k in range(12):
            a = deg(200 + k * 13)
            x0, y0 = 288 + math.cos(a) * 30, 242 + math.sin(a) * 28
            dd.line([P(x0, y0), P(288 + math.cos(a) * 21, 242 + math.sin(a) * 20)], fill=255, width=5)
        for k in range(5):
            dd.line([P(240 + k * 5, 194), P(242 + k * 5, 202)], fill=255, width=4)
        dd.polygon(L2(leaf_pts(252, 194, deg(-70), 36, 4)), fill=255)
        dd.polygon(L2(leaf_pts(260, 197, deg(-48), 34, 4)), fill=255)
    img = clipped(img, inner, hatch, R)
    d = ImageDraw.Draw(img)
    # white belly and scut
    for k in range(6):   # pale chest, hatched in white
        y0 = 222 + k * 5
        d.line([P(249 + abs(k - 2.5) * 1.2, y0), P(257 + abs(k - 2.5) * 0.8, y0 + 2)], fill=WH, width=4)
    d.ellipse([P(313, 239), P(323, 251)], fill=WH)
    disk(d, *P(246, 203), 6, K, 0)
    disk(d, *P(245, 202), 2, WH, 0)
    disk(d, *P(232, 209), 3, K, 0)
    d.line(L2([(228, 214), (220, 212)]), fill=K, width=2)
    d.line(L2([(228, 216), (220, 219)]), fill=K, width=2)
    d.line(L2(bez((276, 236), (290, 222), (304, 236), 6)), fill=K, width=4)   # haunch
    d.line(L2([(256, 256), (256, 262)]), fill=K, width=3)
    return img

img = hare(img)

# ------------------------------------------------------------------ birds
def goldfinch(img, x, y, flip=1, flying=False):
    def X(u): return x + u * flip
    def sil(dd):
        dd.ellipse([P(min(X(-14), X(14)), y - 8), P(max(X(-14), X(14)), y + 10)], fill=255)
        dd.ellipse([P(min(X(6), X(24)), y - 14), P(max(X(6), X(24)), y + 3)], fill=255)
        dd.polygon(L2([(X(22), y - 9), (X(31), y - 6), (X(22), y - 3)]), fill=255)
        dd.polygon(L2([(X(-12), y - 2), (X(-30), y + 4), (X(-28), y + 10), (X(-10), y + 6)]), fill=255)
        if flying:
            dd.polygon(L2([(X(-6), y - 4), (X(-18), y - 30), (X(-4), y - 26), (X(8), y - 4)]), fill=255)
    img, m = body(img, sil, Y, 3)  # buff body
    d = ImageDraw.Draw(img)
    # red face, black cap, white cheek
    d.ellipse([P(min(X(17), X(25)), y - 11), P(max(X(17), X(25)), y - 3)], fill=R)
    d.pieslice([P(min(X(6), X(24)), y - 14), P(max(X(6), X(24)), y + 3)], 200 if flip > 0 else -20, 290 if flip > 0 else 70, fill=K)
    d.ellipse([P(min(X(8), X(15)), y - 7), P(max(X(8), X(15)), y)], fill=WH)
    disk(d, *P(X(19), y - 8), 3, K, 0)
    # black wing with yellow bar & white spots
    wing = L2([(X(-12), y - 5), (X(6), y - 6), (X(8), y + 2), (X(-14), y + 5)])
    if flying:
        wing = L2([(X(-5), y - 4), (X(-17), y - 29), (X(-4), y - 25), (X(7), y - 4)])
    opoly(d, wing, K, 2)
    if flying:
        d.line(L2([(X(-9), y - 14), (X(2), y - 13)]), fill=Y, width=6)
        for u in (-14, -9):
            disk(d, *P(X(u), y - 24), 3, WH, 0)
    else:
        d.line(L2([(X(-8), y - 1), (X(4), y - 2)]), fill=Y, width=6)
        disk(d, *P(X(-12), y + 3), 3, WH, 0)
    d.line(L2([(X(-14), y + 2), (X(-27), y + 7)]), fill=K, width=4)
    if not flying:
        d.line(L2([(X(0), y + 10), (X(-2), y + 17)]), fill=K, width=3)
        d.line(L2([(X(4), y + 10), (X(6), y + 17)]), fill=K, width=3)
        d.line(L2([(X(-6), y + 17), (X(10), y + 17)]), fill=K, width=3)
    return img

img = goldfinch(img, 203, 76, flip=1, flying=True)

def bluebird(img, x, y):
    # a little blue bird on the ground, facing the wolf (left)
    def sil(dd):
        dd.ellipse([P(x - 16, y - 10), P(x + 14, y + 12)], fill=255)
        dd.ellipse([P(x - 22, y - 20), P(x - 4, y - 2)], fill=255)
        dd.polygon(L2([(x - 21, y - 14), (x - 31, y - 10), (x - 21, y - 7)]), fill=255)
        dd.polygon(L2([(x + 10, y - 2), (x + 30, y - 12), (x + 32, y - 6), (x + 12, y + 8)]), fill=255)
    img, m = body(img, sil, B, 3)
    d = ImageDraw.Draw(img)
    d.ellipse([P(x - 14, y), P(x + 6, y + 12)], fill=WH)          # pale breast
    d.ellipse([P(x - 21, y - 6), P(x - 11, y + 4)], fill=R)       # red throat (a robin's)
    disk(d, *P(x - 15, y - 13), 3, WH, 0)
    disk(d, *P(x - 15, y - 13), 1.6, K, 0)
    d.line(L2([(x - 4, y - 4), (x + 10, y - 2), (x + 4, y + 6)]), fill=K, width=3)   # wing
    for u in (0, 5):
        d.line(L2([(x - 2 + u, y - 1), (x + 4 + u, y + 3)]), fill=WH, width=3)
    d.line(L2([(x - 4, y + 12), (x - 6, y + 20)]), fill=K, width=3)
    d.line(L2([(x + 2, y + 12), (x + 3, y + 20)]), fill=K, width=3)
    d.line(L2([(x - 12, y + 20), (x + 8, y + 20)]), fill=K, width=3)
    return img

img = bluebird(img, 210, 446)

# ------------------------------------------------------------------ snail
def snail(img, x, y):
    def sil(dd):
        dd.polygon(L2([(x - 32, y + 14), (x - 26, y + 4), (x + 22, y + 6), (x + 34, y + 14), (x + 26, y + 18), (x - 30, y + 18)]), fill=255)
        dd.polygon(L2([(x + 20, y + 8), (x + 30, y - 4), (x + 36, y + 2), (x + 32, y + 12)]), fill=255)
    img, m = body(img, sil, WH, 3)
    d = ImageDraw.Draw(img)
    for (ex, ey) in ((x + 38, y - 14), (x + 30, y - 16)):
        d.line(L2([(x + 30, y), (ex, ey)]), fill=K, width=4)
        disk(d, *P(ex, ey), 4.5, K, 0)
    d.ellipse([P(x - 22, y - 22), P(x + 18, y + 14)], fill=Y, outline=K, width=4)
    # spiral
    pts = []
    for i in range(60):
        t = i / 59
        a = 4.2 * math.pi * t
        rr = 17 * (1 - t) + 2
        pts.append(P(x - 2 + math.cos(a) * rr, y - 4 + math.sin(a) * rr * 0.9))
    d.line(pts, fill=R, width=5, joint="curve")
    d.line(L2([(x - 22, y + 13), (x + 22, y + 13)]), fill=K, width=2)
    return img

img = snail(img, 296, 492)

# ------------------------------------------------------------------ banderole with the inscription
d = ImageDraw.Draw(img)
def banderole(img):
    d = ImageDraw.Draw(img)
    y0, y1 = 538, 568
    # curled ends (behind)
    for s in (-1, 1):
        cx = 200 + s * 168
        tail = [(cx - s * 14, y0 + 8), (cx + s * 12, y0 + 6), (cx + s * 4, (y0 + y1) / 2 + 4), (cx + s * 14, y1 + 6), (cx - s * 14, y1 + 4)]
        opoly(d, L2(tail), R, 4)
        d.line(L2([(cx - s * 14, y0 + 8), (cx - s * 6, y1 + 4)]), fill=K, width=3)
    # main ribbon with slight wave
    top = [(x, y0 + 3 * math.sin((x - 34) / 332 * math.pi * 2)) for x in range(34, 367, 6)]
    bot = [(x, y1 + 3 * math.sin((x - 34) / 332 * math.pi * 2)) for x in range(366, 33, -6)]
    opoly(d, L2(top + bot), WH, 4)
    # folds
    for s in (-1, 1):
        cx = 200 + s * 166
        opoly(d, L2([(cx, y0 + 2 + (s > 0) * 1), (cx + s * 6, y0 + 8), (cx + s * 6, y1 + 6), (cx, y1)]), Y, 3)
    text = "LAUDATO SI', MI' SIGNORE"
    f = font("serif-b", 36)
    tw = d.textlength(text, font=f)
    tx = W2 / 2 - tw / 2
    ty = (y0 + y1) * S / 2
    # first letter in blue as an illuminated initial, the rest red
    d.text((tx, ty), text[0], font=f, fill=B, anchor="lm")
    d.text((tx + d.textlength(text[0], font=f), ty), text[1:], font=f, fill=R, anchor="lm")
    # little stops
    for s in (-1, 1):
        disk(d, W2 / 2 + s * (tw / 2 + 14), ty, 5, K, 0)
    return img

img = banderole(img)

# ------------------------------------------------------------------ woven selvedge border
def border(img):
    a = np.asarray(img).copy()
    b = BORDER * S
    a[:b, :] = R; a[-b:, :] = R; a[:, :b] = R; a[:, -b:] = R
    img = Image.fromarray(a)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W2 - 1, H2 - 1], outline=K, width=4)
    d.rectangle([b - 4, b - 4, W2 - b + 3, H2 - b + 3], outline=K, width=4)
    d.rectangle([b - 8, b - 8, W2 - b + 7, H2 - b + 7], outline=Y, width=4)
    m = b / 2 - 1
    step = 32
    def motif(x, y, k):
        if k % 2 == 0:
            pts = [(x, y - 7), (x + 8, y), (x, y + 7), (x - 8, y)]
            d.polygon(pts, fill=WH, outline=K)
            d.line(pts + [pts[0]], fill=K, width=2)
            d.rectangle([x - 2, y - 2, x + 1, y + 1], fill=B)
        else:
            d.rectangle([x - 3, y - 3, x + 2, y + 2], fill=Y)
    for i, x in enumerate(range(step // 2, W2, step // 2)):
        motif(x, m + 1, i); motif(x, H2 - m - 2, i)
    for i, y in enumerate(range(step // 2, H2, step // 2)):
        motif(m + 1, y, i); motif(W2 - m - 2, y, i)
    for (x, y) in ((m, m), (W2 - m, m), (m, H2 - m), (W2 - m, H2 - m)):
        d.rectangle([x - 10, y - 10, x + 9, y + 9], fill=B, outline=K, width=3)
        d.rectangle([x - 4, y - 4, x + 3, y + 3], fill=Y)
    return img

img = border(img)

def finish_mode(img):
    """2x -> 1x by majority vote per 2x2 block (ties go to ink: K > R > B > Y > WH > G), so a
    black/white edge never averages to grey (which would snap to green)."""
    a = np.asarray(img).astype(np.int32)
    order = [K, R, B, Y, WH, G]
    idx = np.zeros(a.shape[:2], np.int8)
    for i, c in enumerate(order):
        idx[(a[..., 0] == c[0]) & (a[..., 1] == c[1]) & (a[..., 2] == c[2])] = i
    blocks = idx.reshape(H, 2, W, 2).transpose(0, 2, 1, 3).reshape(H, W, 4)
    counts = np.stack([(blocks == i).sum(-1) for i in range(6)], -1).astype(np.float32)
    counts -= np.arange(6) * 0.01
    out = np.array(order, np.uint8)[counts.argmax(-1)]
    Image.fromarray(out).save(os.environ.get("OUT_RAW", "out.png"))

finish_mode(img)
