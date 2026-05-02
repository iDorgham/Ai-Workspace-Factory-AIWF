"""
workflow_orchestrator.py — Sovereign Pipeline Orchestrator
==========================================================
Chains command stages, enforces the pipeline order, manages state transitions,
and logs every action. Called after cli_router produces a routing payload.

Owner: guide-agent / workflow-agent
Pipeline order (enforced): Research → Scrape/Sync → Create → Polish → Review → Approve → Export
"""

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

from paths import REPO_ROOT, logs_dir  # noqa: E402

WORKSPACE_ROOT = REPO_ROOT
STATE_PATH = WORKSPACE_ROOT / ".ai" / "memory" / "state.json"
WORKFLOW_LOG = logs_dir() / "workflow.jsonl"
SKILL_TELEMETRY_LOG = logs_dir() / "skill-performance.jsonl"
SKILL_MAP_PATH = WORKSPACE_ROOT / ".ai" / "skill-integration-map.json"

# ── Pipeline stage order (enforced) ──────────────────────────────────────────
PIPELINE_STAGES = [
    "setup",
    "research",
    "scrape",
    "create",
    "polish",
    "review",
    "approve",
    "export",
    "archive",
]

STAGE_MAP = {
    "brand_discovery": "setup",
    "research_competitors": "research",
    "scrape_all": "scrape",
    "scrape_single": "scrape",
    "sync": "scrape",
    "extract_brand_voice": "setup",
    "refine_brand_voice": "setup",
    "create_blog_posts": "create",
    "create_website_pages": "create",
    "create_project_pages": "create",
    "create_landing_pages": "create",
    "compare": "create",
    "polish_content": "polish",
    "optimize_images": "polish",
    "review": "review",
    "approve": "approve",
    "revise": "polish",
    "export": "export",
    "archive": "archive",
    "intelligence_operation": "research",
    "antigravity_operation": None,
    "memory_operation": None,   # Cross-cutting, not pipeline-ordered
    "budget_check": None,
}

# Hard blocks: intent → what must be true before it can run
HARD_BLOCKS = {
    "approve": "review_passed",
    "export": "content_approved",
    "sync": "competitors_registered",
    "scrape_all": "competitors_registered",
    "scrape_single": "competitors_registered",
    "compare": "competitor_data_available",
}


def load_state() -> dict:
    """Load current session state."""
    if STATE_PATH.exists():
        try:
            with open(STATE_PATH) as f:
                loaded = json.load(f)
            if isinstance(loaded, dict):
                return loaded
            log_action("state_load_invalid", "system", "workflow-agent", "failed", details={"reason": "state_not_dict"})
        except (json.JSONDecodeError, OSError) as exc:
            log_action("state_load_failed", "system", "workflow-agent", "failed", details={"error": str(exc)})
    return {}


def save_state(state: dict) -> None:
    """Save updated session state."""
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_PATH, "w") as f:
        json.dump(state, f, indent=2)


