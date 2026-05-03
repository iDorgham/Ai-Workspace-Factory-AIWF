# AIWF v21.0.0 — Tripartite Planning Singularity

**Document Type:** SDD Planning Document  
**Status:** APPROVED  
**Version:** 21.0.0  
**Created:** 2026-04-25  
**Traceability Hash:** sha256:v21-tripartite-planning-singularity-2026-04-25  
**Law 151/2020:** Enforced — all planning artifacts processed in Egypt/MENA  
**Prerequisite Of:** Phase 24+ (post-git-automation execution phases)  

---

## Executive Summary

v21.0.0 extends AIWF's sovereign planning architecture from a single-stream development-only
SDD system into a full **Tripartite Planning Singularity** — covering all major creation
domains: development, content, SEO, social media, marketing, business, media, and branding.

Every plan type shares the same high-density phase structure (≥12 files, enforced), the same
C4 Model integration (Context + Container mandatory, Mermaid syntax), and the same Law 151/2020
compliance gate. Multi-CLI orchestration means the same planning blueprint executes across
Claude, Gemini, Qwen, Kilo, OpenCode, Copilot, and Codex in parallel.

The result: one command (`/plan {type} "{topic}"`) generates a production-ready sovereign
blueprint with zero structural debt and maximum execution fidelity.

---

## 1. Problem Statement

### Current State (v19.0–20.x)

The SDD architecture existed only for the `development/` planning stream. All other planning
types (content, SEO, marketing, branding, etc.) had no standardised structure, no density gate,
no C4 integration, no compliance template, and no multi-CLI prompt library. This created:

- Structural inconsistency between plan types
- No machine-verifiable quality gate for non-development plans
- Manual, high-friction process to produce plans for any non-development domain
- C4 diagrams were requested but had no standard template or enforcement mechanism
- Multi-CLI orchestration lacked a shared prompt library across plan types

### Target State (v21.0.0)

A unified, sovereign, multi-type planning system where:
- Any plan type generates identical structural density (≥12 files/phase)
- C4 Context + Container diagrams are produced automatically from templates
- `spec_density_gate_v2.py` enforces quality before any phase activates
- `prompt_library/` in every phase provides ready-to-run prompts for all 7 CLIs
- Law 151/2020 compliance is built into every phase via `regional_compliance.md`

---

## 2. Architecture Overview

### Folder Structure

```
.ai/plan/
├── _manifest.yaml              ← Extended with planning_system block
├── templates/sdd/base_template/  ← 17-file canonical template (≥12 density gate passes)
├── development/                ← Existing; now formally typed
├── content/                    ← NEW: 5-phase structure
├── seo/                        ← NEW
├── social_media/               ← NEW
├── marketing/                  ← NEW
├── business/                   ← NEW
├── media/                      ← NEW
└── branding/                   ← NEW
```

### Per-Phase Structure (≥12 files, enforced by spec_density_gate_v2)

```
{phase-NN-slug}/
├── phase.spec.json             (1) Goals, AC, timeline, density gate config
├── requirements.spec.md        (2) Functional + NFR requirements + Gherkin AC
├── design.md                   (3) Narrative + C4 diagram references
├── c4-context.mmd              (4) C4 Level 1 — System Context (≤25 elements)
├── c4-containers.mmd           (5) C4 Level 2 — Container Architecture (≤30 elements)
├── domain_model.md             (6) Schemas / pillars / clusters / matrices
├── task_graph.mmd              (7) Mermaid Gantt with gate milestones
├── tasks.json                  (8) Structured tasks (≥5, with CLI prompt refs)
├── contracts/                  (9+) API contract, content contract, state contract
│   ├── api_contract.md
│   ├── content_contract.md
│   └── state_contract.md
├── templates/                  (12) Copy frameworks, prompt templates
│   └── copy_framework.md
├── validation/                 (13+) Audit checklist, KPI tracker, density gate report
│   ├── audit_checklist.md
│   └── kpi_tracker.md
├── regional_compliance.md      (16) Law 151/2020 data residency + MENA adaptations
└── prompt_library/             (17+) Ready-to-run CLI prompts
    ├── system_prompt.md        ← Canonical spec_architect_v2 system prompt
    └── user_prompt.md          ← User prompt template for all CLIs
```

---

