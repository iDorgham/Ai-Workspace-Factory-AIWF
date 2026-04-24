# 📐 spec_dsf_02_06: Command Palette & Global Search

Materializes a high-speed `Ctrl+K` command palette for rapid shard navigation and agent-driven action execution.

## 📋 Narrative
Industrial efficiency requires low-latency control. We implement a **Global Command Palette** using Radix UI primitives and Sovereign-UI styling. The palette enables users to search for dashboard pages, execute common actions (e.g., "Create Shard"), and query the AI agent without leaving the keyboard.

## 🛠️ Key Details
- **Trigger**: `Ctrl+K`.
- **Logic**: Fuse.js for fuzzy search; integration with dashboard routes.
- **Entry Point**: `components/dashboard/CommandPalette.tsx`.

## 📋 Acceptance Criteria
- [ ] Search results appear in < 50ms with fuzzy matching.
- [ ] 100% keyboard-only navigation pass (Arrows + Enter).
- [ ] Verified RTL search-input alignment.

## 🛠️ spec.yaml
```yaml
phase_id: dsf-02
evolution_hash: sha256:dsf-v20-02-06-f6g7h8
acceptance_criteria:
  - search_latency_target_met
  - keyboard_navigation_verified
  - command_execution_equilibrium_pass
test_fixture: tests/shard/search_audit.py
regional_compliance: LAW151-MENA-CMD-SOVEREIGNTY
```
