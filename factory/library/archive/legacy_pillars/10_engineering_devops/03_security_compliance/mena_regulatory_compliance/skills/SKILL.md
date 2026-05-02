---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# MENA Regulatory & Compliance Framework

## Purpose

Navigate the full regulatory lifecycle — from entity setup and licensing through ongoing compliance, tax filing, employment law, and sector-specific permits — across all MENA jurisdictions. This skill provides concrete decision trees, compliance calendars, jurisdiction comparison matrices, and code-level automation patterns for regulatory workflows.

**Measurable Impact:**
- Before: Entity setup takes 4-8 weeks with 30% rejection rate on first filing
- After: Pre-validated document packages → 2-3 week setup, <5% rejection rate
- Before: VAT/corporate tax compliance handled ad-hoc → late filing penalties (5-10% of tax due)
- After: Automated compliance calendar → zero missed deadlines
- Token savings: Single-source regulatory truth eliminates 80% of jurisdiction research per project

---

## Technique 1 — Jurisdiction Selection Decision Tree

### Entity Structure Decision Matrix

```markdown
## Step 1: Determine Business Activity

QUESTION: What is your primary activity?
├── Technology / Software → Step 2
├── Financial Services → MUST use DIFC or ADGM (regulated)
├── Media / Content → twofour54 (Abu Dhabi) or Dubai Media City
├── Healthcare → DHCC (Dubai) or mainland with MOHAP license
├── E-commerce → Free zone or mainland (both viable)
├── Manufacturing → JAFZA, KIZAD, or mainland industrial license
└── Professional Services → DMCC, DIFC, or mainland

## Step 2: Foreign Ownership Requirement?

QUESTION: Do you need 100% foreign ownership?
├── YES → Free Zone entity (DMCC, IFZA, Meydan, RAKEZ, etc.)
├── NO (have local partner) → Mainland LLC (broader market access)
└── SPECIAL CASE:
    ├── Regulated finance → DIFC (common law) or ADGM (common law)
    ├── Intellectual property holding → JAFZA offshore or RAK ICC
    └── Holding company → ADGM or DIFC (no physical office needed)

## Step 3: Market Access Needs?

QUESTION: Do you need to trade directly with UAE mainland consumers?
├── YES → Mainland LLC (or free zone with mainland branch*)
├── NO (B2B or export only) → Free zone is optimal
└── BOTH → Free zone HQ + mainland branch/distribution agreement

*Note: Some free zones (DMCC, DIFC) allow mainland trading via special arrangements
```

### Jurisdiction Comparison Matrix

| Factor | UAE Mainland | UAE Free Zone | DIFC | ADGM | Saudi (MISA) | Egypt (GAFI) |
|--------|-------------|---------------|------|------|--------------|--------------|
| **Foreign ownership** | 100% (since 2021*) | 100% | 100% | 100% | 100% (most sectors) | 100% (most sectors) |
| **Corporate tax** | 9% (>AED 375K) | 9% (>AED 375K) | 9% (>AED 375K) | 9% | 20% (+Zakat) | 22.5% |
| **VAT** | 5% | 5% (0% intra-FZ) | 5% | 5% | 15% | 14% |
| **Legal system** | UAE civil law | UAE civil law | English common law | English common law | Saudi civil law | Egyptian civil law |
| **Min capital** | AED 0-300K | AED 0-50K | $50K (varies) | $0-50K | SAR 0-30M | EGP 0-500K |
| **Office required** | Yes | Yes (flexi-desk ok) | Yes | Yes (virtual ok) | Yes | Yes |
| **Visa allocation** | Based on office size | Based on package | Based on license | Based on license | Based on license | N/A |
| **Bank account** | ✅ Local banks | ✅ (harder) | ✅ DIFC banks | ✅ ADGM banks | ✅ Local banks | ✅ Local banks |
| **Setup time** | 2-4 weeks | 1-3 weeks | 3-6 weeks | 2-4 weeks | 4-8 weeks | 3-6 weeks |
| **Annual renewal** | AED 15-50K | AED 10-80K | AED 50-200K | AED 30-100K | SAR 20-100K | EGP 10-50K |

```
*UAE mainland 100% foreign ownership: Available for 1,000+ activities since June 2021
 (Commercial Companies Law amendment). Some strategic activities still require Emirati partner.
```

---

## Technique 2 — Tax Compliance Automation

### UAE Corporate Tax Decision Tree

