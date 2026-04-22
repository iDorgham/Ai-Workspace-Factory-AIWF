# API surface: [Feature Name]

> **Feature ID:** `[feature-id]`
> **Must match:** Zod contracts in `packages/shared/src/contracts/` — no drift.

---

## 1. Base path

- API base: `[e.g. /api/v1/bookings]`
- Auth: [public | JWT | session | …]

---

## 2. Endpoints

| Method | Path | Contract (Zod) | Description |
|--------|------|------------------|-------------|
| POST | | `CreateXxxSchema` | |
| GET | | `XxxQuerySchema` | |

---

## 3. Errors

| HTTP | Code | When |
|------|------|------|
| 400 | | Validation |
| 401 | | |
| 404 | | |

---

## 4. Webhooks / events (if any)

…

---

## 5. Rate limits / idempotency

…
