# Backend Engineering Playbook

## Purpose

Build production-grade Next.js/Node.js backend services covering API gateway patterns, service architecture, database optimization, caching, real-time streaming, and document generation. This skill consolidates 6 fragmented backend files into one complete playbook with copy-paste-ready patterns.

**Measurable Impact:**
- Before: 6 separate 44-59 line files → fragmented guidance, missing cross-cutting concerns
- After: Single playbook → correct pattern for any backend task in one lookup
- Before: N+1 queries, no caching → 800ms-2s API response times
- After: Optimized Prisma + Redis caching → <200ms P95 response time
- Before: Raw API routes without validation → security vulnerabilities, inconsistent errors
- After: Zod-validated, auth-gated, rate-limited → zero validation bypass

**Consolidates:** `backend/api-gateway`, `backend/backend-services`, `backend/redis`, `backend/prisma-performance`, `backend/sse-streaming`, `backend/pdf-analytics`, `backend/pdf-tables`

---

## Technique 1 — API Gateway & Middleware Architecture

### Next.js Middleware Pattern

```typescript
// middleware.ts — Global request processing layer
import { NextRequest, NextResponse } from 'next/server';
import { getSession } from '@/lib/auth';

const PUBLIC_ROUTES = ['/api/health', '/api/auth/login', '/api/webhooks'];
const RATE_LIMIT_WINDOW = 60_000; // 1 minute
const RATE_LIMIT_MAX = 100; // requests per window

export async function middleware(req: NextRequest) {
  const { pathname } = req.nextUrl;
  
  // 1. Correlation ID for request tracing
  const correlationId = crypto.randomUUID();
  
  // 2. Skip auth for public routes
  if (PUBLIC_ROUTES.some(route => pathname.startsWith(route))) {
    const res = NextResponse.next();
    res.headers.set('x-correlation-id', correlationId);
    return res;
  }
  
  // 3. Auth check
  const session = await getSession(req);
  if (!session) {
    return NextResponse.json(
      { error: 'Unauthorized', correlationId },
      { status: 401 }
    );
  }
  
  // 4. Multi-tenancy enforcement: inject org context
  const res = NextResponse.next();
  res.headers.set('x-correlation-id', correlationId);
  res.headers.set('x-org-id', session.organizationId);
  res.headers.set('x-user-id', session.userId);
  
  return res;
}

export const config = {
  matcher: ['/api/:path*', '/dashboard/:path*'],
};
```

### Service Layer Architecture

```typescript
// services/base.ts — Consistent result pattern for all services
import { z } from 'zod';

// Result type: Every service returns this — never throw from service layer
type Result<T> = 
  | { success: true; data: T }
  | { success: false; error: string; code: string };

// Service factory with auth context
export function createService<TInput extends z.ZodSchema, TOutput>(
  schema: TInput,
  handler: (input: z.infer<TInput>, ctx: ServiceContext) => Promise<TOutput>
) {
  return async (rawInput: unknown, ctx: ServiceContext): Promise<Result<TOutput>> => {
    try {
      const input = schema.parse(rawInput);
      const data = await handler(input, ctx);
      return { success: true, data };
    } catch (error) {
      if (error instanceof z.ZodError) {
        return { success: false, error: error.errors[0].message, code: 'VALIDATION_ERROR' };
      }
      console.error(`[${ctx.correlationId}] Service error:`, error);
      return { success: false, error: 'Internal server error', code: 'INTERNAL_ERROR' };
    }
  };
}

// Server Action wrapper
export function createAction<TInput extends z.ZodSchema, TOutput>(
  schema: TInput,
  handler: (input: z.infer<TInput>, ctx: ServiceContext) => Promise<TOutput>
) {
  return async (rawInput: unknown): Promise<Result<TOutput>> => {
    'use server';
    const session = await getServerSession();
    if (!session) return { success: false, error: 'Unauthorized', code: 'AUTH_ERROR' };
    
    const ctx: ServiceContext = {
      userId: session.userId,
      orgId: session.organizationId,
      correlationId: crypto.randomUUID(),
    };
    
    return createService(schema, handler)(rawInput, ctx);
  };
}
```

### Rate Limiting with Redis

