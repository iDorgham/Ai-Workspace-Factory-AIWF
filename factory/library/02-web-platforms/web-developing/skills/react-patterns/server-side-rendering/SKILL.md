# 🌐 React Server-Side Rendering (SSR)

## Purpose
Enforce standards for on-demand server rendering. This skill focuses on the traditional SSR model (pre-RSC) where the server generates the full HTML for each request to ensure immediate visibility and total SEO indexability for dynamic content.

---

## Technique 1 — Isomorphic Fetching
- **Rule**: Data fetching logic must be able to run on both the server and the client.
- **Protocol**: 
    1. Use `getServerSideProps` (Next.js Pages) or equivalent middleware to fetch data.
    2. Pass the fetched data as `dehydratedState` to ensure the client doesn't re-fetch data already available in the HTML.
    3. Ensure no browser-specific globals (like `localStorage` or `window`) are accessed before the component mounts.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)
| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Heavy Server Logic** | High TTFB | Move non-essential computations to the client or a background job. |
| **Silent Failures** | Blank pages | Implement robust server-side error boundaries to prevent a single component crash from breaking the entire render. |
| **Hydration Mismatches** | Inconsistent UI / Re-rendering | Avoid using non-deterministic data (e.g., `Math.random()`, `Date.now()`) during the initial render. |

---

## Success Criteria (SSR QA)
- [ ] SEO bots receive the 100% complete HTML on the first request.
- [ ] TTFB is consistent and under 300ms for standard pages.
- [ ] No Client-Server data mismatches observed during hydration.
- [ ] Critical content is visible without a "loading spinner" on first load.