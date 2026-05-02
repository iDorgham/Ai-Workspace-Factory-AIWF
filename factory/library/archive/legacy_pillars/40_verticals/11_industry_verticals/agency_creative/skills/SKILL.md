---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# 🎨 Agency & Creative Operations (MENA)

## Purpose
Enforce professional operational and technical standards for Creative Agencies and Professional Service firms in the MENA market. This skill focuses on **Client-Retention Loops**, **The Physics of Creative Briefing**, and **Billable-Hour Optimization**.

---

## Technique 1 — The Physics of the Creative Brief

### The "Single-Source-of-Truth" Brief
- **Constraint Definition**: All creative briefs must include the "Hard Constraints" (Budget, Timeline, Brand Guidelines) and "Emotional Objectives" (Action intended, Tone of voice). Use the `skills:16-content-dominance/storytelling-logic` baseline for every brief.
- **VARA / Regulatory Sync**: For financial or crypto clients, the Creative Brief must be pre-vetted against the regional advertising regulations (e.g., UAE National Media Council or Egyptian SCMR) before the first pixel is moved.

---

## Technique 2 — Billable-Hour & Resource Optimization

- **The "Velocity" Tracking**: Implement real-time task tracking (e.g., via Monday.com, ClickUp, or a master Notion dashboard). Maintain a "Billable Utilization Rate" of > 75% for all creative staff while allowing 10% for "Research & R&D."
- **Asset Atomization**: Enforce a "Component-First" design approach. Every creative asset (Logo variation, Social banner, Ad copy) must be saved into a central, searchable DAM (Digital Asset Management) system for instant re-purposing across campaigns.

---

## Technique 3 — Client-Retention & Relationship Physics

### The "Strategic Partner" Loop
- **Proactive Reporting**: Automate "Weekly Performance HUDs" to clients that focus on **Business Impact** (Sales/Leads) rather than just "Vanity Metrics" (Likes/Follows). Use the `@MetricsAgent` to generate these reports.
- **Conflict Escalation**: Use the `agents:10-operations-qa/performance-ops/EscalationHandler` for any project delays. A delay communicated 48 hours in advance is "Professional Management"; a delay communicated 2 hours in advance is "Failure."

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **"Scope Creep" Drift** | Margin death | Any request outside the initial Statement of Work (SOW) must trigger an immediate "Refined Estimate" or "Change Order" before work proceeds. |
| **Subjective Feedback Loops** | Project stalling | Enforce "Stakeholder Consensus"—all feedback must be consolidated into a single document before the second version is produced. |
| **Lack of Cultural Nuance** | Brand rejection | For MENA campaigns, always verify that the "Creative Concept" respects regional sensitivities (Religious holidays, Dress codes, Local humor). |

---

## Success Criteria (Agency QA)
- [ ] Creative Brief completeness score is > 90% for all active projects.
- [ ] Billable utilization rate is maintained > 75% across the team.
- [ ] Client sentiment (NPS) is tracked and maintained > 8.0.
- [ ] Asset DAM is synchronized and searchable by all departments.