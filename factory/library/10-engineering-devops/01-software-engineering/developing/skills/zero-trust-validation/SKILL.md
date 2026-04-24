# Zero-Trust Validation

## Purpose
Validate ALL inputs at every system boundary — API endpoints, Server Actions, webhooks, cron jobs, and admin operations. Trust nothing from outside the boundary. Double-validate at both entry and service layers.

## When to Activate
- Every API endpoint (no exceptions)
- Every Next.js Server Action
- Every form submission
- Every webhook receiver
- Every scheduled job receiving external data
- Every admin operation

## Validation Architecture

```
Browser/Mobile
    ↓
[Client-side Zod] — fast UX feedback, NOT security
    ↓
API/Server Boundary ← SECURITY ENFORCEMENT LAYER
    ↓
[Server Zod.parse()] — throws on invalid
    ↓
[Service Layer] — receives typed, validated data only
    ↓
[DB Layer] — Prisma types + parameterized queries
```

## Hono Backend Pattern

```typescript
// apps/api/src/routes/bookings.ts
import { Hono } from 'hono'
import { zValidator } from '@hono/zod-validator'
import { CreateBookingSchema, BookingQuerySchema } from '@workspace/shared/contracts/booking'

const bookings = new Hono()

// ✅ Validate query params
bookings.get('/', zValidator('query', BookingQuerySchema), async (c) => {
  const query = c.req.valid('query') // fully typed, validated
  return c.json(await bookingService.list(query))
})

// ✅ Validate request body
bookings.post('/', zValidator('json', CreateBookingSchema), async (c) => {
  const data = c.req.valid('json') // fully typed, validated
  return c.json(await bookingService.create(data), 201)
})

// ✅ Validate route params
bookings.get('/:id', zValidator('param', z.object({ id: z.string().uuid() })), async (c) => {
  const { id } = c.req.valid('param')
  return c.json(await bookingService.findById(id))
})

export { bookings }
```

## Next.js Server Action Pattern

```typescript
// apps/web/src/actions/booking.ts
'use server'
import { CreateBookingSchema } from '@workspace/shared/contracts/booking'

export async function createBookingAction(formData: FormData) {
  // ✅ Always validate Server Action inputs — they're API boundaries
  const raw = Object.fromEntries(formData.entries())
  const result = CreateBookingSchema.safeParse(raw)

  if (!result.success) {
    return { error: result.error.flatten().fieldErrors }
  }

  const booking = await bookingService.create(result.data)
  revalidatePath('/bookings')
  return { success: true, booking }
}
```

## Security Headers (Middleware)

```typescript
// apps/web/src/middleware.ts
import { NextResponse } from 'next/server'

export function middleware(request: NextRequest) {
  const response = NextResponse.next()

  // Security headers
  response.headers.set('X-Content-Type-Options', 'nosniff')
  response.headers.set('X-Frame-Options', 'DENY')
  response.headers.set('X-XSS-Protection', '1; mode=block')
  response.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin')
  response.headers.set('Permissions-Policy', 'camera=(), microphone=(), geolocation=()')
  response.headers.set(
    'Content-Security-Policy',
    "default-src 'self'; script-src 'self' 'nonce-{nonce}'; style-src 'self' 'unsafe-inline';"
  )

  return response
}
```

## Rate Limiting Pattern

```typescript
// apps/api/src/middleware/rateLimit.ts
import { Hono } from 'hono'
import { rateLimiter } from 'hono-rate-limiter'

export const publicRateLimit = rateLimiter({
  windowMs: 15 * 60 * 1000, // 15 minutes
  limit: 100,
  standardHeaders: 'draft-7',
  keyGenerator: (c) => c.req.header('x-forwarded-for') ?? 'anonymous',
})

export const authRateLimit = rateLimiter({
  windowMs: 15 * 60 * 1000,
  limit: 5, // strict for auth routes
  message: 'Too many login attempts',
  keyGenerator: (c) => c.req.header('x-forwarded-for') ?? 'anonymous',
})
```

## Input Sanitization Rules

```typescript
// ✅ String fields: max length, no null bytes
z.string().max(500).trim().regex(/^[^\x00]*$/)

// ✅ URLs: restricted protocols
z.string().url().startsWith('https://')

// ✅ Emails: standard + lowercase
z.string().email().toLowerCase()

// ✅ Phone (Egypt/International)
z.string().regex(/^\+?[1-9]\d{6,14}$/)

// ✅ Currency amounts: no negative, max precision
z.number().nonnegative().multipleOf(0.01).max(1_000_000)

// ✅ IDs: always UUID
z.string().uuid()

// ❌ NEVER
z.any()
z.unknown()
z.string() // without max length on user input
```

## SQL Injection Prevention
```typescript
// Prisma parameterizes all queries automatically ✅
const booking = await prisma.booking.findFirst({
  where: { id: bookingId } // safe
})

// Never use raw queries without parameterization
await prisma.$queryRaw`SELECT * FROM bookings WHERE id = ${bookingId}` // ✅ tagged template = safe
await prisma.$queryRawUnsafe(`SELECT * FROM bookings WHERE id = '${bookingId}'`) // ❌ NEVER
```

## Common Mistakes
- Validating only on the frontend — client-side Zod is UX, not security
- Using `z.any()` anywhere in API routes — defeats validation entirely
- Skipping rate limiting on auth endpoints — brute force vulnerability
- Using `$queryRawUnsafe` — SQL injection risk
- Trusting JWT payload without re-validating against DB — replay attacks

## Success Criteria
- [ ] Every POST/PUT/PATCH route uses `zValidator` or `safeParse`
- [ ] Every Server Action validates input with Zod before processing
- [ ] Rate limiting on all auth and public endpoints
- [ ] Security headers set via middleware
- [ ] No `z.any()` in any contract or route handler
- [ ] `security:scan` passes with zero critical/high findings