# 📐 spec_dsf_01_01: Token Strategy & OKLCH Logic

This specification establishes the semantic color foundation for the Sovereign Industrial Design System. By adopting the **OKLCH** color space, the factory ensures perceptual uniformity and high-fidelity contrast across the industrial dark-mode-first aesthetic.

## 📋 Narrative
The design system operates on a "Semantic First" principle. Tokens are named by their function (e.g., `--color-primary`) rather than their appearance. This enables instantaneous thematic shifts (e.g., from Industrial Blue to MENA-soil Gold) without modifying component code. The default palette is optimized for premium dark environments, utilizing deep blacks (`#0a0a0f`) as the base to reduce screen fatigue and enhance accent vibrancy.

## 🛠️ Key Details
- **Base Color Logic**: OKLCH for consistent lightness and chroma.
- **Entry Point**: `factory/library/02-web-platforms/sovereign-ui/tokens.css`
- **Token References**: `--color-background`, `--color-foreground`, `--color-primary`, `--color-accent`, `--color-destructive`.

## 📋 Acceptance Criteria
- [ ] 100% adherence to semantic naming (no `--color-blue-500`).
- [ ] Verified light/dark variants via `.dark` class toggle.
- [ ] 0% hardcoded hex codes in library components.

## 🛠️ spec.yaml
```yaml
phase_id: dsf-01
evolution_hash: sha256:dsf-v20-01-01-f2a1b3
acceptance_criteria:
  - token_coverage_100
  - semantic_logic_verified
  - oklch_normalization_complete
test_fixture: tests/design/tokens/color_audit.py
regional_compliance: LAW151-MENA-COLOR-GEOSPACE
```
