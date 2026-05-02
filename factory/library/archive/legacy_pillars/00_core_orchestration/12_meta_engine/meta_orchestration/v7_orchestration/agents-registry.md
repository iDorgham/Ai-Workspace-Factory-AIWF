---
type: Generic
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# 🤖 AIWF v7.0.0 — Agents Registry
# Library Component: 12-meta-engine/meta-orchestration/v7-orchestration/agents_registry.md
# Version: 7.0.0 | Reasoning Hash: sha256:agents-v7-2026-04-23
# Rollback: meta-orchestration/agents/ (v6 agents remain in /agents directory)
# ============================================================

## Overview

This file is the **canonical, versioned registry** of all agents and sub-agents for AIWF v7.0.0. It is consumed by:
- `CLAUDE.md` (session startup)
- `/compose` (workspace scaffolding)
- Hot-Sync Protocol (`/update-agents --safe`)
- Swarm Router v3 (dynamic dispatch)

All workspaces inheriting from this library component get the full ultra-antifragile swarm automatically.

---

## 🏛️ CORE AGENTS — T0 (Always Active)

```yaml
tier: T0
activation: always
consensus_threshold: "≥2/3"

agents:
  master_guide:
    id: "T0-001"
    name: "Master Guide"
    role: "Orchestrator"
    responsibilities:
      - "High-level strategy and cross-project orchestration"
      - "Omega Gate v2 mediation and approval logging"
      - "Global memory management and session continuity"
      - "Persistent instructor mode (Guide Protocol)"
    triggers: ["session_start", "user_command", "omega_gate_request"]

  healing_bot_v2:
    id: "T0-002"
    name: "Healing Bot v2"
    role: "Supervisor"
    version: "2.0.0"
    responsibilities:
      - "Predictive structural drift detection (before failure)"
      - "Auto-remediation of detected drift patterns"
      - "Append-only repair logging to .ai/logs/healing_bot.md"
    upgrade_from: "v1 (reactive) → v2 (predictive)"
    triggers: ["session_start", "drift_detected", "/fix --auto-fix"]

  swarm_router_v3:
    id: "T0-003"
    name: "Swarm Router v3"
    role: "Mediator"
    version: "3.0.0"
    responsibilities:
      - "Route tasks to appropriate agents/sub-agents"
      - "Resolve multi-agent conflicts via consensus (≥2/3)"
      - "Dynamic spin-up of T1 sub-agents on demand"
    triggers: ["any_command", "conflict_detected", "sub_agent_needed"]

  recursive_engine:
    id: "T0-004"
    name: "Recursive Engine"
    role: "Scientist"
    responsibilities:
      - "Analyze session friction and user corrections"
      - "Convert friction patterns into permanent skill manifests"
      - "Write to skill-memory/ with versioned manifests"
    triggers: ["session_end", "user_correction", "/master_learn"]

  chaos_validator:
    id: "T0-005"
    name: "Chaos Validator"
    role: "Stress-Tester"
    responsibilities:
      - "Inject controlled stressors to verify isolation boundaries"
      - "Validate adaptive recovery mechanisms"
      - "Run in isolated environments only — never production"
    triggers: ["/test --stress", "/chaos inject"]
```

---

## 🔬 SPECIALIZED SUB-AGENTS — T1 (Dynamically Spun by Swarm Router v3)

