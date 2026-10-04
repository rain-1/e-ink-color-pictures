# 3 - afternoon (14:00): The Sermon to the Birds.
# "Laudato si', mi' Signore, per frate Vento / et per aere et nubilo et sereno et onne tempo"
# An early-Italian fresco panel after the Upper Basilica at Assisi: ultramarine ground,
# faceted ochre rocks, a clumped tree, Francis and a companion, and a congregation of birds.
import os, sys, math
sys.path.insert(0, os.path.dirname(__file__))
from common import *

rng = np.random.default_rng(1226)
img, d = new(B)

# ---------- layout (2x px) ----------
BW = 34                     # cosmatesque border band
PX0, PY0, PX1, PY1 = BW, BW, W2 - BW, 1086   # picture field
IY0, IY1 = PY1, H2 - BW      # inscription band

OL = 4                      # outline width at 2x (= 2px on the panel)
BROWN_T = 0.5

def const(t):
    return np.full((H, W), t, np.float32)

def poly_mask(pts):
    return mask_of(lambda m: m.polygon([tuple(p) for p in pts], fill=255))

def tone_poly(pts, t, ink, paper, outline=None, w=OL):
    global img, d
    m = poly_mask(pts)
    img = tone_fill(img, m, t if isinstance(t, np.ndarray) else const(t), ink, paper)
    d = ImageDraw.Draw(img)
    if outline is not None:
        d.line([tuple(p) for p in pts] + [tuple(pts[0])], fill=outline, width=w, joint="curve")

def poly(pts, fill, outline=K, w=OL):
    d.polygon([tuple(p) for p in pts], fill=fill)
    if outline is not None:
        d.line([tuple(p) for p in pts] + [tuple(pts[0])], fill=outline, width=w, joint="curve")

def ellpts(cx, cy, rx, ry, rot=0.0, a0=0, a1=360, n=28):
    out = []
    c, s = math.cos(rot), math.sin(rot)
    for i in range(n + 1):
        a = math.radians(a0 + (a1 - a0) * i / n)
        x, y = rx * math.cos(a), ry * math.sin(a)
        out.append((cx + x * c - y * s, cy + x * s + y * c))
    return out

def circle(cx, cy, r, fill, outline=K, w=OL):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill, outline=outline, width=w if outline else 0)

def bez(p0, p1, p2, n=16):
    return [((1-t)**2*p0[0] + 2*(1-t)*t*p1[0] + t*t*p2[0],
             (1-t)**2*p0[1] + 2*(1-t)*t*p1[1] + t*t*p2[1]) for t in np.linspace(0, 1, n)]

# ======================================================================
# SKY: clean ultramarine, stylised clouds, Brother Wind
# ======================================================================
def cloud(cx, cy, lobes, r0):
    """Fresco cloud: a row of white lobes with a flat base, blue scallop lines inside."""
    pts = []
    xs = np.linspace(-1, 1, lobes)
    circs = []
    for i, u in enumerate(xs):
        r = r0 * (0.75 + 0.45 * (1 - abs(u)) + 0.1 * rng.random())
        circs.append((cx + u * r0 * lobes * 0.55, cy - r * 0.35, r))
    base = cy + r0 * 0.35
    for (x, y, r) in circs:
        d.ellipse([x - r, y - r, x + r, min(y + r, base)], fill=WH)
    d.rectangle([circs[0][0], cy - 4, circs[-1][0], base], fill=WH)
    # lower band of the cloud screened faintly blue (a cool belly)
    global img
    m = mask_of(lambda mm: mm.rectangle([circs[0][0] - r0, base - r0 * 0.35, circs[-1][0] + r0, base], fill=255))
    a = np.asarray(img)
    m = m & np.all(a == WH, axis=-1)
    img = tone_fill(img, m, const(0.3), B, WH)
    dd = ImageDraw.Draw(img)
    # scallop lines: the inner contour of each lobe
    for (x, y, r) in circs:
        dd.arc([x - r * 0.72, y - r * 0.72, x + r * 0.72, y + r * 0.72], 190, 340, fill=B, width=4)
    dd.line([(circs[0][0] - 4, base), (circs[-1][0] + 4, base)], fill=B, width=4)
    return dd

d = cloud(160, 150, 5, 34)
d = cloud(330, 95, 3, 24)
d = cloud(700, 120, 4, 26)

def wind(p0, p1, p2, curl_r, sign=1):
    pts = bez(p0, p1, p2, 24)
    # end in a spiral curl
    cx, cy = p2[0], p2[1] - sign * curl_r
    for i in range(1, 22):
        a = math.pi / 2 * sign + i * 0.32 * sign
        r = curl_r * (1 - i / 26)
        pts.append((cx + r * math.cos(a) * -1, cy + r * math.sin(a)))
    d.line(pts, fill=WH, width=5, joint="curve")

