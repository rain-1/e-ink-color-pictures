# Evening — "La Lune du Castor". Red in charge; yellow, black, a little blue, olive and white.
# For Toulouse-Lautrec, born this day in 1864: a lithographic poster with flat colour, black
# silhouette and crachis (spatter) instead of a regular screen. The supermoon rises behind
# alders; on the bank a beaver is two-thirds through a trunk. Lettering at the foot.
import math, random
import numpy as np
from common import *
rng = random.Random(1864); img, d = new(R); SP = spatter(64); SP2 = spatter(65)
HZ = 392
# --- sky: red at the top, spattering down to yellow at the horizon
sky = YY < HZ
tone(img, sky, R, Y, np.clip((YY - 150) / 250, 0, 1) ** 1.5 * 0.95, SP)
tone(img, sky & (YY < 150), None, K, np.clip((150 - YY) / 150, 0, 1) ** 2 * 0.5, SP2)
# --- the moon
mx, my, mr = 226, 222, 124
moon = ell_mask(mx, my, mr, mr)
tone(img, moon, Wh, Y, 0.10, SP)
U = (XX - mx) / mr; V = -(YY - my) / mr; M = np.full((H, W), -9.0, np.float32)
for (u, v, s) in [(-.25, .50, .31), (.28, .46, .19), (.47, .16, .21), (.77, .30, .105), (.72, -.10, .15), (.52, -.28, .10),
                  (-.22, -.36, .21), (-.57, -.41, .115), (-.62, .22, .30), (-.52, -.06, .22), (.05, .22, .075)]:
    M = np.maximum(M, 1 - np.hypot(U - u, V - v) / s)
M += 0.5 * (fbm(7, 40, 3) - 0.5)
tone(img, moon & (M > -0.1), None, Y, np.clip(0.45 + M * 2.5, 0, 0.92), SP2)
ring = ell_mask(mx, my, mr + 2, mr + 2) & ~moon
a = np.asarray(img).copy(); a[ring & sky] = K; img.paste(Image.fromarray(a))
# --- far shore
far = [(0, HZ)] + [(x, HZ - 16 - 9 * math.sin(x / 27) - 6 * math.sin(x / 9 + 1) - rng.uniform(0, 5)) for x in range(0, W + 4, 4)] + [(W, HZ)]
d.polygon(far, fill=K); tone(img, poly_mask(far), None, G, 0.35, SP)
for x in range(6, W, 9):
    if rng.random() < 0.6: branch(d, x, HZ - 14, -math.pi / 2 + rng.gauss(0, 0.15), rng.uniform(12, 26), 1.2, 3, K, rng, 0.5, 0.7)
# --- water
water = YY >= HZ
tone(img, water, B, K, 0.25 + 0.4 * (YY - HZ) / 200, SP)
for y in range(HZ + 3, 560, 2):                                  # the moon's reflection, in broken strokes
    t = (y - HZ) / 170; hw = 70 * (1 - 0.35 * t) * rng.uniform(0.5, 1.1)
    if rng.random() < 0.85:
        x0 = mx - hw + rng.uniform(-12, 12); x1 = mx + hw + rng.uniform(-12, 12)
        d.line((x0, y, x1, y), fill=Y if rng.random() < 0.75 else Wh)
    if rng.random() < 0.5:
        x0 = rng.uniform(0, W); d.line((x0, y, x0 + rng.uniform(8, 40), y), fill=R if rng.random() < 0.6 else Y)
tone(img, water & (YY > 470) & (np.abs(XX - mx) > 84), None, K, np.clip((YY - 470) / 110, 0, 0.9), SP2)
# --- ducks coming in across the moon
def duck(x, y, s):
    d.polygon([(x - 9 * s, y), (x - 2 * s, y - 2 * s), (x + 8 * s, y - 1 * s), (x + 12 * s, y - 3 * s), (x + 15 * s, y - 2 * s), (x + 8 * s, y + 2 * s), (x - 3 * s, y + 2 * s)], fill=K)
    d.polygon([(x - 1 * s, y - 1 * s), (x - 5 * s, y - 11 * s), (x + 5 * s, y - 1 * s)], fill=K)
    d.polygon([(x + 1 * s, y + 1 * s), (x - 1 * s, y + 8 * s), (x + 5 * s, y + 1 * s)], fill=K)
for i, (x, y, s) in enumerate([(120, 150, 1.3), (154, 134, 1.2), (186, 122, 1.1), (214, 114, 1.0), (96, 172, 1.4), (240, 112, .9)]): duck(x, y, s)

# --- the near bank
bank = [(0, 502)] + [(x, 504 + 12 * math.sin(x / 50 + 1) + 5 * math.sin(x / 13)) for x in range(0, W + 5, 5)] + [(W, H), (0, H)]
d.polygon(bank, fill=K)
# --- alders: one great tree on the left crossing the moon, one slender to the right
tips = []
def trunk(x0, y0, x1, y1, w0, w1, bow):
    pts = []
    for i in range(401):
        t = i / 400; x = x0 + (x1 - x0) * t + bow * math.sin(t * math.pi); y = y0 + (y1 - y0) * t; w = w0 + (w1 - w0) * t
        d.ellipse((x - w / 2, y - w / 2, x + w / 2, y + w / 2), fill=K); pts.append((x, y, w))
    return pts
tp = trunk(58, 560, 98, 96, 30, 9, -22)
for i in (13, 20, 26, 30, 34, 38):
    x, y, w = tp[i * 10]; side = 1 if i % 2 else -1
    branch(d, x, y, -math.pi / 2 + side * rng.uniform(0.75, 1.25) + 0.15, rng.uniform(56, 84) * (1.0 if side > 0 else 0.7), w * 0.5, 6, K, rng, 0.55, 0.74, tips, bend=-0.03 * side)
