---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# 👁️ Sentry Real-Time Observability

## Purpose
Enforce standards for "Self-Healing" systems through deep observability. This skill focuses on the logic of error grouping, performance tracing (Transaction monitoring), and user feedback loops to ensure that every failure in the production environment is captured with full context for immediate resolution.

---

## Technique 1 — Full-Stack Trace Context (Breadcrumbs)
- **Rule**: Every error must be captured with the "Story" of how it happened (User clicks, API requests, state changes).
- **Protocol**: 
    1. Instrument the frontend and backend with Sentry SDKs.
    2. Explicitly log custom "Breadcrumbs" for non-breaking but critical events.
    3. Attach User IDs (anonymized if required) and Environment tags (prod/staging).
    4. Automatically capture the state of the Global Store (Zustand/Redux) at the time of the crash.

---

## Technique 2 — Distributed Tracing (Performance)
- **Rule**: Link frontend transactions to backend database queries to identify the exact source of latency.
- **Protocol**: 
    1. Enable `tracesSampleRate` for a subset of requests.
    2. Pass the `sentry-trace` header between microservices.
    3. Analyze the "Waterfall" in the Sentry dashboard to isolate slow database calls or external API bottlenecks.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Silent Catch Blocks** | "Ghost" errors | Never swallow errors; if you must catch an error, at least log it to Sentry via `captureException(e)`. |
| **Massive Error Noise** | Alert fatigue | Implement "Issue Grouping" and "Fingerprinting" to ensure identical errors aren't treated as new events. |
| **PII in Logs** | Compliance breach | Use Sentry's `beforeSend` hook to scrub passwords, credit card numbers, and emails from all outgoing logs. |

---

## Success Criteria (Observability QA)
- [ ] 100% of unhandled exceptions are captured.
- [ ] Every error report contains a "Replay" (if enabled) or a full Breadcrumb trail.
- [ ] Average time-to-issue-identifcation is < 15 minutes.
- [ ] Performance tracing shows LCP and FID (First Input Delay) metrics for real users.