---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# 🦴 Caveman Automation Physics


## Purpose
Enforce standards for "Rugged, Low-Complexity" automation. This skill focuses on the "Simple is Better" paradigm—using the absolute minimum number of moving parts to achieve 100% reliability. It favors shell scripts, basic webhooks, and direct API calls over complex middleware.

---

## Technique 1 — The "Single-Shell" Pipeline
- **Rule**: If a task can be done with a single `zsh` or `python` script, avoid using a SaaS orchestrator (Zapier/Make).
- **Protocol**: 
    1. Define the input trigger (e.g., File change, Webhook, Cron).
    2. Write an idempotent script that handles its own retry logic.
    3. Use standard Linux/Mac tools (curl, sed, jq) for data processing.
    4. Log failures to a local append-only file and trigger a simple notification (e.g., Discord/Slack webhook).

---

## Technique 2 — Stateless Webhook Catchers
- **Rule**: Use lightweight "Catchers" to receive data, store it immediately in a raw format, and process it asynchronously.
- **Protocol**: 
    1. Deploy a single-purpose endpoint (e.g., Vercel Function).
    2. Store the raw payload in a "Queue" database (e.g., Upstash Redis).
    3. Trigger a background job to parse and route the data.
    4. Benefit: Zero-loss data ingestion even if the primary app is down.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Logic Over-Engineering** | Maintenance nightmare | Use the "Rule of 3": If you haven't done it manually 3 times, don't automate it with complex logic. |
| **Silent Job Death** | Missing data | Always monitor your Cron jobs/Workflows with a "Dead Man's Switch" (e.g., Healthchecks.io). |
| **Non-Idempotent Scripts** | Duplicate side-effects | Ensure your scripts can be run 100 times without creating duplicate entries or broken state. |

---

## Success Criteria (Automation QA)
- [ ] 0% reliance on expensive "Monthly Active Operation" SaaS for basic scripts.
- [ ] 100% visibility into job success/failure via simplified logging.
- [ ] Scripts are portable and run on any POSIX-compliant environment.
- [ ] Average execution time for critical automations is < 1 second.
