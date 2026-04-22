"""
cli_router.py — Sovereign Workspace Command Router
=================================================
Parses flag-free conversational commands and routes them to the correct
primary agent with a structured JSON payload.

Owner: guide-agent
Invoked by: Every command entry point
Output: JSON routing payload {primary_agent, sub_agents, context, entities}
"""

import json
import re
import sys
from pathlib import Path
from datetime import datetime, timezone
import importlib.util

_scripts = Path(__file__).resolve().parent
while _scripts.name != "scripts" and _scripts != _scripts.parent:
    _scripts = _scripts.parent
if str(_scripts) not in sys.path:
    sys.path.insert(0, str(_scripts))

from paths import (  # noqa: E402
    REPO_ROOT,
    active_project,
    logs_dir,
    project_scraped_dir,
    scripts_dir,
)

WORKSPACE_ROOT = REPO_ROOT
TOOL_ROUTER_PATH = scripts_dir() / "tool_router_v2.py"
TOOL_REGISTRY_PATH = REPO_ROOT / ".ai" / "tool-registry.json"

spec = importlib.util.spec_from_file_location("tool_router_v2", TOOL_ROUTER_PATH)
tool_router_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tool_router_module)
ToolRouter = tool_router_module.ToolRouter

_P = active_project()
_REF = f"content/{_P}/reference"
_SCR = f"content/{_P}/scraped"
_CONT = f"content/{_P}"
_OUT = f"content/{_P}/outputs"
_CMP = f"content/{_P}/comparisons"
_WDOC = ".ai/workspace"

