```json
{
  "skill_id": "marketing-brand-voice",
  "name": "Marketing brand voice",
  "version": "1.0.0",
  "description": "Tone extraction, lexical profiling, and CTA style analysis from sources for brand workflows.",
  "cowork_skill": "marketing:brand-voice",
  "integration_ref": ".ai/skills/skill_integration/skill.md",
  "commands": ["/extract brand voice from [source]", "/refine brand voice"],
  "agents": ["brand-agent", "tone-analyzer", "drift-detector", "rule-updater"],
  "timestamp": "2026-05-02T00:00:00Z"
}
```

# Marketing brand voice

## Sovereign mapping

**`marketing:brand-voice`** for `/extract brand voice from [source]` and `/refine brand voice`. See **BRAND DISCOVERY & VOICE** in `.ai/skills/skill_integration/skill.md`.

## Protocol

1. Extract patterns (tone, lexicon, rhythm, CTAs); brand-agent applies Sovereign-specific rules on top.
2. For drift: diff against existing `style_rules.md` (or equivalent) and propose rule updates, not silent overwrites.
3. Preserve user-owned nuance; flag low-evidence inferences explicitly.
