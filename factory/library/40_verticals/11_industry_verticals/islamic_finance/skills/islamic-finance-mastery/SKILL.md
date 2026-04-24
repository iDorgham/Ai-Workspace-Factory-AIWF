---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# 🕋 Islamic Finance Operations (MENA)

## Purpose
Enforce professional operational and technical standards for the Islamic Finance sector in the MENA market. This skill focuses on **Sharia Auditing Architecture**, **Sharia-Compliant Contract Logic**, and **Interest-Free Capital Management**.

---

## Technique 1 — Sharia Auditing & Governance Architecture

### The "Internal Sharia Audit"
- **Internal Sharia Supervision Committee (ISSC)**: Ensure that every financial product is reviewed and approved by an independent ISSC before launch. All fatwas (legal rulings) must be documented and archived for Central Bank (CBUAE/SAMA) audits.
- **Continuous Monitoring**: Perform quarterly Sharia audits to ensure that the actual "Use of Funds" matches the approved Sharia-compliant purpose.

---

## Technique 2 — Sharia-Compliant Contract Logic (The Physics of Trade)

- **Murabaha (Cost-Plus Financing)**: Standardize the logic for buying and re-selling an asset at a transparent profit margin. The bank *must* own the asset before selling it to the client.
- **Musharaka (Partnership Financing)**: Implement Profit-and-Loss sharing (PLS) logic. Ensure that risks are shared proportionally between the bank and the entrepreneur, avoiding guaranteed returns (Riba).

---

## Technique 3 — Compliance & Takaful (Islamic Insurance)

- **Takaful Physics**: Manage the pooling of funds based on "Mutual Assistance" (Tabarru). Ensure that the "Operator Fee" is separate from the "Risk Pool" to prevent conflict of interest.
- **Profit Purification**: Establish a protocol for "Purifying" the income—if any accidental interest is earned during the banking cycle, it must be calculated and donated to charity (Sadaqah) under ISSC supervision.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Guaranteed Returns** | Sharia invalidity | Never use "Fixed Interest" terminology or logic. All returns must be based on "Profit" or "Rental Income." |
| **Pledging Non-Existent Assets** | Void contract | Ensure the asset is physically or constructively possessed at the time of the trade. |
| **Ambiguity (Gharar)** | Dispute risk | Ensure all contract terms, delivery dates, and prices are 100% transparent and quantified. |

---

## Success Criteria (Islamic Finance QA)
- [ ] Product Fatwa is issued and signed by the ISSC.
- [ ] MURABAHA asset ownership is verified before client re-sale.
- [ ] Profit-and-Loss sharing (PLS) logic is active and tested.
- [ ] Quarterly Sharia-compliance reporting is automated and verified.