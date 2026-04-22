# Prisma Advanced Patterns

## Client Singleton (Correct Pattern)

```typescript
// packages/shared/src/lib/prisma.ts
import { PrismaClient } from '@prisma/client'

const globalForPrisma = globalThis as unknown as { prisma: PrismaClient }

export const prisma = globalForPrisma.prisma ?? new PrismaClient({
  log: process.env.NODE_ENV === 'development'
    ? ['query', 'error', 'warn']
    : ['error'],
})

if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = prisma
// ↑ prevents multiple instances during Next.js hot reload (dev mode)
```

---

## Query Patterns

### Cursor Pagination (preferred over skip/offset)
```typescript
// Skip/offset is slow on large tables — full table scan to find the offset row
// Cursor pagination is O(log n) — only fetches from the cursor point

async function getBookingPage(cursor?: string, pageSize = 20) {
  return prisma.booking.findMany({
    take: pageSize,                                   // AP-020: always paginate
    ...(cursor && { skip: 1, cursor: { id: cursor } }),
    orderBy: { createdAt: 'desc' },
    select: {
      id: true,
      status: true,
      checkIn: true,
      checkOut: true,
      totalPrice: true,
      guest: { select: { name: true, email: true } }, // select only needed fields
    },
  })
}
```

### Select Only What You Need
```typescript
// NEVER: SELECT * in Prisma
const booking = await prisma.booking.findUnique({ where: { id } })  // ❌ loads all fields

// ALWAYS: select only what the contract requires
const booking = await prisma.booking.findUnique({
  where: { id },
  select: {
    id: true,
    status: true,
    totalPrice: true,
    currency: true,
    // confirmedBy, cancelledAt, internalNotes — NOT selected if not in response contract
  },
})
```

### Avoiding N+1 Queries
```typescript
// ❌ N+1 — one query per booking
const bookings = await prisma.booking.findMany({ take: 20 })
for (const b of bookings) {
  const guest = await prisma.user.findUnique({ where: { id: b.userId } }) // N queries
}

// ✅ One query with include
const bookings = await prisma.booking.findMany({
  take: 20,
  include: { guest: { select: { name: true, avatarUrl: true } } },
})
```

### Conditional Filters
```typescript
async function searchBookings(filters: BookingFiltersType) {
  return prisma.booking.findMany({
    where: {
      ...(filters.status && { status: filters.status }),
      ...(filters.venueId && { venueId: filters.venueId }),
      ...(filters.from && filters.to && {
        checkIn: { gte: filters.from, lte: filters.to },
      }),
      ...(filters.query && {
        OR: [
          { confirmationCode: { contains: filters.query, mode: 'insensitive' } },
          { guest: { name: { contains: filters.query, mode: 'insensitive' } } },
        ],
      }),
    },
    take: filters.limit ?? 20,
    orderBy: { createdAt: 'desc' },
  })
}
```

---

## Transactions

```typescript
// Use transactions for multi-step operations that must all succeed or all fail
async function confirmBooking(bookingId: string, staffId: string) {
  return prisma.$transaction(async (tx) => {
    // Step 1 — verify booking is in correct state
    const booking = await tx.booking.findUniqueOrThrow({
      where: { id: bookingId, status: 'pending' },
    })

    // Step 2 — update booking
    const updated = await tx.booking.update({
      where: { id: bookingId },
      data: { status: 'confirmed', confirmedBy: staffId, confirmedAt: new Date() },
    })

    // Step 3 — create audit log entry
    await tx.auditLog.create({
      data: { entityId: bookingId, action: 'booking.confirmed', actorId: staffId },
    })

    return updated
    // If ANY step throws — all three roll back automatically
  }, {
    maxWait: 5000,   // wait up to 5s for a connection (default: 2s)
    timeout: 10000,  // transaction must complete within 10s (default: 5s)
  })
}
```

---

## Soft Deletes

```typescript
// prisma/schema.prisma — add deletedAt to tables that need soft delete
model Booking {
  id        String    @id @default(uuid())
  deletedAt DateTime?           // null = active, timestamp = deleted
  // ...
}

// Prisma middleware — automatically filter soft-deleted records
prisma.$use(async (params, next) => {
  if (params.model === 'Booking') {
    if (params.action === 'findMany' || params.action === 'findFirst') {
      params.args.where = { ...params.args.where, deletedAt: null }
    }
    if (params.action === 'delete') {
      params.action = 'update'
      params.args.data = { deletedAt: new Date() }
    }
  }
  return next(params)
})
```

---

## Multi-Tenant Row Isolation (Without Supabase RLS)

```typescript
// Prisma middleware — inject tenantId into every query automatically
export function createTenantPrismaClient(tenantId: string) {
  return prisma.$extends({
    query: {
      $allModels: {
        async findMany({ args, query, model }) {
          if (TENANT_SCOPED_MODELS.includes(model)) {
            args.where = { ...args.where, tenantId }
          }
          return query(args)
        },
        async create({ args, query, model }) {
          if (TENANT_SCOPED_MODELS.includes(model)) {
            args.data = { ...args.data, tenantId }
          }
          return query(args)
        },
      },
    },
  })
}

// Usage in API route
const db = createTenantPrismaClient(c.get('tenantId'))
const bookings = await db.booking.findMany({ take: 20 })
// tenantId automatically injected — no manual WHERE clause
```

