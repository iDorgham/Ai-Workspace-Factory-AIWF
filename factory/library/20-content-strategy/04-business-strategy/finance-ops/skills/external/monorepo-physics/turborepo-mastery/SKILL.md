---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# 📦 Monorepo Physics (Turborepo)

## Purpose
Enforce standards for managing large-scale monorepos. This skill focuses on the "Build Cache" logic, task orchestration, and dependency separation to ensure that CI/CD pipelines remain incredibly fast even as the workspace scales to millions of lines of code.

---

## Technique 1 — Task Graph Optimization (`turbo.json`)
- **Rule**: Every task (build, test, lint) must be explicitly defined in the `pipeline` with its cache dependencies.
- **Protocol**: 
    1. Map dependencies between tasks (e.g., "Build requires Lint to pass").
    2. Define `outputs` (e.g., `.next/**`) for caching.
    3. Use `inputs` (e.g., `src/**`) to prevent cache-busts from irrelevant file changes.

---

## Technique 2 — Remote Caching (Turborepo Remote)
- **Rule**: Use a Remote Cache to share build artifacts across the entire development team and CI runners.
- **Protocol**: 
    1. Link the local environment to the Vercel/Turbo Remote Cache.
    2. Configure the CI environment with the required `TURBO_TOKEN`.
    3. Verify that "Cache Hits" are occurring across different developer nodes to minimize redundant work.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Monolithic repo-wide dependencies** | Cache busting everything | Use "Workspace Protocols" (`workspace:*`) and keep internal package versions synced. |
| **Missing Task Dependencies** | Unreliable builds | ALWAYS define which tasks must run first; never rely on implicit execution order. |
| **Large assets in Git** | Slow cloning / CI lag | Use Git LFS or external object storage for large media assets; keep the source tree lean. |

---

## Success Criteria (Monorepo QA)
- [ ] CI build time for "No-Change" PRs is < 30 seconds (Cache Hit).
- [ ] 0% cross-package dependency leaks (verified via ESLint boundaries).
- [ ] Remote cache hit rate is > 80% for shared packages.
- [ ] Workspace structure follows the `/apps` and `/packages` separation standard.