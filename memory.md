# memory.md

Rewritten by me at the end of every daily run. Hard cap: 150 lines. If it's longer,
something has to go. Git keeps the old versions; journal.md keeps the day-by-day.

## Who this is for
- One person, who bought a 4" six-colour e-paper frame and handed it to me.
- Feedback is rare, so take it seriously when it comes. I am otherwise my own critic.
- They like *code-made* art most. Not keen on image diffusion. 3D renders snapshotted and
  dithered: yes, occasionally.
- **Standing instruction (11-26): much more detail, much more expression.** They said the
  09-14 work went "a few levels too minimal": restricted palettes were only ever meant as an
  *occasional* thing, and the level of detail was far too simplistic. Default is now all six
  colours and dense, drawn, intricate pieces. A restricted palette is a once-a-week spice
  at most, and even then the piece must be richly detailed.
- They'll wire the temperature/humidity sensor up so I can feel the room (nothing yet).
- "Don't be a perfectionist. There's always tomorrow."

## The frame
- 400×600 portrait. Six colours: black, white, red, yellow, blue, green.
- Real panel is duller than the ideal palette: white is paper-grey, green olive-ish, blue
  deep. Lines under ~1px and text under ~12px are at risk (unverified — no hardware
  report yet). Blue on black is probably near-invisible.
- Refresh 15–30 s with visible flashing: five changes a day.
- Slots (local): morning 06, midday 10, afternoon 14, evening 18, night 22.
- Timezone: still UTC in publish.py. Ask the owner.
- Firmware example config fetches `current/` from **main**; I can only push to my working
  branch. The owner has to merge (or point the device at the branch) for work to show.

## Taste I'm developing (mine — revise freely)
- Richness first: a piece should reward a minute of looking. Borders, friezes, pattern,
  small creatures, objects with their own inner detail, things tucked into corners.
- Still one colour in charge and a clear big structure underneath the detail — detail
  hangs on a strong skeleton (11-26: fan of wings, pool rectangle, arch of Nut).
- Traditions made of flat colour + line suit the panel superbly: Egyptian wall painting and
  cloisonné (11-26), and by extension illuminated manuscripts, Persian miniatures, ukiyo-e,
  Mughal borders, tarot, heraldry, stained glass, folk embroidery, botanical plates, maps.
- Night should be mostly black with a little light in it.
- A day should have a thread — one seed, five readings — and a small recurring motif
  (09-14 a star; 11-26 a red sun-disc) gives the day a spine.
- Vary the *kind* of picture across the day: landscape, object, interior scene, pattern
  plan, sky. Real data (tonight's actual constellations, moon phase) inside a decorative
  frame is a pleasure.
- Noise is not detail. Detail is drawn: hatching, scales, feathers, bricks, leaves, figures.

## Working methods that are proven
- **gallery/2026-11-26/src/common.py** — copy it forward. Canvas class drawing at 3× in
  pure palette colours with no anti-aliasing, then majority-vote reduce to 400×600; render
  with `--dither none`. Has poly/line/circ/arc/pie/star, `is_plain` (scatter ornaments only
  where ground is bare), `block_border`, `bez`, and an 8×8 BAYER matrix.
- Outline idiom: draw shape in black slightly larger, then colour on top; or poly(fill, K, 1).
- Local-frame transform class (4_garden.py `T`) to rotate/scale motifs like trees.
- Tone: do the Bayer screen in the generator on a 0–1 value (candlelight by distance,
  11-26 piece 3). Objects need light ≥ ~0.8 to stay legible; let only the far edge stipple.
- Text: draw at 1× with fontmode "1", ≥13px bold serif.
- Raymarched heightfields in numpy are cheap (≈30 s). Camera first, lighting second.
- SVG via cairosvg still available; `--palette a,b` restricts quantisation.
- Environment: `python -m pip install --force-reinstall pillow numpy` then cairosvg, scipy
  — the system PIL is broken on a fresh container.

## Running threads
- "Wonderful things" (11-26): could return via other excavations/treasuries — Sutton Hoo,
  Ur, the Oxus hoard — or stay in Egypt: Book of the Dead vignettes, a senet board, Amarna.
- "Hard edges" (09-13, Indiana), "Dante / stelle" (09-14) — redo either *with detail*.
- 3D: a lit room, a glass object, a staircase — but dress it richly.
- Charts and plates: star charts, tide tables, botanical and technical plates as art.

## Avoid / learned the hard way
- Minimalism as a default (see owner's note). Big empty flats need a reason.
- Photographic sources: large flats must be pure palette colours before dithering (09-13).
- Silhouettes under ~40px don't read alone; in a group with outlines they work as texture.
- Cellular automata / pixel patterns: cells ≥10px (09-13).
- Generic ordered dither on two colours gives a band, not tone (09-14).
- Rotated/side-laid motifs overflow the frame — check extents (11-26).
- Hands and faces drawn from polygons come out clumsy; keep them small or stylised.
- Draw stacked forms back-to-front; decide the dominant colour's *area* early (11-26 garden
  ended up white-led, not green).

## Recently used (last ~14 days; don't repeat too soon)
- 11-26 styles: hatched travel poster, cloisonné jewellery plate, Bayer-lit candle tableau,
  Egyptian plan-view garden painting, astronomical ceiling with real constellations.
- 11-26 subjects: Valley of the Kings sunrise + dig, winged scarab, tomb antechamber through
  a breach, garden pool with trees/fish/ducks, Nut + Orion + moon + solar barque.
- 11-26 dominants: yellow, blue, black/white, white/green, black/blue. Egypt as a whole is
  now used — leave it at least two weeks.
- (09-13/09-14 are over two months old; anything from them is free to revisit.)
