---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# Neon Serverless PostgreSQL

## What Neon Provides

| Feature | Sovereign Value |
|---------|-----------|
| Serverless PostgreSQL | Scale to zero — no idle costs |
| Database Branching | Create a branch per PR — test against real schema copy |
| Instant Restore | Point-in-time recovery without DBA overhead |
| HTTP Driver | Direct SQL over HTTP from Edge/Serverless runtimes |
| Connection Pooling | Built-in via pgBouncer (pooled URL) |
| Read Replicas | Scale reads without config |

---

## Setup in Sovereign Monorepo

### pnpm Catalog Entries
```yaml
# pnpm-workspace.yaml → catalog section
catalog:
  "@neondatabase/serverless": "^0.10.0"  # HTTP driver for Edge/Vercel functions
  # Prisma works with Neon via standard DATABASE_URL — no extra package needed
```

### Environment Variables
```bash
# .env.example
DATABASE_URL=postgresql://[user]:[password]@[endpoint]-pooler.neon.tech/[dbname]?sslmode=require
DATABASE_DIRECT_URL=postgresql://[user]:[password]@[endpoint].neon.tech/[dbname]?sslmode=require
# DATABASE_URL        → pooled (pgBouncer) — for runtime queries
# DATABASE_DIRECT_URL → direct — for Prisma migrations only
```

### Prisma Configuration
```prisma
// prisma/schema.prisma
datasource db {
  provider          = "postgresql"
  url               = env("DATABASE_URL")        // pooled — runtime
  directUrl         = env("DATABASE_DIRECT_URL") // direct — migrations only
}
```

---

## Database Branching (Neon's Killer Feature)

Neon branches are instant, copy-on-write clones of your database. Use one per feature branch.

### Branch Strategy in Sovereign
```
main branch     → production-db (branch: main)
feature/X       → preview-db   (branch: preview/feature-X)
PR #42          → pr-db        (branch: pr/42)

Each branch:
  - Starts as a copy of main's schema + data at that moment
  - Completely isolated — changes don't affect main
  - Auto-deleted after merge (CI step)
  - Used by Vercel preview deployments (1:1 mapping)
```

### Neon CLI + CI Automation
```bash
# Install Neon CLI
pnpm add -D neonctl

# Create branch for a feature
neonctl branches create --name preview/feature-booking --parent main

# Get connection string for the new branch
neonctl connection-string preview/feature-booking

# Delete branch after PR merge
neonctl branches delete preview/feature-booking
```

### GitHub Actions Integration
```yaml
# .github/workflows/preview.yml
- name: Create Neon branch
  uses: neondatabase/create-branch-action@v5
  id: neon-branch
  with:
    project_id: ${{ secrets.NEON_PROJECT_ID }}
    api_key: ${{ secrets.NEON_API_KEY }}
    branch_name: pr/${{ github.event.pull_request.number }}
    parent: main

- name: Run migrations on branch
  env:
    DATABASE_DIRECT_URL: ${{ steps.neon-branch.outputs.db_url_with_pooler }}
  run: pnpm prisma migrate deploy

- name: Deploy preview
  env:
    DATABASE_URL: ${{ steps.neon-branch.outputs.db_url_with_pooler }}
```

---

## HTTP Driver (Edge / Serverless Compatibility)

Standard Prisma/pg drivers use TCP — blocked in Edge runtimes (Vercel Edge, Cloudflare Workers). Use Neon's HTTP driver instead:

```typescript
// packages/shared/src/lib/db/neon-edge.ts
import { neon } from '@neondatabase/serverless'

// For raw SQL in Edge functions
export const sql = neon(process.env.DATABASE_URL!)

// Usage in Vercel Edge route
export const runtime = 'edge'

export async function GET() {
  const bookings = await sql`
    SELECT id, status, check_in, total_price
    FROM bookings
    WHERE status = 'confirmed'
    ORDER BY check_in DESC
    LIMIT 20
  `
  return Response.json(bookings)
}
```

### Prisma + Neon HTTP Adapter (Node.js optional, Edge required)
```typescript
// packages/shared/src/lib/db/prisma.ts
import { PrismaClient } from '@prisma/client'
import { neonConfig, Pool } from '@neondatabase/serverless'
import { PrismaNeon } from '@prisma/adapter-neon'

// Required for WebSocket support in Node.js when using the adapter
import ws from 'ws'
neonConfig.webSocketConstructor = ws

const pool = new Pool({ connectionString: process.env.DATABASE_URL })
const adapter = new PrismaNeon(pool)

export const prisma = new PrismaClient({ adapter })
```

---

## Connection Pooling Rules

```
Pooled URL  (DATABASE_URL)        → use for all runtime queries
                                     (Next.js API routes, Hono, Server Actions)
Direct URL  (DATABASE_DIRECT_URL) → use ONLY for:
                                     - Prisma migrations (migrate deploy)
                                     - Schema introspection
                                     - Admin scripts

Why: pgBouncer (pooler) doesn't support all PostgreSQL features.
     Migrations need SET session-level commands — must bypass pooler.
```

---

## Point-in-Time Restore

```bash
# Restore database to a specific timestamp (no data loss panic)
neonctl branches restore main --to-timestamp "2026-04-10T14:00:00Z"

# Restore to a specific LSN (log sequence number — from an incident log)
neonctl branches restore main --to-lsn 0/16B4100
```

---

## Migration Strategy with Neon

Neon is fully compatible with the Sovereign expand-backfill-contract migration pattern:

```typescript
// scripts/database/migrate.sh — updated for Neon
DATABASE_DIRECT_URL=$DATABASE_DIRECT_URL pnpm prisma migrate deploy
# ↑ always use directUrl for migrations — bypasses pgBouncer
```

**Anti-pattern:** Running `prisma migrate deploy` with the pooled URL — fails with session-level constraint errors.

## 🌍 Regional Calibration (MENA Context)

- **Cultural Alignment:** Ensure all logic respects regional business etiquette and MENA market expectations.
- **RTL Compliance:** Logic must explicitly handle Right-to-Left (RTL) flow where relevant.

## 🛡️ Critical Failure Modes (Anti-Patterns)

- **Anti-Pattern:** Generic Output -> *Correction:* Apply sector-specific professional rules from RULE.md.
- **Anti-Pattern:** Global-Only Logic -> *Correction:* Verify against MENA regional calibration.

---

## Common Mistakes

- **[NP-001]** Using pooled `DATABASE_URL` for migrations — use `DATABASE_DIRECT_URL` for `migrate deploy`
- **[NP-002]** Not creating a branch per PR — losing isolation between preview environments
- **[NP-003]** Leaving old branches alive after PR merge — accumulates costs and confusion
- **[NP-004]** Using TCP Prisma client in Edge runtime — use `@neondatabase/serverless` HTTP driver
- **[NP-005]** Not adding `?sslmode=require` to connection string — connections fail in production
- **[NP-006]** Running migrations against production from local — always use CI pipeline

## Success Criteria
- [ ] Pooled URL in `DATABASE_URL`, direct URL in `DATABASE_DIRECT_URL`
- [ ] Neon branch created per PR in CI (GitHub Actions step)
- [ ] Branch deleted after PR merge (CI cleanup step)
- [ ] HTTP driver used in any Edge/Cloudflare Worker runtime
- [ ] Migrations always run via `directUrl` — never pooled URL
- [ ] Point-in-time restore tested at least once before production launch