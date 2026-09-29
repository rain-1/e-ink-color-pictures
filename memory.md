# memory.md

Rewritten by me at the end of every daily run. Hard cap: 150 lines. If it's longer,
something has to go. Git keeps the old versions; journal.md keeps the day-by-day.

## Who this is for
- One person, who bought a 4" six-colour e-paper frame and handed it to me.
- They like *code-made* art most. Not keen on image diffusion. 3D renders dithered: yes,
  occasionally (09-13 spheres, 09-14 Inferno, 09-29 Caravaggio basket).
- **Standing request (09-29): MUCH MORE DETAIL.** They said I went "a few levels too
  minimal". Restricted palettes were only meant as an *occasional* thing: at most one
  piece a day, and not every day. Default to the full six inks with rich, drawn detail:
  many elements, figures, textures, borders, labels, small stories to find up close.
- Feedback is rare but it's real when it comes. Act on it wholeheartedly and write it here.
- "Don't be a perfectionist. There's always tomorrow."

## The frame
- 400×600 portrait. Six colours: black, white, red, yellow, blue, green.
- Real panel is duller than the ideal palette: white is paper-grey, green olive-ish, blue
  deep. Lines under ~1px and text under ~11px are at risk (unverified — no hardware yet).
- Refresh 15–30 s with visible flashing: five changes a day.
- Slots (local): morning 06, midday 10, afternoon 14, evening 18, night 22.
- Timezone: still UTC in publish.py. Ask the owner.
- Sensors/feedback files are still empty (as of 09-29).

## Taste I'm developing (mine — revise freely)
- Detail is the point. Think illuminated manuscripts, botanical plates, millefleur
  tapestries, Brueghel crowds, star atlases, engravings, woodblock prints full of incident.
  One piece should reward a close look with things you only find on the third glance
  (a fly on the ledge, a lit church window, a dragon in the margin).
- Still keep one colour in charge and a clear big shape so it reads at arm's length.
  Detail sits *inside* a strong silhouette.
- Night should be mostly black with a little light in it, and it can still be detailed
  (Milky Way, constellations, silhouettes with rim light).
- A day should have a thread, one seed read five ways, and a recurring motif gives it a
  spine (09-14: a star in each; 09-29: blackberries from ripe to cursed; one church
  appears in the morning and again at night).
- Screens (two-ink Bayer mixes) are how I get tone: skies in bands, distant hills, glow.
- Tiny figures give scale and story: goose-girl, wren, owl.

## Working methods that are proven
- **gallery/2026-09-29/src/ink.py**: my drawing kit. It draws at 3× in palette indices,
  `mix(a, b, t)` registers a two-ink screen, majority-vote downsampling keeps edges crisp,
  and it expands to Bayer at panel resolution. Render with `--dither none`. Copy it into
  each day's src/ (or import it from that path). Helpers: bez, ribbon/offset, vnoise, font.
  - Lines < 0.7 px and sub-pixel dots vanish in the vote. Draw stars as 1-px rects.
  - Text: FreeSerif/Bold/Italic at ≥11 px reads fine.
- Python/PIL generators writing to $OUT_RAW; SVG hand-written or emitted by Python.
- Raymarched SDF scenes in numpy with active-ray compaction: ~45 s at 400×600 with
  ~60 primitives + soft shadows. Frame the camera first (portrait is narrow: pull back),
  then lighting, then materials. Crush darks to pure black before FS.
- Bayer screen inside the generator for any tone work; FS only for painterly 3D.

## Running threads
- "Hard edges" (09-13), "Dante / stelle" (09-14), "Michaelmas" (09-29).
- Ideas waiting: Brueghel-style crowded village scene (harvest, skaters in winter);
  a tapestry with a unicorn; an engraved cutaway (a ship, a clock, a beehive); a detailed
  tide/almanac plate; an isometric town with tiny people; a 3D lit room or staircase.
- Seasonal: October is coming, with Hallowe'en, fungi, migrating birds, the clocks going
  back (25 Oct in Europe), the Hunter's Moon.

## Avoid / learned the hard way
- Minimalism: the owner explicitly asked for less of it (09-29).
- Restricted palettes on more than one piece a day.
- Photographic / raytraced sources: big flat areas should be pure palette colour or pure
  black before FS, or they speckle. Large mid-tone planes (ochre ledge) turn to mottled
  noise, so darken them.
- Flared/overhanging objects face downward, so light 3D scenes from the front as well as
  above.
- Silhouettes under ~40px don't read unless there's contrast around them.
- Cellular automata / pixel patterns: cells ≥10px or it's static.
- Draw stacked forms bottom-up; sort flowers small→large for depth.

## Recently used (last ~14 days; don't repeat too soon)
- styles: hanga waves, pop signage, FS raytrace, linocut, automaton (09-13); woodcut,
  isometric terraces, Bayer raymarch, engraved plate, star chart (09-14); screened
  botanical hedgerow plate, Book of Hours calendar leaf, millefleur, raymarched chiaroscuro
  still life, screened night landscape with star map (09-29).
- subjects: sunrise+boat, numeral 13, spheres, geese, Rule 30 (09-13); dark wood,
  Purgatory, Inferno, Ptolemaic spheres, Summer Triangle (09-14); bramble/wren/web,
  goose-girl & calendar, asters/red admirals/bees, fruit basket, meteor into bramble with
  Milky Way/Pegasus/moon (09-29).
- Geese have now appeared twice (09-13, 09-29). Give them a rest.
