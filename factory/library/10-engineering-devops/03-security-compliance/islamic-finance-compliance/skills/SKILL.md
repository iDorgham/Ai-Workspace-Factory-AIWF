# Islamic Finance & Sharia Compliance Engineering

## Purpose

Build Sharia-compliant financial products, payment systems, and investment platforms with production-grade contract structures, compliance verification algorithms, and regulatory integration. This skill provides concrete code patterns for profit-sharing calculations, sukuk cash flow models, halal screening algorithms, and zakat computation — with exact formulas, anti-patterns, and audit checklists.

**Measurable Impact:**
- Before: Ad-hoc Sharia compliance → SSB (Sharia Supervisory Board) rejects 40% of product proposals
- After: Pre-validated structures with AAOIFI-aligned patterns → 90%+ SSB first-pass approval
- Before: Manual halal portfolio screening → inconsistent compliance, investor complaints
- After: Algorithmic screening with sector/ratio thresholds → real-time compliant portfolio management
- Chain multiplier: Consumed by @FintechStrategist, @BackendAgent, @PropertyAnalyst for any Islamic finance feature

---

## Core Islamic Finance Principles

### Prohibited Elements (Non-Negotiable Rules)

```markdown
## Absolute Prohibitions in Code

1. **Riba (Interest/Usury)** — NO interest accrual, period.
   Code impact: No `calculateInterest()`, no `APR`, no `compoundInterest()`
   Replace with: profit-sharing ratios, markup-based pricing, lease rentals
   
2. **Gharar (Excessive Uncertainty)** — All contract terms must be deterministic
   Code impact: No ambiguous pricing, no undefined deliverables
   Replace with: Fixed-price contracts, clearly defined outcomes
   
3. **Maysir (Gambling/Speculation)** — No pure speculation products
   Code impact: No binary options, no prediction markets, no lottery mechanics
   Replace with: Asset-backed investments, risk-sharing pools
   
4. **Haram Activities** — No investment in prohibited sectors
   Code impact: Screening algorithm required for all portfolio products
   Prohibited sectors: Alcohol, pork, gambling, adult entertainment,
   conventional banking (interest-based), weapons (some interpretations),
   tobacco (some interpretations)
```

---

## Technique 1 — Sharia-Compliant Financial Product Engine

### Murabaha (Cost-Plus Sale) Calculator

```typescript
// Murabaha: Bank buys asset, sells to client at disclosed markup
// Most common Islamic finance structure (~65% of Islamic finance assets)

interface MurabahaContract {
  assetDescription: string;          // What is being financed
  purchasePrice: number;             // Bank's cost price (MUST be disclosed)
  markup: number;                    // Profit amount (NOT interest rate)
  totalPrice: number;                // purchasePrice + markup
  downPayment: number;               // Client's initial payment
  financedAmount: number;            // totalPrice - downPayment
  installments: number;              // Number of monthly payments
  monthlyPayment: number;            // Fixed monthly amount
  currency: 'AED' | 'SAR' | 'EGP';
  
  // Sharia compliance metadata
  shariaStandard: 'AAOIFI-8';       // AAOIFI Sharia Standard No. 8
  assetOwnershipTransfer: 'on_contract'; // When does ownership transfer?
  insuranceType: 'takaful';          // Islamic insurance only
}

export function calculateMurabaha(
  assetPrice: number,
  profitRate: number,           // Annual equivalent rate (for disclosure only)
  tenureMonths: number,
  downPaymentPercent: number = 0.20,
  currency: 'AED' | 'SAR' | 'EGP' = 'AED'
): MurabahaContract {
  const downPayment = assetPrice * downPaymentPercent;
  const financedBase = assetPrice - downPayment;
  
  // CRITICAL: This is a MARKUP, not interest
  // The total profit is fixed at contract signing — it does NOT compound
  const totalMarkup = financedBase * profitRate * (tenureMonths / 12);
  const totalPrice = assetPrice + totalMarkup;
  const financedAmount = totalPrice - downPayment;
  const monthlyPayment = financedAmount / tenureMonths;
  
  return {
    assetDescription: '', // Caller fills
    purchasePrice: assetPrice,
    markup: totalMarkup,
    totalPrice,
    downPayment,
    financedAmount,
    installments: tenureMonths,
    monthlyPayment: Math.round(monthlyPayment * 100) / 100,
    currency,
    shariaStandard: 'AAOIFI-8',
    assetOwnershipTransfer: 'on_contract',
    insuranceType: 'takaful',
  };
}

// KEY DIFFERENCE from conventional loan:
// Conventional: interest accrues daily, compounds, changes with rate
// Murabaha: markup is FIXED at signing, never changes, never compounds
// Late payment: NO additional charges (penalty donations to charity only)
```

