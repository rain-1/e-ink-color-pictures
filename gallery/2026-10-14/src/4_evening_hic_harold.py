"""HIC HAROLD REX INTERFECTVS EST — a stitched panel.

Every shape is "laid and couched" like the Bayeux Tapestry: filled with parallel
threads (palette colour with linen showing between), crossed by couching bars, and
outlined in stem stitch. Far legs of the horse in a different colour, as the
embroiderers did. Drawn at panel resolution in palette colours (--dither none).
"""
import math, os, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 400, 600
K, Wh, Rd, Yl, Bl, Gr = (0, 0, 0), (255, 255, 255), (0xE0, 0x1B, 0x24), (0xF5, 0xD4, 0x00), (0x12, 0x3D, 0xB0), (0x1E, 0x9B, 0x3C)
R = random.Random(14101066)
yy, xx = np.mgrid[0:H, 0:W]
canvas = np.full((H, W, 3), 255, np.uint8)
# linen weave: a sparse fleck of yellow thread in the ground
weave = ((xx * 7 + yy * 13) % 29 == 0) & ((xx // 2 + yy // 3) % 3 == 0)
canvas[weave] = Yl


class _Filled:
    """ImageDraw proxy that fills shapes with 255 unless told otherwise."""
    def __init__(self, d):
        self.d = d

    def __getattr__(self, name):
        meth = getattr(self.d, name)
        def call(*a, **kw):
            kw.setdefault("fill", 255)
            return meth(*a, **kw)
        return call


def mask_of(fn):
    m = Image.new("L", (W, H), 0)
    fn(_Filled(ImageDraw.Draw(m)))
    return np.asarray(m) > 127


def stitch(fn, col, angle=35, outline=K, gap=3, couch=9, rings=False):
    """Lay threads of `col` inside the shape drawn by fn(draw), couch them, outline it."""
    m = mask_of(fn)
    a = math.radians(angle)
    u = xx * math.cos(a) + yy * math.sin(a)
    v = -xx * math.sin(a) + yy * math.cos(a)
    thread = (np.floor(u) % gap) < gap - 1 if gap > 1 else np.ones_like(u, bool)
    canvas[m & thread] = col
    canvas[m & ~thread] = Wh
    if couch:
        bars = (np.floor(v) % couch == 0) & (np.floor(u / 2) % 3 == 0)
        canvas[m & bars] = K if col in (Yl, Wh) else Yl if col in (Bl, Rd) else Wh
    if rings:  # mail: little rings on a grid
        ring = ((xx % 6 == 0) & (yy % 5 == 0)) | ((xx % 6 == 3) & (yy % 5 == 2))
        canvas[m & ring] = K
    if outline is not None:
        mi = Image.fromarray((m * 255).astype(np.uint8))
        dil = np.asarray(mi.filter(ImageFilter.MaxFilter(3))) > 127
        edge = dil & ~m
        stem = ((xx + 2 * yy) % 6) != 0  # tiny breaks, like stem stitches
        canvas[edge & stem] = outline


def line_shape(pts, w):
    return lambda d: d.line(pts, fill=255, width=w, joint="curve")


# ================================================================== top border: beasts in slanted compartments
TB0, TB1 = 14, 92
stitch(lambda d: d.rectangle([0, TB1 - 1, W, TB1 + 1]), K, outline=None, couch=0, gap=1)
stitch(lambda d: d.rectangle([0, TB0 - 1, W, TB0 + 1]), K, outline=None, couch=0, gap=1)
for i in range(6):
    x0 = i * 72 - 10
    stitch(line_shape([(x0, TB1), (x0 + 30, TB0)], 5), [Bl, Gr, Rd][i % 3], outline=K, couch=0)
    cx, cy = x0 + 50, (TB0 + TB1) / 2 + 6
    col = [Rd, Yl, Gr, Bl, Yl, Rd][i]
    if i % 2 == 0:  # a bird with a curled neck
        stitch(lambda d, cx=cx, cy=cy: d.ellipse([cx - 16, cy - 8, cx + 12, cy + 10]), col, 20)
        stitch(lambda d, cx=cx, cy=cy: d.polygon([(cx + 8, cy - 4), (cx + 18, cy - 26), (cx + 24, cy - 24), (cx + 14, cy)]), col, 70)
        stitch(lambda d, cx=cx, cy=cy: d.polygon([(cx - 14, cy - 2), (cx - 28, cy - 14), (cx - 20, cy + 6)]), [Bl, Gr, Rd][i % 3], 0)
        stitch(lambda d, cx=cx, cy=cy: d.line([(cx - 4, cy + 10), (cx - 6, cy + 22)], fill=255, width=3), K, outline=None, couch=0, gap=1)
        stitch(lambda d, cx=cx, cy=cy: d.line([(cx + 4, cy + 10), (cx + 6, cy + 22)], fill=255, width=3), K, outline=None, couch=0, gap=1)
        canvas[int(cy - 24):int(cy - 22), int(cx + 20):int(cx + 22)] = K
    else:  # a lion passant, tail over its back
        stitch(lambda d, cx=cx, cy=cy: d.ellipse([cx - 20, cy - 8, cx + 14, cy + 6]), col, 0)
        stitch(lambda d, cx=cx, cy=cy: d.ellipse([cx + 8, cy - 18, cx + 24, cy - 2]), col, 60)
        for lx, c2 in ((-16, Rd if col != Rd else Bl), (-10, col), (6, Rd if col != Rd else Bl), (12, col)):
            stitch(lambda d, cx=cx, cy=cy, lx=lx: d.line([(cx + lx, cy + 2), (cx + lx - 2, cy + 22)], fill=255, width=4), c2, 90, couch=0)
        stitch(line_shape([(cx - 20, cy - 4), (cx - 30, cy - 18), (cx - 18, cy - 26)], 3), K, outline=None, couch=0, gap=1)

# ================================================================== the inscription
f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 27)


def text_shape(x, y, s):
    return lambda d: d.text((x, y), s, font=f, fill=255)


line1, line2 = "HIC HAROLD", "REX INTERFECTVS EST"
f2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 22)
tmp = ImageDraw.Draw(Image.new("L", (1, 1)))
x = (W - tmp.textlength(line1, font=f)) / 2
for ch in line1:
    stitch(lambda d, x=x, ch=ch: d.text((x, 100), ch, font=f, fill=255), Bl, 90, outline=None, couch=0, gap=3)
    x += tmp.textlength(ch, font=f)
