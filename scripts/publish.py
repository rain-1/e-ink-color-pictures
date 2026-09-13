#!/usr/bin/env python3
"""Copy gallery/<day>/1..5.png into current/ and write current/manifest.json.

  publish.py gallery/2026-09-13 [--tz Europe/Amsterdam]

The device reads manifest.json, picks the slot whose start hour has passed, and
fetches that file. Slot hours are local time on the device (it syncs via NTP).
"""
import argparse, json, shutil, sys
from datetime import datetime, timezone
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from palette import check

SLOTS = [  # name, start hour (local)
    ("morning", 6), ("midday", 10), ("afternoon", 14), ("evening", 18), ("night", 22),
]

def main():
    p = argparse.ArgumentParser()
    p.add_argument("day_dir"); p.add_argument("--tz", default="UTC")
    a = p.parse_args()
    day = Path(a.day_dir)
    cur = Path("current"); cur.mkdir(exist_ok=True)
    concepts = {}
    cpath = day / "concepts.md"
    if cpath.exists():
        for line in cpath.read_text().splitlines():
            if line.startswith("## "):  # "## 1. Title"
                n, _, title = line[3:].partition(". ")
                concepts[n.strip()] = title.strip()
    entries = []
    for i, (name, hour) in enumerate(SLOTS, 1):
        src = day / f"{i}.png"
        if not src.exists():
            sys.exit(f"missing {src}")
        if check(src):
            sys.exit(f"{src} failed palette check — run render.py on it first")
        shutil.copy(src, cur / f"{i}.png")
        entries.append({"slot": i, "name": name, "start_hour": hour,
                        "file": f"{i}.png", "title": concepts.get(str(i), "")})
    manifest = {"day": day.name, "tz": a.tz,
                "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "slots": entries}
    (cur / "manifest.json").write_text(json.dumps(manifest, indent=2))
    print("published", day.name)

if __name__ == "__main__":
    main()
