"""Shared drawing kit for 2026-09-29.

Draw at 3x in *palette indices* (0-5 pure inks, 6+ registered two-ink screens),
downsample by majority vote (crisp, no speckle), then expand screens with an 8x8
Bayer matrix at panel resolution. Output is already palette-clean: render with
--dither none.
"""
import math, os, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont

S = 3
W, H = 400, 600
K, WH, R, Y, B, G = 0, 1, 2, 3, 4, 5
RGB = np.array([(0, 0, 0), (255, 255, 255), (0xE0, 0x1B, 0x24), (0xF5, 0xD4, 0x00),
                (0x12, 0x3D, 0xB0), (0x1E, 0x9B, 0x3C)], dtype=np.uint8)
_MIX = {}
_BAYER = None


def bayer8():
    global _BAYER
    if _BAYER is None:
        b = np.array([[0, 2], [3, 1]])
        for _ in range(2):
            b = np.block([[4 * b, 4 * b + 2], [4 * b + 3, 4 * b + 1]])
        _BAYER = (b + 0.5) / 64.0
    return _BAYER


def mix(a, b, t):
    """Register a screen: ink b at fraction t over ink a. Returns an index."""
    t = round(t * 16) / 16
    if t <= 0: return a
    if t >= 1: return b
    key = (a, b, t)
    for k, v in _MIX.items():
        if v == key: return k
    k = 6 + len(_MIX)
    assert k < 256
    _MIX[k] = key
    return k


def font(size, kind="serif"):
    names = {"serif": "/usr/share/fonts/truetype/freefont/FreeSerif.ttf",
             "serifb": "/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf",
             "serifi": "/usr/share/fonts/truetype/freefont/FreeSerifItalic.ttf",
             "sans": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
             "sansb": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"}
    return ImageFont.truetype(names[kind], int(size * S))


class Canvas:
    def __init__(self, bg=WH, seed=0):
        self.img = Image.new("L", (W * S, H * S), bg)
        self.d = ImageDraw.Draw(self.img)
        self.rng = random.Random(seed)
        self.np = np.random.default_rng(seed)

    # all coordinates in panel pixels (floats ok)
    def _p(self, pts):
        return [(x * S, y * S) for x, y in pts]

    def poly(self, pts, fill, outline=None, width=1):
        self.d.polygon(self._p(pts), fill=fill)
        if outline is not None:
            self.line(list(pts) + [pts[0]], outline, width)

    def line(self, pts, fill, width=1.0, joint=True):
        self.d.line(self._p(pts), fill=fill, width=max(1, int(round(width * S))),
                    joint="curve" if joint else None)
        if joint and width >= 2:
            r = width / 2
            for x, y in (pts[0], pts[-1]):
                self.circle(x, y, r * 0.98, fill)

    def circle(self, x, y, r, fill, outline=None, width=1.0):
        self.d.ellipse([(x - r) * S, (y - r) * S, (x + r) * S, (y + r) * S], fill=fill,
                       outline=outline, width=max(1, int(round(width * S))) if outline is not None else 0)

    def ellipse(self, x, y, rx, ry, fill, outline=None, width=1.0):
        self.d.ellipse([(x - rx) * S, (y - ry) * S, (x + rx) * S, (y + ry) * S], fill=fill,
                       outline=outline, width=max(1, int(round(width * S))) if outline is not None else 0)

    def rect(self, x0, y0, x1, y1, fill):
        self.d.rectangle([x0 * S, y0 * S, x1 * S - 1, y1 * S - 1], fill=fill)

    def text(self, x, y, s, fill, f, anchor="la"):
        self.d.text((x * S, y * S), s, fill=fill, font=f, anchor=anchor)

    def grid(self):
        """Sub-pixel coordinate grids (in panel px) for numpy masks."""
        ys, xs = np.mgrid[0:H * S, 0:W * S].astype(np.float32)
        return (xs + 0.5) / S, (ys + 0.5) / S

    def mask(self, m, idx):
        a = np.asarray(self.img).copy()
        a[m] = idx
        self.img = Image.fromarray(a, "L")
        self.d = ImageDraw.Draw(self.img)

    def array(self):
        return np.asarray(self.img)

    def set_array(self, a):
        self.img = Image.fromarray(a.astype(np.uint8), "L")
        self.d = ImageDraw.Draw(self.img)

    def finish(self, path=None):
        a = np.asarray(self.img).reshape(H, S, W, S).transpose(0, 2, 1, 3).reshape(H, W, S * S)
        # majority vote per block
        best = a[:, :, 0].copy()
        bestc = np.zeros((H, W), np.int32)
        for v in np.unique(a):
            c = (a == v).sum(-1)
            upd = c > bestc
            best[upd] = v
            bestc[upd] = c[upd]
        out = np.zeros((H, W), np.uint8)
        bay = np.tile(bayer8(), (H // 8 + 1, W // 8 + 1))[:H, :W]
        for v in np.unique(best):
            m = best == v
            if v < 6:
                out[m] = v
            else:
                ia, ib, t = _MIX[int(v)]
                out[m] = np.where(bay[m] < t, ib, ia)
        rgb = RGB[out]
        path = path or os.environ.get("OUT_RAW", "out.png")
        Image.fromarray(rgb, "RGB").save(path)
        return path


def bez(p0, p1, p2, p3, n=60):
    out = []
    for i in range(n + 1):
        t = i / n
        u = 1 - t
        out.append((u**3 * p0[0] + 3 * u*u*t * p1[0] + 3 * u*t*t * p2[0] + t**3 * p3[0],
                    u**3 * p0[1] + 3 * u*u*t * p1[1] + 3 * u*t*t * p2[1] + t**3 * p3[1]))
    return out


def offset(path, w):
    """Left/right outlines of a polyline with per-point width function w(t)."""
    L, Rr = [], []
    n = len(path)
    for i, (x, y) in enumerate(path):
        a = path[max(0, i - 1)]; b = path[min(n - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        l = math.hypot(dx, dy) or 1
        nx, ny = -dy / l, dx / l
        ww = w(i / (n - 1)) if callable(w) else w
        L.append((x + nx * ww / 2, y + ny * ww / 2))
        Rr.append((x - nx * ww / 2, y - ny * ww / 2))
    return L, Rr


def ribbon(cv, path, w, fill):
    L, Rr = offset(path, w)
    cv.poly(L + Rr[::-1], fill)
    return L, Rr


def vnoise(shape_xy, scale, rng, octaves=3):
    """Cheap value noise on panel-res grid, upsampled to canvas res."""
    from scipy.ndimage import zoom
    h, w = shape_xy
    acc = np.zeros((h, w), np.float32)
    amp, tot = 1.0, 0
    for o in range(octaves):
        s = scale / (2 ** o)
        gh, gw = int(h / s) + 3, int(w / s) + 3
        g = rng.random((gh, gw)).astype(np.float32)
        z = zoom(g, (h / (gh - 2), w / (gw - 2)), order=3)[:h, :w]
        acc += amp * z
        tot += amp
        amp *= 0.5
    return acc / tot
