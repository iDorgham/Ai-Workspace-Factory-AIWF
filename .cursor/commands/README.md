# Cursor slash-command docs (mirror)

**Canonical tree:** `.ai/commands/` — edit there first.

**Sync:** `bash factory/scripts/core/sync_ide_triple_layer.sh` copies `.ai/commands/` → this folder (and `.antigravity/commands/`), then deletes legacy duplicate filenames.

## Merged docs (no separate files)

- **`commands.md`** — Command router **and** multi-tool rankings (**MULTI-TOOL RANKINGS** section). Do not add `commands-multi-tool.md` or `commands_multi_tool.md`.
- **`guide.md`** — `/guide` registry **and** Humanization Engine (Antigravity). Do not add `guide_humanize.md`.

## Routing implementation

Executable routing lives in `.ai/registry/routing/command_routing.json` (see header inside `commands.md`). These markdown files are human-readable mirrors for slash prompts and agents.

## Command IDs (content router families)

- `brand`, `research`, `scrape`, `sync`, `voice`, `create`, `compare`, `intel`, `polish`, `optimize`, `review`, `approve`, `revise`, `export`, `archive`, `memory`, `budget`

## Naming

- Use `<group>-<target>-<scope>-<action>` for multi-part commands.
- Use `<group>-<action>` for compact commands.
- Keep families aligned by prefix (`scrape-*`, `create-*`, `intel-*`, `memory-*`, `brand-*`).