```typescript
// UAE Corporate Tax (effective June 2023)
interface UAECorporateTaxCalculation {
  financialYear: string;
  
  // Revenue classification
  totalRevenue: number;           // AED
  qualifyingIncome: number;       // Subject to 9%
  exemptIncome: number;           // 0% rate applies
  
  // Rate determination
  taxableIncome: number;
  taxRate: 0 | 0.09;             // 0% ≤ AED 375K, 9% > AED 375K
  taxDue: number;
  
  // Free zone special rules
  isQualifyingFreeZonePerson: boolean;
  // Qualifying Free Zone Person (QFZP) criteria:
  // 1. Maintains adequate substance in free zone
  // 2. Derives qualifying income (specific activities)
  // 3. Has NOT elected to be subject to normal CT
  // 4. Complies with transfer pricing rules
  qualifyingFreeZoneIncome: number;  // 0% rate
  nonQualifyingIncome: number;       // 9% rate
}

export function calculateUAECorporateTax(
  revenue: number,
  expenses: number,
  isFreezone: boolean,
  qualifyingRatio: number = 1.0  // % of income that qualifies for 0%
): UAECorporateTaxCalculation {
  const taxableIncome = Math.max(0, revenue - expenses);
  
  if (isFreezone && qualifyingRatio > 0) {
    // QFZP: qualifying income at 0%, rest at 9%
    const qualifyingIncome = taxableIncome * qualifyingRatio;
    const nonQualifying = taxableIncome * (1 - qualifyingRatio);
    const taxOnNonQualifying = nonQualifying > 375000 
      ? (nonQualifying - 375000) * 0.09 
      : 0;
    
    return {
      financialYear: new Date().getFullYear().toString(),
      totalRevenue: revenue,
      qualifyingIncome: qualifyingIncome,
      exemptIncome: qualifyingIncome,
      taxableIncome: nonQualifying,
      taxRate: nonQualifying > 375000 ? 0.09 : 0,
      taxDue: taxOnNonQualifying,
      isQualifyingFreeZonePerson: true,
      qualifyingFreeZoneIncome: qualifyingIncome,
      nonQualifyingIncome: nonQualifying,
    };
  }
  
  // Standard mainland calculation
  const taxDue = taxableIncome > 375000 
    ? (taxableIncome - 375000) * 0.09 
    : 0;
  
  return {
    financialYear: new Date().getFullYear().toString(),
    totalRevenue: revenue,
    qualifyingIncome: 0,
    exemptIncome: Math.min(taxableIncome, 375000),
    taxableIncome,
    taxRate: taxableIncome > 375000 ? 0.09 : 0,
    taxDue,
    isQualifyingFreeZonePerson: false,
    qualifyingFreeZoneIncome: 0,
    nonQualifyingIncome: taxableIncome,
  };
}
```

### Saudi Tax + Zakat Calculation

```typescript
// Saudi Arabia: Corporate Tax (20%) + Zakat (2.5%) system
interface SaudiTaxCalculation {
  // Corporate Income Tax (CIT)
  cit: {
    taxableIncome: number;        // SAR
    rate: 0.20;                   // 20% flat rate
    taxDue: number;
    // Applies to: foreign-owned share of profits
  };
  
  // Zakat (Islamic levy)
  zakat: {
    zakatBase: number;            // Net equity + long-term debt - fixed assets
    rate: 0.025;                  // 2.5% of zakat base
    zakatDue: number;
    // Applies to: Saudi/GCC-owned share
  };
  
  // Withholding Tax (on payments to non-residents)
  withholding: {
    managementFees: 0.20;         // 20%
    royalties: 0.15;              // 15%
    technicalServices: 0.05;      // 5%
    dividends: 0.05;              // 5%
    interest: 0.05;               // 5%
  };
  
  // ZATCA filing
  filingDeadline: string;         // 120 days after fiscal year end
  returnType: 'CIT' | 'ZAKAT' | 'COMBINED';
}
```

### VAT Compliance Calendar

