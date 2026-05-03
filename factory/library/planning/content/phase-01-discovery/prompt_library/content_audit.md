# CLI Prompt: Content Audit — AIWF v21 Launch

**Task:** T-C01-02 — Audit existing AIWF content assets  
**Works with:** Claude, Gemini, Qwen, Kilo

---

```
AIWF v21.0.0 Planning Request

Planning Type: content
Task: Content Audit — Existing AIWF Assets
Mode: plan-only

Assets to audit (read and score each):
1. README.md — root repository overview
2. .ai/dashboard/index.md — operational dashboard
3. docs/planning/*.md — SDD planning documents (internal governance)
4. .ai/logs/health_audit_report.md — system health report
5. .ai/plan/development/00_prd/2026_04_24_aiwf_v19.0_prd.md — product requirements

For each asset produce:
- Asset name + path
- Content type (overview | technical | governance | status)
- Estimated SEO score (0–100)
- Estimated readability score (Flesch–Kincaid 0–100)
- Brand voice alignment (0–100)
- Key gap vs. external audience needs
- Recommended action (publish as-is | adapt | create new | skip)

Output as a Markdown table.
Note: docs/planning/ files are internal governance — "adapt" means create public-facing version, not expose the raw doc.

Reasoning Hash: sha256:content-audit-aiwf-v21-2026-04-25
```
