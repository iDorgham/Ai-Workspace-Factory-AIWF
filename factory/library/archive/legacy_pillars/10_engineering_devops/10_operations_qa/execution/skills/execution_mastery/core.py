"""
⚡ Execution Mastery - Operational Core
Enforces Spec-Driven Development (SDD) and Mistake Prevention standards.
Governs the "Factory Settings" for all agentic workflows.
"""

from typing import Dict, Any, List
import re

class ExecutionMastery:
    def __init__(self):
        self.version = "10.1.0"
        self.logic = "operational-intelligence"

    def verify_spec_parity(self, spec_content: str, code_content: str) -> Dict[str, Any]:
        """
        Heuristically verifies implementation parity with requirements.
        New in v10.1.0: Requirement extraction and coverage audit.
        """
        # Extract basic requirements (e.g., bullet points or numbered lists)
        requirements = re.findall(r"(?:^|\n)[ \t]*(?:[-*]|\d+\.)[ \t]+([^\n]+)", spec_content)
        
        found_matches = []
        missing_requirements = []
        
        for req in requirements:
            # Simple keyword matching across the code
            keywords = [w for w in re.split(r"\W+", req) if len(w) > 3]
            if any(k.lower() in code_content.lower() for k in keywords):
                found_matches.append(req)
            else:
                missing_requirements.append(req)
        
        coverage = (len(found_matches) / len(requirements)) * 100 if requirements else 100
        
        return {
            "is_standard": coverage >= 85,
            "coverage_percentage": coverage,
            "missing_features": missing_requirements,
            "requirements_detected": len(requirements)
        }

    def distill_anti_patterns(self, session_logs: List[str]) -> List[str]:
        """
        Automated extraction of recurring error patterns from logs.
        Uplifted in Phase 2: Deduplication and weight assignment.
        """
        raw_patterns = []
        for log in session_logs:
            if re.search(r"error|failure|exception|crash", log, re.IGNORECASE):
                # Clean the log line to distill the core message
                clean = re.sub(r"[\d\-: ]{10,}", "", log).strip()
                raw_patterns.append(clean)
        
        # Deduplicate while preserving order
        unique_patterns = list(dict.fromkeys(raw_patterns))
        return unique_patterns

    def enforce_sdd_workflow(self, task_state: str) -> bool:
        """
        Validates that the current task is following the SDD mandatory sequence.
        (Plan -> Execute -> Verify)
        """
        required_phases = ["planning", "execution", "verification"]
        return all(phase in task_state.lower() for phase in required_phases)
