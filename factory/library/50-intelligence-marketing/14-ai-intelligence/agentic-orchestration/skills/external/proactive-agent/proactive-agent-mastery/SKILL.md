---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# ⚡ Proactive Agent Logic

## Purpose
Enforce standards for autonomous intelligence that anticipates user needs and system risks. This skill focuses on the "Forward-Looking" mindset, where agents identify potential conflicts (e.g., dependency mismatches, context limits) before they occur and suggest preemptive remediations.

---

## Technique 1 — Preventative Gap Discovery
- **Rule**: Before executing a command, scan the environment for "Missing Pre-requisites."
- **Protocol**: 
    1. Analyze the command intent (e.g., "Install React").
    2. Check environment state (e.g., "Is Node installed?").
    3. If a gap is found, inform the user and suggest the installation command **before** attempting the primary task.

---

## Technique 2 — Narrative Continuity Management
- **Rule**: Proactively maintain conversation coherence by summarizing the current state every 10 turns.
- **Protocol**: 
    1. Monitor context window saturation.
    2. Before reaching 80% saturation, generate a high-density "State Summary."
    3. Inject this summary into the permanent memory/artifact to ensure long-term continuity.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Intrusive Proactivity** | User annoyance | Only suggest preemptive actions that are > 80% likely to be required. |
| **Over-Summarization** | Loss of detail | Ensure summaries capture "Reasoning" and "Current Blockers," not just "Tasks." |
| **Assuming Consent** | Destruction risks | Proactive agents MUST request explicit approval before taking any write/delete actions. |

---

## Success Criteria (Proactive QA)
- [ ] 100% of "Missing Dependency" errors are identified before command execution.
- [ ] User feels "anticipated" rather than "interrupted."
- [ ] Context overflows are minimized through proactive state-management.
- [ ] Risk scores are calculated for every planned autonomous move.