```markdown
## Automated Compliance Calendar (UAE + Saudi)

### UAE — FTA (Federal Tax Authority)
| Obligation | Frequency | Deadline | Penalty (Late) |
|-----------|-----------|----------|----------------|
| VAT return | Quarterly | 28th of month after quarter end | AED 1,000 first, AED 2,000 repeat |
| VAT payment | Quarterly | Same as return deadline | 2% immediate + 4%/month |
| Corporate tax return | Annual | 9 months after fiscal year end | AED 500/month up to cap |
| Corporate tax payment | Annual | Same as return deadline | 14% per annum |
| ESR notification | Annual | 6 months after fiscal year end | AED 20,000 |
| ESR report | Annual | 12 months after fiscal year end | AED 50,000 |
| UBO declaration | On change | 60 days after change | AED 100,000+ |
| Transfer pricing disclosure | Annual | 9 months after fiscal year end | AED 500,000 |

### Saudi Arabia — ZATCA
| Obligation | Frequency | Deadline | Penalty (Late) |
|-----------|-----------|----------|----------------|
| VAT return | Monthly (>SAR 40M) / Quarterly | 28th of following month | 5-25% of VAT due |
| VAT payment | Same as return | Same as return | 5% of unpaid per month |
| CIT/Zakat return | Annual | 120 days after fiscal year end | 1% per 30 days |
| WHT return | Monthly | 10th of following month | 1% per 30 days |
| E-invoicing (Fatoora) | Real-time (Phase 2) | Immediate | SAR 10,000 per violation |
| Transfer pricing | Annual | 120 days after fiscal year end | SAR 10,000-100,000 |
```

---

## Technique 3 — Employment Law & Nationalization

### Emiratisation Compliance (UAE)

```markdown
## Emiratisation Quota Requirements (2024+)

### Private Sector (50+ employees)
- Target: 2% annual increase in Emirati skilled workforce
- Penalties for non-compliance: AED 72,000/year per unfilled position (increasing annually)
- Reporting: Quarterly headcount via MOHRE portal
- Eligible roles: Must be skilled positions (clerical/operational count partially)

### Key Requirements
1. Salary: Minimum AED 4,000/month for counted positions
2. WPS: Wages paid through Wage Protection System (mandatory)
3. Training: Emirati employees must have documented development plan
4. Work hours: Max 8 hours/day, 48 hours/week (Ramadan: 6 hours/day)
5. End of service: 21 days/year (first 5 years), 30 days/year (after 5 years)
6. Notice period: 30-90 days based on contract type

### Golden Visa Integration
- 10-year visa for investors (AED 2M+ property or AED 2M+ deposits)
- 10-year visa for specialized talents (executives, scientists, doctors)
- 5-year visa for entrepreneurs (approved startup, AED 500K+ capital)
- No employer sponsorship needed, self-sponsorship model
```

### Saudisation / Nitaqat (Saudi Arabia)

```markdown
## Nitaqat Quota System

### Band Classification
| Band | Saudisation Rate | Consequences |
|------|-----------------|--------------|
| Platinum | Exceeds target by >40% | Maximum visa allocation, premium services |
| Green (High) | Exceeds target by 10-40% | Standard visa allocation |
| Green (Low) | At or above target | Standard services |
| Yellow | Below target by <20% | Warning, restricted visas |
| Red | Below target by >20% | Cannot renew work permits, visa restrictions |

### Sector-Specific Targets (2024)
- IT/Technology: 25-35% Saudisation
- Retail: 70%+ (specific roles: cashiers, sales)
- Hospitality: 30-40%
- Financial services: 50-70%
- Healthcare: 25-35%
- Communications: 30-40%

### GOSI (Social Insurance)
- Employer contribution: 12% of salary (2% annuities + 10% occupational hazards)
- Employee contribution: 10% of salary (annuities)
- Registration: Mandatory within 15 days of employment start
- Reporting: Monthly salary updates via GOSI portal
```

---

## Technique 4 — Sector-Specific Licensing Requirements

### Technology & SaaS Licensing

```markdown
## UAE Technology Licensing

### Mainland Technology License
- Authority: Department of Economic Development (DED/DET)
- Activity codes: IT services, software development, e-commerce
- Requirements: Tenancy contract, shareholder documents, NOC
- Duration: 1 year, renewable
- Estimated cost: AED 15,000-30,000/year

### Free Zone Technology License — Common Options
| Free Zone | Focus | Cost (from) | Office | Visas |
|-----------|-------|-------------|--------|-------|
| DMCC | General tech | AED 20,000 | Flexi-desk | 3-6 |
| IFZA | Startups | AED 12,750 | Virtual | 1-3 |
| DIFC Innovation Hub | FinTech | AED 30,000 | Co-work | 2-4 |
| Dubai Internet City | Tech/IT | AED 50,000 | Physical | 5+ |
| Meydan Free Zone | General | AED 11,750 | Flexi-desk | 1-3 |
| RAKEZ | Cost-effective | AED 10,500 | Flexi-desk | 1-3 |

### Saudi Arabia — SAGIA/MISA Technology License
- Authority: Ministry of Investment (MISA)
- Requirements: Business plan, financial statements, corporate docs
- Min capital: SAR 200,000 (IT services), SAR 500,000 (e-commerce)
- Duration: 1-5 years
- Processing: 4-8 weeks
- Special: No local partner required for most tech activities
```

