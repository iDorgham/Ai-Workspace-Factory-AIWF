# 📁 Planning with Files (SDD)

## Purpose
Enforce standards for Spec-Driven Development (SDD) where the "Truth" of a project is maintained in permanent markdown artifacts rather than chat history. This skill focuses on the creation and maintenance of `implementation_plan.md`, `task.md`, and `walkthrough.md`.

---

## Technique 1 — The Artifact State-Machine
- **Rule**: Every turn must begin with a review of the `task.md` file.
- **Protocol**: 
    1. Read the current task list.
    2. Identify the immediate next item.
    3. Execute the item.
    4. Update the artifact to reflect the new state (`[/]` for in-progress, `[x]` for complete).

---

## Technique 2 — Atomic Discovery Capture
- **Rule**: When new information is discovered during coding, it must be captured in the `implementation_plan.md` immediately.
- **Protocol**: 
    1. Encounter a structural fact (e.g., "The API requires a specific header").
    2. Halt coding.
    3. Update the Implementation Plan to include this technical constraint.
    4. Resume coding based on the updated spec.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)
| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Drifting Tasks** | Unreliable progress tracking | Ensure `task.md` is updated synchronously with every major code change. |
| **Spec-Coding Divergence** | "Spaghetti" integration | ALWAYS update the plan before changing architectural direction. |
| **Vague Walkthroughs** | Information loss | Walkthroughs must link directly to the modified files and provide a "Verification proof" (e.g., test result). |

---

## Success Criteria (SDD QA)
- [ ] `task.md` perfectly matches the current workspace reality.
- [ ] 100% of structural decisions are recorded in the `implementation_plan.md`.
- [ ] Transition between turns is seamless because state is persisted in files.
- [ ] Final `walkthrough.md` provides a zero-friction handoff to the user.