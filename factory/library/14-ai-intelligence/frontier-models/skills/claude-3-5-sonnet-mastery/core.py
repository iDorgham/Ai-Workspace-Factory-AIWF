"""
🦅 Claude 3.5 Sonnet Mastery - Operational Core
Enforces industrial-grade XML-structured prompting, reasoning protocols, and high-density context management.
"""

import re
from typing import Dict, Any, List

class ClaudeMastery:
    def __init__(self):
        self.version = "10.1.0"
        self.logic = "structured-cognitive-engineering"

    def validate_prompt_structure(self, prompt: str) -> Dict[str, Any]:
        """
        Ensures XML tags are present for context, thinking, and instructions.
        Rule: Structured tags maximize instruction adherence in long-context scenarios.
        """
        required_tags = ["context", "instruction"]
        results = {}
        missing = []
        
        for tag in required_tags:
            pattern = rf"<{tag}>.*?</{tag}>"
            if not re.search(pattern, prompt, re.DOTALL):
                missing.append(tag)
        
        return {
            "is_structured": len(missing) == 0,
            "missing_tags": missing,
            "has_thinking_tag": "<thinking>" in prompt.lower()
        }

    def monitor_context_window(self, estimated_tokens: int) -> Dict[str, Any]:
        """
        Monitors token density against Claude 3.5 Sonnet's 200k limit.
        """
        limit = 200000
        saturation = (estimated_tokens / limit) * 100
        
        risk = "LOW"
        if saturation > 80:
            risk = "CRITICAL"
        elif saturation > 50:
            risk = "MEDIUM"
            
        return {
            "estimated_tokens": estimated_tokens,
            "saturation_percentage": round(saturation, 2),
            "risk_level": risk,
            "recommendation": "Initiate state-summary compression" if risk == "CRITICAL" else "CONTINUE"
        }

    def optimize_instruction_position(self, prompt_parts: Dict[str, str]) -> str:
        """
        Optimizes for recency bias by ensuring critical instructions are at the tail.
        """
        context = prompt_parts.get("context", "")
        instruction = prompt_parts.get("instruction", "")
        
        # Rule: instruction must follow context
        structured_prompt = f"<context>\n{context}\n</context>\n\n<instruction>\n{instruction}\n</instruction>"
        return structured_prompt

    def scrub_pii(self, content: str) -> str:
        """
        Baseline safety filter for emails and phones (Internal Sovereign Standard).
        """
        content = re.sub(r"[\w\.-]+@[\w\.-]+\.\w+", "[EMAIL_REDACTED]", content)
        content = re.sub(r"\+?\d{10,12}", "[PHONE_REDACTED]", content)
        return content

    def validate_reasoning_integrity(self, response: str) -> Dict[str, Any]:
        """
        Verifies that a logic-intensive response contains a valid reasoning (<thinking>) block.
        """
        has_thinking = bool(re.search(r"<thinking>.*?</thinking>", response, re.DOTALL))
        
        return {
            "has_reasoning_chain": has_thinking,
            "status": "VALIDATED" if has_thinking else "REASONING_MISSING",
            "recommendation": "Force <thinking> tags for complex logic tasks." if not has_thinking else "PROCEED"
        }

    def score_instruction_efficiency(self, prompt: str) -> Dict[str, Any]:
        """
        Scores prompt based on instruction character counts and clarity ratio.
        """
        instruction_match = re.search(r"<instruction>(.*?)</instruction>", prompt, re.DOTALL)
        if not instruction_match:
            return {"efficiency_score": 0, "status": "NO_INSTRUCTION_TAGS"}
            
        instruction_body = instruction_match.group(1).strip()
        char_count = len(instruction_body)
        
        # Heuristic: Optimal instruction density is 100-1000 characters for complex tasks.
        is_efficient = 100 <= char_count <= 2000
        
        return {
            "instruction_char_count": char_count,
            "is_within_efficiency_limit": is_efficient,
            "efficiency_score": 1.0 if is_efficient else 0.5
        }
    def compress_prompt(self, prompt: str, enabled: bool = False) -> str:
        """
        Removes conversational padding and redundant context if enabled.
        Rule: Industrial-grade tokens should be 100% information-dense.
        """
        if not enabled:
            return prompt
            
        # Strip common conversational fillers (simplified)
        fillers = [
            "I'm happy to help,", "Sure thing!", "As an AI assistant,", 
            "Please let me know if you need anything else."
        ]
        compressed = prompt
        for filler in fillers:
            compressed = compressed.replace(filler, "")
            
        # Strip leading/trailing whitespace
        compressed = compressed.strip()
        
        return compressed

    def inject_thinking_protocol(self, prompt: str) -> str:
        """
        Forces a <thinking> block at the beginning of the response.
        Essential for OMEGA-tier complex reasoning.
        """
        if "<thinking>" not in prompt.lower():
            return f"Begin your response with a <thinking> tag to analyze the problem step-by-step.\n\n{prompt}"
        return prompt
