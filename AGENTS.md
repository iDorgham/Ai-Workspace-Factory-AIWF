# 🤖 AIWF AGENT REGISTRY (v7.0.0)

The AI Workspace Factory operates via a specialized swarm of agents, each governed by specific sovereign protocols and consensus rules.

---

## 🏛️ CORE AGENTS — T0 (Always Active)

| Agent | Role | Responsibility |
| :--- | :--- | :--- |
| **Master Guide** | Orchestrator | High-level strategy, orchestration, cross-project sync, Omega Gate mediation, and global memory management. |
| **Healing Bot v2** | Supervisor | Predictive structural monitoring, drift detection, and auto-remediation. Logs to `.ai/logs/healing-bot.md`. |
| **Swarm Router v3** | Mediator | Routes tasks across agents, resolves conflicts via multi-agent consensus (≥2/3 agreement required). |
| **Recursive Engine** | Scientist | Analyzes session friction and corrections → converts into permanent skill manifests in `skill-memory/`. |
| **Chaos Validator** | Stress-Tester | Injects controlled stressors to verify isolation boundaries and adaptive recovery (isolated env only). |

---

## 🔬 SPECIALIZED SUB-AGENTS — T1 (Dynamically Spun by Swarm Router v3)

| Sub-Agent | Role | Responsibility |
| :--- | :--- | :--- |
| **Spec Architect** | Designer | Builds and validates `spec.md` + `spec.yaml` per the AIWF SDD Blueprint schema. |
| **Contract Guardian** | Enforcer | Enforces `api-contract.yaml`, `state-contract.json`, and all test fixtures. Blocks `/dev` if contracts fail. |
| **Regional Adapter** | Localizer | Injects Egypt/Red Sea/MENA adaptations: Arabic RTL, Fawry/Vodafone Cash, Law 151/2020 data residency, EGP/SAR/AED handling, tourism/hospitality features. |
| **Deployment Specialist** | Deployer | Manages Vercel deployments, environment variables, preview/production separation. Only invoked via `/deploy`. |
| **Integrity Auditor** | Inspector | Runs path integrity, sovereignty checks, and compliance audits. Executes `audit_path_integrity.py`. |

---

## 🛠️ COMPOSITION AGENTS — T2

| Agent | Role | Responsibility |
| :--- | :--- | :--- |
| **Factory Scaffolder** | Architect | Assembles new sovereign workspaces from curated `factory/library/` components. |
| **Profile Auditor** | Gatekeeper | Ensures workspace profiles align with library schemas and compliance rules. |

---

## 📋 REQUIRED SKILLS (Enforced Across All Agents)

- **Library-First Composition**: Always pull from `factory/library/` and `factory/profiles/` before generating ad-hoc.
- **Append-Only Traceability**: All mutations include ISO-8601 timestamp + Reasoning Hash + rollback pointer.
- **Fail-Forward Recovery**: Errors trigger repair branches, not session termination.
- **Token Efficiency**: Session overhead < 2.5% via structured outputs.
- **MENA Sovereignty & Cultural Compliance**: Regional adaptations applied when `--region` flag is active.
- **Spec-Driven Execution**: All implementation gated on validated `spec.yaml` contract.

---

## 🧠 Learned User Preferences
- **Industrial Aesthetic**: Prefers dark mode, high-tech, and "premium" visual styling for all artifacts and UIs.
- **Library-First**: Prioritizes reuse and versioning over ad-hoc generation.
- **Traceability**: Requires ISO-8601 timestamps and Reasoning Hashes for all autonomous mutations.

## 📋 Learned Workspace Facts
- **Root Directory**: `/Users/Dorgham/Documents/Work/Devleopment/AIWF`
- **Sovereign Isolation**: All client work is strictly contained within `workspaces/<slug>/`.
- **Governance**: All structural changes require explicit `Dorgham-Approval` via Omega Gate v2.
- **Deploy Policy**: Vercel deployment ONLY via explicit `/deploy` command — never auto-triggered.

---

*Registry version: 7.0.0*
*Last updated: 2026-04-23T12:44:57+02:00*
