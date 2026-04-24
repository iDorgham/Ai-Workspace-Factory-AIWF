---
type: Command
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---


# /retro — Retrospective & Knowledge Synthesis

> **Primary Agents:** `@RetroFacilitator` (leads) · `@ErrorDetective` (mistake analysis) · `@KnowledgeSynthesizer` (rule propagation)
> **Purpose:** Close the feedback loop — turn sprint experience into permanent agent intelligence
> **Scope:** Sprint-end reflection, error pattern distillation, skill + agent Hard Rules updates, institutional memory

---

## Usage

```bash
/retro start [--sprint N]         → Full retrospective + knowledge synthesis
/retro mistakes [--sprint N]      → Mistake pattern distillation only (no full retro)
/retro action-items [--sprint N]  → Review action item status from previous retro
/retro archive [--sprint N]       → Archive completed retro + retire stale patterns
```

---

## Why /retro Is Critical for the Mistake Prevention System

The mistake prevention system has four layers (see `.ai/skills/mistake_prevention_system.md`):
- Layer 1: Pre-task anti-pattern scan
- Layer 2: Live verification checkpoints
- Layer 3: Failure capture (happens during the sprint)
- **Layer 4: Retro pattern distillation → this command is Layer 4**

Without `/retro`, error patterns accumulate in `error_patterns.md` but never become hard rules. Agents never get smarter. The same mistakes recur indefinitely.

`/retro start` closes that loop.

---

## Phase 0 — Gather All Sprint Data (before facilitating)

`@RetroFacilitator` collects from all sources before the retrospective begins:

```
FROM @MetricsAgent:
  Velocity: this sprint vs last sprint vs project trend
  Sovereign compliance score: change from last sprint
  PR cycle time: average + worst case
  Escalation count: how many, resolved within SLA?
  Test coverage: change (up/down/stable)
  Context Retention Index (CRI): ≥95% target
  Turborepo cache hit rate: ≥85% target

FROM @ErrorDetective (sprint error report):
  Total errors captured in error_patterns.md this sprint
  Error patterns by type, agent, domain
  Errors already promoted to anti_patterns.md
  Errors still pending (1 occurrence) — candidates for review
  Anti-pattern injection effectiveness (injected vs prevented)
  Estimated tokens wasted by errors this sprint
  Estimated tokens saved by AP injection this sprint

FROM .ai/memory/error_patterns.md:
  All EP-[id] entries written this sprint (not yet [PROCESSED])
  Recurrence alerts from @ErrorDetective

FROM .ai/memory/anti_patterns.md:
  AP entries added this sprint
  AP effectiveness scores (which patterns are working, which aren't)
  AP entries flagged as underperforming (<80% effectiveness)

FROM .ai/plans/active/audit/command-logs/:
  Which commands ran most this sprint?
  Any commands that failed or were retried?
  Build failures, test failures, quality gate failures

FROM .ai/plans/active/audit/escalations/:
  All ESC-[id] entries from this sprint
  Were they resolved within SLA? What type?

FROM .ai/plans/active/features/:
  Features planned vs completed (scope accuracy)
  Which features had the most rework?
  Which features had zero rework (what made them smooth)?

FROM .ai/memory/lessons_learned.md:
  Lessons written last sprint — were they applied this sprint?
  Learning loop validation: did past lessons prevent issues?
```

---

## /retro start — Full Retrospective

### Step 1 — Initialize Retro Document

```bash
cp .ai/templates/retro.md .ai/plans/active/retros/sprint-[N]-retro.md
```

Fill header: sprint number, date range, velocity, compliance score, error metrics.

---

### Step 2 — Sprint Performance Summary

