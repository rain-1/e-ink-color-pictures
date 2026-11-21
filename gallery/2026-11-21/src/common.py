"""Shared toolkit for 2026-11-21 — "things that stay up".

Everything is drawn at 3x (1200x1800) on one RGB image. Strokes and flats in the six
exact palette colours stay crisp; anything else (mixes, gradients, shading) is
Floyd-Steinberg dithered at the end. `finish()` writes a palette-clean 400x600 image,
so render with `--dither none`.
"""
import math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

S = 3
W, H = 400, 600
K = (0, 0, 0); WH = (255, 255, 255); R = (0xE0, 0x1B, 0x24)
Y = (0xF5, 0xD4, 0x00); B = (0x12, 0x3D, 0xB0); G = (0x1E, 0x9B, 0x3C)
PAL = [K, WH, R, Y, B, G]
PALA = np.array(PAL, dtype=np.float32)

FONTS = {
    "serif": "/usr/share/fonts/truetype/freefont/FreeSerif.ttf",
    "serif-i": "/usr/share/fonts/truetype/freefont/FreeSerifItalic.ttf",
    "serif-b": "/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf",
    "serif-bi": "/usr/share/fonts/truetype/freefont/FreeSerifBoldItalic.ttf",
    "sans": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
}


def mix(a, b, t):
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))


def font(name, px):
    return ImageFont.truetype(FONTS[name], int(round(px * S)))


def new(bg=WH):
    img = Image.new("RGB", (W * S, H * S), bg)
    d = ImageDraw.Draw(img)
    d.fontmode = "1"
    return img, d


def P(*pts):
    """scale a flat list / list of pairs from final px to canvas px"""
    if len(pts) == 1:
        pts = pts[0]
    out = []
    for p in pts:
        if isinstance(p, (tuple, list)):
            out.append((p[0] * S, p[1] * S))
        else:
            out.append(p * S)
    return out


def BX(x0, y0, x1, y1):
    """scaled box with sorted corners"""
    return [min(x0, x1) * S, min(y0, y1) * S, max(x0, x1) * S, max(y0, y1) * S]


