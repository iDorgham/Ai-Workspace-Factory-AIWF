---
type: Generic
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# Escalation: [Issue Title]

> **Escalation ID:** `ESC-[NNN]`
> **Date:** [YYYY-MM-DD HH:MM]
> **Raised by:** @AgentName
> **Severity:** [critical | high | medium | low]
> **Status:** [open | investigating | mitigated | resolved | closed]
> **Assigned to:** @EscalationHandler

---

## SBAR Format (Situation, Background, Assessment, Recommendation)

### Situation
**What is happening right now?**
[Clear, concise description of the current issue — 1-2 sentences]

**Impact:**
[What is blocked or at risk — features, deadlines, quality]

---

### Background
**Relevant context and history:**
- [Fact 1 — e.g., "Contract for [domain] has been unlocked since [date]"]
- [Fact 2 — e.g., "Three downstream services depend on this schema"]
- [Fact 3 — e.g., "Previous attempt to fix this on [date] was rolled back"]

**Related files:**
- `.ai/plans/active/features/[feature].md`
- `packages/shared/src/contracts/[domain].ts`
- [Other relevant paths]

---

### Assessment
**What is the impact if unresolved?**
- **Timeline impact:** [N] days/weeks delayed
- **Quality impact:** [Description of degradation]
- **Risk score:** [N/25] (5×5 matrix — likelihood × impact)
- **Cascade risk:** [What else might fail if this isn't fixed]

**Attempts so far:**
1. [Action taken] → [Result]
2. [Action taken] → [Result]

---

### Recommendation
**Proposed solution with options:**

| Option | Description | Pros | Cons | Effort | Risk |
|--------|-------------|------|------|--------|------|
| A | [Approach] | [List] | [List] | [S/M/L] | [Low/Med/High] |
| B | [Approach] | [List] | [List] | [S/M/L] | [Low/Med/High] |
| C | [Approach] | [List] | [List] | [S/M/L] | [Low/Med/High] |

**Recommended option:** [A | B | C]
**Rationale:** [Why this option]

---

## Resolution Log

| Date | Action | Agent | Result |
|------|--------|-------|--------|
| [YYYY-MM-DD HH:MM] | [What was done] | @Agent | [success | partial | failed] |
| | | | |

**Resolved at:** [YYYY-MM-DD HH:MM]
**Resolved by:** @EscalationHandler
**Resolution:** [Brief summary of how it was resolved]

---

## Post-Resolution Review

**Root cause:** [What actually caused the issue]
**Prevention:** [What will prevent this in future — process change, automation, monitoring]
**Lesson learned:** [Summary for `.ai/memory/lessons_learned.md`]

**Escalation closed:** ✅
**Time to resolution:** [N hours/days]

---

*Template Version: 1.0 | Maintained by: @EscalationHandler | All escalations logged to `.ai/plans/active/audit/escalations/`*
