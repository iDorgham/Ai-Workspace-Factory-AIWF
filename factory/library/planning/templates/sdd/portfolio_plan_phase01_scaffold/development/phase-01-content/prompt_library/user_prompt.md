# User Prompt Template — AIWF v21.0.0 Planning Request

**Load `system_prompt.md` first, then send this as the user turn.**  
Replace all `{{PLACEHOLDER}}` values before sending.

---

```
**AIWF v21.0.0 Planning Request**

Planning Type: content
Topic: "Ezzat Gamaly — portfolio website (public site + CMS)"
Phase: 01 — refine existing phase-01-content folder (do not duplicate tree)
Mode: plan-only

Requirements:
- Improve files under .ai/plan/development/phase-01-content/ to remove TBDs once PRD and stack are known.
- Keep c4-context.mmd and c4-containers.mmd valid Mermaid C4; ≤30 elements.
- Align contracts with chosen CMS and hosting; keep Law 151 notes accurate.
- Append Reasoning Hash: sha256:portfolio-website-content-phase01-2026-05-04 when you change metadata.
- End with: next actions → run spec_density_gate_v2 from AIWF repo → handoff to /dev when approved.

Additional context:
- Human docs: docs/product/PRD.md, docs/product/ROADMAP.md, docs/overview/CONTEXT.md
- Onboarding order: docs/guides/ONBOARDING.md

Generate or revise the blueprint now.
```

---

## Multi-CLI Launch Pattern

To run this prompt across multiple CLIs simultaneously via `/plan launch`:

1. Save this filled prompt to `prompt_library/launch_portfolio_website.md`
2. Run: `/plan launch .ai/plan/development/phase-01-content/prompt_library/launch_portfolio_website.md`
3. Results aggregate back into the phase folder + dashboard

**Registered CLI adapters:** Claude, Gemini, Qwen, Kilo, OpenCode, Copilot, Codex
