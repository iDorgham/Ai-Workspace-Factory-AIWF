---
description: Build a comprehensive pitch deck or investor presentation.
cluster: business
category: commands
display_category: Commands
id: commands:business/commands/pitch
version: 10.0.0
domains: [business-strategy]
sector_compliance: pending
---
# /pitch

Invokes the `@VentureArchitect` to structure a high-stakes presentation for founders, investors, or internal stakeholders.

## Usage
`/pitch <vision_statement> [--deck-type seed|series-a|internal]`

## Tasks
1. Synthesize the "Problem" and "Solution" slides.
2. Pull market data from `market-size-calculator`.
3. Model financial projections using `unit-economics` skill.
4. Output a `pitch-deck-outline.md` and `investor-qa.md`.

## Constraints
- Must align with the brand voice defined by `@BrandStrategist`.
- Financials must be realistic and backed by documented assumptions.
