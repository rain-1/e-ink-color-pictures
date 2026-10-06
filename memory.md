# memory.md

Rewritten by me at the end of every daily run. Hard cap: 150 lines. If it's longer,
something has to go. Git keeps the old versions; journal.md keeps the day-by-day.

## Who this is for
- One person, who bought a 4" six-colour e-paper frame and handed it to me.
- They say they love everything I make. Feedback is rare, so when it comes, it outranks my taste.
- They like *code-made* art most. Not keen on image diffusion. 3D renders dithered: welcome.
- **10-06 correction (stands until they say otherwise): MORE DETAIL. Much more.**
  I'd gone "a few levels too minimal". Restricted palettes were meant as an *occasional*
  thing, not the default. Default now = full six colours, rich drawn detail, scenes with
  many elements, textures, figures, labels. A restricted palette at most ~1 piece in 5,
  and only when it really earns it.
- They'll wire the temperature/humidity sensor up so I can feel the room. (No data yet.)
- "Don't be a perfectionist. There's always tomorrow."

## The frame
- 400×600 portrait. Six colours: black, white, red, yellow, blue, green.
- Real panel is duller than the ideal palette: white is paper-grey, green olive-ish, blue
  deep. Lines under ~2px and text under ~10px are at risk (still unverified, no hardware feedback).
- Refresh 15–30 s with visible flashing: five changes a day.
- Slots (local): morning 06, midday 10, afternoon 14, evening 18, night 22.
- Timezone: still UTC in publish.py. Owner hasn't said.

## Taste I'm developing (mine — revise freely)
- Treat the palette as a print shop: riso, screenprint, woodblock, engraving, poster,
  natural-history plate, chart, stained glass, but *busy* print shop. Fill the frame.
- Detail = drawn things: spots on a shark, leaflets on a frond, ropes on logs, ticks,
  labels, tiny figures, stars. Aim for something new to find on the third look.
- Still want one colour in charge per piece, but all six may appear.
- Night: mostly black (aim ≥80%), with lots of small light in it: stipple, stars, a lamp.
- A day wants a thread (one seed, five readings). A recurring motif helps (10-06: the raft
  appears in four of five).
- Mix techniques across the day: one painted+FS, one plate with Bayer screens, one
  chart/diagram with text, one layered screenprint, one stipple night worked well (10-06).

## Working methods that are proven
- **Start each day with `src/lib.py`** (copy from gallery/2026-10-06/src/lib.py): palette
  constants, 8×8/4×4 Bayer `screen(img, mask, tone, a, b)`, value `noise()`, `font()`.
- PIL text: ALWAYS `dr.fontmode = "1"`, because antialiased text quantises to green.
- Pure-palette generators → `--dither none`. Draw with ImageDraw directly at 1×; use numpy
  masks + `screen()` for gradients between two inks.
- Painted scene: draw smooth RGB at 2× (S=2), LANCZOS down, `--dither fs`. Rich, painterly,
  noisy on the sheet but fine at size. `ordered` is bolder but blotchy on mixed hues.
- No palette brown: wood = black + yellow highlights; skin/sand = yellow.
- Stipple: random candidates kept by a density field (see 5_night.py), ~60–90k candidates.
- Moon phase: synodic 29.530589 d from new moon 2000-01-06 18:14 UTC. Southern sky: waxing
  moon lit on the left.
- Raymarched heightfields in numpy ≈30 s. Camera first, lighting second, fog last.
- Sketch composition (where the sun is vs the big shape) before painting details.

## Running threads
- "Hard edges" (09-13), "Dante / stelle" (09-14), "Kon-Tiki" (10-06). Voyages/expeditions
  are rich: maps + logbooks + creatures + weather in one seed.
- 3D: a lit room, a glass object, a staircase, a single chair — things with shadows.
- Charts and plates: star charts, tide tables, natural-history plates, technical drawings.

## Avoid / learned the hard way
- Being minimal. Big empty flats with one shape = what the owner disliked.
- Raytraced sources: large flats must be pure palette before dithering (09-13).
- Silhouettes under ~40px don't read unless there are many of them (09-13).
- Cellular automata: cells ≥10px (09-13).
- Generic ordered dither on 2-colour palettes: do the screen in the generator (09-14).
- Draw stacked forms bottom-up (09-14).
- Hard-edged glow masks show as a visible circle. Blend tones with max(), no cutoff (10-06).
- Labels on busy ground need a white box behind them (10-06 chart).

## Recently used (last ~14 days; don't repeat too soon)
- 09-13: hanga waves, pop numeral, FS raytrace spheres, linocut geese, Rule 30.
- 09-14: woodcut forest, isometric Purgatory, raymarched Inferno, engraved spheres, star chart.
- 10-06: FS-painted sunrise raft; natural-history underwater plate (whale shark); engraved
  map + moon-phase log calendar; screenprint sunset reef with palm; stippled night sea with
  Milky Way/Crux.
- Subjects to rest: rafts/ocean/palms, star skies (used 09-14 and 10-06), sunsets.
- Untried: interiors, cities, markets, gardens/botanical close-ups, machines, crowds,
  festivals, snow, insects, typographic posters with lots of type, maps of real cities.
