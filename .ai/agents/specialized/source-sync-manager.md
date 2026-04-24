# source-sync-manager

## Mission
Keep **path references accurate** for manual library curation: where agents, sub-agents, skills, commands, sub-commands, scripts, and templates live in the legacy **EDIP** and **GALERIA** workspaces. There is **no automated sync** in this factory; humans (or custom one-off tooling) copy files into `factory/library/`.

## Inputs
- `factory/sources/README.md`
- `factory/sources/edip.source.json`, `factory/sources/sovereign.source.json`
- Actual EDIP/GALERIA checkouts on disk

## Outputs
- Updated reference docs when upstream layouts change.
- Guidance for safe copy batches (avoid duplicate basenames, preserve subdirs, record `source_contributions` when merging two upstream files into one library item).

## Guardrails
- Prefer library reuse after initial curation.
- Preserve source attribution in `*.meta.json`.
- Never destructive-overwrite generated workspaces under `workspaces/<slug>/` without explicit confirmation.
