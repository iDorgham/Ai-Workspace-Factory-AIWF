---
type: Command
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---


# /init — Workspace Initialization

## Syntax
```
/init [--type web|mobile|backend|fullstack|brand|ai-native|gov-tech|multi-app]
      [--db postgres|mysql|sqlite|none]
      [--mode founder|pro|hybrid]
      [--methodology sovereign-default|contract|contract-first|sdd|tdd|design-first|agile-lean|phase-gated]
      [--brand]
      [--monorepo]
      [--strategy founder|hybrid|enterprise]
      [--prd-existing] [--prd-file <path>]
      [--prd-idea]
      [--no-prd]
```

**PRD flags (optional, mutually exclusive paths):**

| Flag | Meaning |
|------|---------|
| `--prd-existing` | User supplies a PRD; AI runs a **refinement conversation** until it matches vision, scope, and priorities. |
| `--prd-file <path>` | Seed PRD from an existing file (implies `--prd-existing`). |
| `--prd-idea` | User starts from an **idea only**; AI interviews and expands, then writes the PRD. |
| `--no-prd` | Skip PRD prompts entirely and go straight to the workspace interview. |

`--prd-existing` and `--prd-idea` must not be combined; if both appear, `@Guide` asks which path to keep. `--no-prd` wins over any other PRD flag.

**`--methodology` (optional):** Sets `development_methodology.primary` in `.ai/context/project-type.md` without asking during Part B. If omitted on a bare `/init`, `@Guide` / `@Founder` ask at **B3a**. Values: **`sovereign-default`** (SDD — Sovereign template default) · **`sdd`** (same behavior as **`sovereign-default`**) · **`contract`** / **`contract-first`** (aliases — **CFG**, contract-emphasis) · `tdd` · `design-first` · `agile-lean` · `phase-gated`.

If the user invokes **`/init` with no flags**, use **Bare `/init`** below — do not jump straight to scaffolding.

## Primary Agents
`@Guide` + `@Architect` + `@Founder` (Founder mode and PRD paths)

## What It Does
Scaffolds a new Sovereign workspace with full project configuration. The most important command — everything starts here.

On completion (**Step 6**), it creates the **first SDD phase/spec** (`01-foundation/01-workspace-init`) from **`.ai/templates/sdd-spec/`**, a phase **`manifest.md`**, and sprint/roadmap stubs so planning stays phase/spec-first.

Optionally, `/init` can produce or refine a project-level PRD before scaffolding so vision, features, and stack choices stay aligned from the start.

---

## Bare `/init` — no flags (default first-time path)

**When:** The user types `/init` with no arguments.

**Goal:** (1) Explain what `/init` is and how to use it. (2) Walk through ordered discovery questions so the assistant understands what the user wants to build before touching the repo.

**Primary agents:** `@Guide` (orientation + pacing) · `@Founder` (discovery questions) · `@Architect` (when stack tradeoffs arise).

### Part A — Explain how to use `/init`

`@Guide` delivers a compact briefing (not a wall of text):

1. **What `/init` does:** Sets up the Sovereign workspace — project type, optional PRD, scaffold, CI — and seeds the **first SDD phase/spec** under `.ai/plans/active/features/` so `/plan` and `/build` start from a governed spec tree.
2. **Flags can be added anytime:** A follow-up message with flags will re-enter `/init` at the right point.
3. **Show the syntax block** once, summarized in bullets:
   - `--type` — web, mobile, backend, fullstack, brand, ai-native, gov-tech, multi-app
   - `--db` — postgres, mysql, sqlite, none
   - `--mode` — founder (plain language), pro (technical), hybrid
   - `--methodology` — how you want to work: sovereign-default (SDD default), sdd (same as sovereign-default), contract / contract-first (CFG), tdd, design-first, agile-lean, phase-gated
   - `--monorepo` — enable monorepo layout (pnpm workspaces + Turborepo)
   - `--brand` — generate design tokens before apps
   - `--prd-existing` / `--prd-file` — refine an existing PRD
   - `--prd-idea` — conversation → new PRD
   - `--no-prd` — skip PRD steps
4. Full reference: `.ai/commands/init.md` (this file).

If the user **already used flags** on this turn, **skip Part A** and continue with one line: *"Flags detected — continuing; see `.ai/commands/init.md` for the full reference."*

### Part B — Step-by-step: what do you want to build?

`@Founder` leads **one main question per message** (unless the user asks to batch). Track all answers — they become the source of truth for Step 1 and `project-type.md`.

