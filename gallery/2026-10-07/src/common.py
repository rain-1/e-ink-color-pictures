"""Shared helpers for 2026-10-07 ("The Far Side").

Everything composes at native 400x600 so ordered screens stay crisp; vector
detail is drawn on a 2x layer and composited, then the result is snapped to
the six inks.
"""
import math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 400, 600
INK = {
    "K": (0, 0, 0), "W": (255, 255, 255), "R": (0xE0, 0x1B, 0x24),
    "Y": (0xF5, 0xD4, 0x00), "B": (0x12, 0x3D, 0xB0), "G": (0x1E, 0x9B, 0x3C),
}
PAL = np.array(list(INK.values()), np.float32)

_b = np.array([[0]])
for _ in range(3):
    _b = np.block([[4 * _b, 4 * _b + 2], [4 * _b + 3, 4 * _b + 1]])
BAYER = (_b + 0.5) / 64.0  # 8x8, values in (0,1)


def bayer(h=H, w=W, ox=0, oy=0):
    return np.tile(BAYER, (h // 8 + 2, w // 8 + 2))[oy:oy + h, ox:ox + w]


def ramp(t, stops):
    """Ordered-screened gradient. t: HxW in [0,1]; stops: ink letters."""
    t = np.clip(t, 0, 1) * (len(stops) - 1)
    i = np.minimum(t.astype(int), len(stops) - 2)
    f = t - i
    th = bayer(*t.shape)
    k = i + (f > th)
    cols = np.array([INK[s] for s in stops], np.uint8)
    return cols[k]


def snap(arr):
    a = np.asarray(arr, np.float32)[..., :3]
    d = ((a[..., None, :] - PAL) ** 2).sum(-1)
    out = PAL[d.argmin(-1)].astype(np.uint8)
    # the inks have no greys: neutral pixels go to black or white by brightness
    grey = (a.max(-1) - a.min(-1)) < 36
    out[grey] = np.where((a.mean(-1) > 140)[grey, None], 255, 0)
    return out


def fs_dither(gray_rgb, inks):
    """Floyd–Steinberg onto a subset of inks (row-vectorised serpentine-free)."""
    pal = np.array([INK[s] for s in inks], np.float32)
    buf = np.asarray(gray_rgb, np.float32).copy()
    h, w, _ = buf.shape
    out = np.zeros((h, w), int)
    for y in range(h):
        row = buf[y]
        for x in range(w):
            old = row[x]
            i = int(((pal - old) ** 2).sum(1).argmin())
            out[y, x] = i
            e = old - pal[i]
            if x + 1 < w: row[x + 1] += e * 0.4375
            if y + 1 < h:
                if x > 0: buf[y + 1, x - 1] += e * 0.1875
                buf[y + 1, x] += e * 0.3125
                if x + 1 < w: buf[y + 1, x + 1] += e * 0.0625
    return pal[out].astype(np.uint8)


class Layer:
    """2x supersampled RGBA drawing layer."""
    S = 2

    def __init__(self):
        self.im = Image.new("RGBA", (W * self.S, H * self.S), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.im)

    def _p(self, pts):
        return [(x * self.S, y * self.S) for x, y in pts]

    def line(self, pts, c, w=1.0):
        self.d.line(self._p(pts), fill=INK[c], width=max(1, round(w * self.S)), joint="curve")

    def poly(self, pts, c, outline=None, w=1.0):
        self.d.polygon(self._p(pts), fill=INK[c] if c else None)
        if outline:
            self.line(list(pts) + [pts[0]], outline, w)

    def rect(self, x0, y0, x1, y1, c, outline=None, w=1.0):
        self.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], c, outline, w)

    def ellipse(self, cx, cy, rx, ry, c, outline=None, w=1.0):
        s = self.S
        self.d.ellipse([(cx - rx) * s, (cy - ry) * s, (cx + rx) * s, (cy + ry) * s],
                       fill=INK[c] if c else None, outline=INK[outline] if outline else None,
                       width=max(1, round(w * s)))

    def arc(self, cx, cy, r, a0, a1, c, w=1.0):
        s = self.S
        self.d.arc([(cx - r) * s, (cy - r) * s, (cx + r) * s, (cy + r) * s], a0, a1,
                   fill=INK[c], width=max(1, round(w * s)))

    def text(self, xy, s, c, size=12, font="sans", anchor="la"):
        self.d.text((xy[0] * self.S, xy[1] * self.S), s, fill=INK[c], font=F(font, size * self.S), anchor=anchor)

    def onto(self, base):
        """Composite onto an HxWx3 uint8 base; returns snapped array."""
        small = self.im.convert("RGBa").resize((W, H), Image.LANCZOS).convert("RGBA")
        a = np.asarray(small, np.float32)
        al = a[..., 3:4] / 255.0
        # hard-ish alpha: coverage > 0.45 wins, keeps lines crisp after snapping
        al = (al > 0.4).astype(np.float32)
        rgb = snap(a[..., :3]).astype(np.float32)
        out = base.astype(np.float32) * (1 - al) + rgb * al
        return snap(out)


