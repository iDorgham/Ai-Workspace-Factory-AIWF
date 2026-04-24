import time
from .cost_tracker import CostTracker

class BaseAdapter:
    ADAPTER_NAME = "BASE"
    COST_PER_1K_IN = 0.0
    COST_PER_1K_OUT = 0.0

    def query(self, prompt, **kwargs):
        start = time.time()
        # Stub logic to be overridden
        response, tokens_in, tokens_out = self._execute_query(prompt, **kwargs)
        latency = (time.time() - start) * 1000
        
        cost = (tokens_in / 1000.0) * self.COST_PER_1K_IN + (tokens_out / 1000.0) * self.COST_PER_1K_OUT
        CostTracker.log_invocation(self.ADAPTER_NAME, tokens_in, tokens_out, latency, cost)
        return response

    def _execute_query(self, prompt, **kwargs):
        """Must return (response_text, tokens_in, tokens_out)"""
        raise NotImplementedError("Adapters must implement _execute_query")
