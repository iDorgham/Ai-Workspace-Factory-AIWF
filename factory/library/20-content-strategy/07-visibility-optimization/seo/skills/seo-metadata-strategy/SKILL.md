# SEO Metadata Strategy

## Purpose
Ensure every public-facing page in every app is correctly described, indexable, and visible to search engines. Covers Next.js App Router metadata API, JSON-LD structured data, sitemap/robots generation, and bilingual (EN/AR) SEO parity.

## Core Principle
SEO is a quality gate, not an afterthought. Every new page requires metadata before it can be merged. Arabic pages require Arabic metadata — English metadata on Arabic routes is a compliance violation.

---

## 1. Metadata Hierarchy (App Router)

```
app/layout.tsx          ← site-level defaults (title template, og:image fallback)
  app/[locale]/layout.tsx  ← locale-level (hreflang, locale-specific og)
    app/[locale]/products/layout.tsx  ← section-level (section title, description)
      app/[locale]/products/[slug]/page.tsx  ← page-level (specific title, canonical)
```

**Rule:** Page-level metadata always overrides layout-level. Never rely solely on layout metadata for leaf pages.

### Root Layout — Title Template
```typescript
// app/layout.tsx
export const metadata: Metadata = {
  title: {
    template: '%s | Brand Name',  // "Product X | Brand Name"
    default: 'Brand Name',         // fallback if page has no title
  },
  description: 'Default site description — overridden per page',
  metadataBase: new URL(process.env.NEXT_PUBLIC_BASE_URL!),
}
```

---

## 2. Required Fields Per Page

| Field | Required | Notes |
|-------|----------|-------|
| `title` | Yes | Unique per page; 50-60 chars |
| `description` | Yes | 120-160 chars; unique per page |
| `canonical` | Yes | Prevents duplicate content penalties |
| `openGraph.title` | Yes | Can match `title` |
| `openGraph.description` | Yes | Can match `description` |
| `openGraph.images` | Recommended | 1200×630px |
| `twitter.card` | Recommended | `summary_large_image` for image pages |
| `alternates.languages` | Yes (bilingual apps) | EN and AR variants |

---

## 3. Bilingual SEO Rules

All bilingual apps must implement:

### Hreflang (prevents duplicate content)
```typescript
alternates: {
  canonical: `/${locale}/path`,
  languages: {
    'en': `/en/path`,
    'ar': `/ar/path`,
    'x-default': `/en/path`,  // ← fallback for unmatched regions
  },
},
```

### Arabic Metadata
```typescript
// i18n/messages/ar.json
{
  "product": {
    "meta": {
      "title": "{name} — اكتشف المزيد",
      "description": "تعرف على {name} وجميع ما يقدمه من مزايا وخصائص"
    }
  }
}
```

**Rule:** Arabic `title` and `description` must be written in Arabic, not transliterated English.

---

## 4. JSON-LD Schema Types by Project Type

| Project Type | Primary Schema | Secondary Schemas |
|---|---|---|
| `web` (SaaS) | `SoftwareApplication` | `Organization`, `WebSite` |
| `web` (Blog) | `Article` | `Person`, `BreadcrumbList` |
| `web` (E-commerce) | `Product` | `Offer`, `BreadcrumbList`, `AggregateRating` |
| `hospitality` | `LodgingBusiness` | `FoodEstablishment`, `Event`, `Offer` |
| `gov-tech` | `GovernmentOrganization` | `GovernmentService`, `ContactPoint` |
| All | `WebSite` + `Organization` | Always include on home page |

### Organization Schema (site-wide, in root layout)
```typescript
const organizationSchema = {
  '@context': 'https://schema.org',
  '@type': 'Organization',
  name: process.env.NEXT_PUBLIC_SITE_NAME,
  url: process.env.NEXT_PUBLIC_BASE_URL,
  logo: `${process.env.NEXT_PUBLIC_BASE_URL}/logo.png`,
  sameAs: [
    'https://linkedin.com/company/...',
    'https://twitter.com/...',
  ],
  contactPoint: {
    '@type': 'ContactPoint',
    telephone: '+20-...',
    contactType: 'customer service',
    availableLanguage: ['English', 'Arabic'],
  },
}
```

### BreadcrumbList (on all nested pages)
```typescript
function buildBreadcrumbSchema(
  crumbs: { name: string; url: string }[]
) {
  return {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: crumbs.map((crumb, i) => ({
      '@type': 'ListItem',
      position: i + 1,
      name: crumb.name,
      item: crumb.url,
    })),
  }
}
```

---

## 5. Sitemap Patterns

