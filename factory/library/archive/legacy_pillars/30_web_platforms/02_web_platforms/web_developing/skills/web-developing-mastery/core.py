"""
⚡ Web Developing Mastery - Operational Core
Enforces performance, accessibility (A11y), and modern framework standards.
"""

import re
from typing import Dict, Any, List

class WebDevelopingMastery:
    def __init__(self):
        self.version = "10.1.0"
        self.logic = "web-optimization"

    def run_performance_audit(self, metrics_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyzes web vitals against Sovereign Factory performance budgets.
        New in v10.1.0: Detailed threshold analysis.
        """
        thresholds = {
            "LCP": 2500, # ms
            "FID": 100,  # ms
            "CLS": 0.1,   # score
        }
        
        passes = {}
        for metric, value in metrics_data.items():
            if metric in thresholds:
                passes[metric] = value <= thresholds[metric]
        
        score = (sum(passes.values()) / len(thresholds)) * 100 if thresholds else 100
        
        return {
            "score": score,
            "pass_report": passes,
            "meets_omega_standard": score >= 90
        }

    def validate_accessibility(self, html: str) -> List[str]:
        """
        Scans for WCAG 2.1 violations.
        Uplifted in Phase 2: Added ARIA and label checks.
        """
        violations = []
        
        # Check for image alt text
        if re.search(r"<img(?![^>]*\balt=)[^>]*>", html, re.IGNORECASE):
            violations.append("Missing alt attribute on <img> tag.")
        
        # Check for empty buttons
        if re.search(r"<button[^>]*></button>", html, re.IGNORECASE):
            violations.append("Empty <button> detected; missing inner text or ARIA label.")

        # Check for form labels
        if "<input" in html.lower() and "<label" not in html.lower():
            violations.append("Input detected without associated <label> tag.")
            
        return violations

    def audit_logical_properties(self, css_content: str) -> List[str]:
        """
        Verifies usage of CSS logical properties for RTL/Bilingual support.
        """
        violations = []
        physical_props = ["margin-left", "margin-right", "padding-left", "padding-right", "left:", "right:"]
        for prop in physical_props:
            if prop in css_content.lower():
                violations.append(f"Physical property '{prop}' detected; use logical equivalent (e.g., margin-inline-start).")
        return violations
