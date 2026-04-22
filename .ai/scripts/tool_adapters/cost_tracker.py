import os
import time
import json
from datetime import datetime

LOG_FILE = '.ai/logs/health_metrics.log'

class CostTracker:
    @staticmethod
    def log_invocation(adapter_name, tokens_in, tokens_out, latency_ms, cost_estimate):
        """Append-only logging for cost and health metrics."""
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "adapter": adapter_name,
            "latency_ms": latency_ms,
            "tokens": {"in": tokens_in, "out": tokens_out},
            "cost_usd": cost_estimate
        }
        
        # Ping check <50ms overhead (pure IO)
        with open(LOG_FILE, 'a') as f:
            f.write(json.dumps(entry) + '\n')

    @staticmethod
    def health_ping():
        """Returns True if the system is ready, ensuring ultra-low latency."""
        start = time.time()
        # Simulated health check
        healthy = os.path.exists('factory/.env')
        latency = (time.time() - start) * 1000
        if latency > 50:
            print(f"Warning: Health ping latency spike: {latency:.2f}ms")
        return healthy
