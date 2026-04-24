#!/usr/bin/env python3
"""Generate canonical workspace status/index artifacts and summary text."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from paths import REPO_ROOT

WORKSPACE_DIR = REPO_ROOT / ".ai" / "workspace"
INDEX_PATH = WORKSPACE_DIR / "index.json"
STATUS_PATH = WORKSPACE_DIR / "status.json"
SUMMARY_PATH = WORKSPACE_DIR / "ORGANIZATION-SUMMARY.txt"


def _is_ignored(path: Path) -> bool:
    skip = {".git", ".venv", "node_modules", "__pycache__"}
    return any(part in skip for part in path.parts)


def _all_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for p in root.rglob("*"):
        if p.is_file() and not _is_ignored(p):
            files.append(p)
    return files


def _project_payload(project_dir: Path) -> dict[str, Any]:
    cfg_path = project_dir / "project.config.json"
    cfg: dict[str, Any] = {}
    if cfg_path.is_file():
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    required = cfg.get("requiredPaths", [])
    missing = [rel for rel in required if not (project_dir / rel).exists()]
    md_count = len(list(project_dir.rglob("*.md")))
    return {
        "slug": project_dir.name,
        "name": cfg.get("name", project_dir.name),
        "owner": cfg.get("owner", "unknown"),
        "status": cfg.get("status", "unknown"),
        "path": project_dir.relative_to(REPO_ROOT).as_posix(),
        "readme_present": (project_dir / "README.md").is_file(),
        "config_present": cfg_path.is_file(),
        "required_paths_total": len(required),
        "required_paths_missing": missing,
        "markdown_files": md_count,
        "last_modified_utc": datetime.fromtimestamp(
            project_dir.stat().st_mtime, tz=timezone.utc
        ).isoformat(),
    }


def build_artifacts() -> tuple[dict[str, Any], dict[str, Any]]:
    now = datetime.now(timezone.utc).isoformat()
    files = _all_files(REPO_ROOT)
    md_files = [p for p in files if p.suffix.lower() == ".md"]
    json_files = [p for p in files if p.suffix.lower() == ".json"]
    content_root = REPO_ROOT / "content"
    projects = []
    if content_root.is_dir():
        projects = [_project_payload(p) for p in sorted(content_root.iterdir()) if p.is_dir()]

    required_missing_total = sum(len(p["required_paths_missing"]) for p in projects)
    readme_missing = [p["slug"] for p in projects if not p["readme_present"]]
    contracts_missing = [p["slug"] for p in projects if not p["config_present"]]
    healthy = required_missing_total == 0 and not readme_missing and not contracts_missing

    index = {
        "generated_at_utc": now,
        "repo_root": REPO_ROOT.as_posix(),
        "counts": {
            "total_files": len(files),
            "markdown_files": len(md_files),
            "json_files": len(json_files),
            "projects": len(projects),
        },
        "projects": projects,
    }
    status = {
        "generated_at_utc": now,
        "health": {
            "status": "healthy" if healthy else "warning",
            "required_paths_missing_total": required_missing_total,
            "projects_missing_readme": readme_missing,
            "projects_missing_contract": contracts_missing,
        },
        "canonical_source": ".ai/workspace/status.json",
        "index_source": ".ai/workspace/index.json",
    }
    return index, status


def write_summary(index: dict[str, Any], status: dict[str, Any]) -> None:
    counts = index["counts"]
    health = status["health"]
    lines = [
        "================================================================================",
        "GALLERIA WORKSPACE ORGANIZATION SUMMARY",
        "================================================================================",
        f"Generated (UTC): {status['generated_at_utc']}",
        f"Status: {'✅ HEALTHY' if health['status'] == 'healthy' else '🟡 WARNING'}",
        "",
        "Canonical status source: .ai/workspace/status.json",
        "Machine-readable index: .ai/workspace/index.json",
        "",
        "================================================================================",
        "CURRENT METRICS",
        "================================================================================",
        f"Total files: {counts['total_files']}",
        f"Markdown files: {counts['markdown_files']}",
        f"JSON files: {counts['json_files']}",
        f"Projects: {counts['projects']}",
        f"Required-path gaps: {health['required_paths_missing_total']}",
        f"Projects missing README: {', '.join(health['projects_missing_readme']) or 'none'}",
        f"Projects missing contract: {', '.join(health['projects_missing_contract']) or 'none'}",
        "",
        "================================================================================",
        "PROJECTS",
        "================================================================================",
    ]
    for project in index["projects"]:
        missing = project["required_paths_missing"]
        missing_fmt = ", ".join(missing) if missing else "none"
        lines.append(
            f"- {project['slug']}: owner={project['owner']}, status={project['status']}, "
            f"README={'yes' if project['readme_present'] else 'no'}, missing_required={missing_fmt}"
        )
    lines.extend(
        [
            "",
            "================================================================================",
            "NOTES",
            "================================================================================",
            "- This file is generated from workspace state; do not treat it as canonical truth.",
            "- Canonical status lives in .ai/workspace/status.json.",
            "- Regenerate with: python3 .ai/scripts/workspace_health.py",
        ]
    )
    SUMMARY_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate workspace health artifacts.")
    parser.add_argument(
        "--no-summary",
        action="store_true",
        help="Skip writing ORGANIZATION-SUMMARY.txt",
    )
    args = parser.parse_args()

    index, status = build_artifacts()
    WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)
    INDEX_PATH.write_text(json.dumps(index, indent=2), encoding="utf-8")
    STATUS_PATH.write_text(json.dumps(status, indent=2), encoding="utf-8")
    if not args.no_summary:
        write_summary(index, status)

    print(json.dumps({"index": INDEX_PATH.as_posix(), "status": STATUS_PATH.as_posix()}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
