# Asset Optimization

## Purpose
Optimize all media assets (images, videos, fonts, icons) for web delivery. Ensures fast loading, minimal bandwidth usage, and visual quality retention.

## When to Activate
- Adding images to UI components
- Setting up file upload/download features
- Performance diagnosis (slow LCP, large bundles)
- Brand initialization (font loading strategy)

## Step-by-Step Execution

### 1. Image Optimization Pipeline

**Format Selection:**
| Use Case | Format | Compression | Target Size |
|----------|--------|-------------|-------------|
| Photos | WebP (primary), AVIF (modern) | Lossy, 80% quality | <200KB per image |
| Icons/Logos | SVG (vector) | SVGO minified | <10KB per icon |
| Screenshots | PNG (lossless) | Compressed | <500KB |
| Animated content | MP4 (H.264) or WebM | CRF 23-28 | <5MB per video |
| Thumbnails | WebP, 200x200px | Lossy, 70% quality | <20KB |

**Next.js Image Component (Mandatory):**
```tsx
import Image from 'next/image'

// ✅ CORRECT — automatic optimization
<Image
  src="/images/hero.webp"
  alt="Luxury hotel lobby"
  width={1920}
  height={1080}
  priority  // Only for above-the-fold images
  quality={80}
  sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
/>

// ❌ FORBIDDEN — no optimization
<img src="/images/hero.jpg" alt="Luxury hotel lobby" />
```

**Responsive Image Generation:**
```typescript
// next.config.mjs — automatic responsive images
const nextConfig = {
  images: {
    formats: ['image/avif', 'image/webp'],
    deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048],
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],
    minimumCacheTTL: 60 * 60 * 24 * 30, // 30 days
    remotePatterns: [
      { protocol: 'https', hostname: '**.your-domain.com' }, // replace with your actual domain(s)
    ],
  },
}
```

### 2. Font Loading Strategy

**Critical Font Optimization:**
```css
/* ✅ CORRECT — variable font with subset */
@font-face {
  font-family: 'Inter Variable';
  src: url('/fonts/inter-variable-latin.woff2') format('woff2');
  font-weight: 100 900;
  font-style: normal;
  font-display: swap; /* Prevents FOIT */
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC; /* Latin only */
}

/* Arabic font — loaded only when needed */
:root:lang(ar) {
  --font-family-active: var(--font-family-arabic);
}

@font-face {
  font-family: 'Cairo Variable';
  src: url('/fonts/cairo-variable-arabic.woff2') format('woff2');
  font-display: swap;
  unicode-range: U+0600-06FF, U+0750-077F, U+08A0-08FF, U+FB50-FDFF, U+FE70-FEFF; /* Arabic only */
}
```

**Font Loading Priority:**
1. Display font (above-the-fold, preload)
2. Body font (preconnect)
3. Arabic font (load on-demand when `lang="ar"`)
4. Monospace font (lazy, for code blocks only)

### 3. Bundle Analysis

**Analyze Bundle Composition:**
```bash
# Analyze production bundle
pnpm turbo run build -- --analyze

# Check what's using space
npx bundle-phobia-cli packages/ui/dist/index.js
```

**Budget Allocation:**
| Category | Budget | Target |
|----------|--------|-----
## 🌍 Regional Calibration (MENA Context)

- **Cultural Alignment:** Ensure all logic respects regional business etiquette and MENA market expectations.
- **RTL Compliance:** Logic must explicitly handle Right-to-Left (RTL) flow where relevant.

## 🛡️ Critical Failure Modes (Anti-Patterns)

- **Anti-Pattern:** Generic Output -> *Correction:* Apply sector-specific professional rules from RULE.md.
- **Anti-Pattern:** Global-Only Logic -> *Correction:* Verify against MENA regional calibration.

---
|
| React + ReactDOM | 45KB | ≤42KB |
| Next.js framework | 25KB | ≤30KB |
| Design system (ui) | 20KB | ≤25KB |
| App code (web) | 20KB | ≤25KB |
| Third-party libs | 10KB | ≤15KB |
| **Total (gzipped)** | **120KB** | **≤137KB** |

**Tree Shaking Enforcement:**
```typescript
// packages/ui/src/components/index.ts — barrel exports
// ✅ CORRECT — named exports only
export { Button } from './Button'
export { Input } from './Input'
export { Card } from './Card'

// ❌ FORBIDDEN — re-exports everything
export * from './Button'  // Prevents tree shaking
```

### 4. Caching Strategy

**HTTP Cache Headers:**
```typescript
// apps/api/src/middleware/cache.ts
app.use('/api/*', async (c, next) => {
  c.header('Cache-Control', 'public, max-age=60, s-maxage=300') // 1min browser, 5min CDN
  await next()
})

app.use('/static/*', async (c, next) => {
  c.header('Cache-Control', 'public, max-age=31536000, immutable') // 1 year, immutable
  c.header('CDN-Cache-Control', 'public, max-age=31536000, immutable')
  await next()
})
```

**CDN Configuration:**
- Static assets (images, fonts, CSS): 1 year cache, immutable
- API responses: 1-5 minutes (depends on data freshness)
- HTML pages: No cache (SSR), or 1 minute (ISR)
- User-specific data: No cache, private only

### 5. Lazy Loading Strategy

**Component-Level Lazy Loading:**
```tsx
// Lazy load below-the-fold components
const BookingMap = lazy(() => import('./BookingMap'))
const ReviewsSection = lazy(() => import('./ReviewsSection'))

function BookingPage() {
  return (
    <main>
      {/* Above-the-fold — eager */}
      <BookingHero />
      <BookingForm />
      
      {/* Below-the-fold — lazy */}
      <Suspense fallback={<Skeleton height={400} />}>
        <BookingMap />
      </Suspense>
      <Suspense fallback={<Skeleton height={200} />}>
        <ReviewsSection />
      </Suspense>
    </main>
  )
}
```

**Route-Level Code Splitting:**
```tsx
// Next.js App Router — automatic route splitting
// apps/web/src/app/
// ├── page.tsx              → / (home route)
// ├── bookings/
// │   └── page.tsx          → /bookings (separate chunk)
// └── profile/
//     └── page.tsx          → /profile (separate chunk)
```

## Common Mistakes
- Using `<img>` instead of `<Image>` — no optimization
- Loading full icon library instead of tree-shaken icons
- Not setting width/height on images — causes CLS (layout shift)
- Using PNG for photos — 5-10x larger than WebP
- Not subsetting fonts — loading unnecessary glyphs
- No cache headers — every request hits server

## Success Criteria
- [ ] All images use Next.js `<Image>` component or equivalent
- [ ] Images in WebP/AVIF format (fallbacks provided)
- [ ] Fonts subset to required unicode ranges
- [ ] Font display: swap (no FOIT)
- [ ] Bundle <120KB gzipped (first load)
- [ ] Lighthouse Performance ≥95
- [ ] LCP <2.5s, CLS <0.1, TBT <200ms
- [ ] Static assets cached for 1 year (immutable)
- [ ] Below-fold components lazy loaded