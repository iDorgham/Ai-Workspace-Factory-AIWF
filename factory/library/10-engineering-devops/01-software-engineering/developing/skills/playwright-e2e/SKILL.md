---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# Playwright E2E + Accessibility Automation

## Purpose
Test the 3–7 most critical user journeys end-to-end. Resilient selectors (role-based, not CSS-fragile). Locale testing for EN/AR parity. Automated axe-core accessibility audit on every page.

## Critical Journeys to Cover (Priority Order)

```
1. Authentication (login, logout, session refresh)
2. Core booking/reservation flow (create, confirm, cancel)
3. Membership enrollment (sign up, payment, access)
4. Admin operations (create, update, manage records)
5. Search + filter (find bookings/members)
6. Error recovery (failed payment, validation errors)
7. RTL/Arabic locale (same journeys in Arabic)
```

## Page Object Pattern (Maintainable Selectors)

```typescript
// e2e/page-objects/BookingPage.ts
import { type Page, type Locator } from '@playwright/test'

export class BookingPage {
  readonly createButton:  Locator
  readonly partySizeInput: Locator
  readonly dateInput:     Locator
  readonly submitButton:  Locator
  readonly successToast:  Locator
  readonly errorMessage:  Locator

  constructor(private page: Page) {
    // ✅ Role-based selectors — resilient to CSS changes
    this.createButton   = page.getByRole('button', { name: /new booking|حجز جديد/i })
    this.partySizeInput = page.getByLabel(/party size|حجم المجموعة/i)
    this.dateInput      = page.getByLabel(/date|التاريخ/i)
    this.submitButton   = page.getByRole('button', { name: /confirm booking|تأكيد الحجز/i })
    this.successToast   = page.getByRole('status').filter({ hasText: /confirmed|مؤكد/i })
    this.errorMessage   = page.getByRole('alert')
  }

  async goto() {
    await this.page.goto('/bookings')
    await this.page.waitForLoadState('networkidle')
  }

  async createBooking(options: { partySize: number; date: string }) {
    await this.createButton.click()
    await this.partySizeInput.fill(String(options.partySize))
    await this.dateInput.fill(options.date)
    await this.submitButton.click()
  }
}
```

## E2E Test Structure

```typescript
// e2e/booking-flow.spec.ts
import { test, expect } from '@playwright/test'
import { BookingPage } from './page-objects/BookingPage'
import { AuthHelper } from './helpers/auth'

test.describe('Booking Flow — LTR (English)', () => {
  let bookingPage: BookingPage

  test.beforeEach(async ({ page }) => {
    await AuthHelper.loginAsManager(page)
    bookingPage = new BookingPage(page)
    await bookingPage.goto()
  })

  test('creates booking successfully', async ({ page }) => {
    await bookingPage.createBooking({ partySize: 4, date: '2026-04-15' })
    await expect(bookingPage.successToast).toBeVisible()
    await expect(page.getByRole('row').last()).toContainText('Pending')
  })

  test('shows validation error for party size 0', async () => {
    await bookingPage.createBooking({ partySize: 0, date: '2026-04-15' })
    await expect(bookingPage.errorMessage).toBeVisible()
    await expect(bookingPage.errorMessage).toContainText(/party size/i)
  })

  test('cancels booking', async ({ page }) => {
    // Create first, then cancel
    await bookingPage.createBooking({ partySize: 2, date: '2026-04-15' })
    await page.getByRole('button', { name: /cancel/i }).first().click()
    await page.getByRole('button', { name: /confirm cancellation/i }).click()
    await expect(page.getByRole('row').last()).toContainText('Cancelled')
  })
})

test.describe('Booking Flow — RTL (Arabic)', () => {
  test.use({ locale: 'ar-EG' })

  test.beforeEach(async ({ page }) => {
    await page.addInitScript(() => { document.documentElement.dir = 'rtl' })
    await AuthHelper.loginAsManager(page)
  })

  test('creates booking in Arabic', async ({ page }) => {
    const bookingPage = new BookingPage(page)
    await bookingPage.goto()
    await bookingPage.createBooking({ partySize: 4, date: '2026-04-15' })
    await expect(bookingPage.successToast).toBeVisible()
  })
})
```

