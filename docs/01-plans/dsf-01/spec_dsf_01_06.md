# 📐 spec_dsf_01_06: @aiwf/sovereign-ui CLI Scaffolder

Implements the `npx @aiwf/sovereign-ui init` CLI command for rapid, consistent Design System integration across distributed shards.

## 📋 Narrative
To ensure industrial-scale scaling, the design system must be easy to install and initialize. The CLI automates the injection of `tokens.css`, Tailwind v4 configurations, and the core utility library (`utils.ts`). This ensures that every new project shard starts from a verified OMEGA-tier foundation.

## 🛠️ Key Details
- **Command**: `init`.
- **Logic**: Automated file scaffolding and dependency injection.
- **Entry Point**: `factory/library/scripts/sovereign_ui_init.py`
- **Audit**: Registry update and silent versioning upon completion.

## 📋 Acceptance Criteria
- [ ] CLI bootstraps a fresh shard in < 3 seconds.
- [ ] 100% structural parity across materialized shards.
- [ ] Automated registry synchronization verified.

## 🛠️ spec.yaml
```yaml
phase_id: dsf-01
evolution_hash: sha256:dsf-v20-01-06-d9b3e1
acceptance_criteria:
  - cli_bootstrap_verified
  - shard_init_equilibrium_pass
  - registry_sync_active
test_fixture: tests/design/cli/init_audit.py
regional_compliance: LAW151-MENA-CLI-SOVEREIGNTY
```
