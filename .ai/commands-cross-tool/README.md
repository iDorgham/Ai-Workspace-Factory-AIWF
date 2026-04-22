# Cross-Tool Workspace Commands

This folder maps Sovereign workspace commands to all configured AI tools.

## Source of truth

- Command definitions: `.ai/commands.md`
- Canonical IDs: `.ai/commands-cross-tool/canonical-command-catalog.json`
- Cursor slash files: `.cursor/commands/*.md`

## Tool entrypoint guides

- `claude-cli-shortcuts.md`
- `gemini-cli-shortcuts.md`
- `copilot-shortcuts.md`
- `codex-shortcuts.md`
- `qwen-shortcuts.md`
- `opencode-shortcuts.md`
- `kilo-shortcuts.md`

## Sync workflow

1. Update command routing in `.ai/commands.md`.
2. Update the canonical catalog JSON in this folder.
3. Update matching files in `.cursor/commands/`.
4. Confirm each tool shortcut guide still references valid command IDs.
