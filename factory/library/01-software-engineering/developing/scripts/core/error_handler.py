"""
error_handler.py — Sovereign Error Cascade Handler
==================================================
Implements the error recovery cascade defined in .ai/error-recovery.md.
Every error has a single owner, max 3 retries, and a defined fallback.

Owner: guide-agent (coordinates); individual agents own their error domains
"""

import json
import sys
import time
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path

_scripts = Path(__file__).resolve().parent
while _scripts.name != "scripts" and _scripts != _scripts.parent:
    _scripts = _scripts.parent
if not (_scripts / "paths.py").is_file():
    raise RuntimeError("Expected .ai/scripts/paths.py — run from Sovereign workspace.")
if str(_scripts) not in sys.path:
    sys.path.insert(0, str(_scripts))

from paths import REPO_ROOT, logs_dir  # noqa: E402

WORKSPACE_ROOT = REPO_ROOT
WORKFLOW_LOG = logs_dir() / "workflow.jsonl"

MAX_RETRIES = 3


class ErrorSeverity(Enum):
    SKIP = "skip"          # Skip item, continue with others
    RETRY = "retry"        # Retry with backoff
    FALLBACK = "fallback"  # Apply fallback strategy
    HALT = "halt"          # Stop command, alert user
    ROLLBACK = "rollback"  # Undo writes, preserve old state


