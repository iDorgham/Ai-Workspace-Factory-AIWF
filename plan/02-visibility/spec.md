# 🛰️ SPEC: AIWF Operational Visibility (v7.5)
**Phase:** 2 | **Status:** DRAFT | **Reasoning Hash:** sha256:phase2-spec-2026-04-23

---

## 1. Executive Summary
Phase 2 implements the **Omega Dashboard** (TUI) and the **Swarm Router**, providing real-time telemetry and parallel command execution across the entire factory ecosystem.

---

## 2. Requirements (REQ-DASH)

### [REQ-DASH-001] — Omega Dashboard (TUI)
- **Syntax**: `/dashboard`
- **AC**: Must display real-time status of 20+ workspaces simultaneously.
- **AC**: Must show sync version (e.g., v7.2.0) and last mutation timestamp.

### [REQ-DASH-002] — Parallel Swarm Router
- **Syntax**: `/swarm "<command>"`
- **AC**: Execute commands in parallel using ThreadPoolExecutor.
- **AC**: Aggregate results (Success/Fail/Duration) into a summary table.

---

## 3. Architecture Layer
- **UI**: Python `Rich` library (fallback to `print` for Lite mode).
- **Communication**: Local filesystem polling (Phase 2.1) ➔ WebSocket Relay (Phase 2.2).

---

*Spec version: 1.0.0*
