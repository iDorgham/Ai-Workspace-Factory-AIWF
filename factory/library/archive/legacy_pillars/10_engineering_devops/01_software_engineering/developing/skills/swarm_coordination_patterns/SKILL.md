---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# Swarm Coordination Patterns

## Purpose
Choose the right agent coordination pattern for each task. Using sequential for independent tasks wastes time. Using parallel before contracts are locked causes drift. Pattern selection is @Guide's core competency.

## SDD alignment
Default swarms read the active **phase/spec** under **`.ai/plans/active/features/[phase]/[spec]/`**: **`plan.md`** (AC + Data Shape) and, after SOS, **`prompt.md`**. Phase **`manifest.md`** schedules parallel tiers when multiple specs exist. See **`.ai/skills/sdd_spec_workflow.md`** before splitting work across agents.

## Pattern 1: Sequential (Safe Default)

**When:** Tasks have strict dependencies — each step requires the previous to complete.

```
@Architect (plan + contract) 
    → @DBA (schema + migration)
    → @Backend (API implementation)
    → @Frontend (UI implementation)
    → @QA (test suite)
    → @Reviewer (code review)
    → @Automation (CI/CD + deploy)
```

**Trigger:** `/build [feature]` when contract is not yet locked.

**Token Budget:** Full token allocation per agent — they work serially.

```markdown
## Sequential Execution Manifest
Feature: booking-flow
Pattern: sequential
Step 1 → @Architect  | contract create booking | BLOCKED: none
Step 2 → @DBA        | schema + migration      | BLOCKED BY: Step 1
Step 3 → @Backend    | POST /api/bookings      | BLOCKED BY: Step 2
Step 4 → @Frontend   | BookingForm component   | BLOCKED BY: Step 3
Step 5 → @QA         | unit + integration      | BLOCKED BY: Step 4
Step 6 → @Reviewer   | code review             | BLOCKED BY: Step 5
Step 7 → @Automation | deploy to staging       | BLOCKED BY: Step 6
```

## Pattern 2: Parallel-Safe (Post-Contract Lock)

**When:** Contract is locked. Independent domains can work simultaneously.

```
Contract locked ✅
        ↓
┌─────────────────────────────────────────┐
│  @Frontend     │  @Backend   │  @Content │
│  UI components │  API routes │  i18n keys│
│  (independent) │ (independ.) │ (independ)│
└────────┬───────┴──────┬──────┴─────┬─────┘
         └──────────────┼────────────┘
                        ↓
                   @QA (integration tests)
                        ↓
                  @Reviewer (review all)
```

**Trigger:** `/swarm [feature] --pattern parallel` after `/contract lock [domain]`.

**Token Budget:** Partitioned — each parallel agent gets its slice.

```markdown
## Parallel Execution Manifest
Feature: booking-flow
Pattern: parallel-safe
Contract: booking.ts (locked v1.0 ✅)

PARALLEL GROUP A (can start immediately):
  @Frontend   → BookingForm, BookingCard, BookingTable
  @Backend    → POST/GET/PATCH /api/bookings
  @Content    → booking.en.json, booking.ar.json

PARALLEL GROUP B (after Group A):
  @QA         → unit + integration tests
  @VisualQA   → visual regression baselines

SEQUENTIAL (after Group B):
  @Reviewer   → final review
  @Automation → deploy
```

## Pattern 3: Full Feature Swarm

**When:** End-to-end feature delivery — planning through deployment.

```
Phase 1 — PLANNING (sequential)
  @Founder  → business requirements (Founder mode)
  @Architect → plan + contract + acceptance criteria
  @DBA      → schema design

Phase 2 — EXECUTION (parallel)
  @Frontend | @Backend | @Content

Phase 3 — QUALITY (sequential)
  @QA → @VisualQA → @Security → @Reviewer

Phase 4 — AUTOMATION (sequential)
  @Automation → branch + commit + PR + deploy
```

**Trigger:** `/swarm [feature]` (full orchestration).

## Pattern 4: Hierarchical Override

**When:** Architecture decision, contract change, or priority shift interrupts normal flow.

```
@Architect or @Guide issues directive
        ↓
All in-progress agents PAUSE
        ↓
Directive executed (contract change, plan update)
        ↓
Agents RESUME with updated context
```

**Use for:**
- Breaking contract change detected mid-sprint
- Security vulnerability requiring immediate fix
- Stakeholder priority shift
- Blocked dependency discovered

## Pattern 5: Escalation & Recovery

**When:** A blocker prevents progress. Uses SBAR format.

```
Agent detects blocker
    → Files SBAR escalation to @EscalationHandler
    → @Guide pauses dependent steps
    → @EscalationHandler resolves (15min SLA for critical)
    → @Guide resumes with resolution context
```

```markdown
## SBAR Escalation Template

**Situation:** @Backend blocked on payment integration — Stripe webhook signature verification failing.

**Background:** Implementing payment.ts contract (locked v1.0). POST /api/payments/webhook returns 400 on all test events. Issue started after adding signature verification (Step 3.2).

**Assessment:** If unresolved, entire booking-payment flow cannot complete. Sprint goal at risk. ETA impact: +2 sessions.

**Recommendation:**
  Option A: Use Stripe CLI for local webhook forwarding (30 min, no code changes)
  Option B: Mock webhook in integration tests, defer real webhook to next sprint (1 hour)
  Recommended: Option A — resolves root cause, keeps contract intact.
```

## Pattern 6: Retrospective Learning Loop

**When:** Sprint closes, or a significant failure/success is worth capturing.

```
@RetroFacilitator runs structured retro
    → Extracts 3-5 actionable insights
    → Updates .ai/memory/lessons_learned.md
    → Updates agent definitions if behavior calibration needed
    → Feeds @MetricsAgent with velocity/compliance data
    → @Guide uses memory in next sprint planning
```

## Agent Communication Protocol

```markdown
## Agent Handoff Format

From: @[AgentName]
To:   @[NextAgentName]
Task: [Completed task]
Status: COMPLETE | PARTIAL | BLOCKED

Artifacts produced:
- [file path or artifact name]

Context for next agent:
- [Key decision made]
- [Edge case discovered]
- [Contract used: domain.ts v1.0]

Blockers:
- [None | Description of blocker]

Next recommended step: [Step X.Y from active plan]
```

## Parallel Success Rate (PSR) Target

```
Target:  ≥88% of parallel executions complete without merge conflicts
Warning: 75-87%
Critical: <75% → switch to sequential pattern

Causes of parallel failure:
- Contract not locked before parallel start
- Two agents editing the same file
- Missing scope boundaries in the manifest
```

## Common Mistakes
- Starting parallel execution before contract lock — guaranteed drift
- Using full swarm for single-agent tasks — unnecessary overhead
- No agent handoff format — next agent loses context
- Skipping escalation for blockers — silent progress stalls
- Not updating @Guide after escalation resolution — parallel agents may continue on stale context

## Success Criteria
- [ ] Pattern selected based on task type (not default sequential for everything)
- [ ] Contract locked before any parallel pattern starts
- [ ] Execution manifest written before agent work begins
- [ ] Agent handoff format used for all task transitions
- [ ] Escalation filed within 15 min of blocker detection
- [ ] PSR ≥88% tracked by @MetricsAgent