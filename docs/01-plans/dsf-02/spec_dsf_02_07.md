# 📐 spec_dsf_02_07: MENA Regional Dashboard Adaptation

Injects regional adaptations for the MENA market, including RTL directionality, Hijri calendar support, and regional currency formatting.

## 📋 Narrative
Sovereign shards must be culturally and legally compliant with the MENA-soil. We implement a **Regional Adapter Context** that automatically flips the dashboard layout to RTL when Arabic is selected. Additionally, it provides hooks for Hijri date display and localized currency (EGP/SAR/AED) formatting, ensuring a premium native experience.

## 🛠️ Key Details
- **Context**: `RegionalAdapterProvider`.
- **Hooks**: `useRegionalFormat()`.
- **Features**: Hijri calendar; RTL-first layout logic.

## 📋 Acceptance Criteria
- [ ] 100% RTL visual equilibrium pass across all dashboard components.
- [ ] Correct EGP/SAR/AED symbol positioning (MENA-Native).
- [ ] Verified Hijri date conversion accuracy.

## 🛠️ spec.yaml
```yaml
phase_id: dsf-02
evolution_hash: sha256:dsf-v20-02-07-g7h8i9
acceptance_criteria:
  - mena_rtl_equilibrium_pass
  - currency_formatting_verified
  - hijri_calendar_accuracy_pass
test_fixture: tests/shard/mena_audit.py
regional_compliance: LAW151-MENA-CULTURAL-ADAPTATION
```
