# 🧠 React AI UI Patterns

## Purpose
Enforce standards for building AI-powered interfaces (Chatbots, Copilots, Generative UI). This skill focuses on handling streaming text, managing thought/logic state visibility, and ensuring a robust user experience during non-deterministic AI interactions.

---

## Technique 1 — Streaming Text Management
- **Rule**: Use specific hooks (e.g., `useChat` from AI SDKs) to handle Vercel AI SDK or direct OpenAI stream tokens.
- **Protocol**: 
    1. Render partial text as it arrives.
    2. Auto-scroll as content grows, but allow the user to interrupt the scroll.
    3. Use a clear "Loading/Thinking" state that doesn't block the UI thread.

---

## Technique 2 — Generative UI Slots (RSC Injection)
- **Component Injection**: Allow the LLM to return specific React components (tools) instead of just text (using AI SDK `render` or equivalent).
- **Safety**: Sanitization of AI-generated component props and strict boundary shielding.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)
| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **All-at-Once Response** | High perceived latency | Always stream tokens to provide immediate visual feedback. |
| **Silent Collisions** | UI jitter | Use stable heights for AI containers to prevent layout shift as the response streams. |
| **Infinite Loops** | Token drain / Crash | Implement strict cycle detection for AI tool-calling loops. |

---

## Success Criteria (AI UI QA)
- [ ] First token is visible within < 500ms of request.
- [ ] UI remains responsive (60fps) during heavy stream rendering.
- [ ] Complex components (charts, cards) are injected into the stream correctly via RSC.
- [ ] User can cancel or re-generate responses at any time.
- [ ] Arabic RTL is correctly handled during partial word streaming.