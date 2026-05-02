```json
{
  "skill_id": "brand-voice-enforcement",
  "name": "Brand voice enforcement",
  "version": "1.0.0",
  "description": "Validate generated brand artifacts for internal consistency and enforceable rules.",
  "cowork_skill": "brand-voice:brand-voice-enforcement",
  "integration_ref": ".ai/skills/skill_integration/skill.md",
  "commands": ["/brand", "/review"],
  "agents": ["brand-agent", "workflow-agent"],
  "timestamp": "2026-05-02T00:00:00Z"
}
```

# Brand voice enforcement

## Sovereign mapping

**`brand-voice:brand-voice-enforcement`** post-generation for `/brand` and enforcement scoring in `/review` when the brand-voice plugin path is active. See **BRAND DISCOVERY & VOICE** in `.ai/skills/skill_integration/skill.md`.

## Protocol

1. Check `style_rules.md` (or generated equivalent) for contradictions, gaps, and non-enforceable phrasing.
2. Return pass/fail plus concrete rule edits; threshold aligns with brand gate (**≥ 92%**) when used as scorer input.
3. Do not weaken legal or compliance constraints to raise style scores.
