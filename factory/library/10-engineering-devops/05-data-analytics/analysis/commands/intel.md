---
description: Generate competitive intelligence and trend reports.
cluster: analysis
category: commands
display_category: Commands
id: commands:analysis/commands/intel
version: 10.0.0
domains: [research-analytics]
sector_compliance: pending
---
# /intel

Invokes the `@IntelSynthesizer` to scan the environment and provide a summary of market conditions or competitor moves.

## Usage
`/intel <target_entity_or_topic> [--depth deep|surface]`

## Tasks
1. Execute `ethical-crawler` for public data.
2. Run `comparison-analyst` to map product parity.
3. Synthesize social sentiment using `sentiment-processor`.
4. Output a `market-intelligence-report.md`.

## Constraints
- Must cite data sources where applicable.
- Must focus on actionable insights (the "So What?") rather than raw data dumps.
