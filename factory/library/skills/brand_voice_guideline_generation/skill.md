```json
{
  "skill_id": "brand-voice-guideline-generation",
  "name": "Brand voice guideline generation",
  "version": "1.0.0",
  "description": "Synthesize interview and source signals into structured, enforceable brand voice guidelines.",
  "cowork_skill": "brand-voice:guideline-generation",
  "integration_ref": ".ai/skills/skill_integration/skill.md",
  "commands": ["/brand", "/brand workshop", "/extract brand voice"],
  "agents": ["brand-agent", "brand-consultant", "brand-synthesizer", "tone-analyzer"],
  "timestamp": "2026-05-02T00:00:00Z"
}
```

# Brand voice guideline generation

## Sovereign mapping

**`brand-voice:guideline-generation`** — post-interview synthesis for `/brand` and `/brand workshop`; optional path for `/extract brand voice from [source]`. See **BRAND DISCOVERY & VOICE** in `.ai/skills/skill_integration/skill.md`.

## Protocol

1. Run **after** `brand-consultant` interview data exists; do not replace the interview step.
2. Output structured patterns (tone, lexicon, CTAs, taboos) suitable for `style_rules.md`-style enforcement.
3. Hand off to brand-consultant for file writes; keep outputs internally consistent and enforceable.
