# Canonical library audit — agents, subagents, skills (2026-05-03)

## Summary

| Area | Before | After | Notes |
|------|--------|-------|--------|
| `skills.registry.json` | ~297 rows pointing at **removed** pillar trees (`factory/library/NN-*`, `SKILL.md`) | **782** rows, all `factory/library/skills/**/skill.md` on disk | Rebuilt by `factory/scripts/analytics/rebuild_canonical_registries.py` |
| `agents.registry.json` | Legacy pillar `AGENT.md` paths | **34** rows → `.ai/agents/**/*.md` (+ core JSON) with stable `id` | Same script |
| `subagents.registry.json` | `.json` paths that **did not exist** | `.ai/subagents/*.md` underscore filenames | Manual fix + added missing pipeline actors |
| `command_bindings.registry.json` | Broken refs (`marketing-brand-strategy`, `voice-validator`, …) | Aligned to real skill + subagent ids | Edits in-repo |
| `validate_registry.py` | Wrong `ROOT` + wrong bindings filename | Finds repo via `AGENTS.md`; loads `command_bindings.registry.json` | `.ai` + factory mirror |

## New / restored artifacts

- **Subagent docs:** `memory_manager.md`, `continual_learning_engine.md` (pipeline + `/antigravity` support).
- **Enhanced:** `blueprint_architect.md`, `workspace_composer.md` (concrete missions, I/O, guardrails).

## Validation

```bash
python3 .ai/compat/migrations/validate_registry.py
# expect: registry_validation_ok agents=34 subagents=30 skills=782 bindings=30
```

## Maintenance

- After bulk skill add/remove under `factory/library/skills/`, re-run:

```bash
python3 factory/scripts/analytics/rebuild_canonical_registries.py
cp .ai/registry/skills.registry.json .ai/registry/agents.registry.json factory/library/registry/
```

Then `python3 factory/scripts/core/industrial_mirror_sync.py` for outbound mirrors.

## Dead files

- Scanned `.ai/skills`, `.ai/agents`, `.ai/subagents` for **0-byte** files: **none** found.
- Legacy pillar skill files were already absent; registry was the stale surface (now corrected).