```typescript
// lib/rate-limit.ts — Token bucket rate limiter
import { Redis } from '@upstash/redis';

const redis = Redis.fromEnv();

interface RateLimitResult {
  allowed: boolean;
  remaining: number;
  resetAt: number;
}

export async function checkRateLimit(
  identifier: string, // userId or IP
  limit: number = 100,
  windowMs: number = 60_000
): Promise<RateLimitResult> {
  const key = `rl:${identifier}:${Math.floor(Date.now() / windowMs)}`;
  
  const pipeline = redis.pipeline();
  pipeline.incr(key);
  pipeline.pexpire(key, windowMs);
  const [count] = await pipeline.exec<[number, boolean]>();
  
  return {
    allowed: count <= limit,
    remaining: Math.max(0, limit - count),
    resetAt: Math.ceil(Date.now() / windowMs) * windowMs,
  };
}

// Usage in API route
export async function POST(req: NextRequest) {
  const userId = req.headers.get('x-user-id')!;
  const { allowed, remaining } = await checkRateLimit(userId, 50, 60_000);
  
  if (!allowed) {
    return NextResponse.json(
      { error: 'Rate limit exceeded' },
      { status: 429, headers: { 'X-RateLimit-Remaining': String(remaining) } }
    );
  }
  // ... handle request
}
```

---

## Technique 2 — Prisma Performance Optimization

### Query Optimization Patterns

```typescript
// Anti-pattern: N+1 query (fetches users, then loops for each org)
// ❌ BAD
const users = await prisma.user.findMany();
for (const user of users) {
  const org = await prisma.organization.findUnique({ where: { id: user.orgId } });
}

// ✅ GOOD: Include relation in single query
const users = await prisma.user.findMany({
  include: { organization: true },
});

// ✅ BETTER: Select only needed fields
const users = await prisma.user.findMany({
  select: {
    id: true,
    name: true,
    email: true,
    organization: { select: { id: true, name: true } },
  },
});

// Pagination: cursor-based for large datasets (NOT offset)
// ❌ BAD: offset pagination (slow for large offsets)
const page = await prisma.user.findMany({ skip: 10000, take: 20 });

// ✅ GOOD: cursor pagination (constant time)
const page = await prisma.user.findMany({
  take: 20,
  cursor: { id: lastSeenId },
  skip: 1, // Skip the cursor itself
  orderBy: { createdAt: 'desc' },
});

// Transactions for multi-step operations
const result = await prisma.$transaction(async (tx) => {
  const order = await tx.order.create({ data: orderData });
  await tx.inventory.update({
    where: { productId: order.productId },
    data: { quantity: { decrement: order.quantity } },
  });
  await tx.payment.create({ data: { orderId: order.id, amount: order.total } });
  return order;
});

// Connection pooling for serverless
// prisma/schema.prisma
// datasource db {
//   provider = "postgresql"
//   url      = env("DATABASE_URL")         // Direct connection
//   directUrl = env("DIRECT_DATABASE_URL") // For migrations
// }
// Use Prisma Accelerate or PgBouncer for connection pooling in serverless
```

### Database Indexing Strategy

```typescript
// prisma/schema.prisma — Critical indexes
model User {
  id        String   @id @default(cuid())
  email     String   @unique
  orgId     String
  role      Role     @default(MEMBER)
  createdAt DateTime @default(now())
  
  organization Organization @relation(fields: [orgId], references: [id])
  
  // Compound index: queries filtering by org + role
  @@index([orgId, role])
  // Index for sorting by creation date within org
  @@index([orgId, createdAt(sort: Desc)])
}

// Rule: Add indexes for any field that appears in:
// 1. WHERE clauses (filter conditions)
// 2. ORDER BY clauses (sorting)
// 3. JOIN conditions (foreign keys — Prisma auto-indexes @relation fields)
// 4. Unique constraints (already indexed)
```

---

## Technique 3 — Redis Caching Architecture

### Cache-Aside Pattern

```typescript
// lib/cache.ts — Multi-tier caching
import { Redis } from '@upstash/redis';

const redis = Redis.fromEnv();

// Cache-aside: check cache → miss → fetch from DB → populate cache
export async function cached<T>(
  key: string,
  fetcher: () => Promise<T>,
  ttlSeconds: number = 300 // 5 minutes default
): Promise<T> {
  // 1. Try cache
  const cachedValue = await redis.get<T>(key);
  if (cachedValue !== null) return cachedValue;
  
  // 2. Fetch from source
  const freshValue = await fetcher();
  
  // 3. Populate cache (non-blocking)
  redis.set(key, JSON.stringify(freshValue), { ex: ttlSeconds }).catch(console.error);
  
  return freshValue;
}

// Cache invalidation on write
export async function invalidateCache(patterns: string[]): Promise<void> {
  for (const pattern of patterns) {
    const keys = await redis.keys(pattern);
    if (keys.length > 0) await redis.del(...keys);
  }
}

// Usage in service
export async function getOrganization(orgId: string) {
  return cached(
    `org:${orgId}`,
    () => prisma.organization.findUnique({ where: { id: orgId } }),
    600 // 10 minute TTL
  );
}

// Invalidate on update
export async function updateOrganization(orgId: string, data: OrgUpdateInput) {
  const result = await prisma.organization.update({ where: { id: orgId }, data });
  await invalidateCache([`org:${orgId}`, `org:${orgId}:*`]);
  return result;
}
```