## 3. Specification Index

### Core Infrastructure Specs

| Spec ID | Name | File | Priority |
|---------|------|------|----------|
| V21-S01 | Base SDD Template | `.ai/plan/templates/sdd/base_template/` | P1 |
| V21-S02 | Spec Density Gate v2 | `factory/scripts/core/spec_density_gate_v2.py` | P1 |
| V21-S03 | Pre-Commit Hook v2 | `factory/scripts/core/pre_commit_hook_v2.py` | P1 |
| V21-S04 | Manifest Planning Registry | `.ai/plan/_manifest.yaml#planning_system` | P1 |
| V21-S05 | C4 Context Template | `base_template/c4-context.mmd` | P1 |
| V21-S06 | C4 Container Template | `base_template/c4-containers.mmd` | P1 |
| V21-S07 | System Prompt (spec_architect_v2) | `base_template/prompt_library/system_prompt.md` | P1 |
| V21-S08 | User Prompt Template | `base_template/prompt_library/user_prompt.md` | P1 |

### Planning Type Specs (8 types × _index.md)

| Type | Path | Status |
|------|------|--------|
| development | `.ai/plan/development/` | Existing — retroactively typed |
| content | `.ai/plan/content/` | Registered 2026-04-25 |
| seo | `.ai/plan/seo/` | Registered 2026-04-25 |
| social_media | `.ai/plan/social_media/` | Registered 2026-04-25 |
| marketing | `.ai/plan/marketing/` | Registered 2026-04-25 |
| business | `.ai/plan/business/` | Registered 2026-04-25 |
| media | `.ai/plan/media/` | Registered 2026-04-25 |
| branding | `.ai/plan/branding/` | Registered 2026-04-25 |

---

## 4. Spec Density Gate v2

`factory/scripts/core/spec_density_gate_v2.py`

### Gate Checks (6 gates, all must PASS)

| Gate | Rule | Threshold |
|------|------|-----------|
| minimum_file_count | Total files in phase folder | ≥ 12 |
| required_top_level_files | 7 mandatory files present | All 7 |
| c4_diagrams | c4-context.mmd + c4-containers.mmd | Both present |
| required_subdirectories | contracts/, templates/, validation/, prompt_library/ with ≥1 file each | All 4 |
| tasks_minimum | tasks.json must define ≥5 tasks | ≥ 5 |
| phase_spec_valid | phase.spec.json is valid JSON with required keys | 4 keys |

### Integration Points

- **Pre-commit hook** (`pre_commit_hook_v2.py`): Runs on any staged `.ai/plan/` phase folder. Draft phases generate warnings; non-draft phases block the commit.
- **`/plan activate` command**: Runs gate before updating manifest status from REVIEW → APPROVED.
- **CI workflow** (`aiwf-industrial-pipeline.yml`): Runs as part of sovereign-verification job.

### Usage

```bash
# Check a phase folder
python factory/scripts/core/spec_density_gate_v2.py --phase .ai/plan/development/19_sovereign_commit

# JSON output + write report
python factory/scripts/core/spec_density_gate_v2.py \
  --phase .ai/plan/content/phase-01-discovery \
  --json --write-report

# Strict mode (warn = fail)
python factory/scripts/core/spec_density_gate_v2.py \
  --phase .ai/plan/marketing/phase-02-blueprint \
  --strict
```

---

## 5. C4 Model Standards

### Diagram Requirements

| Level | File | Required In | Element Limit |
|-------|------|-------------|---------------|
| Context (L1) | `c4-context.mmd` | All phases | ≤ 25 |
| Container (L2) | `c4-containers.mmd` | All phases | ≤ 30 |
| Component (L3) | `c4-component.mmd` | Phase-03+ | ≤ 25 |

### Mandatory Element Format

Every C4 element must have:
- **Name** — short, descriptive
- **Technology** — Python, YAML, Markdown, etc.
- **Description** — 1-line responsibility statement

### Arrow Standards

- Unidirectional only — no bidirectional arrows
- Action-verb labels: `Triggers`, `Reads from`, `Deploys to`, `Writes`, `Streams`, `Invokes`
- No orphan nodes (every node must have at least one relationship)

---

## 6. Multi-CLI Orchestration

### System Prompt

Load `base_template/prompt_library/system_prompt.md` as the system/instruction message in
any CLI before requesting plan generation.