| Step | Topic | Question direction (adapt wording to user) |
|------|--------|--------------------------------------------|
| **B1** | Product in one breath | What are you building, in one or two sentences? |
| **B2** | Audience | Who is it for (primary users or customers)? |
| **B3** | Problem & outcome | What problem does it solve, and what should be true when it works? |
| **B3a** | Development methodology | **Skip if `--methodology` was passed.** Otherwise: *Which way of working should we optimize for?* Present the **Development methodology options** (Founder mode: plain language; Pro mode: use labels). Allow "Sovereign default / recommend for me" → record `sovereign-default`. |
| **B4** | Shape of the product | Website, mobile app, API only, or a combination? |
| **B5** | Must-haves vs later | What must the first version do? What can wait? |
| **B6** | PRD path | Do you have a PRD to refine, want to shape an idea into one, or skip a written PRD for now? |
| **B7** | Working style | Prefer **Founder** (plain language, guided) or **Pro** (technical, faster assumptions)? |
| **B8** | Confirm | Read back a short summary — vision, audience, methodology, shape, v1 scope, PRD choice, mode — and ask the user to confirm or correct. |

**Rule:** No workspace file generation until the user confirms the **B8** summary (or explicitly says to proceed).

**Learner memory:** During Part B and PRD steps, `@Founder` / `@Guide` update `.ai/memory/user-learning-profile.md` (signal log, inferred expertise, durable facts). After the user confirms B8, invite `@Tutor` to refresh the **Suggested study queue**.

After **B8** confirmation:
- Map **B3a** (or `--methodology`) → `development_methodology.primary` in `.ai/context/project-type.md`.
- Map **B4–B5** toward `--type`, `--db`, and `project-type.md`.
- Apply **B6** → PRD path (Step 0) or skip.
- Apply **B7** → `--mode` for the rest of `/init`.
- Continue to **Step 0** (if PRD path chosen) or **Step 1** directly.

### Development methodology options (present at B3a)

**Recommended default:** **`sovereign-default`** = **SDD** (Spec-Driven Development) — phase/spec plans, structured natural-language specs, auto-generated and locked Zod, SOS **`prompt.md`**, same quality gates. **`sdd`** is an **explicit slug with identical behavior**. **`contract`** / **`contract-first`** → **CFG** (contract-emphasis; **different** slug — stresses manual **`/contract`** checkpoints; same gates). Exceptions: `development_methodology.notes`. Full reference: `docs/workspace/reference/development-methodologies.md`.

**Short codes** (for summaries and Pro mode): **Sovereign** (`sovereign-default`), **SDD** (`sdd`), **CFG** (`contract` / `contract-first`), **TDD**, **DFD**, **ALID**, **PGD**.

| Code | Value (`primary`) | Technical name | Description |
|------|-------------------|----------------|-------------|
| **Sovereign** | `sovereign-default` | Spec-Driven Development (Sovereign default) | Same as **`sdd`**: confirmed spec → auto Zod + lock → SOS → `/build`; **phase/spec** layout. Written when the user picks “Sovereign default / recommend for me” or when **`primary` is unset** after init. |
| **SDD** | `sdd` | Specification-Driven Development (explicit) | **Identical behavior to `sovereign-default`**. Use for dashboards or teams that want the slug to read `sdd`. |
| **CFG** | `contract` (aliases: `contract-first`) | Contract-emphasis governance | Explicit **`/contract`** workflow before heavy implementation; same gate order and phase/spec layout; use when the team wants **more manual** contract ceremony than the SDD default. |
| **TDD** | `tdd` | Test-Driven Development | Tests lead implementation where practical (red → green → refactor); contracts still define API and data boundaries. |
| **DFD** | `design-first` | Design-first development | Visual and UX foundations first: brand, design tokens, shared UI components — then application features. |
| **ALID** | `agile-lean` | Agile lean incremental delivery | Small vertical increments, frequent delivery, light process per increment; contracts still enforce API and data boundaries. |
| **PGD** | `phase-gated` | Phase-gated (staged) delivery | Work moves through explicit phases (discovery → specification → build → release) with documented outputs and approval before each next phase. |

---

## PRD artifact (canonical path)

When any PRD path runs, the single source of truth for the living document is:

```
.ai/plans/active/project-prd.md
```

