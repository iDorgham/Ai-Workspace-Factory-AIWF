# ⏳ React Progressive Hydration

## Purpose
Enforce standards for delaying the hydration of non-critical components. This skill focuses on delivering the full static HTML and only loading/executing the JS for interactive parts when they enter the viewport or are specifically requested by user interaction.

---

## Technique 1 — Viewport-Driven Loading
- **Rule**: Non-critical interactive elements (e.g., reviews section, footer interactions) must load their JS only when visible.
- **Protocol**: 
    1. Deliver static HTML for the component.
    2. Use `IntersectionObserver` to detect when the component is near the viewport.
    3. Dynamically `import()` the interactive JS and hydrate the component on-demand.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)
| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Hydrating Above-the-Fold last** | Poor Interaction to Next Paint (INP) | Prioritize critical path (Nav, CTA) JS; everything else is deferred. |
| **Flashing Content** | Poor Visual Stability | Ensure the static HTML perfectly matches the hydrated state to prevent layout shifts. |
| **Blocking the Thread** | Interaction delay | Hydrate in small idle chunks using `requestIdleCallback` where appropriate. |

---

## Success Criteria (Progressive QA)
- [ ] TTI (Time to Interactive) for critical elements is under 2s.
- [ ] Total JavaScript execution time on load is reduced by > 50%.
- [ ] Non-critical interactive JS is only fetched when needed.
- [ ] No visual "flashing" or layout shifts occur during on-demand hydration.