# Upstash Integration (Redis + Kafka)

## What Upstash Provides in Sovereign

| Service | Sovereign Usage |
|---------|-----------|
| Redis | Caching, rate limiting, session store, deduplication, feature flags |
| Kafka | Event streaming, background job queues, audit logs, webhooks |
| QStash | HTTP-based message queue for background tasks (no worker process) |
| Workflow | Durable serverless workflows (like GitHub Actions, but in code) |

**Why Upstash over self-hosted Redis:** HTTP-based API → works in Edge runtimes, serverless, Cloudflare Workers. No persistent TCP connection needed.

---

## Setup in Sovereign Monorepo

### pnpm Catalog Entries
```yaml
# pnpm-workspace.yaml → catalog section
catalog:
  "@upstash/redis": "^1.34.0"       # Redis client (REST API-based)
  "@upstash/ratelimit": "^2.0.4"    # Rate limiting built on Redis
  "@upstash/kafka": "^1.4.0"        # Kafka client
  "@upstash/qstash": "^2.7.0"       # Message queue / scheduled tasks
  "@upstash/workflow": "^0.2.0"     # Durable serverless workflows
```

### Environment Variables
```bash
# .env.example
UPSTASH_REDIS_REST_URL=https://[region]-[id].upstash.io
UPSTASH_REDIS_REST_TOKEN=AX4...
UPSTASH_KAFKA_REST_URL=https://...
UPSTASH_KAFKA_REST_USERNAME=...
UPSTASH_KAFKA_REST_PASSWORD=...
QSTASH_TOKEN=ey...                   # for QStash message queue
QSTASH_CURRENT_SIGNING_KEY=sig_...   # for webhook verification
QSTASH_NEXT_SIGNING_KEY=sig_...
```

---

## Redis — Caching Patterns

### Client Setup
```typescript
// packages/shared/src/lib/redis.ts
import { Redis } from '@upstash/redis'

export const redis = new Redis({
  url: process.env.UPSTASH_REDIS_REST_URL!,
  token: process.env.UPSTASH_REDIS_REST_TOKEN!,
})
```

### Cache Wrapper (with TTL enforcement — AP-055)
```typescript
// packages/shared/src/utils/cache.ts
import { redis } from '../lib/redis'

const CACHE_TTL = {
  short:  60,          // 1 minute — live pricing, availability
  medium: 60 * 15,     // 15 minutes — user profiles, venue details
  long:   60 * 60,     // 1 hour — static content, feature flags
  day:    60 * 60 * 24 // 24 hours — rarely-changing config
} as const

export async function withCache<T>(
  key: string,
  ttlSeconds: number,        // always explicit — never indefinite (AP-055)
  fetcher: () => Promise<T>
): Promise<T> {
  const cached = await redis.get<T>(key)
  if (cached !== null) return cached

  const fresh = await fetcher()
  await redis.setex(key, ttlSeconds, JSON.stringify(fresh))
  return fresh
}

// Usage
const venue = await withCache(
  `venue:${venueId}`,
  CACHE_TTL.medium,
  () => prisma.venue.findUniqueOrThrow({ where: { id: venueId } })
)
```

### Cache Key Conventions
```typescript
// Always use structured, namespaced keys — never raw IDs
const CACHE_KEYS = {
  venue:          (id: string) => `venue:${id}`,
  venueList:      (page: number) => `venue:list:${page}`,
  userProfile:    (id: string) => `user:profile:${id}`,
  featureFlag:    (flag: string) => `feature:${flag}`,
  availableSlots: (venueId: string, date: string) => `slots:${venueId}:${date}`,
} as const
```

### Cache Invalidation
```typescript
// Invalidate on write operations — not on a timer
async function updateVenue(id: string, data: UpdateVenueInput) {
  await prisma.venue.update({ where: { id }, data })
  await redis.del(CACHE_KEYS.venue(id))       // invalidate specific entry
  await redis.del(CACHE_KEYS.venueList(1))    // invalidate first list page
  // avoid: invalidating everything ("cache flush") — too broad
}
```

---

## Rate Limiting

```typescript
// packages/shared/src/lib/rate-limit.ts
import { Ratelimit } from '@upstash/ratelimit'
import { redis } from './redis'

// Sliding window — most accurate for API abuse prevention
export const apiRateLimit = new Ratelimit({
  redis,
  limiter: Ratelimit.slidingWindow(100, '1 m'),    // 100 req/min per IP
  analytics: true,
  prefix: 'ratelimit:api',
})

export const authRateLimit = new Ratelimit({
  redis,
  limiter: Ratelimit.slidingWindow(5, '15 m'),     // 5 login attempts/15min
  analytics: true,
  prefix: 'ratelimit:auth',
})
```

