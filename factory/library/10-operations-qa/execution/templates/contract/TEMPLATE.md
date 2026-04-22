# Contract Template: [Domain]

> **Domain:** [domain-name]
> **Version:** 1.0.0
> **Status:** [draft | locked | deprecated]
> **Created:** [YYYY-MM-DD]
> **Created by:** @Architect

---

## Zod Schema

```typescript
// packages/shared/src/contracts/[domain].ts
import { z } from 'zod'

// ── Base Schema ──
export const [Domain]Schema = z.object({
  id: z.string().uuid(),
  createdAt: z.string().datetime(),
  updatedAt: z.string().datetime(),

  // Add domain-specific fields below
  // Example:
  // title: z.string().min(1).max(200),
  // status: z.enum(['draft', 'published', 'archived']),
  // userId: z.string().uuid(),
})

// ── Operation Schemas ──

// Create: omit auto-generated fields
export const Create[Domain]Schema = [Domain]Schema.omit({
  id: true,
  createdAt: true,
  updatedAt: true,
})

// Update: require id, all other fields optional
export const Update[Domain]Schema = [Domain]Schema.partial().required({
  id: true,
})

// Query: for filtering/listing
export const [Domain]QuerySchema = z.object({
  // Add query filters
  // Example:
  // status: [Domain]Schema.shape.status.optional(),
  // userId: z.string().uuid().optional(),
  page: z.number().int().min(1).default(1),
  pageSize: z.number().int().min(1).max(100).default(20),
})

// ── Inferred TypeScript Types ──

export type [Domain]Type = z.infer<typeof [Domain]Schema>
export type Create[Domain]Type = z.infer<typeof Create[Domain]Schema>
export type Update[Domain]Type = z.infer<typeof Update[Domain]Schema>
export type [Domain]QueryType = z.infer<typeof [Domain]QuerySchema>
```

---

## Usage Examples

### Backend Validation
```typescript
import { Create[Domain]Schema } from '@sovereign/contracts/[domain]'

app.post('/api/[domain-plural]', async (c) => {
  const body = await c.req.json()
  const data = Create[Domain]Schema.parse(body)
  // data is fully typed — use it safely
})
```

### Frontend Form (React Hook Form + Zod Resolver)
```typescript
import { zodResolver } from '@hookform/resolvers/zod'
import { Create[Domain]Schema } from '@sovereign/contracts/[domain]'
import { useForm } from 'react-hook-form'

const form = useForm<Create[Domain]Type>({
  resolver: zodResolver(Create[Domain]Schema),
  defaultValues: { /* ... */ }
})
```

### Database Schema (Prisma)
```prisma
model [DomainInSnakeCase] {
  id          String   @id @default(cuid())
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt

  // Add fields matching Zod schema
  // @@index([userId])  // Index foreign keys
}
```

---

## Lock File Format

```json
// packages/shared/src/contracts/.lock/[domain].lock.json
{
  "domain": "[domain]",
  "version": "1.0.0",
  "lockedAt": "[YYYY-MM-DDTHH:MM:SSZ]",
  "lockedBy": "@Architect",
  "fingerprint": "sha256:[hash]",
  "fields": [N],
  "breakingChange": false
}
```

---

## Breaking Change Protocol

1. Create new version: `[domain].v2.ts`
2. @Architect reviews diff and approves
3. @DBA writes zero-downtime migration (expand → backfill → contract)
4. Run `/contract lock [domain].v2`
5. Update all consumers in a single PR
6. Archive old version after 1 sprint

---

*Template Version: 1.0 | Maintained by: @Architect | All contracts must follow this structure*
