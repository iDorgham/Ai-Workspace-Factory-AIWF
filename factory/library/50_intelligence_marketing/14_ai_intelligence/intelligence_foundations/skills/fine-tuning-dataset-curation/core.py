"""
🧪 Fine-Tuning & Dataset Curation - Operational Core
Enforces Dataset Purity and Formatting protocols for LLM training.
"""

from typing import List, Dict, Any
import re

class FineTuningMastery:
    def __init__(self):
        self.version = "10.0.0"
        self.logic = "dataset-purity"

    def validate_jsonl_format(self, data: List[Dict[str, Any]]) -> bool:
        """Ensures each record has mandatory System, User, and Assistant roles."""
        required_roles = {"system", "user", "assistant"}
        for record in data:
            if "messages" not in record:
                return False
            roles = {m.get("role") for m in record["messages"]}
            if not required_roles.issubset(roles):
                return False
        return True

    def scrub_pii(self, text: str) -> str:
        """Simplified RegEx scrubber for common PII patterns."""
        # Scrub emails
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL_REDACTED]', text)
        # Scrub phone numbers (simple pattern)
        text = re.sub(r'\+?\d{1,3}[-.\s]?\d{3}[-.\s]?\d{3}[-.\s]?\d{4}', '[PHONE_REDACTED]', text)
        return text
