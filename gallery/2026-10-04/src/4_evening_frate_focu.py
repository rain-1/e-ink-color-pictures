# Slot 4, evening: "Frate Focu".
# "Laudato si', mi' Signore, per frate Focu, per lo quale ennallumini la nocte:
#  ed ello è bello et iocundo et robustoso et forte."
# A bonfire at dusk outside a rough stone hermitage on Monte Subasio, friars gathered round.
# The fire is a Doom-style cellular heat propagation (with wind and a tapering cone)
# run at 1x; heat is banded white -> yellow -> red -> (background) with Bayer screens.
# Sparks are advected through a curl-noise field and drawn as short trails.
import os, sys, math
sys.path.insert(0, os.path.dirname(__file__))
from common import *
from PIL import ImageFilter

rng = np.random.default_rng(1226)
T1 = threshold_1x()                       # 600x400 Bayer thresholds
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)

# canvas as 1x colour field (RGB, uint8) -- everything is composed at 1x in palette colours,
# with text and a few curved outlines composited at 2x at the end.
C = np.zeros((H, W, 3), np.uint8)

def put(mask, col):
    C[mask] = col

def scr(tone):
    return tone > T1

def ramp(t, cols, mask=None):
    """Ordered-dither a 0..1 value along a list of colours (None = leave as is)."""
    n = len(cols) - 1
    v = np.clip(t, 0, 0.9999) * n
    i = np.floor(v).astype(int); f = v - i
    idx = i + (f > T1)
    for k, c in enumerate(cols):
        m = idx == k
        if mask is not None:
            m &= mask
        if c is not None:
            C[m] = c

def poly_mask(pts, scale=1):
    m = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m).polygon([(float(x), float(y)) for x, y in pts], fill=255)
    return np.asarray(m) > 127

def draw_mask(fn):
    m = Image.new("L", (W, H), 0)
    fn(ImageDraw.Draw(m))
    return np.asarray(m) > 127

def shift(m, dx, dy):
    """Shift boolean mask by integer (dx, dy), pad False."""
    out = np.zeros_like(m)
    h, w = m.shape
    xs0, xs1 = max(0, dx), min(w, w + dx)
    ys0, ys1 = max(0, dy), min(h, h + dy)
    out[ys0:ys1, xs0:xs1] = m[ys0 - dy:ys1 - dy, xs0 - dx:xs1 - dx]
    return out

FX, FY = 200, 440                         # light centre of the fire
def light(x, y, r0=95.0):
    d2 = (x - FX) ** 2 + ((y - FY) * 1.15) ** 2
    return 1.0 / (1.0 + d2 / (r0 * r0))

L = light(xx, yy)

# ---------------------------------------------------------------- sky
GROUND = 462
sky_t = np.clip((yy - 70) / 300, 0, 1) ** 0.9            # 0 = blue, 1 = black
sky_t += (noise(H, W, 60, seed=3) - 0.5) * 0.12
C[:] = B
ramp(sky_t, [B, B, K])
# a faint warm glow of the fire on the lower sky / smoke
glow = np.clip(light(xx, yy, 120) - 0.18, 0, 1) * 0.55
glow *= (yy < GROUND)
ramp(glow, [None, R], mask=glow > 0.02)

# smoke plume drifting to the right, darkening the blue
sm_n = noise(H, W, 26, seed=11)
cx = FX + (240 - yy) * 0.35 + np.sin(yy / 40) * 12
wid = 18 + (260 - yy).clip(0) * 0.32
plume = np.exp(-((xx - cx) / wid) ** 2) * np.clip((260 - yy) / 60, 0, 1) * np.clip((yy + 40) / 160, 0, 1)
plume = plume * (0.45 + 0.9 * sm_n)
ramp(np.clip(plume * 0.8, 0, 1), [None, K], mask=(plume > 0.12) & (yy < 300))

# stars
def star(x, y, big=False):
    C[y:y + 2, x:x + 2] = WH
    if big:
        C[y - 4:y + 6, x:x + 2] = WH
        C[y:y + 2, x - 4:x + 6] = WH
        C[y - 1:y + 3, x - 1:x + 3] = WH
        C[y - 2:y + 4, x - 2] = Y; C[y - 2:y + 4, x + 3] = Y
