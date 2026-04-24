# Codex CLI Adapter
**Execution Mode:** CLI  
**Context Window:** 4,096 tokens  
**Cost:** $0.002 per 1M input, $0.0004 per 1M output  
**Avg Latency:** 2.5s  
**Success Rate:** 96%  

---

## Specification

### Input Format
```bash
codex --prompt "[prompt]" --max-tokens 2048 --output json
```

### Output Format
```json
{
  "status": "success",
  "content": "generated text",
  "tokens_input": 1200,
  "tokens_output": 800,
  "cost_usd": 0.002,
  "duration_ms": 2500,
  "quality_metrics": {
    "brand_voice": 0.91,
    "originality": 0.96,
    "readability": 0.87
  }
}
```

### State Sync Protocol
- Read: `.ai/memory/multi-tool-state/codex.session.json`
- Check: `tokens_used_this_session + estimated < 4096`
- After: Increment tokens, cost, execution_history
- Write: Session state file

### Error Handling
- **Timeout (>5s):** Trigger fallback (Codex is fast, timeout is critical)
- **Output truncation:** Retry with lower max-tokens
- **Low quality:** Try Gemini fallback
- **Context exceeded:** Reduce input, then retry

### File Ownership Rules
Same as Copilot: Can write `content/[type]/[slug]_codex_v[n].md`

### Quality Gates
Applies to: Blog posts, website pages, comparisons

### Execution Flow
```
1. Load adapter (0.01s)
2. Validate input (0.01s)
3. Load context (0.05s)
4. Build prompt (0.03s)
5. Invoke Codex CLI (2.5s)
6. Parse output (0.03s)
7. Quality checks (0.1s)
8. Update state (0.05s)
9. Log metrics (0.05s)
──────────────
Total: ~2.83s
```

### Characteristics
- **Strengths:** Cheapest, fastest, good quality, smallest overhead
- **Weaknesses:** Lowest brand voice (91%), smallest context
- **Best for:** Fallback (Rank 2), bulk operations, analysis
- **Avoid:** Very nuanced brand content (prefer Copilot)

---

## Environment Requirements

```bash
pip install codex-cli
export CODEX_API_KEY=...
codex --version
```

## Rate Limits
- 200 requests per minute
- Generous backoff policy

## Ranking
- Rank 2 for most commands (best fallback)
- Preferred for bulk operations due to cost
- Good secondary for all content types

---

## Fallback Chains
- Falls back to Gemini if quality gate fails
- Falls back to Qwen if costs critical
