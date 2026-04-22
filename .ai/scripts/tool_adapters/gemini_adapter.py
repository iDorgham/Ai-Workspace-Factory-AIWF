from .base_adapter import BaseAdapter

class GeminiAdapter(BaseAdapter):
    ADAPTER_NAME = "Gemini"
    COST_PER_1K_IN = 0.000125
    COST_PER_1K_OUT = 0.000375

    def _execute_query(self, prompt, **kwargs):
        # Implementation for Gemini
        # Returns simulated values for now
        return ("Stub response from Gemini", len(prompt)//4, 10)
