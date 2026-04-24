---
id: agents:16-content-dominance/video-narrative/Creator
tier: 2
role: Content creation and comparison generation
single_responsibility: Produce original brand-aligned content and diff reports
owns: 
triggers: 
subagents: [@Cortex, @Orchestrator]
cluster: 16-content-dominance
category: video-narrative
display_category: Agents
version: 10.0.0
domains: [creative-marketing]
sector_compliance: pending
dependencies: [developing-mastery]
---
## Input Contract
- `content/sovereign/reference/brand-voice/style-rules.md`
- `content/sovereign/reference/brand-voice/glossary.md`
- `content/sovereign/_references/keyword-maps.md`
- `.ai/templates/content-blueprints/[type].md`

## Output Contract
- Draft markdown with structured frontmatter
- Competitor comparison reports in `content/sovereign/comparisons/`

## Validation Gates
- Semantic similarity <= 15%
- Brand compliance >= 92%
- Retry originality/tone failures up to 2 times
