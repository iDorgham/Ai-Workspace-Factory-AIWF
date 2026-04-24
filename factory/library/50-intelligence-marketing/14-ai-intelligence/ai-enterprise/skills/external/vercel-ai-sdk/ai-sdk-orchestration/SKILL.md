---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# 🤖 Vercel AI SDK Orchestration

## Purpose
Enforce standards for building intelligent, streaming AI interfaces using the Vercel AI SDK. This skill focuses on the "Streaming UI" pattern (RSC + AI), multi-model orchestration, and reliable Tool Use (function calling) logic.

---

## Technique 1 — Generative UI Streaming (UI = Data)
- **Rule**: Never just stream text; stream **React Components** directly from the server to the client using `streamUI`.
- **Protocol**: 
    1. Define a tool in the `tools` object.
    2. When the tool is called, return a React Component (e.g., a chart or weather widget) instead of raw JSON.
    3. Use `Suspense` and the `Skeleton` pattern to handle the interstitial state during generation.

---

## Technique 2 — Robust Tool Orchestration (Middleware)
- **Rule**: Implement "Guard" logic for every tool to prevent authorized data modification or hallucinated tool calls.
- **Protocol**: 
    1. Validate tool parameters using Zod schemas.
    2. Check user permissions before executing the tool's underlying logic.
    3. Feed the result back into the model context to maintain narrative continuity.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Streaming raw sensitive data** | Security exposure | Filter model outputs before they hit the stream; ensure sensitive DB keys never enter the context. |
| **Unbounded Tool Loops** | Token drain / Performance crash | Implement a `max_steps` cap (e.g., 5 steps) for recursive tool usage. |
| **Ignoring Provider Failovers** | 500 Errors on API outage | Implement the `provider-switching` pattern; if OpenAI fails, fallback to Anthropic or Gemini automatically. |

---

## Success Criteria (AI SDK QA)
- [ ] UI streams reflect the real-time thought-process of the model.
- [ ] 100% of tools are type-safe and validated via Zod.
- [ ] Multi-provider failover is verified.
- [ ] LLM costs are monitored per-request via `onFinish` metadata.