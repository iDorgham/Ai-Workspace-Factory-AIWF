# Unit Economics Modeling

## Purpose

Build, validate, and stress-test unit economics models for SaaS, marketplace, e-commerce, and service businesses — with exact formulas, cohort analysis patterns, MENA-specific benchmarks, and investor-grade reporting. This skill transforms a 32-line stub into a complete financial intelligence tool.

**Measurable Impact:**
- Before: Back-of-napkin CAC/LTV → investor meetings fail due to lack of rigor
- After: Multi-cohort unit economics model → investor-grade diligence pack ready in 4 hours
- Before: Blended CAC hides underperforming channels → budget wasted on negative-ROI channels
- After: Channel-segmented CAC → identify which channels to scale vs cut
- Token savings: Complete formulas + MENA benchmarks eliminate per-model research (~2,000 tokens)

---

## Technique 1 — Core Metric Formulas

### SaaS Unit Economics

```typescript
// SaaS unit economics calculator
interface SaaSUnitEconomics {
  // Revenue metrics
  mrr: number;                      // Monthly Recurring Revenue
  arr: number;                      // ARR = MRR × 12
  arpu: number;                     // Average Revenue Per User
  arppu: number;                    // Per PAYING user (excl. free tier)
  
  // Customer acquisition
  cac: number;                      // Blended CAC: Total S&M / New Customers
  cacByChannel: Record<string, number>; // CAC broken down by channel
  cacPaybackMonths: number;         // Months to recover CAC
  
  // Retention & lifetime
  monthlyChurnRate: number;         // Lost MRR / Starting MRR (%)
  annualChurnRate: number;          // 1 - (1 - monthlyChurn)^12
  averageLifespanMonths: number;    // 1 / monthlyChurnRate
  ltv: number;                      // ARPU × Gross Margin % × Lifespan
  ltvCacRatio: number;              // LTV / CAC (target: >3)
  
  // Efficiency
  grossMargin: number;              // (Revenue - COGS) / Revenue
  nrr: number;                      // Net Revenue Retention (target: >100%)
  magicNumber: number;              // New MRR / S&M Spend (target: >0.75)
  ruleOf40: number;                 // Revenue Growth % + EBITDA Margin % (target: >40)
  burnMultiple: number;             // Net Burn / Net New ARR (target: <1.5)
}

export function calculateSaaSMetrics(inputs: {
  mrrStart: number;
  mrrEnd: number;     // After same period
  newCustomers: number;
  lostCustomers: number;
  salesMarketingSpend: number;
  cogs: number;       // Cost of Goods Sold (hosting, support, CS)
  expansionMRR: number; // Upgrades from existing customers
  contractionMRR: number; // Downgrades
  churnedMRR: number;
  netBurn: number;
}): SaaSUnitEconomics {
  const arpu = inputs.mrrEnd / (inputs.mrrStart > 0 ? inputs.mrrStart : 1);
  const grossMarginRate = (inputs.mrrEnd - inputs.cogs) / inputs.mrrEnd;
  const monthlyChurn = inputs.churnedMRR / inputs.mrrStart;
  const lifespan = monthlyChurn > 0 ? 1 / monthlyChurn : 36; // Cap at 3y if near 0
  
  const ltv = arpu * grossMarginRate * lifespan;
  const cac = inputs.salesMarketingSpend / Math.max(inputs.newCustomers, 1);
  
  // NRR = (Starting MRR + Expansion - Contraction - Churn) / Starting MRR
  const nrr = (inputs.mrrStart + inputs.expansionMRR - inputs.contractionMRR - inputs.churnedMRR) / inputs.mrrStart;
  
  // Magic Number = New MRR generated per $ of S&M  
  const newMRR = inputs.mrrEnd - inputs.mrrStart + inputs.churnedMRR;
  const magicNumber = (newMRR * 12) / inputs.salesMarketingSpend;
  
  return {
    mrr: inputs.mrrEnd,
    arr: inputs.mrrEnd * 12,
    arpu,
    arppu: arpu, // Same if no free tier; adjust otherwise
    cac,
    cacByChannel: {}, // Caller fills from channel breakdown
    cacPaybackMonths: cac / (arpu * grossMarginRate),
    monthlyChurnRate: monthlyChurn,
    annualChurnRate: 1 - Math.pow(1 - monthlyChurn, 12),
    averageLifespanMonths: lifespan,
    ltv,
    ltvCacRatio: ltv / cac,
    grossMargin: grossMarginRate,
    nrr,
    magicNumber,
    ruleOf40: 0, // Add: growth_rate + ebitda_margin
    burnMultiple: inputs.netBurn / Math.max(newMRR * 12, 1),
  };
}
```

