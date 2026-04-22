# 📓 Global Agent Playbook

## Purpose
Enforce a standardized "Moral & Tactical" code for all agents in the factory. This skill focuses on maintaining common mental models, ensuring uniform response patterns, and preventing divergent behaviors in complex multi-step pipelines.

---

## Technique 1 — Recursive Self-Correction
- **Rule**: Every output must be internally validated against the "Global Objective" before being emitted.
- **Protocol**: 
    1. Generate the initial thought.
    2. Review against the `PLAYBOOK.md` constraints.
    3. Modify the thought to align with the core philosophy (e.g., "Accuracy over Speed").
    4. Emit the final response.

---

## Technique 2 — Atomic Action Logging
- **Rule**: Every action that modifies the environment must be logged with its "Reasoning" and "Expected Result."
- **Protocol**: 
    1. Log the intent.
    2. Perform the action.
    3. Log the observed outcome.
    4. Update the "Environmental Belief" state.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Philosophical Drift** | Inconsistent agent personas | Re-inject the Core Playbook values at the start of every long-running thread. |
| **Verbose Justification** | Context bloat | Keep reasoning logs dense and technical; avoid "Conversational Fluff." |
| **Ignoring Failed Beliefs** | Persistent hallucinations | If an action fails to yield the expected result, mark that "Belief" as false and trigger a re-plan. |

---

## Success Criteria (Playbook QA)
- [ ] 100% of agents exhibit unified persona characteristics.
- [ ] Audit logs show clear, linked "Resoning -> Action -> Result" chains.
- [ ] No "divergent logic" detected in multi-agent handoffs.
- [ ] All responses adhere to the localized (AR/EN) linguistic standards.