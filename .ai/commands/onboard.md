---
type: command-registry
tier: OMEGA
version: 1.0.0
compliance: Law 151/2020
traceability: ISO-8601 Certified
agent: guide-agent
registry: .ai/commands/onboard.md
---

# `/onboard`

**Client workspace onboarding** — ordered steps (GitHub → design baseline → human docs → planning) before deep `/guide`, `/plan`, or `/dev`.

## Canonical source & mirrors

- **Canonical:** `.ai/commands/onboard.md`  
- **Factory mirror:** `factory/library/commands/onboard.md` — keep in sync after edits.  
- **IDE layers:** `bash factory/scripts/core/sync_ide_triple_layer.sh`

## State file

**Path:** `.ai/onboarding/state.yaml` (per sovereign workspace under `workspaces/clients/`).

| Key | Meaning |
|-----|---------|
| `onboarding_complete` | `true` when all `steps.*.done` are `true` and operator confirmed |
| `steps` | Named booleans: `github_repo`, `design_baseline`, `docs_prd_roadmap_context`, `planning_ready` |

Materialized workspaces should receive a starter file from `materialize_workspace_from_bundle.py`. Copy manually if missing.

## Subcommands

| Subcommand | Purpose |
|------------|---------|
| `/onboard status` | Show checklist from `state.yaml` + link `docs/guides/ONBOARDING.md` |
| `/onboard step <id>` | Mark one step `done: true` (`id` = `github_repo` \| `design_baseline` \| `docs_prd_roadmap_context` \| `planning_ready`) |
| `/onboard complete` | Set `onboarding_complete: true` **only if** all steps are `done: true`; otherwise list what is left |
| `/onboard reset` | Set all steps `done: false` and `onboarding_complete: false` (owner use only) |

## Assistant behavior

1. On `/onboard status`, read `.ai/onboarding/state.yaml` (create from template below if missing). Print a short table: step id, label, done.  
2. On `/onboard step github_repo`, set that key under `steps.github_repo.done` to `true` and bump `updated_at`.  
3. On `/onboard complete`, verify all `steps.*.done`; if yes, set `onboarding_complete: true`; else refuse with remaining list.  
4. YAML edits must preserve comments optional; use ISO-8601 UTC for `updated_at`.

## Template (`state.yaml`)

```yaml
version: "1"
onboarding_complete: false
steps:
  github_repo:
    label: "GitHub repository created and linked (remote + first commit)"
    done: false
  design_baseline:
    label: "design.md baseline chosen from .ai/templates/design/ (see DESIGN_ONBOARDING)"
    done: false
  docs_prd_roadmap_context:
    label: "docs/product/PRD.md, ROADMAP.md, overview/CONTEXT.md, context/README.md drafted"
    done: false
  planning_ready:
    label: ".ai/plan/development/ scaffold copied and phase spec started (or explicitly waived)"
    done: false
updated_at: "2026-05-04T00:00:00Z"
```

## Gate (interaction with `/guide`)

When `onboarding_complete` is **false**, **`/guide`** must **lead with onboarding** for any heavy mode (see `.ai/commands/guide.md` — Client workspace onboarding gate). **`/guide onboarding`** is treated like **`/onboard status`** (teach-first checklist).

## Gate (interaction with `/plan` and `/dev`)

Until `onboarding_complete: true`, **refuse** `/plan blueprint`, `/plan discovery` (full interview), `/dev implement`, and `/dev build` (production) — short refusal + `/onboard status`. **`/plan status`**, **`/dev init`**, and **`/guide help`** remain allowed for orientation.
