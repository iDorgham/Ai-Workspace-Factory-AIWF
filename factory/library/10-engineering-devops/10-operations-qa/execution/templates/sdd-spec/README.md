# SDD spec templates (`sdd-spec/`)

On **`/plan [phase]/[spec]`** confirmation, copy these **seven** files into:

**`.ai/plans/active/features/[01-phase-name]/[01-spec-name]/`**

| File | Role |
|------|------|
| `plan.md` | User story, AC (+ IDs), **Data Shape**, success metrics, edge cases |
| `design.md` | UI/UX flows, components, tokens |
| `context.md` | Dependencies, constraints, DMP slice hints, anti-pattern hooks |
| `api.md` | Endpoints, request/response, auth |
| `database.md` | Schema, relations, migrations, indexing |
| `contracts.md` | Planning-truth Zod summary (auto from **Data Shape**); **sync** → `packages/shared/src/contracts/[domain].ts` |
| `structure.md` | Module boundaries, layout, import graph |

**Eighth file (not in this folder):** **`prompt.md`** — written by **SOS** after silent pre-flight (`spec:validate` → `contract:auto-generate` → `contract:auto-validate`).

**Phase file:** **`../manifest.md`** at phase root — dependency graph, tiers, gate status (SOS-7 / Router).

**Legacy:** **`/plan --legacy [name]`** may still use a flat **`.ai/plans/active/features/[name].md`**; prefer phase/spec for new work.
