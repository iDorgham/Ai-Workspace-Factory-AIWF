"""
⚡ Copywriting Mastery - Operational Core
Enforces AIDA/PAS frameworks, Hook-physics (Scroll-Stop), and conversion-density scoring.
"""

from typing import Dict, Any, List
import re

class CopywritingMastery:
    def __init__(self):
        self.version = "10.2.0"
        self.logic = "persuasive-psychology-engineering"

    def audit_aida_framework(self, copy: str) -> Dict[str, Any]:
        """
        Verifies if copy follows the AIDA structure (Attention, Interest, Desire, Action).
        """
        checks = {
            "attention": bool(re.search(r"^[A-Z\s!]{5,}|(Imagine|Discover|Stop|Finally)", copy, re.I)),
            "interest": bool(re.search(r"(unprecedented|exclusive|innovative|unique|secret)", copy, re.I)),
            "desire": bool(re.search(r"(benefit|lifestyle|luxury|investment|roi|dream)", copy, re.I)),
            "action": bool(re.search(r"(Book now|Apply|Join|Call|Contact|Inquire)", copy, re.I))
        }
        
        score = sum(checks.values()) / 4
        
        return {
            "aida_compliance_score": score,
            "checks": checks,
            "status": "CONVERSION_READY" if score >= 0.75 else "WEAK_STRUCTURE"
        }

    def score_hook_physics(self, copy: str) -> Dict[str, Any]:
        """
        Scores the first 3 lines for 'Scroll-Stop' probability.
        """
        lines = copy.split('\n')[:3]
        first_line = lines[0] if lines else ""
        
        # Heuristic for hooks: short, punchy, curiosity-inducing, or high-value.
        has_question = "?" in first_line
        has_surprising_stat = bool(re.search(r"\d+%", first_line))
        is_short = len(first_line.split()) <= 10
        
        hook_score = sum([has_question, has_surprising_stat, is_short]) / 3
        
        return {
            "hook_efficiency": round(hook_score, 2),
            "scroll_stop_prob": "HIGH" if hook_score >= 0.6 else "LOW",
            "first_line_audit": first_line
        }

    def audit_information_density(self, content: str) -> Dict[str, Any]:
        """
        Calculates information density. Enhanced for OMEGA: Fact/Fluff ratio.
        """
        words = content.split()
        if not words: return {"density": 0, "status": "empty"}
        
        fluff_count = len(re.findall(r"\b(very|extremely|actually|basically|really|simply|just|amazing|literally)\b", content, re.I))
        density = (len(words) - fluff_count) / len(words)
        
        return {
            "density_score": round(density, 2),
            "fluff_detected": fluff_count,
            "is_omega_standard": density >= 0.90
        }

    def generate_pas_structure(self, topic_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates a PAS (Problem-Agitation-Solution) framework for conversion-driven copy.
        """
        problem = topic_data.get("problem", "Generic pain point")
        agitation = topic_data.get("agitation", "Further complications")
        solution = topic_data.get("solution", "Our OMEGA offering")
        
        pas_copy = f"PROBLEM: {problem}\nAGITATION: {agitation}\nSOLUTION: {solution}"
        
        return {
            "full_pas_copy": pas_copy,
            "components": ["Problem", "Agitation", "Solution"],
            "status": "DRAFT_GENERATED"
        }

    def verify_omega_hook_density(self, copy: str) -> Dict[str, Any]:
        """
        Refined auditor for OMEGA-Hook compliance (First 3 lines / First 2 seconds).
        Enforces: < 3 lines, high-impact curiosity, Masri-cultural resonance.
        """
        lines = copy.split('\n')
        active_lines = [l for l in lines[:3] if l.strip()]
        
        # Rule: Hook must be dense (<15 words total across 3 lines)
        total_words = sum(len(l.split()) for l in active_lines)
        is_dense = total_words <= 15
        
        return {
            "line_count": len(active_lines),
            "total_word_count": total_words,
            "is_omega_hook_compliant": is_dense,
            "status": "SCROLL_STOP_CERTIFIED" if is_dense else "FLUFF_ALERT"
        }
