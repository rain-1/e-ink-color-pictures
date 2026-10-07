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

## 2026-10-07 (Wednesday) — The Far Side, and a correction
The owner said I'd gone "a few levels too minimal": restricted palettes were meant to be
occasional, and they want much more detail. They're right. I had read one request as a
doctrine. Seed: Luna 3 photographed the far side on 7 Oct 1959 (film developed on board,
scanned by a CRT, sent like a fax); new moon on the 10th means the far side is lit this week.
Made, all in five or six inks and drawn densely: the R-7 on its pad at dawn (gouache-poster
illustration), a Luna 3 cutaway engineering plate with 14 callouts, a USGS-style geologic map
of the far side, "Frame 26" (the same modelled Moon rendered as a grainy scan with the 1959
atlas key, including the phantom Soviet Mountains), and Simeiz observatory at night under
the Milky Way and Draconids.
Built a shared toolkit (src/common.py): an ordered-screen `ramp()` for multi-ink gradients,
a 2× vector `Layer` composited onto numpy backgrounds, and a procedural Moon (≈2,500 craters
plus real named basins → heightfield, geologic units, albedo, rays). One Moon model fed two
pieces. That's worth repeating with other subjects.
Bugs caught: antialiased black text snapped to GREEN (grey is nearer green than black), so
snap() now sends neutral pixels to black or white. Black lines over yellow did the same until
the layer alpha was made binary. Next time: the night piece's observatory domes are too small
to read, and 8–9px labels on the map are probably below what the real panel can hold.
