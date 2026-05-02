---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# MENA Localization & Payment Integration

## Purpose

Implement production-grade MENA localization covering Arabic language support, RTL interfaces, local payment methods, regional tax compliance, and cultural date/time/number formatting — with concrete code patterns, component templates, and integration checklists that eliminate the most common MENA market failures.

**Measurable Impact:**
- Before: RTL as afterthought → 30-50% UI bugs on Arabic launch, 2-week remediation
- After: RTL-first with logical CSS properties → zero directional bugs on launch
- Before: Western payment-only checkout → 40% cart abandonment in Saudi (no Mada), 60% in Egypt (no COD/Fawry)
- After: Local-first payment stack → cart abandonment reduced to market benchmarks (15-20%)
- Chain multiplier: Consumed by @Frontend, @BackendAgent, @I18nAgent, @ContentWriter — affects every user-facing feature

---

## Technique 1 — RTL-First Component Architecture

### Next.js + next-intl Setup

```typescript
// app/[locale]/layout.tsx — RTL-aware root layout
import { NextIntlClientProvider, useMessages } from 'next-intl';
import { getTranslations } from 'next-intl/server';
import { Cairo, Inter } from 'next/font/google';

const inter = Inter({ subsets: ['latin'], variable: '--font-latin' });
const cairo = Cairo({ subsets: ['arabic'], variable: '--font-arabic' });

// Locale configuration
const RTL_LOCALES = ['ar', 'ar-AE', 'ar-SA', 'ar-EG'] as const;
type MENALocale = typeof RTL_LOCALES[number] | 'en';

export default async function LocaleLayout({
  children,
  params: { locale },
}: {
  children: React.ReactNode;
  params: { locale: MENALocale };
}) {
  const isRTL = RTL_LOCALES.includes(locale as any);
  const messages = useMessages();
  
  return (
    <html lang={locale} dir={isRTL ? 'rtl' : 'ltr'}>
      <body className={`${inter.variable} ${cairo.variable}`}
        style={{
          fontFamily: isRTL 
            ? 'var(--font-arabic), var(--font-latin), sans-serif'
            : 'var(--font-latin), sans-serif',
        }}
      >
        <NextIntlClientProvider locale={locale} messages={messages}>
          {children}
        </NextIntlClientProvider>
      </body>
    </html>
  );
}
```

### Logical CSS Properties (Mandatory)

```css
/* ✅ CORRECT: Logical properties auto-flip for RTL */
.card {
  padding-inline-start: 16px;   /* Left in LTR, Right in RTL */
  padding-inline-end: 12px;
  margin-inline-start: auto;
  margin-inline-end: 0;
  border-inline-start: 3px solid var(--color-primary);
  text-align: start;           /* Auto-adjusts for dir */
  float: inline-start;         /* Replaces float: left */
}

.sidebar {
  inset-inline-start: 0;       /* Replaces left: 0 */
  inset-inline-end: auto;
}

/* ❌ ANTI-PATTERN: Physical properties break RTL */
.card-broken {
  padding-left: 16px;          /* WRONG — doesn't flip */
  margin-right: auto;          /* WRONG — doesn't flip */
  text-align: left;            /* WRONG — should be 'start' */
  float: left;                 /* WRONG — should be 'inline-start' */
  border-left: 3px solid red;  /* WRONG — should be 'border-inline-start' */
}

/* Directional icons (arrows, chevrons) must flip */
[dir="rtl"] .icon-arrow-right {
  transform: scaleX(-1);       /* Mirror horizontal arrows */
}

/* Numbers always stay LTR even in RTL context */
.price, .phone-number, .date-numeric {
  direction: ltr;
  unicode-bidi: embed;
}
```

### RTL Component Pattern

