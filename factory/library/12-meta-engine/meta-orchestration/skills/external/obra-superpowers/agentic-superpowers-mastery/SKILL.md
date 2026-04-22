# ⚡ Obra Agentic Superpowers

## Purpose
Enforce modern multi-agent orchestration patterns including parallel dispatching, systematic debugging, and subagent-driven development. This skill focuses on the "Brainstorm-Plan-Execute-Verify" lifecycle to ensure autonomous agent reliability.

---

## Technique 1 — Parallel Subagent Dispatching
- **Rule**: Tasks that are mutually exclusive (e.g., scraping 10 different sites) must be dispatched to parallel subagents to maximize computational velocity.
- **Protocol**: 
    1. Define the input/output contract for each subagent.
    2. Spawn workers with specific roles and scope.
    3. Synthesize the return results into a master report using the `@Cortex` aggregator.

---

## Technique 2 — Systematic Debugging Protocol
- **Rule**: Never "Guess" at a fix; always isolate the failure point using the "Bisection" method.
- **Protocol**: 
    1. Reproduce the failure with a minimal test case.
    2. Check state at precisely the halfway point of the logic flow.
    3. Narrow the failure window until the offending line/logic-gate is identified.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Silent Failures in Parallelism** | Poisoned aggregator | Every subagent must return a `SUCCESS/FAILURE` status with a trace. |
| **Vague Brainstorming** | Logical drift | All brainstorms must conclude with a "Feasibility Ranking" and immediate Action Items. |
| **Skipping Verification** | Regressions | Implement a "Strict Verification" step after every code edit; run existing tests to ensure O% regression. |

---

## Success Criteria (Superpowers QA)
- [ ] Multi-agent tasks complete with > 90% autonomous success rate.
- [ ] Debugging cycles identify the root cause in < 3 iterations.
- [ ] Every plan has a corresponding "Verification" block.
- [ ] Subagents stay strictly within their assigned `TaskScope`.