star(62, 46, big=True)                          # the evening star
for (sx, sy) in [(318, 28), (176, 18), (370, 92), (120, 120), (24, 150), (262, 66)]:
    star(sx, sy)

# ---------------------------------------------------------------- far hillside (Subasio)
hill_y = 330 + 25 * np.sin(np.arange(W) / 70.0 + 1.0) + 10 * (noise(1, W, 30, seed=5)[0] - 0.5) - np.arange(W) * 0.12
hill = yy > hill_y[None, :]
hill &= yy < GROUND
put(hill, K)
# distant cypresses / oak clumps on the ridge, faint blue tops
for i in range(14):
    x = int(rng.uniform(0, 240)); hy = int(hill_y[x])
    hgt = int(rng.uniform(8, 22)); w = int(rng.uniform(3, 6))
    m = draw_mask(lambda d: d.ellipse([x - w, hy - hgt, x + w, hy + 4], fill=255))
    put(m, K)
    rim = m & ~shift(m, 0, 2) & (yy < hy)
    put(rim, B)
# blue rim along the ridge line
ridge = hill & ~shift(hill, 0, 2)
put(ridge & scr(np.full((H, W), 0.6)), B)
# firelight washing the near slope behind the circle (so the friars' heads silhouette against it)
hl = np.clip(light(xx, yy, 120) * 1.1 - 0.12, 0, 1) * (0.6 + 0.6 * noise(H, W, 10, seed=7, octaves=2))
ramp(np.clip(hl * 0.85, 0, 0.6), [K, R], mask=hill & (yy > hill_y[None, :] + 4))

# ---------------------------------------------------------------- olive trees
def olive(tx, ty, size, seed, lean=0.0):
    r = np.random.default_rng(seed)
    trunk = np.zeros((H, W), bool)
    # gnarled trunk: several twisting strands
    tops = []
    for s in range(4):
        pts_l, pts_r = [], []
        x = tx + r.uniform(-6, 6) * size; w0 = r.uniform(5, 8) * size
        steps = 14
        for k in range(steps + 1):
            t = k / steps
            y = ty - t * 110 * size
            x += r.uniform(-3, 3) * size + lean * size + (s - 1.5) * 1.2 * size * t
            w = w0 * (1 - 0.6 * t)
            pts_l.append((x - w, y)); pts_r.append((x + w, y))
        tops.append((x, ty - 110 * size))
        trunk |= poly_mask(pts_l + pts_r[::-1])
    # branches
    br = np.zeros((H, W), bool)
    tips = []
    for (bx, by) in tops:
        for j in range(3):
            ang = r.uniform(-2.6, -0.5)
            ln = r.uniform(40, 80) * size
            ex, ey = bx + math.cos(ang) * ln, by + math.sin(ang) * ln * 0.7
            mx, my = (bx + ex) / 2 + r.uniform(-10, 10), (by + ey) / 2 + r.uniform(-10, 10)
            wdt = max(2, int(4 * size))
            br |= draw_mask(lambda d: d.line([(bx, by), (mx, my), (ex, ey)], fill=255, width=wdt, joint="curve"))
            tips.append((ex, ey))
    wood = trunk | br
    put(wood, K)
    # trunk bark: fire-lit fissures (red/yellow) on the fire-facing side
    fis = noise(H, W, 5, seed=seed + 1, octaves=2)
    side = np.sign(FX - tx)
    lit = wood & ~shift(wood, int(side * 3), 0)
    lam = L * 2.2
    put(lit & (lam > 0.35), R)
    put(lit & (lam > 0.75) & ~shift(wood, int(side * 1), 0), Y)
    crack = trunk & (fis > 0.62) & (lam > 0.3) & scr(np.clip(lam, 0, 1))
    put(crack, R)
    # leaves: hundreds of narrow ellipses in clusters around the branch tips
    leafimg = Image.new("L", (W, H), 0)
    ld = ImageDraw.Draw(leafimg)
    leaves = []
    for (ex, ey) in tips + tops:
        R0 = 30 * size * r.uniform(0.8, 1.2)
        for c in range(int(110 * size)):
            a = r.uniform(0, 2 * math.pi); rad = R0 * r.uniform(0, 1) ** 0.7
            ox, oy = math.cos(a) * rad / R0, math.sin(a) * rad / R0
            lx = ex + ox * R0 * 1.3; ly = ey + oy * R0 * 0.7
            leaves.append((lx, ly, r.uniform(-1.5, 1.5), ox, oy, ex))
    cols = {"K": [], "G": [], "B": [], "R": [], "Y": []}
    for (lx, ly, ang, ox, oy, ex) in leaves:
        ln = r.uniform(2.5, 4.5)
        dx, dy = math.cos(ang) * ln, math.sin(ang) * ln
        li = light(lx, ly) * 2.6
        toward = ox * np.sign(FX - ex)
        u = r.random()
        if toward > 0.1 and li > 0.45 + u * 0.35 and oy > -0.4:
            c = "Y" if li > 0.95 + u * 0.3 and toward > 0.5 else "R"
        elif oy < -0.35 and u < 0.6:
            c = "B" if oy < -0.8 and u < 0.3 else "G"
        else:
            c = "K"
        cols[c].append((lx, ly, dx, dy))
    leafm = np.zeros((H, W), bool)
    for c in ["K", "G", "B", "R", "Y"]:
        mm = draw_mask(lambda d: [d.line([(lx - dx, ly - dy), (lx + dx, ly + dy)], fill=255, width=2)
                                  for (lx, ly, dx, dy) in cols[c]])
        put(mm, {"K": K, "G": G, "B": B, "R": R, "Y": Y}[c])
        leafm |= mm
    return wood | leafm

