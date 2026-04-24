# Skill: source-ingestion-and-normalization

## Purpose
Support `source-ingestion-and-normalization` within factory generation and governance workflows.

## Checklist
1. Read `factory/sources/README.md` and confirm upstream paths for EDIP and GALERIA.
2. Copy only approved files into `factory/library/<type>/…` and add or update `*.meta.json`.
3. Run `./factory/scripts/refresh-library.sh` so indexes match the tree.
4. Read relevant profile, intake, and library index files before composing.
5. Prefer reuse from `factory/library/*` during composition (do not regenerate from scratch).
6. Record decisions in manifest/report outputs; emit actionable failure reasons when checks fail.
