# Prompt 01 — Contracts and API for [Feature Name]

**Prerequisites:** Prompt `00` complete; `api.md` and `contracts/README.md` read.

---

Implement or update **Zod contracts** in `packages/shared/src/contracts/[domain].ts` to match `api.md` and `specification.md`.

**Requirements:**

- `Schema`, `Create*`, `Update*`, `Query*` as needed; export inferred types.
- Run `/contract validate` and `/contract lock [domain]` when ready.
- Update `contracts/README.md` with file paths and lock status.

**Forbidden:** implementation in `apps/` until contracts validate for this domain.

**Output:** list of files changed + validation result.
