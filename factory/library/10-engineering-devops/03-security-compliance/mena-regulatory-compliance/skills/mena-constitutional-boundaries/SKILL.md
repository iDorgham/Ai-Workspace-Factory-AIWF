---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# 🏛️ MENA Constitutional Boundaries

## Purpose
Enforce professional legal standards for operating within the macroeconomic and constitutional frameworks of the Middle East and North Africa (Focus: Egypt & UAE). This skill governs the **Hierarchy of Law**, the **Application of Sharia**, and the **Boundaries of the Civil Code**.

---

## Technique 1 — The Hierarchy of Law

### UAE Legal Hierarchy
1. **The Constitution**: The supreme law of the land.
2. **Federal Laws**: Issued by the Supreme Council (e.g., UAE Civil Code, Commercial Companies Law, Penal Code).
3. **Emirate/Local Laws**: Decrees issued by individual Rulers (e.g., Dubai's specific Real Estate laws).
4. **Sharia (Islamic Law)**: The principal source of legislation.

### Egypt Legal Hierarchy
1. **The Constitution of 2014**: The ultimate framework. Article 2 states that the principles of Islamic Sharia are the principal source of legislation.
2. **Parliamentary Laws**: Enacted by the House of Representatives (e.g., Egyptian Civil Code of 1948).
3. **Presidential/Prime Ministerial Decrees**: Executive regulations implementing the laws.

---

## Technique 2 — The Scope of Sharia Law

- **Commercial Application**: In both Egypt and the UAE, general commercial contracts are governed by the Civil and Commercial Codes rather than direct Sharia rulings (except in Islamic Finance scenarios, tracked in `03-security-compliance/islamic-finance-compliance`).
- **Public Policy (Nizam Al Am)**: A contract term is void if it contradicts "Public Policy" or "Public Morals" (which are heavily influenced by Sharia). For example, charging excessive usury (interest) between private non-banking individuals may be contested.

---

## Technique 3 — Common Law "Pockets" (UAE specific)

- **DIFC (Dubai) & ADGM (Abu Dhabi)**: These are Constitutionally carved-out "Free Zones" that have their own civil and commercial laws based on English Common Law.
- **Boundary Warning**: **Criminal Law** always remains under Federal/Mainland jurisdiction. A financial crime committed inside the DIFC is still prosecuted by the UAE Federal Penal Code, not DIFC courts.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Assuming Federal Supremacy Always** | Void contracts | In the UAE, Emirate-level law can supersede Federal law if the Constitution grants the Emirate specific authority (e.g., onshore oil & gas rights). |
| **Ignoring Public Morals clauses** | Severe Fines/Jail | Media and advertising contracts must strictly adhere to the Constitutional baseline of "Public Morals." |

---

## Success Criteria (Constitutional QA)
- [ ] Contract dispute resolution clauses correctly identify the required legal hierarchy.
- [ ] Risk assessments flag any conflict with Federal/Local "Public Policy."