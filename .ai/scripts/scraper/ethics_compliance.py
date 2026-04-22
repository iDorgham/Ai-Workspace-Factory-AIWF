"""
ethics_compliance.py — Sovereign Ethics & Compliance Layer
==========================================================
Enforces robots.txt, rate limiting, and PII filtering.
RESPONSIBILITY: ONLY robots.txt parsing, rate limiting, PII filtering.
Does NOT detect deltas, does NOT write sync-status.json.

Owner: scraper-agent / ethical-crawler sub-agent
"""

import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

_scripts = Path(__file__).resolve().parent
while _scripts.name != "scripts" and _scripts != _scripts.parent:
    _scripts = _scripts.parent
if not (_scripts / "paths.py").is_file():
    raise RuntimeError("Expected .ai/scripts/paths.py — run from Sovereign workspace.")
if str(_scripts) not in sys.path:
    sys.path.insert(0, str(_scripts))

from paths import REPO_ROOT, logs_dir  # noqa: E402

WORKSPACE_ROOT = REPO_ROOT
SCRAPE_AUDIT_LOG = logs_dir() / "scrape-audit.jsonl"

# Rate limiting
DEFAULT_DELAY_SECONDS = 2.0
BACKOFF_DELAYS = [5, 10, 20]  # On 429 retry delays

# PII patterns to redact before saving
PII_PATTERNS = [
    (re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"), "[EMAIL REDACTED]"),
    (re.compile(r"\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"), "[PHONE REDACTED]"),
    (re.compile(r"\b\d{1,5}\s+[A-Za-z0-9\s,\.]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Drive|Dr)\b", re.IGNORECASE), "[ADDRESS REDACTED]"),
]

# Cache for robots.txt rules per domain
_robots_cache: dict[str, list] = {}
_last_request_times: dict[str, float] = {}


def get_domain(url: str) -> str:
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}"


def fetch_robots_txt(domain: str, timeout: int = 5) -> str:
    """Fetch and return robots.txt content for a domain."""
    robots_url = f"{domain}/robots.txt"
    try:
        req = Request(robots_url, headers={"User-Agent": "SovereignBot/1.0"})
        with urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception:
        return ""  # If robots.txt unavailable, assume allowed (conservative)


def parse_robots_txt(content: str, user_agent: str = "SovereignBot") -> list[str]:
    """
    Parse robots.txt and return list of disallowed paths for our bot.
    Returns list of disallowed path prefixes.
    """
    disallowed = []
    current_agent = None
    applies_to_us = False

    for line in content.splitlines():
        line = line.strip().lower()
        if line.startswith("user-agent:"):
            agent = line.split(":", 1)[1].strip()
            current_agent = agent
            applies_to_us = (agent == "*" or agent == user_agent.lower())
        elif line.startswith("disallow:") and applies_to_us:
            path = line.split(":", 1)[1].strip()
            if path:
                disallowed.append(path)

    return disallowed


def is_url_allowed(url: str) -> bool:
    """
    Check if a URL is allowed for scraping based on robots.txt.
    Returns True if allowed, False if blocked.
    """
    domain = get_domain(url)
    parsed = urlparse(url)
    path = parsed.path

    # Cache robots.txt per domain
    if domain not in _robots_cache:
        robots_content = fetch_robots_txt(domain)
        _robots_cache[domain] = parse_robots_txt(robots_content)

    disallowed_paths = _robots_cache[domain]

    for disallowed in disallowed_paths:
        if path.startswith(disallowed) or disallowed == "/":
            return False
    return True


def enforce_rate_limit(domain: str) -> None:
    """Enforce minimum delay between requests to the same domain."""
    now = time.time()
    last = _last_request_times.get(domain, 0)
    elapsed = now - last
    if elapsed < DEFAULT_DELAY_SECONDS:
        time.sleep(DEFAULT_DELAY_SECONDS - elapsed)
    _last_request_times[domain] = time.time()


def filter_pii(text: str) -> tuple[str, int]:
    """
    Remove PII from text content.
    Returns (cleaned_text, count_of_redactions).
    """
    redactions = 0
    for pattern, replacement in PII_PATTERNS:
        matches = pattern.findall(text)
        redactions += len(matches)
        text = pattern.sub(replacement, text)
    return text, redactions


def check_compliance(url: str) -> dict:
    """
    Full compliance check for a single URL.
    Returns {allowed: bool, reason: str, domain: str}
    """
    domain = get_domain(url)

    if not is_url_allowed(url):
        log_compliance(url, domain, allowed=False, reason="robots_disallowed")
        return {"allowed": False, "reason": "robots.txt disallows this path", "domain": domain}

    log_compliance(url, domain, allowed=True, reason="ok")
    return {"allowed": True, "reason": "ok", "domain": domain}


def prepare_ethical_fetch(url: str) -> dict:
    """
    Full pre-fetch compliance pipeline: robots check + rate limit enforcement.
    Returns {proceed: bool, reason: str}
    """
    compliance = check_compliance(url)
    if not compliance["allowed"]:
        return {"proceed": False, "reason": compliance["reason"]}

    # Enforce rate limit
    enforce_rate_limit(compliance["domain"])

    return {"proceed": True, "reason": "ok"}


def sanitize_scraped_content(content: str, url: str) -> dict:
    """
    Apply PII filtering to scraped content.
    Returns {clean_content: str, pii_removed: int, url: str}
    """
    clean, count = filter_pii(content)
    if count > 0:
        log_pii_redaction(url, count)
    return {
        "clean_content": clean,
        "pii_removed": count,
        "url": url,
    }


def log_compliance(url: str, domain: str, allowed: bool, reason: str) -> None:
    """Log compliance check result to scrape-audit.jsonl."""
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": "compliance_check",
        "url": url,
        "domain": domain,
        "allowed": allowed,
        "reason": reason,
    }
    _write_audit_log(entry)


def log_pii_redaction(url: str, count: int) -> None:
    """Log PII redaction event."""
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": "pii_redacted",
        "url": url,
        "count": count,
    }
    _write_audit_log(entry)


def _write_audit_log(entry: dict) -> None:
    SCRAPE_AUDIT_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(SCRAPE_AUDIT_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")


def batch_compliance_check(urls: list[str]) -> dict[str, dict]:
    """Check compliance for a batch of URLs. Returns {url: compliance_result}."""
    return {url: check_compliance(url) for url in urls}
