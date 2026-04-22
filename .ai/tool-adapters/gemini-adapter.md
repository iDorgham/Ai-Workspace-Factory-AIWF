# Gemini Adapter — Sovereign Universal Tool Interface
**Implements:** `interface.json` v1.0.0  
**Tool ID:** `gemini`  
**Last Updated:** 2026-04-13

---

## Tool Profile

| Property | Value |
|----------|-------|
| **Tool Name** | Google Gemini (gemini-2.0-flash, gemini-pro) |
| **Execution Mode** | Async (streaming + callback-ready) |
| **Interface Version** | 1.0.0 |
| **Platform** | Cloud-hosted (Google) |

---

## Capabilities

✅ Reasoning (multi-step, similar to Claude)  
✅ Code generation (Python, JavaScript, SQL)  
❌ Code execution (no sandbox; must use external runtime)  
❌ Direct file I/O (API-only, no native file access)  
✅ API calls (via Python tool in Bash)  
✅ Multimodal (text + images + video + audio; **competitive advantage vs Claude**)  
✅ Streaming (native streaming API)  
✅ Function calling (via Google Tools API)

---

## Constraints

| Constraint | Value | Notes |
|-----------|-------|-------|
| **Context Window** | 1,000,000 tokens | 5x Claude; excellent for large doc analysis |
| **Max Output Tokens** | 8,192 per call | Better for long-form content |
| **Rate Limit** | ~60 requests/min (standard) | Generous; lower than Claude |
| **Timeout** | ~600s | Longer timeout for multimodal processing |
| **Auth Required** | Yes | API key (Google Cloud project) |
| **Local Setup Required** | No | Cloud-native |

---

## Command Input Schema

**Format:** JSON (structured API calls, not conversational)  
**Transport:** HTTP POST to `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent`  
**Authentication:** API key (environ or header)

### Example Input
```json
{
  "command": "/create blog-posts about sustainable interior design",
  "agent": "creator-agent",
  "tool_id": "gemini",
  "context": {
    "brand_voice": "content/sovereign/reference/brand-voice/style-rules.md (loaded)",
    "keyword_map": "content/sovereign/_references/keyword-maps.md (loaded)",
    "images": [
      {
        "path": "content/assets/[slug]-[index].webp",
        "media_type": "image/webp",
        "alt_text": "Reclaimed wood dining table in modern living room"
      }
    ],
    "competitor_data": "content/sovereign/scraped/[top-3]/scraped/content/blog/ (path pointers)"
  },
  "parameters": {
    "content_type": "blog_posts",
    "topic": "sustainable interior design",
    "variants": 3,
    "include_images": true,
    "target_audience": "eco-conscious homeowners"
  }
}
```

**Transport Details:**
- Direct JSON API call (no conversational wrapper)
- Images passed as base64 or file URIs
- Async mode: response includes `operation_id` for polling

---

## Command Output Schema

**Format:** JSON (structured) + Markdown content  
**Transport:** HTTP response or callback webhook  

### Standard Output Structure
```json
{
  "status": "success",
  "tool_id": "gemini",
  "execution_time_ms": 4200,
  "data": {
    "content": [
      {
        "type": "blog_post",
        "slug": "sustainable_interior_design_1",
        "title": "...",
        "body": "...",
        "frontmatter": {
          "author": "Sovereign Team",
          "created_at": "2026-04-13T10:22:00+02:00",
          "version": 1,
          "originality_score": 0.97,
          "tone_score": 0.95,
          "includes_images": true
        }
      }
    ],
    "validation": {
      "brand_voice_compliance": 0.94,
      "semantic_similarity_to_competitors": 0.08,
      "readability_flesch_kincaid": 68
    }
  },
  "state_update": {
    "last_command": "/create blog-posts",
    "last_agent": "creator-agent",
    "pending_review": ["content/sovereign/blog-posts/[slug].md", "post_2_gemini.md", "post_3_gemini.md"]
  },
  "metadata": {
    "model": "gemini-2.0-flash",
    "tokens_used": 18420,
    "images_processed": 3,
    "next_step": "/polish content in content/"
  }
}
```

### Required Output Fields
- `status`: "success" | "partial" | "failed"
- `tool_id`: "gemini"
- `execution_time_ms`: Elapsed time
- `data`: Content (blog posts, optimized images, etc.)
- `validation`: Quality metrics (brand voice, originality, readability)
- `state_update`: State changes
- `metadata`: Model used, tokens, next step

