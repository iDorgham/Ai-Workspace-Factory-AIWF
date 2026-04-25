# Qwen CLI Adapter
**Execution Mode:** CLI  
**Context Window:** 32,000 tokens  
**Cost:** $0.0001 per 1M input, $0.0002 per 1M output (Cheapest!)  
**Avg Latency:** 4.2s  
**Success Rate:** 94%  

---

## Specification

### Input Format
```bash
qwen --prompt "[prompt]" --max-tokens 8000 --output json
```

### Output Format
```json
{
  "status": "success",
  "content": "generated text",
  "tokens_input": 3200,
  "tokens_output": 1500,
  "cost_usd": 0.0005,
  "duration_ms": 4200,
  "quality_metrics": {
    "brand_voice": 0.88,
    "originality": 0.93,
    "readability": 0.86
  }
}
```

### State Sync Protocol
- Read: `.ai/memory/multi-tool-state/qwen.session.json`
- Check: Tokens < 32,000
- After: Update state with tokens, cost, history
- Write: Session file

### Error Handling
- **Timeout (>10s):** Fallback (Qwen is slower but reliable)
- **Quality issues:** Acceptable (88% brand voice vs 94% for Copilot)
- **Context exceeded:** Reduce input and retry

### File Ownership Rules
Can write: `content/[type]/[slug]_qwen_v[n].md`

### Characteristics
- **Strengths:** Dirt cheap ($0.0001), 32K context, reliable
- **Weaknesses:** Slower (4.2s), slightly lower quality (88% brand voice)
- **Best for:** Rank 4 (fallback), bulk operations, cost-critical work
- **Avoid:** When quality is paramount

---

## Environment Requirements
```bash
pip install qwen-cli
export QWEN_API_KEY=...
qwen --version
```

## Ranking
- Rank 4 fallback (after Copilot, Codex, Gemini)
- Preferred for bulk operations (>50 items)
- Good for cost-optimized pipelines

## Use Cases
- Bulk content generation
- SEO analysis
- Template generation
- Cost-optimized fallback
