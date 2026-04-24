# 📐 spec_dsf_02_02: Composable Shell Layout

Materializes the three-pillar industrial dashboard shell: Collapsible Sidebar, Fixed Header, and Fluid Content Area.

## 📋 Narrative
The dashboard shell is the primary container for all shard operations. It implements a **Collapsible Sidebar** for navigation, a **Fixed Header** for global actions (Profile, Notifications), and a **Fluid Content Area** for vertical-specific data. Every layout property is mapped to Sovereign-UI tokens, ensuring visual consistency across all shards.

## 🛠️ Key Details
- **Components**: `DashboardShell`, `Sidebar`, `Header`.
- **Logic**: CSS Grid for layout structure; Tailwind v4 container queries for responsiveness.
- **Entry Point**: `components/dashboard/Shell.tsx`.

## 📋 Acceptance Criteria
- [ ] Seamless transition between collapsed and expanded sidebar states.
- [ ] 100% RTL visual equilibrium (Header icons flip correctly).
- [ ] Verified sticky-header performance on mobile scroll.

## 🛠️ spec.yaml
```yaml
phase_id: dsf-02
evolution_hash: sha256:dsf-v20-02-02-b2c3d4
acceptance_criteria:
  - shell_layout_equilibrium_pass
  - rtl_flip_accuracy_verified
  - responsive_breakpoint_audit_100
test_fixture: tests/shard/layout_audit.py
regional_compliance: LAW151-MENA-LAYOUT-SOVEREIGNTY
```
