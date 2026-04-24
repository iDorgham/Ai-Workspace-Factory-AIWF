---
type: Command
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---


# Command: /swarm

> **Agent:** @Guide + @Router
> **Purpose:** Launch, abort, or check status of coordinated multi-agent execution flows
> **Scope:** Feature-level orchestration across multiple agents

---

## Usage

```bash
/swarm run [feature-name] [--agents @Agent1,@Agent2,@Agent3] [--pattern sequential|parallel|hierarchical] [--live] [--auto] [--dry-run]
/swarm optimize --auto [feature-name]
/swarm abort [feature-name | swarm-id]
/swarm status [feature-name | swarm-id]
/swarm monitor [feature-name | swarm-id] [--once]
/swarm reroute [feature-name] --reason "<why>" [--task T-XXX] [--to @Agent]
```

### Runtime modes (`--live`, `monitor`, `reroute`)

| Mode | Command | Behavior |
|------|---------|----------|
| **Live** | `/swarm run [feature] ... --live` | After each task, **@RuntimeOrchestrator** runs the filesystem loop: read `sos/manifest.md` + `sos/runtime-state.md`, evaluate `drift_score`, checkpoint, re-route if needed. No daemons — human or agent invokes next step; state remains in `sos/runtime-state.md`. |
| **Monitor** | `/swarm monitor [feature] [--once]` | Read-only pass: print compressed status table (tasks, `gate_cursor`, `drift_score_last`) from `sos/runtime-state.md` + manifest alignment. With `--once`, single poll; without, document as “repeat manually after each task” (no background worker). |
| **Reroute** | `/swarm reroute [feature] --reason "..."` | Force reassignment path: log reason → **@ErrorDetective** triage → `.ai/agents/capability-registry.md` lookup → update **only** **`[spec]/sos/runtime-state.md`** when runtime mode is on (never hand-edit phase **`manifest.md`** or spec **`prompt.md`** — regenerate via **`/plan sos`**). Optional `--task` / `--to` overrides defaults. |
| **Auto pipeline** | `/swarm run [feature] ... --auto` | **Zero-prompt loop:** same filesystem iteration as `--live`, but **@RuntimeOrchestrator** applies **auto-unblock**, self-heal on `drift_score >= 2`, and optional weight optimization every N tasks per `.ai/skills/runtime-automation-rules.md`. Still **no daemon** — operator or CI step re-invokes until stop. After each iteration, if `RUNTIME_EXPORT_CI_SUMMARY=1`, run `/runtime sync --ci` (emit summary only; validation obeys `ci_validate` / `pr_gate_strict`). |
| **Optimize** | `/swarm optimize --auto [feature]` | Recompute **`sos/runtime-capability-weights.json`** using `(success_rate * 0.7) - (failure_penalty * 0.3)` and demote/promote rules per `.ai/skills/auto-optimization-loop.md`. Append `trace_id` to runtime log. |
| **Dry-run** | `... --dry-run` | **Read-only rehearsal:** run prerequisite checks + parse `sos/manifest.md` + `sos/runtime-state.md`, print the next iteration plan (tasks that would become `ready`, `gate_cursor`, hypothetical `trace_id`). **No writes** to `sos/runtime-state.md`, `runtime-logs/`, `runtime-capability-weights.json`, or command-logs. |

**Authority split:** **@Router** = plan-time graph + SOS writes. **@RuntimeOrchestrator** = mid-flight state + drift + recovery. **@Router** remains fallback in re-routing hierarchy.

**Logs:** Every `run`/`monitor`/`reroute`/`--auto`/`optimize` append a line to `.ai/plans/active/audit/command-logs/[YYYY-MM-DD].md` and iteration details to `.ai/plans/active/audit/runtime-logs/[feature]-[timestamp].md` when the loop executes. **Every auto-action includes a `trace_id`** (see `.ai/skills/runtime-automation-rules.md`).

---

## Execution Flow

### 1. `/swarm run` — Launch Multi-Agent Execution

**Step-by-Step:**

