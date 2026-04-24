# 📐 spec_dsf_01_03: Sovereign Spacing & Grid

A 4px-based semantic spacing scale integrated with Next.js 15 container queries for responsive layout equilibrium.

## 📋 Narrative
Spacing is the invisible glue of industrial design. We enforce a 4px base unit (`--space-1 = 0.25rem`) to ensure mathematical alignment across all shards. By combining this with **Tailwind v4 container queries**, we enable components to adapt their spacing and layout based on their parent container, rather than just the viewport.

## 🛠️ Key Details
- **Base Unit**: 4px.
- **Responsive Logic**: Container Queries (@container).
- **Entry Point**: `factory/library/02-web-platforms/sovereign-ui/layout.css`
- **Token References**: `--space-1` to `--space-64`; `--max-width-dashboard`.

## 📋 Acceptance Criteria
- [ ] 100% token adherence for all margins, paddings, and gaps.
- [ ] Verified grid-equilibrium on mobile (320px) and ultra-wide (2560px).
- [ ] 0 hardcoded pixel values in layout specifications.

## 🛠️ spec.yaml
```yaml
phase_id: dsf-01
evolution_hash: sha256:dsf-v20-01-03-b5e3f1
acceptance_criteria:
  - spacing_token_audit_pass
  - grid_equilibrium_verified
  - responsive_shard_scaling_active
test_fixture: tests/design/tokens/spacing_audit.py
regional_compliance: LAW151-MENA-GRID-EQUILIBRIUM
```
