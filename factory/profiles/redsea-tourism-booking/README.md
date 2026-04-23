# Red Sea Tourism Booking — Profile README
**Profile ID**: `redsea-tourism-booking`
**Version**: 1.0.0
**Region**: Red Sea / Egypt / MENA
**Vertical**: Hospitality / Tourism

---

## Overview

This profile is a pre-configured factory starter for building hotel and tourism booking platforms targeting Red Sea destinations (Hurghada, Sharm El-Sheikh, Marsa Alam, Dahab, Nuweiba).

It includes all regional adaptations, payment integrations, and data models needed to launch quickly without building from scratch.

---

## Quick Start

```bash
# 1. Create the PRD
/do "Red Sea resort booking platform" --region=redsea

# 2. Generate the SDD plan
/plan --from=00-prd/prd.md --region=redsea

# 3. Implement phase 1
/dev --phase=1 --region=redsea

# 4. Run regional compliance tests
/test --phase=1 --region=redsea

# 5. Deploy to preview
/deploy --preview --region=redsea
```

---

## Included Features

| Feature | Status |
| :--- | :--- |
| Property search + availability calendar | ✅ Core |
| Arabic RTL layout | ✅ Core |
| Fawry payment integration | ✅ Core |
| Vodafone Cash integration | ✅ Core |
| Multi-language (Arabic + English) | ✅ Core |
| PDF booking voucher (bilingual) | ✅ Core |
| Dive certification tracking | 🔵 Optional |
| Liveaboard management | 🔵 Optional |
| Loyalty points (EGP) | 🔵 Optional |

---

## Regional Compliance

- **Data Residency**: Egypt Law 151/2020
- **Currency**: EGP (primary) + USD (international)
- **Timezone**: Africa/Cairo
- **Payments**: Fawry, Vodafone Cash, Stripe (international)
- **Languages**: Arabic (RTL), English (LTR)

---

## Brainstorm Integration

Run this to get a copyable spec block tailored to your project:

```
/brainstorm --skill=redsea-tourism-booking --region=redsea
```

---

*Profile version: 1.0.0 | Created: 2026-04-23 | AIWF v7.0.0*
