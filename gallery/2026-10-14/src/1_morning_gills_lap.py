"""Gills Lap, first light — Ashdown Forest, 14 October.

Painterly landscape built in continuous colour at 2x, then Floyd–Steinberg dithered
onto the six inks by render.py (--dither fs). Detail is drawn: every pine is tiered,
every bracken frond has pinnae, the birch has lenticels.
"""
import math, os, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

W, H = 800, 1200
R = random.Random(1014)
rng = np.random.default_rng(1014)


def ramp(stops, n):
    xs = [s[0] for s in stops]
    return np.stack([np.interp(np.linspace(0, 1, n), xs, [s[1][c] for s in stops]) for c in range(3)], -1)


def noise1d(n, octaves=5, seed=0):
    r = np.random.default_rng(seed)
    out = np.zeros(n)
    for o in range(octaves):
        k = 2 ** (o + 2)
        pts = r.uniform(-1, 1, k + 1)
        out += np.interp(np.linspace(0, k, n), np.arange(k + 1), pts) / (1.7 ** o)
    return out


# ---------------------------------------------------------------- sky
HZ = 610
sky = ramp([(0, (30, 60, 160)), (0.30, (90, 130, 210)), (0.42, (190, 200, 225)),
            (0.49, (255, 225, 140)), (0.52, (255, 240, 200)), (1, (255, 240, 200))], H)
img = np.repeat(sky[:, None, :], W, 1).astype(np.float32)
SX, SY = 590, 585
yy, xx = np.mgrid[0:H, 0:W]
d = np.hypot(xx - SX, (yy - SY) * 1.4)
glow = np.exp(-d / 170.0)[..., None]
img = img * (1 - 0.6 * glow) + np.array([255, 235, 120]) * 0.6 * glow
# streaky dawn clouds: thin horizontal lenses lit from below
cl = Image.new("L", (W, H), 0)
cd = ImageDraw.Draw(cl)
for i in range(26):
    cy = R.uniform(140, 520)
    cx = R.uniform(-100, W + 100)
    ln = R.uniform(120, 420)
    th = R.uniform(5, 16) * (0.6 + cy / 600)
    cd.ellipse([cx - ln / 2, cy - th / 2, cx + ln / 2, cy + th / 2], fill=int(R.uniform(140, 255)))
cl = np.asarray(cl.filter(ImageFilter.GaussianBlur(3)), np.float32)[..., None] / 255
under = np.clip((yy - 0) / H, 0, 1)[..., None]
cloud_col = np.array([235, 90, 60]) * (0.4 + under) + np.array([60, 40, 120]) * (1 - under)
cloud_col = np.clip(cloud_col, 0, 255)
img = img * (1 - cl * 0.85) + cloud_col * cl * 0.85
# sun disc
img[d < 34] = (255, 255, 235)

# ---------------------------------------------------------------- far ridges (the Weald)
def ridge(base, amp, seed, col, mist_to, mist_amt):
    global img
    prof = base + amp * noise1d(W, 6, seed)
    mask = yy >= prof[None, :]
    depth = np.clip((yy - prof[None, :]) / 120, 0, 1)[..., None]
    c = np.array(col, np.float32) * (1 - mist_amt * (1 - depth)) + np.array(mist_to) * mist_amt * (1 - depth)
    img = np.where(mask[..., None], c, img)
    return prof

ridge(600, 10, 3, (170, 170, 215), (250, 230, 200), 0.5)
ridge(622, 14, 5, (120, 120, 190), (240, 220, 200), 0.6)
ridge(648, 12, 9, (80, 95, 160), (230, 210, 200), 0.6)
# mist band
mist = np.exp(-((yy - 660) / 22.0) ** 2)[..., None] * (0.7 + 0.3 * np.sin(xx / 37.0)[..., None])
img = img * (1 - 0.7 * mist) + np.array([255, 245, 230]) * 0.7 * mist

# ---------------------------------------------------------------- Gills Lap hill
hill = 700 - 90 * np.exp(-((np.arange(W) - 300) / 260.0) ** 2) + 6 * noise1d(W, 6, 11)
heath = ramp([(0, (110, 60, 80)), (0.45, (80, 35, 40)), (1, (45, 25, 20))], H)
mask = yy >= hill[None, :]
grain = rng.normal(0, 4, (H, W, 1))
hcol = heath[:, None, :] + grain
img = np.where(mask[..., None], hcol, img)

im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
dr = ImageDraw.Draw(im)

