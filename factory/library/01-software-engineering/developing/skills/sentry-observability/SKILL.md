# Sentry Observability

## What Sentry Provides in Sovereign

| Feature | Sovereign Value |
|---------|-----------|
| Error Tracking | Grouped exceptions with stack traces, user context, breadcrumbs |
| Performance Monitoring | Transaction tracing, Core Web Vitals, slow query detection |
| Session Replay | Video-like replay of user sessions that led to errors |
| Alerts | Slack/email alerts on error spikes, performance regressions |
| Release Tracking | Map errors to specific deployments, regressions per release |
| Source Maps | Readable stack traces from minified production code |
| Crons | Heartbeat monitoring for scheduled jobs (detect silent failures) |
| User Feedback | In-app feedback widget shown after errors |

---

## Setup in Sovereign Monorepo

### pnpm Catalog Entries
```yaml
# pnpm-workspace.yaml → catalog section
catalog:
  "@sentry/nextjs": "^9.14.0"      # Next.js (client + server + edge)
  "@sentry/node": "^9.14.0"        # Node.js / Hono backend
  "@sentry/profiling-node": "^9.14.0"  # CPU profiling (optional)
```

### Environment Variables
```bash
# .env.example
NEXT_PUBLIC_SENTRY_DSN=https://[key]@[org].ingest.sentry.io/[project-id]
SENTRY_ORG=your-sentry-org
SENTRY_PROJECT=sovereign-web
SENTRY_AUTH_TOKEN=sntrys_...   # for source map uploads — CI only, never client-side
```

---

## Next.js Setup

### Automatic Setup (Recommended)
```bash
# Sentry wizard configures everything automatically
pnpm dlx @sentry/wizard@latest -i nextjs
```

### Manual Setup

```typescript
// apps/web/sentry.client.config.ts
import * as Sentry from '@sentry/nextjs'

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  environment: process.env.NODE_ENV,

  // Performance — sample 10% of transactions in production
  tracesSampleRate: process.env.NODE_ENV === 'production' ? 0.1 : 1.0,

  // Session replay — 10% of sessions, 100% of sessions with errors
  replaysSessionSampleRate: 0.1,
  replaysOnErrorSampleRate: 1.0,

  integrations: [
    Sentry.replayIntegration({
      // Mask sensitive fields in replay
      maskAllText: false,
      blockAllMedia: false,
      mask: ['[data-sentry-mask]', '.sensitive'],
    }),
  ],

  // Ignore known non-actionable errors
  ignoreErrors: [
    'ResizeObserver loop limit exceeded',
    'Network request failed',
    /^AbortError/,
  ],
})
```

```typescript
// apps/web/sentry.server.config.ts
import * as Sentry from '@sentry/nextjs'

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  environment: process.env.NODE_ENV,
  tracesSampleRate: process.env.NODE_ENV === 'production' ? 0.1 : 1.0,

  // Scrub sensitive data before sending
  beforeSend(event) {
    if (event.request?.data) {
      delete event.request.data.password
      delete event.request.data.cardNumber
    }
    return event
  },
})
```

```typescript
// apps/web/sentry.edge.config.ts
import * as Sentry from '@sentry/nextjs'

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  tracesSampleRate: 0.1,
})
```

```javascript
// apps/web/next.config.ts — wrap with Sentry
import { withSentryConfig } from '@sentry/nextjs'

const nextConfig = { /* your config */ }

export default withSentryConfig(nextConfig, {
  org:     process.env.SENTRY_ORG,
  project: process.env.SENTRY_PROJECT,

  // Upload source maps to Sentry (CI only — requires SENTRY_AUTH_TOKEN)
  silent: !process.env.CI,
  widenClientFileUpload: true,

  // Auto-instrument server components
  autoInstrumentServerFunctions: true,
  autoInstrumentMiddleware: true,
})
```

---

## Hono / Node.js API Setup

```typescript
// apps/api/src/lib/sentry.ts
import * as Sentry from '@sentry/node'

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.NODE_ENV,
  tracesSampleRate: process.env.NODE_ENV === 'production' ? 0.1 : 1.0,

  integrations: [
    Sentry.prismaIntegration(),   // auto-instruments Prisma queries
    Sentry.httpIntegration(),      // outgoing HTTP requests
  ],

  beforeSend(event) {
    // Never send PII
    if (event.user) {
      delete event.user.email
      delete event.user.ip_address
    }
    return event
  },
})
```

```typescript
// apps/api/src/index.ts — Hono + Sentry middleware
import { Hono } from 'hono'
import { sentryMiddleware } from './middleware/sentry'

const app = new Hono()

// Sentry must be first middleware
app.use('*', async (c, next) => {
  return Sentry.withScope(async (scope) => {
    scope.setUser({ id: c.get('userId') })   // attach user to errors
    scope.setTag('route', c.req.path)
    await next()
  })
})
```

---

## Manual Error Capture

```typescript
import * as Sentry from '@sentry/nextjs'

// Capture exception with context
try {
  await processPayment(booking)
} catch (error) {
  Sentry.withScope((scope) => {
    scope.setTag('action', 'payment.process')
    scope.setContext('booking', { id: booking.id, amount: booking.totalPrice })
    scope.setUser({ id: booking.userId })
    Sentry.captureException(error)
  })
  throw error   // re-throw — don't swallow errors
}

// Capture message (non-exception)
Sentry.captureMessage('Booking limit threshold exceeded', {
  level: 'warning',
  tags: { venueId: venue.id },
  extra: { currentCount: bookings.length, limit: MAX_BOOKINGS },
})
```

