# 📐 spec_dsf_03_05: SEO & Metadata Sovereign Protocol

Automates the generation of meta titles, descriptions, OpenGraph images, and sitemaps to ensure 100% industrial search visibility.

## 📋 Narrative
Visibility is a prerequisite for shard impact. We implement a **Sovereign Metadata Protocol** that automatically generates SEO-rich metadata for every materialized page. This includes dynamic OG Image generation (using `@vercel/og`), automated sitemap updates, and structured JSON-LD data to ensure the shard ranks at OMEGA-tier levels on global search engines.

## 🛠️ Key Details
- **API**: Next.js `generateMetadata()` API.
- **Tools**: `@vercel/og` for dynamic images; `next-sitemap`.
- **Logic**: Automated robots.txt and sitemap.xml generation.

## 📋 Acceptance Criteria
- [ ] Validated OpenGraph images for all page categories.
- [ ] 100% sitemap coverage for all bilingual route variants.
- [ ] 0 SEO critical errors in automated audit tools.

## 🛠️ spec.yaml
```yaml
phase_id: dsf-03
evolution_hash: sha256:dsf-v20-03-05-e6f7g8
acceptance_criteria:
  - og_image_generation_verified
  - sitemap_coverage_100
  - seo_critical_audit_pass
test_fixture: tests/content/seo_purity_audit.py
regional_compliance: LAW151-MENA-SEARCH-VISIBILITY
```
