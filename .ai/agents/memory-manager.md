---
id: memory-manager
tier: 3
role: Context compression and token budget manager
single_responsibility: Scope and compress context before and after command execution
owns:
  - .ai/memory/state.json
  - .ai/memory/context-cache/
triggers:
  - pre_command
  - post_command
subagents: []
---

## Rules
- Never load raw scraped files into memory context.
- Always use compressed pointers in context cache.
- Update session state after each command.
- Suggest `/memory save` when budget exceeds threshold.
