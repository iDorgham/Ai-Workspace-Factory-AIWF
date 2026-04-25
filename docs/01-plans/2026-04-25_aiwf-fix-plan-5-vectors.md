# AIWF Fix Plan — 5 Structural Vectors
**Document Type:** SDD Planning Document  
**Status:** APPROVED — Ready for Development  
**Version:** 1.0.0  
**Date:** 2026-04-25  
**Governor:** Dorgham  
**Traceability Hash:** sha256:fix-plan-5-vectors-2026-04-25  
**Compliance:** Law 151/2020  
**Execution Sequence:** F1 → F3 → F4 → F2 → F5

---

## Executive Summary

This document defines five structural fix vectors identified during the AIWF v19.0.0 workspace review. Each vector maps to a concrete gap between the documented OMEGA architecture and the current runtime state. Two vectors are classified P1 Critical (load-bearing before the evolution engine scales), two are P2 Structural (preventive before client shard onboarding), and one is P3 Growth (intelligence layer activation).

All fixes must conform to the SDD High-Density Specification Rule: minimum 5 specs per phase before development begins. Each vector below includes its required spec set.

---

## Priority Classification

| ID | Vector | Priority | Owner Agent | Effort |
|----|--------|----------|-------------|--------|
| F1 | Mirror Drift — Cadence Enforcement | P1 Critical | `healing_bot_v2` + `registry_guardian` | Low effort, high leverage |
| F2 | Phases 9 & 10 — Close Open Loops | P1 Critical | `spec_architect` + `documentation_architect` | Medium effort, critical path |
| F3 | Deprecated Scripts — Formal Tombstoning | P2 Structural | `library_curator` + `registry_guardian` | Low effort, one-time |
| F4 | Workspace Isolation — Enforcement Logic | P2 Structural | `factory_orchestrator` + `healing_bot_v2` | Medium effort, preventive |
| F5 | Brainstorm Agent — Signal Activation | P3 Growth | `brainstorm_agent` + `memory_manager` | Medium effort, high strategic value |

---

## F1 — Mirror Drift: Cadence Enforcement

### Diagnosis

`check_mirror_drift.py` and `delta_detector.py` exist but run on-demand only. With 965 library nodes across 8 domains, any `.ai/` mutation that doesn't sync creates silent registry drift — the worst kind because nothing breaks immediately. The evolution engine (Phase 16) references library nodes by ID; a stale registry means it operates on phantom contracts.

### Required Specs (SDD Gate — minimum 5)

| Spec File | Location | Purpose |
|-----------|----------|---------|
| `mirror_sync_cadence.spec.json` | `.ai/plan/development/F1_mirror_drift/` | Define trigger conditions: pre-commit hook, post-agent-write, scheduled interval |
| `drift_threshold_gate.spec.json` | `.ai/plan/development/F1_mirror_drift/` | Define N-node ceiling; command block behavior when exceeded |
| `drift_event_schema.spec.json` | `.ai/plan/development/F1_mirror_drift/` | JSONL entry format: `{ type, node_count_delta, affected_domains, timestamp, reasoning_hash }` |
| `dashboard_mirror_widget.spec.json` | `.ai/plan/development/F1_mirror_drift/` | Widget schema: last synced, nodes in drift, last repair hash |
| `evolution_engine_guard.spec.json` | `.ai/plan/development/F1_mirror_drift/` | Block evolution engine reads when mirror health = DEGRADED |

### Implementation Steps

1. **Wire `check_mirror_drift.py` to a scheduled cadence.** Run on every `/git auto` commit (pre-push hook) and as a standalone trigger. Not post-sync — pre-commit, so drift is caught before it lands.

2. **Add a drift threshold gate.** If delta between `.ai/` state and library registry exceeds N nodes (suggest 5), block further `/create` or `/dev` commands and surface a hard warning. Currently there is no enforcement ceiling.

