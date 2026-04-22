# ⚖️ Regulatory Compliance Medical
> **Skill Category:** Healthcare Governance
> **Jurisdictions:** UAE (DHA, DOH), Egypt (MoHP), Global (HIPAA/GDPR)

## Purpose
Enforce healthcare-specific regulatory physics. This skill ensures all clinical operations adhere to regional data sovereignty laws and professional licensure mandates.

---

## 🛠️ Operational Techniques

### 1. Data Sovereignty (NABIDH/Malaffi)
- **Physics**: Automate the hashing and regional-lock of patient identifiers.
- **Protocol**: Block all clinical data exports to non-compliant cloud zones.
- **Workflow**: `/medical AuditSovereignty` scans project stubs for regional data residency violations.

### 2. HCP Licensure Auditing
- **Physics**: Periodically verify Healthcare Professional (HCP) license status against national registries.
- **Trigger**: Flag all surgeries/visits associated with an expired or grey-state license.
- **Compliance**: Enforce 100% DHA/DOH Professional Qualification Requirements (PQR).

---

## 🛡️ Governance & Anti-Patterns
- **Anti-Pattern**: Storing Patient Identifiers (PII) in plain-text markdown.
- **Correction**: Use the "Anonymization-Node" logic—mask all PII with UUIDs before workspace injection.

## Success Criteria
- [ ] 100% of HCP stubs possess a valid, verified license hash.
- [ ] Zero clinical data leaks to non-sovereign nodes.
