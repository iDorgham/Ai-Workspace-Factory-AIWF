```json
{
  "skill_id": "data-interactive-dashboard-builder",
  "name": "Interactive dashboard builder",
  "version": "1.0.0",
  "description": "Build HTML dashboards from sync logs, quality reports, and workspace health signals on request.",
  "cowork_skill": "data:interactive-dashboard-builder",
  "integration_ref": ".ai/skills/skill_integration/skill.md",
  "agents": ["guide-agent"],
  "timestamp": "2026-05-02T00:00:00Z"
}
```

# Interactive dashboard builder

## Sovereign mapping

**`data:interactive-dashboard-builder`** for reporting and dashboards (on request). See **WORKFLOW & QUALITY** in `.ai/skills/skill_integration/skill.md`.

## Protocol

1. Read canonical inputs (e.g. `.ai/workspace/status.json`, `.ai/workspace/index.json`, quality reports) when present.
2. Emit self-contained HTML or linked static assets; no remote telemetry without explicit config.
3. Document how to regenerate the dashboard in a short README section or comment block.