# heather and bracken texture on the hill: thousands of small strokes, warmer toward the sun
for i in range(6000):
    x = R.uniform(0, W)
    top = hill[int(min(W - 1, max(0, x)))]
    y = R.uniform(top + 3, H)
    if y > H:
        continue
    t = (y - top) / (H - top + 1)
    sun = max(0, 1 - abs(x - SX) / 500)
    pick = R.random()
    if pick < 0.45:  # bracken rust
        c = (int(225 + 30 * sun), int(110 + 90 * sun * R.random()), 20)
    elif pick < 0.7:  # heather
        c = (130, 40, 130)
    elif pick < 0.9:  # dark
        c = (25, 15, 15)
    else:  # dry grass
        c = (230, 200, 120)
    ln = 2 + 10 * t
    a = R.uniform(-0.5, 0.5) - math.pi / 2
    dr.line([x, y, x + ln * math.cos(a), y + ln * math.sin(a)], fill=c, width=max(1, int(1 + 2 * t)))

# ---------------------------------------------------------------- the path
pts = []
for i in range(60):
    t = i / 59
    y = H + 20 - t * (H + 20 - (hill[330] + 4))
    x = 470 + 160 * math.sin(t * 2.6 + 0.4) * (1 - t) - 140 * t
    w = 150 * (1 - t) ** 1.6 + 5
    pts.append((x, y, w))
left = [(x - w / 2, y) for x, y, w in pts]
right = [(x + w / 2, y) for x, y, w in reversed(pts)]
dr.polygon(left + right, fill=(225, 195, 140))
# ruts and pebbles
for side in (-0.22, 0.22):
    dr.line([(x + side * w, y) for x, y, w in pts], fill=(160, 110, 70), width=3)
for i in range(500):
    x, y, w = pts[R.randrange(0, 40)]
    px = x + R.uniform(-0.45, 0.45) * w
    s = 1 + w / 60
    dr.ellipse([px - s, y - s * 0.6, px + s, y + s * 0.6], fill=R.choice([(255, 245, 220), (140, 90, 60), (200, 160, 110)]))

# ---------------------------------------------------------------- the pines on the crest
def scots_pine(x, base, h, lean=0.0):
    # orange upper trunk, dark lower trunk, flat tiered crown, sunlit right edges
    top = base - h
    tx = x + lean * h
    dr.line([x, base, tx, top + h * 0.25], fill=(50, 30, 25), width=max(2, int(h / 40)))
    dr.line([x + lean * h * 0.5, base - h * 0.5, tx, top + h * 0.2], fill=(210, 100, 40), width=max(2, int(h / 50)))
    tiers = R.randint(3, 5)
    for k in range(tiers):
        ty = top + k * h * 0.09 + R.uniform(-4, 4)
        bw = h * (0.07 + 0.035 * k) * R.uniform(0.8, 1.3)
        bx = tx + R.uniform(-0.2, 0.2) * bw
        # branch
        dr.line([tx, ty + h * 0.06, bx, ty + h * 0.03], fill=(60, 35, 25), width=2)
        for j in range(9):
            cx = bx + R.uniform(-bw, bw)
            cy = ty + R.uniform(-h * 0.035, h * 0.035)
            rw, rh = R.uniform(bw * 0.25, bw * 0.45), R.uniform(h * 0.025, h * 0.05)
            dr.ellipse([cx - rw, cy - rh, cx + rw, cy + rh], fill=(25, 55, 35))
        # lit edge facing the sun
        for j in range(10):
            cx = bx + R.uniform(0.2, 1.0) * bw
            cy = ty + R.uniform(-h * 0.04, 0)
            rw = R.uniform(3, 6)
            dr.ellipse([cx - rw, cy - 2, cx + rw, cy + 2], fill=(235, 190, 60))

crest = [(120, 0.8), (175, 1.0), (215, 1.15), (250, 1.3), (285, 1.2), (318, 1.35), (350, 1.0), (385, 1.1), (430, 0.85), (470, 0.7)]
for x, s in crest:
    scots_pine(x + R.uniform(-8, 8), hill[x] + 6, 240 * s, R.uniform(-0.06, 0.06))

# long morning shadows from the clump, thrown toward the viewer-left
for x, s in crest:
    by = hill[x] + 8
    dr.polygon([(x - 6, by), (x + 6, by), (x - 160 * s, by + 90 * s), (x - 190 * s, by + 80 * s)], fill=(30, 15, 30))

