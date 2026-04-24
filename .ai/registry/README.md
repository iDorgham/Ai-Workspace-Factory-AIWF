# Registry Layer Guide

This directory is the canonical source of runtime-discoverable orchestration definitions.

## Canonical Registries
- `agents.registry.json`: one entry per agent definition file.
- `subagents.registry.json`: one entry per sub-agent contract file.
- `skills.registry.json`: one entry per .ai/workspace/[external-path] skill handle.
- `command-bindings.registry.json`: command IDs mapped to agent + sub-agent pipelines.

## Schema Contracts
- `schemas/agent.schema.json`
- `schemas/subagent.schema.json`
- `schemas/skill.schema.json`
- `schemas/command-binding.schema.json`

## Required Invariants
- IDs are globally stable and immutable.
- Registry paths must exist.
- No duplicate IDs per registry.
- Every command binding agent/sub-agent/skill ref must resolve.
- Legacy compatibility maps must remain 1:1 with migrated IDs.

## Compatibility
Legacy mirrors are intentionally retained:
- `.ai/agents.md`
- `.ai/sub-agent-contracts.json`
- `.ai/skill_integration.md`

Loaders should prefer registry files first, then fallback via `.ai/compat/*.legacy-map.json`.
