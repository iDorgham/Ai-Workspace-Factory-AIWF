"""
⚡ Proactive Agent Mastery - Operational Core
Enforces standards for anticipating user needs, preventative gap discovery, and weighted risk scoring.
"""

from typing import Dict, Any, List

class ProactiveAgentMastery:
    def __init__(self):
        self.version = "10.1.0"
        self.logic = "agentic-orchestration-forecasting"

    def discover_environment_gaps(self, intent: str, environment_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Scans environment for missing pre-requisites based on task intent.
        """
        # Heuristic mapping for common intents
        pre_reqs = {
            "install react": ["node", "npm"],
            "deploy azure": ["az-cli", "azure-managed-identity"],
            "test code": ["pytest", "unittest"],
            "bundle site": ["webpack", "vite", "next"]
        }
        
        intent_lower = intent.lower()
        findings = []
        
        for key, deps in pre_reqs.items():
            if key in intent_lower:
                for dep in deps:
                    if not environment_state.get(dep, False):
                        findings.append(dep)
                        
        return {
            "intent": intent,
            "has_gaps": len(findings) > 0,
            "missing_dependencies": findings,
            "recommendation": f"Install {', '.join(findings)} before proceeding with '{intent}'" if findings else "READY_FOR_EXECUTION"
        }

    def generate_state_summary(self, turn_count: int, context_saturation: float) -> Dict[str, Any]:
        """
        Heuristic for proactive state-summary generation.
        Rule: Every 10 turns OR > 80% context saturation.
        """
        should_summarize = turn_count >= 10 or context_saturation >= 80.0
        
        return {
            "should_summarize": should_summarize,
            "trigger": "SATURATION_LIMIT" if context_saturation >= 80.0 else ("PERIODIC_CHECK" if turn_count >= 10 else "NONE"),
            "saturation": context_saturation,
            "turn_index": turn_count
        }

    def calculate_risk_score(self, planned_action: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculates safety score for autonomous actions based on a weighted matrix.
        Factors: action_type (delete/write), lines_impacted, and dependency_depth.
        """
        action_type = planned_action.get("type", "read")
        impact = planned_action.get("lines_impacted", 0)
        depth = planned_action.get("dependency_depth", 0)
        
        # Base risk from action type
        score = {"delete": 50, "write": 20, "read": 0}.get(action_type, 10)
        
        # Scaling risk from impact
        score += min(30, impact // 5)
        
        # Scaling risk from dependency depth
        score += min(20, depth * 5)
        
        is_safe = score < 70
        
        return {
            "risk_score": score,
            "is_autonomous_safe": is_safe,
            "requires_approval": not is_safe,
            "risk_mitigation": "Request explicit user approval" if not is_safe else "PROCEED_WITH_CAUTION"
        }
