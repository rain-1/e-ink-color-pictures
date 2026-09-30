"""Shared helpers for 2026-09-30 (Zauberflöte day).

Draw at 2x in pure palette colours, then finish(): box-downsample and snap to the
nearest palette colour (clean anti-aliased-looking edges without dithering), then apply
any 1x Bayer tone layers on top. Output is palette-clean -> render with --dither none.
"""
import math, os, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, S = 400, 600, 2
K = (0, 0, 0); Wh = (255, 255, 255); R = (0xE0, 0x1B, 0x24)
Y = (0xF5, 0xD4, 0x00); B = (0x12, 0x3D, 0xB0); G = (0x1E, 0x9B, 0x3C)
PAL = np.array([K, Wh, R, Y, B, G], dtype=np.float32)

BAYER = np.array([[0, 32, 8, 40, 2, 34, 10, 42], [48, 16, 56, 24, 50, 18, 58, 26],
                  [12, 44, 4, 36, 14, 46, 6, 38], [60, 28, 52, 20, 62, 30, 54, 22],
                  [3, 35, 11, 43, 1, 33, 9, 41], [51, 19, 59, 27, 49, 17, 57, 25],
                  [15, 47, 7, 39, 13, 45, 5, 37], [63, 31, 55, 23, 61, 29, 53, 21]]) / 64.0 + 1 / 128
