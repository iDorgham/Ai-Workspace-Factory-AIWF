# 🤖 AI Automation Lab Operations

## Purpose
Enforce professional operational and technical standards for the AI Automation Lab vertical. This skill focuses on **Prompt-Engineering Pipelines**, **n8n Workflow Design**, and **Multi-Agent Tuning** protocols.

---

## Technique 1 — Prompt-Engineering Pipelines (The Physics of Instruction)

### Structural Prompting Standard
- **Context Priming**: Every system prompt must define a "Persona" (The Agent identity), "Constraint Set" (What NOT to do), and "Output Schema" (JSON/Markdown format).
- **Few-Shot Injectors**: Utilize high-density examples within the prompt to guide the LLM toward the "Omega-Tier" output style.

---

## Technique 2 — n8n Workflow & Orchestration Design

- **The "Node-Modular" Standard**: Design n8n workflows using a "Master-Child" architecture. Large, monolithic workflows must be broken into smaller, decoupled sub-flows triggered by Webhooks to ensure scalability and error-isolation.
- **Error-Trap Logic**: Every external API call (e.g., to OpenAI, Anthropic, or CRM) must have a parallel "Error Branch" that triggers an alert via the `agents:10-operations-qa/performance-ops/EscalationHandler`.

---

## Technique 3 — Multi-Agent Tuning & Logic Validation

- **Agent Consistency Tests**: Run automated tests comparing the outputs of different agent models against a "Gold Standard" dataset. 
- **Latency Benchmarking**: Enforce the `skills:14-ai-intelligence/ai-ops/agent-computational-velocity-protocol`. Any agent response taking > 15 seconds for a non-reasoning task must be pruned for context bloat.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Logic Leaks** | Hallucinations | Use "Strict JSON" output modes to ensure that the logic remains machine-readable and predictable. |
| **Infinite Loops** | API Bill Shock | Implement a "Max Iteration" counter in every looping agent workflow to prevent runaway costs. |
| **Pii Leakage** | Data breach | Ensure all AI requests are "Anonymized" before being sent to external model providers (OpenAI / Claude). |

---

## Success Criteria (AI Lab QA)
- [ ] System prompt clarity score matches "Omega-Tier" status.
- [ ] n8n workflows are modular and documented with error-traps.
- [ ] Agent latency is maintained within established velocity thresholds.
- [ ] Strict JSON schema validation is active for all inter-agent communication.