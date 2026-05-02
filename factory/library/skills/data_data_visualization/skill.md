```json
{
  "skill_id": "data-data-visualization",
  "name": "Data visualization",
  "version": "1.0.0",
  "description": "Optional charts and matrix summaries for intel and opportunity outputs.",
  "cowork_skill": "data:data-visualization",
  "integration_ref": ".ai/skills/skill_integration/skill.md",
  "agents": ["research-agent", "intel-synthesizer"],
  "timestamp": "2026-05-02T00:00:00Z"
}
```

# Data visualization

## Sovereign mapping

**`data:data-visualization`** — e.g. opportunity map summary for `/intel opportunities`. See **MARKET INTELLIGENCE** in `.ai/skills/skill_integration/skill.md`.

## Protocol

1. Prefer markdown tables or Mermaid when embedding in repo docs; avoid binary blobs unless requested.
2. Label axes, units, and data vintage; mark low-confidence slices as `needs_more_data`.
3. Keep file paths under sovereign-owned `content/` trees per command conventions.
