# Portfolio + CMS — SDD `development/` scaffold

[![SDD](https://img.shields.io/badge/SDD-v21-1a2332)](../../../../../../README.md)
[![Density](https://img.shields.io/badge/spec__density__gate-v2-success)](../../../../../scripts/core/spec_density_gate_v2.py)
[![Example docs](https://img.shields.io/badge/example%20docs-Ezzat%20Portfolio-0366d6)](../../../../../../workspaces/clients/ezzat-gamaly/001_portfolio-website/docs/README.md)

Reusable **`.ai/plan/development/`** tree for a **content-first** portfolio and CMS track: **`phase-01-content/`** with C4, contracts, Law **151/2020** posture, and **≥12** phase files.  
Captured from **`workspaces/clients/ezzat-gamaly/001_portfolio-website`** (2026-05-04); validated with **`spec_density_gate_v2`**.

> **Human specs live in `docs/`** — mirror the [example documentation layout](#paired-human-docs-layout) so `requirements.spec.md` can link to PRD, roadmap, and context **before** you duplicate product truth inside `.ai/plan/`.

---

## Contents

- [What you get](#what-you-get)
- [Directory layout](#directory-layout)
- [Paired human `docs/` layout](#paired-human-docs-layout)
- [How to use](#how-to-use)
- [Density gate](#density-gate)
- [Related templates](#related-templates)

---

## What you get

| Artifact | Purpose |
|----------|---------|
| `phase.spec.json` | Goals, AC, timeline, density config |
| `requirements.spec.md` | Functional + NFR (+ Gherkin); **link** `docs/product/*` |
| `design.md` + **C4** | Narrative + `c4-context.mmd` / `c4-containers.mmd` |
| `domain_model.md` | Content types, entities, editorial states |
| `task_graph.mmd` | Mermaid Gantt + gate milestones |
| `tasks.json` | **≥5** tasks (CLI / agent refs) |
| `contracts/` | API, content quality, state machine |
| `templates/` | e.g. `content_brief_template.md` |
| `validation/` | Audit checklist + KPI tracker |
| `regional_compliance.md` | Law **151/2020** + Arabic / MENA handling |
| `prompt_library/` | System + user prompts (+ Law 151 check helper) |

---

## Directory layout

```
development/
└── phase-01-content/
    ├── phase.spec.json
    ├── requirements.spec.md
    ├── design.md
    ├── c4-context.mmd
    ├── c4-containers.mmd
    ├── domain_model.md
    ├── task_graph.mmd
    ├── tasks.json
    ├── regional_compliance.md
    ├── contracts/
    │   ├── api_contract.md
    │   ├── content_contract.md
    │   └── state_contract.md
    ├── templates/
    │   └── content_brief_template.md
    ├── validation/
    │   ├── audit_checklist.md
    │   └── kpi_tracker.md
    └── prompt_library/
        ├── system_prompt.md
        ├── user_prompt.md
        └── law151_check.md
```

---

## Paired human `docs/` layout

Align each new client workspace with a **`docs/`** tree similar to **[`workspaces/clients/ezzat-gamaly/001_portfolio-website/docs/`](../../../../../../workspaces/clients/ezzat-gamaly/001_portfolio-website/docs/README.md)**:

| Area | Suggested path | Notes |
|------|----------------|--------|
| Index | `docs/README.md` | Map to overview, product, guides, profile, context |
| Context | `docs/overview/CONTEXT.md` | Audience + constraints |
| Product | `docs/product/` | PRD, `ROADMAP.md`, GitHub / governance docs |
| Onboarding | `docs/guides/ONBOARDING.md` | GitHub → design → docs → planning |
| Operator playbooks | `docs/profile/` | Command system, `/guide`, design packs, git, hooks |
| Tech notes | `docs/context/README.md` | Stack, ADRs — **no secrets** |

The **Ezzat Portfolio CMS** example also includes rich **`docs/product/`** specs (PRD, Git branching directive, architecture, compliance). Use them as **style and depth references**, then replace names and paths for your client.

---

## How to use

1. **Copy** this `development/` folder into your workspace:

   ```text
   <workspace>/.ai/plan/development/
   ```

   Merge carefully if `development/` already exists.

2. **Rename / rewrite** `spec_id`, `topic`, and client strings in `phase.spec.json`, `requirements.spec.md`, and `tasks.json`.

3. **Fill `docs/`** (PRD, roadmap, context) and link them from `requirements.spec.md` (relative paths like `../../../../docs/product/PRD.md` from `phase-01-content/`).

4. **Run** the density gate from the **AIWF repo root**:

   ```bash
   python3 factory/scripts/core/spec_density_gate_v2.py --phase <path-to>/phase-01-content
   ```

5. **Onboarding:** ensure **`.ai/onboarding/state.yaml`** is complete before heavy `/plan blueprint` / `/dev implement` when using the [client onboarding gate](../../../../../../workspaces/clients/README.md#onboarding-gate).

---

## Density gate

This scaffold was checked with **`spec_density_gate_v2`** (18 files, C4 + contracts + tasks). Re-run after edits; fix any failing gate before calling the phase **active** in manifests.

---

## Related templates

| Template | When to use |
|----------|-------------|
| **[`../base_template/`](../base_template/)** | Empty SDD phase from scratch |
| **`portfolio_plan_phase01_scaffold/`** (this folder) | Portfolio + CMS **content phase 01** with realistic placeholders |
| **Client tier README** | [`workspaces/clients/README.md`](../../../../../../workspaces/clients/README.md) |

**Traceability:** 2026-05-04 — scaffold README aligned with `docs/` example · 2026-05-04 — GitHub-oriented refresh.
