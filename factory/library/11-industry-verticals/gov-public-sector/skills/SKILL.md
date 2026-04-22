# 🏛️ Gov & Public Sector Operations (MENA)

## Purpose
Enforce professional operational and technical standards for Government and Public Sector entities in the MENA market. This skill focuses on **Citizen-Experience (CX) Design**, **Digital Governance Security**, and **Inclusive Accessibility Standards**.

---

## Technique 1 — Citizen-Experience (CX) & Service Design

### The "Paperless" Mandate
- **Unified Identity**: Integrate with national identity providers (UAE Pass, Egypt ID) to eliminate redundant "Login/Profile" creation. A citizen should be authenticated once for all inter-departmental services.
- **Service Orchestration**: Map the "Life Event" journey (e.g., getting married, starting a business) rather than individual siloed services. Ensure that one application triggers all necessary backend government approvals.

---

## Technique 2 — Digital Governance & Sovereign Security

- **Sovereign Cloud Protocol**: All government data MUST reside on national sovereign cloud infrastructure (e.g., UAE G42/Moro Hub, Egypt Data Center nodes). Zero dependency on non-regional private cloud for critical PII.
- **Zero-Trust for Public Nodes**: Implement Zero-Trust architecture for all public-facing API endpoints. Every request must be verified for identity, device health, and authoritative privilege.

---

## Technique 3 — Inclusive Accessibility & RTL Physics

- **Language Supremacy**: In MENA Government portals, Arabic is the primary language. All UI/UX must be designed with "RTL-First" (Right-to-Left) physics, ensuring that progress bars, icons, and menus align correctly with Arabic reading patterns.
- **W3C Accessibility**: Enforce WCAG 2.1 Level AA standards. Use high-contrast color palettes and screen-reader compatibility to ensure services are accessible to people of determination (POD).

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **English-First Design** | Poor citizen adoption | Start all wireframes in Arabic. Mirroring an English UI to Arabic often breaks spacing and trust. |
| **Siloed Databases** | "Visit the office" loops | Ensure API-first connectivity between departments (e.g., Municipalities connecting to Housing authorities). |
| **Slow Mobile Response** | Low accessibility | Optimize all gov-portals for low-bandwidth mobile devices (Lighthouse score > 90 for performance). |

---

## Success Criteria (Gov QA)
- [ ] National Identity (UAE Pass/Egypt ID) integration is verified.
- [ ] RTL layout physics are correct and tested across all viewports.
- [ ] WCAG 2.1 compliance score is AA or higher.
- [ ] Data residency is confirmed as On-Shore Sovereign Cloud.