BAY = np.tile(BAYER, (H // 8 + 1, W // 8 + 1))[:H, :W]


def font(size, bold=False, serif=True):
    names = (["DejaVuSerif-Bold.ttf", "DejaVuSerif.ttf"] if serif else ["DejaVuSans-Bold.ttf", "DejaVuSans.ttf"])
    for base in ["/usr/share/fonts/truetype/dejavu/", ""]:
        try:
            return ImageFont.truetype(base + (names[0] if bold else names[1]), size)
        except OSError:
            pass
    return ImageFont.load_default()


class Canvas:
    def __init__(self, bg=K):
        self.im = Image.new("RGB", (W * S, H * S), bg)
        self.d = ImageDraw.Draw(self.im)
        self.tones = []

    # all coordinates in 1x units
    def P(self, pts):
        return [(x * S, y * S) for x, y in pts]

    def poly(self, pts, fill=None, outline=None, width=1):
        self.d.polygon(self.P(pts), fill=fill)
        if outline is not None:
            self.line(list(pts) + [pts[0]], outline, width)

    def line(self, pts, col, width=1):
        self.d.line(self.P(pts), fill=col, width=max(1, round(width * S)), joint="curve")

    def ell(self, cx, cy, rx, ry=None, fill=None, outline=None, width=1):
        ry = rx if ry is None else ry
        self.d.ellipse([(cx - rx) * S, (cy - ry) * S, (cx + rx) * S, (cy + ry) * S],
                       fill=fill, outline=outline, width=max(1, round(width * S)) if outline else 0)

    def rect(self, x0, y0, x1, y1, fill=None, outline=None, width=1):
        self.d.rectangle([x0 * S, y0 * S, x1 * S - 1, y1 * S - 1], fill=fill,
                         outline=outline, width=max(1, round(width * S)) if outline else 0)

    def text(self, xy, s, col, size, anchor="mm", bold=False, serif=True, spacing=0):
        f = font(size * S, bold, serif)
        if spacing:
            # letter-spaced: lay out manually around the anchor x
            widths = [f.getlength(c) + spacing * S for c in s]
            tot = sum(widths) - spacing * S
            x = xy[0] * S - (tot / 2 if anchor[0] == "m" else 0)
            for c, w in zip(s, widths):
                self.d.text((x, xy[1] * S), c, fill=col, font=f, anchor="l" + anchor[1])
                x += w
        else:
            self.d.text((xy[0] * S, xy[1] * S), s, fill=col, font=f, anchor=anchor)

    def star(self, cx, cy, r, col, points=4, inner=0.28, rot=-math.pi / 2):
        pts = []
        for i in range(points * 2):
            a = rot + i * math.pi / points
            rr = r if i % 2 == 0 else r * inner
            pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
        self.poly(pts, fill=col)

    def tone(self, mask_fn, tone, col_hi, col_lo):
        """Queue a 1x Bayer-screened fill. mask_fn(draw) draws white on an L-mode 2x mask.
        tone: float or HxW array in 0..1 (1 = all col_hi)."""
        m = Image.new("L", (W * S, H * S), 0)
        mask_fn(ImageDraw.Draw(m), S)
        self.tones.append((m, tone, col_hi, col_lo))

    def snapshot_layer(self):
        """Apply queued tones now, so later drawing sits on top of them."""
        arr = self._snap()
        for m, tone, hi, lo in self.tones:
            mm = np.asarray(m.resize((W, H), Image.BOX), dtype=np.float32) / 255 > 0.5
            t = np.broadcast_to(np.asarray(tone, dtype=np.float32), (H, W))
            on = t > BAY
            arr[mm & on] = hi
            arr[mm & ~on] = lo
        self.tones = []
        self.im = Image.fromarray(arr).resize((W * S, H * S), Image.NEAREST)
        self.d = ImageDraw.Draw(self.im)

    def _snap(self):
        """Downsample 2x -> 1x choosing, per pixel, whichever of its four sub-pixels is closest
        to the block average. Never invents a colour that isn't there (grey -> green etc.)."""
        big = np.asarray(self.im, dtype=np.float32)
        idx = ((PAL[None, None] - big[:, :, None]) ** 2).sum(-1).argmin(-1)
        big = PAL[idx]
        sub = big.reshape(H, S, W, S, 3).transpose(0, 2, 1, 3, 4).reshape(H, W, S * S, 3)
        avg = sub.mean(2, keepdims=True)
        pick = ((sub - avg) ** 2).sum(-1).argmin(-1)
        return np.take_along_axis(sub, pick[..., None, None], 2)[:, :, 0].astype(np.uint8)

    def finish(self):
        self.snapshot_layer()
        out = Image.fromarray(self._snap())
        out.save(os.environ.get("OUT_RAW", "out.png"))
        return out


def oval(cx, cy, rx, ry, ang=0.0, n=36):
    ca, sa = math.cos(ang), math.sin(ang)
    return [(cx + rx * math.cos(t) * ca - ry * math.sin(t) * sa, cy + rx * math.cos(t) * sa + ry * math.sin(t) * ca)
            for t in np.linspace(0, 2 * math.pi, n, endpoint=False)]


def bird(c, x, y, s=1.0, f=1, body=R, wing=B, belly=Y, head=None, beak=Y, tilt=-0.3, legs=True, flying=False, crest=False):
    """A little songbird standing on (x, y) = feet. f = +1 faces right, -1 left."""
    head = head or body
    bx, by = x - 1 * s * f, y - 11 * s
    a = tilt * f
    tail = [(bx - 7 * s * f, by + 1 * s), (bx - 22 * s * f, by + 9 * s), (bx - 23 * s * f, by + 13 * s), (bx - 5 * s * f, by + 5 * s)]
    c.poly(tail, fill=wing, outline=K, width=0.7)
    c.line([(bx - 8 * s * f, by + 3 * s), (bx - 22 * s * f, by + 11 * s)], K, 0.5)
    if legs and not flying:
        for dx in (-2, 2):
            c.line([(bx + dx * s * f, by + 5 * s), (x + dx * s * f, y)], K, 0.9)
            c.line([(x + dx * s * f - 2.5 * s, y), (x + dx * s * f + 2.5 * s, y)], K, 0.9)
    c.poly(oval(bx, by, 10 * s, 6.8 * s, a), fill=body, outline=K, width=0.8)
    c.poly(oval(bx + 3 * s * f, by + 2.5 * s, 6 * s, 3.8 * s, a), fill=belly)
    hx, hy = bx + 9 * s * f, by - 6 * s
    if crest:
        c.poly([(hx - 2 * s * f, hy - 4 * s), (hx - 7 * s * f, hy - 12 * s), (hx + 1 * s * f, hy - 5 * s)], fill=head, outline=K, width=0.6)
    c.ell(hx, hy, 5.4 * s, fill=head, outline=K, width=0.8)
    c.poly([(hx + 4 * s * f, hy - 1.8 * s), (hx + 10 * s * f, hy + 0.6 * s), (hx + 4 * s * f, hy + 2 * s)], fill=beak, outline=K, width=0.5)
    c.ell(hx + 1.8 * s * f, hy - 1 * s, 1.7 * s, fill=Wh); c.ell(hx + 2.1 * s * f, hy - 1 * s, 0.9 * s, fill=K)
    if flying:
        wp = [(bx - 2 * s * f, by - 2 * s), (bx - 10 * s * f, by - 22 * s), (bx + 2 * s * f, by - 18 * s), (bx + 5 * s * f, by - 3 * s)]
    else:
        wp = [(bx + 5 * s * f, by - 3 * s), (bx - 4 * s * f, by - 4 * s), (bx - 14 * s * f, by + 3 * s), (bx - 2 * s * f, by + 3.5 * s)]
    c.poly(wp, fill=wing, outline=K, width=0.8)
    for k in range(1, 4):
        t = k / 4
        p0 = (wp[0][0] * (1 - t) + wp[3][0] * t, wp[0][1] * (1 - t) + wp[3][1] * t)
        p1 = (wp[1][0] * (1 - t) + wp[2][0] * t, wp[1][1] * (1 - t) + wp[2][1] * t)
        c.line([p0, ((p0[0] + p1[0]) / 2 * 0.6 + p1[0] * 0.4, (p0[1] + p1[1]) / 2 * 0.6 + p1[1] * 0.4)], K, 0.5)


def vnoise(h, w, cell, seed=0):
    """Smooth value noise, h x w, features ~cell px."""
    rng = np.random.default_rng(seed)
    gh, gw = h // cell + 3, w // cell + 3
    g = rng.random((gh, gw)).astype(np.float32)
    ys, xs = np.arange(h) / cell, np.arange(w) / cell
    y0, x0 = ys.astype(int), xs.astype(int)
    fy, fx = ys - y0, xs - x0
    fy, fx = fy * fy * (3 - 2 * fy), fx * fx * (3 - 2 * fx)
    a = g[y0][:, x0]; b = g[y0][:, x0 + 1]; c_ = g[y0 + 1][:, x0]; d = g[y0 + 1][:, x0 + 1]
    top = a + (b - a) * fx[None]; bot = c_ + (d - c_) * fx[None]
    return top + (bot - top) * fy[:, None]


def paste_1x(c, rgb, mask):
    """Paste a 1x HxWx3 uint8 array onto the canvas where mask (HxW bool) is set."""
    c.snapshot_layer()
    arr = np.asarray(c.im.resize((W, H), Image.NEAREST)).copy()
    arr[mask] = rgb[mask]
    c.im = Image.fromarray(arr).resize((W * S, H * S), Image.NEAREST)
    c.d = ImageDraw.Draw(c.im)
