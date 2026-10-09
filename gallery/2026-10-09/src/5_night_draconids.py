"""Draconids, the night before the new moon. Draco winds across the top; meteors fan from
the dragon's head. Milky Way as sparse stipple; ridges and mist below; a hanok village with
three lit windows; one person lying on a roof looking up."""
import math, random
import numpy as np
from PIL import Image, ImageDraw
from kit import *

rnd = random.Random(1009)
a = np.zeros((H, W, 3), np.uint8)
yy, xx = np.mgrid[0:H, 0:W]
# Milky Way: a diagonal band of stipple, densest at its spine, with a dark rift
dist = (xx * 0.62 + yy * 0.78 - 330) / 70
rift = np.exp(-((xx * 0.62 + yy * 0.78 - 318) / 9) ** 2) * (yy > 120)
dens = np.exp(-dist ** 2) * 0.10 * (1 - 0.9 * rift) * np.clip((470 - yy) / 120, 0, 1)
noise = np.random.default_rng(3).random((H, W))
a[noise < dens * (0.6 + 0.4 * BAYER)] = WH
blue = (noise > 0.995) & (dens > 0.08)
a[blue] = B
img = Image.fromarray(a); d = ImageDraw.Draw(img)

# field stars: a few hundred points, some brighter crosses
for i in range(520):
    x, y = rnd.uniform(0, W), rnd.uniform(0, 470) ** 1.0
    m = rnd.random()
    if m < .85:
        d.point((x, y), fill=WH if rnd.random() < .85 else Y)
    elif m < .97:
        d.rectangle([x, y, x + 1, y + 1], fill=WH)
    else:
        d.line([(x - 3, y), (x + 3, y)], fill=WH); d.line([(x, y - 3), (x, y + 3)], fill=WH)
        d.rectangle([x - 1, y - 1, x + 1, y + 1], fill=WH)

# Draco (stylised): tail between the Dipper bowls, body coiling, head a quadrilateral
draco = [(40, 200), (78, 168), (120, 160), (150, 128), (190, 120), (214, 150), (206, 188),
         (232, 214), (270, 206), (300, 176), (318, 140)]
head = [(318, 140), (350, 120), (362, 146), (336, 160)]
for p, q in zip(draco, draco[1:]):
    d.line([p, q], fill=B, width=1)
d.line(head + [head[0]], fill=B, width=1)
for (x, y) in draco + head:
    r = 3 if (x, y) in head[:2] else 2
    d.ellipse([x - r, y - r, x + r, y + r], fill=WH)
ex, ey = 350, 120  # Eltanin, near the radiant
for k in range(8):  # glow spikes on Eltanin
    t = k * math.pi / 4
    L = 9 if k % 2 == 0 else 5
    d.line([(ex, ey), (ex + L * math.cos(t), ey + L * math.sin(t))], fill=Y)
d.ellipse([ex - 3, ey - 3, ex + 3, ey + 3], fill=WH)
# Little Dipper and Polaris (approximate)
ursa = [(110, 60), (138, 74), (160, 92), (178, 104), (204, 98), (210, 76), (186, 70)]
for p, q in zip(ursa, ursa[1:]): d.line([p, q], fill=B)
d.line([ursa[-1], ursa[3]], fill=B)
for (x, y) in ursa: d.rectangle([x - 1, y - 1, x + 1, y + 1], fill=WH)
d.ellipse([107, 57, 113, 63], fill=Y)

# meteors: fanning from the radiant at the head
RX, RY = 340, 140
for ang, start, L in [(2.4, 40, 120), (1.9, 70, 150), (2.9, 30, 90), (1.45, 60, 110), (3.4, 50, 80),
                      (2.15, 150, 130), (0.9, 40, 70), (2.65, 110, 140), (1.65, 170, 100)]:
    x0, y0 = RX + start * math.cos(ang), RY + start * math.sin(ang)
    x1, y1 = RX + (start + L) * math.cos(ang), RY + (start + L) * math.sin(ang)
    steps = 40
    for s in range(steps):
        u = s / steps
        px, py = x0 + (x1 - x0) * u, y0 + (y1 - y0) * u
        if u < 0.35:
            if s % 3 == 0: d.point((px, py), fill=B)
        elif u < 0.6:
            d.point((px, py), fill=Y)
        else:
            d.point((px, py), fill=WH)
            if u > 0.85: d.rectangle([px - 1, py - 1, px, py], fill=WH)
    d.ellipse([x1 - 2, y1 - 2, x1 + 2, y1 + 2], fill=WH)

