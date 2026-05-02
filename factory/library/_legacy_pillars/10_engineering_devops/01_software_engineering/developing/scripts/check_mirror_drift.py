#!/usr/bin/env python3
"""Check drift between mirrored governance trees (.cursor and .antigravity).

Reasoning Hash Policy:
  Every ledger entry MUST carry a deterministic reasoning hash derived from:
    session_id (git HEAD short SHA) + timestamp + sorted list of affected files
  The legacy "sha256:manual-trigger" sentinel is only emitted when git is unavailable.
"""

from __future__ import annotations

import datetime
import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
CORE_MIRROR_FILES = [
    (".ai/scripts/core/cli_router.py", "factory/library/scripts/core/cli_router.py"),
    (".ai/scripts/core/workflow_orchestrator.py", "factory/library/scripts/core/workflow_orchestrator.py"),
]


# Try to import REPO_ROOT, fallback to discovery
try:
    from paths import REPO_ROOT
except ImportError:
    REPO_ROOT = Path(__file__).resolve().parents[4] # Adjust based on deep path


def _git_head_sha(repo_root: Path) -> str:
    """Return the short git HEAD SHA, or 'no-git' if unavailable."""
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_root), "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, timeout=5
        )
        return result.stdout.strip() if result.returncode == 0 else "no-git"
    except Exception:
        return "no-git"


def generate_reasoning_hash(repo_root: Path, affected_files: list[str], timestamp: str) -> str:
    """
    Compute a deterministic reasoning hash from:
      session_id (git HEAD short SHA) + ISO timestamp + sorted affected file list

    Format: sha256:{hex[:16]}  (16-char prefix for readability in logs)
    Falls back to 'sha256:manual-trigger' only if git is unavailable AND no files detected.
    """
    session_id = _git_head_sha(repo_root)
    if session_id == "no-git" and not affected_files:
        return "sha256:manual-trigger"

    raw = f"{session_id}:{timestamp}:{':'.join(sorted(affected_files))}"
    full_hash = hashlib.sha256(raw.encode()).hexdigest()
    return f"sha256:{full_hash[:16]}"


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


def check_file_mirrors(repo_root: Path, file_pairs: list[tuple[str, str]]) -> dict[str, list[str]]:
    drifted = []
    missing = []
    for left_rel, right_rel in file_pairs:
        left_path = repo_root / left_rel
        right_path = repo_root / right_rel
        if not left_path.exists() or not right_path.exists():
            missing.append(f"{left_rel} <> {right_rel}")
            continue
        if left_path.read_text(encoding="utf-8") != right_path.read_text(encoding="utf-8"):
            drifted.append(f"{left_rel} <> {right_rel}")
    return {"drifted": drifted, "missing": missing}


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
    core_orchestrator_check = check_file_mirrors(REPO_ROOT, CORE_MIRROR_FILES)
    
    drift_total = sum(len(v["left_only"]) + len(v["right_only"]) for v in checks.values())
    drift_total += len(core_orchestrator_check["drifted"]) + len(core_orchestrator_check["missing"])
    affected_domains = [k for k, v in checks.items() if v["left_only"] or v["right_only"]]
    if core_orchestrator_check["drifted"] or core_orchestrator_check["missing"]:
        affected_domains.append("core_orchestrator")
    
    status = "pass" if drift_total <= args.threshold else "fail"
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()

    # Collect all drifted file paths for hash input
    drifted_files: list[str] = []
    for diff in checks.values():
        drifted_files.extend(diff["left_only"])
        drifted_files.extend(diff["right_only"])
    drifted_files.extend(core_orchestrator_check["drifted"])
    drifted_files.extend(core_orchestrator_check["missing"])

    # Use caller-supplied hash, or compute a real deterministic one
    reasoning_hash = (
        args.reasoning_hash
        if args.reasoning_hash
        else generate_reasoning_hash(REPO_ROOT, drifted_files, now_iso)
    )

    payload = {
        "type": "mirror_drift",
        "status": status,
        "node_count_delta": drift_total,
        "affected_domains": affected_domains,
        "timestamp": now_iso,
        "reasoning_hash": reasoning_hash,
        "hash_source": "caller-supplied" if args.reasoning_hash else "auto-generated"
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
        if not core_orchestrator_check["drifted"] and not core_orchestrator_check["missing"]:
            print("- core_orchestrator: in sync")
        else:
            print("- core_orchestrator: drift detected")
            for entry in core_orchestrator_check["missing"]:
                print(f"  missing pair: {entry}")
            for entry in core_orchestrator_check["drifted"]:
                print(f"  content mismatch: {entry}")

    return 0 if status == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
