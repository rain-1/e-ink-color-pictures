"""Morning: the whole International Code of Signals as a printed plate.
Twenty-six letter flags in their true colours (they only ever use red,
yellow, blue, black and white -- the panel's own inks), the answering
pennant, and the day's hoist "UW" in the last cell. Black outlines on paper."""
import os

from PIL import Image, ImageDraw, ImageFont

S = 4
W, H = 400 * S, 600 * S
K = (0, 0, 0); Wt = (255, 255, 255); R = (0xE0, 0x1B, 0x24)
Y = (0xF5, 0xD4, 0x00); B = (0x12, 0x3D, 0xB0)

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"

img = Image.new("RGB", (W, H), Wt)
d = ImageDraw.Draw(img)


def flag(letter, fw, fh):
    """Return an RGB image of the letter flag, fw x fh (already supersampled)."""
    im = Image.new("RGB", (fw, fh), Wt)
    g = ImageDraw.Draw(im)
    w, h = fw, fh
    L = letter

    def rect(x0, y0, x1, y1, c):
        g.rectangle([x0 * w, y0 * h, x1 * w - 1, y1 * h - 1], fill=c)

    def poly(pts, c):
        g.polygon([(x * w, y * h) for x, y in pts], fill=c)

    if L == "A":
        rect(0, 0, .5, 1, Wt); rect(.5, 0, 1, 1, B)
    elif L == "B":
        rect(0, 0, 1, 1, R)
    elif L == "C":
        for i, c in enumerate([B, Wt, R, Wt, B]):
            rect(0, i / 5, 1, (i + 1) / 5, c)
    elif L == "D":
        rect(0, 0, 1, 1, Y); rect(0, .2, 1, .8, B)
    elif L == "E":
        rect(0, 0, 1, .5, B); rect(0, .5, 1, 1, R)
    elif L == "F":
        poly([(.5, 0), (1, .5), (.5, 1), (0, .5)], R)
    elif L == "G":
        for i in range(6):
            rect(i / 6, 0, (i + 1) / 6, 1, Y if i % 2 == 0 else B)
    elif L == "H":
        rect(.5, 0, 1, 1, R)
    elif L == "I":
        rect(0, 0, 1, 1, Y)
        g.ellipse([w * .27, h * .2, w * .73, h * .8], fill=K)
    elif L == "J":
        rect(0, 0, 1, 1 / 3, B); rect(0, 2 / 3, 1, 1, B)
    elif L == "K":
        rect(0, 0, .5, 1, Y); rect(.5, 0, 1, 1, B)
    elif L == "L":
        rect(0, 0, .5, .5, Y); rect(.5, 0, 1, .5, K)
        rect(0, .5, .5, 1, K); rect(.5, .5, 1, 1, Y)
    elif L == "M":
        rect(0, 0, 1, 1, B)
        g.line([(0, 0), (w, h)], fill=Wt, width=int(h * .2))
        g.line([(0, h), (w, 0)], fill=Wt, width=int(h * .2))
    elif L == "N":
        for i in range(4):
            for j in range(4):
                rect(i / 4, j / 4, (i + 1) / 4, (j + 1) / 4, B if (i + j) % 2 == 0 else Wt)
    elif L == "O":
        poly([(0, 0), (1, 0), (0, 1)], R); poly([(1, 0), (1, 1), (0, 1)], Y)
    elif L == "P":
        rect(0, 0, 1, 1, B); rect(.25, .25, .75, .75, Wt)
    elif L == "Q":
        rect(0, 0, 1, 1, Y)
    elif L == "R":
        rect(0, 0, 1, 1, R)
        rect(.4, 0, .6, 1, Y); rect(0, .4, 1, .6, Y)
    elif L == "S":
        rect(.25, .25, .75, .75, B)
    elif L == "T":
        rect(0, 0, 1 / 3, 1, R); rect(2 / 3, 0, 1, 1, B)
    elif L == "U":
        rect(0, 0, .5, .5, R); rect(.5, .5, 1, 1, R)
    elif L == "V":
        g.line([(0, 0), (w, h)], fill=R, width=int(h * .2))
        g.line([(0, h), (w, 0)], fill=R, width=int(h * .2))
    elif L == "W":
        rect(0, 0, 1, 1, B); rect(.17, .2, .83, .8, Wt); rect(.36, .38, .64, .62, R)
    elif L == "X":
        rect(.4, 0, .6, 1, B); rect(0, .4, 1, .6, B)
    elif L == "Y":
        rect(0, 0, 1, 1, Y)
        n = 5
        for i in range(-n, n + 2):
            x0 = i * 2 / n
            if i % 2 == 0:
                poly([(x0, 1), (x0 + 1 / n, 1), (x0 + 1 / n + 1, 0), (x0 + 1, 0)], R)
    elif L == "Z":
        poly([(0, 0), (1, 0), (.5, .5)], Y); poly([(1, 0), (1, 1), (.5, .5)], B)
        poly([(0, 1), (1, 1), (.5, .5)], R); poly([(0, 0), (0, 1), (.5, .5)], K)
    elif L == "AP":  # answering pennant: red/white vertical stripes
        for i in range(5):
            rect(i / 5, 0, (i + 1) / 5, 1, R if i % 2 == 0 else Wt)

    # shapes: swallowtail for A and B, taper for the pennant
    if L in ("A", "B"):
        g.polygon([(w, 0), (w - w * .3, h / 2), (w, h)], fill=Wt)
    if L == "AP":
        g.polygon([(0, 0), (w, 0), (w, h * .25)], fill=Wt)
        g.polygon([(0, h), (w, h), (w, h * .75)], fill=Wt)
    return im


