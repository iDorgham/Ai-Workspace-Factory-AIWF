---
type: Generic
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# 📜 Spec-to-Implementation Flow

## Purpose
Enforce standards for bridging the gap between high-level PRDs and concrete code implementation. This skill focuses on the "Contract-First" approach, where the technical specification must be finalized and verified before a single line of application logic is written.

---

## Technique 1 — The "Strict Verification" Bridge
- **Rule**: Every requirement in the `PRD.md` must have a corresponding "Validation Plan" before implementation.
- **Protocol**: 
    1. Parse the requirement (e.g., "The API must handle 100 req/sec").
    2. Define the test case (e.g., "Script a k6 load test targeting endpoint X").
    3. Document the expected result in the `implementation_plan.md`.
    4. Only proceed to code once the test case is approved.

---

## Technique 2 — Narrative Handoff (The Walkthrough)
- **Rule**: Every implementation phase must conclude with a "Narrative Walkthrough" that explains *why* structural decisions were made.
- **Protocol**: 
    1. Group related changes by feature.
    2. Provide direct links to the modified files.
    3. Summarize any "Technical Debt" or "Assumptions" made during the turn.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)
| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Logic Leapfrogging** | Unverifiable code | Never write code that isn't mapped to a specific requirement in the PRD. |
| **Silent Spec Changes** | Information fragmentation | Update the PRD/Spec immediately if coding reveals the original plan is unfeasible. |
| **Placeholder Verification** | False positives | Validation plans must be concrete; "I'll check it later" is an automatic failure. |

---

## Success Criteria (Spec-to-Implementation QA)
- [ ] 1:1 Mapping between Requirements and Validation Plans.
- [ ] 0% of code is "un-specced."
- [ ] Final implementation passes all predefined verification steps.
- [ ] Documentation is persistent and understandable by both human and AI reviewers.