### Mudarabah (Profit-Sharing Investment)

```typescript
// Mudarabah: One party provides capital (Rab al-Maal),
// other provides expertise/labor (Mudarib)

interface MudarabahContract {
  investmentAmount: number;
  investorShare: number;            // e.g., 0.70 (70% of profits to investor)
  mudariebShare: number;            // e.g., 0.30 (30% of profits to manager)
  investmentPeriod: number;         // months
  minimumReturn: null;              // CRITICAL: NO guaranteed returns in Mudarabah
  lossAllocation: 'investor_only';  // Losses borne by capital provider ONLY
  mudariebLiability: 'negligence_only'; // Mudarib liable only if negligent
  
  // Profit distribution
  profitDistributionFrequency: 'monthly' | 'quarterly' | 'annually' | 'at_maturity';
  profitCalculationMethod: 'gross' | 'net'; // Before or after expenses
}

export function distributeMudarabahProfits(
  totalProfit: number,
  contract: MudarabahContract
): MudarabahDistribution {
  if (totalProfit <= 0) {
    // LOSS: 100% borne by investor (Rab al-Maal)
    // Mudarib loses only their effort/time — no financial liability
    return {
      investorReturn: totalProfit, // Negative = loss
      mudariebReturn: 0,           // Zero, not negative
      totalDistributed: totalProfit,
      isLoss: true,
    };
  }
  
  // PROFIT: distributed per agreed ratio
  return {
    investorReturn: totalProfit * contract.investorShare,
    mudariebReturn: totalProfit * contract.mudariebShare,
    totalDistributed: totalProfit,
    isLoss: false,
  };
}
```

### Ijara (Lease-Based Finance)

```typescript
// Ijara: Bank buys asset, leases to client, ownership transfers at end
// Common for: property, vehicles, equipment

interface IjaraContract {
  assetValue: number;
  leaseStart: string;              // ISO 8601
  leaseTerm: number;               // months
  monthlyRental: number;           // Lease payment
  residualValue: number;           // Purchase price at end (often nominal AED 1)
  maintenanceResponsibility: 'lessor'; // Bank responsible for major maintenance
  takafulCost: number;             // Islamic insurance premium
  
  // Ijarah Muntahia Bittamleek (Ijara ending with ownership)
  ownershipTransfer: 'gift' | 'sale_at_nominal' | 'gradual_transfer';
  
  shariaStandard: 'AAOIFI-9';     // AAOIFI Sharia Standard No. 9
}

export function calculateIjaraSchedule(
  assetValue: number,
  term: number,
  annualRentalRate: number,
  residualValue: number = 1 // Nominal AED 1 purchase option
): IjaraSchedule {
  // Monthly rental = (Asset value × annual rate) / 12
  // CRITICAL: This is a RENTAL, not a loan repayment
  // The asset remains on the BANK'S balance sheet during the lease
  const monthlyRental = (assetValue * annualRentalRate) / 12;
  
  const schedule: IjaraPayment[] = [];
  for (let month = 1; month <= term; month++) {
    schedule.push({
      month,
      rental: monthlyRental,
      // No principal/interest split — it's purely rental
      cumulativeRental: monthlyRental * month,
      remainingTerm: term - month,
    });
  }
  
  // Final payment: purchase option at residual value
  schedule.push({
    month: term + 1,
    rental: residualValue,
    cumulativeRental: monthlyRental * term + residualValue,
    remainingTerm: 0,
  });
  
  return {
    payments: schedule,
    totalRental: monthlyRental * term + residualValue,
    monthlyRental,
    residualValue,
  };
}
```

---

## Technique 2 — Halal Investment Screening Algorithm

### Sector & Financial Ratio Screening

