# Pre-Flight Checklist

## Purpose
A mandatory gate that runs before every task execution. Catches 90% of preventable errors in under 30 seconds of agent processing. Costs ~200 tokens; saves 2,000–10,000 tokens in corrections.

---

## Universal Pre-Flight (ALL agents, ALL tasks)

```markdown
## Universal Pre-Flight Gate
(Complete before any task output)

### 1. CONTEXT CHECK
- [ ] Dynamic Memory Protocol executed (8-step load: Step 0 anti-patterns + Steps 1–7)?
- [ ] Anti-pattern scan completed (mistake-prevention-system.md Layer 1)?
- [ ] Relevant lessons-learned.md entries read?

### 2. CONTRACT CHECK
- [ ] Does this task touch a domain that needs a contract?
   - YES → Is the contract locked? (.lock file exists in contracts/)
     - LOCKED ✅ → continue
     - UNLOCKED ❌ → STOP: route to @Architect for contract lock before proceeding
   - NO (pure refactor / doc / config) → continue

### 3. PLAN STEP CHECK
- [ ] Am I working on the correct plan step? (.ai/plans/active/current-sprint.md)
- [ ] **SDD:** Is the active slice **`.ai/plans/active/features/[phase]/[spec]/plan.md`** (and phase **`manifest.md`** if multi-spec) identified? See **`.ai/skills/sdd-spec-workflow.md`**
- [ ] Is there a task file for this? (.ai/plans/active/tasks/[task].md)
- [ ] Am I duplicating work another agent is doing?

### 4. FILESYSTEM CHECK
- [ ] Does the file I'm creating already exist? (would overwrite without intent)
- [ ] Does the file I'm modifying exist? (must read before editing)
- [ ] Does every import I'm adding already exist in the filesystem?

### 5. SCOPE CHECK
- [ ] Am I staying within my assigned task scope?
- [ ] Am I making changes outside my domain? (if yes → route to correct agent)
- [ ] Is this change isolated enough to not break unrelated features?
```

---

## Agent-Specific Pre-Flights

### @Frontend Pre-Flight
```markdown
### @Frontend Pre-Flight
- [ ] CSS logical properties will be used (no left/right/margin-left)?
- [ ] All text via `t('key')` i18n function (no hardcoded strings)?
- [ ] All colors/spacing via CSS variables (no raw hex/px)?
- [ ] RTL layout will work without code changes?
- [ ] All interactive elements have aria-* labels?
- [ ] shadcn/ui component being used before building custom?
- [ ] Component exists in packages/ui before creating in apps/web?
```

### @Backend Pre-Flight
```markdown
### @Backend Pre-Flight
- [ ] All inputs validated with Zod schema from contracts/?
- [ ] All outputs typed against locked contract fields only?
- [ ] Prisma query has `take:` limit (never unbounded findMany)?
- [ ] No raw SQL unless using Prisma.$queryRaw with parameterized values?
- [ ] Auth middleware applied to protected routes?
- [ ] Rate limiting on public endpoints?
- [ ] Error response format matches API contract?
```

### @DBA Pre-Flight
```markdown
### @DBA Pre-Flight
- [ ] Migration uses expand-backfill-contract pattern (zero-downtime)?
- [ ] Migration has a rollback SQL block?
- [ ] Column additions are nullable first (then NOT NULL after backfill)?
- [ ] Index uses CONCURRENTLY to avoid table lock?
- [ ] Migration tested against production-volume data estimate?
- [ ] No breaking change to existing columns without versioning?
```

### @QA Pre-Flight
```markdown
### @QA Pre-Flight
- [ ] Tests cover the contract (all schema fields exercised)?
- [ ] Edge cases covered: empty state, error state, boundary values?
- [ ] Tests are isolated (no shared mutable state between tests)?
- [ ] Playwright tests run against real DOM, not mocked?
- [ ] Visual tests capture both EN and AR variants?
- [ ] Accessibility assertions included (axe-playwright or similar)?
```

