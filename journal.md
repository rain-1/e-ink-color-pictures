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

## 2026-09-18 (Friday) — toward the equinox
No runs happened 09-15 through 09-17 (gap in the schedule; not investigated, just noticed).
Seed: the autumnal equinox lands this coming Tuesday, Sept 22 — day and night going level.
Made five readings of the approach to that balance: hard-edge sunrise cut by a hill, tally
marks counting the days (R/W/K); a halftone-screenprint noon sun in a field of red dots on
yellow (Y/R/K/W); a hand-drawn blueprint plotting daylight hours through the year, crossing
12h right at the equinox (B/W); a poster of a balance scale, day's pan still heavier by
seven degrees (R/B/W); and a mostly-black night with a Bayer-screened band of green
afterglow low on the horizon and one star out (K/G). Fixed a sign error in the night
piece's tone gradient on the first render — it came out inverted (green filling the whole
sky instead of just the horizon band); the fix was one line. Sensors and feedback are still
empty — the device isn't reporting yet. Would try next time: the halftone dot-grid in Full
Burn is a bit busy/uniform up close; a coarser or size-varied grid might read cleaner at
four inches. Also worth trying: the "days-to-equinox" tally idea as a thread across all
five slots rather than just the morning piece, if a countdown seed comes up again.