### Static Routes
```typescript
const locales = ['en', 'ar']
const staticPaths = ['/', '/about', '/contact', '/pricing', '/blog']

const staticRoutes = staticPaths.flatMap(path =>
  locales.map(locale => ({
    url: `${BASE_URL}/${locale}${path}`,
    lastModified: new Date().toISOString(),
    changeFrequency: path === '/' ? 'daily' : 'monthly',
    priority: path === '/' ? 1.0 : 0.7,
  }))
)
```

### Dynamic Routes (with ISR)
```typescript
// For pages with ISR, set lastModified from the data source
const products = await db.product.findMany({
  select: { slug: true, updatedAt: true },
})

const productRoutes = products.flatMap(p =>
  locales.map(locale => ({
    url: `${BASE_URL}/${locale}/products/${p.slug}`,
    lastModified: p.updatedAt.toISOString(),
    changeFrequency: 'weekly' as const,
    priority: 0.6,
  }))
)
```

---

## 6. Robots.txt Patterns

### Multi-Environment (Critical)
```typescript
// NEVER index staging/preview environments
export default function robots(): MetadataRoute.Robots {
  if (process.env.VERCEL_ENV !== 'production') {
    return { rules: { userAgent: '*', disallow: '/' } }
  }
  return {
    rules: [
      { userAgent: '*', allow: '/', disallow: ['/api/', '/admin/'] },
      { userAgent: 'GPTBot', disallow: '/' },         // opt out of AI training
      { userAgent: 'ChatGPT-User', disallow: '/' },
      { userAgent: 'CCBot', disallow: '/' },
    ],
    sitemap: `${process.env.NEXT_PUBLIC_BASE_URL}/sitemap.xml`,
    host: process.env.NEXT_PUBLIC_BASE_URL,
  }
}
```

---

## 7. Core Web Vitals → SEO Impact

These metrics directly affect Google search ranking (Page Experience signals):

| Metric | Target | SEO Impact if Missed |
|--------|--------|---------------------|
| LCP (Largest Contentful Paint) | ≤ 2.5s | Ranking penalty in competitive niches |
| CLS (Cumulative Layout Shift) | ≤ 0.1 | Significant ranking penalty |
| INP (Interaction to Next Paint) | ≤ 200ms | Ranking signal since March 2024 |
| TTFB (Time to First Byte) | ≤ 800ms | Indirect ranking factor |

**Checklist for LCP:**
- Hero images use `priority` prop: `<Image src="..." priority />`
- Hero images served in WebP/AVIF
- Fonts use `next/font` with `display: swap`
- Critical CSS inlined (Next.js does this automatically with App Router)

**Checklist for CLS:**
- All images have explicit `width` and `height`
- Fonts loaded with size-adjust to prevent FOUT layout shift
- Dynamic content (ads, embeds) has reserved space

## 🌍 Regional Calibration (MENA Context)

- **Cultural Alignment:** Ensure all logic respects regional business etiquette and MENA market expectations.
- **RTL Compliance:** Logic must explicitly handle Right-to-Left (RTL) flow where relevant.

## 🛡️ Critical Failure Modes (Anti-Patterns)

- **Anti-Pattern:** Generic Output -> *Correction:* Apply sector-specific professional rules from RULE.md.
- **Anti-Pattern:** Global-Only Logic -> *Correction:* Verify against MENA regional calibration.

---

## 8. compliance SEO Checks

The following are automatically checked on every PR:

```
✓ Every page.tsx exports metadata or generateMetadata
✓ No page has duplicate <h1>
✓ No <img> without alt attribute
✓ robots.ts exists in app/
✓ sitemap.ts exists in app/
✓ Bilingual pages have alternates.languages with both en and ar
✓ No hardcoded titles (must use t() translation keys)
```

## Common Mistakes

- Using the same title and description across multiple pages → duplicate content penalty
- Forgetting `metadataBase` → relative OG image URLs break social sharing
- Indexing staging environments → pollutes search index with test data
- Missing Arabic metadata → Arabic pages rank poorly in Arabic search
- Setting `priority` or `changeFrequency` to the same value for all pages → search engines ignore both
- Omitting `x-default` hreflang → ambiguous fallback for international visitors

## Success Criteria

- [ ] All public pages have unique `title` and `description`
- [ ] All bilingual pages have `alternates.languages` with EN + AR
- [ ] `sitemap.ts` covers all public routes (static + dynamic)
- [ ] `robots.ts` disallows all non-production environments
- [ ] JSON-LD schema present on home page and key landing pages
- [ ] Lighthouse SEO ≥ 90 (gate passes)
- [ ] No `<img>` without `alt` (combined SEO + a11y gate)
- [ ] No duplicate `<h1>` per page