- Include a version line or short changelog at the bottom when revised.
- `@Architect` and `/plan` treat this file as the primary input for feature plans and the roadmap.
- **Human-facing copy:** Offer to mirror into `docs/product/prd/` (e.g. `PRD.md`) so the team has a visible path in Git. See `docs/product/README.md`.

## Human product docs (`docs/product/`)

| Path | Use |
|------|-----|
| `docs/product/prd/` | User-authored PRDs (any filename; suggested default for `--prd-file`: `docs/product/prd/PRD.md`). |
| `docs/product/idea/` | Brainstorming, discovery notes, rough ideas before a formal PRD. |

Any other new markdown under `docs/`: follow `docs/DOCUMENTATION_MAP.md`. Do not drop loose files into the `docs/` root.

## Root `README.md` (product-facing only)

- The root `README.md` describes **the user's product** (name, audience, vision, links to `docs/product/`). It must not restate Sovereign workspace marketing, agent rosters, slash-command lists, or development workflow.
- When `/init` finishes (or when B8 is confirmed if the user stops early), **rewrite** root `README.md` from the confirmed product summary. Contributors may link to `docs/workspace/README.md` only if the user asks for Sovereign documentation in their team readme.
- The full Sovereign workspace readme always lives at `docs/workspace/README.md` — never delete it; do not merge it into the root readme.

---

## Execution Flow

**Order:** Bare `/init` → Part A → Part B → **Step 0** (if PRD path) → **Steps 1–6**.
Flags-only invocation → skip Part A/B → **Step 0** (if PRD flags) → **Steps 1–6**.

### Step 0: PRD path (run when user chose a PRD path in B6 or passed PRD flags)

Skip entirely if `--no-prd` or user chose *skip for now* at B6.

**Conversation rules (both paths):**
- One clear question at a time in Founder mode; batch only if the user asks for speed.
- After each major revision, show a **short delta** (what changed and why).
- No scaffolding or contract work until the PRD gate is passed (or user overrides with "skip PRD and continue").

#### Path A — Refine existing PRD (`--prd-existing` or `--prd-file` or B6 choice)

**Primary agents:** `@Founder` (conversation) · `@Architect` (structure, technical feasibility) · `@Guide` (facilitation).

1. **Ingest:** Load from `--prd-file` if provided; otherwise ask the user to paste or attach the document.
2. **Refinement conversation** (iterate until user confirms "this matches my vision"):
   - Restate the product in one paragraph; ask what is wrong or missing.
   - **Vision & outcomes:** success metrics, non-goals, and "what would make you say no."
   - **Users & journeys:** primary personas, critical jobs-to-be-done, edge personas.
   - **Scope:** must-have vs later; dependencies; compliance or brand constraints.
   - **Features:** consolidate into a prioritized list; flag vague items and propose crisp definitions.
   - **Risks & assumptions:** explicit assumptions to validate early.
3. **Output:** Rewrite into a structured PRD and save to `.ai/plans/active/project-prd.md`.
4. **Gate:** User explicitly approves the final PRD (or "good enough for v1") before continuing to Step 1.

#### Path B — Idea → PRD (`--prd-idea` or B6 choice)

**Primary agents:** `@Founder` · `@Guide`; `@Architect` joins for stack-impacting constraints.

1. **Open exploration:** What problem, for whom, and why now? What exists today?
2. **Expand:** Propose feature candidates and user-visible outcomes; user adds, removes, and reorders. Capture explicit exclusions (non-goals).
3. **Harden:** Constraints — budget, timeline, team size, regions/locales, offline, accessibility, security/compliance hints.
4. **Synthesize:** Produce a full PRD (executive summary, problem, goals, personas, scope, feature list with priorities, success metrics, risks, open questions) in `.ai/plans/active/project-prd.md`.
5. **Gate:** User confirms the PRD before continuing to Step 1.

---

### Step 1: Project Detection / User Interview

- If **Part B completed**, use B1–B8 answers as the source of truth. Only ask clarifying questions about stack specifics, deployment target, and repo preferences.
- If **Step 0 produced `project-prd.md`**, use it to pre-fill answers and only ask clarifying questions.
- If `--type` was passed directly (no Part B), run the type-specific interview below:
  - `--mode founder` → `@Founder` asks: what are you building / who is it for / most important thing it must do / web only or mobile too / do you have a brand in mind?
  - `--mode pro` → prompt for `--type` directly and skip narrative questions.

---

### Step 2: Project Type Detection

