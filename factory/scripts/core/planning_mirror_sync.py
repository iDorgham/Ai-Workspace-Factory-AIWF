#!/usr/bin/env python3
"""
AIWF v21.0.0 — Planning Mirror Sync
=====================================
Deterministic outbound mirror: .ai/plan/{type}/ → factory/library/planning/{type}/

Rules:
  - Source of truth: .ai/plan/  (active workspace)
  - Target:          factory/library/planning/  (shared library)
  - Dry-run safe:    --dry-run flag prints actions without writing
  - Selective:       --type {slug} mirrors a single planning type
  - Exclusions:      __pycache__/, *.pyc, .DS_Store, scratch/, tmp/
  - Conflict policy: source always wins (active-set priority)
  - Reasoning hash:  auto-generated and written to sync_manifest.json

Usage:
  python3 factory/scripts/core/planning_mirror_sync.py
  python3 factory/scripts/core/planning_mirror_sync.py --type content
  python3 factory/scripts/core/planning_mirror_sync.py --dry-run
  python3 factory/scripts/core/planning_mirror_sync.py --type seo --dry-run

Exit codes:
  0 — sync completed (or dry-run completed)
  1 — source path missing for requested type
  2 — unexpected error
"""

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────────
ROOT        = Path(__file__).resolve().parents[3]          # repo root
SOURCE_BASE = ROOT / ".ai" / "plan"
TARGET_BASE = ROOT / "factory" / "library" / "planning"
MANIFEST    = TARGET_BASE / "sync_manifest.json"

# ── Planning types registered in v21.0.0 ──────────────────────────────────────
PLANNING_TYPES = [
    "development",
    "content",
    "seo",
    "social_media",
    "marketing",
    "business",
    "media",
    "branding",
]

# ── Exclusions ─────────────────────────────────────────────────────────────────
EXCLUDED_NAMES = {".DS_Store", "__pycache__", "scratch", "tmp", ".git"}
EXCLUDED_EXTS  = {".pyc", ".pyo"}


# ── Helpers ────────────────────────────────────────────────────────────────────

def _git_head_sha(repo_root: Path) -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=repo_root, capture_output=True, text=True, timeout=5
        )
        sha = result.stdout.strip()
        return sha if sha else "no-git"
    except Exception:
        return "no-git"


def generate_reasoning_hash(repo_root: Path, synced_files: list[str]) -> str:
    git_sha   = _git_head_sha(repo_root)
    timestamp = datetime.now(timezone.utc).isoformat()
    payload   = f"{git_sha}:{timestamp}:{':'.join(sorted(synced_files))}"
    digest    = hashlib.sha256(payload.encode()).hexdigest()[:16]
    return f"sha256:{digest}"


def should_exclude(path: Path) -> bool:
    if path.name in EXCLUDED_NAMES:
        return True
    if path.suffix in EXCLUDED_EXTS:
        return True
    return False


# ── Core mirror ────────────────────────────────────────────────────────────────

def mirror_directory(source: Path, target: Path, dry_run: bool) -> tuple[list[str], list[str]]:
    """
    Recursively mirror source → target.
    Returns (copied_files, skipped_files).
    """
    copied  = []
    skipped = []

    if not source.exists():
        return copied, skipped

    for item in source.rglob("*"):
        # Check if any parent in the path is excluded
        relative = item.relative_to(source)
        parts    = relative.parts

        excluded = False
        for part in parts:
            p = Path(part)
            if p.name in EXCLUDED_NAMES or p.suffix in EXCLUDED_EXTS:
                excluded = True
                break

        if excluded:
            skipped.append(str(relative))
            continue

        if item.is_dir():
            continue  # handled implicitly by file copy

        dest = target / relative

        if not dry_run:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, dest)

        copied.append(str(item.relative_to(ROOT)))

    return copied, skipped


# ── Manifest ───────────────────────────────────────────────────────────────────

def load_manifest() -> dict:
    if MANIFEST.exists():
        try:
            return json.loads(MANIFEST.read_text())
        except Exception:
            pass
    return {
        "version": "v21.0.0",
        "sync_runs": [],
    }


def write_manifest(manifest: dict, dry_run: bool) -> None:
    if dry_run:
        return
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(manifest, indent=2))


# ── Entry point ────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(
        description="AIWF v21 Planning Mirror Sync — .ai/plan/ → factory/library/planning/"
    )
    parser.add_argument(
        "--type", metavar="SLUG",
        help="Sync only this planning type (e.g. content, seo). Default: all."
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print actions without writing any files."
    )
    args = parser.parse_args()

    dry_run = args.dry_run
    mode    = "[DRY-RUN] " if dry_run else ""

    # Determine which types to sync
    if args.type:
        if args.type not in PLANNING_TYPES:
            print(f"❌ Unknown planning type: '{args.type}'")
            print(f"   Valid types: {', '.join(PLANNING_TYPES)}")
            return 1
        types_to_sync = [args.type]
    else:
        types_to_sync = PLANNING_TYPES

    print(f"\n{mode}🔄 AIWF Planning Mirror Sync — v21.0.0")
    print(f"   Source: {SOURCE_BASE.relative_to(ROOT)}")
    print(f"   Target: {TARGET_BASE.relative_to(ROOT)}")
    print(f"   Types:  {', '.join(types_to_sync)}")
    print()

    manifest       = load_manifest()
    total_copied   = []
    total_skipped  = []
    synced_types   = []
    missing_types  = []

    for slug in types_to_sync:
        source = SOURCE_BASE / slug
        target = TARGET_BASE / slug

        if not source.exists():
            print(f"   ⚠️  SKIP  [{slug}] — source not found ({source.relative_to(ROOT)})")
            missing_types.append(slug)
            continue

        copied, skipped = mirror_directory(source, target, dry_run)
        total_copied.extend(copied)
        total_skipped.extend(skipped)
        synced_types.append(slug)

        print(f"   {'📋' if dry_run else '✅'} [{slug}] {len(copied)} file(s) {'would be synced' if dry_run else 'synced'}, {len(skipped)} excluded")

    # Generate reasoning hash from all synced files
    reasoning_hash = generate_reasoning_hash(ROOT, total_copied)

    # Record this run in manifest
    run_entry = {
        "timestamp":      datetime.now(timezone.utc).isoformat(),
        "reasoning_hash": reasoning_hash,
        "dry_run":        dry_run,
        "types_synced":   synced_types,
        "types_missing":  missing_types,
        "files_copied":   len(total_copied),
        "files_excluded": len(total_skipped),
    }
    manifest.setdefault("sync_runs", []).append(run_entry)
    # Keep last 50 runs only
    manifest["sync_runs"] = manifest["sync_runs"][-50:]
    manifest["last_sync"] = run_entry

    write_manifest(manifest, dry_run)

    print()
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"  {'[DRY-RUN] ' if dry_run else ''}Sync complete")
    print(f"  Types synced:  {len(synced_types)} / {len(types_to_sync)}")
    print(f"  Files copied:  {len(total_copied)}")
    print(f"  Files excluded:{len(total_skipped)}")
    print(f"  Reasoning hash:{reasoning_hash}")
    if not dry_run:
        print(f"  Manifest:      {MANIFEST.relative_to(ROOT)}")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    if missing_types and not synced_types:
        # Requested type(s) entirely missing — error
        return 1

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(2)
