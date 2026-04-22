# Copilot Shortcuts

Use this when running workspace commands through Copilot CLI.

## Shortcut format

```bash
copilot --prompt "Run Sovereign workspace command: <router_command>. Follow .ai/commands.md output format."
```

Example:

```bash
copilot --prompt "Run Sovereign workspace command: /review. Follow .ai/commands.md output format."
```

## Notes

- `<router_command>` should match a command in `.ai/commands.md`.
- Prefer canonical IDs from `.ai/commands-cross-tool/canonical-command-catalog.json` for lookup.
