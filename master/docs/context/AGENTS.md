## Learned User Preferences

- **Industrial Composition**: Prefer deterministic alias-to-profile mapping via `pipeline-alias-mapping.json` over manual profile selection.
- **Structural Sovereignty**: Enforce the `clients/<slug>/001_<slug>/` hierarchy to isolate project logic from client metadata.
- **Proactive Engagement**: Brainstorm suggestions should be triggered by context (Gap, Pattern, Stall) rather than requested, but must be capped at 2 per session.
- **Continual Learning**: Use incremental transcript processing against `.cursor/hooks/state/continual-learning-index.json`.
- **Taxonomy Prefs**: Prefer slash commands organized as parent/subcommand (e.g., `/scrape ...`, `/memory ...`) over dashed variants.

## Learned Workspace Facts

### Industrial Orchestration (v5.0.0)
- **[2026-04-22]** **Master Guide Agent**: Operates at root `.ai/`. Aggregates cross-project memory into `workspace-index.json` via `/master sync`.
- **[2026-04-22]** **Brainstorm Agent**: Proactive service monitoring 6 triggers to generate suggestions in `.ai/dashboard/brainstorm-suggestions.md`.
- **[2026-04-22]** **Deterministic Routing**: Managed by `pipeline-alias-mapping.json`, resolving 30 pipeline aliases to 29 industrial profiles.
- **[2026-04-22]** **Lazy-Load Dashboards**: Rendered by `render_dashboard.py` using a `widget-registry.json` for token efficiency.
- **[2026-04-22]** **Structural Validation**: Compliance with the sovereign hierarchy (FR-2.1) is enforced by `audit_path_integrity.py`.
- **[2026-04-22]** **Smoke Testing**: Verified by `run-smoke-tests.py` (Baseline: 5/5 PASS).

### Sovereign Workspace Architecture
- **Autonomy Protocol**: All projects are deployed as isolated entities to `workspaces/clients/<client>/00X_<project>/`. Each has its own localized agents, skills, and memory.
- **Metadata Isolation**: Client folders must remain 100% code-free (Metadata only).
- **Command Mirroring**: Commands MUST be mirrored to `.cursor/rules/` to appear in the Cursor slash (/) menu.
- **Multi-Tool Routing**: Executable routing defined in `command-routing.json`; active Python router is `tool_router_v2.py`.
- **Path Integrity Summary**: `audit_path_integrity.py` regenerates `.ai/logs/path-integrity-summary.md` to avoid stale-summary failures in integrity audits.
