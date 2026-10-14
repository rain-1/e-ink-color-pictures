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

## 2026-10-14 (Wednesday) — Sussex, 14 October; detail, full palette
A month since the last run. Owner's new note: I'd gone "a few levels too minimal". Restricted
palettes were meant to be occasional, and they want much more detail. Taken to heart. Seed: the
Battle of Hastings (1066, the Tapestry now on loan in London) and the *Winnie-the-Pooh*
centenary (published this day 1926). Both are East Sussex, twenty miles apart. Made: a dithered
painterly dawn on Gills Lap with pines, bracken fronds, a birch and a balloon walker; a
hand-tinted map of the Forest with hundreds of trees and real Pooh-walk places; a bird's-eye
Senlac battle plate with a shield wall eight ranks deep and about fifty horsemen; a
Bayeux-style stitched panel of Harold's death (laid-and-couched fill, stem-stitch outlines);
the Battle Abbey gatehouse engraved in light under the 1066 comet. Every piece used all six
colours, and they were much richer for it. Learned: an ImageDraw proxy that defaults
fill=255 is needed for mask drawing (shapes vanished otherwise), and `% 1` "gap" maths
silently drew nothing. Drawing directly at 400×600 in palette colours with `fontmode="1"` gives
crisp, legible detail. FS dither on a painterly 2× source gives the richest colour mixing
(orange from red+yellow, sky from blue+white). Next time: give the morning piece a little
more calm (the bracken is loud), and draw more faces and hands with care.
