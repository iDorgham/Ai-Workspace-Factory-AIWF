# `/plan` — SDD Blueprint Generator
**Version**: 7.0.0
**Agent**: Spec Architect + Contract Guardian + Regional Adapter

---

## Synopsis

```
/plan [--from=prd.md] [--phase=N] [--region=egypt|redsea|mena] [--validate-only] [--dry-run] [--auto-merge]
```

## Description

Generates a complete AIWF SDD (Spec-Driven Development) workspace from a PRD. The foundation of all implementation work — no `/dev` can run without a validated `/plan` output.

## Behavior

1. **Read PRD**: Load `00-prd/prd.md` and `requirements-trace.json`.
2. **Spec Architect**: Generate `spec.md` (human narrative) + `spec.yaml` (machine contract).
3. **Architecture**: Produce `design.md` with Mermaid diagrams, data flow, security model, RTL notes.
4. **Database**: Generate `db-schema.sql` + `db-erd.md` (cardinality, FK logic, data residency rules).
5. **Task Graph**: Build `tasks.json` with dependency-mapped, agent-assigned tasks.
6. **Contracts**: Create `contracts/api-contract.yaml`, `contracts/state-contract.json`, `contracts/test-fixtures/`.
7. **Regional** (when `--region` active): Populate `regional/egypt-compliance.md`, `regional/mena-adaptations.json`.
8. **Validation Gates**: Run before finalizing output:
   - `spec-lint`: All spec.yaml fields populated.
   - `contract-check`: All ACs have test fixtures.
   - `trace-matrix`: All REQ-IDs traced PRD → spec → tests.
   - `regional-compliance`: MENA flags valid (if `--region` active).
9. **Write `_manifest.yaml`**: Version, phases, status, omega_gate_status, regional_flags.

## Validation Gates

| Gate | Threshold | Blocks? |
| :--- | :--- | :--- |
| spec-lint | 100% | ✅ Yes |
| contract-check | 100% | ✅ Yes |
| trace-matrix | 100% | ✅ Yes |
| regional-compliance | 100% (if --region) | ✅ Yes |

## Flags

| Flag | Description |
| :--- | :--- |
| `--from=prd.md` | Source PRD file path (default: `00-prd/prd.md`). |
| `--phase=N` | Generate plan for a specific phase only. |
| `--region=egypt\|redsea\|mena` | Activate Regional Adapter and populate `regional/` folder. |
| `--validate-only` | Run validation gates without regenerating plan files. |
| `--dry-run` | Show what would be generated without writing files. |
| `--auto-merge` | Set auto-merge eligibility flag in `_manifest.yaml`. |

## Output Structure

```
plan/
├── _manifest.yaml
├── 00-prd/
│   ├── prd.md
│   └── requirements-trace.json
├── 01-<phase-slug>/
│   ├── spec.md
│   ├── spec.yaml
│   ├── design.md
│   ├── db-schema.sql
│   ├── db-erd.md
│   ├── tasks.json
│   ├── contracts/
│   │   ├── api-contract.yaml
│   │   ├── state-contract.json
│   │   └── test-fixtures/
│   ├── prompts/
│   ├── templates/
│   ├── regional/
│   │   ├── egypt-compliance.md
│   │   └── mena-adaptations.json
│   └── validation/
│       ├── spec-lint-report.md
│       ├── contract-coverage.json
│       └── trace-matrix.json
└── _archive/
```

## spec.yaml Schema

```yaml
phase_id: "01-<slug>"
version: "1.0.0"
description: string
requirements: [REQ-001, REQ-002]
acceptance_criteria:
  - id: "AC-001"
    description: string
    test_fixture: "tests/fixtures/ac-001.json"
    contract_gate: true
dependencies: []
sovereign_boundary: "client-only | shared | restricted"
tech_stack: []
regional_compliance:
  target_regions: ["egypt", "redsea", "mena"]
  requirements: []
  feature_flags:
    rtl_layout: boolean
    local_payments: ["Fawry", "Vodafone Cash"]
    data_residency: "Law 151/2020"
approved_by: "pending_omega | Dorgham-Approved"
evolution_hash: "sha256:..."
```

## Examples

```
/plan --from=00-prd/prd.md --region=redsea
/plan --phase=1 --validate-only
/plan --from=AIWF-PRD.md --region=egypt --dry-run
```

---

*Command version: 7.0.0 | Last updated: 2026-04-23*
