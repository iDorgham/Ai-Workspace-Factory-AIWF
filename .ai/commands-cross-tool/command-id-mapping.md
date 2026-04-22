# Command ID Mapping

This maps canonical command IDs to invocation patterns across tools.

## Invocation patterns

- Cursor: parent entrypoints for grouped families:
  - `/scrape` -> menu routes to all scrape router commands
  - `/create` -> menu routes to all create router commands
  - `/intel` -> menu routes to all intel router commands
  - `/memory` -> menu routes to all memory router commands
  - `/brand` -> menu routes to `/brand` and `/brand workshop`
  - `/voice` -> menu routes to `/extract brand voice from [source]` and `/refine brand voice`
  - all other commands remain one file per command ID
- Claude CLI: `Run Sovereign workspace command: <router_command>`
- Gemini CLI: JSON `{"command":"<router_command>"}` piped to `sovereign-gemini --json-output`
- Copilot CLI: `copilot --prompt "Run Sovereign workspace command: <router_command> ..."`
- Codex CLI: `codex --prompt "Run Sovereign workspace command: <router_command> ..."`
- Qwen CLI: `qwen --prompt "Run Sovereign workspace command: <router_command> ..."`
- OpenCode CLI: `opencode --prompt "Run Sovereign workspace command: <router_command> ..."`
- Kilo CLI: `kilo --prompt "Run Sovereign workspace command: <router_command> ..."`

## Examples

| ID | Router command |
|---|---|
| `brand` | `/brand` |
| `research` | `/research competitors` |
| `scrape` | menu -> `/scrape ...` variants |
| `voice` | menu -> `/extract brand voice from [source]` and `/refine brand voice` |
| `create` | menu -> `/create ...` variants |
| `compare` | `/compare sovereign vs competitor [name]` |
| `review` | `/review` |
| `approve` | `/approve` |
| `export` | `/export` |

For complete command set, use `.ai/commands-cross-tool/canonical-command-catalog.json`.
