"""
⚡ Quality Assurance Mastery - Operational Core
Enforces automated testing, structural library health, and smoke-test verification.
"""

from typing import Dict, Any, List
import os

class QualityAssuranceMastery:
    def __init__(self):
        self.version = "10.1.0"
        self.logic = "qa-orchestration"

    def calculate_test_coverage(self, coverage_data: Dict[str, Any]) -> float:
        """Calculates total coverage percentage from raw data."""
        return coverage_data.get("total_percentage", 0.0)

    def audit_library_health(self, nodes: List[str]) -> Dict[str, Any]:
        """
        Audits skill nodes for structural consistency (SKILL.md, core.py, tests presence).
        """
        compliant = []
        violations = []
        
        for node in nodes:
            # Simulated check logic
            has_md = os.path.exists(os.path.join(node, "SKILL.md"))
            has_core = os.path.exists(os.path.join(node, "core.py"))
            has_tests = os.path.exists(os.path.join(node, "tests/test_core.py"))
            
            if has_md and has_core and has_tests:
                compliant.append(node)
            else:
                missing = []
                if not has_md: missing.append("SKILL.md")
                if not has_core: missing.append("core.py")
                if not has_tests: missing.append("test_core.py")
                violations.append({"node": node, "missing": missing})
                
        health_score = (len(compliant) / len(nodes) * 100) if nodes else 0
        
        return {
            "health_score": round(health_score, 2),
            "compliant_count": len(compliant),
            "violation_count": len(violations),
            "violations": violations,
            "status": "HEALTHY" if health_score >= 95 else "DEGRADED"
        }

    def run_smoke_test_engine(self, node_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Verifies baseline health (smoke tests) for all critical engine nodes.
        """
        failures = [r for r in node_results if not r.get("passed", False)]
        
        return {
            "is_smoke_pass": len(failures) == 0,
            "failure_count": len(failures),
            "failed_nodes": [r.get("node") for r in failures],
            "recommendation": "Investigate failed nodes immediately" if failures else "BASELINE_STABLE"
        }
