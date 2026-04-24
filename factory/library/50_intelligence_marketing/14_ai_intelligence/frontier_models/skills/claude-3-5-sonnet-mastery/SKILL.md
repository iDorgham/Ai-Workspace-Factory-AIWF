---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# 🦅 Claude 3.5 Sonnet Mastery (Omega-tier)


## Purpose
Enforce professional standards for utilizing Anthropic's Claude 3.5 Sonnet. This skill focuses on **Instruction Character Counts**, **XML-Structured Prompting**, and high-density reasoning for complex system refactors.

---

## Technique 1 — XML-Tagging for Precision

### Structured Information Injection
- **Rule**: Use XML tags to separate "Code," "Context," and "Instructions."
- **Example**:
    ```xml
    <context>
      [System context or file content here]
    </context>
    <instruction>
      [Specific task to perform]
    </instruction>
    ```
- **Benefit**: Drastically reduces model confusion in long-context scenarios (up to 200k tokens).

---

## Technique 2 — Reasoning & Chain-of-Thought (CoT)

### The "Thinking" Layer
- **Rule**: For any task requiring logic (Math, Refactoring, Planning), force the model to output a `<thinking>` block before the final answer.
- **Protocol**: "Begin your response with a <thinking> tag where you analyze the problem step-by-step."

---

## Technique 3 — Coding Protocols

| Strategy | Action | Result |
| :--- | :--- | :--- |
| **Artifact Logic** | Use for discrete blocks (Code, Docs). | Identifies reusable "Leaf" components. |
| **Differential Edits** | Ask for diffs or specific line replacements. | Minimizes token output and increases accuracy. |
| **Markdown Mastery** | Utilize full GFM (GitHub Flavored Markdown). | Ensures high readability of AI-generated docs. |

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Conversational Padding** | Token waste | Use "Be concise" and "Direct answer" instructions. |
| **Mixing Code/Text** | Parsing errors | Force code into fenced blocks with language identifiers. |
| **Instruction Floating** | Overlooked rules | Place critical instructions at the very **end** of the prompt (Recency bias optimization). |

---

## Success Criteria (Claude QA)
- [ ] Reasoning (`<thinking>`) correctly identifies edge cases.
- [ ] Code snippets are optimized for the target framework (e.g., React hooks correctly used).
- [ ] XML structure is maintained through the entire turn.
- [ ] Instruction adherence remains high across 100k+ token contexts.