# ── Command intent map ────────────────────────────────────────────────────────
COMMAND_PATTERNS = [
    {
        "pattern": r"^/brand(?:\s+workshop)?$",
        "intent": "brand_discovery",
        "primary_agent": "brand-agent",
        "sub_agents": ["brand-consultant"],
        "requires_context": [".ai/templates/brand-discovery/questions.json"],
        "output_paths": [
            f"{_REF}/market-positioning.md",
            f"{_REF}/brand-voice/style-rules.md",
            f"{_REF}/brand-voice/glossary.md",
            f"{_REF}/brand-voice/tone-examples.md",
            f"{_REF}/brand-voice/voice-refinement.md",
            ".ai/logs/brand-session.json",
        ],
        "script": ".ai/scripts/brand/brand_consultant.py",
        "protocol": f"{_WDOC}/06-brand-reference/brand-discovery.md",
        "hard_block_check": None,
    },
    {
        "pattern": r"^/research competitors?$",
        "intent": "research_competitors",
        "primary_agent": "research-agent",
        "sub_agents": ["discovery-engine", "profile-builder"],
        "requires_context": [f"{_REF}/market-positioning.md", f"{_SCR}/index.json"],
        "output_paths": [f"{_SCR}/", f"{_SCR}/index.json"],
    },
    {
        "pattern": r"^/scrape all competitors? (blog|projects?|all website)$",
        "intent": "scrape_all",
        "primary_agent": "scraper-agent",
        "sub_agents": ["delta-detector", "ethical-crawler", "content-parser", "asset-handler", "sync-state-writer"],
        "requires_context": [f"{_SCR}/index.json"],
        "output_paths": [f"{_SCR}/"],
    },
    {
        "pattern": r"^/scrape (.+?) (website|all website)$",
        "intent": "scrape_single",
        "primary_agent": "scraper-agent",
        "sub_agents": ["delta-detector", "ethical-crawler", "content-parser", "asset-handler", "sync-state-writer"],
        "requires_context": [f"{_SCR}/index.json"],
        "output_paths": [f"{_SCR}/"],
    },
    {
        "pattern": r"^/sync$",
        "intent": "sync",
        "primary_agent": "scraper-agent",
        "sub_agents": ["delta-detector", "ethical-crawler", "content-parser", "sync-state-writer"],
        "requires_context": [f"{_SCR}/index.json"],
        "output_paths": [f"{_SCR}/", ".ai/logs/sync-delta.jsonl"],
    },
    {
        "pattern": r"^/extract brand voice from (.+)$",
        "intent": "extract_brand_voice",
        "primary_agent": "brand-agent",
        "sub_agents": ["tone-analyzer"],
        "requires_context": [],
        "output_paths": [f"{_REF}/brand-voice/voice-refinement.md"],
    },
    {
        "pattern": r"^/refine brand voice$",
        "intent": "refine_brand_voice",
        "primary_agent": "brand-agent",
        "sub_agents": ["drift-detector", "rule-updater"],
        "requires_context": [f"{_REF}/brand-voice/style-rules.md", f"{_CONT}/"],
        "output_paths": [f"{_REF}/brand-voice/style-rules.md", f"{_REF}/brand-voice/glossary.md"],
    },
    {
        "pattern": r"^/create website pages?$",
        "intent": "create_website_pages",
        "primary_agent": "creator-agent",
        "sub_agents": ["blueprint-architect", "content-generator", "brand-voice-applier"],
        "requires_context": [f"{_REF}/brand-voice/style-rules.md", f"{_REF}/market-positioning.md"],
        "output_paths": [f"{_CONT}/website-pages/"],
        "template": ".ai/templates/content-blueprints/website-page.md",
    },
    {
        "pattern": r"^/create blog posts? about (.+)$",
        "intent": "create_blog_posts",
        "primary_agent": "creator-agent",
        "sub_agents": ["blueprint-architect", "content-generator", "brand-voice-applier"],
        "requires_context": [f"{_REF}/brand-voice/style-rules.md", f"{_CONT}/_references/keyword-maps.md"],
        "output_paths": [f"{_CONT}/blog-posts/"],
        "template": ".ai/templates/content-blueprints/blog-post.md",
    },
    {
        "pattern": r"^/create project pages?$",
        "intent": "create_project_pages",
        "primary_agent": "creator-agent",
        "sub_agents": ["blueprint-architect", "content-generator", "brand-voice-applier"],
        "requires_context": [f"{_REF}/brand-voice/style-rules.md"],
        "output_paths": [f"{_CONT}/projects/"],
        "template": ".ai/templates/content-blueprints/project-page.md",
    },
    {
        "pattern": r"^/create landing pages? for (.+)$",
        "intent": "create_landing_pages",
        "primary_agent": "creator-agent",
        "sub_agents": ["blueprint-architect", "content-generator", "brand-voice-applier"],
        "requires_context": [f"{_REF}/brand-voice/style-rules.md", f"{_REF}/market-positioning.md"],
        "output_paths": [f"{_CONT}/landing-pages/"],
        "template": ".ai/templates/content-blueprints/landing-page.md",
    },
    {
        "pattern": r"^/compare sovereign vs (?:competitor )?(.+)$",
        "intent": "compare",
        "primary_agent": "creator-agent",
        "sub_agents": ["comparison-analyst"],
        "requires_context": [f"{_SCR}/index.json", f"{_REF}/brand-voice/style-rules.md"],
        "output_paths": [f"{_CMP}/"],
    },
    {
        "pattern": r"^/polish content(?: in content/)?$",
        "intent": "polish_content",
        "primary_agent": "seo-agent",
        "sub_agents": ["keyword-auditor", "technical-auditor", "brand-voice-applier"],
        "requires_context": [f"{_CONT}/", f"{_CONT}/_references/keyword-maps.md", f"{_REF}/brand-voice/style-rules.md"],
        "output_paths": [f"{_CONT}/"],
    },
    {
        "pattern": r"^/optimize images(?: in content/)?$",
        "intent": "optimize_images",
        "primary_agent": "seo-agent",
        "sub_agents": ["image-seo-auditor"],
        "requires_context": [f"{_CONT}/"],
        "output_paths": [f"{_CONT}/assets-seo.json"],
    },
    {
        "pattern": r"^/review$",
        "intent": "review",
        "primary_agent": "workflow-agent",
        "sub_agents": ["quality-checker"],
        "requires_context": [f"{_CONT}/"],
        "output_paths": [".ai/logs/quality-report.json"],
    },
    {
        "pattern": r"^/approve$",
        "intent": "approve",
        "primary_agent": "workflow-agent",
        "sub_agents": ["approval-gate"],
        "requires_context": [".ai/logs/quality-report.json"],
        "output_paths": [f"{_CONT}/"],
        "hard_block_check": "quality_gates_passed",
    },
    {
        "pattern": r"^/revise (.+)$",
        "intent": "revise",
        "primary_agent": "creator-agent",
        "sub_agents": ["content-generator", "brand-voice-applier"],
        "requires_context": [".ai/memory/state.json", f"{_REF}/brand-voice/style-rules.md"],
        "output_paths": [f"{_CONT}/"],
    },
    {
        "pattern": r"^/export$",
        "intent": "export",
        "primary_agent": "workflow-agent",
        "sub_agents": ["export-packager"],
        "requires_context": [f"{_CONT}/", ".ai/templates/csv-schemas/content-export.json"],
        "output_paths": [f"{_OUT}/"],
        "hard_block_check": "content_approved",
    },
    {
        "pattern": r"^/archive old content$",
        "intent": "archive",
        "primary_agent": "workflow-agent",
        "sub_agents": ["archive-manager"],
        "requires_context": [f"{_CONT}/", f"{_SCR}/"],
        "output_paths": ["archive/"],
    },
    {
        "pattern": r"^/memory (save|load|clear)$",
        "intent": "memory_operation",
        "primary_agent": "memory-manager",
        "sub_agents": [],
        "requires_context": [".ai/memory/"],
        "output_paths": [".ai/memory/"],
    },
    {
        "pattern": r"^/budget check$",
        "intent": "budget_check",
        "primary_agent": "guide-agent",
        "sub_agents": [],
        "requires_context": [".ai/memory/state.json"],
        "output_paths": [],
    },
    {
        "pattern": r"^/antigravity (status|sync|learn)$",
        "intent": "antigravity_operation",
        "primary_agent": "antigravity-agent",
        "sub_agents": ["sync-engine", "continual-learning-engine"],
        "requires_context": [".antigravity/commands/", ".cursor/commands/", ".cursor/rules/"],
        "output_paths": [".cursor/commands/", ".cursor/rules/", ".cursor/hooks/state/continual-learning-index.json"],
    },
    {
        "pattern": r"^/intel (competitor|market snapshot|opportunities)(?:\s+(.+))?$",
        "intent": "intelligence_operation",
        "primary_agent": "research-agent",
        "sub_agents": ["intel-synthesizer"],
        "requires_context": [f"{_SCR}/index.json"],
        "output_paths": [f"{_SCR}/"],
    },
]


