# Self-Healing Workflows & Automated Rollback

## Purpose
Detect, diagnose, and recover from standard failure patterns automatically. CI stays green. Deployments roll back on health check failure. DB migrations are reversible. Flaky tests self-heal before blocking teams.

## Self-Healing Categories

### 1. Flaky Test Recovery
```typescript
// vitest.config.ts — retry flaky tests
export default defineConfig({
  test: {
    retry: 2,          // retry failed tests up to 2 times
    testTimeout: 10000,
    hookTimeout: 10000,
  },
})

// playwright.config.ts — E2E retries
export default defineConfig({
  retries: process.env.CI ? 2 : 0, // retry only in CI
  workers: process.env.CI ? 1 : undefined,
})
```

### 2. Database Migration Rollback
```sql
-- Every migration must have a down() function
-- prisma/migrations/20260408_add_venue_capacity/migration.sql

-- UP (expand)
ALTER TABLE venues ADD COLUMN capacity INTEGER;
CREATE INDEX CONCURRENTLY idx_venues_capacity ON venues(capacity);

-- DOWN (rollback — stored in migration metadata)
-- DROP INDEX CONCURRENTLY IF EXISTS idx_venues_capacity;
-- ALTER TABLE venues DROP COLUMN IF EXISTS capacity;
```

```typescript
// packages/database/src/migrate.ts
export async function rollbackLastMigration() {
  const lastMigration = await prisma.$queryRaw<{ name: string }[]>`
    SELECT migration_name as name
    FROM _prisma_migrations
    WHERE rolled_back_at IS NULL
    ORDER BY started_at DESC
    LIMIT 1
  `
  if (lastMigration.length === 0) throw new Error('No migrations to rollback')

  // Execute down migration SQL
  await prisma.$executeRawUnsafe(getDownMigrationSQL(lastMigration[0].name))
  await prisma.$executeRaw`
    UPDATE _prisma_migrations
    SET rolled_back_at = NOW()
    WHERE migration_name = ${lastMigration[0].name}
  `
}
```

### 3. Deployment Health Check + Auto-Rollback

```typescript
// apps/api/src/routes/health.ts
app.get('/health', async (c) => {
  const checks = await Promise.allSettled([
    prisma.$queryRaw`SELECT 1`,
    redis.ping(),
  ])

  const dbHealthy    = checks[0].status === 'fulfilled'
  const cacheHealthy = checks[1].status === 'fulfilled'
  const healthy      = dbHealthy && cacheHealthy

  return c.json({
    status:    healthy ? 'healthy' : 'unhealthy',
    timestamp: new Date().toISOString(),
    checks: {
      database: dbHealthy ? 'ok' : 'error',
      cache:    cacheHealthy ? 'ok' : 'error',
    },
  }, healthy ? 200 : 503)
})
```

```yaml
# .github/workflows/deploy.yml
- name: Deploy to production
  run: vercel deploy --prod --token ${{ secrets.VERCEL_TOKEN }}

- name: Health check (with retry)
  run: |
    for i in 1 2 3 4 5; do
      STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://api.example.com/health)
      if [ "$STATUS" = "200" ]; then
        echo "Health check passed"
        exit 0
      fi
      echo "Attempt $i failed (status: $STATUS), retrying in 10s..."
      sleep 10
    done
    echo "Health check failed — triggering rollback"
    exit 1

- name: Rollback on failure
  if: failure()
  run: |
    PREV_DEPLOYMENT=$(vercel ls --token ${{ secrets.VERCEL_TOKEN }} | grep prod | tail -2 | head -1 | awk '{print $1}')
    vercel rollback $PREV_DEPLOYMENT --token ${{ secrets.VERCEL_TOKEN }}
    echo "Rolled back to $PREV_DEPLOYMENT"
```

### 4. Circuit Breaker Pattern

