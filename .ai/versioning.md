# Sovereign Workspace — Versioning Policy

## Canonical Rule

This file is the single source of truth for workspace versioning behavior.
If other docs conflict, this policy wins.

## File Classes

- `governance`: Replace in place with explicit changelog notes.
- `logs`: Append-only JSONL/JSON artifacts with timestamps.
- `generated_content`: Version by command and slug.
- `analysis_exports`: Version by timestamp or explicit incremental suffix.

## Naming Conventions

- **Timestamped artifacts**: `name-[timestamp].json` or `name-[timestamp].jsonl`
- **Incremental versions**: `name_v2.md`, `name_v3.md`
- **Tool-specific variants** (only when command runs in parallel or explicit compare mode):
  `name_[tool]_v2.md`

## Allowed Modes

- **Default mode**: global incremental versioning (`_vN`) without tool suffix.
- **Parallel/compare mode**: tool-suffixed versioning is allowed to preserve alternatives.
- **In-place optimization mode**: overwrite allowed only when a backup is created first.

## Backup Requirement

Before any in-place overwrite:

1. Save backup to `.ai/memory/backups/` with timestamp.
2. Apply update.
3. On failure, restore backup and log rollback.

## Prohibited Patterns

- Mixing malformed duplicated suffixes (for example: `file.mdname.md`)
- Using both global and tool versioning for the same artifact in one run without explicit merge step
- Overwriting non-overwritable files defined by ownership contracts
