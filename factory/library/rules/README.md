# Rules (artifact-first)

This directory is the **canonical home** for reusable governance and editor-rule bundles that sync into workspaces.

- **Outbound mirror (AIWF repo):** `.ai/rules/` is copied to **`rules/workspace_imports/ai/rules/`** by `python3 factory/scripts/core/industrial_mirror_sync.py` (same run as other `.ai` → `factory/library` mirrors). Keep that subtree aligned with `.ai/rules` after edits.
- The corpus may be sparse until rules are promoted from workspace imports.
- Materialized workspaces should ship a **local** `.ai/rules/README.md` that points here and documents any workspace-only overrides.

**Traceability:** `2026-04-30` — template library sync baseline; `2026-05-02` — documented `.ai/rules` mirror path.
