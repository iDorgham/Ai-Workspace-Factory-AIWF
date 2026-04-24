---
cluster: engineering-core
category: subcommands
display_category: Subcommands
id: commands:engineering-core/subcommands/README
version: 10.0.0
domains: [engineering-core]
sector_compliance: pending
---
# IDE Workspace Commands

These files power IDE chat slash suggestions and command routing.

- Location: workspace command definitions directory
- Source of truth: `.ai/cli-layer/command-routing.json`
- Naming: file name = slash command ID in kebab-case

When routing schema changes or new IDE commands are added, update matching command files here.

## Command IDs

- `brand`
- `research`
- `scrape`
- `sync`
- `voice`
- `create`
- `compare`
- `intel`
- `polish`
- `optimize`
- `review`
- `approve`
- `revise`
- `export`
- `archive`
- `memory`
- `budget`

## Grouping Rules

- Use `<group>-<target>-<scope>-<action>` for multi-part commands.
- Use `<group>-<action>` for compact commands.
- Keep families lexically aligned by prefix (`scrape-*`, `create-*`, `intel-*`, `memory-*`, `brand-*`).
- Parent commands (`scrape`, `create`, `intel`, `memory`, `brand`, `voice`) use menu-style subcommand selection inside one file.