def log_error(agent: str, intent: str, error_type: str, message: str,
              url: str = None, file_path: str = None, attempt: int = 1) -> None:
    """Log an error to workflow.jsonl."""
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": "error",
        "agent": agent,
        "intent": intent,
        "error_type": error_type,
        "message": message,
        "url": url,
        "file_path": file_path,
        "attempt": attempt,
    }
    WORKFLOW_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(WORKFLOW_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")


def backoff_delay(attempt: int) -> None:
    """Exponential backoff: 5s, 10s, 20s."""
    delays = {1: 5, 2: 10, 3: 20}
    time.sleep(delays.get(attempt, 20))


def handle_http_error(status_code: int, url: str, agent: str,
                      intent: str, attempt: int) -> dict:
    """
    Handle HTTP errors during scraping.
    Returns {action: ErrorSeverity, message: str, user_facing: str|None}
    """
    if status_code == 429:
        log_error(agent, intent, "http_429", f"Rate limited on {url}", url=url, attempt=attempt)
        if attempt < MAX_RETRIES:
            backoff_delay(attempt)
            return {"action": ErrorSeverity.RETRY, "message": f"429 on {url}. Retrying (attempt {attempt+1}).", "user_facing": None}
        else:
            return {
                "action": ErrorSeverity.SKIP,
                "message": f"429 on {url} after {MAX_RETRIES} attempts. Skipped.",
                "user_facing": f"⚠️ {url.split('/')[2]} is rate-limiting requests. Some content skipped.",
            }

    elif status_code == 403:
        log_error(agent, intent, "http_403", f"Access denied: {url}", url=url)
        return {"action": ErrorSeverity.SKIP, "message": f"403 on {url}. Skipped.", "user_facing": None}

    elif status_code == 404:
        log_error(agent, intent, "http_404", f"Not found: {url}", url=url)
        return {"action": ErrorSeverity.SKIP, "message": f"404 on {url}. Treating as deleted.", "user_facing": None}

    elif status_code >= 500:
        log_error(agent, intent, f"http_{status_code}", f"Server error: {url}", url=url, attempt=attempt)
        if attempt < MAX_RETRIES:
            backoff_delay(attempt)
            return {"action": ErrorSeverity.RETRY, "message": f"{status_code} on {url}. Retrying.", "user_facing": None}
        return {"action": ErrorSeverity.SKIP, "message": f"{status_code} on {url}. Skipped after retries.", "user_facing": None}

    return {"action": ErrorSeverity.SKIP, "message": f"HTTP {status_code} on {url}.", "user_facing": None}


def handle_robots_block(url: str, agent: str, intent: str) -> dict:
    """robots.txt block — never retry, always skip."""
    log_error(agent, intent, "robots_blocked", f"robots.txt blocks {url}", url=url)
    return {
        "action": ErrorSeverity.SKIP,
        "message": f"robots.txt blocks {url}. Skipped (ethics compliance).",
        "user_facing": f"Path blocked by robots.txt. Skipped in compliance with site rules.",
    }


def handle_parse_error(url: str, html_content: str, agent: str,
                       intent: str, attempt: int) -> dict:
    """Handle malformed HTML parse failures."""
    log_error(agent, intent, "parse_error", f"Failed to parse {url}", url=url, attempt=attempt)
    if attempt == 1:
        return {"action": ErrorSeverity.RETRY, "message": f"Parse failed on {url}. Retrying with alternate parser.", "user_facing": None}
    return {"action": ErrorSeverity.SKIP, "message": f"Parse failed on {url} after retry. Skipped.", "user_facing": None}


def handle_write_failure(file_path: str, agent: str, intent: str,
                         attempt: int, backup_path: str = None) -> dict:
    """Handle file write failures with rollback logic."""
    log_error(agent, intent, "write_failure", f"Failed to write {file_path}", file_path=file_path, attempt=attempt)

    if attempt < MAX_RETRIES:
        return {"action": ErrorSeverity.RETRY, "message": f"Write failed for {file_path}. Retrying.", "user_facing": None}

    # After max retries: rollback if backup exists
    if backup_path and Path(backup_path).exists():
        return {
            "action": ErrorSeverity.ROLLBACK,
            "message": f"Write failed {MAX_RETRIES}x for {file_path}. Rolling back to {backup_path}.",
            "user_facing": f"⚠️ Could not save changes to {Path(file_path).name}. Rolled back to previous version. Try again.",
        }

    return {
        "action": ErrorSeverity.HALT,
        "message": f"Write failed {MAX_RETRIES}x for {file_path} with no backup.",
        "user_facing": f"❌ Could not save {Path(file_path).name}. Check disk space or permissions.",
    }


def handle_quality_gate_failure(gate_name: str, score: float,
                                threshold: float, attempt: int) -> dict:
    """Handle quality gate failures with retry recommendations."""
    log_error("quality-checker", "review", "gate_failure",
              f"{gate_name} gate failed: {score:.0%} < {threshold:.0%}", attempt=attempt)

    fix_commands = {
        "seo": "/polish content in content/",
        "brand_voice": "/revise [improve tone to match brand voice rules]",
        "readability": "/revise [simplify sentences for readability]",
        "image_seo": "/optimize images in content/",
        "originality": "/revise [rewrite with a different structural approach]",
    }

    return {
        "action": ErrorSeverity.FALLBACK,
        "gate": gate_name,
        "score": score,
        "threshold": threshold,
        "fix_command": fix_commands.get(gate_name, "/revise [feedback]"),
        "user_facing": (
            f"❌ {gate_name.replace('_', ' ').title()} gate failed: "
            f"{score:.0%} (required: {threshold:.0%}). "
            f"Fix with: {fix_commands.get(gate_name, '/revise [feedback]')}"
        ),
    }


def handle_originality_failure(similarity_score: float, flagged_passages: list,
                                attempt: int) -> dict:
    """Handle content originality failures."""
    log_error("content-generator", "create", "originality_failure",
              f"Similarity {similarity_score:.0%} > 15%", attempt=attempt)

    if attempt <= 2:
        return {
            "action": ErrorSeverity.RETRY,
            "message": f"Similarity {similarity_score:.0%}. Rewriting with structural shift (attempt {attempt+1}).",
            "user_facing": None,  # Silent auto-retry
        }

    return {
        "action": ErrorSeverity.FALLBACK,
        "message": f"Similarity {similarity_score:.0%} after {attempt} attempts.",
        "user_facing": (
            f"⚠️ Content is {similarity_score:.0%} similar to existing sources after {attempt} attempts. "
            f"Use `/revise [describe a completely different angle or structure]` to guide a fresh approach."
        ),
        "flagged_passages": flagged_passages[:3],  # Surface top 3 for user
    }


def handle_brand_voice_failure(tone_score: float, drift_flags: list,
                                attempt: int) -> dict:
    """Handle brand voice compliance failures."""
    log_error("brand-voice-applier", "create", "brand_voice_failure",
              f"Tone score {tone_score:.0%} < 92%", attempt=attempt)

    if attempt <= 2:
        return {
            "action": ErrorSeverity.RETRY,
            "message": f"Tone {tone_score:.0%}. Reapplying stricter voice matrix (attempt {attempt+1}).",
            "user_facing": None,
        }

    violations_summary = "; ".join([f.get("rule_violated", "") for f in drift_flags[:3]])
    return {
        "action": ErrorSeverity.FALLBACK,
        "message": f"Tone {tone_score:.0%} after {attempt} attempts. Flagged for review.",
        "user_facing": (
            f"⚠️ Brand voice at {tone_score:.0%} (required: 92%) after {attempt} attempts. "
            f"Top violations: {violations_summary}. "
            f"Run `/refine brand voice` to update rules, then `/revise` with tone guidance."
        ),
        "drift_flags": drift_flags,
    }


def handle_competitor_not_found(name: str) -> dict:
    """Handle missing competitor in registry."""
    return {
        "action": ErrorSeverity.HALT,
        "user_facing": (
            f"❌ Competitor '{name}' not found in the registry. "
            f"Run `/research competitors` to discover and add them, "
            f"or `/scrape {name} all website` if you know their URL."
        ),
    }


def handle_no_content_for_review() -> dict:
    """Handle /review with no staged content."""
    return {
        "action": ErrorSeverity.HALT,
        "user_facing": (
            "❌ Nothing staged for review. "
            "Run `/create [type]` to generate content first, "
            "then `/polish content in content/` before reviewing."
        ),
    }


def summarize_errors(error_log: list) -> str:
    """Generate a human-readable error summary from a list of error entries."""
    if not error_log:
        return "No errors."

    skipped = [e for e in error_log if e.get("action") == "skip"]
    retried = [e for e in error_log if e.get("action") == "retry"]
    halted = [e for e in error_log if e.get("action") == "halt"]

    parts = []
    if skipped:
        parts.append(f"{len(skipped)} item(s) skipped (see .ai/logs/workflow.jsonl for details)")
    if retried:
        parts.append(f"{len(retried)} item(s) required retries")
    if halted:
        parts.append(f"⚠️ {len(halted)} critical error(s) — manual action needed")

    return " | ".join(parts) if parts else "Minor errors logged."
