# ☁️ React Server Components (RSC)

## Purpose
Enforce standards for RSC implementation to eliminate client-side JavaScript for non-interactive elements. This skill focuses on the "Server-First" mindset, reducing bundle sizes and improving First Contentful Paint (FCP).

---

## Technique 1 — Zero-Bundle Rendering
- **Rule**: Keep components as Server Components unless they require state (`useState`), effects (`useEffect`), or browser APIs.
- **Protocol**: 
    1. Perform data fetching directly inside the component using `async/await`.
    2. Render complex logic on the server to avoid shipping heavy libraries (e.g., Markdown parsers, Date formatters) to the client.
    3. Pass only serializable data through the "Server-Client Boundary."

---

## Technique 2 — Boundary Orchestration
- **Server/Client Composition**: Always pass Client Components as `children` to Server Components rather than importing Server Components inside Client Components (which is impossible).
- **Data Streaming**: Wrap data-intensive RSCs in `Suspense` to enable progressive loading profiles.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Importing Server into Client** | Fatal Runtime Error | Pass the Server Component as a `prop` or `children` to the Client Component. |
| **Passing Non-Serializable Props** | Hydration Mismatch | Never pass functions, Classes, or complex Dates directly from Server to Client; serialize to JSON-safe primitives. |
| **Prop-Drilling through Boundaries** | Fragmentation | Let Server Components fetch their own data; avoid passing massive data objects from the root. |

---

## Success Criteria (RSC QA)
- [ ] Non-interactive components contribute 0kb to the JS bundle.
- [ ] Secure data (API keys, DB calls) stays purely on the server.
- [ ] No "Hydration Mismatch" errors in the console.
- [ ] User sees meaningful content before the JS finishes loading.