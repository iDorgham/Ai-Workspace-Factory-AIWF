---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# Structured Logging + Distributed Tracing

## Purpose
Every log is a structured JSON object. Every request carries a correlation ID across all services. Operators can query logs, trace requests through the system, and debug production issues in minutes — not hours.

## When to Activate
- Every new API service or route file
- When setting up a new app (during /init)
- When debugging production issues

## Logger Package Setup

```typescript
// packages/logger/src/index.ts
import pino from 'pino'

const isDev = process.env.NODE_ENV === 'development'

export const logger = pino({
  level: process.env.LOG_LEVEL ?? 'info',
  transport: isDev
    ? { target: 'pino-pretty', options: { colorize: true } }
    : undefined, // production: raw JSON for log aggregator
  formatters: {
    level: (label) => ({ level: label }),
  },
  base: {
    service: process.env.SERVICE_NAME ?? 'api',
    env:     process.env.NODE_ENV ?? 'development',
    version: process.env.APP_VERSION ?? '0.0.0',
  },
  redact: [
    'password', 'passwordHash', 'token', 'accessToken', 'refreshToken',
    'nationalId', 'passportNo', 'cardNumber', 'cvv',
    'req.headers.authorization', 'req.headers.cookie',
  ],
  serializers: {
    req: pino.stdSerializers.req,
    res: pino.stdSerializers.res,
    err: pino.stdSerializers.err,
  },
})

// Child logger with request context
export function createRequestLogger(requestId: string, userId?: string) {
  return logger.child({ requestId, userId })
}

// Domain-specific loggers
export const securityLogger  = logger.child({ domain: 'security' })
export const bookingLogger   = logger.child({ domain: 'booking' })
export const paymentLogger   = logger.child({ domain: 'payment' })
export const membershipLogger = logger.child({ domain: 'membership' })
```

## Request Logging Middleware (Hono)

```typescript
// apps/api/src/middleware/logging.ts
import { createMiddleware } from 'hono/factory'
import { createRequestLogger } from '@workspace/logger'
import { randomUUID } from 'crypto'

export const requestLogger = createMiddleware(async (c, next) => {
  const requestId = c.req.header('x-request-id') ?? randomUUID()
  const reqLogger = createRequestLogger(requestId, c.get('user')?.sub)

  // Attach to context for use in handlers
  c.set('logger', reqLogger)
  c.set('requestId', requestId)

  const start = performance.now()

  reqLogger.info({
    event:  'request.start',
    method: c.req.method,
    path:   c.req.path,
    ip:     c.req.header('x-forwarded-for') ?? 'unknown',
    userAgent: c.req.header('user-agent'),
  })

  await next()

  const duration = Math.round(performance.now() - start)

  reqLogger.info({
    event:    'request.end',
    method:   c.req.method,
    path:     c.req.path,
    status:   c.res.status,
    duration, // milliseconds
  })

  // Propagate request ID to response
  c.res.headers.set('x-request-id', requestId)
})
```

## Structured Log Events

```typescript
// Domain event logging patterns
// apps/api/src/services/booking.service.ts

export class BookingService {
  private log = bookingLogger

  async create(data: CreateBookingType, userId: string): Promise<BookingType> {
    this.log.info({ event: 'booking.create.start', userId, venueId: data.venueId })

    try {
      const booking = await prisma.booking.create({ data: { ...data, createdBy: userId } })

      this.log.info({
        event:     'booking.create.success',
        bookingId: booking.id,
        userId,
        venueId:   booking.venueId,
        type:      booking.type,
        partySize: booking.partySize,
        amount:    booking.totalAmount,
        currency:  booking.currency,
      })

      return booking
    } catch (error) {
      this.log.error({
        event:   'booking.create.failure',
        userId,
        venueId: data.venueId,
        error:   error instanceof Error ? error.message : 'Unknown error',
        stack:   error instanceof Error ? error.stack : undefined,
      })
      throw error
    }
  }
}
```

## OpenTelemetry Tracing

```typescript
// packages/monitoring/src/tracing.ts
import { NodeSDK } from '@opentelemetry/sdk-node'
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node'
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http'
import { Resource } from '@opentelemetry/resources'
import { SEMRESATTRS_SERVICE_NAME, SEMRESATTRS_SERVICE_VERSION } from '@opentelemetry/semantic-conventions'

export function initTracing() {
  const sdk = new NodeSDK({
    resource: new Resource({
      [SEMRESATTRS_SERVICE_NAME]:    process.env.SERVICE_NAME ?? 'sovereign-api',
      [SEMRESATTRS_SERVICE_VERSION]: process.env.APP_VERSION ?? '1.0.0',
    }),
    traceExporter: new OTLPTraceExporter({
      url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT ?? 'http://localhost:4318/v1/traces',
    }),
    instrumentations: [
      getNodeAutoInstrumentations({
        '@opentelemetry/instrumentation-http':    { enabled: true },
        '@opentelemetry/instrumentation-prisma':  { enabled: true },
        '@opentelemetry/instrumentation-ioredis': { enabled: true },
      }),
    ],
  })

  sdk.start()
  return sdk
}
```

## Log Levels & When to Use

```typescript
// logger.trace  — very verbose, development only (function entry/exit)
// logger.debug  — debugging info, disable in production
// logger.info   — normal operations (request start/end, domain events)
// logger.warn   — unexpected but recoverable (rate limit hit, retry triggered)
// logger.error  — errors that need attention (failed payment, DB error)
// logger.fatal  — system cannot continue (DB unavailable, corrupt config)

// ✅ Good info log — enough context to debug without sensitive data
log.info({
  event:     'payment.processed',
  bookingId: booking.id,
  amount:    booking.totalAmount,
  currency:  booking.currency,
  provider:  'stripe',
  // ❌ Never: cardNumber, cvv, stripeCustomerId
})

// ✅ Good error log — full context for debugging
log.error({
  event:     'payment.failed',
  bookingId: booking.id,
  provider:  'stripe',
  errorCode: error.code,
  message:   error.message,
  // stack trace for non-production
  ...(process.env.NODE_ENV !== 'production' && { stack: error.stack }),
})
```

## Common Mistakes
- Logging sensitive data (passwords, tokens, national IDs) — use `redact` in pino config
- Using `console.log` in production code — unstructured, unqueryable, unsearchable
- Missing correlation ID — can't trace a request across services
- Too verbose in production — INFO level for normal ops, DEBUG disabled in prod
- Logging inside tight loops — severe performance impact

## Success Criteria
- [ ] All services use `@workspace/logger` — zero `console.log` in production code
- [ ] Request ID propagated via `x-request-id` header
- [ ] Sensitive fields in `redact` list (password, token, national ID, card)
- [ ] Domain events logged with structured context (bookingId, userId, etc.)
- [ ] OpenTelemetry SDK initialized in API entrypoint
- [ ] Logs queryable in log aggregator (Grafana Loki, Datadog, etc.)