```json
{
  "id": "sovereign-deploy-router",
  "version": "1.0.0",
  "triggers": ["release_tagged", "compliance_verified"],
  "inputs": ["shard_id", "target_region"],
  "outputs": ["routing_confirmation", "heartbeat_status"],
  "sovereign_tier": "SOVEREIGN",
  "traceability_schema": "distribution_log.json",
  "library_category": "Global Shard Distribution",
  "mode": "silent"
}
```