def outline(x, y, fw, fh, letter):
    """Black ink outline following the flag's real silhouette."""
    lw = int(1.6 * S)
    if letter in ("A", "B"):
        pts = [(x, y), (x + fw, y), (x + fw - fw * .3, y + fh / 2), (x + fw, y + fh), (x, y + fh)]
    elif letter == "AP":
        pts = [(x, y), (x + fw, y + fh * .25), (x + fw, y + fh * .75), (x, y + fh)]
    else:
        pts = [(x, y), (x + fw, y), (x + fw, y + fh), (x, y + fh)]
    d.line(pts + [pts[0]], fill=K, width=lw, joint="curve")


letters = [chr(c) for c in range(65, 91)] + ["AP", "UW"]
cols, rows = 4, 7
mx, top, bottom = 14 * S, 58 * S, 34 * S
cell_w = (W - 2 * mx) // cols
cell_h = (H - top - bottom) // rows
fw, fh = 68 * S, 46 * S
lab = ImageFont.truetype(FONT, 12 * S)

for idx, L in enumerate(letters):
    r, c = divmod(idx, cols)
    cx = mx + c * cell_w + cell_w // 2
    cy = top + r * cell_h + 6 * S
    x = cx - fw // 2
    if L == "UW":
        # the day's hoist, two small flags stacked on a halyard
        sw, sh = int(fw * .5), int(fh * .46)
        hx = cx - sw // 2 + 8 * S
        y0 = cy - 4 * S
        d.line([(hx - 7 * S, y0 - 4 * S), (hx - 7 * S, y0 + 2 * sh + 8 * S)], fill=K, width=int(2 * S))
        for k, ltr in enumerate(("U", "W")):
            yy = y0 + k * (sh + 4 * S)
            d.line([(hx - 7 * S, yy + 2 * S), (hx, yy + 2 * S)], fill=K, width=int(1.2 * S))
            img.paste(flag(ltr, sw, sh), (hx, yy))
            outline(hx, yy, sw, sh, ltr)
        label = "U W"
        ly = y0 + 2 * sh + 9 * S
    else:
        img.paste(flag(L, fw, fh), (x, cy))
        outline(x, cy, fw, fh, L)
        label = L if L != "AP" else "ANS"
        ly = cy + fh + 5 * S
    tw = d.textlength(label, font=lab)
    d.text((cx - tw / 2, ly), label, font=lab, fill=K)

# title and footer
tf = ImageFont.truetype(SERIF, 15 * S)
sf = ImageFont.truetype(SERIF, 10 * S)
title = "INTERNATIONAL CODE OF SIGNALS"
tw = d.textlength(title, font=tf)
d.text(((W - tw) / 2, 14 * S), title, font=tf, fill=K)
sub = "letter flags and answering pennant"
tw = d.textlength(sub, font=sf)
d.text(((W - tw) / 2, 36 * S), sub, font=sf, fill=K)
d.line([(mx, 52 * S), (W - mx, 52 * S)], fill=K, width=int(1.5 * S))
d.line([(mx, H - bottom + 2 * S), (W - mx, H - bottom + 2 * S)], fill=K, width=int(1.5 * S))
foot = "U W  —  I wish you a pleasant voyage"
tw = d.textlength(foot, font=sf)
d.text(((W - tw) / 2, H - bottom + 10 * S), foot, font=sf, fill=K)

# plate border
d.rectangle([4 * S, 4 * S, W - 4 * S, H - 4 * S], outline=K, width=int(2 * S))
d.rectangle([8 * S, 8 * S, W - 8 * S, H - 8 * S], outline=K, width=int(0.8 * S))

img.resize((400, 600), Image.LANCZOS).save(os.environ["OUT_RAW"])