```markdown
## Sprint [N] Performance

| Metric | Result | Target | Δ vs Last Sprint |
|--------|--------|--------|-----------------|
| Story Points | [X] SP | [Y] SP | [+/-N] |
| Sovereign Compliance | [X]% | ≥95% | [+/-N%] |
| Test Coverage | [X]% | ≥45% | [+/-N%] |
| PR Cycle Time | [X]d avg | <1d | [+/-Nd] |
| Cache Hit Rate | [X]% | ≥85% | [+/-N%] |
| Escalations | [N] | ≤2 | [+/-N] |
| CRI | [X]% | ≥95% | [+/-N%] |
| Errors captured (EP) | [N] | — | [+/-N] |
| Tokens wasted by errors | ~[N] | → 0 | [+/-N] |
| Tokens saved by AP injection | ~[N] | → ↑ | [+/-N] |
```

---

### Step 3 — Reflection (What Went Well / What to Improve)

**For automated retro (AI-driven):**

```
@RetroFacilitator analyzes Phase 0 data and generates:

WHAT WENT WELL (3–5 items, data-backed):
  - Features completed ahead of schedule → what specifically made them smooth?
  - Quality score improved → which new practice drove this?
  - Zero escalations → which pre-flight checks caught issues early?
  - Error pattern X never recurred → which AP injection prevented it?

WHAT TO IMPROVE (3–5 items, root-cause anchored):
  - Rework on [feature] → root cause: [DMP step skipped? contract lock missed?]
  - AP-[id] recurring despite injection → root cause: injected too late in task flow?
  - Test failures rate up → root cause: coverage gaps not caught pre-build?
  - Tokens wasted high → root cause: which error type consumed most?

Rule: every "improve" item must have a root cause identified from the data.
"PRs were slow" is rejected. "PR reviews averaged 2.1d because @Reviewer was on
critical path for 72% of PRs — contract-first flow would have parallelized 40% of these"
is accepted.
```

**For interactive retro (with the user):**

```
@RetroFacilitator prompts:

1. "What are you most proud of this sprint?"
2. "What frustrated you or slowed you down?"
3. "Did the AI agents make any mistake more than once? Which one?"
4. "Was there anything the agents kept doing wrong that wasted your time?"
5. "What should agents start doing, stop doing, or keep doing?"
6. "Were you happy with how much context the agents remembered from previous sessions?"

Questions 3–6 feed directly into the mistake prevention synthesis (Step 5).
User answers about recurring agent mistakes → immediate @ErrorDetective capture.
```

---

### Step 4 — Action Items (max 5, highest-impact only)

```markdown
## Action Items for Sprint [N+1]

| # | Action | Root Cause It Addresses | Owner | By | Success Metric |
|---|--------|------------------------|-------|-----|----------------|
| 1 | [Specific, executable] | [Which EP/AP/pattern] | [@Agent] | Sprint [N+1] | [Measurable outcome] |
| 2 | | | | | |
| 3 | | | | | |

Fewer, better. Not a wishlist. Max 5.
Good: "Add missing aria-label check to @Frontend pre-flight gate (EP-014 root cause)"
Bad:  "Improve accessibility"
```

---

### Step 5 — Mistake Prevention Synthesis (@ErrorDetective leads)

This step runs in parallel with Step 3 reflection. `@ErrorDetective` processes all EP entries from the sprint.

