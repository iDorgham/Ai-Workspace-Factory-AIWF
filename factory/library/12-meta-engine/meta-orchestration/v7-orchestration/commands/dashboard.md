# 🏗️ COMMAND: /dashboard
**Syntax**: `/dashboard`
**Agent**: T0 Master Guide
**Objective**: Interactive terminal monitoring of all factory workspaces.

---

## 🛠️ Execution Flow

1. **Discovery**: Scan `workspaces/` for all managed projects.
2. **Aggregation**: Query status, sync version, and last activity for each project.
3. **Rendering**: Launch the `Rich`-based TUI.
4. **Live Monitoring**: Refresh every 5s with latest filesystem signals.

---

## 📊 Features
- **Project Grid**: Real-time status (Active/Inactive).
- **Sync Tracker**: Verify if projects are on v7.2.0+.
- **Activity Log**: Watch files and mutations across the whole factory.

*Reasoning Hash: sha256:cmd-dash-2026-04-23*
