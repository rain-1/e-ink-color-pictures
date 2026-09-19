"""Afternoon: a bowline's loop, drawn as a technical rope plate -- blue ink
on white paper. Dominant white. Thick stroked rope with white gaps cut at
overlaps to suggest over/under, fine white hatch ticks along its length for
cylindrical shading. A small pennant is tied to the working end -- the
day's recurring motif."""
import math
import os

from PIL import Image, ImageDraw

S = 4
W, H = 400 * S, 600 * S
BLUE = (0x12, 0x3D, 0xB0)
WHITE = (0xFF, 0xFF, 0xFF)
RW = 24 * S  # rope width

img = Image.new("RGB", (W, H), WHITE)
d = ImageDraw.Draw(img)


def rope_line(pts, width=RW):
    d.line(pts, fill=BLUE, width=width, joint="curve")
    r = width // 2
    for p in (pts[0], pts[-1]):
        d.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], fill=BLUE)


def rope_circle(cx, cy, r, width=RW):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=BLUE, width=width)


def hatch_line(pts, every=9, frac=0.6, width=RW):
    for i in range(0, len(pts) - 2, every):
        x0, y0 = pts[i]
        x1, y1 = pts[i + 2]
        dx, dy = x1 - x0, y1 - y0
        n = (dx**2 + dy**2) ** 0.5 or 1
        nx, ny = -dy / n, dx / n
        half = width * frac / 2
        d.line([(x0 - nx * half, y0 - ny * half), (x0 + nx * half, y0 + ny * half)],
               fill=WHITE, width=int(2.2 * S))


def hatch_circle(cx, cy, r, count=26, frac=0.6, width=RW, a0=0, a1=2 * math.pi):
    for k in range(count):
        a = a0 + (a1 - a0) * k / count
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        nx, ny = math.cos(a), math.sin(a)
        half = width * frac / 2
        d.line([(x - nx * half, y - ny * half), (x + nx * half, y + ny * half)],
               fill=WHITE, width=int(2.2 * S))


def gap(pt, size=RW * 1.35):
    d.ellipse([pt[0] - size / 2, pt[1] - size / 2, pt[0] + size / 2, pt[1] + size / 2], fill=WHITE)


def bez(p0, p1, p2, p3, n=50):
    out = []
    for i in range(n + 1):
        t = i / n
        mt = 1 - t
        x = mt**3 * p0[0] + 3 * mt**2 * t * p1[0] + 3 * mt * t**2 * p2[0] + t**3 * p3[0]
        y = mt**3 * p0[1] + 3 * mt**2 * t * p1[1] + 3 * mt * t**2 * p2[1] + t**3 * p3[1]
        out.append((x * S, y * S))
    return out


CX, CY, R = 200, 330, 100

# standing part: rises from the bottom edge, curves into the loop
standing = bez((165, 600), (165, 470), (150, 400), (145, 355))
rope_line(standing)
hatch_line(standing)

# small tucked bight -- a secondary loop where the standing part ties in
tuck = bez((145, 355), (95, 320), (110, 250), (175, 258))
rope_line(tuck, width=int(RW * 0.85))
hatch_line(tuck, width=int(RW * 0.85))

# the main loop: the finished bowline eye
rope_circle(CX * S, CY * S, R * S)
hatch_circle(CX * S, CY * S, R * S)

# gaps where the tucked bight and the standing part pass under the loop
gap((145 * S, 355 * S))
gap((175 * S, 258 * S))

# working end: leaves the loop at upper right, carries the pennant
tail = bez((CX + R * math.cos(-0.5), CY + R * math.sin(-0.5)), (330, 150), (300, 90), (280, 60))
gap(tail[0])
rope_line(tail, width=int(RW * 0.85))
hatch_line(tail, width=int(RW * 0.85))

# pennant tied to the working end
px, py = tail[-1]
d.line([(px, py), (px, py - 40 * S)], fill=BLUE, width=int(4 * S))
d.polygon([(px, py - 40 * S), (px + 34 * S, py - 28 * S), (px, py - 16 * S)], fill=BLUE)

img = img.resize((400, 600), Image.LANCZOS)
img.save(os.environ["OUT_RAW"])