x = (W - tmp.textlength(line2, font=f2)) / 2
for i, ch in enumerate(line2):
    stitch(lambda d, x=x, ch=ch: d.text((x, 134), ch, font=f2, fill=255), Bl if i % 7 else Rd, 90, outline=None, couch=0, gap=3)
    x += tmp.textlength(ch, font=f2)

GROUND = 470

# ================================================================== a stylised tree, the scene divider (right edge)
TX = 378
stitch(lambda d: d.polygon([(TX - 6, GROUND), (TX + 6, GROUND), (TX + 3, 260), (TX - 3, 260)]), Gr, 90)
for k in range(5):
    y0 = 270 + k * 34
    stitch(line_shape([(TX, y0 + 20), (TX - 18, y0), (TX - 10, y0 - 18), (TX + 2, y0 - 10)], 6), [Rd, Yl, Bl, Rd, Yl][k], 45, couch=0)
    stitch(line_shape([(TX, y0 + 20), (TX + 18, y0), (TX + 14, y0 - 16)], 6), [Bl, Rd, Yl, Bl, Rd][k], 135, couch=0)
stitch(lambda d: d.ellipse([TX - 16, 220, TX + 16, 264]), Gr, 0)

# ================================================================== the Norman horseman (right, charging left)
hx, hy = 270, 340  # horse body centre
# far legs first, in red (the embroiderers' second colour)
for p in ([(hx - 40, hy + 10), (hx - 64, hy + 46), (hx - 58, GROUND - 14)], [(hx + 44, hy + 12), (hx + 58, hy + 52), (hx + 76, GROUND - 22)]):
    stitch(line_shape(p, 8), Rd, 80, couch=0)
# body
stitch(lambda d: d.ellipse([hx - 62, hy - 26, hx + 62, hy + 26]), Gr, 25)
# neck + head
stitch(lambda d: d.polygon([(hx - 44, hy - 18), (hx - 74, hy - 70), (hx - 92, hy - 82), (hx - 106, hy - 62), (hx - 84, hy - 56), (hx - 56, hy + 6)]), Gr, 60)
canvas[hy - 72:hy - 69, hx - 90:hx - 87] = K
# mane
for k in range(6):
    stitch(line_shape([(hx - 50 - k * 6, hy - 16 - k * 10), (hx - 42 - k * 6, hy - 26 - k * 10)], 4), Yl, 90, couch=0)
