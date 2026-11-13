"""Small drawing kit for palette-pure pieces (2026-11-13).

Everything is drawn as 1-bit masks (supersampled, then thresholded) and stamped onto an
index canvas in one of the six panel colours, optionally through a pattern (hatch, dots,
Bayer tone). No anti-aliasing ever reaches the output, so no colour fringes: render with
`--dither none`.
"""
import os, math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageChops

W, H = 400, 600
K, WH, R, Y, B, G = 0, 1, 2, 3, 4, 5
RGB = np.array([(0, 0, 0), (255, 255, 255), (0xE0, 0x1B, 0x24), (0xF5, 0xD4, 0x00),
                (0x12, 0x3D, 0xB0), (0x1E, 0x9B, 0x3C)], np.uint8)
_F = "/usr/share/fonts/truetype/"
FONTS = {"serif": _F + "freefont/FreeSerif.ttf", "serif-i": _F + "freefont/FreeSerifItalic.ttf",
         "serif-b": _F + "freefont/FreeSerifBold.ttf", "serif-bi": _F + "freefont/FreeSerifBoldItalic.ttf",
         "lib": _F + "liberation/LiberationSerif-Regular.ttf", "lib-i": _F + "liberation/LiberationSerif-Italic.ttf",
         "lib-b": _F + "liberation/LiberationSerif-Bold.ttf", "lib-bi": _F + "liberation/LiberationSerif-BoldItalic.ttf",
         "dserif": _F + "dejavu/DejaVuSerif.ttf", "dserif-b": _F + "dejavu/DejaVuSerif-Bold.ttf",
         "sans": _F + "dejavu/DejaVuSans.ttf", "sans-b": _F + "dejavu/DejaVuSans-Bold.ttf"}
