---
description: Run a structured SWOT analysis for a product, market, or venture.
cluster: business
category: commands
display_category: Commands
id: commands:business/commands/swot
version: 10.0.0
domains: [business-strategy]
sector_compliance: pending
---
# /swot

Invokes the `@BusinessAnalyst` to produce a comprehensive Strengths, Weaknesses, Opportunities, and Threats matrix.

## Usage
`/swot <product_or_market> [--depth brief|deep]`

## Tasks
1. Gather internal asset data and competitive positioning.
2. Map external opportunities from market-size-calculator output.
3. Identify threats using regulatory and competitor intelligence.
4. Output a `swot-matrix.md` with scored quadrants.

## Constraints
- All threat scores must cite a verifiable data source.
- Must align with brand positioning defined by `@BrandStrategist`.
