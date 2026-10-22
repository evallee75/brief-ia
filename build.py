#!/usr/bin/env python3
"""Regroupe toutes les éditions JSON dans editions.js, chargé par index.html."""
import json
from pathlib import Path

SITE_DIR = Path(__file__).resolve().parent

editions = []
for path in sorted((SITE_DIR / "data").glob("*.json"), reverse=True):
    try:
        editions.append(json.loads(path.read_text(encoding="utf-8")))
    except json.JSONDecodeError as error:
        print(f"Édition ignorée ({path.name}) : {error}")

(SITE_DIR / "editions.js").write_text(
    "window.EDITIONS = " + json.dumps(editions, ensure_ascii=False, indent=1) + ";\n",
    encoding="utf-8",
)
print(f"{len(editions)} édition(s) publiée(s)")
