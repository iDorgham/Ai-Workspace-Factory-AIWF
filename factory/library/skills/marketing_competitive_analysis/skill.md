```json
{
  "skill_id": "marketing-competitive-analysis",
  "name": "Marketing competitive analysis",
  "version": "1.0.0",
  "description": "Discovery-heavy competitor signals: topics, positioning gaps, and evidence-scored comparisons.",
  "cowork_skill": "marketing:competitive-analysis",
  "integration_ref": ".ai/skills/skill_integration/skill.md",
  "commands": ["/research competitors", "/compare sovereign vs competitor", "/intel"],
  "agents": ["research-agent", "creator-agent", "trend-miner", "comparison-analyst"],
  "timestamp": "2026-05-02T00:00:00Z"
}
```

# Marketing competitive analysis

## Sovereign mapping

**`marketing:competitive-analysis`** for `/research competitors`, `/compare`, and `/intel` flows. See **RESEARCH & COMPETITIVE INTELLIGENCE** and **MARKET INTELLIGENCE** in `.ai/skills/skill_integration/skill.md`.

## Protocol

1. Provide raw competitive data layer with relevance scoring; pair with `marketing:competitive-brief` for narrative packaging.
2. Mark low-evidence claims; `trend-miner` outputs should include confidence values.
3. Respect data residency and scraping policy for the active workspace region.