wind((420, 250), (520, 210), (600, 240), 22, 1)
wind((440, 280), (520, 262), (575, 285), 14, 1)
wind((60, 300), (130, 270), (210, 300), 18, 1)

# loose leaves riding the wind
def leaf(x, y, L, ang, col, w=3):
    pts = []
    for t in np.linspace(0, 1, 9):
        pts.append((t * L, -math.sin(math.pi * t) * L * 0.28))
    for t in np.linspace(1, 0, 9):
        pts.append((t * L, math.sin(math.pi * t) * L * 0.28))
    c, s = math.cos(ang), math.sin(ang)
    pts = [(x + px * c - py * s, y + px * s + py * c) for px, py in pts]
    d.polygon(pts, fill=col, outline=K, width=w)
    d.line([pts[0], (x + L * 0.8 * c, y + L * 0.8 * s)], fill=K, width=2)

for (x, y, a, c) in [(612, 205, 0.6, Y), (230, 330, -0.4, G), (650, 268, 2.0, G), (100, 330, 1.2, Y)]:
    leaf(x, y, 24, a, c)

# ======================================================================
# GROUND: ochre with fresco mottle
# ======================================================================
gx = np.linspace(PX0, PX1, 40)
gy = 870 + 14 * np.sin(gx / 90.0) + 8 * np.sin(gx / 37.0 + 1)
ground = [(PX0, PY1)] + list(zip(gx, gy)) + [(PX1, PY1)]
mott = 0.04 + 0.18 * noise(H, W, 40, seed=3)
gm = poly_mask(ground)
img = tone_fill(img, gm, mott, R, Y)
# a few darker earth flecks (very light black)
fl = noise(H, W, 14, seed=7)
img = paint(img, gm & up((fl > 0.86) & (threshold_1x() < 0.25)), K)
d = ImageDraw.Draw(img)
d.line(list(zip(gx, gy)), fill=K, width=OL)

# ---------- Giotto rocks ----------
def peak(ax, ay, wl, wr, base, seed=0, flat=26):
    """Giotto mountain: a chiselled wedge with a flat summit ledge, lit left face,
    shaded right face, a stepped ridge between, horizontal strata on both."""
    r = np.random.default_rng(seed)
    lf = (ax - wl, base); rf = (ax + wr, base)
    t0 = (ax - flat * 0.6, ay); t1 = (ax + flat * 0.6, ay + 6)
    rx = ax + wr * 0.25
    ridge = [t1]
    n = 4
    for k in range(1, n + 1):
        yy = ay + (base - ay) * k / n
        xx = t1[0] + (rx - t1[0]) * k / n + (8 if k % 2 else -4)
        ridge.append((xx, yy))
    lsh = (ax - wl * 0.55, ay + (base - ay) * 0.4)
    rsh = (ax + wr * 0.7, ay + (base - ay) * 0.45)
    left_face = [lf, lsh, t0, t1] + ridge[1:]
    right_face = [t1] + ridge[1:] + [rf, rsh]
    tone_poly(left_face, 0.3, Y, WH)
    tone_poly(right_face, 0.45, R, Y)
    # deep cleft at the foot of the shaded face
    tone_poly([ridge[-2], ridge[-1], (rx + wr * 0.3, base), (ridge[-2][0] + wr * 0.2, ridge[-2][1] + 10)], 0.35, K, R)
    # strata steps on both faces
    for k in range(1, 6):
        yy = ay + (base - ay) * k / 6 + r.integers(-6, 7)
        fr = (yy - ay) / (base - ay)
        xl = ax - wl * min(1, fr * 1.4) * 0.9 + 8
        xr_ = t1[0] + (rx - t1[0]) * fr - 6
        if xr_ - xl > 16:
            d.line([(xl, yy), ((xl + xr_) / 2, yy - 4), (xr_, yy + 3)], fill=K, width=3)
        xs = t1[0] + (rx - t1[0]) * fr + 8; xe = ax + wr * min(1, fr * 1.3) * 0.75 - 6
        if xe - xs > 14:
            d.line([(xs, yy + 4), (xe, yy + 10)], fill=K, width=3)
    d.line(ridge, fill=K, width=3, joint="curve")
    ld = [t0, t1, (t1[0] - 4, t1[1] + 12), (t0[0] + 4, t0[1] + 12)]
    poly(ld, WH, K, 3)
    d.line([lf, lsh, t0, t1, rsh, rf], fill=K, width=OL, joint="curve")

# left crag behind the friars, back to front
peak(84, 540, 70, 170, 900, seed=41, flat=34)
peak(300, 690, 110, 100, 900, seed=43, flat=26)
peak(46, 700, 30, 80, 900, seed=44, flat=20)
# outcrop under the tree
peak(650, 790, 110, 130, 930, seed=46, flat=28)
peak(548, 845, 70, 80, 930, seed=47, flat=20)
peak(752, 840, 50, 40, 930, seed=48, flat=16)
# a few rocks out on the ground
for i, (x, y, w, h) in enumerate([(668, 928, 84, 54), (318, 1022, 58, 38), (690, 1048, 66, 32)]):
    peak(x + w * 0.4, y, w * 0.4, w * 0.6, y + h, seed=80 + i, flat=12)
    d.line([(x, y + h), (x + w, y + h)], fill=K, width=OL)
