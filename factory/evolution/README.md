# Factory evolution (self-update loop)

This folder captures **signals from generated workspaces** so the factory library can improve over time without regenerating components from scratch.

## How it works

1. Each generated workspace under `workspaces/<slug>/` may emit lightweight signal files (JSON or Markdown) describing:
   - missing components (agent, skill, command) that operators had to add manually
   - validation failures and fixes applied
   - recurring tasks that suggest a new reusable skill or script

2. Run `python3 factory/scripts/collect_evolution_signals.py` to aggregate signals into:
   - `factory/evolution/signals/aggregate-<date>.json`
   - append suggestions to `factory/evolution/BACKLOG.md`

3. Human curators (see `library-curator` agent) triage the backlog, promote items into `factory/library/`, update profiles, and run `./factory/scripts/refresh-library.sh` after library edits.

## Governance

- Signals are **non-authoritative** until reviewed.
- Library promotion requires explicit curator approval and version bump in metadata.
- Never auto-overwrite production library items without review (configurable later).
