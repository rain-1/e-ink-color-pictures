"""Shared helpers for 2026-11-25. Everything is drawn 1:1 in pure palette colours;
tone comes from patterns (Bayer tints, hatching, bricks), never from antialiasing."""
import os, math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 400, 600
K, WH, R, Y, B, G = (0,0,0), (255,255,255), (0xE0,0x1B,0x24), (0xF5,0xD4,0x00), (0x12,0x3D,0xB0), (0x1E,0x9B,0x3C)

BAYER = np.array([[0,32,8,40,2,34,10,42],[48,16,56,24,50,18,58,26],[12,44,4,36,14,46,6,38],
                  [60,28,52,20,62,30,54,22],[3,35,11,43,1,33,9,41],[51,19,59,27,49,17,57,25],
                  [15,47,7,39,13,45,5,37],[63,31,55,23,61,29,53,21]]) / 64.0
YY, XX = np.mgrid[0:H, 0:W]

def new(c=WH):
    im = Image.new("RGB", (W, H), c)
    d = ImageDraw.Draw(im); d.fontmode = "1"
    return im, d

def font(size, face="serif", bold=False, italic=False):
    lib = "/usr/share/fonts/truetype/liberation/Liberation"
    name = {"serif": "Serif", "sans": "Sans", "mono": "Mono"}[face]
    style = {(0, 0): "Regular", (1, 0): "Bold", (0, 1): "Italic", (1, 1): "BoldItalic"}[(int(bold), int(italic))]
    return ImageFont.truetype(f"{lib}{name}-{style}.ttf", size)

# ---- patterns: boolean arrays (True = second colour) --------------------------------
def p_bayer(level):            return BAYER[YY % 8, XX % 8] < level
def p_hatch(sp=4, w=1, dx=1):  return ((XX * dx + YY) % sp) < w
def p_cross(sp=5, w=1):        return (((XX + YY) % sp) < w) | (((XX - YY) % sp) < w)
def p_hlines(sp=3, w=1, o=0):  return ((YY + o) % sp) < w
def p_vlines(sp=3, w=1, o=0):  return ((XX + o) % sp) < w
def p_dots(sp=4, o=0):         return ((XX + o) % sp == 0) & ((YY + o) % sp == 0)
def p_dots2(sp=6):             return (((XX % sp == 0) & (YY % sp == 0)) | ((XX % sp == sp // 2) & (YY % sp == sp // 2)))
def p_brick(bw=10, bh=5):
    row = YY // bh
    return (YY % bh == 0) | (((XX + (row % 2) * (bw // 2)) % bw) == 0)
def p_diamond(sp=8):           return ((np.abs((XX % sp) - sp // 2) + np.abs((YY % sp) - sp // 2)) <= 1)
def p_check(s=4):              return ((XX // s + YY // s) % 2) == 0
def p_planks(sp=7):
    col = XX // sp
    return (XX % sp == 0) | (((YY + col * 13) % 37) == 0)

def mask_poly(pts):
    m = Image.new("1", (W, H), 0); ImageDraw.Draw(m).polygon(pts, fill=1); return np.array(m, bool)
def mask_rect(x0, y0, x1, y1):
    m = np.zeros((H, W), bool); m[max(0,int(y0)):max(0,int(y1)), max(0,int(x0)):max(0,int(x1))] = True; return m
def mask_ellipse(box):
    m = Image.new("1", (W, H), 0); ImageDraw.Draw(m).ellipse(box, fill=1); return np.array(m, bool)

def paint(im, mask, c1, c2=None, pat=None):
    """Fill mask with c1, and with c2 where pat is True. Mutates im in place."""
    a = np.array(im)
    a[mask] = c1
    if c2 is not None and pat is not None:
        a[mask & pat] = c2
    im.paste(Image.fromarray(a))

def rect(im, box, c1, c2=None, pat=None):   paint(im, mask_rect(*box), c1, c2, pat)
def poly(im, pts, c1, c2=None, pat=None):   paint(im, mask_poly(pts), c1, c2, pat)
def ell(im, box, c1, c2=None, pat=None):    paint(im, mask_ellipse(box), c1, c2, pat)

def ctext(d, cx, y, s, f, fill):
    w = d.textlength(s, font=f); d.text((cx - w / 2, y), s, font=f, fill=fill)

def spaced(d, cx, y, s, f, fill, gap=2):
    ws = [d.textlength(ch, font=f) for ch in s]; tot = sum(ws) + gap * (len(s) - 1); x = cx - tot / 2
    for ch, w in zip(s, ws):
        d.text((x, y), ch, font=f, fill=fill); x += w + gap

def mouse(d, x, y, s=1.0, c=K, eye=None, flip=False, tail=True):
    """A small mouse, nose at right unless flipped. (x,y) = feet centre. ~18px long at s=1."""
    f = -1 if flip else 1
    d.ellipse([x - 7*s, y - 8*s, x + 6*s, y], fill=c)                       # body
    d.polygon([(x + f*3*s, y - 7*s), (x + f*12*s, y - 2*s), (x + f*3*s, y)], fill=c)  # snout
    d.ellipse([x + f*1*s - 3*s, y - 11*s, x + f*1*s + 3*s, y - 5*s], fill=c)  # ear
    if tail:
        pts = [(x - f*(6 + t)*s, y - 2*s - math.sin(t / 2.2) * 3*s) for t in range(0, 12)]
        d.line(pts, fill=c, width=1)
    if eye: d.point((x + f*6*s, y - 5*s), fill=eye)

def save(im):
    im.save(os.environ.get("OUT_RAW", "out.png"))
