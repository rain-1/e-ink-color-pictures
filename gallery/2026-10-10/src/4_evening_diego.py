# Evening — "Diego, searching". A bust modelled as a signed-distance field (skull, brow,
# deep sockets, long nose, neck, shoulders), raymarched in numpy, and then *not* shown as a
# render: the render only steers a few thousand strokes that wrap around the form the way
# Giacometti's line did, black into the shadows, white onto the lights, a little red
# underdrawing, the head boxed in by redrawn frame lines. Ochre ground for the hour.
import math, numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import gaussian_filter, binary_erosion
from common import *

rng = np.random.default_rng(1964)

# ---------- SDF
def ell(p, c, r):
    q = (p - c) / r
    k0 = np.linalg.norm(q, axis=-1); k1 = np.linalg.norm(q / r, axis=-1)
    return k0 * (k0 - 1) / np.maximum(k1, 1e-6)
def sph(p, c, r): return np.linalg.norm(p - c, axis=-1) - r
def cap(p, a, b, r):
    pa = p - a; ba = b - a
    h = np.clip((pa @ ba) / (ba @ ba), 0, 1)
    return np.linalg.norm(pa - h[..., None]*ba, axis=-1) - r
def smin(a, b, k):
    h = np.clip(0.5 + 0.5*(b-a)/k, 0, 1); return b*(1-h) + a*h - k*h*(1-h)
def smax(a, b, k): return -smin(-a, -b, k)
A = np.array
def sdf(p):
    p = p * A([1/0.86, 1, 1])                 # narrow, Giacometti-thin
    d = ell(p, A([0, 0.38, -0.04]), A([0.40, 0.52, 0.47]))
    d = smin(d, ell(p, A([0, 0.02, 0.10]), A([0.30, 0.44, 0.36])), 0.12)
    d = smin(d, ell(p, A([0, 0.30, 0.32]), A([0.31, 0.07, 0.12])), 0.05)   # brow
    d = smin(d, cap(p, A([0, 0.27, 0.42]), A([0, 0.04, 0.55]), 0.055), 0.05)  # nose
    for s in (-1, 1):
        d = smax(d, -sph(p, A([s*0.14, 0.20, 0.45]), 0.085), 0.04)            # sockets
        d = smin(d, sph(p, A([s*0.14, 0.20, 0.37]), 0.06), 0.01)              # eyes
        d = smin(d, ell(p, A([s*0.41, 0.20, -0.02]), A([0.05, 0.12, 0.08])), 0.03)  # ears
        d = smin(d, ell(p, A([s*0.20, 0.02, 0.30]), A([0.08, 0.10, 0.06])), 0.06)   # cheekbones
    d = smax(d, -ell(p, A([0, -0.13, 0.43]), A([0.11, 0.015, 0.08])), 0.02)   # mouth
    d = smin(d, ell(p, A([0, -0.30, 0.20]), A([0.15, 0.09, 0.12])), 0.08)     # chin
    d = smin(d, cap(p, A([0, -0.85, -0.05]), A([0, -0.2, -0.02]), 0.17), 0.1)  # neck
    d = smin(d, ell(p, A([0, -1.25, -0.05]), A([1.15, 0.42, 0.40])), 0.25)     # shoulders
    d = smin(d, ell(p, A([0, -2.2, -0.05]), A([1.05, 1.0, 0.42])), 0.2)      # chest, runs off the frame
    return d

# ---------- camera + march
Wd, Hd = W, H
ys, xs = np.mgrid[0:Hd, 0:Wd].astype(float)
ro = A([0.35, 0.1, 3.0]); ta = A([0, -0.32, 0])
fw = (ta - ro); fw /= np.linalg.norm(fw)
rt = np.cross(fw, A([0, 1, 0])); rt /= np.linalg.norm(rt); up = np.cross(rt, fw)
u = (xs - Wd/2) / (Hd/2); v = -(ys - Hd*0.47) / (Hd/2)
rd = fw[None, None] * 1.55 + u[..., None]*rt + v[..., None]*up
rd /= np.linalg.norm(rd, axis=-1, keepdims=True)
rdf = rd.reshape(-1, 3); t = np.zeros(len(rdf)); hit = np.zeros(len(rdf), bool)
alive = np.ones(len(rdf), bool)
for it in range(110):
    idx = np.where(alive)[0]
    if len(idx) == 0: break
    p = ro + rdf[idx]*t[idx, None]
    dd = sdf(p)
    t[idx] += dd*0.9
    h = dd < 0.002; hit[idx[h]] = True
    alive[idx[h | (t[idx] > 7)]] = False
P = ro + rdf*t[:, None]
e = 0.002
N = np.stack([sdf(P + A([e, 0, 0])) - sdf(P - A([e, 0, 0])),
              sdf(P + A([0, e, 0])) - sdf(P - A([0, e, 0])),
              sdf(P + A([0, 0, e])) - sdf(P - A([0, 0, e]))], -1)
N /= np.linalg.norm(N, axis=-1, keepdims=True) + 1e-9
L = A([-0.6, 0.55, 0.6]); L /= np.linalg.norm(L)
dif = np.clip(N @ L, 0, 1)
# cheap AO: sample sdf along the normal
ao = np.ones(len(P))
for k, s in enumerate((0.04, 0.09, 0.16)):
    ao -= np.clip(s - sdf(P + N*s), 0, 1) * (1.8/(k+1))