# near legs in green
for p in ([(hx - 30, hy + 14), (hx - 30, hy + 54), (hx - 44, GROUND - 4)], [(hx + 34, hy + 14), (hx + 30, hy + 54), (hx + 46, GROUND - 6)]):
    stitch(line_shape(p, 8), Gr, 80, couch=0)
for fx, fy in [(hx - 58, GROUND - 14), (hx + 76, GROUND - 22), (hx - 44, GROUND - 4), (hx + 46, GROUND - 6)]:
    stitch(lambda d, fx=fx, fy=fy: d.ellipse([fx - 6, fy - 4, fx + 6, fy + 4]), K, outline=None, couch=0, gap=1)
# tail
stitch(line_shape([(hx + 60, hy - 8), (hx + 84, hy - 2), (hx + 92, hy + 26), (hx + 82, hy + 40)], 7), Bl, 70, couch=0)
# saddle cloth + girth
stitch(lambda d: d.polygon([(hx - 20, hy - 26), (hx + 26, hy - 26), (hx + 22, hy + 14), (hx - 16, hy + 14)]), Rd, 0)
# rider: mail tunic with rings, legs hanging, conical helm, kite shield, sword raised
stitch(lambda d: d.polygon([(hx - 12, hy - 80), (hx + 14, hy - 80), (hx + 22, hy - 24), (hx - 18, hy - 24)]), Bl, 90, rings=True)
stitch(line_shape([(hx + 6, hy - 26), (hx + 2, hy + 24), (hx - 6, hy + 30)], 9), Bl, 90, rings=True)
stitch(lambda d: d.ellipse([hx - 12, hy - 104, hx + 10, hy - 80]), Wh, 0, couch=0)
stitch(lambda d: d.polygon([(hx - 14, hy - 94), (hx + 1, hy - 120), (hx + 12, hy - 94)]), Yl, 90)
stitch(line_shape([(hx - 3, hy - 94), (hx - 3, hy - 84)], 2), K, outline=None, couch=0, gap=1)
canvas[hy - 91:hy - 89, hx - 10:hx - 8] = K
# raised sword arm
stitch(line_shape([(hx - 6, hy - 74), (hx - 30, hy - 100), (hx - 40, hy - 120)], 7), Bl, 45, rings=True)
stitch(line_shape([(hx - 42, hy - 124), (hx - 84, hy - 170)], 5), Wh, 45, couch=0)
stitch(line_shape([(hx - 48, hy - 114), (hx - 34, hy - 128)], 4), Yl, 0, couch=0)
# kite shield on the far side, showing its face with a winged device
stitch(lambda d: d.polygon([(hx + 10, hy - 74), (hx + 38, hy - 70), (hx + 36, hy - 40), (hx + 22, hy - 8), (hx + 8, hy - 40)]), Yl, 90)
stitch(line_shape([(hx + 22, hy - 66), (hx + 22, hy - 16)], 3), Rd, 90, outline=None, couch=0)
stitch(line_shape([(hx + 12, hy - 56), (hx + 34, hy - 50)], 3), Rd, 0, outline=None, couch=0)

# ================================================================== Harold, left, pulling the arrow from his eye
X, FOOT = 104, GROUND
# spear, planted
stitch(line_shape([(48, 196), (48, FOOT)], 3), K, outline=None, couch=0, gap=1)
stitch(lambda d: d.polygon([(48, 180), (43, 198), (53, 198)]), Wh, 90)
# legs, cross-gartered
for lx in (-12, 10):
    stitch(lambda d, lx=lx: d.polygon([(X + lx - 7, 384), (X + lx + 7, 384), (X + lx + 6, FOOT - 6), (X + lx - 6, FOOT - 6)]), Rd, 90)
    for k in range(5):
        y0 = 392 + k * 15
        stitch(line_shape([(X + lx - 7, y0), (X + lx + 7, y0 + 8)], 2), K, outline=None, couch=0, gap=1)
    stitch(lambda d, lx=lx: d.polygon([(X + lx - 8, FOOT - 8), (X + lx + 4, FOOT - 8), (X + lx - 12, FOOT), (X + lx - 20, FOOT)]), K, outline=None, couch=0, gap=1)