```typescript
// components/MENAPrice.tsx — Locale-aware price display
'use client';
import { useLocale, useTranslations } from 'next-intl';

interface MENAPriceProps {
  amount: number;
  currency: 'AED' | 'SAR' | 'EGP' | 'BHD' | 'KWD' | 'QAR';
  showVAT?: boolean;
  vatRate?: number;
}

// Currency configuration
const CURRENCY_CONFIG: Record<string, {
  symbol: string;
  symbolAr: string;
  decimals: number;
  vatRate: number;
}> = {
  AED: { symbol: 'AED', symbolAr: 'د.إ', decimals: 2, vatRate: 0.05 },
  SAR: { symbol: 'SAR', symbolAr: 'ر.س', decimals: 2, vatRate: 0.15 },
  EGP: { symbol: 'EGP', symbolAr: 'ج.م', decimals: 2, vatRate: 0.14 },
  BHD: { symbol: 'BHD', symbolAr: 'د.ب', decimals: 3, vatRate: 0.10 },
  KWD: { symbol: 'KWD', symbolAr: 'د.ك', decimals: 3, vatRate: 0 },
  QAR: { symbol: 'QAR', symbolAr: 'ر.ق', decimals: 2, vatRate: 0 },
};

export function MENAPrice({ amount, currency, showVAT = true, vatRate }: MENAPriceProps) {
  const locale = useLocale();
  const t = useTranslations('common');
  const config = CURRENCY_CONFIG[currency];
  const effectiveVAT = vatRate ?? config.vatRate;
  
  // Format with Arabic-Indic numerals for Arabic locales
  const formatter = new Intl.NumberFormat(locale, {
    style: 'currency',
    currency,
    minimumFractionDigits: config.decimals,
    maximumFractionDigits: config.decimals,
  });
  
  const priceWithVAT = amount * (1 + effectiveVAT);
  const vatAmount = amount * effectiveVAT;
  
  return (
    <div className="price-container" style={{ direction: 'ltr', unicodeBidi: 'embed' }}>
      <span className="price-amount">{formatter.format(priceWithVAT)}</span>
      {showVAT && effectiveVAT > 0 && (
        <span className="price-vat text-muted-foreground text-xs">
          {t('vatInclusive', { rate: (effectiveVAT * 100).toFixed(0) })}
        </span>
      )}
    </div>
  );
}
```

---

## Technique 2 — Payment Stack Integration

### Multi-Gateway Payment Service

```typescript
// services/payment-gateway.ts — MENA payment orchestrator

interface PaymentGatewayConfig {
  gateway: 'stripe' | 'paytabs' | 'moyasar' | 'checkout' | 'fawry';
  country: string;
  supportedMethods: PaymentMethod[];
  settlementCurrency: string;
  supports3DS: boolean;
}

type PaymentMethod = 
  | 'visa' | 'mastercard' | 'amex'     // Global cards
  | 'mada'                              // Saudi national debit
  | 'knet'                              // Kuwait national network
  | 'benefit'                           // Bahrain national network
  | 'fawry'                             // Egypt payment network
  | 'meeza'                             // Egypt national card
  | 'stc_pay'                           // Saudi digital wallet
  | 'apple_pay' | 'google_pay'         // Mobile wallets
  | 'tabby' | 'tamara'                 // BNPL
  | 'cod';                              // Cash on delivery

// Optimal gateway selection by country
const GATEWAY_MAP: Record<string, PaymentGatewayConfig> = {
  AE: {
    gateway: 'checkout',
    country: 'AE',
    supportedMethods: ['visa', 'mastercard', 'amex', 'apple_pay', 'google_pay', 'tabby', 'cod'],
    settlementCurrency: 'AED',
    supports3DS: true,
  },
  SA: {
    gateway: 'moyasar',
    country: 'SA',
    supportedMethods: ['visa', 'mastercard', 'mada', 'stc_pay', 'apple_pay', 'tamara', 'cod'],
    settlementCurrency: 'SAR',
    supports3DS: true,
  },
  EG: {
    gateway: 'paytabs',
    country: 'EG',
    supportedMethods: ['visa', 'mastercard', 'fawry', 'meeza', 'cod'],
    settlementCurrency: 'EGP',
    supports3DS: true,
  },
  BH: {
    gateway: 'checkout',
    country: 'BH',
    supportedMethods: ['visa', 'mastercard', 'benefit', 'apple_pay'],
    settlementCurrency: 'BHD',
    supports3DS: true,
  },
  KW: {
    gateway: 'paytabs',
    country: 'KW',
    supportedMethods: ['visa', 'mastercard', 'knet'],
    settlementCurrency: 'KWD',
    supports3DS: true,
  },
};

// Payment checkout component data
export function getPaymentMethods(country: string): PaymentMethodDisplay[] {
  const config = GATEWAY_MAP[country];
  if (!config) return getPaymentMethods('AE'); // Default to UAE

  return config.supportedMethods.map(method => ({
    id: method,
    ...PAYMENT_METHOD_DISPLAY[method],
    // Priority order: local methods first, then global, then COD last
    priority: getMethodPriority(method, country),
  })).sort((a, b) => a.priority - b.priority);
}

const PAYMENT_METHOD_DISPLAY: Record<PaymentMethod, {
  nameEn: string;
  nameAr: string;
  icon: string;
  category: 'card' | 'wallet' | 'bnpl' | 'cash' | 'bank';
}> = {
  mada:       { nameEn: 'mada', nameAr: 'مدى', icon: 'mada-logo', category: 'card' },
  stc_pay:    { nameEn: 'STC Pay', nameAr: 'STC Pay', icon: 'stc-pay', category: 'wallet' },
  fawry:      { nameEn: 'Fawry', nameAr: 'فوري', icon: 'fawry-logo', category: 'bank' },
  meeza:      { nameEn: 'Meeza', nameAr: 'ميزة', icon: 'meeza-logo', category: 'card' },
  tabby:      { nameEn: 'Pay in 4 with Tabby', nameAr: 'قسّطها على ٤ دفعات مع تابي', icon: 'tabby-logo', category: 'bnpl' },
  tamara:     { nameEn: 'Split in 3 with Tamara', nameAr: 'قسّطها على ٣ مع تمارا', icon: 'tamara-logo', category: 'bnpl' },
  cod:        { nameEn: 'Cash on Delivery', nameAr: 'الدفع عند الاستلام', icon: 'cod-icon', category: 'cash' },
  visa:       { nameEn: 'Visa', nameAr: 'فيزا', icon: 'visa-logo', category: 'card' },
  mastercard: { nameEn: 'Mastercard', nameAr: 'ماستركارد', icon: 'mc-logo', category: 'card' },
  amex:       { nameEn: 'American Express', nameAr: 'أمريكان إكسبريس', icon: 'amex-logo', category: 'card' },
  apple_pay:  { nameEn: 'Apple Pay', nameAr: 'Apple Pay', icon: 'apple-pay', category: 'wallet' },
  google_pay: { nameEn: 'Google Pay', nameAr: 'Google Pay', icon: 'google-pay', category: 'wallet' },
  knet:       { nameEn: 'KNET', nameAr: 'كي نت', icon: 'knet-logo', category: 'card' },
  benefit:    { nameEn: 'Benefit Pay', nameAr: 'بنفت', icon: 'benefit-logo', category: 'card' },
};
```

