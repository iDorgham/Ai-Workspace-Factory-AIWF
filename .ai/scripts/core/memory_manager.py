"""
memory_manager.py — Sovereign Context & Session Memory Manager
=============================================================
Manages context loading, compression, and session state.
CRITICAL RULE: Never loads raw scraped files into LLM context.
Always uses summaries and file pointers from context-cache/.

Owner: guide-agent / memory-manager utility agent
Invoked by: guide-agent before and after every command
"""

import gzip
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

from paths import REPO_ROOT, active_project, project_scraped_dir  # noqa: E402

WORKSPACE_ROOT = REPO_ROOT
STATE_PATH = WORKSPACE_ROOT / ".ai" / "memory" / "state.json"
CACHE_DIR = WORKSPACE_ROOT / ".ai" / "memory" / "context-cache"

def _rel_project_paths():
    p = active_project()
    return p, f"content/{p}/reference", f"content/{p}/scraped", f"content/{p}"


_P, _REF, _SCR, _CONT = _rel_project_paths()

# Files that are ALWAYS safe to load into context (small, structured)
SAFE_CONTEXT_FILES = [
    ".ai/agents.md",
    ".ai/commands.md",
    ".ai/data-ownership.md",
    ".ai/error-recovery.md",
    ".ai/skill-integration.md",
    f"{_REF}/market-positioning.md",
    f"{_REF}/brand-voice/style-rules.md",
    f"{_REF}/brand-voice/glossary.md",
    f"{_REF}/brand-voice/tone-examples.md",
    f"{_SCR}/index.json",
    ".ai/memory/state.json",
]

# Files NEVER to load raw into context
FORBIDDEN_RAW_PATHS = [
    f"{_SCR}/*/scraped/",
    f"{_SCR}/*/scraped/content/",
    f"{_SCR}/*/scraped/images/",
]

def _token_estimates() -> dict:
    _, ref, scr, cont = _rel_project_paths()
    return {
        ".ai/agents.md": 3500,
        ".ai/commands.md": 2000,
        f"{ref}/market-positioning.md": 800,
        f"{ref}/brand-voice/style-rules.md": 2500,
        f"{ref}/brand-voice/glossary.md": 1500,
        f"{ref}/brand-voice/tone-examples.md": 2000,
        f"{scr}/index.json": 500,
        ".ai/memory/state.json": 300,
        f"{cont}/_references/keyword-maps.md": 1200,
    }


def load_state() -> dict:
    if STATE_PATH.exists():
        with open(STATE_PATH) as f:
            return json.load(f)
    return {}


def save_state(state: dict) -> None:
    with open(STATE_PATH, "w") as f:
        json.dump(state, f, indent=2)


def is_forbidden_path(file_path: str) -> bool:
    """Check if a file path is in the forbidden raw-load list."""
    path = Path(file_path)
    path_parts = path.parts
    if "scraped" not in path_parts:
        return False

    raw_markers = {"content", "images"}
    for idx, part in enumerate(path_parts):
        if part != "scraped":
            continue
        # Block raw payload segments like ".../scraped/content/*" or ".../scraped/images/*"
        if idx + 1 < len(path_parts) and path_parts[idx + 1] in raw_markers:
            return True

    for forbidden in FORBIDDEN_RAW_PATHS:
        forbidden_clean = forbidden.replace("*", "")
        if forbidden_clean and forbidden_clean in file_path:
            return True
    return False


