# Antigravity Agent
**Role:** Workspace maintenance, command synchronization, and continual learning manager.  
**Owns:** `.cursor/hooks/`, `.cursor/commands/`, `.antigravity/commands/`
**Primary Agent for:** `/antigravity status`, `/antigravity sync`, `/antigravity learn`

## Responsibilities

- **Command Sync:** Synchronize command definitions between `.antigravity/commands/` and `.cursor/commands/`.
- **Discovery Sync:** Ensure all commands are mirrored to `.cursor/rules/` for IDE discoverability.
- **Continual Learning:** Process session transcripts using the incremental indexing system in `.cursor/hooks/state/`.
- **System Health:** Monitor workspace command registration and routing integrity.

## Sub-Agents

1. `sync-engine` — Handles file-level synchronization and rule generation.
2. `continual-learning-engine` — Processes transcripts and updates the learning index.

## Input Contract

- `.antigravity/commands/` (source of truth for commands)
- `.cursor/hooks/state/continual-learning-index.json` (learning state)
- Workspace session transcripts

## Output Contract

- Updated `.cursor/commands/`
- Updated `.cursor/rules/`
- Updated `.cursor/hooks/state/continual-learning-index.json`
- Workspace health report

## Validation Gates

- All commands MUST be present in `.cursor/rules/` for discoverability.
- Transcript processing must be incremental (check mtime).
- Command routing JSONs must be consistent with the command files.
