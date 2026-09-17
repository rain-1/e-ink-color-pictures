# Morning — "Rollout, Palmdale" (6 September... 17 September 1976).
# Palette: red, white, black. Fifty years ago today the prototype orbiter Enterprise was
# towed out of Rockwell's Palmdale plant for the first time, into a crowd and a brass band,
# named after the Star Trek ship on the strength of a write-in campaign to the White House.
# Flat poster / silkscreen: white hangar, black doorway, bunting, a spotlight on the nose.
# The spotlight is the day's motif — one red light, carried through all five pieces.
import os, math
import numpy as np
from PIL import Image, ImageDraw

W, H = 400, 600
RED, WHT, BLK = (0xE0, 0x1B, 0x24), (0xFF, 0xFF, 0xFF), (0, 0, 0)
rng = np.random.default_rng(19760917)

im = Image.new("RGB", (W, H), WHT)
d = ImageDraw.Draw(im)

# hangar facade: horizontal ribbing to suggest corrugated metal, upper 1/3
d.rectangle((0, 0, W, 210), fill=WHT)
for y in range(0, 210, 14):
    d.line((0, y, W, y), fill=BLK, width=1)

# bunting: a string of small red pennants along the eaves
py = 24
n = 17
xs = np.linspace(10, W - 10, n)
for i in range(n - 1):
    x0, x1 = xs[i], xs[i + 1]
    sag = 10
    mx = (x0 + x1) / 2
    d.line((x0, py, mx, py + sag), fill=BLK, width=2)
    d.line((mx, py + sag, x1, py), fill=BLK, width=2)
    d.polygon([(mx - 7, py + sag - 2), (mx + 7, py + sag - 2), (mx, py + sag + 16)], fill=RED)

# the open hangar doorway: a big black rectangle, slightly trapezoidal for depth
door_top, door_bot = 60, 480
d.polygon([(70, door_top), (330, door_top), (355, door_bot), (45, door_bot)], fill=BLK)

# spotlight: a single red wedge cut into the dark doorway from the upper-left, aimed at
# where the nose will be — the day's motif light. Drawn now so the orbiter (below) sits on
# top of it, leaving only a sliver showing above the fuselage.
CX = 200
nose_y = 250
sx, sy = 12, 6
tip = (CX, nose_y - 88)
spread = 0.075
ang = math.atan2(tip[1] - sy, tip[0] - sx)
L = 520
p1 = (sx + L * math.cos(ang - spread), sy + L * math.sin(ang - spread))
p2 = (sx + L * math.cos(ang + spread), sy + L * math.sin(ang + spread))
d.polygon([(sx, sy), p1, p2], fill=RED)

# orbiter, nose-first, just clear of the doorway: white fuselage, black nose cone and windows,
# a delta wingtip emerging low on each side, still mostly swallowed by the dark of the hangar
d.polygon([(CX - 8, nose_y - 60), (CX + 8, nose_y - 60), (CX + 34, nose_y + 40),
           (CX - 34, nose_y + 40)], fill=WHT)                       # forward fuselage, tapering to nose
d.polygon([(CX - 8, nose_y - 60), (CX + 8, nose_y - 60), (CX, nose_y - 92)], fill=BLK)  # nose cone
for i in range(4):                                                   # cockpit windows
    wx = CX - 15 + i * 10
    d.polygon([(wx, nose_y - 48), (wx + 7, nose_y - 48), (wx + 5, nose_y - 38), (wx - 2, nose_y - 38)], fill=BLK)
d.polygon([(CX - 60, nose_y + 30), (CX - 34, nose_y + 10), (CX - 34, nose_y + 40), (CX - 70, nose_y + 55)], fill=WHT)
d.polygon([(CX + 60, nose_y + 30), (CX + 34, nose_y + 10), (CX + 34, nose_y + 40), (CX + 70, nose_y + 55)], fill=WHT)
d.line((CX - 34, nose_y + 40, CX + 34, nose_y + 40), fill=BLK, width=2)   # where the dark swallows the rest
# a black underline stripe and lettering, like the real "UNITED STATES" wordmark
d.rectangle((CX - 30, nose_y - 4, CX + 30, nose_y + 2), fill=BLK)
d.text((CX - 27, nose_y - 3), "ENTERPRISE", fill=WHT)

# the glint where the light lands, on the very tip of the nose
d.ellipse((tip[0] - 4, tip[1] - 4, tip[0] + 4, tip[1] + 4), fill=RED)

# the crowd: a foreground row of small black silhouettes, some with white "camera flash" dots gone —
# keep it simple, heads and shoulders, uneven heights, facing the doorway
gy = door_bot
d.rectangle((0, gy, W, H), fill=WHT)
xs = np.arange(6, W - 6, 8) + rng.uniform(-2, 2, size=len(np.arange(6, W - 6, 8)))
for x in xs:
    h = rng.uniform(20, 34)
    hw = rng.uniform(5, 8)
    base = H - 8
    d.ellipse((x - hw * 0.55, base - h, x + hw * 0.55, base - h + hw * 1.1), fill=BLK)
    d.polygon([(x - hw, base - h + hw), (x + hw, base - h + hw), (x + hw * 0.8, base), (x - hw * 0.8, base)], fill=BLK)

d.text((14, H - 20), "PALMDALE, CALIFORNIA · 17 SEPTEMBER 1976", fill=BLK)

im.save(os.environ["OUT_RAW"])
