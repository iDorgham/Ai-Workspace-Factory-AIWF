# Repository structure: [Feature Name]

> **Feature ID:** `[feature-id]`
> **Purpose:** Map planned work to concrete paths under `apps/` and `packages/`.

---

## 1. Packages touched

| Package | Change type | Notes |
|---------|-------------|-------|
| `packages/shared` | contracts | New or updated `[domain].ts` |
| `packages/ui` | components | |
| `apps/web` | pages, components | |
| `apps/api` | routes, services | |

---

## 2. New files (planned)

```
apps/web/src/app/...
apps/api/src/routes/...
packages/shared/src/contracts/[domain].ts
```

---

## 3. Dependencies

- New npm packages: [must use pnpm catalog — list here for `@RiskAgent`]

---

## 4. No duplicate logic

- Shared behavior lives in `packages/`; apps stay thin.