def parse_command(raw_command: str) -> dict:
    """
    Parse a flag-free command string and return a structured routing payload.

    Args:
        raw_command: The raw user command string (e.g. "/create blog posts about sustainable design")

    Returns:
        Routing payload dict or error dict with clarifying_question
    """
    command_without_flags, _ = parse_cli_flags(raw_command)
    command = command_without_flags.strip().lower()

    for cmd in COMMAND_PATTERNS:
        match = re.match(cmd["pattern"], command, re.IGNORECASE)
        if match:
            entities = extract_entities(command, cmd["intent"], match)
            missing = check_missing_context(cmd.get("requires_context", []))

            payload = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "raw_command": raw_command,
                "intent": cmd["intent"],
                "primary_agent": cmd["primary_agent"],
                "sub_agents": cmd["sub_agents"],
                "entities": entities,
                "requires_context": cmd.get("requires_context", []),
                "missing_context": missing,
                "output_paths": cmd.get("output_paths", []),
                "template": cmd.get("template"),
                "hard_block_check": cmd.get("hard_block_check"),
                "clarifying_question": None,
                "status": "ready" if not missing else "needs_context",
            }

            payload["tool_execution"] = build_tool_execution(raw_command, payload["intent"])

            # Apply one clarifying question if context is critically missing
            if missing:
                payload["clarifying_question"] = get_clarifying_question(cmd["intent"], missing)

            return payload

    # No match found
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "raw_command": raw_command,
        "intent": "unknown",
        "primary_agent": None,
        "status": "unrecognized",
        "clarifying_question": (
            f"I didn't recognize that command. Available commands: "
            f"/brand, /research competitors, /scrape, /sync, /create, /compare, "
            f"/polish, /optimize, /review, /approve, /revise, /export, /archive, "
            f"/memory save|load|clear, /budget check. "
            f"Start with /brand if you haven't set up your brand foundation yet."
        ),
    }