### E-Commerce / Marketplace Unit Economics

```typescript
// E-commerce unit economics (transactional, not subscription)
interface EcommerceUnitEconomics {
  // Order metrics
  aov: number;             // Average Order Value (in local currency)
  grossMarginPerOrder: number; // AOV × gross margin rate
  contributionMarginPerOrder: number; // After variable costs
  
  // Acquisition
  cac: number;             // Total S&M spend / new customers
  cacToAOV: number;        // CAC / AOV (target: <0.5× for first purchase)
  
  // Repeat behavior
  purchaseFrequency: number; // Orders per customer per year
  repeatRate: number;       // % customers who buy again within 12 months
  ltv12m: number;           // 12-month LTV
  ltv24m: number;           // 24-month LTV (most useful for MENA)
  
  // Profitability
  contributionMargin: number; // Revenue - variable costs (excl. fixed)
  breakEvenOrders: number;   // CAC / contribution margin per order
}
```

---

## Technique 2 — Cohort Analysis

### Cohort Retention Table

```markdown
## Monthly Cohort Template

| Cohort | Month 0 | Month 1 | Month 2 | Month 3 | Month 6 | Month 12 |
|--------|---------|---------|---------|---------|---------|----------|
| Jan-26 | 100%    | 78%     | 65%     | 58%     | 48%     | 38%      |
| Feb-26 | 100%    | 81%     | 70%     | 63%     | 52%     | —        |
| Mar-26 | 100%    | 83%     | 72%     | —       | —       | —        |

Reading the table:
- Jan cohort: 38 of every 100 customers still active at month 12 → 62% annual churn
- Improving M1 retention (78% → 83%) indicates better onboarding (Feb/Mar)
- Target: M6 retention > 50% for healthy SaaS; M12 > 35%

## RevRet Cohort (Track MRR, not just headcount)
| Cohort | Month 0 | Month 3 | Month 6 | Month 12 |
|--------|---------|---------|---------|----------|
| Jan-26 | AED 100K | AED 105K | AED 112K | AED 120K |
                     ↑ +5% expansion = NRR > 100% despite some churn

If MRR per cohort GROWS: NRR > 100% → expansion offsets churn (target state)
```

---

## Technique 3 — MENA Unit Economics Benchmarks

### Benchmark Reference by Category

```markdown
## Healthy Unit Economics Benchmarks (MENA SaaS — 2024)

| Metric | Good | Great | Source |
|--------|------|-------|--------|
| LTV:CAC | > 3× | > 5× | Industry |
| CAC Payback | < 18 months | < 12 months | Typical MENA B2B |
| Gross Margin (SaaS) | > 65% | > 80% | Saas Capital |
| Annual Churn | < 15% | < 8% | Industry |
| NRR | > 100% | > 110% | Industry |
| Magic Number | > 0.75 | > 1.0 | Bessemer |
| Rule of 40 | > 40 | > 60 | Industry |
| Burn Multiple | < 2 | < 1 | David Sacks |

## MENA-Specific Context
- CAC typically 30-50% higher than equivalent US market (smaller addressable market)
- Sales cycle: 2-4× longer than US (relationship-based, multilayer approval)
- Churn: Higher risk in SMB segment (business closures, economic volatility)
- Expansion revenue: Lower than US average (less mature upsell culture)
- Payment: Higher mix of annual contracts in GCC (corporate culture)
- Currency risk: EGP devaluation creates pricing complexity for Egypt cohort

## E-Commerce MENA Benchmarks
| Metric | Good | Great |
|--------|------|-------|
| M12 Repeat Rate | > 30% | > 45% |
| CAC : AOV | < 0.5× | < 0.3× |
| Return Rate | < 12% | < 8% |
| Cart Abandonment | < 65% | < 50% |
| NPS | > 40 | > 60 |
```