d.line(list(zip(gx, gy)), fill=K, width=OL)
# pebbles
for i in range(16):
    x = rng.uniform(300, 750); y = rng.uniform(895, 1075)
    r = rng.uniform(4, 6)
    pts = ellpts(x, y, r * 1.4, r, rng.uniform(0, 1), n=6)
    poly(pts, WH if i % 3 else Y, K, 3)

# ---------- plant tufts ----------
def tuft(x, y, n=5, h=28, flower=None):
    for k in range(n):
        a = math.radians(-90 + (k - (n - 1) / 2) * 22)
        L = h * (0.7 + 0.3 * (1 - abs(k - (n - 1) / 2) / n))
        tip = (x + L * math.cos(a), y + L * math.sin(a))
        mid = (x + L * 0.5 * math.cos(a) - 3, y + L * 0.5 * math.sin(a))
        d.polygon([(x - 4, y), mid, tip, (x + 4, y)], fill=G, outline=K, width=2)
    if flower:
        fx, fy = x + 2, y - h - 6
        for k in range(5):
            a = k * 2 * math.pi / 5
            circle(fx + 6 * math.cos(a), fy + 6 * math.sin(a), 5, flower, K, 2)
        circle(fx, fy, 4, Y if flower != Y else R, None)

for (x, y, f) in [(320, 905, R), (590, 900, None), (760 - 30, 900, WH), (360, 1075, None),
                  (560, 1080, R), (470, 935, None), (80, 1078, WH), (200, 1080, None), (255, 862, R),
                  (150, 806, None), (60, 760, R), (300, 788, WH)]:
    tuft(x, y, 5, 26, f)

# ======================================================================
# TREES
# ======================================================================
def brown_poly(pts):
    tone_poly(pts, 0.5, K, R, outline=K)

def limb(path, w0, w1):
    """tapering limb as polygon along a polyline."""
    path = np.array(path, float)
    L = len(path)
    left, right = [], []
    for i in range(L):
        p = path[i]
        q = path[min(i + 1, L - 1)] - path[max(i - 1, 0)]
        n = np.array([-q[1], q[0]]) / (np.hypot(*q) + 1e-6)
        wv = w0 + (w1 - w0) * i / (L - 1)
        left.append(tuple(p + n * wv / 2)); right.append(tuple(p - n * wv / 2))
    return left + right[::-1]

def clump(cx, cy, r, seed, n=None):
    """Clumped leaf mass: dark green core, then every leaf drawn, lit from upper left."""
    global img, d
    rr = np.random.default_rng(seed)
    core = ellpts(cx, cy, r, r * 0.82, n=30)
    tone_poly(core, 0.3, K, G)
    n = n or int(r * r / 75)
    leaves = []
    for _ in range(n):
        a = rr.uniform(0, 2 * math.pi); rad = r * math.sqrt(rr.uniform(0.05, 1.0))
        x = cx + rad * math.cos(a); y = cy + rad * 0.82 * math.sin(a)
        leaves.append((y, x, a))
    leaves.sort()
    for y, x, a in leaves:
        lit = (x - cx) * -0.6 + (y - cy) * -0.8
        col = Y if lit > r * 0.45 else G
        ang = a + rr.uniform(-0.6, 0.6)
        leaf(x - 10 * math.cos(ang), y - 10 * math.sin(ang), 26, ang, col, 3)
    d.line(core, fill=K, width=3)

# little tree on the crag
d.line([(84, 540), (80, 480), (70, 420)], fill=K, width=14)
d.line([(84, 540), (80, 480), (70, 420)], fill=R, width=6)
d.line([(82, 490), (116, 462)], fill=K, width=10)
clump(68, 400, 44, 11)
clump(124, 452, 30, 12)
tuft(112, 540, 5, 22, R)
tuft(590, 846, 4, 20, WH)

# main tree (right)
trunk = limb([(640, 1000), (628, 880), (622, 760), (616, 640), (612, 540)], 54, 26)
branches = [
    [(618, 660), (560, 600), (490, 545), (420, 500)],
    [(616, 600), (680, 520), (730, 470), (760, 450)],
    [(612, 545), (580, 450), (545, 360), (520, 300)],
    [(612, 545), (630, 450), (650, 330)],
    [(622, 740), (690, 700), (745, 680)],
]
brown_poly(trunk)
for b in branches:
    brown_poly(limb(b, 20, 8))
# bark lines
for k in range(8):
    y0 = 600 + k * 50
    d.arc([600, y0, 650, y0 + 40], 200, 320, fill=K, width=3)

