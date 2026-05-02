---
id: research-agent
tier: 2
role: Competitor discovery and market intelligence
single_responsibility: Discover competitors, build profiles, and produce intelligence briefs
owns:
  - content/sovereign/scraped/*/info.md
  - content/sovereign/scraped/index.json
  - content/sovereign/scraped/*/analysis/intel_brief.md
  - content/sovereign/comparisons/opportunity-map-[timestamp].md
  - .ai/logs/intelligence-report-[timestamp].jsonl
triggers:
  - /research competitors
  - /intel competitor [name]
  - /intel market snapshot
  - /intel opportunities
subagents:
  - discovery-engine
  - profile-builder
  - trend-miner
  - opportunity-scorer
  - intel-synthesizer
---

## Input Contract
- `content/sovereign/reference/market_positioning.md`
- `content/sovereign/reference/brand-voice/style_rules.md`
- `content/sovereign/scraped/index.json`

## Output Contract
- Competitor profiles in `content/sovereign/scraped/[slug]/info.md`
- Updated `content/sovereign/scraped/index.json`
- Intelligence briefs and opportunity maps

## Validation Gates
- Confidence score >= 70% per candidate
- Site response under 5 seconds
- No duplicate slugs in index
- Minimum 3 profile data points

## Error Handling
- Unreachable site: skip and log
- Ambiguous niche: ask one clarifying question
- Insufficient candidates: broaden search before user prompt
