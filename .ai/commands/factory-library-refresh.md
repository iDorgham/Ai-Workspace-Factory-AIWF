# `/factory library refresh`

## Syntax
`/factory library refresh`

## Required Inputs
- None.

## Outputs
- Regenerates `factory/library-index/*.json` from `*.meta.json` files next to library components.
- Runs `factory/scripts/validate-library.sh`.

## Failure Conditions
- Malformed `*.meta.json`, missing required metadata fields.

## Beginner Example
`/factory library refresh`

## Purpose
Use **after you manually copy** agents, sub-agents, skills, commands, sub-commands, scripts, and templates from the legacy **GALERIA** and **EDIP** workspaces into `factory/library/`. There is **no automated sync**; this command only refreshes indexes and validates metadata.

## Shell equivalent
```bash
./factory/scripts/refresh-library.sh
```