Writes result to `.ai/context/project-type.md`, including:
- `type` — from `--type` or B4 answer
- `database` — from `--db` or clarifying question
- `monorepo` — from `--monorepo` flag or clarifying question
- `development_methodology.primary` — from B3a or `--methodology`; default `sovereign-default` if unset
- **SDD plan defaults (phase/spec layout — all methodologies):** persist **`plan_structure: phase/spec-sdd`**, **`spec_output_mode: inline`**, and **`contract_generation: auto-from-spec`**. If **`primary`** is **`contract`** or **`contract-first`** (CFG), keep the same keys; add a one-line note under **`development_methodology.notes`** that the team prefers explicit **`/contract`** checkpoints before scaling implementation (unless the user declines).

Selects the correct agent subset for the project type and sets the branching strategy (default: `hybrid` for Pro mode, `founder` for Founder mode).

After Step 2 is persisted, run **immediately**:
```bash
bash scripts/setup/create-github-workflows.sh
```
This creates `.github/workflows/` (if missing) and copies all YAML from `.ai/templates/github-workflows/` — including `ci-quality-gates.yml`, which enforces the Sovereign gate order on GitHub CI. Safe to re-run: only overwrites files that exist in the template folder.

---

### Step 3: Design-First Check

If `--brand` is passed, or project type is `brand` / `hospitality` / `multi-app`:
- Run the brand initialization flow (see `/brand` command)
- Generate design tokens **before** any app scaffold
- Produces `packages/ui/src/lib/styles/tokens.css`

---

### Step 4: Workspace Scaffold

The template root starts intentionally minimal (`CLAUDE.md`, `.cursorrules`, `.antigravity/`, `.claude/`, `scripts/`, `docs/`). Run these scripts before generating other root files:

```bash
bash scripts/cursor/init-cursor-dir.sh
bash scripts/git/init-gitignore.sh
```

`init-cursor-dir.sh` creates `.cursor/agent-transcripts/` (empty) and `.cursor/README.md` only.
`init-gitignore.sh` writes the Sovereign baseline `.gitignore`. Use `--force` only if replacing an existing file.

Generated layout:

```
├── .github/workflows/           ← already created in Step 2
├── .cursor/                     ← from init-cursor-dir.sh
├── .gitignore                   ← from init-gitignore.sh
├── .env.example                 ← based on selected integrations
├── package.json                 ← workspace root
├── pnpm-workspace.yaml          ← if --monorepo
├── turbo.json                   ← if --monorepo
├── tsconfig.json                ← TypeScript base
│
├── packages/
│   ├── shared/src/contracts/    ← empty; ready for /contract
│   ├── ui/src/
│   │   ├── components/
│   │   └── lib/styles/tokens.css
│   └── config/                  ← ESLint, TypeScript, Tailwind
├── apps/
│   ├── web/                     ← if type = web | fullstack
│   └── api/                     ← if type = backend | fullstack
│
├── scripts/dev/        run.sh  stop.sh  fresh-start.sh
├── scripts/database/   migrate.sh  add-test-data.sh  reset.sh  (only if --db ≠ none)
└── scripts/deploy/     preview.sh  go-live.sh
```

The existing `scripts/` tree (`check/`, `git/`, `hooks/`, `tools/`, `lib/`) is carried over as-is. New automation always goes under `scripts/<category>/` per `scripts/SCRIPTS_MAP.md`.

---

### Step 4b: Tool Selection

`@Guide` asks two questions to activate optional IDE integrations and AI assistants.

**Question 1 — IDE / editor tools:**
```
@Guide: Claude Code, Cursor (via .cursorrules), and Antigravity are already active.
Which of these do you also use?

  1. OpenAI Codex       → CODEX.md, AGENTS.md, .codex/
  2. VS Code tasks      → .vscode/tasks.json
  3. Windsurf IDE       → .windsurfrules
  4. Kilo Code          → .kilocode/rules/
  5. Continue.dev       → .continue/rules/
  6. None
```

**Question 2 — CI/CD assistants and AI tools:**
```
@Guide: GitHub Actions CI is already set up (Step 2).
Which of these do you also use?

  1. GitHub Copilot     → .github/copilot-instructions.md
  2. Gemini CLI         → GEMINI.md
  3. Qwen CLI           → QWEN.md
  4. OpenCode           → .opencode/AGENTS.md
  5. Amazon Q Developer → .amazonq/rules/
  6. None
```

For each selected tool, run:
```bash
bash scripts/tools/add-tool.sh <tool-name>
```

