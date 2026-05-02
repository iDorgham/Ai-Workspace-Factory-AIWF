---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# Dynamic Memory Protocol

## Purpose
Load workspace context in a deterministic, hierarchical order before every task. Prevents agents from hallucinating outdated contracts, missing active plans, or contradicting past decisions.

## When to Activate
- At the start of every agent task (no exceptions)
- When switching between features mid-session
- After any `/contract lock` or plan update
- When resuming work after a context gap

## The 8-Step Load Sequence

```
Step 0 → .ai/memory/anti_patterns.md        (injected constraints — what NEVER to do — checked FIRST)
Step 1 → .ai/context/architecture.md        (global rules, tech stack, naming)
Step 2 → .ai/context/project_type.md        (active project type + mode adaptations)
Step 3 → packages/shared/src/contracts/     (locked Zod schemas — the ground truth)
Step 4 → .ai/plans/active/                  (current sprint + feature in progress)
Step 5 → Current filesystem state           (what actually exists right now)
Step 6 → .ai/memory/                        (decisions, lessons, project-context; user-learning-profile + learning-progress for teaching/tone)
Step 7 → .ai/templates/                     (available scaffolds)
```

**Rule:** Never skip steps. Never reorder. Step 0 is mandatory — anti-patterns are injected as hard constraints before any other context loads. If a step is empty, note it and continue.

### Step 0 — Anti-Pattern Scan (new, runs first)
```
Load: .ai/memory/anti_patterns.md
Filter: entries matching current agent type + task type + domain
Inject: matched patterns as CONSTRAINTS into task context
Block: CRITICAL patterns require explicit human confirmation to proceed
Result: @ContextSlicer outputs the constraint list before any code generation begins
See: .ai/skills/lesson_injection.md for the full injection algorithm
```

## Step-by-Step Execution

### Step 1 — Global Architecture Rules
```
Read: .ai/context/architecture.md
Extract:
  - Technology stack (Next.js 15, Hono, Prisma, pnpm, Turborepo)
  - Naming conventions
  - Package boundaries (what imports what)
  - Quality gate order
  - Zero-trust security baseline
```

### Step 2 — Project-Type Context
```
Read: .ai/context/project_type.md
Extract:
  - project_type: [web | mobile | fullstack | gov-tech | hospitality | ...]
  - mode: [founder | pro | hybrid]
  - initialized: [true | false]
  - Active apps and their frameworks
  - Branching strategy
```

### Step 3 — Active Contracts
```
Read: packages/shared/src/contracts/
Extract for each locked domain:
  - Schema fields and types
  - Lock state + fingerprint
  - Version number
  - Any pending breaking changes
```

### Step 4 — Active Plans (SDD default: phase → spec)
```
Read: .ai/plans/active/current_sprint.md
Read: .ai/plans/active/features/[phase]/manifest.md     (when present — phase coordination)
Read: .ai/plans/active/features/[phase]/[spec]/plan.md (primary — user story, AC + IDs, Data Shape)
Then as task requires (compressed):
  contracts.md, api.md, database.md, design.md, context.md, structure.md, prompt.md
Extract:
  - Sprint goal and acceptance criteria (from plan.md + sprint file)
  - Current step in the plan
  - Assigned agents and status
  - Blockers
```
**SDD detail:** See **`.ai/skills/sdd_spec_workflow.md`**. **Legacy:** a single flat **`.ai/plans/active/features/[name].md`** may still exist — load it only when the sprint explicitly points there or the user is migrating (`/plan --legacy`).

### Step 5 — Filesystem State
```
Check: Does the file/component/route I need to create already exist?
Check: What packages are installed (package.json)?
Check: What DB migrations have run?
Check: What tests exist?
```

### Step 6 — Memory (Past Decisions + Learner Context)
```
Read: .ai/memory/decisions.md               → Architecture choices + rationale
Read: .ai/memory/lessons_learned.md         → What went wrong + fixes
Read: .ai/memory/project_context.md       → Persistent project state
Read (onboarding, /init, teaching): .ai/memory/user_learning_profile.md → Expertise, study queue, session notes
Read (onboarding, teaching): .ai/memory/learning_progress.md            → Concepts checklist (@Tutor)
```

### Step 7 — Templates
```
Read: .ai/templates/
Check if a scaffold exists for:
  - The component/feature type being built
  - The test pattern needed
  - The PR/ADR format required
```

## Context Slice Output Format

After loading, `@ContextSlicer` produces a compressed context slice:

```markdown
## Active Context Slice — [Feature Name] — [Date]

**Project:** [Name] | **Type:** [web/fullstack/etc] | **Mode:** [founder/pro]
**Sprint:** [N] | **Step:** [X.Y] | **Agent:** [@AgentName]

**Relevant Contracts:**
- booking.ts (locked v1.2 | 13 fields) ✅
- payment.ts (UNLOCKED — blocks build) ❌

**Active Feature:** [feature-name]
**Current Task:** [task description]
**Next Task:** [next task]
**Blockers:** [list or none]

**Relevant Past Decisions:**
- [Decision 1 — rationale]

**Available Templates:**
- [Template name → path]
```

## Token Budget by Agent Tier
```
Leadership (@Guide, @Architect, @Founder): 8,000 tokens
Execution  (@Frontend, @Backend, @DBA):    6,000 tokens
QA/Quality (@QA, @Reviewer, @Security):    4,000 tokens
Support    (@Content, @DesignSystem):       3,000 tokens
```

`@ContextSlicer` ensures no agent exceeds its budget by trimming lower-priority steps first (Step 7 → Step 6 → Step 5 in descending priority when tight).

## Common Mistakes
- Skipping Step 3 and building against a stale or unlocked contract
- Not checking Step 4 — missing the active plan step leads to duplicate or out-of-order work
- Ignoring Step 6 — repeating solved problems from previous sprints
- Loading all memory at full resolution — use `@ContextSlicer` for budget-aware slicing

## Success Criteria
- [ ] All 8 steps executed in order before task begins (Step 0 anti-patterns + Steps 1–7)
- [ ] Active contracts confirmed as locked
- [ ] Current sprint step identified
- [ ] Token budget not exceeded for agent tier
- [ ] Output references: `Active Plan Step | Contract | Template | Project Type | Agent`