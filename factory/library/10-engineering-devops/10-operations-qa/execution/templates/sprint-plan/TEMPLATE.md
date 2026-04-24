---
type: Generic
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# Sprint Plan: Sprint [N]

> **Sprint ID:** `sprint-[N]`
> **Start Date:** [YYYY-MM-DD]
> **End Date:** [YYYY-MM-DD]
> **Sprint Goal:** [One sentence — what success looks like]
> **Status:** [planning | active | review | complete]

---

## 1. Sprint Goal

**Objective:** [What we're delivering this sprint]
**Business Impact:** [Why this sprint matters — revenue, user value, compliance]
**Success Metrics:** [How we measure success — velocity, compliance score, features delivered]

---

## 2. Capacity & Resources

| Agent/Role | Availability | Assigned Features |
|------------|--------------|-------------------|
| @Architect | [Full | Partial] | Contract design, architecture |
| @Backend | [Full | Partial] | [Feature list] |
| @Frontend | [Full | Partial] | [Feature list] |
| @DBA | [Full | Partial] | [Migration list] |
| @QA | [Full | Partial] | Test suites, coverage |
| @Security | [Full | Partial] | Security audits |
| @Reviewer | [Full | Partial] | Code review, drift detection |

**Total Story Points:** [N]
**Historical Velocity:** [N] points/sprint
**Confidence Level:** [High | Medium | Low]

---

## 3. Features in This Sprint

| Feature ID | Feature Name | Priority | Story Points | Status | Assigned Agent(s) |
|------------|--------------|----------|--------------|--------|-------------------|
| [SPRINT-N]-[slug] | [Name] | [critical | high | medium | low] | [N] | [in-progress | complete | blocked] | @Agent |
| | | | | | |

---

## 4. Task Breakdown

### Feature: [Feature Name] — `[SPRINT-N]-[slug]`

| Task ID | Step | Description | Agent | Status | Dependencies |
|---------|------|-------------|-------|--------|--------------|
| [N].1 | Contract | Create and lock Zod schema | @Architect | [pending | in-progress | complete] | — |
| [N].2 | DB | Write zero-downtime migration | @DBA | [pending | in-progress | complete] | [N].1 |
| [N].3 | Backend | Implement API routes + services | @Backend | [pending | in-progress | complete] | [N].1 |
| [N].4 | Frontend | Build UI components + forms | @Frontend | [pending | in-progress | complete] | [N].1 |
| [N].5 | Testing | Write unit + integration + E2E tests | @QA | [pending | in-progress | complete] | [N].3, [N].4 |
| [N].6 | Quality | Run compliance + security gates | @Security + @Reviewer | [pending | in-progress | complete] | [N].5 |

---

## 5. Risks & Blockers

| Risk/Blocker | Impact | Mitigation | Owner | Status |
|--------------|--------|------------|-------|--------|
| [Description] | [High | Medium | Low] | [Action plan] | @Agent | [open | mitigated | resolved] |

---

## 6. Quality Gate Summary

| Gate | Target | Current | Status |
|------|--------|---------|--------|
| Contract Lock | 100% | [N]% | ✅ / ❌ |
| compliance | 95%+ | [N]% | ✅ / ❌ |
| Security Scan | 0 critical/high | [N] findings | ✅ / ❌ |
| Test Coverage | Unit 45%, Int 30%, E2E 5% | [N]% | ✅ / ❌ |
| Build | No errors | [passing | failing] | ✅ / ❌ |
| Visual Regression | 0 drift | [N] regressions | ✅ / ❌ |

---

## 7. Daily Progress Log

| Date | Progress | Blockers | Next Steps | Agent |
|------|----------|----------|------------|-------|
| [YYYY-MM-DD] | [What was accomplished] | [Any blockers] | [Next actions] | @Agent |
| | | | | |

---

## 8. Sprint Review Notes

**What was delivered:**
- [Feature 1]
- [Feature 2]

**What was deferred:**
- [Feature/moved to next sprint]

**Lessons learned:**
- [Insight → action for next sprint]

**Sprint velocity:** [N] story points delivered / [N] planned
**Sprint completion:** [N]% of planned work delivered

---

*Template Version: 1.0 | Maintained by: @Guide + @RetroFacilitator | Used every sprint*
