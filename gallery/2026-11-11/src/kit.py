"""Shared drawing kit for 2026-11-10. Draw big (S x), in pure palette colours,
shrink, and let render.py snap to the palette."""
import math, os, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, S = 400, 600, 3
K = (0, 0, 0); Wh = (255, 255, 255); R = (0xE0, 0x1B, 0x24)
Y = (0xF5, 0xD4, 0x00); B = (0x12, 0x3D, 0xB0); G = (0x1E, 0x9B, 0x3C)

def canvas(bg=Wh, s=S):
    im = Image.new("RGB", (W * s, H * s), bg)
    return im, ImageDraw.Draw(im)

def vote_down(im, s=S, wk=2.0):
    """Shrink s-fold without inventing colours: snap every sub-pixel to an ink, then each
    final pixel takes the ink with most votes (black counts double, so hairlines hold).
    Plain resampling turns a thin black line on white into grey, which the panel reads
    as green."""
    a = np.asarray(im.convert("RGB"), np.float32)
    pal = np.array([K, Wh, R, Y, B, G], np.float32)
    idx = ((a[:, :, None, :] - pal[None, None]) ** 2).sum(-1).argmin(-1)
    sat = a.max(-1) - a.min(-1)                       # antialiased text: greys go to K or W
    grey = sat < 70
    idx[grey] = np.where(a[grey].mean(-1) < 150, 0, 1)
    h, w = idx.shape[0] // s, idx.shape[1] // s
    blocks = idx.reshape(h, s, w, s)
    votes = np.stack([(blocks == i).sum((1, 3)) * (wk if i == 0 else 1.0) for i in range(6)], -1)
    return Image.fromarray(pal[votes.argmax(-1)].astype(np.uint8))

def save(im):
    out = os.environ.get("OUT_RAW", "out_raw.png")
    if im.size != (W, H):
        im = vote_down(im, im.size[0] // W)
    im.save(out)

def font(size, bold=False, italic=False, s=S):
    name = "LiberationSerif-" + ("BoldItalic" if bold and italic else "Bold" if bold
                                 else "Italic" if italic else "Regular")
    return ImageFont.truetype(f"/usr/share/fonts/truetype/liberation/{name}.ttf", int(size * s))

def P(pts, s=S):
    return [(x * s, y * s) for x, y in pts]

def line(d, pts, fill=K, w=1.0, s=S):
    d.line(P(pts, s), fill=fill, width=max(1, int(round(w * s))), joint="curve")

def poly(d, pts, fill=None, outline=None, w=1.0, s=S):
    if fill is not None:
        d.polygon(P(pts, s), fill=fill)
    if outline is not None:
        line(d, list(pts) + [pts[0]], outline, w, s)

def rect(d, x0, y0, x1, y1, fill=None, outline=None, w=1.0, s=S):
    poly(d, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], fill, outline, w, s)

def circ(d, x, y, r, fill=None, outline=None, w=1.0, s=S):
    d.ellipse([(x - r) * s, (y - r) * s, (x + r) * s, (y + r) * s], fill=fill,
              outline=outline, width=max(1, int(round(w * s))) if outline else 0)

def ell(d, x, y, rx, ry, fill=None, outline=None, w=1.0, s=S):
    d.ellipse([(x - rx) * s, (y - ry) * s, (x + rx) * s, (y + ry) * s], fill=fill,
              outline=outline, width=max(1, int(round(w * s))) if outline else 0)

def bez(p0, p1, p2, p3, n=24):
    out = []
    for i in range(n + 1):
        t = i / n; u = 1 - t
        out.append((u**3 * p0[0] + 3*u*u*t * p1[0] + 3*u*t*t * p2[0] + t**3 * p3[0],
                    u**3 * p0[1] + 3*u*u*t * p1[1] + 3*u*t*t * p2[1] + t**3 * p3[1]))
    return out

def scurve(x, y, h, amp, n=40, turns=1.0, phase=0.0):
    """Hogarth's line: a vertical S from (x,y) down h, swinging +-amp."""
    return [(x + amp * math.sin(phase + turns * 2 * math.pi * i / n), y + h * i / n) for i in range(n + 1)]

def hatch(im, pts, fill=K, gap=3.0, ang=45, w=0.6, s=S, cross=False):
    """Hatch the polygon pts with parallel lines."""
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    bw, bh = int((x1 - x0) * s) + 2, int((y1 - y0) * s) + 2
    if bw < 2 or bh < 2: return
    mask = Image.new("L", (bw, bh), 0)
    ImageDraw.Draw(mask).polygon([((x - x0) * s, (y - y0) * s) for x, y in pts], fill=255)
    lay = Image.new("L", (bw, bh), 0); ld = ImageDraw.Draw(lay)
    for a in ([ang, ang + 90] if cross else [ang]):
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        L = bw + bh
        t = -L
        while t < L:
            cx, cy = bw / 2 - sa * t, bh / 2 + ca * t
            ld.line([(cx - ca * L, cy - sa * L), (cx + ca * L, cy + sa * L)], fill=255,
                    width=max(1, int(round(w * s))))
            t += gap * s
    m = Image.composite(lay, Image.new("L", (bw, bh), 0), mask)
    im.paste(fill, (int(x0 * s), int(y0 * s)), m)

def text(d, x, y, t, size=10, fill=K, anchor="mm", bold=False, italic=False, s=S):
    d.text((x * s, y * s), t, font=font(size, bold, italic, s), fill=fill, anchor=anchor)

PAL6 = np.array([K, Wh, R, Y, B, G], np.float32)
BAYER8 = (np.array([[0,32,8,40,2,34,10,42],[48,16,56,24,50,18,58,26],[12,44,4,36,14,46,6,38],[60,28,52,20,62,30,54,22],
                    [3,35,11,43,1,33,9,41],[51,19,59,27,49,17,57,25],[15,47,7,39,13,45,5,37],[63,31,55,23,61,29,53,21]]) + 0.5) / 64

def pair_screen(im, pairs=None):
    """Quantise to the palette by screening each pixel between the *two* inks whose mix
    is nearest to it. Pure flats stay pure; a tone between two inks becomes a clean
    Bayer screen of just those two, never a speckle of a third."""
    a = np.asarray(im.convert("RGB"), np.float32); h, w, _ = a.shape
    best = np.full((h, w), 1e12, np.float32); out = np.zeros((h, w, 3), np.float32)
    th = np.tile(BAYER8, (h // 8 + 1, w // 8 + 1))[:h, :w]
    for i in range(6):
        for j in range(i + 1, 6):
            if pairs and (i, j) not in pairs: continue
            p, q = PAL6[i], PAL6[j]; dq = q - p
            t = np.clip(((a - p) * dq).sum(-1) / (dq * dq).sum(), 0, 1)
            dist = ((a - (p + t[..., None] * dq)) ** 2).sum(-1)
            m = dist < best
            best[m] = dist[m]
            pick = np.where((t > th)[..., None], q, p)
            out[m] = pick[m]
    return Image.fromarray(out.astype(np.uint8))

def mix(a, b, t):
    t = max(0.0, min(1.0, t))
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))
