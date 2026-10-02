"""Shared helpers for 2026-10-02: a small Sunday-page print shop on the six inks.

Everything is drawn at 1x on the 400x600 grid with no anti-aliasing, so output is
already palette-pure (render with --dither none). Tone comes from Ben-Day dots,
Bayer screens and hatching done here, never from the quantiser.
"""
import math, os, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 400, 600
K = (0x00, 0x00, 0x00)
WH = (0xFF, 0xFF, 0xFF)
R = (0xE0, 0x1B, 0x24)
Y = (0xF5, 0xD4, 0x00)
B = (0x12, 0x3D, 0xB0)
G = (0x1E, 0x9B, 0x3C)

BAYER8 = np.array([
    [0, 32, 8, 40, 2, 34, 10, 42], [48, 16, 56, 24, 50, 18, 58, 26],
    [12, 44, 4, 36, 14, 46, 6, 38], [60, 28, 52, 20, 62, 30, 54, 22],
    [3, 35, 11, 43, 1, 33, 9, 41], [51, 19, 59, 27, 49, 17, 57, 25],
    [15, 47, 7, 39, 13, 45, 5, 37], [63, 31, 55, 23, 61, 29, 53, 21]]) / 64.0 + 1 / 128
YY, XX = np.mgrid[0:H, 0:W]
SCREEN = BAYER8[YY % 8, XX % 8]

FONTS = "/usr/share/fonts/truetype/"
def font(size, name="dejavu/DejaVuSans-Bold.ttf"):
    return ImageFont.truetype(FONTS + name, size)


class Canvas:
    def __init__(self, bg=WH):
        self.a = np.zeros((H, W, 3), np.uint8)
        self.a[:] = bg

    # --- masks -------------------------------------------------------------
    @staticmethod
    def mask(fn):
        """fn(draw) on a 1-bit image → bool mask. No anti-aliasing."""
        m = Image.new("1", (W, H), 0)
        fn(ImageDraw.Draw(m))
        return np.array(m, bool)

    def fill(self, m, c):
        self.a[m] = c

    def draw(self, fn, c):
        self.fill(self.mask(fn), c)

    # --- tone ----------------------------------------------------------------
    def screen(self, m, tone, c_lo, c_hi):
        """Bayer screen: tone 0 → c_lo, 1 → c_hi. tone is scalar or HxW array."""
        t = np.broadcast_to(np.asarray(tone, float), (H, W))
        hi = m & (t > SCREEN)
        self.a[m & ~hi] = c_lo
        self.a[hi] = c_hi

    def ramp(self, m, tone, stops):
        """Multi-stop screened gradient. stops = [c0, c1, ...]; tone 0..1."""
        t = np.clip(np.broadcast_to(np.asarray(tone, float), (H, W)), 0, 1) * (len(stops) - 1)
        i = np.minimum(t.astype(int), len(stops) - 2)
        f = t - i
        for k in range(len(stops) - 1):
            mk = m & (i == k)
            hi = mk & (f > SCREEN)
            self.a[mk & ~hi] = stops[k]
            self.a[hi] = stops[k + 1]

    def benday(self, m, c, pitch=5, r=1.3, angle=45, ox=0, oy=0):
        """Ben-Day dots of colour c over mask m (background left as is)."""
        th = math.radians(angle)
        u = (XX - ox) * math.cos(th) + (YY - oy) * math.sin(th)
        v = -(XX - ox) * math.sin(th) + (YY - oy) * math.cos(th)
        du = (u % pitch) - pitch / 2
        dv = (v % pitch) - pitch / 2
        r = np.broadcast_to(np.asarray(r, float), (H, W))
        self.a[m & (du * du + dv * dv <= r * r)] = c

    def hatch(self, m, c, pitch=4, angle=45, width=1, phase=0):
        th = math.radians(angle)
        u = XX * math.cos(th) + YY * math.sin(th) + phase
        self.a[m & ((u % pitch) < width)] = c

    def image(self):
        return Image.fromarray(self.a, "RGB")

    def save(self):
        self.image().save(os.environ.get("OUT_RAW", "out.png"))


def text(cv, xy, s, size, c, name="dejavu/DejaVuSans-Bold.ttf", anchor="la", stroke=0, stroke_c=None):
    """Text without anti-aliasing (1-bit mask), optional outline."""
    f = font(size, name)
    if stroke:
        cv.draw(lambda d: d.text(xy, s, font=f, fill=1, anchor=anchor, stroke_width=stroke), stroke_c)
    cv.draw(lambda d: d.text(xy, s, font=f, fill=1, anchor=anchor), c)


def poly_outline(cv, pts, fill, line=K, w=2):
    cv.draw(lambda d: d.polygon(pts, fill=1), line)
    if fill is not None:
        # shrink by drawing fill then outline on top
        cv.draw(lambda d: d.polygon(pts, fill=1), fill)
    cv.draw(lambda d: d.line(list(pts) + [pts[0]], fill=1, width=w, joint="curve"), line)


def ellipse_outline(cv, box, fill, line=K, w=2):
    if fill is not None:
        cv.draw(lambda d: d.ellipse(box, fill=1), fill)
    cv.draw(lambda d: d.ellipse(box, outline=1, width=w), line)
