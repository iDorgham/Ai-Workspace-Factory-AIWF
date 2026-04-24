---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# Lesson Injection

## Purpose
Turn past mistakes and decisions into automatic guardrails. Instead of agents passively having access to memory files, this skill actively injects only the most relevant lessons as hard constraints in agent context before work begins.

---

## How Injection Differs from Passive Memory Loading

```
PASSIVE MEMORY LOADING (current baseline):
  Agent loads .ai/memory/lessons_learned.md
  Agent reads 2,000 tokens of lessons
  Agent may or may not apply them (human error, token budget pressure)
  → Lessons are available but not enforced

LESSON INJECTION (this skill):
  @ContextSlicer analyzes the task
  Extracts ONLY relevant lessons (domain + agent + task type match)
  Injects them as CONSTRAINTS in the agent's task context
  Agent sees: "CONSTRAINT: [lesson] — violation will be flagged by @Reviewer"
  → Lessons become rules the agent cannot ignore
```

---

## Injection Algorithm (@ContextSlicer)

```typescript
// @ContextSlicer lesson injection
function injectLessons(task: TaskContext, agent: AgentId): Lesson[] {
  const allLessons = loadMemory([
    '.ai/memory/lessons_learned.md',
    '.ai/memory/anti_patterns.md',    // high-priority rules
    '.ai/memory/error_patterns.md',   // recent errors
  ])

  return allLessons
    // Filter by relevance
    .filter(lesson => (
      matchesDomain(lesson, task.domain) ||
      matchesAgent(lesson, agent) ||
      matchesTaskType(lesson, task.type) ||
      lesson.severity === 'CRITICAL'  // always inject CRITICAL
    ))
    // Sort by relevance score (domain match > agent match > task type match)
    .sort((a, b) => relevanceScore(b, task) - relevanceScore(a, task))
    // Budget: max 10 lessons or 400 tokens (whichever comes first)
    .slice(0, 10)
    .filter(cumulative => cumulativeTokens < 400)
}
```

---

## Injection Format in Agent Context

```markdown
## Injected Lessons — @Frontend — booking-form task
(Constraints derived from past mistakes — apply without exception)

### CRITICAL Constraints (blocking — violation fails review)
- [AP-003] NEVER use margin-left/right or padding-left/right CSS classes.
  USE: margin-inline-start, padding-inline-start (logical properties)
  Why: RTL layout breaks silently with directional CSS. Found: Sprint 2, 8 components reworked.

- [AP-011] NEVER hardcode colors (#hex) or spacing (px) values.
  USE: CSS variables from packages/ui/src/lib/styles/tokens.css
  Why: Token governance. Raw values fail compliance gate.

### HIGH Constraints (warned — agent must acknowledge)
- [L-003] Arabic text overflows table columns wider than 8 characters.
  USE: truncate class + title attribute for full text tooltip
  Why: Arabic has longer words than English for same concepts. Found: Sprint 1.

- [L-009] BookingForm price field — always show currency symbol BEFORE amount.
  USE: formatCurrency(amount, currency) from @workspace/shared/utils
  Why: EGP formats differently from USD/EUR. Found: Sprint 3, QA caught it.

### MEDIUM Constraints (informational — apply if applicable)
- [L-014] Skeleton loading states use Tailwind animate-pulse class.
  USE: the Skeleton component from packages/ui (don't rebuild)
  Why: Consistency with existing loading states across all forms.

**Active constraints: 5 | Budget used: 280 tokens | Remaining for content: 5,720 tokens**
```

---

## Lesson Classification System

```markdown
## Lesson Categories for Injection Priority

INJECT ALWAYS:
- CRITICAL anti-patterns (AP-[id] from .ai/memory/anti_patterns.md)
- Any lesson where severity = CRITICAL
- Any lesson matching exact domain + agent combination

INJECT IF BUDGET ALLOWS:
- Lessons matching task domain (HIGH severity)
- Lessons matching agent type (any severity)
- Lessons from the last 2 sprints (recency bonus)
- Lessons that prevented >3,000 token fixes in the past

DO NOT INJECT:
- Lessons >3 sprints old with no recurrence
- Lessons from different project types
- Lessons about agents not involved in this task
- Lessons below LOW severity that don't match domain
```

---

## Lesson Capture Flow (Feeding the Injection System)

