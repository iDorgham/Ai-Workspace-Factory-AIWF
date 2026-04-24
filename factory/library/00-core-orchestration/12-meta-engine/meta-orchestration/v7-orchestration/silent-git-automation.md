---
type: Generic
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# AIWF v7.0.0 — Silent Git Automation Engine
# Library Component: 12-meta-engine/meta-orchestration/v7-orchestration/silent-git-automation.md
# Version: 7.0.0 | Reasoning Hash: sha256:git-v7-2026-04-23
# ============================================================

## Overview

The Silent Git Automation Engine manages all Git operations during `/dev` execution. It operates **silently** (no user prompts required) but with strict conditional gates to prevent unsafe merges. All operations are logged to `.ai/logs/github_auto.log` with full rationale.

> ⚠️ **Critical Separation**: Git automation **NEVER triggers Vercel deployment**. The `/deploy` command is the only path to deployment and requires explicit user invocation.

---

## Branch Strategy

### Branch Naming Convention
```
phase/{N}-{slug}     # Primary: for /dev --phase=N
feature/{slug}       # Secondary: for standalone features
fix/{issue-slug}     # Tertiary: for /fix patches
```

### Branch Lifecycle
```
main
 └── phase/1-hotel-booking          ← auto-created by /dev --phase=1
      └── feature/fawry-integration ← auto-created for sub-features
```

### Branch Creation Logic
```bash
# Auto-executed silently at /dev start
git checkout -b phase/{N}-{slug}    # if not already on correct branch
git push --set-upstream origin phase/{N}-{slug}
```

---

## Commit Format

All auto-commits follow this structure (append-only, never force-push):

```
{type}({scope}): {description}

#sdd-trace:{REQ-ID}
#phase:{N}
#agent:{agent-id}
reasoning-hash:{sha256:...}
approved-by:{Dorgham-Approved|pending_omega}
```

### Commit Types
| Type | Usage |
| :--- | :--- |
| `feat` | New feature implementation |
| `fix` | Bug fix or healing bot patch |
| `spec` | spec.yaml or contract updates |
| `test` | Test additions or updates |
| `docs` | Documentation only changes |
| `chore` | Scaffolding, deps, config |
| `regional` | MENA/regional adaptations |

### Example Commit
```
feat(hotel-booking): implement property search with availability calendar

#sdd-trace:REQ-001
#phase:1
#agent:T0-001-master-guide
reasoning-hash:sha256:abc123def456
approved-by:Dorgham-Approved
```

---

## Auto-Merge Gate (Conditional)

Auto-merge to `main` is executed **only when ALL 5 gates pass**:

```yaml
auto_merge_gates:
  gate_1:
    name: "All Tests Pass"
    check: "exit code 0 from /test --phase=N"
    severity: blocking

  gate_2:
    name: "Contract Coverage ≥ 100%"
    check: "contract-coverage.json shows 100% for all AC items"
    severity: blocking

  gate_3:
    name: "Omega Gate Approval"
    check: "approved_by: Dorgham-Approved in spec.yaml"
    severity: blocking

  gate_4:
    name: "Regional Compliance"
    check: "regional-compliance gate passed (if --region was active)"
    severity: blocking
    conditional: "only when --region flag was used"

  gate_5:
    name: "No Pending Mutations"
    check: "no uncommitted Healing Bot repairs or spec changes in queue"
    severity: blocking
```

### Auto-Merge Execution
```bash
# Only runs if all 5 gates pass
git checkout main
git merge --no-ff phase/{N}-{slug} -m "release(phase-{N}): merge {slug} [auto-merge] #gates:5/5 #hash:{reasoning_hash}"
git push origin main
# DO NOT trigger /deploy — user must run /deploy explicitly
```

---

## Audit Log Format

File: `.ai/logs/github_auto.log`

```
[ISO-8601] ACTION={branch|commit|push|merge} | BRANCH={name} | HASH={commit-sha} | GATES={N/5} | STATUS={success|blocked} | REASON={...} | REASONING-HASH={sha256:...}
```

### Example Log Entry
```
[2026-04-23T12:56:22+02:00] ACTION=auto-merge | BRANCH=phase/1-hotel-booking | HASH=9a52570 | GATES=5/5 | STATUS=success | REASON=all gates passed | REASONING-HASH=sha256:abc123
[2026-04-23T12:56:22+02:00] ACTION=auto-merge-BLOCKED | BRANCH=phase/2-payments | HASH=pending | GATES=3/5 | STATUS=blocked | REASON=contract-coverage 87% (need 100%) | REASONING-HASH=sha256:def456
```

---

## Toggle Controls

```
/git auto on|off        # Enable/disable silent Git automation entirely
/git merge-auto on|off  # Enable/disable conditional auto-merge specifically
/git status             # Show current branch, uncommitted changes, gate status
```

---

## Rollback Protocol

If an auto-commit needs reverting:
```bash
git revert {commit-sha}   # append-only — never force-push or reset
git push origin {branch}
# Log to .ai/logs/github_auto.log with REASON=rollback
```

---

*Component version: 7.0.0*
*Library path: 12-meta-engine/meta-orchestration/v7-orchestration/silent-git-automation.md*
*Last updated: 2026-04-23T12:56:22+02:00*
*Reasoning Hash: sha256:git-v7-2026-04-23*
