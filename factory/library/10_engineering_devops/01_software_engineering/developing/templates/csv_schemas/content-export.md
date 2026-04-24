---
type: Generic
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# content-export

Converted from `content-export.json` for template-folder type consistency.

```json
{
  "_meta": {
    "version": "1.0",
    "description": "CSV export schema. export-packager sub-agent validates all output against this schema before writing to content/sovereign/outputs/csv-exports/. All required fields must be present and non-null for export to proceed.",
    "owner": "workflow-agent"
  },

  "schema": {
    "slug": {
      "type": "string",
      "required": true,
      "format": "url-safe lowercase, hyphens only",
      "example": "sustainable-luxury-interiors-cairo"
    },
    "content_type": {
      "type": "string",
      "required": true,
      "enum": ["blog-post", "project", "landing-page", "website-page"]
    },
    "title": {
      "type": "string",
      "required": true,
      "max_chars": 60
    },
    "meta_description": {
      "type": "string",
      "required": true,
      "min_chars": 120,
      "max_chars": 155
    },
    "primary_keyword": {
      "type": "string",
      "required": true
    },
    "secondary_keywords": {
      "type": "string",
      "required": false,
      "format": "comma-separated",
      "example": "interior design Cairo, bespoke home design, luxury interiors Egypt"
    },
    "body_markdown_path": {
      "type": "string",
      "required": true,
      "format": "relative path to content/ file",
      "example": "content/sovereign/blog-posts/sustainable_luxury_interiors.md"
    },
    "word_count": {
      "type": "integer",
      "required": true,
      "minimum": 300
    },
    "flesch_kincaid_score": {
      "type": "float",
      "required": true,
      "minimum": 65
    },
    "seo_score": {
      "type": "float",
      "required": true,
      "minimum": 0.85,
      "format": "decimal (e.g., 0.91 = 91%)"
    },
    "brand_voice_score": {
      "type": "float",
      "required": true,
      "minimum": 0.92,
      "format": "decimal (e.g., 0.95 = 95%)"
    },
    "originality_score": {
      "type": "float",
      "required": true,
      "maximum": 0.15,
      "note": "Lower is better. Max 15% similarity to any source."
    },
    "image_seo_coverage": {
      "type": "float",
      "required": true,
      "value": 1.00,
      "note": "Must be 1.00 (100%). Hard block if not."
    },
    "images": {
      "type": "string",
      "required": false,
      "format": "comma-separated webp paths",
      "example": "content/sovereign/blog-posts/images/hero.webp, content/sovereign/blog-posts/images/detail.webp"
    },
    "internal_links": {
      "type": "string",
      "required": false,
      "format": "comma-separated URLs",
      "minimum_count": 2
    },
    "schema_markup_type": {
      "type": "string",
      "required": false,
      "enum": ["Article", "LocalBusiness", "Service", "FAQPage", "BreadcrumbList", ""]
    },
    "status": {
      "type": "string",
      "required": true,
      "value": "approved",
      "note": "Export is blocked if status ≠ 'approved'"
    },
    "approved_at": {
      "type": "string",
      "required": true,
      "format": "ISO8601",
      "example": "2026-04-13T14:30:00+02:00"
    },
    "approved_by": {
      "type": "string",
      "required": true,
      "note": "Role or name of approver (brand/admin role)"
    },
    "created_at": {
      "type": "string",
      "required": true,
      "format": "ISO8601"
    },
    "version": {
      "type": "integer",
      "required": true,
      "minimum": 1
    },
    "cms_target": {
      "type": "string",
      "required": false,
      "enum": ["wordpress", "webflow", "contentful", "custom", ""],
      "note": "Informs CMS pack formatting in cms-packs/"
    },
    "campaign": {
      "type": "string",
      "required": false,
      "note": "Required only for landing-page content type"
    },
    "project_location": {
      "type": "string",
      "required": false,
      "note": "Required only for project content type"
    },
    "project_year": {
      "type": "integer",
      "required": false,
      "note": "Required only for project content type"
    }
  },

  "validation_rules": {
    "hard_blocks": [
      "status must equal 'approved'",
      "image_seo_coverage must equal 1.00",
      "seo_score must be ≥ 0.85",
      "brand_voice_score must be ≥ 0.92",
      "originality_score must be ≤ 0.15",
      "title must not be null or empty",
      "meta_description must not be null or empty"
    ],
    "auto_fill_defaults": [
      "If cms_target is missing: default to 'custom'",
      "If schema_markup_type is missing: default to 'Article' for blog-posts",
      "If version is missing: default to 1"
    ],
    "warnings_only": [
      "secondary_keywords missing (export proceeds, logged as warning)",
      "internal_links_count < 2 (export proceeds, logged as warning)",
      "word_count < recommended for type (export proceeds, logged as warning)"
    ]
  }
}

```