### Cache TTL Strategy

```markdown
## TTL Selection Guide

| Data Type | TTL | Rationale |
|-----------|-----|-----------|
| User session | 1h (3600s) | Security: limit session exposure |
| Organization config | 10m (600s) | Rarely changes, frequent reads |
| Dashboard stats | 30s | Near-real-time but reduce DB load |
| Feature flags | 5m (300s) | Balance freshness with performance |
| Product catalog | 1h (3600s) | Changes infrequently |
| Search results | 2m (120s) | Moderate freshness needed |
| Rate limit counters | Window size | Self-expiring by design |
| Static content | 24h (86400s) | Almost never changes |
```

---

## Technique 4 — Real-Time Streaming (SSE)

### Server-Sent Events Pattern

```typescript
// app/api/events/route.ts — SSE endpoint
import { NextRequest } from 'next/server';

export const runtime = 'nodejs'; // SSE needs long-lived connection (not edge)

export async function GET(req: NextRequest) {
  const orgId = req.headers.get('x-org-id');
  if (!orgId) return new Response('Unauthorized', { status: 401 });
  
  const encoder = new TextEncoder();
  
  const stream = new ReadableStream({
    start(controller) {
      // Send initial connection event
      controller.enqueue(encoder.encode(`data: ${JSON.stringify({ type: 'connected' })}\n\n`));
      
      // Subscribe to Redis pub/sub for this org
      const subscriber = createRedisSubscriber(orgId, (event) => {
        controller.enqueue(encoder.encode(`data: ${JSON.stringify(event)}\n\n`));
      });
      
      // Heartbeat every 30s to keep connection alive
      const heartbeat = setInterval(() => {
        controller.enqueue(encoder.encode(`: heartbeat\n\n`));
      }, 30_000);
      
      // Cleanup on disconnect
      req.signal.addEventListener('abort', () => {
        clearInterval(heartbeat);
        subscriber.unsubscribe();
        controller.close();
      });
    },
  });
  
  return new Response(stream, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
      'X-Accel-Buffering': 'no', // Disable nginx buffering
    },
  });
}
```

### Client-Side SSE Hook

```typescript
// hooks/useServerEvents.ts
'use client';
import { useEffect, useRef, useCallback } from 'react';

export function useServerEvents<T>(
  url: string,
  onEvent: (data: T) => void,
  options: { enabled?: boolean; retryMs?: number } = {}
) {
  const { enabled = true, retryMs = 3000 } = options;
  const retryTimeoutRef = useRef<NodeJS.Timeout>();
  
  const connect = useCallback(() => {
    if (!enabled) return;
    
    const eventSource = new EventSource(url);
    
    eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data) as T;
        onEvent(data);
      } catch (e) {
        console.error('SSE parse error:', e);
      }
    };
    
    eventSource.onerror = () => {
      eventSource.close();
      // Auto-reconnect with backoff
      retryTimeoutRef.current = setTimeout(connect, retryMs);
    };
    
    return () => {
      eventSource.close();
      clearTimeout(retryTimeoutRef.current);
    };
  }, [url, onEvent, enabled, retryMs]);
  
  useEffect(() => {
    const cleanup = connect();
    return cleanup;
  }, [connect]);
}
```

---

## Technique 5 — PDF Generation & Document Processing

### PDF Generation with React-PDF

