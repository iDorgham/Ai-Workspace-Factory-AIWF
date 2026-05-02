#!/usr/bin/env python3
"""Run docs quality gates: links, required files, stale dates/versions, mirror drift."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from paths import REPO_ROOT

DOC_EXTENSIONS = {".md", ".txt"}
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
DATE_RE = re.compile(r"(20\d{2}-\d{2}-\d{2})")
VERSION_RE = re.compile(r"v\d+\.\d+(?:\.\d+)?(?:-[A-Za-z0-9.]+)?")


def run_cmd(*cmd: str) -> tuple[int, str]:
    p = subprocess.run(list(cmd), cwd=REPO_ROOT, capture_output=True, text=True)
    return p.returncode, p.stdout.strip() or p.stderr.strip()


def _markdown_paths_for_link_audit() -> Iterable[Path]:
    """Curated surfaces only — avoid scanning the entire factory mirror (legacy relative links)."""
    dirs = [
        REPO_ROOT / "docs",
        REPO_ROOT / ".ai" / "workspace",
        REPO_ROOT / "dashboard",
        REPO_ROOT / "factory" / "library" / "templates" / "dashboard",
    ]
    singles = [
        REPO_ROOT / "README.md",
        REPO_ROOT / "AGENTS.md",
        REPO_ROOT / "factory" / "library" / "README.md",
    ]
    for f in singles:
        if f.is_file() and f.suffix in DOC_EXTENSIONS:
            yield f
    for root in dirs:
        if not root.is_dir():
            continue
        for path in root.rglob("*"):
            if path.is_file() and path.suffix in DOC_EXTENSIONS:
                if ".ai/logs/" in path.as_posix():
                    continue
                yield path


def check_local_links() -> dict[str, Any]:
    broken: list[dict[str, str]] = []
    for path in _markdown_paths_for_link_audit():
        text = path.read_text(encoding="utf-8", errors="ignore")
        for raw in LINK_RE.findall(text):
            target = raw.strip()
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            # Ignore regex/template examples that look like links but are not file paths.
            if any(ch in target for ch in ("[", "]", "^", "*")):
                continue
            target_path = (path.parent / target).resolve()
            if not target_path.exists():
                broken.append(
                    {
                        "file": path.relative_to(REPO_ROOT).as_posix(),
                        "target": target,
                    }
                )
    return {"status": "pass" if not broken else "fail", "broken": broken}


def check_required_files() -> dict[str, Any]:
    content_root = REPO_ROOT / "content"
    missing: list[dict[str, Any]] = []
    if not content_root.is_dir():
        return {"status": "pass", "missing": [], "note": "content/ absent — skip required-path scan"}
    for project in sorted(content_root.iterdir()):
        if not project.is_dir():
            continue
        cfg_path = project / "project.config.json"
        if not cfg_path.is_file():
            missing.append({"project": project.name, "missing": ["project.config.json"]})
            continue
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
        required = cfg.get("requiredPaths", [])
        absent = [entry for entry in required if not (project / entry).exists()]
        if absent:
            missing.append({"project": project.name, "missing": absent})
    return {"status": "pass" if not missing else "fail", "missing": missing}


def check_stale_markers(max_age_days: int) -> dict[str, Any]:
    stale: list[dict[str, Any]] = []
    now = datetime.now(timezone.utc).date()
    scoped_paths = [
        REPO_ROOT / ".ai/workspace/README.md",
        REPO_ROOT / ".ai/workspace/ORGANIZATION-SUMMARY.txt",
        REPO_ROOT / ".ai/workspace/status.json",
        REPO_ROOT / ".ai/workspace/index.json",
    ]
    for path in scoped_paths:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        dates = DATE_RE.findall(text)
        versions = VERSION_RE.findall(text)
        if not dates or not versions:
            continue
        newest = max(dates)
        try:
            age = (now - datetime.strptime(newest, "%Y-%m-%d").date()).days
        except ValueError:
            continue
        if age > max_age_days:
            stale.append(
                {
                    "file": path.relative_to(REPO_ROOT).as_posix(),
                    "latest_date": newest,
                    "age_days": age,
                }
            )
    return {"status": "pass" if not stale else "fail", "max_age_days": max_age_days, "stale": stale}


def check_mirror_drift() -> dict[str, Any]:
    drift_script = REPO_ROOT / "factory/scripts/core/check_mirror_drift.py"
    rc, out = run_cmd("python3", str(drift_script), "--json")
    try:
        payload = json.loads(out)
    except json.JSONDecodeError:
        payload = {"status": "fail", "error": out}
    payload["exit_code"] = rc
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Run docs quality gates.")
    parser.add_argument("--max-age-days", type=int, default=90, help="Staleness threshold for date+version docs")
    args = parser.parse_args()

    local_links = check_local_links()
    required_files = check_required_files()
    stale_markers = check_stale_markers(args.max_age_days)
    mirror_drift = check_mirror_drift()

    report = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "checks": {
            "local_links": local_links,
            "required_files": required_files,
            "stale_markers": stale_markers,
            "mirror_drift": mirror_drift,
        },
    }
    failed = [
        name
        for name, payload in report["checks"].items()
        if payload.get("status") != "pass"
    ]
    report["summary"] = {"status": "pass" if not failed else "fail", "failed_checks": failed}
    print(json.dumps(report, indent=2))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
