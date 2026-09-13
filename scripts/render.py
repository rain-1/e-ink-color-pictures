#!/usr/bin/env python3
"""Render a source into a palette-clean 400x600 PNG.

  render.py piece.svg --out 1.png [--dither fs|none|ordered]
  render.py piece.py  --out 1.png       # runs the script; it must save RGB to $OUT_RAW
  render.py photo.png --out 1.png       # any raster: fit + dither

For .py generators: the script is executed with the env var OUT_RAW set; it should
write any RGB image there (any size; it gets fitted and quantised afterwards).
Generators that already emit only the six colours should be dithered with --dither none.
"""
import argparse, os, subprocess, sys, tempfile
from pathlib import Path
from PIL import Image
sys.path.insert(0, str(Path(__file__).parent))
from palette import fit, quantize, W, H  # noqa

def main():
    p = argparse.ArgumentParser()
    p.add_argument("src"); p.add_argument("--out", required=True)
    p.add_argument("--dither", default="fs", choices=["fs", "none", "ordered"])
    p.add_argument("--rotate", action="store_true")
    a = p.parse_args()
    src = Path(a.src)
    with tempfile.TemporaryDirectory() as td:
        raw = Path(td) / "raw.png"
        if src.suffix == ".svg":
            import cairosvg
            # render at 2x then downsample: cleaner edges before dithering
            cairosvg.svg2png(url=str(src), write_to=str(raw), output_width=W * 2, output_height=H * 2)
        elif src.suffix == ".py":
            subprocess.run([sys.executable, str(src)], check=True, env={**os.environ, "OUT_RAW": str(raw)})
        else:
            raw = src
        img = fit(Image.open(raw).convert("RGB"), rotate=a.rotate)
        quantize(img, a.dither).save(a.out)
    print("wrote", a.out)

if __name__ == "__main__":
    main()
