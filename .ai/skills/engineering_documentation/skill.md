```json
{
  "skill_id": "engineering-documentation",
  "name": "Engineering documentation",
  "version": "1.0.0",
  "description": "Technical documentation for scripts, agent contracts, and workspace automation.",
  "cowork_skill": "engineering:documentation",
  "integration_ref": ".ai/skills/skill_integration/skill.md",
  "agents": ["guide-agent"],
  "timestamp": "2026-05-02T00:00:00Z"
}
```

# Engineering documentation

## Sovereign mapping

**`engineering:documentation`** for workspace documentation on request. See **WORKFLOW & QUALITY** in `.ai/skills/skill_integration/skill.md`.

## Protocol

1. Match repo tone: imperative headings, concrete paths, copy-pasteable commands.
2. Cross-link to `AGENTS.md`, phase manifests, and gate scripts only when stable.
3. Avoid secrets; redact env var names as `VAR_NAME` without example values unless public.