## Authentication Helper

```typescript
// e2e/helpers/auth.ts
import { type Page } from '@playwright/test'

export const AuthHelper = {
  async loginAsManager(page: Page) {
    await page.goto('/auth/login')
    await page.getByLabel(/email|البريد/i).fill('manager@test.com')
    await page.getByLabel(/password|كلمة المرور/i).fill('Test1234!')
    await page.getByRole('button', { name: /sign in|تسجيل الدخول/i }).click()
    await page.waitForURL('/dashboard')
  },

  async loginAsAdmin(page: Page) {
    await page.goto('/auth/login')
    await page.getByLabel(/email/i).fill('admin@test.com')
    await page.getByLabel(/password/i).fill('Test1234!')
    await page.getByRole('button', { name: /sign in/i }).click()
    await page.waitForURL('/dashboard')
  },

  // Faster: inject token via localStorage/cookie (bypass UI)
  async injectSession(page: Page, role: 'manager' | 'admin' = 'manager') {
    const token = generateTestToken(role)
    await page.addInitScript((t) => {
      window.__GALERIA_TEST_TOKEN__ = t
    }, token)
  },
}
```

## Automated Accessibility Testing

```typescript
// e2e/accessibility.spec.ts
import { test, expect } from '@playwright/test'
import AxeBuilder from '@axe-core/playwright'

const pagesToTest = [
  { path: '/bookings', name: 'Bookings List' },
  { path: '/bookings/new', name: 'New Booking' },
  { path: '/members', name: 'Members' },
  { path: '/dashboard', name: 'Dashboard' },
]

for (const { path, name } of pagesToTest) {
  test.describe(`Accessibility — ${name}`, () => {
    test('has no WCAG AA violations - LTR', async ({ page }) => {
      await AuthHelper.loginAsManager(page)
      await page.goto(path)
      await page.waitForLoadState('networkidle')

      const results = await new AxeBuilder({ page })
        .withTags(['wcag2a', 'wcag2aa', 'wcag21aa'])
        .exclude('[data-testid="map"]') // third-party widgets
        .analyze()

      expect(results.violations).toEqual([])
    })

    test('has no WCAG AA violations - RTL', async ({ page }) => {
      await page.addInitScript(() => { document.documentElement.dir = 'rtl' })
      await AuthHelper.loginAsManager(page)
      await page.goto(`/ar${path}`)
      await page.waitForLoadState('networkidle')

      const results = await new AxeBuilder({ page })
        .withTags(['wcag2a', 'wcag2aa'])
        .analyze()

      expect(results.violations).toEqual([])
    })
  })
}
```

## Self-Healing Strategy (Flaky Test Recovery)

```typescript
// When selectors break after UI changes:
// Step 1: Add data-testid to component (never use CSS/text first)
// Step 2: Update Page Object selector

// Flaky network — use route intercept
test('handles slow API', async ({ page }) => {
  await page.route('/api/bookings', async route => {
    await new Promise(resolve => setTimeout(resolve, 2000)) // simulate slow
    await route.continue()
  })
  await bookingPage.goto()
  await expect(page.getByRole('progressbar')).toBeVisible()
  await expect(page.getByRole('table')).toBeVisible({ timeout: 10_000 })
})
```

## Common Mistakes
- Using CSS selectors in E2E tests — breaks on refactor, use `getByRole`/`getByLabel`
- Testing everything E2E — E2E is slow; unit tests cover logic
- No RTL E2E tests — Arabic journeys fail silently
- Not cleaning test data between runs — state leaks cause flaky tests
- Real API calls in tests without mocking — slow, non-deterministic

## Success Criteria
- [ ] 3–7 critical journeys covered in E2E
- [ ] Same journeys covered in both EN and AR locale
- [ ] All selectors role-based or label-based (no CSS)
- [ ] Axe accessibility audit runs on every main page
- [ ] Test suite completes in <5 minutes on CI
- [ ] Zero flaky tests in last 10 CI runs