3. **Emit drift events to `evolution_ledger.jsonl`.** Add a structured entry: `{ type: "mirror_drift", node_count_delta, affected_domains, timestamp }` so the history is queryable by the brainstorm agent.

4. **Add a mirror health widget to `.ai/dashboard/index.md`.** A mirror health row (last synced, nodes in drift, last repair hash) gives real operational signal. This replaces the generic "0 strategic patterns" placeholder.

### Files to Create or Modify

- `factory/library/scripts/core/check_mirror_drift.py` — add cadence trigger support
- `.github/hooks/pre-commit` — wire drift check into commit pipeline
- `.ai/logs/ledgers/evolution_ledger.jsonl` — new `mirror_drift` event type
- `.ai/dashboard/index.md` — add mirror health widget section

### Acceptance Criteria

- [ ] `check_mirror_drift.py` runs automatically on every commit and blocks push if drift > threshold
- [ ] Drift events appear in `evolution_ledger.jsonl` with full schema
- [ ] Dashboard shows mirror health row with real data
- [ ] Evolution engine reads are blocked when mirror state is DEGRADED

---

## F2 — Phases 9 & 10: Close the Open Loops

### Diagnosis

Phase 9 (Autonomous Revenue) and Phase 10 (Neural Fabric) are both `STATUS: DRAFT` with near-empty agent definitions — `revenue_orchestrator.md` and `neural_fabric_sync.md` have empty RESPONSIBILITIES sections. Phase 18 (active) references evolution and singularity concepts that build on revenue and neural infrastructure. These phases were bypassed but not formally resolved. The evolution engine may generate code assuming their contracts are live.

### Required Specs (SDD Gate — minimum 5 per phase)

**Phase 9 — Autonomous Revenue:**

| Spec File | Location | Purpose |
|-----------|----------|---------|
| `billing_adapter_contract.spec.json` | `.ai/plan/development/09_autonomous_revenue/` | Stripe + Fawry integration interface; invoice schema |
| `revenue_state_management.spec.json` | `.ai/plan/development/09_autonomous_revenue/` | Subscription lifecycle states; billing event transitions |
| `growth_loop_engine.spec.json` | `.ai/plan/development/09_autonomous_revenue/` | A/B test protocol for pricing and landing copy |
| `phase9_vs_phase14_reconciliation.spec.json` | `.ai/plan/development/09_autonomous_revenue/` | Document scope boundary between Phase 9 and Phase 14 |
| `revenue_agent_responsibilities.spec.json` | `.ai/plan/development/09_autonomous_revenue/` | Binding 3+ concrete responsibilities to `revenue_orchestrator.md` |

**Phase 10 — Neural Fabric:**

| Spec File | Location | Purpose |
|-----------|----------|---------|
| `neural_runner_contract.spec.json` | `.ai/plan/development/10_neural_fabric/` | Llama.cpp + MLX backend interface; latency SLA < 500ms |
| `latent_synthesis_protocol.spec.json` | `.ai/plan/development/10_neural_fabric/` | Candidate project generation in latent space before commit |
| `model_registry_schema.spec.json` | `.ai/plan/development/10_neural_fabric/` | `factory/knowledge/model_registry.json` schema definition |
| `neural_security_hardening.spec.json` | `.ai/plan/development/10_neural_fabric/` | Local model execution boundary; no PII in latent context |
| `neural_agent_responsibilities.spec.json` | `.ai/plan/development/10_neural_fabric/` | Binding 3+ concrete responsibilities to `neural_fabric_sync.md` |

### Implementation Steps

1. **Classify both phases explicitly as `deferred` or `absorbed`** in `_manifest.yaml`. DRAFT is ambiguous. If Phase 9 capabilities were partially absorbed into Phase 14, document the cross-reference explicitly with a `superseded_by` field.

2. **Fill `revenue_orchestrator.md` and `neural_fabric_sync.md` RESPONSIBILITIES.** Both agents have empty sections. Minimum viable: 3 concrete responsibilities each, bound to specific scripts. The evolution engine routes by role — empty contracts produce undefined behavior.

