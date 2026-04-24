# 📐 spec_dsf_01_07: Core Component Library (15+ Components)

Materializes the foundational component set using Radix UI primitives and CVA for composable, token-driven technical equilibrium.

## 📋 Narrative
The `@aiwf/sovereign-ui` core includes 15+ high-fidelity components (Button, Card, Badge, Avatar, Tooltip, Dialog, Tabs, etc.). These are designed to be composable and reference semantic tokens ONLY. By building on Radix UI, we inherit industrial-grade accessibility (WCAG 2.2 AA) while maintaining full control over the premium industrial aesthetic via Tailwind v4.

## 🛠️ Key Details
- **Base Primitives**: Radix UI.
- **Variant Logic**: Class Variance Authority (CVA).
- **Entry Point**: `factory/library/02-web-platforms/sovereign-ui/components/ui/`
- **Token References**: 100% token coverage required.

## 📋 Acceptance Criteria
- [ ] 100% WCAG 2.2 AA accessibility audit pass.
- [ ] 0 hardcoded colors or spacing in component definitions.
- [ ] Verified RTL parity for complex components (Dialog, Tabs).

## 🛠️ spec.yaml
```yaml
phase_id: dsf-01
evolution_hash: sha256:dsf-v20-01-07-e7a1b3
acceptance_criteria:
  - radix_primitive_integration_pass
  - cva_variant_equilibrium_verified
  - token_compliance_audit_100
test_fixture: tests/design/components/core_audit.py
regional_compliance: LAW151-MENA-COMP-ARCH
```
