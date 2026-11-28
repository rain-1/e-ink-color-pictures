"""Shared toolkit for the 2026-11-28 pieces (Blake's birthday).

Print-shop pipeline:
  * a *colour layer* painted freely in RGB at 3x, downsampled, then screened to the six
    inks by pair-mixing (each pixel = the best blend of two palette inks, Bayer 8x8).
    That gives orange, olive, navy, pink, teal... as tidy two-ink screens.
  * *ink layers* drawn at 3x in pure palette colours, laid on top un-dithered, so line
    work stays crisp.
Output is palette-pure 400x600; render with --dither none.
"""
import os, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, S = 400, 600, 3
PAL = {"k": (0, 0, 0), "w": (255, 255, 255), "r": (0xE0, 0x1B, 0x24),
       "y": (0xF5, 0xD4, 0x00), "b": (0x12, 0x3D, 0xB0), "g": (0x1E, 0x9B, 0x3C)}
K, WH, R, Y, B, G = (PAL[c] for c in "kwrybg")
_P = np.array(list(PAL.values()), dtype=np.float32)


def mix(a, b, t):
    return tuple(int(round(a[i] * (1 - t) + b[i] * t)) for i in range(3))


# handy secondary colours (all lie on a segment between two inks)
ORANGE, AMBER = mix(R, Y, .5), mix(R, Y, .75)
CREAM, PALE = mix(WH, Y, .3), mix(WH, Y, .12)
PINK, MAROON = mix(WH, R, .45), mix(R, K, .5)
SKY, NAVY, MID = mix(WH, B, .35), mix(B, K, .55), mix(B, K, .25)
LIME, OLIVE = mix(Y, G, .5), mix(Y, K, .45)
FOREST, MINT, TEAL = mix(G, K, .5), mix(WH, G, .4), mix(B, G, .5)
GREY, DGREY, LGREY = mix(WH, K, .5), mix(WH, K, .75), mix(WH, K, .2)
PURPLE = mix(R, B, .5)

_B8 = None
def bayer8():
    global _B8
    if _B8 is None:
        m = np.array([[0, 2], [3, 1]])
        for _ in range(2):
            m = np.block([[4 * m, 4 * m + 2], [4 * m + 3, 4 * m + 1]])
        _B8 = (m + .5) / 64
    return _B8


