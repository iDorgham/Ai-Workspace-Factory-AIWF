---
description: Run a competitive benchmark analysis across key market dimensions.
cluster: analysis
category: commands
display_category: Commands
id: commands:analysis/commands/benchmark
version: 10.0.0
domains: [research-analytics]
sector_compliance: pending
---
# /benchmark

Invokes the `@ResearchAnalyst` to compare a product or brand against 3–5 competitors across defined KPIs.

## Usage
`/benchmark <product_name> [--competitors "A,B,C"] [--dimensions ux|pricing|features]`

## Tasks
1. Identify the top 3–5 competitors for the given product or vertical.
2. Score each competitor across UX, pricing, feature depth, and market reach.
3. Generate a comparison matrix with gap analysis.
4. Output `benchmark-report.md` and `competitor-matrix.csv`.

## Constraints
- All competitor data must be sourced from public information.
- Scoring rubric must be documented before results are presented.
