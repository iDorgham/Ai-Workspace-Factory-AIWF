# CLI Prompt: Production Execution — Phase 04

**Task:** Execute multi-CLI content generation for all 12 AIWF v21 launch pieces
**Works with:** Claude (primary), Qwen (Arabic), Gemini (fallback)

---

```
AIWF v21.0.0 Content Production Request

Planning Type: content
Phase: 04 — Tasks + Contracts
Mode: execute

Execute production for piece: [PIECE_ID]

Brief location: .ai/plan/content/phase-03-detailed-design/templates/content_briefs/[PIECE_ID].md

Instructions:
1. Read the brief completely before generating
2. Follow the structure section exactly (numbered sections)
3. Use the hook verbatim as your opening line
4. Include all 3 proof points — concrete, no paraphrasing
5. End with the specified CTA
6. Channel constraints are hard limits — do not exceed word count targets

Quality gate targets:
- SEO: embed primary keyword in first 100 words + at least 2 secondary keywords
- Brand voice: authoritative-yet-accessible, no forbidden language
- Readability: short sentences (max 20 words), no passive voice
- Originality: no boilerplate, no template language

Output: raw content only — no explanatory text, no meta-commentary

Reasoning Hash: sha256:aiwf-v21-launch-content-04-production-2026-04-25
```
