"""Night — 'Lune gibbeuse'. Tonight's real sky: an 89% waxing moon with Saturn beside it.
The balloon drifts across the limb, its brazier the only red thing in the picture; Paris
sleeps below with a few windows lit. Mezzotint: black in charge."""
import sys, math, os
sys.path.insert(0, os.path.dirname(__file__))
from common import *

rng = np.random.default_rng(22)
img, d = new(K)
yy, xx = np.mgrid[0:H * S, 0:W * S].astype(np.float32) / S
MX, MY, MR = 236, 196, 122
HZ = 500

# ---- sky tone: halo round the moon, haze over the city
a = np.zeros((H * S, W * S, 3), np.float32)
dm = np.hypot(xx - MX, yy - MY)
halo = np.clip(1 - (dm - MR) / 95, 0, 1) ** 2.4 * (dm > MR)
haze = np.clip((yy - 380) / (HZ - 380), 0, 1) ** 2 * (yy < HZ)
n = fbm((H * S, W * S), 50, 4, 2)
a += np.array(B, np.float32) * np.clip(halo * .55 + haze * .62 * (.6 + .8 * n), 0, 1)[..., None]
# a faint band of thin cloud catching moonlight
cl = fbm((H * S, W * S // 6), 30, 4, 8); cl = np.asarray(Image.fromarray((cl * 255).astype(np.uint8)).resize((W * S, H * S), Image.BICUBIC), np.float32) / 255
cband = np.clip((cl - .6) * 5, 0, 1) * np.clip(1 - np.abs(yy - 392) / 60, 0, 1)
a += (np.array(mix(B, WH, .5), np.float32))[None, None, :] * (cband * .55)[..., None]
paint(img, a); d = ImageDraw.Draw(img); d.fontmode = "1"

# ---- stars (fewer near the moon), with a handful of proper sparkles
for i in range(520):
    x = rng.random() * 400; y = rng.random() * (HZ - 30)
    dist = math.hypot(x - MX, y - MY)
    if dist < MR + 26 or rng.random() < max(0, 1 - (dist - MR) / 150) * .8: continue
    m = rng.random()
    if m < .05:
        r = 1.2 + rng.random()
        d.line(P((x - r * 2, y), (x + r * 2, y)), fill=WH, width=S); d.line(P((x, y - r * 2), (x, y + r * 2)), fill=WH, width=S)
        d.ellipse(P(x - r * .7, y - r * .7, x + r * .7, y + r * .7), fill=WH)
    elif m < .3:
        d.rectangle(P(x, y, x + 1, y + 1), fill=WH if rng.random() < .8 else Y)
    else:
        d.rectangle(P(x, y, x + .67, y + .67), fill=WH)

# ---- the moon: orthographic globe, maria, craters, rays, terminator on the left
u = (xx - MX) / MR; v = -(yy - MY) / MR
rr2 = u * u + v * v; disk = rr2 <= 1
z = np.sqrt(np.clip(1 - rr2, 0, 1))
alb = np.full(u.shape, .86, np.float32)
wob = fbm((H * S, W * S), 22, 4, 5) - .5; wob2 = fbm((H * S, W * S), 60, 3, 6) - .5
MARIA = [(-.28, .47, .30, .26), (.27, .40, .19, .18), (.42, .14, .21, .17), (.76, .30, .09, .13), (.70, -.06, .12, .16),
         (.50, -.27, .09, .09), (-.62, .18, .26, .42), (-.22, -.36, .20, .16), (-.56, -.42, .10, .10), (0.0, .76, .46, .055),
         (-.05, .12, .12, .10), (.15, .62, .1, .05), (-.45, -.12, .16, .14)]
mare = np.zeros_like(alb)
for (mx_, my_, ra, rb) in MARIA:
    q = ((u - mx_ + wob * .10) / ra) ** 2 + ((v - my_ + wob2 * .10) / rb) ** 2
    mare = np.maximum(mare, np.clip((1.0 - q) * 4, 0, 1))
alb -= mare * .50
alb += (fbm((H * S, W * S), 9, 3, 7) - .5) * .22 * (1 - mare * .5)          # highland mottling
SUN = np.array([math.sin(math.radians(41)), .12, math.cos(math.radians(41))]); SUN /= np.linalg.norm(SUN)
lam = np.clip(u * SUN[0] + v * SUN[1] + z * SUN[2], 0, 1)
# craters: bright rim toward the sun, shadow inside the sunward wall
bump = np.zeros_like(alb)
CR = [(-.10, -.70, .050), (-.33, .16, .042), (-.61, .13, .024), (-.68, .40, .022), (.05, -.50, .06), (.2, -.62, .045),
      (-.02, -.86, .05), (.33, -.45, .04), (-.42, .60, .03), (.6, .55, .035), (.12, .2, .025), (.56, -.52, .04), (-.25, -.58, .035)]
for i in range(150):
    an = rng.random() * math.tau; rad = math.sqrt(rng.random()) * .96
    cu, cv = rad * math.cos(an), rad * math.sin(an)
    south = 1.6 if cv < -.2 else .7
    if rng.random() < .75 * south:
        CR.append((cu, cv, .008 + .022 * rng.random() ** 2))
for (cu, cv, cr) in CR:
    fz = math.sqrt(max(.05, 1 - cu * cu - cv * cv))
    du = (u - cu) / cr
    dv = (v - cv) / cr
    q = np.sqrt(du * du + dv * dv)
    rim = np.exp(-((q - 1) / .28) ** 2)
    bump += rim * (-(du) / np.maximum(q, .2)) * -.42            # sun from the right: right rim bright outside, left wall lit
    bump += (q < .85) * (du / np.maximum(q, .3)) * .24 - (q < .85) * .03
for (cu, cv, n_r, ln) in [(-.10, -.70, 13, .95), (-.33, .16, 9, .30), (-.61, .13, 7, .22)]:   # rays: Tycho, Copernicus, Kepler
    ang = np.arctan2(v - cv, u - cu); dist = np.hypot(u - cu, v - cv)
    r2 = np.random.default_rng(int(abs(cu) * 100))
    for k in range(n_r):
        a0 = r2.random() * math.tau; wd = .03 + .03 * r2.random(); l_ = ln * (.5 + .5 * r2.random())
        dd_ = np.abs(np.angle(np.exp(1j * (ang - a0))))
        alb += np.clip(1 - dd_ / wd, 0, 1) * np.clip(1 - dist / l_, 0, 1) * (dist > .05) * .22
    alb += np.clip(1 - dist / .07, 0, 1) * .3
limb = .62 + .38 * z ** .5
tone = np.clip((alb + bump) * limb, 0, 1.1) * np.clip(lam * 1.9, 0, 1) ** .55
earth = .0
tone = np.clip(tone, 0, 1)
# neutral greys would dither into red/green/blue specks on a six-colour palette, so the moon
# is screened here in black and white only (Floyd-Steinberg on the tone at panel resolution)
tl = tone.reshape(H, S, W, S).mean((1, 3)); dk = disk.reshape(H, S, W, S).mean((1, 3)) > .5
tb = (tl ** 1.15).tolist(); bw = np.zeros((H, W), bool)
for y_ in range(H):
    for x_ in (range(W) if y_ % 2 == 0 else range(W - 1, -1, -1)):
        if not dk[y_, x_]: continue
        o = tb[y_][x_]; nv = 1.0 if o > .5 else 0.0; bw[y_, x_] = nv > 0; e = o - nv
        sx_ = 1 if y_ % 2 == 0 else -1
        if 0 <= x_ + sx_ < W: tb[y_][x_ + sx_] += e * .4375
        if y_ + 1 < H:
            if 0 <= x_ - sx_ < W: tb[y_ + 1][x_ - sx_] += e * .1875
            tb[y_ + 1][x_] += e * .3125
            if 0 <= x_ + sx_ < W: tb[y_ + 1][x_ + sx_] += e * .0625
up = lambda m_: np.repeat(np.repeat(m_, S, 0), S, 1)
aa = np.asarray(img).copy(); aa[up(dk & bw)] = WH; aa[up(dk & ~bw)] = K
img.paste(Image.fromarray(aa)); d = ImageDraw.Draw(img); d.fontmode = "1"

# ---- Saturn, a little west of the moon
sx, sy = 70, 150
ring = Image.new("L", (60 * S, 40 * S), 0); rd = ImageDraw.Draw(ring)
rd.ellipse([8 * S, 14 * S, 52 * S, 26 * S], outline=255, width=3 * S)
ring = ring.rotate(18, resample=Image.BICUBIC)
img.paste(Y, (int((sx - 30) * S), int((sy - 20) * S)), ring)
d.ellipse(P(sx - 8, sy - 7.4, sx + 8, sy + 7.4), fill=Y)
d.line(P((sx - 7, sy - 2), (sx + 7, sy - 3.5)), fill=mix(Y, K, .4), width=S); d.line(P((sx - 7, sy + 2.5), (sx + 7, sy + 1)), fill=mix(Y, K, .3), width=S)
front = Image.new("L", (60 * S, 40 * S), 0); fd = ImageDraw.Draw(front)
fd.arc([8 * S, 14 * S, 52 * S, 26 * S], 0, 180, fill=255, width=3 * S)
front = front.rotate(18, resample=Image.BICUBIC)
img.paste(Y, (int((sx - 30) * S), int((sy - 20) * S)), front)
d.ellipse(P(sx + 31, sy + 13, sx + 33, sy + 15), fill=WH)      # Titan
text(d, (sx, sy + 32), "Saturne", "serif-bi", 13, WH)
text(d, (MX + 84, MY + MR + 20), "Lune · 89 %", "serif-bi", 13, WH)

# ---- the balloon across the limb, lit only from its own fire
BCX, BT, BH_ = 172, 236, 142
balloon(img, BCX, BT, BH_, rot=.42, simple=False, light=.2, tint=(K, .66), outline=False, figures=False, gallery=True)
aa = np.asarray(img).astype(np.float32)
bm = balloon_mask(BCX, BT, BH_)
fy = BT + BH_ * 1.0
fg = np.clip(1 - np.hypot(xx - BCX, (yy - fy) * .8) / (BH_ * .42), 0, 1) ** 1.6
warm = lerp_rgb([(0, K), (.5, mix(R, K, .3)), (.85, R), (1, mix(R, Y, .6))], fg)
sel = bm & (fg > .02) & (yy > BT + BH_ * .55)
aa[sel] = np.maximum(aa[sel] * .6, warm[sel])
# moon-rim on the right flank
edge = bm & ~np.roll(bm, -2 * S, 1) & (yy < BT + BH_ * .8)
aa[edge] = np.array(mix(WH, B, .3), np.float32)
img.paste(Image.fromarray(np.clip(aa, 0, 255).astype(np.uint8))); d = ImageDraw.Draw(img); d.fontmode = "1"
d.ellipse(P(BCX - 5, fy - 2, BCX + 5, fy + 6), fill=R); d.ellipse(P(BCX - 2.5, fy, BCX + 2.5, fy + 5), fill=Y)
for sgn in (-1, 1):                              # the two aeronauts, lit red
    fx = BCX + sgn * BH_ * .176; fyy = BT + BH_ * .91
    d.polygon(P((fx - 2, fyy), (fx + 2, fyy), (fx + 2.4, fyy - 7), (fx - 2.4, fyy - 7)), fill=mix(R, K, .2))
    d.ellipse(P(fx - 1.7, fyy - 10.5, fx + 1.7, fyy - 7), fill=mix(R, Y, .5))
for i in range(60):                              # sparks
    f = rng.random(); x = BCX + 6 + f * 70 + rng.normal(0, 5); y = fy + 8 + f * 26 + rng.normal(0, 5)
    d.rectangle(P(x, y, x + .8, y + .8), fill=R if rng.random() < .6 else Y)

# ---- Paris asleep
sk = [(0, HZ + 8)]
x = 0.0
roofs = []
while x < 400:
    w = 8 + rng.random() * 20; h_ = 10 + rng.random() * 30
    kind = rng.random()
    roofs.append((x, w, h_, kind)); x += w
d.rectangle(P(0, HZ + 6, 400, 548), fill=K)
for (x, w, h_, kind) in roofs:
    top = HZ + 8 - h_
    d.rectangle(P(x, top, x + w + .4, 548), fill=K)
    if kind < .55:
        d.polygon(P((x, top), (x + w, top), (x + w * .8, top - w * .35), (x + w * .2, top - w * .35)), fill=K)
    elif kind < .7:
        d.polygon(P((x, top), (x + w, top), (x + w / 2, top - w * .6)), fill=K)
    for k in range(int(1 + w / 9)):
        cx_ = x + 2 + rng.random() * (w - 5)
        d.rectangle(P(cx_, top - w * .3 - 5 - rng.random() * 5, cx_ + 2.4, top), fill=K)
    # moonlit right-hand edges and roof lines
    d.line(P((x + w, top + 1), (x + w, HZ + 30)), fill=mix(K, B, .8), width=1)
    d.line(P((x + 1, top), (x + w, top)), fill=mix(B, WH, .45), width=1)
    for r_ in range(int(h_ / 9) + 2):
        for c_ in range(int(w / 6)):
            wx = x + 2.5 + c_ * 6; wy = top + 5 + r_ * 9
            if wy > 540: continue
            p = rng.random()
            if p < .07:
                d.rectangle(P(wx, wy, wx + 2.4, wy + 4), fill=Y)
            elif p < .45:
                d.rectangle(P(wx, wy, wx + 2.4, wy + 4), fill=mix(K, B, .55))
# Notre-Dame, a dome, a spire
nx = 300
d.rectangle(P(nx, HZ - 46, nx + 12, HZ + 10), fill=K); d.rectangle(P(nx + 17, HZ - 46, nx + 29, HZ + 10), fill=K)
d.rectangle(P(nx + 12, HZ - 26, nx + 17, HZ + 10), fill=K); d.rectangle(P(nx + 29, HZ - 22, nx + 70, HZ + 10), fill=K)
d.polygon(P((nx + 29, HZ - 22), (nx + 70, HZ - 22), (nx + 66, HZ - 34), (nx + 29, HZ - 34)), fill=K)
d.polygon(P((nx + 48, HZ - 34), (nx + 52, HZ - 34), (nx + 50, HZ - 66)), fill=K)
for tx in (nx, nx + 17):
    d.line(P((tx + 12, HZ - 45), (tx + 12, HZ)), fill=mix(B, WH, .45), width=1)
    for k in range(3):
        d.rectangle(P(tx + 3 + k * 3, HZ - 40, tx + 4 + k * 3, HZ - 26), fill=mix(K, B, .7))
d.ellipse(P(nx + 11, HZ - 18, nx + 18, HZ - 11), fill=mix(K, B, .7)); d.ellipse(P(nx + 13.5, HZ - 15.5, nx + 15.5, HZ - 13.5), fill=Y)
dx_ = 60
d.rectangle(P(dx_ - 16, HZ - 16, dx_ + 16, HZ + 10), fill=K); d.pieslice(P(dx_ - 14, HZ - 40, dx_ + 14, HZ + 4), 180, 360, fill=K)
d.rectangle(P(dx_ - 2.5, HZ - 50, dx_ + 2.5, HZ - 38), fill=K); d.line(P((dx_, HZ - 60), (dx_, HZ - 48)), fill=K, width=S)
d.arc(P(dx_ - 14, HZ - 40, dx_ + 14, HZ + 4), 280, 350, fill=mix(B, WH, .45), width=S)

# ---- the Seine, with the moon's road on it
d.rectangle(P(0, 548, 400, 600), fill=K)
d.line(P((0, 548), (400, 548)), fill=mix(K, B, .7), width=S)
for i in range(150):
    x = rng.random() * 400; y = 551 + rng.random() * 48; ln = 4 + rng.random() * 16
    d.line(P((x, y), (x + ln, y)), fill=B, width=S)
y = 551.0
while y < 600:
    f = (y - 551) / 49
    for k in range(int(2 + f * 3)):
        w_ = (6 + 22 * f) * rng.random(); off = rng.normal(0, 7 + 16 * f)
        d.line(P((MX + off - w_ / 2, y), (MX + off + w_ / 2, y)), fill=WH if rng.random() < .8 else Y, width=S)
    y += 2.2 + f
# a bridge with lamps
by = 556
d.rectangle(P(0, by - 5, 400, by), fill=K)
for k in range(5):
    cx_ = 40 + k * 80
    d.rectangle(P(cx_ - 4, by, cx_ + 4, by + 14), fill=K)
    d.line(P((cx_, by - 5), (cx_, by - 13)), fill=K, width=S); d.rectangle(P(cx_ - 1.5, by - 16, cx_ + 1.5, by - 12), fill=Y)
    for j in range(5):
        if rng.random() < .7: d.line(P((cx_ - 1.5, by + 18 + j * 4), (cx_ + 2, by + 18 + j * 4)), fill=Y, width=S)
d.line(P((0, by - 5), (400, by - 5)), fill=mix(B, WH, .45), width=1)
finish(img)