1. **Validate prerequisites:**
   - [ ] Spec exists: **`.ai/plans/active/features/[phase]/[spec]/plan.md`** (or legacy **`.ai/plans/active/features/[feature-name].md`**)
   - [ ] Phase **`manifest.md`** and/or spec **`prompt.md`** present when using SOS-optimized swarm (else fall back to **`plan.md`** with a warning)
   - [ ] Contract locked for all domains touched by the spec
   - [ ] Current sprint active: `.ai/plans/active/current-sprint.md`
   - [ ] No existing swarm running for this target
   - [ ] If `--live`, `--auto`, or runtime hooks enabled: **`[spec]/sos/runtime-state.md`** exists or will be initialized by **@RuntimeOrchestrator** (read phase **`manifest.md`** / spec **`prompt.md`** first; do not create/modify **`manifest.md`** / **`prompt.md`** here)

2. **Parse parameters:**
   - `feature-name`: Required — identifies the feature plan to execute
   - `--agents`: Optional — override default agent assignments from feature plan
   - `--pattern`: Optional — execution pattern (default: `hierarchical`)

3. **Select execution pattern:**

   | Pattern | When to use | Behavior |
   |---------|-------------|----------|
   | `sequential` | High dependency tasks | Step 1 → Step 2 → Step 3 (each waits for previous) |
   | `parallel` | Independent tasks | Steps with no dependencies run simultaneously |
   | `hierarchical` | Complex features (default) | @Guide coordinates, @Router dispatches, agents execute per dependency graph |

4. **Initialize swarm:**
   ```
   Swarm ID: swarm-[YYYYMMDD]-[feature-slug]
   Status: initialized
   Started at: [timestamp]
   Assigned agents: [list from feature plan or --agents flag]
   Execution pattern: [sequential | parallel | hierarchical]
   ```

5. **Execute per pattern:**

   **Sequential:**
   ```
   For each step in feature plan:
     1. Assign to agent per plan
     2. Agent executes step
     3. Agent updates task status to complete
     4. Next step begins
   ```

   **Parallel:**
   ```
   Identify independent steps (no dependencies):
     Group 1: Steps with no prerequisites → run all simultaneously
     Group 2: Steps depending on Group 1 → run all after Group 1 complete
     ...
   For each group:
     Dispatch all agents in parallel
     Wait for all to complete
     Proceed to next group
   ```

   **Hierarchical:**
   ```
   @Guide reads full feature plan
   @Router builds dependency graph
   @Guide dispatches first available tasks to agents
   As agents complete, @Router resolves next available tasks
   @Guide monitors progress, handles blockers
   Escalate to @EscalationHandler if blocked > 10 minutes
   ```

6. **Monitor and log:**
   - Log every step start/completion to `.ai/plans/active/audit/command-logs/[YYYY-MM-DD].md`
   - Update feature plan status in real-time
   - Update current sprint progress

7. **Complete swarm:**
   - When all feature plan steps complete → mark swarm as `completed`
   - Run quality gates in order: `spec:validate → contract:auto-generate → contract:auto-validate → compliance → security:scan → test → build → deploy`
   - If all gates pass → mark feature as `complete`
   - If any gate fails → create tasks for fixes, swarm status: `failed-gates`

8. **Runtime wrap-up (when `--live` or `--auto` was used):**
   - Set `sos/runtime-state.md` `status` to `completed` or `failed`
   - Final append to `.ai/plans/active/audit/runtime-logs/[feature]-[timestamp].md` with gate summary + `reroute_count` + `trace_id_last`

---

### 1b. `/swarm optimize --auto` — Registry Weight Update

1. Load task outcome tallies from **`[spec]/sos/runtime-state.md`** when present (`tasks[]` statuses by `assigned_agent`).
2. Apply formula and demote/promote rules from `.ai/skills/auto-optimization-loop.md`.
3. Write **`[spec]/sos/runtime-capability-weights.json`** (never phase **`manifest.md`** or spec **`prompt.md`**).
4. Append runtime log line with `trace_id`.