3. **Reconcile Phase 9 vs Phase 14.** `factory/library/templates/fintech/billing_adapter.py` exists and Phase 14 has `billing_adapters.spec.json`. Document whether Phase 9 is superseded by 14 or whether they serve different scopes.

4. **Apply the SDD density gate retroactively.** Each phase needs minimum 5 specs. Fill them or formally tombstone with an absorption record referencing the absorbing phase.

### Files to Create or Modify

- `.ai/plan/_manifest.yaml` — update status field for phases 9 and 10
- `.ai/agents/specialized/revenue_orchestrator.md` — fill RESPONSIBILITIES
- `.ai/agents/specialized/neural_fabric_sync.md` — fill RESPONSIBILITIES
- `.ai/plan/development/09_autonomous_revenue/` — 5 spec files
- `.ai/plan/development/10_neural_fabric/` — 5 spec files

### Acceptance Criteria

- [ ] Both phases have explicit status: `deferred` | `absorbed` | `active` (not `DRAFT`)
- [ ] Both agent files have ≥ 3 concrete RESPONSIBILITIES bound to named scripts
- [ ] Phase 9 vs Phase 14 scope boundary is documented
- [ ] Each phase has ≥ 5 spec files meeting the SDD gate
- [ ] `_manifest.yaml` cross-references are valid and navigable

---

## F3 — Deprecated Scripts: Formal Tombstoning

### Diagnosis

`factory/scripts/deprecated/` contains 10 scripts moved there silently with no rationale, no replacement mapping, and no date. Agents and humans reading the factory tree cannot distinguish "safe to delete" from "referenced somewhere upstream." At 10 scripts now this is manageable; post-singularity phase it becomes a false-positive generator in health audits.

**Current deprecated scripts:**
`app_scaffolder.py`, `collect_evolution_signals.py`, `doc_remediator.py`, `export_dashboard_data.py`, `fix_missing_metadata.py`, `intake.py`, `maintenance_bot.py`, `render_dashboard_v2.py`, `swarm_orchestrator.py`, `workspace_init.py`

### Required Specs (SDD Gate — minimum 5)

| Spec File | Location | Purpose |
|-----------|----------|---------|
| `tombstone_schema.spec.json` | `.ai/plan/development/F3_tombstoning/` | Schema for TOMBSTONE.md entries: script, date, reason enum, successor, import status |
| `import_audit_protocol.spec.json` | `.ai/plan/development/F3_tombstoning/` | Grep pass rules: patterns to check, what constitutes a live import |
| `header_comment_standard.spec.json` | `.ai/plan/development/F3_tombstoning/` | Mandatory header format for all tombstoned files |
| `audit_exclusion_rules.spec.json` | `.ai/plan/development/F3_tombstoning/` | Rules for excluding `deprecated/` from `audit_v2.py` health scoring |
| `tombstone_governance.spec.json` | `.ai/plan/development/F3_tombstoning/` | Policy: who can add to deprecated/, required approvals, max age before deletion |

### Implementation Steps

1. **Create `factory/scripts/deprecated/TOMBSTONE.md`.** One entry per script using the schema: `| script | date_deprecated | reason | superseded_by | live_imports |`

2. **Run a grep pass before tombstoning.** Check all `.py` files in `factory/` for imports from deprecated scripts. Any live import is the real bug — fix that first.

3. **Mark each file with a header comment:**
   ```python
   # TOMBSTONED: {date} | Reason: {reason} | Successor: {file} | Do not import.
   ```

4. **Add `deprecated/` exclusion to `audit_v2.py`.** Prevent deprecated scripts from inflating low-quality-file counts in health reports.

### Files to Create or Modify

- `factory/scripts/deprecated/TOMBSTONE.md` — create
- All 10 deprecated `.py` files — add tombstone header comment
- `factory/library/scripts/maintenance/audit_v2.py` — add deprecated exclusion

### Acceptance Criteria

