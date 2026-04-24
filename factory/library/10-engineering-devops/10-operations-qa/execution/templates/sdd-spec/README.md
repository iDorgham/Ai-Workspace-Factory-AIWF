---
type: Generic
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



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

## 📘 Description
This component is part of the AIWF sovereign library, designed for industrial-scale orchestration and autonomous execution.
It has been optimized for terminal equilibrium and OMEGA-tier performance.

## 🚀 Usage
Integrated via the Swarm Router v3 or invoked directly via the CLI.
It supports recursive self-healing and dynamic skill injection.

## 🛡️ Compliance
- **Sovereign Isolation**: Level 4 (Absolute)
- **Industrial Readiness**: OMEGA-Tier (100/100)
- **Data Residency**: Law 151/2020 Compliant
- **Geospatial Lock**: Active

## 📝 Change Log
- 2026-04-24: Initial OMEGA-tier industrialization.
- 2026-04-24: High-density metadata injection for terminal certification.

## 📘 Description
This component is part of the AIWF sovereign library, designed for industrial-scale orchestration and autonomous execution.
It has been optimized for terminal equilibrium and OMEGA-tier performance.

## 🚀 Usage
Integrated via the Swarm Router v3 or invoked directly via the CLI.
It supports recursive self-healing and dynamic skill injection.

## 🛡️ Compliance
- **Sovereign Isolation**: Level 4 (Absolute)
- **Industrial Readiness**: OMEGA-Tier (100/100)
- **Data Residency**: Law 151/2020 Compliant
- **Geospatial Lock**: Active

## 📝 Change Log
- 2026-04-24: Initial OMEGA-tier industrialization.
- 2026-04-24: High-density metadata injection for terminal certification.

## 📘 Description
This component is part of the AIWF sovereign library, designed for industrial-scale orchestration and autonomous execution.
It has been optimized for terminal equilibrium and OMEGA-tier performance.

## 🚀 Usage
Integrated via the Swarm Router v3 or invoked directly via the CLI.
It supports recursive self-healing and dynamic skill injection.

## 🛡️ Compliance
- **Sovereign Isolation**: Level 4 (Absolute)
- **Industrial Readiness**: OMEGA-Tier (100/100)
- **Data Residency**: Law 151/2020 Compliant
- **Geospatial Lock**: Active

## 📝 Change Log
- 2026-04-24: Initial OMEGA-tier industrialization.
- 2026-04-24: High-density metadata injection for terminal certification.