---

### 2. `/swarm abort` — Cancel Running Swarm

**When to use:**
- Feature requirements changed fundamentally
- Critical blocker discovered
- User requests cancellation

**Flow:**
1. Identify active swarm by feature-name or swarm-id
2. Notify all assigned agents to stop work
3. Mark swarm status as `aborted`
4. Log abort reason to feature plan
5. Save partial progress to `.ai/plans/active/features/[feature-name].md`
6. Notify @EscalationHandler if abort is due to blocker
7. Clean up any in-progress branches (if @Automation created them)

---

### 3. `/swarm status` — Check Swarm Progress

**Output format:**
```markdown
## Swarm Status: [feature-name]

**Swarm ID:** swarm-[id]
**Status:** [initialized | running | completed | failed | aborted]
**Started:** [timestamp]
**Elapsed:** [duration]
**Execution pattern:** [sequential | parallel | hierarchical]

### Step Progress
| Step | Agent | Status | Started | Completed | Notes |
|------|-------|--------|---------|-----------|-------|
| 1.0 | @Architect | ✅ complete | HH:MM | HH:MM | Contract locked |
| 2.0 | @Backend | 🔄 in-progress | HH:MM | — | Building API routes |
| 3.0 | @Frontend | ⏳ pending | — | — | Waiting for contract |

### Quality Gates
- spec:validate: ✅ / ❌ / ⏳ pending
- contract:auto-validate: ✅ / ❌ / ⏳ pending
- compliance: ✅ / ❌ / ⏳ pending
- security:scan: ✅ / ❌ / ⏳ pending
- test: ✅ / ❌ / ⏳ pending
- build: ✅ / ❌ / ⏳ pending

### Blockers
- [List any current blockers or "none"]

### Next Steps
- [What's happening next]
- [Estimated completion if available]
```

---

## Common Patterns

### Pattern 1: Standard Feature (Hierarchical)
```bash
/swarm run booking-flow --pattern hierarchical
# Uses default agent assignments from feature plan
# @Guide orchestrates, @Router dispatches
```

### Pattern 2: Parallel Independent Tasks
```bash
/swarm run design-system --agents @Frontend,@Backend,@DesignSystem --pattern parallel
# Frontend builds UI, Backend builds API, DesignSystem audits tokens — all at once
```

### Pattern 3: Sequential High-Risk Tasks
```bash
/swarm run payment-integration --pattern sequential
# Contract → Security audit → Backend → Frontend → Testing (each waits for previous)
```

### Pattern 4: Targeted Agent Override
```bash
/swarm run user-auth --agents @Backend,@Security,@QA --pattern sequential
# Custom agent list — skipping Frontend (backend-only feature)
```

---

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| "Feature plan not found" | No `.ai/plans/active/features/[name].md` | Run `/plan [feature-name]` first |
| "Contract not locked" | Contract exists but lock state ≠ TRUE | Run `/contract lock [domain]` |
| "Swarm already running" | Existing swarm for this feature | Use `/swarm status` to check, or `/swarm abort` to cancel |
| "No agents assigned" | Feature plan missing agent assignments | Update feature plan or use `--agents` flag |
| "Execution failed at step X" | Agent couldn't complete step | Check task log, fix issue, retry step |

---

## Integration Points

- **@Guide:** Orchestrates hierarchical swarms, monitors progress
- **@Router:** Builds dependency graphs, dispatches tasks optimally
- **@EscalationHandler:** Receives blocked swarms, resolves critical failures
- **@Automation:** Creates branches, commits, PRs as steps complete
- **@MetricsAgent:** Tracks swarm velocity, success rate, avg duration
- **@RuntimeOrchestrator:** Live filesystem loop, `sos/runtime-state.md`, drift detection, re-routing, auto-unblock + self-heal (`--live`, `--auto`, `monitor`, `reroute`, `optimize --auto`)

---

*Command Version: 1.3 | Created: 2026-04-08 | Maintained by: @Guide*
