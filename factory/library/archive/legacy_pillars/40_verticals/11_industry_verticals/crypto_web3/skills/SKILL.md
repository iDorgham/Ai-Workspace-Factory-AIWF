---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# ⛓️ Crypto & Web3 Engineering (MENA Focus)

## Purpose
Enforce professional operational and technical standards for the Crypto and Web3 sectors in the MENA market. This skill focuses on **Smart-Contract Security**, **Tokenomics Modeling**, and **VASP (Virtual Asset Service Provider) Compliance**.

---

## Technique 1 — Smart-Contract Security & Audit Physics

### The "Zero-Vulnerability" Standard
- **Formal Verification**: Utilize formal verification tools to mathematically prove the correctness of contract logic. Focus on "Reentrancy Protection," "Integer Overflow/Underflow" safety, and "Access Control" (e.g., Ownable, Role-based).
- **Multi-Sig Governance**: Enforce the use of multi-signature wallets (e.g., Gnosis Safe) for all admin functions and treasury management. Never utilize a single-key "God Mode" for production contracts.

---

## Technique 2 — Tokenomics & Institutional Modeling

- **Deflationary / Inflationary Loops**: Model token supply mechanics using the `skills:05-data-analytics/market-research` baseline. Ensure that "Vesting Schedules" align with long-term ecosystem health to prevent "Venture Liquidation" dumps on retail investors.
- **Liquidity Depth**: Maintain a minimum 2:1 ratio for liquidity pools before any public launch to prevent extreme price slippage.

---

## Technique 3 — VASP Regulatory Compliance (VARA / ADGM)

- **Regional Licensing**: Ensure all operations comply with the **VARA (Virtual Assets Regulatory Authority)** in Dubai or the **FSRA (Financial Services Regulatory Authority)** in ADGM. 
- **Travel Rule Compliance**: Integrate with providers (e.g., Notabene / CipherTrace) to comply with the FATF "Travel Rule" for all transfers exceeding the defined threshold (e.g., $1,000 USD).

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Unguarded Admin Keys** | Treasury drain | Use 3-of-5 or 5-of-7 multi-sig with keys distributed across geographically separate hardware modules. |
| **Ignoring Gas Physics** | High user friction | Optimize contract logic for gas efficiency (e.g., batching transactions, using `uint256` where appropriate). |
| **Shadow Token Sales** | Legal shutdown | Never conduct token sales in the UAE/KSA region without the explicit "VASP" marketing license. |

---

## Success Criteria (Web3 QA)
- [ ] Smart-contract audit report is verified by an independent firm.
- [ ] Multi-sig governance is active and tested.
- [ ] VARA/FSRA compliance baseline is satisfied for regional operations.
- [ ] Tokenomics model maintains stability under extreme market simulation.