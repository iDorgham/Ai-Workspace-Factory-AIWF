---
cluster: engineering-core
category: subcommands
display_category: Subcommands
id: commands:engineering-core/subcommands/github
version: 10.0.0
domains: [engineering-core]
sector_compliance: pending
---
# Github

**Perfect Versioning Workflow** — Zero-manual-config git lifecycle for plan phases.

## Automated lifecycle
The Git lifecycle is managed by `scripts/ralph-git.js`.

### 1. Branching
`node scripts/ralph-git.js branch <slug> <N>`

### 2. Committing
`node scripts/ralph-git.js commit <slug> <N>`

### 3. Merging
`node scripts/ralph-git.js merge <slug> <N>`

## Convention
- **Branch**: `feat/<slug>-phase-<N>`
- **Commit**: `feat(<slug>): Phase <N> - <Description> (Phase <N>)`
- **Logic**: Always rebase main before branching, always merge --no-ff back to main.
