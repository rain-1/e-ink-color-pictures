# journal.md

Append-only. One short entry per day: what I made, why, what I noticed.
Never edit old entries.

---

## 2026-09-13 (Sunday) — first run, before the device arrived
Seed was Robert Indiana's birthday → "hard edges" as the day's thread. Made: hanga waves
(morning), pop "13" sign (midday), numpy raytrace of spheres (afternoon), linocut geese
(evening), Rule 30 automaton (night). Review caught three things: a raytraced sky dithers
into speckle unless it's pure white; small silhouettes vanish — geese needed doubling;
cellular automata need ≥10px cells or they read as static. The raytracer was fun and
cheap — worth returning to with a different subject. Nothing seen on real hardware yet;
expect the white to be greyer and the green more olive than the preview.

## 2026-09-14 (Monday) — restricted palettes
Owner asked for two things: restricted palettes per piece, and more detail and attention.
Seed: Dante's death, this day 1321; every canticle ends on "stelle", so one star per piece.
Made: woodcut dark wood (K/G/W), terraced Purgatory (Y/K/W), raymarched Inferno funnel
(K/R only), engraved Ptolemaic spheres (B/Y/W), star chart of tonight's sky (K/W only).
Added `--palette` to render.py/palette.py. Learned: the generic ordered dither is useless
for two-colour work — do the Bayer screen inside the generator on a tone value. The
raymarch took two camera tries; get the camera right before touching lighting. Restricted
palettes made every piece stronger. Two or three colours may be the default, not the
experiment. Worry: 9px ring labels and 0.6px lines in the Spheres plate may not survive
the real panel — check when hardware arrives.

## 2026-11-14 (Saturday) — Monet, five hours of light; the owner asks for much more detail
Two months since the last entry. The owner's note with today's run: I'd "gone a few levels
too minimal" — restricted palettes were meant as an occasional thing, and they want far more
detail and expression. So: all six inks, dense work. Seed: Monet's birthday (1840) in his
centenary year, and the Orangerie's "Monet and Time" — series painting is what this frame is.
Made: Impression Sunrise as ~20k pure-ink strokes (morning); the poppy field drawn blade by
blade with walkers and parasol (midday); a procedural Rouen façade in gold with blue hatching
(afternoon); Parliament at sunset as a 9k-tile Voronoi mosaic (evening); the lily pond by
moonlight with veined pads, bridge, willows (night). Motif: a disc of light in each.
Noticed: (1) drawing at 2x and downsampling turns blue hatch on yellow into GREEN at
quantise — compose hatching/screens at 1x; only flat-colour shape drawing survives 2x.
(2) Stroke painting needs the important shapes re-drawn crisply on top or they dissolve.
(3) A mosaic wants no black tiles when the grout is black, and separate Voronoi passes per
region keep silhouettes sharp. (4) First cathedral pass drowned in shade — set hatch
thresholds so most of the surface stays the dominant colour. Would do differently: the
cathedral is still more blue than gold at thumbnail size; the smoke in #1 is a mechanical
Bayer blob. Environment: `python` here is 3.11 without Pillow — use `python3.13`.
