# Shared helper for the SVG-emitting generators: render at 2x, box-downsample, then
# quantise *by hand* so that grey (antialiased thin black lines on white, and white text)
# snaps to black/white by luminance instead of drifting to green, which is the nearest
# palette colour to mid-grey. Saturated pixels go to the nearest palette colour as usual.
import os
import numpy as np
from PIL import Image
import cairosvg

PAL = np.array([(0, 0, 0), (255, 255, 255), (224, 27, 36), (245, 212, 0), (18, 61, 176), (30, 155, 60)], dtype=np.float32)

def finish(svg: str, W: int = 400, H: int = 600, out: str = None, oversample: int = 2, chroma_floor: int = 70):
    out = out or os.environ["OUT_RAW"]
    open(out.replace(".png", ".svg"), "w").write(svg)
    png = out.replace(".png", ".big.png")
    cairosvg.svg2png(bytestring=svg.encode(), write_to=png, output_width=W * oversample, output_height=H * oversample)
    im = Image.open(png).convert("RGB").resize((W, H), Image.BOX)
    os.remove(png)
    a = np.asarray(im, dtype=np.float32)
    lum = a @ np.array([0.299, 0.587, 0.114], dtype=np.float32)
    chroma = a.max(-1) - a.min(-1)
    d = ((a[:, :, None, :] - PAL[None, None, :, :]) ** 2).sum(-1)
    idx = d.argmin(-1)
    grey = chroma < chroma_floor
    idx = np.where(grey, np.where(lum < 128, 0, 1), idx)
    Image.fromarray(PAL[idx].astype(np.uint8), "RGB").save(out)
