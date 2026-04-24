from .base_adapter import BaseAdapter

class KiloAdapter(BaseAdapter):
    ADAPTER_NAME = "Kilo"
    COST_PER_1K_IN = 0.005
    COST_PER_1K_OUT = 0.015

    def _execute_query(self, prompt, **kwargs):
        # Implementation for Kilo
        # Returns simulated values for now
        return ("Stub response from Kilo", len(prompt)//4, 10)
