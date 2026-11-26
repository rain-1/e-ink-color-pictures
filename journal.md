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

## 2026-11-26 (Thursday) — wonderful things; the owner asks for much more detail
First run since 09-14. Owner's note: I'd gone "a few levels too minimal" — restricted
palettes were meant as an occasional thing, and they want much more detail and expression.
So: all six inks, dense drawn detail. Seed: Carter's first look into Tutankhamun's tomb,
this day 1922. Made: the Valley at sunrise with the dig (poster + hatching), a winged-scarab
cloisonné pectoral, the candlelit antechamber through the breach (Bayer light falloff),
a Nebamun-style garden pool, and Nut over tonight's real sky (Orion, Sirius, gibbous moon).
A red sun-disc in each. New method that worked very well: draw at 3× in pure palette colours
with no anti-aliasing, reduce by majority vote per 3×3 block (src/common.py) — crisp edges,
no off-palette fringes, `--dither none`. Scattering ornaments wherever the ground is still
plain (is_plain) fills a composition quickly. Noticed: gold objects on black need a nearly
solid light level or they dissolve into stipple; rotated side trees must be scaled to fit;
the garden ended up white-dominant rather than green. Egyptian art suits this palette almost
unfairly well. Would do differently: the candle hand is clumsy; blue stars on black will
probably vanish on the real panel. requirements.txt needed a forced pillow reinstall here.
