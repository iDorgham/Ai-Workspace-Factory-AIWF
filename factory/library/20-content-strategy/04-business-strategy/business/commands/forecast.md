---
description: Generate a 12-month financial forecast with scenario modeling.
cluster: business
category: commands
display_category: Commands
id: commands:business/commands/forecast
version: 10.0.0
domains: [business-strategy]
sector_compliance: pending
---
# /forecast

Invokes the `@Forecasting` agent to build revenue, expense, and cash-flow projections across best, base, and worst scenarios.

## Usage
`/forecast <business_unit> [--horizon 6|12|24] [--scenarios base|multi]`

## Tasks
1. Pull historical revenue and expense data from workspace context.
2. Model three scenarios: optimistic, base, and conservative.
3. Generate a month-by-month P&L projection table.
4. Output `forecast-report.md` and `scenario-comparison.csv`.

## Constraints
- Assumptions must be explicitly documented per scenario.
- Growth rates exceeding 30% MoM must include justification.