---

## Zero-Downtime Migration Checklist

Every migration @DBA produces must follow the expand-backfill-contract pattern:

```sql
-- Phase 1: EXPAND — add nullable column (safe, zero-downtime)
ALTER TABLE bookings ADD COLUMN confirmed_by UUID;

-- Phase 2: BACKFILL — populate existing rows (run as background job in batches)
-- Never: UPDATE bookings SET confirmed_by = ... (locks entire table)
UPDATE bookings
SET confirmed_by = (SELECT id FROM staff WHERE role = 'default_confirmer' LIMIT 1)
WHERE confirmed_by IS NULL AND status = 'confirmed'
LIMIT 1000;
-- Repeat until 0 rows updated

-- Phase 3: CONTRACT — add NOT NULL constraint (only after 100% rows populated)
ALTER TABLE bookings ALTER COLUMN confirmed_by SET NOT NULL;
```

### Migration File Structure
```
prisma/migrations/
  20260411000001_add_confirmed_by_to_bookings/
    migration.sql        ← forward migration (what runs)
    rollback.sql         ← reverse migration (AP-021: required)
    notes.md             ← why this change, estimated rows, risk level
```

---

## Schema Design Rules

```prisma
// Sovereign Prisma schema conventions
model Booking {
  // IDs: always UUID, never auto-increment (portable, no enumeration attack)
  id        String   @id @default(uuid())

  // Timestamps: always both, always server-generated
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  // Foreign keys: explicit relation + cascade rules defined
  userId    String
  user      User     @relation(fields: [userId], references: [id], onDelete: Cascade)

  // Enums: define in schema (Prisma validates at write time)
  status    BookingStatus @default(PENDING)

  // Monetary values: store as Integer cents, never Float
  totalPrice Int      // 1999 = $19.99 (no floating point precision issues)
  currency   String   @default("USD")

  // Indexes: add for every foreign key + every field used in WHERE/ORDER BY
  @@index([userId])
  @@index([status, createdAt])
  @@index([venueId, checkIn, checkOut])
}
```

---

## Useful Prisma CLI Commands

```bash
# Typical development workflow
pnpm prisma generate          # regenerate client after schema change
pnpm prisma migrate dev       # create + apply migration in development
pnpm prisma migrate deploy    # apply pending migrations in CI/production
pnpm prisma studio            # visual DB browser (dev only)
pnpm prisma db pull           # pull schema from existing DB (reverse engineering)
pnpm prisma validate          # validate schema before committing
pnpm prisma format            # format schema.prisma file

# Debugging
pnpm prisma migrate status    # check which migrations are applied
pnpm prisma migrate resolve   # mark a failed migration as resolved
```

## 🌍 Regional Calibration (MENA Context)

- **Cultural Alignment:** Ensure all logic respects regional business etiquette and MENA market expectations.
- **RTL Compliance:** Logic must explicitly handle Right-to-Left (RTL) flow where relevant.

## 🛡️ Critical Failure Modes (Anti-Patterns)

- **Anti-Pattern:** Generic Output -> *Correction:* Apply sector-specific professional rules from RULE.md.
- **Anti-Pattern:** Global-Only Logic -> *Correction:* Verify against MENA regional calibration.

---

## Common Mistakes

- **[PA-001]** Creating multiple `PrismaClient` instances — use the singleton pattern above
- **[PA-002]** Using `skip`/`offset` pagination on large tables — use cursor pagination
- **[PA-003]** `findMany` without `take:` — unbounded query (AP-020)
- **[PA-004]** `SELECT *` style `findMany` without `select:` — loads unused fields
- **[PA-005]** Not using transactions for multi-step operations — partial writes on failure
- **[PA-006]** `migrate deploy` with pooled DATABASE_URL — use directUrl for migrations
- **[PA-007]** Storing monetary values as Float — use Integer (cents) to avoid precision errors
- **[PA-008]** Missing indexes on foreign keys — full table scans on JOIN queries
- **[PA-009]** Migrations without rollback.sql — no recovery path during incidents (AP-021)
- **[PA-010]** NOT NULL column added without expand-backfill-contract — table lock in production

## Success Criteria
- [ ] Prisma singleton pattern used (no multiple `new PrismaClient()`)
- [ ] Cursor pagination on all list endpoints (not skip/offset)
- [ ] `select:` specified on all queries — no implicit SELECT *
- [ ] All multi-step operations wrapped in `$transaction`
- [ ] All migrations include `rollback.sql`
- [ ] All migrations follow expand-backfill-contract for NOT NULL additions
- [ ] Monetary values stored as Integer cents (never Float)
- [ ] Indexes on all foreign keys and common filter/sort columns