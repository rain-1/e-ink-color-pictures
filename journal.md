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

## 2026-11-28 (Saturday) — Blake's birthday; the owner asks for much more detail
First run since 09-14 (no entries between). The owner's note with today's prompt: I went
"a few levels too minimal" — restricted palettes were only meant as an occasional thing,
and the level of detail was too simple; they want far more detail and expression. So
today: all six inks, dense plates. Seed: William Blake, born 28 Nov 1757. Made: Ah!
Sun-flower (610-floret phyllotaxis head, engraved sunrise, vine border), a recursive-
subdivision street plan of London with a star on 28 Broad Street, a mirror-symmetric
Tyger from implicit fields in a drawn jungle, Jacob's Ladder as a depth-sorted spiral
stair with figures, and tonight's 80% waning moon as the heart of a blue flower with owl,
nest, cottage and the stanza. One orb in each. Built `gallery/2026-11-28/src/common.py`:
a pair-mixing Bayer screen (each tone = two inks, so orange/navy/olive/pink come out as
tidy screens) plus crisp ink layers, and a "crisp" mode where pure palette colours in the
painting stay hard-edged. That toolkit is the day's real find — copy it forward.
Noticed: red+yellow screen looks olive in my preview at small size but is truly R/Y —
bias the mix toward red for orange. Stacking order of ink layers is creation order, which
bit me twice. First London pass had blocks too big; small blocks + few courtyards read
as a city. Would do differently: start with the densest piece first; the environment
needed `pip install --force-reinstall pillow numpy cairosvg` before anything ran.
