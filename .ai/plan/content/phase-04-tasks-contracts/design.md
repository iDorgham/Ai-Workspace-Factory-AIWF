# Design Document — Phase 04: Tasks & Contracts

**Reasoning Hash:** sha256:aiwf-v21-launch-content-04-tasks-contracts-2026-04-25

---

## 1. Production Architecture

Each content piece flows through a 3-step pipeline:
1. **Generate** — CLI adapter executes prompt from `prompt_library/{piece_id}.md`
2. **Gate** — Automated quality scoring (SEO + brand voice + readability + originality)
3. **Commit** — Passes → sovereign commit to `docs/content/launch/`; fails → revise prompt

---

## 2. CLI Assignment Strategy

| Piece Type | Preferred CLI | Fallback | Rationale |
|------------|--------------|----------|-----------|
| Technical (README, Dev.to) | Claude | Kilo | Highest technical accuracy |
| LinkedIn thought leadership | Claude | Gemini | Brand voice fidelity |
| X threads | Claude | OpenCode | Conciseness and hooks |
| Arabic content | Qwen | Claude | Arabic language quality |
| Architecture diagrams (Mermaid) | Claude | Codex | Mermaid syntax reliability |

---

## 3. Output Structure

```
docs/content/launch/
├── github_readme_v21.md
├── linkedin_launch_announcement.md
├── x_thread_v21_live.md
├── linkedin_12_spec_files.md
├── x_tripartite_diagram.md
├── linkedin_law151_architecture.md
├── arabic_linkedin_post.md
├── arabic_mena_community_post.md
├── devto_spec_density_gate.md
├── linkedin_7_clis_pipeline.md
├── x_multi_llm_thread.md
└── github_mena_readme_section.md
```
