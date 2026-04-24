---
type: Command
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---


# /runtime — CI Sync, Audit, Log Hygiene

> **Agent:** @RuntimeOrchestrator + @Automation  
> **Purpose:** Bind filesystem runtime state to CI artifacts, rotate logs, compress snapshots — **no daemons**, **no external APIs** (GitHub Actions reads committed files only).

---

## Syntax

```bash
/runtime sync --ci              # Emit validation + compressed snapshot (stdout / step summary)
/runtime audit --auto-clean     # Rotate runtime logs: size >500KB dir or age >30d → archive
/runtime validate [--strict]    # Run scripts/validate/runtime_state_guard.py locally
```

---

## `/runtime sync --ci`

**When:** In CI (workflow) or locally before push.

**Steps:**

1. Resolve repo root; discover optional `sos/runtime-state.md` (repo root) + `.ai/plans/active/features/*/sos/runtime-state.md`. Bootstrap: **`.ai/templates/sos-root/runtime-state.md`**.
2. Run `python3 scripts/validate/runtime_state_guard.py --emit-summary` → append to `$GITHUB_STEP_SUMMARY` in Actions, or print locally.
3. Run `python3 scripts/validate/runtime_state_guard.py --ci` — fails if any file has `ci_validate: true` or `pr_gate_strict: true` **and** (`drift_score_last > 0` OR any `gate_status` value ≠ `passed`).
4. Log append to `.ai/plans/active/audit/command-logs/[YYYY-MM-DD].md` with `trace_id`.

**DMP:** Step 0 — load `.ai/memory/anti-patterns.md` before mutating disk.

**Token discipline:** Summary is a **single compressed table** (paths + status + drift + trace).

---

## `/runtime audit --auto-clean`

**Log hygiene (filesystem):**

| Rule | Action |
|------|--------|
| Directory `.ai/plans/active/audit/runtime-logs/` total size **> 500KB** | Move oldest files (by mtime) to `.ai/plans/archive/runtime-logs/` until under 500KB or ≤3 files remain |
| Files **older than 30 days** (mtime) | Move to `.ai/plans/archive/runtime-logs/` |
| Archive | Preserve tree; never delete without moving to `archive/` first |

**Implementation:** `bash scripts/git/runtime-log-rotate.sh` (idempotent; portable mtime).

**Trace:** Each batch append one line to latest runtime log or command-log with `trace_id` + count moved.

---

## `/runtime validate`

```bash
python3 scripts/validate/runtime_state_guard.py --ci
python3 scripts/validate/runtime_state_guard.py --critical-only   # pre-commit style
```

---

## Integration

- **GitHub Actions:** `.github/workflows/runtime-gate-validator.yml`
- **Pre-commit:** `scripts/git/pre-commit` → `runtime_state_guard.py --critical-only`
- **Swarm:** `/swarm run --auto` documents calling `/runtime sync --ci` after each loop when `RUNTIME_EXPORT_CI_SUMMARY=1`

---

*Command Version: 1.0 | Maintained by: @Guide + @RuntimeOrchestrator*
