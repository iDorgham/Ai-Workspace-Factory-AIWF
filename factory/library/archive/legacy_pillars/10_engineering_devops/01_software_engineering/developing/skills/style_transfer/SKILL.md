---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# Style Transfer & Brand Application

## Purpose
Apply brand-specific styles across multiple brands or white-label solutions while maintaining strict brand isolation. Enables multi-brand workspaces where each brand has distinct visual identity without cross-contamination.

## When to Activate
- Multi-brand projects (hospitality portfolio, white-label SaaS)
- Theme switching (light/dark, brand-specific themes)
- Applying brand grammar to new components
- White-label client onboarding

## Step-by-Step Execution

### 1. Multi-Brand Architecture

**Directory Structure:**
```
.ai/context/brands/
├── [brand-a]/
│   ├── brand_grammar.md     ← Brand A's emotional intent, voice, visual doctrine
│   ├── tokens.css           ← Brand A token overrides
│   ├── palette.json         ← Brand A full color palette
│   └── assets/              ← Brand A logos, fonts, imagery
├── [brand-b]/
│   ├── brand_grammar.md
│   ├── tokens.css
│   ├── palette.json
│   └── assets/
└── shared/
    └── base-tokens.css      ← Shared foundations (spacing, z-index, animation)
```

**Brand Namespace Isolation:**
```css
/* packages/ui/src/lib/styles/themes/brand/[brand-name].css */

/* ✅ CORRECT — brand-specific overrides */
:root[data-brand="brand-a"] {
  /* Brand A: Luxury hospitality */
  --color-primary: #0B4F6C;
  --color-primary-hover: #093D54;
  --font-family-display: 'Playfair Display Variable', serif;
  --radius-card: var(--radius-2xl);
  --shadow-card: var(--shadow-xl);
  --duration-animation: 400ms; /* Slow, smooth = luxury */
}

:root[data-brand="brand-b"] {
  /* Brand B: Bold entertainment */
  --color-primary: #E63946;
  --color-primary-hover: #C1121F;
  --font-family-display: 'Poppins Variable', sans-serif;
  --radius-card: var(--radius-sm); /* Sharp = bold */
  --shadow-card: 0 0 20px rgba(230, 57, 70, 0.3); /* Glow effect */
  --duration-animation: 150ms; /* Fast, energetic */
}

/* ❌ FORBIDDEN — brand bleeding */
:root[data-brand="brand-a"] {
  --color-primary: var(--brand-b-primary); /* Never reference other brand */
}
```

### 2. Brand Application Pipeline

**Step 1 — Brand Selection:**
```tsx
// apps/web/src/app/layout.tsx — brand-aware root
import { getActiveBrand } from '@/lib/brand-config'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  const brand = getActiveBrand() // From env, subdomain, or user preference
  
  return (
    <html 
      lang={brand.defaultLang} 
      dir={brand.defaultDir}
      data-brand={brand.id}
      data-theme={brand.defaultTheme}
    >
      <body className={brand.fontClass}>{children}</body>
    </html>
  )
}
```

**Step 2 — Token Loading:**
```typescript
// apps/web/src/lib/brand-config.ts
interface BrandConfig {
  id: string
  name: string
  archetype: 'luxury' | 'bold' | 'gov-tech' | 'empowering' | 'calm'
  defaultLang: 'en' | 'ar'
  defaultDir: 'ltr' | 'rtl'
  defaultTheme: 'light' | 'dark'
  fontClass: string
  emotionalIntent: string
  visualDoctrine: string[]
}

const BRAND_REGISTRY: Record<string, BrandConfig> = {
  'red-sea-resort': {
    id: 'red-sea-resort',
    name: 'Red Sea Resort',
    archetype: 'luxury',
    defaultLang: 'en',
    defaultDir: 'ltr',
    defaultTheme: 'light',
    fontClass: 'font-playfair',
    emotionalIntent: 'Exclusivity, sophistication, aspirational experience',
    visualDoctrine: [
      'Generous whitespace (minimum 48px section padding)',
      'Dark/deep palettes OR white with gold accents',
      'Serif display fonts',
      'Large border-radius (--radius-2xl or --radius-3xl)',
      'Deep shadows (--shadow-xl)',
      'Slow, smooth animations (300-500ms ease-out)',
    ],
  },
  'neon-lounge': {
    id: 'neon-lounge',
    name: 'Neon Lounge',
    archetype: 'bold',
    defaultLang: 'en',
    defaultDir: 'ltr',
    defaultTheme: 'dark',
    fontClass: 'font-poppins',
    emotionalIntent: 'Energy, excitement, exclusivity, FOMO',
    visualDoctrine: [
      'High contrast (dark backgrounds, neon accents)',
      '3D depth effects and layered compositions',
      'Dynamic typography',
      'Sharp or very large radius',
      'Glow effects (box-shadow with color)',
      'Fast, energetic animations (100-200ms, spring easing)',
    ],
  },
}

export function getActiveBrand(): BrandConfig {
  const brandId = process.env.NEXT_PUBLIC_BRAND_ID || 'red-sea-resort'
  
  if (!BRAND_REGISTRY[brandId]) {
    throw new Error(`Brand "${brandId}" not registered`)
  }
  
  return BRAND_REGISTRY[brandId]
}
```

**Step 3 — Component Branding (Automatic):**
```tsx
// Components automatically pick up brand tokens — no brand-specific code needed
export function BookingCard({ booking }: BookingCardProps) {
  return (
    <article className="rounded-[var(--radius-card)] bg-surface-primary p-spacing-xl shadow-[var(--shadow-card)]">
      {/* Font, colors, spacing, shadows — all from active brand tokens */}
      <h2 className="font-[var(--font-family-display)] text-heading-md text-[var(--color-primary)]">
        {booking.title}
      </h2>
      
      {/* Animation timing from brand */}
      <button 
        className="btn-primary transition-[background-color] duration-[var(--duration-animation)] ease-out"
      >
        Book Now
      </button>
    </article>
  )
}
```

