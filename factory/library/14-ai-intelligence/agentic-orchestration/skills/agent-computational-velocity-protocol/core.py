"""
⚡ Agent Computational Velocity Protocol - Operational Core
Enforces Context Pruning and JSON-First output protocols for high-speed inference.
"""

from typing import List, Dict, Any

class VelocityProtocol:
    def __init__(self):
        self.version = "10.0.0"
        self.logic = "efficiency-optimization"

    def prune_context(self, file_paths: List[str], max_files: int = 3) -> List[str]:
        """Enforces the 'Need-to-Know' rule: limit RAG context to max_files."""
        if len(file_paths) <= max_files:
            return file_paths
        return file_paths[:max_files]

    def inject_efficiency_system_rule(self, system_prompt: str) -> str:
        """Appends the CRITICAL SYSTEM RULE to force high-speed processing."""
        rule = ("\nCRITICAL SYSTEM RULE: Output strictly the <COMMAND> or <JSON> required for execution. "
                "Zero conversational filler. Maximize token efficiency.")
        return f"{system_prompt}{rule}"

    def strip_conversational_padding(self, text: str) -> str:
        """Removes common AI conversational filler phrases."""
        fillers = ["Certainly!", "I will now do", "Of course,", "Sure,"]
        for filler in fillers:
            text = text.replace(filler, "")
        return text.strip()

    def track_latency(self, start_time: float, end_time: float) -> Dict[str, Any]:
        """
        Tracks model response latency and scores it against OMEGA standards (Target < 2.0s).
        """
        latency = end_time - start_time
        score = 1.0 if latency < 2.0 else 0.5
        
        return {
            "latency_sec": round(latency, 2),
            "performance_score": score,
            "status": "OMEGA_VELOCITY" if score == 1.0 else "INFRASTRUCTURE_LAG"
        }

    def score_token_efficiency(self, token_count: int, information_chars: int) -> Dict[str, Any]:
        """
        Calculates the information-to-token ratio (Goal: > 4.0 chars/token).
        """
        if token_count == 0: return {"efficiency_ratio": 0}
        ratio = information_chars / token_count
        
        return {
            "efficiency_ratio": round(ratio, 2),
            "is_token_optimized": ratio >= 4.0,
            "status": "DENSE_INTELLIGENCE" if ratio >= 4.0 else "PADDING_DETECTED"
        }
