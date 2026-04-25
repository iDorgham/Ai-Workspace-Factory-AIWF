# CLI Prompt: Content Brief Generation — Phase 03

**Task:** Generate all 12 content briefs for AIWF v21 Launch Content Strategy
**Works with:** Claude, Gemini, Kilo
**Phase:** 03 — Detailed Design

---

```
AIWF v21.0.0 Planning Request

Planning Type: content
Task: Generate Content Briefs — All 12 Launch Pieces
Phase: 03 — Detailed Design
Mode: plan-only

Context:
- 4 pillars: Sovereignty, Density, MENA-First, Multi-LLM
- 4 personas: Sovereign Builder, Pragmatic Dev, MENA Pioneer, AI Director
- 30-day launch window (see phase-02-blueprint/design.md for calendar)
- Brand voice: authoritative-yet-accessible
- Forbidden: game-changing, revolutionary, disruptive, seamless
- Preferred: sovereign, governance, factory, orchestration

For each of the 12 pieces in the inventory (domain_model.md Section 2), produce a brief with:
- Hook (opening sentence)
- 3 proof points (concrete, data-backed)
- Structure outline (numbered sections)
- CTA (channel-appropriate)
- SEO: primary keyword + 2–3 secondary keywords
- cli_adapter assignment (claude for EN, qwen for AR)
- law_151_flag (true only for C-07, C-08)

Output format: One Markdown file per brief matching the schema in domain_model.md Section 1.

Quality gate targets per contracts/content_contract.md:
- SEO ≥ 85, brand voice ≥ 92, readability ≥ 65

Reasoning Hash: sha256:aiwf-v21-launch-content-03-detailed-design-2026-04-25
```
