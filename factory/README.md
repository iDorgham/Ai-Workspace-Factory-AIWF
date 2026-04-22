# Workspace Factory

The **Workspace Factory** is a **composition system**: it builds new client workspaces by **copying curated components** from a versioned **component library**, not by regenerating files from prompts on every run.

## Non-negotiables

1. **No `projects/` folder for factory outputs.** All generated client workspaces live under repository-root `workspaces/<workspace_slug>/`.
2. **Library-first.** Prefer reuse from `factory/library/`. Create new library items only when a capability does not exist yet.
3. **Manual library curation.** Components from the legacy **GALERIA** and **Sovereign** workspaces are **copied by humans** (or your own one-off scripts) into `factory/library/`. There is **no built-in sync** from those repos.
4. **Profile-driven.** `factory/profiles/*.json` declare which agents, sub-agents, skills, commands, sub-commands, templates, and scripts a workspace needs.
5. **Observable runs.** Every compose writes a manifest under `factory/manifests/` and reports under `factory/reports/`.
6. **Self-improvement loop (evolution).** Generated workspaces can emit signals under `workspaces/<slug>/.factory/signals/`; `factory/scripts/collect_evolution_signals.py` aggregates them for curator review (`factory/evolution/`).

## Repository layout

| Path                                                | Role                                                                                           |
| --------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| `factory/library/`                                  | Canonical copies of reusable components (by type).                                             |
| `factory/library/subcommands/<field>/`              | Sub-commands grouped by field (IDE specs under `engineering/cursor/` and `engineering/antigravity/`). |
| `factory/library-index/`                            | Generated indexes for search and validation.                                                   |
| `factory/sources/`                                  | **Reference paths** for where components live in Sovereign/GALERIA (`README.md` + `*.source.json`). |
| `factory/profiles/`                                 | Composition profiles (required + optional modules).                                            |
| `factory/schema/`                                   | JSON Schemas for library items, profiles, intake, manifests.                                   |
| `factory/intake/`                                   | Client/workspace intake answers.                                                               |
| `factory/manifests/`                                | Exact component lists used for a generation.                                                   |
| `factory/reports/`                                  | Composition and validation reports.                                                            |
| `factory/registry/factory-config.json`              | Workspace root name, evolution toggles.                                                        |
| `factory/scripts/`                                  | Index, validate, compose, evolution helpers.                                                   |
| `factory/evolution/`                                | Backlog and aggregated signals for library updates.                                            |
| `workspaces/`                                       | **Output** client workspaces (factory-generated).                                              |

## Operator commands

- **After manual copies into `factory/library/`:** `./factory/scripts/refresh-library.sh` (rebuild indexes + validate metadata).
- **Normalize layout (optional, after bulk imports):** `python3 factory/scripts/organize_library.py` then `./factory/scripts/refresh-library.sh` (see `factory/library/_taxonomy.json`). Field-based tree migration: `python3 factory/scripts/migrate_library_to_fields.py`.
- Or: `./factory/scripts/rebuild-library-index.sh` then `./factory/scripts/validate-library.sh`
- **Interactive create:** `./factory/scripts/create-workspace.sh`
- Or: `python3 factory/scripts/compose.py <slug> --profile <name>` then `python3 factory/scripts/validate.py <slug>`
- **Evolution:** `python3 factory/scripts/collect_evolution_signals.py`

**Where to copy from:** see `factory/sources/README.md`.

See **Playbook** under `docs/workspace/playbook/` for full operational detail.