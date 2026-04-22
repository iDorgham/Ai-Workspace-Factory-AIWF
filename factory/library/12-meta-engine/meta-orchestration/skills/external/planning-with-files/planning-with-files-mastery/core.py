"""
📁 Planning with Files (SDD) - Operational Core
Enforces Spec-Driven Development (SDD) standards through artifact state-machines.
"""

from typing import Dict, Any, List
import datetime

class PlanningWithFilesMastery:
    def __init__(self):
        self.version = "10.1.0"
        self.logic = "spec-driven-development-physics"

    def audit_artifact_sync(self, artifact_states: Dict[str, Any]) -> Dict[str, Any]:
        """
        Audits synchronization between task.md, implementation_plan.md, and codebase reality.
        Rule: task.md must perfectly match current workspace reality.
        """
        plan_approved = artifact_states.get("plan_approved", False)
        task_list_exists = artifact_states.get("task_list_exists", False)
        code_drift_detected = artifact_states.get("code_drift_detected", False)
        
        is_synchronized = plan_approved and task_list_exists and not code_drift_detected
        
        return {
            "is_synchronized": is_synchronized,
            "drift_identified": code_drift_detected,
            "status": "SDD_COMPLIANT" if is_synchronized else "SPEC_DIVERGENCE",
            "recommendation": "Update task.md before proceeding with code changes." if code_drift_detected else "CONTINUE"
        }

    def validate_discovery_capture(self, discovery_log: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Ensures new structural facts are captured in implementation_plan.md.
        Rule: Halt coding and update plan upon encountering a structural constraint.
        """
        uncaptured_facts = [f for f in discovery_log if not f.get("is_in_spec", False)]
        
        is_safe = len(uncaptured_facts) == 0
        
        return {
            "is_spec_safe": is_safe,
            "uncaptured_structural_facts": uncaptured_facts,
            "required_action": "UPDATE_PLAN_BEFORE_RESUMING" if not is_safe else "NONE"
        }

    def verify_turn_transition(self, session_metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verifies state persistence across turns.
        Rule: Transition must be seamless because state is persisted in files.
        """
        last_save = session_metadata.get("last_artifact_update_time")
        current_time = datetime.datetime.now()
        
        # Heuristic: Artifacts should be updated frequently (e.g., within last 30 mins for active sessions)
        is_persistent = False
        if last_save:
            delta = (current_time - last_save).total_seconds() / 60
            is_persistent = delta < 30
            
        return {
            "is_state_persisted": is_persistent,
            "minutes_since_last_sync": round((current_time - last_save).total_seconds() / 60, 2) if last_save else -1,
            "transition_health": "OPTIMIZED" if is_persistent else "RISKY_STATE_LOSS"
        }
