"""
delta_detector.py — Sovereign Delta Detection Engine
====================================================
Detects new, updated, and deleted content on competitor sites.
READ-ONLY: This module never writes to disk. It only reads.
Output: delta_payload.json consumed by scraper_engine.py

Owner: scraper-agent / delta-detector sub-agent
Authoritative writer of sync-status.json: sync_state_writer.py (NOT this file)
"""

import hashlib
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

_scripts = Path(__file__).resolve().parent
while _scripts.name != "scripts" and _scripts != _scripts.parent:
    _scripts = _scripts.parent
if not (_scripts / "paths.py").is_file():
    raise RuntimeError("Expected .ai/scripts/paths.py — run from Sovereign workspace.")
if str(_scripts) not in sys.path:
    sys.path.insert(0, str(_scripts))

from paths import REPO_ROOT, project_scraped_dir  # noqa: E402

WORKSPACE_ROOT = REPO_ROOT
MIN_DELTA_AGE_HOURS = 24   # Only flag deltas older than 24h as real changes
FALSE_POSITIVE_THRESHOLD = 0.10  # Alert if >10% of detected deltas are false positives


def load_index() -> dict:
    """Load the competitors master registry."""
    index_path = project_scraped_dir() / "index.json"
    if not index_path.exists():
        return {"competitors": []}
    with open(index_path) as f:
        return json.load(f)


def load_sync_status(slug: str) -> dict:
    """Load the last sync status for a competitor."""
    status_path = project_scraped_dir() / slug / "sync-status.json"
    if not status_path.exists():
        return {
            "last_sync": None,
            "url_hashes": {},
            "total_content": 0,
            "new_since_last": 0,
        }
    with open(status_path) as f:
        return json.load(f)


def hash_url_content(url: str, content: str = None) -> str:
    """Generate a stable hash for a URL + its content (if provided)."""
    data = f"{url}:{content or ''}"
    return hashlib.md5(data.encode("utf-8")).hexdigest()


def fetch_sitemap(base_url: str, timeout: int = 5) -> list[str]:
    """
    Attempt to fetch URLs from sitemap.xml.
    Returns list of URLs or empty list on failure.
    """
    sitemap_url = urljoin(base_url.rstrip("/") + "/", "sitemap.xml")
    try:
        req = Request(sitemap_url, headers={"User-Agent": "SovereignBot/1.0 (research)"})
        with urlopen(req, timeout=timeout) as resp:
            content = resp.read().decode("utf-8", errors="replace")
        # Extract URLs from sitemap XML (simple regex — avoids heavy XML parser dep)
        urls = re.findall(r"<loc>(https?://[^<]+)</loc>", content)
        return [u.strip() for u in urls]
    except (URLError, HTTPError, Exception):
        return []


def fetch_rss(base_url: str, timeout: int = 5) -> list[dict]:
    """
    Attempt to fetch entries from RSS feed.
    Returns list of {url, publish_date} dicts or empty list on failure.
    """
    rss_candidates = [
        urljoin(base_url.rstrip("/") + "/", "feed"),
        urljoin(base_url.rstrip("/") + "/", "feed.xml"),
        urljoin(base_url.rstrip("/") + "/", "rss.xml"),
        urljoin(base_url.rstrip("/") + "/", "blog/feed"),
    ]

    for rss_url in rss_candidates:
        try:
            req = Request(rss_url, headers={"User-Agent": "SovereignBot/1.0 (research)"})
            with urlopen(req, timeout=timeout) as resp:
                content = resp.read().decode("utf-8", errors="replace")
            urls = re.findall(r"<link>(https?://[^<]+)</link>", content)
            dates = re.findall(r"<pubDate>([^<]+)</pubDate>", content)
            entries = []
            for i, url in enumerate(urls):
                entries.append({
                    "url": url.strip(),
                    "publish_date": dates[i].strip() if i < len(dates) else None,
                })
            if entries:
                return entries
        except Exception:
            continue
    return []


