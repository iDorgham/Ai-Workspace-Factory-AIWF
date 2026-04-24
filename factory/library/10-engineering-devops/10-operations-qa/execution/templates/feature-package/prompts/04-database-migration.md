# Prompt 04 — Database migration for [Feature Name]

**Prerequisites:** `database.md` reviewed; contract shapes stable for persisted fields.

---

Update Prisma schema and create migrations per `database.md`.

**Requirements:**

- Follow zero-downtime pattern if production: nullable → backfill → constraint.
- Include down migration where applicable.
- No raw SQL in application code.

**Output:** migration folder name + summary of model changes.
