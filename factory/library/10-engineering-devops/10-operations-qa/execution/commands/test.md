---
type: Command
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---


# /test — Testing & Validation

## Syntax
```
/test unit [--scope path]       → Run unit tests
/test integration [--scope]     → Run integration tests (real DB)
/test e2e [--scope]             → Run Playwright E2E tests
/test visual [--scope]          → Run visual regression tests
/test a11y [--scope]            → Run accessibility audit
/test contract [domain]         → Validate API responses against schema
/test --coverage                → Generate coverage report
/test --watch                   → Watch mode during development
/test all                       → Full pyramid (all types)
```

## Primary Agents
`@QA` (leads) + `@VisualQA` (visual/a11y) + `@Debugger` (on failure) + `@ErrorDetective` (pattern capture)

---

## Phase 0 — Pre-Test Checks (mandatory before writing or running tests)

### Coverage Gap Identification (incremental strategy)
```
Before writing any tests:

1. What test coverage already exists for this feature?
   (Don't rewrite existing tests — identify gaps only)

2. Which behaviors are NOT covered?
   - Contract fields not exercised?
   - Error states not tested?
   - AR locale not covered?
   - Edge cases (empty state, boundary values) missing?

3. Write ONLY tests for uncovered behaviors
   See: .ai/skills/incremental-build-strategy.md (test coverage gap detection)

Result: 2 targeted tests instead of rewriting 20 existing ones
```

### Anti-Pattern Scan for Test Code
```
Load: .ai/memory/anti-patterns.md
Filter: test-relevant patterns
Apply as constraints before writing test code:

Common test anti-patterns (injected automatically):
  - Shared mutable state between tests (breaks test isolation)
  - mocking the DB (use real test DB — learned from previous incidents)
  - Testing implementation details vs behavior
  - Missing AR locale assertion in visual tests
  - Asserting on exact timestamps (flaky — use relative assertions)
```

---

## Coverage Targets

| Type | Target | Blocks merge if |
|------|--------|----------------|
| Unit | 45% overall | Coverage drops below 40% |
| Integration | 30% coverage | Critical paths uncovered |
| E2E | All happy paths | Any critical journey fails |
| Visual | All components, 3 viewports × 2 locales | Drift > 0.02% threshold |

---

## /test unit

```markdown
### @QA — Unit Test Report
Running: pnpm vitest --coverage --filter='...[HEAD^1]'

Results:
  Test Files: [N] passed / [N] failed
  Tests:      [N] passed / [N] failed
  Duration:   [N]s

Coverage:
  Statements: [N]% [✅≥45% | ❌<40%]
  Functions:  [N]%
  Lines:      [N]%
  Branches:   [N]%

Notable:
  ✅ [Domain]Service: [N]% coverage
  ⚠️ [Domain]Service: [N]% — integration tests recommended

Status: PASS / FAIL | Next: /test integration
```

**On test failure → immediate error capture:**
```
@Debugger activated:
  Step 1: Read the exact test assertion that failed
  Step 2: Read the actual vs expected values
  Step 3: Diagnose: contract mismatch? implementation bug? stale mock?
  Step 4: Fix the ROOT CAUSE (never fix the test assertion to match wrong behavior)
  Step 5: @ErrorDetective captures EP-[id] to error-patterns.md
```

---

## /test integration

```markdown
### @QA — Integration Test Report
Running: pnpm vitest --project=integration

Environment: Real test database (never mocked — AP: use real DB for integration tests)

Results:
  [N] tests passed / [N] failed

Critical paths covered:
  ✅ [Feature] happy path (create → read → update → delete)
  ✅ Auth flow (token issue → protected route → refresh → revoke)
  ❌ [Feature] error path — [specific failure]

Status: PASS / FAIL
```

**On failure → @Debugger leads, @ErrorDetective captures.**

---

## /test e2e

```markdown
### @QA — E2E Test Report
Running: pnpm playwright test

  ✅ [feature].spec.ts (LTR)   — [N] tests, [N]s
  ✅ [feature].spec.ts (RTL)   — [N] tests, [N]s  ← AR locale always required
  ✅ auth.spec.ts              — [N] tests, [N]s
  ❌ [feature].spec.ts         — [N] failed

Failures:
  FAIL: "[test name]" — [exact error]
  Route to: @Debugger (root cause) → @Frontend or @Backend (fix) → re-run

Status: FAIL | @Debugger notified
```

**On failure:** @Debugger runs the 6-step diagnosis protocol. Fix is minimal — only the failing path. @ErrorDetective captures EP-[id].

---

## /test visual

```markdown
### @VisualQA — Visual Regression Report
Running: Playwright + Percy (or local snapshot comparison)

Locales tested: EN (LTR) + AR (RTL) — both REQUIRED
Viewports: mobile (375px) + tablet (768px) + desktop (1440px)

  ✅ BookingCard — EN × 3 viewports: no drift
  ✅ BookingCard — AR × 3 viewports: no drift
  ❌ BookingForm — AR mobile: drift 0.8% (above 0.02% threshold)
    → Diff image: [path to diff]
    → Cause: padding-inline-start changed — AP-001 check (was this a logical property violation?)

Status: FAIL (1 component, AR mobile)
```

