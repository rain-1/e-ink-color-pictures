"""Shared helpers for 2026-10-13: draw at S× in pure palette colours, then
majority-downsample to 400×600 so edges are smooth-ish but never off-palette."""
import os, math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont

S = 3
W, H = 400, 600
K, Wh, R, Y, B, G = (0,0,0), (255,255,255), (0xE0,0x1B,0x24), (0xF5,0xD4,0x00), (0x12,0x3D,0xB0), (0x1E,0x9B,0x3C)
PAL = [K, Wh, R, Y, B, G]

class C:
    def __init__(self, bg=Wh):
        self.im = Image.new("RGB", (W*S, H*S), bg)
        self.d = ImageDraw.Draw(self.im)
    def _p(self, pts):
        return [(x*S, y*S) for x, y in pts]
    def poly(self, pts, fill=None, outline=None, width=1):
        self.d.polygon(self._p(pts), fill=fill)
        if outline is not None:
            p = self._p(pts); self.d.line(p + [p[0]], fill=outline, width=max(1, round(width*S)), joint="curve")
    def rect(self, x0, y0, x1, y1, fill=None, outline=None, width=1):
        self.poly([(x0,y0),(x1,y0),(x1,y1),(x0,y1)], fill, outline, width)
    def line(self, pts, fill, width=1):
        self.d.line(self._p(pts), fill=fill, width=max(1, round(width*S)), joint="curve")
    def ell(self, cx, cy, rx, ry=None, fill=None, outline=None, width=1):
        ry = rx if ry is None else ry
        self.d.ellipse([(cx-rx)*S, (cy-ry)*S, (cx+rx)*S, (cy+ry)*S], fill=fill,
                       outline=outline, width=max(1, round(width*S)) if outline else 0)
    def text(self, xy, s, fill, size=14, anchor="la", bold=True):
        self.d.text((xy[0]*S, xy[1]*S), s, fill=fill, font=font(size*S, bold), anchor=anchor)
    def clip_paste(self, layer, mask_pts):
        """paste another C's image through a polygon mask"""
        m = Image.new("L", self.im.size, 0)
        ImageDraw.Draw(m).polygon(self._p(mask_pts), fill=255)
        self.im.paste(layer.im, (0, 0), m)
    def save(self):
        out = finish(self.im)
        out.save(os.environ.get("OUT_RAW", "out.png"))
        return out

def font(px, bold=True):
    for f in (["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"] if bold else []) + \
             ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
        if os.path.exists(f):
            return ImageFont.truetype(f, int(px))
    return ImageFont.load_default()

def finish(im):
    a = np.asarray(im.convert("RGB"), dtype=np.int32)
    pal = np.array(PAL, dtype=np.int32)
    idx = ((a[:, :, None, :] - pal[None, None]) ** 2).sum(-1).argmin(-1)
    h, w = idx.shape
    blk = idx.reshape(h // S, S, w // S, S).transpose(0, 2, 1, 3).reshape(h // S, w // S, S * S)
    counts = np.stack([(blk == i).sum(-1) for i in range(6)], -1)
    # centre pixel breaks ties, so thin lines survive
    centre = blk[:, :, (S * S) // 2]
    counts[np.arange(h // S)[:, None], np.arange(w // S)[None, :], centre] += 1
    return Image.fromarray(pal[counts.argmax(-1)].astype(np.uint8), "RGB")

def bayer(n=8):
    m = np.array([[0]])
    while m.shape[0] < n:
        m = np.block([[4*m, 4*m+2], [4*m+3, 4*m+1]])
    return (m + 0.5) / m.size

def kite(c, cx, cy, r, cols=(R, Y, B, G, Wh, R), rot=0.0, tail=None, frame=K):
    """A barrilete: hexagonal kite, six coloured paper sectors, cane spars, bow tail."""
    pts = [(cx + r*math.cos(rot + math.pi/6 + i*math.pi/3), cy + r*math.sin(rot + math.pi/6 + i*math.pi/3)) for i in range(6)]
    for i in range(6):
        c.poly([(cx, cy), pts[i], pts[(i+1) % 6]], fill=cols[i % len(cols)])
    # inner ring of contrasting paper
    inner = [(cx + (p[0]-cx)*0.45, cy + (p[1]-cy)*0.45) for p in pts]
    for i in range(6):
        c.poly([(cx, cy), inner[i], inner[(i+1) % 6]], fill=cols[(i+3) % len(cols)])
    c.poly(pts, outline=frame, width=max(1, r/14))
    for i in range(3):
        c.line([pts[i], pts[i+3]], frame, max(1, r/18))
    c.ell(cx, cy, max(1.5, r/9), fill=frame)
    if tail:
        # tail: list of points; bows every few
        c.line(tail, frame, max(1, r/20))
        for j, (x, y) in enumerate(tail[2::3]):
            bw = max(2.5, r/4.5)
            col = cols[j % len(cols)]
            c.poly([(x-bw, y-bw*0.6), (x, y), (x-bw, y+bw*0.6)], fill=col, outline=frame, width=0.6)
            c.poly([(x+bw, y-bw*0.6), (x, y), (x+bw, y+bw*0.6)], fill=col, outline=frame, width=0.6)
    return pts

def tail_curve(x0, y0, length, amp, n=30, seed=0, dirx=0.15):
    rnd = random.Random(seed)
    ph = rnd.random()*6
    return [(x0 + dirx*length*t/n + amp*math.sin(ph + t*0.45)*(t/n), y0 + length*t/n) for t in range(n+1)]
