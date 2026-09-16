# Night — the circle motif taken to its quietest form: a loose constellation of
# discs on black, echoing both Kandinsky's circles and the equinox six days off
# (day and night nearing balance) — two larger anchor circles hold the sheet like
# a pair of scales. Palette: black, green, white. Mostly dark.
import os
from PIL import Image, ImageDraw
import numpy as np
W, H = 400, 600
BLK, GRN, WHT = (0, 0, 0), (0x1E, 0x9B, 0x3C), (255, 255, 255)
rng = np.random.default_rng(2606)
im = Image.new("RGB", (W, H), BLK)
d = ImageDraw.Draw(im)

# the two anchor circles: balance of day and night, upper and lower thirds
anchors = [(150, 170, 58, GRN), (260, 430, 58, GRN)]
for x, y, r, col in anchors:
    d.ellipse((x - r, y - r, x + r, y + r), fill=col)
    d.ellipse((x - 20, y - 20, x + 20, y + 20), fill=BLK)

# a thin white line balancing the two, like a fulcrum
d.line((anchors[0][0], anchors[0][1], anchors[1][0], anchors[1][1]), fill=WHT, width=1)
mx, my = (anchors[0][0] + anchors[1][0]) / 2, (anchors[0][1] + anchors[1][1]) / 2
d.line((mx - 14, my - 14, mx + 14, my + 14), fill=WHT, width=2)
d.line((mx - 14, my + 14, mx + 14, my - 14), fill=WHT, width=2)

# small green and white pinpricks scattered sparsely — stars, or distant circles
for _ in range(26):
    x, y = rng.integers(0, W), rng.integers(0, H)
    r = rng.integers(2, 5)
    col = WHT if rng.random() < 0.6 else GRN
    d.ellipse((x - r, y - r, x + r, y + r), fill=col)

# a few larger, faint rings drifting in from the edges — distant circles, unresolved
for _ in range(3):
    x = rng.choice([-20, W + 20])
    y = rng.integers(80, H - 80)
    r = rng.integers(50, 90)
    d.ellipse((x - r, y - r, x + r, y + r), outline=GRN, width=3)

im.save(os.environ["OUT_RAW"])