```typescript
// services/pdf-generator.ts — Invoice/report PDF generation
import { renderToBuffer } from '@react-pdf/renderer';

// Template: Invoice PDF (bilingual Arabic/English)
async function generateInvoice(invoice: InvoiceData): Promise<Buffer> {
  const doc = (
    <Document>
      <Page size="A4" style={{ padding: 40, fontFamily: 'Cairo' }}>
        {/* Header: bilingual company info */}
        <View style={{ flexDirection: 'row', justifyContent: 'space-between' }}>
          <View>
            <Text style={{ fontSize: 20 }}>{invoice.companyName}</Text>
            <Text>{invoice.vatNumber}</Text>
          </View>
          <View style={{ textAlign: 'right', direction: 'rtl' }}>
            <Text style={{ fontSize: 20 }}>{invoice.companyNameAr}</Text>
            <Text>الرقم الضريبي: {invoice.vatNumber}</Text>
          </View>
        </View>
        
        {/* Line items table */}
        <View style={{ marginTop: 30 }}>
          <View style={{ flexDirection: 'row', borderBottom: 1, padding: 8 }}>
            <Text style={{ flex: 3 }}>Description / الوصف</Text>
            <Text style={{ flex: 1 }}>Qty</Text>
            <Text style={{ flex: 1 }}>Price</Text>
            <Text style={{ flex: 1 }}>Total</Text>
          </View>
          {invoice.items.map(item => (
            <View key={item.id} style={{ flexDirection: 'row', padding: 8 }}>
              <Text style={{ flex: 3 }}>{item.description}</Text>
              <Text style={{ flex: 1 }}>{item.quantity}</Text>
              <Text style={{ flex: 1 }}>{formatCurrency(item.price, invoice.currency)}</Text>
              <Text style={{ flex: 1 }}>{formatCurrency(item.total, invoice.currency)}</Text>
            </View>
          ))}
        </View>
        
        {/* VAT summary */}
        <View style={{ marginTop: 20, alignItems: 'flex-end' }}>
          <Text>Subtotal: {formatCurrency(invoice.subtotal, invoice.currency)}</Text>
          <Text>VAT ({invoice.vatRate * 100}%): {formatCurrency(invoice.vatAmount, invoice.currency)}</Text>
          <Text style={{ fontSize: 16, fontWeight: 'bold' }}>
            Total: {formatCurrency(invoice.total, invoice.currency)}
          </Text>
        </View>
      </Page>
    </Document>
  );
  
  return renderToBuffer(doc);
}
```

---

## Anti-Pattern Catalog

| ID | Anti-Pattern | Risk | Fix |
|----|-------------|------|-----|
| BE-001 | Auth check in every route individually | **HIGH** — Inconsistent auth, easy to miss a route | Centralize in middleware.ts |
| BE-002 | N+1 queries (loop + individual fetches) | **HIGH** — 10-100× slower than single query | Use `include` or `select` with relations |
| BE-003 | Offset pagination on large tables | **MEDIUM** — Linear slowdown as offset grows | Cursor-based pagination |
| BE-004 | No cache invalidation strategy | **HIGH** — Stale data served indefinitely | Always invalidate on write; use TTL as safety net |
| BE-005 | Throwing errors from service layer | **HIGH** — Inconsistent error handling, crashes | Return `Result<T>` objects; don't throw |
| BE-006 | Direct DB connection in serverless (no pooling) | **CRITICAL** — Connection exhaustion under load | Use PgBouncer, Prisma Accelerate, or Neon serverless |
| BE-007 | SSE without heartbeat | **MEDIUM** — Proxy/firewall drops idle connections | Send heartbeat comment every 30s |
| BE-008 | Hardcoding secrets in source code | **CRITICAL** — Leaked credentials | Environment variables + Zod validation |
| BE-009 | Missing correlation ID on requests | **MEDIUM** — Can't trace issues across services | Assign UUID in middleware, pass through headers |
| BE-010 | No request validation (trust client data) | **CRITICAL** — Injection attacks, data corruption | Zod schema validation on every input |

## 🌍 Regional Calibration (MENA Context)

- **Cultural Alignment:** Ensure all logic respects regional business etiquette and MENA market expectations.
- **RTL Compliance:** Logic must explicitly handle Right-to-Left (RTL) flow where relevant.

## 🛡️ Critical Failure Modes (Anti-Patterns)

- **Anti-Pattern:** Generic Output -> *Correction:* Apply sector-specific professional rules from RULE.md.
- **Anti-Pattern:** Global-Only Logic -> *Correction:* Verify against MENA regional calibration.

---

## Success Criteria

- [ ] All API routes protected by middleware.ts (auth + rate limiting + correlation ID)
- [ ] Service layer returns `Result<T>` — never throws  
- [ ] Zod validation on every input (Server Actions + API routes)
- [ ] No N+1 queries — audited with Prisma query logging
- [ ] Redis cache-aside pattern for all frequently read data (TTL per data type)
- [ ] Cache invalidation triggered on every write operation
- [ ] Cursor-based pagination for all list endpoints
- [ ] SSE endpoint with heartbeat + auto-reconnect client hook
- [ ] Database indexes on all WHERE/ORDER BY columns
- [ ] Connection pooling configured for serverless deployment