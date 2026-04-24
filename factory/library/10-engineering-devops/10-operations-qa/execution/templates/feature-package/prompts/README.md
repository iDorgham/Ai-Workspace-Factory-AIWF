# Prompts: [Feature Name]

> **Feature ID:** `[feature-id]`
> **Usage:** Run in order during implementation sessions, or assign steps to agents. Paste into chat **after** loading this feature package in context.

---

## Sequence

| Order | File | Purpose |
|-------|------|---------|
| 00 | `00-load-context.md` | Load workspace + package docs |
| 01 | `01-contract-and-api.md` | Author or lock contracts; align API |
| 02 | `02-implementation-backend.md` | API routes and services |
| 03 | `03-implementation-frontend.md` | UI with tokens and i18n |
| 04 | `04-database-migration.md` | Prisma migrations |
| 05 | `05-documentation-and-i18n.md` | Copy and docs |
| 06 | `06-quality-gates.md` | Run gates and fix violations |

---

## Rules

- Obey **Dynamic Memory Protocol** and **contract-first** rules in `CLAUDE.md` / `.cursorrules`.
- Do not skip **quality gate** order in `06`.
