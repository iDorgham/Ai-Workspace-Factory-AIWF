# 🏗️ React Static Rendering (SSG)

## Purpose
Enforce standards for pre-rendered content. This skill focuses on the Static Site Generation (SSG) model, where HTML is generated at build-time and served via CDN for maximum possible performance and edge-caching capacity.

---

## Technique 1 — Build-Time Data Ingestion
- **Rule**: Prefetch all data required for the page during the build process.
- **Protocol**: 
    1. Use `getStaticProps` (Next.js Pages) or direct RSC file-system imports to load data.
    2. Generate optimized assets (images, fonts) alongside the HTML.
    3. Ensure no runtime dependencies are required for the initial page render.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)
| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Massive Build Times** | Deployment bottlenecks | Use `getStaticPaths` with `fallback: blocking` to generate less-frequent pages on-demand. |
| **Stale Content** | Outdated info | Implement **Incremental Static Regeneration (ISR)** to refresh the cache in the background. |
| **Client-Only Hydration** | Interaction delay | Ensure the pre-rendered HTML is "interactive-ready" and avoid heavy layout-shifting JS during hydration. |

---

## Success Criteria (Static QA)
- [ ] 100% of pages are served from the CDN edge.
- [ ] LCP (Largest Contentful Paint) is < 1s for globally distributed users.
- [ ] Build process generates complete HTML, CSS, and SEO metadata for every route.
- [ ] Zero server-side compute required at request time.