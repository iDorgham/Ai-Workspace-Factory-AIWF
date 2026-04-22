# Legacy workspace paths (manual copy only)

The factory **does not run sync** from Sovereign or GALERIA. You **copy** (or merge by hand) components into `factory/library/` and then run `./factory/scripts/refresh-library.sh`.

Use the JSON files here as a **cheat sheet** for where components live in each legacy repo (paths are relative to that repo’s root).

| Component type | Copy into `factory/library/…` | GALERIA (typical) | Sovereign (typical) |
|----------------|-------------------------------|-------------------|----------------|
| Agents | `agents/` | `.ai/agents/` | `.ai/agents/` |
| Sub-agents | `subagents/` | `.ai/subagents/` | `.ai/subagents/` (if present) |
| Skills | `skills/<name>/` | `.ai/skills/<name>/` | `.ai/skills/<name>/` |
| Commands | `commands/` | `.ai/commands/` (if present) | `.ai/commands/` |
| Sub-commands | `subcommands/engineering/cursor/`, `subcommands/engineering/antigravity/` | `.cursor/commands/`, `.antigravity/commands/` | same paths if present |
| Templates | `templates/` | `.ai/templates/` | `.ai/templates/` |
| Scripts | `scripts/` (preserve subdirs) | `.ai/scripts/` | repo `scripts/` (Sovereign) |

## Metadata

Each copied file should have a sibling `*.meta.json` satisfying `factory/schema/library-item.schema.json` (see existing library items for examples). Set `source` to `sovereign`, `sovereign`, or `local`, and `last_synced_at` to an ISO timestamp (field name kept for schema compatibility; treat it as **last updated**).

## Reference JSON

- `sovereign.source.json` — Sovereign-relative paths for documentation.
- `sovereign.source.json` — GALERIA-relative paths for documentation.
