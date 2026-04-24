---
cluster: engineering-core
category: subcommands
display_category: Subcommands
id: commands:engineering-core/subcommands/docs
version: 10.0.0
domains: [engineering-core]
sector_compliance: pending
---
# Docs

Update documentation when behavior or setup changes.

## Instructions

1. Update `docs/` for: new APIs, schema, env vars, workflows.
2. Key files: `CLAUDE.md`, `docs/plan/`, `docs/APP_DESIGN_DOCS.md`.
3. Keep README and PRD in sync.

## When to update

- New API route → document in APP_DESIGN_DOCS or API docs
- Schema change → update CLAUDE.md, migration notes
- New command → update DEVELOPMENT_WORKFLOWS.md
