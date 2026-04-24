---
type: Command
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---


# /build — Code Generation & Implementation

## Syntax
```
/build feature [name]           → Build a complete feature (all layers)
/build component [name]         → Build a UI component
/build api [endpoint]           → Build an API route + service
/build migration [name]         → Build a DB migration
/build design-system            → Generate component library from tokens
/build [name] --dry-run         → Preview what would be generated (no files written)
/build [name] --parallel        → Run @Frontend + @Backend simultaneously
/build [name] --scope web|api   → Target specific app only
```

## Primary Agents
`@Guide` (orchestrates) → `@Router` (distributes) → `@Frontend` + `@Backend` + `@DBA` (implement) → `@QA` (tests)

---

## Phase 0 — Mistake Prevention (runs before everything else)

This phase is mandatory. It cannot be skipped. It is the single most effective token-saving step.

### Step 0-A: Anti-Pattern Scan (@ContextSlicer)
```
Load: .ai/memory/anti_patterns.md
Filter: entries matching → current agent type + build type + domain
Inject: matched constraints into ALL agent contexts before task assignment
Block: any CRITICAL anti-pattern triggers human confirmation before proceeding

Output: constraint list prepended to every agent's context slice
See: .ai/skills/mistake_prevention_system.md (Layer 1) + .ai/skills/lesson_injection.md
```

### Step 0-B: Inventory Check (@Router via incremental_build_strategy.md)
```
Before routing any build task:

For each expected output file:
  EXISTS_COMPLETE  → skip entirely (0 tokens)
  EXISTS_PARTIAL   → route only the missing parts
  EXISTS_STALE     → contract changed — route targeted find-and-update only
  MISSING          → create fresh

Also check:
  - Does this component exist in packages/ui? → import, don't rebuild
  - Does shadcn/ui have this component? → add, don't build
  - Which files are stale due to contract version bump?

Result: @Router assigns ONLY the delta — not a full regeneration
See: .ai/skills/incremental_build_strategy.md
```

### Step 0-C: Context Compression (@ContextSlicer)
```
For each assigned agent, build a compressed context slice:
  - Architecture subset (not full file) — 80–90% size reduction
  - Contract: task-relevant fields only (not full schema)
  - Memory: domain-matched, recency-filtered lessons only
  - Skills: pointer notation for skills not directly activated

Target: ≤4,000 tokens for Execution agents | ≤2,000 for Coordination
See: .ai/skills/context_compression.md
```

---

## Phase 1 — Pre-Build Gate (mandatory before code generation)

`@Guide` verifies all gates. Any FAIL blocks the build immediately.

```
Gate 1: Anti-pattern scan completed? (Phase 0-A done)
Gate 2: Inventory check done? (Phase 0-B done)
Gate 3: Contract exists? packages/shared/src/contracts/[domain].ts
Gate 4: Contract LOCKED? (@ContractLock confirms lock state = TRUE)
Gate 5: Feature plan exists? .ai/plans/active/features/[name].md
Gate 6: DMP loaded? (8 steps — Step 0 mandatory)
Gate 7: No active blockers in .ai/plans/active/tasks/?
Gate 8: Per-agent pre-flight checklist ready? (see .ai/skills/pre_flight_checklist.md)

If ANY gate FAILS → build blocked, fix path provided, @EscalationHandler notified if CRITICAL
```

### Per-Agent Pre-Flight (each agent runs its own before starting)
```
@Frontend:  CSS logical props? | i18n keys? | tokens only? | aria? | shadcn check?
@Backend:   Zod validation? | auth middleware? | take: on queries? | error handling?
@DBA:       Rollback SQL? | CONCURRENTLY index? | expand-backfill-contract pattern?
@QA:        Coverage gaps identified? | contract fields exercised? | EN + AR locales?

See: .ai/skills/pre_flight_checklist.md (agent-specific sections)
```

---

## Phase 2 — Build Execution

### /build feature [name]

Full-stack implementation. Follows D-CDD (Design → Contract → Develop → Deliver) sequence.

