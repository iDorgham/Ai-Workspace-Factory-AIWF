---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# 📜 UAE Contract Drafting Physics

## Purpose
Enforce professional legal standards for commercial drafting within the UAE. This skill sets the logic for MoHRE-compliant employment, Mainland vs. Freezone commercial agreements, and absolute bilingual alignment.

---

## Technique 1 — MoHRE & Employment Logistics

### The UAE Labor Law (Federal Decree-Law No. 33 of 2021)
- **Term Limits**: All employment contracts must be **Fixed-Term** (up to 3 years, renewable). Unlimited contracts are no longer legally valid in the UAE private sector.
- **Probation Periods**: Maximum of 6 months.
- **Arbitration Avoidance**: Employment disputes must go through MoHRE first; do not include complex international arbitration clauses in standard employment contracts.

---

## Technique 2 — Real Estate & Ejari (Leasing)

- **Tenancy Contracts**: For Dubai, the contract *must* align with the RERA (Real Estate Regulatory Agency) unified tenancy contract standards to be registered in the **Ejari** system.
- **Addendums**: Because the standard Ejari is rigid, all custom terms (e.g., fit-out periods, subleasing restrictions) must be placed in a legally referenced **Addendum**.

---

## Technique 3 — Bilingual Formatting & The "Prevailing Language"

- **Two-Column Standard**: Professional UAE contracts should be formatted in a two-column table (English on the Left [LTR], Arabic on the Right [RTL]).
- **The "Prevailing" Clause**:
  - *Mainland UAE*: "In the event of a discrepancy between the Arabic and English texts, the Arabic text shall prevail."
  - *DIFC/ADGM*: "This agreement is drafted in English. Any Arabic translation is for convenience only, and the English text shall prevail."

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Using "Consideration"** | Legal ambiguity | UAE law requires "Cause" (Sabab) rather than the English Common Law concept of "Consideration." Adjust drafting terminology accordingly. |
| **Invalid Penalty Clauses** | Unenforceable terms | Penalty clauses (Liquidated Damages) must be a reasonable pre-estimate of loss, subject to a judge's reduction under the UAE Civil Code. |
| **Missing Capacity Verification** | Contract Nullified | For corporate signers, explicitly state that they are signing via a legally valid and notarized Power of Attorney (PoA) or as the registered Manager on the Trade License. |

---

## Success Criteria (UAE Drafting QA)
- [ ] Contract governing law correctly targets either "UAE Federal Law and Emirate Law" or "DIFC/ADGM Law" based on incorporation.
- [ ] Sub-jurisdiction courts are defined (e.g., "The Courts of Dubai").
- [ ] Document layout supports clean RTL and LTR rendering side-by-side.