def screen(rgb):
    """HxWx3 float -> HxW palette index, pair-mix ordered dither."""
    h, w, _ = rgb.shape
    c = rgb.reshape(-1, 3).astype(np.float32)
    best = np.full(len(c), 1e18, np.float32)
    ia = np.zeros(len(c), np.int8); ib = np.zeros(len(c), np.int8)
    tt = np.zeros(len(c), np.float32)
    for i in range(6):
        for j in range(i + 1, 6):
            a, b = _P[i], _P[j]
            d = b - a; L = (d * d).sum()
            t = np.clip(((c - a) @ d) / L, 0, 1)
            e = c - (a + t[:, None] * d)
            cost = (e * e).sum(1) + 0.03 * L * t * (1 - t)   # prefer low-contrast pairs
            m = cost < best
            best[m] = cost[m]; ia[m] = i; ib[m] = j; tt[m] = t[m]
    th = np.tile(bayer8(), (h // 8 + 1, w // 8 + 1))[:h, :w].reshape(-1)
    return np.where(tt > th, ib, ia).reshape(h, w)


def fbm(seed, scale=64, octaves=4, w=W, h=H, gain=.5):
    """Smooth value noise in 0..1, shape (h, w)."""
    rng = np.random.default_rng(seed)
    out = np.zeros((h, w), np.float32); amp = 1; tot = 0
    for o in range(octaves):
        s = max(2, int(scale / 2 ** o))
        g = rng.random((h // s + 3, w // s + 3)).astype(np.float32)
        im = Image.fromarray((g * 255).astype(np.uint8)).resize(((w // s + 3) * s, (h // s + 3) * s), Image.BICUBIC)
        out += amp * np.asarray(im, np.float32)[s:s + h, s:s + w] / 255
        tot += amp; amp *= gain
    return out / tot


def font(size, style="Italic", fam="serif"):
    paths = {"serif": "/usr/share/fonts/truetype/liberation/LiberationSerif-%s.ttf",
             "cal": "/usr/share/fonts/truetype/crosextra/Caladea-%s.ttf"}
    return ImageFont.truetype(paths[fam] % style, int(size * S))


class Art:
    def __init__(self, bg=WH, crisp=False):
        self.crisp = crisp
        self.col = Image.new("RGB", (W * S, H * S), bg)
        self.c = ImageDraw.Draw(self.col)
        self.inks = []          # (rgb, L image) in stacking order
        self.post = None        # optional fn(rgb_float_small) -> rgb_float_small

    def ink(self, rgb=K):
        im = Image.new("L", (W * S, H * S), 0)
        self.inks.append((rgb, im))
        return ImageDraw.Draw(im)

    def ink_image(self, rgb, im):
        self.inks.append((rgb, im))

    def finish(self):
        if self.crisp:
            # pure palette colours in the colour layer stay crisp; everything else is a tone
            big = np.asarray(self.col, np.float32)
            sub = big.reshape(H, S, W, S, 3).transpose(0, 2, 1, 3, 4).reshape(H, W, S * S, 3)
            pure = np.full((H, W, S * S), -1, np.int8)
            for i, pc in enumerate(_P):
                pure[(sub == pc).all(-1)] = i
            tone = pure < 0; nt = tone.sum(-1)
            mean = (sub * tone[..., None]).sum(2) / np.maximum(nt, 1)[..., None]
            idx = screen(mean)
            cnt = np.stack([(pure == i).sum(-1) for i in range(6)], -1)
            best = cnt.argmax(-1); bc = cnt.max(-1)
            idx = np.where((bc >= 5) | (bc > nt) | (cnt[..., 0] >= 4), np.where(cnt[..., 0] >= 4, 0, best), idx)
            out = _P[idx].astype(np.uint8)
        else:
            small = np.asarray(self.col.resize((W, H), Image.LANCZOS), np.float32)
            if self.post:
                small = self.post(small)
            out = _P[screen(np.clip(small, 0, 255))].astype(np.uint8)
        for rgb, im in self.inks:
            m = np.asarray(im.resize((W, H), Image.LANCZOS)) > 110
            out[m] = rgb
        Image.fromarray(out, "RGB").save(os.environ.get("OUT_RAW", "out.png"))


# ---------- drawing helpers (coordinates in panel px; scaled by S here) ----------
def P(pts):
    return [(x * S, y * S) for x, y in pts]


def line(d, pts, fill=255, w=1.0):
    d.line(P(pts), fill=fill, width=max(1, int(round(w * S))), joint="curve")


def poly(d, pts, fill=255, outline=None, w=1.0):
    d.polygon(P(pts), fill=fill)
    if outline is not None:
        d.line(P(list(pts) + [pts[0]]), fill=outline, width=max(1, int(round(w * S))), joint="curve")


def disc(d, x, y, r, fill=255, outline=None, w=1.0):
    d.ellipse([(x - r) * S, (y - r) * S, (x + r) * S, (y + r) * S], fill=fill,
              outline=outline, width=max(1, int(round(w * S))) if outline is not None else 0)


def ell(d, x, y, rx, ry, fill=255, outline=None, w=1.0):
    d.ellipse([(x - rx) * S, (y - ry) * S, (x + rx) * S, (y + ry) * S], fill=fill,
              outline=outline, width=max(1, int(round(w * S))) if outline is not None else 0)


def bez(p0, p1, p2, p3, n=24):
    out = []
    for i in range(n + 1):
        t = i / n; u = 1 - t
        out.append((u**3 * p0[0] + 3 * u*u*t * p1[0] + 3 * u*t*t * p2[0] + t**3 * p3[0],
                    u**3 * p0[1] + 3 * u*u*t * p1[1] + 3 * u*t*t * p2[1] + t**3 * p3[1]))
    return out


def leaf(cx, cy, ang, L, wd, n=14):
    """Pointed leaf outline starting at (cx,cy), growing along ang."""
    ca, sa = math.cos(ang), math.sin(ang)
    top, bot = [], []
    for i in range(n + 1):
        t = i / n
        hw = wd * math.sin(math.pi * t) ** .8 * (1 - .35 * t)
        x, y = L * t, hw
        top.append((cx + x * ca - y * sa, cy + x * sa + y * ca))
        bot.append((cx + x * ca + y * sa, cy + x * sa - y * ca))
    return top + bot[::-1]


def text(d, xy, s, f, fill=255, anchor="mm"):
    d.text((xy[0] * S, xy[1] * S), s, font=f, fill=fill, anchor=anchor)


def border(art, rgb=K, inset=6, w=1.5, inner=3):
    d = art.ink(rgb)
    for k, ww in ((inset, w), (inset + inner, .7)):
        d.rectangle([k * S, k * S, (W - k) * S, (H - k) * S], outline=255, width=max(1, int(ww * S)))
    return d