---

## Performance — Custom Transactions & Spans

```typescript
import * as Sentry from '@sentry/nextjs'

// Wrap a slow operation in a custom span
async function processBookingConfirmation(bookingId: string) {
  return Sentry.startSpan(
    { name: 'booking.confirmation', op: 'function' },
    async (span) => {
      span.setAttribute('booking.id', bookingId)

      const booking = await prisma.booking.findUniqueOrThrow({ where: { id: bookingId } })
      span.setAttribute('booking.status', booking.status)

      await sendConfirmationEmail(booking)
      await updateAuditLog(booking)

      return booking
    }
  )
}
```

---

## Crons — Heartbeat Monitoring

```typescript
// Wrap a scheduled job with Sentry check-in
import * as Sentry from '@sentry/node'

export async function runNightlyCleanup() {
  const checkInId = Sentry.captureCheckIn({
    monitorSlug: 'nightly-cleanup',
    status: 'in_progress',
  })

  try {
    await deleteExpiredSessions()
    await archiveOldBookings()

    Sentry.captureCheckIn({
      checkInId,
      monitorSlug: 'nightly-cleanup',
      status: 'ok',
    })
  } catch (error) {
    Sentry.captureCheckIn({
      checkInId,
      monitorSlug: 'nightly-cleanup',
      status: 'error',
    })
    Sentry.captureException(error)
    throw error
  }
}
```

---

## Release Tracking

```bash
# Create a release tied to a commit (in CI/CD)
# Sentry will map errors to this release and detect regressions

# GitHub Actions step
- name: Create Sentry release
  env:
    SENTRY_AUTH_TOKEN: ${{ secrets.SENTRY_AUTH_TOKEN }}
    SENTRY_ORG: ${{ env.SENTRY_ORG }}
    SENTRY_PROJECT: ${{ env.SENTRY_PROJECT }}
  run: |
    pnpm dlx @sentry/cli releases new ${{ github.sha }}
    pnpm dlx @sentry/cli releases set-commits ${{ github.sha }} --auto
    pnpm dlx @sentry/cli releases finalize ${{ github.sha }}
    pnpm dlx @sentry/cli releases deploys ${{ github.sha }} new -e production
```

---

## Alert Rules (Recommended)

Configure in Sentry dashboard or via `sentry.yml`:

```yaml
# High-priority alerts
- name: Error spike
  trigger: error_rate > 10/min for 5 minutes
  action: slack:#alerts-critical

- name: New issue in production
  trigger: new issue with tag environment:production
  action: slack:#dev-alerts

- name: Performance regression
  trigger: p95 response time > 2000ms for 10 minutes
  action: slack:#dev-alerts

- name: Cron missed
  trigger: cron check-in missed (nightly-cleanup)
  action: pagerduty + slack:#alerts-critical
```

---

## Source Maps in CI

```yaml
# .github/workflows/deploy.yml
- name: Build
  run: pnpm build
  env:
    SENTRY_AUTH_TOKEN: ${{ secrets.SENTRY_AUTH_TOKEN }}
    SENTRY_ORG: your-org
    SENTRY_PROJECT: sovereign-web
    # withSentryConfig in next.config.ts handles upload automatically on build
```

## 🌍 Regional Calibration (MENA Context)

- **Cultural Alignment:** Ensure all logic respects regional business etiquette and MENA market expectations.
- **RTL Compliance:** Logic must explicitly handle Right-to-Left (RTL) flow where relevant.

## 🛡️ Critical Failure Modes (Anti-Patterns)

- **Anti-Pattern:** Generic Output -> *Correction:* Apply sector-specific professional rules from RULE.md.
- **Anti-Pattern:** Global-Only Logic -> *Correction:* Verify against MENA regional calibration.

---

## Common Mistakes

- **[SE-001]** `SENTRY_AUTH_TOKEN` exposed in client bundle — it must be server/CI-only (never `NEXT_PUBLIC_`)
- **[SE-002]** `tracesSampleRate: 1.0` in production — captures every transaction, hits Sentry quota quickly
- **[SE-003]** Not calling `Sentry.init()` before any imports that use it — init must be first
- **[SE-004]** Swallowing errors with Sentry capture but not re-throwing — hides bugs from callers
- **[SE-005]** Not scrubbing PII in `beforeSend` — passwords, card numbers, emails in error context
- **[SE-006]** Missing source maps in production — stack traces show minified code, useless for debugging
- **[SE-007]** Not using `withScope` for context — error context leaks between concurrent requests
- **[SE-008]** No cron heartbeats on scheduled jobs — silent failures go undetected until user reports

## Success Criteria
- [ ] `SENTRY_AUTH_TOKEN` is server/CI-only — never in `NEXT_PUBLIC_` variables
- [ ] `tracesSampleRate` ≤ 0.1 in production
- [ ] `beforeSend` scrubs PII (password, card, email fields)
- [ ] Source maps uploaded to Sentry in CI build step
- [ ] Release created in Sentry on each production deploy
- [ ] Cron heartbeats on every scheduled job
- [ ] Alert rules configured for error spikes + cron misses
- [ ] Session replay enabled with sensitive fields masked