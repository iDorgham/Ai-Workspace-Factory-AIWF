# Kilo Code CLI Adapter
**Execution Mode:** CLI  
**Context Window:** 8,000 tokens  
**Cost:** Custom pricing (contact Kilo)  
**Avg Latency:** 3.8s  
**Success Rate:** 95%  

---

## Specification

### Input Format
```bash
kilo --prompt "[prompt]" --api-key $KILO_API_KEY --output json
```

### Output Format
```json
{
  "status": "success",
  "content": "generated text",
  "tokens_input": 1500,
  "tokens_output": 900,
  "cost_usd": null,
  "duration_ms": 3800,
  "quality_metrics": {
    "brand_voice": 0.90,
    "originality": 0.94,
    "readability": 0.86
  }
}
```

### State Sync Protocol
- Read: `.ai/memory/multi-tool-state/kilo.session.json`
- Check: Tokens < 8,000, API key present
- After: Update state (cost tracking TBD with Kilo)
- Write: Session file

### Error Handling
- **Timeout (>8s):** Fallback
- **API key invalid:** Error with setup instructions
- **Quality acceptable:** 90% brand voice (good for fallback)

### File Ownership Rules
Can write: `content/[type]/[slug]_kilo_v[n].md`

### Characteristics
- **Strengths:** Fast (3.8s), good quality (90%), unique models
- **Weaknesses:** Requires API key setup, custom pricing unknown
- **Best for:** Rank 6 (fallback), if/when fully integrated
- **Avoid:** Until pricing/integration complete

---

## Status: Not Installed
Requires API key setup before use.

To enable:
```bash
pip install kilo-code-cli
export KILO_API_KEY=...
kilo --test
```

## Ranking
- Rank 6 (fallback, requires setup)
- Good alternative when available
- Integration pending
