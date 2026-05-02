#!/usr/bin/env python3
"""Workspace integrity audit for routing, state, and adapter contracts."""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

_scripts = Path(__file__).resolve().parent
_lib = _scripts / "lib"
for p in [str(_scripts), str(_lib)]:
    if p not in sys.path:
        sys.path.insert(0, p)

from paths import REPO_ROOT  # noqa: E402

ROOT = REPO_ROOT
ROUTING_PATH = ROOT / ".ai/cli-layer/command-routing.json"
ROUTING_DOC_PATH = ROOT / ".ai/commands-multi-tool.md"
STATE_PATH = ROOT / ".ai/memory/state.json"
TOOL_REGISTRY_PATH = ROOT / ".ai/tool-registry.json"
ADAPTERS_DIR = ROOT / ".ai/scripts/adapters"
PATH_REPORT_PATH = ROOT / ".ai/logs/path-integrity-report.json"
PATH_SUMMARY_PATH = ROOT / ".ai/logs/path-integrity-summary.md"


@dataclass
class Issue:
    code: str
    message: str
    file: str


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def check_routing_contract(issues: list[Issue]) -> None:
    if not ROUTING_PATH.exists():
        issues.append(Issue("routing_missing", "Canonical routing schema is missing", str(ROUTING_PATH)))
        return

    data = load_json(ROUTING_PATH)
    commands = data.get("commands", [])
    if not commands:
        issues.append(Issue("routing_empty", "Routing schema has no commands", str(ROUTING_PATH)))

    missing_patterns = [item.get("id", "<unknown>") for item in commands if not item.get("patterns")]
    if missing_patterns:
        issues.append(
            Issue(
                "routing_pattern_missing",
                f"Commands missing regex patterns: {', '.join(missing_patterns)}",
                str(ROUTING_PATH),
            )
        )

    if ROUTING_DOC_PATH.exists():
        text = ROUTING_DOC_PATH.read_text(encoding="utf-8")
        if "canonical executable source is `.ai/cli-layer/command-routing.json`" not in text:
            issues.append(
                Issue(
                    "routing_doc_drift",
                    "Routing documentation is not pointing to canonical schema",
                    str(ROUTING_DOC_PATH),
                )
            )


def check_state_schema(issues: list[Issue]) -> None:
    if not STATE_PATH.exists():
        issues.append(Issue("state_missing", "State file is missing", str(STATE_PATH)))
        return

    state = load_json(STATE_PATH)
    session = state.get("session", {})
    pipeline = state.get("pipeline_state", {})

    if "last_tool" not in session:
        issues.append(Issue("state_last_tool_missing", "session.last_tool is missing", str(STATE_PATH)))
    if "last_tool" not in pipeline:
        issues.append(Issue("pipeline_last_tool_missing", "pipeline_state.last_tool is missing", str(STATE_PATH)))


def check_tool_registry_vs_adapters(issues: list[Issue]) -> None:
    if not TOOL_REGISTRY_PATH.exists():
        issues.append(Issue("tool_registry_missing", "Tool registry file is missing", str(TOOL_REGISTRY_PATH)))
        return

    registry = load_json(TOOL_REGISTRY_PATH)
    available = set(registry.get("available_tools", []))
    specs = registry.get("tool_specs", {})

    for tool in sorted(available):
        adapter_path = ADAPTERS_DIR / f"{tool}_adapter.py"
        if not adapter_path.exists():
            issues.append(
                Issue(
                    "adapter_missing",
                    f"Available tool '{tool}' has no adapter implementation at .ai/scripts/adapters/{tool}_adapter.py",
                    str(TOOL_REGISTRY_PATH),
                )
            )

    for tool, spec in specs.items():
        if spec.get("status") == "available" and tool not in available:
            issues.append(
                Issue(
                    "registry_inconsistent",
                    f"Tool '{tool}' marked available in tool_specs but missing from available_tools",
                    str(TOOL_REGISTRY_PATH),
                )
            )


def check_path_report_freshness(issues: list[Issue]) -> None:
    if not PATH_REPORT_PATH.exists() or not PATH_SUMMARY_PATH.exists():
        return

    if PATH_SUMMARY_PATH.stat().st_mtime < PATH_REPORT_PATH.stat().st_mtime:
        issues.append(
            Issue(
                "path_summary_stale",
                "path-integrity-summary.md is older than path-integrity-report.json",
                str(PATH_SUMMARY_PATH),
            )
        )


def main() -> int:
    issues: list[Issue] = []
    check_routing_contract(issues)
    check_state_schema(issues)
    check_tool_registry_vs_adapters(issues)
    check_path_report_freshness(issues)

    report = {
        "summary": {
            "issues": len(issues),
            "status": "pass" if not issues else "fail",
        },
        "issues": [issue.__dict__ for issue in issues],
    }

    print(json.dumps(report, indent=2))
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
