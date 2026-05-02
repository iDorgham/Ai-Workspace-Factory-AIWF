```json
{
  "skill_id": "marketing-competitive-brief",
  "name": "Marketing competitive brief",
  "version": "1.0.0",
  "description": "Structured competitor profiling and positioning narratives for research and compare flows.",
  "cowork_skill": "marketing:competitive-brief",
  "integration_ref": ".ai/skills/skill_integration/skill.md",
  "commands": ["/research competitors", "/compare sovereign vs competitor", "/intel"],
  "agents": ["research-agent", "creator-agent", "intel-synthesizer", "profile-builder"],
  "timestamp": "2026-05-02T00:00:00Z"
}
```

# Marketing competitive brief

## Sovereign mapping

**`marketing:competitive-brief`** across `/research`, `/compare`, and `/intel` flows. See **RESEARCH & COMPETITIVE INTELLIGENCE** and **MARKET INTELLIGENCE** in `.ai/skills/skill_integration/skill.md`.

## Protocol

1. Cover messaging, positioning, services, and proof points with citations or scraped pointers.
2. Pair with `marketing:competitive-analysis` when raw discovery is needed first.
3. After output: creator-agent validates originality **≤ 15%** and applies Sovereign positioning lens.