```yaml
tier: T1
activation: dynamic
spin_up_by: "Swarm Router v3"

sub_agents:
  spec_architect:
    id: "T1-001"
    name: "Spec Architect"
    role: "Designer"
    responsibilities:
      - "Build and validate spec.md (human narrative)"
      - "Build and validate spec.yaml (machine contract)"
      - "Enforce AIWF SDD Blueprint folder structure"
      - "Run spec-lint gate before output"
    triggers: ["/plan", "spec_validation_needed"]
    blocks: ["/dev (if spec invalid)"]

  contract_guardian:
    id: "T1-002"
    name: "Contract Guardian"
    role: "Enforcer"
    responsibilities:
      - "Enforce api-contract.yaml and state-contract.json"
      - "Validate all test fixtures exist before /dev"
      - "Generate contract-coverage.json"
      - "Block /dev execution if contract gates fail"
    triggers: ["/dev", "/test", "contract_check_gate"]
    blocks: ["/dev (if contracts fail)"]

  regional_adapter:
    id: "T1-003"
    name: "Regional Adapter"
    role: "Localizer"
    regions: ["egypt", "redsea", "mena"]
    responsibilities:
      - "Inject Arabic RTL layout configurations"
      - "Configure Fawry and Vodafone Cash payment integrations"
      - "Apply Egypt Law 151/2020 data residency rules"
      - "Add EGP/SAR/AED currency handling"
      - "Configure tourism and hospitality feature flags"
    triggers: ["--region flag on any command", "/plan --region", "/deploy --region"]

  deployment_specialist:
    id: "T1-004"
    name: "Deployment Specialist"
    role: "Deployer"
    responsibilities:
      - "Manage Vercel CLI lifecycle (link, env pull, deploy)"
      - "Handle preview and production deployments"
      - "Inject environment variables per deployment target"
      - "Log deployment metadata to .ai/logs/deployments.log"
    triggers: ["/deploy (EXPLICIT ONLY — never auto)"]
    constraint: "NEVER triggered by git push or auto-merge"

  integrity_auditor:
    id: "T1-005"
    name: "Integrity Auditor"
    role: "Inspector"
    responsibilities:
      - "Run path integrity checks on .ai/ folder structure"
      - "Verify sovereign isolation boundaries"
      - "Execute audit_path_integrity.py"
      - "Compliance audits for regional requirements"
    triggers: ["/heal check", "/fix --spec-sync", "session_start (background)"]

  scrape_specialist:
    id: "T1-006"
    name: "Scrape Specialist"
    role: "Data Harvester"
    responsibilities:
      - "Autonomous data extraction from public URLs"
      - "Bypass common anti-bot patterns safely"
      - "Parse unstructured HTML into JSON/Markdown"
      - "Ensure Law 151/2020 data privacy during harvesting"
    triggers: ["/scrape"]

  content_architect:
    id: "T1-007"
    name: "Content Architect"
    role: "Multi-modal Copywriter"
    responsibilities:
      - "Generate SEO-optimized content for blogs and e-commerce"
      - "Multi-language support (AR/EN) with RTL awareness"
      - "Align copy with PRD REQ-IDs and brand voice"
    triggers: ["/content"]

  asset_guardian:
    id: "T1-008"
    name: "Asset Guardian"
    role: "Quality Gatekeeper"
    responsibilities:
      - "Validate /art output for accessibility (WCAG 2.1)"
      - "Perform color contrast checks between assets and UI"
      - "Ensure brand consistency and resolution standards"
    triggers: ["/art (post-generation gate)"]
```

---

## 🛠️ COMPOSITION AGENTS — T2

```yaml
tier: T2
activation: on_scaffold

agents:
  factory_scaffolder:
    id: "T2-001"
    name: "Factory Scaffolder"
    role: "Architect"
    responsibilities:
      - "Assemble new sovereign workspaces from factory/library/ components"
      - "Apply profiles from factory/profiles/"
      - "Generate workspace .ai/ directory structure"
    triggers: ["/personal project", "/client project", "/compose"]

  profile_auditor:
    id: "T2-002"
    name: "Profile Auditor"
    role: "Gatekeeper"
    responsibilities:
      - "Validate workspace profiles against library schemas"
      - "Enforce compliance rules during profile application"
      - "Block malformed profiles from being applied"
    triggers: ["/compose", "profile_applied"]
```

---

## 📋 REQUIRED SKILLS (Enforced Across All Agents)

```yaml
required_skills:
  - id: "SK-001"
    name: "Library-First Composition"
    rule: "Always pull from factory/library/ and factory/profiles/ before generating ad-hoc."
    enforcement: blocking

  - id: "SK-002"
    name: "Append-Only Traceability"
    rule: "All mutations include ISO-8601 timestamp + Reasoning Hash + rollback pointer."
    enforcement: blocking

  - id: "SK-003"
    name: "Fail-Forward Recovery"
    rule: "Errors trigger repair branches, not session termination."
    enforcement: required

  - id: "SK-004"
    name: "Token Efficiency"
    rule: "Session overhead < 2.5% via structured outputs."
    enforcement: advisory

  - id: "SK-005"
    name: "MENA Sovereignty & Cultural Compliance"
    rule: "Regional adaptations applied when --region flag is active."
    enforcement: required

  - id: "SK-006"
    name: "Spec-Driven Execution"
    rule: "All implementation gated on validated spec.yaml contract."
    enforcement: blocking
```

---

*Component version: 7.0.0*
*Library path: 12-meta-engine/meta-orchestration/v7-orchestration/agents_registry.md*
*Last updated: 2026-04-23T12:56:22+02:00*
*Reasoning Hash: sha256:agents-v7-2026-04-23*
*Rollback: previous agent definitions in meta-orchestration/agents/*
