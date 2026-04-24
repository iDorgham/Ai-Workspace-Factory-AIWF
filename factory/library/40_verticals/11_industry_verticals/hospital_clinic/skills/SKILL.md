---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# 🏥 Hospital & Clinic Operations (MENA)

## Purpose
Enforce professional operational standards for the management of hospitals and medical clinics in the MENA market. This skill focuses on **Patient Flow Optimization**, **EMR Integration**, and **Insurance Claims Governance**.

---

## Technique 1 — Patient Flow & Throughput Optimization

### The "Frictionless" Clinic
- **Wait-Time Governance**: Implement digital queue management systems with real-time SMS updates to keep "Wait Room Density" < 75% of capacity.
- **Triage Logic**: Standardize the triage process to ensure that critical cases are identified within 120 seconds of arrival, regardless of appointment status.

---

## Technique 2 — EMR (Electronic Medical Record) Physics

- **Interoperability**: Standardize on HL7/FHIR protocols to allow seamless data transfer between the clinic and national health portals (Malaffi, Nabidh).
- **Access Control**: Enforce "Least Privilege" access. A receptionist should only see "Scheduling/Name" data; "Diagnosis/Clinical Notes" should be restricted via biometric or two-factor auth for medical staff only.

---

## Technique 3 — Revenue Cycle & Insurance Governance

- **Insurance Pre-Approval Logic**: Automate the "Eligibility Check" at the point of registration to avoid "Unpaid Claims" or "Rejection" by major providers (Daman, NextCare, MetLife).
- **Billing Transparency**: Ensure all patient invoices clearly delineate between "Provider Cost" and "Member Co-pay" to ensure trust and compliance with national consumer protection laws.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Manual Billing Entry** | High rejection rate | Integrate the Billing module directly into the EMR to auto-generate codes (ICD-10 / CPT-4) based on doctor notes. |
| **Paper-Based Records** | Data loss / Breach | Target 100% "Digital-First" operations; paper should only exist for physical consent signatures which are then immediately scanned and shredded. |
| **Poor Staff-to-Patient Ratio** | Burnout / Fatal error | Use predictive analytics (derived from `skills:05-data-analytics/market-research`) to forecast peak hours and staff accordingly. |

---

## Success Criteria (Clinic QA)
- [ ] Average patient wait-time is < 15 minutes.
- [ ] Insurance claim rejection rate is < 5%.
- [ ] EMR access is verified via 2FA and biometrics.
- [ ] Successful sync with national health portals is verified weekly.