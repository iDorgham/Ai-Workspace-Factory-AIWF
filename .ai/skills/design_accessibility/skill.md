```json
{
  "skill_id": "design-accessibility",
  "name": "Design Accessibility",
  "version": "1.0.0",
  "description": "WCAG-oriented checks on generated pages and assets (alt text, structure) aligned with SEO polish flows.",
  "cowork_skill": "design:accessibility",
  "integration_ref": ".ai/skills/skill_integration/skill.md",
  "agents": ["seo-agent", "image-seo-auditor"],
  "timestamp": "2026-05-02T00:00:00Z"
}
```

# Design accessibility

## Sovereign mapping

**`design:accessibility`** — accessibility check on generated pages; often paired with image SEO. See **DESIGN ALIGNMENT** in `.ai/skills/skill_integration/skill.md`.

## Protocol

1. Target WCAG **AA** for user-facing generated content unless a stricter project brief exists.
2. Check semantic headings, focus order, labels, contrast claims, and image `alt` coverage.
3. Report issues with severity and fix hints; do not silently strip accessibility requirements.