def parse_cli_flags(raw_command: str) -> tuple[str, dict]:
    tokens = raw_command.strip().split()
    command_tokens = []
    flag_tokens = []
    parsing_command = True
    for token in tokens:
        if token.startswith("--"):
            parsing_command = False
            flag_tokens.append(token)
        elif parsing_command:
            command_tokens.append(token)
        else:
            flag_tokens.append(token)

    flags = {
        "tool": None,
        "tool_forced": False,
        "explain_routing": False,
        "prefer": None,
        "parallel": False,
    }
    i = 0
    while i < len(flag_tokens):
        token = flag_tokens[i]
        if token == "--tool" and i + 1 < len(flag_tokens):
            flags["tool"] = flag_tokens[i + 1]
            flags["tool_forced"] = True
            i += 2
        elif token == "--prefer" and i + 1 < len(flag_tokens):
            flags["prefer"] = flag_tokens[i + 1]
            i += 2
        elif token == "--parallel":
            flags["parallel"] = True
            i += 1
        elif token == "--explain-routing":
            flags["explain_routing"] = True
            i += 1
        else:
            i += 1
    return " ".join(command_tokens), flags


def build_tool_execution(raw_command: str, intent: str) -> dict:
    command_without_flags, flags = parse_cli_flags(raw_command)
    if intent not in {"research_competitors", "scrape_all", "scrape_single", "sync"}:
        return {"status": "skipped", "reason": "intent_not_accuracy_routed"}
    if not TOOL_REGISTRY_PATH.exists():
        return {"status": "skipped", "reason": "tool_registry_missing"}
    with open(TOOL_REGISTRY_PATH) as f:
        tool_registry = json.load(f)
    router = ToolRouter(tool_registry=tool_registry, command_routing={})
    result = router.route_command(command_without_flags, flags)
    return result


def extract_entities(command: str, intent: str, match) -> dict:
    """Extract named entities from command based on intent."""
    entities = {}
    groups = match.groups()

    if intent == "brand_discovery":
        pass  # No entities — /brand is a self-contained session
    elif intent == "create_blog_posts" and groups:
        entities["topic"] = groups[0].strip()
    elif intent == "create_landing_pages" and groups:
        entities["campaign"] = groups[0].strip()
    elif intent == "extract_brand_voice" and groups:
        entities["source"] = groups[0].strip()
    elif intent == "scrape_single" and groups:
        entities["competitor_name"] = groups[0].strip()
        entities["scope"] = groups[1].strip() if len(groups) > 1 else "website"
    elif intent == "scrape_all" and groups:
        entities["scope"] = groups[0].strip()
    elif intent == "compare" and groups:
        entities["competitor_name"] = groups[0].strip()
    elif intent == "revise" and groups:
        entities["feedback"] = groups[0].strip()
    elif intent == "memory_operation" and groups:
        entities["operation"] = groups[0].strip()
    elif intent == "antigravity_operation" and groups:
        entities["operation"] = groups[0].strip()
    elif intent == "intelligence_operation" and groups:
        entities["type"] = groups[0].strip()
        entities["target"] = groups[1].strip() if len(groups) > 1 and groups[1] else None

    return entities


