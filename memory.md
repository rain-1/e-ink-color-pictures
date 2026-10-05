# memory.md

Rewritten by me at the end of every daily run. Hard cap: 150 lines. If it's longer,
something has to go. Git keeps the old versions; journal.md keeps the day-by-day.

## Who this is for
- One person, who bought a 4" six-colour e-paper frame and handed it to me.
- They say they love everything I make. Feedback is rare, so when it comes, it's law.
- They like *code-made* art most. Not keen on image diffusion. 3D renders snapshotted and
  dithered: yes, occasionally.
- **Standing correction (10-05): I had gone "a few levels too minimal." Restricted palettes
  were meant as an OCCASIONAL thing, not the default. They want MUCH MORE DETAIL: express
  myself, fill the frame with drawn incident.** Default = all six colours, dense scenes.
  A 2–3 colour piece is fine maybe once every few days, and still detailed.
- They'll wire the temperature/humidity sensor up so I can feel the room (no data yet).
- "Don't be a perfectionist. There's always tomorrow."

## The frame
- 400×600 portrait. Six colours: black, white, red, yellow, blue, green.
- Real panel is duller than the ideal palette: white is paper-grey, green olive-ish, blue
  deep. Unverified on hardware still.
- Refresh 15–30 s with visible flashing: five changes a day.
- Slots (local): morning 06, midday 10, afternoon 14, evening 18, night 22.
- Timezone: still UTC in publish.py. Owner hasn't said.

## Taste I'm developing (mine — revise freely)
- Density is the point now: villages, figures, boats, birds, windows, flowers in margins,
  labels, reflections. Think Patinir, Bruegel, Guardi, book-of-hours pages, survey maps,
  Richard Scarry-level incident. Every square inch should reward a second look.
- Still: one colour in charge per piece (sheet should show five different dominants),
  big readable structure first, then detail layered on top.
- Night stays mostly black (~85–90%) with small lit things in it: lanterns, fires, windows, stars.
- A day should have a thread: one seed, five readings. 10-05's "one world, five views"
  (panorama / city / map / calendar page / myth at night) was a strong structure.
- A tiny figure gives scale and story. Several tiny figures give a world.
- Text set crisply (fontmode '1') works: cartouches, labels, calendar headings.

## Working methods that are proven
- `gallery/2026-10-05/src/ink.py` is a good helper to copy: palette constants,
  `mix(img, mask, c1, c2, t)` = 8×8 Bayer screen between two palette colours (t can be
  an array, which gives gradients), `fill`, `vnoise` fractal value noise, `noise1`. Generators
  output only palette colours → `render.py --dither none`.
- Masks from PIL: draw polygons/lines into an 'L' image, `np.array(m) > 0`.
- Text: `ImageDraw` on mode '1' with `d.fontmode='1'`; fonts in /usr/share/fonts/truetype
  (liberation serif/italic/bold, dejavu). Add a 1px white halo for labels on busy ground.
- Contours: `q=floor(h/step)`, line where q differs from the up/left neighbour.
- Reflections: sample the scene mirrored about the waterline with a sine x-wobble, keep
  only where the source was architecture, drop every 4th row and fade with Bayer.
- Scatter many objects, then draw the important ones LAST (villages over trees).
- Cloud lighting: take the gradient of a smooth noise field, never of a detailed one.
- Raymarched heightfields in numpy are cheap (≈30 s at 400×600). Camera first, lighting second.
- Render SVG at 2× then downsample (render.py does this). `--palette a,b,c` exists.
- `pip install -r requirements.txt` first. The container starts without numpy.
- Preview at 2× with NEAREST into the scratchpad to inspect details; the sheet for balance.

## Running threads
- Patinir world (10-05): the Meuse, Dinant, the rock pinnacles, St Jerome, Charon. Could
  return as a recurring imaginary country, the same map from other angles and seasons.
- Book-of-hours calendar pages: a different month's page when the month turns (Nov: pig/acorns,
  Dec: boar hunt). Strong frame, lots of room for detail.
- Hard edges (09-13), Dante (09-14).
- 3D: a lit room, a glass object, a staircase, a dense miniature town. Same density as 10-05.

## Avoid / learned the hard way
- Being minimal by default (owner, 10-05).
- Black figures on black ground vanish. Give them a rim light and a glow behind.
- Photographic / raytraced sources: flats must be pure palette colours before dithering.
- Silhouettes under ~40px don't read alone; small figures work in crowds, with colour.
- Cellular automata: cells ≥10px or it's static.
- Generic ordered dither on a 2-colour palette = thin band of texture. Screen it in-generator.
- Noisy hillshade/cloud edges → blotchy "map of continents". Smooth the field first.

## Recently used (last ~14 days; don't repeat too soon)
- 09-13: hanga waves, pop "13" sign, raytraced spheres, linocut geese, Rule 30.
- 09-14: woodcut dark wood, Purgatory terraces, raymarched Inferno, Ptolemaic plate, star chart.
- 10-05 styles: Patinir panorama, Guardi veduta/capriccio, topographic survey sheet,
  illuminated calendar page, night river scene.
- 10-05 subjects: rock pinnacles + St Jerome, Venice (campanile, dome, gondola, bragozzo),
  Meuse/Dinant map, sower + Scorpio, Charon + Saturn.
- Untried: 3D at high density, isometric city, botanical plate, cutaway building, market
  scene, underwater, a busy harbour at night, a library, a Bruegel-style crowd.
