# Architecture Decision Record: [Decision Title]

> **ADR ID:** `adr-[NNN]`
> **Status:** [proposed | accepted | deprecated | superseded]
> **Date:** [YYYY-MM-DD]
> **Author:** @AgentName
> **Reviewers:** @Architect, @Reviewer
> **Supersedes:** `adr-[NNN]` (if applicable)

---

## 1. Context

**What is the issue?**
[Describe the architectural decision that needs to be made]

**Why is this important?**
[Impact on codebase, team, performance, security, or maintainability]

**Constraints:**
- [Constraint 1 — e.g., "Must support Arabic RTL"]
- [Constraint 2 — e.g., "Must maintain zero-downtime deployments"]
- [Constraint 3 — e.g., "Must comply with contract-first principle"]

---

## 2. Decision

**We have decided to:**
[Clear statement of the chosen approach]

**Rationale:**
[Why this option over alternatives — reference data, benchmarks, or experiments]

---

## 3. Options Considered

| Option | Pros | Cons | Score |
|--------|------|------|-------|
| [Option A] | [List] | [List] | [N/10] |
| [Option B] | [List] | [List] | [N/10] |
| [Option C] | [List] | [List] | [N/10] |

---

## 4. Implications

### Positive
- [Benefit 1]
- [Benefit 2]

### Negative / Trade-offs
- [Trade-off 1 — and why it's acceptable]
- [Trade-off 2]

### Required Changes
- [File/directory to create]
- [File/directory to modify]
- [File/directory to delete]

---

## 5. Migration Plan

**If this ADR requires migration:**
```
Step 1: [Action] — Agent: @AgentName
Step 2: [Action] — Agent: @AgentName
Step 3: [Action] — Agent: @AgentName
```

**Rollback plan:**
[How to undo this decision if it fails]

---

## 6. Compliance

- [ ] Aligns with Sovereign architecture principles ✅ / ❌
- [ ] No contract violations ✅ / ❌
- [ ] No design token violations ✅ / ❌
- [ ] Security review completed ✅ / ❌
- [ ] Performance impact assessed ✅ / ❌

---

## 7. Approval

| Agent | Status | Date | Comments |
|-------|--------|------|----------|
| @Architect | [approved | rejected] | [YYYY-MM-DD] | [Notes] |
| @Reviewer | [approved | rejected] | [YYYY-MM-DD] | [Notes] |
| @Security | [approved | rejected | N/A] | [YYYY-MM-DD] | [Notes] |

**ADR Status:** [accepted | rejected | superseded]
**Effective date:** [YYYY-MM-DD]

---

## 8. Links

- Feature plan: `.ai/plans/active/features/[name].md`
- Related contracts: `packages/shared/src/contracts/[domain].ts`
- Related code: [file paths]
- External references: [URLs if applicable]

---

*Template Version: 1.0 | Maintained by: @Architect | All significant architectural decisions must be recorded*
