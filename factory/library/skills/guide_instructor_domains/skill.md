# guide:instructor-domains

**Purpose:** When Antigravity `/guide` runs in **instructor mode** (explain · understand · learn), use this map to stay accurate and repo-grounded. Do not invent vendor APIs—prefer linked official skills or docs.

**Sibling skills:** `.ai/skills/guide_teaching/skill.md` (layered L0–L3 pedagogy) · `.ai/skills/guide_sdd_mastery/skill.md` (SDD, gates, manifests).

## Default behavior

- User says `/guide …` with **natural language** (not `plan`, `heal`, `ping`, etc.) → teach first, **then** one next prompt or terminal line in the global footer.
- **Session memory** only: `/guide memory:*`. Durable facts belong in **`AGENTS.md`** (human edit) or new **skills**, not chat-only state.

## Domain → where to look

| Domain | AIWF anchors |
|--------|----------------|
| Security / secrets | `.github/workflows/`, `factory/scripts/core/pre_commit_hook_v2.py`, `official_semgrep_*` skills |
| Development / engineering | `.ai/plan/`, `factory/scripts/`, `factory/tests/` |
| Design | `factory/library/design/`, `official_figma_*`, `official_anthropics_canvas_*` |
| Content / SEO / marketing | `.ai/plan/content/`, `marketing_*`, `egyptian_arabic_content_master` |
| GitHub / Actions / Advanced Security | `.github/workflows/`, `official_github_*`, `official_callstackincubator_github_actions` |
| Vercel / deployment | `official_vercel_*` skills; deploy only via `/deploy` per `AGENTS.md` |
| Agents / skills / workspaces | `AGENTS.md`, `factory/library/skills/`, `.ai/skills/`, `workspaces/<slug>/` |
| AI environment (IDE, MCP, prompts) | `.cursor/rules/`, `.ai/commands/`, user MCP config |

## Optional deep lesson (workflows)

For orchestrated long-form teaching, use **`.ai/subagents/guide_instructor.md`** — not for every short `/guide` question.

## When to suggest a new skill or rule

Only if the **same** teaching gap appears **often**. Propose a **small** `skill.md` in its own folder under `.ai/skills/` or a focused `.cursor/rules/*.mdc`—never store secrets in either.

## Spelling / branding

Use **Vercel** (not “Versel”). **GitHub** is one word. **Law 151/2020** for MENA data context when relevant.
