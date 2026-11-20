"""V. Nor does lightning travel in a straight line — a midpoint-displaced, branching
stroke over a harbour town: lit cloud bellies, rain, windows, a lighthouse, the strike
doubled in the water. Black in charge; blue, white and a little yellow for light."""
import numpy as np
from common import *

rng = np.random.default_rng(2010)
CAP = 34
PIC_H = H - CAP
HZ = 462
p = Plate(K)

# --- the stroke -----------------------------------------------------------------------
segs = []                                      # (x0, y0, x1, y1, width)
def displace(a, b, rough, depth):
    if depth == 0:
        return [a, b]
    mid = (a + b) / 2
    n = np.array([-(b - a)[1], (b - a)[0]])
    mid = mid + n * rng.normal(0, rough)
    return displace(a, mid, rough * 0.92, depth - 1)[:-1] + displace(mid, b, rough * 0.92, depth - 1)
def bolt(a, b, width, depth):
    pts = displace(np.array(a, float), np.array(b, float), 0.20, 6)
    for q0, q1 in zip(pts, pts[1:]):
        segs.append((*q0, *q1, width))
    if depth == 0:
        return
    n = len(pts)
    for _ in range(int(rng.integers(3, 6))):
        i = int(rng.integers(n // 8, n * 7 // 8))
        main_dir = np.array(b, float) - np.array(a, float)
        L = np.linalg.norm(main_dir) * rng.uniform(0.3, 0.6)
        ang = np.arctan2(main_dir[1], main_dir[0]) + rng.choice([-1, 1]) * rng.uniform(0.35, 0.9)
        end = pts[i] + L * np.array([np.cos(ang), np.sin(ang)])
        if end[1] < HZ - 6:
            bolt(pts[i], end, max(1, width - 1), depth - 1)
STRIKE = (292, HZ)
bolt((205, 70), STRIKE, 3, 3)
main_n = 64
bm = Plate(0); thin = Plate(0)
with bm.draw() as d:
    for x0, y0, x1, y1, w in segs:
        d.line([(x0, y0), (x1, y1)], fill=1, width=w)
with thin.draw() as d:
    for x0, y0, x1, y1, w in segs[:main_n]:
        d.line([(x0, y0), (x1, y1)], fill=1, width=3)
stroke = bm.a == 1; core = thin.a == 1
glow_w = blur(core.astype(np.float32), 9) * 5.0 + blur(stroke.astype(np.float32), 4) * 1.6
glow_b = blur(stroke.astype(np.float32), 26) * 13.0 + blur(core.astype(np.float32), 60) * 22.0

# --- clouds, lit from inside ----------------------------------------------------------------
c1 = fbm(3, scale=95, octaves=6, gain=0.55, stretch=(0.6, 1.4))
c2 = fbm(4, scale=30, octaves=4)
deck = np.clip((300 - YY) / 150.0, 0, 1)
dens = np.clip((c1 - 0.38) * 2.2, 0, 1) * deck ** 0.6
dens = np.clip(dens + (c2 - 0.5) * 0.3 * (dens > 0.05), 0, 1)
sky = YY < HZ
p.put(sky & screen(np.clip(dens * (0.16 + glow_b * 0.75), 0, 0.92)), B)
p.put(sky & screen(np.clip(dens * glow_w * 1.1 - 0.05, 0, 0.9)), WH)
# billow edges: iso-lines in blue, like the morning's engraving, but nearly swallowed
lev = np.floor(dens / 0.09)
iso = np.zeros((H, W), bool)
iso[:, :-1] |= lev[:, :-1] != lev[:, 1:]; iso[:-1, :] |= lev[:-1, :] != lev[1:, :]
p.put(sky & iso & (dens > 0.08) & (glow_b > 0.12), B)
p.put(sky & iso & (dens > 0.08) & (glow_w > 0.45), WH)
# open air under the deck glows a little near the channel
p.put(sky & (dens < 0.05) & screen(np.clip(glow_b * 0.42 - 0.05, 0, 0.7)), B)
p.put(sky & (dens < 0.05) & screen(np.clip(glow_w * 0.5 - 0.12, 0, 0.8)), WH)
# a second discharge crawling inside the cloud
segs2 = segs; segs = []
bolt((30, 120), (190, 82), 1, 2); bolt((230, 60), (392, 132), 1, 2)
with p.draw() as d:
    for x0, y0, x1, y1, w in segs:
        d.line([(x0, y0), (x1, y1)], fill=B, width=1)
segs = segs2

# --- rain ------------------------------------------------------------------------------------
with p.draw() as d:
    for _ in range(1500):
        x, y = rng.integers(-20, W), rng.integers(150, PIC_H)
        ln = rng.integers(5, 12)
        gl = glow_b[min(y, H - 1), max(0, min(x, W - 1))]
        if rng.random() < 0.22 + gl:
            d.line([(x, y), (x + ln * 0.32, y + ln)], fill=WH if gl > 0.55 and rng.random() < 0.5 else B)

# --- sea ---------------------------------------------------------------------------------------
sea = (YY >= HZ) & (YY < PIC_H)
p.put(sea, K)
wav = fbm(8, scale=12, octaves=3, stretch=(0.22, 3.0))
depth = (YY - HZ) / float(PIC_H - HZ)
p.put(sea & (wav > 0.60 - 0.10 * depth) & (YY % 2 == 0), B)
refl = np.exp(-((XX - STRIKE[0]) / (7.0 + 34 * depth)) ** 2)
p.put(sea & (wav > 0.50) & screen(refl * 0.95) & (YY % 2 == 0), WH)
p.put(sea & (wav > 0.44) & screen(refl * 0.6) & (YY % 2 == 1), Y)
p.put(sea & (np.abs(XX - STRIKE[0]) < 3) & (YY < HZ + 5), WH)

# --- the stroke itself, over everything in the sky ---------------------------------------------
p.put(grow(stroke, 1) & sky & ~stroke, B)
p.put(grow(core, 1) & sky, Y)
p.put(stroke & sky, WH)
with p.draw() as d:                                # the splash where it lands
    for k in range(13):
        a = np.pi * (k + 0.5) / 13
        r0, r1 = 5, 12 + (k * 7) % 9
        d.line([(STRIKE[0] + r0 * np.cos(a), HZ - r0 * np.sin(a)), (STRIKE[0] + r1 * np.cos(a), HZ - r1 * np.sin(a))], fill=Y if k % 2 else WH)

# --- the hill and the town --------------------------------------------------------------------
x = np.arange(W)
prof = HZ - 150 * np.clip(1 - x / 250.0, 0, 1) ** 1.25 - 8 * fbm(6, scale=40, octaves=3, shape=(1, W))[0] * (x < 250)
hill = (YY >= prof[None, :]) & (YY < PIC_H) & (XX < 262)
p.put(hill, K)
rim = hill & ~np.roll(hill, 1, axis=0)
p.put(rim, B)
with p.draw() as d:
    f8 = font(8)
    # trees on the skyline
    for tx in range(4, 236, 7):
        ty = prof[tx]; r = rng.integers(3, 7)
        d.ellipse([tx - r, ty - 2 * r, tx + r, ty + 1], fill=K, outline=B)
        d.arc([tx - r, ty - 2 * r, tx + r, ty + 1], 270, 40, fill=WH)
    houses = []
    for _ in range(150):
        hx = int(rng.integers(-6, 236)); base = int(rng.integers(int(prof[max(0, hx)]) + 16, PIC_H - 34))
        if base < prof[min(W - 1, hx + 20)] + 14:
            continue
        houses.append((base, hx))
    for base, hx in sorted(houses):
        w = int(rng.integers(13, 24)); h = int(rng.integers(12, 24)); top = base - h
        d.rectangle([hx, top, hx + w, base], fill=K, outline=None)
        # the wall that faces the flash
        d.rectangle([hx + w - 3, top, hx + w, base], fill=B)
        d.line([(hx + w, top), (hx + w, base)], fill=WH)
        kind = rng.integers(3)
        if kind < 2:
            d.polygon([(hx - 2, top), (hx + w / 2, top - h * 0.45), (hx + w + 2, top)], fill=K)
            d.line([(hx + w / 2, top - h * 0.45), (hx + w + 2, top)], fill=WH)
            d.line([(hx - 2, top), (hx + w / 2, top - h * 0.45)], fill=B)
            if rng.random() < 0.5:
                d.rectangle([hx + 2, top - h * 0.45, hx + 4, top - 3], fill=K, outline=B)
        else:
            d.line([(hx, top), (hx + w, top)], fill=WH)
            d.line([(hx, top), (hx, top + 3)], fill=B)
        for wy in range(top + 3, base - 3, 6):
            for wx in range(hx + 2, hx + w - 5, 5):
                r_ = rng.random()
                if r_ < 0.42:
                    d.rectangle([wx, wy, wx + 2, wy + 3], fill=Y)
                elif r_ < 0.47:
                    d.rectangle([wx, wy, wx + 2, wy + 3], fill=R)
                elif r_ < 0.6:
                    d.rectangle([wx, wy, wx + 2, wy + 3], outline=B)
    # church on the shoulder of the hill
    cx_, cb = 150, int(prof[150]) + 4
    d.rectangle([cx_, cb - 44, cx_ + 12, cb], fill=K); d.line([(cx_ + 12, cb - 44), (cx_ + 12, cb)], fill=WH)
    d.polygon([(cx_ - 1, cb - 44), (cx_ + 6, cb - 70), (cx_ + 13, cb - 44)], fill=K)
    d.line([(cx_ + 6, cb - 70), (cx_ + 13, cb - 44)], fill=WH); d.line([(cx_ + 6, cb - 70), (cx_ - 1, cb - 44)], fill=B)
    d.line([(cx_ + 6, cb - 70), (cx_ + 6, cb - 78)], fill=WH); d.line([(cx_ + 3, cb - 75), (cx_ + 9, cb - 75)], fill=WH)
    d.ellipse([cx_ + 3, cb - 38, cx_ + 9, cb - 32], fill=Y)
    d.rectangle([cx_ + 12, cb - 20, cx_ + 40, cb], fill=K); d.line([(cx_ + 12, cb - 20), (cx_ + 40, cb - 20)], fill=WH)
    for k in range(4):
        d.rectangle([cx_ + 16 + k * 6, cb - 14, cx_ + 18 + k * 6, cb - 6], fill=[R, Y, B, Y][k])

    # quay, lamps, boats
    qy = PIC_H - 30
    d.rectangle([0, qy, 250, qy + 4], fill=K); d.line([(0, qy), (250, qy)], fill=WH)
    for lx in range(14, 250, 34):
        d.line([(lx, qy), (lx, qy - 14)], fill=B); d.rectangle([lx - 1, qy - 17, lx + 1, qy - 14], fill=Y)
        for k in range(1, 6):
            d.line([(lx - 2 + k % 2, qy + 5 + k * 3), (lx + 2 - k % 2, qy + 5 + k * 3)], fill=Y)
    for bx, by, s in ((276, PIC_H - 20, 1.0), (322, PIC_H - 34, 0.8), (240, PIC_H - 12, 1.1), (366, PIC_H - 16, 0.9)):
        d.polygon([(bx - 15 * s, by), (bx + 17 * s, by), (bx + 12 * s, by + 6 * s), (bx - 11 * s, by + 6 * s)], fill=K, outline=WH)
        d.line([(bx, by), (bx, by - 34 * s)], fill=WH)
        d.line([(bx, by - 34 * s), (bx - 13 * s, by)], fill=B); d.line([(bx, by - 34 * s), (bx + 15 * s, by)], fill=B)
        d.line([(bx, by - 26 * s), (bx + 9 * s, by - 24 * s)], fill=B)
        d.rectangle([bx - 1, by - 36 * s - 2, bx + 1, by - 36 * s], fill=R)
        d.rectangle([bx - 6 * s, by - 5 * s, bx + 3 * s, by], fill=K, outline=B); d.point((bx - 2 * s, by - 3 * s), fill=Y)

    # lighthouse on the mole, its beam going the other way
    lx, ly = 352, HZ
    d.polygon([(300, HZ + 3), (400, HZ + 3), (400, HZ - 3), (318, HZ - 3)], fill=K)
    d.line([(318, HZ - 3), (400, HZ - 3)], fill=B)
    d.polygon([(lx - 7, ly - 3), (lx + 7, ly - 3), (lx + 4, ly - 52), (lx - 4, ly - 52)], fill=WH)
    for k in range(3):
        d.polygon([(lx - 6 + k * 0.4, ly - 12 - k * 15), (lx + 6 - k * 0.4, ly - 12 - k * 15), (lx + 5.4 - k * 0.4, ly - 20 - k * 15), (lx - 5.4 + k * 0.4, ly - 20 - k * 15)], fill=R)
    d.polygon([(lx - 7, ly - 3), (lx - 1, ly - 3), (lx - 1, ly - 52), (lx - 4, ly - 52)], fill=K)   # its dark side
    d.rectangle([lx - 6, ly - 60, lx + 6, ly - 52], fill=Y, outline=WH)
    d.polygon([(lx - 6, ly - 60), (lx, ly - 68), (lx + 6, ly - 60)], fill=K, outline=WH)
beam = (XX > 358) & (np.abs((YY - (HZ - 56)) - (XX - 358) * 0.10) < (XX - 358) * 0.16 + 2) & (YY < HZ - 8)
p.put(beam & screen(0.5 + 0 * depth), Y)

# --- caption -------------------------------------------------------------------------------------
p.caption("V", "NOR DOES LIGHTNING TRAVEL\nIN A STRAIGHT LINE", fg=WH, bg=K, height=CAP, size=11)
p.save()