def load_context_for_command(intent: str) -> dict:
    """
    Load only the context files needed for the given command intent.
    Scoped loading — never loads everything.

    Returns: {file_path: content, ...} dict + token_estimate
    """
    _, ref, scr, cont = _rel_project_paths()
    scoped_files = {
        "research_competitors": [
            f"{ref}/market-positioning.md",
            f"{scr}/index.json",
            f"{ref}/brand-voice/style-rules.md",
        ],
        "create_blog_posts": [
            f"{ref}/brand-voice/style-rules.md",
            f"{ref}/brand-voice/glossary.md",
            f"{ref}/brand-voice/tone-examples.md",
            f"{cont}/_references/keyword-maps.md",
            f"{ref}/market-positioning.md",
        ],
        "create_website_pages": [
            f"{ref}/brand-voice/style-rules.md",
            f"{ref}/brand-voice/glossary.md",
            f"{ref}/brand-voice/tone-examples.md",
            f"{ref}/market-positioning.md",
        ],
        "create_landing_pages": [
            f"{ref}/brand-voice/style-rules.md",
            f"{ref}/brand-voice/glossary.md",
            f"{ref}/market-positioning.md",
        ],
        "create_project_pages": [
            f"{ref}/brand-voice/style-rules.md",
            f"{ref}/brand-voice/glossary.md",
            f"{ref}/brand-voice/tone-examples.md",
        ],
        "compare": [
            f"{ref}/brand-voice/style-rules.md",
            f"{scr}/index.json",
        ],
        "polish_content": [
            f"{ref}/brand-voice/style-rules.md",
            f"{ref}/brand-voice/glossary.md",
            f"{cont}/_references/keyword-maps.md",
        ],
        "optimize_images": [],
        "extract_brand_voice": [
            f"{ref}/brand-voice/style-rules.md",
        ],
        "refine_brand_voice": [
            f"{ref}/brand-voice/style-rules.md",
            f"{ref}/brand-voice/glossary.md",
        ],
        "review": [
            f"{ref}/brand-voice/style-rules.md",
            f"{cont}/_references/keyword-maps.md",
        ],
        "sync": [f"{scr}/index.json"],
        "scrape_all": [f"{scr}/index.json"],
        "scrape_single": [f"{scr}/index.json"],
        "approve": [],
        "export": [".ai/templates/csv-schemas/content-export.json"],
        "archive": [],
    }

    files_to_load = scoped_files.get(intent, [])
    loaded = {}
    total_tokens = 0

    for file_path in files_to_load:
        if is_forbidden_path(file_path):
            continue  # Never load forbidden paths
        full_path = WORKSPACE_ROOT / file_path
        if full_path.exists():
            try:
                loaded[file_path] = full_path.read_text(encoding="utf-8")
                total_tokens += _token_estimates().get(file_path, len(loaded[file_path]) // 4)
            except Exception:
                pass  # Silently skip unreadable files

    return {"files": loaded, "token_estimate": total_tokens}


def save_context(label: str, data: dict) -> str:
    """
    Compress and save context data to cache.
    Returns cache file path.
    Only summaries and structured data — never raw scraped content.
    """
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    cache_file = CACHE_DIR / f"{label}_{timestamp}.json.gz"

    # Filter out any forbidden paths from data before saving
    safe_data = {k: v for k, v in data.items() if not is_forbidden_path(k)}

    compressed = gzip.compress(json.dumps(safe_data).encode("utf-8"))
    cache_file.write_bytes(compressed)
    return str(cache_file)


def load_cached_context(cache_file: str) -> dict:
    """Load and decompress cached context."""
    path = Path(cache_file)
    if not path.exists():
        return {}
    try:
        compressed = path.read_bytes()
        return json.loads(gzip.decompress(compressed).decode("utf-8"))
    except Exception:
        return {}


def clear_temp_context() -> None:
    """Clear temporary context files after command completes."""
    # Only clears files older than 1 session (not the most recent save)
    if not CACHE_DIR.exists():
        return
    cache_files = sorted(CACHE_DIR.glob("*.json.gz"), key=lambda f: f.stat().st_mtime)
    # Keep the most recent 3 cache files; remove the rest
    for old_file in cache_files[:-3]:
        old_file.unlink(missing_ok=True)


def check_budget(state: dict) -> dict:
    """
    Return current token budget status.
    Warns if >70% used; alerts if >90%.
    """
    session = state.get("session", {})
    token_budget = session.get("token_budget", {})
    used = token_budget.get("used", 0)
    total = token_budget.get("estimated_total", 200000)
    percent = used / total if total > 0 else 0

    return {
        "used": used,
        "total": total,
        "percent_used": round(percent * 100, 1),
        "status": "critical" if percent > 0.90 else "warning" if percent > 0.70 else "ok",
        "recommendation": (
            "Run /memory clear before continuing — context is near limit."
            if percent > 0.90
            else "Consider /memory save to preserve context efficiently."
            if percent > 0.70
            else "Context budget is healthy."
        ),
    }


def update_token_usage(state: dict, tokens_used: int) -> dict:
    """Update token usage in session state."""
    session = state.get("session", {})
    token_budget = session.get("token_budget", {})
    token_budget["used"] = token_budget.get("used", 0) + tokens_used
    token_budget["last_updated"] = datetime.now(timezone.utc).isoformat()
    session["token_budget"] = token_budget
    state["session"] = session
    return state


def build_competitor_summary(competitor_slug: str) -> str:
    """
    Build a compressed summary of a competitor for context loading.
    NEVER loads raw scraped content — reads info.md only.
    """
    scraped = project_scraped_dir()
    info_path = scraped / competitor_slug / "info.md"
    sync_path = scraped / competitor_slug / "sync-status.json"

    summary_parts = [f"# Competitor: {competitor_slug}"]

    if info_path.exists():
        # Read only first 500 chars of info.md for summary
        content = info_path.read_text(encoding="utf-8")[:500]
        summary_parts.append(content)

    if sync_path.exists():
        with open(sync_path) as f:
            sync = json.load(f)
        summary_parts.append(
            f"Last sync: {sync.get('last_sync', 'never')} | "
            f"Total content: {sync.get('total_content', 0)} | "
            f"New since last: {sync.get('new_since_last', 0)}"
        )

    return "\n".join(summary_parts)