# hauberk
stitch(lambda d: d.polygon([(X - 22, 262), (X + 22, 262), (X + 34, 392), (X + 2, 392), (X, 372), (X - 2, 392), (X - 34, 392)]), Yl, 90, rings=True)
# head, nasal helm, beard
stitch(lambda d: d.ellipse([X - 13, 220, X + 13, 252]), Wh, 0, couch=0)
stitch(lambda d: d.polygon([(X - 15, 232), (X - 2, 198), (X + 15, 232)]), Bl, 90)
stitch(line_shape([(X - 5, 232), (X - 5, 244)], 3), Bl, 90, outline=None, couch=0)
stitch(lambda d: d.polygon([(X - 10, 246), (X + 10, 246), (X + 2, 262), (X - 6, 260)]), Yl, 90, couch=0)
canvas[238:240, X + 1:X + 4] = K  # the good eye
# the arrow, in from the left, into the eye
stitch(line_shape([(4, 168), (X - 8, 236)], 3), K, outline=None, couch=0, gap=1)
for k in range(3):
    stitch(line_shape([(8 + k * 5, 170 + k * 3), (2 + k * 5, 160 + k * 3)], 2), Rd, 0, outline=None, couch=0, gap=1)
    stitch(line_shape([(8 + k * 5, 170 + k * 3), (16 + k * 5, 162 + k * 3)], 2), Rd, 0, outline=None, couch=0, gap=1)
# arm up to the arrow
stitch(line_shape([(X + 16, 270), (X + 4, 296), (X - 18, 250), (X - 22, 236)], 8), Yl, 45, rings=True)
stitch(lambda d: d.ellipse([X - 28, 226, X - 14, 240]), Wh, 0, couch=0)
# round shield on his left side, red with a yellow rim and boss
stitch(lambda d: d.ellipse([X - 70, 284, X - 6, 360]), Rd, 30)
stitch(lambda d: d.ellipse([X - 44, 314, X - 30, 330]), Yl, 0, couch=0)
for k in range(8):
    a = k / 8 * 2 * math.pi
    stitch(line_shape([(X - 38 + 10 * math.cos(a), 322 + 10 * math.sin(a)), (X - 38 + 28 * math.cos(a), 322 + 34 * math.sin(a))], 2), Yl, 0, outline=None, couch=0, gap=1)

# ================================================================== the ground: little mounds, a fallen dragon standard
stitch(lambda d: d.rectangle([0, GROUND, W, GROUND + 2]), Gr, 0, outline=None, couch=0, gap=1)
for mx in range(-10, W, 46):
    stitch(lambda d, mx=mx: d.chord([mx, GROUND - 12, mx + 40, GROUND + 12], 180, 360), [Gr, Bl][(mx // 46) % 2], 0, couch=0)
stitch(line_shape([(150, GROUND - 4), (214, GROUND - 40)], 3), K, outline=None, couch=0, gap=1)
dpts = [(214 + k * 7, GROUND - 40 + 10 * math.sin(k / 1.4) + k * 3) for k in range(7)]
stitch(line_shape(dpts, 10), Rd, 0, couch=0)
stitch(lambda d: d.polygon([(210, GROUND - 48), (222, GROUND - 42), (210, GROUND - 32)]), Rd, 0)

# ================================================================== lower border: archers
LB0 = GROUND + 18
stitch(lambda d: d.rectangle([0, LB0 - 1, W, LB0 + 1]), K, outline=None, couch=0, gap=1)
stitch(lambda d: d.rectangle([0, H - 14, W, H - 12]), K, outline=None, couch=0, gap=1)
for i, ax in enumerate(range(34, W, 66)):
    by = H - 18
    col = [Bl, Gr, Rd, Yl, Bl, Gr][i]
    stitch(lambda d, ax=ax: d.ellipse([ax - 6, by - 72, ax + 6, by - 58]), Wh, 0, couch=0)
    stitch(lambda d, ax=ax, col=col: d.polygon([(ax - 8, by - 58), (ax + 8, by - 58), (ax + 12, by - 26), (ax - 12, by - 26)]), col, 90)
    stitch(line_shape([(ax - 4, by - 26), (ax - 12, by)], 5), K if col != Bl else Rd, 90, couch=0)
    stitch(line_shape([(ax + 4, by - 26), (ax + 10, by)], 5), K if col != Bl else Rd, 90, couch=0)
    # bow drawn upward
    stitch(lambda d, ax=ax: d.arc([ax + 6, by - 92, ax + 30, by - 44], 250, 110, fill=255, width=3), K, outline=None, couch=0, gap=1)
    stitch(line_shape([(ax + 2, by - 54), (ax + 20, by - 82)], 2), Rd, 0, outline=None, couch=0, gap=1)
    stitch(line_shape([(ax + 2, by - 54), (ax + 20, by - 66)], 2), K, outline=None, couch=0, gap=1)

Image.fromarray(canvas).save(os.environ.get("OUT_RAW", "raw4.png"))
