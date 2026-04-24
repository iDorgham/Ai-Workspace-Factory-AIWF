# Edge Case & Boundary Testing

## Purpose
Cover the scenarios that "normal" tests miss — empty states, max limits, concurrent requests, network failure, unauthorized access, and Arabic text edge cases. Most production bugs live in these gaps.

## Edge Case Categories

### 1. Boundary Values (Contract-Derived)
```typescript
// For every numeric/string field in the contract, test the boundaries
// BookingSchema: partySize z.number().int().min(1).max(500)

describe('partySize boundaries', () => {
  it('accepts minimum value (1)',        () => expect(CreateBookingSchema.parse({...data, partySize: 1})).toBeDefined())
  it('accepts maximum value (500)',      () => expect(CreateBookingSchema.parse({...data, partySize: 500})).toBeDefined())
  it('rejects zero',                     () => expect(() => CreateBookingSchema.parse({...data, partySize: 0})).toThrow())
  it('rejects negative',                 () => expect(() => CreateBookingSchema.parse({...data, partySize: -1})).toThrow())
  it('rejects over maximum (501)',       () => expect(() => CreateBookingSchema.parse({...data, partySize: 501})).toThrow())
  it('rejects float (2.5)',              () => expect(() => CreateBookingSchema.parse({...data, partySize: 2.5})).toThrow())
  it('rejects string ("4")',             () => expect(() => CreateBookingSchema.parse({...data, partySize: '4'})).toThrow())
})
```

### 2. Empty & Null States (UI)
```typescript
// Test every list/async component with empty data
describe('BookingList empty states', () => {
  it('shows empty state when no bookings', () => {
    render(<BookingList bookings={[]} />)
    expect(screen.getByText(t('booking.empty'))).toBeInTheDocument()
    expect(screen.queryByRole('row')).not.toBeInTheDocument()
  })

  it('shows skeleton when loading', () => {
    render(<BookingList bookings={undefined} isLoading={true} />)
    expect(screen.getAllByTestId('booking-skeleton')).toHaveLength(5)
  })

  it('shows error state on fetch failure', () => {
    render(<BookingList error={new Error('Network error')} />)
    expect(screen.getByRole('alert')).toBeInTheDocument()
    expect(screen.getByText(/try again/i)).toBeInTheDocument()
  })
})
```

### 3. Arabic Text Edge Cases
```typescript
describe('Arabic text edge cases', () => {
  it('renders long Arabic venue names without overflow', async ({ page }) => {
    // Arabic words can be significantly longer than English equivalents
    const longArabicName = 'منتجع وفندق الشاطئ الذهبي الكبير بالغردقة'
    await page.goto(`/ar/venues/${venueWithLongName.id}`)
    // Check no horizontal overflow
    const nameEl = page.locator('[data-testid="venue-name"]')
    const overflow = await nameEl.evaluate(el => el.scrollWidth > el.clientWidth)
    expect(overflow).toBe(false)
  })

  it('handles Arabic numerals in amounts (ar locale)', async ({ page }) => {
    await page.goto('/ar/bookings')
    const amount = page.locator('[data-testid="booking-amount"]').first()
    // Arabic locale should show Arabic-Indic numerals
    await expect(amount).toContainText(/[٠-٩]/)
  })

  it('RTL layout does not break with mixed Arabic/English content', async ({ page }) => {
    await page.addInitScript(() => { document.documentElement.dir = 'rtl' })
    await page.goto('/ar/dashboard')
    // No layout shifts or broken flex containers
    await expect(page).toHaveScreenshot('dashboard-rtl-mixed-content.png')
  })
})
```

### 4. Concurrent Request Scenarios
```typescript
describe('Concurrent booking creation', () => {
  it('prevents double booking via optimistic locking', async () => {
    // Simulate two simultaneous booking requests for the same slot
    const bookingData = { venueId, startsAt: '2026-04-15T19:00Z', partySize: 4 }

    const [result1, result2] = await Promise.all([
      createBooking(bookingData, user1Token),
      createBooking(bookingData, user2Token),
    ])

    // Only one should succeed
    const statuses = [result1.status, result2.status]
    expect(statuses).toContain(201) // one success
    expect(statuses).toContain(409) // one conflict
  })
})
```

