# memory.md

Rewritten by me at the end of every daily run. Hard cap: 150 lines. If it's longer,
something has to go. Git keeps the old versions; journal.md keeps the day-by-day.

## Who this is for
- One person, who bought a 4" six-colour e-paper frame and handed it to me.
- They say they love everything I make. Feedback will be rare; I am my own critic.
- They like *code-made* art most. Not keen on image diffusion, curious if I ever have a
  real reason. 3D renders snapshotted and dithered: yes, occasionally — they've now had
  two (spheres 09-13, Inferno funnel 09-14) and asked for nothing less.
- They asked on 09-14 for restricted palettes and *more detail and attention per piece*.
  That request stands until they say otherwise.
- They'll wire the temperature/humidity sensor up so I can feel the room — sensors.jsonl
  and feedback.jsonl are still both empty as of 09-18. Don't assume data will be there;
  check first, and don't invent a location/climate if it isn't.
- "Don't be a perfectionist. There's always tomorrow."

## The frame
- 400×600 portrait. Six colours: black, white, red, yellow, blue, green.
- Real panel is duller than the ideal palette: white is paper-grey, green olive-ish, blue
  deep. Big flat shapes and contrast survive; lines under ~2px and text under ~12px are
  at risk (unverified — no hardware yet). Small technical-plate labels (Spheres 09-14,
  the Daylight blueprint's title block 09-18) are decorative texture, not meant to be
  read up close — don't rely on them carrying meaning.
- Refresh 15–30 s with visible flashing: five changes a day.
- Slots (local): morning 06, midday 10, afternoon 14, evening 18, night 22.
- Timezone: still UTC in publish.py. Ask the owner. Location also unknown — no weather
  seed has been usable yet for that reason; lead with the calendar/sky instead.

## Taste I'm developing (mine — revise freely)
- Treat the palette as a print shop, not a screen. Riso, screenprint, woodblock, linocut,
  engraving, poster, cut-paper, stained glass, star charts, technical plates, blueprints.
- Two or three colours per piece beats six. One colour in charge; the others are ink.
  Exception worth allowing deliberately: a true 50/50 split (evening scales 09-18, red vs
  blue) when the *concept itself* is a balance — don't force dominance where parity is
  the point, but know it's the exception, not the default.
- Night should be mostly black with a little light in it (09-13 star chart; 09-18
  afterglow — a Bayer-screened glow band covering under 10% of the frame reads as
  "night with light in it" and still keeps black dominant. Good ratio to reuse.)
- A day should have a thread — one seed, five readings of it — and a small recurring
  motif across the five (09-14: one star each; 09-18: a circle marking a moment — sun,
  data point, pan-contents, star) gives the day a spine.
- Detail is welcome when it's *drawn* detail: hatching, ticks, labels, tiny figures,
  plotted data. Noise is not detail.
- A tiny figure gives scale and story. Use sparingly; it's a trick.
- A halftone/dot-grid glow (09-18 Full Burn) works but a uniform grid gets busy up close;
  next time vary dot size or spacing more aggressively, or accept it as an all-over
  texture piece rather than a focal one.

## Working methods that are proven
- Python/PIL generators writing to $OUT_RAW; SVG hand-written or emitted by Python
  (emit SVG from Python for anything with geometry — rings, tiers, ticks, charts).
- Render SVG at 2× then downsample (render.py does this; hand-built generators should
  match by rendering at 2x with cairosvg and letting fit() downsample, or by drawing
  straight at 400x600 in numpy when the piece is flat colour/tone with no fine edges).
- `--palette a,b,c` on render.py restricts quantisation. For 2-colour work with tone,
  do the 8×8 Bayer screen *inside* the generator on a 0–1 tone value and use `--dither
  none`. Double-check the sign of any tone formula before rendering — an inverted
  gradient (09-18 night piece, first attempt) fills the whole frame instead of a band;
  render once and look before moving on.
- Raymarched heightfields in numpy are cheap (≈30 s at 400×600, 220 steps). Camera first,
  lighting second, fog last.
- Floyd–Steinberg only when I want a halftone/photographic feel (09-13 spheres).
- Fonts available in this environment: DejaVu Sans/Serif/Sans Mono, Liberation
  Sans/Serif/Mono, FreeMono. "Helvetica"/"Georgia"/"Courier New" font-family names may
  fall back oddly (garbled glyphs seen 09-18 first draft) — name an installed family
  directly, or at least list it first in the stack, and re-render to check the text.
- A plotted dataset (09-18 daylight chart) is a good technical-plate subject alongside
  star charts and tide tables — approximate astronomical/seasonal curves are fine to draw
  from formula/memory, same standard as the 09-14 star chart: "good enough at four
  inches," not a research paper.

## Running threads
- "Hard edges" (09-13, 09-18) and "Dante / stelle" (09-14). All could return.
- 3D: a lit room, a glass object, a staircase, a single chair — things with shadows.
- Charts and plates: star charts, tide tables, blueprints, old technical drawings as art.
- The equinox itself (Sept 22, 2026) hasn't happened yet as of this writing — the day of,
  or the day after, could be worth a return visit ("level now" vs. "four days out").
- A countdown/tally motif (09-18 morning ticks) could be threaded across all five slots
  instead of just one, if a future seed has its own deadline or count to mark.

## Avoid / learned the hard way
- Photographic / raytraced sources: large flats must be pure palette colours before
  dithering or they speckle (09-13).
- Silhouettes under ~40px don't read. Double them (09-13).
- Cellular automata / pixel patterns: cells ≥10px or it's static (09-13).
- Generic ordered dither on a two-colour palette produces a thin band of texture, not
  tone. Do the screen in the generator (09-14).
- Draw stacked forms bottom-up so upper tiers overlap lower ones (09-14, Purgatory).
- Named fonts not actually installed can render mangled glyphs on punctuation/symbols
  (em dash, degree sign) — plain ASCII in SVG text is safer until fonts are confirmed
  (09-18). A gradient tone formula's sign is easy to get backwards — render and check
  before calling a generator done (09-18).
- Missed days happen (09-15 to 09-17 skipped, cause unknown from this side) — the run
  doesn't try to backfill missed days, just picks up the seed as of today.

## Recently used (last ~14 days; don't repeat too soon)
- styles: hanga waves, pop signage, FS-dithered raytrace, linocut bands, 1-D automaton
  (09-13); woodcut forest, isometric terraces, Bayer-screened raymarch, engraved
  cosmological plate, star chart (09-14); hard-edge flat colour, halftone dot-grid,
  blueprint chart, poster/scale illustration, Bayer-screened glow band (09-18).
- subjects: sunrise+boat, numeral 13, spheres still-life, geese, Rule 30 (09-13);
  dark wood, Purgatory mountain, Inferno funnel, Ptolemaic spheres, Summer Triangle
  (09-14); sunrise+hill, noon sunburst, daylight-vs-year chart, balance scale, horizon
  afterglow (09-18, all under the equinox thread — avoid another full "balance/equinox"
  day soon, though a single piece revisiting it post-equinox is fine).
- palettes used: K/G/W, Y/K/W, K/R, B/Y/W, K/W (09-14); R/W/K, Y/R/K/W, B/W, R/B/W, K/G
  (09-18). Still untouched: G/Y, R/Y (plain pair), G/W plain, B/K plain, all-six.
