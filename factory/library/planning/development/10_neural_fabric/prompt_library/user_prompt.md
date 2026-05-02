# User Prompt Template — AIWF v21.0.0 Planning Request

**Load `system_prompt.md` first, then send this as the user turn.**  
Replace all `{{PLACEHOLDER}}` values before sending.

---

```
**AIWF v21.0.0 Planning Request**

Planning Type: {{development | content | seo | social_media | marketing | business | media | branding}}
Topic: "{{Exact topic or project name}}"
Phase: {{01-discovery | 02-blueprint | 03-detailed-design | 04-tasks-contracts | 05-validation-handoff}}
Mode: {{plan-only | full}}   ← Default: plan-only (pure blueprint, no implementation)

Requirements:
- Generate the complete phase-gated SDD structure under .ai/plan/{{TYPE}}/{{PHASE}}-{{SLUG}}/
- Use the base SDD template with full C4 integration:
    - c4-context.mmd (mandatory — system context)
    - c4-containers.mmd (mandatory — technology + responsibilities)
    - c4-component.mmd (optional — add for phase-03+)
- Ensure ≥12 high-density files per phase per the exact folder structure.
- Include best-practice adaptations for {{PLANNING_TYPE}} planning type.
- Produce ready-to-use prompt_library/ entries for multi-CLI orchestration.
- Output in clean Markdown/JSON with embedded Mermaid (valid syntax, focused diagrams ≤30 elements).
- Append Reasoning Hash: sha256:{{TOPIC_SLUG}}-{{TYPE}}-{{PHASE}}-{{DATE}}
- End with: next actions list → review dashboard → run /plan launch or handoff to /dev.

Additional Context / Constraints:
{{Add specific goals, audience, Law 151 requirements, existing PRD links, or domain constraints here.}}

Generate the full blueprint now.
```

---

## Multi-CLI Launch Pattern

To run this prompt across multiple CLIs simultaneously via `/plan launch`:

1. Save this filled prompt to `prompt_library/launch_{{TOPIC_SLUG}}.md`
2. Run: `/plan launch .ai/plan/{{TYPE}}/{{PHASE}}/prompt_library/launch_{{TOPIC_SLUG}}.md`
3. AIWF will route to all registered CLI adapters in parallel
4. Results aggregate back into the phase folder + dashboard

**Registered CLI adapters:** Claude, Gemini, Qwen, Kilo, OpenCode, Copilot, Codex
