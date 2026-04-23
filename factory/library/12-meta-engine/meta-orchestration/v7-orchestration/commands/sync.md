# 🏗️ COMMAND: /sync
**Syntax**: `/sync [slug|--all] [flags]`
**Agent**: T0 Root Orchestrator
**Objective**: Propagate library updates to sovereign workspaces safely.

---

## 🛠️ Execution Flow

1. **Target Identification**: Resolve workspace slug or select all managed projects.
2. **Snapshot**: Create a snapshot branch `sync/v{version}` in the factory (for tracking) and log intent.
3. **Engine Invocation**: Trigger `factory/scripts/sync_engine.py`.
4. **File Propagation**: Copy agents, commands, and skills from library to workspace `.ai/`.
5. **Retrofitting**: Ensure mandatory folders (docs/00-06) and files (.env, .gitignore) exist.
6. **Verification**: Run `integrity_auditor` in the target workspace.

---

## 📋 Examples

```bash
/sync my-project --safe
/sync --all --dry-run
```

*Reasoning Hash: sha256:cmd-sync-2026-04-23*
