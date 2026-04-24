---
type: Command
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---


# /contract — Auto-Generate & Audit

> **SDD default:** Contracts are **generated automatically** from the confirmed spec **`Data Shape`** in **`.ai/plans/active/features/[phase]/[spec]/plan.md`**, mirrored in **`contracts.md`**, then synced to **`packages/shared/src/contracts/[domain].ts`**. Use this command for **manual overrides**, **audits**, **diff/history**, or **legacy** flat **`features/[id]/plan.md`** migrations.

## Syntax

```
/contract                           → Default: read confirmed spec → generate/update Zod → validate → lock (all touched domains)
/contract auto [phase]/[spec]         → Same as bare /contract when id omitted (active spec)
/contract create [domain]         → Manual: create new Zod schema (override / legacy)
/contract validate [domain]       → Validate existing schema
/contract lock [domain]           → Lock schema (required before /build if not already locked)
/contract diff [domain]           → Show changes since last lock
/contract history [domain]        → Show version history
/contract unlock [domain]         → Unlock for modification (requires @Architect)
/contract list                    → List all contracts + lock states
/contract sync [phase]/[spec]   → Re-run **contract:auto-generate** + **contract:auto-validate** only (e.g. after `/plan --no-sos`) without regenerating **`prompt.md`**
```

## Primary agents

`@ContractLock` (auto pipeline, validate, lock) · `@Architect` (manual create, drift approval, spec clarification when auto-gen fails)

## SDD auto pipeline (default)

1. Load **confirmed** **`plan.md`** (and **`contracts.md`** stub/summary) for **`[phase]/[spec]`** (or legacy flat path): User Story, Acceptance Criteria, **Data Shape**, Edge Cases.
2. If `spec:validate` would fail (missing/ambiguous AC or Data Shape) → stop; return control to `@Architect` / `@Founder` for clarification — **no Zod write**.
3. Map Data Shape → update **`contracts.md`** + Zod in `packages/shared/src/contracts/[domain].ts` (create or update).
4. Run validation (TypeScript + Zod integrity + cross-references).
5. Fingerprint and **lock** in **`.contract-locks.json`** at the **repository root** (file is **created on first lock** — not required in bare clones).
6. Notify `@Router` that execution agents may proceed for those domains.

## Manual: /contract create [domain]

`@Architect` (or Pro operator) authors a complete Zod schema when auto-gen is insufficient:

```typescript
// packages/shared/src/contracts/[domain].ts
import { z } from 'zod'

// 1. Enums
export const [Domain]StatusSchema = z.enum(['PENDING', 'ACTIVE', 'ARCHIVED'])

// 2. Base schema (shared fields)
const [Domain]Base = z.object({ ... })

// 3. Operation-specific schemas
export const [Domain]CreateSchema = [Domain]Base.omit({ status: true })
export const [Domain]UpdateSchema = [Domain]Base.partial()
export const [Domain]Schema = [Domain]Base.extend({ id, createdAt, updatedAt })
export const [Domain]ListSchema = z.array([Domain]Schema)

// 4. Inferred types
export type [Domain]Status = z.infer<typeof [Domain]StatusSchema>
export type [Domain]Type = z.infer<typeof [Domain]Schema>
export type [Domain]CreateType = z.infer<typeof [Domain]CreateSchema>
export type [Domain]UpdateType = z.infer<typeof [Domain]UpdateSchema>
```

### /contract validate [domain]

`@ContractLock` runs:

1. TypeScript compilation check  
2. Zod schema validity  
3. Inferred type completeness  
4. Cross-contract reference check  
5. API endpoint compliance (if routes exist)

### /contract lock [domain]

- Generates SHA-256 fingerprint of schema + types  
- Writes to **`.contract-locks.json`** (repo root)  
- Marks status = LOCKED in feature plan  
- Notifies `@Router` that execution agents can proceed  

### /contract diff [domain]

Shows what changed since last lock:

```
Contract: booking.ts
Last locked: 2026-04-01 (v1.0.0)
Changes detected:
  + Added: price: z.number().positive() (new required field)
  ~ Changed: status default 'DRAFT' → 'PENDING'
  - Removed: notes: z.string().optional()

Impact: @Frontend, @Backend, @QA all affected
Action: Update lock version, notify affected agents
```

## Enforcement rules

- `@Router` checks lock state before routing ANY execution agent.  
- CI / Turborepo: **`contract:auto-validate`** is implemented by the existing `contract:validate` task where present (Zod + locks); **`spec:validate`** is enforced at plan time in AI workflows.  
- Contract changes require re-lock before next `/build`.  
- Breaking changes (removing fields) require `@Architect` approval + version bump.  

## /contract list output

```
Contract Status Report:
├── auth.ts         🔒 LOCKED v1.2.0 (2026-04-01)
├── booking.ts      🔒 LOCKED v1.0.0 (2026-04-05)
├── payment.ts      🔓 UNLOCKED — DRAFT (blocks @Frontend, @Backend)
└── user.ts         🔒 LOCKED v2.1.0 (2026-03-20)

⚠️ payment.ts must be locked before booking-flow Sprint Task T-005
Action: /contract lock payment → @Router unblocks execution agents
```

---

*Invokes: @ContractLock (auto + validate + lock), @Architect (manual create / clarifications)*
