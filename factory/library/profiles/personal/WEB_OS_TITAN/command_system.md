# WEB_OS_TITAN — Command system (websites, portfolio, CMS, SDD)

**Source of truth:** **`factory/library/`** — agents, subagents, skills, commands, subcommands, rules, templates, and library scripts referenced in [`workspace_bundle.manifest.yaml`](workspace_bundle.manifest.yaml) must be **read and edited there** (then mirrored into workspace `.ai/` / `.cursor/` per `AGENTS.md`). See **[`factory/library/canonical_source.md`](../../../canonical_source.md)**.

This profile targets **marketing sites**, **portfolios**, **content-managed** experiences, and a **CMS / admin-style dashboard** beside the public frontend — all governed by **Spec-Driven Development (SDD)**.

## 0. Create a workspace from this profile (library-first)

From the **AIWF repo root**, materialize a sovereign folder under `workspaces/` with **symlinks** into `factory/library/` driven by [`workspace_bundle.manifest.yaml`](workspace_bundle.manifest.yaml) (skills allowlist + `library:` paths — commands, registries, design packs, scripts, operator docs). Each run also creates a human **`docs/`** tree if missing: `docs/overview/CONTEXT.md`, `docs/product/PRD.md`, `docs/product/ROADMAP.md`, `docs/guides/ONBOARDING.md`, `docs/context/README.md`, and `docs/README.md` (index). For **`--client` / `--clients` / two-arg client paths**, it adds **`.ai/onboarding/state.yaml`** and symlinks **`.ai/commands/onboard.md`** so **`/onboard`** and the **client onboarding gate** (see `.cursor/rules/workspace-client-onboarding-gate.mdc`) apply.

```bash
python3 factory/scripts/core/materialize_workspace_from_bundle.py <slug> --personal \
  --manifest factory/library/profiles/personal/WEB_OS_TITAN/workspace_bundle.manifest.yaml
```

Use `--client <name>` instead of `--personal` for `workspaces/clients/<client>/001_<slug>/`, or **`--clients`** when the client folder equals the slug, or **two positionals** `python3 … <client_folder> <project_slug> …` (same as `--client` + slug). Omit routing flags for `workspaces/<slug>/`. Add `--dry-run` to print paths only. **PyYAML** is optional if **Node** can `require('yaml')` (see script header). This path is separate from **`/mat`** (shard templates under `factory/shards/`) and from **`compose.py`** (JSON under `factory/profiles/*.json`).

## 1. How pieces fit together

| Layer | Role | Primary commands |
|-------|------|-------------------|
| **SDD planning** | Phases, dense specs, gates | `/plan blueprint`, `/plan status`, `/plan review`, `/plan adr` |
| **Implementation** | Frontend, CMS UI, APIs | `/dev init`, `/dev implement`, `/dev test`, `/dev build`, `/dev fix` |
| **Content & SEO** | Editorial, scrape, polish | `/create …`, `/scrape …`, `/polish …`, `/research …`, `/intel …` |
| **Design onboarding** | Pick a `design.md` pack | `/design list`, `/design use [pack]`, `/design install [pack]` — see [design/design_onboarding.md](design/design_onboarding.md) |
| **Quality & security** | Gates before ship | `/audit health`, `/audit security`, `/audit seo` |
| **Git & release** | Branches, commits, tags, push | `/git …` — see [scripts/git_workflow.md](scripts/git_workflow.md) |
| **Teaching & process** | `/guide` for humans + SDD | [guide/recommendations.md](guide/recommendations.md) |
| **Automation hooks** | IDE / agent lifecycle | [hooks/README.md](hooks/README.md) |

Canonical router tables live in **`factory/library/commands/commands.md`** (mirror into workspace `.ai/commands/` per your sync).

## 2. Artifact map (this folder)

**Materialized client workspaces:** operator summaries from the rows below are symlinked under **`docs/profile/`** (not `PROFILE_DOCS/`). Hooks catalog is **`docs/profile/HOOKS.md`** to avoid clashing with **`docs/profile/README.md`**.

| Path | Contents |
|------|----------|
| [workspace_bundle.manifest.yaml](workspace_bundle.manifest.yaml) | Allowlist: agents, subagents, skills, commands, **library** paths, rules, templates, scripts |
| [agents/planned_agents.md](agents/planned_agents.md) | T0/T1 roles for web + CMS + SDD |
| [skills/planned_skills.md](skills/planned_skills.md) | Skill folder ids under `factory/library/skills/` |
| [commands/planned_commands.md](commands/planned_commands.md) | Slash commands to retain |
| [design/design_onboarding.md](design/design_onboarding.md) | Installing a **design.md** pack during onboarding |
| [scripts/git_workflow.md](scripts/git_workflow.md) | Branch, tag, release, deploy tags, push/pull |
| [scripts/list_design_packs.sh](scripts/list_design_packs.sh) | Lists every `factory/library/templates/design/**/design.md` |
| [hooks/README.md](hooks/README.md) | Suggested Cursor hooks for this workspace |
| [guide/recommendations.md](guide/recommendations.md) | **`/guide`** usage + recommendations |

## 3. SDD reminder (short)

1. **`/plan blueprint`** (or `/plan discovery`) before large builds.  
2. Keep **phase density** honest (see `factory/scripts/core/spec_density_gate_v2.py` on the AIWF repo).  
3. **Implement** only against approved specs (`/dev implement`).  
4. **Audit** then **git** lifecycle for traceability.

## 4. Deploy policy

Align with workspace **`AGENTS.md`**: production deploy only via explicit **`/deploy`** (or your shard’s equivalent) — never silent production deploy from hooks.

**Traceability:** `2026-05-04` — WEB_OS_TITAN command system for portfolio + CMS + SDD + git + guide.