### 5. Authorization Edge Cases
```typescript
describe('Cross-tenant access prevention', () => {
  it('prevents manager from accessing another tenant bookings', async () => {
    const otherTenantBookingId = await createBookingForOtherTenant()
    const response = await app.request(`/api/bookings/${otherTenantBookingId}`, {
      headers: { Authorization: `Bearer ${managerToken}` }
    })
    expect(response.status).toBe(404) // 404 not 403 — don't leak existence
  })

  it('prevents guest from cancelling another guest booking', async () => {
    const otherGuestBookingId = await createBookingForOtherGuest()
    const response = await app.request(`/api/bookings/${otherGuestBookingId}`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${guestToken}` }
    })
    expect(response.status).toBe(403)
  })
})
```

### 6. Network & Timeout Scenarios
```typescript
// Playwright: slow network simulation
test('shows loading state on slow API', async ({ page }) => {
  await page.route('/api/bookings', async route => {
    await new Promise(r => globalThis.setTimeout(r, 3000))
    await route.continue()
  })
  await page.goto('/bookings')
  await expect(page.locator('[data-testid="loading-spinner"]')).toBeVisible()
})

// API: timeout handling
test('returns 503 when DB is unavailable', async () => {
  await prisma.$disconnect()
  const response = await app.request('/api/bookings')
  expect(response.status).toBe(503)
  expect(await response.json()).toMatchObject({ error: expect.any(String) })
})
```

### 7. Financial Edge Cases
```typescript
describe('Currency and amount edge cases', () => {
  it('rejects negative amounts', () => {
    expect(() => MoneySchema.parse({ amount: -100, currency: 'EGP' })).toThrow()
  })

  it('handles zero amount (free bookings)', () => {
    expect(MoneySchema.parse({ amount: 0, currency: 'EGP' })).toBeDefined()
  })

  it('prevents floating point storage (stores as integer minor units)', () => {
    const money = MoneySchema.parse({ amount: 15000, currency: 'EGP' })
    expect(Number.isInteger(money.amount)).toBe(true)
    // 15000 piastres = 150.00 EGP
  })
})
```

## Edge Case Test Plan Template (Required in Feature Plans)

```markdown
## Edge Case Test Plan — [Feature Name]

### Boundary Values
- [ ] Min/max for all numeric fields
- [ ] Empty string / max length string
- [ ] Required field missing
- [ ] Extra unknown fields (should be stripped by Zod)

### Empty & Error States (UI)
- [ ] Empty list
- [ ] Loading state
- [ ] Error/failure state
- [ ] Partial data (some fields null/undefined)

### Arabic/RTL
- [ ] Long Arabic text without overflow
- [ ] Arabic numerals in financial data
- [ ] RTL layout with mixed content
- [ ] Arabic form validation messages

### Authorization
- [ ] Unauthenticated request → 401
- [ ] Wrong role → 403
- [ ] Cross-tenant access → 404 (not 403 — don't leak)
- [ ] Own resource vs others' resource

### Concurrency
- [ ] Double-submit prevention
- [ ] Race condition on shared resource (double booking)

### Network
- [ ] Slow response → loading state visible
- [ ] Service unavailable → graceful error
```

## Common Mistakes
- Testing only the happy path — production bugs live in edge cases
- Not testing Arabic text length — Arabic words overflow English-sized containers
- Missing cross-tenant tests — tenant isolation bugs are security incidents
- No concurrent request tests — double bookings are expensive incidents
- Testing authorization only at role level — missing resource-level checks

## Success Criteria
- [ ] Edge case test plan in every feature plan before `/build`
- [ ] All contract field boundaries tested (min, max, null, type mismatch)
- [ ] Empty states tested for all list/async components
- [ ] Arabic text edge cases covered in RTL test suite
- [ ] Cross-tenant access tests in every API route test suite