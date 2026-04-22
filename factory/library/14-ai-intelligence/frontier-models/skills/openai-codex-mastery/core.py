"""
🤖 OpenAI & Codex Mastery - Operational Core
Enforces high-precision code generation, context-slicing, and strict function-calling schemas.
"""

from typing import Dict, Any, List
import json

class OpenAIMastery:
    def __init__(self):
        self.version = "10.1.0"
        self.logic = "high-precision-orchestration"

    def slice_context_window(self, code_lines: List[str], target_index: int) -> List[str]:
        """
        Calculates the optimal 'Context Slice' for code modification.
        Rule: Do not exceed 1,000 lines. Focus on Interface + Target Implementation.
        """
        max_slice = 1000
        start = max(0, target_index - (max_slice // 2))
        end = min(len(code_lines), start + max_slice)
        
        # Adjust start if end hit the ceiling
        if end == len(code_lines):
            start = max(0, end - max_slice)
            
        return code_lines[start:end]

    def validate_function_schema(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enforced strict schema validation to minimize model hallucinations.
        Rule: All tool definitions must include required parameters and dense descriptions (>20 chars).
        """
        params = schema.get("parameters", {})
        properties = params.get("properties", {})
        required = params.get("required", [])
        
        missing_docs = []
        for name, prop in properties.items():
            desc = prop.get("description", "")
            if len(desc) < 20:
                missing_docs.append(f"Property '{name}' has low-density documentation ({len(desc)} chars).")
        
        is_valid = len(required) > 0 and len(missing_docs) == 0
        
        return {
            "is_schema_compliant": is_valid,
            "required_count": len(required),
            "missing_documentation": missing_docs,
            "status": "PRODUCTION_READY" if is_valid else "HALLUCINATION_RISK"
        }

    def audit_token_economy(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Audits request config for noise-reduction and stop sequences.
        """
        stop_sequences = config.get("stop", [])
        logit_bias = config.get("logit_bias", {})
        has_json_mode = config.get("response_format", {}).get("type") == "json_object"
        
        score = 0
        if stop_sequences: score += 33
        if logit_bias: score += 33
        if has_json_mode: score += 34
        
        return {
            "economy_score": score,
            "has_stop_sequences": len(stop_sequences) > 0,
            "has_logit_bias": len(logit_bias) > 0,
            "is_json_optimized": has_json_mode
        }
