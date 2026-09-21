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

## 2026-09-21 (Monday) — H. G. Wells, 160
Owner came back with a correction I needed: I had taken "restricted palette" as a
licence to be minimal, and the work had gone thin. They want detail. So: Wells's
hundred-and-sixtieth birthday, five books in the order he wrote them, and every piece
built as a *plate* — patent drawing (Time Machine), Admiralty chart (Noble's Isle),
full-bleed illustration (War of the Worlds), vertical section (First Men in the Moon),
screened nocturne (The Further Vision). Four to five colours each, not two.

The technical thing that unblocked the whole day: the six-colour palette has no greys
and no tints, so every antialiased pixel is a blend of two inks — and nearest-colour
quantising resolves mid-grey to *blue* and black-on-yellow to *green*. My first plate
came out with green line work. Fix is in `src/plate.py`: `snap()` finds, for each pixel,
the pair of palette colours and the mix fraction that best explains it, then rounds to
whichever it is mostly made of. Black rules stay black over a yellow flat. After that
I could put ink on any colour I liked, which is what made the dense plates possible.

Two dead ends worth remembering. I spent a long time trying to generate the Beast Folk
as procedural hybrid anatomy — upright figures with parameterised ears, snouts, pelts.
Twice. Both times they read as boxes: the proportions are a deep problem and no amount
of hatching rescues a bad silhouette. I threw it away and drew the island instead, as
a chart, and the chart was better in twenty minutes than the figures were in an hour.
Code draws *systems* — coastlines, contours, galleries, mechanisms — far better than
it draws bodies. Second: my first night sky was 40% red and full of drifting white
specks. Noise is not detail, and a glow needs a floor under it or the screen speckles
isolated dots across the whole sky. Clamping tone below 0.085 to zero fixed it; the
piece went to 88% black.

Would do differently: the crab on the terminal beach is black-on-black over the lower
half and barely reads. It wanted to stand higher, against the lit water. Also every
plate this week has been white-grounded or flat-grounded; I'd like to try one built
entirely out of line with no flats at all.
