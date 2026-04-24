---
type: Generic
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# AIWF v7.0.0 — Regional Adapter (Egypt / Red Sea / MENA)
# Library Component: 12-meta-engine/meta-orchestration/v7-orchestration/regional-adapter.md
# Version: 7.0.0 | Reasoning Hash: sha256:regional-v7-2026-04-23
# ============================================================

## Overview

The Regional Adapter is a T1 sub-agent that activates whenever a `--region` flag is present on any command. It injects MENA-specific adaptations across UI, payments, data residency, currency, and compliance.

It operates **silently** — injecting regional config without interrupting the main command flow — but logs all adaptations to `.ai/logs/workflow.jsonl`.

---

## Activation

```yaml
triggers:
  - "--region=egypt on any command"
  - "--region=redsea on any command"
  - "--region=mena on any command"
  - "Auto-detect: project slug or domain contains 'egypt', 'cairo', 'redsea', 'hurghada', 'sharm'"
```

---

## Region Profiles

### 🇪🇬 Egypt (`--region=egypt`)

```yaml
region: egypt
legal_framework: "Law 151/2020 — Personal Data Protection Law"
data_residency: required
  note: "Data must be stored/processed in Egypt or approved jurisdictions"
currency:
  primary: "EGP"
  secondary: ["USD"]
language:
  primary: "Arabic (ar)"
  secondary: "English (en)"
  direction: "RTL"
payments:
  - name: "Fawry"
    type: "Cash reference code + card"
    sdk: "Fawry SDK v3"
  - name: "Vodafone Cash"
    type: "Mobile wallet"
    api: "Vodafone Cash Business API"
  - name: "Meeza"
    type: "National debit card"
  - name: "InstaPay"
    type: "Instant bank transfer"
  - name: "Stripe"
    type: "International cards"
tax: "VAT 14%"
timezone: "Africa/Cairo (UTC+2, no DST)"
date_format: "DD/MM/YYYY"
phone_format: "+20 10X XXXX XXXX"
```

### 🌊 Red Sea (`--region=redsea`)

```yaml
region: redsea
inherits: egypt  # All Egypt rules apply
additional_features:
  tourism_booking:
    - Hotel/resort property search
    - Dive center booking (PADI/SSI certification tracking)
    - Liveaboard itinerary management
    - Excursion/safari booking
    - Airport transfer booking
  certifications:
    - "PADI Open Water, Advanced, Divemaster"
    - "SSI levels 1-3"
  key_locations:
    - "Hurghada"
    - "Sharm El-Sheikh"
    - "Marsa Alam"
    - "Dahab"
    - "Nuweiba"
    - "El Gouna"
  currency_note: "USD widely accepted alongside EGP for tourism"
  language_note: "English primary for international tourists, Arabic for domestic"
```

### 🌍 MENA (`--region=mena`)

```yaml
region: mena
coverage: ["egypt", "redsea", "saudi_arabia", "uae", "jordan", "kuwait", "bahrain", "oman"]
currency:
  - "EGP (Egypt)"
  - "SAR (Saudi Arabia)"
  - "AED (UAE)"
  - "KWD (Kuwait)"
  - "BHD (Bahrain)"
  - "OMR (Oman)"
  - "JOD (Jordan)"
payments:
  egypt: ["Fawry", "Vodafone Cash", "Meeza", "InstaPay"]
  ksa: ["Mada", "STC Pay", "Tamara (BNPL)", "Tabby (BNPL)"]
  uae: ["Apple Pay", "Google Pay", "Tabby", "Postpay"]
  universal: ["Stripe", "PayTabs", "HyperPay"]
compliance:
  egypt: "Law 151/2020"
  ksa: "PDPL (Personal Data Protection Law)"
  uae: "DIFC Data Protection Law"
rtl_required: true
```

---

## What the Regional Adapter Injects

### Into `/plan` output:
```
regional/
├── egypt-compliance.md         # Law 151/2020 checklist
├── mena-adaptations.json       # Feature flags, payment configs
└── rtl-layout-guide.md         # Arabic RTL implementation notes
```

### Into `spec.yaml`:
```yaml
regional_compliance:
  target_regions: ["redsea", "egypt"]
  requirements:
    - "Law 151/2020 data residency"
    - "Arabic RTL layout"
    - "Fawry payment integration"
  feature_flags:
    rtl_layout: true
    local_payments: ["Fawry", "Vodafone Cash"]
    data_residency: "Law 151/2020"
    currency: ["EGP"]
```

### Into `/deploy --region` environment:
```bash
NEXT_PUBLIC_LOCALE=ar
NEXT_PUBLIC_RTL=true
NEXT_PUBLIC_CURRENCY=EGP
PAYMENT_GATEWAY=fawry
FAWRY_ENDPOINT=$FAWRY_ENDPOINT
VODAFONE_CASH_ENDPOINT=$VODAFONE_CASH_ENDPOINT
```

### Into `/test --region` suite:
- RTL rendering validation (text alignment, flex direction)
- Fawry reference code generation test
- Vodafone Cash wallet API mock test
- Law 151/2020 data field compliance check
- Arabic date/number formatting tests
- EGP currency formatting tests

---

## Auto-Detection Heuristics

```yaml
auto_detect_triggers:
  keywords: ["egypt", "cairo", "redsea", "hurghada", "sharm", "mena", "arabic", "fawry", "egp", "نظام", "حجز"]
  domain_patterns: [".eg", ".com.eg", ".net.eg"]
  prd_fields: ["target_market", "region", "payment_methods"]
```

When auto-detected, the adapter suggests regional adaptations but does **not** apply them without the explicit `--region` flag.

---

*Component version: 7.0.0*
*Library path: 12-meta-engine/meta-orchestration/v7-orchestration/regional-adapter.md*
*Last updated: 2026-04-23T12:56:22+02:00*
*Reasoning Hash: sha256:regional-v7-2026-04-23*
