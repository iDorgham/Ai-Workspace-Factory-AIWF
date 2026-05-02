```json
{
  "id": "silent-git-protocol",
  "version": "1.0.0",
  "triggers": ["spec_validated", "health>=85"],
  "inputs": ["workspace_state", "reasoning_hash"],
  "outputs": ["commit_id", "tag_id", "trace_log"],
  "sovereign_tier": "OMEGA",
  "traceability_schema": "workflow.jsonl",
  "library_category": "Repository & Versioning",
  "mode": "silent"
}
```
