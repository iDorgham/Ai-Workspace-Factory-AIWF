# 🌊 React Streaming SSR

## Purpose
Enforce standards for streaming HTML from the server. This skill focuses on delivering initial critical UI instantly and "streaming" slower data-bound components as they become ready on the server, ensuring excellent TTFB (Time to First Byte) and FCP (First Contentful Paint).

---

## Technique 1 — Progressive Chunk Delivery
- **Rule**: Use `renderToReadableStream` (or equivalent framework features) to send HTML as a stream of chunks.
- **Protocol**: 
    1. Send the `head` and critical CSS/HTML in the first chunk.
    2. Stream component placeholders (skeletons) to the client immediately.
    3. As data-fetching finishes on the server, stream the final HTML + inline `<script>` tags to replace the placeholders.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)
| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Blocking on Server Fetch** | High TTFB / White screen | Wrap data-fetching components in `Suspense` to let the shell stream first. |
| **Client-Only Libs in Stream** | Runtime crashes | Ensure only server-compatible logic executes before the stream boundary. |
| **Deep Component Nesting** | Fragmented loading | Balance granularity; too many streams can lead to "Layout Thrashing" as content pops in. |

---

## Success Criteria (Streaming QA)
- [ ] TTFB (Time to First Byte) is < 200ms regardless of data complexity.
- [ ] Initial shell is visible before any data-fetching completes.
- [ ] Content "pops into place" without significant layout shift (utilizing reserved skeleton heights).
- [ ] All SEO bots see the full content in the final rendered stream.