# 🌍 Bilingual Next.js Performance (Omega-tier)

## Purpose
Enforce professional standards for optimizing bilingual (AR/EN) Next.js applications. This skill focuses on **RTL Integrity**, **GCC-specific Mobile Performance**, and **Cultural Calibration** for high-growth MENA markets.

---

## 🌍 Regional Calibration (MENA Context)

- **RTL Integrity:** Mandatory scroll-bar re-alignment and icon-mirroring for the Arabic locale.
- **Cultural Speed:** Optimize for 4G/5G mobile-first populations in GCC.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

- **Anti-Pattern:** Hardcoded LTR Padding -> *Correction:* Use `ps-` and `pe-` logical properties.
- **Anti-Pattern:** Non-Subsetted Fonts -> *Correction:* Only load required Arabic glyphs to save ~300KB.

---

## Success Criteria (Bilingual QA)
- [ ] RTL layout remains intact across all breakpoints.
- [ ] Font sub-setting reduces bundle size by at least 200KB.
- [ ] Native logical properties (`ps`, `pe`, `ms`, `me`) used throughout the CSS.
- [ ] TTFB in GCC regions optimized via regional edge caching.
