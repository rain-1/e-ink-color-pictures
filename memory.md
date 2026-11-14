# memory.md

Rewritten by me at the end of every daily run. Hard cap: 150 lines. If it's longer,
something has to go. Git keeps the old versions; journal.md keeps the day-by-day.

## Who this is for
- One person, who bought a 4" six-colour e-paper frame and handed it to me.
- Feedback is rare, so take it seriously when it comes. Latest (2026-11-14), verbatim gist:
  "you've gone a few levels too minimal. I only suggested a restricted palette as an
  occasional thing, but you took that to heart and also used extremely simplistic levels of
  detail — I'd like to see you express yourself with much more detail!!"
  => DEFAULT IS NOW: all six inks available, dense, richly detailed, expressive pieces.
  A 2–3 colour piece is an occasional choice (at most ~1 in a day, not every day), and even
  then it must be intricate. Never mistake "few shapes" for good design here.
- They like *code-made* art most. Not keen on image diffusion. 3D renders dithered: yes,
  occasionally (had two in September).
- They'll wire the temperature/humidity sensor up so I can feel the room (sensors.jsonl and
  feedback.jsonl were still empty on 11-14).
- "Don't be a perfectionist. There's always tomorrow."

## The frame
- 400×600 portrait. Six colours: black, white, red, yellow, blue, green.
- Real panel is duller than the ideal palette: white is paper-grey, green olive-ish, blue
  deep. Lines under ~2px and text under ~12px are at risk (unverified — no hardware report
  yet). I now use 1px line freely for texture, but never for the thing that carries the image.
- Refresh 15–30 s with visible flashing: five changes a day.
- Slots (local): morning 06, midday 10, afternoon 14, evening 18, night 22.
- Timezone: still UTC in publish.py. Asked the owner on 11-14 via notification; no answer yet.

## Taste I'm developing (mine — revise freely)
- The panel can't mix colour, so mix it optically: pure inks side by side as strokes,
  tesserae, hatching, stipple. That is where richness comes from on six colours.
- Detail should be *drawn and countable*: blades, petals, voussoirs, tiles, veins, rigging.
  Thousands of meaningful marks, organised by a clear big composition. Noise is not detail.
- Still want one colour in charge and a strong silhouette so it reads at four inches —
  detail lives inside a simple big structure (11-14: each piece read fine on the sheet).
- Night should be mostly black (≈2/3) with a little light in it.
- A day should have a thread — one seed, five readings — and a small recurring motif
  (09-14 a star; 11-14 a disc of light) gives the day a spine.
- Vary *technique* across the five as well as subject.
- Tiny figures give scale and story; draw them ≥40px and on top of surrounding texture.

## Working methods that are proven
- Run everything with `python3.13` (plain `python` is 3.11 without Pillow). cairosvg may
  need `python3.13 -m pip install cairosvg`. No scipy; numpy + PIL only.
- Python/PIL generators writing to $OUT_RAW, emitting only palette colours, rendered with
  `--dither none`. A shared `src/common.py` per day (palette, value noise/fbm, Bayer, mask,
  weighted `pick`) saves time — copy 11-14's.
- "Weight field" approach: build six H×W weight arrays (K,W,R,Y,B,G) from noise + masks, then
  sample a pure ink per mark (stroke, tile). Used for strokes (11-14 #1) and mosaic (#4).
- Stroke painting: 3 layers (4px, 2px, 1px wide), then re-draw key shapes crisply on top.
- Voronoi mosaic: seeds laid along flow lines (rings, courses, rows); nearest/second-nearest
  by chunked brute force (≈6 s); grout where the two distances are within ~1px; one pass
  per region mask so silhouettes stay sharp.
- Depth-sorted mark lists (grass, flowers, figures) for meadows/crowds: 15k marks ≈ 1 s.
- Architecture: draw separate greyscale layers (depth, line, accents, sky) at 2x, box-
  downsample the *masks*, then compose colour + hatching at 1x.
- Raymarched heightfields in numpy are cheap (≈30 s). Camera first, lighting second.
- For 2-colour tone, do the Bayer screen inside the generator; generic ordered dither is weak.

## Running threads
- Painters' series as a day-structure (Monet 11-14). Could do: Hokusai's Fuji views,
  Hiroshige stations, Turner, Hockney's arrival of spring, Klee, Hilma af Klint.
- "Hard edges" (09-13, Indiana) and "Dante / stelle" (09-14). Both could return, denser.
- Charts and plates as art: star charts, tide tables, botanical plates, maps, cross-sections.
- Untried techniques worth a day: isometric city, L-system botany, stained-glass leading,
  woven/textile patterns, a dense 3D interior, marbling/flow fields, typeset poem + ornament.

## Avoid / learned the hard way
- Never hatch or screen at 2x and downsample: blue-on-yellow averages to green, black-on-
  white to grey→random ink. Flat shapes only at 2x; all fine pattern at 1x (11-14).
- Shade thresholds: keep most of a surface in its dominant ink; first cathedral pass went
  nearly solid blue (11-14). Check the coverage % that palette.py check prints.
- Mosaic: no black tiles with black grout; mid-tone mixes of blue+black kill silhouettes.
- Features inside stroke/dither fields vanish unless re-drawn solid afterwards (11-14).
- Photographic sources: large flats must be pure palette colours before dithering (09-13).
- Cellular automata / pixel patterns: cells ≥10px or it's static (09-13).
- Draw stacked forms bottom-up so upper tiers overlap lower ones (09-14).
- Too minimal / too few colours — the owner said so. Don't drift back.

## Recently used (last ~14 days; don't repeat too soon)
- 2026-11-14 styles: broken-stroke painting, blade-by-blade drawn meadow, hatched
  architectural elevation, Voronoi mosaic, flat-ink nocturne with fine line.
- 2026-11-14 subjects: Le Havre sunrise, poppy field + parasol, Rouen Cathedral front,
  Houses of Parliament sunset, water-lily pond + Japanese bridge. Thread: Monet.
- Dominant inks 11-14: blue, green, blue/yellow, red/blue, black. Blue was heavy across
  the day — lean on red, yellow, green or white-ground pieces next.
- (September work is outside the window: Indiana hard edges 09-13, Dante 09-14.)
