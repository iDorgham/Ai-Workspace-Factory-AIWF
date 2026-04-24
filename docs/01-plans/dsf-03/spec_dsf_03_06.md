# 📐 spec_dsf_03_06: AI-Led Content Image Optimization

Integrates specialized sub-agents to generate and optimize industrial-grade assets, ensuring 100% visual equilibrium and performance.

## 📋 Narrative
Images must be both beautiful and performant. We utilize specialized **Visual Agents** to generate industrial-aesthetic assets that are then processed through the Next.js `<Image />` component. This ensures that every image is automatically resized, converted to WebP, and lazy-loaded with a blur-up placeholder, reducing page weight without sacrificing quality.

## 🛠️ Key Details
- **Logic**: Next.js Image Optimization (unpic / sharp).
- **Features**: Automated Alt-text; WebP/AVIF support.
- **Entry Point**: `components/ui/OptimizedImage.tsx`.

## 📋 Acceptance Criteria
- [ ] 0 broken images in production build.
- [ ] Image weight optimized to < 100KB per asset (average).
- [ ] Automated Alt-text coverage verified for all marketing images.

## 🛠️ spec.yaml
```yaml
phase_id: dsf-03
evolution_hash: sha256:dsf-v20-03-06-f7g8h9
acceptance_criteria:
  - image_load_perf_pass
  - webp_conversion_verified
  - alt_text_coverage_100
test_fixture: tests/content/image_perf_audit.py
regional_compliance: LAW151-MENA-VISUAL-EQUILIBRIUM
```
