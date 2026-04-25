# Domain Model — Phase 03: Detailed Design
**Reasoning Hash:** sha256:aiwf-v21-launch-content-03-detailed-design-2026-04-25

---

## 1. Content Brief Schema

Every launch piece is governed by a brief. Each brief is a production contract with these mandatory fields:

| Field | Type | Description |
|-------|------|-------------|
| `piece_id` | string | Unique ID e.g. C-01-README |
| `title` | string | Working title |
| `channel` | enum | github \| linkedin \| x \| dev_to \| arabic_mena |
| `pillar` | enum | sovereignty \| density \| mena_first \| multi_llm |
| `persona` | string | Primary target persona |
| `publish_day` | int | Day in 30-day calendar (1–30) |
| `word_count_target` | int | Target word/character count by channel |
| `primary_keyword` | string | SEO primary keyword |
| `secondary_keywords` | list | 2–4 secondary SEO terms |
| `hook` | string | Opening sentence / headline |
| `proof_points` | list | 3 concrete facts or claims |
| `cta` | string | Call to action |
| `cli_adapter` | enum | claude \| qwen \| gemini \| kilo |
| `law_151_flag` | bool | True if piece handles Egyptian user data |
| `status` | enum | draft \| briefed \| generated \| gated \| published |

---

## 2. Content Inventory — All 12 Launch Pieces

| Piece ID | Title | Channel | Pillar | Persona | Day | CLI |
|----------|-------|---------|--------|---------|-----|-----|
| C-01-README | GitHub README v21 overhaul | github | Density | Pragmatic Dev | 1 | claude |
| C-02-LI-LAUNCH | LinkedIn launch announcement | linkedin | Sovereignty | Sovereign Builder | 1 | claude |
| C-03-X-LAUNCH | X thread: "AIWF v21 is live" (5 posts) | x | Sovereignty | All | 1 | claude |
| C-04-LI-12SPEC | LinkedIn: "12 spec files before /dev" | linkedin | Density | Pragmatic Dev | 3 | claude |
| C-05-X-ARCH | X: Architecture diagram — Tripartite Planning | x | Density | Pragmatic Dev | 5 | claude |
| C-06-LI-LAW151 | LinkedIn: "Law 151/2020 as architecture" | linkedin | MENA-First | MENA Pioneer | 7 | claude |
| C-07-AR-LI | Arabic LinkedIn post | linkedin | MENA-First | MENA Pioneer | 7 | qwen |
| C-08-AR-MENA | Arabic MENA community post | arabic_mena | MENA-First | MENA Pioneer | 7 | qwen |
| C-09-DEVTO | Dev.to: spec_density_gate_v2 deep-dive | dev_to | Density | Pragmatic Dev | 10 | claude |
| C-10-LI-7CLI | LinkedIn: "7 CLIs, 1 sovereign pipeline" | linkedin | Multi-LLM | AI Director | 14 | claude |
| C-11-X-MULTILLL | X: Multi-LLM orchestration thread | x | Multi-LLM | AI Director | 14 | claude |
| C-12-GH-MENA | GitHub: MENA README section | github | MENA-First | MENA Pioneer | 21 | qwen |

---

## 3. Channel Specs

| Channel | Format | Word Count | Key Constraint |
|---------|--------|------------|----------------|
| github | Markdown README | 800–1500 words | Must render in GitHub dark mode; code blocks required |
| linkedin | Long-form post | 900–1300 chars | No external links in body; link in first comment |
| x | Thread | 280 chars × N posts | Post 1 = hook; last post = CTA + link |
| dev_to | Article | 1200–2000 words | Front matter: tags, canonical_url, cover_image |
| arabic_mena | Mixed (LI + community) | 600–900 chars | RTL layout; no transliteration — full Arabic |

---

## 4. Persona Briefs (Summary)

| Persona | Pain | Wants | Avoid |
|---------|------|-------|-------|
| Sovereign Builder | AI tools leak jurisdiction | Governance-first architecture | Marketing fluff |
| Pragmatic Dev | Specs become stale on day 2 | Concrete density gates, real file counts | Theory without code |
| MENA Pioneer | Law 151 treated as blocker | Framework that uses law as architecture feature | Western-centric framing |
| AI Director | 7 CLIs = 7 governance silos | Single orchestration layer proof | Vendor lock-in language |

---

## 5. Glossary

| Term | Definition | Slug |
|------|------------|------|
| Content Brief | Production contract for a single piece — all fields mandatory before generation | `content_brief` |
| Pillar | Thematic bucket organising content by audience problem | `content_pillar` |
| Launch Window | 30-day period from v21 public announcement | `launch_window` |
| Quality Gate | Automated scoring: SEO ≥85%, brand voice ≥92%, readability ≥65, originality ≤15% | `quality_gate` |
| CLI Adapter | Multi-CLI executor (Claude, Qwen, Gemini, Kilo) assigned per piece | `cli_adapter` |
| Density Gate | spec_density_gate_v2.py — 6-gate validator; ≥12 files, C4 required, ≥5 tasks | `density_gate` |