clumps = [(445, 430, 66, 21), (525, 270, 74, 22), (655, 260, 80, 23), (742, 380, 56, 24),
          (565, 440, 52, 25), (712, 580, 52, 26), (600, 175, 50, 27), (440, 560, 40, 28)]
for c in clumps:
    clump(*c)
# re-draw some limb segments in front of the leaves so perches show
front_limbs = [
    [(560, 600), (490, 545), (430, 505)],
    [(616, 600), (680, 520), (730, 470)],
    [(622, 740), (690, 700), (745, 680)],
    [(612, 545), (590, 470)],
]
for b in front_limbs:
    brown_poly(limb(b, 16, 9))

# ======================================================================
# FIGURES
# ======================================================================
def skin_poly(pts, w=OL):
    tone_poly(pts, 0.28, R, WH, outline=K, w=w)

def halo(cx, cy, r):
    circle(cx, cy, r, Y, K, OL)
    d.ellipse([cx - r + 6, cy - r + 6, cx + r - 6, cy + r - 6], outline=R, width=8)
    # punched decoration: ring of red dots inside the rim
    for k in range(28):
        a = k * 2 * math.pi / 28
        circle(cx + (r - 22) * math.cos(a), cy + (r - 22) * math.sin(a), 3, R, None)
    d.ellipse([cx - r + 30, cy - r + 30, cx + r - 30, cy + r - 30], outline=R, width=2)

def hand(x, y, ang, flip=1):
    """open hand, palm with four fingers + thumb, pointing along ang."""
    c, s = math.cos(ang), math.sin(ang)
    def T(u, v):
        return (x + u * c - v * s * flip, y + u * s + v * c * flip)
    palm = [T(0, -11), T(20, -12), T(24, 10), T(0, 11)]
    skin_poly(palm, 3)
    for k, v in enumerate([-9, -3, 3, 9]):
        L = [14, 17, 16, 12][k]
        d.line([T(20, v), T(20 + L, v * 1.2)], fill=K, width=8)
        d.line([T(20, v), T(19 + L, v * 1.2)], fill=WH, width=4)
    d.line([T(6, -11), T(14, -24)], fill=K, width=8)
    d.line([T(6, -11), T(13, -23)], fill=WH, width=4)

def head(cx, cy, look=1, beard=True):
    """3/4 head facing right, tonsured."""
    face = ellpts(cx, cy, 34, 43, n=30)
    skin_poly(face)
    # tonsure: crown bare, a ring of hair round the head at brow level, fuller at the back
    ring = ellpts(cx, cy - 20, 37, 15, a0=0, a1=180, n=16) + ellpts(cx, cy - 22, 33, 8, a0=180, a1=0, n=16)
    poly(ring, K, K, 2)
    backh = ellpts(cx, cy, 35, 44, a0=150, a1=215, n=10) + [(cx - 20, cy - 10), (cx - 24, cy + 18)]
    poly(backh, K, K, 2)
    # ear
    skin_poly(ellpts(cx - 16, cy + 2, 7, 11, n=12), 3)
    # features
    ex = cx + 16
    d.line([(ex - 10, cy - 6), (ex + 8, cy - 9)], fill=K, width=4)          # brow
    circle(ex, cy + 1, 4, K, None)                                         # eye
    d.line([(cx + 30, cy - 4), (cx + 37, cy + 14), (cx + 29, cy + 16)], fill=K, width=4)  # nose
    d.line([(cx + 16, cy + 26), (cx + 28, cy + 25)], fill=R, width=4)       # mouth
    if beard:
        bd = ellpts(cx, cy, 35, 45, a0=5, a1=175, n=18) + [(cx - 28, cy + 18)] + ellpts(cx + 6, cy + 17, 27, 16, a0=160, a1=20, n=14) + [(cx + 33, cy + 18)]
        poly(bd, K, K, 2)
        d.line([(cx + 16, cy + 27), (cx + 28, cy + 26)], fill=R, width=4)

def habit(sil, folds, lights, cowl):
    tone_poly(sil, BROWN_T, K, R, outline=K)
    for L in lights:                       # lit fold ridges in plain red
        poly(L, R, None)
    for f in folds:
        d.line(f, fill=K, width=OL, joint="curve")
    tone_poly(cowl, BROWN_T, K, R, outline=K)
    d.line(sil + [sil[0]], fill=K, width=OL, joint="curve")

def cord(pts, hang):
    d.line(pts, fill=K, width=12, joint="curve")
    d.line(pts, fill=WH, width=6, joint="curve")
    d.line(hang, fill=K, width=12, joint="curve")
    d.line(hang, fill=WH, width=6, joint="curve")
    for t in (0.35, 0.65, 0.95):
        i = int(t * (len(hang) - 1))
        circle(hang[i][0], hang[i][1], 8, WH, K, 3)