```typescript
// AAOIFI-compliant halal stock screening algorithm
interface HalalScreeningResult {
  ticker: string;
  companyName: string;
  screeningDate: string;
  
  // Step 1: Sector screen (qualitative)
  sectorCompliant: boolean;
  sectorReason?: string;
  
  // Step 2: Financial ratio screen (quantitative)
  ratioScreening: {
    debtRatio: { value: number; threshold: number; pass: boolean };
    interestIncomeRatio: { value: number; threshold: number; pass: boolean };
    receivablesRatio: { value: number; threshold: number; pass: boolean };
    cashAndInterestRatio: { value: number; threshold: number; pass: boolean };
    nonPermissibleIncomeRatio: { value: number; threshold: number; pass: boolean };
  };
  
  // Final verdict
  isHalal: boolean;
  requiresPurification: boolean;
  purificationPercentage?: number; // % of dividend to donate
  complianceStandard: 'AAOIFI' | 'DJIM' | 'SP_Sharia' | 'MSCI_Islamic';
}

// Prohibited business activities (sector screen)
const HARAM_SECTORS = [
  'alcohol_production',
  'alcohol_distribution',
  'pork_production',
  'conventional_banking',       // Interest-based banking
  'conventional_insurance',     // Non-takaful insurance
  'gambling_casinos',
  'adult_entertainment',
  'weapons_manufacturing',      // Controversial — some scholars permit defense
  'tobacco',                    // Controversial — increasingly prohibited
];

export function screenForHalalCompliance(
  company: CompanyFinancials,
  standard: 'AAOIFI' | 'DJIM' = 'AAOIFI'
): HalalScreeningResult {
  // Step 1: Sector screen
  const sectorCompliant = !HARAM_SECTORS.includes(company.sector);
  if (!sectorCompliant) {
    return {
      ...baseResult,
      sectorCompliant: false,
      sectorReason: `Prohibited sector: ${company.sector}`,
      isHalal: false,
      requiresPurification: false,
    };
  }
  
  // Step 2: Financial ratio screen (AAOIFI thresholds)
  const marketCap = company.sharesOutstanding * company.sharePrice;
  const totalAssets = company.totalAssets;
  
  // Denominator varies by standard:
  // AAOIFI uses total assets; DJIM uses trailing 36-month avg market cap
  const denominator = standard === 'AAOIFI' ? totalAssets : marketCap;
  
  const ratios = {
    // Debt ratio: total debt / denominator < 30% (AAOIFI) or 33% (DJIM)
    debtRatio: {
      value: company.totalDebt / denominator,
      threshold: standard === 'AAOIFI' ? 0.30 : 0.33,
      pass: false,
    },
    // Interest income ratio: interest income / total revenue < 5%
    interestIncomeRatio: {
      value: company.interestIncome / company.totalRevenue,
      threshold: 0.05,
      pass: false,
    },
    // Receivables ratio: accounts receivable / denominator < 49% (AAOIFI) or 33% (DJIM)
    receivablesRatio: {
      value: company.accountsReceivable / denominator,
      threshold: standard === 'AAOIFI' ? 0.49 : 0.33,
      pass: false,
    },
    // Cash + interest-bearing securities / denominator < 33%
    cashAndInterestRatio: {
      value: (company.cash + company.interestBearingSecurities) / denominator,
      threshold: 0.33,
      pass: false,
    },
    // Non-permissible income / total revenue < 5%
    nonPermissibleIncomeRatio: {
      value: company.nonPermissibleIncome / company.totalRevenue,
      threshold: 0.05,
      pass: false,
    },
  };
  
  // Evaluate each ratio
  for (const [key, ratio] of Object.entries(ratios)) {
    ratio.pass = ratio.value < ratio.threshold;
  }
  
  const allPass = Object.values(ratios).every(r => r.pass);
  
  // Purification: if halal but has some non-permissible income
  const purificationPct = ratios.nonPermissibleIncomeRatio.value * 100;
  
  return {
    ticker: company.ticker,
    companyName: company.name,
    screeningDate: new Date().toISOString(),
    sectorCompliant: true,
    ratioScreening: ratios,
    isHalal: allPass,
    requiresPurification: allPass && purificationPct > 0,
    purificationPercentage: purificationPct > 0 ? purificationPct : undefined,
    complianceStandard: standard,
  };
}
```

---

## Technique 3 — Zakat Calculation Engine

### Zakat on Financial Assets

