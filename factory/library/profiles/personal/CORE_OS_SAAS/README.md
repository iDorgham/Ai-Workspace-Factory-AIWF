# L3 personal mirror — CORE_OS_SAAS

Reserved slot for **operator-specific** preferences, vault pointers, and cross-session shards after a workspace is materialized from the `CORE_OS_SAAS` template.

- Do not commit secrets; use your workspace `.env` / vault patterns from governance docs.
- Canonical shared patterns remain in `factory/library/` (artifact-first).

## Workspace bundle (planned allowlist)

Use these when **trimming** a materialized workspace so it only ships agents, skills, and commands this template needs:

| File | Purpose |
|------|---------|
| [`workspace_bundle.manifest.yaml`](workspace_bundle.manifest.yaml) | YAML allowlist: agents, `.ai/skills/<id>/`, slash commands. |
| [`agents/planned_agents.md`](agents/planned_agents.md) | T0/T1 role rationale. |
| [`skills/planned_skills.md`](skills/planned_skills.md) | Minimum skill folder ids. |
| [`commands/planned_commands.md`](commands/planned_commands.md) | Minimum router commands. |

**Traceability:** `2026-04-30` — template library sync (memory_layers L3 anchor). `2026-05-04` — workspace bundle manifests.
