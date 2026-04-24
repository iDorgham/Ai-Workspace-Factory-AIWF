# 📐 spec_dsf_03_04: Dynamic Blog & Resource Hub

Implements a high-performance, static-first blog and resource hub using MDX for industrial-grade articles and guides.

## 📋 Narrative
Content hubs must be fast and easily discoverable. We implement a **Static-First Blog Hub** that renders MDX content at build time for near-instantaneous page loads. The hub features automated table-of-contents generation, tag-based filtering, and deep integration with the shard's AI orchestrator for personalized content recommendations.

## 🛠️ Key Details
- **Architecture**: Next.js Static Site Generation (SSG).
- **Features**: Tag filtering; Category grouping; Search integration.
- **Entry Point**: `app/[locale]/blog/page.tsx`.

## 📋 Acceptance Criteria
- [ ] Blog post LCP < 200ms on simulated high-latency connections.
- [ ] Automated Table-of-Contents (TOC) verified for all articles.
- [ ] 100/100 Lighthouse SEO score for article pages.

## 🛠️ spec.yaml
```yaml
phase_id: dsf-03
evolution_hash: sha256:dsf-v20-03-04-d5e6f7
acceptance_criteria:
  - blog_performance_target_met
  - toc_generation_verified
  - lighthouse_seo_audit_100
test_fixture: tests/content/blog_audit.py
regional_compliance: LAW151-MENA-RESOURCE-SOVEREIGNTY
```
