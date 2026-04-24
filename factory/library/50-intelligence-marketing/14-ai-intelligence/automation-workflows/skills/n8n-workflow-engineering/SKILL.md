---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# ⚡ n8n Workflow Engineering (Omega-tier)


## Purpose
Enforce professional standards for designing and maintaining complex automation workflows in n8n. This skill focuses on **Self-Healing Logic**, **Recursive AI Nodes**, and **High-Volume Data Processing.**

---

## Technique 1 — The "Self-Healing" Workflow

### Error Handling & Retries
- **Rule**: No production node should exist without an **Error Trigger** path.
- **Protocol**: Route all node failures to a `GlobalError` handler that:
    1. Logs the failing `NodeName` and `InputData`.
    2. Sends a notification to `@AIOps` or a Dev-slack channel.
    3. Attempts a "Cool-down" retry (Exponential backoff).

### Flow Control
- **Wait Nodes**: Always use `Wait` nodes before high-concurrency API calls to avoid 429 Rate Limits.
- **IF Nodes**: Prioritize specific binary logic over complex JS expressions to maintain visual readability.

---

## Technique 2 — AI-Integrated Nodes

### The AI-Router Pattern
- **Logic**: Use an LLM node to categorize input data *before* routing to specialized sub-workflows.
- **Prompting**: Use the "Bilingual Context" rules to ensure the AI-node understands regional data (e.g., Arabic address formats).

---

## Technique 3 — Resource Optimization

| Strategy | Action | Result |
| :--- | :--- | :--- |
| **Node Pruning** | Combine multiple `Edit Binary` nodes into a single JS node. | 30% reduction in execution memory. |
| **Batching** | Process large datasets in chunks of 50-100. | Prevents n8n "Out of Memory" crashes. |
| **Data Stripping** | Filter unneeded fields early in the flow. | Reduces database/memory load. |

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Direct Webhook Exposure** | Security risk / DDOS | Always route webhooks through a `Validation Node` (API Key check). |
| **Long-Running Loops** | Token/Run cost bloat | Set a "Hard-Kill" timer on recursive AI tasks. |
| **Hardcoded Credentials** | Security leak | Use n8n **Credentials** system; never use plain-text keys in nodes. |

---

## Success Criteria (n8n QA)
- [ ] Workflow passes "Error-Stress" test (Graceful failure on 404/500).
- [ ] Execution time is optimized (Avg < 5s for non-AI tasks).
- [ ] Data lineage is clear (Input -> Transform -> Output).
- [ ] AI prompts in nodes utilize XML-tagging as per @ClaudeMastery.
