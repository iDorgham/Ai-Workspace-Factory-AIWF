# Gemini CLI Shortcuts

Use this when running workspace commands through Gemini.

## Shortcut format

Gemini adapter accepts structured JSON. Use:

```bash
echo '{"command":"<router_command>","context":{"source":"sovereign-workspace"}}' | sovereign-gemini --json-output
```

Example:

```bash
echo '{"command":"/research competitors","context":{"source":"sovereign-workspace"}}' | sovereign-gemini --json-output
```

## Notes

- Replace `<router_command>` with a command from `.ai/commands.md`.
- Keep output aligned with the command output format in `.ai/commands.md`.
