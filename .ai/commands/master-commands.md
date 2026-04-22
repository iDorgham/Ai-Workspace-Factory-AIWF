# Master Guide Commands

The Master Guide orchestrates the root AI Workspace Factory namespace.

## `/master sync all`
- **Trigger**: Run via CLI `python3 .ai/scripts/master_sync.py`
- **Action**: Sweeps all 3-Tier isolated Sovereign workspaces, compresses their `.ai/memory/state.json` via delta protocols, and aggregates the data into `.ai/memory/workspace-index.json`. Updates the Root Dashboard index widgets implicitly.

## `/master delegate [client/project] [task]`
- **Trigger**: Native prompt execution.
- **Action**: The Master Guide parses the task, queries `workspace-index.json` to find the correct project folder, and writes a delegatory prompt into that specific workspace's `plan.md` to trigger its local `guide-agent`.

## `/master suggest [scope]`
- **Trigger**: Native prompt execution or CLI parameter.
- **Action**: Reads `.ai/memory/user-skill-profile.json` and evaluates past successful pipelines to recommend proactive Brainstorm opportunities for stalled workspaces.
