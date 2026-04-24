#!/usr/bin/env python3
from pathlib import Path
import datetime
import json

ROOT = Path(__file__).resolve().parents[1]
BUCKETS = [
    "agents",
    "subagents",
    "skills",
    "commands",
    "subcommands",
    "templates",
    "scripts",
]


def main() -> None:
    for bucket in BUCKETS:
        folder = ROOT / "library" / bucket
        items: list[dict] = []
        if folder.is_dir():
            for meta in folder.rglob("*.meta.json"):
                items.append(json.loads(meta.read_text()))
        out = {
            "version": "1.0.0",
            "type": bucket,
            "generated_at": datetime.datetime.now(datetime.timezone.utc)
            .replace(microsecond=0)
            .isoformat(),
            "items": sorted(items, key=lambda x: x["id"]),
        }
        (ROOT / "library-index" / f"{bucket}.index.json").write_text(json.dumps(out, indent=2) + "\n")


if __name__ == "__main__":
    main()
