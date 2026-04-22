"""
🎬 Video Scripting Mastery - Operational Core
Optimizes for Short-form Virality and Long-form Authority through structural retention logic.
"""

from typing import Dict, Any, List
import re

class VideoScriptingMastery:
    def __init__(self):
        self.version = "10.1.0"
        self.logic = "content-creative-narrative"

    def audit_script_retention(self, script_text: str, format_type: str = "short") -> Dict[str, Any]:
        """
        Audits script structure for retention logic (Hooks, curiosity loops, CTAs).
        """
        # Hook Check (First two lines or ~20 words)
        words = script_text.split()
        hook_text = " ".join(words[:20])
        has_hook = any(keyword in hook_text.lower() for keyword in ["why", "stop", "never", "lying", "secret", "how to"])
        
        # ACT/Structure Check
        has_cta = any(cta in script_text.lower() for cta in ["follow", "click", "comment", "subscribe", "buy"])
        
        # Curiosity Loops (Look for questions followed by content)
        loops = len(re.findall(r"\? [A-Z]", script_text))
        
        if format_type == "short":
            score = (30 if has_hook else 0) + (40 if has_cta else 0) + (min(30, loops * 10))
        else: # long form
            score = (20 if has_hook else 0) + (30 if has_cta else 0) + (min(50, loops * 10))
            
        return {
            "format": format_type,
            "retention_score": score,
            "has_scroll_stop_hook": has_hook,
            "has_cta": has_cta,
            "curiosity_loops_detected": loops,
            "is_standard": score >= 70
        }

    def validate_regional_flow(self, script_text: str, target_market: str = "Masri") -> Dict[str, Any]:
        """
        Validates linguistic flow and code-switching parity for MENA markets.
        """
        # Masri dialect cues (simplified)
        masri_cues = ["يا", "إيه", "كدا", "باشا", "تمام"]
        english_tech = ["design", "ui", "ux", "marketing", "code", "ai"]
        
        masri_matches = [cue for cue in masri_cues if cue in script_text]
        tech_matches = [tech for tech in english_tech if tech in script_text.lower()]
        
        # Code-switching is healthy if both are present in a tech script
        health = 1.0 if masri_matches and tech_matches else 0.5
        
        return {
            "target_market": target_market,
            "regional_cues": masri_matches,
            "tech_terms": tech_matches,
            "linguistic_flow_score": health
        }

    def calculate_pacing_metrics(self, script_text: str, target_duration_sec: int) -> Dict[str, Any]:
        """
        Predicts words-per-minute (WPM) and identifies pacing violations.
        Average professional speed: ~150 WPM.
        """
        word_count = len(script_text.split())
        predicted_duration = (word_count / 150) * 60
        
        variance = abs(predicted_duration - target_duration_sec)
        
        return {
            "word_count": word_count,
            "predicted_duration_sec": round(predicted_duration, 2),
            "variance": round(variance, 2),
            "status": "on_target" if variance < (target_duration_sec * 0.1) else "pacing_mismatch"
        }

    def generate_hbco_script(self, segment_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates a high-density HBCO (Hook-Bridge-Content-Offer) script structure.
        """
        hook = segment_data.get("hook", "Stop scrolling if you want OMEGA results.")
        bridge = segment_data.get("bridge", "Most developers miss this one secret.")
        content = segment_data.get("content", "Here is the step-by-step breakdown.")
        offer = segment_data.get("offer", "Join the Sovereign Factory today.")
        
        full_script = f"HOOK: {hook}\nBRIDGE: {bridge}\nCONTENT: {content}\nOFFER: {offer}"
        
        return {
            "script_text": full_script,
            "segments": ["Hook", "Bridge", "Content", "Offer"],
            "target_duration_prediction": self.calculate_pacing_metrics(full_script, 60)["predicted_duration_sec"],
            "status": "STRUCTURE_READY"
        }
