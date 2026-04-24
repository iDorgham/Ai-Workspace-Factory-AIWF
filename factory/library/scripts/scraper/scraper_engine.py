"""
scraper_engine.py — Sovereign Ethical Scraper Engine
====================================================
Fetches delta URLs, converts HTML to structured Markdown.
Calls ethics_compliance before every fetch.
sync-status.json is written ONLY by sync_state_writer() at the end.

Owner: scraper-agent
Authoritative writer of: content/<active_project>/scraped/*/scraped/content/*, per-slug sync-status.json (via sync_state_writer)
"""

import hashlib
import json
import re
import sys
import time
import html as html_lib
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

_scraper_dir = Path(__file__).resolve().parent
if str(_scraper_dir) not in sys.path:
    sys.path.insert(0, str(_scraper_dir))

_scripts = _scraper_dir
while _scripts.name != "scripts" and _scripts != _scripts.parent:
    _scripts = _scripts.parent
if not (_scripts / "paths.py").is_file():
    raise RuntimeError("Expected .ai/scripts/paths.py — run from Sovereign workspace.")
if str(_scripts) not in sys.path:
    sys.path.insert(0, str(_scripts))

from paths import REPO_ROOT, logs_dir, project_scraped_dir  # noqa: E402

from delta_detector import build_delta_payload, detect_all_deltas  # noqa: E402
from ethics_compliance import prepare_ethical_fetch, sanitize_scraped_content  # noqa: E402

WORKSPACE_ROOT = REPO_ROOT
SYNC_LOG = logs_dir() / "sync-delta.jsonl"

HEADERS = {
    "User-Agent": "SovereignBot/1.0 (competitive research; contact@sovereign.studio)",
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": "en-US,en;q=0.9",
}

PROJECT_URL_MARKERS = (
    "/project/",
    "/projects/",
    "/work/",
    "/portfolio/",
    "/case-study/",
    "/property/",
    "/properties/",
    "/development/",
    "/developments/",
    "/listing/",
    "/listings/",
)

NOISE_HEADING_PATTERNS = (
    "schedule a tour",
    "your information",
    "contact us",
    "contact me",
    "compare listings",
    "want to find out more",
    "sign into your account",
    "reset password",
    "virtual tour",
    "video chat",
)

NOISE_LINE_PATTERNS = (
    "facebook",
    "twitter",
    "pinterest",
    "whatsapp",
    "favorite",
    "print",
    "login",
    "register",
    "forgot password",
    "gdpr terms",
    "welcome to your real estate website",
    "create an account",
    "a password will be e-mailed to you",
)

ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg"}


def fetch_url(url: str, timeout: int = 10) -> tuple[str | None, int]:
    """
    Fetch a URL with ethics compliance pre-check.
    Returns (html_content | None, status_code).
    """
    compliance = prepare_ethical_fetch(url)
    if not compliance["proceed"]:
        return None, 0  # 0 = blocked (not an HTTP error)

    try:
        req = Request(url, headers=HEADERS)
        with urlopen(req, timeout=timeout) as resp:
            html = resp.read().decode("utf-8", errors="replace")
            return html, resp.status
    except HTTPError as e:
        return None, e.code
    except URLError:
        return None, -1  # Network failure


def extract_project_links_from_homepage(base_url: str, html: str, max_links: int = 100) -> list[str]:
    """
    Extract project-like links from a homepage fallback crawl.
    Used when delta detection returns no project URLs.
    """
    hrefs = re.findall(r'href=["\']([^"\']+)["\']', html, re.IGNORECASE)
    candidates: list[str] = []
    seen = set()
    for href in hrefs:
        absolute = urljoin(base_url, href.strip())
        absolute_lower = absolute.lower()
        if not absolute_lower.startswith(("http://", "https://")):
            continue
        if any(marker in absolute_lower for marker in PROJECT_URL_MARKERS):
            if absolute not in seen:
                candidates.append(absolute)
                seen.add(absolute)
        if len(candidates) >= max_links:
            break
    return candidates


