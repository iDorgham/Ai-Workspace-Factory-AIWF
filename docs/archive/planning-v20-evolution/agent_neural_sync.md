# 🤖 AGENT SPECIFICATION: Neural Fabric Sync Agent
**Version**: 1.0.0 (v20.0-compat)
**Tier**: T1 Specialist (Candidate for T0)
**Role**: Bidirectional Outbound Mirror Orchestrator
**Status**: DRAFT / BLUEPRINT

---

## 1. Objective
The **Neural Fabric Sync Agent** replaces the legacy `sync_engine.py`. Its primary objective is to maintain **Industrial Equilibrium** between the Active-Set (`.ai/`) and the Archive-Set (`factory/library/`) through event-driven, bidirectional synchronization.

## 2. Core Logic & Behavioral Protocols

### 2.1 Event-Driven Propagation
- **Monitor**: Actively watches for `inotify` / `fsevents` on the `.ai/` directory.
- **Trigger**: Any mutation (create, update, delete) in `.ai/` triggers a sync event.
- **Latency Target**: < 10ms propagation delay.

### 2.2 Bidirectional Outbound Mirror Protocol
- **Primary Flow**: `.ai/` (Active) → `factory/library/` (Archive).
- **Secondary Flow**: `factory/library/` → `.ai/` (Only for validated global updates).
- **Conflict Resolution**: Defaults to `.ai/` state. Discrepancies are logged as `SYNC_CONFLICT` in the governance ledger.

### 2.3 Schema-Gated Integrity
- Before any file is mirrored, the agent invokes the **Integrity Auditor** to validate:
    1. **Naming**: Must be `snake_case`.
    2. **Metadata**: Must contain valid `evolution_hash` and `iso-8601` timestamp.
    3. **Residency**: Validates Law 151/2020 geofencing for sensitive shards.

## 3. Integration Matrix

| Agent | Interaction Type | Purpose |
| :--- | :--- | :--- |
| **Integrity Auditor** | Validation Call | Pre-sync schema check. |
| **Recursive Engine** | Learning Hook | Extracts sync friction to refine propagation logic. |
| **Healing Bot v2** | Remediation Hook | Triggers repair if the mirror fails to achieve equilibrium. |

---

## 4. Operational Commands
- `/factory sync --deep`: Full reconciliation of active and archive sets.
- `/factory sync --watch`: Enables real-time neural propagation.
- `/factory sync --audit`: Generates a synchronization health report.

---
*Evolution Hash: sha256:agent-sync-v20-logic-2026-04-25T01:10:00*
*Governor: Dorgham* | *Registry Version: 19.0.0*