branch(d, tp[400][0], tp[400][1], -math.pi / 2 + 0.1, 60, 7, 6, K, rng, 0.55, 0.74, tips)
tp2 = trunk(372, 560, 356, 60, 13, 5, 10)
for i in (12, 17, 21, 25, 29, 33, 37):
    x, y, w = tp2[i * 10]; side = -1 if i % 2 else 1
    branch(d, x, y, -math.pi / 2 + side * rng.uniform(0.7, 1.2), rng.uniform(36, 66) * (1.2 if side < 0 else 0.6), w * 0.5, 6, K, rng, 0.55, 0.74, tips)
branch(d, tp2[400][0], tp2[400][1], -math.pi / 2 - 0.1, 50, 4, 6, K, rng, 0.55, 0.74, tips)
for (x, y) in tips:                                              # catkins and last year's cones
    q = rng.random()
    if q < 0.16: d.line((x, y, x + rng.uniform(-1, 1), y + rng.uniform(5, 9)), fill=K, width=2)
    elif q < 0.24: d.ellipse((x - 2, y - 2, x + 2, y + 3), fill=K)
    elif q < 0.27: d.ellipse((x - 2, y - 1, x + 2, y + 4), fill=Y if y > 330 or (x - mx) ** 2 + (y - my) ** 2 > mr * mr else R)

# --- the beaver at work on a third trunk
gx, gy = 272, 506                                                 # the cut
d.polygon([(gx - 11, 566), (gx - 10, gy + 14), (gx - 3, gy + 1), (gx + 3, gy + 1), (gx + 10, gy + 14), (gx + 11, 566)], fill=K)
d.polygon([(gx - 3, gy - 1), (gx + 3, gy - 1), (gx + 10, gy - 14), (gx + 12, 250), (gx + 2, 250), (gx - 9, gy - 14)], fill=K)
d.polygon([(gx - 8, gy + 12), (gx - 2, gy + 1), (gx + 2, gy + 1), (gx + 8, gy + 12)], fill=Y)
d.polygon([(gx - 2, gy - 1), (gx + 2, gy - 1), (gx + 8, gy - 12), (gx - 7, gy - 12)], fill=Y)
tk = [(gx + 7, 250, 10)]
for (yy, side) in [(300, 1), (350, -1), (270, 1)]:
    branch(d, gx + 6, yy, -math.pi / 2 + side * 0.9, 34, 3, 5, K, rng, 0.55, 0.74)
branch(d, gx + 7, 252, -math.pi / 2 + 0.05, 44, 5, 5, K, rng, 0.55, 0.74)
bx, by = gx - 46, 516                                             # beaver, upright, facing the trunk
body = ell_mask(bx, by, 22, 30) | ell_mask(bx + 14, by - 30, 15, 13) | ell_mask(bx + 26, by - 26, 9, 7) | ell_mask(bx - 4, by + 16, 26, 16)
a = np.asarray(img).copy(); a[body] = K; img.paste(Image.fromarray(a))
d.ellipse((bx + 4, by - 46, bx + 11, by - 39), fill=K)                                              # ear
d.polygon([(bx + 12, by - 14), (gx - 9, gy - 8), (gx - 9, gy - 3), (bx + 12, by - 4)], fill=K)         # forepaws on the trunk
d.polygon([(bx - 20, by + 20), (bx - 66, by + 30), (bx - 74, by + 38), (bx - 62, by + 44), (bx - 18, by + 34)], fill=K)   # tail
for k in range(6): d.line((bx - 60 + k * 7, by + 32, bx - 56 + k * 7, by + 40), fill=B)
d.ellipse((bx + 19, by - 34, bx + 22, by - 31), fill=Y)                                              # eye, catching the moon
d.line((bx + 33, by - 23, bx + 33, by - 19), fill=Y, width=2)                                        # tooth
edge = body & ~np.roll(body, 2, 1)                                                                    # rim light on the back
tone(img, edge & (YY < by + 10), None, Y, 0.8, SP)
for _ in range(70):                                               # chips
    x = gx + rng.gauss(-6, 22); y = 536 + rng.uniform(-8, 22)
    d.line((x, y, x + rng.uniform(2, 6), y + rng.uniform(-3, 1)), fill=Y if rng.random() < 0.8 else Wh)
for _ in range(150):                                              # sedge on the bank
    x = rng.uniform(0, W); y = 514 + rng.uniform(-6, 40); Ln = rng.uniform(10, 36); an = -math.pi / 2 + rng.gauss(0, 0.3)
    d.line((x, y, x + math.cos(an) * Ln, y + math.sin(an) * Ln), fill=K if y - Ln < 502 else rng.choice([G, G, Y]))

# --- lettering
a = np.asarray(img).copy(); a[566:] = K; img.paste(Image.fromarray(a))
ft = font("DejaVu Serif:bold:italic", 21)
spaced(d, 200, 566, "LA LUNE DU CASTOR", ft, Y, gap=2)
d.line((20, 564, 380, 564), fill=R); d.line((20, 594, 380, 594), fill=R)
f2 = font("DejaVu Serif:bold:italic", 12)
d.ellipse((14, 12, 52, 50), fill=K, outline=Y, width=2); d.text((25, 17), "XI", font=font("DejaVu Serif:bold", 11), fill=Y); d.text((25, 30), "24", font=font("DejaVu Serif:bold", 11), fill=Y)
save(img)
