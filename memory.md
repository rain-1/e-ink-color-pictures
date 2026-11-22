# memory.md

Rewritten by me at the end of every daily run. Hard cap: 150 lines. If it's longer,
something has to go. Git keeps the old versions; journal.md keeps the day-by-day.

## Who this is for
- One person, who bought a 4" six-colour e-paper frame and handed it to me.
- Feedback is rare, so when it comes it outweighs my own theories.
- **11-22, their words: I'd "gone a few levels too minimal". Restricted palettes were only
  meant as an occasional thing; I over-applied that and also made the drawing simplistic.
  They want me to "express myself with much more detail!!"** This is the standing brief:
  rich, dense, fully drawn pictures, all six colours welcome. A 2–3 colour piece is now an
  occasional change of pace (at most one in a day, not every day), and even then detailed.
- They like *code-made* art most. Not keen on image diffusion. 3D renders dithered: fine
  occasionally (had two in September).
- "Don't be a perfectionist. There's always tomorrow."

## The frame
- 400×600 portrait. Six colours: black, white, red, yellow, blue, green.
- Real panel is duller than the ideal palette: white is paper-grey, green olive-ish, blue
  deep. (Still unverified by me — sensors.jsonl and feedback.jsonl are empty.)
- Refresh 15–30 s with flashing: five changes a day.
- Slots (local): morning 06, midday 10, afternoon 14, evening 18, night 22.
- Timezone: still UTC in publish.py — owner hasn't said. Firmware example suggests CET.
- The device reads `current/` on **main**. Scheduled cloud runs push to a `claude/…`
  branch; it needs merging to main to reach the frame. Flag this to the owner when it applies.

## Taste (mine — revised 11-22)
- Detail is the point. Aim for pictures you can keep finding things in from 30 cm:
  hundreds of drawn elements, each with its own inner detail (a house gets tiles, sashes,
  a chimney pot, smoke; a pebble gets an outline and a highlight).
- Structure keeps density legible: one colour in charge, clear big zones (sky / sea /
  ground), then fill the zones. Dense ≠ noisy. Random multi-colour fill is confetti —
  limit a population to 2 main colours + rare accents.
- Use all six colours when the subject wants them. Print-shop idioms still serve well:
  colour woodcut, naive townscape, stained glass, engraving, charts and plates.
- A day wants a thread and a small story across the five (11-22: a boat leaves the beach,
  is seen in the storm, is missing at night). Re-running one generator in different light
  (dawn/night) makes a good bookend.
- Real-world anchors please me: tonight's actual moon phase and planets, the actual weekday.
- Tiny text, names on boats, signs, labels: yes — they reward a close look.
- Night should be mostly black with a little light in it; no more than two dark pieces a day.

## Working methods that are proven
- `gallery/2026-11-22/src/common.py`: class `D` draws with PIL at 3× in panel units
  (poly/line/ell/arc/pie/text, `bez`, `gull`), then `save()` reduces 3×3 blocks by majority
  vote → pure palette, no antialias fringes; render with `--dither none`. Copy it into each
  new day's src/. Lines ≥ ~0.45 units survive as 1px; text ≥ ~5.5 units stays legible.
- Painter's algorithm, back to front. Actors that sit *in* a layered field (boat among
  wave rows) must be drawn 2 rows later than the row they ride or they get buried.
- Populations: loop rows back→front, scale size with depth, jitter everything with a
  seeded `random.Random`.
- Engraved gradients: ruled lines whose thickness varies (sky), hatching that follows a
  form's own contour (waves, clouds). Stipple matting: blur a mask of the black lines,
  threshold with a 4×4 Bayer, apply only to R/B/G so white and yellow stay clean.
- Arbitrary clip shapes (arch): per-pixel `inside(x, y, inset)` function; insets give
  borders and mouldings for free. Slow-ish (~20 s) but fine.
- Older: `--palette a,b` on render.py for restricted work; do Bayer screens inside the
  generator; numpy raymarch ≈30 s (camera first, lighting second).
- Environment: `pip` and `python` are different interpreters in the cloud session. Use
  `python -m pip install numpy cairosvg` then `python -m pip install --force-reinstall
  --no-deps pillow`.

## Running threads
- Music (11-22). Could return: an orchestra seating plan drawn player by player, a
  score as landscape, instruments in cross-section, bell-ringing method diagrams.
- The Borough / the beach with LT 22 and LT 13 — a place I can revisit in other weather.
- Dante (09-14), hard edges / Indiana (09-13).
- Ideas not yet tried: a busy interior in 3D with shadows; a cutaway building; a
  detailed map of an invented island; a botanical plate; a market crowd; a clockwork.

## Avoid / learned the hard way
- Minimalism as a default (the owner's 11-22 correction).
- Five-colour random fills (confetti). Silhouettes under ~40px need doubling or outlines.
- Photographic sources: big flats must be pure palette before dithering or they speckle.
- Generic ordered dither on two colours gives a band, not tone.
- Thin lines of colour A over colour B at ≤0.4 units vanish in the majority reduction.
- Things placed behind a later-drawn layer disappear (11-22: the sparrow stave behind
  the top terrace; check overlaps on the render, not in the head).
- Green on blue is weak (lily stems in the window) — outline in white or yellow.

## Recently used (last ~14 days; don't repeat too soon)
- 11-22 styles: colour-woodcut seascape, naive townscape, stained glass, engraved storm
  sea, night re-light of the dawn scene.
- 11-22 subjects: shingle beach + fishing boats, hill town with church and quay,
  St Cecilia at the organ, lighthouse storm, moonlit beach. Seed: Britten / St Cecilia.
- (September entries have aged out: Dante plates, Indiana signage, spheres, geese, Rule 30.)
