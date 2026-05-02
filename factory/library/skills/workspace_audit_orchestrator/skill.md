---
name: workspace-audit-orchestrator
description: Schedule and orchestrate recurring workspace audits, then generate concise health reports from canonical artifacts.
owner_agent: workflow-agent
---

# workspace:audit-orchestrator

Use this skill for recurring audits and report generation without introducing a separate thin agent.

## Responsibilities

- Run the full audit sequence in stable order:
  1. `python3 .ai/scripts/docs_quality_gate.py`
  2. `python3 .ai/scripts/workspace_health.py`
- Produce a human summary from:
  - `.ai/workspace/status.json` (canonical status truth)
  - `.ai/workspace/index.json` (machine-readable index)
  - `.ai/workspace/ORGANIZATION-SUMMARY.txt` (rendered snapshot)
- Attach pass/fail breakdown and clear follow-up actions.

## Boundaries

- Owns orchestration cadence and report synthesis only.
- Does not define lint rules (delegates docs checks to `docs:lint-link-check`).
- Does not change brand/content generation behavior.

## Trigger Phrases

- "audit workspace"
- "run recurring audit"
- "generate workspace health report"
- "nightly audit report"

## Output Contract

- A compact report containing:
  - overall status
  - failed checks (if any)
  - key counts (files, markdown, json, projects)
  - contract/readme health
  - timestamp + next recommended action
