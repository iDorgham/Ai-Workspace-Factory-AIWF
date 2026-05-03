# Factory Library Organization

This directory is the **global component library** for AIWF: agents, skills, templates, design packs, registries, and mirrored planning artifacts. Workspaces consume from here; they do not fork the library as a competing source of truth.

**See also:** [docs/CONTEXT.md](../../docs/CONTEXT.md) (orientation), [docs/PRD.md](../../docs/PRD.md) §3.3 and §4.8 (full protocol).

---

## Canonical top-level folders

| Folder | Role |
|--------|------|
| `agents/` | Shared agent definitions and mirrors |
| `subagents/` | Claude/Codex pack registries (kebab-case upstream filenames) |
| `skills/` | Sovereign skills plus **vendored** trees (`skills/github_imports/`, `skills/nexu_open_design/`) |
| `commands/` | Command mirrors |
| `subcommands/` | Subcommand docs |
| `templates/` | Industrial blueprints; includes `templates/design/` and `templates/subagents/` mirrors |
| `design/` | Provider UI/design packs (`<provider>/design.md`) — aligned with `.ai/templates/design/` |
| `scripts/` | Library-scoped automation (`scripts/maintenance/external_library_sync.py`, import helpers, …) |
| `rules/` | Rules mirrors |

---

## Supporting folders

| Folder | Role |
|--------|------|
| `registry/` | `external_sources.registry.json`, `skills.registry.json`, and related aggregate JSON |
| `profiles/` | Workspace profile JSON (also see `factory/profiles/`) |
| `planning/` | Mirror of `.ai/plan/` (`planning_mirror_sync.py` target); includes `sync_manifest.json` |
| `mirror/` | Mirror/auxiliary payloads per outbound mirror protocol |
| `reports/` | `external_library_merge_report.json` / `.md` and similar merge or audit outputs |
| `reference/` | Curated reference snapshots (e.g. awesome-list mirrors) |

---

## External design sync (operator checklist)

1. Edit **`registry/external_sources.registry.json`** when adding or changing upstream Git sources.
2. Run **`python3 factory/library/scripts/maintenance/external_library_sync.py`** from the repo root.
3. Review **`reports/external_library_merge_report.md`** for conflicts and tier decisions.
4. Run **`python3 factory/scripts/core/industrial_mirror_sync.py`** when `.ai/` ↔ `factory/library/` drift must be reconciled (see AGENTS.md).
5. Optionally rebuild registries: **`python3 factory/scripts/analytics/rebuild_canonical_registries.py`**.

Pre-commit **snake_case** rules skip vendored prefixes under `skills/github_imports/` and **`skills/nexu_open_design/`**; first-party paths remain strict.

---

## Core orchestration mirror (`.ai` outbound)

Industrial mirror sync writes **agents** and **governance** copies here (see `factory/scripts/core/industrial_mirror_sync.py`):

- `core_orchestration/registry/agents/` — mirrored from `.ai/agents/`
- `core_orchestration/omega_singularity/governance/` — mirrored from `.ai/governance/`

Parallel copies also land under `agents/workspace_imports/ai/agents/` and `archive/legacy_pillars/00_core_orchestration/registry/agents/` for imports and historical pillars.

---

## Legacy content

Historical domain pillars live under read-only archive paths (do not treat as canonical sources of truth for new work):

- `archive/legacy_pillars/`

See `archive/legacy_pillars/MIGRATION_MANIFEST.json` for the recorded move map.
