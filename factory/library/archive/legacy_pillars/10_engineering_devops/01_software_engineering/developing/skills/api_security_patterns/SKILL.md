---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# API Security Patterns

## OWASP API Security Top 10 — Sovereign Mitigations

| # | Threat | Sovereign Mitigation |
|---|--------|----------------|
| API1 | Broken Object Level Authorization | Check ownership on every resource fetch |
| API2 | Broken Authentication | Short-lived JWT (15min) + HttpOnly refresh rotation |
| API3 | Broken Object Property Level Auth | Zod `select` on output — never expose hidden fields |
| API4 | Unrestricted Resource Consumption | Rate limiting + pagination on all list endpoints |
| API5 | Broken Function Level Authorization | RBAC middleware before every route handler |
| API6 | Unrestricted Access to Sensitive Business Flows | Per-operation rate limits (5 bookings/min max) |
| API7 | Server-Side Request Forgery | Validate + allowlist all URLs in user input |
| API8 | Security Misconfiguration | CORS allowlist, no stack traces in prod responses |
| API9 | Improper Inventory Management | `/health` and `/docs` not exposed publicly in prod |
| API10 | Unsafe Consumption of APIs | Zod validates all external API responses at boundary |

---

## Authentication Patterns

### JWT — Short-Lived Access + Rotating Refresh

```typescript
// packages/shared/src/lib/auth/tokens.ts
import { SignJWT, jwtVerify } from 'jose'

const ACCESS_TTL  = 15 * 60        // 15 minutes
const REFRESH_TTL = 7 * 24 * 3600  // 7 days

export async function signAccessToken(payload: TokenPayload): Promise<string> {
  return new SignJWT({ ...payload, type: 'access' })
    .setProtectedHeader({ alg: 'HS256' })
    .setIssuedAt()
    .setExpirationTime(`${ACCESS_TTL}s`)
    .sign(new TextEncoder().encode(process.env.JWT_SECRET!))
}

export async function verifyAccessToken(token: string): Promise<TokenPayload> {
  const { payload } = await jwtVerify(
    token,
    new TextEncoder().encode(process.env.JWT_SECRET!),
    { algorithms: ['HS256'] }
  )
  if (payload.type !== 'access') throw new Error('Not an access token')
  return payload as TokenPayload
}
```

### Auth Middleware (Hono)

```typescript
// apps/api/src/middleware/auth.ts
import { createMiddleware } from 'hono/factory'
import { verifyAccessToken } from '@workspace/shared/lib/auth/tokens'

export const authMiddleware = createMiddleware(async (c, next) => {
  const authHeader = c.req.header('Authorization')
  if (!authHeader?.startsWith('Bearer ')) {
    return c.json({ error: 'Unauthorized' }, 401)
  }

  try {
    const token = authHeader.slice(7)
    const payload = await verifyAccessToken(token)
    c.set('userId', payload.sub)
    c.set('userRole', payload.role)
  } catch {
    return c.json({ error: 'Invalid or expired token' }, 401)
  }

  return next()
})
```

---

## Authorization Patterns

### Object-Level Authorization (API1 — most critical)

```typescript
// ❌ WRONG — checks auth but not ownership
app.get('/bookings/:id', authMiddleware, async (c) => {
  const booking = await prisma.booking.findUnique({ where: { id: c.req.param('id') } })
  return c.json(booking)
})

// ✅ CORRECT — always scope to authenticated user
app.get('/bookings/:id', authMiddleware, async (c) => {
  const booking = await prisma.booking.findUnique({
    where: {
      id: c.req.param('id'),
      userId: c.get('userId'),     // ← ownership check in the query itself
    },
    select: { id: true, status: true, checkIn: true, totalPrice: true },
                                   // ← never expose internal fields
  })
  if (!booking) return c.json({ error: 'Not found' }, 404)
  return c.json(booking)
})
```

### RBAC Middleware

```typescript
// apps/api/src/middleware/rbac.ts
export function requireRole(...roles: Role[]) {
  return createMiddleware(async (c, next) => {
    const userRole = c.get('userRole') as Role
    if (!roles.includes(userRole)) {
      return c.json({ error: 'Forbidden' }, 403)
    }
    return next()
  })
}

// Usage
app.delete('/bookings/:id',
  authMiddleware,
  requireRole('admin', 'staff'),   // role check AFTER auth check
  async (c) => { /* ... */ }
)
```

---

## Input Validation & Sanitization

```typescript
// All input validated at route boundary via Zod — before any business logic
import { zValidator } from '@hono/zod-validator'
import { CreateBookingSchema } from '@workspace/shared/contracts/booking'

app.post('/bookings',
  authMiddleware,
  zValidator('json', CreateBookingSchema),   // validation happens here
  async (c) => {
    const data = c.req.valid('json')         // type-safe, already validated
    // business logic below — no raw req.json() access
  }
)
```

### SSRF Prevention (API7)