def detect_delta(slug: str, competitor_url: str, sync_status: dict) -> dict:
    """
    Detect what has changed for a single competitor since last sync.

    Returns:
        {
            new_urls: [...],
            updated_urls: [...],
            deleted_urls: [...],
            source: "sitemap" | "rss" | "failed",
            error: None | str
        }
    """
    known_hashes = sync_status.get("url_hashes", {})
    known_urls = set(known_hashes.keys())

    # Step 1: Try sitemap
    live_urls = fetch_sitemap(competitor_url)
    source = "sitemap"

    # Step 2: Fallback to RSS if sitemap failed
    if not live_urls:
        rss_entries = fetch_rss(competitor_url)
        live_urls = [e["url"] for e in rss_entries]
        source = "rss"

    # Step 3: Mark as stale if both failed
    if not live_urls:
        return {
            "new_urls": [],
            "updated_urls": [],
            "deleted_urls": [],
            "source": "failed",
            "error": "Both sitemap and RSS unavailable",
        }

    live_url_set = set(live_urls)

    # Calculate delta
    new_urls = [u for u in live_urls if u not in known_urls]
    deleted_urls = [u for u in known_urls if u not in live_url_set]

    # Filter new_urls: only include if not seen in last 24h (avoid false positives)
    cutoff = datetime.now(timezone.utc) - timedelta(hours=MIN_DELTA_AGE_HOURS)
    last_sync_str = sync_status.get("last_sync")
    if last_sync_str:
        try:
            last_sync = datetime.fromisoformat(last_sync_str)
            # Only treat as delta if last sync was > 24h ago, or URL is truly new
            if (datetime.now(timezone.utc) - last_sync) < timedelta(hours=MIN_DELTA_AGE_HOURS):
                new_urls = []  # Too recent — likely false positives
        except ValueError:
            pass

    return {
        "new_urls": new_urls[:50],      # Cap at 50 new URLs per run
        "updated_urls": [],             # Full update detection requires content comparison
        "deleted_urls": deleted_urls[:20],
        "source": source,
        "error": None,
    }


def detect_all_deltas(scope: str = "all") -> dict:
    """
    Detect deltas for all sync-enabled competitors.

    Args:
        scope: "all" | "blog" | "projects" — filters by content type if specified

    Returns:
        {competitor_slug: delta_payload, ...}
    """
    index = load_index()
    competitors = [c for c in index.get("competitors", []) if c.get("sync_enabled", True)]
    all_deltas = {}

    for comp in competitors:
        # Backward/forward compatibility:
        # - legacy: slug/url
        # - current index: id/website
        slug = comp.get("slug") or comp.get("id")
        url = comp.get("url") or comp.get("website")
        if not slug or not url:
            continue

        sync_status = load_sync_status(slug)
        delta = detect_delta(slug, url, sync_status)

        # Filter by scope if specified
        if scope == "blog":
            delta["new_urls"] = [u for u in delta["new_urls"] if "/blog/" in u or "/post/" in u or "/news/" in u]
        elif scope == "projects":
            project_markers = (
                "/project/",
                "/projects/",
                "/work/",
                "/portfolio/",
                "/properties/",
                "/property/",
                "/development/",
                "/developments/",
                "/listing/",
                "/listings/",
            )
            delta["new_urls"] = [u for u in delta["new_urls"] if any(marker in u.lower() for marker in project_markers)]

        all_deltas[slug] = delta

    return all_deltas


def build_delta_payload(delta_results: dict) -> dict:
    """
    Format delta results into the standard payload for scraper_engine.py.
    """
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_new_urls": sum(len(d["new_urls"]) for d in delta_results.values()),
        "total_deleted_urls": sum(len(d["deleted_urls"]) for d in delta_results.values()),
        "competitors": {}
    }

    for slug, delta in delta_results.items():
        if delta.get("error"):
            payload["competitors"][slug] = {
                "status": "stale",
                "error": delta["error"],
                "new_urls": [],
                "updated_urls": [],
                "deleted_urls": [],
            }
        else:
            payload["competitors"][slug] = {
                "status": "ok",
                "source": delta["source"],
                "new_urls": delta["new_urls"],
                "updated_urls": delta.get("updated_urls", []),
                "deleted_urls": delta.get("deleted_urls", []),
            }

    return payload


if __name__ == "__main__":
    print("Running delta detection for all sync-enabled competitors...")
    deltas = detect_all_deltas()
    payload = build_delta_payload(deltas)
    print(json.dumps(payload, indent=2))
