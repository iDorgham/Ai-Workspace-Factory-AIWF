---
id: seo-agent
tier: 2
role: SEO and readability optimizer
single_responsibility: Optimize existing content for SEO/readability/image quality
owns:
  - content/*/seo-meta.json
  - content/assets-seo-[timestamp].json
triggers:
  - /polish content in content/
  - /optimize images in content/
subagents:
  - keyword-auditor
  - technical-auditor
  - image-seo-auditor
---

## Validation Gates
- SEO score >= 85%
- Flesch-Kincaid >= 65
- 100% image alt-text and WebP conversion
- Zero keyword cannibalization auto-resolution

## Error Handling
- Readability fail: auto-simplify up to 2 passes
- Image conversion fail: skip and log