```
Step 1 — Stub (with locked contract):
  @Backend: Create route stubs returning contract-shaped mock data
  @Frontend: Create components consuming contract types
  [PARALLEL — both can stub simultaneously with same locked contract]

Step 2 — Test-first:
  @QA: Write unit + contract tests against stubs
  [Acceptance criteria from feature plan → Gherkin → test scaffolds]

Step 3 — Implement (with injected constraints active):
  @Backend: Implement real business logic in service layer
    → Constraint: every input validated with Zod (AP-041)
    → Constraint: every findMany has take: limit (AP-020)
    → Constraint: auth middleware on all non-public routes (AP-042)
  @Frontend: Implement real UI
    → Constraint: CSS logical properties only (AP-001)
    → Constraint: all text via t('key') (AP-010)
    → Constraint: all colors/spacing via tokens (AP-002/003)
  @DBA: Generate Prisma schema + migration (if new data)
    → Constraint: rollback SQL required (AP-021)
    → Constraint: CONCURRENTLY on index creation (AP-023)
    → Constraint: expand-backfill-contract for live tables (AP-022)

Step 4 — Validate:
  @QA: Run full test suite (unit + integration + E2E)
  @DesignSystem: Token audit + a11y + RTL check
  @VisualQA: Capture visual regression baselines (EN + AR viewports)

Step 5 — Review:
  @Reviewer: Final review against contract + architecture + anti-patterns
  @Automation: /commit + /push + PR creation
```

### /build component [name]

```
@Frontend — inventory check first:
  ✓ Does it exist in packages/ui/src/components/? → import, stop here
  ✓ Does shadcn/ui have it? → npx shadcn@latest add [name], stop here
  ✓ Is it a composition? → compose from existing components, stop here
  → Only build fresh if none of the above apply

If building fresh, generate to packages/ui (never to apps/):
  packages/ui/src/components/[Name]/
    ├── [Name].tsx          (component implementation)
    ├── [Name].test.tsx     (unit + visual tests)
    └── index.ts            (re-export)

Per-component checklist (auto-applied from pre-flight):
  ✅ Props typed from locked contract (z.infer<typeof Schema>)
  ✅ No raw hex/px — CSS variables only
  ✅ No hardcoded text — t('key') only
  ✅ CSS logical properties (ms-/me-/ps-/pe-)
  ✅ ARIA attributes (aria-label, aria-describedby, role)
  ✅ Loading + error + empty states implemented
  ✅ Works in both EN (LTR) and AR (RTL) without code changes
```

### /build api [endpoint]

```
@Backend — inventory check first:
  ✓ Does the route file already exist? → read before editing, not overwriting
  ✓ Does the service already exist? → extend, don't duplicate

Generate:
  apps/api/src/routes/[domain].routes.ts    (Hono route handlers)
  apps/api/src/services/[domain].service.ts (business logic)

Per-endpoint checklist (auto-applied from pre-flight):
  ✅ zValidator('json', DomainSchema) on every mutation route
  ✅ authMiddleware on every non-public route (document public routes explicitly)
  ✅ take: [default 20] on every findMany query
  ✅ Typed service layer (return types match contract)
  ✅ Error handling: AppError with status codes
  ✅ Structured logging (no sensitive field logging)
  ✅ Rate limiting on auth + public endpoints
  ✅ Integration test file generated alongside route
```

### /build migration [name]

```
@DBA — inventory check first:
  ✓ Has this migration been started already? (check prisma/migrations/)
  ✓ Is a migration for this domain already planned? (check .ai/plans/active/)
  → If partially applied: diagnose why — don't create a duplicate

Generate (using expand-backfill-contract pattern):
  prisma/migrations/[timestamp]_[name]/migration.sql

Required structure:
  -- UP: expand (nullable column) → application code deployed → backfill → contract (NOT NULL)
  -- DOWN: rollback SQL — required, not optional
  -- CONCURRENTLY: on all new indexes
  -- Estimated rows affected: [N] (helps @DBA assess risk)

@DBA signs off before @Backend writes code depending on schema
```

### /build design-system

