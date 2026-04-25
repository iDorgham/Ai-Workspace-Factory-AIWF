# Content Contract — Phase 04: Tasks + Contracts
**Reasoning Hash:** sha256:aiwf-v21-launch-content-04-tasks-contracts-2026-04-25

## Production Thresholds (inherited from Phase 03 + enforced at generation)

```yaml
seo_score_min: 85
brand_voice_score_min: 92
readability_score_min: 65
originality_max: 15
max_regeneration_cycles: 2
```

## Adapter Execution Rules

**Claude:**
- Temperature: 0.7 for long-form, 0.5 for technical
- Max tokens: 2000 (README/Dev.to), 500 (LinkedIn), 300 (X posts)
- System prompt: `phase-03-detailed-design/prompt_library/system_prompt.md`

**Qwen:**
- Arabic pieces only (C-07, C-08, C-12)
- Anonymisation MUST complete before prompt dispatch
- RTL output expected — verify rendering before gate submission
- Log law_151_flag=true entries with separate tag in tool_performance.jsonl

## Failure Handling

| Failure Type | Action | Escalation |
|-------------|--------|------------|
| Gate fail cycle 1 | Revise prompt, regenerate | None |
| Gate fail cycle 2 | Revise brief + prompt, regenerate | Notify founder |
| Gate fail cycle 3 | Manual rewrite required | Block publish_log update |
| Adapter timeout | Retry once, then switch to fallback | Log error_code in ledger |
| Law 151 anonymisation fail | HARD STOP — do not execute prompt | Escalate immediately |
