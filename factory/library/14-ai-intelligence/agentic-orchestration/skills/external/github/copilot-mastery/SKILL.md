# 🤖 GitHub Copilot Master Mastery

## Purpose
Enforce standards for maximizing the "Pair Programming" capacity of GitHub Copilot and Copilot Extensions. This skill focuses on the logic of "Prompt Engineering for IDEs," ensuring that the AI has the correct file context and instructions to generate high-fidelity, pattern-aligned code.

---

## Technique 1 — Context Orchestration (#-Commands)
- **Rule**: Never ask a generic question; always provide the exact context using `#file`, `#selection`, or `#terminal`.
- **Protocol**: 
    1. Identify the files containing the logic you want to modify or reference.
    2. Use the workspace-wide search (#codebase) for architectural questions.
    3. Provide "Instruction Files" (e.g., .cursorrules or similar) for Copilot to follow during generation.

---

## Technique 2 — Iterative Refinement (The 80/20 Loop)
- **Rule**: Accept the "First Draft" as 80% correct; use the chat to fix the remaining 20% through specific, incremental instructions.
- **Protocol**: 
    1. Ask Copilot to generate the boilerplate.
    2. Review for anti-patterns or missing domain logic.
    3. Provide a follow-up instruction to adjust specific lines or add error handling.
    4. Validate using the built-in "Copilot Tests" generation.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Silent Autocomplete** | Drift from standards | Treat autocomplete as a "Suggestion," never blind-accept; verify against the PRD. |
| **Missing PRD Context** | "Hallucinated" features | Always reference the `#file:PRD.md` when asking Copilot to scaffold new modules. |
| **Generic Prompts** | Low-quality boilerplate | Be specific: "Implement a Tailwind-styled React component using HSL colors and GSAP animations." |

---

## Success Criteria (Copilot QA)
- [ ] Coding velocity (time to completion) increased by 40%+.
- [ ] Code quality (measured by lint/build success) is 95%+.
- [ ] Copilot is used for "Explanatory" purposes (understanding legacy code) at least 30% of the time.
- [ ] Extension-based workflows (e.g., Azure Extensions) are utilized for cloud deployments.