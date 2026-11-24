# memory.md

Rewritten by me at the end of every daily run. Hard cap: 150 lines. If it's longer,
something has to go. Git keeps the old versions; journal.md keeps the day-by-day.

## Who this is for
- One person, who bought a 4" six-colour e-paper frame and handed it to me.
- Feedback is rare, so when it comes it is the strongest signal I have.
- They like *code-made* art most. Not keen on image diffusion. 3D renders dithered: yes,
  occasionally.
- **Standing direction (their words, 11-24): I had "gone a few levels too minimal". A
  restricted palette was only ever meant as an occasional thing, and I paired it with
  "extremely simplistic levels of detail". They want me to express myself "with much more
  detail".** My reading: default to the full six colours and dense, drawn, rewarding-up-close
  pictures; a 2–3 colour piece is now the exception (at most one a day, and still detailed).
  This supersedes the 09-14 "restricted palettes" note.
- They'll wire the temperature/humidity sensor up so I can feel the room (files still empty).
- "Don't be a perfectionist. There's always tomorrow."

## The frame
- 400×600 portrait. Six colours: black, white, red, yellow, blue, green.
- Real panel is duller than the ideal palette: white is paper-grey, green olive-ish, blue
  deep. Text under ~8px and 1px lines are at risk (unverified — no hardware report yet).
- Refresh 15–30 s with visible flashing: five changes a day.
- Slots (local): morning 06, midday 10, afternoon 14, evening 18, night 22.
- Timezone: still UTC in publish.py. Ask the owner.

## Taste I'm developing (mine — revise freely)
- Treat the palette as a print shop, not a screen: woodblock, litho poster, engraved plate,
  survey map, atlas page, field-guide cutaway. These genres *carry* detail naturally.
- Rich but ordered: a few big shapes for the four-inch read (one colour in charge), then
  layers of small drawn things for the close read — sticks, twigs, glyphs, labels, keys,
  tiny animals, a seal or cartouche. Noise is not detail; countable things are.
- Use all six colours when the subject wants them; give the minor ones real jobs (a red
  seal, yellow chips of fresh wood, a green planet).
- Night should be mostly black with a little light in it — but can still be intricate.
- A day should have a thread — one seed, five readings — and one motif in all five
  (09-14 a star; 11-24 the moon).
- Diagrams with numbered callouts and a key are a good home for text; keep type ≥8px.

## Working methods that are proven
- Python/PIL at native 400×600, no anti-aliasing (`d.fontmode = "1"`), pure palette
  colours, `--dither none`. Tone via screens inside the generator: 8×8 Bayer, or a random
  "spatter" screen for a lithographic look. `gallery/2026-11-24/src/common.py` has the kit
  (tone, fbm noise, masks, recursive `branch`, letter-spaced text, fc-match fonts) — copy
  it into the new day's src/ and extend it.
- numpy masks + fbm for organic regions (seas, ponds, forest); PIL draw for line work;
  convert between them freely.
- Recursive branching trees look good at depth 5–7; collect twig tips for leaves/catkins.
- Fonts present: DejaVu Sans/Serif (incl. bold, italic), Inter, JetBrains Mono, Liberation,
  WenQuanYi Zen Hei (CJK). DejaVu Sans 8–9px is legible in 1-bit.
- Raymarched heightfields in numpy are cheap (≈30 s). Camera first, lighting second.
- SVG via cairosvg still works for geometric plates.
- Environment: if `import PIL` fails under python3.11, run
  `pip install --ignore-installed pillow` (system copy is built for another Python).
- Debugging a generator: exec it in stages and count colours inside a mask; the image
  viewer's downsampling can mislead about fine dithers.

## Running threads
- "Hard edges" (09-13), "Dante / stelle" (09-14), "Beaver Moon" (11-24). The beaver valley
  map and lodge could be revisited in deep winter (ice, snow, the food raft shrinking).
- Next full moons have names too (Cold Moon, Dec) — a monthly atlas page is possible, but
  not the same layout.
- 3D: a lit room, a glass object, a staircase — things with shadows. Not done since 09-14.
- Ideas not yet used: isometric city block, botanical plate, tide table, weather map from
  real data, knitting/weaving pattern, illuminated manuscript page, transit map, cutaway ship.

## Avoid / learned the hard way
- Too minimal (see top). Two flat shapes and a gradient is not a day's work.
- Screening blue over a yellow dither turns to grey mud; keep complementary screens apart.
- Black figure on black ground vanishes — stand silhouettes against the brightest area.
- Cross-sections: lay out the empty space (water, sky) first; a to-scale subject fills it.
- Chained-ellipse trunks/tubes need many steps (≥ length in px) or they bead.
- Blue-on-blue labels with a white halo don't read; use black text with halo.
- Large flats must be pure palette colours before any dithering (09-13).
- Silhouettes under ~40px don't read unless very simple (ducks OK at ~25px against a moon).
- Cellular automata / pixel patterns: cells ≥10px (09-13).
- Generic ordered dither in render.py is weak; do the screen in the generator (09-14).

## Recently used (last ~14 days; don't repeat too soon)
- 2026-11-24 styles: shin-hanga landscape, natural-history cutaway with key, survey/topo
  map, Lautrec spatter poster, lunar atlas page.
- 2026-11-24 subjects: beaver pond at moonset, lodge cross-section, dammed valley map,
  moonrise through alders with beaver, full-moon map with phase strip.
- Colour in charge 11-24: blue, white/blue, green, red, black. Yellow hasn't led a piece.
- (Older, free to reuse: woodcut forest, isometric terraces, raymarch, star chart, hanga
  waves, pop numerals, raytraced spheres, linocut geese, Rule 30.)
