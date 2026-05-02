# Workspace template library sync — reconciliation report

**ISO-8601:** `2026-04-30T22:15:00+00:00`  
**Scope:** Six templates under `workspaces/templates/` (ASSET_OS_LAB, BRAND_OS_STRATEGY, CORE_OS_SAAS, MENA_OS_BILINGUAL, MOBILE_OS_FORGE, WEB_OS_TITAN).

## Summary

| Area | Action |
| :--- | :--- |
| Branding guide | Replaced sole reliance on `_legacy_pillars/06-branding` with **canonical** `factory/library/templates/brand_discovery`; legacy pillar noted as optional archive. |
| Subagent registry | Added **`.ai/registry/subagents.registry.json`** (copy of repo `.ai` registry) to every template. |
| Subagent contracts | Added **`.ai/agents/registry/sub_agent_contracts.json`** to every template; agent docs now cite this path explicitly. |
| Routing docs | **`multi_tool.md`** and **`data_ownership_multi_tool.md`** list registry + contracts + factory canonical mirror. |
| L3 memory | **`memory_layers.md`** L3 section clarified; **`factory/library/profiles/personal/<TEMPLATE>/README.md`** anchors created so the documented path exists. |
| Design baseline | **`.ai/templates/design/README.md`** per template (domain-tuned pointers into `factory/library/design/`). |
| Rules baseline | **`.ai/rules/README.md`** per template + **`factory/library/rules/README.md`** factory extension-point doc. |

## Files changed (pattern)

Per template `workspaces/templates/<T>/`:

- `.ai/docs/guides/saas_materialization_guide.md` (edit)
- `.ai/docs/protocols/memory_layers.md` (edit)
- `.ai/commands/multi_tool.md` (edit)
- `.ai/governance/data_ownership_multi_tool.md` (edit)
- `.ai/agents/security_auditor.md`, `neural_fabric_sync.md`, `revenue_orchestrator.md` (edit)
- `.ai/registry/subagents.registry.json` (**new**)
- `.ai/agents/registry/sub_agent_contracts.json` (**new**)
- `.ai/templates/design/README.md` (**new**)
- `.ai/rules/README.md` (**new**)

Repo factory:

- `factory/library/profiles/personal/<TEMPLATE>/README.md` — six anchors (**new**)
- `factory/library/rules/README.md` (**new**)

## Validation

- **Targeted markdown links** in all edited protocol/command/agent/design/rules files: **0 broken** (resolver treats `factory/...` from repo root and `.ai/...` from materialized template root).
- **Full-template** naive link scan still reports many broken links inside vendored `.ai/skills/**` (upstream relative links); **out of scope** for this sync — not introduced by this pass.

## Unresolved / follow-ups

- Per-subagent JSON under `.ai/subagents/*.json` referenced by `subagents.registry.json` is **not** materialized in templates (same as monorepo root). Runtime that requires split files should either generate them from `sub_agent_contracts.json` or extend the template pack in a later phase.
- Optional: enrich **BRAND_OS_STRATEGY** with a thin copy or symlink of `factory/library/templates/brand_discovery/*` into `.ai/templates/brand_discovery/` if offline materialization must not depend on factory paths.

**Reasoning hash:** `template-library-sync-2026-04-30`