Config files for all tools live in `.ai/support/` — see `.ai/support/README.md`.

If the user skips or says "none", show how to add tools later:
```
bash scripts/tools/list-tools.sh      # see available tools
bash scripts/tools/add-tool.sh <name> # activate one anytime
```

---

### Step 5: GitHub Setup

`@Automation` prepares the initial repository state:

- Creates the first commit with the scaffolded workspace
- Creates `CODEOWNERS` referencing relevant Sovereign agents for their areas
- Confirms the branching strategy (Founder = Squash, Hybrid = Merge, Enterprise = Rebase) and the default branch protections to apply

**Requires user confirmation before applying branch protection rules** — these affect push permissions and review requirements on the remote. Show the intended rules and ask: "Apply these branch protection rules to your remote? (yes / skip for now)"

Note: Dependabot, CodeQL, and secret-scanning alerts are enabled by default on GitHub for public repos. For private repos, the user enables these in repository → Settings → Security — show a one-line reminder in the First-Run Checklist (Step 5b).

---

### Step 5b: First-Run Setup Checklist

`@Guide` shows this checklist after `/init` completes and tracks completion in `.ai/plans/active/current-sprint.md`.

```
□ Turborepo Remote Cache (reduces CI from ~10 min to ~2–3 min)
    npx turbo login && npx turbo link
  → Add TURBO_TOKEN + TURBO_TEAM to GitHub repository secrets

□ Vercel project link (if deploying to Vercel)
    vercel link
  → Add VERCEL_TOKEN + VERCEL_ORG_ID + VERCEL_PROJECT_ID to GitHub secrets

□ Lighthouse CI (for PR score comments)
  → Add LHCI_GITHUB_APP_TOKEN to GitHub secrets
  → Install the Lighthouse CI GitHub App on your repo

□ Chromatic (for visual regression)
  → Add CHROMATIC_TOKEN to GitHub secrets

□ GitHub Security (private repos only)
  → Settings → Security → enable Dependabot alerts, CodeQL analysis, secret scanning

□ Git hooks (optional — quick lint/typecheck on commit & push)
    bash scripts/setup/install-auto-checks.sh
  → See scripts/hooks/README.md
  → Skip once: SKIP=1 git commit / GALERIA_NO_HOOKS=1 git push
  → Deep push gate: PRE_PUSH_DEEP=1 git push
```

---

### Step 6: First plan — SDD phase/spec scaffold

`/init` always materializes the **canonical SDD tree** (phase → spec, eight files per spec). This is the **program-level** plan surface; methodology slugs (**`sovereign-default`** / **`sdd`** / **`contract`**, etc.) only change **emphasis** and next-command hints — not the folder shape. Reference: **`docs/workspace/reference/feature-plan-package-layout.md`**.

**6a — Directories**

Ensure these exist (create if missing):

- `.ai/plans/active/features/`
- `.ai/plans/active/tasks/` (optional empty or with a one-line README)
- `.ai/plans/active/audit/` (optional; command logs land here per workspace practice)

**6b — Bootstrap phase + spec (seed from B1–B8 and PRD)**

`@Architect` creates:

| Path | Action |
|------|--------|
| **`.ai/plans/active/features/01-foundation/manifest.md`** | New file: phase name **`01-foundation`**, table of specs with columns **Spec folder · Status (draft) · Depends on · Notes**. First row: **`01-workspace-init`** — note *Seeded at `/init`; refine `plan.md` then run SOS refresh*. |
| **`.ai/plans/active/features/01-foundation/01-workspace-init/`** | New spec folder — copy **seven** files from **`.ai/templates/sdd-spec/`** (`plan.md`, `design.md`, `context.md`, `api.md`, `database.md`, `contracts.md`, `structure.md`) and **fill placeholders** from B1–B8 (and **`project-prd.md`** when present). Replace **`[name]`** / **`[phase]`** headers with **`01-workspace-init`** / **`01-foundation`**. |
| **`01-workspace-init/prompt.md`** | **Not** in `sdd-spec/` — create a **stub**: state that the full SOS **`prompt.md`** is produced after spec confirmation; instruct **Pro** users to run **`/plan sos --refresh 01-foundation/01-workspace-init`** once `plan.md` reflects the agreed scope (same path pattern as **`/plan`**). |
| **`contracts.md`** | If **`development_methodology.primary`** is **`contract`** or **`contract-first`**, add a short “CFG” callout: explicit **`/contract create` · `validate` · `lock`** before **`/build`** at scale; SDD auto-generation still applies after **`spec:validate`** unless **`notes`** say otherwise. |

