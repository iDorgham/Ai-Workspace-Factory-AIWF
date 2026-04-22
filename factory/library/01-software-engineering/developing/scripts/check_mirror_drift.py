#!/usr/bin/env python3
"""Check drift between mirrored governance trees (.cursor and .antigravity)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from paths import REPO_ROOT


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


def main() -> int:
    parser = argparse.ArgumentParser(description="Check mirrored folder drift.")
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    args = parser.parse_args()

    cursor_root = REPO_ROOT / ".cursor"
    anti_root = REPO_ROOT / ".antigravity"
    checks = {
        "commands": check_pair(cursor_root / "commands", anti_root / "commands"),
        "rules": check_pair(cursor_root / "rules", anti_root / "rules"),
    }
    drift_total = sum(len(v["left_only"]) + len(v["right_only"]) for v in checks.values())
    payload = {"status": "pass" if drift_total == 0 else "fail", "drift_total": drift_total, "checks": checks}

    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print(f"mirror-drift status={payload['status']} drift_total={drift_total}")
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

    return 0 if drift_total == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
