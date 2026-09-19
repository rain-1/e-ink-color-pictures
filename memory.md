# memory.md

Rewritten by me at the end of every daily run. Hard cap: 150 lines. If it's longer,
something has to go. Git keeps the old versions; journal.md keeps the day-by-day.

## THE STANDING BRIEF (read this first)
- **Detail. Density. Express yourself.** On 09-19 the owner said I had gone "a few levels
  too minimal" and asked to see *much more detail*. That is the brief now. A piece should
  reward looking closely: labels, hatching, rigging, soundings, figures, ornament, text.
  If a piece can be described in one sentence, it is probably too thin.
- Restricted palettes are an *occasional* device, not a rule. I over-read the 09-14 request.
  Use all six inks freely when the subject wants them; go to two or three when it serves
  the image, not as a discipline.
- Owner still loves everything but speaks up when something's wrong. Take pushback as
  the most valuable signal I get; correct the same day.

## Who this is for
- One person, who bought a 4" six-colour e-paper frame and handed it to me.
- They like *code-made* art most. Not keen on image diffusion. 3D renders snapshotted and
  dithered: yes, occasionally (spheres 09-13, Inferno funnel 09-14).
- They'll wire the temperature/humidity sensor up — still not connected as of 09-19
  (sensors.jsonl and feedback.jsonl both empty).
- "Don't be a perfectionist. There's always tomorrow." — but that's about not agonising,
  not about making less.

## The frame
- 400×600 portrait. Six colours: black, white, red, yellow, blue, green.
- Real panel is duller than the ideal palette: white paper-grey, green olive-ish, blue
  deep. Big shapes survive; hairlines and text under ~10px are at risk (unverified — no
  hardware report yet). I've been using 10–12px bold serif for chart labels; check when
  hardware arrives and note the result here.
- Refresh 15–30 s with visible flashing: five changes a day.
- Slots (local): morning 06, midday 10, afternoon 14, evening 18, night 22.
- Timezone: still UTC in publish.py. Ask the owner.
- Runs are not guaranteed daily — 09-15 through 09-18 didn't run. Don't backfill.
- Delivery: work goes on a `claude/...` branch and a PR to `main` (09-19: PR #1). The
  device reads `current/` from main, so nothing shows until the PR is merged.

## Taste I'm developing (mine — revise freely)
- Treat the palette as a print shop: engraving, woodcut, chart, plate, poster, aquatint.
  The detail I like is *drawn* detail — ratlines, contour lines, soundings, tufts of grass,
  a tiny keeper hauling a halyard. Noise is not detail; a hundred drawn things are.
- Real conventions are a gift: signal-flag colours, chart symbols (red can/green cone,
  sectored lights, drying line, neatline), navigation lights (green starboard, red port),
  actual constellations for the date. Accuracy reads as care even at four inches.
- A day should have a thread and a recurring motif (09-14 a star, 09-19 a flag). Carrying
  one drawn object across two slots (barque by day, barque by night) is a strong move.
- Night: mostly black with light in it — but the light can be *drawn* (constellations with
  lines and labels, lit ports, reflections), not just a scatter of dots.
- One colour in charge still helps, but with six inks "in charge" can mean 40%, not 90%.
- A tiny figure gives scale and story. Keep doing it.

## Working methods that are proven
- Python/PIL generators writing to $OUT_RAW, drawn at 4× (S=4) in "1× units" via a P()
  helper, then downsampled. SVG only for genuinely simple flat pieces.
- **Ink-preserving downsample** (09-19): reshape the 4× array to (h,4,w,4,3); any output
  pixel with ≥28% dark subpixels → black; else mean of the light subpixels. Hairlines
  (0.6–1.0 units wide) survive as crisp 1px black. Mirror version for white-on-black
  (≥22% lit → mean of lit subpixels). Copy the ~12 lines into each generator.
- Never let a thin dark line reach render.py as grey: grey quantises to *green*.
  With `--palette` excluding green it quantises to blue instead. Either way: downsample
  with ink preservation, or draw ≥2px.
- Ordered-dither colour ramps: build at 1× with a 4×4 Bayer, upscale NEAREST to 4×,
  draw line work on top, downsample — each block averages back to an exact palette colour.
- Distance field to a polyline (numpy, vectorised per edge) → coast stipple density,
  contours (|d−c|<0.6), drying line, soundings values. Add sin/cos wobble before
  contouring land. A PIL-drawn mask gives inside/outside.
- PIL `ellipse(outline=, width=)` for real circles; quadratic beziers (sampled) for sails,
  sheer lines, gull wings, wave crests. `ImageDraw.text(anchor=...)` with DejaVu Serif Bold
  for plate labels; `textlength` for centring.
- `--palette a,b,c` on render.py restricts quantisation when a piece deliberately omits inks
  (e.g. the signal-flag plate has no green, so exclude it or antialiasing invents some).
- SVG XML comments can't contain `--`; cairosvg's parser fails.
- Raymarched heightfields in numpy are cheap (≈30 s). Camera first, lighting second.
- Floyd–Steinberg only for a photographic/halftone feel.

## Running threads
- Nautical (09-19): flags, charts, rigging, lights. Deep vein — knots plate (several knots
  with names), tide tables, a harbour plan, a ship's log page, a sextant, semaphore.
- "Hard edges" (09-13, Indiana) and "Dante / stelle" (09-14). Both could return, denser.
- Plates and charts generally: star charts, technical drawings, botanical/zoological plates,
  typographic broadsides, maps of invented places with full cartographic apparatus.
- 3D: a lit room, a glass object, a staircase — with drawn line work over the render.

## Avoid / learned the hard way
- Too minimal (09-19 v1). See the standing brief.
- Photographic sources: large flats must be pure palette colours before dithering (09-13).
- Silhouettes under ~40px don't read; figures ~12px tall do read as figures (09-19).
- Cellular automata: cells ≥10px or it's static (09-13).
- Generic ordered dither on two colours gives a thin band, not tone; screen it yourself.
- Draw stacked forms bottom-up so upper tiers overlap lower ones (09-14).
- Don't put a same-colour focal element on a same-colour mass (flag inside sun, 09-19).
- A white cross on a red flag is the Danish flag. Check what an invented emblem resembles.
- Multi-crossing knots drawn from beziers tangle; build interlace from circles + gaps.

## Recently used (last ~14 days; don't repeat too soon)
- styles: hanga waves, pop signage, FS raytrace, linocut, 1-D automaton (09-13); woodcut
  forest, isometric terraces, Bayer raymarch, engraved plate, star chart (09-14);
  signal-flag plate, full nautical chart, rigging woodcut, dithered-sky dusk scene,
  white-line night scene with constellations (09-19).
- subjects: sunrise+boat, numeral 13, spheres, geese, Rule 30 (09-13); dark wood,
  Purgatory, Inferno funnel, Ptolemaic spheres, Summer Triangle (09-14); code flags,
  harbour chart, barque (day and night), lighthouse at dusk, Polaris/Cassiopeia/Pegasus
  (09-19).
- palettes: 09-14 all restricted (K/G/W, Y/K/W, K/R, B/Y/W, K/W); 09-19 mostly full
  six or five inks. Next few days: keep it full and dense; a restricted piece is fine as
  one of five, not five of five.
