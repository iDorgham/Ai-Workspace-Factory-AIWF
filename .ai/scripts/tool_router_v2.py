#!/usr/bin/env python3
"""Accuracy-first tool router with adaptive fallback."""

import json
import re
import sys
import threading
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

_scripts = Path(__file__).resolve().parent
if str(_scripts) not in sys.path:
    sys.path.insert(0, str(_scripts))

from paths import REPO_ROOT, logs_dir  # noqa: E402

WORKSPACE_ROOT = REPO_ROOT
ROUTING_SCHEMA_PATH = WORKSPACE_ROOT / ".ai" / "registry" / "routing" / "command_routing.json"
TOOL_PERF_LOG = logs_dir() / "tool-performance.jsonl"


class ToolRouter:
    def __init__(
        self,
        tool_registry: Dict,
        command_routing: Optional[Dict] = None,
        test_mode: bool = False,
        test_results: Optional[Dict] = None,
        routing_schema_path: Optional[str] = None,
    ):
        self.tool_registry = tool_registry
        self.command_routing = command_routing or {}
        self.execution_log: List[Dict[str, Any]] = []
        self.test_mode = test_mode
        self.test_results = test_results or {}
        self.routing_schema = self._load_routing_schema(routing_schema_path)

    def route_command(self, command: str, flags: Dict) -> Dict:
        if flags.get("explain_routing"):
            return self.explain_routing_mode(command)
        if flags.get("tool_forced"):
            return self.forced_tool_mode(command, flags.get("tool"))
        if flags.get("parallel"):
            return self.parallel_execution_mode(command)
        return self.normal_execution_mode(command, flags.get("prefer"))

    def explain_routing_mode(self, command: str) -> Dict:
        command_type = self.parse_command_type(command)
        ranking = self.get_ranking_for_command(command, command_type)
        available_tools = self.tool_registry.get("available_tools", [])
        rule = self.get_route_rule(command)
        actual_ranking = [t for t in ranking if t in available_tools]
        ranking_explanation = []
        for rank, tool in enumerate(actual_ranking, 1):
            tool_info = self.tool_registry["tool_specs"].get(tool, {})
            ranking_explanation.append(
                {
                    "rank": rank,
                    "tool": tool,
                    "latency_ms": tool_info.get("latency_ms", "unknown"),
                    "cost_usd": tool_info.get("cost_usd", "unknown"),
                    "success_rate": tool_info.get("success_rate", "unknown"),
                    "why_this_rank": self.get_rank_explanation(tool, command_type),
                }
            )
        return {
            "status": "explanation",
            "command": command,
            "command_type": command_type,
            "routing_rule_id": rule.get("id"),
            "ranking": ranking_explanation,
            "selected_tool": actual_ranking[0] if actual_ranking else None,
            "available_tools": available_tools,
            "timestamp": datetime.now().isoformat(),
        }

    def forced_tool_mode(self, command: str, forced_tool: str) -> Dict:
        available_tools = self.tool_registry.get("available_tools", [])
        if forced_tool not in available_tools:
            return {
                "status": "error",
                "error_type": "tool_unavailable",
                "tool": forced_tool,
                "message": f"Tool '{forced_tool}' is not available",
                "available_tools": available_tools,
            }
        result = self.execute_tool(forced_tool, command)
        quality = self.evaluate_quality(command, result)
        if result.get("status") == "success" and quality["gate_passed"]:
            return {
                "status": "success",
                "tool": forced_tool,
                "tool_forced": True,
                "quality_score": quality["confidence"],
                "output": result.get("output"),
                "timestamp": datetime.now().isoformat(),
            }
        return {
            "status": "error",
            "error_type": quality["failure_type"] if result.get("status") == "success" else "forced_tool_failed",
            "tool": forced_tool,
            "message": f"Forced tool '{forced_tool}' failed",
            "error": result.get("error"),
        }

    def parallel_execution_mode(self, command: str) -> Dict:
        command_type = self.parse_command_type(command)
        ranking = self.get_ranking_for_command(command, command_type)
        available_tools = self.tool_registry.get("available_tools", [])
        actual_ranking = [t for t in ranking if t in available_tools]
        if len(actual_ranking) < 2:
            return {"status": "error", "error_type": "insufficient_tools"}
        rank_1_tool, rank_2_tool = actual_ranking[0], actual_ranking[1]
        results: Dict[str, Dict[str, Any]] = {}
        errors: Dict[str, str] = {}
        outputs: Dict[str, Any] = {}

        def execute(tool: str) -> None:
            results[tool] = self.execute_tool(tool, command)

        thread_1 = threading.Thread(target=execute, args=(rank_1_tool,))
        thread_2 = threading.Thread(target=execute, args=(rank_2_tool,))
        thread_1.start()
        thread_2.start()
        thread_1.join(timeout=300)
        thread_2.join(timeout=300)

        for tool in [rank_1_tool, rank_2_tool]:
            item = results.get(tool, {"status": "error", "error": "timeout"})
            if item.get("status") == "success":
                quality = self.evaluate_quality(command, item)
                if quality["gate_passed"]:
                    outputs[tool] = item.get("output")
                else:
                    errors[tool] = quality["failure_type"]
            else:
                errors[tool] = self.classify_failure(item.get("error", "timeout"), command)

        status = "partial"
        if len(outputs) == 2:
            status = "success_both"
        elif len(outputs) == 0:
            status = "error"
        return {"status": status, "execution_mode": "parallel", "tools": [rank_1_tool, rank_2_tool], "outputs": outputs, "errors": errors}

    def normal_execution_mode(self, command: str, preferred_tool: Optional[str]) -> Dict:
        command_type = self.parse_command_type(command)
        ranking = self.get_ranking_for_command(command, command_type)
        available_tools = self.tool_registry.get("available_tools", [])
        tools_to_try = [t for t in ranking if t in available_tools]
        if preferred_tool and preferred_tool in available_tools:
            if preferred_tool in tools_to_try:
                tools_to_try.remove(preferred_tool)
            tools_to_try.insert(1, preferred_tool)
        if not tools_to_try:
            return {"status": "error", "error_type": "no_tools_available"}
        first_failure = None
        for idx, tool in enumerate(tools_to_try, 1):
            result = self.execute_tool(tool, command)
            if result.get("status") != "success":
                first_failure = first_failure or self.classify_failure(result.get("error", "tool_error"), command)
                continue
            quality = self.evaluate_quality(command, result)
            if quality["gate_passed"]:
                payload = {
                    "status": "success",
                    "tool": tool,
                    "tool_rank": idx,
                    "fallback_used": idx > 1,
                    "quality_score": quality["confidence"],
                    "output": result.get("output"),
                    "timestamp": datetime.now().isoformat(),
                }
                if idx > 1:
                    payload["fallback_from"] = tools_to_try[0]
                    payload["fallback_reason"] = "previous_tool_failed_or_low_confidence"
                self.log_command(command, tool, "success", mode="normal", tool_rank=idx, confidence=quality["confidence"])
                return payload
            first_failure = first_failure or quality["failure_type"]
        self.log_command(command, "all", "error", mode="normal", failure_type=first_failure, tools_tried=tools_to_try)
        return {"status": "error", "error_type": "all_tools_failed", "failure_type": first_failure, "tools_tried": tools_to_try}

    def parse_command_type(self, command: str) -> str:
        parts = command.strip().split()
        if parts and parts[0].startswith("/"):
            parts[0] = parts[0][1:]
        return "_".join(parts).lower()

    def _load_routing_schema(self, override_path: Optional[str]) -> Dict[str, Any]:
        path = Path(override_path) if override_path else ROUTING_SCHEMA_PATH
        if path.exists():
            with path.open() as f:
                return json.load(f)
        return {"defaults": {"ranking": ["copilot", "codex", "gemini", "qwen"]}, "commands": []}

    def get_route_rule(self, command: str) -> Dict[str, Any]:
        command_lower = command.strip().lower()
        for rule in self.routing_schema.get("commands", []):
            for pattern in rule.get("patterns", []):
                if re.match(pattern, command_lower, re.IGNORECASE):
                    return rule
        return {}

    def get_ranking_for_command(self, command: str, command_type: str) -> List[str]:
        rule = self.get_route_rule(command)
        if rule.get("ranking"):
            return rule["ranking"]
        if command_type in self.command_routing:
            return self.command_routing[command_type].get("ranking", [])
        return self.routing_schema.get("defaults", {}).get("ranking", ["copilot", "codex", "gemini", "qwen"])

    def get_rank_explanation(self, tool: str, command_type: str) -> str:
        explanation = {
            "copilot": "High quality, strong brand voice",
            "codex": "Fast and cost-effective",
            "gemini": "Large context and analysis strength",
            "qwen": "Low-cost bulk operations",
        }
        return explanation.get(tool, f"Recommended for {command_type}")

    def classify_failure(self, error: str, command: str) -> str:
        lowered = (error or "").lower()
        if "timeout" in lowered:
            return "timeout"
        if "block" in lowered or "captcha" in lowered or "robot" in lowered:
            return "blocked_target"
        if "partial" in lowered:
            return "partial_scrape"
        if "citation" in lowered:
            return "missing_citations"
        return "tool_error"

    def evaluate_quality(self, command: str, result: Dict[str, Any]) -> Dict[str, Any]:
        rule = self.get_route_rule(command)
        gates = rule.get("quality_gates", {})
        threshold = gates.get("min_confidence", rule.get("confidence_threshold", self.routing_schema.get("defaults", {}).get("confidence_threshold", 0.75)))
        confidence = float(result.get("confidence", result.get("quality_score", 0.85)))
        citations_count = int(result.get("citations_count", 0))
        if gates.get("require_citations") and citations_count <= 0:
            return {"gate_passed": False, "confidence": confidence, "failure_type": "missing_citations"}
        if confidence < threshold:
            return {"gate_passed": False, "confidence": confidence, "failure_type": "low_confidence_extraction"}
        return {"gate_passed": True, "confidence": confidence, "failure_type": None}

    def execute_tool(self, tool: str, command: str) -> Dict:
        if self.test_mode and tool in self.test_results:
            test_result = self.test_results[tool]
            if isinstance(test_result, dict):
                return test_result
            if test_result == "success":
                payload = {"status": "success", "output": f"Generated content via {tool}", "tool": tool, "tokens_used": 2500, "confidence": 0.9}
                if "research" in command.lower():
                    payload["citations_count"] = 2
                return payload
            return {"status": "error", "error": test_result, "tool": tool}
        return {"status": "success", "output": f"Generated content via {tool}", "tool": tool, "tokens_used": 2000, "confidence": 0.9, "citations_count": 1}

    def log_command(self, command: str, tool: str, status: str, **extra: Any) -> None:
        entry = {"timestamp": datetime.now().isoformat(), "command": command, "tool": tool, "status": status, **extra}
        self.execution_log.append(entry)
        TOOL_PERF_LOG.parent.mkdir(parents=True, exist_ok=True)
        with TOOL_PERF_LOG.open("a") as f:
            f.write(json.dumps(entry) + "\n")