def fbm(shape, scale=64, octaves=4, seed=0, persistence=0.5):
    """smooth value noise in 0..1, shape=(h,w), scale = feature size in px"""
    rng = np.random.default_rng(seed)
    h, w = shape
    out = np.zeros(shape, np.float32); amp = 1.0; tot = 0
    for o in range(octaves):
        s = max(2, int(scale / (2 ** o)))
        small = rng.random((h // s + 3, w // s + 3)).astype(np.float32)
        im = Image.fromarray((small * 255).astype(np.uint8)).resize(
            ((w // s + 3) * s, (h // s + 3) * s), Image.BICUBIC)
        out += amp * (np.asarray(im, np.float32)[:h, :w] / 255)
        tot += amp; amp *= persistence
    return out / tot


def lerp_rgb(stops, t):
    """t: array 0..1 ; stops: [(pos, rgb), ...] -> (...,3) float array"""
    t = np.clip(t, 0, 1)
    out = np.zeros(t.shape + (3,), np.float32)
    for (p0, c0), (p1, c1) in zip(stops[:-1], stops[1:]):
        m = (t >= p0) & (t <= p1)
        f = ((t - p0) / max(p1 - p0, 1e-6))[..., None]
        seg = np.array(c0, np.float32) + (np.array(c1, np.float32) - np.array(c0, np.float32)) * f
        out[m] = seg[m]
    return out


def paint(img, rgb, mask=None):
    """paste a float/uint8 (h,w,3) array onto img (same size), optionally through a mask"""
    a = np.asarray(img).copy()
    rgb = np.clip(rgb, 0, 255).astype(np.uint8)
    if mask is None:
        a[:] = rgb
    else:
        a[mask] = rgb[mask]
    img.paste(Image.fromarray(a))


def mask_of(drawfn):
    m = Image.new("L", (W * S, H * S), 0)
    drawfn(ImageDraw.Draw(m))
    return np.asarray(m) > 127


def finish(img, damp=0.92):
    """3x RGB -> 400x600 palette image. Blocks that are mostly one pure palette colour
    are fixed (crisp); the rest are box-averaged and FS-dithered (serpentine)."""
    a = np.asarray(img.convert("RGB"), np.float32).reshape(H, S, W, S, 3)
    mean = a.mean((1, 3))
    fixed = np.full((H, W), -1, np.int64); best = np.zeros((H, W), np.int64)
    for i, c in enumerate(PAL):
        cnt = (np.abs(a - np.array(c, np.float32)).sum(-1) < 3).sum((1, 3))
        fixed[cnt >= 5] = i
        best = np.maximum(best, cnt)
    buf = mean.tolist(); fx = fixed.tolist()
    pal = [tuple(map(float, c)) for c in PAL]
    idx = [[0] * W for _ in range(H)]
    for y in range(H):
        row = buf[y]; nxt = buf[y + 1] if y + 1 < H else None
        xs = range(W) if y % 2 == 0 else range(W - 1, -1, -1)
        dx = 1 if y % 2 == 0 else -1
        for x in xs:
            f = fx[y][x]
            if f >= 0:
                idx[y][x] = f; continue
            r, g, b = row[x]
            bi = 0; bd = 1e18
            for i, (pr, pg, pb) in enumerate(pal):
                dd = (r - pr) ** 2 + (g - pg) ** 2 + (b - pb) ** 2
                if dd < bd:
                    bd = dd; bi = i
            idx[y][x] = bi
            pr, pg, pb = pal[bi]
            er, eg, eb = (r - pr) * damp, (g - pg) * damp, (b - pb) * damp
            x1 = x + dx
            if 0 <= x1 < W and fx[y][x1] < 0:
                p = row[x1]; p[0] += er * .4375; p[1] += eg * .4375; p[2] += eb * .4375
            if nxt is not None:
                x0 = x - dx
                if 0 <= x0 < W and fx[y + 1][x0] < 0:
                    p = nxt[x0]; p[0] += er * .1875; p[1] += eg * .1875; p[2] += eb * .1875
                if fx[y + 1][x] < 0:
                    p = nxt[x]; p[0] += er * .3125; p[1] += eg * .3125; p[2] += eb * .3125
                if 0 <= x1 < W and fx[y + 1][x1] < 0:
                    p = nxt[x1]; p[0] += er * .0625; p[1] += eg * .0625; p[2] += eb * .0625
    out = PALA[np.array(idx)].astype(np.uint8)
    Image.fromarray(out, "RGB").save(os.environ.get("OUT_RAW", "out_raw.png"))


# ---------------------------------------------------------------- the balloon
R_EQ, R_NECK, T_EQ, T_NECK = 0.31, 0.135, 0.42, 0.80


def profile(t):
    """radius (fraction of height) of the 1783 Montgolfière at t = 0 (crown) .. 1 (mouth)"""
    t = np.asarray(t, np.float32)
    dome = R_EQ * np.sqrt(np.clip(1 - ((T_EQ - t) / T_EQ) ** 2, 0, 1))
    taper = R_NECK + (R_EQ - R_NECK) * (0.5 + 0.5 * np.cos(np.pi * np.clip((t - T_EQ) / (T_NECK - T_EQ), 0, 1)))
    neck = R_NECK + 0.02 * np.clip((t - T_NECK) / (1 - T_NECK), 0, 1)
    return np.where(t < T_EQ, dome, np.where(t < T_NECK, taper, neck))


def _stamp_lis(sz, col):
    im = Image.new("RGBA", (sz, int(sz * 1.3)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    w, h = im.size; cx = w / 2
    d.polygon([(cx, 0), (cx + w * .16, h * .30), (cx + w * .07, h * .62), (cx, h * .98),
               (cx - w * .07, h * .62), (cx - w * .16, h * .30)], fill=col)
    for sgn in (-1, 1):
        d.ellipse([cx + sgn * w * .30 - w * .17, h * .16, cx + sgn * w * .30 + w * .17, h * .56], fill=col)
        d.ellipse([cx + sgn * w * .22 - w * .13, h * .04, cx + sgn * w * .22 + w * .13, h * .44], fill=(0, 0, 0, 0))
        d.polygon([(cx + sgn * w * .14, h * .5), (cx + sgn * w * .46, h * .44), (cx + sgn * w * .40, h * .80),
                   (cx + sgn * w * .1, h * .64)], fill=col)
    d.rectangle([cx - w * .34, h * .60, cx + w * .34, h * .68], fill=col)
    return im


def _stamp_sun(sz):
    im = Image.new("RGBA", (sz, sz), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    c = sz / 2
    for k in range(24):
        a = k * math.tau / 24; rr = c * (0.98 if k % 2 == 0 else 0.78); wd = 0.085
        d.polygon([(c + rr * math.cos(a), c + rr * math.sin(a)),
                   (c + c * .5 * math.cos(a - wd * 2), c + c * .5 * math.sin(a - wd * 2)),
                   (c + c * .5 * math.cos(a + wd * 2), c + c * .5 * math.sin(a + wd * 2))], fill=Y)
    d.ellipse([c - c * .56, c - c * .56, c + c * .56, c + c * .56], fill=Y, outline=K, width=max(2, sz // 60))
    e = c * .2
    lw = max(2, sz // 50)
    for sgn in (-1, 1):
        d.arc([c + sgn * e - c * .13, c - c * .26, c + sgn * e + c * .13, c - c * .06], 180, 360, fill=K, width=lw)
        d.ellipse([c + sgn * e - c * .05, c - c * .17, c + sgn * e + c * .05, c - c * .07], fill=K)
        d.ellipse([c + sgn * c * .32 - c * .08, c + c * .02, c + sgn * c * .32 + c * .08, c + c * .18], fill=R)
    d.line([(c, c - c * .1), (c - c * .05, c + c * .1), (c + c * .04, c + c * .1)], fill=K, width=lw)
    d.arc([c - c * .2, c + c * .02, c + c * .2, c + c * .32], 20, 160, fill=K, width=lw)
    return im


_SKIN = {}


def skin(simple=False):
    """the unwrapped envelope: x = longitude 0..2pi, y = t 0..1"""
    if simple in _SKIN:
        return _SKIN[simple]
    SW, SH = 2160, 1080
    DB = mix(B, K, .45)
    im = Image.new("RGB", (SW, SH), B); d = ImageDraw.Draw(im); d.fontmode = "1"
    Yy = lambda t: int(t * SH)
    # gore seams
    for k in range(24):
        x = int((k + .5) * SW / 24)
        d.line([(x, 0), (x, SH)], fill=DB, width=3)
    # crown: gold cap with rays
    d.rectangle([0, 0, SW, Yy(.035)], fill=Y)
    for k in range(48):
        x = k * SW / 48
        d.polygon([(x, Yy(.03)), (x + SW / 96, Yy(.085)), (x + SW / 48, Yy(.03))], fill=Y)
    # fleur-de-lis ring
    n = 12 if not simple else 8
    lis = _stamp_lis(64, Y)
    for k in range(n):
        x = int((k + .5) * SW / n)
        if not simple:
            im.paste(lis, (x - 32, Yy(.105)), lis)
    # zodiac band
    d.rectangle([0, Yy(.19), SW, Yy(.275)], fill=Y)
    d.rectangle([0, Yy(.198), SW, Yy(.267)], fill=mix(B, K, .25) if not simple else R)
    d.line([(0, Yy(.185)), (SW, Yy(.185))], fill=K, width=3)
    d.line([(0, Yy(.279)), (SW, Yy(.279))], fill=K, width=3)
    if not simple:
        zf = ImageFont.truetype(FONTS["sans"], 62)
        for k in range(12):
            x = int((k + .5) * SW / 12)
            d.text((x, Yy(.2325)), chr(0x2648 + k) + "︎", font=zf, fill=Y, anchor="mm")
            xm = int(k * SW / 12)
            d.ellipse([xm - 9, Yy(.2325) - 9, xm + 9, Yy(.2325) + 9], fill=Y)
    # scattered lis above the equator
    if not simple:
        lis2 = _stamp_lis(46, Y)
        for k in range(16):
            x = int((k + (.0 if k % 2 else .0)) * SW / 16)
            y = Yy(.30) if k % 2 == 0 else Yy(.325)
            im.paste(lis2, (x - 23, y), lis2);
            if x == 0:
                im.paste(lis2, (SW - 23, y), lis2)
    # suns on the equator, royal cyphers between
    ns = 4
    sun = _stamp_sun(300 if not simple else 260)
    for k in range(ns):
        x = int((k + .5) * SW / ns)
        im.paste(sun, (x - sun.width // 2, Yy(T_EQ + .035) - sun.height // 2), sun)
        if simple:
            continue
        xc = int(k * SW / ns); yc = Yy(T_EQ + .03)
        for dx in ((0,) if xc else (0, SW)):
            X = xc + dx
            d.ellipse([X - 92, yc - 108, X + 92, yc + 108], outline=Y, width=10)
            for j in range(20):   # laurel leaves round the cartouche
                a = j * math.tau / 20
                lx, ly = X + 104 * math.cos(a), yc + 120 * math.sin(a)
                d.ellipse([lx - 12, ly - 7, lx + 12, ly + 7], fill=Y)
            lf = ImageFont.truetype(FONTS["serif-bi"], 150)
            d.text((X - 22, yc), "L", font=lf, fill=Y, anchor="mm")
            t2 = Image.new("L", (160, 180), 0); ImageDraw.Draw(t2).text((80, 90), "L", font=lf, fill=255, anchor="mm")
            t2 = t2.transpose(Image.FLIP_LEFT_RIGHT)
            im.paste(Y, (X + 22 - 80, yc - 90), t2)
            # crown above the cypher
            d.polygon([(X - 40, yc - 122), (X - 46, yc - 160), (X - 22, yc - 140), (X, yc - 170), (X + 22, yc - 140),
                       (X + 46, yc - 160), (X + 40, yc - 122)], fill=Y)
    # festoons (garlands) below the suns
    nf = 8
    for X in range(SW):
        ph = (X / SW * nf) % 1.0
        sag = math.sin(ph * math.pi)
        y0 = Yy(.60 + .045 * sag)
        d.line([(X, y0), (X, y0 + (14 if not simple else 20))], fill=Y)
        if not simple and X % 14 < 7:
            d.line([(X, y0 + 14), (X, y0 + 22)], fill=G)
    for k in range(nf):
        x = int(k * SW / nf)
        for X in ((x,) if x else (0, SW)):
            d.ellipse([X - 20, Yy(.59) - 20, X + 20, Yy(.59) + 20], fill=Y)
            d.polygon([(X - 12, Yy(.60)), (X + 12, Yy(.60)), (X + 5, Yy(.68)), (X, Yy(.66)), (X - 5, Yy(.68))], fill=Y)
    # red drapery with scalloped top and gold fringe
    nd = 8
    for X in range(SW):
        ph = ((X / SW * nd) + .5) % 1.0
        y0 = Yy(.70 + .035 * math.sin(ph * math.pi))
        d.line([(X, y0), (X, Yy(.86))], fill=R)
        d.line([(X, y0 - 8), (X, y0)], fill=Y)
        fold = math.sin(ph * math.pi * 6)
        if not simple and fold > .82:
            d.line([(X, y0 + 6), (X, Yy(.80))], fill=mix(R, K, .55))
    d.rectangle([0, Yy(.80), SW, Yy(.815)], fill=Y)
    if not simple:
        for X in range(0, SW, 18):
            d.line([(X, Yy(.815)), (X, Yy(.845))], fill=Y, width=6)
    # neck: blue with gold pilasters
    d.rectangle([0, Yy(.86), SW, SH], fill=B)
    for k in range(16):
        x = int(k * SW / 16)
        d.rectangle([x - 6, Yy(.865), x + 6, SH], fill=Y)
    d.rectangle([0, Yy(.975), SW, SH], fill=Y)
    _SKIN[simple] = np.asarray(im)
    return _SKIN[simple]


def balloon_mask(cx, cy_top, h, shape=None):
    """boolean mask (canvas px) of the envelope; cx, cy_top, h in final px"""
    shape = shape or (H * S, W * S)
    yy, xx = np.mgrid[0:shape[0], 0:shape[1]].astype(np.float32)
    t = (yy - cy_top * S) / (h * S)
    r = profile(np.clip(t, 0, 1)) * h * S
    return (t >= 0) & (t <= 1) & (np.abs(xx - cx * S) <= r)


def balloon(img, cx, cy_top, h, rot=0.35, simple=None, light=-0.55, outline=True, gallery=True,
            figures=True, tint=None, fire=False):
    """draw the Montgolfier balloon. cx, cy_top, h in final px. Returns envelope mask."""
    if simple is None:
        simple = h < 150
    a = np.asarray(img).copy()
    hs = h * S
    x0 = max(0, int((cx - h * .34) * S)); x1 = min(W * S, int((cx + h * .34) * S) + 1)
    y0 = max(0, int(cy_top * S)); y1 = min(H * S, int((cy_top + h) * S) + 1)
    if x1 <= x0 or y1 <= y0:
        return None
    yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
    t = (yy - cy_top * S) / hs
    r = profile(np.clip(t, 0, 1)) * hs
    u = (xx - cx * S) / np.maximum(r, 1e-3)
    inside = (t >= 0) & (t <= 1) & (np.abs(u) <= 1)
    uc = np.clip(u, -1, 1)
    th = np.arcsin(uc) + rot
    sk = skin(simple)
    sx = ((th / math.tau) % 1.0 * sk.shape[1]).astype(int) % sk.shape[1]
    sy = np.clip((t * sk.shape[0]).astype(int), 0, sk.shape[0] - 1)
    col = sk[sy, sx].astype(np.float32)
    # shading: lambert-ish from upper left, darker rim on the right, under-belly shadow
    nz = np.sqrt(np.clip(1 - uc * uc, 0, 1))
    lum = 0.50 + light * uc * 0.75 + 0.22 * nz - 0.30 * np.clip((t - .45) / .4, 0, 1) + 0.18 * np.clip((.3 - t) / .3, 0, 1)
    dark = np.clip((0.48 - lum) / 0.55, 0, 0.72)[..., None]
    lite = np.clip((lum - 0.80) / 0.5, 0, 0.42)[..., None]
    col = col * (1 - dark)
    col = col + (255 - col) * lite
    if tint is not None:
        col = col * (1 - tint[1]) + np.array(tint[0], np.float32) * tint[1]
    sub = a[y0:y1, x0:x1]
    sub[inside] = np.clip(col, 0, 255).astype(np.uint8)[inside]
    if outline:
        m = Image.fromarray((inside * 255).astype(np.uint8))
        er = np.asarray(m.filter(ImageFilter.MinFilter(2 * (S + 1) + 1))) > 127
        sub[inside & ~er] = 0
    a[y0:y1, x0:x1] = sub
    img.paste(Image.fromarray(a))
    d = ImageDraw.Draw(img); d.fontmode = "1"
    if gallery:
        # wicker gallery ring round the neck
        gy = cy_top + h * .90; gr = h * .215; gh = h * .055; ry = gr * .22
        lw = max(1, int(S * max(1, h / 300)))
        def ring(yc, front, fill):
            box = P(cx - gr, yc - ry, cx + gr, yc + ry)
            if front:
                d.pieslice(box, 0, 180, fill=fill)
            else:
                d.ellipse(box, fill=fill)
        # back rim (behind the neck) is hidden by the envelope already drawn; draw front apron
        pts = []
        for k in range(41):
            ang = math.pi * k / 40
            pts.append((cx + gr * math.cos(ang), gy + ry * math.sin(ang)))
        bot = [(x, y + gh) for (x, y) in pts]
        d.polygon(P(pts + bot[::-1]), fill=Y)
        if h >= 90:
            for k in range(0, 40):
                (xa, ya), (xb, yb) = pts[k], bot[min(40, k + 3)]
                d.line(P((xa, ya), (xb, yb)), fill=K, width=1 if h < 200 else 2)
                (xa, ya), (xb, yb) = pts[min(40, k + 3)], bot[k]
                d.line(P((xa, ya), (xb, yb)), fill=K, width=1 if h < 200 else 2)
        d.line(P(pts), fill=K, width=lw); d.line(P(bot), fill=K, width=lw)
        d.line(P(pts[0], bot[0]), fill=K, width=lw); d.line(P(pts[-1], bot[-1]), fill=K, width=lw)
        # red cloth swags over the rail
        if h >= 120:
            for k in range(0, 40, 8):
                seg = pts[k:k + 9]
                mid = [(x, y + gh * (.55 * math.sin(math.pi * i / 8))) for i, (x, y) in enumerate(seg)]
                d.polygon(P(seg + mid[::-1]), fill=R)
                d.line(P(mid), fill=K, width=1)
        if figures and h >= 90:
            # two aeronauts on opposite sides of the gallery, one waving his hat
            for sgn, wave in ((-1, True), (1, False)):
                fx = cx + sgn * gr * .82; fy = gy + ry * .45
                fh = h * .075
                d.polygon(P((fx - fh * .16, fy), (fx + fh * .16, fy), (fx + fh * .2, fy - fh * .62), (fx - fh * .2, fy - fh * .62)),
                          fill=K if sgn > 0 else R)
                d.ellipse(P(fx - fh * .12, fy - fh * .88, fx + fh * .12, fy - fh * .62), fill=WH, outline=K, width=S)
                d.polygon(P((fx - fh * .2, fy - fh * .86), (fx + fh * .2, fy - fh * .86), (fx, fy - fh * 1.02)), fill=K)
                if wave:
                    d.line(P((fx - fh * .15, fy - fh * .5), (fx - fh * .5, fy - fh * 1.0)), fill=K, width=max(S, int(fh * .1 * S)))
                    d.polygon(P((fx - fh * .72, fy - fh * 1.0), (fx - fh * .3, fy - fh * 1.0), (fx - fh * .5, fy - fh * 1.2)), fill=K)
                else:
                    d.line(P((fx + fh * .15, fy - fh * .5), (fx + fh * .5, fy - fh * .2)), fill=K, width=max(S, int(fh * .1 * S)))
    if fire:
        fy = cy_top + h * 1.0
        d.ellipse(P(cx - h * .035, fy - h * .02, cx + h * .035, fy + h * .025), fill=R)
        d.ellipse(P(cx - h * .016, fy - h * .008, cx + h * .016, fy + h * .018), fill=Y)
    return balloon_mask(cx, cy_top, h)


def cumulus(img, cx, cy, w, seed=0, base=WH, shade=None, flat=True):
    """a Magritte cumulus: lumpy top, flattish base, soft blue-grey underside."""
    rng = np.random.default_rng(seed)
    m = Image.new("L", img.size, 0); d = ImageDraw.Draw(m)
    n = int(6 + w / 14)
    hgt = w * .30
    for i in range(n):
        f = i / (n - 1)
        x = cx - w / 2 + f * w
        env = math.sin(f * math.pi) ** .7
        r = (w * .07 + w * .10 * rng.random()) * (0.55 + 0.6 * env)
        y = cy - hgt * env * (0.35 + 0.65 * rng.random())
        d.ellipse(P(x - r, y - r, x + r, y + r), fill=255)
        d.ellipse(P(x - r * 1.2, cy - r * .9, x + r * 1.2, cy + r * .35), fill=255)
    if flat:
        d.rectangle(P(cx - w, cy + w * .035, cx + w, cy + w), fill=0)
    mk = np.asarray(m) > 127
    ys, xs = np.nonzero(mk)
    if len(ys) == 0:
        return mk
    a = np.asarray(img).astype(np.float32)
    yy = np.arange(img.size[1], dtype=np.float32)[:, None]
    top = ys.min(); bot = ys.max()
    f = np.clip((yy - top) / max(1, bot - top), 0, 1)
    nz = fbm((img.size[1], img.size[0]), scale=w * S / 6, octaves=3, seed=seed + 5)
    sh = np.clip((f - 0.45) * 1.6 + (nz - .5) * .9, 0, 1) * 0.5
    sc = np.array(shade if shade is not None else mix(B, K, .15), np.float32)
    col = np.array(base, np.float32)[None, None, :] * (1 - sh[..., None]) + sc * sh[..., None]
    a[mk] = col[mk]
    img.paste(Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)))
    return mk


def tree(d, x, y, length, ang=-math.pi / 2, depth=7, width=None, col=K, rng=None, spread=.45, shrink=.74):
    """bare November tree, recursive; coordinates in final px"""
    rng = rng or np.random.default_rng(1)
    width = width if width is not None else max(1.0, length / 7)
    x2 = x + length * math.cos(ang); y2 = y + length * math.sin(ang)
    d.line(P((x, y), (x2, y2)), fill=col, width=max(1, int(round(width * S))))
    if depth <= 0 or length < 1.6:
        return
    n = 2 if rng.random() < .7 else 3
    for i in range(n):
        da = (i - (n - 1) / 2) * spread * (1.4 if n == 2 else 1) + (rng.random() - .5) * .35
        tree(d, x2, y2, length * shrink * (.85 + .3 * rng.random()), ang + da, depth - 1, width * .68, col, rng, spread, shrink)


def text(d, xy, s, fnt="serif", px=12, fill=K, anchor="mm", spacing=0):
    f = font(fnt, px)
    if spacing:
        # letterspaced
        widths = [d.textlength(ch, font=f) for ch in s]
        total = sum(widths) + spacing * S * (len(s) - 1)
        x = xy[0] * S - (total / 2 if anchor[0] == "m" else 0 if anchor[0] == "l" else total)
        for ch, wd in zip(s, widths):
            d.text((x, xy[1] * S), ch, font=f, fill=fill, anchor="l" + anchor[1])
            x += wd + spacing * S
    else:
        d.text((xy[0] * S, xy[1] * S), s, font=f, fill=fill, anchor=anchor)