```typescript
// apps/api/src/middleware/rate-limit.middleware.ts (Hono)
import { apiRateLimit } from '@workspace/shared/lib/rate-limit'

export const rateLimitMiddleware = createMiddleware(async (c, next) => {
  const ip = c.req.header('x-forwarded-for') ?? '127.0.0.1'
  const { success, limit, remaining, reset } = await apiRateLimit.limit(ip)

  c.header('X-RateLimit-Limit', String(limit))
  c.header('X-RateLimit-Remaining', String(remaining))
  c.header('X-RateLimit-Reset', String(reset))

  if (!success) {
    return c.json({ error: t('errors.rateLimitExceeded') }, 429)
  }

  return next()
})
```

---

## QStash — Background Jobs (No Worker Process)

QStash pushes HTTP requests on a schedule or delay. No persistent worker needed — works in serverless.

```typescript
// packages/shared/src/lib/qstash.ts
import { Client } from '@upstash/qstash'

export const qstash = new Client({ token: process.env.QSTASH_TOKEN! })

// Enqueue a background job
export async function enqueueJob<T>(endpoint: string, payload: T, options?: {
  delay?: number     // seconds
  retries?: number   // default: 3
}) {
  await qstash.publishJSON({
    url: `${process.env.NEXT_PUBLIC_APP_URL}/api/jobs/${endpoint}`,
    body: payload,
    retries: options?.retries ?? 3,
    delay: options?.delay,
  })
}
```

```typescript
// apps/web/src/app/api/jobs/send-confirmation/route.ts
import { verifySignatureAppRouter } from '@upstash/qstash/nextjs'
import { BookingConfirmationSchema } from '@workspace/shared/contracts/booking'

export const POST = verifySignatureAppRouter(async (req) => {
  const payload = BookingConfirmationSchema.parse(await req.json())
  await sendConfirmationEmail(payload)       // actual work
  return Response.json({ ok: true })
})
```

---

## Deduplication

```typescript
// Prevent duplicate operations (idempotency)
async function processWebhook(eventId: string, handler: () => Promise<void>) {
  const key = `processed:webhook:${eventId}`
  const alreadyProcessed = await redis.set(key, '1', {
    ex: 60 * 60 * 24,  // 24h window
    nx: true,           // only set if not exists
  })

  if (alreadyProcessed === null) {
    console.log(`Webhook ${eventId} already processed — skipping`)
    return
  }

  await handler()
}
```

---

## Feature Flags

```typescript
// Simple feature flag using Redis
export async function isFeatureEnabled(flag: string, userId?: string): Promise<boolean> {
  // Global flag
  const global = await redis.get<boolean>(CACHE_KEYS.featureFlag(flag))
  if (global !== null) return global

  // User-specific override
  if (userId) {
    const userFlag = await redis.get<boolean>(`feature:${flag}:user:${userId}`)
    if (userFlag !== null) return userFlag
  }

  return false  // default off
}
```

## 🌍 Regional Calibration (MENA Context)

- **Cultural Alignment:** Ensure all logic respects regional business etiquette and MENA market expectations.
- **RTL Compliance:** Logic must explicitly handle Right-to-Left (RTL) flow where relevant.

## 🛡️ Critical Failure Modes (Anti-Patterns)

- **Anti-Pattern:** Generic Output -> *Correction:* Apply sector-specific professional rules from RULE.md.
- **Anti-Pattern:** Global-Only Logic -> *Correction:* Verify against MENA regional calibration.

---

## Common Mistakes

- **[UP-001]** Not setting TTL on Redis entries — data never expires, memory grows unbounded (AP-055)
- **[UP-002]** Using bare IDs as cache keys (`user:123`) — collisions across different data types
- **[UP-003]** Cache-flush on write instead of targeted invalidation — thundering herd on re-population
- **[UP-004]** Not verifying QStash signature on job endpoints — any HTTP call can trigger jobs
- **[UP-005]** Using `redis.set()` without `ex:` option — same as not setting TTL
- **[UP-006]** Rate limiting by user ID before auth check — unauthenticated calls bypass limits
- **[UP-007]** Caching mutable data with long TTL — stale availability/pricing served to users

## Success Criteria
- [ ] Every `redis.set()` / `redis.setex()` call has an explicit TTL (no indefinite entries)
- [ ] Cache keys follow namespaced convention (`entity:id` format)
- [ ] Rate limiting applied to all auth + public API endpoints
- [ ] QStash endpoints verify signature before processing
- [ ] Deduplication guard on all webhook handlers
- [ ] Cache invalidation is targeted (key-level), not global flushes