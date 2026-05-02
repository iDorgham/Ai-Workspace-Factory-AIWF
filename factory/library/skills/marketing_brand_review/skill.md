```json
{
  "skill_id": "marketing-brand-review",
  "name": "Marketing brand review",
  "version": "1.0.0",
  "description": "Brand voice compliance scoring and practical writing guidance against sovereign rubrics.",
  "cowork_skill": "marketing:brand-review",
  "integration_ref": ".ai/skills/skill_integration/skill.md",
  "commands": ["/brand workshop", "/review", "/polish"],
  "agents": ["brand-agent", "workflow-agent", "seo-agent"],
  "timestamp": "2026-05-02T00:00:00Z"
}
```

# Marketing brand review

## Sovereign mapping

**`marketing:brand-review`** for `/brand workshop`, brand gate in `/review`, and brand pass in `/polish`. Rubric: `content/sovereign/reference/brand-voice/style_rules.md` where present. See **BRAND DISCOVERY & VOICE** and **WORKFLOW & QUALITY** in `.ai/skills/skill_integration/skill.md`.

## Protocol

1. Score compliance; brand gate threshold **≥ 92%** when used as gate input.
2. Return actionable edits (voice, clarity, CTA) not only a number.
3. Chain failures to `/refine brand voice` or human review—do not auto-rewrite approved legal/compliance copy without scope.
