from .base_adapter import BaseAdapter

class CodexAdapter(BaseAdapter):
    ADAPTER_NAME = "Codex"
    COST_PER_1K_IN = 0.0015
    COST_PER_1K_OUT = 0.002

    def _execute_query(self, prompt, **kwargs):
        # Implementation for Codex
        # Returns simulated values for now
        return ("Stub response from Codex", len(prompt)//4, 10)