### 3. Style Transfer Validation

**Brand Isolation Test:**
```typescript
// tests/brand/isolation.test.ts
import { describe, it, expect } from 'vitest'
import { readFileSync } from 'fs'

describe('Brand Isolation', () => {
  it('Brand A tokens do not reference Brand B', () => {
    const brandA = readFileSync('.ai/context/brands/brand-a/tokens.css', 'utf-8')
    const brandB = readFileSync('.ai/context/brands/brand-b/tokens.css', 'utf-8')
    
    // Extract all token values from Brand B
    const brandBValues = extractTokenValues(brandB)
    
    // Verify none appear in Brand A
    for (const [key, value] of brandBValues) {
      expect(brandA).not.toContain(value)
    }
  })

  it('Each brand has distinct primary color', () => {
    const brands = ['brand-a', 'brand-b']
    const primaryColors = brands.map(brand => {
      const tokens = readFileSync(`.ai/context/brands/${brand}/tokens.css`, 'utf-8')
      return extractTokenValue(tokens, '--color-primary')
    })

    // All colors must be distinct
    expect(new Set(primaryColors).size).toBe(primaryColors.length)
  })

  it('Brand-specific fonts are distinct', () => {
    const brands = ['brand-a', 'brand-b']
    const displayFonts = brands.map(brand => {
      const tokens = readFileSync(`.ai/context/brands/${brand}/tokens.css`, 'utf-8')
      return extractTokenValue(tokens, '--font-family-display')
    })

    // Fonts must differ (unless intentionally shared)
    expect(new Set(displayFonts).size).toBeGreaterThan(1)
  })
})
```

### 4. Brand Grammar Transfer

**Copy Voice Adaptation:**
```typescript
// apps/web/src/lib/i18n/brand-copy.ts
const brandCopy: Record<string, Record<string, string>> = {
  'red-sea-resort': {
    'booking.cta': 'Reserve Your Experience',
    'booking.confirm': 'Your Journey Awaits',
    'booking.success': 'You\'re All Set — We Look Forward to Welcoming You',
    'booking.error': 'Something Went Wrong. Our Concierge Is Here to Assist.',
    'empty.bookings': 'No Reservations Yet — Your Perfect Stay Awaits',
  },
  'neon-lounge': {
    'booking.cta': 'Claim Your Spot',
    'booking.confirm': "You're In — Let's Go!",
    'booking.success': "You're All Set! See You Tonight",
    'booking.error': "Oops! Let's Try That Again",
    'empty.bookings': "No Events Yet — Check What's Coming Up",
  },
}

export function getBrandCopy(brandId: string, key: string): string {
  return brandCopy[brandId]?.[key] || key
}
```

### 5. Visual Regression per Brand

**Multi-Brand Visual Testing:**
```typescript
// tests/visual/brand-parity.spec.ts
import { test, expect } from '@playwright/test'

const BRANDS = ['red-sea-resort', 'neon-lounge']

test.describe('Brand Visual Parity', () => {
  for (const brand of BRANDS) {
    test.describe(`Brand: ${brand}`, () => {
      test('BookingCard matches brand baseline', async ({ page }) => {
        await page.addInitScript((brand) => {
          document.documentElement.setAttribute('data-brand', brand)
        }, brand)
        
        await page.goto('/storybook/iframe.html?id=booking-card--default')
        await expect(page).toHaveScreenshot(`booking-card-${brand}.png`, {
          threshold: 0.1, // 10% pixel difference tolerance
        })
      })

      test('RTL layout preserves brand aesthetics', async ({ page }) => {
        await page.addInitScript((brand) => {
          document.documentElement.setAttribute('data-brand', brand)
          document.documentElement.setAttribute('dir', 'rtl')
          document.documentElement.setAttribute('lang', 'ar')
        }, brand)
        
        await page.goto('/storybook/iframe.html?id=booking-card--default')
        await expect(page).toHaveScreenshot(`booking-card-${brand}-rtl.png`)
      })
    })
  }
})
```

### 6. White-Label Onboarding

**New Brand Setup:**
```bash
# 1. Create brand directory
mkdir -p .ai/context/brands/[new-brand]/{assets}

# 2. Run brand initialization
/brand --name [new-brand] --colors [hex,hex] --fonts [font] --tone [tone]

# 3. Generate brand tokens
# → .ai/context/brands/[new-brand]/tokens.css
# → .ai/context/brands/[new-brand]/palette.json
# → .ai/context/brands/[new-brand]/brand_grammar.md

# 4. Register brand in code
# → Add to BRAND_REGISTRY in apps/web/src/lib/brand-config.ts

# 5. Deploy with brand
NEXT_PUBLIC_BRAND_ID=[new-brand] pnpm run build
```

## Common Mistakes
- Hardcoding brand-specific logic in components — use tokens instead
- Referencing one brand's tokens from another — isolation violation
- Not testing each brand visually — assumptions lead to drift
- Shared copy between brands — each brand needs distinct voice
- Not registering new brands in BRAND_REGISTRY — runtime errors

## Success Criteria
- [ ] Each brand has isolated token file (no cross-references)
- [ ] Components use tokens, not brand-specific values
- [ ] Brand registry includes all active brands
- [ ] Visual regression tests pass for each brand
- [ ] Brand copy distinct per brand (no shared strings)
- [ ] RTL layout tested for each brand
- [ ] New brand onboarding documented and repeatable
- [ ] No brand token bleeding (isolation tests pass)