When something goes wrong or is solved unusually well:

```markdown
## Lesson Capture — instant protocol

RIGHT AFTER finding/fixing a problem:

1. @ErrorDetective (or the agent that found the issue) writes:

   --- NEW LESSON ---
   Date: 2026-04-11
   ID: L-023 (next sequential)
   Agent: @Frontend
   Domain: booking
   Task type: form-component
   Severity: HIGH
   Pattern: [what went wrong or what worked well]
   Example: Used `margin-left` instead of `margin-inline-start` on BookingForm inputs
   Fix: Replace all directional CSS with logical properties
   Prevention rule: Before any CSS class, check: is it directional? → use logical equivalent
   Tokens wasted: ~2,400 (rewrite + @Reviewer cycle)
   ---

2. @ContextSlicer indexes the new lesson:
   - Tags: agent=Frontend, domain=booking, type=form-component, severity=HIGH
   - Adds to injection pool

3. Next time any @Frontend task on a form-component starts:
   - L-023 is automatically injected as a constraint
   - Agent cannot output directional CSS without flagging it

Result: second occurrence is prevented, not just recorded.
```

---

## Lesson Aging and Retirement

```markdown
## Lesson Lifecycle

Active (inject):
  - Lessons written in last 3 sprints
  - Lessons that have been triggered (same pattern seen again) within 6 sprints
  - CRITICAL lessons (never retire)

Aging (inject with lower priority):
  - Lessons 4–6 sprints old without recurrence
  - Consider: is this codebase area still active?

Retired (don't inject, archive):
  - Lessons 7+ sprints old with zero recurrence
  - Lessons about removed features or replaced libraries
  - Move to: .ai/memory/archive/lessons-[sprint].md

Never retire:
  - Security lessons (OWASP, auth, secrets handling)
  - CRITICAL anti-patterns
  - Lessons marked: keep-forever: true
```

---

## Cross-Agent Lesson Sharing

```markdown
## When a lesson from @Backend benefits @Frontend

Normally: lessons are agent-specific
Exception: cross-agent injection for lessons that affect shared surfaces

Triggers for cross-agent injection:
- @Backend lesson about API field naming → @Frontend that calls the API
- @DBA lesson about migration order → @Backend that depends on schema
- @Security lesson about input validation → @Frontend that builds forms
- @QA lesson about test isolation → ALL agents that write tests

Format for cross-agent lessons:
  [L-028 | originally @Backend] API route returns `confirmationId` not `id` for booking confirmation.
  Cross-injected to @Frontend because: UI displays this field by name.
```

---

## Injection for Swarm Execution

```markdown
## During /swarm parallel execution

@ContextSlicer injects to EACH agent independently:
  @Frontend task → receives Frontend + domain + UI-type lessons
  @Backend task → receives Backend + domain + API-type lessons
  @QA task → receives QA + domain + test-type lessons
  @Security task → receives Security + ALL severity CRITICAL

De-duplication: if same lesson applies to multiple agents, each receives it
  (a 40-token constraint is cheap vs a 3,000-token fix from missing it)

Swarm lesson injection budget: 400 tokens per agent × 3 agents = 1,200 tokens
  vs average fix cost of missing a lesson: 4,000–8,000 tokens
  ROI: 3–6× return per swarm execution
```

## 🌍 Regional Calibration (MENA Context)

- **Cultural Alignment:** Ensure all logic respects regional business etiquette and MENA market expectations.
- **RTL Compliance:** Logic must explicitly handle Right-to-Left (RTL) flow where relevant.

## 🛡️ Critical Failure Modes (Anti-Patterns)

- **Anti-Pattern:** Generic Output -> *Correction:* Apply sector-specific professional rules from RULE.md.
- **Anti-Pattern:** Global-Only Logic -> *Correction:* Verify against MENA regional calibration.

---

## Success Criteria
- [ ] Every agent task receives injected lessons before starting
- [ ] CRITICAL anti-patterns always injected (no budget exception)
- [ ] New lessons captured within the same session they occur
- [ ] Lessons aged and retired to prevent context bloat
- [ ] Cross-agent sharing active for shared-surface lessons
- [ ] @MetricsAgent tracks: lessons injected vs lessons triggered (effectiveness rate)
- [ ] Target: injected lesson prevents issue 80%+ of the time it's injected