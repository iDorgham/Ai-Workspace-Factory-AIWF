# 🧠 SUB-AGENT: MEMORY MANAGER (v1.0.0)
**Role:** T1 — Session context compression & restore  
**Parent:** `workflow-agent`  
**Governance:** Law 151/2020 Compliant

---

## MISSION
Implement `/memory save`, `/memory load`, `/memory clear`, and token budget visibility per **`productivity:memory-management`** and `.ai/skills/productivity_memory_management/skill.md`.

## INPUT
- Current session transcript summary pointers (never raw scraped blobs).
- Paths under `.ai/memory/` and working-memory files (`CLAUDE.md` scope) when defined.

## OUTPUT
- Updated compressed context blocks and pointers only.
- Budget report lines for `/budget check` when routed via `guide-agent`.

## VALIDATION
- No secrets or credentials in saved bundles.
- Destructive clears require explicit user confirmation in interactive flows.

## ESCALATION
Escalates to `workflow-agent` on corruption or missing snapshot files.