# ---------------------------------------------------------------- the walker with a blue balloon
fx, fy = pts[28][0] + 4, pts[28][1]
dr.ellipse([fx - 18, fy - 3, fx + 24, fy + 5], fill=(110, 60, 50))  # shadow
dr.line([fx - 5, fy, fx - 2, fy - 30], fill=(20, 20, 30), width=6)
dr.line([fx + 6, fy, fx + 2, fy - 30], fill=(20, 20, 30), width=6)
dr.polygon([(fx - 12, fy - 28), (fx + 12, fy - 28), (fx + 8, fy - 66), (fx - 8, fy - 66)], fill=(230, 40, 40))
dr.ellipse([fx - 9, fy - 86, fx + 9, fy - 66], fill=(240, 200, 160))
dr.line([fx + 10, fy - 58, fx + 30, fy - 150], fill=(20, 20, 20), width=2)
dr.ellipse([fx + 8, fy - 210, fx + 56, fy - 148], fill=(20, 60, 200))
dr.ellipse([fx + 18, fy - 200, fx + 30, fy - 184], fill=(200, 220, 255))

# ---------------------------------------------------------------- silver birch, right edge
bx0 = 700
dr.polygon([(bx0 - 22, H), (bx0 + 24, H), (bx0 + 12, 0), (bx0 - 6, 0)], fill=(245, 240, 230))
for i in range(80):
    y = R.uniform(0, H)
    w = R.uniform(8, 30)
    x = bx0 - 18 + R.uniform(0, 30) * (1 - y / H * 0.2)
    dr.line([x, y, x + w, y + R.uniform(-2, 2)], fill=(20, 20, 20), width=R.choice([2, 3, 4]))
dr.polygon([(bx0 - 22, H), (bx0 - 22, 1000), (bx0 - 10, 1100), (bx0 + 24, 1060), (bx0 + 24, H)], fill=(30, 25, 25))
for (sx, sy, ex, ey) in [(bx0 + 8, 160, 800, 60), (bx0 - 2, 330, 560, 230), (bx0 + 8, 420, 800, 380)]:
    dr.line([sx, sy, ex, ey], fill=(60, 50, 45), width=6)
    for k in range(30):
        t = R.random()
        lx, ly = sx + (ex - sx) * t, sy + (ey - sy) * t
        for j in range(3):
            ox, oy = lx + R.uniform(-30, 30), ly + R.uniform(0, 50)
            dr.line([lx, ly, ox, oy], fill=(60, 50, 45), width=1)
            dr.ellipse([ox - 5, oy - 3, ox + 5, oy + 3], fill=R.choice([(250, 210, 30), (240, 180, 20), (255, 235, 90)]))

# falling leaves
for i in range(45):
    x, y = R.uniform(380, 790), R.uniform(150, 1150)
    a = R.uniform(0, math.pi)
    dr.polygon([(x + 7 * math.cos(a), y + 7 * math.sin(a)), (x + 3 * math.cos(a + 1.6), y + 3 * math.sin(a + 1.6)),
                (x - 7 * math.cos(a), y - 7 * math.sin(a)), (x - 3 * math.cos(a + 1.6), y - 3 * math.sin(a + 1.6))],
               fill=(250, 210, 30))

# ---------------------------------------------------------------- foreground bracken fronds
def frond(x, y, ln, ang, curl, col, dark):
    px, py = x, y
    segs = 22
    for s in range(segs):
        t = s / segs
        a = ang + curl * t
        nx, ny = px + ln / segs * math.cos(a), py + ln / segs * math.sin(a)
        dr.line([px, py, nx, ny], fill=dark, width=3)
        pin = ln * 0.32 * math.sin(math.pi * (0.15 + 0.85 * t)) * (1 - t * 0.5)
        for side in (-1, 1):
            pa = a + side * 1.15
            ex, ey = nx + pin * math.cos(pa), ny + pin * math.sin(pa) + pin * 0.25
            dr.line([nx, ny, ex, ey], fill=col, width=5)
            # leaflets
            for k in range(1, 5):
                u = k / 5
                lx, ly = nx + (ex - nx) * u, ny + (ey - ny) * u
                dr.line([lx, ly, lx + 6 * math.cos(pa + side * 0.9), ly + 6 * math.sin(pa + side * 0.9) + 3], fill=col, width=3)
        px, py = nx, ny

for i in range(14):
    x = R.choice([R.uniform(-40, 280), R.uniform(560, 760)])
    y = R.uniform(1000, 1240)
    col = R.choice([(235, 90, 20), (250, 160, 20), (225, 40, 30), (250, 210, 40)])
    frond(x, y, R.uniform(200, 340), -math.pi / 2 + R.uniform(-0.9, 0.9), R.uniform(0.6, 1.2) * R.choice([-1, 1]), col, (40, 15, 10))

im.save(os.environ.get("OUT_RAW", "raw1.png"))
