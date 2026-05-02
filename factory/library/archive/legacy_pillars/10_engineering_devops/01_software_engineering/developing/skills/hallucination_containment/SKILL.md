---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# Hallucination Containment

## Purpose
Prevent agents from inventing APIs, contract fields, or system behaviors that don't exist. Every claim an agent makes must be verifiable against the filesystem, locked contracts, or loaded memory. Unverified output blocks downstream work.

## Sources of Hallucination

```
1. Stale training data — agent "remembers" old API versions
2. Context gap — agent doesn't load current filesystem state (skipped Step 5 of DMP)
3. Assumption creep — agent assumes a field exists without checking the contract
4. Memory drift — agent uses outdated .ai/memory/ without verifying against current state
5. Pattern confusion — applying a pattern from a different project type
```

## Prevention Protocol (Before Code Generation)

```markdown
## Pre-Generation Verification Checklist

Before writing any implementation code, verify:

1. CONTRACT CHECK
   - [ ] Load the locked contract: packages/shared/src/contracts/[domain].ts
   - [ ] Confirm every field referenced in my output EXISTS in the schema
   - [ ] Confirm field types match (string, number, enum values)
   - [ ] Confirm the contract is LOCKED (check .lock file exists)

2. FILESYSTEM CHECK
   - [ ] Does the file I'm modifying already exist?
   - [ ] Does the function/component I'm calling already exist?
   - [ ] Does the import path I'm using exist in packages/?

3. API REFERENCE CHECK
   - [ ] Load architecture.md for tech stack versions
   - [ ] If using a library (Hono, Prisma, Zod) — verify method signature exists
   - [ ] Don't assume a method exists — check the actual package version in pnpm-workspace.yaml

4. MEMORY CHECK
   - [ ] Does .ai/memory/decisions.md contradict what I'm about to do?
   - [ ] Does .ai/memory/lessons_learned.md show this approach has failed before?
```

## Verification Pattern (Agent Self-Check)

```markdown
## Agent Verification Statement
(Include at top of every substantive code output)

Verified against:
- Contract: packages/shared/src/contracts/booking.ts (locked v1.2) ✅
- Tech stack: Hono v4.7, Prisma v6.6, Zod v3.24 (from pnpm-workspace.yaml) ✅
- Filesystem: apps/api/src/routes/bookings.ts EXISTS ✅
- Memory: No conflicting decisions in .ai/memory/decisions.md ✅

Assumptions made (MUST be flagged):
- Assumed prisma.booking.findMany supports `cursor` pagination — NEEDS VERIFICATION
- Assumed @workspace/logger is installed — NEEDS VERIFICATION

Action required:
- @Reviewer: please verify the assumptions above before merging
```

## @Reviewer Rejection Criteria

```markdown
## Rejection Triggers

Reject any agent output that:

1. References a contract field that doesn't exist in the locked schema
   Example: agent uses `booking.guestEmail` but schema has `booking.guestId` only

2. Calls a library method that doesn't exist in the installed version
   Example: agent uses `prisma.booking.upsert()` but Prisma v5 changed the signature

3. Imports from a package not in pnpm-workspace.yaml
   Example: import { something } from '@workspace/notifications' — doesn't exist yet

4. Contradicts a locked architecture decision
   Example: uses REST when ADR-001 specified tRPC for this module

5. Uses API patterns from older library versions
   Example: Hono v3 patterns in a Hono v4 codebase

6. References a file that doesn't exist
   Example: import { Button } from '@workspace/ui/components/Button' — file not created yet
```

## Correction Protocol

```markdown
## When Hallucination Is Detected

1. STOP — do not continue building on hallucinated foundation
2. IDENTIFY — what specifically is wrong (field name, method signature, import)
3. VERIFY — load the actual source of truth (contract, package docs, filesystem)
4. CORRECT — rewrite only the affected section with verified information
5. FLAG — note the correction in agent output so @Reviewer knows what changed
6. REMEMBER — if the hallucination pattern is recurring, add to lessons_learned.md
```

## High-Risk Hallucination Zones

```
HIGH RISK — always verify:
- Prisma query method signatures (changed significantly v5→v6)
- Next.js App Router APIs (changed in v14/v15)
- Zod method chains (.nullable vs .optional vs .nullish)
- Hono context methods (c.req.valid vs c.req.json)
- pnpm catalog package names (typos create wrong imports)

MEDIUM RISK — verify if uncertain:
- shadcn/ui component prop names (updated frequently)
- next-intl API (v3→v4 had breaking changes)
- Tailwind CSS v4 (significant changes from v3)

LOW RISK — generally stable:
- JavaScript/TypeScript language features
- HTTP status codes
- Standard REST patterns
- UUID format
```

## Common Mistakes
- Skipping Step 5 of Dynamic Memory Protocol (filesystem state) — most common hallucination source
- Assuming a package is installed without checking pnpm-workspace.yaml
- Using documentation examples without checking the version against the catalog
- Not flagging assumptions — silent assumptions become bugs

## Success Criteria
- [ ] Pre-generation verification checklist completed before every code output
- [ ] All contract references verified against locked schema
- [ ] All library method calls verified against installed versions
- [ ] Assumptions explicitly flagged for @Reviewer
- [ ] Zero hallucinated fields/methods in merged code