# Auto Optimization Loop

## Purpose

Recalculate **capability routing weights** from observed outcomes so predictive routing favors reliable agents. Filesystem-native: weights live in **`sos/runtime-capability-weights.json`** (JSON next to runtime state; create on first optimization).

## Cadence

- **N** default = **5** completed tasks since last optimization (configurable in `sos/runtime-state.md` as `optimization_every_n_tasks: 5`).
- Also runs on `/swarm optimize --auto` (single pass).

## Metrics per `agent_id` (from capability registry slug, e.g. `frontend`)

| Field | Meaning |
|-------|---------|
| `successes` | Tasks completed without reroute-from-failure |
| `failures` | Tasks marked `failed` or rerouted after failed gate |
| `success_rate` | `successes / max(1, successes + failures)` |

## Weight Formula (deterministic)

```
failure_penalty = failures / max(1, successes + failures)
weight = (success_rate * 0.7) - (failure_penalty * 0.3)
```

Clamp `weight` to `[0.0, 1.0]`.

## Predictive Routing Rules

| Condition | Action |
|-----------|--------|
| `success_rate < 0.5` | **Demote:** subtract `0.15` from weight; push agent to end of candidate list for matching `task_types`. |
| Fallback agent `success_rate > 0.8` | **Promote:** add `0.1` to weight; prefer as secondary when primary demoted. |
| Tie-break | Higher `weight`, then lexicographic `agent_id`. |

## Output File — `sos/runtime-capability-weights.json`

```json
{
  "format_version": "1.0",
  "updated_at": "ISO8601",
  "trace_id": "RT-...",
  "optimization_counter": 0,
  "weights": {
    "frontend": { "raw_score": 0.58, "routing_bias": 0.0, "success_rate": 0.85, "failures": 1, "successes": 6 },
    "backend": { "raw_score": 0.42, "routing_bias": -0.15, "success_rate": 0.4, "failures": 3, "successes": 2 }
  }
}
```

- **`routing_bias`:** accumulated demote/promote deltas (clamp [-0.3, 0.3]).
- **`raw_score`:** formula output before bias.

## Integration

- **@RuntimeOrchestrator** reads weights during reassignment after **@ErrorDetective**.
- **@Router** may read weights for plan-time suggestions only; SOS outputs still immutable at runtime.

## 🌍 Regional Calibration (MENA Context)

- **Cultural Alignment:** Ensure all logic respects regional business etiquette and MENA market expectations.
- **RTL Compliance:** Logic must explicitly handle Right-to-Left (RTL) flow where relevant.

## 🛡️ Critical Failure Modes (Anti-Patterns)

- **Anti-Pattern:** Generic Output -> *Correction:* Apply sector-specific professional rules from RULE.md.
- **Anti-Pattern:** Global-Only Logic -> *Correction:* Verify against MENA regional calibration.

---

*Consumed by: `/swarm optimize --auto` · `/swarm run --auto` (every N tasks)*