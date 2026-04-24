---
description: Curate a design moodboard from brand guidelines and reference assets.
cluster: design
category: commands
display_category: Commands
id: commands:design/commands/moodboard
version: 10.0.0
domains: [design-media]
sector_compliance: pending
---
# /moodboard

Invokes the `@DesignDirector` to assemble a structured visual moodboard with color palettes, typography, and layout references.

## Usage
`/moodboard <project_name> [--style minimal|editorial|brutalist]`

## Tasks
1. Extract brand tokens from the project's design system.
2. Curate 5–8 reference images aligned with the target aesthetic.
3. Map typography pairings and spacing scales.
4. Output a `moodboard.md` with embedded asset references.

## Constraints
- All colors must reference semantic design tokens, not raw hex.
- Image references must be from licensed or generated assets.
