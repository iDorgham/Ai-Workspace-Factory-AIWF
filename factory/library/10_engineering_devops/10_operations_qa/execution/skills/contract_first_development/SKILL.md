---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# Contract-First Development

## Purpose
Define the data shape (Zod schema) **before** any implementation code. The contract is the single source of truth for all API inputs/outputs, form validations, DB shapes, and frontend types.

## Relationship to SDD (Spec-Driven Development)
Sovereign’s default methodology (**`sovereign-default`** ≡ **`sdd`**) stores the **human planning truth** under **`.ai/plans/active/features/[phase]/[spec]/`**, especially **`plan.md`** (**User Story**, **AC**, **Data Shape**). After confirmation, **`contract:auto-*`** produces Zod in **`packages/shared/src/contracts/`** and planning **`contracts.md`**. This skill covers **how to write and lock** those Zod files; **`.ai/skills/sdd_spec_workflow.md`** covers **where specs live**, **SOS `prompt.md`**, and **phase `manifest.md`**. Under **CFG** (`contract` / `contract-first`), teams still use the same tree but stress **manual `/contract`** checkpoints — document in **`development_methodology.notes`**.

## When to Activate
- Before writing any API endpoint
- Before creating a database table or migration
- Before building a form or UI component that submits data
- Before any `/build` or `/swarm` command
- When a new domain is introduced to the workspace

## Step-by-Step Execution

### 1. Create the contract file
```bash
# Location: packages/shared/src/contracts/[domain].ts
# Naming: [Domain]Schema (Zod) + [Domain]Type (inferred TS)
```

### 2. Write the Zod schema
```typescript
// packages/shared/src/contracts/booking.ts
import { z } from 'zod'

export const BookingSchema = z.object({
  id:          z.string().uuid(),
  guestId:     z.string().uuid(),
  venueId:     z.string().uuid(),
  type:        z.enum(['table', 'room', 'activity', 'class']),
  startsAt:    z.string().datetime(),
  endsAt:      z.string().datetime(),
  partySize:   z.number().int().min(1).max(500),
  status:      z.enum(['pending', 'confirmed', 'cancelled', 'no-show']),
  totalAmount: z.number().nonnegative(),
  currency:    z.enum(['EGP', 'USD', 'EUR', 'SAR']),
  notes:       z.string().max(500).optional(),
  createdAt:   z.string().datetime(),
  updatedAt:   z.string().datetime(),
})

// Partials for create/update operations
export const CreateBookingSchema = BookingSchema.omit({ id: true, createdAt: true, updatedAt: true })
export const UpdateBookingSchema = BookingSchema.partial().required({ id: true })
export const BookingQuerySchema  = z.object({
  venueId:  z.string().uuid().optional(),
  guestId:  z.string().uuid().optional(),
  status:   BookingSchema.shape.status.optional(),
  from:     z.string().datetime().optional(),
  to:       z.string().datetime().optional(),
  page:     z.number().int().min(1).default(1),
  pageSize: z.number().int().min(1).max(100).default(20),
})

// Inferred TypeScript types — never write these manually
export type BookingType        = z.infer<typeof BookingSchema>
export type CreateBookingType  = z.infer<typeof CreateBookingSchema>
export type UpdateBookingType  = z.infer<typeof UpdateBookingSchema>
export type BookingQueryType   = z.infer<typeof BookingQuerySchema>
```

### 3. Lock the contract
```bash
/contract lock booking
# @ContractLock generates SHA-256 fingerprint + sets lock state = TRUE
# Stores in: packages/shared/src/contracts/.lock/booking.lock.json
```

### 4. Validate before every build
```bash
/contract validate
# Runs: contract:validate Turborepo task
# Fails if: schema changed after lock without /contract lock re-run
```

### 5. Use in implementation
```typescript
// Backend (Hono/NestJS) — validate at boundary
import { CreateBookingSchema } from '@workspace/shared/contracts/booking'

app.post('/api/bookings', async (c) => {
  const body = await c.req.json()
  const data = CreateBookingSchema.parse(body) // throws ZodError on invalid
  // ...
})

// Frontend (Server Action / React Hook Form)
import { zodResolver } from '@hookform/resolvers/zod'
import { CreateBookingSchema } from '@workspace/shared/contracts/booking'

const form = useForm({ resolver: zodResolver(CreateBookingSchema) })
```

## Contract Lock File Format
```json
{
  "domain": "booking",
  "version": "3.3.1",
  "lockedAt": "2026-04-08T10:00:00Z",
  "lockedBy": "@Architect",
  "fingerprint": "sha256:a3f9c2...",
  "fields": 13,
  "breakingChange": false
}
```

## Enforcement Rules
- `@ContractLock` blocks all `/build` and `/swarm` commands until lock state = TRUE
- `contract:validate` Turborepo task runs before every `build` task
- Breaking changes (removing/renaming fields) require `@Architect` sign-off
- All API inputs/outputs MUST reference a contract type — no `any`, no raw `object`
- Frontend forms MUST use `zodResolver` with the contract schema

## Breaking Change Protocol
```
1. Create new contract version: booking.v2.ts
2. @Architect reviews + approves the diff
3. @DBA writes zero-downtime migration (expand → backfill → contract)
4. /contract lock booking.v2
5. Update all consumers in a single PR
6. Archive booking.v1.ts after 1 sprint
```

## Common Mistakes
- Writing implementation first then "retrofitting" a schema — always schema first
- Using `z.any()` or `object` types — defeats the entire contract system
- Forgetting `omit` for create/update partials — every API operation needs its own schema
- Not exporting inferred TypeScript types — downstream code needs them
- Editing a locked contract without running `/contract lock` again

## Success Criteria
- [ ] Schema defined in `packages/shared/src/contracts/[domain].ts`
- [ ] Create / Update / Query schemas derived from base
- [ ] TypeScript types exported as inferred (`z.infer<>`)
- [ ] Contract locked (`.lock/[domain].lock.json` exists)
- [ ] `contract:validate` passes in CI
- [ ] Both frontend (resolver) and backend (parse) reference the same schema