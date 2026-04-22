# Kilo Shortcuts

Use this when running workspace commands through Kilo CLI.

## Shortcut format

```bash
kilo --prompt "Run Sovereign workspace command: <router_command>. Follow .ai/commands.md output format." --api-key "$KILO_API_KEY" --output json
```

Example:

```bash
kilo --prompt "Run Sovereign workspace command: /intel market snapshot. Follow .ai/commands.md output format." --api-key "$KILO_API_KEY" --output json
```

## Status

Kilo requires `KILO_API_KEY` in this workspace (`.ai/tool-registry.json`).
