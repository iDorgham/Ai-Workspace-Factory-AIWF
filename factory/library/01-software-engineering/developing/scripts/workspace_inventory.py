#!/usr/bin/env python3
"""Emit bucketed workspace inventory for cleanup triage (paths, size, mtime, action)."""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from paths import REPO_ROOT


def classify(rel_posix: str, name: str) -> tuple[str, str]:
    """Return (bucket, recommended_action)."""
    lower = rel_posix.lower()
    if name == ".ds_store" or "__pycache__" in lower or name.endswith((".pyc", ".pyo")):
        return "editor_os_cruft", "delete_safe; covered_by_gitignore"
    if lower.startswith(".git/"):
        return "git_internal", "skip"
    if "legacy-snapshots" in lower:
        return "legacy_narrative", "review_relocate_or_delete"
    if lower.startswith(".ai/migrations/"):
        if name.endswith(".py"):
            return "migration_script", "keep"
        return "migration_report", "review_delete_if_obsolete_regenerates_from_py"
    if lower.startswith(".ai/logs/"):
        if name == "workspace-cleanup-inventory.md":
            return "inventory_report", "keep_regenerate_via_workspace_inventory"
        if name == "path-integrity-report.json":
            return "path_integrity_artifact", "keep_regenerate_via_audit_path_integrity"
        if name == "path-integrity-summary.md":
            return "path_integrity_summary", "refresh_after_audit_path_integrity"
        if name.endswith(".json") and (
            "day-" in name or "smoke" in lower or "test-results" in lower or "results" in name
        ):
            return "generated_test_output", "optional_archive_after_user_confirms"
        if name.endswith(".jsonl"):
            return "append_only_runtime_log", "do_not_delete_without_retention_policy"
        return "ai_logs_misc", "review_case_by_case"
    if ".cursor/commands" in lower or ".cursor/rules" in lower:
        return "intentional_cursor_mirror", "keep_discoverability"
    if ".antigravity/commands" in lower or ".antigravity/rules" in lower:
        return "intentional_antigravity_mirror", "keep_discoverability"
    return "other", "review_if_unused"


def walk_files(root: Path):
    for dirpath, dirnames, filenames in os.walk(root, topdown=True):
        # Prune heavy / local-only subtrees from inventory noise
        skip = {".git", ".venv", "node_modules"}
        dirnames[:] = [d for d in dirnames if d not in skip]
        base = Path(dirpath)
        for fn in filenames:
            abs_path = base / fn
            if not abs_path.is_file():
                continue
            rel = abs_path.relative_to(root)
            yield abs_path, rel.as_posix()


def main() -> None:
    parser = argparse.ArgumentParser(description="Workspace cleanup inventory")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of markdown")
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Output file (default: .ai/logs/workspace-cleanup-inventory.md)",
    )
    args = parser.parse_args()

    rows: list[dict[str, str | int]] = []
    for abs_path, rel_posix in walk_files(REPO_ROOT):
        stat = abs_path.stat()
        size = stat.st_size
        mtime = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat()
        name = abs_path.name
        bucket, action = classify(rel_posix, name)
        rows.append(
            {
                "path": rel_posix,
                "size_bytes": size,
                "mtime_utc": mtime,
                "bucket": bucket,
                "recommended_action": action,
            }
        )

    rows.sort(key=lambda r: (str(r["bucket"]), str(r["path"])))

    out = args.out or (REPO_ROOT / ".ai" / "logs" / "workspace-cleanup-inventory.md")
    out.parent.mkdir(parents=True, exist_ok=True)

    if args.json:
        text = json.dumps(rows, indent=2)
    else:
        lines = [
            "# Workspace cleanup inventory",
            "",
            f"Generated (UTC): `{datetime.now(timezone.utc).isoformat()}`",
            "",
            f"Repo root: `{REPO_ROOT}`",
            "",
            "| Path | Size (bytes) | mtime (UTC) | Bucket | Recommended action |",
            "|------|-------------:|-------------|--------|-------------------|",
        ]
        for r in rows:
            p = str(r["path"]).replace("|", "\\|")
            lines.append(
                f"| `{p}` | {r['size_bytes']} | {str(r['mtime_utc'])[:19]} | {r['bucket']} | {r['recommended_action']} |"
            )
        text = "\n".join(lines) + "\n"

    out.write_text(text, encoding="utf-8")
    print(f"Wrote {len(rows)} entries to {out}")


if __name__ == "__main__":
    main()
