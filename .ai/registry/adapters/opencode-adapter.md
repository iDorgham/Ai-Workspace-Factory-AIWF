# OpenCode CLI Adapter
**Execution Mode:** CLI  
**Context Window:** 16,000 tokens  
**Cost:** Free (open source)  
**Avg Latency:** 5.0s  
**Success Rate:** 92%  

---

## Specification

### Input Format
```bash
opencode --prompt "[prompt]" --model [model] --output json
```

### Output Format
```json
{
  "status": "success",
  "content": "generated text",
  "tokens_input": 2000,
  "tokens_output": 1000,
  "cost_usd": 0,
  "duration_ms": 5000,
  "quality_metrics": {
    "brand_voice": 0.85,
    "originality": 0.91,
    "readability": 0.84
  }
}
```

### State Sync Protocol
- Read: `.ai/memory/multi-tool-state/opencode.session.json`
- Check: Tokens < 16,000
- After: Update state (no cost tracking needed)
- Write: Session file

### Error Handling
- **Timeout (>15s):** Fallback
- **Model not found:** Retry with default model
- **Quality issues:** Acceptable for fallback (85% brand voice)

### File Ownership Rules
Can write: `content/[type]/[slug]_opencode_v[n].md`

### Characteristics
- **Strengths:** Free, no API keys, self-hosted possible
- **Weaknesses:** Slower (5s), lower quality (85% brand voice)
- **Best for:** Cost-free fallback, dev environments, private deployments
- **Avoid:** Production critical paths (slower, lower quality)

---

## Status: Not Installed
This tool is available but not currently installed in Sovereign.

To enable:
```bash
pip install opencode-cli
opencode --setup
opencode --test
```

## Ranking
- Rank 5 (emergency fallback, only if others fail)
- Good for development/testing (no cost)
- Not recommended for production
