# 🌐 Programmatic Ads Mastery (High-End DSPs)

## Purpose
Enforce professional standards for high-scale media buying using Demand-Side Platforms (DSPs). This skill focuses on **Display & Video 360 (DV360)** and **The Trade Desk (TTD)**, optimizing for global scale, fraud prevention, and audience targeting.

---

## Technique 1 — DSP Logic & Setup

### Google DV360 (Enterprise Ecosystem)
- **Integration**: Link directly to Campaign Manager 360 and Google Analytics 4 (GA4) to use first-party audience loops.
- **Budget Pacing**: Use "Flighted" budgets with daily spend caps to prevent front-loading.

### The Trade Desk (Open Web Dominance)
- **Audience Orchestration**: Utilize "Koa AI" for automated bidding based on performance intent.
- **Cross-Device Attribution**: Leverage TTD’s unified ID (UID2.0) to track the customer journey across Mobile, CTV, and Desktop without cookies.

---

## Technique 2 — Supply-Path Optimization (SPO)

- **Inventory Filtering**: Only buy from "Authorized Sellers" (ads.txt verification). 
- **Private Marketplaces (PMPs)**: Bypass the "Open Auction" for premium sites (e.g., Bloomberg, Vogue) to ensure brand safety and higher viewability.

---

## Technique 3 — Fraud & Brand Safety (Sentinel Shield)

- **Verification Tooling**: Integrate **IAS (Integral Ad Science)** or **DoubleVerify** directly into the DSP to block impressions on non-brand-safe sites.
- **IVT (Invalid Traffic)**: Monitor and auto-exclude IPs showing robotic behavior (High Click/Zero View).

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Buying the Long Tail** | Low-quality placements | Use "Inclusion Lists" of verified premium sites instead of targeting the entire web. |
| **No Viewability Floor** | Paying for invisible ads | Set a Minimum Viewability threshold (e.g., > 70% in-view). |
| **Frequency Over-saturation** | Brand annoyance | Set a strict "Frequency Cap" (e.g., max 3 exposures per user per 24 hours). |

---

## Success Criteria (Programmatic QA)
- [ ] Brand safety filters are active and verified.
- [ ] PMP deals are used for 50%+ of the display spend.
- [ ] IVT rate is below 2%.
- [ ] Conversion attribution is mapped across multiple devices.