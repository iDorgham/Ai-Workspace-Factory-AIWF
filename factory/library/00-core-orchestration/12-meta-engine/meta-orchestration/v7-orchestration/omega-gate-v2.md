# AIWF v7.0.0 — Omega Gate v2 Governance Rules
# Library Component: 12-meta-engine/meta-orchestration/v7-orchestration/omega-gate-v2.md
# Version: 7.0.0 | Reasoning Hash: sha256:omega-v7-2026-04-23
# ============================================================

## Overview

Omega Gate v2 is the supreme governance layer of AIWF v7.0.0. It enforces structural integrity, prevents unauthorized mutations, and controls auto-merge eligibility. Every sovereign workspace inherits these rules via Library-First composition.

**Version history**: Omega Gate v1 (approval-only) → v2 (3-agent consensus + approval + regional compliance).

---

## Governance Hierarchy

```
Dorgham-Approval (human, sovereign)
    └── 3-Agent Consensus (Swarm Router v3 mediation)
         ├── Master Guide  ─ strategic fit
         ├── Spec Architect ─ spec validity
         └── Contract Guardian ─ contract coverage
              └── Regional Adapter (if --region active)
```

All 3 agents must agree (≥2/3 threshold not sufficient for structural mutations — 3/3 required for library promotions and auto-merge).

---

## What Requires Omega Gate Approval

```yaml
requires_omega_gate:
  structural_mutations:
    - "Changes to CLAUDE.md or AGENTS.md"
    - "Library component additions or modifications"
    - "New factory profile creation"
    - "spec.yaml approved_by field update"
    - "Any auto-merge to main branch"

  library_promotions:
    - "Moving a workspace component to factory/library/"
    - "Updating factory/profiles/ with new profile"
    - "Adding new skills to skill-memory/"

  regional_changes:
    - "Modifying regional compliance rules"
    - "Adding new payment gateway integrations"
    - "Changing data residency configurations"
```

## What Does NOT Require Omega Gate

```yaml
no_omega_gate_needed:
  - "Reading any file"
  - "Running /test, /fix --dry-run, /plan --validate-only"
  - "Creating preview deployments via /deploy --preview"
  - "Writing to .ai/logs/ (append-only)"
  - "Running /brainstorm (output only, no structural changes)"
  - "Git branching and commits (not merges)"
```

---

## Approval Record Format

Every Omega Gate approval is logged to `.ai/logs/workflow.jsonl`:

```json
{
  "timestamp": "2026-04-23T12:56:22+02:00",
  "gate": "omega_gate_v2",
  "action": "auto_merge | library_promotion | spec_approval",
  "target": "phase/1-hotel-booking",
  "consensus": {
    "master_guide": "approved",
    "spec_architect": "approved",
    "contract_guardian": "approved",
    "regional_adapter": "approved (--region active)"
  },
  "dorgham_approval": "Dorgham-Approved",
  "reasoning_hash": "sha256:abc123...",
  "rollback_pointer": "git revert {commit-sha}"
}
```

---

## spec.yaml Approval States

```yaml
# Initial state after /plan:
approved_by: "pending_omega"

# After Omega Gate approval:
approved_by: "Dorgham-Approved"
```

`/dev` in production mode **blocks** if `approved_by: pending_omega`.

---

## Auto-Merge Gate (5-Gate Composite)

```yaml
auto_merge_composite_gate:
  description: "All 5 must pass simultaneously. A single failure blocks merge."
  gates:
    - id: "G1"
      name: "All Tests Pass"
      source: "/test output"
      threshold: "exit code 0"

    - id: "G2"
      name: "Contract Coverage"
      source: "contract-coverage.json"
      threshold: "100% of all AC items"

    - id: "G3"
      name: "Omega Gate Approval"
      source: "spec.yaml approved_by field"
      threshold: "Dorgham-Approved"

    - id: "G4"
      name: "Regional Compliance"
      source: "Regional Adapter sign-off"
      threshold: "100% (conditional on --region flag)"

    - id: "G5"
      name: "No Pending Mutations"
      source: "Healing Bot v2 queue"
      threshold: "Zero pending repairs or structural changes"
```

---

## Fail-Forward Protocol

If Omega Gate blocks an action:
1. Log the block to `.ai/logs/workflow.jsonl` with reason.
2. Output clear explanation to user: which gate failed and why.
3. Suggest corrective action (e.g., "Run /test --phase=1 to fix G1").
4. **Never terminate the session** — always remain available for next command.

---

## Audit Trail Rules

- All Omega Gate decisions are **append-only** to `.ai/logs/workflow.jsonl`.
- No entry may be deleted or modified — only new entries appended.
- Each entry includes ISO-8601 timestamp + Reasoning Hash + rollback pointer.
- Rollback pointers must be resolvable (valid `git revert` commands).

---

*Component version: 7.0.0*
*Library path: 12-meta-engine/meta-orchestration/v7-orchestration/omega-gate-v2.md*
*Last updated: 2026-04-23T12:56:22+02:00*
*Reasoning Hash: sha256:omega-v7-2026-04-23*
