"""
Scans data/cases/<collection>/ folders and writes data/cases/index.json —
a manifest listing the JSON filenames in each collection.

Static sites served from GitHub Pages have no way to list a folder's
contents at runtime, so the front-end JS needs this manifest to know
which files to fetch after an editor publishes a new entry via /admin.

Run automatically by .github/workflows/build-case-index.yml whenever
a file under data/cases/ changes.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
CASES_DIR = ROOT / "data" / "cases"
COLLECTIONS = ["corruption", "killings", "promises", "news"]
OUTPUT_FILE = CASES_DIR / "index.json"


def main() -> None:
    manifest = {}
    for name in COLLECTIONS:
        folder = CASES_DIR / name
        if not folder.exists():
            manifest[name] = []
            continue
        manifest[name] = sorted(f.name for f in folder.glob("*.json"))

    OUTPUT_FILE.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    total = sum(len(v) for v in manifest.values())
    print(f"Wrote {OUTPUT_FILE} — {total} entries across {len(COLLECTIONS)} collections")


if __name__ == "__main__":
    main()
