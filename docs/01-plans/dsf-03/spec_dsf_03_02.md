# 📐 spec_dsf_03_02: Bilingual Content Materialization (EN/AR)

Establishes the industrial framework for bilingual content equilibrium, ensuring 100% translation parity for all shard marketing and documentation assets.

## 📋 Narrative
Global shards must be culturally accessible. We implement a **Bilingual Content Protocol** that mandates 1-to-1 parity between English and Arabic versions of every page. Using `next-intl`, we ensure that localized strings are managed centrally and injected into the UI with zero performance overhead, while maintaining full RTL directionality for Arabic content.

## 🛠️ Key Details
- **Tooling**: `next-intl` (Next.js i18n).
- **Messages**: `messages/en.json`, `messages/ar.json`.
- **Logic**: Locale-aware routing (`/[locale]/page.tsx`).

## 📋 Acceptance Criteria
- [ ] 0 missing translation strings in automated audit.
- [ ] Correct RTL layout flip verified for all Arabic content pages.
- [ ] Instantaneous locale-switching with state preservation.

## 🛠️ spec.yaml
```yaml
phase_id: dsf-03
evolution_hash: sha256:dsf-v20-03-02-b3c4d5
acceptance_criteria:
  - translation_parity_verified
  - rtl_visual_equilibrium_pass
  - locale_routing_accuracy_pass
test_fixture: tests/content/translation_audit.py
regional_compliance: LAW151-MENA-LINGUISTIC-SOVEREIGNTY
```
