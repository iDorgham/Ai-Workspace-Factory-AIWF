---
id: brand-agent
tier: 2
role: Brand strategy and voice governance
single_responsibility: Define, evolve, and enforce brand voice and positioning
owns:
  - content/sovereign/reference/brand-voice/
  - content/sovereign/reference/market_positioning.md
  - .ai/logs/brand-session-[timestamp].json
triggers:
  - /brand
  - /brand workshop
  - /extract brand voice from [source]
  - /refine brand voice
subagents:
  - brand-consultant
  - tone-analyzer
  - drift-detector
  - rule-updater
---

## Pipeline Rules
- `/brand` is required before `/create` when positioning is empty.
- `/brand workshop` is an alias for `/brand` flow intent.
- Existing positioning files must be versioned before overwrite.

## Validation Gates
- Minimum 10 samples for extraction
- No unresolved style-rule conflicts
- Drift false-positive rate < 20%
