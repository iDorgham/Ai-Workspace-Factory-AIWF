#!/usr/bin/env python3
"""
spec_density_gate_v2 — AIWF v21.0.0 SDD Phase Density Enforcer

Validates that a phase folder satisfies all structural requirements before
it can transition from DRAFT/REVIEW → APPROVED → ACTIVE.

Rules enforced:
  1. Minimum 12 spec files (total, recursive)
  2. Mandatory C4 diagrams present (c4-context.mmd, c4-containers.mmd)
  3. Required top-level files: phase.spec.json, requirements.spec.md,
     design.md, domain_model.md, task_graph.mmd, tasks.json, regional_compliance.md
  4. Required subdirectories with ≥1 file each: contracts/, templates/,
     validation/, prompt_library/
  5. tasks.json must contain ≥5 tasks

Exit codes:
  0 — PASS: All gates satisfied
  1 — FAIL: One or more gates failed (details in JSON output)
  2 — ERROR: Phase path does not exist or is not a directory

Integration:
  - Called by pre-commit hook (alongside check_mirror_drift.py)
  - Called by /plan activate command before manifest status update
  - Called by CI workflow aiwf-industrial-pipeline.yml sovereign-verification job

Usage:
  python spec_density_gate_v2.py --phase .ai/plan/development/19_sovereign_commit
  python spec_density_gate_v2.py --phase .ai/plan/content/phase-01-discovery --json
  python spec_density_gate_v2.py --phase . --strict   # fail on any warning
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# ── Constants ──────────────────────────────────────────────────────────────────

MINIMUM_FILES = 12
MINIMUM_TASKS = 5

REQUIRED_TOP_LEVEL_FILES = [
    "phase.spec.json",
    "requirements.spec.md",
    "design.md",
    "domain_model.md",
    "task_graph.mmd",
    "tasks.json",
    "regional_compliance.md",
]

REQUIRED_C4_FILES = [
    "c4-context.mmd",
    "c4-containers.mmd",
]

REQUIRED_SUBDIRS_WITH_FILES = [
    "contracts",
    "templates",
    "validation",
    "prompt_library",
]

# ── Helpers ────────────────────────────────────────────────────────────────────

def _count_files(path: Path) -> int:
    """Recursive count of all files (excluding hidden files and __pycache__)."""
    return sum(
        1 for p in path.rglob("*")
        if p.is_file()
        and not any(part.startswith(".") for part in p.parts[-3:])
        and "__pycache__" not in str(p)
    )


def _git_head(repo_root: Path) -> str:
    try:
        r = subprocess.run(
            ["git", "-C", str(repo_root), "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, timeout=5
        )
        return r.stdout.strip() if r.returncode == 0 else "no-git"
    except Exception:
        return "no-git"


def _reasoning_hash(phase_path: str, timestamp: str, repo_root: Path) -> str:
    session = _git_head(repo_root)
    raw = f"density-gate:{session}:{phase_path}:{timestamp}"
    return f"sha256:{hashlib.sha256(raw.encode()).hexdigest()[:16]}"


def _load_tasks(phase: Path) -> list[dict]:
    tasks_file = phase / "tasks.json"
    if not tasks_file.exists():
        return []
    try:
        data = json.loads(tasks_file.read_text())
        return data.get("tasks", [])
    except (json.JSONDecodeError, KeyError):
        return []


# ── Gate Checks ────────────────────────────────────────────────────────────────

def check_minimum_file_count(phase: Path) -> dict:
    count = _count_files(phase)
    passed = count >= MINIMUM_FILES
    return {
        "gate": "minimum_file_count",
        "passed": passed,
        "value": count,
        "threshold": MINIMUM_FILES,
        "message": f"{count} files found — {'✓ PASS' if passed else f'✗ FAIL (need {MINIMUM_FILES})'}",
    }


def check_required_files(phase: Path) -> dict:
    missing = [f for f in REQUIRED_TOP_LEVEL_FILES if not (phase / f).exists()]
    passed = len(missing) == 0
    return {
        "gate": "required_top_level_files",
        "passed": passed,
        "missing": missing,
        "message": (
            "All required files present ✓"
            if passed
            else f"Missing: {', '.join(missing)}"
        ),
    }


def check_c4_diagrams(phase: Path) -> dict:
    missing = [f for f in REQUIRED_C4_FILES if not (phase / f).exists()]
    passed = len(missing) == 0
    return {
        "gate": "c4_diagrams",
        "passed": passed,
        "missing": missing,
        "message": (
            "C4 diagrams present ✓"
            if passed
            else f"Missing C4 files: {', '.join(missing)}"
        ),
    }


def check_subdirectories(phase: Path) -> dict:
    results = {}
    all_pass = True
    for subdir in REQUIRED_SUBDIRS_WITH_FILES:
        sub = phase / subdir
        if not sub.is_dir():
            results[subdir] = {"exists": False, "file_count": 0}
            all_pass = False
        else:
            count = _count_files(sub)
            ok = count >= 1
            results[subdir] = {"exists": True, "file_count": count, "pass": ok}
            if not ok:
                all_pass = False
    return {
        "gate": "required_subdirectories",
        "passed": all_pass,
        "subdirs": results,
        "message": (
            "All required subdirs populated ✓"
            if all_pass
            else f"Empty or missing subdirs: {[k for k, v in results.items() if not v.get('pass', False)]}"
        ),
    }


def check_tasks_minimum(phase: Path) -> dict:
    tasks = _load_tasks(phase)
    count = len(tasks)
    passed = count >= MINIMUM_TASKS
    return {
        "gate": "tasks_minimum",
        "passed": passed,
        "value": count,
        "threshold": MINIMUM_TASKS,
        "message": (
            f"{count} tasks defined ✓"
            if passed
            else f"Only {count} tasks — need ≥{MINIMUM_TASKS}"
        ),
    }


def check_phase_spec_valid(phase: Path) -> dict:
    spec_file = phase / "phase.spec.json"
    if not spec_file.exists():
        return {"gate": "phase_spec_valid", "passed": False, "message": "phase.spec.json missing"}
    try:
        data = json.loads(spec_file.read_text())
        required_keys = ["spec_id", "planning_type", "phase_name", "status"]
        # Allow templates with placeholder values
        missing = [k for k in required_keys if k not in data]
        passed = len(missing) == 0
        return {
            "gate": "phase_spec_valid",
            "passed": passed,
            "missing_keys": missing,
            "message": "phase.spec.json valid ✓" if passed else f"Missing keys: {missing}",
        }
    except json.JSONDecodeError as e:
        return {
            "gate": "phase_spec_valid",
            "passed": False,
            "message": f"JSON parse error: {e}",
        }


# ── Main ───────────────────────────────────────────────────────────────────────

def run_all_gates(phase: Path) -> dict:
    """Run all density gates against a phase folder. Returns full report."""
    now = datetime.now(timezone.utc).isoformat()

    # Discover repo root (walk up to find .git)
    repo_root = phase.resolve()
    for parent in [phase.resolve()] + list(phase.resolve().parents):
        if (parent / ".git").exists():
            repo_root = parent
            break

    gates = [
        check_minimum_file_count(phase),
        check_required_files(phase),
        check_c4_diagrams(phase),
        check_subdirectories(phase),
        check_tasks_minimum(phase),
        check_phase_spec_valid(phase),
    ]

    all_passed = all(g["passed"] for g in gates)
    failed_gates = [g["gate"] for g in gates if not g["passed"]]

    return {
        "type": "density_gate_report",
        "phase_path": str(phase.resolve()),
        "phase_name": phase.name,
        "timestamp": now,
        "reasoning_hash": _reasoning_hash(str(phase), now, repo_root),
        "overall": "PASS" if all_passed else "FAIL",
        "gates_passed": len(gates) - len(failed_gates),
        "gates_total": len(gates),
        "failed_gates": failed_gates,
        "gates": gates,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="AIWF v21 SDD Spec Density Gate v2 — validates phase folder structure"
    )
    parser.add_argument(
        "--phase",
        required=True,
        help="Path to the phase folder to validate"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit full JSON report"
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail on any warning (not just hard failures)"
    )
    parser.add_argument(
        "--write-report",
        action="store_true",
        help="Write report to validation/density_gate_report.json inside the phase folder"
    )
    args = parser.parse_args()

    phase = Path(args.phase).resolve()

    if not phase.exists():
        print(f"ERROR: Phase path does not exist: {phase}", file=sys.stderr)
        return 2

    if not phase.is_dir():
        print(f"ERROR: Phase path is not a directory: {phase}", file=sys.stderr)
        return 2

    report = run_all_gates(phase)

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        status_icon = "✅" if report["overall"] == "PASS" else "❌"
        print(f"\n{status_icon} DENSITY GATE {report['overall']} — {phase.name}")
        print(f"   Gates: {report['gates_passed']}/{report['gates_total']} passed")
        print(f"   Hash:  {report['reasoning_hash']}")
        print()
        for gate in report["gates"]:
            icon = "  ✓" if gate["passed"] else "  ✗"
            print(f"{icon} [{gate['gate']}] {gate['message']}")
        print()
        if report["failed_gates"]:
            print(f"BLOCKED — Fix failed gates before activating phase: {report['failed_gates']}")
        else:
            print("APPROVED — Phase meets all density requirements.")

    if args.write_report:
        validation_dir = phase / "validation"
        validation_dir.mkdir(exist_ok=True)
        report_file = validation_dir / "density_gate_report.json"
        report_file.write_text(json.dumps(report, indent=2))
        if not args.json:
            print(f"\nReport written to: {report_file}")

    return 0 if report["overall"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
