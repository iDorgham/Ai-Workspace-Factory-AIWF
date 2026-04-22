"""
⚡ AI Automation Ops Mastery - Operational Core
SLA monitoring, resource cost auditing, and token-budget reconciliation for automated pipelines.
"""

from typing import Dict, Any, List

class AiAutomationOpsMastery:
    def __init__(self):
        self.version = "10.1.0"
        self.logic = "data-intelligence-ops"

    def audit_resource_costs(self, pipeline_data: Dict[str, Any], budget: float) -> Dict[str, Any]:
        """
        Audits token usage vs. budget for automated AI pipelines.
        """
        token_cost = pipeline_data.get("tokens_used", 0) * pipeline_data.get("cost_per_token", 0.00001)
        infra_cost = pipeline_data.get("infra_fixed_cost", 0)
        total_cost = token_cost + infra_cost
        
        return {
            "total_actual_cost": round(total_cost, 4),
            "budget_threshold": budget,
            "is_within_budget": total_cost <= budget,
            "variance": round(budget - total_cost, 4),
            "critical_warning": total_cost > (budget * 0.9)
        }

    def monitor_sla_compliance(self, executions: List[Dict[str, Any]], target_latency_ms: int = 5000) -> Dict[str, Any]:
        """
        Monitors SLA compliance (latency and success rate) for automated pipelines.
        """
        if not executions:
            return {"status": "no_data"}
            
        success_count = sum(1 for e in executions if e.get("status") == "success")
        avg_latency = sum(e.get("latency_ms", 0) for e in executions) / len(executions)
        
        success_rate = (success_count / len(executions)) * 100
        
        return {
            "avg_latency_ms": round(avg_latency, 2),
            "success_rate_percent": round(success_rate, 2),
            "is_sla_compliant": success_rate >= 99.5 and avg_latency <= target_latency_ms,
            "executions_count": len(executions)
        }

    def detect_pipeline_bottlenecks(self, steps: List[Dict[str, Any]]) -> List[str]:
        """
        Identifies high-latency steps in the automation pipeline.
        """
        # A bottleneck is any step taking > 40% of total pipeline time or > 3000ms
        bottlenecks = []
        for step in steps:
            duration = step.get("duration_ms", 0)
            if duration > 3000:
                bottlenecks.append(f"CRITICAL Bottleneck: Step '{step.get('name')}' is too slow ({duration}ms)")
                
        return bottlenecks
