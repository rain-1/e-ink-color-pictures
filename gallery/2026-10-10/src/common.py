# Shared helpers for 2026-10-10 (Giacometti at 125). Palette constants, an 8x8 Bayer
# screen for in-generator tone, value-noise fBm, and the little Walking Man who appears
# somewhere in every piece today.
import math, numpy as np
from PIL import Image, ImageDraw

W, H = 400, 600
K, Wh, R, Y, B, G = (0,0,0), (255,255,255), (224,27,36), (245,212,0), (18,61,176), (30,155,60)

def _bayer(n):
    m = np.array([[0]])
    while m.shape[0] < n:
        m = np.block([[4*m, 4*m+2], [4*m+3, 4*m+1]])
    return (m + 0.5) / m.size
BAYER = _bayer(8)

def screen(h, w, ox=0, oy=0):
    return np.tile(BAYER, (h//8+2, w//8+2))[oy:oy+h, ox:ox+w]

def ramp(t, stops):
    """t: HxW array in [0,1]. stops: list of palette colours. Ordered-dither between
    adjacent stops. Returns HxWx3 uint8."""
    t = np.clip(t, 0, 1) * (len(stops) - 1)
    i = np.minimum(np.floor(t).astype(int), len(stops) - 2)
    f = t - i
    th = screen(*t.shape)
    j = np.where(f > th, i + 1, i)
    pal = np.array(stops, dtype=np.uint8)
    return pal[j]

def paste_arr(im, arr, mask=None, x0=0, y0=0):
    """Paste an HxWx3 array into PIL image, optionally through a bool mask."""
    h, w = arr.shape[:2]
    base = np.asarray(im).copy()
    reg = base[y0:y0+h, x0:x0+w]
    if mask is None:
        reg[:] = arr
    else:
        reg[mask] = arr[mask]
    im.paste(Image.fromarray(base))

def fbm(h, w, seed=0, octaves=5, base=4):
    rng = np.random.default_rng(seed)
    out = np.zeros((h, w)); amp = 1.0; tot = 0
    for o in range(octaves):
        n = base * 2**o
        g = rng.random((n+1, int(n*w/h)+2))
        img = Image.fromarray((g*255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
        out += amp * np.asarray(img, dtype=float)/255; tot += amp; amp *= 0.5
    return out / tot

def walker(d, x, yf, h, fill, stride=0.5, facing=1, outline=None):
    """Giacometti's Homme qui marche: tiny head, long rod body, heavy feet, leaning
    forward. (x, yf) = point between the feet. h = total height in px."""
    s = h / 100.0; f = facing
    def P(px, py): return (x + f*px*s, yf - py*s)
    lean = 4
    hip = (lean*0.45, 50); neck = (lean, 86)
    # legs
    st = 14*stride + 4
    for foot, knee in (((st, 0), (st*0.5+1, 26)), ((-st, 0), (-st*0.45+lean*0.2, 25))):
        d.line([P(*hip), P(*knee), P(*foot)], fill=fill, width=max(1, round(2.6*s)), joint="curve")
    # feet: heavy blocks
    for fx in (st, -st):
        d.polygon([P(fx-5, 0), P(fx+8, 0), P(fx+7, 3.5), P(fx-4, 4.5)], fill=fill)
    # torso: thin wedge
    d.polygon([P(hip[0]-2.2, hip[1]), P(hip[0]+2.2, hip[1]), P(neck[0]+3, neck[1]-4),
               P(neck[0]+1.5, neck[1]), P(neck[0]-2.5, neck[1]-3)], fill=fill)
    # arms hanging, slightly back
    d.line([P(neck[0]-1, neck[1]-4), P(-3, 62), P(-4, 48)], fill=fill, width=max(1, round(1.6*s)))
    d.line([P(neck[0]+2, neck[1]-4), P(lean+4, 64), P(lean+5, 50)], fill=fill, width=max(1, round(1.6*s)))
    # head: small, tilted forward
    r = 4.2*s
    cx, cy = P(neck[0]+1.5, neck[1]+5)
    d.ellipse((cx-r*0.8, cy-r, cx+r*0.8, cy+r), fill=fill)

def save(im):
    import os
    im.save(os.environ.get("OUT_RAW", "out.png"))

def polymask(poly, size=(W, H)):
    m = Image.new("L", size, 0); ImageDraw.Draw(m).polygon(poly, fill=255)
    return np.asarray(m) > 0

def tone_poly(im, poly, t, stops):
    """Fill polygon with tone t (scalar or HxW array) screened through stops."""
    m = polymask(poly, im.size)
    tt = t if isinstance(t, np.ndarray) else np.full(m.shape, float(t))
    paste_arr(im, ramp(tt, stops), m)

def scribble(d, cx, cy, rx, ry, n, rng, fill, width=1):
    """Giacometti's searching line: an ellipse redrawn n times, wobbling."""
    for k in range(n):
        a0 = rng.uniform(0, 6.28); pts = []
        jx, jy = rng.normal(0, rx*0.08), rng.normal(0, ry*0.08)
        for s in range(28):
            a = a0 + s/27*6.28*rng.uniform(0.8, 1.1)
            pts.append((cx + jx + rx*math.cos(a)*rng.uniform(0.92, 1.06),
                        cy + jy + ry*math.sin(a)*rng.uniform(0.92, 1.06)))
        d.line(pts, fill=fill, width=width)
