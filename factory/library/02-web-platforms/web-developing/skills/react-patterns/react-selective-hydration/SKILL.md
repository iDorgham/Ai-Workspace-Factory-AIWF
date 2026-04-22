# 💧 React Selective Hydration

## Purpose
Enforce standards for prioritizing the hydration of interactive components. This skill focuses on using `Suspense` to let React "hydrate" high-priority sections (like a clicked button) before lower-priority content, improving interaction readiness.

---

## Technique 1 — Suspense-Driven Priorities
- **Rule**: Wrap independent interactive areas in `Suspense` boundaries.
- **Protocol**: 
    1. Deliver HTML for the whole page immediately.
    2. React will attempt to hydrate the components inside Suspense.
    3. If a user interacts with a Suspense boundary that hasn't hydrated yet, React will interrupt other work to hydrate that area first.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **All-or-Nothing Hydration** | Main thread lockup | Split the app into meaningful `Suspense` islands to allow "Out-of-Order" hydration. |
| **Blocking Browser Globals** | Hydration mismatch | Ensure shared code doesn't touch `window` or `document` during the initial server render. |
| **Deep Nesting without Suspense** | TBT (Total Blocking Time) spikes | Use granular boundaries at the component level to distribute hydration costs. |

---

## Success Criteria (Selective Hydration QA)
- [ ] TBT (Total Blocking Time) is minimized during initial load.
- [ ] User interactions (clicks) trigger immediate priority-hydration of the target area.
- [ ] HTML is interactive in parts before the full JS bundle is processed.