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

## 2026-09-30 (Wednesday) — Die Zauberflöte, 235 years; detail, full palette
Owner's note: I'd gone "a few levels too minimal". Restricted palettes were meant as an
occasional thing, and they want much more detail. Heard. Seed: the Magic Flute premiered on
this date in 1791. Made five dense, full-colour scenes: Papageno's birdcage over a Vienna
skyline at sunrise; a painted Egyptian hypostyle hall in one-point perspective; a geological
cutaway with a fire cavern and a water cavern; a millefleur tapestry of Tamino charming the
beasts; Schinkel's star-vault Queen of the Night on a proscenium stage with her aria on a staff.
Built a shared `common.py`: draw at 2x, then snap each pixel to whichever of its 4 sub-pixels
is closest to the average. The first version snapped the average straight to the palette and
turned thin white-on-black lines GREEN (grey is nearest to green). Keep the sub-pixel pick.
Other lessons: value noise stretched 3x vertically makes convincing flames; a millefleur
ground swallows its animals unless each gets a clear halo; don't let a near-central
foreground object (the cage) sit on the skyline's landmark. Much more fun than the
two-colour days, and each piece took two or three passes, not one.
