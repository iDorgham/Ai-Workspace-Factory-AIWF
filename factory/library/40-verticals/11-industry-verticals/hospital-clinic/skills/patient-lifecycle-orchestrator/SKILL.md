# 🧬 Patient Lifecycle Orchestrator
> **Skill Category:** Clinical Operations / EMR Physics
> **Domains:** Inpatient, Outpatient, Tele-medicine

## Purpose
Govern the technical lifecycle of a patient node. This skill ensures clinical consistency, appointment integrity, and perfectly sequenced insurance claim triggers.

---

## 🛠️ Operational Techniques

### 1. EMR Physics (Electronic Medical Record)
- **Physics**: Draft and maintain structured patient stubs (History, Vitals, Diagnostics).
- **Staging**: Assign "Status Nodes" (e.g., Triage -> Consultant -> Treatment -> Discharge).
- **Logic**: Automate the generation of a "Post-Visit Summary" in bilingual (AR/EN) format.

### 2. Insurance Claim Physics
- **Trigger Logic**: Automated mapping of ICD-10/ICD-11 codes to clinical procedures.
- **Verification**: Cross-check treatment plans against insurance approval stubs before final billing.
- **Workflow**: `/medical ClaimAudit` scans patient files for missing pre-authorizations (pre-auth).

---

## 🛡️ Governance & Anti-Patterns
- **Anti-Pattern**: Using non-standard ICD codes.
- **Correction**: Enforce the "ICD-Master" block—all diagnoses MUST map to a valid WHO ICD registry node.

## Success Criteria
- [ ] 100% of patient visits result in a valid, bilingual clinical stub.
- [ ] Claim error rate reduced via pre-submission automated auditing.