---

## State Sync Protocol

**Reads State Before:** ✅ YES  
**Writes State After:** ✅ YES  
**State File:** `.ai/memory/multi-tool-state/gemini.session.json`  
**Lock Mechanism:** JSON lock with timestamp verification  
**Conflict Resolution:** Optimistic locking (retry if timestamp mismatch)

### State Read Flow
1. guide-agent loads `.ai/memory/state.json` + `.ai/memory/multi-tool-state/gemini.session.json`
2. Attaches to JSON request body
3. Gemini executes with awareness of pipeline state
4. Outputs state update in JSON response

### State Write Flow
1. After command completes, Gemini returns:
   ```json
   {
     "state_update": {
       "timestamp": "2026-04-13T10:22:00+02:00",
       "last_command": "/create blog-posts",
       "pipeline_stage": "content_creation",
       "last_agent": "creator-agent",
       "active_content": {
         "last_created": "content/sovereign/blog-posts/[slug].md",
         "pending_review": [...]
       }
     }
   }
   ```
2. guide-agent compares `timestamp` with existing in `.ai/memory/multi-tool-state/gemini.session.json`
3. If Gemini's timestamp > existing, merge patch into both JSON files
4. If conflict (simultaneous writes from Claude + Gemini), apply `version_branch` resolution:
   - Claude's result: `content/sovereign/blog-posts/[slug]_[tool]_v[version].md`
   - Gemini's result: `content/sovereign/blog-posts/[slug]_[tool]_v[version].md`
   - Merge logic deferred to human review or explicit `/merge` command

---

## File Ownership Rules

### Can Write To
- ✅ `content/` — creator-agent primary (Gemini operating as creator-agent)
- ✅ `content/assets/[asset]` — Can optimize/add images (via seo-agent role)
- ✅ `content/[type]/seo-meta.json` — seo-agent secondary
- ✅ `.ai/logs/workflow.jsonl` — append only
- ✅ `.ai/memory/multi-tool-state/gemini.session.json` — tool-specific state

### Cannot Write To
- ❌ `content/sovereign/scraped/` — research/scraper-agent owns exclusively
- ❌ `content/sovereign/reference/brand-voice/*` — brand-agent owns
- ❌ Other tools' session files (`claude.session.json`, `copilot.session.json`)
- ❌ Overwrite files (must version)

### Ownership Awareness
Gemini must:
1. Check `.ai/data-ownership.md` before any write
2. Always version outputs: `[slug]_gemini_v1.md`, `_gemini_v2.md`, etc.
3. Respect creator-agent's primary ownership of `content/`
4. On write conflict (two tools write to same file), suffix with tool ID

---

## Error Handling

**Error Format:** JSON with detailed error context  
**Timeout Behavior:** Return partial results + mark for retry  
**Retry Logic:** Exponential backoff (2s → 10s → 20s → abort)  
**Fallback Enabled:** ✅ YES (guide-agent can reroute to Claude or Codex on failure)

### Error Response Example
```json
{
  "status": "failed",
  "error": {
    "code": "api_overloaded",
    "message": "Google API rate limit exceeded. Retry in 30s.",
    "recovery": "Auto-fallback to Claude enabled.",
    "tool_id": "gemini",
    "timestamp": "2026-04-13T10:22:00+02:00",
    "fallback_agent": "claude"
  }
}
```

### Common Failure Modes & Recovery
| Error | Cause | Recovery |
|-------|-------|----------|
| `api_overloaded` | Rate limit hit | Exponential backoff; fallback to Claude |
| `invalid_image` | Image cannot be processed | Skip image, continue with text-only output |
| `context_too_large` | > 1M tokens | Summarize context cache; retry |
| `api_key_invalid` | Bad authentication | guide-agent halts, reports error |
| `originality_low` | Generated content too similar to source | Auto-retry with different prompt; max 2 retries |

---

## Performance Profile

| Metric | Value | Notes |
|--------|-------|-------|
| **Latency (p50)** | ~1200ms | Slightly slower than Claude due to streaming |
| **Latency (p95)** | ~4500ms | Includes image processing overhead |
| **Cost per 1M tokens** | $0.075-0.6 | Gemini 2.0 Flash is very cheap; Pro costs more |
| **Success Rate** | 98.8% | Good; slightly lower than Claude |
| **Cold Start** | 0ms | Cloud-native, always warm |

