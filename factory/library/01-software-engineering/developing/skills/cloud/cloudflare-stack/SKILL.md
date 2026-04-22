# Cloudflare Stack (Workers, D1, R2, KV, Durable Objects)

## What Cloudflare Provides in Sovereign

| Service | Sovereign Usage |
|---------|-----------|
| Workers | Edge API handlers, middleware, auth — zero cold start |
| Pages | Full-stack app hosting (Next.js, Remix, SvelteKit) |
| D1 | SQLite-compatible edge database (Prisma-compatible) |
| R2 | S3-compatible object storage — zero egress fees |
| KV | Global key-value store — cache, config, session |
| Durable Objects | Stateful coordination — rate limiting, WebSockets, presence |
| Queues | Background jobs at the edge — at-least-once delivery |
| Hyperdrive | Connection pooling for external PostgreSQL/MySQL |

**Why Cloudflare:** Zero cold starts, 300+ edge locations, R2's zero egress fees vs S3, all services within one platform.

---

## Setup in Sovereign Monorepo

### pnpm Catalog Entries
```yaml
# pnpm-workspace.yaml → catalog section
catalog:
  "wrangler": "^3.90.0"                        # CLI (devDependencies)
  "@cloudflare/workers-types": "^4.20241127.0" # TypeScript types
  "@hono/zod-validator": "^0.4.1"              # Zod integration for Hono on Workers
  "hono": "^4.6.20"                            # API framework for Workers
  "drizzle-orm": "^0.39.0"                     # ORM for D1 (Prisma has D1 adapter too)
  "drizzle-kit": "^0.30.0"
```

### wrangler.toml
```toml
# apps/api/wrangler.toml
name = "sovereign-api"
main = "src/index.ts"
compatibility_date = "2024-11-01"
compatibility_flags = ["nodejs_compat"]   # enables Node.js APIs in Workers

[[d1_databases]]
binding = "DB"
database_name = "sovereign-production"
database_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"

[[r2_buckets]]
binding = "BUCKET"
bucket_name = "sovereign-uploads"

[[kv_namespaces]]
binding = "CACHE"
id = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

[[queues.producers]]
binding = "JOBS"
queue = "sovereign-background-jobs"

[[queues.consumers]]
queue = "sovereign-background-jobs"
max_batch_size = 10
max_batch_timeout = 30
```

### Environment Variables
```bash
# .env.example
CLOUDFLARE_ACCOUNT_ID=...
CLOUDFLARE_API_TOKEN=...     # for wrangler deploy + CI
# Secrets — never in wrangler.toml, use: wrangler secret put SECRET_NAME
```

---

## Workers — Hono API

```typescript
// apps/api/src/index.ts
import { Hono } from 'hono'
import { zValidator } from '@hono/zod-validator'
import { CreateBookingSchema } from '@workspace/shared/contracts/booking'

// Type the Cloudflare bindings
type Bindings = {
  DB: D1Database
  BUCKET: R2Bucket
  CACHE: KVNamespace
  JOBS: Queue
}

const app = new Hono<{ Bindings: Bindings }>()

app.post(
  '/bookings',
  zValidator('json', CreateBookingSchema),  // validate at edge
  async (c) => {
    const data = c.req.valid('json')
    const db = c.env.DB

    const booking = await db
      .prepare('INSERT INTO bookings (id, status, user_id) VALUES (?, ?, ?) RETURNING *')
      .bind(crypto.randomUUID(), 'pending', data.userId)
      .first()

    // Enqueue confirmation email (background job)
    await c.env.JOBS.send({ type: 'send-confirmation', bookingId: booking.id })

    return c.json(booking, 201)
  }
)

export default app
```

---

## D1 — Edge SQLite Database

### Migrations with Drizzle
```typescript
// packages/shared/src/db/schema.ts (Drizzle + D1)
import { sqliteTable, text, integer } from 'drizzle-orm/sqlite-core'

export const bookings = sqliteTable('bookings', {
  id:        text('id').primaryKey(),
  status:    text('status', { enum: ['pending', 'confirmed', 'cancelled'] }).notNull(),
  userId:    text('user_id').notNull(),
  totalPrice: integer('total_price').notNull(),  // Integer cents — AP-007 equivalent
  createdAt: integer('created_at', { mode: 'timestamp' }).$defaultFn(() => new Date()),
})
```

```bash
# Generate and apply migration to D1
pnpm drizzle-kit generate
wrangler d1 migrations apply sovereign-production --local    # local dev
wrangler d1 migrations apply sovereign-production            # production
```

### D1 with Prisma (Alternative)
```prisma
// prisma/schema.prisma — D1 adapter
datasource db {
  provider = "sqlite"
  url      = "file:./dev.db"   // local dev only
}
// Use @prisma/adapter-d1 in Worker runtime
```

```typescript
import { PrismaClient } from '@prisma/client'
import { PrismaD1 } from '@prisma/adapter-d1'

// Inside Worker request handler — create per-request (D1 is request-scoped)
export default {
  async fetch(request: Request, env: Bindings) {
    const adapter = new PrismaD1(env.DB)
    const prisma = new PrismaClient({ adapter })
    // ... handle request
  }
}
```

---

## R2 — Object Storage (Zero Egress)