```markdown
## @ErrorDetective — Sprint [N] Error Analysis

### Raw Error Log Review
Entries in error_patterns.md this sprint (not yet [PROCESSED]):
  [EP-001]: [pattern type] | [agent] | [domain] | Severity: [level]
  [EP-002]: ...
  [EP-003]: ...

### Recurrence Detection
| Pattern Type | Count | Agents Involved | Severity |
|-------------|-------|----------------|----------|
| Directional CSS (AP-001) | 3 | @Frontend | HIGH — recurring despite injection |
| Hardcoded string (AP-010) | 1 | @Frontend | HIGH — first occurrence |
| Missing Zod validation | 2 | @Backend | CRITICAL — promote immediately |

### Promotion Decisions
| EP-IDs | Decision | AP Action |
|--------|---------|-----------|
| EP-001, EP-005, EP-011 | 3× same pattern | Promote → AP-054 (new) |
| EP-002 | 1× occurrence | Monitor — no promotion yet |
| EP-007, EP-009 | 2× same | Promote → AP-055 (new) |
| EP-003 | Matches AP-001 | Update AP-001 (raise severity, add example) |

### Underperforming AP Analysis
| AP-ID | Injections | Violations | Effectiveness | Root Cause of Failure |
|-------|-----------|------------|--------------|----------------------|
| AP-001 | 24 | 3 | 88% | Injected in context but agent still skips — need Hard Rule in agent definition |
| AP-010 | 18 | 2 | 89% | Pre-flight check passes too quickly for i18n step |

### Token Cost Summary
Total tokens wasted by errors this sprint: ~[N]
Top error types by token cost:
  1. [Pattern type]: ~[N] tokens ([N] occurrences × avg [N] tokens/fix)
  2. [Pattern type]: ~[N] tokens
Total tokens saved by AP injection: ~[N]
Net benefit of mistake prevention system: [N]× ROI
```

---

### Step 6 — Knowledge Synthesis & Propagation (@KnowledgeSynthesizer leads)

This is the step that was previously missing. `@KnowledgeSynthesizer` takes `@ErrorDetective`'s analysis and writes the results back into skill files and agent definitions.

**This step makes every agent permanently smarter after every sprint.**

```markdown
## @KnowledgeSynthesizer — Sprint [N] Knowledge Synthesis

### New Anti-Patterns to Write (from Step 5 decisions)

For each AP promoted or updated:

--- AP WRITE ---
Target file: .ai/memory/anti_patterns.md
Action: Add AP-[id] entry using standard format
Quality check before writing:
  ✓ Specific (describes exact code, not vague guideline)?
  ✓ Actionable (tells agent exactly what to do instead)?
  ✓ Justified (explains WHY, not just WHAT)?
  ✓ Scoped (right agents and task types)?
  ✓ Non-duplicate (doesn't overlap existing AP)?
  ✓ Testable (can @Reviewer detect violations)?

Write: [AP-054] [AP-055] entries
---

### Skill Files to Update

For each new or updated AP, identify which skill files cover that area:

| AP-ID | Pattern Area | Skill File | Change |
|-------|-------------|-----------|--------|
| AP-054 | Missing icon aria-label | pre_flight_checklist.md | Add to @Frontend Pre-Flight section |
| AP-054 | Missing icon aria-label | hallucination_containment.md | Add to HIGH RISK zones |
| AP-055 | Redis TTL not set | pre_flight_checklist.md | Add to @Backend Pre-Flight section |
| AP-001 update | Directional CSS (raised severity) | lesson_injection.md | Update filter threshold |

For each skill file change:
  Section to add to: "## Common Mistakes" (most recent lessons at top)
  Format: **[AP-NNN]** [description of mistake and correct approach]
           Sprint [N] addition — [brief reason it was added]

Also check if "## Success Criteria" needs a new checkbox.
```

**Writing the skill file updates:**

```markdown
### Skill File Updates Applied

.ai/skills/pre_flight_checklist.md:
  @Frontend Pre-Flight section → added:
    - [ ] All icon buttons have aria-label (not just aria-hidden) [AP-054]

  @Backend Pre-Flight section → added:
    - [ ] Redis cache entries have explicit TTL set (never indefinite) [AP-055]

.ai/skills/hallucination_containment.md:
  HIGH RISK section → added:
    - Icon aria patterns (aria-label vs aria-hidden — easy to confuse) [AP-054]

.ai/skills/lesson_injection.md:
  Injection filter → updated:
    - AP-001 severity raised — now CRITICAL for @Frontend (was HIGH)
    - Injection timing note: must be in pre-flight, not just context load
```

### Agent Hard Rules Updates

