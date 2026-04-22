# Prompt 02 — Backend implementation for [Feature Name]

**Prerequisites:** Contracts locked for this domain; `api.md` current.

---

Implement API routes and services under `apps/api/` per `structure.md` and `api.md`.

**Requirements:**

- Parse all inputs with the Zod schemas from `@sovereign/contracts/*` (or package path in use).
- Auth middleware on protected routes; no secrets in code.
- Structured errors; no stack traces to clients in production.

**Output:** list of files changed + how to run quick-check locally.
