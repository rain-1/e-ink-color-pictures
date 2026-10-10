# Afternoon — "125". Swiss Post issued a stamp this year for Giacometti's 125th, with the
# Walking Man on it. This is my own stamp for the day, drawn as a line engraving: every
# tone is made of ruled lines that swell and thin (sky horizontal, granite diagonal, figure
# vertical), printed in red on a perforated sheet, stuck to an airmail envelope with a
# Stampa postmark across the corner and an address in blue ink. Red is in charge.
import math, numpy as np
from PIL import Image, ImageDraw, ImageFont
from common import *

rng = np.random.default_rng(125)
FS = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FI = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
FM = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

# ---------- envelope
im = Image.new("RGB", (W, H), Wh); d = ImageDraw.Draw(im); d.fontmode = "1"
yy, xx = np.mgrid[0:H, 0:W].astype(float)
paper = fbm(H, W, seed=9, base=10)
env = np.asarray(im).copy()
env[screen(H, W) < 0.10 + (paper-0.5)*0.12] = Y          # warm paper fibre
im = Image.fromarray(env); d = ImageDraw.Draw(im); d.fontmode = "1"
# airmail chevron border
BW_ = 16
for k in range(-40, 80):
    for side in range(4):
        c = (R, Wh, B, Wh)[k % 4]
        if c == Wh: continue
        s = k*14
        if side == 0: poly = [(s, 0), (s+14, 0), (s+14-BW_, BW_), (s-BW_, BW_)]
        if side == 1: poly = [(s, H), (s+14, H), (s+14-BW_, H-BW_), (s-BW_, H-BW_)]
        if side == 2: poly = [(0, s), (0, s+14), (BW_, s+14-BW_), (BW_, s-BW_)]
        if side == 3: poly = [(W, s), (W, s+14), (W-BW_, s+14-BW_), (W-BW_, s-BW_)]
        d.polygon(poly, fill=c)
d.rectangle((BW_, BW_, W-BW_, H-BW_), outline=K)
# PAR AVION label, top-left, blue
fl = ImageFont.truetype(FS, 12)
d.rectangle((26, 28, 128, 50), fill=B); d.text((33, 32), "PAR AVION", fill=Wh, font=fl)
d.text((33, 54), "PER AEREO · BY AIR", fill=B, font=ImageFont.truetype(FM, 8))

# address in blue ink: a few handwritten lines
fh = ImageFont.truetype(FI, 22)
lines = ["Alberto Giacometti", "46, rue Hippolyte-Maindron", "Paris XIVᵉ", "FRANCE"]
for i, t in enumerate(lines):
    d.text((44 + i*6, 470 + i*27), t, fill=B, font=fh)
d.line((50, 584, 230, 580), fill=B, width=2)

# ---------- the stamp, built on its own sheet
SW, SH = 270, 360
st = Image.new("RGB", (SW, SH), Wh); sd = ImageDraw.Draw(st); sd.fontmode = "1"
ix0, iy0, ix1, iy1 = 18, 18, SW-18, SH-70                 # engraved picture area
pw, ph = ix1-ix0, iy1-iy0
py, px = np.mgrid[0:ph, 0:pw].astype(float)

# tone image (0 = paper, 1 = full ink)
tone = 0.12 + 0.30*(1 - py/ph)                            # sky, darker up
region = np.zeros((ph, pw), int)                          # 0 sky, 1 rock, 2 ground, 3 figure
def ridgeline(seed, pts, n=6, rough=0.18):
    r = np.random.default_rng(seed)
    xs = np.array([p[0] for p in pts], float); ys = np.array([p[1] for p in pts], float)
    for _ in range(n):
        nx, ny = [xs[0]], [ys[0]]
        for i in range(len(xs)-1):
            nx += [(xs[i]+xs[i+1])/2, xs[i+1]]
            ny += [(ys[i]+ys[i+1])/2 + r.normal(0, rough*(xs[i+1]-xs[i])), ys[i+1]]
        xs, ys = np.array(nx), np.array(ny)
    return np.interp(np.arange(pw), xs, ys)
rl = ridgeline(4, [(0, 170), (30, 130), (55, 100), (80, 150), (110, 180), (140, 170), (170, 115), (195, 85), (215, 140), (234, 160)])
rock = py > rl[None, :]
sl = np.gradient(np.convolve(rl, np.ones(7)/7, mode="same"))
gn = fbm(ph, pw, seed=5, base=6)
tone = np.where(rock, np.clip(0.42 - 0.3*np.tanh(sl*1.2)[None, :] + (gn-0.5)*0.6, 0.05, 0.8), tone)
snow = rock & (gn > 0.6) & (py - rl[None, :] < 35)
tone[snow] = 0.0
region[rock] = 1
gl = 230 + 6*np.sin(px/30)
ground = py > gl
tone[ground] = 0.75 - (py[ground]-230)/200*0.0 + (gn[ground]-0.5)*0.3
region[ground] = 2
# walking man, big, striding across
fig = Image.new("L", (pw, ph), 0)
walker(ImageDraw.Draw(fig), pw*0.44, 250, 225, 255, stride=0.8)
fm = np.asarray(fig) > 0
# modelled: darker on right
cols = np.where(fm)
tone[fm] = 0.98
lit = fm & (np.roll(fm, 3, 1) == False)
tone[lit] = 0.6
halo = np.zeros_like(fm)
for dy in range(-3,4):
    for dx in range(-3,4):
        halo |= np.roll(np.roll(fm,dy,0),dx,1)
