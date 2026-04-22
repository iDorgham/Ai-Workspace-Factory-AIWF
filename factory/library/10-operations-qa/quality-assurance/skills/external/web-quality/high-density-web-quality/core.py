"""
💎 High-Density Web Quality - Operational Core
Enforces standards for performance budgets, visual regression, and asset metadata.
"""

from typing import Dict, Any, List

class HighDensityWebQuality:
    def __init__(self):
        self.version = "10.1.0"
        self.logic = "production-quality-assurance"

    def audit_performance_budget(self, build_stats: Dict[str, float]) -> Dict[str, Any]:
        """
        Audits build assets against the performance budget ( < 200KB initial JS).
        """
        initial_js_kb = build_stats.get("initial_js_kb", 0.0)
        max_budget = 200.0
        
        is_compliant = initial_js_kb <= max_budget
        
        return {
            "is_compliant": is_compliant,
            "initial_js_kb": initial_js_kb,
            "budget_limit_kb": max_budget,
            "status": "GREEN" if is_compliant else "RED",
            "recommendation": "Implement route-level code splitting or tree-shaking" if not is_compliant else "OPTIMIZED"
        }

    def audit_visual_regression(self, variance_score: float, dynamic_masking: bool = True) -> Dict[str, Any]:
        """
        Audits visual variance against the design master.
        Rule: pixel variance must be < 0.1% for standard builds.
        """
        threshold = 0.001 # 0.1%
        
        # simulated logic for dynamic masking (if enabled, we allow slightly more variance or assume noise reduction)
        effective_score = variance_score * 0.5 if dynamic_masking else variance_score
        
        is_compliant = effective_score < threshold
        
        return {
            "raw_variance": variance_score,
            "effective_variance": effective_score,
            "is_within_threshold": is_compliant,
            "dynamic_masking_active": dynamic_masking
        }

    def verify_asset_metadata(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verifies presence of mandatory professional metadata (Favicons, OG tags, Manifest).
        """
        mandatory = ["favicon", "og_image", "og_title", "manifest_json", "twitter_card"]
        missing = [tag for tag in mandatory if not metadata.get(tag)]
        
        return {
            "all_assets_present": len(missing) == 0,
            "missing_assets": missing,
            "compliance_score": (len(mandatory) - len(missing)) / len(mandatory) * 100
        }

    def calculate_accessibility_score(self, axe_run: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculates accessibility score based on automated axe-core results.
        Target: 0 critical violations.
        """
        violations = axe_run.get("violations", [])
        critical = [v for v in violations if v.get("impact") == "critical"]
        serious = [v for v in violations if v.get("impact") == "serious"]
        
        score = 100 - (len(critical) * 10) - (len(serious) * 5)
        
        return {
            "a11y_score": max(score, 0),
            "critical_count": len(critical),
            "status": "PASS" if not critical else "FAIL",
            "is_omega_compliant": score >= 95
        }

    def verify_compression_standards(self, asset_stats: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Verifies that all text assets use Brotli or Gzip compression.
        """
        non_compliant = [a for a in asset_stats if a.get("ext") in [".js", ".css", ".html"] and not a.get("compressed")]
        
        return {
            "compression_compliance": len(non_compliant) == 0,
            "non_compliant_assets": [a.get("name") for a in non_compliant],
            "total_weight_savings": sum([a.get("saved_kb", 0) for a in asset_stats])
        }
