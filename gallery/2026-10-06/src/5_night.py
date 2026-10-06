"""Night: the raft under the southern sky, the sea alight with plankton, something big glowing below.
Stipple in pure palette on black."""
import os, sys, math
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(__file__))
from lib import *

rng = np.random.default_rng(1914)
im = Image.new("RGB", (W, H), K); dr = ImageDraw.Draw(im)
HZ = 268

def stipple(density, n, cols, weights, rmax=0.0, ymin=0, ymax=H):
    """Scatter n candidate points; keep with probability density(x,y)."""
    xs = rng.uniform(0, W, n); ys = rng.uniform(ymin, ymax, n)
    keep = rng.random(n) < density[np.clip(ys.astype(int), 0, H - 1), np.clip(xs.astype(int), 0, W - 1)]
    cs = rng.choice(len(cols), n, p=weights)
    for x, y, c, k in zip(xs, ys, cs, keep):
        if k:
            if rmax and rng.random() < 0.08:
                dr.ellipse([x - 1, y - 1, x + 1, y + 1], fill=cols[c])
            else:
                dr.point((x, y), fill=cols[c])

# --- Milky Way: a diagonal band of stipple with a dark rift
u = (XX * 0.62 - YY * 0.78) + 40          # distance across the band
along = (XX * 0.78 + YY * 0.62)
mw = np.exp(-(u / 52) ** 2) * (0.55 + 0.45 * noise(31, 30, 4))
rift = np.exp(-((u - 8 + 14 * np.sin(along / 60)) / 9) ** 2) * (along > 140) * (along < 380)
dens = np.clip(mw - rift * 0.9, 0, 1) * (YY < HZ - 4)
stipple(dens * 0.55, 60000, [WH, B, Y], [0.6, 0.3, 0.1], ymax=HZ)
# field stars
for k in range(260):
    x, y = rng.uniform(0, W), rng.uniform(0, HZ - 6)
    dr.point((x, y), fill=WH if rng.random() < 0.8 else Y)
def star(x, y, r, col=WH):
    dr.ellipse([x - r, y - r, x + r, y + r], fill=col)
    if r >= 2:
        dr.line([(x - r * 3, y), (x + r * 3, y)], fill=col); dr.line([(x, y - r * 3), (x, y + r * 3)], fill=col)
# Crux, and the two pointers
crux = [(282, 92, 3), (296, 150, 3), (262, 128, 2.5), (318, 118, 2), (300, 132, 1)]
for (x, y, r) in crux: star(x, y, r)
star(372, 204, 3.5, Y); star(352, 178, 3)           # α and β Centauri
dr.text((292, 166), "Crux", fill=B, font=font(11, "serifi"))
# the Magellanic Clouds, faint smudges low in the south-west
for (cx, cy, rx, ry) in [(70, 208, 22, 12), (108, 236, 12, 7)]:
    m = np.exp(-(((XX - cx) / rx) ** 2 + ((YY - cy) / ry) ** 2)) * 0.6
    stipple(m, 3000, [WH, B], [0.5, 0.5], ymin=cy - 30, ymax=cy + 30)
# a meteor
dr.line([(36, 40), (96, 76)], fill=WH)
dr.line([(80, 66), (96, 76)], fill=Y, width=2)

# --- sea: black, a faint horizon line, plankton everywhere it is disturbed
dr.line([(0, HZ), (W, HZ)], fill=B)
wake = np.zeros((H, W), np.float32)
# raft geometry
cx, wl = 200, 392
# wake streaming behind (to the right and toward the viewer), bow-wave around the logs
wx = XX - cx
wake += np.exp(-((YY - wl - 6 - 0.15 * np.clip(wx, 0, None)) / (6 + 0.18 * np.clip(wx + 100, 0, None))) ** 2) * (wx > -110) * np.clip(1 - wx / 300, 0, 1)
wake += np.exp(-((YY - wl - 2) / 4) ** 2) * (np.abs(wx) < 125)
# random swirls (eddies of light)
for k in range(9):
    ex, ey = rng.uniform(20, 380), rng.uniform(HZ + 30, 590)
    r = np.hypot(XX - ex, YY - ey)
    th = np.arctan2(YY - ey, XX - ex)
    wake += 0.5 * np.exp(-((r - 6 - 3 * ((th + r / 6) % (2 * math.pi))) / 2.0) ** 2) * (r < 26)
# the big glowing thing below: an elongated body with a bright rim and two eyes
gx, gy = 150, 520
ge = ((XX - gx) / 120) ** 2 + ((YY - gy) / 30) ** 2
body = np.exp(-((np.sqrt(ge) - 1) / 0.08) ** 2) * 0.9 + (ge < 1) * 0.12
wake += body * (YY > HZ + 150)
sea_d = np.clip(wake, 0, 1) * (YY > HZ + 2)
stipple(sea_d * 0.85, 90000, [G, B, WH], [0.5, 0.3, 0.2], rmax=1, ymin=HZ)
# general scintillation: sparse sparks across the whole sea
for k in range(700):
    x, y = rng.uniform(0, W), HZ + 4 + (rng.random() ** 1.5) * (H - HZ - 4)
    dr.point((x, y), fill=[G, B, WH][rng.integers(3)])
# its eyes
for ex in (40, 58):
    dr.ellipse([ex - 6, 512 - 5, ex + 6, 512 + 5], fill=G); dr.ellipse([ex - 2, 510, ex + 2, 514], fill=K)

