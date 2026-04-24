# 📐 spec_dsf_03_01: Sovereign Content Architecture (MDX + Next.js)

Materializes the high-performance MDX foundation for dynamic page materialization, enabling the seamless integration of industrial components into markdown content.

## 📋 Narrative
Content in the AIWF is treated with the same engineering rigor as code. We implement **MDX (Markdown + JSX)** to allow our `@aiwf/sovereign-ui` components to be used directly within articles, guides, and marketing pages. This architectural choice ensures that content remains expressive while inheriting the design system's technical equilibrium and performance benefits.

## 🛠️ Key Details
- **Logic**: Next.js `@next/mdx` configuration.
- **Components**: `mdx-components.tsx` (Mapping Markdown tags to Sovereign-UI components).
- **Entry Point**: `app/blog/` and `app/marketing/`.

## 📋 Acceptance Criteria
- [ ] Sovereign-UI components (Button, Card) render correctly within MDX files.
- [ ] Zero layout shift (CLS) during MDX component hydration.
- [ ] Verified support for frontmatter metadata extraction.

## 🛠️ spec.yaml
```yaml
phase_id: dsf-03
evolution_hash: sha256:dsf-v20-03-01-a2b3c4
acceptance_criteria:
  - mdx_component_parity_verified
  - frontmatter_parsing_active
  - hydration_equilibrium_pass
test_fixture: tests/content/mdx_render_audit.py
regional_compliance: LAW151-MENA-CONTENT-INTEGRITY
```