---

## Technique 4 — Stress Testing & Scenario Analysis

### Sensitivity Analysis Template

```markdown
## Three-Scenario Model

### BASE CASE (Most likely)
  CAC: AED 800 | Monthly Churn: 2% | ARPU: AED 499 | Gross Margin: 72%
  → LTV: AED 17,964 | LTV:CAC: 22.5× | Payback: 2.2 months | PASS ✅

### BEAR CASE (Pessimistic — test unit economics robustness)
  CAC: AED 1,500 (+88%) | Monthly Churn: 4% | ARPU: AED 399 (-20%) | GM: 65%
  → LTV: AED 6,468 | LTV:CAC: 4.3× | Payback: 5.8 months
  → Still PASS ✅ but payback creeping up — watch churn carefully

### BULL CASE (Optimistic — size the prize)
  CAC: AED 600 (-25%) | Monthly Churn: 1% | ARPU: AED 599 (+20%) | GM: 78%
  → LTV: AED 46,722 | LTV:CAC: 77.9× | Payback: 1.3 months | PASS ✅

## Key Sensitivities (What breaks the model first?)
1. Churn rate has the HIGHEST leverage: 1% → 4% = LTV drops 73%
2. ARPU second: -20% ARPU = LTV drops 20% (linear)
3. CAC third: +88% CAC is survivable if LTV is strong

## Breakeven Analysis
  Question: At what monthly churn rate does LTV:CAC = 1 (breakeven)?
  Formula: LTV = ARPU × GM × (1/churn) = CAC
  → Breakeven churn = ARPU × GM / CAC
  → Example: (499 × 0.72) / 800 = 44.9% monthly churn
  → We'd need 45%/month churn (extreme) to lose money per customer
```

---

## Anti-Pattern Catalog

| ID | Anti-Pattern | Risk | Fix |
|----|-------------|------|-----|
| UE-001 | Using blended CAC (ignores channel) | **HIGH** — Hides which channels are unprofitable | Break CAC by channel: paid, organic, referral, events |
| UE-002 | Using revenue instead of gross margin in LTV | **CRITICAL** — 40-80% overstates LTV | LTV = ARPU × **gross margin** × lifespan |
| UE-003 | Ignoring cohort retention (using averages) | **HIGH** — New user churn masked by large base | Build full cohort table — averages lie |
| UE-004 | No scenario analysis before fundraising | **HIGH** — Investor questions kill momentum | Prepare base/bear/bull case with sensitivity table |
| UE-005 | Optimistic lifespan assumptions | **HIGH** — Inflated LTV: CAC looks good until it doesn't | Cap lifespan assumption at current data; max 36 months |
| UE-006 | Confusing NRR with gross retention | **MEDIUM** — Different signal, different actions | Gross retention = headcount kept; NRR includes expansion |
| UE-007 | Not tracking payback by cohort | **MEDIUM** — Can't tell if sales efficiency improving | Monthly cohort payback; look for shortening trend |

## 🌍 Regional Calibration (MENA Context)

- **Cultural Alignment:** Ensure all logic respects regional business etiquette and MENA market expectations.
- **RTL Compliance:** Logic must explicitly handle Right-to-Left (RTL) flow where relevant.

## 🛡️ Critical Failure Modes (Anti-Patterns)

- **Anti-Pattern:** Generic Output -> *Correction:* Apply sector-specific professional rules from RULE.md.
- **Anti-Pattern:** Global-Only Logic -> *Correction:* Verify against MENA regional calibration.

---

## Success Criteria

- [ ] CAC calculated per channel (not blended) with channel attribution
- [ ] LTV uses gross margin × ARPU × lifespan formula (not revenue)
- [ ] Monthly cohort retention table built (minimum 3 months of cohorts)
- [ ] NRR calculated separately from gross retention
- [ ] Three-scenario model (base/bear/bull) documented
- [ ] MENA benchmarks consulted for LTV:CAC, payback, churn targets
- [ ] Sensitivity analysis identifies #1 driver of LTV (usually churn)
- [ ] Model updated monthly from actual billing/CRM data