lum = np.clip(0.15 + 0.85*dif*np.clip(ao, 0, 1), 0, 1)
lum = np.where(P[:, 1] < -0.75, lum*0.55, lum)   # the jacket sits in shadow below the face
hit = hit.reshape(Hd, Wd); lum = lum.reshape(Hd, Wd)
lum[~hit] = 0
Nn = N.reshape(Hd, Wd, 3)

# ---------- ground: ochre (yellow screened with black), darker scrubbed halo round the head
noise = fbm(H, W, seed=4, base=6)
dist = gaussian_filter(hit.astype(float), 25)
bg = 0.30 + (noise-0.5)*0.35 + dist*0.5
img = ramp(np.clip(bg, 0, 1)*0.9, [Y, K])                  # 0 = yellow, 1 = black
im = Image.fromarray(img); d = ImageDraw.Draw(im)
# underpaint inside the figure: lighter ochre where lit, dark where not
fig_t = np.clip(0.95 - lum*0.85, 0, 1)
paste_arr(im, ramp(fig_t, [Wh, Y, K]), hit)
d = ImageDraw.Draw(im)

# ---------- the cage: the frame he drew round his sitters, redrawn many times
for k in range(9):
    j = lambda: rng.normal(0, 4)
    box = [(52+j(), 70+j()), (350+j(), 66+j()), (356+j(), 560+j()), (46+j(), 566+j())]
    d.line(box + [box[0]], fill=K if k % 3 else Wh, width=1)
for k in range(6):  # floor / table edge lines behind
    y0 = 470 + rng.normal(0, 4)
    d.line((48, y0, 352, y0 - 6 + rng.normal(0, 3)), fill=K, width=1)
for k in range(4):  # the vertical axis line he measured with
    x0 = 200 + rng.normal(0, 3)
    d.line((x0, 72, x0 + rng.normal(0, 4), 120), fill=R)

# ---------- stroke field: wrap around the form (perpendicular to the screen normal)
nx = gaussian_filter(Nn[..., 0], 2); ny = gaussian_filter(-Nn[..., 1], 2)
ang = np.arctan2(ny, nx) + math.pi/2
lum_s = gaussian_filter(lum, 1.2)
def trace(x, y, steps, dl, sign):
    pts = [(x, y)]
    for s in range(steps):
        xi, yi = int(x), int(y)
        if not (0 <= xi < W and 0 <= yi < H) or not hit[yi, xi]: break
        a = (ang[yi, xi] if P3[yi, xi, 1] > -0.75 else math.pi/2 + 0.3*math.sin(xi/40)) + rng.normal(0, 0.12)
        x += sign*dl*math.cos(a); y += sign*dl*math.sin(a)
        pts.append((x, y))
    return pts
P3 = P.reshape(Hd, Wd, 3)
hy, hx = np.where(hit)
order = rng.permutation(len(hx))
nk = nw = nr = 0
for i in order[:26000]:
    x, y = hx[i] + rng.random(), hy[i] + rng.random()
    l = lum_s[hy[i], hx[i]]
    r_ = rng.random()
    if r_ < (1-l)**1.2 * 0.7:
        col = K; nk += 1
    elif r_ > 1 - l**3 * 0.35:
        col = Wh; nw += 1
    elif r_ < 0.58 and rng.random() < 0.02:
        col = R; nr += 1
    else:
        continue
    pts = trace(x, y, rng.integers(4, 12), 1.8, 1 if rng.random() < 0.5 else -1)
    if len(pts) > 2: d.line(pts, fill=col)

# ---------- silhouette and inner contours, searched for again and again
edge = hit & ~binary_erosion(hit, iterations=1)
# depth discontinuities inside (nose against cheek, ear, chin over neck)
tt = t.reshape(Hd, Wd); tt[~hit] = 9
dz = np.abs(np.gradient(gaussian_filter(tt, 0.7))[0]) + np.abs(np.gradient(gaussian_filter(tt, 0.7))[1])
inner = hit & (dz > 0.025)
ey, ex = np.where(edge | inner)
for i in rng.choice(len(ex), size=min(2600, len(ex)), replace=False):
    x, y = ex[i] + rng.normal(0, 1.4), ey[i] + rng.normal(0, 1.4)
    a = ang[ey[i], ex[i]] + rng.normal(0, 0.2)
    L_ = rng.uniform(3, 10)
    d.line((x - L_*math.cos(a)/2, y - L_*math.sin(a)/2, x + L_*math.cos(a)/2, y + L_*math.sin(a)/2),
           fill=K if rng.random() < 0.85 else R)
# the eyes: dark, insistent knots of line
P2 = P.reshape(Hd, Wd, 3)
for sgn in (-1, 1):
    c = A([sgn*0.14*0.86, 0.20, 0.42])
    # project the socket centre
    rel = c - ro; zc = rel @ fw
    sx = Wd/2 + (rel @ rt)/zc*1.55*(Hd/2); sy = Hd*0.47 - (rel @ up)/zc*1.55*(Hd/2)
    for k in range(14):
        scribble(d, sx + rng.normal(0, 1), sy + rng.normal(0, 1), rng.uniform(4, 9), rng.uniform(3, 6), 1, rng, K)
    d.ellipse((sx-1.5, sy-1.5, sx+1.5, sy+1.5), fill=Wh)

# the walking man, very small, on the table edge in the background
walker(d, 60, 468, 34, K, facing=1)
save(im)
