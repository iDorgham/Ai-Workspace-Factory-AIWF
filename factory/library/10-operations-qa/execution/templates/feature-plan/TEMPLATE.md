# Feature Plan: [Feature Name]

> **Created:** [YYYY-MM-DD]
> **Created by:** @Architect
> **Status:** [planning | approved | in-progress | complete | archived]
> **Priority:** [critical | high | medium | low]
> **Sprint:** [Sprint N]

---

## 1. Overview

**Feature ID:** `[SPRINT-N]-[slug]`
**User Story:** As a [user type], I want to [action] so that [benefit].
**Business Value:** [Why this matters — revenue, retention, compliance, user satisfaction]

---

## 2. Acceptance Criteria (Gherkin)

```gherkin
Feature: [Feature Name]

  Scenario 1: [Primary happy path]
    Given [precondition]
    When [user action]
    Then [expected outcome]

  Scenario 2: [Alternative path]
    Given [precondition]
    When [user action]
    Then [expected outcome]

  Scenario 3: [Error/edge case]
    Given [precondition]
    When [user action]
    Then [expected error handling]
```

---

## 3. Technical Design

### 3.1 Contracts Required
| Contract | Status | File |
|----------|--------|------|
| [Domain]Schema | [pending | locked] | `packages/shared/src/contracts/[domain].ts` |

### 3.2 Components/Files to Create
| File | Type | Purpose |
|------|------|---------|
| `apps/web/src/components/[Name].tsx` | Component | [Description] |
| `apps/api/src/routes/[name].ts` | Route | [Description] |
| `apps/api/src/services/[name].service.ts` | Service | [Description] |
| `tests/[name].test.ts` | Test | [Description] |

### 3.3 Database Changes
```prisma
// schema.prisma changes
model [ModelName] {
  // ...
}
```

**Migration Strategy:** Expand → Backfill → Contract (zero-downtime)

### 3.4 Dependencies
- **Internal:** [List internal packages/components this depends on]
- **External:** [List new npm packages — must go through pnpm catalog]

---

## 4. Implementation Plan

### Step 1 — Contract Creation
- [ ] Create Zod schema in `packages/shared/src/contracts/[domain].ts`
- [ ] Create/update/create partials (Create, Update, Query schemas)
- [ ] Run `/contract lock [domain]`
- **Agent:** @Architect | **Contract:** `[domain].ts`

### Step 2 — Database Migration (if applicable)
- [ ] Write Prisma migration (expand phase)
- [ ] Test migration on staging data
- [ ] Write backfill migration (idempotent)
- [ ] Write constraint migration (contract phase)
- **Agent:** @DBA | **Contract:** `[domain].ts`

### Step 3 — Backend Implementation
- [ ] Create route handler with Zod validation
- [ ] Create service layer with business logic
- [ ] Write unit + contract tests
- **Agent:** @Backend | **Contract:** `[domain].ts`

### Step 4 — Frontend Implementation
- [ ] Create components using design tokens
- [ ] Implement form with Zod resolver
- [ ] Add i18n keys for all user-facing text
- [ ] Add a11y attributes (aria-*, keyboard nav, focus)
- **Agent:** @Frontend | **Contract:** `[domain].ts`

### Step 5 — Testing & Quality Gates
- [ ] Unit tests pass (coverage ≥ target)
- [ ] Integration/contract tests pass
- [ ] E2E test for happy path
- [ ] Visual regression baselines captured (EN + AR)
- [ ] `compliance` passes
- [ ] Security scan passes
- **Agent:** @QA + @VisualQA + @Security

### Step 6 — Review & Merge
- [ ] @Reviewer approval (no architectural drift)
- [ ] @DesignSystem approval (token compliance)
- [ ] @BrandGuardian approval (brand grammar, if applicable)
- [ ] All gates pass in CI
- **Agent:** @Reviewer

---

## 5. Risk Assessment

| Risk | Likelihood (1-5) | Impact (1-5) | Score | Mitigation |
|------|------------------|--------------|-------|------------|
| [Risk description] | [N] | [N] | [L×I] | [Mitigation strategy] |

**Overall Risk Score:** [Low | Medium | High | Critical]
**Assessed by:** @RiskAgent

---

## 6. Definition of Done

- [ ] Spec confirmed (User Story, testable AC, Data Shape, Edge Cases) — `spec:validate`
- [ ] Contract exists and is locked — `contract:auto-validate`
- [ ] All acceptance criteria met (Gherkin scenarios pass)
- [ ] Zod + locks pass CI / `contract:validate` task if present (implements `contract:auto-validate`)
- [ ] Code passes `compliance` (tokens, a11y, i18n, RTL)
- [ ] Code passes `security:scan` (zero critical/high findings)
- [ ] All tests pass (unit + integration + E2E + visual)
- [ ] Build passes with no TypeScript errors
- [ ] @Reviewer + @BrandGuardian (if applicable) approved
- [ ] Deployed to staging and verified
- [ ] Documentation updated (if applicable)

---

## 7. Audit Trail

| Date | Step | Agent | Action | Status |
|------|------|-------|--------|--------|
| [YYYY-MM-DD] | 1.0 | @Architect | Feature plan created | ✅ |
| | | | | |

---

*Template Version: 1.0 | Maintained by: @Architect | Used by: All execution agents*