def html_to_markdown(html: str, url: str) -> dict:
    """
    Convert HTML to structured Markdown with metadata extraction.
    Simple implementation — production would use a proper HTML parser.
    """
    # Extract title
    title_match = re.search(r"<title[^>]*>([^<]+)</title>", html, re.IGNORECASE)
    title = title_match.group(1).strip() if title_match else "Untitled"

    # Extract meta description
    meta_match = re.search(
        r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']',
        html, re.IGNORECASE
    )
    meta_desc = meta_match.group(1).strip() if meta_match else ""

    # Extract publish date (common patterns)
    date_patterns = [
        r'<meta\s+property=["\']article:published_time["\']\s+content=["\']([\d\-T:Z+]+)["\']',
        r'"datePublished"\s*:\s*"([\d\-T:Z+]+)"',
        r'<time[^>]+datetime=["\']([\d\-T:Z+]+)["\']',
    ]
    publish_date = None
    for pattern in date_patterns:
        match = re.search(pattern, html, re.IGNORECASE)
        if match:
            publish_date = match.group(1)
            break

    # Strip low-value HTML regions first
    body = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL | re.IGNORECASE)
    body = re.sub(r"<style[^>]*>.*?</style>", "", body, flags=re.DOTALL | re.IGNORECASE)
    body = re.sub(r"<nav[^>]*>.*?</nav>", "", body, flags=re.DOTALL | re.IGNORECASE)
    body = re.sub(r"<footer[^>]*>.*?</footer>", "", body, flags=re.DOTALL | re.IGNORECASE)
    body = re.sub(r"<header[^>]*>.*?</header>", "", body, flags=re.DOTALL | re.IGNORECASE)
    body = re.sub(r"<aside[^>]*>.*?</aside>", "", body, flags=re.DOTALL | re.IGNORECASE)
    body = re.sub(r"<form[^>]*>.*?</form>", "", body, flags=re.DOTALL | re.IGNORECASE)

    # Normalize common blocks and list items before stripping tags
    body = re.sub(r"<br\s*/?>", "\n", body, flags=re.IGNORECASE)
    body = re.sub(r"<li[^>]*>(.*?)</li>", r"\n- \1\n", body, flags=re.IGNORECASE | re.DOTALL)
    body = re.sub(r"</(p|div|section|article|ul|ol|table|tr)>", "\n", body, flags=re.IGNORECASE)

    # Convert headings to markdown with line boundaries
    for level in range(6, 0, -1):
        body = re.sub(
            rf"<h{level}[^>]*>(.*?)</h{level}>",
            lambda m, l=level: f"\n{'#' * l} {re.sub('<[^>]+>', '', m.group(1)).strip()}\n",
            body,
            flags=re.IGNORECASE | re.DOTALL,
        )

    # Extract image references (absolute + relative)
    raw_img_srcs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html, re.IGNORECASE)
    img_srcs: list[str] = []
    for src in raw_img_srcs:
        src_clean = src.strip()
        if not src_clean or src_clean.startswith(("data:", "javascript:", "mailto:")):
            continue
        absolute = urljoin(url, src_clean)
        if absolute.startswith(("http://", "https://")):
            img_srcs.append(absolute)

    # Strip remaining tags, decode entities, and preserve structure by line
    body = re.sub(r"<[^>]+>", "", body)
    body = html_lib.unescape(body)
    body = re.sub(r"\r\n?", "\n", body)

    lines = [re.sub(r"[ \t]+", " ", ln).strip() for ln in body.split("\n")]
    lines = [ln for ln in lines if ln]

    # Start from first meaningful heading to avoid top-nav leftovers.
    first_heading_idx = next((i for i, ln in enumerate(lines) if ln.startswith("# ")), None)
    if first_heading_idx is not None:
        lines = lines[first_heading_idx:]

    # De-duplicate adjacent repeated lines.
    deduped: list[str] = []
    for ln in lines:
        if deduped and deduped[-1] == ln:
            continue
        deduped.append(ln)

    # Organize content into sections with markdown headings.
    sectioned: list[str] = []
    active_section = False
    skip_section = False
    seen_headings: set[str] = set()
    host = urlparse(url).netloc.lower().replace("www.", "")
    for ln in deduped:
        is_heading = ln.startswith("#")
        if is_heading:
            heading_text = re.sub(r"^#+\s*", "", ln).strip().lower()
            if host and host in heading_text:
                skip_section = True
                continue
            if heading_text in seen_headings:
                skip_section = True
                continue
            seen_headings.add(heading_text)
            if any(p in heading_text for p in NOISE_HEADING_PATTERNS):
                skip_section = True
                continue
            skip_section = False
            if sectioned and sectioned[-1] != "":
                sectioned.append("")
            sectioned.append(ln)
            active_section = True
            continue

        if skip_section:
            continue
        if any(p in ln.lower() for p in NOISE_LINE_PATTERNS):
            continue

        # Ensure non-heading text lives under a section.
        if not active_section:
            sectioned.append("## Content")
            sectioned.append("")
            active_section = True

        sectioned.append(ln)

    body = "\n".join(sectioned).strip()

    word_count = len(body.split())

    return {
        "url": url,
        "title": title,
        "meta_description": meta_desc,
        "publish_date": publish_date,
        "word_count": word_count,
        # Keep full body to support full project-content scraping.
        "body_markdown": body,
        "image_refs": img_srcs,
    }


