# Phases: [Feature Name]

> **Feature ID:** `[feature-id]`
> **PGD:** Do not advance to the next phase without exit criteria met and a log entry in **`../phase_logs/`**.

---

## Phase index

| # | File | Purpose | Exit criteria (summary) |
|---|------|---------|---------------------------|
| 01 | `01-discovery.md` | Problem, users, constraints | Stakeholder alignment |
| 02 | `02-specification.md` | Contracts, API, data | Spec + contracts ready to lock |
| 03 | `03-implementation.md` | Build, integrate | Tests green, gates pass |
| 04 | `04-verification.md` | QA, docs, release | Ship checklist complete |

---

## Methodology note

- **ALID:** Phases may collapse into one increment.
- **DFD:** Complete design assets before `03-implementation`.
- **TDD:** Embed test-first in `03-implementation` and `test-plan.md`.