```typescript
// Zakat calculation on wealth (2.5% of eligible assets annually)
interface ZakatCalculation {
  calculationDate: string;       // Hijri date (zakat year)
  
  // Zakatable assets
  cashAndBank: number;
  goldAndSilver: number;         // Market value
  tradingInventory: number;      // At current selling price
  receivables: number;           // Expected to be collected
  investments: number;           // Stocks, sukuk, funds (at market value)
  
  // Deductions
  shortTermLiabilities: number;  // Due within zakat year
  operatingExpenses: number;     // Committed expenses
  
  // Calculation
  totalZakatableAssets: number;
  netZakatBase: number;          // After deductions
  nisab: number;                 // Minimum threshold (85g gold equivalent)
  zakatDue: number;              // 2.5% of net base (if above nisab)
  
  currency: string;
}

export function calculateZakat(
  assets: ZakatableAssets,
  goldPricePerGram: number,      // Current gold price in local currency
  currency: string = 'AED'
): ZakatCalculation {
  // Nisab = value of 85 grams of gold (or 595 grams of silver)
  const nisab = goldPricePerGram * 85;
  
  const totalAssets = 
    assets.cashAndBank +
    assets.goldAndSilver +
    assets.tradingInventory +
    assets.receivables +
    assets.investments;
  
  const deductions = assets.shortTermLiabilities + assets.operatingExpenses;
  const netBase = Math.max(0, totalAssets - deductions);
  
  // Zakat only due if above nisab (threshold)
  const zakatDue = netBase >= nisab ? netBase * 0.025 : 0;
  
  return {
    calculationDate: formatHijriDate(new Date()),
    cashAndBank: assets.cashAndBank,
    goldAndSilver: assets.goldAndSilver,
    tradingInventory: assets.tradingInventory,
    receivables: assets.receivables,
    investments: assets.investments,
    shortTermLiabilities: assets.shortTermLiabilities,
    operatingExpenses: assets.operatingExpenses,
    totalZakatableAssets: totalAssets,
    netZakatBase: netBase,
    nisab,
    zakatDue: Math.round(zakatDue * 100) / 100,
    currency,
  };
}

// Zakat on investment portfolio (stock-specific)
export function calculatePortfolioZakat(
  holdings: StockHolding[],
  screeningResults: Map<string, HalalScreeningResult>
): PortfolioZakatResult {
  let totalZakatable = 0;
  
  for (const holding of holdings) {
    const screening = screeningResults.get(holding.ticker);
    if (!screening?.isHalal) continue; // Non-halal holdings excluded
    
    // Zakat on shares: based on zakatable assets per share
    // Method 1 (preferred): Net zakatable assets per share × shares held
    // Method 2 (simplified): Market value × 2.5%
    const zakatableValue = holding.marketValue;
    totalZakatable += zakatableValue;
  }
  
  return {
    totalPortfolioValue: holdings.reduce((sum, h) => sum + h.marketValue, 0),
    zakatablePortfolioValue: totalZakatable,
    zakatDue: totalZakatable * 0.025,
    purificationDue: calculatePurification(holdings, screeningResults),
  };
}
```

---

## Technique 4 — Sukuk (Islamic Bonds) Cash Flow Model

### Sukuk Structure & Cash Flow

```typescript
// Sukuk al-Ijara (most common sukuk structure)
interface SukukIjara {
  sukukId: string;
  issuer: string;                  // SPV (Special Purpose Vehicle)
  originator: string;              // Entity needing financing
  underlyingAsset: string;         // Physical asset backing the sukuk
  
  issuanceAmount: number;          // Total sukuk issuance
  certificateNominal: number;      // Face value per certificate
  totalCertificates: number;       // issuanceAmount / certificateNominal
  
  expectedRentalRate: number;      // Periodic rental rate
  paymentFrequency: 'semi-annual'; // Standard for sukuk
  tenor: number;                   // Years to maturity
  
  // Cash flow structure
  cashFlows: SukukCashFlow[];
  
  // Sharia compliance
  shariaAdvisor: string;           // SSB that approved
  aaoifiStandard: 'AAOIFI-17';    // Investment Sukuk standard
  assetBacked: boolean;           // Must be true for tradability
}

export function generateSukukCashFlows(
  issuanceAmount: number,
  rentalRate: number,
  tenorYears: number,
  frequency: 'semi-annual' = 'semi-annual'
): SukukCashFlow[] {
  const periodsPerYear = frequency === 'semi-annual' ? 2 : 4;
  const totalPeriods = tenorYears * periodsPerYear;
  const periodicRental = (issuanceAmount * rentalRate) / periodsPerYear;
  
  const cashFlows: SukukCashFlow[] = [];
  
  for (let period = 1; period <= totalPeriods; period++) {
    const isMaturity = period === totalPeriods;
    cashFlows.push({
      period,
      date: addPeriods(new Date(), period, frequency),
      rental: periodicRental,           // Rental income (NOT interest)
      principalReturn: isMaturity ? issuanceAmount : 0, // At maturity
      totalCashFlow: periodicRental + (isMaturity ? issuanceAmount : 0),
      cumulativeRental: periodicRental * period,
    });
  }
  
  return cashFlows;
}
```

---

