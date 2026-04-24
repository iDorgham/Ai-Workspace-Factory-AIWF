# 📐 AIWF — SDD PLANNING PROTOCOLS (v19.0.0 OMEGA)
**Status:** Canonical Planning Standard  
**Tier:** OMEGA (Singularity Level)  
**Governance:** Law 151/2020 Compliant

---

## 🏛️ 1. ARCHITECTURAL PHASING
Every industrial project must be decomposed into logical phases.

### 🚩 MVP PRIORITY RULE
For all **New Projects**, the initial phase **MUST** be designated as `00-mvp`.
- **Focus**: Core functionality, critical path, and feasibility verification.
- **Gate**: No secondary phases can be scaffolded until the `00-mvp` blueprint is OMEGA-Certified.

---

## 🛰️ 2. HIGH-DENSITY SPECIFICATION RULE
A phase is considered "Blueprint Ready" only if it contains a minimum of **5 to 10 unique specifications**. Single-file monolith specs are strictly forbidden.

### 📋 REQUIRED SPEC TYPES (MINIMUM 5)
1. **`api-contract.spec.json`**: Technical interface and endpoint definitions.
2. **`state-management.spec.json`**: Data flow, persistence, and state transitions.
3. **`security-hardening.spec.json`**: Encryption, auth, and boundary validation.
4. **`ui-ux-design.spec.json`**: Component hierarchy, interaction flows, and aesthetics.
5. **`industrial-compliance.spec.json`**: Law 151/2020 residency and regional audit rules.
6. **`performance-slas.spec.json`**: Latency targets, resource limits, and scaling gates.
7. **`seo-strategic-map.spec.json`**: Semantic structure, metadata, and visibility goals.
8. **`test-fixtures.spec.json`**: Mock data and automated validation scenarios.

---

## 🛡️ 3. GOVERNANCE & TRACEABILITY
- **Naming Convention**: `[PHASE-ID]-[DOMAIN].spec.json`
- **Location**: `.ai/plan/[STREAM]/[PHASE-ID]/`
- **Equilibrium**: Every spec must include a `traceability_hash` linked to the parent phase.

---
*Governor: Dorgham | Registry: .ai/governance/SDD_PROTOCOLS.md*
