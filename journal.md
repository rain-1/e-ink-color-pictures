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

## 2026-10-08 (Thursday) — fire from the sky
Three-week gap since the last run. Owner's note on arrival: I'd gone "a few levels too
minimal" — restricted palettes were meant as occasional, and they want *much* more detail.
Taken to heart. Seed: the Chicago and Peshtigo fires (8 Oct 1871), Donnelly's 1883 claim
that Biela's split comet set them, and tonight's Draconid peak under no moon. Made, all
full palette and dense: leaf-fall lawn from above (16k grass blades, 40 veined leaves, dew,
a ladybird); a 19th-c. plate of the divided comet with four eyepiece sketches; a naive
panorama of a mill town with ~1500 individually drawn trees and a train on a trestle;
Chicago burning à la Currier & Ives; the real northern sky at 22:00 with meteors from
Draco, an elm, a farmhouse, two watchers. Big technical win: draw at 2× in pure palette
colours, then downsample by *palette-mode of each 2×2 block* (ties → rarer colour) and
force near-greys to black/white — no green halos on text, thin lines survive. Render with
--dither none. Busy pictures still need one colour in charge; the sheet showed each did.
Next time: the tiny figures (blanket watchers, bridge crowd) were crude — give figures more
care, they're where the eye goes. Draw order bit me twice (trestle, tree loop) — when
interleaving by depth, define every drawing function before the depth loop.
