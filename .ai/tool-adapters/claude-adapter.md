# Claude Adapter — Sovereign Universal Tool Interface
**Implements:** `interface.json` v1.0.0  
**Tool ID:** `claude`  
**Last Updated:** 2026-04-13

---

## Tool Profile

| Property | Value |
|----------|-------|
| **Tool Name** | Claude (claude.ai) |
| **Execution Mode** | Interactive (conversational) |
| **Interface Version** | 1.0.0 |
| **Platform** | Cloud-hosted (Anthropic) |

---

## Capabilities

✅ Reasoning  
✅ Code generation (Python, shell, etc.)  
❌ Code execution (sandboxed only in Claude Code)  
❌ Direct file I/O (reads/writes via MCP adapter)  
✅ API calls (via Bash tool in sandboxed environment)  
❌ Multimodal (text + images only; no video/audio)  
✅ Streaming (via claude.ai interface)  
✅ Function calling (tool use)

---

## Constraints

| Constraint | Value | Notes |
|-----------|-------|-------|
| **Context Window** | 200,000 tokens | Ample for full workspace context |
| **Max Output Tokens** | 4,096 per turn | Sufficient for structured output |
| **Rate Limit** | Varies by plan | Free: ~3-5 requests/min; Pro: higher |
| **Timeout** | ~300s | Typical response time 2-8s |
| **Auth Required** | Yes | API key or session token |
| **Local Setup Required** | No | Cloud-native |

---

## Command Input Schema

**Format:** Natural language (conversational)  
**Transport:** HTTP POST to claude.ai or API endpoint  
**Authentication:** Bearer token (API) or session cookie (Web)

### Example Input
```
User: "/create blog-posts about sustainable interior design"

guide-agent context injection:
{
  "command": "/create blog-posts about sustainable interior design",
  "agent": "creator-agent",
  "context": {
    "brand_voice": "content/sovereign/reference/brand-voice/style-rules.md (loaded)",
    "keyword_map": "content/sovereign/_references/keyword-maps.md (loaded)",
    "competitor_data": "content/sovereign/scraped/[top-3]/scraped/content/blog/ (path pointers)",
    "market_positioning": "content/sovereign/reference/market-positioning.md (loaded)"
  },
  "parameters": {
    "content_type": "blog_posts",
    "topic": "sustainable interior design",
    "variants": 3,
    "target_audience": "eco-conscious homeowners"
  }
}
```

**Transport Details:**
- **Web Interface:** User types command naturally; guide-agent parses and injects context
- **API:** JSON POST to `https://api.anthropic.com/v1/messages` with system + user prompt

---

## Command Output Schema

**Format:** Markdown + YAML frontmatter  
**Transport:** HTTP response (streaming or buffered) + file writes via workspace I/O

### Standard Output Structure
```markdown
✅ Command completed: /create blog-posts
→ Generated 3 blog posts: post_1.md, post_2.md, post_3.md
→ Saved to: content/sovereign/blog-posts/
→ Brand voice compliance: 94%
→ Originality score: 97%

[Detailed output below]

---

## Post 1: [Title]
[Markdown content with YAML frontmatter]
...

💡 Suggested Next Step:
/polish content in content/
```

### Required Output Fields
Every Claude response includes:
- `status`: "success" | "partial" | "failed"
- `data`: Actual content (Markdown, JSON, etc.)
- `execution_time_ms`: How long the command took
- `tool_id`: "claude"
- `validation_scores`: Brand voice, originality, readability, etc.
- `next_step`: Suggested command

---

## State Sync Protocol

**Reads State Before:** ✅ YES  
**Writes State After:** ✅ YES  
**State File:** `.ai/memory/multi-tool-state/claude.session.json`  
**Lock Mechanism:** File-based (optimistic locking)  
**Conflict Resolution:** Last-write-wins (with timestamp comparison)

### State Read Flow
1. guide-agent loads `.ai/memory/state.json` + `.ai/memory/multi-tool-state/claude.session.json`
2. Injects into system prompt context
3. Claude operates with full awareness of pipeline state
4. Upon command completion, Claude outputs state update

### State Write Flow
1. After command completes, Claude outputs:
   ```json
   {
     "action": "update_state",
     "state_patch": {
       "last_command": "/create blog-posts",
       "last_command_at": "2026-04-13T10:22:00+02:00",
       "pipeline_stage": "content_creation",
       "last_agent": "creator-agent",
       "active_content": {
         "last_created": "content/sovereign/blog-posts/[slug].md",
         "pending_review": ["content/sovereign/blog-posts/[slug].md", "post_2.md", "post_3.md"]
       }
     }
   }
   ```
2. guide-agent merges patch into `state.json` + `claude.session.json`
3. Timestamps compared; write only if Claude's timestamp > existing

---

## File Ownership Rules

### Can Write To
- ✅ `content/` — creator-agent primary (Claude operating as creator-agent)
- ✅ `content/[type]/seo-meta.json` — seo-agent secondary (when optimizing)
- ✅ `.ai/logs/workflow.jsonl` — append only
- ✅ `.ai/memory/multi-tool-state/claude.session.json` — tool-specific state

