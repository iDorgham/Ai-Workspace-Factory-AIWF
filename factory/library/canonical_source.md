# Canonical source: `factory/library/`

Treat **`factory/library/`** as the **editorial and structural source of truth** for:

| Domain | Primary path under `factory/library/` |
|--------|--------------------------------------|
| **Agents** | `agents/` (including `agents/workspace_imports/ai/agents/…`) |
| **Subagents** | `subagents/` (`registry.json`, packs under `templates/subagents/` as applicable) |
| **Skills** | `skills/` (first-party folders + `skills/github_imports/`, `skills/nexu_open_design/`, etc.) |
| **Commands** | `commands/` (`commands.md`, `registry.yaml`, per-command `*.md`, `commands/templates/`) |
| **Subcommands** | `subcommands/` (including `subcommands/ide-commands/`) |
| **Rules** | `rules/` (e.g. `rules/workspace_imports/ai/rules/*.mdc` for IDE mirrors) |
| **Templates** | `templates/` (`templates/core/`, `templates/design/<provider>/design.md`, …) |
| **Design packs** | `design/` (parallel catalog; see also `templates/design/`) |
| **Scripts** | `scripts/` (library automation; repo-wide gates may live under `factory/scripts/core/`) |
| **Registries & planning mirrors** | `registry/`, `planning/` |

**Workspace `.ai/`** and **`.cursor/commands/`** are **downstream mirrors** after sync — edit commands/agents/skills in **`factory/library/`** (or the documented canonical `.ai/` path when the protocol says “canonical in `.ai`” for a given file), then run the sync steps in **`AGENTS.md`** so outbound mirrors stay coherent.

**See:** [README.md](README.md) for the full folder map.

**Traceability:** `2026-05-04` — explicit canonical-source map for agents, subagents, skills, commands, rules, templates, scripts.
