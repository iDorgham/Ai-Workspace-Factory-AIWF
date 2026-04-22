# 🏛️ AIWF MASTER REFERENCE (v6.0.0-alpha)
**The Single Source of Truth for the AI Workspace Factory**

---

## 0. 📜 PROJECT EVOLUTION (v1 — v6)
The AI Workspace Factory has evolved through six major architectural generations to reach its current antifragile state.

| Version | Era | Key Architectural Shift |
| :--- | :--- | :--- |
| **v1.0** | **Genesis** | Manual workspace scaffolding and basic context-sharing between AI tools. |
| **v2.0** | **Sovereign Core** | Formalization of the `.ai/` intelligence layer and the separation of "Master" vs "Client" logic. |
| **v3.0** | **Agentic Swarm** | Introduction of specialized sub-agents and the first iteration of the "Master Guide" orchestrator. |
| **v4.0** | **Industrial Grade** | Taxonomy expansion to 17 departments and 327+ library nodes. Standardized composition profiles. |
| **v5.0** | **Resilient Factory** | "Sovereign Isolation" protocol (zero cross-project writes) and deterministic JSON-based routing. |
| **v6.0** | **Antifragile Factory** | **Current State**. Autonomous Healing, Recursive Learning, and Swarm Consensus Orchestration. |

---

## 1. 🎯 STRATEGIC CORE: THE ANTIFRAGILE MISSION
The AI Workspace Factory (AIWF) is an **Antifragile Sovereign Composition Engine**. It learns from operational stressors, auto-remediates structural drift, and routes via swarm consensus.

---

## 2. 🤖 THE AGENT SWARM & COMMANDS
### Core Orchestrators (Tier 0/1)
- **Master Guide**: Root orchestrator; owns `WORKSPACE_MASTER_CONTEXT.md`.
- **Healing Bot**: Monitors drift via `audit_path_integrity.py`; auto-fixes violations.
- **Recursive Engine**: Processes feedback via `/master learn`; generates skill manifests.
- **Swarm Router v3**: Multi-agent consensus routing with deterministic fallback.
- **Chaos Validator**: Stress-tests recovery success rates (Target ≥95%).

### Commands Manual
- `/master learn`: Analyzes session friction → updates `skill-memory/`.
- `/heal check`: Executes structural audit → triggers remediation.
- `/route consensus`: Multi-agent validation for critical strategy paths.
- `/chaos inject`: Injects stressors (latency, metadata gaps) for verification.
- `/compose [slug]`: Standard factory assembly from profile + library.

---

## 🛠️ OPERATIONAL TOOLS (SCRIPTS)
| Script | Path | Purpose |
| :--- | :--- | :--- |
| **Integrity Auditor** | `.ai/scripts/audit_path_integrity.py` | Validates sovereign boundaries and file placement. |
| **Remediation Agent** | `.ai/scripts/healing_agent.py` | The logic behind the Healing Bot; auto-fixes drift. |
| **Recursive Learning** | `.ai/scripts/recursive_engine.py` | The logic for `/master learn` and manifest generation. |
| **Environment Shim** | `factory/scripts/init-v6-shims.py` | Initialized v6 memory layers and upgraded configs. |
| **Safe Backup** | `scripts/backup-workspaces.sh` | Creates timestamped archives with SHA256 verification. |
| **Emergency Rollback** | `scripts/emergency-rollback.sh` | Reverts the entire factory to the stable v5.0.0 baseline. |

---

