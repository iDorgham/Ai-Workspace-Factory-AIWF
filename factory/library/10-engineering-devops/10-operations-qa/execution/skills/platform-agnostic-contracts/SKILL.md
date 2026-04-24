---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# Platform-Agnostic Contracts & Adapters

## Purpose
Write contracts once in `packages/shared/` that work identically on web (Next.js), mobile (React Native), and backend (Hono/NestJS). Platform-specific behavior lives in adapters, never in contracts.

## When to Activate
- Building features that must work on both web and mobile
- Adding a new platform (e.g., admin dashboard, mobile app)
- When a contract would need platform-specific logic

## Contract Layer (Platform-Neutral)

```typescript
// packages/shared/src/contracts/membership.ts
// ✅ Pure Zod — no platform imports, no Next.js, no React Native
import { z } from 'zod'

export const MembershipSchema = z.object({
  id:          z.string().uuid(),
  memberId:    z.string().uuid(),
  clubId:      z.string().uuid(),
  tier:        z.enum(['basic', 'silver', 'gold', 'vip']),
  startsAt:    z.string().datetime(),
  expiresAt:   z.string().datetime(),
  autoRenew:   z.boolean().default(true),
  qrCode:      z.string(),
  status:      z.enum(['active', 'expired', 'suspended', 'cancelled']),
  benefits:    z.array(z.string()),
  monthlyFee:  z.number().nonnegative(),
  currency:    z.enum(['EGP', 'USD', 'EUR', 'SAR']),
})

export type MembershipType = z.infer<typeof MembershipSchema>
```

## Platform Adapters Pattern

```typescript
// packages/platform-adapters/src/storage/index.ts
// Defines the contract for storage operations
export interface StorageAdapter {
  getItem(key: string): Promise<string | null>
  setItem(key: string, value: string): Promise<void>
  removeItem(key: string): Promise<void>
}

// packages/platform-adapters/src/storage/web.ts
export class WebStorageAdapter implements StorageAdapter {
  async getItem(key: string) {
    return document.cookie.match(`(^|;)\\s*${key}\\s*=\\s*([^;]+)`)?.pop() ?? null
  }
  async setItem(key: string, value: string) {
    document.cookie = `${key}=${value}; Secure; SameSite=Strict`
  }
  async removeItem(key: string) {
    document.cookie = `${key}=; Max-Age=0`
  }
}

// packages/platform-adapters/src/storage/native.ts
import AsyncStorage from '@react-native-async-storage/async-storage'
export class NativeStorageAdapter implements StorageAdapter {
  async getItem(key: string) { return AsyncStorage.getItem(key) }
  async setItem(key: string, value: string) { return AsyncStorage.setItem(key, value) }
  async removeItem(key: string) { return AsyncStorage.removeItem(key) }
}
```

## API Client Pattern (Platform-Neutral)

```typescript
// packages/shared/src/api/bookings.ts
// ✅ Uses fetch — works on web, React Native, and Node.js
import { BookingQuerySchema, BookingType, CreateBookingType } from '../contracts/booking'

export class BookingApiClient {
  constructor(
    private baseUrl: string,
    private getToken: () => Promise<string>
  ) {}

  async list(query: BookingQueryType): Promise<BookingType[]> {
    const params = new URLSearchParams(Object.entries(query).map(([k, v]) => [k, String(v)]))
    const response = await fetch(`${this.baseUrl}/api/bookings?${params}`, {
      headers: { Authorization: `Bearer ${await this.getToken()}` }
    })
    if (!response.ok) throw new Error('Failed to fetch bookings')
    return response.json()
  }

  async create(data: CreateBookingType): Promise<BookingType> {
    const response = await fetch(`${this.baseUrl}/api/bookings`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${await this.getToken()}`
      },
      body: JSON.stringify(data)
    })
    if (!response.ok) throw new Error('Failed to create booking')
    return response.json()
  }
}
```

## Cross-Platform Parity Checklist

Every multi-platform feature plan MUST include:

```markdown
## Platform Parity Checklist

### Web (Next.js)
- [ ] Route: /[feature] renders correctly
- [ ] Server Action validates contract
- [ ] RTL layout works with `dir="rtl"`
- [ ] Accessible (keyboard nav + ARIA)

### Mobile (React Native + Expo)
- [ ] Screen component mirrors web functionality
- [ ] Uses NativeStorageAdapter (not Web)
- [ ] RTL layout uses StyleSheet logical properties
- [ ] Accessible (AccessibilityInfo + role props)

### Shared
- [ ] Same Zod contract used on both platforms
- [ ] Same API client from packages/shared
- [ ] Same business logic from packages/shared
- [ ] Arabic/English translation keys identical
- [ ] Test coverage: web + mobile both ≥90%
```

## Token Constants for React Native

```typescript
// packages/ui/src/lib/styles/tokens.ts
// ✅ JavaScript/TypeScript token file for non-CSS environments
export const tokens = {
  color: {
    primary:          '#1B4F72',
    primaryHover:     '#154360',
    surface:          '#FFFFFF',
    contentPrimary:   '#0F172A',
    contentSecondary: '#64748B',
    error:            '#EF4444',
    success:          '#22C55E',
  },
  spacing: {
    xs:  4,
    sm:  8,
    md:  12,
    lg:  16,
    xl:  24,
    '2xl': 32,
    '3xl': 48,
  },
  radius: {
    sm:   4,
    md:   6,
    lg:   8,
    xl:   12,
    full: 9999,
  },
  fontSize: {
    sm:  14,
    md:  16,
    lg:  18,
    xl:  20,
    '2xl': 24,
  },
} as const
```

## Common Mistakes
- Importing Next.js-specific modules in `packages/shared/` — breaks React Native
- Using CSS in shared contracts — use tokens.ts for React Native
- Duplicating business logic per platform instead of putting it in packages/shared
- Writing separate API calls per platform instead of a shared client

## Success Criteria
- [ ] All contracts in `packages/shared/` have zero platform imports
- [ ] Platform-specific behavior isolated in `packages/platform-adapters/`
- [ ] API client shared across platforms
- [ ] `tokens.ts` exported alongside `tokens.css` for native use
- [ ] Cross-platform parity checklist included in feature plan