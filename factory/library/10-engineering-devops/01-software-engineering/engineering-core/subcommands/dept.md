---
cluster: engineering-core
category: subcommands
display_category: Subcommands
id: commands:engineering-core/subcommands/dept
version: 10.0.0
domains: [engineering-core]
sector_compliance: pending
---
# Dept

Subagent hierarchy — role assignment for phases. Company-style departments.

## Roles

PLANNING | ARCHITECTURE | SECURITY | BACKEND-Database | BACKEND-API | FRONTEND | MOBILE | QA | i18n | DEVOPS | EXPLORE

## When to use

- Assign primary role to each phase (from `docs/development/guidelines/SUBAGENT_HIERARCHY.md`).
- **Adopt agent:** Paste role prompt from `.antigravity/agents/roles/<role>.md` when starting phase.
- Use role prefix when invoking CLIs for consistent output.
- Match role to phase domain: schema → BACKEND-Database, UI → FRONTEND.
