# Multi-Tenant Isolation

## Purpose
Support multiple clients (venues, businesses) on shared infrastructure with complete data isolation. A manager at Coral Terrace must never see Blue Lagoon data. Tenant isolation is a security requirement, not just a feature.

## Tenancy Model for Sovereign (Hurghada Context)

```
Platform Operator (Sovereign)
    ↓
Tenant: Red Sea Ventures (property management company)
    ├── Venue: Coral Terrace Restaurant
    ├── Venue: Blue Lagoon Dive School
    └── Venue: Pearl Beach VIP Club

Tenant: Gulf Hospitality Group
    ├── Venue: Hurghada Grand Hotel
    └── Venue: Desert Rose Spa

Each Tenant is isolated at the data layer.
Each Venue is isolated at the access control layer.
```

## Row-Level Security (Recommended Approach)

```sql
-- Enable RLS on all tables
ALTER TABLE bookings ENABLE ROW LEVEL SECURITY;
ALTER TABLE guests ENABLE ROW LEVEL SECURITY;
ALTER TABLE venues ENABLE ROW LEVEL SECURITY;
ALTER TABLE memberships ENABLE ROW LEVEL SECURITY;

-- Policy: tenant can only see their own data
CREATE POLICY tenant_isolation ON bookings
  USING (tenant_id = current_setting('app.current_tenant_id')::uuid);

CREATE POLICY tenant_isolation ON guests
  USING (tenant_id = current_setting('app.current_tenant_id')::uuid);

-- Policy: superadmin can see all data
CREATE POLICY superadmin_bypass ON bookings
  USING (current_setting('app.current_role') = 'superadmin');
```

## Tenant Context Middleware

```typescript
// apps/api/src/middleware/tenant.ts
import { createMiddleware } from 'hono/factory'
import { prisma } from '@workspace/database'

export const tenantContext = createMiddleware(async (c, next) => {
  const user = c.get('user') as TokenPayload

  if (!user.tenantId && user.role !== 'superadmin') {
    return c.json({ error: 'No tenant context' }, 403)
  }

  // Set PostgreSQL session variable for RLS
  await prisma.$executeRaw`
    SELECT set_config('app.current_tenant_id', ${user.tenantId ?? ''}, true),
           set_config('app.current_role', ${user.role}, true)
  `

  await next()
})

// Attach to all authenticated routes
app.use('/api/*', requireAuth, tenantContext)
```

## Schema Design

```prisma
// packages/database/prisma/schema.prisma

model Tenant {
  id          String   @id @default(cuid())
  name        String
  slug        String   @unique  // used for subdomain: coral-terrace.sovereign.app
  plan        TenantPlan @default(STARTER)
  isActive    Boolean  @default(true)
  createdAt   DateTime @default(now())

  venues      Venue[]
  users       User[]
  settings    TenantSettings?
}

model Venue {
  id          String   @id @default(cuid())
  tenantId    String   // FK to Tenant — always required
  name        String
  type        VenueType
  timezone    String   @default("Africa/Cairo")
  currency    String   @default("EGP")

  bookings    Booking[]
  members     Membership[]

  tenant      Tenant @relation(fields: [tenantId], references: [id])

  @@index([tenantId])
}

model Booking {
  id          String   @id @default(cuid())
  tenantId    String   // ALWAYS required — enables RLS + fast queries
  venueId     String
  guestId     String
  // ...

  @@index([tenantId])
  @@index([tenantId, venueId])
  @@index([tenantId, guestId])
}
```

## Prisma Client with Tenant Extension

```typescript
// packages/database/src/tenant-client.ts
import { PrismaClient } from '@prisma/client'

export function createTenantClient(tenantId: string) {
  return new PrismaClient().$extends({
    query: {
      // Automatically inject tenantId into all create operations
      $allOperations({ model, operation, args, query }) {
        if (['create', 'createMany'].includes(operation)) {
          args.data = { ...args.data, tenantId }
        }
        // Automatically filter all reads by tenantId
        if (['findMany', 'findFirst', 'count', 'aggregate'].includes(operation)) {
          args.where = { ...args.where, tenantId }
        }
        return query(args)
      },
    },
  })
}

// Usage in route handlers
const db = createTenantClient(user.tenantId)
const bookings = await db.booking.findMany() // automatically scoped to tenant
```

## Subdomain Routing (Multi-Tenant URLs)

```typescript
// apps/web/src/middleware.ts
export function middleware(request: NextRequest) {
  const hostname = request.headers.get('host') ?? ''
  const subdomain = hostname.split('.')[0]

  // Resolve tenant from subdomain
  if (subdomain && subdomain !== 'www' && subdomain !== 'app') {
    const requestHeaders = new Headers(request.headers)
    requestHeaders.set('x-tenant-slug', subdomain)

    return NextResponse.rewrite(new URL(request.url), {
      request: { headers: requestHeaders }
    })
  }

  return NextResponse.next()
}
```

## Tenant Onboarding Flow

```typescript
// POST /api/admin/tenants — superadmin only
async function createTenant(data: CreateTenantType) {
  return prisma.$transaction(async (tx) => {
    // 1. Create tenant record
    const tenant = await tx.tenant.create({ data: { name: data.name, slug: data.slug } })

    // 2. Create default venue
    const venue = await tx.venue.create({
      data: { tenantId: tenant.id, name: data.venueName, type: data.venueType }
    })

    // 3. Create admin user for tenant
    const adminUser = await tx.user.create({
      data: {
        tenantId: tenant.id,
        email:    data.adminEmail,
        role:     'admin',
        passwordHash: await bcrypt.hash(generateTempPassword(), 12),
      }
    })

    // 4. Enable RLS policies for this tenant
    await tx.$executeRaw`
      INSERT INTO tenant_rls_config (tenant_id, enabled) VALUES (${tenant.id}, true)
    `

    return { tenant, venue, adminUser }
  })
}
```

## Tenant Escape Audit Query

```sql
-- Run weekly to detect cross-tenant data leaks
-- Every booking should have a tenantId that matches its venue's tenantId
SELECT b.id, b.tenant_id as booking_tenant, v.tenant_id as venue_tenant
FROM bookings b
JOIN venues v ON b.venue_id = v.id
WHERE b.tenant_id != v.tenant_id;
-- Expected: 0 rows
```

## Common Mistakes
- Missing `tenantId` on a new table — all queries return cross-tenant data
- Caching responses without tenant scope — tenant A gets tenant B's cached data
- JWT doesn't include `tenantId` — middleware can't set RLS context
- Superadmin routes not explicitly bypassing RLS — superadmin blocked from seeing any data
- Forgetting to index `tenantId` columns — every query does full table scan

## Success Criteria
- [ ] RLS enabled on all tables with personal/business data
- [ ] All queries include `tenantId` via Prisma extension or explicit filter
- [ ] JWT payload includes `tenantId`
- [ ] Tenant escape audit query returns 0 rows
- [ ] Cross-tenant access test cases in integration tests
- [ ] @Security audits for tenant isolation on every new table/route