# Shared helpers for 2026-10-01 (the Tōkaidō, 1833 / 1964).
# Everything draws directly in palette colours at 1x so nothing needs dithering afterwards;
# tone comes from an 8x8 Bayer screen applied inside the generator.
import math, numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 400, 600
K, Wh, R, Y, B, G = (0,0,0), (255,255,255), (224,27,36), (245,212,0), (18,61,176), (30,155,60)

_b2 = np.array([[0, 2], [3, 1]])
def _bayer(n):
    m = _b2
    while m.shape[0] < n:
        m = np.block([[4*m, 4*m+2], [4*m+3, 4*m+1]])
    return (m + 0.5) / m.size
BAYER = _bayer(8)

def screen(shape):
    h, w = shape
    return np.tile(BAYER, (h // 8 + 1, w // 8 + 1))[:h, :w]

def blend(im, tone, c_lo, c_hi, mask=None):
    """Where mask, paint c_hi if tone > bayer threshold else c_lo. tone in 0..1 (H,W)."""
    a = np.array(im)
    t = screen(tone.shape)
    hi = tone > t
    m = np.ones(tone.shape, bool) if mask is None else mask
    a[m & hi] = c_hi
    a[m & ~hi] = c_lo
    return Image.fromarray(a)

def font(size, jp=False, bold=False, serif=True):
    if jp:
        return ImageFont.truetype("/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf", size)
    p = "/usr/share/fonts/truetype/dejavu/DejaVuSerif%s.ttf" if serif else "/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf"
    return ImageFont.truetype(p % ("-Bold" if bold else ""), size)

def vtext(d, x, y, s, f, fill, step=None):
    """Vertical Japanese text, one glyph per line."""
    step = step or f.size + 1
    for i, ch in enumerate(s):
        d.text((x, y + i * step), ch, font=f, fill=fill)

def cartouche(d, x, y, s, f, bg, fg, pad=4, border=K):
    n = len(s); w = f.size + 2 * pad; h = n * (f.size + 1) + 2 * pad
    d.rectangle((x, y, x + w, y + h), fill=bg, outline=border)
    vtext(d, x + pad, y + pad, s, f, fg)
    return w, h

# ---------------------------------------------------------------- figures
def traveller(d, x, y, h, robe=B, hat=Y, skin=Wh, ink=K, facing=1, stride=0.0,
              load=None, staff=False, umbrella=None):
    """A small Hiroshige-ish walker. (x,y) = feet on ground. h = total height."""
    s = h / 30.0
    # legs (bare, ink outlined)
    lx = 3 * s * (0.5 + stride)
    d.line((x - lx, y, x - 1 * s, y - 9 * s), fill=ink, width=max(1, int(1.6 * s)))
    d.line((x + lx, y, x + 1 * s, y - 9 * s), fill=ink, width=max(1, int(1.6 * s)))
    # robe: trapezoid, hitched up
    body = [(x - 4.5 * s, y - 8 * s), (x + 4.5 * s, y - 8 * s), (x + 3 * s, y - 21 * s), (x - 3 * s, y - 21 * s)]
    d.polygon(body, fill=robe, outline=ink)
    # obi
    d.line((x - 3.6 * s, y - 14 * s, x + 3.6 * s, y - 14 * s), fill=ink if robe != K else Wh, width=max(1, int(1.2 * s)))
    # arm forward
    d.line((x, y - 19 * s, x + facing * 5 * s, y - 13 * s), fill=ink, width=max(1, int(1.4 * s)))
    # head
    d.ellipse((x - 2.2 * s, y - 25 * s, x + 2.2 * s, y - 20.5 * s), fill=skin, outline=ink)
    # kasa hat: wide flat cone
    if hat is not None:
        d.polygon([(x - 7 * s, y - 22.5 * s), (x + 7 * s, y - 22.5 * s), (x, y - 28 * s)], fill=hat, outline=ink)
    if staff:
        d.line((x + facing * 6 * s, y - 20 * s, x + facing * 8 * s, y), fill=ink, width=1)
    if load == "pole":   # tenbin: shoulder pole with two baskets
        px0, px1 = x - 11 * s, x + 11 * s; py = y - 20 * s
        d.line((px0, py + 1 * s, px1, py - 1 * s), fill=ink, width=max(1, int(1.2 * s)))
        for px, pyy in ((px0, py + 1 * s), (px1, py - 1 * s)):
            d.line((px, pyy, px, pyy + 6 * s), fill=ink, width=1)
            d.polygon([(px - 4 * s, pyy + 6 * s), (px + 4 * s, pyy + 6 * s), (px + 3 * s, pyy + 12 * s), (px - 3 * s, pyy + 12 * s)],
                      fill=Y, outline=ink)
    if load == "box":    # hasami-bako on a pole over shoulder
        d.line((x - 8 * s, y - 20 * s, x + 8 * s, y - 20 * s), fill=ink, width=1)
        d.rectangle((x + 2 * s, y - 27 * s, x + 9 * s, y - 20 * s), fill=K, outline=ink)
    if load == "spear":
        d.line((x + 2 * s, y - 12 * s, x + 2 * s, y - 52 * s), fill=ink, width=1)
        d.ellipse((x - 0.5 * s, y - 56 * s, x + 4.5 * s, y - 48 * s), fill=ink)
    if umbrella is not None:
        d.line((x + facing * 2 * s, y - 15 * s, x + facing * 2 * s, y - 33 * s), fill=ink, width=1)
        d.pieslice((x - 11 * s + facing * 2 * s, y - 40 * s, x + 11 * s + facing * 2 * s, y - 26 * s), 180, 360, fill=umbrella, outline=ink)
        for k in range(-3, 4):
            d.line((x + facing * 2 * s, y - 33 * s, x + facing * 2 * s + k * 3.2 * s, y - 33 * s), fill=ink, width=1)

def pine(d, x, y, h, ink=K, needles=G, rng=None, lean=0.0):
    """Hiroshige roadside pine: crooked trunk, flat cloud-pads of needles."""
    rng = rng or np.random.default_rng(int(x * 31 + y))
    pts = [(x, y)]
    cx, cy = x, y
    for i in range(6):
        cx += lean * h / 6 + rng.normal(0, h * 0.03); cy -= h / 6
        pts.append((cx, cy))
    for i in range(len(pts) - 1):
        wdt = max(1, int(h * 0.06 * (1 - i / 7)))
        d.line((pts[i], pts[i + 1]), fill=ink, width=wdt)
    for i in range(2, len(pts)):
        px, py = pts[i]
        for side in (-1, 1):
            if rng.random() < 0.85:
                L = h * (0.22 + 0.25 * rng.random()) * (1 - i / 9)
                ex, ey = px + side * L, py - h * 0.03
                d.line((px, py, ex, ey), fill=ink, width=1)
                pw, ph = L * 0.7, h * 0.07
                d.ellipse((ex - pw, ey - ph, ex + pw * 0.6, ey + ph * 0.5), fill=needles, outline=ink)
                for k in range(int(pw / 2)):  # needle ticks along the pad's lower edge
                    tx = ex - pw + 2 + k * 2
                    d.line((tx, ey + ph * 0.3, tx + 1, ey + ph * 0.3 + 2), fill=ink)
    tx, ty = pts[-1]
    d.ellipse((tx - h * 0.18, ty - h * 0.08, tx + h * 0.18, ty + h * 0.05), fill=needles, outline=ink)

def waves(d, x0, y0, x1, y1, ink=Wh, spacing=7, amp=2.0, rng=None):
    rng = rng or np.random.default_rng(7)
    y = y0
    while y < y1:
        x = x0 + rng.uniform(-10, 0)
        while x < x1:
            L = rng.uniform(8, 26)
            pts = [(x + t, y + amp * math.sin(t * 0.5 + y)) for t in np.arange(0, L, 2)]
            if len(pts) > 1:
                d.line(pts, fill=ink, width=1)
            x += L + rng.uniform(4, 14 + (y1 - y) * 0.1)
        y += spacing * (0.6 + 0.8 * (y - y0) / max(1, y1 - y0))

def save(im, path):
    im.save(path)