YY, XX = np.mgrid[0:H, 0:W]
_B4 = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]])
_B8 = np.block([[4 * _B4, 4 * _B4 + 2], [4 * _B4 + 3, 4 * _B4 + 1]])
BAYER = (np.tile(_B8, (H // 8 + 1, W // 8 + 1))[:H, :W] + 0.5) / 64.0


# ---- patterns: boolean H×W arrays -------------------------------------------------
def hatch(angle=45, period=4, width=1, phase=0.0):
    a = math.radians(angle)
    return ((XX * math.sin(a) + YY * math.cos(a) + phase) % period) < width

def cross(angle=45, period=4, width=1):
    return hatch(angle, period, width) | hatch(angle + 90, period, width)

def dots(period=6, r=1.0, stagger=True, ox=0, oy=0):
    row = ((YY - oy) // period).astype(int)
    x = (XX - ox + (row % 2) * period / 2 * stagger) % period - period / 2
    y = (YY - oy) % period - period / 2
    return x * x + y * y <= r * r

def tone(t):
    """Bayer screen of a tone value (scalar or H×W array), 0 = none, 1 = solid."""
    return BAYER < t

def checker(n=4, ox=0, oy=0):
    return (((XX - ox) // n + (YY - oy) // n) % 2) == 0

def speckle(p, seed=0):
    return np.random.default_rng(seed).random((H, W)) < p

def grow(m, n=1):
    for _ in range(n):
        m = m | np.roll(m, 1, 0) | np.roll(m, -1, 0) | np.roll(m, 1, 1) | np.roll(m, -1, 1)
    return m

def depth(m, n):
    """How many pixels inside mask m each pixel is (0 outside, capped at n)."""
    d = np.zeros(m.shape, np.int32); cur = m.copy()
    for i in range(n):
        d += cur
        e = cur & np.roll(cur, 1, 0) & np.roll(cur, -1, 0) & np.roll(cur, 1, 1) & np.roll(cur, -1, 1)
        if i % 2:  # alternate 4- and 8-neighbourhoods for rounder contours
            e &= np.roll(np.roll(cur, 1, 0), 1, 1) & np.roll(np.roll(cur, -1, 0), -1, 1) \
               & np.roll(np.roll(cur, 1, 0), -1, 1) & np.roll(np.roll(cur, -1, 0), 1, 1)
        cur = e
    return d


# ---- geometry ---------------------------------------------------------------------
def bez(p0, p1, p2, p3, n=20):
    out = []
    for i in range(n + 1):
        t = i / n; u = 1 - t
        out.append((u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0],
                    u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1]))
    return out

def smooth(pts, closed=True, n=8):
    """Catmull-Rom through pts."""
    P = list(pts); out = []; N = len(P)
    rng = range(N) if closed else range(N - 1)
    for i in rng:
        if closed:
            p0, p1, p2, p3 = P[i - 1], P[i], P[(i + 1) % N], P[(i + 2) % N]
        else:
            p0, p1, p2, p3 = P[max(i - 1, 0)], P[i], P[i + 1], P[min(i + 2, N - 1)]
        for k in range(n):
            t = k / n
            out.append(tuple(0.5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t * t
                             + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t**3) for j in (0, 1)))
    if not closed: out.append(P[-1])
    return out

def arc(cx, cy, rx, ry, a0, a1, n=24):
    return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
             cy + ry * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]

def star(cx, cy, r1, r2, n=5, rot=-90):
    return [(cx + (r1 if i % 2 == 0 else r2) * math.cos(math.radians(rot + 180 * i / n)),
             cy + (r1 if i % 2 == 0 else r2) * math.sin(math.radians(rot + 180 * i / n))) for i in range(2 * n)]

_fc = {}
def font(name, px):
    k = (name, px)
    if k not in _fc: _fc[k] = ImageFont.truetype(FONTS[name], px)
    return _fc[k]


class Layer:
    """A 1-bit drawing surface in user coordinates (400×600), supersampled ss×."""
    def __init__(s, c, ss=4):
        s.c, s.ss = c, ss
        s.im = Image.new("L", (W * ss, H * ss), 0); s.d = ImageDraw.Draw(s.im)
    def _p(s, pts): return [(x * s.ss, y * s.ss) for x, y in pts]
    def poly(s, pts, v=255): s.d.polygon(s._p(pts), fill=v); return s
    def line(s, pts, w=1.0, v=255, closed=False):
        p = s._p(pts)
        if closed: p = p + [p[0]]
        s.d.line(p, fill=v, width=max(1, round(w * s.ss)), joint="curve"); return s
    def seg(s, x0, y0, x1, y1, w=1.0, v=255): return s.line([(x0, y0), (x1, y1)], w, v)
    def rect(s, x0, y0, x1, y1, v=255):
        s.d.rectangle([x0 * s.ss, y0 * s.ss, x1 * s.ss - 1, y1 * s.ss - 1], fill=v); return s
    def ellipse(s, cx, cy, rx, ry, v=255):
        s.d.ellipse([(cx - rx) * s.ss, (cy - ry) * s.ss, (cx + rx) * s.ss, (cy + ry) * s.ss], fill=v); return s
    def circle(s, cx, cy, r, v=255): return s.ellipse(cx, cy, r, r, v)
    def ring(s, cx, cy, r, w=1.0, v=255):
        s.d.ellipse([(cx - r) * s.ss, (cy - r) * s.ss, (cx + r) * s.ss, (cy + r) * s.ss],
                    outline=v, width=max(1, round(w * s.ss))); return s
    def text(s, x, y, t, f="serif", size=12, anchor="mm", angle=0, track=0.0, v=255):
        fo = font(f, int(round(size * s.ss)))
        if track:
            wd = sum(fo.getlength(ch) for ch in t) + track * s.ss * (len(t) - 1)
            tmp = Image.new("L", (int(wd) + 8 * s.ss, int(size * s.ss * 2)), 0); td = ImageDraw.Draw(tmp)
            xx = 4 * s.ss
            for ch in t:
                td.text((xx, size * s.ss), ch, font=fo, fill=255, anchor="ls"); xx += fo.getlength(ch) + track * s.ss
            box = tmp.getbbox(); tmp = tmp.crop(box)
        else:
            l, tp, r, b = fo.getbbox(t, anchor="ls")
            tmp = Image.new("L", (r - l + 4, b - tp + 4), 0)
            ImageDraw.Draw(tmp).text((2 - l, 2 - tp), t, font=fo, fill=255, anchor="ls")
        if angle: tmp = tmp.rotate(angle, expand=True, resample=Image.BICUBIC)
        tw, th = tmp.size
        ax = {"l": 0, "m": tw / 2, "r": tw}[anchor[0]]; ay = {"t": 0, "m": th / 2, "b": th}[anchor[1]]
        px, py = int(x * s.ss - ax), int(y * s.ss - ay)
        if v == 255:
            reg = s.im.crop((px, py, px + tw, py + th)); s.im.paste(ImageChops.lighter(reg, tmp), (px, py))
        else:
            s.im.paste(0, (px, py), tmp)
        return s
    def mask(s, thr=0.5):
        if s.ss == 1: return np.asarray(s.im) > 127
        return np.asarray(s.im.resize((W, H), Image.BOX)) > thr * 255
    def put(s, col, pat=None, thr=0.5):
        m = s.mask(thr); s.c.put(m, col, pat); return m


class Canvas:
    def __init__(s, bg=WH):
        s.a = np.full((H, W), bg, np.uint8); s.clip = None
    def layer(s, ss=4): return Layer(s, ss)
    def put(s, m, col, pat=None):
        if pat is not None: m = m & pat
        if s.clip is not None: m = m & s.clip
        s.a[m] = col
    def fill(s, col, pat=None): s.put(np.ones((H, W), bool), col, pat)
    # one-shot helpers
    def poly(s, pts, col, pat=None, ss=4):
        return s.layer(ss).poly(pts).put(col, pat)
    def line(s, pts, col, w=1.0, closed=False, pat=None, thr=0.35):
        return s.layer(4).line(pts, w, closed=closed).put(col, pat, thr)
    def hair(s, pts, col, closed=False):
        """True 1-px line, never broken."""
        return s.layer(1).line(pts, 1, closed=closed).put(col)
    def text(s, x, y, t, col, f="serif", size=12, anchor="mm", angle=0, track=0.0, thr=0.42, halo=None, hw=1):
        m = s.tmask(x, y, t, f, size, anchor, angle, track, thr)
        if halo is not None: s.put(grow(m, hw), halo)
        s.put(m, col); return m
    def tmask(s, x, y, t, f="serif", size=12, anchor="mm", angle=0, track=0.0, thr=0.42):
        """Text as a mask. Small upright text is drawn 1:1 with the font's own mono hinting
        (use lib / lib-i / dserif / sans for that); display sizes are supersampled."""
        if size <= 13 and not angle and not track:
            L = s.layer(1); L.d.fontmode = "1"
            L.d.text((round(x), round(y)), t, font=font(f, int(round(size))), fill=255, anchor=anchor[0] + {"t": "a", "m": "m", "b": "s"}[anchor[1]])
            return L.mask()
        return s.layer(4).text(x, y, t, f, size, anchor, angle, track).mask(thr)
    def image(s): return Image.fromarray(RGB[s.a])
    def save(s, default="preview.png"): s.image().save(os.environ.get("OUT_RAW", default))
