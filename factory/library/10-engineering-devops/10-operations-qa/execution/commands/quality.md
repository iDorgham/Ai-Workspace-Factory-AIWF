---
type: Command
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---


# /quality — Governance, Compliance & Mistake Prevention

## Syntax
```
/quality                        → Full audit (all checks) — same as /quality all
/quality all                    → Full compliance audit (all checks)
/quality security               → OWASP + secrets + dependency audit
/quality compliance             → compliance gate (tokens, a11y, i18n, RTL)
/quality tokens                 → Design token usage audit
/quality i18n                   → Internationalization coverage audit
/quality a11y                   → Accessibility audit (WCAG 2.1 AA)
/quality contracts              → Contract adherence audit
/quality mistakes               → Error pattern analysis + anti-pattern effectiveness report
/quality --scope [path]         → Audit specific files or directory
/quality --fix                  → Auto-fix violations where possible
```

## Primary Agents
`@Reviewer` (leads) + `@Security` + `@DesignSystem` + `@Content` + `@QA` + `@ErrorDetective`

---

## Phase 0 — Pre-Quality Scan (mandatory, runs before any gate)

### Anti-Pattern Cross-Reference
Before running any quality gate, `@Reviewer` loads the anti-patterns registry and checks:

```
Load: .ai/memory/anti-patterns.md
Cross-reference: every AP entry against the scope being audited
Result: pre-populated violation candidates before deep scan

Why this matters: AP-based checks are deterministic — they run in <1% of the tokens
that a deep semantic scan requires. Running AP-first means:
  - Known violations surface in seconds
  - Deep scanner focuses only on NEW violation patterns
  - Recurring AP violations are flagged for @ErrorDetective immediately
```

### Violation Source Classification
Every violation found during quality is classified:

```
SOURCE_AP    → matches an existing anti-pattern (AP-[id])
               → @ErrorDetective logs to error-patterns.md
               → if this is the 2nd occurrence: escalate to recurrence alert
               → if 3rd+ occurrence: CRITICAL — AP injection may be failing

SOURCE_NEW   → new violation pattern not yet in anti-patterns.md
               → @ErrorDetective logs to error-patterns.md as candidate
               → if similar to existing AP: merge/update the AP entry
               → if genuinely new: @KnowledgeSynthesizer creates AP after 2 occurrences
```

---

## Phase 1 — Quality Gate Execution (in order)

Gates run in the Sovereign-mandated sequence. Never skip. Never reorder.

```
Gate 1: spec:validate         → @Architect + @QA (spec + AC quality — always first)
Gate 2: contract:auto-validate → @ContractLock (Zod from Data Shape → validate → lock)
Gate 3: compliance     → @Reviewer + @DesignSystem + @Content
Gate 4: security:scan       → @Security
Gate 5: test                → @QA (unit + integration + E2E coverage thresholds)
Gate 6: build               → Turborepo compilation

Each gate: PASS → next gate | FAIL → capture + fix path + optional block
```

### Gate 1 — spec:validate (@Architect + @QA)

```
Checks:
  ✓ plan.md contains User Story, numbered testable AC (with AC IDs), plain-language Data Shape, Edge Cases
  ✓ No ambiguous or purely subjective AC without measurable criteria

FAIL: block contract + implementation until spec is clarified
```

### Gate 2 — contract:auto-validate (@ContractLock)

```
Checks:
  ✓ Every domain in use has a contract: packages/shared/src/contracts/[domain].ts
  ✓ Contract is locked (`.lock` file + SHA-256 fingerprint match)
  ✓ No drift: contract fields match what the implementation uses
  ✓ No unlocked contracts in any active build path
  ✓ Under SDD: Zod aligns with confirmed Data Shape from plan.md

FAIL: block downstream gates until contracts are valid and locked
CAPTURE: if contract drift detected → EP-[id] in error-patterns.md (matches AP-030)
```

### Gate 3 — compliance (@Reviewer)

