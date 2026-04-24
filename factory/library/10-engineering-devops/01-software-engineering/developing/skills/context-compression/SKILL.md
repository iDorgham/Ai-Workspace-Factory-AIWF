---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# Context Compression

## Purpose
Slash token usage by 60–80% through intelligent context compression without losing information quality. Raw files are expensive. Compressed slices are cheap. Same agent intelligence, 4× fewer tokens.

---

## Compression Techniques

### Technique 1 — Schema Field Filtering
Instead of loading the full contract, load only fields relevant to the current task.

```markdown
## FULL CONTRACT (expensive — ~800 tokens)
export const BookingSchema = z.object({
  id: z.string().uuid(),
  guestId: z.string().uuid(),
  venueId: z.string().uuid(),
  checkIn: z.date(),
  checkOut: z.date(),
  adults: z.number().int().min(1).max(20),
  children: z.number().int().min(0).max(10),
  status: z.enum(['pending','confirmed','cancelled','completed']),
  totalPrice: z.number().positive(),
  currency: z.enum(['USD','EUR','EGP']),
  specialRequests: z.string().optional(),
  createdAt: z.date(),
  updatedAt: z.date(),
  confirmedBy: z.string().uuid().optional(),
  cancelledAt: z.date().nullable(),
})

## COMPRESSED — @Frontend BookingCard task (~120 tokens)
Contract: booking.ts (locked v1.3)
Task-relevant fields: id, guestId, status, checkIn, checkOut, totalPrice, currency
Omitted: adults, children, specialRequests, confirmedBy, cancelledAt (not displayed in card)
```

**Savings: 85% fewer tokens for the contract alone.**

---

### Technique 2 — Architecture Subset Extraction
Never load the full architecture.md. Extract only the section relevant to the current task.

```markdown
## FULL architecture.md loads (~1,500 tokens)
## COMPRESSED subset for @Frontend task (~200 tokens)

Architecture subset — @Frontend:
- Framework: Next.js 15 App Router, RSC preferred
- Styling: Tailwind CSS v4 + CSS variables (tokens.css)
- Components: shadcn/ui → packages/ui → apps/web (never skip the chain)
- i18n: next-intl, all text via t('key')
- State: Zustand for client state, RSC for server state
[DB, Auth, API, CI/CD sections omitted — not relevant for UI task]
```

**Savings: 87% fewer tokens for architecture context.**

---

### Technique 3 — Memory Staleness Filter
Don't load all memory. Apply a staleness + relevance filter.

```markdown
## Memory Filter Algorithm

Load from .ai/memory/ only entries where:
  1. Age: written within last 3 sprints (not older)
  2. Domain match: same domain as current task (booking / auth / payment)
  3. Agent match: relevant to current agent type
  4. Severity: LESSONS rated HIGH or CRITICAL (skip LOW unless exact domain match)

## Result: instead of loading 6,000-token memory files
## Agent receives 300–500 tokens of directly relevant lessons
```

---

### Technique 4 — Reference Notation (Don't Copy, Point)
Instead of embedding large content, use pointer notation and let agents pull on demand.

```markdown
## Instead of embedding full skill content (~400 tokens each):
skill: shadcn-atomic-design.md    → use button variants, not raw HTML
skill: playwright-e2e.md          → use page objects, not raw locators
skill: owasp-zero-trust.md        → validate all inputs at route layer

## Agent knows WHERE to look if it needs details
## Most tasks don't need the full skill — saving ~1,200 tokens per task
```

---

### Technique 5 — Differential Context (Incremental Loads)
On second and subsequent tasks in a session, load only what changed since the last task.

```markdown
## Session Cache (maintained by @ContextSlicer)

On task 1: Load full context slice → cache all loaded items with hash
On task 2+:
  - Check: has architecture.md changed since task 1? (hash match)
    - NO → use cached version (0 tokens)
    - YES → reload changed sections only
  - Check: has the contract changed?
    - NO → use cached version (0 tokens)  
    - YES → reload contract, update hash

## Sprint savings: architecture.md loaded ONCE instead of once per task
## If 10 tasks in a sprint: saves 9 × 1,500 = 13,500 tokens
```

