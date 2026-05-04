# Design pack onboarding — `design.md` installs

All curated packs live under **`factory/library/templates/design/<provider>/design.md`**, indexed in **`factory/library/templates/design/catalog.json`**.

## A. Discover packs

**Slash (when router is synced):**

```text
/design list
```

**Terminal (lists every `design.md`):**

```bash
bash factory/library/profiles/personal/WEB_OS_TITAN/scripts/list_design_packs.sh
```

## B. Select a pack for the workspace

1. Open **`factory/library/templates/design/README.md`** for human-oriented catalog notes.  
2. Pick a provider folder (e.g. `vercel`, `shadcn`, `framer`, `webflow`, `dashboard`, `editorial`, `portfolio`-style packs).  
3. Use **`/design use [pack]`** or **`/design install [pack]`** per **`factory/library/commands/guide.md`** / **`commands.md`** routing (install copies into the project’s template scope).

## C. Suggested packs by product shape

| Product shape | Example packs (paths under `templates/design/`) |
|---------------|--------------------------------------------------|
| **Marketing + blog** | `editorial`, `semrush`, `notion` |
| **Portfolio / creative** | `framer`, `webflow`, `figma`, `premium` |
| **SaaS dashboard + CMS** | `dashboard`, `shadcn`, `vercel`, `linear-app` |
| **Media / motion** | `runwayml`, `remotion` (if present in catalog) |

Always verify the folder exists on disk before documenting in client-facing READMEs.

## D. After install

- Point **`/guide`** or design critique skills at the chosen **`design.md`** for consistency reviews.  
- Re-run **`bash factory/scripts/core/sync_ide_triple_layer.sh`** in AIWF when you change canonical commands, so IDE slash docs stay aligned.

**Traceability:** `2026-05-04` — WEB_OS_TITAN design onboarding.
