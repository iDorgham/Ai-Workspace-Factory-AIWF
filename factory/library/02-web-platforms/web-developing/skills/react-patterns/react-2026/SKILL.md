# ⚛️ React 2026 Mastery

## Purpose
Enforce professional standards for building React applications using the definitive 2026 stack (Server Components, Actions, and Selective Hydration). This skill focuses on maximizing performance and security while minimizing client-side bundle weight.

---

## Technique 1 — "Server-First" Architecture
- **Rule**: All data-fetching components must be Server Components by default.
- **Protocol**: 
    1. Fetch data directly in the component using `await`.
    2. Pass serializable data down to "Client Islands" only when interactivity is required.
    3. Use `Suspense` boundaries to handle loading states at the granular level.

---

## Technique 2 — Action-Driven Mutation
- **Server Actions**: Define mutations in `use server` files to simplify forms and reduce API boilerplate.
- **Optimistic Updates**: Wrap actions in `useOptimistic` to provide zero-latency feedback to users.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **"use client" at Root** | Massive bundle bloat | Push "use client" as far down the component tree as possible. |
| **Prop Drilling Server Data** | Serialization overhead | Use `Context` only for client-side state; let Server Components fetch their own data. |
| **Silent Mutations** | Poor UX | Always use `useTransition` or `useFormStatus` to show mutation progress. |

---

## Success Criteria (React 2026 QA)
- [ ] Bundle size is < 50kb for initial page load.
- [ ] No "waterfall" data fetches detected.
- [ ] 100% of mutations use Server Actions.
- [ ] All interactive elements are wrapped in `Suspense`.