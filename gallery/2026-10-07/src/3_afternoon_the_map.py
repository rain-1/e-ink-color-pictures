"""3. Afternoon — The Map. A geologic map of the far side, USGS I-map manner."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from common import *

ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
xi, yi = xs.astype(int), ys.astype(int)
CX, CY, RR = 200, 232, 176
LAT0, LON0 = 5, 165
m = moon(LAT0, LON0, CX, CY, RR, n=2600)
mask, unit, h = m["mask"], m["unit"], m["h"]

# patterned unit fills
def fill(code):
    if code == "pIt":   # terra: yellow, red stipple
        return np.where(((xi % 6 == 0) & (yi % 6 == 0)) | ((xi % 6 == 3) & (yi % 6 == 3)), 2, 3)
    if code == "SPA":   # South Pole-Aitken floor: blue, white dots
        return np.where((xi % 4 == 0) & (yi % 4 == 0), 1, 4)
    if code == "pNc":   # pre-Nectarian crater: yellow, black hatch
        return np.where((xi - yi) % 5 == 0, 0, 3)
    if code == "Nb":    # basin material: green, yellow hatch
        return np.where((xi + yi) % 6 == 0, 3, 5)
    if code == "Nc":    # Nectarian crater: green, black cross-hatch
        return np.where(((xi + yi) % 5 == 0) | ((xi - yi) % 5 == 0), 0, 5)
    if code == "Ic":    # Imbrian crater: white, green hatch
        return np.where((xi - yi) % 4 == 0, 5, 1)
    if code == "Im":    # mare basalt: red
        return np.where((xi % 5 == 0) & (yi % 5 == 2), 0, 2)
    if code == "Ec":    # Eratosthenian crater: blue
        return np.full(xi.shape, 4)
    if code == "Cc":    # Copernican crater: white, red dots
        return np.where((xi % 3 == 0) & (yi % 3 == 0), 2, 1)
INKS = np.array([INK[k] for k in "KWRYBG"], np.uint8)
idx = np.zeros((H, W), int)
for code in UNITS:
    sel = mask & (unit == U[code])
    idx[sel] = fill(code)[sel]
img = INKS[idx]
# rays over everything young: white
ry = mask & (m["ray"] > 0.35 + bayer() * 0.4)
img[ry] = INK["W"]
# relief: hillshade from the NW, laid on as black screen in the shadows
gy_, gx_ = np.gradient(h)
shade = -(gx_ * -0.7 + gy_ * -0.7)
sh = mask & (shade < -0.25) & (bayer() < np.clip(-shade * 0.5, 0, 0.7))
img[sh] = INK["K"]
lit = mask & (shade > 0.5) & (bayer() < 0.35)
img[lit & (unit != U["Im"])] = INK["W"]
# unit contacts: black where the unit changes
edge = np.zeros_like(mask)
edge[:-1] |= unit[:-1] != unit[1:]
edge[:, :-1] |= unit[:, :-1] != unit[:, 1:]
img[edge & mask] = INK["K"]
# sea of paper around the disc
outside = ~mask
paper = np.full((H, W, 3), 255, np.uint8)
img[outside] = paper[outside]

L = Layer()
# graticule every 30 degrees
V = sph(LAT0, LON0); E = np.array([-math.sin(math.radians(LON0)), math.cos(math.radians(LON0)), 0]); N = np.cross(V, E)
def proj(la, lo):
    p = sph(la, lo)
    return CX + RR * p @ E, CY - RR * p @ N, p @ V
for lo in range(-180, 180, 30):
    seg = []
    for la in np.linspace(-90, 90, 120):
        x, y, z = proj(la, lo)
        if z > 0: seg.append((x, y))
        elif len(seg) > 1: L.line(seg, "K", 0.5); seg = []
    if len(seg) > 1:
        for i in range(0, len(seg) - 1, 3): L.line(seg[i:i + 2], "K", 0.7)
for la in range(-60, 90, 30):
    seg = []
    for lo in np.linspace(-180, 180, 240):
        x, y, z = proj(la, lo)
        if z > 0: seg.append((x, y))
    for i in range(0, len(seg) - 1, 3): L.line(seg[i:i + 2], "K", 0.7)
L.ellipse(CX, CY, RR, RR, None, "K", 1.8)
L.ellipse(CX, CY, RR + 4, RR + 4, None, "K", 0.6)
for la in (-60, -30, 0, 30, 60):
    x, y, z = proj(la, LON0 - 90 + 3)
    L.text((CX - RR - 6, y), f"{abs(la)}°{'N' if la > 0 else 'S' if la < 0 else ''}", "K", 8, "monob", "rm")
for lo in (120, 150, 180, 210):
    x, y, z = proj(-LAT0 + 0, lo)
    lab = f"{lo if lo <= 180 else 360 - lo}°{'E' if lo < 180 else 'W' if lo > 180 else ''}"
    x2, y2, _ = proj(88 - LAT0, lo)
    L.text((x, CY + RR + 13), lab, "K", 8, "monob", "mm")
# names, with leaders, in the cartographer's italic-free caps
names = [("MOSCOVIENSE", 27, 148, -1), ("TSIOLKOVSKIY", -21, 129, -1), ("KOROLEV", -4, -157, 1),
         ("APOLLO", -36, -151, 1), ("HERTZSPRUNG", 2, -129, -1), ("MENDELEEV", 6, 141, -1),
         ("INGENII", -34, 163, -1), ("GAGARIN", -20, 149, -1), ("JACKSON", 22, -163, 1),
         ("DAEDALUS", -6, 180, 1)]
for nm, la, lo, side in names:
    x, y, z = proj(la, lo)
    if z <= 0.1: continue
    L.ellipse(x, y, 1.6, 1.6, "K")
    L.text((x + 4 * side, y - 1), nm, "K", 8, "sansb", "lm" if side > 0 else "rm")
img = L.onto(img)
# knock the name labels out on a white halo: redraw text bolder in white beneath? Simple: second pass on top
L2 = Layer()
for nm, la, lo, side in names:
    x, y, z = proj(la, lo)
    if z <= 0.1: continue
    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1), (1, 1), (-1, -1), (1, -1), (-1, 1)):
        L2.text((x + 4 * side + dx * 0.9, y - 1 + dy * 0.9), nm, "W", 8, "sansb", "lm" if side > 0 else "rm")
    L2.text((x + 4 * side, y - 1), nm, "K", 8, "sansb", "lm" if side > 0 else "rm")
# title cartouche
L2.rect(6, 6, 394, 40, "W", "K", 1.2)
L2.rect(9, 9, 391, 37, None, "K", 0.5)
L2.text((200, 16), "GEOLOGIC MAP OF THE FAR SIDE OF THE MOON", "K", 10, "sansb", "mm")
L2.text((200, 30), "after the first photographs, Luna 3, 7 October 1959", "R", 9, "sans", "mm")
# legend
units = [("Cc", "Copernican crater"), ("Ec", "Eratosthenian crater"), ("Im", "Mare basalt"),
         ("Ic", "Imbrian crater"), ("Nc", "Nectarian crater"), ("Nb", "Basin material"),
         ("pNc", "Pre-Nectarian crater"), ("SPA", "S. Pole–Aitken floor"), ("pIt", "Terra, undivided")]
L2.rect(6, 432, 394, 594, "W", "K", 1.2)
L2.text((14, 444), "EXPLANATION", "K", 9, "sansb", "lm")
L2.line([(14, 451), (386, 451)], "K", 0.5)
for i, (code, label) in enumerate(units):
    col, row = divmod(i, 5)
    x = 14 + col * 192; y = 458 + row * 24
    L2.rect(x, y, x + 30, y + 17, None, "K", 1)
    L2.text((x + 36, y + 2), code, "K", 9, "monob")
    L2.text((x + 36, y + 11), label, "K", 9, "sans")
# age arrow
L2.line([(208 + 0, 556), (380, 556)], "K", 0.8)
L2.poly([(380, 556), (374, 553), (374, 559)], "K")
L2.text((208, 566), "older", "K", 8, "serif", "lm"); L2.text((380, 566), "younger", "K", 8, "serif", "rm")
L2.line([(208, 580), (308, 580)], "K", 2.4); L2.line([(208, 580), (258, 580)], "W", 1.2)
for x in (208, 258, 308): L2.line([(x, 576), (x, 584)], "K", 0.8)
L2.text((314, 580), "0  500  1000 km", "K", 8, "monob", "lm")
img = L2.onto(img)
# legend swatches: fill each box with its pattern
for i, (code, label) in enumerate(units):
    col, row = divmod(i, 5)
    x = 14 + col * 192; y = 458 + row * 24
    sl = (slice(y + 2, y + 16), slice(x + 2, x + 29))
    img[sl] = INKS[fill(code)[sl]]
save(img)
