# Factory Library Organization

This library follows an artifact-first taxonomy.

## Canonical Top-Level Folders

- `agents`
- `subagents`
- `skills`
- `commands`
- `subcommands`
- `templates`
- `scripts`
- `rules`
- `design`

## Supporting Folders

- `registry`
- `profiles`
- `planning`
- `mirror`
- `reports`

## Core orchestration mirror (`.ai` outbound)

Industrial mirror sync writes **agents** and **governance** copies here (see `factory/scripts/core/industrial_mirror_sync.py`):

- `core_orchestration/registry/agents/` — mirrored from `.ai/agents/`
- `core_orchestration/omega_singularity/governance/` — mirrored from `.ai/governance/`

Parallel copies also land under `agents/workspace_imports/ai/agents/` and `archive/legacy_pillars/00_core_orchestration/registry/agents/` for imports and historical pillars.

## Legacy Content

Historical domain pillars live under read-only archive paths (do not treat as canonical sources of truth for new work):

- `archive/legacy_pillars/`

See `archive/legacy_pillars/MIGRATION_MANIFEST.json` for the recorded move map.