---

## Technique 3 — VAT Engine & E-Invoicing

### Multi-Jurisdiction VAT Calculator

```typescript
// VAT calculation engine with MENA jurisdiction rules
interface VATCalculation {
  subtotal: number;
  vatRate: number;
  vatAmount: number;
  total: number;
  currency: string;
  jurisdiction: string;
  vatRegistrationNumber: string;
  isReverseCharge: boolean;
  exemptionReason?: string;
}

const VAT_RULES: Record<string, {
  standardRate: number;
  reducedRates: Record<string, number>;
  exemptions: string[];
  zeroRated: string[];
  registrationThreshold: number;
  currency: string;
  authority: string;
  filingFrequency: 'monthly' | 'quarterly';
}> = {
  AE: {
    standardRate: 0.05,
    reducedRates: {},
    exemptions: ['residential_rent', 'bare_land', 'local_passenger_transport', 'financial_services_margin'],
    zeroRated: ['exports', 'international_transport', 'first_supply_residential', 'crude_oil'],
    registrationThreshold: 375000, // AED
    currency: 'AED',
    authority: 'FTA (Federal Tax Authority)',
    filingFrequency: 'quarterly',
  },
  SA: {
    standardRate: 0.15,
    reducedRates: {},
    exemptions: ['financial_services_margin', 'residential_rent'],
    zeroRated: ['exports', 'international_transport', 'medicines_listed', 'investment_metals'],
    registrationThreshold: 375000, // SAR
    currency: 'SAR',
    authority: 'ZATCA',
    filingFrequency: 'monthly', // If revenue > SAR 40M, otherwise quarterly
  },
  EG: {
    standardRate: 0.14,
    reducedRates: { 'professional_services': 0.10 },
    exemptions: ['basic_food', 'healthcare_public', 'education_public'],
    zeroRated: ['exports', 'goods_free_zones'],
    registrationThreshold: 500000, // EGP
    currency: 'EGP',
    authority: 'ETA (Egyptian Tax Authority)',
    filingFrequency: 'monthly',
  },
  BH: {
    standardRate: 0.10,
    reducedRates: {},
    exemptions: ['financial_services_margin', 'residential_construction'],
    zeroRated: ['exports', 'international_transport', 'basic_food_items'],
    registrationThreshold: 37500, // BHD
    currency: 'BHD',
    authority: 'NBR (National Bureau for Revenue)',
    filingFrequency: 'monthly',
  },
  QA: {
    standardRate: 0,
    reducedRates: {},
    exemptions: [],
    zeroRated: [],
    registrationThreshold: 0,
    currency: 'QAR',
    authority: 'N/A — No VAT',
    filingFrequency: 'quarterly',
  },
  KW: {
    standardRate: 0,
    reducedRates: {},
    exemptions: [],
    zeroRated: [],
    registrationThreshold: 0,
    currency: 'KWD',
    authority: 'N/A — No VAT',
    filingFrequency: 'quarterly',
  },
};

export function calculateVAT(
  amount: number,
  country: string,
  productCategory: string = 'standard',
  isExport: boolean = false
): VATCalculation {
  const rules = VAT_RULES[country];
  if (!rules) throw new Error(`Unsupported country: ${country}`);
  
  let vatRate = rules.standardRate;
  let exemptionReason: string | undefined;
  
  // Check zero-rated
  if (isExport || rules.zeroRated.includes(productCategory)) {
    vatRate = 0;
    exemptionReason = isExport ? 'Export — zero-rated' : `Zero-rated: ${productCategory}`;
  }
  
  // Check exemptions
  if (rules.exemptions.includes(productCategory)) {
    vatRate = 0;
    exemptionReason = `VAT exempt: ${productCategory}`;
  }
  
  // Check reduced rates
  if (rules.reducedRates[productCategory] !== undefined) {
    vatRate = rules.reducedRates[productCategory];
  }
  
  const vatAmount = amount * vatRate;
  
  return {
    subtotal: amount,
    vatRate,
    vatAmount: Math.round(vatAmount * 100) / 100, // Round to 2 decimal places
    total: Math.round((amount + vatAmount) * 100) / 100,
    currency: rules.currency,
    jurisdiction: country,
    vatRegistrationNumber: '', // To be filled by caller
    isReverseCharge: false,
    exemptionReason,
  };
}
```

