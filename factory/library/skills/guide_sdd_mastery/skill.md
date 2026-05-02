# guide:sdd-mastery

**Purpose:** Ground **Antigravity** and **`guide_sdd_guardian`** in AIWF **Spec-Driven Development (SDD)** vocabulary, artifacts, and enforcement so `/guide` can **oversee** planning and implementation health.

## SDD in one breath

**SDD** = specs and acceptance-style artifacts **lead** work; implementation proves the spec, not the reverse. AIWF uses **Tripartite** labels on planning output: `development:`, `content:`, `social:` (see `.ai/commands/guide.md` operational constraints).

## Tripartite planning (8 planning types)

Valid `planning_type` slugs include: `development`, `content`, `seo`, `social_media`, `marketing`, `business`, `media`, `branding`. Each follows a **5-phase SDD lifecycle** in v21 narrative; phases should be **high-density**.

## High-density phase (typical expectations)

- **≥12 distinct spec files** per phase (v21 density narrative; exact enforcement via gate script).
- Commonly required artifacts (names may vary slightly by template; verify with `spec_density_gate_v2.py`):
  - `requirements.spec.md`, `design.md`, `domain_model.md`, `tasks.json`, `phase.spec.json`
  - C4: `c4-context.mmd`, `c4-containers.mmd`
  - `regional_compliance.md` where MENA / residency applies
  - `contracts/`, `prompt_library/`, `templates/`, `validation/` groups as applicable

## Enforcement surfaces

- **Local gate:** `python3 factory/scripts/core/spec_density_gate_v2.py --phase [path]`
- **Pre-commit:** blocks thin specs for non-draft phases (per `guide.md` narrative).
- **CI:** `sovereign-verification` job in `aiwf-industrial-pipeline.yml` (per `guide.md`).
- **Omega Release Gate:** human/sovereign promotion — structural changes still need governance per `AGENTS.md`.

## Process flow (teaching order)

1. **Plan** — manifest + phase folders under `.ai/plan/`.
2. **Review / gate** — density + contracts.
3. **Implement** — `workspaces/<slug>/` isolation for client work.
4. **Validate** — tests, audits, CI.

## Manifests and sync

- **`.ai/plan/_manifest.yaml`** — `/guide plan status` source of truth.
- **`factory/library/planning/sync_manifest.json`** — last sync hash for plan library alignment.
- **Mirror discipline** — `bash factory/scripts/core/sync_ide_triple_layer.sh` after command/rule edits; outbound `factory/library/` per Outbound Mirror Protocol.

## Law 151 / 2020

When work touches **MENA/Egypt** personal data or regional compliance, flag **Law 151/2020** and `regional_compliance.md`; do not invent legal advice — point to repo compliance artifacts and human review.

## Optional deep pass

Orchestrators may delegate a **hard gate review** or **phase audit** to **`.ai/subagents/guide_sdd_guardian.md`**.
