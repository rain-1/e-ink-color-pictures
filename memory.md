# memory.md

Rewritten by me at the end of every daily run. Hard cap: 150 lines. If it's longer,
something has to go. Git keeps the old versions; journal.md keeps the day-by-day.

## Who this is for
- One person, who bought a 4" six-colour e-paper frame and handed it to me.
- They say they love everything I make. Feedback is rare; when it comes, it's in the run prompt.
- They like *code-made* art most. Not keen on image diffusion. 3D renders dithered: yes, occasionally.
- **10-08 correction (most important note here):** I had gone "a few levels too minimal".
  Restricted palettes were meant as an *occasional* thing, not a rule. They want me to
  "express myself with much more detail". Default now: full six colours, rich drawn detail —
  hundreds/thousands of drawn elements, scenes with stuff in them. A 2–3 colour piece is
  fine maybe once a week, and even then dense.
- They'll wire the temperature/humidity sensor up so I can feel the room (no data yet).
- "Don't be a perfectionist. There's always tomorrow."

## The frame
- 400×600 portrait. Six colours: black, white, red, yellow, blue, green.
- Real panel is duller than the ideal palette: white is paper-grey, green olive-ish, blue
  deep. Lines under ~2px and text under ~12px are at risk (still unverified — no hardware
  report yet). I now accept 1px detail as texture, but keep *structure* bold.
- Refresh 15–30 s with visible flashing: five changes a day.
- Slots (local): morning 06, midday 10, afternoon 14, evening 18, night 22.
- Timezone: still UTC in publish.py. Ask the owner.

## Taste I'm developing (mine — revise freely)
- Detail is the point. Scenes, not symbols: a lawn with every blade, a town with every tree,
  a plate with captions and ticks and eyepiece sketches. Fill the frame.
- Still: one colour in charge per piece (a busy picture needs a dominant field), and night
  mostly black with light in it.
- Print-shop references still help: engraving, Currier & Ives, naive painting, botanical
  plates, star charts, technical plates. They come with built-in detail conventions.
- A day should have a thread — one seed, five readings. A historical event + something
  real in today's sky/weather is a strong pairing (10-08: 1871 fires + Draconids).
- Text on the plate (title, caption, date) makes a piece feel like an object. Worth it.
- Tiny figures give scale and story — but they're where the eye goes, so draw them with
  care (10-08's were crude).

## Working methods that are proven
- **Pipeline (10-08):** a shared `h.py` in the day's src/ with palette constants, fonts,
  fbm noise, a Bayer `screen(tone)`, and `save()`. Draw at 2× (800×1200) in exact palette
  colours; `save()` downsamples by palette-mode of each 2×2 block (ties → rarer colour) and
  maps near-greys to black/white (antialiased text otherwise turns green). Render with
  `--dither none`. Copy 2026-10-08/src/h.py as a starting point.
- Tone with six colours: Bayer screen inside the generator (`screen(tone, 2)`) for skies,
  glows, haze; hatching lines for engraved tone.
- Depth: collect objects with a y, sort, draw far-to-near; insert buildings/bridges at
  their depth. Define every draw function *before* the depth loop.
- Procedural vocab that worked: leaves from polar/width functions + vein ticks; crowns as
  black-outlined blob clusters with dabs of a 2nd colour; recursive branching trees;
  flame tongues as 3 nested polygons (R/Y/W); smoke = warped fbm thresholded with black
  contour lines; water = mirrored rows broken into dashes + blue lines.
- Real sky: alt-az from RA/Dec + LST, stereographic projection; catalogue in
  2026-10-08/src/5_night_draconids.py (Draco, UMa, UMi, Cas, Cep, bright stars).
- Raymarched heightfields in numpy are cheap (≈30 s, 220 steps). Camera first.
- `--palette a,b,c` on render.py restricts quantisation when I do want few colours.

## Running threads
- "Hard edges" (09-13), "Dante / stelle" (09-14), "fire from the sky" (10-08).
- 3D: a lit room, a glass object, a staircase — things with shadows. Not done since 09-14.
- Plates: botanical, astronomical, technical. They suit detail. Do a botanical one properly.
- Possible: a dense city/market/harbour crowd scene with well-drawn figures; an
  isometric interior; a map.

## Avoid / learned the hard way
- Minimalism as a default (owner's correction, 10-08).
- Supersampled stipple of 1px squares → coloured noise after downsampling. Snap stipple to
  even coordinates at 2× (one output pixel each).
- Flat-bottomed clouds as solid rectangles look like slabs.
- Hatch fills must be clipped (paste through a polygon mask), not drawn across the frame.
- Photographic sources: large flats must be pure palette colours or they speckle (09-13).
- Silhouettes under ~40px don't read; cellular automata need ≥10px cells (09-13).
- Low-contrast labels (blue on black/blue) vanish; use yellow/white on dark.

## Recently used (last ~14 days; don't repeat too soon)
- 10-08 styles: overhead naturalist lawn, 19th-c. astronomical plate, naive panorama,
  Currier & Ives disaster print, real-sky star chart with landscape.
- 10-08 subjects: autumn leaves, Biela's comet/observatory, Wisconsin mill town/river/train,
  Chicago fire/Water Tower/schooners, Draconids/Draco/elm/farmhouse.
- Older (09-13/14, now aging out): hanga waves, pop numeral, raytraced spheres, linocut geese,
  Rule 30; Dante woodcut forest, Purgatory terraces, Inferno funnel, Ptolemaic spheres,
  Summer Triangle chart.
- Star charts used twice (09-14, 10-08) — rest them for a couple of weeks.
