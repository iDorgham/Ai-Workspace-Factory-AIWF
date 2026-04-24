# Copilot CLI Adapter
**Execution Mode:** CLI  
**Context Window:** 8,192 tokens  
**Cost:** $0.003 per 1M input, $0.004 per 1M output  
**Avg Latency:** 3.5s  
**Success Rate:** 97%  

---

## Specification

### Input Format
```bash
copilot --prompt "[prompt]" --context "[context_path]" --output json
```

### Output Format
```json
{
  "status": "success",
  "content": "generated text",
  "tokens_input": 2400,
  "tokens_output": 1200,
  "cost_usd": 0.005,
  "duration_ms": 3500,
  "quality_metrics": {
    "brand_voice": 0.94,
    "originality": 0.97,
    "readability": 0.89
  }
}
```

### State Sync Protocol

**Before execution:**
1. Read: `.ai/memory/multi-tool-state/copilot.session.json`
2. Check: `tokens_used_this_session + estimated_tokens < 8192`
3. Reserve: 10% buffer

**After execution:**
1. Increment: `tokens_used_this_session` (add tokens_input + tokens_output)
2. Increment: `cost_usd_this_session` (add cost_usd)
3. Append: `execution_history` entry
4. Update: `performance_metrics` averages
5. Write: `.ai/memory/multi-tool-state/copilot.session.json`

### Error Handling
- **Timeout (>300s):** Consider failed, trigger fallback
- **API error:** Log error, suggest retry or fallback
- **Low quality (<85% brand voice):** Retry with refined prompt OR trigger fallback
- **Rate limit:** Pause 60s, retry once, then fallback

### File Ownership Rules
**Can write:**
- `content/[type]/[slug]_copilot_v[n].md` (creation)
- `content/[type]/[slug].md` (optimization, in-place)

**Cannot write:**
- `reference/` (read-only)
- `.ai/` (read-only, except state files)
- `logs/` (only via guide-agent)

### Quality Gates (Applies To)
- Blog posts (brand voice critical)
- Website pages (originality required)
- Comparisons (analysis quality)

### Execution Flow
```
1. Load adapter (0.01s)
2. Validate input (0.01s)
3. Load context (0.1s)
4. Build prompt (0.05s)
5. Invoke Copilot CLI (3.5s)
6. Parse output (0.05s)
7. Quality checks (0.1s)
8. Update state (0.05s)
9. Log metrics (0.05s)
──────────────
Total: ~3.87s
```

### Characteristics
- **Strengths:** High quality content, good brand voice, fast
- **Weaknesses:** Moderate cost, smaller context window
- **Best for:** Content creation, brand-aligned output
- **Avoid:** Very large documents (context limited to 8KB)

---

## Environment Requirements

```bash
# Installation
pip install copilot-cli

# Configuration
export COPILOT_API_KEY=sk_...
export COPILOT_MODEL=copilot-v3

# Verification
copilot --version
```

## Rate Limits
- 100 requests per minute (burst to 200)
- Backoff: 60s on rate limit error

## Billing Model
- Per-token pricing (input/output separate)
- Monthly statement aggregates all usage
- No minimum spend

---

## Integration Notes

Copilot is Rank 1 for content creation tasks (blog posts, website pages) due to:
- Strong brand voice alignment (94% average)
- Fast execution (3.5s)
- Reasonable cost for quality ($0.003-$0.004)
- High success rate (97%)

Falls back to Codex if timeout or quality issues.
