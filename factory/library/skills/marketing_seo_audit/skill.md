```json
{
  "skill_id": "marketing-seo-audit",
  "name": "Marketing SEO Audit",
  "version": "1.0.0",
  "description": "SEO scoring for polish and review gates: headings, meta, readability, keyword use against sovereign keyword maps.",
  "cowork_skill": "marketing:seo-audit",
  "integration_ref": ".ai/skills/skill_integration/skill.md",
  "commands": ["/polish", "/optimize images", "/review"],
  "agents": ["seo-agent", "workflow-agent"],
  "timestamp": "2026-05-02T00:00:00Z"
}
```

# Marketing SEO audit

## Sovereign mapping

Invoked as **`marketing:seo-audit`** for `/polish content in content/`, image SEO under `/optimize images in content/`, and the SEO gate in `/review`. See **SEO OPTIMIZATION** in `.ai/skills/skill_integration/skill.md`.

## Protocol

1. Load `content/sovereign/_references/keyword_maps.md` (sovereign keyword source).
2. Audit headings, meta schema (`.ai/templates/seo-meta-templates/meta-template.json` where present), alt text, readability.
3. Emit scores; SEO gate expects **≥ 85%** before pass.
4. Never bypass brand or originality gates; skill output feeds `workflow-agent` / quality-checker only.
