# Prompt 00 — Load context for [Feature Name]

Copy everything below the line into your AI session (fill `[feature-id]`).

---

You are executing work for feature **`[feature-id]`** in an Sovereign workspace.

**Read in order:**

1. `.ai/memory/anti-patterns.md` (constraints)
2. `.ai/context/architecture.md`
3. `.ai/context/project-type.md`
4. This feature package under `.ai/plans/active/features/[feature-id]/`:
   - `README.md`
   - `plan.md`
   - `context.md`
   - `specification.md` (if present)
   - `api.md`, `structure.md`, `design.md`, `database.md`
   - `contracts/README.md`

**Do not write code yet.** Summarize:

- What is in scope vs out of scope
- Which contract files exist or are missing
- Which phase we are in (`phases/`)

Wait for confirmation before proceeding to prompt `01-contract-and-api.md`.