When an AP is recurring despite being in `anti_patterns.md` (effectiveness <90%), the rule must be written directly into the agent's definition file under a `## Hard Rules` section:

```markdown
### Agent Hard Rules Updates Applied

.ai/agents/frontend.md:
  Section "## Hard Rules (Non-Negotiable)" — added:
    - [AP-054] NEVER use <Icon> without aria-label. Every icon that conveys meaning
      needs aria-label="[action description]". Decorative icons use aria-hidden="true".
      (Added Sprint [N] — recurring: appeared 3× despite AP injection)

    - [AP-001] NEVER use ml-/mr-/pl-/pr-/margin-left/margin-right Tailwind classes or
      CSS properties. ALWAYS use ms-/me-/ps-/pe-/margin-inline-start/margin-inline-end.
      (Severity raised to CRITICAL Sprint [N] — appeared 3× this sprint)

.ai/agents/backend.md:
  Section "## Hard Rules (Non-Negotiable)" — added:
    - [AP-055] NEVER set cache entries without an explicit TTL.
      ALWAYS: redis.set(key, value, 'EX', TTL_SECONDS)
      Default TTL: use CACHE_TTL_DEFAULT from env (never hardcode seconds inline)
      (Added Sprint [N] — appeared 2× in integration tests)

Rule for when to add Hard Rules vs rely on AP injection:
  AP effectiveness ≥90% → AP injection alone is sufficient
  AP effectiveness 80–89% → add to pre-flight checklist for that agent
  AP effectiveness <80% → add Hard Rule to agent definition + pre-flight
  AP CRITICAL and any recurrence → Hard Rule always (regardless of effectiveness %)
```

---

### Step 7 — Lessons Learned Capture & Archiving

**Write new lessons to `.ai/memory/lessons_learned.md`:**

```markdown
## Lessons Learned — Sprint [N] (YYYY-MM-DD)

### L-[N]-001: [Short, searchable title]
Situation: [What happened — 1 sentence]
Root cause: [Why it happened — 1 sentence]
Fix applied: [What was changed — AP entry, Hard Rule, skill update, gate change]
Watch for: [Trigger condition that signals this is happening again]
Tokens cost: ~[N] tokens before caught
Resolution sprint: [N] | Expected: [N+1 target]

### L-[N]-002: ...
```

**Archive processed EP entries:**

```markdown
For every EP entry reviewed in Step 5:
  Mark as: [PROCESSED-Sprint-N] in error_patterns.md

Entries to archive (3+ sprints old, [PROCESSED]):
  Move to: .ai/memory/archive/error-patterns-sprint-[N].md
  Preserve summary row in: error_patterns.md recurring patterns tracker
```

**Review AP entries for retirement:**

```markdown
Retirement candidates (no trigger in 6+ sprints):
  Check each AP-MEDIUM entry: last triggered sprint?
  If 6+ sprints with zero occurrences → mark RETIRED
  Move to: .ai/memory/archive/anti_patterns_retired.md

CRITICAL and security APs: never retire
APs added this sprint: never retire (regardless of sprint count — too new to assess)
```

---

### Step 8 — Complete Retro

```
1. Mark retro status: complete
2. Save to: .ai/plans/active/retros/sprint-[N]-retro.md
3. Archive sprint plan: .ai/plans/archive/sprint-[N].md
4. Update .ai/memory/project_context.md (velocity trend, error rate trend)
5. Notify @Guide: action items ready for next sprint planning
6. Notify @ContextSlicer: AP injection pool updated (new APs, updated severities)
```

---

## /retro start — Full Output Format