---

## Technique 4 — Date, Time & Number Localization

### Hijri Calendar Integration

```typescript
// Hijri date formatting for MENA applications
export function formatMENADate(
  date: Date,
  locale: string,
  options: {
    includeHijri?: boolean;
    format?: 'short' | 'long' | 'full';
  } = {}
): string {
  const { includeHijri = true, format = 'long' } = options;
  
  // Gregorian date
  const gregorian = new Intl.DateTimeFormat(locale, {
    day: 'numeric',
    month: format === 'short' ? 'numeric' : 'long',
    year: 'numeric',
  }).format(date);
  
  if (!includeHijri) return gregorian;
  
  // Hijri date (Umm al-Qura calendar — Saudi standard)
  const hijri = new Intl.DateTimeFormat(`${locale}-u-ca-islamic-umalqura`, {
    day: 'numeric',
    month: format === 'short' ? 'numeric' : 'long',
    year: 'numeric',
  }).format(date);
  
  // Display both: "15 شعبان 1447 / 12 فبراير 2026"
  return locale.startsWith('ar') ? `${hijri} / ${gregorian}` : `${gregorian} (${hijri})`;
}

// Locale-aware number formatting
export function formatMENANumber(
  value: number,
  locale: string,
  type: 'decimal' | 'percent' | 'currency' = 'decimal',
  currency?: string
): string {
  const options: Intl.NumberFormatOptions = { style: type };
  if (type === 'currency' && currency) {
    options.currency = currency;
  }
  
  return new Intl.NumberFormat(locale, options).format(value);
  // ar-EG: ١٢٬٣٤٥ (Arabic-Indic numerals)
  // ar-MA: 12,345 (Western numerals — Morocco exception)
  // en-AE: 12,345
}

// Working hours by country with Ramadan adjustment
export function getWorkingHours(country: string, isRamadan: boolean = false): WorkingHours {
  const WORKING_HOURS: Record<string, WorkingHours> = {
    AE: {
      days: ['mon', 'tue', 'wed', 'thu', 'fri'],
      start: isRamadan ? '09:00' : '09:00',
      end: isRamadan ? '14:00' : '18:00', // 6 hrs Ramadan
      timezone: 'Asia/Dubai',    // UTC+4
      weekend: ['sat', 'sun'],
    },
    SA: {
      days: ['sun', 'mon', 'tue', 'wed', 'thu'],
      start: isRamadan ? '10:00' : '08:00',
      end: isRamadan ? '15:00' : '17:00',
      timezone: 'Asia/Riyadh',   // UTC+3
      weekend: ['fri', 'sat'],
    },
    EG: {
      days: ['sun', 'mon', 'tue', 'wed', 'thu'],
      start: isRamadan ? '10:00' : '09:00',
      end: isRamadan ? '15:00' : '17:00',
      timezone: 'Africa/Cairo',  // UTC+2
      weekend: ['fri', 'sat'],
    },
  };
  return WORKING_HOURS[country] || WORKING_HOURS['AE'];
}
```