### Cannot Write To
- ❌ `content/sovereign/scraped/` — research/scraper-agent owns
- ❌ `content/sovereign/reference/brand-voice/*` — brand-agent owns
- ❌ Other tools' session files (`.ai/memory/multi-tool-state/gemini.session.json`, etc.)

### Ownership Awareness
Before any write, Claude must:
1. Check `.ai/data-ownership.md` to confirm write permission
2. Respect versioning rules (never overwrite; version as `_v2.md`, `_v3.md`)
3. If write not permitted, halt and report: "I cannot write to [path]. Permission denied (owned by [agent])."

---

## Error Handling

**Error Format:** JSON + markdown explanation  
**Timeout Behavior:** Return partial results + flag for retry  
**Retry Logic:** Exponential backoff (2s → 10s → 20s → abort)  
**Fallback Enabled:** ✅ YES (guide-agent can reroute to Gemini on failure)

### Error Response Example
```json
{
  "status": "failed",
  "error": {
    "code": "context_insufficient",
    "message": "Missing brand voice rules. Cannot proceed.",
    "recovery": "Run /brand to define your voice first.",
    "tool_id": "claude",
    "timestamp": "2026-04-13T10:22:00+02:00"
  }
}
```

### Common Failure Modes & Recovery
| Error | Cause | Recovery |
|-------|-------|----------|
| `brand_voice_missing` | No `style-rules.md` | Run `/brand` first |
| `insufficient_context` | Keyword maps not loaded | guide-agent reloads cache |
| `timeout` | Response takes >300s | Retry with narrower scope |
| `file_write_denied` | No write permission | Fallback to tool with permission |
| `semantic_similarity_high` | Generated content too similar to competitor | Retry with structural shift |

---

## Performance Profile

| Metric | Value | Notes |
|--------|-------|-------|
| **Latency (p50)** | ~800ms | Typical response time |
| **Latency (p95)** | ~3000ms | Includes token streaming |
| **Cost per 1M tokens** | $3-15 | Depends on model (Opus, Sonnet, Haiku) |
| **Success Rate** | 99.5% | Highly reliable |
| **Cold Start** | 0ms | Cloud-native, always warm |

---

## CLI Integration

**Has CLI:** ✅ YES (`claude-code` CLI exists; web interface is primary)  
**CLI Binary Path:** N/A (web-first tool)  
**Example CLI Usage:** (See `claude-code-adapter.md` for true CLI support)  
**Stdin Mode:** ❌ NO (conversational only)  
**JSON Output:** ✅ YES (via structured output in response)

---

## Multi-Tool Execution Mode: Default for Claude

**Primary Mode:** `sequential` (Claude is synchronous, single-threaded)  
**Fallback Mode:** `fallback` (if Claude fails, try Gemini or Codex)  
**Cannot Parallel:** ❌ (no concurrent requests supported per session)

---

## Integration with Other Adapters

### Claude → Gemini Handoff
If Claude exhausts context or hits token limit mid-task:
```
Claude: "Context exhausted. Falling back to Gemini for continuation."
guide-agent: Reroute to gemini-adapter
Gemini: Reads claude.session.json + claude's partial output, continues
```

### Claude ← Gemini Handoff
If Gemini fails on visual analysis:
```
Gemini: "Cannot analyze image [path]. Falling back to Claude."
guide-agent: Reroute to claude-adapter
Claude: Attempts text-only fallback analysis
```

---

## Workspace Integration Checklist

- ✅ Reads `.ai/memory/state.json` before each command
- ✅ Loads `.ai/memory/context-cache/*` summaries (never raw files)
- ✅ Respects `.ai/data-ownership.md` for file writes
- ✅ Versions all content outputs (`_v2.md`, `_v3.md`, etc.)
- ✅ Appends to logs (never overwrites)
- ✅ Outputs structured JSON for state updates
- ✅ Implements error recovery with fallback routing
- ✅ Tracks execution time in all outputs
- ✅ Validates against quality gates (SEO, brand voice, originality)
- ✅ Enforces pipeline order (no Export before Approve)

---

## Implementation Notes for guide-agent

1. **When dispatching to Claude:**
   - Load `.ai/memory/state.json` + `.ai/memory/multi-tool-state/claude.session.json`
   - Inject brand voice context if `/create` or `/polish` command
   - Include competitor data pointers (not full content)
   - Set temperature/mode based on task (reasoning = 0.5, creative = 0.8)

2. **When receiving Claude's output:**
   - Extract structured JSON section (if present)
   - Merge state patch into `.ai/memory/state.json`
   - Log action to `.ai/logs/workflow.jsonl`
   - Suggest next step from Claude's recommendation

3. **On timeout (>300s):**
   - Buffer partial response
   - Ask Claude to summarize progress
   - Offer to continue with narrower scope or fallback tool

4. **On failure:**
   - Check error code in JSON response
   - If recoverable (e.g., `brand_voice_missing`), fix and retry
   - If not recoverable, reroute to `gemini-adapter` with full context

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-04-13 | Initial adapter spec for Phase 1 |