def foot(x, y, dirn=1):
    pts = [(x - 16 * dirn, y - 14), (x + 18 * dirn, y - 12), (x + 38 * dirn, y + 2), (x + 38 * dirn, y + 8),
           (x - 16 * dirn, y + 8)]
    skin_poly(pts, OL)
    for k in range(3):
        d.line([(x + (22 + k * 6) * dirn, y - 4), (x + (22 + k * 6) * dirn, y + 6)], fill=K, width=3)

# --- companion friar (behind) ---
halo(140, 590, 66)
csil = [(118, 632), (165, 632), (190, 660), (205, 760), (215, 900), (232, 1030), (60, 1032),
        (70, 930), (80, 800), (90, 680)]
habit(csil,
      folds=[[(105, 790), (95, 900), (88, 1030)], [(140, 790), (138, 900), (140, 1030)],
             [(175, 790), (185, 900), (195, 1030)], [(100, 700), (120, 760)]],
      lights=[[(112, 800), (122, 800), (118, 1028), (104, 1028)], [(152, 800), (160, 800), (170, 1028), (156, 1028)]],
      cowl=[(100, 628), (180, 628), (196, 668), (160, 690), (110, 688), (88, 662)])
cord([(84, 790), (140, 800), (204, 788)], [(170, 798), (176, 870), (172, 940)])
# raised hand in wonder (palm out)
tone_poly([(160, 700), (205, 690), (215, 720), (170, 740)], BROWN_T, K, R, outline=K)
hand(212, 698, -1.3, 1)
head(142, 592, beard=True)

# --- Saint Francis ---
halo(272, 532, 80)
# rear arm (behind body) reaching toward the birds, higher
rear = [(290, 628), (360, 618), (430, 628), (440, 664), (380, 676), (320, 684)]
tone_poly(rear, BROWN_T, K, R, outline=K)
d.line([(330, 640), (420, 640)], fill=K, width=3)
hand(440, 640, 0.15, 1)
fsil = [(252, 588), (304, 590), (336, 622), (346, 700), (348, 800), (360, 900), (380, 1000),
        (386, 1030), (176, 1034), (168, 1000), (182, 900), (194, 800), (204, 700), (216, 630)]
habit(fsil,
      folds=[[(214, 790), (206, 900), (196, 1030)], [(248, 790), (244, 900), (240, 1030)],
             [(284, 790), (290, 900), (296, 1030)], [(320, 790), (334, 900), (350, 1030)],
             [(230, 650), (262, 760)], [(312, 650), (300, 760)], [(270, 640), (282, 760)]],
      lights=[[(222, 800), (234, 800), (228, 1030), (210, 1030)],
              [(258, 800), (270, 800), (270, 1030), (254, 1030)],
              [(296, 800), (306, 800), (318, 1030), (304, 1030)],
              [(240, 660), (250, 660), (268, 760), (258, 760)]],
      cowl=[(226, 584), (316, 588), (340, 632), (300, 660), (250, 656), (210, 632)])
cord([(190, 772), (266, 788), (346, 772)], [(300, 784), (308, 860), (300, 940), (310, 1000)])
foot(330, 1046, 1)
foot(240, 1048, 1)
# front arm: wide sleeve reaching forward and slightly down, blessing the birds
front = [(296, 640), (346, 646), (440, 690), (458, 734), (428, 752), (338, 722), (300, 692)]
tone_poly(front, BROWN_T, K, R, outline=K)
poly([(330, 660), (430, 700), (440, 712), (340, 684)], R, None)
d.line([(338, 700), (440, 736)], fill=K, width=3)
hand(456, 720, 0.45, 1)
head(282, 540)

# ======================================================================
# BIRDS
# ======================================================================
SP = {
    # body, back, head, cap, face, breast, wing, bars, tail, beak
    "robin":     dict(body=WH, head=K, cap=None, face=R, breast=R, wing=K, bars=WH, tail=K, beak=K),
    "goldfinch": dict(body=WH, head=WH, cap=K, face=R, breast=Y, wing=K, bars=Y, tail=K, beak=WH, tailspots=WH),
    "bluetit":   dict(body=G, head=WH, cap=B, face=None, breast=Y, wing=B, bars=WH, tail=B, beak=K, stripe=K),
    "magpie":    dict(body=K, head=K, cap=None, face=None, breast=WH, wing=B, bars=WH, tail=K, beak=K, longtail=True, shoulder=WH),
    "dove":      dict(body=WH, head=WH, cap=None, face=None, breast=WH, wing=WH, bars=K, tail=WH, beak=R, collar=K),
    "swallow":   dict(body=B, head=B, cap=None, face=R, breast=WH, wing=K, bars=B, tail=K, beak=K, fork=True),
    "crow":      dict(body=K, head=K, cap=None, face=None, breast=None, wing=K, bars=B, tail=K, beak=K, bigbeak=True),
    "hoopoe":    dict(body=R, head=R, cap=None, face=None, breast=None, wing=K, bars=WH, tail=K, beak=K, crest=True, curved=True, zebra=True),
    "greenpecker": dict(body=G, head=G, cap=R, face=K, breast=Y, wing=G, bars=Y, tail=G, beak=K, bigbeak=True),
    "kingfisher": dict(body=B, head=B, cap=None, face=R, breast=R, wing=B, bars=WH, tail=B, beak=K, bigbeak=True, cheek=WH),
}