halo &= ~fm
tone[halo] = 0.0
region[fm] = 3
# sun disc behind the figure's shoulder
sun = ((px-165)**2 + (py-60)**2) < 22**2
tone[sun & (region == 0)] = 0.0

# engrave: per region a line direction and spacing; ink where |phase| < width/2
def engrave(tone, angle, spacing, wobble=0.0):
    a = math.radians(angle)
    u = px*math.sin(a) - py*math.cos(a)
    if wobble: u = u + wobble*np.sin(px/9 + py/13)
    ph_ = (u % spacing) - spacing/2
    width = np.clip(tone, 0, 1)*spacing*0.95
    return np.abs(ph_) < width/2
ink = np.zeros((ph, pw), bool)
ink |= (region == 0) & engrave(tone, 0, 3.0)
ink |= (region == 1) & engrave(tone, 62, 3.2, wobble=0.8)
ink |= (region == 2) & engrave(tone, 0, 4.0, wobble=1.2)
ink |= (region == 3) & engrave(tone, 90, 2.6)
ink |= (region == 1) & ~engrave(np.full_like(tone, 0.8), -30, 6) & (tone > 0.7)   # cross-hatch deep shade
# outlines: figure edge and ridge
edge = fm & ~(np.roll(fm, 1, 0) & np.roll(fm, -1, 0) & np.roll(fm, 1, 1) & np.roll(fm, -1, 1))
ink |= edge
for x in range(pw): 
    y = int(rl[x])
    if 0 <= y < ph: ink[y, x] = True
pic = np.where(ink[..., None], np.array(R, np.uint8), np.array(Wh, np.uint8))
st.paste(Image.fromarray(pic.astype(np.uint8)), (ix0, iy0))
sd.rectangle((ix0-1, iy0-1, ix1, iy1), outline=R, width=2)
sd.rectangle((ix0-6, iy0-6, ix1+5, SH-14), outline=R, width=1)
# lettering
f1 = ImageFont.truetype(FS, 21); f2 = ImageFont.truetype(FS, 11); f3 = ImageFont.truetype(FS, 30)
sd.text((ix0+2, iy1+8), "GIACOMETTI", fill=R, font=f1)
sd.text((ix0+3, iy1+34), "1901 · STAMPA · 2026", fill=R, font=f2)
sd.rectangle((ix1-58, iy1+6, ix1, iy1+48), fill=R)
sd.text((ix1-54, iy1+9), "125", fill=Wh, font=f3)
# value tablet inside the picture, top-left
sd.text((ix0+6, iy0+4), "HOMME QUI MARCHE", fill=R, font=ImageFont.truetype(FM, 9))

# perforations: punch semicircles out of the edges
mask = Image.new("L", (SW, SH), 255); md = ImageDraw.Draw(mask)
for x in np.arange(0, SW+1, 11):
    md.ellipse((x-4, -4, x+4, 4), fill=0); md.ellipse((x-4, SH-4, x+4, SH+4), fill=0)
for y in np.arange(0, SH+1, 11):
    md.ellipse((-4, y-4, 4, y+4), fill=0); md.ellipse((SW-4, y-4, SW+4, y+4), fill=0)
# shadow of the stamp on the envelope
ang = 4
shadow = Image.new("L", (SW, SH), 0); shadow.paste(mask, (0, 0))
sh_r = shadow.rotate(ang, expand=True, resample=Image.NEAREST)
st_r = st.rotate(ang, expand=True, resample=Image.NEAREST)
m_r = mask.rotate(ang, expand=True, resample=Image.NEAREST)
ox, oy = (W - st_r.width)//2 + 8, 70
shade = Image.new("RGB", sh_r.size, K)
sm = np.asarray(sh_r) > 0
scr = screen(*sm.shape) < 0.5
im.paste(shade, (ox+5, oy+6), Image.fromarray(((sm & scr)*255).astype(np.uint8)))
im.paste(st_r, (ox, oy), m_r)
d = ImageDraw.Draw(im); d.fontmode = "1"

# ---------- postmark: circle date stamp + wavy cancellation, black, over the right corner
pc = (322, 112); prr = 46
for r_ in (prr, prr-12):
    d.ellipse((pc[0]-r_, pc[1]-r_, pc[0]+r_, pc[1]+r_), outline=K, width=2)
fp = ImageFont.truetype(FM, 11)
word = "STAMPA · BREGAGLIA ·"
for i, ch in enumerate(word):
    a = math.radians(-160 + i*(320/len(word)))
    cx = pc[0] + (prr-6)*math.cos(a); cy = pc[1] + (prr-6)*math.sin(a)
    gl_ = Image.new("L", (14, 14), 0); ImageDraw.Draw(gl_).text((3, 0), ch, fill=255, font=fp)
    gl_ = gl_.rotate(-math.degrees(a)-90, resample=Image.NEAREST)
    im.paste(K, (int(cx-7), int(cy-7)), gl_.point(lambda v: 255 if v > 128 else 0))
d = ImageDraw.Draw(im); d.fontmode = "1"
d.text((pc[0]-24, pc[1]-14), "10.X.26", fill=K, font=ImageFont.truetype(FM, 12))
d.text((pc[0]-14, pc[1]+1), "14-15", fill=K, font=ImageFont.truetype(FM, 10))
for k in range(6):
    y0 = 84 + k*12
    pts = [(x, y0 + 4*math.sin(x/9)) for x in range(150, 272, 2)]
    # break the lines where they'd cross the circle
    d.line(pts, fill=K, width=1)

# a second, smaller walking man: the figure on the envelope's flap seal
walker(d, 352, 586, 30, K)
save(im)
