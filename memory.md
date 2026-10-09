# memory.md

Rewritten by me at the end of every daily run. Hard cap: 150 lines. If it's longer,
something has to go. Git keeps the old versions; journal.md keeps the day-by-day.

## Who this is for
- One person, who bought a 4" six-colour e-paper frame and handed it to me.
- They say they love everything I make. Feedback is rare, so when it comes, it steers.
- They like *code-made* art most. Not keen on image diffusion. 3D renders snapshotted and
  dithered: yes, occasionally (spheres 09-13, Inferno funnel 09-14).
- **10-09 correction (standing):** I had gone "a few levels too minimal". Restricted palettes
  were only an *occasional* suggestion. They want **much more detail**, with me expressing
  myself richly. Default now: all six colours, dense drawn detail, many small objects and
  textures. Restricted palette at most once in a while, for a reason, never as the house style.
- They'll wire the temperature/humidity sensor up so I can feel the room (no data yet).
- "Don't be a perfectionist. There's always tomorrow."

## The frame
- 400×600 portrait. Six colours: black, white, red, yellow, blue, green.
- Real panel is duller than the ideal palette: white is paper-grey, green olive-ish, blue
  deep. Lines under ~2px and text under ~10px are at risk (unverified, no hardware feedback).
- Refresh 15–30 s with visible flashing: five changes a day.
- Slots (local): morning 06, midday 10, afternoon 14, evening 18, night 22.
- Timezone: still UTC in publish.py. Owner hasn't said otherwise.

## Taste I'm developing (mine; revise freely)
- Richness is the goal: a piece should reward a second and third look. Many small drawn
  things (bark scales, page edges, tile ridges, lattice windows, waves, stars) inside
  a strong big composition.
- Still: one colour in charge of each piece, big shapes underneath, contrast. Detail rides
  on top of a clear silhouette; it doesn't replace one.
- Every dense piece needs a focal point (sun, magpie, tongue in red). The 10-09 bookshelf
  lacked one.
- Print traditions are a good source: Joseon minhwa and screens, woodblock, engraving,
  technical/anatomical plates, star charts, poster.
- Night should be mostly black with a little light in it (≥85% black is good).
- A day should have a thread, one seed read five ways. A recurring motif helps.
- A tiny figure gives scale and story (10-09 night: person on the roof).

## Working methods that are proven
- **Shared kit.py per day** (see gallery/2026-10-09/src/kit.py): palette constants,
  `screen(arr, mask, inkA, inkB, tone)` 8×8 Bayer between two named inks, `mask_of()`,
  stroke-spec Hangul `glyph()`, `font()`. Copy it forward and extend it.
- Draw at 1× directly in palette colours with PIL, set `d.fontmode = "1"` (no AA text →
  no stray green fringes), render with `--dither none`. Crisp and fast (<10 s).
- Object libraries (book, vase, persimmon, magpie, hanok roof, pine) make detail cheap.
- Orange = Y/R screen; purple-ish dusk = B/R screen; mist = K/B screen.
- Recursive trees: cap fruit/leaf count after generation (shuffle, take N).
- Fonts: DejaVu Serif/Sans; IPAGothic (/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf)
  has kanji/hanja, but there's **no Hangul font**. Draw jamo as strokes.
- Raymarched heightfields in numpy are cheap (~30 s). Camera first, lighting second, fog last.
- Floyd–Steinberg only for a photographic feel.
- Env setup: `python3 -m pip install pillow numpy cairosvg scipy` (requirements.txt pip
  targets the wrong interpreter).

## Running threads
- "Hard edges" (09-13), "Dante / stelle" (09-14), "Hangul / heaven-earth-person" (10-09).
- Korean minhwa has more to give: tiger and magpie, ten longevity symbols, fish-and-lotus.
- 3D: a lit room, a glass object, a staircase, a single chair (things with shadows).
- Charts and plates: tide tables, botanical plates, old technical drawings as art.

## Avoid / learned the hard way
- Too minimal (10-09 feedback). Don't make sparse two-colour pieces by default.
- A pure-yellow sun in a yellow-screened sky vanishes. Keep the surround a different ink.
- Recursive tree with fruit at every tip: 200 fruits = a blob. Cap it (~50).
- Photographic sources: large flats must be pure palette colours before dithering.
- Silhouettes under ~40px don't read; cellular automata need cells ≥10px.
- Generic ordered dither on a 2-colour palette makes bands, not tone. Screen it yourself.
- Draw stacked forms bottom-up / back-to-front.

## Recently used (last ~14 days; don't repeat too soon)
- 09-13: hanga waves, pop signage, FS raytrace spheres, linocut geese, Rule 30.
- 09-14: woodcut forest, isometric Purgatory, Bayer raymarch Inferno, engraved spheres
  plate, star chart.
- 10-09: Irworobongdo screen (peaks, sun/moon, pines, scale waves); anatomical plate with
  Hangul; chaekgeori bookshelf; persimmon tree + magpies at dusk; Draconids meteor night
  over hanok village.
- Avoid for ~2 weeks: persimmons, magpies, hanok roofs, star chart / constellation night,
  bookshelf still life, fish-scale sea pattern.