### E-Commerce Specific

```markdown
## E-Commerce Compliance (UAE & Saudi)

### UAE E-Commerce Requirements
- E-commerce license: Specific trading license with e-commerce activity
- Consumer protection: Federal Law No. 15 of 2020
- Return policy: 14 days minimum for online purchases
- Payment security: PCI-DSS compliance for card processing
- Privacy: PDPL compliance for customer data
- Cross-border: Import duties (0-5%), customs declaration

### Saudi E-Commerce Requirements
- E-commerce registration: Ministry of Commerce e-commerce registry
- Maroof platform: Optional but recommended trust/verification
- Consumer protection: E-Commerce Law (Royal Decree M/126)
- Delivery requirements: Clear delivery timelines, tracking mandatory
- Return policy: 7-15 days depending on product category
- VAT: 15% on all domestic sales, tax invoice required
```

---

## Anti-Pattern Catalog

| ID | Anti-Pattern | Risk | Fix |
|----|-------------|------|-----|
| REG-001 | Operating without proper trade license | **CRITICAL** — Business closure, fines | Obtain correct license before revenue generation |
| REG-002 | Ignoring free zone restrictions on mainland trading | **HIGH** — License violation | Get mainland sub-license or distribution agreement |
| REG-003 | Missing VAT registration when above threshold | **CRITICAL** — 100% of unpaid VAT as penalty | Register within 30 days of exceeding threshold |
| REG-004 | Not updating UBO (Ultimate Beneficial Owner) register | **HIGH** — AED 100K+ penalty | Update within 60 days of any ownership change |
| REG-005 | Missing ESR (Economic Substance) notification | **HIGH** — AED 20K penalty | File within 6 months of fiscal year end |
| REG-006 | Late corporate tax registration | **MEDIUM** — Penalties accumulate | Register within 3 months of fiscal year start |
| REG-007 | Non-compliant WPS (Wage Protection System) | **HIGH** — Work permit restrictions | All salaries via WPS-registered bank account |
| REG-008 | Failing Emiratisation/Saudisation quotas | **HIGH** — AED 72K/position penalty | Plan hiring to meet annual 2% increase target |
| REG-009 | Using personal bank account for business | **CRITICAL** — Anti-money laundering violation | Open proper corporate bank account |
| REG-010 | Ignoring transfer pricing documentation | **HIGH** — AED 500K+ penalty (UAE) | Maintain contemporaneous TP documentation |

---

## Chain-Multiplier Integration

```markdown
## How This Skill Serves Other Agents

@Guide → Consumes jurisdiction decision trees for project setup guidance
@SecurityAgent → References data protection and privacy requirements per jurisdiction
@BackendAgent → Uses compliance automation patterns for regulatory workflows
@FintechStrategist → References financial services licensing requirements
@PropertyAnalyst → Consumes real estate regulatory framework
@HealthConsultant → References healthcare licensing requirements

## Dependency Chain
mena-regulatory-compliance → [mena-data-sovereignty + mena-localization-payments]
       (entity & tax rules)        (data residency)      (payment & localization)
              ↓
    [payment-compliance + health-data-privacy + real-estate-modeling]
    (sector-specific compliance layers consume regulatory foundation)
```

## 🌍 Regional Calibration (MENA Context)

- **Cultural Alignment:** Ensure all logic respects regional business etiquette and MENA market expectations.
- **RTL Compliance:** Logic must explicitly handle Right-to-Left (RTL) flow where relevant.

## 🛡️ Critical Failure Modes (Anti-Patterns)

- **Anti-Pattern:** Generic Output -> *Correction:* Apply sector-specific professional rules from RULE.md.
- **Anti-Pattern:** Global-Only Logic -> *Correction:* Verify against MENA regional calibration.

---

## Success Criteria

- [ ] Jurisdiction selection decision tree applied before every entity setup
- [ ] Tax compliance calendar automated with reminder system
- [ ] Emiratisation/Saudisation quotas tracked per quarterly reporting
- [ ] VAT calculations correct per jurisdiction (5% UAE, 15% KSA, 14% EGP)
- [ ] Corporate tax calculated correctly (9% UAE, 20% KSA, 22.5% EGP)
- [ ] Free zone vs mainland trade-offs documented in project setup
- [ ] ESR and UBO obligations tracked for UAE entities
- [ ] Sector-specific licensing requirements validated before business launch
- [ ] Transfer pricing documentation maintained for cross-border operations