def url_to_slug(url: str) -> str:
    """Convert a URL to a safe file slug."""
    from urllib.parse import urlparse
    parsed = urlparse(url)
    path = parsed.path.rstrip("/").replace("/", "-").lstrip("-")
    return re.sub(r"[^a-z0-9\-]", "", path.lower()) or "index"


def detect_content_type(url: str) -> str:
    """Infer content type from URL pattern."""
    url_lower = url.lower()
    if any(k in url_lower for k in ["/blog/", "/post/", "/article/", "/news/"]):
        return "blog"
    if any(k in url_lower for k in [
        "/project/", "/projects/",
        "/work/", "/portfolio/", "/case-study/",
        "/property/", "/properties/",
        "/development/", "/developments/",
        "/listing/", "/listings/",
    ]):
        return "projects"
    return "pages"


def _sanitize_filename(name: str) -> str:
    """Sanitize arbitrary text into a safe filename fragment."""
    return re.sub(r"[^a-zA-Z0-9._-]", "-", name).strip("-") or "file"


def _download_images(image_urls: list[str], destination_dir: Path, timeout: int = 15) -> tuple[list[str], list[dict]]:
    """
    Download image URLs to destination_dir.
    Returns (saved_paths, errors).
    """
    destination_dir.mkdir(parents=True, exist_ok=True)
    saved_paths: list[str] = []
    errors: list[dict] = []

    for i, image_url in enumerate(image_urls, start=1):
        try:
            req = Request(image_url, headers=HEADERS)
            with urlopen(req, timeout=timeout) as resp:
                mime = resp.headers.get_content_type() if hasattr(resp, "headers") else ""
                parsed_url = urlparse(image_url)
                source_name = Path(parsed_url.path).name
                source_name = _sanitize_filename(source_name) if source_name else ""

                ext = ""
                if "." in source_name:
                    ext = source_name.split(".")[-1].lower()
                elif mime.startswith("image/"):
                    ext = mime.split("/", 1)[1].lower()

                # Restrict saved image files to png/jpg/jpeg only.
                # If source is another format (e.g. avif/webp), keep bytes as-is
                # but normalize extension for workspace consistency.
                if ext == "jpeg":
                    ext = "jpg"
                if ext not in ALLOWED_IMAGE_EXTENSIONS:
                    ext = "jpg"

                filename = f"image_{i:03d}.{ext}"
                file_path = destination_dir / filename

                file_path.write_bytes(resp.read())
                saved_paths.append(str(file_path))
        except Exception as e:
            errors.append({"url": image_url, "reason": str(e)})

    return saved_paths, errors


def save_scraped_content(slug: str, content_type: str,
                         parsed: dict, attempt_version: int = 1) -> tuple[str, list[str], list[dict]]:
    """
    Save parsed content as Markdown file.
    Versions file if it already exists (_v2.md, _v3.md).
    Returns saved file path.
    """
    base_dir = project_scraped_dir() / slug / "scraped" / "content" / content_type
    base_dir.mkdir(parents=True, exist_ok=True)

    file_slug = url_to_slug(parsed["url"])
    image_paths: list[str] = []
    image_errors: list[dict] = []

    # Project scraping layout:
    # content/<project>/scraped/<slug>/scraped/content/projects/<project-slug>/{content.md, images/*}
    if content_type == "projects":
        project_dir = base_dir / file_slug
        project_dir.mkdir(parents=True, exist_ok=True)
        file_path = project_dir / "content.md"
        images_dir = project_dir / "images"
    else:
        file_path = base_dir / f"{file_slug}.md"
        if file_path.exists():
            v = 2
            while (base_dir / f"{file_slug}_v{v}.md").exists():
                v += 1
            file_path = base_dir / f"{file_slug}_v{v}.md"
        images_dir = None

    frontmatter = f"""---
url: "{parsed['url']}"
title: "{parsed['title']}"
meta_description: "{parsed['meta_description']}"
publish_date: "{parsed.get('publish_date', '')}"
word_count: {parsed['word_count']}
scraped_at: "{datetime.now(timezone.utc).isoformat()}"
content_type: "{content_type}"
competitor_slug: "{slug}"
---

"""
    if content_type == "projects":
        image_paths, image_errors = _download_images(parsed.get("image_refs", []), images_dir)
        image_list = "\n".join([f"- {Path(p).name}" for p in image_paths]) if image_paths else "_No images downloaded._"
        content = (
            frontmatter
            + f"# {parsed['title']}\n\n"
            + parsed["body_markdown"]
            + "\n\n## Downloaded Images\n\n"
            + image_list
            + "\n"
        )
    else:
        content = frontmatter + f"# {parsed['title']}\n\n{parsed['body_markdown']}"
    file_path.write_text(content, encoding="utf-8")
    return str(file_path), image_paths, image_errors


