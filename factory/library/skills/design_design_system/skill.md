```json
{
  "skill_id": "design-design-system",
  "name": "Design system alignment",
  "version": "1.0.0",
  "description": "Align copy and references with the workspace visual design system and tokens.",
  "cowork_skill": "design:design-system",
  "integration_ref": ".ai/skills/skill_integration/skill.md",
  "agents": ["brand-agent"],
  "timestamp": "2026-05-02T00:00:00Z"
}
```

# Design system alignment

## Sovereign mapping

**`design:design-system`** — ensure content references match Sovereign visual system. See **DESIGN ALIGNMENT** in `.ai/skills/skill_integration/skill.md`.

## Protocol

1. Resolve active tokens/components from project design sources (design packs under `factory/library/design/` when applicable).
2. Flag copy or markup that contradicts documented spacing, type scale, or color roles.
3. Prefer additive fixes; do not override locked brand artifacts without explicit approval.
