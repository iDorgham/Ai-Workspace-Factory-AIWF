# Antigravity IDE Adapter
**Execution Mode:** IDE-Integrated (NOT CLI)  
**Context Window:** Unlimited (IDE-managed)  
**Cost:** TBD (IDE licensing)  
**Avg Latency:** Variable (IDE-dependent)  
**Success Rate:** TBD  

---

## Important Note

**Antigravity is IDE-based, not CLI-based.**

It does NOT execute via `/create blog-posts --tool antigravity` flag.

Instead, users invoke it directly within the Antigravity IDE environment.

---

## Architecture

### Integration Points

1. **IDE Native** — User activates Antigravity IDE
2. **Commands Available** — All Sovereign commands work within IDE
3. **Output Handling** — IDE manages file creation and state
4. **State Sync** — Manual or auto-sync back to workspace

### Execution Model

```
User in Antigravity IDE
        │
        └─> /create blog-posts
            (command runs in IDE context)
            │
            └─> Generates content
            │
            └─> Creates: content/sovereign/blog-posts/[slug]_[tool]_v[version].md
            │
            └─> Optional: Sync back to workspace
```

### Characteristics

- **Strengths:** IDE-integrated, visual, interactive editing
- **Weaknesses:** Not accessible via CLI flags, requires IDE
- **Best for:** Manual/interactive content creation
- **Avoid:** Batch automation (CLI tools better)

---

## Integration Path

Phase 2a focuses on CLI tools (6 tools).

Antigravity IDE integration planned for Phase 2c (IDE Integration Layer).

---

## No CLI Interface

This adapter explicitly has **no CLI entry point**.

The following will error:
```bash
/create blog-posts --tool antigravity
# Error: Antigravity is IDE-based, not CLI-callable
```

---

## State Syncing

If using Antigravity IDE within Sovereign workspace:

1. Create content in IDE
2. Files saved to: `content/sovereign/blog-posts/[slug]_[tool]_v[version].md`
3. Optional sync: Merge back to workspace
4. State updates: Manual or via workspace sync

---

## Future (Phase 2c)

When IDE integration is planned:
- Create: `.ai/ide-layer/antigravity_integration.md`
- Define: IDE-specific state management
- Specify: How IDE commands map to workspace
