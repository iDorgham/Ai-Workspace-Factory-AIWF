# Hooks — WEB_OS_TITAN (Cursor / IDE)

Hooks are **not** bulk-shipped from `factory/library/` into every shard; configure them **per workspace** under **`.cursor/hooks/`** (see Cursor docs and the **create-hook** skill in your environment).

## Recommended hook ideas for this profile

| Hook moment | Purpose |
|-------------|---------|
| **After file edit** (agent stop) | Append high-signal notes to a local ledger (never secrets); optional continual-learning index refresh if you adopted that pipeline. |
| **Before `git push`** | Run quick lint or `pnpm run validate` when defined in the workspace. |
| **After terminal command** | Log command class for debugging long scraper or build jobs — redact env and tokens. |

## Governance

- Do **not** store API keys or tokens in hook JSON.  
- Keep hook scripts **short** and **fast**; avoid blocking the IDE for network calls.  
- If hooks call `git commit` or `git tag`, prefer wrapping the same rules as [scripts/git_workflow.md](../scripts/git_workflow.md) so behavior matches **`/git`** documentation.

## Library reference (optional skills with hook examples)

Some vendored skills under **`factory/library/skills/github_imports/`** ship example `hooks.json` + shell scripts (e.g. Playwright). Only copy patterns you need; keep **skip_prefixes** policy from **`AGENTS.md`** for pre-commit.

**Traceability:** `2026-05-04` — WEB_OS_TITAN hooks README.