```markdown
## Retrospective Complete — Sprint [N]
Date: YYYY-MM-DD | Facilitator: @RetroFacilitator + @ErrorDetective + @KnowledgeSynthesizer

---

## Sprint [N] Summary
| Metric | Result | Target | Status |
|--------|--------|--------|--------|
| Story Points | [X] SP | [Y] SP | ✅ / ⚠️ / ❌ |
| Sovereign Compliance | [X]% | ≥95% | ✅ / ⚠️ / ❌ |
| Test Coverage | [X]% | ≥45% | ✅ / ⚠️ / ❌ |
| PR Cycle Time | [X]d avg | <1d | ✅ / ⚠️ / ❌ |
| Escalations | [N] | ≤2 | ✅ / ⚠️ / ❌ |
| Cache Hit Rate | [X]% | ≥85% | ✅ / ⚠️ / ❌ |
| CRI | [X]% | ≥95% | ✅ / ⚠️ / ❌ |

## Mistake Prevention Cycle (Sprint [N])
| Metric | Sprint [N] | Trend |
|--------|-----------|-------|
| Errors captured (EP entries) | [N] | ↑↓→ vs Sprint [N-1] |
| Patterns promoted to AP | [N] | — |
| Agent definitions updated | [N] | — |
| Skill files updated | [N] | — |
| Tokens wasted by errors | ~[N] | ↓ target |
| Tokens saved by AP injection | ~[N] | ↑ target |
| AP injection effectiveness | [N]% avg | ≥80% target |
| APs underperforming (<80%) | [N] → Hard Rules added | — |
| APs retired this sprint | [N] | — |

## What Went Well
1. [Specific achievement + data that proves it]
2. [Specific achievement + data]
3. [Specific achievement + data]

## What to Improve
1. [Issue] → Root cause: [specific] → Cost: [tokens/time] → Action: [Step 4 item]
2. [Issue] → Root cause: [specific] → Cost: [tokens/time] → Action: [Step 4 item]
3. [Issue] → Root cause: [specific] → Cost: [tokens/time] → Action: [Step 4 item]

## Action Items for Sprint [N+1]
| # | Action | Root Cause | Owner | Success Metric |
|---|--------|-----------|-------|----------------|
| 1 | [specific action] | [EP/AP/pattern] | [@Agent] | [measurable] |
| 2 | | | | |
| 3 | | | | |

## Knowledge Synthesis Results
### New Anti-Patterns Written
| AP-ID | Title | Severity | Derived From |
|-------|-------|----------|-------------|
| AP-054 | [title] | HIGH | EP-001, EP-005, EP-011 |
| AP-055 | [title] | MEDIUM | EP-007, EP-009 |

### Agent Hard Rules Updated
| Agent | Rule Added | AP-ID | Reason |
|-------|-----------|-------|--------|
| @Frontend | [rule summary] | AP-054 | 3× recurring despite injection |
| @Backend | [rule summary] | AP-055 | 2× occurrence this sprint |

### Skill Files Updated
| File | Change | AP-ID |
|------|--------|-------|
| pre_flight_checklist.md | Added @Frontend icon aria check | AP-054 |
| pre_flight_checklist.md | Added @Backend Redis TTL check | AP-055 |
| hallucination_containment.md | Added aria pattern to HIGH RISK | AP-054 |

### Lessons Learned Added
| ID | Title | Severity |
|----|-------|----------|
| L-[N]-001 | [lesson title] | HIGH |
| L-[N]-002 | [lesson title] | MEDIUM |

### Memory Housekeeping
- EP entries marked [PROCESSED]: [N]
- EP entries archived to archive/: [N]
- AP entries retired: [N]
- AP entries raised in severity: [N]

**Retro document:** `.ai/plans/active/retros/sprint-[N]-retro.md`
**Next sprint planning:** @Guide ready with action items
**AP injection pool:** Updated — @ContextSlicer notified
```

---

## /retro mistakes — Mistake Pattern Distillation Only

Run this at any point in a sprint when you want to synthesize error patterns without a full retro.

