"""Shared drawing helpers for the 2026-09-21 Wells plates.

Everything is emitted as SVG in a 400x600 user-unit space (the panel's own
pixels), rasterised at 2x by render.py and quantised with --dither none, so
every colour written here must already be one of the six panel colours.

The vocabulary is Victorian reproductive engraving: line is the only tone.
Flats are made of hatching, shadow of cross-hatching, sky of ruled lines that
thin out. Nothing here is a gradient.
"""
import math
import random

W, H = 400, 600

K = "#000000"   # black
P = "#FFFFFF"   # white  (the paper)
R = "#E01B24"   # red
Y = "#F5D400"   # yellow
B = "#123DB0"   # blue
G = "#1E9B3C"   # green

SERIF = "Liberation Serif, DejaVu Serif, serif"


class Plate:
    def __init__(self, bg=P, w=W, h=H):
        self.w, self.h = w, h
        self.defs = []
        self.body = []
        self._n = 0
        self.body.append(f'<rect width="{w}" height="{h}" fill="{bg}"/>')

    def uid(self, tag="id"):
        self._n += 1
        return f"{tag}{self._n}"

    def add(self, s):
        self.body.append(s)

    def clip(self, d):
        """Register a clip path from path data; returns its id."""
        i = self.uid("clip")
        self.defs.append(f'<clipPath id="{i}"><path d="{d}"/></clipPath>')
        return i

    def clip_rect(self, x, y, w, h):
        i = self.uid("clip")
        self.defs.append(f'<clipPath id="{i}"><rect x="{x}" y="{y}" width="{w}" height="{h}"/></clipPath>')
        return i

    def clip_circle(self, cx, cy, r):
        i = self.uid("clip")
        self.defs.append(f'<clipPath id="{i}"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>')
        return i

    # ---- line work -------------------------------------------------------

    def rule_field(self, clip_id, bounds, angle, spacing, width=1.0,
                   color=K, phase=0.0, taper=None, dash=None, jitter=0.0,
                   seed=7):
        """Parallel ruled lines across `bounds` (x0,y0,x1,y1), clipped.

        taper: optional f(t)->width_multiplier, t = 0..1 across the field, so a
        sky can thin out towards the horizon the way a ruled engraving does.
        """
        rnd = random.Random(seed)
        x0, y0, x1, y1 = bounds
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        diag = math.hypot(x1 - x0, y1 - y0) / 2 + 4
        a = math.radians(angle)
        dx, dy = math.cos(a), math.sin(a)          # along the line
        nx, ny = -dy, dx                           # across the lines
        out = [f'<g clip-path="url(#{clip_id})" stroke="{color}" fill="none" stroke-linecap="butt">']
        n = int(2 * diag / spacing) + 2
        for i in range(-n, n + 1):
            t = i * spacing + phase
            if abs(t) > diag + spacing:
                continue
            wmul = 1.0
            if taper:
                wmul = taper((t + diag) / (2 * diag))
                if wmul <= 0.02:
                    continue
            jx = rnd.uniform(-jitter, jitter) if jitter else 0.0
            mx, my = cx + nx * t + nx * jx, cy + ny * t + ny * jx
            ax, ay = mx - dx * diag, my - dy * diag
            bx, by = mx + dx * diag, my + dy * diag
            d = f' stroke-dasharray="{dash}"' if dash else ""
            out.append(f'<line x1="{ax:.2f}" y1="{ay:.2f}" x2="{bx:.2f}" y2="{by:.2f}" '
                       f'stroke-width="{width * wmul:.2f}"{d}/>')
        out.append('</g>')
        self.add("".join(out))

    def hatch(self, d, bounds, angle=45, spacing=3.2, width=1.0, color=K, **kw):
        """Hatch the interior of a path."""
        self.rule_field(self.clip(d), bounds, angle, spacing, width, color, **kw)

    def crosshatch(self, d, bounds, angles=(45, -45), spacing=3.4, width=1.0, color=K):
        c = self.clip(d)
        for a in angles:
            self.rule_field(c, bounds, a, spacing, width, color)

    def contour_shade(self, clip_id, cx, cy, r0, r1, step=3.0, width=1.0,
                      color=K, a0=0, a1=360, taper=None):
        """Concentric arcs — the engraver's way of rounding a solid."""
        out = [f'<g clip-path="url(#{clip_id})" stroke="{color}" fill="none">']
        r = r0
        i = 0
        while r < r1:
            wmul = taper(( r - r0) / max(1e-6, r1 - r0)) if taper else 1.0
            if wmul > 0.02:
                out.append(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" '
                           f'stroke-width="{width * wmul:.2f}"/>')
            r += step
            i += 1
        out.append('</g>')
        self.add("".join(out))

    def stipple(self, clip_id, bounds, n, rmin=0.5, rmax=1.1, color=K, seed=3,
                density=None):
        """Dotted tone. density: f(x,y)->0..1 probability of keeping a dot."""
        rnd = random.Random(seed)
        x0, y0, x1, y1 = bounds
        pts = []
        for _ in range(n):
            x = rnd.uniform(x0, x1)
            y = rnd.uniform(y0, y1)
            if density and rnd.random() > density(x, y):
                continue
            pts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rnd.uniform(rmin, rmax):.2f}"/>')
        self.add(f'<g clip-path="url(#{clip_id})" fill="{color}">' + "".join(pts) + '</g>')

    # ---- objects ---------------------------------------------------------

    def gear(self, cx, cy, r, teeth, tooth=4.0, fill="none", stroke=K, sw=1.4,
             bore=None, spokes=0):
        pts = []
        for i in range(teeth * 2):
            a = 2 * math.pi * i / (teeth * 2)
            rr = r + tooth / 2 if i % 2 == 0 else r - tooth / 2
            pts.append(f"{cx + rr * math.cos(a):.2f},{cy + rr * math.sin(a):.2f}")
        self.add(f'<polygon points="{" ".join(pts)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
        if spokes:
            for i in range(spokes):
                a = 2 * math.pi * i / spokes
                self.add(f'<line x1="{cx:.2f}" y1="{cy:.2f}" '
                         f'x2="{cx + (r - tooth) * math.cos(a):.2f}" y2="{cy + (r - tooth) * math.sin(a):.2f}" '
                         f'stroke="{stroke}" stroke-width="{sw}"/>')
        if bore:
            self.add(f'<circle cx="{cx}" cy="{cy}" r="{bore}" fill="{P}" stroke="{stroke}" stroke-width="{sw}"/>')

    def dial(self, cx, cy, r, needle_deg, ticks=24, face=P, stroke=K, sw=1.3,
             needle_color=R, label=None, label_size=0):
        self.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{face}" stroke="{stroke}" stroke-width="{sw}"/>')
        for i in range(ticks):
            a = 2 * math.pi * i / ticks - math.pi / 2
            long = (i % (ticks // 4 if ticks >= 8 else 2) == 0)
            r0 = r - (r * 0.30 if long else r * 0.16)
            self.add(f'<line x1="{cx + r0 * math.cos(a):.2f}" y1="{cy + r0 * math.sin(a):.2f}" '
                     f'x2="{cx + (r - 1.2) * math.cos(a):.2f}" y2="{cy + (r - 1.2) * math.sin(a):.2f}" '
                     f'stroke="{stroke}" stroke-width="{1.5 if long else 1.0}"/>')
        a = math.radians(needle_deg - 90)
        self.add(f'<line x1="{cx:.2f}" y1="{cy:.2f}" x2="{cx + r * 0.78 * math.cos(a):.2f}" '
                 f'y2="{cy + r * 0.78 * math.sin(a):.2f}" stroke="{needle_color}" stroke-width="2.2" stroke-linecap="round"/>')
        self.add(f'<circle cx="{cx}" cy="{cy}" r="2.0" fill="{stroke}"/>')
        if label:
            self.text(cx, cy + r + label_size + 2, label, size=label_size or 9, anchor="middle")

    def rivets(self, pts, r=1.6, fill=P, stroke=K, sw=1.0):
        for (x, y) in pts:
            self.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

    # ---- typography ------------------------------------------------------

    def text(self, x, y, s, size=11, color=K, anchor="start", family=SERIF,
             weight="normal", style="normal", spacing=0, opacity=None):
        ls = f' letter-spacing="{spacing}"' if spacing else ""
        op = f' opacity="{opacity}"' if opacity else ""
        s = (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
        self.add(f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
                 f'fill="{color}" text-anchor="{anchor}" font-weight="{weight}" '
                 f'font-style="{style}"{ls}{op}>{s}</text>')

    def text_on_arc(self, cx, cy, r, s, size=10, color=K, start_deg=180,
                    sweep=180, family=SERIF, spacing=0):
        pid = self.uid("arc")
        a0 = math.radians(start_deg)
        a1 = math.radians(start_deg + sweep)
        large = 1 if abs(sweep) > 180 else 0
        sweepf = 1 if sweep > 0 else 0
        d = (f"M {cx + r * math.cos(a0):.2f} {cy + r * math.sin(a0):.2f} "
             f"A {r} {r} 0 {large} {sweepf} {cx + r * math.cos(a1):.2f} {cy + r * math.sin(a1):.2f}")
        self.defs.append(f'<path id="{pid}" d="{d}"/>')
        ls = f' letter-spacing="{spacing}"' if spacing else ""
        s = s.replace("&", "&amp;")
        self.add(f'<text font-family="{family}" font-size="{size}" fill="{color}"{ls}>'
                 f'<textPath href="#{pid}" startOffset="50%" text-anchor="middle">{s}</textPath></text>')

    def leader(self, x0, y0, x1, y1, s, size=10, color=K, anchor="start",
               dot=1.8, sw=1.0, family=SERIF):
        """Numbered leader line with a dot at the thing and a label at the end."""
        self.add(f'<circle cx="{x0}" cy="{y0}" r="{dot}" fill="{color}"/>')
        self.add(f'<path d="M {x0} {y0} L {x1} {y1}" stroke="{color}" stroke-width="{sw}" fill="none"/>')
        off = 3 if anchor == "start" else -3
        self.text(x1 + off, y1 + size * 0.35, s, size=size, color=color, anchor=anchor, family=family)

    # ---- frame -----------------------------------------------------------

    def border(self, m=10, color=K, inner=P, rules=(2.4, 1.0), gap=4, corners=True):
        x, y = m, m
        w, h = self.w - 2 * m, self.h - 2 * m
        off = 0
        for i, sw in enumerate(rules):
            self.add(f'<rect x="{x + off}" y="{y + off}" width="{w - 2 * off}" height="{h - 2 * off}" '
                     f'fill="none" stroke="{color}" stroke-width="{sw}"/>')
            off += gap
        if corners:
            for (cx, cy) in ((x, y), (x + w, y), (x, y + h), (x + w, y + h)):
                self.add(f'<circle cx="{cx}" cy="{cy}" r="3.4" fill="{inner}" stroke="{color}" stroke-width="1.6"/>')

    def svg(self):
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
                f'viewBox="0 0 {self.w} {self.h}">'
                + ("<defs>" + "".join(self.defs) + "</defs>" if self.defs else "")
                + "".join(self.body) + "</svg>")

    def save(self, path=None, names=(K, P, R, Y, B, G), scale=2):
        """Write the SVG beside the source and a panel-clean PNG to $OUT_RAW.

        Rendered at `scale`x and reduced, then unmixed onto `names` here rather
        than left for render.py, so the only colours that reach the quantiser
        are ones this drawing actually asked for.
        """
        import os
        src = self.svg()
        if path:
            with open(path, "w") as f:
                f.write(src)
        out = os.environ.get("OUT_RAW")
        if out:
            import io
            import cairosvg
            from PIL import Image
            buf = io.BytesIO()
            cairosvg.svg2png(bytestring=src.encode(), write_to=buf,
                             output_width=self.w * scale, output_height=self.h * scale)
            im = Image.open(buf).convert("RGB")
            if scale != 1:
                im = im.resize((self.w, self.h), Image.LANCZOS)
            snap(im, list(names)).save(out)
        return src


PALETTE_RGB = {K: (0, 0, 0), P: (255, 255, 255), R: (0xE0, 0x1B, 0x24),
               Y: (0xF5, 0xD4, 0x00), B: (0x12, 0x3D, 0xB0), G: (0x1E, 0x9B, 0x3C)}


def snap(img, names):
    """Map a rendered image onto the panel colours by *unmixing* it.

    A six-colour print has no greys and no tints, so every soft pixel in the
    raster is an antialiased blend of exactly two of the inks. For each pixel
    we find the pair of palette colours (and the mix fraction) that explains it
    best, then round to whichever of the two it is mostly made of. That is why
    a black rule over a yellow flat stays black and yellow instead of turning
    olive, and why mid-grey stops resolving to blue.
    """
    import numpy as np
    from PIL import Image
    pal = np.array([PALETTE_RGB[n] for n in names], dtype=np.float32)
    a = np.asarray(img.convert("RGB"), dtype=np.float32)
    h, w, _ = a.shape
    flat = a.reshape(-1, 3)
    best_res = np.full(len(flat), np.inf, dtype=np.float32)
    best_idx = np.zeros(len(flat), dtype=np.int32)
    n = len(pal)
    for i in range(n):
        for j in range(i, n):
            pi, pj = pal[i], pal[j]
            d = pi - pj
            dd = float((d * d).sum())
            if dd < 1e-6:
                alpha = np.ones(len(flat), dtype=np.float32)
            else:
                alpha = np.clip(((flat - pj) @ d) / dd, 0.0, 1.0)
            mix = pj[None, :] + alpha[:, None] * d[None, :]
            res = ((flat - mix) ** 2).sum(1)
            better = res < best_res
            if better.any():
                pick = np.where(alpha >= 0.5, i, j).astype(np.int32)
                best_idx = np.where(better, pick, best_idx)
                best_res = np.where(better, res, best_res)
    out = pal[best_idx].astype(np.uint8).reshape(h, w, 3)
    return Image.fromarray(out, "RGB")


def smoothstep(a, b, t):
    t = max(0.0, min(1.0, (t - a) / (b - a)))
    return t * t * (3 - 2 * t)


def poly(pts):
    return "M " + " L ".join(f"{x:.2f},{y:.2f}" for x, y in pts) + " Z"
