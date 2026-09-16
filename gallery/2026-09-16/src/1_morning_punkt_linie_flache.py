# Morning — "Punkt und Linie zu Fläche" (Point and Line to Plane), Kandinsky's 1926
# theoretical treatise. Three registers, top to bottom: a point, a line under tension,
# a plane. Palette: black, white, blue. Pure geometry, no type (risk of small text).
import os, math
from PIL import Image, ImageDraw
W, H = 400, 600
WHT, BLK, BLU = (255, 255, 255), (0, 0, 0), (0x12, 0x3D, 0xB0)
im = Image.new("RGB", (W, H), WHT)
d = ImageDraw.Draw(im)

# faint blue grid across the whole sheet (graph-paper ground)
for x in range(20, W, 20):
    d.line((x, 0, x, H), fill=BLU, width=1)
for y in range(20, H, 20):
    d.line((0, y, W, y), fill=BLU, width=1)

# divider lines between the three registers
R1, R2 = 200, 400
d.line((0, R1, W, R1), fill=BLK, width=2)
d.line((0, R2, W, R2), fill=BLK, width=2)

# --- register 1: PUNKT — a single point, with its field of tension marked by ticks ---
cx, cy = W // 2, R1 // 2
d.ellipse((cx - 26, cy - 26, cx + 26, cy + 26), fill=BLK)
for a in range(0, 360, 15):
    r0, r1 = 55, 68
    x0, y0 = cx + r0 * math.cos(math.radians(a)), cy + r0 * math.sin(math.radians(a))
    x1, y1 = cx + r1 * math.cos(math.radians(a)), cy + r1 * math.sin(math.radians(a))
    d.line((x0, y0, x1, y1), fill=BLU, width=2)

# --- register 2: LINIE — a line under tension: not straight, a zigzag of forces ---
pts = [(20, R1 + 30), (130, R1 + 150), (230, R1 + 50), (330, R1 + 160), (380, R1 + 30)]
d.line(pts, fill=BLK, width=6, joint="curve")
# small blue arrowheads at each vertex showing the pull of direction
for i in range(1, len(pts) - 1):
    x, y = pts[i]
    d.ellipse((x - 5, y - 5, x + 5, y + 5), fill=BLU)

# --- register 3: FLÄCHE — a plane, built from the line's own tension: a blue
#     trapezoid, ruled with the black grid that generated it, with one point
#     resting on it (the circle motif, closing the sequence) ---
plane = [(40, R2 + 190), (360, R2 + 190), (300, R2 + 40), (100, R2 + 40)]
d.polygon(plane, fill=BLU)
for i in range(1, 8):
    t = i / 8
    x0 = 40 + (100 - 40) * t
    y0 = R2 + 190 + (40 - 190) * t
    x1 = 360 + (300 - 360) * t
    y1 = R2 + 190 + (40 - 190) * t
    d.line((x0, y0, x1, y1), fill=BLK, width=1)
d.ellipse((cx - 16, R2 + 95 - 16, cx + 16, R2 + 95 + 16), fill=BLK)

im.save(os.environ["OUT_RAW"])
