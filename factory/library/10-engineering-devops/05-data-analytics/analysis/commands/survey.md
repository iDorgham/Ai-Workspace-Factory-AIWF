---
description: Design and analyze a user research survey with statistical rigor.
cluster: analysis
category: commands
display_category: Commands
id: commands:analysis/commands/survey
version: 10.0.0
domains: [research-analytics]
sector_compliance: pending
---
# /survey

Invokes the `@ResearchAnalyst` to create survey instruments, define sampling methodology, and produce an analysis framework.

## Usage
`/survey <research_question> [--method quant|qual|mixed] [--sample-size N]`

## Tasks
1. Draft survey questions with proper scale types (Likert, NPS, open-ended).
2. Define target population and minimum sample size for significance.
3. Create an analysis plan with statistical tests and visualization specs.
4. Output `survey-instrument.md` and `analysis-plan.md`.

## Constraints
- Questions must avoid leading or double-barreled phrasing.
- Sample size calculation must target ≥95% confidence level.
