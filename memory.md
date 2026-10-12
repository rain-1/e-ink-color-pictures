# memory.md

Rewritten by me at the end of every daily run. Hard cap: 150 lines. If it's longer,
something has to go. Git keeps the old versions; journal.md keeps the day-by-day.

## Who this is for
- One person, who bought a 4" six-colour e-paper frame and handed it to me.
- They say they love everything I make. Feedback is rare; when it comes, it's law.
- They like *code-made* art most. Not keen on image diffusion. 3D renders dithered: yes.
- **Standing request (10-12): MUCH more detail, full expression.** I had over-read their
  09-14 note. Restricted palettes are an *occasional* tool, not the default. Default to all
  six colours and dense, drawn, considered detail: rigging, planks, labels, keys, borders,
  tiny figures, stipple, hatching. Simple flat minimalism is now the exception.
- "Don't be a perfectionist. There's always tomorrow."

## The frame
- 400×600 portrait. Six colours: black, white, red, yellow, blue, green.
- Real panel is duller: white paper-grey, green olive, blue deep, yellow ochre-ish (it
  reads as parchment). Lines under ~1px and text under ~8px are at risk (unverified, no
  hardware feedback yet).
- Refresh 15–30 s with flashing: five changes a day.
- Slots (local): morning 06, midday 10, afternoon 14, evening 18, night 22.
- Timezone: still UTC in publish.py. Owner hasn't said.

## Taste I'm developing (mine — revise freely)
- The panel as a print shop: woodblock, poster, portolan, engraving, signal plates,
  screenprint, star charts, technical plates. These styles *carry* detail well.
- One colour in charge per piece still helps, even with all six present (10-12: blue
  morning, white midday, yellow chart, red/blue sunset, black night).
- Night mostly black with a little light in it.
- A day has a thread: one seed, five readings. Two seeds on the same date can braid
  (10-12: Columbus + Vaughan Williams → "the sea").
- Detail = drawn detail: ratlines, planking, labelled keys, borders, cartouches, dated
  stations, wave marks. Noise is not detail.
- Look for subjects whose *native* colours are the panel's colours: ICS signal flags,
  heraldry, portolans, Mondrian, railway signals, maritime charts, playing cards.
- Text works at 9–15px in Liberation Serif bold/italic; 7px is borderline.

## Working methods that are proven
- gallery/2026-10-12/src/common.py: Canvas class drawing in 400×600 units on a 2× image,
  `finish()` mode-downsamples 2×2 blocks (ties lean to ink) → always on-palette; render
  with `--dither none`. Copy it into each day's src/ (generators import from their dir).
- **Stipple / Bayer screens must be built at 1× and doubled with np.kron**, or the mode
  downsample erases them (10-12).
- Rotated text: render to an "L" layer, rotate NEAREST, threshold, paste with mask.
- Ramp-dither for 3D: map a scalar tone along an ordered list of palette colours
  (e.g. K→B→R→Y→W) and Bayer-screen between neighbours. Clean, painterly (10-12 sunset).
- Ocean: plane intersection + analytic normals from ~18 sines, damped with distance;
  Fresnel × reflected sky + spec^900 sun road. Under 1 s at 400×600.
- Raymarched heightfields in numpy (≈30 s). Camera first, lighting second, fog last.
- Floyd–Steinberg only for a photographic/halftone feel.
- `--palette a,b,c` on render.py exists for occasional restricted pieces.

## Running threads
- "Hard edges" (09-13), "Dante / stelle" (09-14), "the sea" (10-12). All could return.
- 3D still wanted: a lit room, a glass object, a staircase, a chair, a lighthouse interior.
- Charts and plates: tide tables, botanical plates, old technical drawings, flag keys.
- Vaughan Williams: The Lark Ascending, an autumn English landscape. Not yet made.

## Avoid / learned the hard way
- Photographic sources: large flats must be pure palette before dithering (09-13).
- Silhouettes under ~40px don't read; double them (09-13).
- CA / pixel patterns: cells ≥10px (09-13).
- Dark figures on a dark ground vanish even with rim lines. Put light *behind* them
  (sky glow, lantern halo, the Milky Way) instead (10-12).
- Full-page rhumb networks get busy; keep lines 0.5px and let one colour (yellow) rule.
- Hard-edged screen cut-offs (y > N) look like rectangles. Let glows fall off radially.
- Draw stacked forms bottom-up (09-14).

## Recently used (last ~14 days; don't repeat too soon)
- 10-12 styles: woodblock seascape, harbour poster + flag key plate, portolan chart,
  ramp-dithered 3D ocean, stippled night scene with figures.
- 10-12 subjects: caravel at dawn, barque dressed overall, Atlantic route chart, sunset sea
  with three ships, two figures at a rail under the Milky Way.
- Older (09-13/14, now out of the window): hanga waves, pop numeral, raytraced spheres,
  geese, Rule 30, dark wood, Purgatory, Inferno funnel, Ptolemaic plate, star chart.
- Ships have now appeared in four of the five 10-12 pieces. Give ships a rest for two weeks.
