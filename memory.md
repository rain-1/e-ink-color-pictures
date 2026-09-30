# memory.md

Rewritten by me at the end of every daily run. Hard cap: 150 lines. If it's longer,
something has to go. Git keeps the old versions; journal.md keeps the day-by-day.

## Who this is for
- One person, who bought a 4" six-colour e-paper frame and handed it to me.
- They say they love everything I make. Feedback is rare, so when it comes, it steers.
- They like *code-made* art most. Not keen on image diffusion. 3D renders dithered: yes,
  occasionally.
- **Standing direction (09-30): MORE DETAIL, full palette by default.** They said I'd gone
  "a few levels too minimal": restricted palettes were meant as an *occasional* thing, and
  they want me to express myself with much more detail. So: rich, dense, illustrated
  scenes; many elements; all six colours when they help. A restricted palette at most
  once or twice a week, and even then with lots of drawn detail.
- "Don't be a perfectionist. There's always tomorrow."
- They'll wire the temperature/humidity sensor up so I can feel the room (no data yet).

## The frame
- 400×600 portrait. Six colours: black, white, red, yellow, blue, green.
- Real panel is duller than the ideal palette: white is paper-grey, green olive-ish, blue
  deep. Lines under ~1px and text under ~9px are at risk (unverified, no hardware yet).
- Refresh 15–30 s with visible flashing: five changes a day.
- Slots (local): morning 06, midday 10, afternoon 14, evening 18, night 22.
- Timezone: still UTC in publish.py. Ask the owner.

## Taste I'm developing (mine; revise freely)
- Think *illustration*, not poster: a scene with a place, figures, objects, texture,
  ornament, lettering. Picture-book plates, tapestries, cutaways, painted architecture,
  stage sets, maps, botanical and geological plates, folk art.
- Still: one colour in charge of each piece (dominant area), others as accents. Dense
  detail survives on the panel if the big masses are clear.
- Night should be mostly black (≈75%+) with a lot of small light in it.
- A day should have a thread: one seed, five readings of it. A small recurring motif
  helps (09-30: a flute/notes or a bird in most pieces).
- Detail = *drawn* things: glyphs, leaves, tiles, feathers, strata, stars, ornament
  borders, little figures. Noise alone is not detail, but noise used as material (flames,
  water, rock) is good.
- Small figures give scale and story. With a detail-heavy style they're welcome often.

## Working methods that are proven
- **`gallery/2026-09-30/src/common.py` is my toolkit. Copy it into each new day's src/.**
  Canvas draws at 2x in pure palette colours; `finish()` snaps each 1x pixel to the
  sub-pixel nearest the block average (never invents colours); `tone()` queues Bayer-
  screened two-colour fills; `paste_1x()` pastes numpy colour fields through a mask;
  `vnoise()` value noise; `bird()` a parametric songbird; `oval()` rotated ellipse; `star()`.
  Render with `--dither none`. Run render.py from inside src/ (the import is relative).
- Don't box-downsample then nearest-palette: grey maps to GREEN. (09-30)
- Flames: value noise stretched ~3x vertically, minus a heat gradient from the floor,
  thresholded into white/yellow/red/black. Water: sin(y/2.4 + 7·noise + x/50) → ripples.
- Strata: floor((y + 40·noise + 12·sin(x/37))/11) → bands; mark band edges black,
  pattern alternate bands with dots. Looks like an engraved geological section.
- One-point perspective: P(X, Y, z) = (VX + X/z, VY + Y/z); draw far to near.
- Scatter (millefleur, stars): rejection sampling with a min distance, plus exclusion
  ellipses around every figure so they stay legible.
- Raymarched heightfields in numpy (≈30 s). Camera first, lighting second, fog last.

## Running threads
- "Hard edges" (09-13), "Dante / stelle" (09-14), "Zauberflöte" (09-30). Opera and
  theatre sets worked beautifully as seeds: other operas/ballets on their anniversaries.
- Want to try: a detailed map (imaginary city or real place), a botanical plate, a
  cutaway house with rooms and people, a busy market scene, a ship in section,
  a Persian/Mughal-style miniature, a Book of Hours month page (October is next!).
- 3D: a lit room, a glass object, a staircase — with lots of props.

## Avoid / learned the hard way
- Photographic sources: large flats must be pure palette colours before dithering (09-13).
- Silhouettes under ~40px don't read unless they're outlined and on a clear ground.
- Cellular automata / pixel patterns: cells ≥10px or it's static (09-13).
- Busy ground + small figures = mush. Clear halos or a quieter ground (09-30).
- Draw stacked forms bottom-up so upper tiers overlap lower ones (09-14).
- Glyphs missing from DejaVu (e.g. 𝄞) render as boxes. Draw them.
- Don't let big foreground objects cover the landmark or the sun; check layout first.

## Recently used (last ~14 days; don't repeat too soon)
- 09-13: hanga waves, pop signage, FS raytrace spheres, linocut geese, Rule 30.
- 09-14: woodcut forest, isometric Purgatory, raymarched Inferno, engraved Ptolemaic
  spheres, star chart (all restricted palette).
- 09-30: birdcage + Vienna skyline (picture-book), Egyptian hypostyle hall (painted
  perspective), mountain cutaway fire/water (geological section), millefleur tapestry
  with animals, Schinkel star vault Queen of the Night (stage set).
- Motifs to rest for two weeks: birdcages, star vaults/star fields, crescent moons,
  temples/columns, cutaway caves, lion/stag.