olive(26, GROUND + 2, 1.15, 21, lean=0.6)

# ---------------------------------------------------------------- hermitage
WX0 = 252
roof_y = lambda x: 238 + (x - WX0) * 0.06
wall = (xx >= WX0) & (yy >= roof_y(xx)) & (yy < GROUND + 6)
# rough left edge (quoins)
put(wall, K)
blocks = []
y = 246
row = 0
while y < GROUND + 6:
    bh = int(rng.integers(13, 20))
    x = WX0 - (6 if row % 2 == 0 else 0)
    while x < W:
        bw = int(rng.integers(18, 38)) if x > WX0 + 4 else int(rng.integers(22, 30))
        blocks.append((x, y, bw, bh))
        x += bw
    y += bh
    row += 1

door = draw_mask(lambda d: (d.rectangle([316, 372, 360, GROUND + 6], fill=255),
                            d.ellipse([316, 350, 360, 394], fill=255)))
window = draw_mask(lambda d: (d.rectangle([276, 300, 292, 330], fill=255),
                              d.ellipse([276, 292, 292, 308], fill=255)))
texture = noise(H, W, 4, seed=77, octaves=3)
for (bx, by, bw, bh) in blocks:
    j = lambda: rng.uniform(-1.6, 1.6)
    pts = [(bx + 1 + j(), by + 1 + j()), (bx + bw - 1 + j(), by + 1 + j()),
           (bx + bw - 1 + j(), by + bh - 1 + j()), (bx + 1 + j(), by + bh - 1 + j())]
    m = poly_mask(pts) & wall
    if not m.any():
        continue
    cxb, cyb = bx + bw / 2, by + bh / 2
    lb = light(cxb, cyb) * rng.uniform(0.75, 1.25)
    # per-pixel: brighter toward the fire-facing (left/lower) edge, texture pits
    local = lb * 1.55 * (1.0 + 0.45 * (cxb - xx) / bw) + (texture - 0.5) * 0.18
    t = np.clip(local, 0, 1)
    ramp(t, [K, K, R, R, Y], mask=m)  # far stones: cool blue sheen; near: red -> yellow
    # lit top-left edge highlight
    edge = m & ~shift(m, 2, 0)
    put(edge & (lb > 0.42), Y)
    put(edge & (lb > 0.12) & (lb <= 0.42), R)
    topb = m & ~shift(m, 0, 2)
    put(topb & (lb <= 0.2), B)                       # far stones: cool dusk on their top faces
    # dark pits
    put(m & (texture > 0.8), K)

