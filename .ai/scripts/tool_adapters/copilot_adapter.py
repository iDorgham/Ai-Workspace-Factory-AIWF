from .base_adapter import BaseAdapter

class CopilotAdapter(BaseAdapter):
    ADAPTER_NAME = "Copilot"
    COST_PER_1K_IN = 0.0
    COST_PER_1K_OUT = 0.0

    def _execute_query(self, prompt, **kwargs):
        # Implementation for Copilot
        # Returns simulated values for now
        return ("Stub response from Copilot", len(prompt)//4, 10)
