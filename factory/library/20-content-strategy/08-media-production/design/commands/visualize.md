---
description: Generate moodboards or visual scene specifications.
cluster: design
category: commands
display_category: Commands
id: commands:design/commands/visualize
version: 10.0.0
domains: [design-media]
sector_compliance: pending
---
# /visualize

This command invokes the `@DesignDirector` to transform a set of product requirements or brand positioning notes into a visual specification.

## Usage
`/visualize <source_context> [--tier luxury|saas|govtech]`

## Tasks
1. Extract emotional intent from the source context.
2. Select a color palette and typography stack from the `design-system.md` tokens.
3. Generate image prompts for the `@Creator` agent.
4. Output a `visual-spec.md` in the target project folder.

## Constraints
- Must use tokens from `packages/ui/src/lib/styles/tokens.css`.
- Must respect the "Cine-Serious" aesthetic.
