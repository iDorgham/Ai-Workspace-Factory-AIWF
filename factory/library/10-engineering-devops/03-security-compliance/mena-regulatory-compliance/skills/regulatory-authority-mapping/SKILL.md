---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# 🏛️ Regulatory Authority Mapping

## Purpose
Enforce professional legal standards for identifying and complying with the correct jurisdictional authorities in the UAE and Egypt. This skill ensures that business models (especially Tech, FinTech, and Data) seek licensing and approvals from the correct authoritative node.

---

## Technique 1 — Financial & FinTech Authorities

### United Arab Emirates (UAE)
- **Central Bank of the UAE (CBUAE)**: Governs all onshore banking, payment gateways, and insurance.
- **DFSA (Dubai Financial Services Authority)**: The independent regulator for financial/crypto services operating *inside* the DIFC.
- **FSRA (Financial Services Regulatory Authority)**: The independent regulator for entities inside the ADGM (Abu Dhabi).
- **VARA (Virtual Assets Regulatory Authority)**: The unified authority for Crypto/Web3 licensing in Dubai (excluding DIFC).

### Egypt
- **CBE (Central Bank of Egypt)**: Governs all banking operations and standard payment service providers.
- **FRA (Financial Regulatory Authority)**: Non-banking financial markets (Insurance, Micro-finance, Leasing, Capital Markets).

---

## Technique 2 — Corporate & Foreign Direct Investment (FDI)

### United Arab Emirates (UAE)
- **DED (Department of Economy and Tourism, Dubai)**: Governs all Mainland commercial licenses.
- **MoHRE (Ministry of Human Resources and Emiratisation)**: Governs all private-sector labor relations and Emiritisation quotas.
- **FDI Office / Ministry of Economy**: Regulates specific 100% foreign ownership criteria on the mainland.

### Egypt
- **GAFI (General Authority for Investment and Free Zones)**: The primary gateway for all corporate incorporation and foreign investment incentives.
- **ITIDA (Information Technology Industry Development Agency)**: Promotes and regulates the ICT sector, and acts as the root authority for E-Signatures in Egypt.

---

## Technique 3 — Data Sovereignty & Communications

- **UAE**: **TDRA (Telecommunications and Digital Government Regulatory Authority)** oversees VoIP, telecommunications, and internet governance. Also coordinates with the **UAE Data Office** regarding the Federal Personal Data Protection Law (PDPL).
- **Egypt**: **NTRA (National Telecom Regulatory Authority)** governs telecoms. The Egyptian Data Protection Center (under the Personal Data Protection Law No. 151) governs cross-border data transfer logic.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Applying to DED for Crypto** | Immediate Rejection | Web3/Crypto activities must route through VARA (Dubai) or ADGM (Abu Dhabi). |
| **Bypassing the FRA in Egypt** | Criminal Liability | Operating a FinTech/Micro-finance app without explicit FRA/CBE sandbox approval is illegal. |
| **Ignoring Data Localization** | Fines / Platform Ban | Healthcare and Financial data *cannot* leave the UAE or Egypt without explicit authority exemptions. |

---

## Success Criteria (Authority Mapping QA)
- [ ] The "Regulator Matrix" is checked before any new product launch.
- [ ] FinTech models clearly delineate whether they fall under Central Bank or FRA/DFSA jurisdiction.
- [ ] Data storage architectures comply with the specific national Data Protection Laws.