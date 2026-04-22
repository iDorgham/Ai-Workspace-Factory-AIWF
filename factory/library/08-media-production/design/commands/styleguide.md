---
description: Generate a living style guide document from existing design tokens.
cluster: design
category: commands
display_category: Commands
id: commands:design/commands/styleguide
version: 10.0.0
domains: [design-media]
sector_compliance: pending
---
# /styleguide

Invokes the `@DesignDirector` to produce a comprehensive, developer-ready style guide covering color, type, spacing, and component patterns.

## Usage
`/styleguide <project_name> [--format md|html] [--scope full|tokens-only]`

## Tasks
1. Scan design-token files for color, typography, and spacing definitions.
2. Document each token with usage examples and do/don't guidelines.
3. Generate a component pattern inventory with visual hierarchy rules.
4. Output `style-guide.md` with linked token references.

## Constraints
- Must include WCAG 2.2 AA contrast ratios for all color pairs.
- Token names must follow the project's existing naming convention.
