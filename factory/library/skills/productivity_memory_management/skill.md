```json
{
  "skill_id": "productivity-memory-management",
  "name": "Memory and session management",
  "version": "1.0.0",
  "description": "Compress, restore, and clear session context; token budget visibility for guide flows.",
  "cowork_skill": "productivity:memory-management",
  "integration_ref": ".ai/skills/skill_integration/skill.md",
  "commands": ["/memory save", "/memory load", "/memory clear", "/budget check"],
  "agents": ["guide-agent", "memory-manager"],
  "timestamp": "2026-05-02T00:00:00Z"
}
```

# Memory and session management

## Sovereign mapping

**`productivity:memory-management`** for `/memory save|load|clear` and `/budget check`. See **MEMORY & SESSION MANAGEMENT** in `.ai/skills/skill_integration/skill.md`.

## Protocol

1. Two-tier model: working memory in `CLAUDE.md` / session scope; fuller notes under `.ai/memory/` when used.
2. **Never** embed raw scraped blobs in saves—summaries and pointers only.
3. Clear operations must not delete immutable ledgers or user-approved specs without confirmation.