def bird(cx, cy, s, sp, facing=-1, tilt=0.0, pose="perch"):
    """Parametric bird. Local unit coords, head toward +x; facing=-1 mirrors to face left.
    (cx, cy) is the body centre, s the body length in 2x px."""
    p = SP[sp]
    ca, sa = math.cos(tilt), math.sin(tilt)
    def T(x, y):
        xr, yr = x * ca - y * sa, x * sa + y * ca
        return (cx + facing * xr * s, cy + yr * s)
    def Tl(pts):
        return [T(x, y) for x, y in pts]
    def E(x, y, rx, ry, rot=0, a0=0, a1=360, n=20):
        return Tl(ellpts(x, y, rx, ry, rot, a0, a1, n))
    ow = 3 if s < 40 else OL
    fly = pose == "fly"

    # far wing (flying): raised behind the body
    if fly:
        far = Tl([(0.05, -0.08), (-0.18, -0.72), (0.02, -0.82), (0.24, -0.12)])
        poly(far, p["wing"], K, ow)
    # legs
    if not fly:
        for lx in (0.02, -0.1):
            a = T(lx, 0.18)
            b = (a[0] - facing * 0.02 * s, cy + 0.42 * s)
            d.line([a, b], fill=K, width=5)
            d.line([b, (b[0] + facing * 0.14 * s, b[1])], fill=K, width=3)
            d.line([b, (b[0] - facing * 0.08 * s, b[1])], fill=K, width=3)
    # tail
    if p.get("fork"):
        tail = [(-0.3, -0.04), (-1.05, 0.0), (-0.72, 0.1), (-1.05, 0.26), (-0.3, 0.12)]
    elif p.get("longtail"):
        tail = [(-0.3, -0.04), (-1.15, 0.08), (-1.15, 0.2), (-0.3, 0.12)]
    elif fly:
        tail = [(-0.3, -0.02), (-0.8, -0.12), (-0.86, 0.08), (-0.8, 0.26), (-0.3, 0.12)]
    else:
        tail = [(-0.32, -0.04), (-0.82, 0.14), (-0.78, 0.28), (-0.3, 0.13)]
    poly(Tl(tail), p["tail"], K, ow)
    if p.get("tailspots"):
        for t in (0.55, 0.7):
            x, y = T(-t, 0.12 + (t - 0.5) * 0.15)
            circle(x, y, 3, WH, None)
    if p.get("longtail"):
        d.line([T(-0.4, 0.08), T(-1.1, 0.14)], fill=B, width=4)
    # body
    body = E(0, 0.04, 0.42, 0.25, -0.2)
    poly(body, p["body"], K, ow)
    if p["breast"] is not None:
        br = E(0.16, 0.1, 0.22, 0.15, -0.4, n=16)
        poly(br, p["breast"], None)
    if p.get("shoulder"):
        poly(E(-0.05, -0.02, 0.18, 0.08, -0.1, n=12), WH, None)
    d.line(body + [body[0]], fill=K, width=ow, joint="curve")
    # head
    hx, hy, hr = 0.36, -0.2, 0.19
    if p.get("crest"):
        for k in range(5):
            a = math.radians(-160 + k * 22)
            x0, y0 = hx + hr * 0.6 * math.cos(a), hy + hr * 0.6 * math.sin(a)
            x1, y1 = hx + hr * 1.9 * math.cos(a), hy + hr * 1.9 * math.sin(a)
            fe = Tl([(x0 - 0.04, y0), (x1, y1), (x0 + 0.04, y0)])
            poly(fe, Y, K, 2)
            tp = T(x1 * 0.85 + x0 * 0.15, y1 * 0.85 + y0 * 0.15)
            circle(tp[0], tp[1], 3, K, None)
    hd = E(hx, hy, hr, hr, n=20)
    poly(hd, p["head"], K, ow)
    if p["cap"] is not None:
        poly(E(hx, hy, hr, hr, a0=180, a1=360, n=12), p["cap"], None)
    if p["face"] is not None:
        poly(E(hx + 0.1, hy + 0.02, 0.11, 0.11, n=12), p["face"], None)
    if p.get("stripe"):
        d.line([T(hx - 0.14, hy + 0.02), T(hx + 0.17, hy - 0.02)], fill=K, width=4)
    if p.get("cheek"):
        poly(E(hx - 0.04, hy + 0.08, 0.07, 0.05, n=10), WH, None)
    if p.get("collar"):
        d.arc  # noop placeholder for readability
        d.line([T(hx - 0.12, hy + 0.12), T(hx + 0.02, hy + 0.17)], fill=K, width=4)
    d.line(hd + [hd[0]], fill=K, width=ow, joint="curve")
    # beak
    bx, by = hx + hr * 0.92, hy + 0.02
    if p.get("curved"):
        bk = Tl([(bx, by - 0.04)] + [(bx + 0.42 * t, by - 0.02 + 0.16 * t * t) for t in np.linspace(0, 1, 6)][1:] +
                [(bx, by + 0.04)])
        poly(bk, K, K, 2)
    else:
        L = 0.24 if p.get("bigbeak") else 0.15
        bk = Tl([(bx - 0.02, by - 0.06), (bx + L, by + 0.01), (bx - 0.02, by + 0.07)])
        poly(bk, p["beak"], K, 2)
    # eye (white ring on dark heads)
    ex, ey = T(hx + 0.06, hy - 0.04)
    er = max(3, s * 0.05)
    if p["head"] == K or p["head"] == B or p["face"] == K:
        circle(ex, ey, er + 3, WH, None)
    circle(ex, ey, er, K, None)
    # wing
    if fly:
        nw = Tl([(0.18, -0.06), (-0.05, -0.92), (0.16, -1.02), (0.4, -0.55), (0.34, -0.05)])
        poly(nw, p["wing"], K, ow)
        for k in range(4):
            t = 0.35 + k * 0.17
            a = (0.18 + (-0.05 - 0.18) * t, -0.06 + (-0.92 + 0.06) * t)
            b = (0.34 + (0.4 - 0.34) * t, -0.05 + (-0.55 + 0.05) * t)
            d.line([T(*a), T(*b)], fill=p["bars"], width=4)
        d.line(nw + [nw[0]], fill=K, width=ow, joint="curve")
    else:
        wg = [(0.2, -0.1), (-0.04, -0.17), (-0.44, -0.04), (-0.56, 0.08), (-0.12, 0.13), (0.14, 0.06)]
        poly(Tl(wg), p["wing"], K, ow)
        if p.get("zebra"):
            for x in (-0.38, -0.24, -0.1, 0.04):
                d.line([T(x, -0.12), T(x - 0.06, 0.1)], fill=WH, width=5)
        else:
            d.line([T(0.12, -0.02), T(-0.3, 0.02)], fill=p["bars"], width=4)
            for x in (-0.28, -0.4):
                d.line([T(x + 0.04, 0.04), T(x - 0.06, 0.1)], fill=p["bars"], width=3)
        d.line(Tl(wg) + [T(*wg[0])], fill=K, width=ow, joint="curve")

