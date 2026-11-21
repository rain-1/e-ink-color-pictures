"""Morning — 'Avant le feu'. Six o'clock at La Muette: the envelope hangs slack between its
two masts, the brazier is being lit, and the four morning planets of 21 November 2026
(Jupiter and Mars high, Venus and Mercury low) stand over the garden.
Aquatint dawn with black silhouettes; red-orange in charge."""
import sys, math, os
sys.path.insert(0, os.path.dirname(__file__))
from common import *

rng = np.random.default_rng(6)
img, d = new(K)
yy, xx = np.mgrid[0:H * S, 0:W * S].astype(np.float32) / S
GY = 505
n1 = fbm((H * S, W * S), 70, 4, 3)
t = np.clip(yy / GY + (n1 - .5) * .07, 0, 1)
NAVY = mix(B, K, .55)
sky = lerp_rgb([(0, NAVY), (.22, B), (.40, mix(B, R, .55)), (.56, R), (.74, mix(R, Y, .55)), (.90, Y), (1, mix(Y, WH, .6))], t)
# long cloud bars, lit from beneath
bars = fbm((H * S, W * S // 7), 26, 4, 11)
bars = np.asarray(Image.fromarray((bars * 255).astype(np.uint8)).resize((W * S, H * S), Image.BICUBIC), np.float32) / 255
band = np.clip((bars - .56) * 7, 0, 1) * np.clip((yy - 150) / 80, 0, 1) * np.clip((GY - 20 - yy) / 60, 0, 1)
dark = lerp_rgb([(0, NAVY), (.45, mix(B, K, .3)), (.7, mix(R, K, .45)), (1, mix(R, K, .2))], t)
sky = sky * (1 - band[..., None] * .85) + dark * band[..., None] * .85
under = np.clip(np.roll(band, -5 * S, 0) - band, 0, 1)[..., None]
sky = sky + (np.array(Y, np.float32) - sky) * under * .8
paint(img, sky)
d = ImageDraw.Draw(img); d.fontmode = "1"

# ---- stars and the four planets along the ecliptic
for i in range(110):
    x = rng.random() * 400; y = rng.random() ** 1.8 * 190
    if rng.random() < .16:
        d.line(P((x - 2, y), (x + 2, y)), fill=WH, width=S); d.line(P((x, y - 2), (x, y + 2)), fill=WH, width=S)
    else:
        d.rectangle(P(x, y, x + .7, y + .7), fill=WH)
ecl = lambda x: 30 + (x - 330) ** 2 * 0.0042 + (330 - x) * .08
for x in range(40, 372, 7):
    d.ellipse(P(x - .7, ecl(x) - .7, x + .7, ecl(x) + .7), fill=WH)
def spark(x, y, r, col=WH):
    d.polygon(P((x, y - r * 2.4), (x + r * .45, y - r * .45), (x + r * 2.4, y), (x + r * .45, y + r * .45), (x, y + r * 2.4),
                (x - r * .45, y + r * .45), (x - r * 2.4, y), (x - r * .45, y - r * .45)), fill=col)
    d.ellipse(P(x - r, y - r, x + r, y + r), fill=col)
jx, mx_, vx, hx = 318, 282, 128, 66
spark(jx, ecl(jx), 3.4)
for k in (-11, -7, 6, 13):                      # the Galilean moons
    d.rectangle(P(jx + k, ecl(jx) - 1.5 + k * .12, jx + k + 1, ecl(jx) - .5 + k * .12), fill=WH)
d.ellipse(P(mx_ - 3, ecl(mx_) - 3, mx_ + 3, ecl(mx_) + 3), fill=R, outline=WH, width=S)
spark(vx, ecl(vx), 4.6)
d.ellipse(P(hx - 2.4, ecl(hx) - 2.4, hx + 2.4, ecl(hx) + 2.4), fill=WH)
text(d, (jx + 10, ecl(jx) - 16), "Jupiter", "serif-bi", 13, WH, anchor="lm")
text(d, (mx_ - 9, ecl(mx_) + 13), "Mars", "serif-bi", 13, WH, anchor="rm")
text(d, (vx + 14, ecl(vx) - 13), "Vénus", "serif-bi", 13, WH, anchor="lm")
text(d, (hx + 8, ecl(hx) - 12), "Mercure", "serif-bi", 13, WH, anchor="lm")

# ---- distant garden wall of trees, and the château
for i in range(60):
    x = rng.random() * 400; r = 6 + rng.random() * 12
    d.ellipse(P(x - r, GY - 14 - r * 1.2, x + r, GY + 6), fill=mix(K, R, .25))
CH = (0, 150)                                   # château de la Muette, left
d.rectangle(P(0, 408, 150, GY), fill=K)
d.polygon(P((0, 408), (150, 408), (140, 380), (0, 380)), fill=K)              # mansard
d.polygon(P((52, 408), (104, 408), (104, 392), (78, 366), (52, 392)), fill=K)   # pediment pavilion
for cx_ in (18, 40, 116, 134):
    d.rectangle(P(cx_, 360, cx_ + 8, 384), fill=K); d.rectangle(P(cx_ - 1, 357, cx_ + 9, 360), fill=K)
for cx_ in (28, 126):                           # dormers
    d.polygon(P((cx_ - 6, 398), (cx_ + 6, 398), (cx_ + 6, 388), (cx_, 383), (cx_ - 6, 388)), fill=K)
    d.rectangle(P(cx_ - 3, 389, cx_ + 3, 397), fill=mix(K, R, .4))
d.line(P((78, 366), (78, 352)), fill=K, width=S); d.polygon(P((78, 352), (90, 355), (78, 358)), fill=K)
d.line(P((0, 409), (150, 409)), fill=mix(K, R, .6), width=1); d.line(P((0, 452), (150, 452)), fill=mix(K, R, .5), width=1)
lit = {(0, 1), (1, 4), (0, 5)}
for r_ in range(2):
    for c_ in range(7):
        wx = 8 + c_ * 20.5; wy = 418 + r_ * 44
        if (r_, c_) in lit:
            d.rectangle(P(wx, wy, wx + 9, wy + 26), fill=Y); d.rectangle(P(wx + 1.5, wy + 2, wx + 7.5, wy + 11), fill=mix(Y, WH, .6))
        else:
            d.rectangle(P(wx, wy, wx + 9, wy + 26), fill=mix(K, B, .45))
        d.line(P((wx + 4.5, wy), (wx + 4.5, wy + 26)), fill=K, width=S)
        for j in (1, 2): d.line(P((wx, wy + j * 8.6), (wx + 9, wy + j * 8.6)), fill=K, width=1)
d.rectangle(P(70, 470, 86, GY), fill=mix(K, B, .3)); d.pieslice(P(70, 462, 86, 478), 180, 360, fill=mix(K, B, .3))

# ---- bare trees against the light
tree(d, 388, GY, 62, ang=-1.62, depth=9, width=9, rng=np.random.default_rng(4), spread=.5)
tree(d, 356, GY, 34, ang=-1.45, depth=7, width=4.5, rng=np.random.default_rng(9))
tree(d, 166, GY, 30, ang=-1.7, depth=7, width=4, rng=np.random.default_rng(12))

# ---- masts, ropes, the slack envelope, the stage
M1, M2, MT = 182, 352, 176
CX, BT, BH_ = 267, 232, 236
for mx in (M1, M2):
    d.polygon(P((mx - 3, GY), (mx + 3, GY), (mx + 1.2, MT), (mx - 1.2, MT)), fill=K)
    d.ellipse(P(mx - 3, MT - 3, mx + 3, MT + 3), fill=K)
    d.polygon(P((mx, MT - 3), (mx + 15, MT - 12), (mx, MT - 20)), fill=R); d.line(P((mx, MT + 2), (mx, MT - 22)), fill=K, width=S)
    for k in range(9):                           # climbing cleats
        y = GY - 20 - k * 32
        d.line(P((mx - 5, y), (mx + 5, y)), fill=K, width=S)
    sgn = -1 if mx == M1 else 1
    d.line(P((mx, MT + 6), (mx + sgn * 52, GY)), fill=K, width=S)       # guy rope
# rope from mast-head to mast-head, sagging to the crown of the balloon
rope = []
for i in range(41):
    f = i / 40; x = M1 + (M2 - M1) * f
    sag = (BT - MT + 4) * (1 - abs(2 * f - 1) ** 1.6)
    rope.append((x, MT + sag))
d.line(P(rope), fill=K, width=S + 1)
m = balloon(img, CX, BT, BH_, rot=.5, light=.75, tint=(mix(K, B, .25), .62), gallery=False, outline=True)
d = ImageDraw.Draw(img); d.fontmode = "1"
# slack folds in the lower half: dark creases and a caught edge of dawn on the right
for i in range(16):
    f = (i + .5) / 16
    tt = np.linspace(.52, .99, 30)
    xs = CX + (f * 2 - 1) * profile(tt) * BH_ * (.96 - .1 * np.sin(tt * 9 + i))
    ys = BT + tt * BH_
    d.line(P(list(zip(xs.tolist(), ys.tolist()))), fill=K, width=S if i % 3 else S + 2)
tt = np.linspace(.03, .78, 60)
xs = CX + profile(tt) * BH_ * .985; ys = BT + tt * BH_
d.line(P(list(zip(xs.tolist(), ys.tolist()))), fill=mix(R, Y, .5), width=S + 1)
# hauling ropes from the equator down to the ground crews
for sgn, gx in ((-1, 205), (1, 338), (-1, 226), (1, 318)):
    ex = CX + sgn * R_EQ * BH_ * .97; ey = BT + T_EQ * BH_
    d.line(P((ex, ey), (gx, GY - 34)), fill=K, width=S)

# the stage (drawn over the mouth of the balloon), with brazier glow and stairs
SY = 458
d.rectangle(P(206, SY, 328, SY + 7), fill=K)
gm = (np.hypot(xx - CX, (yy - (SY + 34)) * 1.3) < 44)
glow = np.clip(1 - np.hypot(xx - CX, (yy - (SY + 34)) * 1.3) / 44, 0, 1) ** 1.2
a = np.asarray(img).astype(np.float32)
box = (xx > 210) & (xx < 324) & (yy > SY + 7) & (yy < GY)
gcol = lerp_rgb([(0, mix(K, R, .5)), (.45, R), (.8, Y), (1, mix(Y, WH, .7))], glow)
a[box] = gcol[box]; img.paste(Image.fromarray(a.astype(np.uint8))); d = ImageDraw.Draw(img); d.fontmode = "1"
for x in range(210, 326, 13):                    # trestle posts and cross-braces in silhouette
    d.rectangle(P(x - 1.5, SY + 7, x + 1.5, GY), fill=K)
    if x + 13 < 326:
        d.line(P((x, SY + 8), (x + 13, GY)), fill=K, width=S); d.line(P((x + 13, SY + 8), (x, GY)), fill=K, width=S)
for x in range(206, 330, 6):                     # railing
    d.line(P((x, SY - 13), (x, SY)), fill=K, width=S)
d.line(P((206, SY - 13), (329, SY - 13)), fill=K, width=S + 1)
for k in range(8):                               # stairs on the left
    d.rectangle(P(206 - (k + 1) * 6, SY + k * 6, 206 - k * 6, GY), fill=K)

# ---- people: all silhouettes, a few lanterns
def man(x, y, h=20, arm=None, hat=True, lantern=False):
    d.polygon(P((x - h * .16, y), (x + h * .16, y), (x + h * .2, y - h * .72), (x - h * .2, y - h * .72)), fill=K)
    d.ellipse(P(x - h * .12, y - h * .95, x + h * .12, y - h * .72), fill=K)
    if hat: d.polygon(P((x - h * .24, y - h * .9), (x + h * .24, y - h * .9), (x, y - h * 1.06)), fill=K)
    if arm is not None:
        d.line(P((x, y - h * .62), (x + arm[0], y - h * .62 + arm[1])), fill=K, width=S + 1)
    if lantern:
        lx, ly = x + h * .42, y - h * .38
        d.line(P((x + h * .1, y - h * .6), (lx, ly - 3)), fill=K, width=S)
        d.rectangle(P(lx - 2.2, ly - 3, lx + 2.2, ly + 3), fill=Y, outline=K, width=1); d.rectangle(P(lx - 1, ly - 1.5, lx + 1, ly + 1.5), fill=WH)
for gx, sgn in ((205, 1), (198, 1), (338, -1), (345, -1), (226, 1), (318, -1)):     # rope crews, leaning back
    man(gx, GY, 21, arm=(sgn * 7, -11))
man(240, SY, 18, arm=(8, -9)); man(294, SY, 18, arm=(-8, -10)); man(268, SY, 19, arm=(0, -13), hat=False)
man(M2 + 1, GY - 150, 15, arm=(-6, -8), hat=False)                                 # a rigger up the mast
for x, h_, lan in ((16, 22, True), (30, 20, False), (120, 22, True), (134, 19, False), (150, 21, False), (372, 21, True), (386, 19, False)):
    man(x, GY + 6, h_, lantern=lan)
# a ladder against the stage
d.line(P((330, SY), (344, GY)), fill=K, width=S); d.line(P((336, SY), (350, GY)), fill=K, width=S)
for k in range(7):
    y = SY + 5 + k * 6.5; x = 330 + (y - SY) * 14 / (GY - SY)
    d.line(P((x, y), (x + 6, y)), fill=K, width=S)

# ---- foreground: parterre in the dark — clipped box, gravel walk, a fountain basin
d.rectangle(P(0, GY, 400, 600), fill=K)
gr = mask_of(lambda dd: dd.polygon(P((150, GY + 2), (250, GY + 2), (330, 600), (70, 600)), fill=255))
a = np.asarray(img).astype(np.float32)
gn = fbm((H * S, W * S), 6, 2, 5)
gt = np.clip(.22 + .5 * (gn - .5) + .25 * np.clip(1 - np.abs(xx - 200) / 120, 0, 1), 0, 1)
gcol = lerp_rgb([(0, K), (1, mix(R, Y, .6))], gt * np.clip(1.25 - (yy - GY) / 110, .3, 1))
a[gr] = gcol[gr]; img.paste(Image.fromarray(a.astype(np.uint8))); d = ImageDraw.Draw(img); d.fontmode = "1"
for sgn in (-1, 1):                              # box-hedge scrolls either side of the walk
    for k in range(4):
        y0 = GY + 10 + k * 22 + k * k * 1.5; hgt = 14 + k * 3
        xa = 200 + sgn * (62 + k * 24); xb = 200 + sgn * 215
        box_ = BX(xa, y0, xb, y0 + hgt)
        d.rounded_rectangle(box_, radius=hgt * S / 2, fill=mix(K, G, .55))
        d.rounded_rectangle(BX(xa + sgn * 5, y0 + 4, xb, y0 + hgt - 4), radius=max(1, (hgt - 8) * S / 2), fill=K)
        for j in range(3):                       # topiary cones
            tx = xa + sgn * (16 + j * (38 + k * 6))
            d.polygon(P((tx - 4 - k, y0 + 2), (tx + 4 + k, y0 + 2), (tx, y0 - 14 - k * 4)), fill=mix(K, G, .7))
            d.ellipse(P(tx - 2, y0 - 18 - k * 4, tx + 2, y0 - 13 - k * 4), fill=mix(K, G, .7))
d.ellipse(P(160, 560, 240, 584), fill=K); d.ellipse(P(164, 562, 236, 580), fill=mix(R, Y, .55))
d.ellipse(P(170, 564, 230, 578), fill=mix(B, K, .4)); d.rectangle(P(198, 548, 202, 572), fill=K); d.ellipse(P(193, 544, 207, 552), fill=K)
finish(img)
