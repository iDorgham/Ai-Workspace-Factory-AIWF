---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# 🏛️ Business Incorporation (Egypt)

## Purpose
Enforce professional legal standards for structuring businesses within the Arab Republic of Egypt. This skill governs the logic of navigating **GAFI (General Authority for Investment and Free Zones)**, parsing **Company Law No. 159 & Investment Law No. 72**, and managing foreign ownership constraints.

---

## Technique 1 — GAFI Frameworks & Corporate Structures

### LLC (Limited Liability Company - ذات مسئولية محدودة)
- **Use Case**: The standard vehicle for foreign investors (FDI) and local SMEs.
- **Ownership**: Can be 100% foreign-owned in most sectors. Requires a minimum of two quota-holders (shareholders) and at least one manager (who may be a foreigner).
- **Capital**: Zero minimum capital required by law for an LLC, though specific banking thresholds apply.

### JSC (Joint Stock Company - مساهمة)
- **Use Case**: Large-scale projects, FinTech, and companies planning to go public/issue bonds.
- **Capital Constraint**: Minimum issued capital of EGP 250,000, with 10% paid upon incorporation, 25% within 3 months, and the remainder within 5 years.

---

## Technique 2 — Investment Law No. 72 Incentives

- **Targeted Sectors**: Utilizing Investment Law No. 72 of 2017 provides tax deductions (up to 50% of the investment cost offset against taxable profits) for companies operating in "Sector A" (Suez Canal Economic Zone, Upper Egypt) or specifically promoted industries (Green Energy, Tech).
- **Free Zones**: Egyptian Free Zones (e.g., Media Production City, Public Free Zones) offer lifetime exemption from corporate tax, VAT, and customs, provided the output is exported.

---

## Technique 3 — Foreign Labor Quotas (Wafid Logic)

- **The 10% Rule**: Egyptian Labor Law mandates that foreign workers cannot exceed 10% of the total workforce of a company, and their salaries cannot exceed 20% of the total payroll.
- **Exemptions**: Investment Law companies can apply for exemptions to increase the quota to 20% (and exceptionally higher) if specialized technical expertise is unavailable locally.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Ignoring the Commercial Register** | Frozen operations | A company does not legally exist until its Commercial Registration (Sagel Togary) and Tax ID (Bataqa Darebeya) are issued. |
| **Import/Export Misalignment** | Customs blockage | 100% foreign-owned companies CANNOT hold a standard Import/Export license for trading purposes (manufacturing/capital goods excepted); they require a 51% Egyptian partner. |
| **Shahr El Aqari Friction** | Invalidated leases | All corporate headquarters lease agreements must be notarized at the Real Estate Registration Office (Shahr El Aqari) to complete tax registration. |

---

## Success Criteria (Egypt Structuring QA)
- [ ] Sector is vetted against the "Negative List" (activities restricted to Egyptians, e.g., Sinai real estate, certain import licenses).
- [ ] GAFI incorporation pathway (Law 159 vs Law 72) is strategically selected.
- [ ] Foreign labor quota requirements are modeled in the business plan.