```typescript
// Upload to R2 from a Worker
async function uploadToR2(bucket: R2Bucket, key: string, file: ReadableStream, contentType: string) {
  await bucket.put(key, file, {
    httpMetadata: { contentType },
    customMetadata: { uploadedAt: new Date().toISOString() },
  })

  // Generate a presigned URL (valid for 1 hour)
  const url = await bucket.createSignedUrl(key, { expiresIn: 3600 })
  return url
}

// Serve R2 object through Worker (with cache headers)
app.get('/files/:key', async (c) => {
  const object = await c.env.BUCKET.get(c.req.param('key'))
  if (!object) return c.notFound()

  return new Response(object.body, {
    headers: {
      'Content-Type': object.httpMetadata?.contentType ?? 'application/octet-stream',
      'Cache-Control': 'public, max-age=31536000, immutable',
      'ETag': object.etag,
    },
  })
})
```

---

## KV — Global Key-Value Cache

```typescript
// packages/shared/src/lib/cf-cache.ts
// KV is eventually consistent — use for cache, not source of truth

const CACHE_TTL = {
  short:  60,
  medium: 60 * 15,
  long:   60 * 60,
} as const

export async function withKVCache<T>(
  kv: KVNamespace,
  key: string,
  ttl: number,
  fetcher: () => Promise<T>
): Promise<T> {
  const cached = await kv.get<T>(key, 'json')
  if (cached !== null) return cached

  const fresh = await fetcher()
  await kv.put(key, JSON.stringify(fresh), { expirationTtl: ttl })
  return fresh
}
```

---

## Durable Objects — Stateful Edge

```typescript
// Rate limiter using Durable Objects (stateful, single-instance per key)
export class RateLimiter implements DurableObject {
  private state: DurableObjectState

  constructor(state: DurableObjectState) {
    this.state = state
  }

  async fetch(request: Request): Promise<Response> {
    const { count = 0, resetAt = 0 } = await this.state.storage.get<{ count: number; resetAt: number }>('rate') ?? {}
    const now = Date.now()

    if (now > resetAt) {
      // New window
      await this.state.storage.put('rate', { count: 1, resetAt: now + 60_000 })
      return Response.json({ allowed: true, remaining: 99 })
    }

    if (count >= 100) {
      return Response.json({ allowed: false, remaining: 0 }, { status: 429 })
    }

    await this.state.storage.put('rate', { count: count + 1, resetAt })
    return Response.json({ allowed: true, remaining: 99 - count })
  }
}
```

---

## Queues — Background Jobs at Edge

```typescript
// Producer — enqueue a job from a Worker
await env.JOBS.send({
  type: 'send-confirmation-email',
  bookingId: booking.id,
  userId: booking.userId,
})

// Consumer — process jobs (in same or different Worker)
export default {
  async queue(batch: MessageBatch<JobPayload>, env: Bindings): Promise<void> {
    for (const message of batch.messages) {
      try {
        await processJob(message.body, env)
        message.ack()    // mark as processed
      } catch (error) {
        message.retry()  // re-queue (with backoff)
      }
    }
  }
}
```

---

## Hyperdrive — Connect to External PostgreSQL

```typescript
// Use when Neon/Supabase PostgreSQL is the primary DB but Workers need access
// Hyperdrive pools and caches connections at the edge

const pool = new Pool({ connectionString: env.HYPERDRIVE.connectionString })
const result = await pool.query('SELECT * FROM bookings WHERE id = $1', [bookingId])
```

```toml
# wrangler.toml
[[hyperdrive]]
binding = "HYPERDRIVE"
id = "your-hyperdrive-id"
```

---

## Cloudflare Pages (Full-Stack Hosting)

```bash
# Deploy Next.js to Cloudflare Pages (using @cloudflare/next-on-pages)
pnpm add -D @cloudflare/next-on-pages
# Add to next.config.ts:
# import { setupDevPlatform } from '@cloudflare/next-on-pages/next-dev'
# if (process.env.NODE_ENV === 'development') await setupDevPlatform()

wrangler pages deploy .vercel/output/static   # after next build
```

## 🌍 Regional Calibration (MENA Context)

- **Cultural Alignment:** Ensure all logic respects regional business etiquette and MENA market expectations.
- **RTL Compliance:** Logic must explicitly handle Right-to-Left (RTL) flow where relevant.

## 🛡️ Critical Failure Modes (Anti-Patterns)

- **Anti-Pattern:** Generic Output -> *Correction:* Apply sector-specific professional rules from RULE.md.
- **Anti-Pattern:** Global-Only Logic -> *Correction:* Verify against MENA regional calibration.

---

## Common Mistakes

- **[CF-001]** Using `process.env` in Workers — use `env` bindings from the fetch handler (Workers don't have Node.js process)
- **[CF-002]** Creating PrismaClient singleton in Workers — D1 adapter must be request-scoped (no persistent TCP)
- **[CF-003]** KV for source of truth data — KV is eventually consistent; use D1 or external DB for authoritative data
- **[CF-004]** Large payloads in Queue messages — Queues have a 128KB message limit; store payload in R2/D1 and send reference
- **[CF-005]** Not using `nodejs_compat` flag — many Node.js APIs unavailable without it (crypto, Buffer, etc.)
- **[CF-006]** Durable Object per user/request — each DO is a single JS instance; use them for shared coordination only
- **[CF-007]** R2 without signed URLs for private files — R2 buckets can be public; always use signed URLs for sensitive content
- **[CF-008]** Missing `compatibility_date` in wrangler.toml — Workers behavior is date-pinned; omitting causes breakage on updates

## Success Criteria
- [ ] All environment secrets set via `wrangler secret put` (never in wrangler.toml)
- [ ] `nodejs_compat` flag enabled in wrangler.toml
- [ ] D1 migrations managed via Drizzle Kit or Prisma D1 adapter
- [ ] KV used only for cache (TTL always set), not source of truth
- [ ] R2 private files served through Worker with signed URLs
- [ ] Queue consumers implement ack/retry correctly
- [ ] Durable Objects used only for stateful coordination (not per-request state)