FONTS = {
    "sans": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "sansb": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "cond": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "serif": "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    "serifb": "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "mono": "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    "monob": "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
}
_fc = {}


def F(name, size):
    k = (name, size)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(FONTS[name], int(size))
    return _fc[k]


def save(arr):
    Image.fromarray(np.asarray(arr, np.uint8)).save(os.environ.get("OUT_RAW", "out.png"))


# ---------------------------------------------------------------- the Moon
def sph(lat, lon):
    la, lo = np.radians(lat), np.radians(lon)
    return np.array([np.cos(la) * np.cos(lo), np.cos(la) * np.sin(lo), np.sin(la)])


R_MOON = 1737.0
NAMED = [  # name, lat, lon(E), diameter km, kind
    ("Mare Moscoviense", 27, 148, 280, "mare"),
    ("Tsiolkovskiy", -21, 129, 185, "dark"),
    ("Mare Crisium", 17, 59, 556, "mare"),
    ("Mare Marginis", 13, 86, 360, "mare"),
    ("Mare Smythii", -2, 87, 370, "mare"),
    ("Mare Humboldtianum", 57, 81, 270, "mare"),
    ("Mare Ingenii", -34, 163, 300, "mare"),
    ("Apollo", -36, -151, 540, "basin"),
    ("Korolev", -4, -157, 430, "basin"),
    ("Hertzsprung", 2, -129, 570, "basin"),
    ("Mendeleev", 6, 141, 313, "basin"),
    ("Giordano Bruno", 36, 103, 22, "rays"),
    ("Jackson", 22, -163, 71, "rays"),
    ("Lomonosov", 27, 98, 92, "crater"),
    ("Jules Verne", -35, 147, 143, "crater"),
    ("Gagarin", -20, 149, 262, "basin"),
    ("Freundlich-Sharonov", 19, 175, 600, "basin"),
    ("Orientale", -19, -93, 930, "basin"),
    ("South Pole-Aitken", -53, -169, 2500, "spa"),
    ("Daedalus", -6, 180, 93, "crater"),
    ("Langmuir", -9, -129, 91, "crater"),
]


def craters(n=1400, seed=1959):
    """Random crater population (lat, lon, diam km, kind) plus the named ones."""
    rng = np.random.default_rng(seed)
    z = rng.uniform(-1, 1, n)
    lon = rng.uniform(-180, 180, n)
    lat = np.degrees(np.arcsin(z))
    # power-law sizes: many small, few large
    u = rng.uniform(0, 1, n)
    d = 8 * (1 - u) ** (-1 / 1.25)
    d = np.clip(d, 8, 260)
    out = [(a, b, c, "crater") for a, b, c in zip(lat, lon, d)]
    for name, la, lo, dd, k in NAMED:
        out.append((la, lo, dd, k))
    return out


def ortho_grid(lat0, lon0, cx, cy, r, h=H, w=W, ss=1):
    """Pixel grid -> unit-sphere points for an orthographic view. Returns (P, mask, nz)."""
    ys, xs = np.mgrid[0:h * ss, 0:w * ss].astype(np.float32) / ss
    x = (xs - cx) / r
    y = -(ys - cy) / r
    rr = x * x + y * y
    mask = rr < 1
    zc = np.sqrt(np.clip(1 - rr, 0, 1))
    V = sph(lat0, lon0)
    E = np.array([-np.sin(np.radians(lon0)), np.cos(np.radians(lon0)), 0.0])
    N = np.cross(V, E)
    P = x[..., None] * E + y[..., None] * N + zc[..., None] * V
    return P.astype(np.float32), mask, zc


# geologic units, oldest first
UNITS = ["pIt", "SPA", "pNc", "Nb", "Nc", "Ic", "Im", "Ec", "Cc"]
U = {k: i for i, k in enumerate(UNITS)}