**6c — Sprint + roadmap + product-facing docs**

- **`.ai/plans/active/current-sprint.md`** — Sprint 1: link to **`features/01-foundation/01-workspace-init/`**, checklist items (Turbo/Vercel/hooks from Step 5b), and **next command**: refine seed spec → **`/plan sos --refresh 01-foundation/01-workspace-init`** → first vertical feature spec via **`/plan 01-foundation/02-<slug>`** (or next free spec id the user chooses).
- **`roadmap.md`** under **`.ai/plans/`** — from B1–B8 and **`project-prd.md`** when present; include a line that active SDD specs live under **`.ai/plans/active/features/[phase]/[spec]/`**.
- **Root README:** Rewrites **`README.md`** per the *Root README (product-facing only)* section above — product summary + **`docs/product/`** links, no Sovereign internals.
- **Human PRD:** If **`.ai/plans/active/project-prd.md`** exists, offer to write **`docs/product/prd/PRD.md`** (or the user's preferred filename).
- **Founder mode:** `@Tutor` explains the seed spec, **`manifest.md`**, and that **`prompt.md`** completes after SOS refresh.

---

## Output (Founder Mode)
```
@Founder: Your workspace is ready! Here's what was set up:

✅ Your AI team is assembled and ready
✅ Your project structure is created ([type] + [db if any])
✅ Your design system has your brand colors
✅ All quality checks are set up automatically
✅ GitHub is connected and your code is safe

Your first plan is already started (SDD): **`.ai/plans/active/features/01-foundation/01-workspace-init/plan.md`**
1. Open that file with me and tighten the story and acceptance criteria.
2. When it matches what you want, we'll refresh the AI brief: type **`/plan sos --refresh 01-foundation/01-workspace-init`**
3. Then we add your first real product slice: **`/plan 01-foundation/02-<short-name>`** (I'll help you pick the folder name).
```

## Output (Pro Mode)
```
@Guide: Workspace initialized ✅

Stack: [resolved stack — e.g. Next.js 15 + Hono + Prisma + PostgreSQL]
Design system: tokens generated ([primary token name])
Methodology: [code — e.g. Sovereign / sovereign-default or SDD / sdd; CFG / contract if contract-emphasis]
Branching: [strategy — e.g. Hybrid Agile (feature/* → develop → main)]
CI: GitHub Actions configured (all Sovereign gates)
Contracts: packages/shared/src/contracts/ ready (empty)
Monorepo: [yes — pnpm workspaces + Turborepo | no — single-app]

Plans (SDD): **`.ai/plans/active/features/01-foundation/01-workspace-init/`** (7 templates + **`prompt.md`** stub)
Next: refine **`plan.md`** → **`/plan sos --refresh 01-foundation/01-workspace-init`** → **`/plan 01-foundation/02-<spec>`** for first vertical slice → gates → **`/build`**
CFG (`contract`): add explicit **`/contract create [domain]`** / **`lock`** when **`contracts.md`** is ready for human checkpoint.
```

---

## Flags Reference

| Flag | Options | Default | Description |
|------|---------|---------|-------------|
| `--type` | web, mobile, backend, fullstack, brand, ai-native, gov-tech, multi-app | auto-detect | Project type |
| `--db` | postgres, mysql, sqlite, none | postgres | Database type |
| `--mode` | founder, pro, hybrid | hybrid | Interaction mode |
| `--brand` | flag | false | Run brand initialization before app scaffold |
| `--monorepo` | flag | false | Enable pnpm workspaces + Turborepo layout |
| `--strategy` | founder, hybrid, enterprise | hybrid | Git branching strategy |
| `--prd-existing` | flag | false | Start PRD **refinement** conversation |
| `--prd-file` | filesystem path | — | Load existing PRD from this path (implies `--prd-existing`) |
| `--prd-idea` | flag | false | Idea-first interview → generate new PRD |
| `--no-prd` | flag | false | Skip all PRD prompts |
| `--methodology` | sovereign-default, sdd, contract, contract-first, tdd, design-first, agile-lean, phase-gated | ask at B3a | Development style — see **Development methodology options** (`sovereign-default` = SDD) |

---

*Invokes: @Guide · @Architect · @Founder (Founder mode + PRD paths) · @Automation · @DesignSystem (--brand)*