# --- the raft: black silhouette over the bright wake, Milky Way behind the sail
deck = wl - 12
dr.polygon([(cx - 118, wl - 6), (cx + 110, wl - 10), (cx + 116, wl + 4), (cx - 112, wl + 10)], fill=K)
dr.line([(cx - 118, wl - 6), (cx + 110, wl - 10)], fill=B)
for k in range(9):  # log ends at the bow, catching plankton light
    dr.arc([cx - 124, wl - 6 + k * 2, cx - 112, wl + 4 + k * 2], 90, 270, fill=G)
# cabin with the lantern-lit doorway
c0, c1 = cx + 16, cx + 84
dr.rectangle([c0, deck - 40, c1, deck], fill=K)
dr.polygon([(c0 - 8, deck - 40), (c1 + 8, deck - 40), (c1 - 4, deck - 60), (c0 + 4, deck - 60)], fill=K)
dr.line([(c0 - 8, deck - 40), (c0 + 4, deck - 60), (c1 - 4, deck - 60), (c1 + 8, deck - 40)], fill=B)
door = [c0 + 26, deck - 28, c0 + 42, deck]
# lantern glow: concentric screened rings of yellow on black
gl = np.hypot(XX - (c0 + 34), (YY - (deck - 12)) * 1.2)
arr = np.asarray(im).copy()
ring = (gl < 46) & (gl > 9) & (YY < deck + 8) & (YY > deck - 70) & (XX > c0 - 30) & (XX < c1 + 40)
on = (np.clip(1 - gl / 46, 0, 1) ** 1.3 * 1.1) > T8
outside = ring & on & ~((XX >= c0) & (XX <= c1) & (YY >= deck - 40) & (YY <= deck))
arr[outside] = Y
im = Image.fromarray(arr); dr = ImageDraw.Draw(im)
dr.rectangle(door, fill=Y)
dr.ellipse([c0 + 31, deck - 22, c0 + 37, deck - 14], fill=WH)
# light falling on the deck from the door
dr.polygon([(c0 + 26, deck), (c0 + 42, deck), (c0 + 60, deck + 6), (c0 + 8, deck + 6)], fill=Y)
# a figure sitting in the doorway, black against the lamp
dr.ellipse([c0 + 28, deck - 26, c0 + 35, deck - 19], fill=K)
dr.polygon([(c0 + 27, deck - 18), (c0 + 37, deck - 18), (c0 + 39, deck - 4), (c0 + 26, deck - 4)], fill=K)
# A-frame mast, yard, sail: the sail is the darkest blue, the god's face barely red
top = (cx - 30, 130)
dr.line([(cx - 70, deck + 2), top], fill=K, width=5); dr.line([(cx + 8, deck + 2), top], fill=K, width=5)
sail = [(cx - 106, 152), (cx + 42, 146), (cx + 48, deck - 52), (cx - 110, deck - 46)]
arr = np.asarray(im).copy()
m = Image.new("1", (W, H), 0); ImageDraw.Draw(m).polygon(sail, fill=1); m = np.asarray(m)
arr[m] = K
seam = m & (((XX - cx + 106) % 22) < 1) & (np.sin(YY * 0.9) > 0.2)
arr[seam] = B
im = Image.fromarray(arr); dr = ImageDraw.Draw(im)
dr.polygon(sail, outline=B)
fx, fy = cx - 32, 228
for k in range(18):
    a = math.pi + k * math.pi / 17
    dr.line([(fx + 24 * math.cos(a), fy - 4 + 24 * math.sin(a)), (fx + (34 + (k % 2) * 5) * math.cos(a), fy - 4 + (34 + (k % 2) * 5) * math.sin(a))], fill=R, width=2)
dr.ellipse([fx - 22, fy - 26, fx + 22, fy + 18], outline=R, width=2)
for ex in (-9, 9): dr.ellipse([fx + ex - 3, fy - 4, fx + ex + 3, fy + 1], fill=R)
for k in range(-3, 4): dr.line([(fx + k * 4, fy + 16), (fx + k * 5, fy + 32 - abs(k) * 2)], fill=R, width=2)
dr.line([(cx - 116, 154), (cx + 54, 144)], fill=K, width=4)
dr.line([(cx - 116, 154), (cx + 54, 144)], fill=B, width=1)
for p in [(cx - 118, deck), (cx + 108, deck - 4)]: dr.line([top, p], fill=B)
# steering oar trailing a streak of light
dr.line([(cx + 100, deck - 26), (cx + 160, wl + 40)], fill=K, width=4)
dr.line([(cx + 140, wl + 16), (cx + 172, wl + 56)], fill=G, width=1)
# a flying fish, glowing, mid-leap over the wake
fxp, fyp = 300, 340
dr.polygon([(fxp - 12, fyp), (fxp + 10, fyp - 2), (fxp + 14, fyp), (fxp + 10, fyp + 2)], fill=WH)
dr.polygon([(fxp, fyp - 1), (fxp - 10, fyp - 12), (fxp - 2, fyp - 13), (fxp + 6, fyp - 1)], fill=B)
dr.polygon([(fxp - 12, fyp), (fxp - 18, fyp - 4), (fxp - 16, fyp), (fxp - 19, fyp + 4)], fill=WH)
for k in range(10): dr.point((fxp + 16 + k * 3, fyp + 8 + k * k * 0.4), fill=G)
im.save(os.environ.get("OUT_RAW", "night.png"))
