```json
{
  "skill_id": "marketing-content-creation",
  "name": "Marketing content creation",
  "version": "1.0.0",
  "description": "Draft blogs, pages, landing copy, and revisions with SEO structure under sovereign templates.",
  "cowork_skill": "marketing:content-creation",
  "integration_ref": ".ai/skills/skill_integration/skill.md",
  "commands": ["/create", "/revise"],
  "agents": ["creator-agent", "content-generator"],
  "timestamp": "2026-05-02T00:00:00Z"
}
```

# Marketing content creation

## Sovereign mapping

**`marketing:content-creation`** for `/create` blog, website, landing, project pages and `/revise [feedback]`. See **CONTENT CREATION** in `.ai/skills/skill_integration/skill.md`.

## Protocol

1. Load `.ai/templates/content-blueprints/[type].md` before drafting when the template exists.
2. All drafts pass **brand-voice** (≥ 92% target) and **originality** (≤ 15%) checks before save.
3. Save to sovereign-owned `content/` paths per command; log significant steps to `workflow.jsonl` when that file is in scope.
