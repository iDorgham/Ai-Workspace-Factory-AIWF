---
type: Generic
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# SOS Runtime State

> **Mutable control plane** for live execution. Safe to edit during a swarm.  
> **Read-only:** `sos/manifest.md`, `sos/prompts/*.md` — never modify from this loop.

**Path resolution:** If the active manifest lives under `.ai/plans/active/features/[feature-id]/sos/manifest.md`, keep the paired runtime file as `.../sos/runtime_state.md` next to it. This copy lives under **`.ai/templates/sos-root/`** for bootstrapping — **do not** rely on a permanent repo-root `sos/` unless you intentionally run a global swarm.

---

## Schema (`runtime_state` v1)

| Field | Type | Description |
|-------|------|-------------|
| `schema_version` | string | e.g. `1.0` |
| `feature_id` | string | Matches feature package / swarm id |
| `swarm_id` | string | e.g. `swarm-YYYYMMDD-slug` |
| `status` | enum | `idle` \| `running` \| `paused` \| `completed` \| `failed` \| `failed-critical` |
| `started_at` | ISO8601 | Wall clock string |
| `updated_at` | ISO8601 | Last loop write |
| `active_plan_step` | string | Traceability ref, e.g. `2.3` |
| `contract_refs` | string[] | Locked contract paths |
| `gate_cursor` | enum | `spec:validate` → `contract:auto-validate` → `compliance` → `security:scan` → `test` → `build` → `deploy` |
| `gate_status` | map | Each gate: `pending` \| `passed` \| `failed` |
| `tasks` | array | Per-task rows (below) |
| `last_output_hash` | string | Short hash of last completed artifact bundle |
| `last_runtime_log` | string | Path to latest `.ai/plans/active/audit/runtime-logs/*.md` |
| `drift_score_last` | number | 0–4 from previous iteration |
| `reroute_count` | number | Integer, total reassignments |
| `notes` | string | Human-readable; keep ≤20 lines |
| `trace_id_last` | string | Latest automation trace, e.g. `RT-20260411-a1b2c3` |
| `optimization_counter` | number | Increments on task completion; triggers weight pass every N |
| `optimization_every_n_tasks` | number | Default `5` — see `.ai/skills/auto_optimization_loop.md` |
| `ci_validate` | boolean | If `true`, CI workflow fails on `drift_score_last > 0` or any gate ≠ `passed` |
| `pr_gate_strict` | boolean | If `true`, same strict checks as `ci_validate` (use for release branches) |

### Per-task row (`tasks[]`)

| Column | Type | Description |
|--------|------|-------------|
| `task_id` | string | e.g. `T-001` — must exist in `sos/manifest.md` |
| `tier` | number | From manifest schedule |
| `assigned_agent` | string | `@Agent` handle |
| `status` | enum | `pending` \| `ready` \| `in_progress` \| `completed` \| `blocked` \| `failed` |
| `blocked_by` | string[] | Task ids; mirror manifest (read-only source) |
| `blocked_by_gates` | string[] | Optional gate keys blocking this task; **auto-cleared** when gate passes (see `.ai/skills/runtime_automation_rules.md`) |
| `last_checkpoint` | ISO8601 | When row last updated |
| `output_hash` | string | Optional; artifact fingerprint |
| `compliance_signals` | string[] | Short tags, e.g. `token_violation`, `tests_green` |

---

## Update Rules

1. **Init (first run):** Copy task ids + tiers + `blocked-by` + default agents from `sos/manifest.md`. Set all `pending` except tier-1 `ready`. Set `gate_cursor` to `spec:validate`. `status` → `running`.
2. **After task start:** Set row `in_progress`; set `active_plan_step`.
3. **After task complete:** Set `completed`, write `output_hash`, advance dependents to `ready` if deps satisfied; append runtime log.
4. **Gate progression:** Only advance `gate_cursor` in **strict order** when prior gate `passed`. Never skip.
5. **Auto-unblock:** When `gate_status[G]=passed`, remove `G` from every task’s `blocked_by_gates`. Then promote any task whose `blocked_by` tasks are all `completed` and `blocked_by_gates` is empty to `ready`.
6. **Drift:** On `drift_score >= 2`, set task `blocked` or `ready` with new `assigned_agent`, increment `reroute_count`, set `drift_score_last`, **do not** edit manifest/prompts.
7. **Token discipline:** Status tables in logs use compressed rows; no full prompt duplication.
8. **Trace:** Every automated batch update sets `trace_id_last` and appends to `runtime-logs/` with the same id.

---

## Current State (template — replace on use)

```yaml
schema_version: "1.0"
feature_id: "<feature-id>"
swarm_id: "<swarm-id>"
status: idle
started_at: ""
updated_at: ""
active_plan_step: ""
contract_refs: []
gate_cursor: spec:validate
gate_status:
  spec:validate: pending
  contract:auto-validate: pending
  compliance: pending
  security:scan: pending
  test: pending
  build: pending
  deploy: pending
tasks: []
last_output_hash: ""
last_runtime_log: ""
drift_score_last: 0
reroute_count: 0
trace_id_last: ""
optimization_counter: 0
optimization_every_n_tasks: 5
ci_validate: false
pr_gate_strict: false
notes: "Initialize via @RuntimeOrchestrator — read sos/manifest.md first."
```

---

*Consumed by: `.ai/skills/runtime_adaptive_loop.md` · `@RuntimeOrchestrator`*