```typescript
// packages/shared/src/utils/circuitBreaker.ts
type CircuitState = 'CLOSED' | 'OPEN' | 'HALF_OPEN'

export class CircuitBreaker {
  private failures    = 0
  private lastFailure: Date | null = null
  private state: CircuitState = 'CLOSED'

  constructor(
    private readonly threshold = 5,        // failures before opening
    private readonly recoveryTimeout = 30000 // 30s before half-open
  ) {}

  async call<T>(fn: () => Promise<T>): Promise<T> {
    if (this.state === 'OPEN') {
      if (Date.now() - this.lastFailure!.getTime() > this.recoveryTimeout) {
        this.state = 'HALF_OPEN'
      } else {
        throw new Error('Circuit is OPEN — service unavailable')
      }
    }

    try {
      const result = await fn()
      this.onSuccess()
      return result
    } catch (error) {
      this.onFailure()
      throw error
    }
  }

  private onSuccess() {
    this.failures = 0
    this.state = 'CLOSED'
  }

  private onFailure() {
    this.failures++
    this.lastFailure = new Date()
    if (this.failures >= this.threshold) {
      this.state = 'OPEN'
    }
  }
}

// Usage
const stripeBreaker = new CircuitBreaker(3, 60000)
const payment = await stripeBreaker.call(() => stripe.charges.create(data))
```

### 5. Zero-Downtime DB Migrations (Expand-Backfill-Contract)

```bash
# Phase 1 — EXPAND (safe to deploy)
# Add new nullable column — no downtime
ALTER TABLE bookings ADD COLUMN confirmed_by UUID;

# Phase 2 — BACKFILL (background job, no downtime)
# Populate existing rows in batches
UPDATE bookings
SET confirmed_by = staff_id
WHERE confirmed_by IS NULL AND status = 'confirmed'
LIMIT 10000;

# Phase 3 — CONTRACT (safe after all rows populated)
# Add NOT NULL constraint
ALTER TABLE bookings ALTER COLUMN confirmed_by SET NOT NULL;
```

### 6. Retry with Exponential Backoff

```typescript
// packages/shared/src/utils/retry.ts
// Node.js context (API routes, services) — uses a portable sleep helper
// In Vercel Workflow sandbox context, use sleep() from "workflow" instead

// In Vercel Workflow DevKit: import { sleep } from 'workflow'
// In Node.js runtime / Fluid Compute: use @workspace/shared/utils/sleep
// import { sleep } from '@workspace/shared/utils/sleep'

export async function withRetry<T>(
  fn: () => Promise<T>,
  options: { maxAttempts?: number; baseDelay?: number; maxDelay?: number } = {}
): Promise<T> {
  const { maxAttempts = 3, baseDelay = 1000, maxDelay = 10000 } = options

  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      return await fn()
    } catch (error) {
      if (attempt === maxAttempts) throw error
      const delay = Math.min(baseDelay * 2 ** (attempt - 1), maxDelay)
      const jitter = Math.random() * 0.1 * delay
      await sleep(delay + jitter)
    }
  }
  throw new Error('Max retries reached')
}

// Usage
const bookings = await withRetry(() => bookingApi.list(query), { maxAttempts: 3 })
```

## @Automation Monitoring Triggers

```markdown
Auto-trigger self-healing when:
- CI test suite fails: retry flaky tests (up to 2 times)
- Deployment health check fails: rollback to previous version
- DB migration fails: run rollback migration, alert @DBA
- API error rate >5%: enable circuit breaker, alert @EscalationHandler
- Cache hit rate <70%: analyze pipeline inputs, @MetricsAgent alert
```

## Common Mistakes
- Migrations without down() — catastrophic during incidents
- Health checks that only ping (not test DB connection) — false healthy state
- Circuit breaker not used on external services (Stripe, email) — cascading failures
- Infinite retry loops — use max attempts + backoff + circuit breaker
- Rolling back without notifying on-call — silent rollbacks hide recurring issues

## Success Criteria
- [ ] All migrations include rollback SQL
- [ ] `/health` endpoint tests DB + critical dependencies
- [ ] Deployment pipeline has health check + auto-rollback step
- [ ] Circuit breaker wraps all external service calls
- [ ] Test retries configured in Vitest and Playwright
- [ ] Zero-downtime migration pattern used for all schema changes