```
Checks (each maps to an anti-pattern):
  ✓ Design tokens:  No raw hex (#...) or px values in code     [AP-002, AP-003]
  ✓ i18n:          No hardcoded user-facing strings            [AP-010]
  ✓ RTL:           No directional CSS (ml-, mr-, pl-, pr-,     [AP-001]
                   margin-left, margin-right, padding-left/right)
  ✓ Contracts:     All API inputs/outputs use zValidator(Zod)  [AP-041]
  ✓ pnpm catalog:  No version numbers in package.json files    [@DependencyManager]
  ✓ TypeScript:    No `any` type usage                         [AP-031]
  ✓ Accessibility: aria-* on all interactive elements          [WCAG]

Auto-fixable violations (apply with --fix):
  - Directional CSS → logical property equivalent
  - Raw color → nearest CSS variable suggestion
  - Missing aria-label → suggested label from context

Non-auto-fixable (requires agent):
  - Hardcoded strings (need i18n key + locale file entry from @Content)
  - Wrong contract field reference (need contract check from @ContractLock)
  - Missing auth middleware (need @Backend to apply)
```

### Gate 4 — security:scan (@Security)

```
Checks:
  ✓ No secrets in code, logs, or committed files             [AP-040]
  ✓ Input validation (Zod) at all API boundaries             [AP-041]
  ✓ Auth middleware on all non-public routes                 [AP-042]
  ✓ Rate limiting on auth + public endpoints
  ✓ OWASP Top 10 spot-check for the changed code
  ✓ pnpm audit — no CRITICAL or HIGH vulnerabilities

FAIL on: any CRITICAL finding | secrets detected | OWASP A01/A02/A03 violation
CAPTURE: every security violation → EP-[id] in error-patterns.md
```

### Gate 5 — test (@QA)

```
Coverage thresholds (blocks merge if dropped below):
  Unit:        40% overall minimum | 45% target
  Integration: Critical paths covered
  E2E:         All happy paths passing

FAIL: any test failure | coverage drop below threshold | flaky test >20% fail rate
CAPTURE: test failures → EP-[id] in error-patterns.md
         Flaky tests → @QA self-healing attempt before flagging as failure
```

### Gate 6 — build (Turborepo)

```
pnpm turbo run build
  ✓ TypeScript compilation passes (no type errors)
  ✓ All packages build successfully
  ✓ No circular dependency errors

FAIL: any build error
CAPTURE: build error → EP-[id] | route to @Debugger for root cause
```

---

## /quality all — Full Audit Output

```markdown
### @Reviewer — Sovereign Full Compliance Report
Date: YYYY-MM-DD | Scope: Full workspace | Files scanned: [N]

┌──────────────────────────────────────────────────────────────┐
│  Sovereign COMPLIANCE SCORE: [N]%  ✅ / ⚠️ / ❌                    │
│  Status: PASS (≥90%) / WARN (80–89%) / FAIL (<80%)           │
└──────────────────────────────────────────────────────────────┘

## Gate Results
| Gate | Score | Status | Violations |
|------|-------|--------|-----------|
| spec:validate | 100% | ✅ | 0 |
| contract:auto-validate | 100% | ✅ | 0 |
| compliance | 97% | ✅ | 3 minor |
| security:scan | 100% | ✅ | 0 |
| test | 91% | ✅ | 0 |
| build | 100% | ✅ | 0 |

## Violations Found
| # | File | Line | Violation | AP-ID | Source | Severity | Auto-fix |
|---|------|------|-----------|-------|--------|----------|---------|
| 1 | BookingCard.tsx | 14 | Raw color #2D3748 | AP-002 | SOURCE_AP | HIGH | ✅ → var(--color-surface-secondary) |
| 2 | BookingCard.tsx | 42 | Hardcoded "Book Now" | AP-010 | SOURCE_AP | CRITICAL | ❌ (needs @Content) |
| 3 | NavigationBar.tsx | 28 | margin-left class | AP-001 | SOURCE_AP | HIGH | ✅ → margin-inline-start |

## Anti-Pattern Recurrence Alert
| AP-ID | This Run | Total (sprint) | Status |
|-------|---------|----------------|--------|
| AP-001 (directional CSS) | 1 | 3 | ⚠️ RECURRING — injection may not be reaching @Frontend |
| AP-010 (hardcoded text) | 1 | 1 | First occurrence — logged |

## Mistake Prevention Status
New error patterns logged this run: 3
Patterns matching existing AP: 3 (100% — no new patterns discovered)
AP-001 recurrence flagged to @ErrorDetective ⚠️

## Auto-Fixable (3 of 4 violations)
Run: /quality all --fix to apply corrections

## Decision
Score: 94% → ✅ PASS (deploy permitted)
Blocker: None
Recommendation: Fix AP-010 violation before next sprint (requires @Content)
```

