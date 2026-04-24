---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# Runtime Automation Rules

Self-managing pipeline rules for **@RuntimeOrchestrator**. No daemons: each rule runs when a human/agent completes a loop step or invokes `/swarm run --auto` (zero-prompt = same loop, repeated until stop condition without extra chat prompts).

## Trace ID (mandatory)

Every automated transition appends one line to `.ai/plans/active/audit/runtime-logs/[feature]-[timestamp].md` including:

`trace_id` — `RT-[YYYYMMDD]-[6 hex]` (filesystem-safe, unique per append batch).

Also set `trace_id_last` in `sos/runtime-state.md` YAML to the latest trace.

## Auto-Transition Table

| Trigger | Condition | Automated action | Log tag |
|---------|-----------|------------------|---------|
| **gate_passed** | `gate_status[G]` transitions to `passed` (strict order preserved) | 1) Advance `gate_cursor` to next gate only after prior `passed`. 2) **Auto-unblock:** remove `G` from every task’s `blocked_by_gates[]` (if present). 3) For each task: if `blocked_by` task ids all `completed` and `blocked_by_gates` empty → set `ready` (was `blocked`/`pending`). | `AUTO:gate_unblock` |
| **drift_ge_2** | `drift_score >= 2` | Invoke **@ErrorDetective** triage path; update `assigned_agent` per registry; increment `reroute_count`; **do not** touch SOS manifest/prompts. | `AUTO:drift_heal` |
| **task_completed** | Task row → `completed` | Recompute ready set; set `last_output_hash`; append audit row; if `optimization_counter % N == 0` optionally run **auto-optimization-loop** (see that skill). | `AUTO:task_close` |
| **all_tasks_done** | All tasks `completed` | Run gate pipeline in order until terminal; set `status`; append final audit. | `AUTO:swarm_close` |

## Auto-Unblock Detail

1. **Manifest deps:** `blocked_by` remains the SOS truth from `sos/manifest.md` (read-only). Runtime may only add **`blocked_by_gates`** (optional per-task) for gate gating — never remove manifest task ids from `blocked_by` except:
   - **Correction:** When a gate passes that was the *sole* synthetic blocker, agents may clear `blocked_by_gates` entries only (never delete manifest-derived task ids manually; if manifest wrong, escalate — AP-060).
2. **Gate-only unblock:** On `gate_status[G]=passed`, strip `G` from `blocked_by_gates` on all tasks.
3. **Ready promotion:** If ∀`b` ∈ `blocked_by`: task `b` is `completed`, and `blocked_by_gates` is empty or all referenced gates `passed`, then `status := ready`.

## Self-Heal Drift

When `drift_score >= 2`:

1. Log `trace_id` + components (contract / gate / anti-pattern).
2. **@ErrorDetective** classifies → suggested agent from `.ai/agents/capability-registry.md`.
3. Apply **predictive routing** weights from `sos/runtime-capability-weights.json` (demote `<0.5` success_rate; promote fallback when `>0.8`).
4. Emit **delta** prompt delta (≤4K) in runtime log only.

## Completed → Audit Append

On any task → `completed`:

- Append compressed row to latest runtime log for feature (create file if missing for this run).
- Rotate logs per **log hygiene** (`.ai/commands/runtime.md` — `/runtime audit --auto-clean`).

## Token Economy

- Automation steps emit **tables**, not prose.
- Per-iteration assembled context ≤ **4K** tokens (unchanged).

## 🌍 Regional Calibration (MENA Context)

- **Cultural Alignment:** Ensure all logic respects regional business etiquette and MENA market expectations.
- **RTL Compliance:** Logic must explicitly handle Right-to-Left (RTL) flow where relevant.

## 🛡️ Critical Failure Modes (Anti-Patterns)

- **Anti-Pattern:** Generic Output -> *Correction:* Apply sector-specific professional rules from RULE.md.
- **Anti-Pattern:** Global-Only Logic -> *Correction:* Verify against MENA regional calibration.

---

*Pairs with: `.ai/skills/runtime-adaptive-loop.md` · `.ai/skills/auto-optimization-loop.md`*