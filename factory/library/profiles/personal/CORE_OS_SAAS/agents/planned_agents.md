# Planned agents — CORE_OS_SAAS

| Agent (registry name) | Why this template needs it |
|----------------------|-----------------------------|
| **Master Guide** | Phase intent, `/guide`, orchestration across monorepo packages. |
| **Spec Architect** | SDD density, `spec.md` / fixtures before `/dev implement`. |
| **Contract Guardian** | API + state contracts across `apps/*` and `packages/*`. |
| **CI Specialist** | Turborepo pipelines, flaky test triage, workflow repair. |
| **Security Auditor** | Auth, secrets, dependency surface for SaaS. |
| **Integrity Auditor** | `/audit health`, path + gate hygiene in large trees. |
| **Deployment Specialist** | Preview/prod separation; only when `/deploy` (or equivalent) is invoked. |
| **Factory Scaffolder** | Library-first pulls from `factory/library/` when extending the shard. |
| **Profile Auditor** | Keeps workspace profile JSON aligned with governance. |
| **Healing Bot v2** | Structural drift remediation (`/dev fix`). |

Drop for a **minimal** R&D copy: Profile Auditor, Contract Guardian (only if you have no public API yet) — at your risk.
