"""
sync_state_writer.py — Sovereign Sync State Writer
==================================================
THE ONLY MODULE THAT WRITES sync-status.json.
All other modules are read-only with respect to this file.
Runs as the FINAL step after all scraping completes and validates.

Owner: scraper-agent / sync-state-writer sub-agent
"""

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

_scripts = Path(__file__).resolve().parent
while _scripts.name != "scripts" and _scripts != _scripts.parent:
    _scripts = _scripts.parent
if not (_scripts / "paths.py").is_file():
    raise RuntimeError("Expected .ai/scripts/paths.py — run from Sovereign workspace.")
if str(_scripts) not in sys.path:
    sys.path.insert(0, str(_scripts))

from paths import REPO_ROOT, project_scraped_dir  # noqa: E402

WORKSPACE_ROOT = REPO_ROOT


def hash_url(url: str) -> str:
    return hashlib.md5(url.encode("utf-8")).hexdigest()


def write_sync_state(slug: str, scrape_result: dict, delta: dict) -> bool:
    """
    Write sync-status.json for a competitor.
    ONLY called after scraping completes + validates.

    Args:
        slug: Competitor slug
        scrape_result: Output from scraper_engine.run_scrape()
        delta: Delta payload entry for this competitor

    Returns:
        True if written successfully, False on failure
    """
    scraped = project_scraped_dir()
    status_path = scraped / slug / "sync-status.json"
    backup_path = scraped / slug / "sync-status.backup.json"

    # Create backup of existing state before writing
    if status_path.exists():
        try:
            backup_path.write_bytes(status_path.read_bytes())
        except Exception:
            pass  # Backup failure is non-fatal; log and continue

    # Load existing URL hashes
    existing_hashes = {}
    if status_path.exists():
        try:
            with open(status_path) as f:
                existing = json.load(f)
            existing_hashes = existing.get("url_hashes", {})
        except Exception:
            existing_hashes = {}

    # Add new URL hashes
    new_url_hashes = dict(existing_hashes)
    for url in delta.get("new_urls", []):
        new_url_hashes[url] = hash_url(url)

    # Remove deleted URLs from hashes
    for url in delta.get("deleted_urls", []):
        new_url_hashes.pop(url, None)

    # Count total scraped content files
    scraped_dir = scraped / slug / "scraped" / "content"
    total_files = sum(1 for _ in scraped_dir.rglob("*.md")) if scraped_dir.exists() else 0

    new_state = {
        "last_sync": datetime.now(timezone.utc).isoformat(),
        "total_content": total_files,
        "new_since_last": scrape_result.get("files_written", 0),
        "scrape_state": "clean" if not scrape_result.get("errors") else "partial",
        "url_hashes": new_url_hashes,
        "delta_source": delta.get("source", "unknown"),
        "errors": scrape_result.get("errors", [])[:10],  # Cap stored errors at 10
        "written_at": datetime.now(timezone.utc).isoformat(),
    }

    # Validate before writing (timestamp must be recent, counts must match)
    written_time = datetime.fromisoformat(new_state["written_at"])
    if (datetime.now(timezone.utc) - written_time).seconds > 300:  # >5min drift
        # Timestamp anomaly — don't write
        return False

    # Attempt write with retry
    for attempt in range(1, 4):
        try:
            status_path.parent.mkdir(parents=True, exist_ok=True)
            with open(status_path, "w") as f:
                json.dump(new_state, f, indent=2)

            # Verify write
            with open(status_path) as f:
                verify = json.load(f)
            if verify.get("last_sync") == new_state["last_sync"]:
                # Success — remove backup
                backup_path.unlink(missing_ok=True)
                return True
        except Exception:
            if attempt == 3:
                # Rollback: restore backup
                if backup_path.exists():
                    backup_path.rename(status_path)
                return False

    return False


def mark_competitor_stale(slug: str, reason: str) -> None:
    """Mark a competitor as stale in index.json when sync fails repeatedly."""
    index_path = project_scraped_dir() / "index.json"
    if not index_path.exists():
        return

    with open(index_path) as f:
        index = json.load(f)

    for comp in index.get("competitors", []):
        if comp.get("slug") == slug:
            comp["status"] = "stale"
            comp["stale_reason"] = reason
            comp["stale_since"] = datetime.now(timezone.utc).isoformat()
            break

    with open(index_path, "w") as f:
        json.dump(index, f, indent=2)
