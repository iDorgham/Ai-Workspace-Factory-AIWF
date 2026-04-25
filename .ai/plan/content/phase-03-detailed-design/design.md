# Design Document — Phase 03: Detailed Design

**Reasoning Hash:** sha256:aiwf-v21-launch-content-03-detailed-design-2026-04-25

---

## 1. Content Brief Architecture

Each of the 12 launch pieces gets a dedicated brief file in `templates/content_briefs/`
following the content_brief_template.md from Phase 01. The briefs are the production
contracts — every field must be completed before the piece goes to multi-CLI generation.

**12 Launch Pieces:**
1. GitHub README v21 overhaul (Density / Pragmatic Dev)
2. LinkedIn launch announcement (Sovereignty / Sovereign Builder)
3. X thread: "AIWF v21 is live" — 5 posts (Sovereignty / All)
4. LinkedIn: "12 spec files before /dev" (Density / Pragmatic Dev)
5. X: Architecture diagram: Tripartite Planning (Density / Pragmatic Dev)
6. LinkedIn: "Law 151/2020 as architecture" (MENA-First / MENA Pioneer)
7. Arabic LinkedIn post (MENA-First / MENA Pioneer)
8. Arabic MENA community post (MENA-First / MENA Pioneer)
9. Dev.to: spec_density_gate_v2 deep-dive (Density / Pragmatic Dev)
10. LinkedIn: "7 CLIs, 1 sovereign pipeline" (Multi-LLM / AI Director)
11. X: Multi-LLM orchestration thread (Multi-LLM / AI Director)
12. GitHub: MENA README section (MENA-First / MENA Pioneer)

---

## 2. SEO Keyword Strategy

| Piece | Primary Keyword | Secondary Keywords |
|-------|----------------|--------------------|
| GitHub README | "sovereign AI orchestration" | "multi-LLM governance", "AI workspace factory", "Law 151 AI" |
| Dev.to deep-dive | "AI spec density gate" | "SDD methodology", "AI planning framework", "sovereign development" |
| LinkedIn launch | "AI factory Egypt" | "AIWF v21", "sovereign AI MENA", "multi-CLI orchestration" |

---

## 3. Content Pipeline Flow

```
Phase 02 Calendar
  → [Phase 03 brief generation]
  → templates/content_briefs/{piece_id}.md

prompt_library/{piece_id}.md
  → [multi-CLI execution in Phase 04]
  → Raw content output

Quality gate (SEO + brand voice + readability)
  → [Pass: commit to docs/content/launch/]
  → [Fail: revise prompt + regenerate]
```

---

## 4. Key Design Decisions

| Decision | Chosen | Rationale |
|----------|--------|-----------|
| Brief-first vs generate-first | Brief-first | Eliminates prompt ambiguity; every brief is a contract |
| SEO tool | Internal scoring (factory scripts) | Sovereign; no external tool dependency |
| Arabic brief language | English brief, Arabic output | spec_architect_v2 works in English; Arabic generation via Qwen adapter |