# door: dressed arch stones (voussoirs) and black interior
arch = draw_mask(lambda d: d.ellipse([306, 340, 370, 404], fill=255)) | draw_mask(lambda d: d.rectangle([306, 372, 370, GROUND + 6], fill=255))
arch &= ~door
put(arch, K)
for k in range(9):
    a0 = math.pi + k * math.pi / 9
    a1 = a0 + math.pi / 9 - 0.06
    cxv, cyv = 338, 372
    pts = [(cxv + 22 * math.cos(a0), cyv + 22 * math.sin(a0)), (cxv + 32 * math.cos(a0), cyv + 32 * math.sin(a0)),
           (cxv + 32 * math.cos(a1), cyv + 32 * math.sin(a1)), (cxv + 22 * math.cos(a1), cyv + 22 * math.sin(a1))]
    m = poly_mask(pts)
    lv = light(cxv + 27 * math.cos(a0), cyv + 27 * math.sin(a0)) * 2.4
    ramp(np.full((H, W), np.clip(lv, 0, 1)), [K, R, R, Y], mask=m)
for k in range(5):   # jamb stones
    for sx in (306, 362):
        m = draw_mask(lambda d: d.rectangle([sx + 1, 374 + k * 18, sx + 7, 374 + k * 18 + 16], fill=255))
        lv = light(sx, 380 + k * 18) * 2.4
        ramp(np.full((H, W), np.clip(lv, 0, 1)), [K, R, R, Y], mask=m)
put(door, K)
# door planks faintly lit, iron studs
for px in range(322, 358, 8):
    put(draw_mask(lambda d: d.line([(px, 372), (px, GROUND + 4)], fill=255, width=2)) & door & scr(np.full((H, W), 0.5)), R)
# the small window glows: a lamp inside
put(window, K)
put(window & scr(np.clip(1.0 - np.hypot(xx - 284, yy - 318) / 14, 0, 1) * 1.2), Y)
put(window & ~shift(window, 0, -2) , R)

# roof: overhanging terracotta tiles in rows, dusk on top, firelight under the eave
roof = poly_mask([(WX0 - 10, 240), (W, 232), (W, 246), (WX0 - 10, 252)])
put(roof, K)
for tx in range(WX0 - 10, W, 6):
    m = draw_mask(lambda d: d.rounded_rectangle([tx, roof_y(tx) - 6, tx + 4, roof_y(tx) + 10], radius=2, fill=255))
    put(m & roof, R)
    put(m & roof & (yy < roof_y(tx) - 2), B)
put(roof & ~shift(roof, 0, -2) & (xx < 330), Y)   # eave underside catching fire
# bell-cote with bell
bc = poly_mask([(356, 236), (356, 196), (373, 180), (390, 196), (390, 236)])
put(bc, K)
bo = draw_mask(lambda d: (d.rectangle([363, 206, 383, 232], fill=255), d.ellipse([363, 198, 383, 216], fill=255)))
put(bo, B)
put(draw_mask(lambda d: d.chord([366, 212, 380, 232], 180, 360, fill=255)), K)
put(draw_mask(lambda d: d.rectangle([367, 222, 379, 227], fill=255)), K)
put(bc & ~bo & ~shift(bc, 2, 0), R)
put(draw_mask(lambda d: (d.line([(373, 166), (373, 182)], fill=255, width=2), d.line([(368, 171), (378, 171)], fill=255, width=2))), K)

# ---------------------------------------------------------------- ground
ground = yy >= GROUND
gn = noise(H, W, 7, seed=91, octaves=3)
put(ground, K)
gl = np.clip(light(xx, yy, 130) * 1.3 - 0.15, 0, 1) * (0.45 + 0.9 * gn)
ramp(np.clip(gl, 0, 1) * 0.72, [K, K, R, R, Y], mask=ground)
# pebbles
for i in range(140):
    px = rng.uniform(0, W); py = rng.uniform(GROUND + 4, 560)
    r0 = rng.uniform(1.5, 3)
    if abs(px - FX) < 80 and py < 520: continue
    m = draw_mask(lambda d: d.ellipse([px - r0 * 1.4, py - r0, px + r0 * 1.4, py + r0], fill=255))
    lv = light(px, py) * 2.2
    if lv < 0.25:
        continue
    put(m & (yy > py), K)                                   # pebble's own shadow side
    top = m & (yy <= py)
    put(top, R if lv < 1.0 else Y)
    put(m & ~shift(m, 0, -2) & (yy > py), K)
