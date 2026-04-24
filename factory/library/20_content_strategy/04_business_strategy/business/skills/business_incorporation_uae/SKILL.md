---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# 🏢 Business Incorporation (UAE)

## Purpose
Enforce professional legal and corporate strategy standards for incorporating and structuring businesses within the United Arab Emirates. This skill governs the logic of **Mainland vs. Freezone** jurisdiction, **Common Law implementation (DIFC/ADGM)**, and compliance with the UAE Commercial Companies Law.

---

## Technique 1 — Jurisdictional Logic (Mainland vs. Freezone)

### Mainland (DED - Department of Economic Development)
- **Use Case**: B2C retail, restaurants, and businesses requiring direct interaction with the local UAE market or government tenders.
- **Ownership Law Update**: Foreign investors can now own 100% of Mainland LLCs for most commercial and industrial activities (removing the legacy 51% Emirati sponsor requirement).
- **Compliance Constraint**: Requires a physical office lease (Ejari) for most trade licenses.

### Freezone (e.g., DMCC, JAFZA, DDA)
- **Use Case**: 100% foreign ownership with 0% corporate tax (subject to Qualifying Freezone rules) focused on international trade, tech, and consulting.
- **Constraint**: Cannot trade physical goods directly into the UAE Mainland without a local distributor.

---

## Technique 2 — Common Law Hubs (DIFC & ADGM)

- **The Financial Centers**: For high-scale FinTech, VC funds, and Holding companies, utilize the Dubai International Financial Centre (DIFC) or Abu Dhabi Global Market (ADGM).
- **Legal Physics**: These zones operate under **English Common Law**, completely separate from the UAE Civil Code. This provides absolute familiarity for international investors regarding contract enforcement and dispute resolution.

---

## Technique 3 — Emiritisation & Corporate Tax (Compliance)

- **Corporate Tax (Federal Decree-Law No.47 of 2022)**: 9% standard rate on taxable income exceeding AED 375,000. Freezones may be exempt ("Qualifying Income") but *must* still file audited financials.
- **Nafis (Emiritisation)**: Mainland companies with 50+ employees must increase their Emirati workforce by 2% annually. Failure results in severe accumulating fines.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Random Freezone Selection** | Banking rejection | Freezones must be chosen based on activity; some "cheap" Northern Emirate freezones face heavy compliance friction when opening UAE bank accounts. |
| **Ignoring VAT Registration** | Federal fines | Mandatory VAT registration if taxable supplies exceed AED 375,000; voluntary at AED 187,500. |
| **Treating ADGM as Mainland** | Contract voiding | Contracts drafted for ADGM entities must follow Common Law, not UAE Civil Law terms. |

---

## Success Criteria (UAE Structuring QA)
- [ ] Business activity is verified against DED or specific Freezone authority lists.
- [ ] Bank account opening probability is assessed before incorporation.
- [ ] Corporate Tax and VAT timelines are mapped in the incorporation strategy.