## 📁 COMPLETE FILESYSTEM INVENTORY (.ai)
The intelligence layer containing all agents, memory, and logs:
- **.ai/agents/**: Agent personas and instruction sets.
- **.ai/scripts/**: Core automation and evolution logic.
- **.ai/memory/**:
    - `workspace-index.json`: Global client tracking.
    - `skill-memory/`: Cumulative learned skill manifests (JSON).
- **.ai/logs/**:
    - `healing-bot.md`: Audit and remediation history.
    - `learning-engine.md`: History of generated skill manifests.
    - `workflow.jsonl`: Append-only traceability log.

---

## 📁 COMPLETE LIBRARY INVENTORY (factory/library)
The 491-component library structured by department:
- **01-Software-Engineering**: Backend, Frontend, Engineering Core, Mobile.
- **02-Web-Platforms**: SaaS Platforms, API Design, Cloud Architecture.
- **03-Security-Compliance**: Cybersecurity, Fintech, Data Sovereignty, LegalTech.
- **04-Business-Strategy**: Venture Design, Business Analysis, Finance Ops.
- **05-Data-Analytics**: Market Research, Intel Synthesis, AI Automation.
- **06-Branding**: Identity Engine, Brand Strategy, Agency Ops.
- **07-Visibility-Optimization**: SEO, LLMO, Semantic Search.
- **08-Media-Production**: 3D, Video, Image, Audio Tech.
- **09-Social-Engagement**: Viral Loops, Community, Influencer Ops.
- **10-Operations-QA**: Execution, Supply Chain, Training, Performance.
- **11-Industry-Verticals**: (Legal, Medical, Hospitality, Real Estate, Travel, GovTech).
- **12-Meta-Engine**: Blueprints, Library Taxonomy, Scripts.
- **13-Gaming-Entertainment**: Game Engines, Metaverse Narrative.
- **14-Ai-Intelligence**: Frontier Models, Fine-Tuning, Workflows.
- **15-Music-Sound-Engineering**: Composition Theory, Sound Design.
- **16-Content-Dominance**: Storytelling, Viral Loops, Copywriting.
- **17-Performance-Marketing**: Ad Production, Growth Economics.

---

## 📁 COMPOSITION PROFILES (factory/profiles)
- `3d-rendering-studio.json`
- `ai-automation-lab-pro.json`
- `healthcare-medical-system.json`
- `legal-brokerage-hub.json`
- `islamic-finance-hub.json`
- `hospitality-restaurant-ops.json`
- `real-estate-developer-pro.json`
- `tourism-travel-suite.json`
- `govtech-v11.json`
- `cyber-security-hardening.json`
- `branding-agency.json`
- `seo-dominance-engine.json`
- *(+ 17 additional profiles for all industry verticals)*

---

## 🛡️ GOVERNANCE: THE OMEGA GATE
- **Multi-Agent Consensus**: Structural changes require 3-agent agreement.
- **Dorgham-Approval**: Explicit human flag required for library mutations.
- **Reasoning Hashes**: Every autonomous edit is stamped with a unique hash.
- **ISO-8601 Traceability**: No truncation; all logs are append-only.

---

## 📄 THE PRD (STRATEGIC SPECIFICATIONS)
### Problem Statement:
v5.0.0 achieved deterministic routing and isolation, but v6.0.0 solves the "Static Library" and "Manual Remediation" bottlenecks through autonomous evolution.

### Core Requirements:
- **FR-1.1**: Healing Bot autonomous remediation (logs to `.ai/logs/healing-bot.md`).
- **FR-2.1**: Recursive Learning (`/master learn`) via correction pattern analysis.
- **FR-3.1**: Swarm Consensus Router (Multi-agent validation, fallback on timeout).
- **FR-4.1**: Chaos Scaffolding (Verifies 95%+ recovery success).
- **FR-5.1**: Adaptive Token Budgeting (<2.5% session cap).

---

## 🗺️ THE ROADMAP (PHASE-GATED EVOLUTION)
### Phase 6: Full Antifragile Release (COMPLETE)
- **Status**: Industrialized and Operational (2026-04-22).
- **Achievements**: Documentation suite, core scripts, and operational engine verification.

### Phase 7: Sovereign Scale (Q3 2026)
- **Deliverables**: Hot-Sync Protocol (`/update-agents --safe`), Multi-machine orchestration.
- **Goal**: Implement a mechanism to pull library-first updates into existing sovereign projects without state loss.

### Phase 8: Autonomous Industrialization (Q4 2026)
- **Deliverables**: CI/CD Workspace Generation, automated health scoring.
- **Goal**: 100% autonomous provisioning and library maintenance.

---
**Version**: 6.0.0-alpha | **Status**: Industrialized
**Developed by**: Antigravity (Advanced Agentic Coding)
