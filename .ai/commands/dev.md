---
type: command-registry
tier: OMEGA
version: 19.0.0
compliance: Law 151/2020
traceability: ISO-8601 Certified
---

# `/dev`

Implementation, testing, and automated remediation

## 📋 Subcommands

| Subcommand | Purpose | Usage |
|------------|---------|-------|
| `init` | Env setup & CI/CD scaffolding | `/dev init` |
| `implement` | Code generation governed by specs | `/dev implement` |
| `test` | Execute industrial test suites | `/dev test` |
| `fix` | Recursive remediation of drift & failures | `/dev fix` |
| `build` | Production bundle & verification | `/dev build` |

## 🛡️ Sovereign Protocol
- **Agent**: factory_orchestrator
- **Gate**: Omega Gate v2
- **Traceability**: Appends Reasoning Hash to .ai/logs/factory.jsonl
- **Compliance**: Egyptian Law 151/2020 Certified

## Client workspace onboarding gate

Under **`workspaces/clients/**`**, if **`.ai/onboarding/state.yaml`** has **`onboarding_complete: false`**, **refuse** **`implement`** and **`build`** (production bundle) until onboarding is finished — redirect to **`/onboard status`**. **`init`** (tooling only) remains allowed.
