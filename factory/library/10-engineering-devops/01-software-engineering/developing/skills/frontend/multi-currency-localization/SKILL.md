---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# Multi-Currency + Regional Localization

## Purpose
Handle EGP, USD, EUR, and SAR accurately for Hurghada's international guest mix. Egyptian tourists pay in EGP, European tourists in EUR/USD, Gulf visitors in SAR. All amounts stored as integers (minor units) — never floats.

## Currency Contract

```typescript
// packages/shared/src/contracts/currency.ts
import { z } from 'zod'

export const CurrencyEnum = z.enum(['EGP', 'USD', 'EUR', 'SAR', 'GBP'])
export type Currency = z.infer<typeof CurrencyEnum>

// Always store amounts as integers (minor units)
// EGP: 1500 = 15.00 EGP (piastres)
// USD: 1000 = $10.00 USD (cents)
export const MoneySchema = z.object({
  amount:   z.number().int().nonnegative(), // stored in minor units
  currency: CurrencyEnum,
})
export type Money = z.infer<typeof MoneySchema>
```

## Safe Money Arithmetic (Dinero.js)

```typescript
// packages/shared/src/utils/money.ts
import { dinero, add, subtract, multiply, toDecimal, toSnapshot } from 'dinero.js'
import { EGP, USD, EUR, SAR } from '@dinero.js/currencies'

const CURRENCY_MAP = { EGP, USD, EUR, SAR }

export function createMoney(amount: number, currency: Currency) {
  return dinero({ amount, currency: CURRENCY_MAP[currency] })
}

// ✅ Safe addition — no floating point errors
export function addMoney(a: Money, b: Money): Money {
  if (a.currency !== b.currency) throw new Error('Cannot add different currencies')
  const result = add(createMoney(a.amount, a.currency), createMoney(b.amount, b.currency))
  const { amount, currency } = toSnapshot(result)
  return { amount, currency: currency.code as Currency }
}

// ✅ Percentage calculation (for service charges, VAT)
export function applyPercentage(money: Money, percent: number): Money {
  const result = multiply(createMoney(money.amount, money.currency), { amount: percent, scale: 2 })
  const { amount, currency } = toSnapshot(result)
  return { amount, currency: currency.code as Currency }
}

// Convert to display decimal for rendering
export function toDisplayAmount(money: Money): string {
  return toDecimal(createMoney(money.amount, money.currency))
}
```

## Currency Display (Locale-Aware)

```typescript
// packages/shared/src/utils/formatting.ts
export function formatMoney(money: Money, locale: string): string {
  const amount = Number(toDisplayAmount(money))

  return new Intl.NumberFormat(locale === 'ar' ? 'ar-EG' : 'en-US', {
    style:                 'currency',
    currency:              money.currency,
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(amount)
}

// Results:
// formatMoney({ amount: 150000, currency: 'EGP' }, 'en') → "EGP 1,500.00"
// formatMoney({ amount: 150000, currency: 'EGP' }, 'ar') → "١٬٥٠٠٫٠٠ ج.م."
// formatMoney({ amount: 9999, currency: 'USD' }, 'en')   → "$99.99"
// formatMoney({ amount: 9999, currency: 'EUR' }, 'ar')   → "٩٩٫٩٩ €"
```

## Egypt VAT (14%)

```typescript
// packages/shared/src/utils/tax.ts
const EGYPT_VAT_RATE = 14 // 14% standard rate

export function addEgyptVAT(subtotal: Money): { subtotal: Money; vat: Money; total: Money } {
  const vat = applyPercentage(subtotal, EGYPT_VAT_RATE)
  const total = addMoney(subtotal, vat)
  return { subtotal, vat, total }
}

// Tourism service charge (common in Red Sea hospitality: 12%)
export function addServiceCharge(subtotal: Money, percent = 12): Money {
  return applyPercentage(subtotal, percent)
}
```

## DB Schema (Integer Storage)

```prisma
model Booking {
  totalAmount   Int    // stored as minor units (piastres/cents)
  depositAmount Int    @default(0)
  currency      String // 'EGP' | 'USD' | 'EUR' | 'SAR'
}

model Payment {
  amount        Int
  currency      String
  exchangeRate  Decimal? // rate at time of payment (for reporting)
  paidIn        String   // original currency if different from booking
}
```

## Exchange Rate Display (Read-Only)

```typescript
// Exchange rates for display only — never for settlement
// Settlements always in booking currency
export async function getDisplayRate(from: Currency, to: Currency): Promise<number> {
  // Cache rates for 1 hour
  const cached = await redis.get(`rate:${from}:${to}`)
  if (cached) return Number(cached)

  // Fetch from exchange rate API
  const rate = await fetchExchangeRate(from, to)
  await redis.setex(`rate:${from}:${to}`, 3600, String(rate))
  return rate
}
```

## Regional Number Formats

```typescript
// Arabic-Indic numerals for Arabic locale
export function formatNumber(value: number, locale: string): string {
  return new Intl.NumberFormat(locale === 'ar' ? 'ar-EG' : 'en-US').format(value)
}
// Arabic: ١٬٥٠٠ | English: 1,500

// Date formatting with Cairo timezone
export function formatBookingDate(iso: string, locale: string): string {
  return new Intl.DateTimeFormat(locale === 'ar' ? 'ar-EG' : 'en-US', {
    weekday: 'long',
    year:    'numeric',
    month:   'long',
    day:     'numeric',
    hour:    '2-digit',
    minute:  '2-digit',
    timeZone: 'Africa/Cairo',
  }).format(new Date(iso))
}
// Arabic:  "الخميس، ١٥ أبريل ٢٠٢٦ في ٧:٠٠ م"
// English: "Thursday, April 15, 2026 at 7:00 PM"
```

## Common Mistakes
- Storing amounts as floats (0.1 + 0.2 ≠ 0.3 in floating point) — always use integers
- Doing currency arithmetic without Dinero.js — rounding errors accumulate
- Displaying USD format for SAR — each currency has different symbol placement
- Forgetting to apply Egypt VAT (14%) on taxable services
- Using exchange rates for settlement — always settle in booking currency
- Hardcoding currency symbols — use `Intl.NumberFormat` with currency option

## Success Criteria
- [ ] All money amounts stored as integers (minor units) in DB
- [ ] `Dinero.js` used for all arithmetic operations
- [ ] `Intl.NumberFormat` used for all display formatting
- [ ] Arabic locale shows Arabic-Indic numerals
- [ ] Egypt VAT (14%) applied where legally required
- [ ] Exchange rates cached, never used for settlement