def log_action(event: str, intent: str, agent: str, status: str,
               duration_ms: int = 0, details: dict = None) -> None:
    """Append one action line to workflow.jsonl."""
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": event,
        "command_intent": intent,
        "agent": agent,
        "status": status,
        "duration_ms": duration_ms,
        "details": details or {},
    }
    WORKFLOW_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(WORKFLOW_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")


def log_skill_action(intent: str, skill: str, status: str, retries: int, details: dict | None = None) -> None:
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "intent": intent,
        "skill": skill,
        "status": status,
        "retries": retries,
        "details": details or {},
    }
    SKILL_TELEMETRY_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(SKILL_TELEMETRY_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")


def load_skill_map() -> dict:
    if SKILL_MAP_PATH.exists():
        try:
            with open(SKILL_MAP_PATH) as f:
                loaded = json.load(f)
            if isinstance(loaded, dict):
                return loaded
            log_action("skill_map_invalid", "system", "workflow-agent", "failed", details={"reason": "skill_map_not_dict"})
        except (json.JSONDecodeError, OSError) as exc:
            log_action("skill_map_load_failed", "system", "workflow-agent", "failed", details={"error": str(exc)})
    return {}


def validate_routing_payload(routing_payload: dict) -> dict | None:
    """Validate minimal payload contract before orchestration."""
    if not isinstance(routing_payload, dict):
        return {"code": "invalid_payload", "reason": "routing_payload must be an object"}

    if not routing_payload.get("intent") or not isinstance(routing_payload.get("intent"), str):
        return {"code": "invalid_payload", "reason": "missing_or_invalid_intent"}

    if not routing_payload.get("primary_agent") or not isinstance(routing_payload.get("primary_agent"), str):
        return {"code": "invalid_payload", "reason": "missing_or_invalid_primary_agent"}

    status = routing_payload.get("status", "ready")
    if status not in {"ready", "needs_context", "unrecognized"}:
        return {"code": "invalid_payload", "reason": "invalid_status"}

    if "sub_agents" in routing_payload and not isinstance(routing_payload.get("sub_agents", []), list):
        return {"code": "invalid_payload", "reason": "invalid_sub_agents"}

    if "entities" in routing_payload and not isinstance(routing_payload.get("entities", {}), dict):
        return {"code": "invalid_payload", "reason": "invalid_entities"}

    return None


def check_hard_block(intent: str, state: dict) -> dict | None:
    """
    Check if a hard block applies to this intent.
    Returns a block dict {blocked: True, reason, recommendation} or None.
    """
    block_condition = HARD_BLOCKS.get(intent)
    if not block_condition:
        return None

    workspace_state = state.get("workspace_state", {})
    quality_state = state.get("quality_state", {})
    active_content = state.get("active_content", {})

    if block_condition == "review_passed":
        if not quality_state.get("overall_pass"):
            return {
                "blocked": True,
                "reason": "No passing review found. Quality gates have not all passed.",
                "recommendation": "Run /review first, then /approve once all gates pass.",
            }

    elif block_condition == "content_approved":
        approved = active_content.get("last_approved")
        if not approved:
            return {
                "blocked": True,
                "reason": "No approved content found. Export requires approval.",
                "recommendation": "Run /review → /approve before /export.",
            }

    elif block_condition == "competitors_registered":
        if workspace_state.get("competitors_registered", 0) == 0:
            return {
                "blocked": True,
                "reason": "No competitors registered in index.json.",
                "recommendation": "Run /research competitors first.",
            }

    elif block_condition == "competitor_data_available":
        # Warn but don't hard-block — can compare against live site
        pass

    return None


def get_next_suggested_step(intent: str, status: str) -> str:
    """Return the suggested next command based on completed intent."""
    next_steps = {
        "brand_discovery": "/research competitors",
        "research_competitors": "/scrape all competitors blog",
        "scrape_all": "/sync",
        "scrape_single": "/sync",
        "sync": "/create blog posts about [topic]",
        "extract_brand_voice": "/refine brand voice",
        "refine_brand_voice": "/create blog posts about [topic]",
        "create_blog_posts": "/polish content in content/",
        "create_website_pages": "/polish content in content/",
        "create_project_pages": "/polish content in content/",
        "create_landing_pages": "/polish content in content/",
        "compare": "/create blog posts about [identified topic gap]",
        "polish_content": "/optimize images in content/",
        "optimize_images": "/review",
        "review": "/approve" if status == "passed" else "/revise [feedback for failing gate]",
        "revise": "/review",
        "approve": "/export",
        "export": "/sync",
        "archive": "/memory clear",
        "intelligence_operation": "/create blog posts about [topic]",
        "antigravity_operation": "Continue with your previous command",
        "memory_operation": "Continue with your previous command",
    }
    return next_steps.get(intent, "/sync")


def orchestrate(routing_payload: dict) -> dict:
    """
    Main orchestration function. Validates the routing payload,
    checks hard blocks, logs, updates state, and returns execution context.

    Args:
        routing_payload: Output from cli_router.parse_command()

    Returns:
        Execution context dict for the primary agent to act on
    """
    payload_error = validate_routing_payload(routing_payload)
    if payload_error:
        log_action("execution_rejected", "unknown", "workflow-agent", payload_error["code"], details=payload_error)
        return {
            "status": payload_error["code"],
            "blocked_reason": payload_error["reason"],
            "recommendation": "Check command routing payload schema before orchestration.",
            "suggested_next_step": "Retry command after payload validation.",
        }

    intent = routing_payload.get("intent")
    agent = routing_payload.get("primary_agent")
    start_time = datetime.now(timezone.utc)

    # Load state
    state = load_state()

    # Check hard blocks
    block = check_hard_block(intent, state)
    if block:
        log_action("command_blocked", intent, agent, "blocked",
                   details={"reason": block["reason"]})
        return {
            "status": "blocked",
            "blocked_reason": block["reason"],
            "recommendation": block["recommendation"],
            "suggested_next_step": block["recommendation"],
        }

    # Check for missing context (non-blocking — agent applies defaults)
    if routing_payload.get("status") == "needs_context":
        log_action("context_missing", intent, agent, "clarifying",
                   details={"missing": routing_payload.get("missing_context", [])})
        return {
            "status": "clarifying",
            "clarifying_question": routing_payload.get("clarifying_question"),
            "missing_context": routing_payload.get("missing_context", []),
        }

    # Determine pipeline stage
    stage = STAGE_MAP.get(intent)

    # Build execution context for primary agent
    skill_map = load_skill_map()
    skill_plan = skill_map.get(intent, {"skills": [], "retry_limit": 2})
    context = {
        "intent": intent,
        "primary_agent": agent,
        "sub_agents": routing_payload.get("sub_agents", []),
        "entities": routing_payload.get("entities", {}),
        "tool_execution": routing_payload.get("tool_execution", {}),
        "template": routing_payload.get("template"),
        "output_paths": routing_payload.get("output_paths", []),
        "pipeline_stage": stage,
        "workspace_root": str(WORKSPACE_ROOT),
        "state": state,
        "skill_plan": skill_plan,
        "started_at": start_time.isoformat(),
    }

    # Log start
    log_action("execution_started", intent, agent, "in_progress")

    # Update pipeline state in session
    pipeline_state = state.get("pipeline_state", {})
    pipeline_state["current_stage"] = stage or pipeline_state.get("current_stage", "setup")
    pipeline_state["last_command"] = routing_payload.get("raw_command")
    pipeline_state["last_command_at"] = start_time.isoformat()
    pipeline_state["last_agent"] = agent
    pipeline_state["last_status"] = "in_progress"

    if not isinstance(pipeline_state.get("stages_completed"), list):
        pipeline_state["stages_completed"] = []

    state["pipeline_state"] = pipeline_state
    state["suggested_next_step"] = get_next_suggested_step(intent, "in_progress")
    save_state(state)

    return context


def finalize(context: dict, result: dict) -> dict:
    """
    Called after agent execution completes.
    Updates state, logs completion, returns final response.

    Args:
        context: Execution context from orchestrate()
        result: Agent execution result {status, output, errors, duration_ms}

    Returns:
        Final response for guide-agent to format
    """
    intent = context.get("intent")
    agent = context.get("primary_agent")
    status = result.get("status", "unknown")
    duration_ms = result.get("duration_ms", 0)

    # Log completion
    log_action("execution_completed", intent, agent, status,
               duration_ms=duration_ms, details=result.get("details", {}))

    for run in result.get("skill_runs", []):
        log_skill_action(
            intent=intent,
            skill=run.get("skill", "unknown"),
            status=run.get("status", "unknown"),
            retries=run.get("retries", 0),
            details=run.get("details", {}),
        )

    # Update state
    state = load_state()
    pipeline_state = state.get("pipeline_state", {})
    pipeline_state["last_status"] = status
    stage = context.get("pipeline_stage")
    stages_completed = pipeline_state.get("stages_completed", [])
    if not isinstance(stages_completed, list):
        stages_completed = []
    if stage and status in {"success", "passed", "completed"} and stage not in stages_completed:
        stages_completed.append(stage)
    pipeline_state["stages_completed"] = stages_completed
    state["pipeline_state"] = pipeline_state

    # Update workspace counters based on intent
    workspace_state = state.get("workspace_state", {})
    if intent == "research_competitors":
        workspace_state["competitors_registered"] = result.get("details", {}).get("total_competitors", 0)
    elif intent in ("sync", "scrape_all", "scrape_single"):
        workspace_state["last_sync"] = datetime.now(timezone.utc).isoformat()
    elif intent in ("create_blog_posts", "create_website_pages", "create_project_pages", "create_landing_pages"):
        workspace_state["content_drafts"] = workspace_state.get("content_drafts", 0) + result.get("details", {}).get("files_created", 0)
    elif intent == "approve":
        workspace_state["content_approved"] = workspace_state.get("content_approved", 0) + 1
    elif intent == "export":
        workspace_state["content_exported"] = workspace_state.get("content_exported", 0) + 1
        workspace_state["last_export"] = datetime.now(timezone.utc).isoformat()
    elif intent == "archive":
        workspace_state["last_archive"] = datetime.now(timezone.utc).isoformat()

    state["workspace_state"] = workspace_state
    state["suggested_next_step"] = get_next_suggested_step(intent, status)
    save_state(state)

    return {
        "status": status,
        "output": result.get("output", ""),
        "errors": result.get("errors", []),
        "suggested_next_step": state["suggested_next_step"],
    }
