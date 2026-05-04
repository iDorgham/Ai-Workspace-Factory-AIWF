# `/guide` — Recommendations for WEB_OS_TITAN workspaces

Canonical **`/guide`** spec: **`factory/library/commands/guide.md`** (keep in sync with `.ai/commands/guide.md`).

## When to use `/guide`

| Situation | Suggested `/guide` usage |
|-----------|---------------------------|
| New builder on the team | `/guide` + plain question, or `/guide explain <topic>` |
| “Are our SDD phases healthy?” | `/guide plan status` or `/guide gate [phase_path]` |
| Picking design / UX direction | `/guide` “how do we choose a design pack for portfolio vs CMS dashboard?” |
| Git / branch / tag confusion | `/guide understand git tags vs releases` then follow [scripts/git_workflow.md](../scripts/git_workflow.md) |
| MENA / bilingual site | `/guide` with region context — Antigravity applies Law **151/2020** notes when relevant |
| Before shipping | `/guide` + ask for SDD guardian pass on risks + `/audit` pointers |

## Recommended prompts (copy-paste)

```text
/guide plan status
```

```text
/guide explain how SDD phases connect to our CMS and marketing frontend
```

```text
/guide what is the safest order: plan blueprint, dev implement, then git auto?
```

```text
/guide understand semantic versioning and release tags for our portfolio site
```

## Response expectations (Antigravity v3.5)

On `/guide` triggers, assistants should follow **`.cursor/rules/guide-response-style.mdc`**: layered **L0–L3**, scannable headings, and an **inline SDD guardian** block when plans, specs, or gates are in scope.

Footer discipline: **`.cursor/rules/guide-handoff-footer.mdc`** — `### What to do next` plus **one** of `### Next prompt` or `### Next terminal command` (one line inside the fence).

## Companion skills (repo)

- **`.ai/skills/guide_sdd_mastery/`** — density, manifests, C4 vocabulary  
- **`.ai/skills/guide_teaching/`** — layered teaching patterns  
- **`.ai/skills/guide_instructor_domains/`** — domain anchors (web, SEO, content)

**Traceability:** `2026-05-04` — WEB_OS_TITAN `/guide` recommendations.
