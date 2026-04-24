---
id: scraper-agent
tier: 2
role: Ethical delta scraping pipeline
single_responsibility: Detect and scrape only changed content safely
owns:
  - content/sovereign/scraped/*/scraped/
  - content/sovereign/scraped/*/sync-status.json
  - .ai/logs/sync-delta.jsonl
  - .ai/logs/scrape-audit.jsonl
triggers:
  - /scrape *
  - /sync
subagents:
  - delta-detector
  - ethical-crawler
  - content-parser
  - asset-handler
  - sync-state-writer
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
