#!/usr/bin/env python3
"""Spectra 6 palette tools for the PaperColor (400x600).

  palette.py quantize IN.png OUT.png [--dither fs|none|ordered] [--rotate]
  palette.py check   IN.png                # exit 1 if not 400x600 / not on palette
  palette.py sheet   DIR --out sheet.png   # contact sheet of 1.png..5.png
  palette.py swatch  OUT.png               # the six colours, for reference

The six colours are the *ideal* values. Real E6 panels are duller: the white is
paper-grey, the green is a bit olive, the blue is deep. Designs that rely on
large flat areas and strong contrast survive this; fine gradients do not.
"""
import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image

W, H = 400, 600

PALETTE = {
    "black":  (0x00, 0x00, 0x00),
    "white":  (0xFF, 0xFF, 0xFF),
    "red":    (0xE0, 0x1B, 0x24),
    "yellow": (0xF5, 0xD4, 0x00),
    "blue":   (0x12, 0x3D, 0xB0),
    "green":  (0x1E, 0x9B, 0x3C),
}
ORDER = ["black", "white", "red", "yellow", "blue", "green"]
PAL = np.array([PALETTE[k] for k in ORDER], dtype=np.float32)

# Roughly what the panel actually shows — used for the "preview" in the sheet.
DISPLAYED = {
    "black":  (0x1A, 0x1A, 0x1A),
    "white":  (0xE8, 0xE6, 0xDF),
    "red":    (0xB8, 0x2A, 0x2A),
    "yellow": (0xD9, 0xC1, 0x3A),
    "blue":   (0x24, 0x3F, 0x8A),
    "green":  (0x3E, 0x7F, 0x4A),
}


def _nearest(px):
    d = ((PAL[None, :, :] - px[:, None, :]) ** 2).sum(-1)
    return d.argmin(1)


def quantize(img: Image.Image, dither: str = "fs") -> Image.Image:
    """Return an RGB image using only the six palette colours."""
    a = np.asarray(img.convert("RGB"), dtype=np.float32)
    h, w, _ = a.shape
    if dither == "none":
        idx = _nearest(a.reshape(-1, 3)).reshape(h, w)
    elif dither == "ordered":
        bayer = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16 - 0.5
        noise = np.tile(bayer, (h // 4 + 1, w // 4 + 1))[:h, :w] * 48
        idx = _nearest((a + noise[:, :, None]).reshape(-1, 3)).reshape(h, w)
    else:  # Floyd–Steinberg
        idx = np.zeros((h, w), dtype=np.int64)
        buf = a.copy()
        for y in range(h):
            for x in range(w):
                old = buf[y, x]
                i = int(((PAL - old) ** 2).sum(1).argmin())
                idx[y, x] = i
                err = old - PAL[i]
                if x + 1 < w:
                    buf[y, x + 1] += err * 7 / 16
                if y + 1 < h:
                    if x > 0:
                        buf[y + 1, x - 1] += err * 3 / 16
                    buf[y + 1, x] += err * 5 / 16
                    if x + 1 < w:
                        buf[y + 1, x + 1] += err * 1 / 16
    out = PAL[idx].astype(np.uint8)
    return Image.fromarray(out, "RGB")


def fit(img: Image.Image, rotate: bool = False) -> Image.Image:
    """Rotate landscape sources if asked, then centre-crop/resize to 400x600."""
    if rotate:
        img = img.rotate(90, expand=True)
    if (img.width, img.height) == (W, H):
        return img
    scale = max(W / img.width, H / img.height)
    img = img.resize((round(img.width * scale), round(img.height * scale)), Image.LANCZOS)
    left, top = (img.width - W) // 2, (img.height - H) // 2
    return img.crop((left, top, left + W, top + H))


def check(path: Path) -> list[str]:
    problems = []
    img = Image.open(path).convert("RGB")
    if (img.width, img.height) != (W, H):
        problems.append(f"size is {img.width}x{img.height}, want {W}x{H}")
    a = np.asarray(img).reshape(-1, 3)
    colours = {tuple(c) for c in np.unique(a, axis=0)}
    bad = colours - {tuple(v) for v in PALETTE.values()}
    if bad:
        problems.append(f"{len(bad)} off-palette colour(s), e.g. {sorted(bad)[:3]}")
    # coverage report (informational)
    counts = {}
    idx = _nearest(a.astype(np.float32))
    for i, k in enumerate(ORDER):
        counts[k] = round(100 * (idx == i).mean(), 1)
    print("coverage %:", counts)
    return problems


def sheet(day_dir: Path, out: Path, preview: bool = True):
    files = sorted(day_dir.glob("[1-5].png"))
    if not files:
        sys.exit(f"no 1.png..5.png in {day_dir}")
    pad, tw, th = 12, 200, 300
    canvas = Image.new("RGB", (pad + len(files) * (tw + pad), th + 2 * pad), (40, 40, 40))
    lut = {PALETTE[k]: DISPLAYED[k] for k in ORDER}
    for n, f in enumerate(files):
        im = Image.open(f).convert("RGB")
        if preview:
            a = np.asarray(im).copy()
            for src, dst in lut.items():
                a[(a == src).all(-1)] = dst
            im = Image.fromarray(a)
        im = im.resize((tw, th), Image.NEAREST)
        canvas.paste(im, (pad + n * (tw + pad), pad))
    canvas.save(out)
    print("wrote", out)


def swatch(out: Path):
    im = Image.new("RGB", (6 * 60, 60))
    for i, k in enumerate(ORDER):
        im.paste(PALETTE[k], (i * 60, 0, (i + 1) * 60, 60))
    im.save(out)


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    q = sub.add_parser("quantize"); q.add_argument("inp"); q.add_argument("out")
    q.add_argument("--dither", default="fs", choices=["fs", "none", "ordered"])
    q.add_argument("--rotate", action="store_true")
    c = sub.add_parser("check"); c.add_argument("inp")
    s = sub.add_parser("sheet"); s.add_argument("dir"); s.add_argument("--out", required=True)
    s.add_argument("--exact", action="store_true", help="show ideal colours, not the panel preview")
    w = sub.add_parser("swatch"); w.add_argument("out")
    a = p.parse_args()

    if a.cmd == "quantize":
        img = fit(Image.open(a.inp), rotate=a.rotate)
        quantize(img, a.dither).save(a.out)
        print("wrote", a.out)
    elif a.cmd == "check":
        probs = check(Path(a.inp))
        for pr in probs:
            print("PROBLEM:", pr)
        sys.exit(1 if probs else 0)
    elif a.cmd == "sheet":
        sheet(Path(a.dir), Path(a.out), preview=not a.exact)
    elif a.cmd == "swatch":
        swatch(Path(a.out))


if __name__ == "__main__":
    main()