```
1. @DesignSystem reads packages/ui/src/lib/styles/tokens.css
2. Generates base components (Button, Input, Card, Badge, Modal, Table, etc.)
3. Each component: tokens only, a11y ready, RTL ready, i18n ready
4. @VisualQA captures baselines (3 viewports × 2 locales = 6 baseline sets per component)
5. All exports via packages/ui/src/index.ts
```

---

## Phase 3 — On Failure (Error Capture Protocol)

**When any build step fails:**

```
Step 1 — STOP: don't continue building on a broken step
Step 2 — Route to @Debugger:
  @Debugger reads the error, diagnoses root cause (6-step protocol)
  Does NOT refactor, does NOT add features, fixes ONLY the specific failure
Step 3 — @ErrorDetective captures:
  Writes to .ai/memory/error_patterns.md (standard capture format)
  Checks: is this the 2nd occurrence of this pattern?
    YES → promote to .ai/memory/anti_patterns.md immediately
    NO  → log and monitor
Step 4 — Fix applied → re-run from the failed step (not from start)
Step 5 — @Guide updates plan step status and logs to audit
```

**Never:**
- Retry the exact same approach after a failure without understanding the root cause
- Silence TypeScript errors with `any` or `@ts-ignore`
- Bypass contract validation to unblock a build
- Skip error capture to "save time" (costs more tokens on recurrence)

---

## --dry-run Output

```markdown
### @Guide — Build Preview (dry-run): [feature-name]

## Phase 0 — Mistake Prevention
Anti-pattern scan: 4 constraints injected (2 CRITICAL, 2 HIGH)
  AP-001: CSS logical props enforced for @Frontend
  AP-020: take: required on all @Backend queries
  AP-010: t('key') required for all UI text
  AP-041: Zod validation required at all API boundaries

Inventory check:
  EXISTS_COMPLETE  (skip): BookingCard.tsx, booking.test.ts
  EXISTS_PARTIAL   (update): BookingForm.tsx (missing baseRate field from v1.3)
  EXISTS_STALE     (retarget): booking.service.ts (contract v1.2→v1.3 drift)
  MISSING          (create): BookingPage.tsx, visual.spec.ts

Delta — what will actually be built:
  MOD  apps/web/src/components/BookingForm.tsx     (+8 lines — baseRate field)
  MOD  apps/api/src/services/booking.service.ts    (+2 lines — field rename)
  NEW  apps/web/src/app/bookings/page.tsx          (~60 lines)
  NEW  apps/web/src/__tests__/visual.spec.ts       (~40 lines)
  MOD  prisma/schema.prisma                        (+5 lines — new field)

Skipped (already complete):
  BookingCard.tsx, booking.test.ts, BookingList.tsx

## Quality gates that WILL run:
  spec:validate → contract:auto-validate → compliance → security:scan → test → build

## Token estimate (with compression):
  Context loading: ~890 tokens (vs ~2,935 raw — 70% saved)
  Code generation: ~3,200 tokens (delta only — vs ~9,400 full regeneration)
  Total: ~4,090 tokens | Full rebuild would cost: ~12,335 tokens
  Efficiency: 67% token saving

Risk score: 6/25 (Low) — no blockers, anti-patterns contained

Proceed? Run: /build [name] (without --dry-run)
```

---

## Execution Log

Every `/build` run is logged to `.ai/plans/active/audit/command-logs/YYYY_MM_DD.md`:

```
[YYYY-MM-DD HH:MM] /build [name]
  Phase 0: AP scan (4 matched) | Inventory (2 skip, 1 update, 2 create) | Context: 890 tokens
  Phase 1: All gates PASS
  Phase 2: @Frontend (BookingForm update, BookingPage new) | @Backend (service update) | @QA (visual spec)
  Phase 3: No failures
  Result: SUCCESS | Tokens used: 4,090 | Skipped: 2 files
```

---

*Invokes: @Guide, @Router, @ContextSlicer, @ErrorDetective, @Debugger, @Frontend, @Backend, @DBA, @QA, @DesignSystem, @Reviewer, @Automation*
*Skills: mistake-prevention-system, pre-flight-checklist, context-compression, incremental-build-strategy, lesson-injection, hallucination-containment*
