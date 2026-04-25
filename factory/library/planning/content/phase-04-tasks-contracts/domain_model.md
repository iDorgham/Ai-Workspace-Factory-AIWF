# Domain Model — Phase 04: Tasks + Contracts
**Reasoning Hash:** sha256:aiwf-v21-launch-content-04-tasks-contracts-2026-04-25

---

## 1. Production Pipeline Model

```
[Brief] ──→ [CLI Prompt] ──→ [Adapter Execution] ──→ [Raw Output]
                                                           │
                                                    [Quality Gate]
                                                           │
                                             ┌─────────────┴──────────────┐
                                          PASS                          FAIL
                                             │                             │
                                    [docs/content/launch/]        [Revise Prompt]
                                             │                    [Regenerate (max 2x)]
                                    [publish_log.md]
```

## 2. Task Registry — All 12 Production Tasks

| Task ID | Piece ID | Title | CLI | Day | Dependencies |
|---------|----------|-------|-----|-----|--------------|
| T-C04-01 | C-01-README | Generate GitHub README v21 | claude | 1 | Phase 03 brief |
| T-C04-02 | C-02-LI-LAUNCH | Generate LinkedIn launch post | claude | 1 | T-C04-01 (README must exist first) |
| T-C04-03 | C-03-X-LAUNCH | Generate X launch thread | claude | 1 | T-C04-01 |
| T-C04-04 | C-04-LI-12SPEC | Generate LinkedIn spec post | claude | 3 | T-C04-01 |
| T-C04-05 | C-05-X-ARCH | Generate X architecture post | claude | 5 | T-C04-01 |
| T-C04-06 | C-06-LI-LAW151 | Generate LinkedIn Law 151 post | claude | 7 | none |
| T-C04-07 | C-07-AR-LI | Generate Arabic LinkedIn (Qwen) | qwen | 7 | Law 151 anonymisation |
| T-C04-08 | C-08-AR-MENA | Generate Arabic community post (Qwen) | qwen | 7 | Law 151 anonymisation |
| T-C04-09 | C-09-DEVTO | Generate Dev.to deep-dive | claude | 10 | T-C04-01 |
| T-C04-10 | C-10-LI-7CLI | Generate LinkedIn 7-CLI post | claude | 14 | none |
| T-C04-11 | C-11-X-MULTILLL | Generate X multi-LLM thread | claude | 14 | T-C04-10 |
| T-C04-12 | C-12-GH-MENA | Generate GitHub MENA section (Qwen) | qwen | 21 | T-C04-07, T-C04-08 |

## 3. Output File Structure

```
docs/content/launch/
├── C-01-README_raw.md          ← raw CLI output
├── C-01-README_final.md        ← post-gate approved version
├── C-02-LI-LAUNCH_raw.md
├── C-02-LI-LAUNCH_final.md
├── ...                         ← (all 12 pieces × 2 files = 24 files)
├── quality_gate_reports/
│   ├── C-01-README_gate.json
│   ├── ...
└── publish_log.md              ← URL, date, status per piece
```

## 4. Quality Gate Score Model

```json
{
  "piece_id": "C-01-README",
  "seo_score": 0,
  "brand_voice_score": 0,
  "readability_score": 0,
  "originality_score": 0,
  "gate_result": "pending",
  "gate_run_count": 0,
  "reasoning_hash": "sha256:pending"
}
```

## 5. Adapter Assignment Summary

| Adapter | Pieces | Rationale |
|---------|--------|-----------|
| claude | C-01 through C-06, C-09, C-10, C-11 | English content, technical depth |
| qwen | C-07, C-08, C-12 | Arabic-first generation; Law 151 compliant |
| gemini | None (fallback only) | Available if Claude rate-limited |
| kilo | None (Phase 04 primary) | Architecture diagrams if needed |
