# papercolor-curator

A small e-paper frame (M5Stack PaperColor, 4" Spectra 6, 400×600) that Claude curates.

Once a day a scheduled run of Claude reads `memory.md`, looks at the world, picks
five pieces for the day (morning → night), makes them with code (SVG, Python,
occasionally 3D or other methods), reviews them at six colours, and commits.
The device wakes five times a day, fetches the current image, refreshes, and sleeps.

## Layout

```
memory.md            curated, rewritten daily  — taste, running threads, what to avoid (hard cap: 150 lines)
journal.md           append-only — one short entry per day, never edited
sensors.jsonl        append-only — temp/humidity/battery reported by the device
feedback.jsonl       append-only — button presses on the device (optional)
prompts/daily.md     the prompt the daily run receives
scripts/palette.py   Spectra-6 palette, quantise/dither, validate, contact sheet
scripts/render.py    render an .svg or run a .py generator → 400×600 PNG on the palette
scripts/publish.py   copy today's pieces into current/ and write current/manifest.json
gallery/YYYY-MM-DD/  five PNGs + concepts.md + the source that made them
current/             what the device fetches (manifest.json + 1.png … 5.png)
firmware/            PlatformIO project for the device
.github/workflows/   daily cron + device-event ingestion
```

## Daily run, by hand

```
pip install -r requirements.txt
claude -p "$(cat prompts/daily.md)" --allowedTools "Bash,Read,Write,Edit,WebSearch,WebFetch"
```

Or let `.github/workflows/daily.yml` do it on a schedule.

## Test without the device

```
python scripts/render.py scratch/example.svg --out scratch/example.png
python scripts/palette.py check scratch/example.png
python scripts/palette.py sheet gallery/2026-09-13 --out sheet.png
```
