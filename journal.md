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

## 2026-11-20 (Friday) — roughness; the owner asks for much more detail
First entry since 09-14 (no journal for the weeks between). The owner's note today: I had
gone "a few levels too minimal" — restricted palette was meant as an occasional thing, and
the detail level was far too simple; they want me to express myself with much more detail.
Seed: Mandelbrot's birthday (1924) and his five-clause sentence, one clause per slot. Made:
engraved fBm cloudscape over patchwork fields (morning), voxel-rendered mountains inked as
a survey plate with a red cone that doesn't fit (midday), a sea chart whose coast is
measured with five divider lengths, real numbers (afternoon), a Worley-bark trunk at sunset
with owl, woodpecker, ivy, fungi (evening), branching lightning over a harbour town (night,
77% black). All full six-colour, drawn natively at 400×600 in palette indices with screens
done in the generator — no antialiasing, `--dither none`. A shared `common.py` (Plate, fbm,
screen, hatch, grow, mandel, caption) made five dense pieces affordable in one run.
Noticed: layering is what makes density — field, then tone screens, then iso-lines, then
drawn objects (trees, houses, birds), then one piece of wit (the cone, the dividers, the
owl). The mountains took four camera/terrain tries; decide classes by percentiles of what
is visible, not absolute heights. Small hand-drawn animals (woodpecker) are still blobs
under ~50px. Chart text at 8–9px is a gamble on the real panel. Environment: use
`/usr/bin/python3` (plain `python` lacks numpy/PIL); no scipy; `Image.fromarray` results
must be `.copy()`'d before drawing/floodfill. Sensors and feedback files still empty.
