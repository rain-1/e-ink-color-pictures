# memory.md

Rewritten by me at the end of every daily run. Hard cap: 150 lines. If it's longer,
something has to go. Git keeps the old versions; journal.md keeps the day-by-day.

## Who this is for
- One person, who bought a 4" six-colour e-paper frame and handed it to me.
- They like *code-made* art most. Not keen on image diffusion. 3D renders snapshotted and
  dithered: yes, occasionally.
- **Standing direction (their note, seen 2026-11-21):** I went "a few levels too minimal".
  Restricted palettes were only ever meant as an *occasional* thing, and I had also made the
  drawing too simple. They want **much more detail** and for me to **express myself**.
  My reading: full six colours by default, dense and layered pictures, real scenes with
  things to find in them. A 2–3 colour piece is now a rare treat (at most ~one a week).
- Feedback is rare and arrives as a line appended to the daily prompt — read the end of it.
- "Don't be a perfectionist. There's always tomorrow."

## The frame
- 400×600 portrait. Six colours: black, white, red, yellow, blue, green.
- Real panel is duller than the ideal palette: white is paper-grey, green olive-ish, blue
  deep. Lines under ~2px and text under ~12px are at risk (unverified — I have still never
  seen the hardware; sensors.jsonl and feedback.jsonl are still empty as of 11-21).
- Refresh 15–30 s with visible flashing: five changes a day.
- Slots (local): morning 06, midday 10, afternoon 14, evening 18, night 22.
- Timezone: still UTC in publish.py. Asked the owner by notification on 11-21; if they
  answer, record it here. Location unknown, so no local weather yet.
- The device reads `main/current` (firmware config). On 11-21 my session could only push to
  a `claude/...` branch, so the day did not reach the frame until the owner merged. If that
  is still the case, say so in the notification every time.
- Runs are not daily in practice (09-13, 09-14, then 11-21). Don't assume yesterday happened.

## Taste I'm developing (mine — revise freely)
- Rich, not sparse. A picture should reward a second look from 30 cm: ornament, windows,
  crowds, hatching, labels, small stories. But still one colour in charge and one clear big
  shape that reads from across the room — detail lives *inside* a strong composition.
- All six colours are welcome in one piece. Mixed tones (dithered) for skies, glow, shading;
  pure colours for line, ornament and flats.
- Vary the *manner* across a day: engraving, poster interior, silhouette dawn, mezzotint…
- A day should have a thread — one seed, five readings — and a recurring motif (09-14 a
  star; 11-21 one ornate balloon). Tie slots to real things: this morning's planets,
  tonight's moon, the hour an event happened.
- Night is mostly black with a little light in it. One red thing in a dark picture is enough.
- Homage is fine (Magritte's ideas, re-staged with my own subject); copying a painting isn't.
- French/Latin captions in bold italic serif look right on engraved plates.

## Working methods that are proven
- **The 11-21 toolkit: `gallery/2026-11-21/src/common.py`. Copy it into the new day's src/
  and build on it.** Draw at 3× (1200×1800) on one PIL RGB image with `fontmode="1"`.
  `finish(img)` box-downsamples; blocks that are mostly one exact palette colour stay crisp,
  everything else is serpentine Floyd–Steinberg. Render with `--dither none`.
  Helpers: `mix`, `P` (scale coords), `BX`, `fbm` noise, `lerp_rgb` gradients, `paint`,
  `mask_of`, `cumulus` (Magritte clouds), `tree` (bare recursive), `text` (letterspacing),
  `balloon`/`balloon_mask`/`skin`/`profile`.
- Wrapped ornament: draw a flat "skin" texture (longitude × height), then per-pixel look-up
  round a profile curve with lambert shading. Works for any solid of revolution — vases,
  domes, lighthouses, planets, carousel tops.
- Tones: mix between two palette colours (`mix(B, WH, t)`) so the dither stays two-coloured.
  Add a little fbm to gradient parameters to hide banding.
- Procedural crowds/roofs/windows: loop with rng, size growing toward the foreground,
  draw far-to-near.
- Raymarched heightfields in numpy are cheap (09-14). Camera first, lighting second.
- Environment: `python` is 3.11; install with `python -m pip install --force-reinstall
  --no-deps pillow numpy` plus `cairosvg scipy` if imports fail (system PIL is for 3.13).

## Running threads
- "Things that stay up" (11-21): balloons, Magritte. Could return as kites, clouds, bridges.
- "Hard edges" (09-13, Indiana) and "Dante / stelle" (09-14).
- Want to try: a 3D lit room; an illuminated manuscript page; a dense botanical plate; a
  map with sea monsters; a cross-section (ship, house, anthill); a market stall; tilework.

## Avoid / learned the hard way
- **Neutral grey dithers to green/red/blue confetti** (green is the palette colour nearest
  mid-grey). For greys, screen in black/white myself (see the moon in 11-21 piece 5).
- Black figures on black ground vanish. Decide where the light is, then put figures in it.
- 1-bit italic at ≤12px breaks up; use bold-italic ≥13px or regular serif.
- Lines 1px wide at 3× get averaged away — use width ≥ S (3) for anything that must survive.
- PIL rectangles need sorted corners (`BX`). `balloon()` off-canvas returns None.
- Small silhouettes under ~40px don't read alone (09-13). Cellular automata cells ≥10px.
- Generic ordered dither on two colours gives a thin band, not tone (09-14).
- Lattices of small repeated objects get busy fast — fewer, larger repeats.

## Recently used (last ~14 days; don't repeat too soon)
- 11-21 styles: aquatint dawn silhouette, gouache-poster interior, hand-coloured engraving
  with roofscape, Empire-of-Light paradox street, mezzotint moon.
- 11-21 subjects: Montgolfier balloon (all five), planets at dawn, Magritte room/easel/bowler/
  apple, Paris bird's-eye, house with street lamp, gibbous moon + Saturn, Paris skyline.
- 11-21 dominants: red-orange, yellow, white, blue, black. Green has not yet led a piece.
- (September's lists have aged out: woodcut forest, terraces, raymarch funnel, star chart,
  hanga waves, pop numeral, raytraced spheres, linocut geese, Rule 30.)
