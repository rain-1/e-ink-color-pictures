# Night — "Afterglow". Mostly black; a Bayer-screened band of green low on the horizon,
# the last of the light, and one green star already out. Palette: black, green only.
import os
import numpy as np
from PIL import Image

W, H = 400, 600
BLACK = np.array([0x00, 0x00, 0x00], dtype=np.uint8)
GREEN = np.array([0x1E, 0x9B, 0x3C], dtype=np.uint8)

img = np.zeros((H, W, 3), dtype=np.uint8)
img[:, :] = BLACK

# Bayer 8x8 ordered-dither matrix, normalised to 0..1
BAYER8 = np.array([
    [ 0,32, 8,40, 2,34,10,42],[48,16,56,24,50,18,58,26],
    [12,44, 4,36,14,46, 6,38],[60,28,52,20,62,30,54,22],
    [ 3,35,11,43, 1,33, 9,41],[51,19,59,27,49,17,57,25],
    [15,47, 7,39,13,45, 5,37],[63,31,55,23,61,29,53,21],
]) / 64.0
tile = np.tile(BAYER8, (H // 8 + 1, W // 8 + 1))[:H, :W]

HORIZON = 470          # the glow sits just above this line
BAND = 130             # how tall the glow reaches into the sky

yy = np.arange(H).reshape(H, 1)
tone = np.clip(1.0 - (HORIZON - yy) / BAND, 0.0, 1.0)   # 1 at the horizon, fading to 0 upward
tone = np.where(yy > HORIZON, 0.0, tone)           # nothing below the horizon: that's ground
tone = tone ** 1.6                                 # concentrate the glow near the line
tone = np.repeat(tone, W, axis=1)

mask = tone > tile
img[mask] = GREEN

# ground below the horizon: solid black (already), with a hard green rule at the line itself
img[HORIZON-1:HORIZON+1, :] = GREEN

# one star already out, upper sky, off-centre
sx, sy, r = 268, 150, 3
yg, xg = np.ogrid[:H, :W]
star = (xg - sx) ** 2 + (yg - sy) ** 2 <= r * r
img[star] = GREEN
# a faint four-point sparkle so the single star reads as a star, not a fleck
for dx, dy, length in [(1, 0, 9), (-1, 0, 9), (0, 1, 7), (0, -1, 7)]:
    for k in range(2, length):
        px, py = sx + dx * k, sy + dy * k
        if 0 <= px < W and 0 <= py < H:
            img[py, px] = GREEN

Image.fromarray(img, "RGB").save(os.environ["OUT_RAW"])
