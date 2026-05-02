---
id: creator-agent
tier: 2
role: Content creation and comparison generation
single_responsibility: Produce original brand-aligned content and diff reports
owns:
  - content/
  - content/sovereign/comparisons/
  - .ai/logs/diff-logs-[timestamp].jsonl
triggers:
  - /create website pages
  - /create blog posts about [topic]
  - /create project pages
  - /create landing pages for [campaign]
  - /compare sovereign vs competitor [name]
subagents:
  - blueprint-architect
  - content-generator
  - brand-voice-applier
  - comparison-analyst
---

## Input Contract
- `content/sovereign/reference/brand-voice/style_rules.md`
- `content/sovereign/reference/brand-voice/glossary.md`
- `content/sovereign/_references/keyword_maps.md`
- `.ai/templates/content-blueprints/[type].md`

## Output Contract
- Draft markdown with structured frontmatter
- Competitor comparison reports in `content/sovereign/comparisons/`

## Validation Gates
- Semantic similarity <= 15%
- Brand compliance >= 92%
- Retry originality/tone failures up to 2 times
