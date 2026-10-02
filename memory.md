# memory.md

Rewritten by me at the end of every daily run. Hard cap: 150 lines. If it's longer,
something has to go. Git keeps the old versions; journal.md keeps the day-by-day.

## Who this is for
- One person, who bought a 4" six-colour e-paper frame and handed it to me.
- They say they love everything I make. Feedback is rare; I am my own critic.
- They like *code-made* art most. Not keen on image diffusion. 3D renders snapshotted
  and dithered: yes, occasionally.
- **10-02 correction, standing:** I'd gone "a few levels too minimal". Restricted
  palettes are an *occasional* device, not the default. They want MUCH more detail:
  full scenes, many drawn elements, all six colours as the norm. Express myself.
- They'll wire the temperature/humidity sensor up so I can feel the room (still empty).
- "Don't be a perfectionist. There's always tomorrow."

## The frame
- 400×600 portrait. Six colours: black, white, red, yellow, blue, green.
- Real panel is duller than the ideal palette: white is paper-grey, green olive-ish, blue
  deep. Lines under ~2px and text under ~10px are at risk (unverified — no hardware yet).
- Refresh 15–30 s with visible flashing: five changes a day.
- Slots (local): morning 06, midday 10, afternoon 14, evening 18, night 22.
- Timezone: still UTC in publish.py. Ask the owner.

## Taste I'm developing (mine — revise freely)
- Default: a full scene, full palette, dense with *drawn* detail — windows, rivets,
  ticks, fabric prints, craters, leaves, tiny figures, labels. Then make one colour
  lead and keep a clear big shape so it still reads at four inches.
- Treat the palette as a colour print shop: Sunday comics (Ben-Day dots), deco posters,
  screenprint, woodblock, quilts, stained glass, technical plates, instrument panels.
- Restricted palette (2–3 inks) maybe one piece in five, when it serves the idea.
- Night should be mostly black with a little light in it (≥ ~70% black). Instruments,
  lit windows, stars work well.
- A day should have a thread — one seed, five readings — and a recurring motif (09-14: a
  star; 10-02: a red rocket) gives it a spine.
- Two birthdays on one date can be braided (10-02: Raymond + Marston). Good seed source.
- Noise is not detail. Calico/random speckle is the edge of that line.

## Working methods that are proven
- **`gallery/2026-10-02/src/ink.py`** — reuse it (copy into the day's src/). 1x canvas,
  no anti-aliasing, bool masks via PIL 1-bit drawing; `ramp` (multi-stop Bayer gradient),
  `screen`, `benday` (dots, variable radius), `hatch`, `text` (1-bit, with outline).
  Output is palette-pure → `--dither none`. Each piece renders in ~1 s.
- For PIL text on RGB images set `draw.fontmode = "1"` or it anti-aliases off-palette.
- Recursive fronds/L-systems: polyline per branch, width ≥2 at leaves, ≥3–4 at stems.
- Comic page: paint each panel on a full canvas, copy its rect, then 3px border.
- Raymarched heightfields in numpy are cheap (≈30 s, 220 steps). Camera first,
  lighting second, fog last. Floyd–Steinberg only for a photographic feel.
- `--palette a,b,c` on render.py restricts quantisation (for the occasional restricted piece).

## Readability checks that keep catching things
- Black figures on black buildings vanish → give them a 2px coloured halo/rim.
- Dark linework over hatched ground vanishes → thicken + coloured halo, or lighten ground.
- Text near panel/canvas edges gets clipped → compute boxes against the edge first.
- Silhouettes under ~40px only work as detail, not as the subject.
- Cellular automata cells ≥10px. Large flats must be pure palette before any dithering.
- Draw stacked forms bottom-up so upper tiers overlap lower ones.

## Running threads
- Retro space opera (10-02): Mongo, rockets, deco cities — could return as a serial
  ("NEXT WEEK: THE CRYSTAL CAVES!" was promised on the 10-02 Sunday page).
- Quilts as a format: blocks + printed fabrics + stitching; lots of room left
  (Gee's Bend, crazy quilts, sampler quilts).
- Dante / stelle (09-14), hard edges (09-13).
- 3D: a lit room, a glass object, a staircase, a single chair — things with shadows.
- Charts and plates: star charts, tide tables, technical drawings, instrument panels.
- Sky facts: Draconids peak 9 Oct (new moon 10 Oct — dark), Orionids 21–22 Oct,
  full moon 26 Oct.

## Recently used (last ~14 days; don't repeat too soon)
- 10-02 styles: deco poster with Bayer sky, Sunday comic page, liberated quilt,
  engraved/hatched dusk jungle, cockpit instrument panel.
- 10-02 subjects: rocket launch city, ringed planet, ZZAP burst, giant fungi, quilt
  medallion, cratered moon, fern fronds, dials/radar.
- 09-14: woodcut forest, isometric Purgatory, raymarched Inferno, engraved Ptolemaic
  spheres, star chart (all restricted palettes).
- 09-13: hanga waves, pop "13" sign, raytraced spheres, linocut geese, Rule 30.
