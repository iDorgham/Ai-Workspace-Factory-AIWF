# 💎 High-Density Web Quality

## Purpose
Enforce standards for professional-grade web output. This skill focuses on the "Final 10%"—the polish that distinguishes an MVP from an industry-leading product. It covers performance budgets, visual regression testing, and semantic asset management.

---

## Technique 1 — Performance Budgeting (Brotli/Weight)
- **Rule**: Every production build must fit within a predefined weight budget (e.g., < 200kb initial JS).
- **Protocol**: 
    1. Implement Brotli/Gzip compression for all text assets.
    2. Enforce code-splitting for routes and large components.
    3. Use tree-shaking to eliminate unused library code.

---

## Technique 2 — Visual Regression Guard (Snapshot)
- **Rule**: Every UI change must be verified against the design "Master" via visual snapshots.
- **Protocol**: 
    1. Run automated Playwright/Cypress snapshot tests.
    2. Identify variance in pixels > 0.1%.
    3. Require sign-off from @DesignDirector if variances are intentional.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)
| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Asset Bloat** | High bounce rates | Use Next/Image for automatic format conversion (WebP/AVIF) and responsive sizing. |
| **Missing Favicons/Meta** | Unprofessional presence | Ensure a complete set of brand assets (favicons, OG images, manifest.json) is generated for every site. |
| **Ignoring Cross-Browser Glitch** | Broken layout (Safari/Firefox) | Explicitly test `backdrop-filter` and `grid` implementations on non-Blink engines. |

---

## Success Criteria (Web Quality QA)
- [ ] Lighthouse Performance score is consistently 90+ [💎 OMEGA].
- [ ] 0 Accessible violations in automated `axe-core` scans.
- [ ] Favicon and Social Meta tags are 100% verified.
- [ ] Site remains interactive under "Slow 3G" throttling.
- [ ] Arabic fonts are subsetted to include only required characters to reduce weight.