---

## Anti-Pattern Catalog

| ID | Anti-Pattern | Risk | Fix |
|----|-------------|------|-----|
| LOC-001 | Using physical CSS properties (left/right) | **HIGH** — Broken RTL layout | Use logical properties (inline-start/end) exclusively |
| LOC-002 | Hardcoded LTR direction | **HIGH** — Unreadable Arabic text | Set `dir` from locale; use `text-align: start` |
| LOC-003 | English-only payment receipts | **MEDIUM** — Compliance gap, user confusion | Bilingual receipts (Arabic + English) |
| LOC-004 | USD-only pricing | **HIGH** — Friction, lower MENA conversion | Local currency display with correct decimal places |
| LOC-005 | No COD option in Egypt | **CRITICAL** — Loses 40%+ of Egyptian customers | Always include COD for Egyptian e-commerce |
| LOC-006 | Missing Mada for Saudi checkout | **CRITICAL** — 70% of Saudi cards are Mada | Integrate Mada-compatible gateway (Moyasar/PayTabs) |
| LOC-007 | Western numerals forced in Arabic UI | **MEDIUM** — Reduced familiarity | Use `Intl.NumberFormat` with Arabic locale |
| LOC-008 | No Hijri date option | **MEDIUM** — Missing cultural context | Offer dual Hijri/Gregorian dates |
| LOC-009 | Ignoring BHD/KWD 3-decimal currencies | **HIGH** — Pricing errors | Use currency-aware decimal places (3 for BHD/KWD/OMR) |
| LOC-010 | Machine-translated Arabic without review | **HIGH** — Embarrassing errors, brand damage | Native Arabic speaker review mandatory |
| LOC-011 | BNPL not offered in GCC checkout | **MEDIUM** — 15-25% revenue lift missed | Integrate Tabby (UAE) / Tamara (KSA) |
| LOC-012 | Same working hours for all MENA countries | **MEDIUM** — SLA violations, missed communications | Country-specific working hours + Ramadan adjustment |

---

## Chain-Multiplier Integration

```markdown
## How This Skill Serves Other Agents

@Frontend → Consumes RTL component patterns, price formatting, payment UI
@BackendAgent → Uses VAT engine, payment gateway integration, e-invoicing
@I18nAgent → References Arabic typography, locale config, message file patterns
@ContentWriter → Uses bilingual template patterns, number/date formatting rules
@QAAgent → References RTL testing checklist, payment flow validation

## Dependency Chain
bilingual-rtl-first → mena-localization-payments → mena-regulatory-compliance
   (CSS/layout layer)     (payments/tax/formatting)      (entity/licensing)
         ↓
    [payment-compliance + mena-cultural-business-practices]
    (deep payment patterns)  (cultural adaptation layer)
```

## 🌍 Regional Calibration (MENA Context)

- **Cultural Alignment:** Ensure all logic respects regional business etiquette and MENA market expectations.
- **RTL Compliance:** Logic must explicitly handle Right-to-Left (RTL) flow where relevant.

## 🛡️ Critical Failure Modes (Anti-Patterns)

- **Anti-Pattern:** Generic Output -> *Correction:* Apply sector-specific professional rules from RULE.md.
- **Anti-Pattern:** Global-Only Logic -> *Correction:* Verify against MENA regional calibration.

---

## Success Criteria

- [ ] All CSS uses logical properties — zero `left/right/margin-left/padding-right`
- [ ] Arabic font (Cairo/Tajawal) loaded and applied for Arabic locales
- [ ] Local payment methods integrated per country (Mada/STC Pay/Fawry/KNET)
- [ ] BNPL (Tabby/Tamara) available in UAE/Saudi checkout
- [ ] VAT calculated correctly: 5% UAE, 15% Saudi, 14% Egypt, 10% Bahrain
- [ ] Hijri date option available for Arabic locale users
- [ ] Arabic-Indic numerals displayed for Arabic locales (except Morocco)
- [ ] 3-decimal currencies (BHD/KWD/OMR) handled correctly
- [ ] Bilingual receipts and invoices generated
- [ ] Working hours and SLAs adjusted for Ramadan period
- [ ] COD available as payment option for Egypt e-commerce