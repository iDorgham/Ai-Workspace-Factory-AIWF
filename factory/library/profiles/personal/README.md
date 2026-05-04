# Personal workspace profiles (`factory/library/profiles/personal/`)

Planning **bundles** for workspaces materialized from the six **Industrial OS** templates (`factory/shards/…`) plus **`shadcn_saas_v21`**.

**Canonical definitions** for agents, subagents, skills, commands, rules, templates, and library scripts live under **`factory/library/`** — see **[`../../canonical_source.md`](../../canonical_source.md)**. Each profile’s `workspace_bundle.manifest.yaml` lists **which** `factory/library/...` paths that workspace should ship or sync; the profile folder itself is mostly **operator + allowlist** docs, not a second library.

Each folder under `personal/<TEMPLATE>/` holds:

| Artifact | Purpose |
|----------|---------|
| `workspace_bundle.manifest.yaml` | **Allowlist** — agent roles, `.ai/skills/<id>/` folder names, slash commands, and a **`library:`** block listing **required `factory/library/...` sources** (agents registry, subagents registry + ids, commands + registry, subcommand `.md`, rules `.mdc`, design templates, scripts). |
| `agents/planned_agents.md` | Human-readable rationale and routing table for **T0/T1** roles (names align with repo `AGENTS.md`). |
| `skills/planned_skills.md` | Minimum **first-party + official** skills for that product shape (paths are skill **folder ids**, not files). |
| `commands/planned_commands.md` | Minimum **commands.md** / router rows the workspace should expose. |

### `library:` block (inside `workspace_bundle.manifest.yaml`)

| Key | Maps to workspace / sync target |
|-----|----------------------------------|
| `canonical_source` | Always **`factory/library`** — reminder that **agents, subagents, skills, commands, rules, templates, scripts** are authored under `factory/library/` (see [canonical_source.md](../../canonical_source.md)); `.ai/` is downstream after sync. |
| `agents_registry_yaml` | `factory/library/agents/workspace_imports/ai/agents/registry/registry.yaml` → shard `.ai/agents/...` when mirrored. |
| `subagents_registry_json` | `factory/library/subagents/registry.json` (subset: `subagent_ids`). |
| `subagent_ids` | JSON `id` values present in that registry; copy only matching `.ai/subagents/<id>.json` definitions when trimming. |
| `commands_merged_md` / `commands_registry_yaml` / `commands_support_md` | Canonical merged router + per-command markdown under `factory/library/commands/`. |
| `command_templates_dir` | `factory/library/commands/templates/` (blog, landing, …). |
| `subcommands_md` | `factory/library/subcommands/` and `subcommands/ide-commands/` docs used by slash routing. |
| `rules_workspace_mirror_mdc` | `factory/library/rules/workspace_imports/ai/rules/*.mdc` → `.cursor/rules` / `.ai` mirror per your sync script. |
| `templates_design_*` | Design pack catalog + selected `factory/library/templates/design/<pack>/design.md`. |
| `templates_core_dir` | `factory/library/templates/core/` (e.g. `industrial_templates.yaml`). |
| `scripts_workspace_imports` | `factory/library/scripts/...` automation used by that profile (plus `scripts/core/` where noted). |
| `skill_mirror_base` | `factory/library/skills/` — each `skills:` entry is `<skill_mirror_base>/<id>/`. |
| `additional_skill_paths` / `profile_operator_docs` | Optional explicit paths (e.g. `github_imports/...`, profile-local `agents/*.md`). |

**Not executed automatically:** AIWF does not yet strip `.ai/` from shards using these manifests; use them as the **contract** when pruning a materialized tree or building a custom sync script. Operator L3 notes stay in each template `README.md`.

**Reference layout:** `shadcn_saas_v21/` — deeper example with extra `plan/`, `vault/`, `logs/`.

**Traceability:** `2026-05-04` — workspace bundle manifests (OMEGA + shadcn v21). `2026-05-04` — `library:` factory paths for agents, subagents, commands, subcommands, rules, templates, scripts.
