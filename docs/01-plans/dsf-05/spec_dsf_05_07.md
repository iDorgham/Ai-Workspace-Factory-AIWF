# 📐 spec_dsf_05_07: MENA Vertical Localization

Injects regional compliance shards specifically for Egypt, Saudi Arabia, and UAE local laws and business protocols.

## 📋 Narrative
Regional specificity is a hallmark of the Sovereign Shard. We implement **MENA Vertical Localization**, providing specialized adapters for Egypt (EGP, VAT), Saudi Arabia (SAR, ZATCA), and UAE (AED, FTA). These adapters ensure that every verticalized shard is instantly compliant with local tax, legal, and operational standards.

## 🛠️ Key Details
- **Logic**: Regional Compliance Adapters.
- **Features**: ZATCA E-invoicing support; Egyptian Law 151 compliance badges.
- **Entry Point**: `lib/regional/law_adapter.ts`.

## 📋 Acceptance Criteria
- [ ] Correct EGP/SAR/AED VAT calculation verified for mock invoices.
- [ ] ZATCA-compliant XML generation pass for Saudi shards.
- [ ] Verified Law 151 data residency badges in UI.

## 🛠️ spec.yaml
```yaml
phase_id: dsf-05
evolution_hash: sha256:dsf-v20-05-07-g7h8i9
acceptance_criteria:
  - regional_compliance_verified
  - vat_calculation_parity_pass
  - residency_badging_verified
test_fixture: tests/shard/mena_localization_audit.py
regional_compliance: LAW151-MENA-LOCAL-SOVEREIGNTY
```