**On visual failure:**
```
1. Check if violation matches AP-001 (directional CSS) or AP-003 (raw spacing)
2. If AP match: @ErrorDetective captures recurrence
3. @Frontend fixes the specific rule violation
4. @VisualQA updates baseline after confirmed fix
5. Never: update baseline without fixing the cause (masks the issue)
```

---

## /test a11y

```markdown
### @QA — Accessibility Audit
Tool: axe-playwright + WCAG 2.1 AA checklist

Page: /[route]
  ✅ Images: all have alt text
  ✅ Buttons: all have accessible names
  ✅ Forms: all inputs have visible labels + aria-describedby on errors
  ⚠️ Color contrast: [N] elements below 4.5:1
    → [component:line]: [token used] → use [higher-contrast token]
  ✅ Focus order: logical and complete
  ✅ Keyboard navigation: all paths reachable
  ✅ Screen reader: tested with aria-live for dynamic content

WCAG 2.1 Score: [N]% | Target: 100% AA
```

**On a11y failure:** Each violation is an AP candidate. If it's the 2nd occurrence of the same a11y pattern (e.g., missing aria-label on icon buttons) → @ErrorDetective promotes to anti-pattern immediately.

---

## /test contract [domain]

Validates live API responses against the locked Zod schema:

```markdown
### @QA — Contract Test Report
Domain: [domain] | Contract: packages/shared/src/contracts/[domain].ts (locked v[N])

Testing: every API endpoint that produces [domain] data

  GET /api/[domain]         → [N] fields validated | ✅ all match schema
  POST /api/[domain]        → Input validation ✅ | Response shape ✅
  PUT /api/[domain]/:id     → Input validation ✅ | Response shape ✅
  DELETE /api/[domain]/:id  → Response matches contract ✅

Status: PASS — all responses conform to locked schema v[N]
```

**On contract mismatch:** CRITICAL — @ContractLock reviews drift. @ErrorDetective captures as AP-030 recurrence if contract was being bypassed.

---

## Self-Healing on Flaky Tests

```
Flaky test detected (failed [N] of 5 runs):
  "[test name]" — timing issue / network issue / test pollution suspected

@QA self-healing attempt:
  1. Identify if it's: timing → add waitFor | pollution → add cleanup | network → add retry
  2. Re-run 5 times with fix → [N]/5 pass
  3. If 5/5 pass → apply fix to test file
  4. If still flaky → route to @Debugger for deeper diagnosis
  5. Log self-healing event to: .ai/plans/active/audit/self-healing.md
  6. @ErrorDetective: is this a known flaky pattern? → check error-patterns.md

Never: disable or skip a flaky test without first diagnosing root cause
```

---

## On Test Failure — Error Capture Protocol

**Immediately after any test failure:**

```markdown
## Test Failure → Error Capture

@ErrorDetective writes to .ai/memory/error-patterns.md:

--- ERROR CAPTURE ---
Date: YYYY-MM-DD
Source: /test [type] run
Agent: @QA
Task type: [unit | integration | e2e | visual | a11y | contract]
Domain: [affected domain]
Severity: [CRITICAL (contract fail, security) | HIGH (E2E fail) | MEDIUM (unit fail) | LOW (visual drift)]
Pattern type: [classify]

Error: [exact test failure message]
Root Cause: [diagnosed by @Debugger]
Fix Applied: [what resolved it]
Tokens wasted: [estimate]
Prevention rule: [what pre-flight check would prevent this?]
---

Recurrence check:
  2nd occurrence of same pattern? → @ErrorDetective promotes to anti-patterns.md
  @ContextSlicer updates injection pool for next task
```

---

## Execution Log

Every `/test` run is logged to `.ai/plans/active/audit/command-logs/YYYY-MM-DD.md`:

```
[YYYY-MM-DD HH:MM] /test all
  Pre-test: coverage gap check (2 gaps found) | AP scan (3 test anti-patterns injected)
  Unit: PASS (91%, 187 tests)
  Integration: PASS (critical paths covered)
  E2E: FAIL (2 of 14) → @Debugger activated → fixed → re-run PASS
  Visual: PASS (EN + AR, 3 viewports)
  a11y: WARN (1 contrast issue queued)
  Error capture: EP-001 written (E2E failure — timing, not AP match)
  Result: PASS (after fix) | Tokens used: ~3,200
```

---

*Invokes: @QA, @VisualQA, @Debugger, @ErrorDetective*
*Skills: mistake-prevention-system, pre-flight-checklist, incremental-build-strategy, playwright-e2e, visual-regression-testing, edge-case-boundary-testing, self-healing-workflows*
*Reports to: @MetricsAgent (coverage trend, flaky test rate)*
