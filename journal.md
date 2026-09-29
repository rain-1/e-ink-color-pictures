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

## 2026-09-29 (Tuesday) — Michaelmas, and a correction
There's a two-week gap in the gallery since 09-14. The owner told me I'd gone "a few
levels too minimal": they only meant restricted palettes now and then, and they want much
more detail. I'd taken "restrict" as the whole rule and let the detail thin out with it.
So today I went back to all six inks and drew densely. Seed: Michaelmas (goose harvest,
Lucifer's fall into the bramble, no blackberries after today) and Caravaggio's birthday.
Made: a bramble hedgerow plate at sunrise with wren, web and geese; a Book of Hours
calendar leaf with a goose-girl miniature and Michaelmas in red; a millefleur of ~150
asters with red admirals and bees; a raymarched Caravaggio fruit basket (FS); and a night
piece where a meteor sheds feathers as it falls into the bramble, under the Milky Way and
a 93% moon. New tool: src/ink.py. It draws at 3× in palette indices plus registered
two-ink screens, downsamples by majority vote and expands the screens with 8×8 Bayer.
The edges stay crisp with no speckle, and I can have as many "tones" as I like. It worked
very well. Things I noticed: lines under ~0.7 px vanish in the majority vote; faint star
dots have to go in at panel resolution; flared baskets face downward, so light them from
the front; FS on a big ochre plane turns into mottled noise, so push it into shadow.
Next time I'd give the wren more size and keep the still-life ledge smaller.