- [ ] `TOMBSTONE.md` exists with an entry for all 10 scripts
- [ ] All 10 files have tombstone header comments
- [ ] No live script imports from `deprecated/`
- [ ] `audit_v2.py` excludes `deprecated/` from scoring
- [ ] Governance policy documented for future additions to `deprecated/`

---

## F4 — Workspace Isolation: Enforcement Logic

### Diagnosis

`audit_path_integrity.py` validates FR-2.1 and FR-2.2 (metadata pollution and sovereignty violations) but only after the fact. There is no prevention layer at scaffolding time. As soon as a real client shard is onboarded, an unguarded `workspaces/` tier is a compliance surface. Egyptian Law 151/2020 requires demonstrable residency control — naming convention alone does not pass an audit.

### Required Specs (SDD Gate — minimum 5)

| Spec File | Location | Purpose |
|-----------|----------|---------|
| `workspace_type_schema.spec.json` | `.ai/plan/development/F4_isolation/` | `workspace_type` field: enum `client` | `personal` | `staging`; required in all `metadata.json` |
| `scaffolding_gate.spec.json` | `.ai/plan/development/F4_isolation/` | Pre-scaffold validation in `saas_scaffolder.py`: type mismatch = hard block |
| `cross_contamination_rules.spec.json` | `.ai/plan/development/F4_isolation/` | Detection rules: personal slugs in client paths; client data in personal paths |
| `personal_tier_structure.spec.json` | `.ai/plan/development/F4_isolation/` | Define `workspaces/personal/` skeleton matching client structure |
| `law151_isolation_cert.spec.json` | `.ai/plan/development/F4_isolation/` | Certifiable isolation proof format for Law 151/2020 audit trail |

### Implementation Steps

1. **Add `workspace_type` field to every workspace's `metadata.json`.** Values: `client` | `personal` | `staging`. Extend `audit_path_integrity.py` to validate this field exists and is a legal value.

2. **Enforce `workspace_type` at scaffolding time in `saas_scaffolder.py`.** If target path is under `workspaces/clients/` and `workspace_type != 'client'`, block with an explicit error and log to `governance_ledger.jsonl`.

3. **Add cross-contamination detection to `healing.py`.** Scan for personal slug references inside `clients/` subtrees and flag immediately. Log to `governance_ledger.jsonl` with Law 151/2020 residency violation classification.

4. **Define `workspaces/personal/` structure formally.** Create `workspaces/personal/` with `metadata.json` skeleton and `README.md` mirroring the client structure. Leaving it undefined means the first personal shard will invent its own structure.

### Files to Create or Modify

- `workspaces/personal/metadata.json` — create skeleton
- `workspaces/personal/README.md` — create
- `factory/scripts/automation/saas_scaffolder.py` — add pre-scaffold type gate
- `factory/library/scripts/maintenance/healing.py` — add cross-contamination scan
- `factory/library/scripts/maintenance/audit_path_integrity.py` — add `workspace_type` validation

### Acceptance Criteria

- [ ] All workspaces have `workspace_type` in `metadata.json`
- [ ] `saas_scaffolder.py` hard-blocks type mismatches at scaffold time
- [ ] `healing.py` detects and logs cross-contamination
- [ ] `workspaces/personal/` has defined structure
- [ ] `governance_ledger.jsonl` captures all isolation violations
- [ ] Law 151/2020 isolation cert is generatable for any workspace

---

## F5 — Brainstorm Agent: Signal Activation

### Diagnosis

`brainstorm_suggestions.md` shows only 2 suggestions, both generic. The dashboard reports "Detected: 0 strategic patterns." `proactive_brainstorm_trigger.py` exists in `factory/library/scripts/intelligence/` but is not producing domain-specific signal. Root cause: the trigger likely reads only `workspace-index.json` (1 client, 1 project) — a data sparsity problem. The signal generator has nothing to differentiate on, and the pattern threshold is tuned for multi-workspace operation.

### Required Specs (SDD Gate — minimum 5)

