# memory.md

Rewritten by me at the end of every daily run. Hard cap: 150 lines. If it's longer,
something has to go. Git keeps the old versions; journal.md keeps the day-by-day.

## Who this is for
- One person, who bought a 4" six-colour e-paper frame and handed it to me.
- They say they love everything I make. Feedback is rare, so take it seriously when it comes.
- They like *code-made* art most. Not keen on image diffusion. 3D renders dithered: welcome
  occasionally.
- **10-11 correction, standing:** "you've gone a few levels too minimal". Restricted
  palettes were only ever an *occasional* suggestion. They want **much more detail**, so I
  should express myself fully. Default = all six colours, dense, drawn, rich. A restricted
  palette is now the exception (≤1 piece a day, and only when the idea demands it).
- "Don't be a perfectionist. There's always tomorrow."

## The frame
- 400×600 portrait. Six colours: black, white, red, yellow, blue, green.
- Real panel is duller: white is paper-grey, green olive-ish, blue deep. Lines under ~2px
  and text under ~11px are at risk (still unverified — no hardware feedback yet).
- Refresh 15–30 s with visible flashing: five changes a day.
- Slots (local): morning 06, midday 10, afternoon 14, evening 18, night 22.
- Timezone: still UTC in publish.py. Ask the owner.

## Taste (mine — revise freely)
- Richness first: scenes with many parts — architecture, figures, foliage, water,
  reflections, patterned cloth, labels. A piece should reward a second and third look.
- Still: one colour in charge of the composition (gold screen, blue dusk, black night),
  even when all six appear.
- Print-shop idioms still guide me: ukiyo-e, shin-hanga, herbarium/botanical plates,
  emaki, posters, engraving. Now with full colour and density.
- A day has a thread (one seed, five readings) and a small recurring motif (09-14 a star,
  10-11 a maple leaf in every piece).
- Tiny figures give scale and story; three on a bridge worked at 2× canvas.
- Night: mostly black, lit by something in the scene (fire, windows, moon).

## Working methods that are proven
- Generators draw on an **800×1200 canvas (2×)** with PIL, write to $OUT_RAW; render.py
  fits and quantises. Use `--dither fs` for full-colour pieces.
- A per-day `src/lib.py` of helpers (leaf shapes, vgrad, value_noise, colour constants)
  makes dense work cheap. Copy the 10-11 lib.py as a starting point.
  It has: maple_leaf(cx,cy,size,angle,lobes,...), maple_veins, draw_maple, vgrad,
  value_noise, fonts (DejaVu/Liberation; there are NO CJK fonts installed).
- Colour strategy with FS: flats in *pure* palette colours; gradients and intended blends
  (ORANGE 235,120,18; SKY 130,160,220; dusk blues) dither nicely. AVOID muddy darks/greys
  (e.g. 60,40,10 or 70,60,60): they become red/green/blue confetti. Use pure K plus
  coloured lines instead.
- Reflections: flip the band above the waterline in numpy, roll rows by a sine, darken
  toward deep blue, then add ripple strokes and broken vertical streaks for lights.
- Masked pattern fills (paste a pattern image through a polygon mask) give textiles.
- Raymarched heightfields in numpy are cheap (~30 s). Camera first, lighting second.
- `--palette a,b,c` exists for the occasional restricted piece; do the Bayer screen in the
  generator in that case.

## Running threads
- Done: "hard edges" (09-13), Dante/stelle (09-14), momijigari (10-11).
- Ideas: a busy market or harbour scene; an illustrated map; a cutaway house / ship;
  a 3D lit interior; a dense botanical or insect plate; a night city with lit windows;
  a full-moon piece around 10-26 (Hunter's Moon).

## Avoid / learned the hard way
- Over-minimalism (owner said so). Don't let a piece be a single shape and a field.
- Photographic sources: large flats must be pure palette colours before dithering.
- Silhouettes under ~40px (at 1×) don't read. Double them.
- Cellular automata / pixel patterns: cells ≥10px.
- Draw order: stacked forms bottom-up; hair and capes *behind* bodies.
- Random recursive branches can hook oddly; reseed the RNG just before drawing them.
- Leaves/labels in a grid: fix label rows first, then fit leaves above them.

## Recently used (last ~14 days; don't repeat too soon)
- 10-11 styles: ukiyo-e landscape, herbarium plate, bonsai still-life before a gold screen,
  shin-hanga dusk with reflections, torchlit Noh figure.
- 10-11 subjects: maple gorge+pagoda+bridge, nine leaves, Deshojo bonsai, Heian dragon
  boat, hannya demon. Motif: maple leaf. Lots of red/orange: tomorrow lean on another hue.
- Older (09-13/14, now outside the window): hanga waves, pop numeral, raytraced spheres,
  geese, Rule 30, Dante set.
