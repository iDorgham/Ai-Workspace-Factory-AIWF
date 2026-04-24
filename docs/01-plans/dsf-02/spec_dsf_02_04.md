# 📐 spec_dsf_02_04: Industrial Data Grids & Tables

High-density data tables using `@aiwf/sovereign-ui` primitives, featuring virtualized scrolling and server-side filtering.

## 📋 Narrative
Data presentation is core to the industrial dashboard. We implement a **High-Density Data Grid** that leverages TanStack Table logic with Sovereign-UI styling. The grid supports virtualized scrolling for massive datasets and server-side operations to ensure the dashboard remains reactive even with 100,000+ records.

## 🛠️ Key Details
- **Base Logic**: TanStack Table (React Table).
- **Styling**: `@aiwf/sovereign-ui/Table`.
- **Logic**: Virtualized scrolling; server-side sorting/filtering.

## 📋 Acceptance Criteria
- [ ] Virtualized scrolling verified with 10,000 rows at 60fps.
- [ ] Server-side filtering hooks integrated and testable.
- [ ] WCAG 2.2 AA compliant focus states and keyboard navigation.

## 🛠️ spec.yaml
```yaml
phase_id: dsf-02
evolution_hash: sha256:dsf-v20-02-04-d4e5f6
acceptance_criteria:
  - virtualization_performance_pass
  - server_action_filtering_verified
  - accessibility_audit_100
test_fixture: tests/shard/data_grid_audit.py
regional_compliance: LAW151-MENA-DATA-SOVEREIGNTY
```