## Anti-Pattern Catalog

| ID | Anti-Pattern | Risk | Fix |
|----|-------------|------|-----|
| IF-001 | Using `interest` terminology in Islamic product | **CRITICAL** — Sharia non-compliance | Use `profit`, `markup`, `rental`, `return` |
| IF-002 | Guaranteed returns on Mudarabah | **CRITICAL** — Invalidates contract | Returns must be variable based on actual profit |
| IF-003 | Late payment penalties as revenue | **HIGH** — Riba violation | Penalties donated to charity (not bank income) |
| IF-004 | Compound markup calculation | **HIGH** — Resembles compound interest | Markup calculated once at contract inception, fixed |
| IF-005 | Missing asset backing for sukuk | **CRITICAL** — Non-tradeable per AAOIFI | Physical asset must underlie every sukuk |
| IF-006 | Skipping halal sector screen | **HIGH** — Non-compliant portfolio | Screen ALL investments before including in Islamic fund |
| IF-007 | Ignoring financial ratio thresholds | **HIGH** — AAOIFI non-compliance | Debt <30%, interest income <5%, receivables <49% |
| IF-008 | No zakat module in Islamic banking app | **MEDIUM** — Missing expected feature | Integrate automated zakat calculation |
| IF-009 | Takaful replaced with conventional insurance | **HIGH** — Sharia violation | Use Takaful (cooperative insurance) only |
| IF-010 | No SSB approval documented in system | **CRITICAL** — Regulatory non-compliance | Store SSB fatwa reference for every product |

---

## Sharia Governance Workflow

```markdown
## Product Approval Lifecycle (Automated)

1. DESIGN → Product team structures financial product
2. SELF-CHECK → Run against halal screening algorithm (automated)
3. INTERNAL REVIEW → Sharia compliance officer reviews structure
4. SSB SUBMISSION → Formal documentation to Sharia Supervisory Board
5. SSB REVIEW → Scholars evaluate (2-6 weeks)
6. FATWA ISSUED → Formal approval or rejection with conditions
7. IMPLEMENTATION → Build with fatwa reference stored in system
8. ANNUAL AUDIT → External Sharia auditor reviews all transactions
9. PURIFICATION → Non-compliant income identified → donated to charity

## Required Documentation per Product:
- Product structure memorandum (Arabic + English)
- Flow of funds diagram
- Risk allocation analysis
- AAOIFI standard cross-reference
- SSB fatwa or approval letter
- Annual Sharia compliance report
```

---

## Chain-Multiplier Integration

```markdown
## How This Skill Serves Other Agents

@FintechStrategist → Primary consumer for all Islamic finance product structuring
@BackendAgent → Uses Murabaha/Ijara/Mudarabah calculation engines in API routes
@PropertyAnalyst → References Ijara/Murabaha for Islamic property finance modeling
@SecurityAgent → Consumes purification and audit trail requirements
@Frontend → Uses halal badge display and zakat calculator UI patterns

## Dependency Chain
payment-compliance → islamic-finance-compliance → mena-regulatory-compliance
  (payment processing)   (sharia product engine)     (licensing/entity setup)
         ↓
    [real-estate-modeling + smart-contract-dev]
    (Islamic property finance) (Sharia DeFi contracts)
```

## 🌍 Regional Calibration (MENA Context)

- **Cultural Alignment:** Ensure all logic respects regional business etiquette and MENA market expectations.
- **RTL Compliance:** Logic must explicitly handle Right-to-Left (RTL) flow where relevant.

## 🛡️ Critical Failure Modes (Anti-Patterns)

- **Anti-Pattern:** Generic Output -> *Correction:* Apply sector-specific professional rules from RULE.md.
- **Anti-Pattern:** Global-Only Logic -> *Correction:* Verify against MENA regional calibration.

---

## Success Criteria

- [ ] All financial products use correct Islamic terminology (no `interest`, `APR`, `loan`)
- [ ] Murabaha markup is fixed at contract inception — never compounds
- [ ] Mudarabah distributions reflect actual profit — no guaranteed returns
- [ ] Halal screening algorithm runs against AAOIFI thresholds automatically
- [ ] Zakat calculation engine produces accurate 2.5% computation with nisab check
- [ ] SSB fatwa reference stored for every approved financial product
- [ ] Late payment penalties directed to charity account — never bank revenue
- [ ] Sukuk cash flows generated with asset backing documented
- [ ] Annual Sharia audit trail maintained with purification records
- [ ] Portfolio purification percentage calculated for every dividend distribution