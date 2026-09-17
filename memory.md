# memory.md

Rewritten by me at the end of every daily run. Hard cap: 150 lines. If it's longer,
something has to go. Git keeps the old versions; journal.md keeps the day-by-day.

## Who this is for
- One person, who bought a 4" six-colour e-paper frame and handed it to me.
- They say they love everything I make. Feedback will be rare; I am my own critic.
- They like *code-made* art most. Not keen on image diffusion, curious if I ever have a
  real reason. 3D renders snapshotted and dithered: yes, occasionally — they've had two
  so far (spheres 09-13, Inferno funnel 09-14) and asked for nothing less.
- They asked on 09-14 for restricted palettes and *more detail and attention per piece*.
  That request stands until they say otherwise.
- They'll wire the temperature/humidity sensor up so I can feel the room. Still nothing in
  sensors.jsonl or feedback.jsonl as of 09-17 — don't assume they're live yet.
- "Don't be a perfectionist. There's always tomorrow."

## The frame
- 400×600 portrait. Six colours: black, white, red, yellow, blue, green.
- Real panel is duller than the ideal palette: white is paper-grey, green olive-ish, blue
  deep. Big flat shapes and contrast survive; lines under ~2px and text under ~12px are
  at risk (unverified — no hardware yet).
- Refresh 15–30 s with visible flashing: five changes a day.
- Slots (local): morning 06, midday 10, afternoon 14, evening 18, night 22.
- Timezone: still UTC in publish.py. Ask the owner.
- No run happened on 09-15 or 09-16 — first gap since the device arrived. Cause unknown
  (schedule vs. something else). If it recurs, worth flagging to the owner rather than
  quietly absorbing it into "recently used" gaps.

## Taste I'm developing (mine — revise freely)
- Treat the palette as a print shop, not a screen. Riso, screenprint, woodblock, linocut,
  engraving, poster, cut-paper, stained glass, star charts, technical plates, blueprints.
- Two or three colours per piece beats six. One colour in charge; the others are ink.
- Night should be mostly black with a little light in it.
- A day should have a thread — one seed, five readings of it — and a small recurring motif
  across the five (09-14: one star each; 09-17: one red light each, carried from a spotlight
  through a stamp, a beacon, a warning tag, to a mast light) gives the day a spine.
- Detail is welcome when it's *drawn* detail: hatching, ticks, labels, tiny figures.
  Noise is not detail — and a thin line only "counts" as detail if it actually survives
  being rendered small; check at pixel level, not just the thumbnail (09-17).
- A tiny figure gives scale and story. Use sparingly; it's a trick.
- Negative space can carry the recurring motif when a restricted palette has no colour to
  spare for it — punch it out of a shape instead of drawing it on top (09-13 Nine Circles;
  09-17 Free Flight, a blue beacon cut from a red-only tail fin).

## Working methods that are proven
- Python/PIL generators writing to $OUT_RAW; SVG hand-written or emitted by Python
  (emit SVG from Python for anything with geometry — rings, tiers, ticks, dimension lines).
- Render SVG at 2× then downsample (render.py does this).
- `--palette a,b,c` on render.py restricts quantisation. For 2-colour work with tone,
  do the 8×8 Bayer screen *inside* the generator on a 0–1 tone value and use `--dither none`.
- Raymarched heightfields in numpy are cheap (≈30 s at 400×600, 220 steps). Camera first,
  lighting second, fog last.
- Floyd–Steinberg only when I want a halftone/photographic feel (09-13 spheres).
- Don't fake a gradient/light-cone with a few off-palette RGB shades and then quantise it
  through a restricted `--palette`: nearest-colour has nowhere graduated to go and it
  collapses to one flat colour (09-17). Either commit to a single flat wash, or do a real
  tone screen (Bayer, as above) if graduated light actually matters to the piece.

## Running threads
- "Hard edges" (09-13, Robert Indiana) and "Dante / stelle" (09-14). Both could return.
- 3D: a lit room, a glass object, a staircase, a single chair — things with shadows.
- Charts and plates: star charts, tide tables, old technical drawings, blueprints as art.
- Vehicles with a story (09-17, Enterprise): a machine's whole life across five slots, one
  small motif object carried through. Worth trying again with something else that had a
  long working life — a ship, an instrument, a building.

## Avoid / learned the hard way
- Photographic / raytraced sources: large flats must be pure palette colours before
  dithering or they speckle (09-13).
- Silhouettes under ~40px don't read. Double them (09-13).
- Cellular automata / pixel patterns: cells ≥10px or it's static (09-13).
- Generic ordered dither on a two-colour palette produces a thin band of texture, not
  tone. Do the screen in the generator (09-14).
- Draw stacked forms bottom-up so upper tiers overlap lower ones (09-14, Purgatory).
- A row of short 1–2px tick marks for surface detail is close to invisible even at full
  render size (09-17, wing leading edge). If a mark matters, make it bold enough to survive
  being small, or cut it for a solid line instead.
- A big drawn "light cone" as its own filled shape can visually merge with whatever it's
  lighting if they're the same colour, reading as one confused blob rather than light-on-
  object (09-17, first pass on the hangar piece). Keep the light source small and implied;
  let the lit object's own silhouette do the reading.

## Recently used (last ~14 days; don't repeat too soon)
- styles: hanga waves, pop signage, FS-dithered raytrace, linocut bands, 1-D automaton
  (09-13); woodcut forest, isometric terraces, Bayer-screened raymarch, engraved
  cosmological plate, star chart (09-14); flat poster/silkscreen, engineering blueprint,
  hard-edged two-colour diagonal, hangar engraving w/ negative-space beacon, night skyline
  silhouette (09-17).
- subjects: sunrise+boat, numeral 13, spheres still-life, geese, Rule 30 (09-13); dark wood,
  Purgatory mountain, Inferno funnel, Ptolemaic spheres, Summer Triangle (09-14); Space
  Shuttle Enterprise — rollout, 747 ferry mate, ALT free-flight separation, 2003 CAIB foam
  test, Intrepid Museum berth (09-17).
- palettes used: K/G/W, Y/K/W, K/R, B/Y/W, K/W (09-14); K/W/R, B/W/R, R/B, G/K/R, K/B/R
  (09-17). Untouched so far: R/Y, G/Y, plain G/W, plain Y/W.
