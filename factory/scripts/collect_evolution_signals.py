#!/usr/bin/env python3
"""
Aggregate evolution signals from generated workspaces under workspaces/<slug>/.factory/signals/*.json
into factory/evolution for curator review.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent


def main() -> None:
    cfg = json.loads((ROOT / "registry" / "factory-config.json").read_text())
    if not cfg.get("evolution", {}).get("enabled", True):
        print("Evolution collection disabled in factory-config.json")
        return

    root_name = cfg.get("workspace_root_folder", "workspaces")
    ws_root = REPO_ROOT / root_name
    out_dir = ROOT / "evolution" / "signals"
    out_dir.mkdir(parents=True, exist_ok=True)

    aggregate: list[dict] = []
    if ws_root.is_dir():
        for ws in sorted(p for p in ws_root.iterdir() if p.is_dir()):
            sig_dir = ws / ".factory" / "signals"
            if not sig_dir.is_dir():
                continue
            for f in sorted(sig_dir.glob("*.json")):
                try:
                    payload = json.loads(f.read_text())
                except json.JSONDecodeError:
                    continue
                aggregate.append(
                    {
                        "workspace": ws.name,
                        "signal_file": str(f.relative_to(REPO_ROOT)),
                        "payload": payload,
                    }
                )

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out_path = out_dir / f"aggregate-{stamp}.json"
    out_path.write_text(json.dumps({"generated_at": stamp, "items": aggregate}, indent=2) + "\n")
    print(f"Wrote {out_path} ({len(aggregate)} signal(s))")


if __name__ == "__main__":
    main()