```typescript
// When user input can be a URL — always validate against an allowlist
const ALLOWED_DOMAINS = ['maps.googleapis.com', 'api.stripe.com']

function validateUrl(input: string): URL {
  const url = new URL(input)   // throws on invalid URL

  if (!ALLOWED_DOMAINS.includes(url.hostname)) {
    throw new Error(`URL domain not allowed: ${url.hostname}`)
  }

  // Block internal/private IPs
  if (/^(10\.|192\.168\.|172\.(1[6-9]|2\d|3[01])\.|127\.|localhost)/i.test(url.hostname)) {
    throw new Error('Internal URLs not allowed')
  }

  return url
}
```

---

## Rate Limiting (Per Operation)

```typescript
// Different limits per sensitivity of operation
import { Ratelimit } from '@upstash/ratelimit'
import { redis } from '@workspace/shared/lib/redis'

export const rateLimits = {
  // Public API endpoints
  api:    new Ratelimit({ redis, limiter: Ratelimit.slidingWindow(100, '1 m') }),
  // Auth endpoints — prevent brute force
  auth:   new Ratelimit({ redis, limiter: Ratelimit.slidingWindow(5,   '15 m') }),
  // Sensitive business operations
  booking: new Ratelimit({ redis, limiter: Ratelimit.slidingWindow(10,  '1 m') }),
  // Password reset — prevent enumeration
  reset:  new Ratelimit({ redis, limiter: Ratelimit.slidingWindow(3,   '1 h') }),
}

// Apply in middleware
const { success } = await rateLimits.auth.limit(clientIp)
if (!success) return c.json({ error: 'Too many attempts' }, 429)
```

---

## CORS Configuration

```typescript
// apps/api/src/index.ts
import { cors } from 'hono/cors'

app.use('*', cors({
  origin: (origin) => {
    const allowed = (process.env.ALLOWED_ORIGINS ?? '').split(',')
    return allowed.includes(origin) ? origin : null
  },
  allowMethods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowHeaders: ['Content-Type', 'Authorization'],
  exposeHeaders: ['X-Request-ID'],
  maxAge: 86400,
  credentials: true,
}))
```

---

## Response Security Headers

```typescript
// apps/api/src/middleware/security-headers.ts
app.use('*', async (c, next) => {
  await next()
  c.header('X-Content-Type-Options', 'nosniff')
  c.header('X-Frame-Options', 'DENY')
  c.header('Referrer-Policy', 'strict-origin-when-cross-origin')
  c.header('Permissions-Policy', 'geolocation=(), microphone=()')
  // Never: expose stack traces, DB errors, internal paths in production
})
```

---

## Error Response Sanitization

```typescript
// ❌ NEVER expose internal errors to the client
return c.json({ error: error.message, stack: error.stack })   // leaks internals

// ✅ Always sanitize — log internally, return generic message
import * as Sentry from '@sentry/node'

app.onError((err, c) => {
  Sentry.captureException(err)
  console.error({ err, path: c.req.path })  // internal log

  if (err instanceof ZodError) {
    return c.json({ error: 'Validation failed', issues: err.issues }, 400)
  }
  return c.json({ error: 'Internal server error' }, 500)  // generic to client
})
```

## 🌍 Regional Calibration (MENA Context)

- **Cultural Alignment:** Ensure all logic respects regional business etiquette and MENA market expectations.
- **RTL Compliance:** Logic must explicitly handle Right-to-Left (RTL) flow where relevant.

## 🛡️ Critical Failure Modes (Anti-Patterns)

- **Anti-Pattern:** Generic Output -> *Correction:* Apply sector-specific professional rules from RULE.md.
- **Anti-Pattern:** Global-Only Logic -> *Correction:* Verify against MENA regional calibration.

---

## Common Mistakes

- **[AS-001]** Object-level auth missing — verifying user is logged in but not that they own the resource
- **[AS-002]** JWT stored in localStorage — use HttpOnly cookie; localStorage accessible via XSS
- **[AS-003]** Long-lived access tokens (>1h) — use 15min access + rotating refresh
- **[AS-004]** Stack traces / DB errors exposed in API responses — always sanitize
- **[AS-005]** CORS wildcard (`*`) in production — always explicit origin allowlist
- **[AS-006]** Missing rate limit on auth/reset endpoints — brute-force and enumeration attacks
- **[AS-007]** User input used as a URL without allowlist — Server-Side Request Forgery (SSRF)
- **[AS-008]** Input validated client-side only — always re-validate server-side at route boundary

## Success Criteria
- [ ] Every route has ownership check (not just auth check) — resource scoped to userId
- [ ] JWT: 15min access tokens + rotating HttpOnly refresh tokens
- [ ] Rate limits: auth ≤5/15min, booking ≤10/1min, reset ≤3/1h
- [ ] CORS: explicit origin allowlist (no wildcard)
- [ ] All user input validated via Zod at route boundary before business logic
- [ ] Error responses never include stack traces, DB messages, or internal paths
- [ ] Security headers on all responses
- [ ] RBAC enforced before sensitive route handlers