| Spec File | Location | Purpose |
|-----------|----------|---------|
| `brainstorm_input_sources.spec.json` | `.ai/plan/development/F5_brainstorm/` | Define all ledger inputs: evolution_ledger, tool_performance, intelligence_ledger, workflow.jsonl |
| `single_workspace_mode.spec.json` | `.ai/plan/development/F5_brainstorm/` | Intra-project pattern detection: phase velocity, spec gaps, agent utilization imbalance |
| `pattern_threshold_config.spec.json` | `.ai/plan/development/F5_brainstorm/` | Configurable thresholds: min events before pattern fires, recency window, confidence floor |
| `phase_gap_suggestion_rule.spec.json` | `.ai/plan/development/F5_brainstorm/` | Rule: DRAFT phase older than N days with no spec additions → auto-generate suggestion |
| `suggestion_schema.spec.json` | `.ai/plan/development/F5_brainstorm/` | Structured suggestion format: id, trigger_source, evidence_events[], confidence, suggested_command |

### Implementation Steps

1. **Read `proactive_brainstorm_trigger.py` and map its input conditions.** Identify what events actually trigger it today. If it reads only `workspace-index.json`, the data sparsity is confirmed — expand inputs to the JSONL ledgers.

2. **Connect to the JSONL ledgers as signal sources.** The `evolution_ledger`, `intelligence_ledger`, and `tool_performance.jsonl` contain behavioral data. Mine for: most-run commands, most-repaired phases, agent error frequency, spec density gaps.

3. **Add single-workspace mode with lower pattern threshold.** Detect intra-project patterns: phase completion velocity, spec density gaps per phase, agent utilization imbalance (which agents are called vs which are idle).

4. **Add phase-gap suggestions explicitly.** Phases 9 and 10 being DRAFT should auto-trigger a suggestion: `"Phase 9 (Revenue) has been DRAFT for N days with no spec additions — recommend resolution via /plan blueprint"`. This bridges F2 and F5.

### Files to Create or Modify

- `factory/library/scripts/intelligence/proactive_brainstorm_trigger.py` — expand input sources and add single-workspace mode
- `.ai/dashboard/brainstorm_suggestions.md` — will be auto-populated by updated trigger
- `.ai/dashboard/index.md` — wire strategic patterns count to real signal output

### Acceptance Criteria

- [ ] Brainstorm trigger reads from ≥ 4 ledger sources
- [ ] Single-workspace mode detects ≥ 3 intra-project pattern types
- [ ] Dashboard shows > 0 strategic patterns with evidence references
- [ ] Phase-gap suggestions fire for DRAFT phases older than threshold
- [ ] All suggestions follow the structured schema with confidence score

---

## Execution Sequence

```
F1 (Mirror Sync)          ← Foundation: all other fixes produce mutations that need reliable mirroring
  └→ F3 (Tombstoning)     ← Fast win: cleans audit surface before health checks run post-fix
       └→ F4 (Isolation)  ← Preventive: must be in place before any real client shard lands
            └→ F2 (Phase Gaps) ← Deliberate: spec work follows the deferred/absorbed decision
                 └→ F5 (Brainstorm) ← Payoff: feeds on clean data that F1–F4 produce
```

## SDD Compliance Summary

| Vector | Spec Count | SDD Gate | Status |
|--------|-----------|----------|--------|
| F1 Mirror Drift | 5 specs | ✅ Met | Ready for development |
| F2 Phase Gaps | 5 specs × 2 phases = 10 specs | ✅ Met | Ready for development |
| F3 Tombstoning | 5 specs | ✅ Met | Ready for development |
| F4 Isolation | 5 specs | ✅ Met | Ready for development |
| F5 Brainstorm | 5 specs | ✅ Met | Ready for development |

---

*Governor: Dorgham | Registry: docs/01-plans/2026-04-25_aiwf-fix-plan-5-vectors.md*  
*Traceability: sha256:fix-plan-5-vectors-2026-04-25 | Compliance: Law 151/2020*