def moon(lat0, lon0, cx, cy, r, seed=1959, n=2200):
    """Render fields for an orthographic Moon: height (px), unit id, albedo, mask, rays."""
    P, mask, zc = ortho_grid(lat0, lon0, cx, cy, r)
    pts = P[mask]                              # (M,3)
    M = len(pts)
    h = np.zeros(M, np.float32)
    unit = np.full(M, U["pIt"], np.int8)
    alb = np.zeros(M, np.float32)
    ray = np.zeros(M, np.float32)
    rng = np.random.default_rng(seed)
    cr = craters(n, seed)
    ages = []
    for la, lo, d, kind in cr:
        if kind in ("spa",): a = 0
        elif kind in ("basin", "mare"): a = rng.choice([2, 3], p=[.5, .5])
        elif kind == "dark": a = 4
        elif kind == "rays": a = 8
        else: a = int(rng.choice([2, 4, 5, 7, 8], p=[.36, .26, .2, .12, .06]))
        ages.append(a)
    order = sorted(range(len(cr)), key=lambda i: (ages[i], -cr[i][2]))
    for i in order:
        la, lo, d, kind = cr[i]; age = ages[i]
        c = sph(la, lo).astype(np.float32)
        R = d / 2 / R_MOON
        cosmax = math.cos(min(R * 2.6, math.pi))
        dots = pts @ c
        sel = dots > cosmax
        if not sel.any():
            continue
        q = np.arccos(np.clip(dots[sel], -1, 1)) / R
        Rp = R * r                              # crater radius in px
        big = d > 300
        depth = Rp * (0.22 if d < 30 else 0.22 * (30 / d) ** 0.55)
        if kind == "spa":
            dh = -Rp * 0.04 * np.clip(1 - q * q, 0, 1) + Rp * 0.01 * np.exp(-((q - 1) / 0.12) ** 2)
        elif big or kind == "basin":
            dh = (-depth * 0.5 * (q < 0.95) * (1 - (q / 0.95) ** 6)
                  + depth * 0.35 * np.exp(-((q - 1) / 0.07) ** 2)
                  + depth * 0.15 * np.exp(-((q - 0.62) / 0.05) ** 2)
                  + depth * 0.05 * np.clip(q, 1.05, None) ** -2.5 * (q > 1.05))
        else:
            flo = np.clip(1 - q * q, 0, 1)
            if d > 25: flo = np.minimum(flo, 0.7) / 0.7
            dh = -depth * flo + depth * 0.45 * np.exp(-((q - 1) / 0.13) ** 2) \
                 + depth * 0.25 * np.clip(q, 1, None) ** -3 * (q > 1)
            if d > 45:
                dh += depth * 0.5 * np.exp(-(q / 0.16) ** 2)
        # older craters are softened
        soft = {0: .4, 2: .55, 3: .7, 4: .8, 5: .9, 7: 1, 8: 1}[age]
        h[sel] += dh * soft
        # geology
        inner = q < (1.35 if kind not in ("spa", "basin", "mare") else 1.0)
        idx = np.where(sel)[0]
        if kind == "spa":
            unit[idx[q < 0.85]] = U["SPA"]
        elif kind in ("basin", "mare"):
            unit[idx[(q < 1.45) & (q > 0.3)]] = U["Nb"]
            unit[idx[q <= 0.3]] = U["Nb"]
        else:
            unit[idx[inner]] = age
        if kind in ("mare",):
            mm = q < 0.72 + 0.08 * np.sin(np.arctan2(*(pts[sel][:, :2].T)) * 5)
            unit[idx[mm]] = U["Im"]; alb[idx[mm]] = -0.45
        if kind == "dark":
            mm = q < 0.62
            unit[idx[mm]] = U["Im"]; alb[idx[mm]] = -0.5
            h[idx] += depth * 0.6 * np.exp(-(q / 0.12) ** 2)
        if age >= 7:
            ej = (q < 1.6)
            alb[idx[ej]] += 0.25 * (1.6 - q[ej]) / 1.6 * (2 if age == 8 else 1)
        if age == 8 and (kind == "rays" or d > 30):
            # bright ray system: spokes reaching ~12 radii
            t = np.cross(c, np.array([0, 0, 1], np.float32)); t /= np.linalg.norm(t) + 1e-9
            b = np.cross(c, t)
            far = dots > math.cos(min(R * 14, 1.2))
            qq = np.arccos(np.clip(dots[far], -1, 1)) / R
            v = pts[far] - dots[far, None] * c
            ang = np.arctan2(v @ b, v @ t)
            k = rng.integers(9, 16)
            phase = rng.uniform(0, 6.3)
            spokes = np.abs(np.sin(ang * k / 2 + phase)) ** 18 + 0.4 * np.abs(np.sin(ang * (k + 3) / 2 + 1.3 * phase)) ** 30
            fall = np.clip(1 - qq / 14, 0, 1) * (qq > 1.2)
            ray[np.where(far)[0]] = np.maximum(ray[np.where(far)[0]], spokes * fall)
    full = lambda v, fill=0: (lambda o: (o.__setitem__(mask, v), o)[1])(np.full(mask.shape, fill, v.dtype))
    return dict(mask=mask, P=P, zc=zc, h=full(h), unit=full(unit, -1), alb=full(alb), ray=full(ray))