# grass tufts at the edges (a little green under dusk, red near the fire)
for i in range(70):
    gx = rng.uniform(0, W); gy = rng.uniform(GROUND + 2, 556)
    if abs(gx - FX) < 70: continue
    lv = light(gx, gy) * 2.2
    col = Y if lv > 1.0 else R if lv > 0.45 else G
    for b in range(4):
        a = -math.pi / 2 + rng.uniform(-0.6, 0.6)
        ln = rng.uniform(5, 10)
        m = draw_mask(lambda d: d.line([(gx + b * 2, gy), (gx + b * 2 + math.cos(a) * ln, gy + math.sin(a) * ln)], fill=255, width=2))
        put(m, col)

# ---------------------------------------------------------------- fire (Doom-style heat propagation)
# Each frame every cell hands its heat to the cell above (shifted sideways by sway + jitter)
# minus a decay. The decay is read from a noise field that scrolls upward exactly as fast as
# the heat does, so a parcel keeps its "luck" as it rises: lucky columns become tongues,
# unlucky ones die early -> licking flames rather than a fuzzy cone.
FW, FH = 220, 330
FX0, FBOT = FX - FW // 2, 482                # grid left edge and bottom row on the canvas
NF = 640
heat = np.zeros((FH, FW), np.float32)
gx = np.arange(FW) - FW / 2
src_profile = np.clip(1.0 - (np.abs(gx) / 64) ** 2.0, 0, 1)
decay_x = 0.0036 * (1.0 + 4.0 * (np.abs(gx) / 80) ** 2)       # tapering cone
ND = np.asarray(Image.fromarray((noise((FH + NF) // 3 + 2, FW, 6, seed=41, octaves=3) * 255).astype(np.uint8))
                .resize((FW, ((FH + NF) // 3 + 2) * 3), Image.BICUBIC), np.float32) / 255   # tall features
NS = noise(FH + NF + 4, FW, 34, seed=42, octaves=2)
fr = np.random.default_rng(800)
ys = np.arange(1, FH)[:, None].repeat(FW, 1)
xs = np.arange(FW)[None, :].repeat(FH - 1, 0)
for f in range(NF):
    heat[-1] = src_profile * (0.82 + 0.18 * ND[f + FH])
    nd = ND[f + 1:f + FH]; ns = NS[f + 1:f + FH]
    sway = (ns - 0.5) * 1.6 + 0.10                                # gentle breeze to the right
    r = np.floor(sway + fr.random((FH - 1, FW))).astype(int)
    dstx = np.clip(xs + r, 0, FW - 1)
    dec = decay_x[None, :] * (0.12 + 3.2 * nd ** 3) * (0.5 + fr.random((FH - 1, FW)))
    new = heat.copy()
    new[ys - 1, dstx] = np.clip(heat[ys, xs] - dec, 0, 1)
    heat = new
# soften by a hair so tongues read as shapes, not static
hi = Image.fromarray((heat * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.1))
heat = np.asarray(hi, np.float32) / 255
HF = np.zeros((H, W), np.float32)
HF[FBOT - FH:FBOT, FX0:FX0 + FW] = heat
HF = np.clip((HF - 0.16) / 0.74, 0, 1)

# glow halo around the flames (red screen over whatever is behind)
halo = np.asarray(Image.fromarray((HF * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(6)), np.float32) / 255
ramp(np.clip(halo * 1.1, 0, 1) * 0.6, [None, R], mask=(halo > 0.06) & (HF <= 0.02) & (yy < GROUND + 30))

# sparks (drawn before the flames; most rise above them anyway)
nx = noise(H, W, 45, seed=5, octaves=2); ny = noise(H, W, 45, seed=6, octaves=2)
pot = noise(H, W, 55, seed=8, octaves=2)
gpy, gpx = np.gradient(pot)
curl_x, curl_y = gpy * 170, -gpx * 170
sparks = Image.new("RGB", (W, H), (0, 0, 0))
spark_head = []
for i in range(420):
    x = FX + rng.normal(0, 22); y = rng.uniform(230, 400)
    vy = -rng.uniform(1.4, 3.0); steps = int(rng.uniform(18, 110))
    path = [(x, y)]
    for s in range(steps):
        ix = int(np.clip(x, 0, W - 1)); iy = int(np.clip(y, 0, H - 1))
        x += curl_x[iy, ix] + 0.45 + rng.normal(0, 0.25)
        y += vy + curl_y[iy, ix] * 0.6
        path.append((x, y))
        if y < 8: break
    tail = path[-int(rng.uniform(2, 5)):]
    age = len(path) / 110
    spark_head.append((path[-1], tail, age))
SP = np.zeros((H, W), np.uint8)   # 0 none, 1 red, 2 yellow, 3 white
spimg = Image.new("L", (W, H), 0); sd = ImageDraw.Draw(spimg)
for (hx, hy), tail, age in spark_head:
    if hy < 4 or hx < 2 or hx > W - 3: continue
    lev = 1 if age > 0.6 else 2 if age > 0.25 else 3
    if len(tail) > 1 and rng.random() < 0.45:
        sd.line(tail, fill=1 if lev < 3 else 2, width=2)
    sd.rectangle([hx - 1, hy - 1, hx, hy], fill=lev)
SP = np.asarray(spimg)
put(SP == 1, R); put(SP == 2, Y); put(SP == 3, WH)

# flames: background -> red -> yellow -> white, Bayer-screened bands
fm = HF > 0.02
t = HF ** 0.85
ramp(t, [None, R, R, Y, Y, WH, WH], mask=fm)
# a thin dark-red 'edge' gives tongues a contour against the lit wall
edge = fm & ~shift(fm, 0, 1) & (HF < 0.3)

# ---------------------------------------------------------------- logs (dark in the flames, ember cracks)
logs = [((150, 486), (232, 430), 9), ((252, 488), (168, 428), 9), ((140, 474), (262, 476), 8),
        ((196, 492), (205, 418), 7), ((166, 492), (250, 454), 7)]
for (a, b, w) in logs:
    m = draw_mask(lambda d: d.line([a, b], fill=255, width=2 * w))
    put(m, K)
    # bark: stripes along the log
    dx, dy = b[0] - a[0], b[1] - a[1]; ln = math.hypot(dx, dy); ux, uy = dx / ln, dy / ln
    vx, vy = -uy, ux
    along = (xx - a[0]) * ux + (yy - a[1]) * uy
    across = (xx - a[0]) * vx + (yy - a[1]) * vy
    bark = np.sin(across * 1.3 + np.sin(along * 0.25) * 1.5) * 0.5 + 0.5
    hot = np.clip(HF * 1.4 + L * 0.4, 0, 1)
    crack = m & (bark > 0.82) & (np.abs(across) < w - 2)
    put(crack & (hot > 0.55), Y); put(crack & (hot <= 0.55) & (hot > 0.25), R)
    # glowing checker-cracks (alligatored charcoal)
    chk = (np.sin(along * 0.9) > 0.85) & m & (np.abs(across) < w - 2) & (hot > 0.5)
    put(chk, R)
    # lower edge rim catching the coals
    put(m & ~shift(m, 0, -2) & (hot > 0.3), Y)
    # log end with rings
    ex, ey = a
    for rr, col in [(w - 1, K), (w - 3, R), (w - 5, K)]:
        if rr > 0:
            put(draw_mask(lambda d: d.ellipse([ex - rr, ey - rr, ex + rr, ey + rr], fill=255)), col)
# coal bed
for i in range(90):
    cx_ = rng.normal(FX, 30); cy_ = rng.uniform(476, 494)
    r0 = rng.uniform(2, 4)
    m = draw_mask(lambda d: d.ellipse([cx_ - r0, cy_ - r0 * 0.7, cx_ + r0, cy_ + r0 * 0.7], fill=255))
    put(m, [K, R, R, Y][rng.integers(0, 4)])
# small licks of flame in front of the logs
fl2 = (HF > 0.5) & (yy > 440) & (yy < 478) & (noise(H, W, 6, seed=401) > 0.55)
put(fl2, Y)

# ---------------------------------------------------------------- hearth stone ring
for k in range(16):
    a = k / 16 * 2 * math.pi + 0.1
    sx = FX + math.cos(a) * 74; sy = 486 + math.sin(a) * 13
    if math.sin(a) < -0.2:
        continue                                  # back stones hidden by fire/logs
    rw, rh = rng.uniform(10, 14), rng.uniform(7, 10)
    pts = [(sx + math.cos(t) * rw * rng.uniform(0.85, 1.1), sy + math.sin(t) * rh * rng.uniform(0.85, 1.1))
           for t in np.linspace(0, 2 * math.pi, 9)[:-1]]
    m = poly_mask(pts)
    ob = draw_mask(lambda d: d.polygon([(sx + (x - sx) * 1.15, sy + (y - sy) * 1.2) for x, y in pts], fill=255))
    put(ob, K)
    lx_ = sx + (FX - sx) / 74 * rw * 0.5
    tone = np.clip(1.25 - np.hypot((xx - lx_) * 0.8, yy - (sy - rh * 0.7)) / (rw * 1.0), 0, 1)
    ramp(tone, [K, K, R, R, Y], mask=m)
    put(m & ~shift(m, 0, 2) & (tone > 0.2), Y)
    # a few chisel/lichen pits
    put(m & (noise(H, W, 3, seed=k + 500, octaves=1) > 0.82), K)

# ---------------------------------------------------------------- friars
# Built from parts in a local frame (feet at 0,0, facing +x = toward the fire), then mirrored.
def friar_parts(kind):
    parts = []   # list of (kind, data) drawn as union
    if kind == "stand":
        parts += [("poly", [(-27, 0), (-22, -3), (-12, 0), (0, -3), (12, 0), (24, -2), (20, -40), (17, -78),
                            (16, -104), (-6, -116), (-20, -108), (-24, -70), (-26, -30)]),
                  ("ell", (-4, -108, 17, 13)),                       # shoulders, slight stoop
                  ("ell", (6, -132, 10, 12)),                        # head in the hood
                  ("poly", [(-2, -146), (6, -144), (-4, -128), (-20, -112), (-14, -108)]),   # pointed cowl down the back
                  ("poly", [(14, -136), (18, -128), (16, -122), (12, -118)]),   # brow / nose profile
                  ("line", ((2, -102), (30, -86), 12)),              # sleeve held out
                  ("ell", (32, -85, 6, 8)),                          # wide sleeve mouth
                  ("poly", [(14, 0), (24, 0), (24, -3), (16, -4)])]  # sandal toe
        head = (13, -128); hand = (39, -84); cord = ((16, -78), 52); belt = ((-20, -80), (17, -78))
    else:
        parts += [("poly", [(-26, 0), (40, 0), (42, -14), (38, -32), (14, -38), (12, -60), (-6, -70),
                            (-22, -60), (-28, -30)]),
                  ("ell", (5, -78, 10, 12)),
                  ("poly", [(-2, -92), (6, -90), (-4, -74), (-22, -60), (-14, -58)]),
                  ("poly", [(12, -82), (17, -74), (14, -68), (10, -66)]),
                  ("line", ((0, -56), (30, -44), 11)),
                  ("ell", (32, -44, 5, 7))]
        head = (12, -74); hand = (38, -44); cord = ((12, -38), 26); belt = ((-24, -40), (12, -38))
    return parts, head, hand, cord, belt

def friar_mask(parts, fx, fy, dirx, sc):
    T = lambda x, y: (fx + dirx * x * sc, fy + y * sc)
    def fn(d):
        for k, v in parts:
            if k == "poly":
                d.polygon([T(*p) for p in v], fill=255)
            elif k == "ell":
                cx_, cy_, rx, ry = v; X, Yc = T(cx_, cy_)
                d.ellipse([X - rx * sc, Yc - ry * sc, X + rx * sc, Yc + ry * sc], fill=255)
            elif k == "line":
                p0, p1, w = v; d.line([T(*p0), T(*p1)], fill=255, width=int(w * sc))
    return draw_mask(fn), T

figures = [  # kind, x, y_feet, facing right?, scale
    ("stand", 50, 552, True, 1.12),
    ("sit", 118, 548, True, 1.05),
    ("sit", 284, 548, False, 1.02),
    ("stand", 352, 554, False, 1.16),
]
# seat log (left) and stone (right) first
for (x0, x1, y0) in [(84, 150, 540), (258, 318, 540)]:
    m = draw_mask(lambda d: d.rounded_rectangle([x0, y0, x1, y0 + 12], radius=6, fill=255))
    put(m, K); put(m & ~shift(m, 0, 2), R)
for kind, fx, fy, right, sc in figures:
    parts, head, hand, cord, belt = friar_parts(kind)
    dirx = 1 if right else -1
    m, T = friar_mask(parts, fx, fy, dirx, sc)
    # long shadow cast away from the fire across the ground
    sd_ = -dirx
    shadow = poly_mask([(fx - 24 * sc, fy), (fx + 24 * sc, fy), (fx + sd_ * 90 + 16, fy + 12), (fx + sd_ * 90 - 16, fy + 12)])
    put(shadow & ground & ~m, K)
    put(m, K)
    # depth inside the silhouette measured from the fire-facing edge
    depth = np.zeros((H, W), np.float32)
    run = m.copy()
    for n in range(1, 15):
        run &= shift(m, -dirx * n, 0)
        depth += run
    # folds: the light wraps further on ridges of cloth
    folds = 0.22 * np.sin((xx - fx) * 0.9 + np.sin(yy * 0.05) * 2) * (yy > fy - 100 * sc)
    lv = np.clip(light(xx, yy) * 2.6, 0, 1.2)
    tone = np.clip(lv * np.clip(1.0 - depth / 13.0, 0, 1) ** 1.4 + folds * (depth < 12), 0, 1)
    ramp(tone, [K, K, R, R, Y], mask=m & (depth > 1))
    put(m & (depth <= 1) & (lv > 0.35), Y)
    put(m & (depth <= 1) & (lv <= 0.35), R)
    # cool dusk on the shoulders / hood top (the sky behind)
    top = m & ~shift(m, 0, 2) & (depth >= 7) & (yy < fy - 60 * sc)
    put(top, B)
    # hood opening: a dark line separating face from cowl, then the lit profile
    hx, hy = T(*head)
    put(draw_mask(lambda d: d.arc([hx - 9 * sc, hy - 10 * sc, hx + 5 * sc, hy + 12 * sc],
                                  -80 if right else 100, 80 if right else 260, fill=255, width=2)) & m, K)
    # cord belt + hanging cord with three knots
    (bx0, by0), (bx1, by1) = T(*belt[0]), T(*belt[1])
    put(draw_mask(lambda d: d.line([(bx0, by0), (bx1, by1)], fill=255, width=2)) & m & (depth < 9), R)
    (cx0, cy0), clen = T(*cord[0]), cord[1] * sc
    put(draw_mask(lambda d: d.line([(cx0, cy0), (cx0 + dirx * 2, cy0 + clen)], fill=255, width=2)), Y)
    for k in range(3):
        ky = cy0 + clen * (0.3 + 0.28 * k); kx = cx0 + dirx * 2 * (0.3 + 0.28 * k)
        put(draw_mask(lambda d: d.ellipse([kx - 2, ky - 2, kx + 2, ky + 2], fill=255)), Y)
    # hands held out to the warmth
    hx2, hy2 = T(*hand)
    hm = draw_mask(lambda d: d.ellipse([hx2 - 4, hy2 - 3, hx2 + 4, hy2 + 3], fill=255))
    put(hm, Y); put(hm & ~shift(hm, -dirx * 3, 0), R)

# ---------------------------------------------------------------- caption band
cap_top = 562
put(yy >= cap_top, K)
img = Image.fromarray(np.repeat(np.repeat(C, 2, 0), 2, 1))
d = ImageDraw.Draw(img)
d.line([(40, cap_top * 2 + 4), (W2 - 40, cap_top * 2 + 4)], fill=R, width=2)
f1 = font("serif-i", 26)
f2 = font("serif-b", 26)
line1 = "Laudato si', mi' Signore, per frate Focu,"
line2 = "per lo quale ennallumini la nocte."
for txt, fnt, y, col in [(line1, f1, cap_top * 2 + 14, Y), (line2, f1, cap_top * 2 + 44, WH)]:
    tw = d.textlength(txt, font=fnt)
    d.text(((W2 - tw) / 2, y), txt, font=fnt, fill=col)
finish(img)