---

## CLI Integration

**Has CLI:** ✅ YES (via `gcloud` CLI or direct API calls)  
**CLI Binary Path:** N/A (API-first; use `gcloud` wrapper or REST)  
**Example CLI Usage:** See `cli/sovereign-gemini` wrapper  
**Stdin Mode:** ✅ YES (accepts JSON on stdin)  
**JSON Output:** ✅ YES (native JSON output)

### CLI Example
```bash
echo '{"command": "/create blog-posts", "parameters": {...}}' | \
  sovereign-gemini --json-output --async --tool-id gemini
```

---

## Multi-Tool Execution Mode: Best for Multimodal

**Primary Mode:** `async` (Gemini's streaming makes this natural)  
**Fallback Mode:** `fallback` (if API fails, try Claude)  
**Parallel Mode:** `canary` (run Claude + Gemini in parallel, compare outputs for quality)

---

## Competitive Advantages vs Claude

| Aspect | Gemini | Claude |
|--------|--------|--------|
| **Context Window** | 1M tokens | 200k tokens |
| **Multimodal** | ✅ Video, audio, images | ⚠️ Images only |
| **Cost** | ~$0.075-0.6 / 1M tokens | $3-15 / 1M tokens |
| **Output Length** | 8,192 tokens | 4,096 tokens |
| **Reasoning** | Good | Better (o1-style) |
| **Brand Voice Compliance** | ~92% (2nd tier) | ~95% (1st tier) |

**When to Use Gemini:**
- ✅ Processing large documents (>200k tokens)
- ✅ Analyzing images, video, or multi-media content
- ✅ Cost-sensitive workloads (much cheaper)
- ✅ Long-form content generation (larger output window)

**When to Prefer Claude:**
- ✅ Brand voice compliance (stricter adherence)
- ✅ Complex reasoning (o1 capabilities)
- ✅ Multi-step workflows (more reliable)

---

## Integration with Other Adapters

### Gemini → Claude Handoff (Image Cannot Be Processed)
```json
{
  "status": "partial",
  "error": {
    "code": "image_unsupported",
    "message": "Video file not supported. Falling back to Claude for text analysis.",
    "fallback_agent": "claude"
  }
}
```
Claude receives same input minus video; processes text only.

### Claude → Gemini Handoff (Large Document)
```
Claude: "Document too large for context (250k tokens). Switching to Gemini."
guide-agent: Route to gemini-adapter
Gemini: Processes full document with 1M token capacity
```

### Gemini → Codex Handoff (Code Generation)
```
Gemini: "Code generation task routed to Codex (specialized)."
guide-agent: Route to codex-adapter
Codex: Generates optimized code
```

---

## Workspace Integration Checklist

- ✅ Reads `.ai/memory/state.json` + `.ai/memory/multi-tool-state/gemini.session.json`
- ✅ Loads context cache summaries (never raw files)
- ✅ Respects `.ai/data-ownership.md` for file writes
- ✅ Versions all outputs with `_gemini` suffix
- ✅ Appends to logs (never overwrites)
- ✅ Outputs structured JSON for state updates
- ✅ Handles concurrent writes via `version_branch` conflict resolution
- ✅ Implements error recovery with fallback routing
- ✅ Tracks execution time and token usage
- ✅ Validates against quality gates
- ✅ Enforces pipeline order

---

## Implementation Notes for guide-agent

1. **When dispatching to Gemini:**
   - Prepare JSON request body (not conversational prompt)
   - Attach images as base64 or file URIs
   - Include state JSON in `context` field
   - Use `async: true` for long-running tasks

2. **When receiving Gemini's output:**
   - Parse JSON response
   - Extract content array (multiple outputs possible)
   - Merge state update into `.ai/memory/state.json`
   - If filename conflict (same slug from Claude), apply `_gemini` suffix
   - Log to `.ai/logs/workflow.jsonl`

3. **On rate limit (429):**
   - Retry with exponential backoff
   - If persistent, fallback to Claude
   - Log rate limit event to `.ai/logs/workflow.jsonl`

4. **On image processing failure:**
   - Skip image, continue with text-only output
   - Log which images failed
   - Flag for manual review

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-04-13 | Initial adapter spec for Phase 1; multimodal focus |

