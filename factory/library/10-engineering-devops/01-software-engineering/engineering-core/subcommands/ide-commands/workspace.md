---
cluster: engineering-core
category: subcommands
display_category: Subcommands
id: commands:engineering-core/subcommands/workspace
version: 10.0.0
domains: [engineering-core]
sector_compliance: pending
---
# Workspace Command Family

This command family handles workspace-specific operations.

## Available Actions

- `/workspace status` -> Show current agent status and workspace health.
- `/workspace sync` -> Synchronize commands between IDE command directories.
- `/workspace learn` -> Process new transcripts for continual learning.

## Usage Rule

When a user invokes `/workspace`, show a menu of options and ask for clarification if needed.
Always maintain the workspace command output format as defined in `.ai/cli-layer/`.
