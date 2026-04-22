# Codex Shortcuts

Use this when running workspace commands through Codex CLI.

## Shortcut format

```bash
codex --prompt "Run Sovereign workspace command: <router_command>. Follow .ai/commands.md output format." --max-tokens 2048 --output json
```

Example:

```bash
codex --prompt "Run Sovereign workspace command: /budget check. Follow .ai/commands.md output format." --max-tokens 2048 --output json
```

## Notes

- Replace `<router_command>` with a command from `.ai/commands.md`.
