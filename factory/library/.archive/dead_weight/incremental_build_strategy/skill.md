---
type: Generic
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# Incremental Build Strategy

## Purpose
Prevent agents from regenerating code that already exists, re-running tasks already completed, or overlapping with other agents' work. Build only the delta. Spend tokens only where value is created.

---

## The Diff-First Principle

Before writing any code, determine what already exists:

```markdown
## Diff-First Protocol

For every /build or code generation task:

Step 1 — INVENTORY existing artifacts
  Check for each expected output:
  - Does the file exist? (filesystem check)
  - Is the component already in packages/ui?
  - Is the route already in apps/api?
  - Is the test already in __tests__/?
  - Is the migration already in prisma/migrations/?

Step 2 — CLASSIFY each artifact as:
  - EXISTS_COMPLETE    → skip entirely (0 tokens)
  - EXISTS_PARTIAL     → update only the missing parts
  - EXISTS_STALE       → contract changed, must regenerate affected sections only
  - MISSING            → create fresh

Step 3 — OUTPUT only the delta
  Agent generates ONLY what's in MISSING + EXISTS_PARTIAL + EXISTS_STALE
  Agent NEVER touches EXISTS_COMPLETE items

Step 4 — LOG what was skipped
  Include in output: "Skipped: [list of existing items]" so @Reviewer knows
```

---

## File Existence Check Pattern

```markdown
## Before creating any file, run this mental check:

"Does [file path] already exist in the filesystem?"
  YES → Read it first, then determine if update is needed
  NO  → Create fresh

"Does [component name] already exist in packages/ui/src/components/?"
  YES → Import from there instead of creating duplicate
  NO  → Create in packages/ui (never in apps/)

"Does [API route] already exist in apps/api/src/routes/?"
  YES → Extend it, don't duplicate
  NO  → Create new route file

"Does [test describe block] already cover this behavior?"
  YES → Add missing assertions, don't rewrite the whole test
  NO  → Create new test
```

---

## Turborepo-Aware Incremental Building

```typescript
// turbo.json — only rebuild what changed
{
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": [".next/**", "dist/**"],
      "inputs": ["src/**", "package.json", "tsconfig.json"]
      // Turbo hashes inputs — if unchanged, uses cache. Agents should know this.
    },
    "test": {
      "dependsOn": ["build"],
      "outputs": ["coverage/**"],
      "inputs": ["src/**", "__tests__/**"]
      // Only re-test if src or tests changed
    },
    "lint": {
      "outputs": [],
      "inputs": ["src/**", ".eslintrc*"]
      // Only re-lint if source changed
    }
  }
}
```

```markdown
## @Router Turborepo Awareness

Before routing a build task, check:
1. Which packages changed since last successful build? (git diff --name-only HEAD~1)
2. Which Turborepo tasks need to re-run? (turbo run build --dry-run)
3. Route ONLY to agents responsible for changed packages

Example:
  Changed: apps/web/src/components/BookingCard.tsx
  → @Frontend (update component) ✅
  → @QA (re-run visual test for BookingCard) ✅
  → @Backend (NO CHANGE — API unchanged) ❌ skip
  → @DBA (NO CHANGE — DB unchanged) ❌ skip

Token saving: ~60% of agent invocations skipped when only one package changed
```

---

## Stale Contract Detection

```markdown
## When a contract changes (after /contract lock with version bump):

1. @ContractLock emits: "booking.ts changed from v1.2 → v1.3, breaking fields: [pricePerNight renamed to baseRate]"

2. @Router determines what's stale:
   - All files that import from contracts/booking.ts → stale
   - All tests that use booking contract fields → stale
   - All API routes that return booking objects → stale
   - All UI components that display booking data → stale

3. Diff the stale items:
   - Only the changed fields matter (pricePerNight → baseRate)
   - Find every occurrence in stale files
   - Route to agents for targeted find-and-update (not full regeneration)

4. Result: instead of "rebuild booking feature" (15,000 tokens)
   → "Update 3 files: rename pricePerNight → baseRate" (~2,000 tokens)
```

---

## Component Reuse Check (Before Building UI)

