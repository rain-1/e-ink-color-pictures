"""Night: a small ship crossing under the stars, near the equinox when day
and night are close to balanced. Aquatint-style stipple for the sky, mostly
black. A single low band of blue at the horizon is the last of the light;
a tiny pennant at the stern is the day's recurring motif."""
import math
import os
import random

from PIL import Image, ImageDraw

S = 4
W, H = 400 * S, 600 * S
BLACK = (0x00, 0x00, 0x00)
BLUE = (0x12, 0x3D, 0xB0)

img = Image.new("RGB", (W, H), BLACK)
d = ImageDraw.Draw(img)

random.seed(919)

HORIZON = 470

# --- aquatint stipple: dense near the top, thinning toward the horizon,
#     a soft grain rather than pinprick stars (all but a few are tiny) ---
for _ in range(1400):
    y = random.triangular(20, HORIZON - 10, 20)
    x = random.uniform(0, 400)
    r = random.choice([1, 1, 1, 2]) * S
    d.ellipse([x * S - r, y * S - r, x * S + r, y * S + r], fill=BLUE)

# a few bright stars, one marked -- the pole star, steering by it tonight
stars = [(70, 90), (140, 60), (330, 110), (250, 200), (60, 260), (310, 300)]
for sx, sy in stars:
    d.line([(sx * S - 10 * S, sy * S), (sx * S + 10 * S, sy * S)], fill=BLUE, width=int(2 * S))
    d.line([(sx * S, sy * S - 10 * S), (sx * S, sy * S + 10 * S)], fill=BLUE, width=int(2 * S))

polaris = (200, 55)
d.line([(polaris[0] * S - 16 * S, polaris[1] * S), (polaris[0] * S + 16 * S, polaris[1] * S)],
       fill=BLUE, width=int(3 * S))
d.line([(polaris[0] * S, polaris[1] * S - 16 * S), (polaris[0] * S, polaris[1] * S + 16 * S)],
       fill=BLUE, width=int(3 * S))
d.ellipse([(polaris[0] - 24) * S, (polaris[1] - 24) * S, (polaris[0] + 24) * S, (polaris[1] + 24) * S],
          outline=BLUE, width=int(1.5 * S))

# --- last light: a thin band right at the horizon, equinox-even ---
for i in range(int(4 * S)):
    t = i / (4 * S)
    d.line([(0, (HORIZON - 4 + t * 4) * S), (400 * S, (HORIZON - 4 + t * 4) * S)],
           fill=BLUE, width=1)

# --- sea, solid black below the horizon, with a faint reflected glint ---
d.rectangle([0, HORIZON * S, 400 * S, 600 * S], fill=BLACK)
for gx in range(160, 240, 8):
    d.line([(gx * S, (HORIZON + 6) * S), (gx * S + 3 * S, (HORIZON + 16) * S)],
           fill=BLUE, width=int(1.5 * S))

# --- small ship, dead reckoning across the horizon ---
hx = 230
hull = [(hx - 70, HORIZON), (hx + 70, HORIZON), (hx + 50, HORIZON + 16),
        (hx - 50, HORIZON + 16)]
d.polygon([(x * S, y * S) for x, y in hull], fill=BLUE)
d.line([(hx * S, HORIZON * S), (hx * S, (HORIZON - 70) * S)], fill=BLUE, width=int(3 * S))
d.line([(hx * S, (HORIZON - 60) * S), ((hx + 45) * S, (HORIZON - 30) * S)], fill=BLUE, width=int(2 * S))

# tiny pennant at the stern
px, py = hx - 68, HORIZON - 6
d.polygon([(px * S, py * S), ((px - 22) * S, (py - 8) * S), (px * S, (py - 16) * S)], fill=BLUE)

img = img.resize((400, 600), Image.LANCZOS)
img.save(os.environ["OUT_RAW"])