# ridges, back to front, with screened mist in the valleys
arr = np.array(img)
def ridge_y(x, base, amp, f, ph):
    return base - amp * (0.6 * math.sin(x / f + ph) + 0.4 * math.sin(x / (f * .37) + ph * 2)) - abs(math.sin(x / (f * 2.1) + ph)) * amp * .5
layers = [(420, 26, 60, 0.3, 0.30), (450, 22, 48, 1.7, 0.18), (482, 18, 40, 2.9, 0.08)]
for base, amp, f, ph, mist in layers:
    top = np.array([ridge_y(x, base, amp, f, ph) for x in range(W)])
    m = yy >= top[None, :]
    arr[m] = K
    band = m & (yy < top[None, :] + 12)
    screen(arr, band, K, B, np.clip(1 - (yy - top[None, :]) / 12, 0, 1) * mist * 1.6)
    for x in range(0, W, 3):  # pine bristles on the crest
        if (x * 7 + base) % 5 < 3:
            h_ = 3 + (x * 13 + base) % 6
            arr[int(top[x]) - h_:int(top[x]), x] = K
img = Image.fromarray(arr); d = ImageDraw.Draw(img)

# village: hanok roofs with upturned eaves, foreground
def hanok(cx, by, w, h, lit=None, rafters=True):
    roof = [(cx - w / 2 - 14, by - h - 2), (cx - w / 2 - 4, by - h - 6), (cx - w * .32, by - h - 22),
            (cx + w * .32, by - h - 22), (cx + w / 2 + 4, by - h - 6), (cx + w / 2 + 14, by - h - 2),
            (cx + w / 2, by - h + 6), (cx - w / 2, by - h + 6)]
    d.rectangle([cx - w / 2 + 4, by - h + 6, cx + w / 2 - 4, by], fill=K)
    d.polygon(roof, fill=K)
    # tile ridges catching starlight
    for k in range(int(w / 5)):
        x = cx - w * .32 + k * 5 * (w * .64) / w
        d.line([(x, by - h - 21), (x + (x - cx) * .45, by - h + 4)], fill=B, width=1)
    d.line([(cx - w * .32, by - h - 22), (cx + w * .32, by - h - 22)], fill=WH, width=2)
    d.line(roof[:6], fill=B, width=1)
    if lit:
        for lx in lit:
            x = cx - w / 2 + lx
            d.rectangle([x, by - h + 14, x + 14, by - 6], fill=Y)
            for gx in range(1, 3):  # changhoji lattice
                d.line([(x + gx * 14 / 3, by - h + 14), (x + gx * 14 / 3, by - 6)], fill=K)
            for gy in range(by - h + 18, by - 6, 5):
                d.line([(x, gy), (x + 14, gy)], fill=K)
            d.line([(x - 2, by - 3), (x + 16, by - 3)], fill=R, width=1)

hanok(70, 548, 110, 30, lit=[18])
hanok(300, 560, 150, 36, lit=[30, 56])
hanok(185, 586, 120, 26)
# stone wall line in the very front
d.rectangle([0, 586, W, H], fill=K)
for x in range(0, W, 11):
    d.arc([x, 584, x + 11, 594], 180, 360, fill=B)
# a person lying on the big roof, looking up
px, py = 290, 516
d.line([(px - 14, py + 1), (px + 10, py - 3)], fill=WH, width=4)   # body
d.ellipse([px + 9, py - 9, px + 17, py - 1], fill=WH)                # head
d.line([(px - 14, py + 1), (px - 26, py - 3)], fill=WH, width=3)   # legs
d.line([(px - 2, py - 1), (px + 4, py - 12)], fill=WH, width=2)    # arm pointing
d.point((px + 13, py - 6), fill=K)

d.rectangle([0, 0, W - 1, H - 1], outline=K, width=4)
save(img)
