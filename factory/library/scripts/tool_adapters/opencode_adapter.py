from .base_adapter import BaseAdapter

class OpencodeAdapter(BaseAdapter):
    ADAPTER_NAME = "Opencode"
    COST_PER_1K_IN = 0.0
    COST_PER_1K_OUT = 0.0

    def _execute_query(self, prompt, **kwargs):
        # Implementation for Opencode
        # Returns simulated values for now
        return ("Stub response from Opencode", len(prompt)//4, 10)
