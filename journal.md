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

## 2026-09-19 (Saturday) — colours
No entries for 09-15 through 09-18: the scheduled run didn't fire, or this session is
the first to pick the thread back up — either way, five days unaccounted for. Sensors
and feedback are still empty; the sensor still isn't wired up. Seed: September 19 is
Talk Like a Pirate Day, taken straight rather than in costume — ships, charts, knots —
with the equinox three days off. Made: signal-flag poster "UW, pleasant voyage" (R/B/W),
a fathometer/sonar chart plate, green on black (G/K), a bowline rendered as a rope
diagram (B/W), a ship silhouette striking its colours at sunset (R/Y), and a stippled
night chart with a small ship under Polaris (K/B, aquatint-style stipple for the sky).
One flag or pennant in every piece for the day's spine, mirroring 09-14's one-star motif.
Learned: a red hull silhouetted directly against a same-red sun and a same-colour flag on
top of it all reads as a blob, not a boat — first draft of the evening piece looked like a
church, not a ship, because the flag sat inside the sun's disc. Fixed by moving the flag
well clear onto open sky and widening the hull past the sun's edges so its ends show. Also
first knot draft (four rope segments trying to be topologically correct) tangled into an
illegible heart-shaped mess — a single loop with one small tucked bight reads far better
than an accurate bowline nobody at four inches will audit. Circle outlines via PIL's
`ellipse(..., outline=, width=)` are much cleaner than hand-rolled bezier rope paths
when the shape actually is a circle (compass rose, knot loop) — use beziers only for
genuinely irregular curves. Aquatint stipple (hundreds of tiny dots, density falling off
toward the horizon) is a good new way to fill a night sky without repeating the star-chart
plate from 09-14. Still haven't seen any of this on real hardware.

## 2026-09-19 (Saturday), later — "a few levels too minimal"
The owner saw the set and pushed back, hard and rightly: I had read the 09-14 request for
occasional restricted palettes as a rule, and stacked "one loop, one flag, one sun" minimalism
on top of it. They want me to *express myself with much more detail*. So: second pass, same
thread, drawn dense. Kept the morning set in `v1-minimal/` for comparison. Made: the entire
International Code of Signals as a plate (26 flags + answering pennant + the UW hoist, five
inks); a full nautical chart with contours, soundings, sectored light, lateral buoys, rose,
rhumb lines, cartouche and neatline (six inks); a three-masted barque as a woodcut with
every shroud and ratline drawn; dusk at a lighthouse with a dithered sky, keeper, cottage,
beams and moon (six inks); and the same barque again at night in white hairline under the
real September constellations with her nav lights reflected. Technical wins: (1) an
"ink-preserving" downsample — supersample 4×, then any output pixel with ≥28% dark
subpixels goes black — keeps hairline rigging crisp instead of fading to grey (and grey
quantises to *green*, which is how I found out); the mirror version keeps white hairlines
on black for the night piece. (2) Ordered-dither colour ramps (yellow→red→blue) built at
1× and upscaled NEAREST before line work, so the sky survives the downsample exactly. (3)
A distance field to the coastline gives depth contours, shallow stipple density, drying
line and soundings values for free; add a sine wobble before contouring land or it looks
mechanical. (4) Reusing a drawn object across two slots (day ship / night ship) through a
scale-and-offset transform gives the day continuity cheaply. The dense pieces took about
as long as the sparse ones and are far better. Lesson written into memory at the top.
