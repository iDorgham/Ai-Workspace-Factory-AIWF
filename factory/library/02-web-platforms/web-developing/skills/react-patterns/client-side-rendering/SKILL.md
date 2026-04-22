# 💻 React Client-Side Rendering (CSR)

## Purpose
Enforce standards for traditional Single Page Applications (SPAs). While modern React favors SSR/RSC, CSR remains the standard for internal dashboards, authenticated-only apps, and tools where initial load time is less critical than highly fluid, stateful interactivity.

---

## Technique 1 — Robust Bootstrapping
- **Rule**: Minimize the "White Screen" during JS download.
- **Protocol**: 
    1. Provide meaningful "Loading Shell" HTML in the static `index.html`.
    2. Use code-splitting to ensure the initial bundle is as small as possible.
    3. Use `React.lazy` and `Suspense` for route-level splitting.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)
| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Giant Monolith Bundle** | Extremely slow FCP | Use dynamic imports (`import()`) for any modules > 20kb. |
| **Empty index.html** | SEO invisibility / poor UX | Add a minimal CSS/SVG loader and meta-tags to the root HTML. |
| **Waterfall API calls** | Sluggish startup | Initiate critical API calls in a script tag or concurrently with JS boot rather than waiting for component mount. |

---

## Success Criteria (CSR QA)
- [ ] Initial JS bundle is < 150kb (gzipped).
- [ ] Routes are split and loaded on-demand.
- [ ] App has 0 "Hydration" overhead (since it renders purely on client).
- [ ] Meaningful loader is visible within < 300ms.