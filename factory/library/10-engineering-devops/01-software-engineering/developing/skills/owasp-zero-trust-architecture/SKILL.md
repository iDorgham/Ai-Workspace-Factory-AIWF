---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# OWASP Top 10 + Zero-Trust Architecture

## Purpose
Implement defense-in-depth against the OWASP Top 10 vulnerabilities in every application. Zero-Trust means no implicit trust — every request is authenticated, every input validated, every action authorized.

## OWASP Top 10 Coverage Map

### A01 — Broken Access Control
```typescript
// ✅ Every route checks authorization — not just authentication
bookings.patch('/:id',
  requireAuth,
  requireRole('manager', 'admin'), // authorization check
  requireSameVenue,                 // resource-level check
  zValidator('json', UpdateBookingSchema),
  handler
)

// ✅ Resource ownership check
async function requireSameVenue(c: Context, next: Next) {
  const { id } = c.req.param()
  const booking = await bookingService.findById(id)
  const user = c.get('user') as TokenPayload

  if (booking.venueId !== user.venueId && user.role !== 'superadmin') {
    return c.json({ error: 'Forbidden' }, 403)
  }
  await next()
}
```

### A02 — Cryptographic Failures
```typescript
// ✅ Password hashing — bcrypt with cost factor 12
const BCRYPT_ROUNDS = 12
await bcrypt.hash(plainPassword, BCRYPT_ROUNDS)

// ✅ Sensitive data never logged
logger.info({ userId: user.id, action: 'login' }) // ✅ no email/password in logs

// ✅ Encryption at rest — via Prisma + DB-level encryption
// ✅ TLS enforced — Vercel/Railway auto-handle, no HTTP allowed
```

### A03 — Injection
```typescript
// ✅ Parameterized queries only (Prisma handles this)
const bookings = await prisma.booking.findMany({
  where: { venueId: venueId } // ✅ parameterized
})

// ✅ Zod strips unknown fields
const safe = CreateBookingSchema.parse(untrustedInput) // unknown fields removed

// ✅ No eval(), no dynamic SQL
```

### A04 — Insecure Design
```typescript
// ✅ Rate limiting on sensitive endpoints
auth.use('/login', authRateLimit)  // 5 attempts per 15min
auth.use('/reset', authRateLimit)

// ✅ Account lockout after failures
async function trackFailedLogin(email: string) {
  const attempts = await redis.incr(`failed:${email}`)
  if (attempts >= 5) {
    await redis.setex(`locked:${email}`, 900, '1') // 15min lockout
  }
}
```

### A05 — Security Misconfiguration
```typescript
// ✅ Security headers (middleware)
response.headers.set('X-Content-Type-Options', 'nosniff')
response.headers.set('X-Frame-Options', 'DENY')
response.headers.set('Strict-Transport-Security', 'max-age=31536000; includeSubDomains')
response.headers.set('Permissions-Policy', 'camera=(), microphone=()')

// ✅ CORS — whitelist only
app.use('/*', cors({
  origin: ['https://app.example.com', 'https://admin.example.com'],
  credentials: true,
  allowMethods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
}))

// ✅ No stack traces in production responses
if (process.env.NODE_ENV === 'production') {
  app.onError((err, c) => c.json({ error: 'Internal Server Error' }, 500))
}
```

### A06 — Vulnerable & Outdated Components
```bash
# Runs in CI via security:scan
pnpm audit --audit-level=high
# Dependabot auto-PRs for security patches
# SBOM generated on every release
```

### A07 — Identification & Authentication Failures
```typescript
// ✅ See stateless-auth.md for full implementation
// Key points:
// - bcrypt cost 12 for passwords
// - JWT 15min access + 7d rotating refresh
// - HttpOnly cookies for refresh token
// - Rate limit on login endpoint
// - Account lockout after 5 failures
// - Password reset tokens expire in 1 hour
```

### A08 — Software & Data Integrity
```bash
# ✅ package-lock integrity
pnpm install --frozen-lockfile  # CI always uses this

# ✅ Subresource Integrity for CDN assets
# ✅ Signed commits required on main branch
```

### A09 — Security Logging & Monitoring
```typescript
// ✅ Structured security audit log
import { securityLogger } from '@workspace/logger'

// Log security-relevant events
securityLogger.warn({
  event: 'auth.failed_login',
  ip: c.req.header('x-forwarded-for'),
  email: sanitize(body.email), // never log raw password
  attempts: failedAttempts,
  timestamp: new Date().toISOString(),
})

securityLogger.info({
  event: 'booking.created',
  userId: user.id,
  resourceId: booking.id,
  ip: c.req.header('x-forwarded-for'),
})

// Alert on: 5+ failed logins, unusual access patterns, admin operations
```

### A10 — Server-Side Request Forgery (SSRF)
```typescript
// ✅ URL allowlist for outbound HTTP
const ALLOWED_DOMAINS = ['api.stripe.com', 'api.mailgun.net']

function validateWebhookUrl(url: string): boolean {
  const parsed = new URL(url)
  return ALLOWED_DOMAINS.includes(parsed.hostname)
}

// ✅ No user-controlled URLs in server-side fetch
```

## Security Scan Setup

```yaml
# .github/workflows/security.yml
- name: Dependency audit
  run: pnpm audit --audit-level=high

- name: Secret scanning (TruffleHog)
  uses: trufflesecurity/trufflehog@main
  with: { path: ./, base: main }

- name: SBOM generation
  run: npx @cyclonedx/cyclonedx-npm --output sbom.json
  
- name: License scan
  run: npx license-checker --failOn GPL --production
```

## Security Environment Variables

```bash
# .env.example — templates only, never real values
DATABASE_URL=postgresql://user:password@localhost:5432/sovereign
JWT_ACCESS_SECRET=minimum-32-character-secret-here
JWT_REFRESH_SECRET=different-minimum-32-character-secret
ENCRYPTION_KEY=32-byte-hex-key-for-sensitive-data
```

## Common Mistakes
- Same JWT secret for access and refresh tokens — compromise of one = compromise of both
- Logging user passwords or tokens (even "hashed") — use only userId
- Broad CORS `origin: '*'` — allows any origin to make credentialed requests
- Error responses that leak stack traces in production
- Not rate-limiting password reset endpoints — enumeration attack vector

## Success Criteria
- [ ] All OWASP A01–A10 items addressed for the feature
- [ ] Rate limiting on auth, reset, and sensitive endpoints
- [ ] Security headers set via middleware
- [ ] No `pnpm audit` critical/high vulnerabilities
- [ ] TruffleHog secret scan passes
- [ ] Security audit logging for auth events
- [ ] `security:scan` CI gate passes