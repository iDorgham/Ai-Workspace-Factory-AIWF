---
type: Generic
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# Task: [Task Name]

> **Task ID:** `[SPRINT-N]-[feature-slug]-[step]`
> **Feature:** [Feature name — link to feature plan]
> **Assigned to:** @AgentName
> **Status:** [pending | in-progress | blocked | complete | archived]
> **Priority:** [critical | high | medium | low]
> **Estimated effort:** [S | M | L | XL]

---

## 1. Task Description

**What needs to be done:**
[Clear, concise description of the work required]

**Why this matters:**
[Context — how this fits into the larger feature/sprint]

---

## 2. Prerequisites

- [ ] Contract locked: `packages/shared/src/contracts/[domain].ts` ✅ / ❌
- [ ] Active plan loaded: `.ai/plans/active/features/[feature].md` ✅ / ❌
- [ ] Dependencies completed: [List task IDs]
- [ ] Dynamic Memory Protocol executed (7-step load sequence) ✅ / ❌

---

## 3. Acceptance Criteria

- [ ] [Criterion 1 — specific, testable]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

---

## 4. Implementation Details

### Files to Create/Modify
| File Path | Action | Purpose |
|-----------|--------|---------|
| `packages/shared/src/contracts/[domain].ts` | Create/Update | [Description] |
| `apps/web/src/components/[Name].tsx` | Create | [Description] |
| `apps/api/src/routes/[name].ts` | Create | [Description] |
| `tests/[name].test.ts` | Create | [Description] |

### Code Patterns to Follow
```typescript
// Reference correct patterns (from coding_standards.md)
// e.g., Zod validation, component structure, service layer pattern
```

### Design Tokens to Use
```css
/* Reference tokens from packages/ui/src/lib/styles/tokens.css */
/* e.g., --color-primary, --spacing-lg, --text-heading-md */
```

### i18n Keys to Add
```json
{
  "namespace": {
    "key": "English text value"
  }
}
```

---

## 5. Quality Checklist

- [ ] Contract validated and locked
- [ ] No raw values (hex, px, strings — all tokens/i18n)
- [ ] RTL support (CSS logical properties)
- [ ] Accessibility (aria-*, keyboard nav, focus, contrast)
- [ ] TypeScript strict (no `any`, no `!` without comment)
- [ ] Tests written (unit + integration as appropriate)
- [ ] No secrets/tokens in code
- [ ] No `console.log` in production code
- [ ] `compliance` passes

---

## 6. Dependencies & Blockers

| Dependency | Status | Notes |
|------------|--------|-------|
| [Task ID or external dependency] | [pending | complete | blocked] | [Details] |

**Current blockers:** [List or "none"]
**Escalation needed:** [Yes/No — if yes, file SBAR escalation]

---

## 7. Execution Log

| Timestamp | Action | Agent | Result |
|-----------|--------|-------|--------|
| [YYYY-MM-DD HH:MM] | [What was done] | @Agent | [success | failed | partial] |
| | | | |

---

## 8. Completion Sign-Off

**Task completed:** [YYYY-MM-DD HH:MM]
**Completed by:** @AgentName
**Tests passing:** ✅ / ❌
**Quality gates passing:** ✅ / ❌
**Next task in feature:** [Task ID — or "none, feature complete"]

**Reviewer notes:** [Any follow-up actions or observations]

---

*Template Version: 1.0 | Maintained by: @Guide | Used by: All execution agents*
