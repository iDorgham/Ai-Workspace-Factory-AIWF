"""
🌍 Bilingual Next.js Performance - Operational Core
Enforces RTL integrity, GCC-specific performance targets, and font-subsetting audits.
"""

from typing import Dict, Any, List
import re

class BilingualNextJSPerformance:
    def __init__(self):
        self.version = "10.1.0"
        self.logic = "regional-performance-optimization"

    def audit_logical_properties(self, css_content: str) -> Dict[str, Any]:
        """
        Scans for legacy directional properties (left/right) instead of logical (ps/pe/ms/me).
        Rule: Use logical properties to ensure perfect AR/EN bilingual rendering.
        """
        forbidden = [
            r"padding-left", r"padding-right", 
            r"margin-left", r"margin-right",
            r"border-left", r"border-right",
            r"text-align:\s*(left|right)"
        ]
        
        violations = []
        for pattern in forbidden:
            matches = re.findall(pattern, css_content)
            if matches:
                violations.append(f"Hardcoded directional property pattern found: '{pattern}' ({len(matches)} occurrences)")
                
        return {
            "is_bilingual_compliant": len(violations) == 0,
            "violations": violations,
            "recommendation": "Use ps-, pe-, ms-, me-, or text-start/text-end logical properties."
        }

    def audit_font_subsetting(self, font_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Audits Arabic font-subsetting to reduce bundle weight.
        Rule: Subsetted fonts should save ~200-300KB over full Unicode ranges.
        """
        full_size_kb = font_config.get("full_size_kb", 500.0)
        is_subsetted = font_config.get("is_subsetted", False)
        
        expected_savings = 300.0 # Standard heuristic from SKILL.md
        predicted_size = full_size_kb - (expected_savings if not is_subsetted else 0)
        
        return {
            "current_is_subsetted": is_subsetted,
            "potential_savings_kb": expected_savings if not is_subsetted else 0.0,
            "is_optimized": is_subsetted,
            "estimated_final_weight_kb": full_size_kb if is_subsetted else predicted_size
        }

    def verify_regional_edge_caching(self, ttfb_stats: Dict[str, float]) -> Dict[str, Any]:
        """
        Verifies Time to First Byte (TTFB) in GCC regions.
        Target: < 200ms for optimal MENA experience.
        """
        regions = ["UAE", "KSA", "Egypt"]
        violations = []
        
        for region in regions:
            ttfb = ttfb_stats.get(region, 0.0)
            if ttfb > 200.0:
                 violations.append(f"Region {region} TTFB is high: {ttfb}ms (Target: < 200ms)")
                 
        return {
            "is_regionally_optimized": len(violations) == 0,
            "violations": violations,
            "target_ttfb": 200.0
        }