# --- congregation ---
ground_birds = [
    # back row
    (424, 906, 38, "dove"), (498, 904, 36, "goldfinch"), (566, 910, 36, "bluetit"), (712, 916, 38, "crow"),
    # middle row
    (412, 972, 46, "robin"), (494, 970, 46, "hoopoe"), (580, 976, 46, "magpie"), (668, 980, 44, "greenpecker"),
    (744, 990, 40, "goldfinch"),
    # front row
    (446, 1050, 54, "kingfisher"), (556, 1052, 56, "dove"), (660, 1056, 54, "robin"), (742, 1064, 44, "bluetit"),
]
tree_birds = [
    (478, 536, 40, "goldfinch", 0), (690, 500, 40, "robin", 0), (726, 672, 38, "dove", 0),
    (594, 470, 36, "greenpecker", 0), (520, 205, 40, "magpie", 0), (662, 192, 38, "goldfinch", 0),
    (742, 335, 34, "robin", 0), (440, 372, 38, "kingfisher", 0), (575, 400, 34, "bluetit", 0),
    (700, 255, 34, "hoopoe", 0),
]
fly_birds = [
    (390, 360, 38, "swallow", 0.35), (330, 270, 34, "dove", 0.25), (460, 150, 34, "swallow", 0.2),
    (600, 95, 32, "crow", 0.1), (240, 210, 30, "goldfinch", 0.3), (400, 610, 30, "bluetit", 0.4),
    (250, 396, 30, "robin", 0.45), (175, 335, 28, "swallow", 0.3), (100, 222, 28, "magpie", 0.15),
]
TILT = {"dove": -0.2, "crow": -0.22, "magpie": -0.25, "hoopoe": -0.25, "greenpecker": -0.3}
for (x, y, s, sp, t) in fly_birds:
    bird(x, y, s, sp, -1, t, "fly")
for (x, y, s, sp, t) in tree_birds:
    bird(x, y - s * 0.42, s, sp, -1, TILT.get(sp, -0.4))
for (x, y, s, sp) in sorted(ground_birds, key=lambda b: b[1]):
    bird(x, y - s * 0.42, s, sp, -1, TILT.get(sp, -0.4))

