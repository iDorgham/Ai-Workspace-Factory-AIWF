---
type: Generic
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# Compound Engineering

## Purpose
Each sprint's work becomes a reusable asset for the next. Verified patterns, tested contracts, and resolved problems are captured in memory — so the team never solves the same problem twice. Knowledge compounds across projects.

## The Compound Loop

```
Sprint N → Solve problem X
    ↓
@RetroFacilitator extracts the solution pattern
    ↓
Pattern stored in .ai/memory/ or .ai/templates/
    ↓
Sprint N+1 → Problem X variant appears
    ↓
@ContextSlicer loads relevant memory
    ↓
Agent applies known pattern (faster, fewer errors)
    ↓
New variant extends the pattern
    ↓
Repeat → knowledge grows non-linearly
```

## What Gets Captured

### 1. Verified Code Patterns (Templates)
```
When a pattern has been:
  ✅ Implemented
  ✅ Tested (≥90% coverage)
  ✅ Reviewed by @Reviewer
  ✅ Deployed successfully

→ Extract to .ai/templates/[domain]/[pattern].md
```

**Example:** A booking creation flow that works perfectly becomes `booking_create_pattern.md` — ready to copy for restaurant bookings, hotel bookings, activity bookings, etc.

### 2. Architecture Decisions (ADRs)
```typescript
// .ai/memory/decisions.md — every significant "why" is logged
// Format: ADR-[number] | [date] | [status]

## ADR-001 — Use Hono over Express for API
Date: 2026-04-08
Status: ACCEPTED

Context:
  Needed a lightweight, TypeScript-first web framework for the API.
  Express is well-known but verbose TypeScript support.

Decision:
  Use Hono v4 for all API apps.

Rationale:
  - Built-in TypeScript types, excellent DX
  - 3-5× faster than Express in benchmarks
  - zValidator middleware integrates with Zod contracts natively
  - Same API style works on Edge and Node.js

Consequences:
  - Slightly smaller community than Express
  - Migration path to Fastify is straightforward if needed
  - All API agents default to Hono patterns
```

### 3. Lessons Learned
```markdown
# .ai/memory/lessons_learned.md

## L-001 — RTL Testing Must Include Arabic Text Length
Sprint: 2 | Date: 2026-04-08

Lesson:
  Arabic words are often longer than English equivalents.
  "Bookings" (8 chars) = "الحجوزات" (9 chars but wider display width).
  This caused table column overflow in RTL mode that wasn't caught
  because visual tests used placeholder text, not real Arabic.

Fix Applied:
  All visual regression tests now use real Arabic translation strings,
  not Lorem Ipsum or placeholder text.

Applies To: @VisualQA, @I18n, @Frontend
```

### 4. Domain Contracts as Reusable Starting Points
```typescript
// Once booking.ts is verified for a venue project,
// it becomes the starting contract for the next hospitality project.
// New project → copy → adjust for new domain → lock.
// No re-designing from scratch.
```

## Template Extraction Protocol

```markdown
## Template Extraction Checklist

Trigger: After any pattern is used successfully in 2+ places OR explicitly after a sprint retro

For each extractable pattern:
1. [ ] Name the pattern clearly: [domain]-[operation]-pattern.md
2. [ ] Document: inputs, outputs, dependencies, constraints
3. [ ] Include working code examples (copy-paste ready)
4. [ ] Include test examples (unit + integration)
5. [ ] Note: what project types this applies to
6. [ ] Note: what to customize per project
7. [ ] Save to: .ai/templates/[category]/[name].md
8. [ ] Reference in: .ai/memory/decisions.md (if architectural)
9. [ ] Update: .ai/context/skills_framework.md if it's a new capability
```

## Memory Update Protocol (Post-Sprint)

```bash
# @RetroFacilitator runs after every sprint close

1. Review git log for this sprint
2. For each significant commit:
   - Was a problem solved that could recur? → lessons_learned.md
   - Was a reusable pattern created? → templates/
   - Was an architecture decision made? → decisions.md
   - Was a performance insight gained? → project_context.md

3. Update project_context.md:
   - Current project state (what's built, what's pending)
   - Active technical constraints
   - Vendor choices + rationale

4. Calibrate agent definitions:
   - Did any agent repeatedly struggle? → update .ai/agents/[agent].md
   - Did a new agent type seem needed? → create it
```

## Knowledge Compounding in Practice

```markdown
## Project Sequence Example (Hurghada Portfolio)

Project 1: Coral Terrace Restaurant
  → Solved: booking flow, RBAC, Egyptian payment integration
  → Captured: booking_create_pattern.md, payment_egypt.md, rbac_setup.md

Project 2: Blue Lagoon Dive School
  → Reused: booking_create_pattern.md (saved 2 sprints)
  → Adapted: activity_scheduling_pattern.md (extends booking)
  → New: equipment_rental_contract.md
  → Captured: activity_scheduling_pattern.md, equipment_rental.md

Project 3: Pearl Beach Club
  → Reused: booking_create_pattern.md, activity_scheduling_pattern.md
  → New: membership_tier_system.md, vip_table_booking.md
  → Sprint 1 delivered in 60% of normal time (compound effect)

By Project 4: Sovereign workspace delivers features at 2-3× initial speed.
```

## Common Mistakes
- Extracting patterns before they're verified (tested + deployed) — broken patterns spread
- Capturing "what" without "why" — future agents can't judge when to apply the pattern
- Over-generalizing patterns — "universal booking" that actually only fits one domain
- Not updating memory after failed approaches — negative knowledge is also valuable
- Letting .ai/memory/ grow stale — outdated decisions mislead more than help

## Success Criteria
- [ ] .ai/memory/decisions.md updated after every architectural decision
- [ ] .ai/memory/lessons_learned.md updated after every sprint retro
- [ ] .ai/templates/ grows by at least 1 template per sprint
- [ ] @ContextSlicer loads relevant memory before each task
- [ ] Sprint velocity improves over time (tracked by @MetricsAgent)