---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# 🚀 Next.js SEO Master Protocols

## Purpose
Enforce standards for technical SEO orchestration in Next.js 15+ applications. This skill focuses on the "Indexability-First" model—ensuring perfect Core Web Vitals, dynamic metadata generation, and multi-regional crawling optimization for MENA and Global markets.

---

## Technique 1 — Dynamic OpenGraph & Meta Orchestration
- **Rule**: Every route must have a unique, optimized meta-object generated on the server.
- **Protocol**: 
    1. Implement the `generateMetadata` async function for all dynamic routes.
    2. Extract title/desc from the database/content source.
    3. Generate a dynamic social sharing image (OG-Image) using `@vercel/og` or a pre-rendered template.
    4. Inject regional `alternates` (e.g., `en-US`, `ar-EG`) to prevent duplicate content penalties.

---

## Technique 2 — Performance-Driven Indexing (CWV)
- **Rule**: Maintain "Passed" status for all Core Web Vitals (LCP, INP, CLS) to maximize crawl priority.
- **Protocol**: 
    1. Prioritize SSR/ISR for all landing pages to ensure instant HTML availability.
    2. Subset fonts and optimize images (WebP/AVIF) via `next/image`.
    3. Monitor "Interaction to Next Paint" (INP) to ensure high responsiveness.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)
| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Client-side Meta Updates** | Ghost snippets in Google | Always use Next.js built-in `Metadata` API; never use manual `<head>` injections in Client Components. |
| **Missing Robots/Sitemap** | Indexing stall | Automate `sitemap.xml` and `robots.ts` generation based on the active route tree. |
| **Canonical URL Confusion** | Duplicate content debt | Ensure every page has a single, absolute `canonical` link to avoid splitting authority between `www` and root domains. |

---

## Success Criteria (Technical SEO QA)
- [ ] 100% Indexability score in Google Search Console simulations.
- [ ] 0% Cumulative Layout Shift (CLS) on page load.
- [ ] All social media previews (X, Facebook, LinkedIn) render perfectly with brand imagery.
- [ ] Google Lighthouse SEO score is 100/100.
- [ ] Hreflang tags are correctly implemented for AR/EN markets.