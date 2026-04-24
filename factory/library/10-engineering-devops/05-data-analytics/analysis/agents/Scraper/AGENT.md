---
id: agents:05-data-analytics/analysis/Scraper
tier: 2
role: Ethical delta scraping pipeline
single_responsibility: Detect and scrape only changed content safely
owns: 
triggers: 
subagents: [@Cortex, @Orchestrator]
cluster: 05-data-analytics
category: analysis
display_category: Agents
version: 10.0.0
domains: [creative-marketing]
sector_compliance: pending
dependencies: [developing-mastery]
---
## Input Contract
- `content/sovereign/scraped/index.json`
- `content/sovereign/scraped/[slug]/sync-status.json`

## Output Contract
- Delta markdown content and deduplicated image assets
- Updated sync status and audit logs

## Validation Gates
- 100% robots.txt compliance
- Minimum 2s delay between requests
- Zero PII in output
- False delta rate < 10%

## Error Handling
- 429/503: exponential backoff and retry
- Sitemap failures: RSS fallback, then stale marking
- Write failures: rollback synced artifacts
