---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# Core Web Vitals + Bundle Size Optimization

## Purpose
Every page must score ≥95 on Lighthouse. Bundle size target: <120KB gzipped for first load JS. Performance is a feature — especially critical for Hurghada hospitality sites serving tourists on mobile data connections.

## Core Web Vitals Targets

```
LCP (Largest Contentful Paint)    < 2.5s    (good) | < 4s (acceptable)
FID (First Input Delay)           < 100ms   (good) | < 300ms (acceptable)
CLS (Cumulative Layout Shift)     < 0.1     (good) | < 0.25 (acceptable)
INP (Interaction to Next Paint)   < 200ms   (good) | < 500ms (acceptable)
TTFB (Time to First Byte)         < 800ms   (good)
FCP (First Contentful Paint)      < 1.8s    (good)
```

## Image Optimization

```tsx
// ✅ Always use Next.js Image component
import Image from 'next/image'

// Hero images — priority, explicit size
<Image
  src="/images/red-sea-diving.jpg"
  alt={t('hero.imageAlt')}
  width={1440}
  height={810}
  priority           // preload — eliminates LCP penalty
  quality={85}
  sizes="100vw"
  className="object-cover"
/>

// Card thumbnails — lazy, responsive
<Image
  src={venue.thumbnail}
  alt={venue.name}
  fill
  sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
  className="object-cover"
/>

// ❌ Never use <img> tag — no optimization
<img src="/hero.jpg" /> // ❌
```

### Image Format Priority
```
AVIF  → smallest size, modern browsers (2022+)
WebP  → excellent compression, wide support
JPEG  → fallback for photography
PNG   → only for images requiring transparency
SVG   → icons, logos (inline when possible)
```

## Font Optimization

```typescript
// apps/web/src/app/layout.tsx
import { Inter, Cairo } from 'next/font/google'

// ✅ next/font — zero layout shift, self-hosted, preloaded
const inter = Inter({
  subsets: ['latin'],
  variable: '--font-sans',
  display: 'swap',
  preload: true,
})

const cairo = Cairo({
  subsets: ['arabic', 'latin'],
  variable: '--font-arabic',
  display: 'swap',
  weight: ['400', '600', '700'],
  preload: false, // only load when needed (Arabic locale)
})

// ❌ Never use Google Fonts @import in CSS — blocks render
// @import url('https://fonts.googleapis.com/...') ❌
```

## Bundle Size Management

```bash
# Analyze bundle — run after build
ANALYZE=true pnpm build

# Bundle size targets
First Load JS:  < 120KB gzipped
Per-route JS:   < 50KB gzipped
CSS:            < 30KB gzipped
```

### Code Splitting Patterns
```typescript
// ✅ Dynamic import for large components
import dynamic from 'next/dynamic'

// Heavy map component — only load when needed
const VenueMap = dynamic(() => import('@/components/VenueMap'), {
  ssr: false,
  loading: () => <div className="h-64 bg-[var(--color-surface-secondary)] animate-pulse rounded-[var(--radius-xl)]" />,
})

// Heavy chart library
const AnalyticsChart = dynamic(
  () => import('recharts').then(m => ({ default: m.LineChart })),
  { ssr: false }
)
```

### Tree-Shaking
```typescript
// ✅ Named imports — tree-shakeable
import { format, parseISO } from 'date-fns'
import { ChevronRight } from 'lucide-react'

// ❌ Namespace imports — prevents tree-shaking
import * as dateFns from 'date-fns'  // includes entire library
import * as Icons from 'lucide-react' // includes ALL icons
```

## Preventing CLS (Layout Shift)

```tsx
// ✅ Reserve space for async content
function BookingList() {
  const { data, isLoading } = useBookings()

  if (isLoading) {
    return (
      // Skeleton matches exact dimensions of real content
      <div className="space-y-[var(--space-4)]">
        {Array.from({ length: 5 }).map((_, i) => (
          <div key={i} className="h-24 bg-[var(--color-surface-secondary)] animate-pulse rounded-[var(--radius-xl)]" />
        ))}
      </div>
    )
  }

  return <BookingTable bookings={data} />
}

// ✅ Explicit dimensions for images (prevents CLS)
<Image width={400} height={300} ... />  // explicit = no CLS

// ❌ Unknown dimensions = CLS
<img src={url} />  // browser doesn't know size until loaded
```

## Server-Side Rendering Strategy

```typescript
// ✅ RSC (React Server Components) — zero client JS
// Use for: static content, data display, navigation
async function BookingsPage() {
  const bookings = await getBookings() // runs on server
  return <BookingTable bookings={bookings} /> // no client JS needed
}

// ✅ Server Component + Client Island pattern
async function DashboardPage() {
  const stats = await getDashboardStats()
  return (
    <div>
      <Stats data={stats} />          {/* Server Component */}
      <BookingCalendar />             {/* 'use client' — interactive */}
      <RealtimeBookings />            {/* 'use client' — websocket */}
    </div>
  )
}
```

## Lighthouse CI

```yaml
# .github/workflows/lighthouse.yml
- name: Lighthouse CI
  uses: treosh/lighthouse-ci-action@v11
  with:
    urls: |
      https://preview-${{ github.sha }}.example.com/
      https://preview-${{ github.sha }}.example.com/bookings
      https://preview-${{ github.sha }}.example.com/ar/
    budgetPath: ./lighthouse-budget.json
    uploadArtifacts: true

# lighthouse-budget.json
{
  "ci": {
    "assert": {
      "assertions": {
        "categories:performance":    ["error", { "minScore": 0.95 }],
        "categories:accessibility":  ["error", { "minScore": 0.95 }],
        "categories:best-practices": ["warn",  { "minScore": 0.90 }],
        "categories:seo":            ["warn",  { "minScore": 0.90 }]
      }
    }
  }
}
```

## Common Mistakes
- `<img>` instead of `<Image>` — no optimization, LCP penalty
- Google Fonts CSS `@import` — blocks render, CLS risk
- No loading skeletons — CLS when async data loads
- Full library imports (`import * as`) — massive bundle bloat
- Not using `priority` on LCP image — guaranteed LCP failure

## Success Criteria
- [ ] All images use `next/image` with explicit width/height or `fill`
- [ ] Hero/LCP image has `priority` prop
- [ ] Fonts loaded via `next/font/google`
- [ ] Bundle size < 120KB gzipped first load
- [ ] CLS < 0.1 (skeletons for all async content)
- [ ] Lighthouse ≥95 performance score
- [ ] Lighthouse CI runs on every PR