---

### Technique 6 — Response Format Compression
Agents produce outputs in compressed formats unless detail is explicitly requested.

```markdown
## Response Format Rules

For STATUS reports:
  Compressed: "✅ Step 4.2 done | 🔄 4.3 in progress | ⏳ 4.4 queued"
  NOT this: "Step 4.2 has been successfully completed. Step 4.3 is currently in progress. Step 4.4 is queued and waiting..."

For CODE REVIEW:
  Compressed: "AP-003 violation: line 24 — use ms-4 not ml-4 | AP-011: line 31 — use var(--color-primary) not #1a2b3c"
  NOT this: "On line 24 of the file, I noticed that you are using the margin-left class which violates our design system guidelines..."

For ROUTING DIRECTIVES:
  Compressed table format (as in router.md) — never prose

For ERROR REPORTS:
  Use the capture format in mistake-prevention-system.md — structured, not narrative

Rule: if something can be expressed in a table or a list, it must not be prose.
```

---

### Technique 7 — Lazy Loading Pattern
Load context only when the specific sub-task that needs it begins.

```markdown
## Lazy Load Decision Tree

Starting a /swarm run on "booking-flow" feature:

IMMEDIATE LOAD (all agents need this):
  - Booking contract (locked)
  - Current plan step
  - Anti-pattern scan results

LAZY LOAD (load when that agent's Group begins):
  - DB schema details → load when @DBA task starts
  - Playwright config → load when @QA E2E task starts
  - CI/CD config → load when @Automation task starts
  - Brand tokens → load when @Frontend visual task starts

## Savings: 40–60% of context never loaded for agents that don't need it
```

---

## Compression Report Format

```markdown
## @ContextSlicer — Compression Report
**Task:** [name] | **Agent:** @[name] | **Date:** YYYY-MM-DD

| Content Item | Raw Size | Compressed | Saved | Method |
|-------------|---------|-----------|-------|--------|
| architecture.md | 1,500 tok | 180 tok | 88% | Subset extraction |
| booking.ts contract | 820 tok | 95 tok | 88% | Field filtering |
| decisions.md | 2,200 tok | 310 tok | 86% | Staleness filter |
| lessons-learned.md | 1,800 tok | 240 tok | 87% | Domain + recency filter |
| skills (3 loaded) | 1,200 tok | 120 tok | 90% | Pointer notation |
| **TOTAL** | **7,520 tok** | **945 tok** | **87%** | |

**Context Retention Index (CRI): 97%** (estimated — validated after task)
```

---

## When NOT to Compress

```
Do NOT compress:
- The active locked contract fields the agent is directly implementing
- Specific error messages being debugged
- Security scan results (must be complete)
- Explicit user requirements from the plan step
- Anything @Reviewer needs to validate the output

Always compress:
- Architecture sections unrelated to the current task
- Memory entries older than 3 sprints
- Skills not directly activated for this task
- Other agents' tasks and outputs
```

## 🌍 Regional Calibration (MENA Context)

- **Cultural Alignment:** Ensure all logic respects regional business etiquette and MENA market expectations.
- **RTL Compliance:** Logic must explicitly handle Right-to-Left (RTL) flow where relevant.

## 🛡️ Critical Failure Modes (Anti-Patterns)

- **Anti-Pattern:** Generic Output -> *Correction:* Apply sector-specific professional rules from RULE.md.
- **Anti-Pattern:** Global-Only Logic -> *Correction:* Verify against MENA regional calibration.

---

## Target Metrics

```
Per-task context: ≤ 2,000 tokens for Coordination agents, ≤ 4,000 for Execution agents
Session cache hit rate: ≥ 70% (most items should come from cache after task 1)
CRI target: ≥ 95% (compression doesn't degrade output quality)
Sprint token savings vs naive loading: ≥ 60%
```

## Success Criteria
- [ ] @ContextSlicer produces compression report with every task slice
- [ ] Session cache active and tracking item hashes
- [ ] No agent receives full architecture.md unless explicitly needed
- [ ] Response format compression applied (tables/lists over prose)
- [ ] Cache hit rate tracked per sprint by @MetricsAgent