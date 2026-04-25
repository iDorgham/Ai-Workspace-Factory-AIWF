#!/usr/bin/env python3
"""Check drift between mirrored governance trees (.cursor and .antigravity)."""

from __future__ import annotations

import datetime
import argparse
import json
import sys
from pathlib import Path

# Try to import REPO_ROOT, fallback to discovery
try:
    from paths import REPO_ROOT
except ImportError:
    REPO_ROOT = Path(__file__).resolve().parents[4] # Adjust based on deep path


def _relative_files(root: Path) -> set[str]:
    if not root.is_dir():
        return set()
    return {
        p.relative_to(root).as_posix()
        for p in root.rglob("*")
        if p.is_file() and ".DS_Store" not in p.name
    }


def check_pair(left: Path, right: Path) -> dict[str, list[str]]:
    left_files = _relative_files(left)
    right_files = _relative_files(right)
    return {
        "left_only": sorted(left_files - right_files),
        "right_only": sorted(right_files - left_files),
    }


def log_to_ledger(payload: dict):
    ledger_path = REPO_ROOT / ".ai/logs/ledgers/evolution_ledger.jsonl"
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    with open(ledger_path, "a") as f:
        f.write(json.dumps(payload) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Check mirrored folder drift.")
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    parser.add_argument("--threshold", type=int, default=5, help="Drift threshold for failure")
    parser.add_argument("--reasoning-hash", type=str, help="Reasoning hash for ledger")
    args = parser.parse_args()

    cursor_root = REPO_ROOT / ".cursor"
    anti_root = REPO_ROOT / ".antigravity"
    
    checks = {
        "commands": check_pair(cursor_root / "commands", anti_root / "commands"),
        "rules": check_pair(cursor_root / "rules", anti_root / "rules"),
    }
    
    drift_total = sum(len(v["left_only"]) + len(v["right_only"]) for v in checks.values())
    affected_domains = [k for k, v in checks.items() if v["left_only"] or v["right_only"]]
    
    status = "pass" if drift_total <= args.threshold else "fail"
    
    payload = {
        "type": "mirror_drift",
        "status": status,
        "node_count_delta": drift_total,
        "affected_domains": affected_domains,
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "reasoning_hash": args.reasoning_hash or "sha256:manual-trigger"
    }

    # Log to evolution ledger
    log_to_ledger(payload)

    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print(f"mirror-drift status={status} drift_total={drift_total} threshold={args.threshold}")
        if status == "fail":
            print(f"CRITICAL DRIFT: .ai registry out of sync with library. Run /git sync to repair.")
        
        for section, diff in checks.items():
            if not diff["left_only"] and not diff["right_only"]:
                print(f"- {section}: in sync")
                continue
            print(f"- {section}: drift detected")
            if diff["left_only"]:
                print("  .cursor only:")
                for entry in diff["left_only"]:
                    print(f"    - {entry}")
            if diff["right_only"]:
                print("  .antigravity only:")
                for entry in diff["right_only"]:
                    print(f"    - {entry}")

    return 0 if status == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
