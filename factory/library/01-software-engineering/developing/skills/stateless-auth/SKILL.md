# Stateless JWT Authentication + Refresh Rotation

## Purpose
Implement secure, stateless authentication using short-lived access tokens (15min) and long-lived HttpOnly refresh tokens (7d) with automatic rotation. No server-side session storage.

## When to Activate
- Building any feature requiring user authentication
- Creating protected API routes
- Implementing role-based access (RBAC)
- Building admin dashboards

## Token Architecture

```
ACCESS TOKEN (JWT)
  - Expires: 15 minutes
  - Storage: Memory only (never localStorage)
  - Contains: userId, role, permissions, exp
  - Used: Authorization: Bearer [token]

REFRESH TOKEN (Opaque)
  - Expires: 7 days
  - Storage: HttpOnly, Secure, SameSite=Strict cookie
  - Contains: random token (hashed in DB)
  - Used: POST /auth/refresh (automatic)
  - Rotated: New token issued on every refresh
```

## Auth Contract

```typescript
// packages/shared/src/contracts/auth.ts
import { z } from 'zod'

export const LoginSchema = z.object({
  email:    z.string().email().toLowerCase(),
  password: z.string().min(8).max(128),
})

export const TokenPayloadSchema = z.object({
  sub:         z.string().uuid(),  // userId
  role:        z.enum(['guest', 'staff', 'manager', 'admin', 'superadmin']),
  permissions: z.array(z.string()),
  venueId:     z.string().uuid().optional(), // for multi-tenant
  exp:         z.number(),
  iat:         z.number(),
})

export const AuthResponseSchema = z.object({
  accessToken: z.string(),
  user: z.object({
    id:          z.string().uuid(),
    email:       z.string().email(),
    name:        z.string(),
    role:        TokenPayloadSchema.shape.role,
    permissions: z.array(z.string()),
  }),
})

export type LoginType       = z.infer<typeof LoginSchema>
export type TokenPayload    = z.infer<typeof TokenPayloadSchema>
export type AuthResponseType = z.infer<typeof AuthResponseSchema>
```

## Login Flow (Hono)

```typescript
// apps/api/src/routes/auth.ts
import { Hono } from 'hono'
import { setCookie } from 'hono/cookie'
import { zValidator } from '@hono/zod-validator'
import { SignJWT, jwtVerify } from 'jose'
import { LoginSchema } from '@workspace/shared/contracts/auth'

const auth = new Hono()

auth.post('/login', zValidator('json', LoginSchema), async (c) => {
  const { email, password } = c.req.valid('json')

  const user = await userService.findByEmail(email)
  if (!user || !(await bcrypt.compare(password, user.passwordHash))) {
    return c.json({ error: 'Invalid credentials' }, 401)
  }

  const accessToken = await createAccessToken(user)
  const refreshToken = await createRefreshToken(user.id)

  // Set refresh token as HttpOnly cookie
  setCookie(c, 'refresh_token', refreshToken, {
    httpOnly: true,
    secure: true,
    sameSite: 'Strict',
    maxAge: 7 * 24 * 60 * 60, // 7 days
    path: '/auth/refresh',
  })

  return c.json({ accessToken, user: sanitizeUser(user) })
})

auth.post('/refresh', async (c) => {
  const refreshToken = getCookie(c, 'refresh_token')
  if (!refreshToken) return c.json({ error: 'No refresh token' }, 401)

  const session = await sessionService.findByToken(refreshToken)
  if (!session || session.expiresAt < new Date()) {
    deleteCookie(c, 'refresh_token')
    return c.json({ error: 'Invalid or expired refresh token' }, 401)
  }

  // Rotate: invalidate old, issue new
  await sessionService.rotate(session.id)
  const newRefreshToken = await createRefreshToken(session.userId)
  const accessToken = await createAccessToken(session.user)

  setCookie(c, 'refresh_token', newRefreshToken, {
    httpOnly: true,
    secure: true,
    sameSite: 'Strict',
    maxAge: 7 * 24 * 60 * 60,
    path: '/auth/refresh',
  })

  return c.json({ accessToken })
})

auth.post('/logout', async (c) => {
  const refreshToken = getCookie(c, 'refresh_token')
  if (refreshToken) await sessionService.invalidate(refreshToken)
  deleteCookie(c, 'refresh_token')
  return c.json({ success: true })
})
```

## JWT Helpers

```typescript
// packages/auth/src/tokens.ts
import { SignJWT, jwtVerify } from 'jose'

const ACCESS_SECRET = new TextEncoder().encode(process.env.JWT_ACCESS_SECRET!)
const REFRESH_SECRET = new TextEncoder().encode(process.env.JWT_REFRESH_SECRET!)

export async function createAccessToken(user: User): Promise<string> {
  return new SignJWT({
    sub: user.id,
    role: user.role,
    permissions: user.permissions,
    venueId: user.venueId,
  })
    .setProtectedHeader({ alg: 'HS256' })
    .setIssuedAt()
    .setExpirationTime('15m')
    .sign(ACCESS_SECRET)
}

export async function verifyAccessToken(token: string): Promise<TokenPayload> {
  const { payload } = await jwtVerify(token, ACCESS_SECRET)
  return TokenPayloadSchema.parse(payload)
}
```

## Protected Route Middleware

```typescript
// apps/api/src/middleware/auth.ts
import { createMiddleware } from 'hono/factory'

export const requireAuth = createMiddleware(async (c, next) => {
  const authHeader = c.req.header('Authorization')
  if (!authHeader?.startsWith('Bearer ')) {
    return c.json({ error: 'Unauthorized' }, 401)
  }

  try {
    const token = authHeader.slice(7)
    const payload = await verifyAccessToken(token)
    c.set('user', payload)
    await next()
  } catch {
    return c.json({ error: 'Invalid or expired token' }, 401)
  }
})

export const requireRole = (...roles: Role[]) =>
  createMiddleware(async (c, next) => {
    const user = c.get('user') as TokenPayload
    if (!roles.includes(user.role)) {
      return c.json({ error: 'Forbidden' }, 403)
    }
    await next()
  })

// Usage
bookings.get('/', requireAuth, requireRole('manager', 'admin'), handler)
```

## Frontend Token Management

```typescript
// apps/web/src/lib/auth/tokenStore.ts
// Store access token in memory ONLY (never localStorage/sessionStorage)
let accessToken: string | null = null

export const tokenStore = {
  get: () => accessToken,
  set: (token: string) => { accessToken = token },
  clear: () => { accessToken = null },
}

// Auto-refresh before expiry
export async function getValidToken(): Promise<string> {
  if (accessToken && !isExpired(accessToken)) return accessToken
  const { accessToken: newToken } = await refreshTokens()
  tokenStore.set(newToken)
  return newToken
}
```

## Common Mistakes
- Storing access tokens in localStorage — XSS vulnerability
- Not rotating refresh tokens — stolen token can be reused indefinitely
- Long-lived access tokens (>1 hour) — too much exposure window
- Not invalidating all sessions on password change
- Sending refresh token on all routes (not just `/auth/refresh`)

## Success Criteria
- [ ] Access token: 15min expiry, memory storage only
- [ ] Refresh token: HttpOnly, Secure, SameSite=Strict cookie
- [ ] Refresh rotation implemented — old token invalidated on use
- [ ] All protected routes use `requireAuth` middleware
- [ ] RBAC via `requireRole` middleware
- [ ] Password change invalidates all sessions
- [ ] `security:scan` shows no auth vulnerabilities