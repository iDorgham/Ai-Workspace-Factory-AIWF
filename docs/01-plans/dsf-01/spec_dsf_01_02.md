# 📐 spec_dsf_01_02: Industrial Typography Scales

Implements a fluid typography system with dedicated Arabic font fallbacks for Law 151/2020 compliance and high-fidelity MENA-soil legibility.

## 📋 Narrative
Industrial typography requires a strict hierarchy that scales predictably across devices. We utilize a **Major Second** scale ratio, combined with fluid `clamp()` values for responsive sizing. For MENA sovereignty, we integrate **Cairo** and **Amiri** as primary Arabic fallbacks, ensuring that cultural compliance is baked into the layout primitives.

## 🛠️ Key Details
- **Primary Stack**: Inter (Variable) + Cairo (Fallback).
- **Secondary Stack**: JetBrains Mono + Amiri (Fallback).
- **Entry Point**: `factory/library/02-web-platforms/sovereign-ui/typography.css`
- **Token References**: `--font-size-h1` to `--font-size-caption`; `--font-weight-bold`.

## 📋 Acceptance Criteria
- [ ] 100% RTL readability pass for all header levels.
- [ ] Verified font-fallback sequence (MENA-Aware).
- [ ] Zero layout shift during font loading (Font Display: Swap).

## 🛠️ spec.yaml
```yaml
phase_id: dsf-01
evolution_hash: sha256:dsf-v20-01-02-a8c7d9
acceptance_criteria:
  - typography_scale_verified
  - mena_font_fallback_active
  - rtl_readability_pass
test_fixture: tests/design/tokens/typography_audit.py
regional_compliance: LAW151-MENA-TYPO-SOVEREIGN
```