```markdown
## @ErrorDetective + @KnowledgeSynthesizer — Mistake Distillation Run
Date: YYYY-MM-DD | Mode: mid-sprint | Sprint: [N]

Step 1: Load all new EP entries since last distillation run
Step 2: Run recurrence detection
Step 3: Promote qualifying patterns to anti_patterns.md
Step 4: Update affected skill files
Step 5: Update affected agent Hard Rules
Step 6: Mark processed EP entries
Step 7: Notify @ContextSlicer of injection pool changes

Output: same format as "Knowledge Synthesis Results" section above

When to use:
  - AP-[id] appearing repeatedly mid-sprint (can't wait for retro)
  - CRITICAL new error pattern caught (promote immediately regardless of sprint phase)
  - User reports "agents keep doing the same mistake" mid-sprint
  - After any @EscalationHandler incident (patterns from incidents must be captured fast)
```

---

## /retro action-items — Review Previous Action Items

```markdown
## Action Items — Sprint [N] Retro

| # | Action | Owner | Priority | Status | Root Cause Addressed | Notes |
|---|--------|-------|----------|--------|---------------------|-------|
| 1 | [action] | @Agent | high | ✅ complete | [EP/AP/pattern] | AP-054 added, 0 recurrences |
| 2 | [action] | @Agent | high | 🔄 in-progress | [pattern] | Hard Rule drafted, not merged |
| 3 | [action] | @Agent | medium | ❌ not-started | [pattern] | At risk — carry to Sprint [N+1] |

### Summary
Complete: [N] of [N] | In progress: [N] | Not started: [N] | Rate: [N]%

### Mistake Prevention Actions Specifically
| AP-ID | Action from last retro | Applied? | Effect |
|-------|----------------------|---------|--------|
| AP-054 | Add Hard Rule to frontend.md | ✅ | 0 recurrences this sprint |
| AP-001 | Raise to CRITICAL in injection | ✅ | Reduced from 3× to 1× |

### Recommendations
- Completion rate <80%: cut to 3 items next retro — fewer, better
- Incomplete mistake prevention action: carry forward + escalate if 2nd sprint missed
- Same root cause appearing again: @ErrorDetective immediate mid-sprint distillation
```

---

## /retro archive — Archive & Close Sprint

```markdown
Flow:
1. Validate retro complete (status = complete, all steps run)
2. Move retro doc: .ai/plans/active/retros/ → .ai/plans/archive/retros/sprint-[N]-retro.md
3. Archive sprint plan: .ai/plans/active/ → .ai/plans/archive/sprint-[N].md
4. Verify lessons_learned.md has Sprint [N] section
5. Verify anti_patterns.md has new AP entries from Sprint [N]
6. Verify all agent .md files updated with Hard Rules from Sprint [N]
7. Verify all skill .md files updated with new Common Mistakes from Sprint [N]
8. Update .ai/memory/project_context.md (velocity trend, error rate trend, AP count)
9. Tag processed EP entries: [PROCESSED-Sprint-N] in error_patterns.md
10. Confirm: "Sprint [N] fully archived and knowledge propagated"

Output:
✅ Sprint [N] retro archived: .ai/plans/archive/retros/sprint-[N]-retro.md
✅ Lessons preserved: .ai/memory/lessons_learned.md (Sprint [N] section)
✅ [N] new APs written: .ai/memory/anti_patterns.md
✅ [N] agent files updated with Hard Rules
✅ [N] skill files updated with Common Mistakes
✅ [N] EP entries archived: .ai/memory/archive/error-patterns-sprint-[N].md
✅ @ContextSlicer notified: injection pool refreshed for Sprint [N+1]
```

---

## The Knowledge Propagation Chain

This is how a single mistake in Sprint 1 becomes a permanent guard by Sprint 2:

