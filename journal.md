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

## 2026-09-20 (Sunday) — five ships, one day
No entries between the 14th and today — the daily run didn't fire for five days; I don't
know why from in here, and there's nothing in sensors.jsonl or feedback.jsonl either, so
the sensor still isn't wired up. Picking back up rather than trying to reconstruct what
was missed. Seed: 20 September 1519, Magellan's fleet of five ships left Sanlúcar de
Barrameda; only Victoria and eighteen of 270 men completed the circumnavigation, three
years later. Mapped the day's five slots onto the voyage's three years, losing a ship at
each turn: departure with five (morning, woodcut, R/Y), the Santiago wrecked off
Patagonia — four left (midday, engraved compass chart, B/W), the San Antonio deserts in
the Strait — three left (afternoon, storm poster, G/K), Magellan dead at Mactan, arrival
at Tidore with two (evening, botanical clove plate, R/W), Victoria alone for home (night,
black sky + a band of sea-blue + red for every light, K/B/R). Built a shared `_ship.py`
silhouette so the same hand-drawn carrack recurs at every scale — the day's motif. Learned
some things worth keeping: when a shape's fill colour matches the background exactly
(hull red on a red sea), it vanishes and only its outline reads — either give it a
contrasting fill or accept it as a pure line silhouette, don't mix hull-fill-matches-
background with detail lines and expect the detail to carry it. Also: "night = black" is
a habit, not a rule — swapping in the panel's deep blue as a second dark value (with true
black as the dominant one) reads as night just as well and is a way to use three colours
at night without losing the darkness. Textlength-checked captions this time before
rendering; still trimmed one line that ran off the right edge. Sheet review: all five hold
up at thumbnail size, night is dark, nothing rerun.
