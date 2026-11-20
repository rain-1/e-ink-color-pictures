"""Shared tools for the 2026-11-20 plates (Mandelbrot's birthday: "roughness").

Everything is drawn natively at 400x600 in palette indices, no antialiasing, so the
generators emit only the six panel colours and render with --dither none.
Tone is made with screens (Bayer / line hatch) inside the generator.
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 400, 600
K, WH, R, Y, B, G = 0, 1, 2, 3, 4, 5
RGB = np.array([(0, 0, 0), (255, 255, 255), (0xE0, 0x1B, 0x24), (0xF5, 0xD4, 0x00),
                (0x12, 0x3D, 0xB0), (0x1E, 0x9B, 0x3C)], dtype=np.uint8)
YY, XX = np.mgrid[0:H, 0:W]

_B8 = np.array([[0, 32, 8, 40, 2, 34, 10, 42], [48, 16, 56, 24, 50, 18, 58, 26],
                [12, 44, 4, 36, 14, 46, 6, 38], [60, 28, 52, 20, 62, 30, 54, 22],
                [3, 35, 11, 43, 1, 33, 9, 41], [51, 19, 59, 27, 49, 17, 57, 25],
                [15, 47, 7, 39, 13, 45, 5, 37], [63, 31, 55, 23, 61, 29, 53, 21]])
BAYER = np.tile((_B8 + 0.5) / 64.0, (H // 8 + 1, W // 8 + 1))[:H, :W]


def screen(tone):
    """True where 'ink' goes, for a 0..1 tone field (1 = solid)."""
    return tone > BAYER


def hatch(tone, angle=45.0, period=4.0, phase=0.0):
    """Line screen: parallel lines whose thickness follows tone."""
    a = np.deg2rad(angle)
    t = ((XX * np.cos(a) + YY * np.sin(a) + phase) % period) / period
    return t < tone


def fbm(seed, scale=64.0, octaves=5, gain=0.5, shape=(H, W), stretch=(1.0, 1.0)):
    """Value-noise fBm in 0..1 (bicubic-upsampled random lattices)."""
    rng = np.random.default_rng(seed)
    h, w = shape
    out = np.zeros(shape, np.float32)
    amp, tot, s = 1.0, 0.0, float(scale)
    for _ in range(octaves):
        gh = max(2, int(h / (s * stretch[0])) + 3)
        gw = max(2, int(w / (s * stretch[1])) + 3)
        g = rng.random((gh, gw)).astype(np.float32)
        im = Image.fromarray(g, "F").resize((int(gw * s * stretch[1]), int(gh * s * stretch[0])), Image.BICUBIC)
        a = np.asarray(im)
        oy, ox = int(s * stretch[0]), int(s * stretch[1])
        out += amp * a[oy:oy + h, ox:ox + w]
        tot += amp
        amp *= gain
        s = max(1.0, s / 2)
    out /= tot
    return np.clip(out, 0, 1)


def blur(a, r):
    im = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8), "L").filter(ImageFilter.GaussianBlur(r))
    return np.asarray(im, np.float32) / 255.0


def grow(mask, n=1):
    im = Image.fromarray((mask * 255).astype(np.uint8), "L")
    for _ in range(n):
        im = im.filter(ImageFilter.MaxFilter(3))
    return np.asarray(im) > 127


def edge(mask):
    """One-pixel outline just inside a boolean mask."""
    m = mask
    inner = m.copy()
    inner[1:, :] &= m[:-1, :]; inner[:-1, :] &= m[1:, :]
    inner[:, 1:] &= m[:, :-1]; inner[:, :-1] &= m[:, 1:]
    return m & ~inner


def mandel(size, iters=60):
    """Boolean mask (size*0.9 high, size wide) of the Mandelbrot set, head to the left."""
    w, h = size, int(size * 0.9)
    x = np.linspace(-2.05, 0.6, w)[None, :]
    y = np.linspace(-1.2, 1.2, h)[:, None]
    c = x + 1j * y
    z = np.zeros_like(c)
    inside = np.ones(c.shape, bool)
    for _ in range(iters):
        z = np.where(inside, z * z + c, z)
        inside &= np.abs(z) < 2
    return inside


def font(size, name="DejaVuSans-Bold"):
    for d in ("/usr/share/fonts/truetype/dejavu/", "/usr/share/fonts/dejavu/", ""):
        try:
            return ImageFont.truetype(d + name + ".ttf", size)
        except OSError:
            pass
    return ImageFont.load_default()


class Plate:
    """A palette-index canvas with numpy and PIL access."""

    def __init__(self, fill=WH):
        self.a = np.full((H, W), fill, np.uint8)

    def put(self, mask, colour):
        self.a[mask] = colour

    def draw(self):
        """Context: with p.draw() as d: d.line(...). Colours are palette indices."""
        return _Draw(self)

    def stamp(self, mask, x, y, colour):
        h, w = mask.shape
        y0, x0 = max(0, y), max(0, x)
        y1, x1 = min(H, y + h), min(W, x + w)
        sub = mask[y0 - y:y1 - y, x0 - x:x1 - x]
        self.a[y0:y1, x0:x1][sub] = colour

    def caption(self, numeral, text, fg=K, bg=WH, height=26, size=12):
        """The plate band shared by all five: numeral, the little set, the clause."""
        top = H - height
        self.a[top:, :] = bg
        self.a[top, :] = fg
        self.a[top + 2, :] = fg
        m = mandel(26)
        with self.draw() as d:
            d.fontmode = "1"
            f = font(size)
            d.text((8, top + (height - size) // 2 - 1), numeral, font=f, fill=fg)
            lines = text.split("\n")
            lh = size + 2
            y = top + 3 + (height - 3 - lh * len(lines)) // 2
            for ln in lines:
                tw = d.textlength(ln, font=f)
                d.text(((W - tw) // 2 + 4, y), ln, font=f, fill=fg)
                y += lh
        self.stamp(m, W - 36, top + 3 + (height - 3 - m.shape[0]) // 2, fg)

    def save(self):
        out = os.environ.get("OUT_RAW", "out.png")
        Image.fromarray(RGB[self.a], "RGB").save(out)


class _Draw:
    def __init__(self, plate):
        self.p = plate

    def __enter__(self):
        self.im = Image.fromarray(self.p.a, "P")
        d = ImageDraw.Draw(self.im)
        d.fontmode = "1"
        return d

    def __exit__(self, *exc):
        self.p.a[:] = np.asarray(self.im)
