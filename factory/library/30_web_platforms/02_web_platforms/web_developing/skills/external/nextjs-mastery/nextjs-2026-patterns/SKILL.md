---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# 🌐 Next.js 2026 Master Patterns

## Purpose
Enforce the definitive "App Router" physics for Next.js 15+. This skill focuses on the orchestration of React Server Components (RSC), Client Components, and Server Actions to achieve a zero-bundle-size baseline for dynamic content.

---

## Technique 1 — RSC-First Data Fetching
- **Rule**: Fetch data directly in Server Components (Async Components) to eliminate client-side useEffects and waterfalls.
- **Protocol**: 
    1. Define the component as `async`.
    2. Execute `fetch` or DB calls directly in the body.
    3. Use `Suspense` with localized skeletons for granular loading states.
    4. Pass data as props to leaf-level Client Components only when interactivity is required.

---

## Technique 2 — Progressive Enhancement (Server Actions)
- **Rule**: Use Server Actions for all data mutations to ensure a seamless "Forms-to-Database" bridge.
- **Protocol**: 
    1. Define functions with the `"use server"` directive.
    2. Use `useActionState` (or `useFormState`) for handling loading and error states on the client.
    3. Trigger `revalidatePath` or `revalidateTag` immediately after successful mutation to sync the UI.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **"use client" at the Root** | Massive bundle size | Keep interactivity at the "leaves" of the component tree; default to RSC for all layout and data logic. |
| **Prop-Drilling Large Objects** | Slow serialization | Only pass the primitive IDs required by the client component; refetch detail on the server if needed. |
| **Unprotected Server Actions** | Security vulnerability | ALWAYS perform authentication and authorization checks inside the Server Action body before executing logic. |

---

## Success Criteria (Next.js QA)
- [ ] 0% unnecessary client-side JS for static/data-only views.
- [ ] 100% of mutations use Server Actions with comprehensive error handling.
- [ ] LCP (Largest Contentful Paint) is < 1.2s for global cached routes.
- [ ] SEO-ready: Metadata and OpenGraph tags are dynamically generated via `generateMetadata`.
- [ ] RTL support enabled for all generated layouts.