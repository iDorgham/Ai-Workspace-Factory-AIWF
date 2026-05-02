---
type: command-registry
tier: OMEGA
version: 19.0.0
compliance: Law 151/2020
traceability: ISO-8601 Certified
---

# `/factory`

The `/factory` command suite governs the project and workspace lifecycle, from discovery to materialization and maintenance.

## 📋 Subcommands

| Subcommand | Purpose | Usage |
|------------|---------|-------|
| `start` | Begin new project discovery | `/factory start [client]` |
| `profile` | List/show composition templates | `/factory profile [list|show]` |
| `build` | Assemble project blueprint | `/factory build [client]` |
| `make` | Materialize workspace | `/factory make [client]` |
| `test` | Verify structure & compliance | `/factory test [client]` |
| `check` | Detect workspace drift | `/factory check [client]` |
| `sync` | Aggregate global state | `/factory sync [--scope]` |
| `assign` | Route task to swarm agent | `/factory assign [client] [task]` |
| `suggest` | AI-driven optimizations | `/factory suggest [client]` |
| `repair` | Self-heal core components | `/factory repair [--auto]` |
| `report` | Generate industrial reports | `/factory report [type]` |
| `help` | Interactive teaching engine | `/factory help [--category]` |
| `status` | Real-time health tracking | `/factory status` |

## 🛡️ Sovereign Protocol
- **Agent**: factory_orchestrator
- **Gate**: Omega Gate v2
- **Traceability**: Appends Reasoning Hash to .ai/logs/factory.jsonl
- **Compliance**: Egyptian Law 151/2020 Certified
