```json
[
  {
    "id": "silent_factory_protocol",
    "version": "19.0.0",
    "triggers": ["/factory start", "/factory make", "/factory sync"],
    "inputs": ["client_id", "profile", "region"],
    "outputs": ["workspace_path", "trace_id"],
    "sovereign_tier": "T0",
    "traceability_schema": "ISO-8601",
    "teaching_mode_config": { "demo": true, "walkthrough": "Silent automation for project lifecycle." }
  },
  {
    "id": "library_curation_workflow",
    "version": "19.0.0",
    "triggers": ["/library create", "/library scan", "/library improve"],
    "inputs": ["component_type", "metadata"],
    "outputs": ["component_path", "validation_score"],
    "sovereign_tier": "T0",
    "traceability_schema": "ISO-8601",
    "teaching_mode_config": { "demo": true, "walkthrough": "Standards for component management." }
  },
  {
    "id": "interactive_teaching_engine",
    "version": "19.0.0",
    "triggers": ["/factory help", "/library help"],
    "inputs": ["query", "category"],
    "outputs": ["pedagogy_markdown", "demo_block"],
    "sovereign_tier": "T1",
    "traceability_schema": "ISO-8601",
    "teaching_mode_config": { "demo": false, "walkthrough": "Interactive pedagogy logic." }
  },
  {
    "id": "sovereign_memory_router",
    "version": "19.0.0",
    "triggers": ["/factory sync", "/master sync"],
    "inputs": ["shard_id", "delta_state"],
    "outputs": ["indexed_memory", "residency_confirmation"],
    "sovereign_tier": "T0",
    "traceability_schema": "ISO-8601",
    "teaching_mode_config": { "demo": true, "walkthrough": "Law 151 aware memory propagation." }
  },
  {
    "id": "auto_chain_state_machine",
    "version": "19.0.0",
    "triggers": ["--chain"],
    "inputs": ["chain_sequence", "initial_state"],
    "outputs": ["final_state", "rollback_report"],
    "sovereign_tier": "T1",
    "traceability_schema": "ISO-8601",
    "teaching_mode_config": { "demo": true, "walkthrough": "Deterministic multi-command sequencing." }
  },
  {
    "id": "predictive_drift_healing",
    "version": "19.0.0",
    "triggers": ["/factory repair", "/library fix"],
    "inputs": ["drift_metrics", "schema_definitions"],
    "outputs": ["remediation_script", "health_delta"],
    "sovereign_tier": "T0",
    "traceability_schema": "ISO-8601",
    "teaching_mode_config": { "demo": true, "walkthrough": "Autonomous remediation of structural drift." }
  },
  {
    "id": "component_contract_validator",
    "version": "19.0.0",
    "triggers": ["/library test", "/factory test"],
    "inputs": ["component_file", "contract_yaml"],
    "outputs": ["compliance_report", "violation_list"],
    "sovereign_tier": "T1",
    "traceability_schema": "ISO-8601",
    "teaching_mode_config": { "demo": true, "walkthrough": "Enforcement of industrial specs." }
  },
  {
    "id": "recursive_skill_promotion",
    "version": "19.0.0",
    "triggers": ["/library improve", "/guide learn"],
    "inputs": ["session_logs", "skill_templates"],
    "outputs": ["new_skill_manifest", "evolution_hash"],
    "sovereign_tier": "T2",
    "traceability_schema": "ISO-8601",
    "teaching_mode_config": { "demo": true, "walkthrough": "Conversion of session experience into library skills." }
  }
]
```
