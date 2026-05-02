```json
{
  "skill_id": "data-statistical-analysis",
  "name": "Statistical analysis",
  "version": "1.0.0",
  "description": "Quantify trend strength, confidence bands, and opportunity scoring for intel flows.",
  "cowork_skill": "data:statistical-analysis",
  "integration_ref": ".ai/skills/skill_integration/skill.md",
  "commands": ["/intel market snapshot", "/intel opportunities"],
  "agents": ["research-agent", "opportunity-scorer", "trend-miner"],
  "timestamp": "2026-05-02T00:00:00Z"
}
```

# Statistical analysis

## Sovereign mapping

**`data:statistical-analysis`** for `/intel market snapshot` and `/intel opportunities`. See **MARKET INTELLIGENCE** in `.ai/skills/skill_integration/skill.md`.

## Protocol

1. Emit confidence and rationale; weak evidence must be flagged `needs_more_data`.
2. Opportunity scoring should include suggested **next command** per top item.
3. Prefer transparent methods (counts, rates, simple models); document assumptions.
