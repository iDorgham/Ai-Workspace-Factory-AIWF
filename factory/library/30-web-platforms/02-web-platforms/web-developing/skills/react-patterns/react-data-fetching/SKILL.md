# 📊 React Data Fetching (Modern)

## Purpose
Enforce standards for high-performance data fetching. This skill focuses on moving away from `useEffect` fetches toward declarative, state-aware handlers like TanStack Query, SWR, and Suspense for Data Fetching to ensure caching, deduplication, and optimistic consistency.

---

## Technique 1 — Declarative Query Management
- **Rule**: Use a query manager (TanStack Query/SWR) for all asynchronous data.
- **Protocol**: 
    1. Define unique cache keys for every distinct data request.
    2. Leverage "Stale-While-Revalidate" patterns to deliver immediate cached results while updating in the background.
    3. Use `Suspense` for data fetching to decouple data loading from component rendering logic.

---

## Technique 2 — Optimistic Mutations
- **Optimistic UI**: Update the local cache immediately upon user action.
- **Rollback Logic**: Maintain the previous state and revert automatically if the server request fails.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)
| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **useEffect Fetching** | Race conditions / double-fetches | Replace with a dedicated fetcher (Query/SWR) that handles lifecycle and deduplication. |
| **Missing Loading States** | "Broken" UI feel | Use `Suspense` boundaries or granular `isLoading` flags for every fetch. |
| **Manual Cache Busting** | Inconsistent Data | Use declarative cache invalidation (Invalidate Tags/Keys) instead of manual state resets. |

---

## Success Criteria (Data QA)
- [ ] No "Race Conditions" detected in concurrent navigation.
- [ ] Data is cached and deduplicated across components.
- [ ] 0% of fetch logic exists inside primitive `useEffect` hooks.
- [ ] Optimistic updates are applied to all primary user interactions (e.g., Favoriting, Adding to Cart).