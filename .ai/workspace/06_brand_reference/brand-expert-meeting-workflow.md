# Brand Expert Meeting Workflow
# ===========================================
# Purpose: Run `/brand` as a structured strategy meeting
# Mode: User + branding expert interview (question-led)

## Outcome

After one session, the workspace should have:

- `content/sovereign/reference/market_positioning.md`
- `content/sovereign/reference/brand-voice/style_rules.md`
- `content/sovereign/reference/brand-voice/glossary.md`
- `content/sovereign/reference/brand-voice/tone_examples.md`
- `content/sovereign/reference/brand-voice/voice_refinement.md`
- `logs/brand-session-[timestamp].json`

## Meeting Stages

1. **Foundation**
   - Define service, market, stage, one-liner
2. **Audience**
   - Define ideal client, motivations, objections, value signals
3. **Personality**
   - Set archetype and spectrum (formality, tone, expressiveness)
4. **Positioning**
   - Clarify differentiators and anti-positioning
5. **Voice**
   - Define vocabulary, prohibited language, CTA style
6. **Content Strategy**
   - Define topics, channels, keyword direction
7. **Reference Alignment**
   - Capture inspirations and anti-inspirations

## Interview Rules

- Ask one question at a time.
- Prioritize required questions first.
- If answer is ambiguous, ask one focused follow-up.
- Preserve exact user wording for strategic statements.
- Convert abstractions into operational rules when synthesizing.

## Quality Checks Before Write

- No contradictions between positioning and voice.
- Tone rules are testable by `/review` brand gate.
- Glossary has both preferred and prohibited language.
- CTA style is explicit and reusable.
- Outputs are specific enough for `/create` without extra clarification.

## Command Aliases

- `/brand` and `/brand workshop` are equivalent entry points.

