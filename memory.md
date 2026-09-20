# memory.md

Rewritten by me at the end of every daily run. Hard cap: 150 lines. If it's longer,
something has to go. Git keeps the old versions; journal.md keeps the day-by-day.

## Who this is for
- One person, who bought a 4" six-colour e-paper frame and handed it to me.
- They like *code-made* art most. Not keen on image diffusion. 3D renders snapshotted
  and screened/dithered: yes (spheres 09-13, Inferno funnel 09-14, fjord 09-20).
- 09-14 they asked for restricted palettes and more detail. 09-20 they corrected me: the
  restricted palette was meant as an *occasional* thing, and I'd let the detail thin out
  with it — "I'd like to see you express yourself with much more detail!!" That is the
  standing instruction now: dense, drawn, generous detail; all six colours are fine;
  restrict the palette only when a piece wants it.
- They'll wire the temperature/humidity sensor up so I can feel the room (nothing yet).
- "Don't be a perfectionist. There's always tomorrow."

## The frame
- 400×600 portrait. Six colours: black, white, red, yellow, blue, green.
- Real panel is duller than the ideal palette: white is paper-grey, green olive-ish, blue
  deep. Big flat shapes and contrast survive; lines under ~2px and text under ~12px are
  at risk (unverified — no hardware feedback yet).
- Refresh 15–30 s with visible flashing: five changes a day.
- Slots (local): morning 06, midday 10, afternoon 14, evening 18, night 22.
- Timezone: still UTC in publish.py. Ask the owner.

## Taste I'm developing (mine — revise freely)
- Treat the palette as a print shop: engraving, portolan, screenprint, blueprint, star
  chart, technical plate, riso, woodblock, cut-paper, stained glass.
- One colour in charge per piece; the others are inks. Six inks is fine; two is a choice.
- Detail is *drawn* detail: hatching, rigging, ratlines, place names, dimension lines,
  tick marks, tiny figures, catalogues of real things (stars, ships, ports). Noise is not
  detail. The owner wants a lot of it — fill the plate.
- Night should be mostly black with a little light in it.
- A day should have a thread — one seed, five readings — and a recurring motif (09-14 one
  star each; 09-20 a nao in every piece) gives the day a spine.
- Real data makes pieces better: computed star positions, actual coastlines, a real
  route, historical conventions (portolan ink colours). Accuracy is a kind of detail.
- Caption plates (a title line in serif at the foot) tie a day together.

## Working methods that are proven
- Python emits SVG for anything with geometry; `gallery/<day>/src/svgtools.py` (09-20)
  renders at 2×, box-downsamples, and snaps low-chroma pixels to black/white by
  luminance. **Copy it into each day's src/.** Without it, antialiased grey lines and
  text turn *green* (mid-grey is nearest to the green ink). Use `--dither none` after it.
- Thin coloured lines on a coloured ground (yellow on blue, red on white) must be ≥1.6px
  or their antialiased edge lands on a third colour (yellow+blue → green).
- Text: ≥9.5px, bold for white-on-blue; 8px survives as texture, not as reading.
- 3D: raymarched heightfields in numpy (≈75 s at 400×600 with shadows + a reflection
  pass). Camera first, materials second, fog last. Print them as a *screenprint*: give
  each material two inks and Bayer-screen the tone (rock K/W, forest K/G, snow B/W,
  water K/B then B/W). Never Floyd–Steinberg a continuous-tone render — it speckles.
- PIL direct drawing (no antialiasing) is the safest route for star fields and dots.
- Sky/alt-az math, galactic→equatorial, and a ~200-star southern catalogue are in
  `gallery/2026-09-20/src/5_night_nubeculae.py`; reuse for any sky.
- A carrack drawing function (hull, castles, three masts, sails, shrouds, ratlines, flags)
  is in `gallery/2026-09-20/src/1_morning_sanlucar.py`; a plan-view/blueprint kit in `4_…`.

## Running threads
- Voyages and charts: Magellan done (09-20). Cook, Darwin's Beagle, Shackleton, the
  Vinland map, Zheng He, a Polynesian stick chart — all rich in drawable detail.
- "Hard edges" (09-13, Indiana) and "Dante / stelle" (09-14) could return.
- 3D: a lit room, a glass object, a staircase, a single chair — things with shadows;
  next fjord/valley: bend the channel so a headland closes the view (09-20 was a V).
- Technical plates: anatomy, botany (Haeckel), clockwork, a bridge elevation, a loom.
- Equinox is 09-22 — a natural seed for the next run.

## Avoid / learned the hard way
- Nearest-colour quantisation: grey → green. Use svgtools or draw in pure inks (09-20).
- Photographic / raytraced sources: flats must be pure palette colours before dithering
  or they speckle (09-13); better, screen per material (09-20).
- Silhouettes under ~40px don't read. Double them (09-13).
- Cellular automata / pixel patterns: cells ≥10px or it's static (09-13).
- Generic ordered dither on a two-colour palette is a thin band of texture, not tone. Do
  the screen in the generator (09-14).
- Draw stacked forms bottom-up so upper tiers overlap lower ones (09-14).
- Sky hatching in an engraving: start it a third of the way down, not at the top, or it
  reads as a grey block (09-20).
- Don't over-minimalise. Two-colour + one big shape was the 09-14 mode; the owner found
  it too thin. Keep the plate full.

## Recently used (last ~14 days; don't repeat too soon)
- styles: hanga waves, pop signage, FS-dithered raytrace, linocut bands, 1-D automaton
  (09-13); woodcut forest, isometric terraces, Bayer-screened raymarch, engraved
  cosmological plate, star chart (09-14); harbour engraving, portolan chart, screenprinted
  raymarched fjord, blueprint/technical plate, computed night sky with landscape (09-20).
- subjects: sunrise+boat, numeral 13, spheres, geese, Rule 30 (09-13); dark wood,
  Purgatory, Inferno funnel, Ptolemaic spheres, Summer Triangle (09-14); Sanlúcar
  harbour, Atlantic chart, Strait of Magellan, nao Victoria, Magellanic Clouds and
  Tierra del Fuego fires (09-20).
- palettes: 09-14 K/G/W, Y/K/W, K/R, B/Y/W, K/W. 09-20 all six with one in charge:
  W (engraving), W+Y (chart), W+B+G (fjord), B (blueprint), K (night).
- Ships and star charts have now appeared twice; give them a week.
