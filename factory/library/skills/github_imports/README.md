# GitHub-imported skills

Vendored skill bundles from public repositories listed in `docs/files.md`, produced by:

```bash
python3 factory/scripts/core/import_github_skills_library.py --clone-root /path/to/shallow/clones
```

## Sources and merge priority

When two skills share the same merge key (usually the folder name next to `SKILL.md`), this order wins:

1. **anthropics_official** — `anthropics/skills`
2. **anthropics_claude_code** — `anthropics/claude-code` plugins
3. **obra_superpowers** — `obra/superpowers`
4. **k_dense_scientific** — `K-Dense-AI/claude-scientific-skills`
5. **alirezarezvani** — `alirezarezvani/claude-skills` (`.gemini/` excluded)
6. **wshobson_agents** — `wshobson/agents` plugin skills

Ties on priority use the larger `SKILL.md` file.

## Provenance

Each folder includes `_AIWF_IMPORT.json` with the winning source and original paths. Full import log: `_IMPORT_MANIFEST.json` (includes skipped duplicates).

## Re-import

Shallow-clone the repos under one directory (see script docstring), then re-run the command above; it replaces each destination folder.