### @Security Pre-Flight
```markdown
### @Security Pre-Flight
- [ ] No secrets in code, env files, or logs?
- [ ] User inputs sanitized before DB/query use?
- [ ] OWASP Top 10 review for this feature type done?
- [ ] Auth/authz checks present on every protected operation?
- [ ] Rate limiting in place on auth and public endpoints?
- [ ] Zero-trust assumption: validate everything, trust nothing?
```

### @Automation Pre-Flight (/commit, /push, /deploy)
```markdown
### @Automation Pre-Flight
- [ ] quick-check.sh passes (lint + typecheck)?
- [ ] No secrets staged for commit (secrets scan done)?
- [ ] Contract:validate gate passed?
- [ ] compliance gate passed?
- [ ] Tests passing (at least unit tests for changed code)?
- [ ] PR title follows conventional commits format?
- [ ] Staging deploy tested before production deploy?
```

---

## Pre-Flight Output Format

```markdown
## @[AgentName] — Pre-Flight Complete
**Task:** [description] | **Date:** YYYY-MM-DD

### Gate Results
| Gate | Status | Notes |
|------|--------|-------|
| Dynamic Memory Protocol | ✅ | All 7 steps loaded |
| Anti-pattern scan | ✅ | 2 matched — constraints applied |
| Contract: booking.ts | ✅ LOCKED v1.3 | |
| Plan step | ✅ Step 4.2 | |
| Filesystem | ✅ | File exists, read before edit |
| Scope | ✅ | Staying within @Frontend domain |

### Applied Constraints (from anti-pattern scan)
- AP-003: Using `ms-`/`me-` instead of `left`/`right` ← applied
- AP-011: CSS variables only for colors ← applied

**Verdict: CLEAR TO PROCEED** ✅
```

If any gate fails:
```markdown
**Verdict: BLOCKED** ❌
**Blocker:** Contract `payment.ts` is UNLOCKED
**Action required:** `/contract lock payment` → then re-run this task
**Routing:** @Architect → @ContractLock → [return here]
```

---

## Fast-Path for Simple Tasks

For tasks with scope <500 tokens (doc updates, config tweaks, single-line fixes):
```markdown
### Fast Pre-Flight (simple tasks only)
- [ ] Not touching contracts or DB?
- [ ] Not touching auth or security?
- [ ] Not touching shared packages?
- [ ] Not touching i18n keys?

If ALL yes → FAST TRACK (skip agent-specific checks, run universal only)
```

---

## Token Cost of Skipping Pre-Flight

```
Skipped gate               | Average extra tokens to fix
---------------------------|----------------------------
Anti-pattern scan          | 2,000–8,000 (repeating known mistake)
Contract check             | 5,000–15,000 (building on wrong schema)
Filesystem check           | 1,000–3,000 (overwriting existing work)
Scope check                | 3,000–10,000 (rework when agent exceeds scope)
@Backend input validation  | 4,000+ (security review + rewrite)
```

## 🌍 Regional Calibration (MENA Context)

- **Cultural Alignment:** Ensure all logic respects regional business etiquette and MENA market expectations.
- **RTL Compliance:** Logic must explicitly handle Right-to-Left (RTL) flow where relevant.

## 🛡️ Critical Failure Modes (Anti-Patterns)

- **Anti-Pattern:** Generic Output -> *Correction:* Apply sector-specific professional rules from RULE.md.
- **Anti-Pattern:** Global-Only Logic -> *Correction:* Verify against MENA regional calibration.

---

## Success Criteria
- [ ] Pre-flight gate runs before every code-generating task (no exceptions)
- [ ] Every BLOCKED verdict is resolved before work continues
- [ ] Constraints from anti-pattern scan visibly applied in output
- [ ] Fast-path only used for clearly non-critical tasks
- [ ] Pre-flight completion logged in audit file