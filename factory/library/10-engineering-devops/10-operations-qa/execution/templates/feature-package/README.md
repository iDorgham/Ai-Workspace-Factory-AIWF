---
type: Generic
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# Feature package template (legacy / optional deep tree)

**SDD default:** **`/plan [phase]/[spec]`** + **`.ai/templates/sdd-spec/`** — see **`docs/workspace/reference/feature-plan-package-layout.md`**. Use this folder for **`/plan --legacy`**, migration, or extra **`phases/`** / **`prompts/`** depth.

Copy this entire folder to:

```
.ai/plans/active/features/[feature-id]/
```

Replace `[feature-id]`, `[Feature Name]`, and all bracketed placeholders. Keep **one package per feature**; link tasks in **`.ai/plans/active/tasks/`** from **`tasks/README.md`**.

**Canonical layout spec:** **`docs/workspace/reference/feature-plan-package-layout.md`**

**Legacy SDD order:** `README.md` → **`plan.md`** → confirm → **`spec:validate`** / **`contract:auto-generate`** / **`contract:auto-validate`** → **`sos/manifest.md`** + **`sos/prompts/`** (if not using phase **`manifest.md`** + spec **`prompt.md`**) → **`/swarm`** / **`/build`**.  
**Depth order (optional files):** `context.md` → **`specification.md`** (if split from plan) → **`contracts/README.md`** → **`api.md`** → **`database.md`** → **`structure.md`** → **`design.md`** → template **`prompts/`** (00 → 06) → **`phase_logs/`** after each gate. **Do not confuse** template **`prompts/`** with **`sos/prompts/`** (legacy SOS output).

---

## Contents

| Path | Role |
|------|------|
| `plan.md` | Master plan and milestones |
| `specification.md` | Formal spec narrative (SDD) |
| `context.md` | Domain and constraints |
| `api.md` | API surface (aligned with contracts) |
| `structure.md` | Repo file/package map |
| `design.md` | UI/UX, tokens, a11y |
| `database.md` | Schema and migration notes |
| `documentation.md` | User docs and release notes |
| `test-plan.md` | TDD: tests before implementation (optional) |
| `contracts/README.md` | Links to Zod contracts in `packages/shared/src/contracts/` |
| `phases/` | In-feature phase breakdown |
| `phase_logs/` | Dated audit trail |
| `tasks/` | Task index |
| `prompts/` | Optional manual playbook (00–06) |
| `sos/` | **Not in this zip-tree** until SOS runs — create **`manifest.md`**, **`prompts/`**, optional **`runtime-state.md`** per **`docs/workspace/reference/feature-plan-package-layout.md`** |

---

*Template version: 1.1 (SDD + SOS) | @Architect*