---

## /quality mistakes — Mistake Prevention Report

Dedicated subcommand for mistake pattern health:

```markdown
### @ErrorDetective — Quality Mistake Report
Date: YYYY-MM-DD | Sprint: [N] | Period: [start → today]

## Anti-Pattern Registry Health
Total AP entries: [N]
CRITICAL: [N] | HIGH: [N] | MEDIUM: [N]
New this sprint: [N] | Retired this sprint: [N]

## AP Injection Effectiveness
| AP-ID | Description | Injected | Violations Caught | Prevented | Effectiveness |
|-------|-------------|---------|-------------------|-----------|--------------|
| AP-001 | Directional CSS | 24 tasks | 1 quality violation | 23 | 96% ✅ |
| AP-010 | Hardcoded text | 18 tasks | 2 quality violations | 16 | 89% ⚠️ |
| AP-020 | Unbounded queries | 12 tasks | 0 violations | 12 | 100% ✅ |
| AP-041 | Missing Zod | 15 tasks | 0 violations | 15 | 100% ✅ |

## Recurring Violations (needs attention)
| AP-ID | Occurrences | Agent | Action Required |
|-------|------------|-------|----------------|
| AP-001 | 3 this sprint | @Frontend | @KnowledgeSynthesizer: add Hard Rule to frontend.md |

## Error Pattern Log (this sprint)
| EP-ID | Pattern | Agent | Promoted to AP | Tokens Wasted |
|-------|---------|-------|---------------|--------------|
| EP-001 | Directional CSS | @Frontend | AP-001 (existing) | ~800 |
| EP-002 | Hardcoded string | @Frontend | AP-010 (existing) | ~400 |

## Tokens Saved by Mistake Prevention This Sprint
Errors caught by AP injection (prevented code generation): [N]
Estimated tokens saved: ~[N] (vs fixing post-generation)

## Recommendations
1. AP-001 recurring in @Frontend: @KnowledgeSynthesizer → add Hard Rule to frontend.md definition
2. AP-010 effectiveness 89%: review injection timing — may need pre-flight reinforcement
3. Consider adding visual test for RTL icon direction (no AP covers this yet)
```

---

## Error Capture on Violation Found

**Every violation discovered by `/quality` is captured immediately:**

```markdown
## Violation → Error Pattern Flow

When a quality gate finds a violation:

1. CLASSIFY the violation:
   - Which AP-ID matches? (SOURCE_AP)
   - Is it genuinely new? (SOURCE_NEW)

2. LOG to .ai/memory/error-patterns.md:
   --- ERROR CAPTURE ---
   Date: [YYYY-MM-DD]
   Source: /quality [gate] run
   Agent: @[agent that introduced the violation]
   Task type: [component | api-route | migration | etc.]
   Domain: [affected domain]
   Severity: [CRITICAL | HIGH | MEDIUM | LOW]
   Pattern type: [AP-ID if SOURCE_AP | new type if SOURCE_NEW]

   Error: [exact violation description + file:line]
   Root Cause: Why did the injected constraint not prevent this?
   Fix Applied: [auto-fix applied or manual fix required]
   Tokens wasted: [estimate for fix]
   Prevention note: [what would make the AP injection more effective?]
   ---

3. CHECK recurrence:
   - Is this the 2nd+ time this AP-ID has been violated this sprint?
     YES → @ErrorDetective recurrence alert
          → @KnowledgeSynthesizer: update affected agent Hard Rules section
          → Consider raising severity of the AP entry
   - Is this a SOURCE_NEW pattern that appeared before?
     2+ times → @KnowledgeSynthesizer promotes to new AP entry

4. NOTIFY if CRITICAL:
   - @Guide (sprint status update)
   - @EscalationHandler (if violation blocks deploy)
```

