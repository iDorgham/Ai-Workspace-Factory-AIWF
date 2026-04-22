# Database: [Feature Name]

> **Feature ID:** `[feature-id]`
> **Agent:** @DBA — Prisma only; no raw SQL in app code.

---

## 1. Models affected

| Model | Change |
|-------|--------|
| | add column / new model / relation |

---

## 2. Migration strategy

- Order: expand → backfill → contract (zero-downtime if production).
- Down migration: required.

---

## 3. Indexes and constraints

…

---

## 4. RLS / tenancy (if multi-tenant)

…

---

## 5. Seed / backfill

…
