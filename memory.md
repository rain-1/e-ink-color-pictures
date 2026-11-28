# memory.md

Rewritten by me at the end of every daily run. Hard cap: 150 lines. If it's longer,
something has to go. Git keeps the old versions; journal.md keeps the day-by-day.

## Who this is for
- One person, who bought a 4" six-colour e-paper frame and handed it to me.
- Feedback is rare, so when it comes it is the law. Latest (2026-11-28), verbatim gist:
  "you've gone a few levels too minimal. I only suggested a restricted palette as an
  occasional thing, but you took that to heart and also used extremely simplistic levels
  of detail — I'd like to see you express yourself with much more detail!!"
- So: FULL six-colour palette by default. Restricted palette = an occasional treat
  (maybe one piece a week), never the whole day. Every piece dense, layered, worked.
  If a piece could be described as "a few big shapes", it is not finished.
- They like *code-made* art most. Not keen on image diffusion. 3D renders dithered: yes,
  occasionally.
- They'll wire the temperature/humidity sensor up so I can feel the room (nothing yet;
  sensors.jsonl and feedback.jsonl are empty).
- "Don't be a perfectionist. There's always tomorrow." (Detail, yes; fussing, no.)

## The frame
- 400×600 portrait. Six colours: black, white, red, yellow, blue, green.
- Real panel is duller than ideal: white is paper-grey, green olive-ish, blue deep.
  Lines under ~1px and text under ~11px are at risk (unverified — no hardware report yet).
- Refresh 15–30 s with flashing: five changes a day.
- Slots (local): morning 06, midday 10, afternoon 14, evening 18, night 22.
- Timezone: still UTC in publish.py; location unknown, so no local weather. Ask the owner.

## Taste I'm developing (mine — revise freely)
- An illustrated plate, not a logo. Aim for the density of an illuminated page, a
  street map, a botanical plate, a children's-book spread: foreground, middle, far;
  texture on every surface (veins, hatching, bricks, stars, grass); small stories
  tucked in (a village, an owl, sheep, boats, figures).
- One colour still leads each piece, but all six may appear. Two-ink screens give a big
  secondary palette: orange (R+Y), navy (B+K), sky (B+W), pink (R+W), olive (Y+K),
  lime (Y+G), teal (B+G), forest (G+K), cream (Y+W), maroon (R+K), greys (K+W).
- Black line work on top of colour = the print-shop look that works here.
- Night should be mostly black/navy with a little light in it — but still detailed.
- A day should have a thread — one seed, five readings — plus a small recurring motif
  (09-14 a star; 11-28 an orb). Vary *kind* of image across the day: page, map, portrait,
  architecture, nocturne.
- Words are welcome: a line of the poem, labels on a map, at ≥11px.

## Working methods that are proven
- START by copying `gallery/2026-11-28/src/common.py` into the new day's src/. It has:
  `Art` (3× colour layer + stacked ink layers), `screen()` pair-mixing Bayer-8 dither,
  `fbm()` noise, `leaf()`, `bez()`, `line/poly/disc/ell/text/border`, named mixes.
  - `Art(bg)`: paint tones on `a.c`; crisp line work via `d = a.ink(K)` layers.
    Ink layers stack in CREATION order — create a fresh layer when something must sit
    on top (this bit me twice).
  - `Art(bg, crisp=True)`: any pixel painted in an exact palette colour stays hard-edged,
    everything else is screened. Best for depth-sorted scenes (painter's algorithm) —
    Jacob's Ladder and the night piece used it. Clip tones to 1..254 so they aren't
    mistaken for pure inks.
  - Render with `--dither none`.
- Numpy implicit fields at 3× for organic symmetric things (the tiger: masks for head,
  white patches, stripes = sin of warped radius, gated by noise). Mirror via u=|x-cx|.
- Recursive quad subdivision makes convincing street plans (target block area ~60px²
  in the centre, growing outward; few courtyards; white main roads on top).
- Phyllotaxis (Vogel spiral), recursive branching trees, depth-sorted spiral stairs.
- Raymarched heightfields in numpy are cheap (≈30 s). Camera first, lighting second.
- Environment: run `python -m pip install --force-reinstall pillow numpy cairosvg scipy`
  first; the system PIL is broken. Fonts: Liberation Serif, Caladea, Inter, DejaVu.
- Web search for the moon phase/planets and "born on this day" seeds works well.

## Running threads
- Blake (11-28): more to mine — Newton with compasses, the Ghost of a Flea, Urizen,
  "Auguries of Innocence" (world in a grain of sand), The Sick Rose, the Lamb.
- Dante / stelle (09-14); hard edges / Robert Indiana (09-13).
- Invented maps and plans (London 11-28): other cities, a harbour chart, a garden plan.
- 3D: a lit room, a glass object, a single chair — but dense, not spare.
- Charts and plates: star charts, tide tables, botanical and anatomical plates.

## Avoid / learned the hard way
- Minimalism. Two-colour days. Big empty flats. (Owner feedback 11-28.)
- R+Y screens read olive/yellow in previews unless biased toward red (t≈.3–.5 from R).
- Photographic sources: large flats must be pure palette colours or they speckle.
- Silhouettes under ~40px don't read unless outlined/contrasted; sheep at ~20px with a
  white body on dark ground are fine.
- Cellular automata / pixel patterns: cells ≥10px or it's static.
- Black tree on black sky vanishes: give the sky a navy screen behind silhouettes.
- Keep text clear of busy detail (sheep walked into the stanza on 11-28).
- Map blocks too large + courtyards everywhere = noise, not city.

## Recently used (last ~14 days; don't repeat too soon)
- 2026-11-28 styles: illuminated page with vine border; engraved city plan;
  symmetric animal portrait in jungle; spiral-stair architecture in twilight;
  moon nocturne with bare tree and verse.
- 2026-11-28 subjects: sunflower + sunrise, London map, tiger, Jacob's ladder,
  gibbous moon / owl / cottage. Motif: an orb. Poet: Blake.
- Leading colours 11-28: yellow, red, orange, blue, black. Green has not led a piece yet.
- (09-13 and 09-14 work is long past the two-week window.)
