# 🤖 Wshobson Agent Orchestration

## Purpose
Enforce standards for state-aware multi-agent workflows. This skill focuses on cyclic graphs, persistent memory management, and agent-to-agent delegation protocols to build robust, iterative AI systems.

---

## Technique 1 — Cyclic Graph Workflow
- **Rule**: All complex tasks must use a "Check-and-Loop" pattern.
- **Protocol**: 
    1. Agent A generates a draft.
    2. Agent B (Reviewer) critiques the draft.
    3. If the critique identifies errors, the state is sent back to Agent A for revision.
    4. Loop terminates only when Agent B issues a "PASS" signal.

---

## Technique 2 — Context Slicing (Memory Management)
- **Rule**: Never pass the entire conversation history; slice the context to keep it relevant to the current task.
- **Protocol**: 
    1. Identify the "Critical Context" (PRD, current error, latest file state).
    2. Discard "Noise" (older chat logs, irrelevant file histories).
    3. Inject specifically requested background knowledge via RAG (Retrieval Augmented Generation).

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Endless Feedback Loops** | Token drain / Timeout | Implement a `max_iterations` guard (e.g., 5 loops) before automatic escalation. |
| **Blind Delegation** | Context fragmentation | Ensure every delegated task includes the "Global Goal" and "Immediate Constraints." |
| **Flat History Padding** | Context overflow | Always summarize long conversations before continuing to the next phase. |

---

## Success Criteria (Orchestration QA)
- [ ] Multi-agent loops converge on a correct solution in < 4 iterations.
- [ ] Context window usage is optimized (< 20% saturation per turn).
- [ ] No "Hallucination cascades" observed in agent-to-agent communication.
- [ ] High-accuracy task handoffs with 100% contract adherence.