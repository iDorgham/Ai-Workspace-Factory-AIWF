# Sovereign Workspace — Versioning Policy v13.0.0

## Canonical Rule
This file is the single source of truth for workspace versioning behavior.
If other docs conflict, this policy wins.

## 🛰️ Silent Git Protocol (`/git auto`)
1. **Autonomous Mutation**: When active, all structural and code changes are automatically committed to the current branch.
2. **Commit Pattern**: `feat({workspace}): {description} [Reasoning: {hash}]`
3. **Traceability**: Every mutation must include an ISO-8601 timestamp and a reasoning hash linked to the session memory.
4. **Immutable Tagging**: Phase completion triggers a workspace-specific tag (e.g., `v13.1.0-sovereign-web`).

## 📁 File Classes
- **Governance**: Replace in place with explicit changelog notes.
- **Logs**: Append-only JSONL/JSON artifacts with timestamps.
- **Generated Content**: Section-based assembly with versioned full-page aggregates.
- **Analysis Exports**: Version by timestamp or explicit incremental suffix.

## ⚙️ Allowed Modes
- **Silent Automation**: Default for `/git auto`. Full autonomy for version control.
- **Manual Handover**: Triggered via `/git release`. Finalizes version and creates immutable tag.
- **In-place Optimization**: Overwrite allowed only when a backup is created in `.ai/memory/backups/`.

## 🚫 Prohibited Patterns
- Overwriting non-overwritable files defined by ownership contracts.
- Committing without a reasoning hash when `/git auto` is active.
- Manual tagging that conflicts with factory versioning schema.