```markdown
## @Frontend Component Decision Tree

Before building any UI component:

1. Does it exist in packages/ui/src/components/? → IMPORT, don't build
2. Does shadcn/ui have it? → npx shadcn@latest add [component], don't build
3. Is it a composition of existing components? → COMPOSE, don't build custom
4. Is it truly new and project-specific? → BUILD in packages/ui, not apps/web

Result: most "new" features actually reuse 70–80% of existing components.
Agents that don't check first regenerate existing work → wasted tokens.
```

---

## Test Coverage Gap Detection (Instead of Full Rewrite)

```markdown
## @QA Incremental Test Strategy

Before writing tests:
1. Run: what test coverage exists for [feature]?
2. Check: which specific behaviors are NOT covered?
3. Write: ONLY tests for uncovered behaviors

Report format:
  Existing coverage: 78% (BookingForm unit, API route integration)
  Missing: visual regression tests for BookingCard RTL layout
  Action: Add visual test for RTL — don't rewrite existing unit tests

Token saving: writing 2 missing tests vs rewriting 20 existing ones
```

---

## Migration Incremental Safety

```markdown
## @DBA Incremental Migration Protocol

Before creating a migration:
1. Check prisma/migrations/ — has this schema change been started?
2. Check .ai/plans/active/ — is a migration for this domain planned already?
3. If migration exists and partially applied:
   - DON'T create a new migration for the same change
   - Diagnose why the existing one didn't complete
   - Fix the existing migration or rollback it cleanly

This prevents: duplicate migration entries that conflict on merge
```

---

## Parallel Agent Deduplication

During `/swarm` parallel execution:

```markdown
## Deduplication Protocol (@Router)

Before assigning parallel tasks:
1. Check: will @Frontend and @Backend both try to modify the same shared file?
   (e.g., both touching types/index.ts or a shared utility)
   → If YES: one modifies, other reviews — not both modifying

2. Check: will @QA write tests that overlap with stubs @Frontend creates?
   → Coordinate: @Frontend stubs, @QA fills — no overlap

3. Check: will @Backend and @DBA both try to modify the Prisma schema?
   → ALWAYS sequential: @DBA first, @Backend second (depends on migration)

These checks prevent merge conflicts that cost 3,000–8,000 tokens to resolve.
```

---

## Output Format — Incremental Build Report

```markdown
## @[AgentName] — Incremental Build Report
**Feature:** [name] | **Date:** YYYY-MM-DD

### Inventory Results
| Artifact | Status | Action |
|---------|--------|--------|
| BookingCard.tsx | EXISTS_COMPLETE | Skipped ✓ |
| BookingForm.tsx | EXISTS_PARTIAL | Updated 3 fields |
| booking.test.ts | EXISTS_STALE | Updated for v1.3 contract |
| BookingPage.tsx | MISSING | Created fresh |
| visual.spec.ts | MISSING | Created fresh |

### Skipped (already complete)
- BookingCard.tsx (no changes since last build)
- BookingList.tsx (unaffected by contract v1.3 change)

### What was built (delta only)
- BookingForm.tsx: added `baseRate` field (renamed from `pricePerNight`)
- booking.test.ts: updated 4 assertions for new field name
- BookingPage.tsx: new route page
- visual.spec.ts: new visual regression tests

**Token efficiency:** Built 2 files, updated 2 files, skipped 2 files
**Estimated saving vs full rebuild:** ~5,200 tokens
```

## 🌍 Regional Calibration (MENA Context)

- **Cultural Alignment:** Ensure all logic respects regional business etiquette and MENA market expectations.
- **RTL Compliance:** Logic must explicitly handle Right-to-Left (RTL) flow where relevant.

## 🛡️ Critical Failure Modes (Anti-Patterns)

- **Anti-Pattern:** Generic Output -> *Correction:* Apply sector-specific professional rules from RULE.md.
- **Anti-Pattern:** Global-Only Logic -> *Correction:* Verify against MENA regional calibration.

---

## Success Criteria
- [ ] Inventory check runs before every code generation task
- [ ] No file created without first checking if it exists
- [ ] No component built if it exists in packages/ui
- [ ] No test rewritten if coverage already exists for that behavior
- [ ] Stale contract fields traced to specific files (not whole feature)
- [ ] @Router deduplication prevents parallel agent file conflicts
- [ ] Build report includes skip list for @Reviewer visibility