```
Sprint 1: @Frontend uses margin-left (AP-001 violation)
          ↓
          /quality catches it → EP-001 captured in error_patterns.md
          ↓
          Second occurrence same sprint → @ErrorDetective flags recurrence
          ↓
/retro start (Sprint 1 end):
  Step 5: @ErrorDetective — EP-001 + EP-005 both directional CSS → 2 occurrences
          Decision: promote to anti-pattern (already AP-001 — raise severity)
          ↓
  Step 6: @KnowledgeSynthesizer:
          → Raises AP-001 from HIGH to CRITICAL in anti_patterns.md
          → Adds Hard Rule to .ai/agents/frontend.md:
            "NEVER use ml-/mr- classes. ALWAYS use ms-/me-. Violation = CRITICAL."
          → Adds check to .ai/skills/pre_flight_checklist.md @Frontend section
          → Updates lesson_injection.md: AP-001 now CRITICAL priority in filter
          ↓
Sprint 2: @ContextSlicer loads AP-001 as CRITICAL constraint
          @Frontend pre-flight: directional CSS check active
          → 0 occurrences of AP-001 in Sprint 2
          → Tokens saved: 3 occurrences × avg 1,200 tokens = 3,600 tokens

This is the compounding return: each sprint, the swarm makes fewer mistakes
and saves more tokens than the previous sprint.
```

---

## Retro Facilitation Principles

### Blameless, Pattern-Focused
- Focus on **process and system**, not individual agent performance
- Every mistake is a system design opportunity, not a fault
- "We built a rule to prevent this" is the goal — not "we blamed the agent"

### Data-Driven
- Every "improve" item must cite a metric or EP-[id] — no gut-feel items
- Tokens wasted is a valid metric — inefficiency is a quality defect
- Effectiveness % for AP injection is a first-class sprint metric

### Compounding Improvement
- A retro that updates 2 skill files and 1 agent definition is worth 10× its time cost
- The goal is not to "have the retro" — it's to propagate knowledge into permanent rules
- If no files are updated during a retro, the retro was incomplete

---

## Common Retro Failure Modes

| Failure | Symptom | Fix |
|---------|---------|-----|
| No Knowledge Synthesis | Lessons written but skill/agent files unchanged | Step 6 + 7 are not optional — run them |
| Too many action items | 10+ items, <50% completed | Cap at 5, rank by token-cost impact |
| Vague improvements | "Improve accessibility" | Must cite EP-[id] and specific rule to add |
| Recurring same mistake | Same AP violated 3+ sprints | Hard Rule directly into agent definition — injection alone insufficient |
| Skipping retro | "No time" | /retro mistakes (15-min version) — better than nothing; full retro monthly minimum |
| AP injection pool not updated | @ContextSlicer not notified | Archive step 10 — explicit notification |

---

## Integration Points

| Agent | Role |
|-------|------|
| `@RetroFacilitator` | Leads the process, facilitates reflection, produces retro doc |
| `@ErrorDetective` | Step 5 — error analysis, recurrence detection, promotion decisions |
| `@KnowledgeSynthesizer` | Step 6 + 7 — writes AP entries, updates skill files, updates agent Hard Rules |
| `@ContextSlicer` | Notified at archive step — refreshes injection pool with new APs + severity updates |
| `@Guide` | Receives action items → adds to next sprint planning |
| `@MetricsAgent` | Supplies sprint velocity, compliance, CRI, cache hit rate data |
| `@RiskAgent` | Receives systemic risks identified in retro → updates risk register |
| `@EscalationHandler` | Receives recurring patterns that block multiple sprints |
| `@Founder` | Receives plain-language version of retro insights (Founder mode) |

---

*Command Version: 2.0 | Updated: 2026-04-11*
*Invokes: @RetroFacilitator, @ErrorDetective, @KnowledgeSynthesizer, @ContextSlicer, @Guide, @MetricsAgent*
*Skills: mistake-prevention-system, lesson-injection, dynamic-memory-protocol, blameless-escalation-sbar*
*Writes to: anti_patterns.md, error_patterns.md, lessons_learned.md, skill files, agent files, project_context.md*
