# State Contract — {{PHASE_NAME}}

**Contract Type:** State / Data Model  
**Reasoning Hash:** {{REASONING_HASH}}  

---

## State Definitions

```yaml
states:
  - id: "DRAFT"
    description: "Initial state — spec created but not reviewed"
    allowed_transitions: ["REVIEW", "DELETED"]
    owner: "spec_architect_v2"

  - id: "REVIEW"
    description: "Under quality review"
    allowed_transitions: ["APPROVED", "DRAFT"]
    owner: "factory_orchestrator"

  - id: "APPROVED"
    description: "Cleared for activation"
    allowed_transitions: ["ACTIVE", "DRAFT"]
    prerequisite: "spec_density_gate_v2 PASS"
    owner: "factory_orchestrator"

  - id: "ACTIVE"
    description: "In execution"
    allowed_transitions: ["COMPLETED", "DEPRECATED"]
    owner: "{{AGENT}}"

  - id: "COMPLETED"
    description: "All tasks done, phase closed"
    allowed_transitions: []
    requires: "all tasks.json tasks status=completed"

  - id: "DEPRECATED"
    description: "Superseded — tombstone pending"
    allowed_transitions: ["TOMBSTONED"]

  - id: "TOMBSTONED"
    description: "Hard-deprecated per F3 protocol"
    allowed_transitions: []
    ttl: "2 release cycles"
```

---

## Transition Guards

| Transition | Guard Condition |
|------------|----------------|
| DRAFT → REVIEW | All required spec files present |
| REVIEW → APPROVED | spec_density_gate_v2 ≥ 12 files, C4 present |
| APPROVED → ACTIVE | OMEGA Gate v3 PASS, Law 151 cert generated |
| ACTIVE → COMPLETED | All tasks.json entries status=completed |