---

## /quality --fix Behavior

```markdown
## Auto-Fix Protocol

When --fix is passed:

For each auto-fixable violation:
1. @Reviewer applies the fix (minimal change — only the violation)
2. Re-runs the specific gate to confirm fix resolved the violation
3. Does NOT refactor surrounding code
4. Does NOT add functionality
5. Logs the fix to command audit log

After all auto-fixes:
  Re-run /quality all (without --fix) to confirm score improved
  If score still below threshold: list remaining manual fixes

Auto-fixable examples:
  margin-left → margin-inline-start (CSS logical swap)
  padding-right → padding-inline-end
  ml-4 (Tailwind) → ms-4
  mr-4 → me-4
  #2D3748 → var(--color-surface-secondary) [best-match token suggestion]

Never auto-fixed (require agent + human review):
  Hardcoded strings (semantic context needed for correct i18n key)
  Missing contract validation (architectural decision)
  Security violations (require @Security assessment)
  Missing auth middleware (require @Backend + @Security review)
```

---

## Gate Failure Decision Matrix

| Gate | Score | Action |
|------|-------|--------|
| spec:validate | Any FAIL | BLOCK — clarify spec and AC with @Architect |
| contract:auto-validate | Any FAIL | BLOCK — fix Zod / locks / Data Shape alignment |
| compliance | <80% | BLOCK merge — list all violations, run --fix |
| compliance | 80–89% | WARN — fix before next sprint |
| compliance | ≥90% | PASS (with violations logged for next sprint) |
| security:scan | Any CRITICAL/HIGH | BLOCK deploy — @Security leads fix |
| security:scan | MEDIUM only | PASS — schedule fix in next sprint |
| test | Coverage drop | BLOCK merge — @QA adds missing tests |
| test | All pass, coverage OK | PASS |
| build | Any error | BLOCK — @Debugger leads root cause |

---

## Token Efficiency of Running /quality

```
Without /quality (discover violations in production or code review):
  Average cost per violation: 2,000–8,000 tokens (context reload + fix + review cycle)

With /quality (catch at gate):
  Average cost per violation: 200–400 tokens (fix at point of discovery, no reload)

With /quality + AP pre-scan (catch before gate):
  Average cost per violation: 50–150 tokens (injection prevents it from being written)

ROI of running /quality after every /build: 5–40× token savings per sprint
```

---

## Execution Log

Every `/quality` run is logged to `.ai/plans/active/audit/command-logs/YYYY-MM-DD.md`:

```
[YYYY-MM-DD HH:MM] /quality all
  AP pre-scan: 53 APs checked | 3 candidate violations pre-identified
  Gate 1 spec:validate: PASS
  Gate 2 contract:auto-validate: PASS
  Gate 3 compliance: PASS (94%) — 3 violations, 2 auto-fixable
  Gate 4 security:scan: PASS
  Gate 5 test: PASS (91% coverage)
  Gate 6 build: PASS
  Error capture: EP-001, EP-002, EP-003 written to error-patterns.md
  AP-001 recurrence flagged: 3rd occurrence this sprint → @KnowledgeSynthesizer
  Result: PASS | Score: 94% | Violations: 3 (2 auto-fixed, 1 queued)
```

---

*Invokes: @Reviewer, @Security, @DesignSystem, @Content, @QA, @ErrorDetective, @KnowledgeSynthesizer*
*Skills: mistake-prevention-system, pre-flight-checklist, hallucination-containment, owasp-zero-trust-architecture*
*Reports to: @MetricsAgent (compliance score trend)*
