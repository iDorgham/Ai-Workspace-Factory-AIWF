"""
archive_manager.py — Sovereign Archive Manager
==============================================
Compresses content and competitor files older than 30 days.
Verifies checksums. Rolls back on failure.
Updates archive-index.json (append only).

Owner: workflow-agent / archive-manager sub-agent
"""

import gzip
import hashlib
import json
import shutil
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

_scripts = Path(__file__).resolve().parent
while _scripts.name != "scripts" and _scripts != _scripts.parent:
    _scripts = _scripts.parent
if not (_scripts / "paths.py").is_file():
    raise RuntimeError("Expected .ai/scripts/paths.py — run from Sovereign workspace.")
if str(_scripts) not in sys.path:
    sys.path.insert(0, str(_scripts))

from paths import (  # noqa: E402
    REPO_ROOT,
    logs_dir,
    project_comparisons_dir,
    project_content_root,
    project_scraped_dir,
)

WORKSPACE_ROOT = REPO_ROOT
ARCHIVE_DIR = WORKSPACE_ROOT / "archive"
ARCHIVE_INDEX_PATH = WORKSPACE_ROOT / "archive" / "archive-index.json"
WORKFLOW_LOG = logs_dir() / "workflow.jsonl"

CUTOFF_DAYS = 30


def sha256_file(file_path: Path) -> str:
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def is_archivable(file_path: Path) -> bool:
    """Check if a file is old enough to archive (> 30 days)."""
    if not file_path.is_file():
        return False
    modified = datetime.fromtimestamp(file_path.stat().st_mtime, tz=timezone.utc)
    age = datetime.now(timezone.utc) - modified
    return age.days > CUTOFF_DAYS


def compress_file(source: Path, archive_path: Path) -> str:
    """Compress a file to .gz and return checksum."""
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    original_checksum = sha256_file(source)

    with open(source, "rb") as f_in:
        with gzip.open(archive_path, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)

    # Verify by decompressing and checking
    with gzip.open(archive_path, "rb") as f:
        decompressed = f.read()
    decompressed_checksum = hashlib.sha256(decompressed).hexdigest()

    if original_checksum != decompressed_checksum:
        archive_path.unlink(missing_ok=True)  # Remove failed archive
        raise ValueError(f"Checksum mismatch for {source.name}")

    return original_checksum


def build_archive_path(source_path: Path) -> Path:
    """Determine where to save the archive file."""
    relative = source_path.relative_to(WORKSPACE_ROOT)
    return ARCHIVE_DIR / relative.parent / (relative.name + ".gz")


def load_archive_index() -> dict:
    if ARCHIVE_INDEX_PATH.exists():
        with open(ARCHIVE_INDEX_PATH) as f:
            return json.load(f)
    return {"archives": [], "_meta": {"total_archived_files": 0}}


def append_to_archive_index(entry: dict) -> None:
    """Append only — never overwrite existing archive entries."""
    index = load_archive_index()
    index["archives"].append(entry)
    index["_meta"]["total_archived_files"] = len(index["archives"])
    index["_meta"]["last_archived"] = datetime.now(timezone.utc).isoformat()

    with open(ARCHIVE_INDEX_PATH, "w") as f:
        json.dump(index, f, indent=2)


def archive_file(source_path: Path) -> dict:
    """
    Archive a single file: compress, verify checksum, update index.
    Returns archive entry or raises on failure.
    """
    archive_path = build_archive_path(source_path)
    checksum = compress_file(source_path, archive_path)

    entry = {
        "original_path": str(source_path.relative_to(WORKSPACE_ROOT)),
        "archive_path": str(archive_path.relative_to(WORKSPACE_ROOT)),
        "checksum_sha256": checksum,
        "original_size_bytes": source_path.stat().st_size,
        "archived_at": datetime.now(timezone.utc).isoformat(),
        "original_modified": datetime.fromtimestamp(source_path.stat().st_mtime, tz=timezone.utc).isoformat(),
    }

    append_to_archive_index(entry)

    # Remove original after successful archive
    source_path.unlink()
    return entry


def run_archive(dry_run: bool = False) -> dict:
    """
    Find and archive all eligible files (> 30 days old).

    Args:
        dry_run: If True, report what would be archived without archiving

    Returns:
        {archived: int, skipped: int, errors: [...], space_freed_bytes: int}
    """
    # Directories eligible for archiving
    archive_dirs = [
        project_content_root(),
        project_scraped_dir(),
        project_comparisons_dir(),
    ]

    candidates = []
    for d in archive_dirs:
        if d.exists():
            for f in d.rglob("*.md"):
                if "_references" not in str(f) and is_archivable(f):
                    candidates.append(f)

    if dry_run:
        return {
            "dry_run": True,
            "would_archive": [str(f.relative_to(WORKSPACE_ROOT)) for f in candidates],
            "count": len(candidates),
        }

    archived = []
    errors = []
    space_freed = 0

    for source_path in candidates:
        try:
            original_size = source_path.stat().st_size
            entry = archive_file(source_path)
            archived.append(entry)
            space_freed += original_size
        except Exception as e:
            errors.append({"file": str(source_path.relative_to(WORKSPACE_ROOT)), "error": str(e)})

    result = {
        "archived_count": len(archived),
        "error_count": len(errors),
        "space_freed_bytes": space_freed,
        "space_freed_kb": round(space_freed / 1024, 1),
        "errors": errors,
        "archived_files": [a["original_path"] for a in archived],
    }

    log_archive(len(archived), space_freed, len(errors))
    return result


def log_archive(archived_count: int, space_freed: int, error_count: int) -> None:
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": "archive_completed",
        "archived_count": archived_count,
        "space_freed_bytes": space_freed,
        "error_count": error_count,
    }
    with open(WORKFLOW_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")


if __name__ == "__main__":
    print("Running archive (dry run)...")
    result = run_archive(dry_run=True)
    print(f"Would archive {result['count']} files:")
    for f in result["would_archive"][:10]:
        print(f"  {f}")
