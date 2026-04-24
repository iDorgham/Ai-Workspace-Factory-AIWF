# SOS root template (reference copy)

Use these files as **starting points** when you add SOS to a feature:

- Copy into **`.ai/plans/active/features/[feature-id]/sos/`** (recommended).
- A **repo-root** `sos/` folder is **optional** only for rare global swarms; keep the root clean by default.

| File | Purpose |
|------|---------|
| **`runtime-state.md`** | Schema + YAML template for `@RuntimeOrchestrator` |
| **`runtime-capability-weights.json`** | Empty weights envelope for `/swarm optimize --auto` |

**Discovery:** `scripts/validate/runtime_state_guard.py` checks root `sos/runtime-state.md` if present **and** every **`.ai/plans/active/features/*/sos/runtime-state.md`**.

---

*See: `docs/workspace/reference/feature-plan-package-layout.md`*
