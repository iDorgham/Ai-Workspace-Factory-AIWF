# AIWF — Project Context

**Purpose:** Fast orientation for humans and agents. This file complements the [Product Requirements Document](../product/PRD.md); it does not replace it. For full protocols, acceptance criteria, and version history, read the PRD.

**Last updated:** 2026-05-03  
**Product line:** AI Workspace Factory (AIWF)  
**Governor:** Dorgham  

---

## What this repository is

AIWF is a **spec-driven orchestration factory**: a curated system of agents, skills, commands, planning templates, and automation scripts used to spawn and govern **isolated workspaces** under `workspaces/`. Client and personal shards are materialized from **`factory/shards/`** only (via **`/mat`**). The global component library lives under `factory/library/` with canonical intelligence under `.ai/`. Factory runtime reports live under **`docs/reports/factory/`** (single `docs/` tree at repo root).

---

## Where to look first

| Need | Location |
|------|----------|
| Full product spec, gates, compliance | [docs/product/PRD.md](../product/PRD.md) |
| Long-range evolution | [docs/product/ROADMAP_LONGTERM.md](../product/ROADMAP_LONGTERM.md) |
| Agent registry and workspace rules | [AGENTS.md](../AGENTS.md) (repo root) |
| Slash commands and humanized `/guide` | [.ai/commands/guide.md](../.ai/commands/guide.md) |
| Active planning phases and manifest | [.ai/plan/_manifest.yaml](../.ai/plan/_manifest.yaml) |
| Generated audits and machine reports | [docs/reports/](reports/) |
| Workspace spawn script | [.ai/scripts/factory_materialize.sh](../.ai/scripts/factory_materialize.sh) (alias: `bin/materialize.sh`) |

---

## Three-tier layout (mental model)

1. **`.ai/`** — Plans, commands, governance, registries, logs, and **template mirrors** (including `templates/design/` for UI/design provider packs).
2. **`factory/`** — Executable engine: `factory/scripts/`, `factory/core/`, **`factory/library/`** (agents, skills, design packs, planning mirror, reports), **`factory/shards/`** (OS copy sources), **`factory/cfg/`** (config bundle), **`factory/stubs/`** (scaffold seeds), tests.
3. **`workspaces/`** — Runtime shards (`clients/`, `personal/`). Template bodies live under **`factory/shards/`** (often gitignored); paths and behavior are documented in [workspaces/README.md](../workspaces/README.md).

Cross-cutting documentation: **`docs/`** (this file, PRD, roadmap). Do not store generated audit JSON in the repo root; use **`docs/reports/`**.

---

## Design catalog & external library sync

Industrial UI/design **provider packs** are stored as one folder per provider, each containing `design.md`, under:

- **Canonical templates:** `.ai/templates/design/` (catalog: `.ai/templates/design/catalog.json`, index: `README.md`)
- **Factory library mirror:** `factory/library/design/`
- **Template mirror (library):** `factory/library/templates/design/`

Ingestion is **manifest-driven** from `factory/library/registry/external_sources.registry.json`, implemented by:

- `factory/library/scripts/maintenance/external_library_sync.py` — clone/merge external sources, refresh catalogs, write merge reports to `factory/library/reports/external_library_merge_report.{json,md}`.

Optional helper for bundling Nexu Open Design-style skills:

- `factory/library/scripts/maintenance/import_nexu_open_design_skills.py`

Registry maintenance for skills/agents may use `factory/scripts/analytics/rebuild_canonical_registries.py` where applicable.

---

## Naming, commits, and local IDE state

- **Pre-commit gate:** `factory/scripts/core/pre_commit_gate.py` (installed as `.git/hooks/pre-commit`). Checks include **snake_case** stems on staged files, mirror drift threshold, forbidden placeholders, and SDD density for touched phase folders.
- **Vendored exceptions:** Upstream mirrors that legitimately use kebab-case or mixed stems are excluded by **path prefix** in the gate (same mechanism as `factory/library/skills/github_imports/`). The **Nexu Open Design** bundle under `factory/library/skills/nexu_open_design/` is treated as vendored third-party content for naming checks.
- **`.cursor/`** — Intended as **local IDE state** (see root `.gitignore`). Do not rely on committing hook state under `.cursor/hooks/state/` for reproducibility.

---

## Compliance snapshot (MENA)

Law **151/2020** (Egypt PDPL) and MENA residency assumptions are design constraints documented in the PRD and phase `regional_compliance.md` files. Arabic-sensitive workflows are routed per governance; PII handling and residency are release-gate concerns, not optional add-ons.

---

## Verification commands (quick)

From repository root (Python 3.10+):

```bash
python3 factory/scripts/maintenance/health_scorer.py
python3 factory/scripts/core/spec_density_gate_v2.py --phase <path-to-phase-dir>   # when editing plans
python3 factory/scripts/core/planning_mirror_sync.py --dry-run
python3 factory/scripts/core/omega_release_gate.py --all
```

For pytest: `pytest factory/tests/` (see `factory/tests/README.md`).

---

## Version label

Documentation and factory metadata are aligned around **v20.2.0** for the design-catalog and external-library documentation wave (2026-05). The authoritative feature timeline and gate definitions remain in [PRD.md](../product/PRD.md) §2 and §4.

---

*Sovereign Intelligence. Absolute Equilibrium.*
