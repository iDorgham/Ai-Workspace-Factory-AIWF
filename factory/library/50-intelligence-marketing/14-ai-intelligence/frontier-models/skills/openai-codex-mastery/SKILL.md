---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# 🤖 OpenAI & Codex Mastery (Omega-tier)


## Purpose
Enforce professional standards for utilizing OpenAI GPT-4o and Codex-family models. This skill focuses on **Function Calling**, **Structured Output (JSON Mode)**, and high-precision code generation.

---

## Technique 1 — High-Precision Code Generation (Codex)

### "Context-Slicing" for Model Purity
- **Rule**: Do not feed the model more than 1,000 lines of code per prompt. Use specific "Slice Targets."
- **Protocol**: Provide the `Interface` or `Header` definitions first, followed by the specific `Implementation` logic to be modified.

---

## Technique 2 — Structured Output & Tool Use

### Function Calling Protocols
- **Schema Enforcement**: All tool definitions must include strict `Required` parameters and high-density `Description` fields to minimize model hallucination.
- **JSON Mode**: Always use `response_format: { "type": "json_object" }` for programmatic parsing of AI intelligence.

---

## Technique 3 — Token Economy

| Strategy | Action | Result |
| :--- | :--- | :--- |
| **Logit Bias** | Force specific tokens (e.g., forcing a "Yes/No" response). | 98% reduction in "Chatter" noise. |
| **Stop Sequences** | Terminate generation at `\n\n` or `###`. | Prevents redundant or runaway tokens. |
| **System Prompting** | Move all "Role" and "Rules" to the System layer. | Maintains instruction adherence over long turns. |

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Vague Prompting** | Hallucinations | Use "Chain-of-Thought" (CoT) prompting for complex logic. |
| **Ignoring Seed Values** | Non-deterministic output | Use `seed` parameter for reproducible testing and audits. |
| **Max Token Ceiling** | Cut-off code | Calculate `max_tokens` based on input/output headroom (target 4096). |

---

## Success Criteria (OpenAI QA)
- [ ] Code generated compiles/passes lint with zero manual edits.
- [ ] JSON outputs are valid and schema-compliant.
- [ ] Tool selection accuracy > 95% in multi-tool scenarios.