def check_missing_context(required_paths: list) -> list:
    """Check which required context files are missing or empty."""
    missing = []
    for path_str in required_paths:
        full_path = WORKSPACE_ROOT / path_str
        if not full_path.exists():
            missing.append(path_str)
        elif full_path.is_file() and full_path.stat().st_size < 50:
            # File exists but appears to be a placeholder (< 50 bytes)
            missing.append(f"{path_str} (appears empty — needs to be filled in)")
    return missing


def get_clarifying_question(intent: str, missing: list) -> str:
    """Return exactly one clarifying question based on missing context."""
    questions = {
        "brand_discovery": "The brand interview question bank is missing. Ensure .ai/templates/brand-discovery/questions.json exists before running /brand.",
        "research_competitors": "Your brand foundation isn't set up yet — run `/brand` first, then `/research competitors`.",
        "create_blog_posts": "What tone should this post take — educational, perspective-driven, or project-focused?",
        "create_landing_pages": "What is the primary conversion goal for this campaign — consultation booking, portfolio enquiry, or service awareness?",
        "create_website_pages": "Which page should I create first — Home, About, Services, Contact, or FAQ?",
        "compare": "I don't have scraped data for that competitor yet. Should I run `/scrape [name] all website` first, or compare against their live site directly?",
        "extract_brand_voice": "Please provide the source text or URL to extract tone from. Paste it directly or share a file path.",
        "intelligence_operation": "Which competitor or market segment should I analyze for this intelligence brief?",
        "antigravity_operation": "Should I perform a status check, synchronize commands, or process new transcripts for learning?",
    }
    return questions.get(intent, f"Some required context is missing: {', '.join(missing[:2])}. Can you provide this before we proceed?")


def resolve_competitor_slug(name: str) -> str | None:
    """
    Attempt to match a competitor name to a registered slug.
    Returns the slug or None if not found.
    """
    index_path = project_scraped_dir() / "index.json"
    if not index_path.exists():
        return None

    with open(index_path) as f:
        index = json.load(f)

    competitors = index.get("competitors", [])
    name_lower = name.lower().replace(" ", "-")

    # Exact slug match
    for comp in competitors:
        if comp.get("slug") == name_lower:
            return comp["slug"]

    # Fuzzy name match
    for comp in competitors:
        if name_lower in comp.get("slug", "") or name_lower in comp.get("name", "").lower():
            return comp["slug"]

    return None


def log_routing(payload: dict) -> None:
    """Append routing event to workflow log."""
    log_path = logs_dir() / "workflow.jsonl"
    log_entry = {
        "timestamp": payload["timestamp"],
        "event": "command_routed",
        "command": payload["raw_command"],
        "intent": payload["intent"],
        "primary_agent": payload["primary_agent"],
        "status": payload["status"],
    }
    with open(log_path, "a") as f:
        f.write(json.dumps(log_entry) + "\n")


if __name__ == "__main__":
    # Quick self-test
    test_commands = [
        "/research competitors",
        "/sync",
        "/create blog posts about sustainable luxury interiors",
        "/compare sovereign vs competitor designstudio",
        "/review",
        "/approve",
        "/export",
        "/memory save",
        "/unknown command here",
    ]
    for cmd in test_commands:
        result = parse_command(cmd)
        print(f"\n{'='*50}")
        print(f"CMD: {cmd}")
        print(f"  → Agent: {result.get('primary_agent')}")
        print(f"  → Intent: {result.get('intent')}")
        print(f"  → Status: {result.get('status')}")
        if result.get("clarifying_question"):
            print(f"  → Q: {result['clarifying_question']}")
