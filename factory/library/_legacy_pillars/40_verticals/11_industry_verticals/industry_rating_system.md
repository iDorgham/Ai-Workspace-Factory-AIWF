---
type: Generic
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---


# 📊 Industry Maturity Rating System

To ensure all 20+ Industry Verticals within the Sovereign Factory are capable of "Omega-Tier" automation, we employ a 3-tier rating system. This dictates the priority for scaling Skills, Agents, Commands, and Templates.

## ⭐ Tier 1: Legacy (The Scaffold)
**Definition**: The industry exists in the file structure but lacks high-density AI instruction sets.
- **Characteristics**: Empty `skills/` and `agents/` directories, or relying on generic ChatGPT prompts instead of professional operational logic.
- **Action Required**: Immediate deployment of `14-ai-intelligence` (Automations) and `16-content-dominance` (Specialized Tone).

## ⭐⭐ Tier 2: Operational (The Baseline)
**Definition**: The industry has specialized skills and baseline templates but cannot execute end-to-end workflows autonomously.
- **Characteristics**: Contains Markdown strategy playbooks and at least one Sentinel Agent, but lacks executable Subcommands or Code Boilerplates.
- **Action Required**: Seed the `templates/` bucket with high-fidelity files (Figma, HTML, Notion) and build CLI routing commands.

## ⭐⭐⭐ Tier 3: Omega (The Autonomous Hub)
**Definition**: The absolute standard of the Sovereign Factory. The vertical operates as a fully independent machine.
- **Characteristics**: 
  - [x] Has a dedicated Sentinel Agent (e.g., `@MediaMediaBuyer`).
  - [x] Contains specialized, dense `skills/` with anti-patterns logic.
  - [x] Has executable CLI commands in the `commands/` directory.
  - [x] Possesses ready-to-deploy assets in the `templates/` directory.
- **Action Required**: Routine QA and indexing via `audit_library.py`.

---

## 🛠️ The "Enhance Again" Protocol
If an industry is stuck at ⭐ or ⭐⭐, apply the **Triple-A Upgrade**:
1. **Analytics**: Inject data/research protocols from `05-data-analytics`.
2. **Authority**: Inject emotional storytelling logic from `16-content-dominance`.
3. **Action**: Create automated `n8n` or CLI commands under `14-ai-intelligence`.