def run_scrape(scope: str = "all", competitor_slug: str = None) -> dict:
    """
    Main scrape execution: detect deltas → fetch → parse → save.

    Args:
        scope: "blog" | "projects" | "all"
        competitor_slug: If set, scrape only this competitor

    Returns:
        Scrape results dict for sync_state_writer
    """
    # Detect deltas
    all_deltas = detect_all_deltas(scope)

    # Filter to single competitor if specified
    if competitor_slug:
        all_deltas = {k: v for k, v in all_deltas.items() if k == competitor_slug}

    delta_payload = build_delta_payload(all_deltas)

    results = {}
    total_scraped = 0
    total_errors = 0

    for slug, delta in delta_payload["competitors"].items():
        if delta.get("status") == "stale":
            results[slug] = {"files_written": 0, "errors": [delta.get("error")], "status": "stale"}
            continue

        urls_to_fetch = delta.get("new_urls", []) + delta.get("updated_urls", [])
        if scope == "projects" and not urls_to_fetch:
            # Fallback for project scraping: extract project links from homepage
            # so "/scrape all competitors projects" can still collect content
            # even when sitemap/RSS deltas are empty.
            website = all_deltas.get(slug, {}).get("base_url")
            if not website:
                # best-effort: infer base from first known URL fields if present
                website = ""
            # If base URL is unavailable from delta payload, derive from index.
            if not website:
                index_path = project_scraped_dir() / "index.json"
                if index_path.exists():
                    try:
                        index_data = json.loads(index_path.read_text(encoding="utf-8"))
                        comp = next((c for c in index_data.get("competitors", []) if (c.get("id") or c.get("slug")) == slug), None)
                        website = (comp or {}).get("website") or (comp or {}).get("url") or ""
                    except Exception:
                        website = ""
            if website:
                home_html, home_status = fetch_url(website)
                if home_html:
                    urls_to_fetch = extract_project_links_from_homepage(website, home_html)
                elif home_status not in (200,):
                    errors.append({"url": website, "status": home_status, "reason": "homepage_fetch_failed"})
        files_written = []
        errors = []

        for url in urls_to_fetch:
            content_type = detect_content_type(url)
            html, status = fetch_url(url)

            if html is None:
                errors.append({"url": url, "status": status, "reason": "fetch_failed"})
                total_errors += 1
                continue

            # Sanitize PII
            sanitized = sanitize_scraped_content(html, url)
            html_clean = sanitized["clean_content"]

            # Parse to Markdown
            parsed = html_to_markdown(html_clean, url)

            # Save
            try:
                saved_path, image_paths, image_errors = save_scraped_content(slug, content_type, parsed)
                files_written.append(saved_path)
                if image_paths:
                    files_written.extend(image_paths)
                if image_errors:
                    errors.extend([{"url": url, "reason": "image_download_failed", "details": image_errors}])
                total_scraped += 1
            except Exception as e:
                errors.append({"url": url, "reason": str(e)})
                total_errors += 1

        results[slug] = {
            "files_written": len(files_written),
            "file_paths": files_written,
            "errors": errors,
            "status": "ok" if not errors else "partial",
            "new_urls_processed": urls_to_fetch,
            "deleted_urls": delta.get("deleted_urls", []),
        }

    # Write sync state ONLY after all scraping completes
    from sync_state_writer import write_sync_state
    for slug, result in results.items():
        write_sync_state(slug, result, all_deltas.get(slug, {}))

    # Log sync delta
    log_sync_delta(delta_payload, results, scope)

    return {
        "total_scraped": total_scraped,
        "total_errors": total_errors,
        "competitor_results": results,
        "delta_summary": {
            "total_new_urls": delta_payload["total_new_urls"],
        },
    }


def log_sync_delta(delta_payload: dict, results: dict, scope: str) -> None:
    """Append sync run to sync-delta.jsonl."""
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": "sync_completed",
        "scope": scope,
        "competitors_checked": len(delta_payload["competitors"]),
        "total_new_urls": delta_payload["total_new_urls"],
        "total_files_written": sum(r.get("files_written", 0) for r in results.values()),
        "total_errors": sum(len(r.get("errors", [])) for r in results.values()),
    }
    SYNC_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(SYNC_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")