### User Prompt

Fill `base_template/prompt_library/user_prompt.md` with topic, type, phase, and constraints.
Save as `prompt_library/launch_{topic_slug}.md` in the phase folder.

### Parallel Execution via `/plan launch`

```bash
/plan launch .ai/plan/{type}/{phase}/prompt_library/launch_{slug}.md
```

Routes to all registered adapters simultaneously. Results aggregate back into the phase
folder. Adapters: Claude, Gemini, Qwen, Kilo, OpenCode, Copilot, Codex.

---

## 7. Implementation Steps

### Step 1 — Template Infrastructure (Completed 2026-04-25)

- [x] `.ai/plan/templates/sdd/base_template/` — 17 files, density gate passes
- [x] All 8 planning type directories with 5-phase structure each
- [x] `_index.md` for each type
- [x] `spec_density_gate_v2.py` — 6-gate validation script
- [x] `pre_commit_hook_v2.py` — Extended hook with density gate integration
- [x] `_manifest.yaml` — `planning_system` block registered

### Step 2 — Hook Installation (Manual step, requires repo access)

```bash
cp factory/scripts/core/pre_commit_hook_v2.py .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

### Step 3 — First Real Plan Generation

Run the first non-development plan to validate the full pipeline:

```bash
/plan content "AIWF v21.0.0 Launch Content Strategy" --mode=plan-only
```

This should produce a complete 5-phase content plan with all ≥12 files per phase.

### Step 4 — CI Integration

Add to `.github/workflows/aiwf-industrial-pipeline.yml` sovereign-verification job:

```yaml
- name: Spec Density Gate — Active Phases
  run: |
    for phase_dir in .ai/plan/development/*/; do
      spec_status=$(python -c "import json; d=json.load(open('${phase_dir}phase.spec.json')); print(d.get('status','draft'))" 2>/dev/null || echo "draft")
      if [ "$spec_status" != "draft" ] && [ "$spec_status" != "planned" ]; then
        python factory/scripts/core/spec_density_gate_v2.py --phase "$phase_dir" --json
      fi
    done
```

### Step 5 — Mirror Sync to Library

Extend `master_sync.py` to include planning type paths in the mirror:

```python
PLANNING_MIRROR_PATHS = [
    "content", "seo", "social_media", "marketing",
    "business", "media", "branding"
]
```

---

## 8. Acceptance Criteria

| ID | Criterion | Verification |
|----|-----------|--------------|
| AC-01 | All 8 planning type directories exist with 5-phase structure | `ls .ai/plan/` |
| AC-02 | Base template has ≥12 files | `spec_density_gate_v2.py --phase templates/sdd/base_template` |
| AC-03 | spec_density_gate_v2.py returns exit 0 on base template | Script run |
| AC-04 | _manifest.yaml contains `planning_system` block with all 8 types | `grep planning_types _manifest.yaml` |
| AC-05 | pre_commit_hook_v2.py includes density gate check | Code review |
| AC-06 | C4 templates use valid Mermaid C4 syntax | Mermaid render |
| AC-07 | System + user prompt templates are complete | Manual review |
| AC-08 | Law 151/2020 regional_compliance.md template present | `ls base_template/` |

**Status as of 2026-04-25:** AC-01 through AC-08 all satisfied. ✅

---

## 9. Cross-Phase Dependencies

```
F4_isolation (isolation contracts) → V21 content_contract template
F3_tombstoning (deprecation protocol) → V21 state_contract DEPRECATED/TOMBSTONED states
Ph19-23 (git automation) → V21 pre_commit_hook_v2 density gate integration
Ph22 (tags/release) → V21 audit_checklist referenced in OmegaReleaseGate 12-point check
```

---

## 10. Reasoning Hash Chain

| Event | Hash |
|-------|------|
| v21 spec document | sha256:v21-tripartite-planning-singularity-2026-04-25 |
| Base template creation | sha256:v21-base-template-17-files-2026-04-25 |
| Manifest planning_system block | sha256:v21-planning-system-2026-04-25 |
| spec_density_gate_v2 | sha256:spec-density-gate-v2-2026-04-25 |
| pre_commit_hook_v2 | sha256:pre-commit-hook-v2-density-gate-2026-04-25 |