# ======================================================================
# FRAME: cosmatesque band + inscription
# ======================================================================
d.rectangle([0, IY0, W2, IY1], fill=K)
d.rectangle([0, 0, W2, BW], fill=R); d.rectangle([0, H2 - BW, W2, H2], fill=R)
d.rectangle([0, 0, BW, H2], fill=R); d.rectangle([W2 - BW, 0, W2, H2], fill=R)

def lozenges(x0, y0, x1, y1, horiz):
    L = 48
    if horiz:
        n = int((x1 - x0) // L); step = (x1 - x0) / n
        for i in range(n):
            cx = x0 + step * (i + 0.5); cy = (y0 + y1) / 2; hw, hh = step / 2 - 1, (y1 - y0) / 2 - 5
            poly([(cx - hw, cy), (cx, cy - hh), (cx + hw, cy), (cx, cy + hh)], WH, K, 3)
            inner = [B, G, Y][i % 3]
            poly([(cx - hw * 0.45, cy), (cx, cy - hh * 0.45), (cx + hw * 0.45, cy), (cx, cy + hh * 0.45)], inner, K, 2)
    else:
        n = int((y1 - y0) // L); step = (y1 - y0) / n
        for i in range(n):
            cy = y0 + step * (i + 0.5); cx = (x0 + x1) / 2; hh, hw = step / 2 - 1, (x1 - x0) / 2 - 5
            poly([(cx - hw, cy), (cx, cy - hh), (cx + hw, cy), (cx, cy + hh)], WH, K, 3)
            inner = [B, G, Y][i % 3]
            poly([(cx - hw * 0.45, cy), (cx, cy - hh * 0.45), (cx + hw * 0.45, cy), (cx, cy + hh * 0.45)], inner, K, 2)

lozenges(BW, 0, W2 - BW, BW, True)
lozenges(BW, H2 - BW, W2 - BW, H2, True)
lozenges(0, BW, BW, H2 - BW, False)
lozenges(W2 - BW, BW, W2, H2 - BW, False)
for (x, y) in [(0, 0), (W2 - BW, 0), (0, H2 - BW), (W2 - BW, H2 - BW)]:
    d.rectangle([x, y, x + BW, y + BW], fill=K)
    circle(x + BW / 2, y + BW / 2, 10, Y, R, 3)
# inner fillets
d.rectangle([BW, BW, W2 - BW, H2 - BW], outline=K, width=4)
d.rectangle([BW + 4, BW + 4, W2 - BW - 4, PY1 - 4], outline=WH, width=4)
d.line([(BW, IY0), (W2 - BW, IY0)], fill=WH, width=4)
d.rectangle([BW + 4, IY0 + 10, W2 - BW - 4, IY1 - 10], outline=Y, width=2)

text = "LAVDATO SI, MI SIGNORE, PER FRATE VENTO"
for size in range(34, 20, -1):
    f = font("dejavu-serif-b", size)
    bb = d.textbbox((0, 0), text, font=f)
    if bb[2] - bb[0] < W2 - 2 * BW - 70:
        break
tw, th = bb[2] - bb[0], bb[3] - bb[1]
tx = (W2 - tw) / 2; ty = (IY0 + IY1) / 2 - th / 2 - bb[1]
TXT = Image.new("L", (W2, H2), 0)
ImageDraw.Draw(TXT).text((tx, ty), text, font=f, fill=255)
for x in (BW + 20, W2 - BW - 20):
    cy = (IY0 + IY1) / 2
    d.line([(x - 9, cy), (x + 9, cy)], fill=R, width=5)
    d.line([(x, cy - 9), (x, cy + 9)], fill=R, width=5)

def mode_down(im):
    """2x -> 1x by majority vote per 2x2 block (ties go to ink over paper), so thin dark
    lines never average with yellow into a stray green. Returned at 2x for finish()."""
    a = np.asarray(im).astype(np.int32)
    idx = np.zeros(a.shape[:2], np.int32) - 1
    for i, c in enumerate(PAL.astype(np.int32)):
        idx[np.all(a == c, -1)] = i
    if (idx < 0).any():   # anti-aliased strays: nearest palette colour
        bad = idx < 0
        dd = ((a[bad][:, None, :] - PAL[None].astype(np.int32)) ** 2).sum(-1)
        idx[bad] = dd.argmin(1)
    blk = idx.reshape(H, 2, W, 2).transpose(0, 2, 1, 3).reshape(H, W, 4)
    pri = np.array([0.5, 0.0, 0.4, 0.1, 0.3, 0.2])   # K, W, R, Y, B, G
    cnt = np.stack([(blk == i).sum(-1) + pri[i] for i in range(6)], -1)
    out = PAL[cnt.argmax(-1)].astype(np.uint8)
    return Image.fromarray(np.repeat(np.repeat(out, 2, 0), 2, 1))

out = mode_down(img)
# inscription: decide each panel pixel from the text's 2x coverage, so strokes stay whole
tm = np.asarray(TXT, np.float32).reshape(H, 2, W, 2).mean((1, 3)) > 90
out = paint(out, up(tm), WH)
finish(out)
