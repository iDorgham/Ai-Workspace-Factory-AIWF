```json
{
  "skill_id": "content-architecture",
  "name": "Content Architecture",
  "version": "1.0.0",
  "description": "Defines the structural patterns for website content systems — sitemaps, section naming conventions, multilingual folder hierarchies, and component mapping.",
  "commands": ["/plan content", "/content"],
  "agents": ["content-planner-agent", "spec-architect"],
  "protocols": [
    "Section files must use naming convention: {index}-{component-slug}.md",
    "Each page must have a folder containing section files and a full-page.md aggregate",
    "Legal pages are always placed in the /legal/ root folder",
    "Sitemap must be generated at workspace root as sitemap.md",
    "Bilingual pages must mirror exact folder structure per locale (/en/, /ar-eg/)"
  ],
  "templates": [
    ".ai/templates/content-discovery/discovery-interview.json",
    ".ai/templates/content-discovery/content-plan-template.md"
  ],
  "scripts": [
    "factory/scripts/plan_content.py",
    "factory/core/content_engine.py"
  ],
  "timestamp": "2026-04-23T18:06:00+02:00"
}
```
