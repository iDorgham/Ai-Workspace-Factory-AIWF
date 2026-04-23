# 🏗️ COMMAND: /swarm
**Syntax**: `/swarm "<command>" [--group=name]`
**Agent**: T0 Swarm Router
**Objective**: Parallel command execution across multiple workspaces.

---

## 🛠️ Execution Flow

1. **Target Selection**: Filter workspaces by group or select all.
2. **Task Distribution**: Dispatch the command to the `Swarm Router`.
3. **Parallel Execution**: Run tasks using multi-threaded workers (Default: 5).
4. **Result Aggregation**: Display success/failure and duration for each workspace.

---

## 📋 Examples

```bash
/swarm "/test" --group=02-Clients
/swarm "/sync --safe"
```

*Reasoning Hash: sha256:cmd-swarm-2026-04-23*
