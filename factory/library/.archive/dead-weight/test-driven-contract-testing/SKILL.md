# Test-Driven / Contract-Driven Testing Pyramid

## Purpose
Follow the CONTRACT → STUB → TEST → IMPLEMENT flow. Tests are derived from locked Zod contracts, making them the verification layer for contracts. If the contract changes and the test doesn't, drift is detected immediately.

## The D-CDD Flow

```
1. CONTRACT  → Zod schema locked in packages/shared/src/contracts/
2. STUB      → API/service stub that returns typed mock data
3. TEST      → Tests written against the stub (they MUST fail against empty impl)
4. IMPLEMENT → Real implementation written to make tests pass
```

## Testing Pyramid Targets

```
E2E Tests (Playwright)           5% of test budget
  Full user flows, critical paths

Integration Tests (Vitest)       30% of test budget
  API routes, service layer, DB queries

Unit Tests (Vitest)              45% of test budget
  Pure functions, validators, formatters, hooks

Contract Tests                   20% of test budget
  Every API response validated against Zod schema
```

## Contract Test Pattern

```typescript
// packages/shared/src/contracts/__tests__/booking.contract.test.ts
import { describe, it, expect } from 'vitest'
import { BookingSchema, CreateBookingSchema } from '../booking'

describe('BookingSchema contract tests', () => {
  it('validates a complete booking', () => {
    const validBooking = {
      id:          '550e8400-e29b-41d4-a716-446655440000',
      guestId:     '550e8400-e29b-41d4-a716-446655440001',
      venueId:     '550e8400-e29b-41d4-a716-446655440002',
      type:        'table',
      startsAt:    '2026-04-15T19:00:00.000Z',
      endsAt:      '2026-04-15T23:00:00.000Z',
      partySize:   4,
      status:      'confirmed',
      totalAmount: 2500,
      currency:    'EGP',
      createdAt:   '2026-04-08T10:00:00.000Z',
      updatedAt:   '2026-04-08T10:00:00.000Z',
    }
    expect(() => BookingSchema.parse(validBooking)).not.toThrow()
  })

  it('rejects negative party size', () => {
    const result = CreateBookingSchema.safeParse({ ...validCreateBooking, partySize: -1 })
    expect(result.success).toBe(false)
    expect(result.error?.issues[0].path).toEqual(['partySize'])
  })

  it('rejects invalid currency', () => {
    const result = CreateBookingSchema.safeParse({ ...validCreateBooking, currency: 'GBP' })
    expect(result.success).toBe(false)
  })

  it('rejects overlapping booking dates', () => {
    const result = CreateBookingSchema.safeParse({
      ...validCreateBooking,
      startsAt: '2026-04-15T23:00:00.000Z',
      endsAt:   '2026-04-15T19:00:00.000Z', // end before start
    })
    // Refine-based validation
    expect(result.success).toBe(false)
  })
})
```

## Unit Test Pattern

```typescript
// packages/shared/src/utils/__tests__/formatting.test.ts
import { describe, it, expect } from 'vitest'
import { formatCurrency, formatDate } from '../formatting'

describe('formatCurrency', () => {
  it('formats EGP in en locale', () => {
    expect(formatCurrency(1500, 'EGP', 'en')).toBe('EGP 1,500.00')
  })

  it('formats EGP in ar locale with Arabic numerals', () => {
    const result = formatCurrency(1500, 'EGP', 'ar')
    expect(result).toContain('١٬٥٠٠')
  })

  it('handles zero amount', () => {
    expect(formatCurrency(0, 'USD', 'en')).toBe('$0.00')
  })

  it('handles large amounts', () => {
    expect(formatCurrency(1_000_000, 'EGP', 'en')).toBe('EGP 1,000,000.00')
  })
})
```

## Integration Test Pattern (API)

```typescript
// apps/api/src/routes/__tests__/bookings.integration.test.ts
import { describe, it, expect, beforeAll, afterAll, afterEach } from 'vitest'
import { createTestApp } from '../test-utils/app'
import { createTestDb, cleanDb } from '../test-utils/db'
import { BookingSchema } from '@workspace/shared/contracts/booking'

describe('POST /api/bookings', () => {
  let app: TestApp
  let db: TestDb

  beforeAll(async () => {
    db = await createTestDb()
    app = await createTestApp({ db })
  })

  afterEach(async () => { await cleanDb(db) })
  afterAll(async () => { await db.disconnect() })

  it('creates booking and returns valid contract shape', async () => {
    const token = await getTestToken('manager')
    const response = await app.request('/api/bookings', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        guestId:   testGuestId,
        venueId:   testVenueId,
        type:      'table',
        startsAt:  '2026-04-15T19:00:00.000Z',
        endsAt:    '2026-04-15T23:00:00.000Z',
        partySize: 4,
        currency:  'EGP',
      }),
    })

    expect(response.status).toBe(201)
    const body = await response.json()

    // ✅ Contract validation — always validate API response against schema
    const result = BookingSchema.safeParse(body)
    expect(result.success).toBe(true)
    expect(body.status).toBe('pending')
  })

  it('returns 401 without authentication', async () => {
    const response = await app.request('/api/bookings', { method: 'POST' })
    expect(response.status).toBe(401)
  })

  it('returns 400 with invalid party size', async () => {
    const token = await getTestToken('manager')
    const response = await app.request('/api/bookings', {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({ ...validBookingData, partySize: 0 }),
    })
    expect(response.status).toBe(400)
  })
})
```

## Hook Test Pattern (Frontend)

```typescript
// apps/web/src/hooks/__tests__/useBookings.test.ts
import { renderHook, waitFor } from '@testing-library/react'
import { QueryClientProvider } from '@tanstack/react-query'
import { describe, it, expect, vi } from 'vitest'
import { useBookings } from '../useBookings'

describe('useBookings', () => {
  it('returns bookings from API', async () => {
    const mockBookings = [mockBooking]
    vi.spyOn(bookingApi, 'list').mockResolvedValue(mockBookings)

    const { result } = renderHook(() => useBookings(), {
      wrapper: createQueryWrapper(),
    })

    await waitFor(() => expect(result.current.isSuccess).toBe(true))
    expect(result.current.data).toEqual(mockBookings)
  })

  it('handles API error gracefully', async () => {
    vi.spyOn(bookingApi, 'list').mockRejectedValue(new Error('Network error'))

    const { result } = renderHook(() => useBookings(), { wrapper: createQueryWrapper() })

    await waitFor(() => expect(result.current.isError).toBe(true))
    expect(result.current.error?.message).toBe('Network error')
  })
})
```

## Vitest Configuration

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',  // 'jsdom' for frontend tests
    coverage: {
      provider: 'v8',
      thresholds: {
        lines:     90,
        functions: 90,
        branches:  85,
        statements: 90,
      },
      exclude: ['**/*.config.*', '**/*.d.ts', '**/index.ts'],
    },
    reporters: ['verbose', 'html'],
  },
})
```

## Common Mistakes
- Writing tests after implementation — defeats contract-driven detection
- Not validating API response against Zod in integration tests — contract drift goes undetected
- Using `any` in test mocks — type safety disappears
- Mocking the database in integration tests — masks real query issues
- Testing implementation details instead of behavior

## Success Criteria
- [ ] CONTRACT exists and is locked before first test is written
- [ ] Unit tests: ≥45% of test suite, ≥90% function coverage
- [ ] Integration tests: ≥30% of test suite, all API routes covered
- [ ] Every API endpoint integration test validates response against Zod schema
- [ ] E2E tests cover the 3-5 most critical user journeys
- [ ] CI fails if any coverage threshold drops