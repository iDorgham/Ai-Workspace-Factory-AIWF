# Publishing Contract — Phase 03: Detailed Design
**Reasoning Hash:** sha256:aiwf-v21-launch-content-03-detailed-design-2026-04-25

---

## Approval Workflow

```
[Brief] → [Founder Review] → [Generate] → [Quality Gate] → [Founder Approve] → [Publish]
           ↑ manual              ↑ CLI          ↑ automated      ↑ manual
```

## Stage Definitions

### Stage 1: Brief (`status: briefed`)
- All fields in content brief are populated
- law_151_flag correctly set
- cli_adapter assigned
- Founder has reviewed hook + proof points

### Stage 2: Generate (`status: generated`)
- CLI adapter has run with prompt from prompt_library/
- Raw output stored in docs/content/launch/{piece_id}_raw.md
- No editing at this stage — raw output only

### Stage 3: Quality Gate (`status: gated`)
- SEO score ≥ 85%
- Brand voice score ≥ 92%
- Readability ≥ 65 (Flesch-Kincaid)
- Originality ≤ 15%
- If gate FAILS: revise prompt → regenerate → re-gate (max 2 cycles)
- If gate still FAILS after 2 cycles: escalate to manual rewrite

### Stage 4: Published (`status: published`)
- Content posted to channel per distribution_contract.md
- URL logged in docs/content/launch/publish_log.md
- Mirror sync triggered: factory/library/planning/content/ updated

## Rollback Rule
If published content requires retraction: update publish_log.md with RETRACTED status + reason. Never delete published URLs.
