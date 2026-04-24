---
type: Command
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---


# Command: /help

> **Agent:** @Guide
> **Purpose:** Provide contextual help — commands, workspace, agents, modes
> **Scope:** Navigation, state awareness, contextual guidance

---

## Usage

```bash
/help [commands|workspace|agents|mode] [--verbose]
/help [command-name]  # Help for specific command
```

---

## Execution Flow

### 1. `/help` — General Help (No Subcommand)

**Output:**
```markdown
## Sovereign Workspace Factory Help

**Project:** [Project name from project-type.md]
**Type:** [Project type]
**Mode:** [Current mode]
**Sprint:** [Current sprint N]

### Quick Start
| If you want to... | Run this |
|--------------------|----------|
| Start a new project | `/init` (explain + discovery) or `/init --type [type] --mode [mode]` — see `.ai/commands/init.md` for PRD flags |
| Plan a feature | `/plan [feature-name]` |
| Check project status | `/status` or `/next` |
| Build a feature | `/build [feature]` (after /plan and /contract) |
| Get brand/design set up | `/brand` |
| See all commands | `/help commands` |
| Understand the agents | `/help agents` |

### Current State
- **Contracts:** [N] locked, [N] pending
- **Active features:** [N]
- **Sprint progress:** [N]% complete
- **Quality gates:** All passing ✅ / Issues found ❌

### Need More Help?
- **New to Sovereign?** Read **`docs/workspace/guides/ONBOARDING.md`** (first day) and **`docs/workspace/guides/GUIDE_COMPANION.md`** (how @Guide follows you + end-of-reply next steps)
- `/help commands` — All available commands
- `/help agents` — Agent swarm reference
- `/help workspace` — Workspace structure
- `/help mode` — Mode explanations
- `/help [command]` — Help for specific command

**Type a command or ask me a question about your project!**
```

---

### 2. `/help commands` — Command Reference

**Parameters:**
- `--verbose`: Optional — detailed descriptions for each command

**Output (default):**
```markdown
## Sovereign Commands Reference

### Project Setup
| Command | Description |
|---------|-------------|
| `/init` (no flags) or `/init [flags…]` | Scaffold / align workspace; bare `/init` = explain command + guided discovery |
| `/detect-project-type` | Auto-detect project type from workspace |
| `/brand [--name] [--colors] [--fonts]` | Initialize brand design system |

### Planning
| Command | Description |
|---------|-------------|
| `/plan [feature-name] [sprint|roadmap|backlog]` | Create feature plan |
| `/monorepo status|add-app|add-package` | Manage monorepo structure |

### Contracts
| Command | Description |
|---------|-------------|
| `/contract create|validate|lock|diff [domain]` | Manage Zod contracts |

### Building
| Command | Description |
|---------|-------------|
| `/build [feature|component|api] [--dry-run]` | Generate code |
| `/swarm run|abort|status [feature]` | Multi-agent orchestration |

### Testing & Quality
| Command | Description |
|---------|-------------|
| `/test [unit|e2e|visual|a11y] [--coverage]` | Run tests |
| `/quality [security|compliance|all]` | Run quality gates |
| `/diagnose [feature|performance|security|logs]` | Deep diagnostics |

### Git & Deployment
| Command | Description |
|---------|-------------|
| `/branch [type] [name] [--strategy]` | Create Git branch |
| `/commit [--message] [--auto]` | Commit changes |
| `/push [--pr]` | Push to remote |
| `/deploy [staging|production] [--rollback]` | Deploy application |

### Monitoring & Improvement
| Command | Description |
|---------|-------------|
| `/metrics dashboard|velocity|risk|forecast` | View metrics |
| `/retro start|action-items` | Run retrospective |
| `/upgrade [dependencies|stack|contracts]` | Upgrade dependencies |

### Configuration
| Command | Description |
|---------|-------------|
| `/mode switch|status [--mode]` | Switch operational mode |
| `/help [commands|workspace|agents|mode]` | This help system |

**For detailed help on any command:** `/help [command-name]`
```

**Output (verbose):**
```markdown
## Sovereign Commands Reference (Detailed)

### /init — Project Initialization
```bash
/init
/init [--type web|mobile|backend|fullstack|brand|ai-native|gov-tech|multi-app]
      [--db postgres|mysql|sqlite|none]
      [--mode founder|pro|hybrid]
      [--methodology sovereign-default|sdd|tdd|design-first|agile-lean|phase-gated]
      [--brand] [--monorepo] [--strategy founder|hybrid|enterprise]
      [--prd-existing] [--prd-file <path>] [--prd-idea] [--no-prd]
```
**Bare `/init` (no flags):** @Guide explains how to use `/init`, then @Founder runs **step-by-step discovery** (B1–B8, including **B3a** development methodology with explanations); no scaffold until the user confirms the summary — see **`.ai/commands/init.md`**.
**With flags:** Scaffolds workspace structure, creates apps and packages, sets up configs.
**PRD paths:** Optional refine or idea-to-PRD → **`.ai/plans/active/project-prd.md`**; human copies under **`docs/product/prd/`** (see **`docs/product/README.md`**). Default **`--prd-file`** suggestion: **`docs/product/prd/PRD.md`**.
**Root readme:** After `/init`, root **`README.md`** is **product-only**; full Sovereign template readme stays at **`docs/workspace/README.md`**.
**Learner memory:** Updates **`.ai/memory/user-learning-profile.md`** during discovery; @Tutor maintains **`.ai/memory/learning-progress.md`**.
**When to use:** New project, re-alignment, or PRD-first setup.
**What it creates (typical):**
- apps/ directory with selected app types
- packages/ directory with shared, ui, config
- pnpm-workspace.yaml with catalog
- turbo.json with pipeline
- .ai/context/project-type.md with detected configuration
**Agents involved:** @Guide, @Architect, @Founder (discovery/PRD), @Tutor (learning files)

... [detailed entry for each command] ...
```

---

### 3. `/help workspace` — Workspace Structure

**Output:**
```markdown
## Sovereign Workspace Factory Structure

```
/
├── README.md                   ← Your product (after /init); not Sovereign marketing
├── CLAUDE.md, GEMINI.md, QWEN.md, AGENTS.md  ← CLI / universal instructions
├── CODEX.md                    ← OpenAI Codex playbook
├── docs/
│   ├── README.md               ← Documentation index
│   ├── DOCUMENTATION_MAP.md    ← Where new markdown must go (categories)
│   ├── workspace/              ← Hub README + guides/ + reference/
│   ├── product/                ← Your PRD + ideas (README, prd/, idea/)
│   └── archive/                ← Superseded drafts
├── scripts/                    ← SCRIPTS_MAP + check/ git/ setup/ hooks/ lib/
├── .vscode/tasks.json          ← Optional Sovereign tasks (validate, hooks)
├── .codex/config.toml              ← Codex project layer (when trusted)
├── .cursorrules, .windsurfrules    ← Cursor / Windsurf rules
│
├── .ai/                             ← AI Knowledge & Operations Layer
│   ├── context/                     ← Global standards (READ FIRST — see README.md)
│   │   ├── README.md                ← Catalog + conditional load matrix
│   │   ├── architecture.md          ← System design, tech stack, naming
│   │   ├── coding-standards.md      ← TypeScript, React, API, tests, security patterns
│   │   ├── project-type.md          ← Active project configuration
│   │   ├── design-system.md         ← Token governance, components
│   │   ├── brand-grammar.md         ← Brand voice, emotional intent
│   │   ├── skills-framework.md      ← Skills matrix (9 categories)
│   │   ├── security.md              ← Trust boundaries, review triggers (@Security)
│   │   ├── internationalization.md  ← EN/AR, RTL, a11y baseline (@I18n, @Accessibility)
│   │   └── quality-gates.md         ← Gate order: contract → compliance → security → test → build → deploy
│   │
│   ├── agents/                      ← 35 agent definitions (.md files)
│   ├── skills/                      ← 48+ reusable capability modules
│   ├── commands/                    ← 19 command handlers
│   ├── templates/                   ← 17+ scaffolds + README catalog (PRD, risk, bug, spike, test plan, story, release, incident, backlog, …)
│   ├── memory/                      ← Institutional + learner memory (see README.md)
│   │   ├── README.md                      ← Catalog + DMP map
│   │   ├── decisions.md                   ← Architecture decision log
│   │   ├── lessons-learned.md             ← Retro insights
│   │   ├── project-context.md             ← Current project state
│   │   ├── anti-patterns.md               ← DMP Step 0 — never-repeat rules (AP-IDs)
│   │   ├── error-patterns.md              ← Active error log (EP-IDs)
│   │   ├── user-learning-profile.md       ← Expertise signals, readings, session notes
│   │   ├── learning-progress.md           ← Concepts checklist (@Tutor)
│   │   └── archive/                       ← Retired APs, EP sprint snapshots
│   │
│   └── plans/                       ← Planning & tracking
│       ├── active/                  ← Current work
│       │   ├── current-sprint.md    ← Sprint goals + progress
│       │   ├── features/            ← Feature plans (one per feature)
│       │   ├── tasks/               ← Granular tasks
│       │   └── audit/               ← Command logs, escalations
│       ├── backlog/                 ← Future work
│       ├── archive/                 ← Completed work
│       └── roadmaps/                ← Long-term planning
│
├── packages/                        ← Shared code
│   ├── shared/src/contracts/        ← Zod schemas (CONTRACT-FIRST)
│   ├── ui/src/                      ← Design tokens + components
│   └── config/                      ← ESLint, TypeScript, Tailwind configs
│
├── apps/                            ← Deployable applications
│   ├── web/                         ← Next.js App Router
│   └── api/                         ← Hono/Fastify backend
│
└── .github/                         ← CI/CD, workflows, Copilot instructions
```

### Key Principles
1. **SDD (default):** **`sovereign-default`** or **`sdd`** — confirmed spec → auto Zod + lock in `packages/shared/src/contracts/` before implementation. **`/init --methodology contract`** (or **`contract-first`**) for **CFG** / contract-emphasis (slug **`contract`**).
2. **Design-First:** Brand → tokens → components → apps (never reverse)
3. **Dynamic Memory:** Agents load context in strict 7-step sequence
4. **Quality Gates:** spec:validate → contract:auto-validate → compliance → security:scan → test → build → deploy
5. **Self-Generation:** Missing resources auto-generated from templates

### File Ownership
| Directory | Managed by | Modified by |
|-----------|------------|-------------|
| .ai/context/ | @Architect | @Architect, @Guide |
| .ai/agents/ | @Guide | Read-only (definitions) |
| .ai/skills/ | @RetroFacilitator | @RetroFacilitator, @Architect |
| .ai/commands/ | @Guide | @Guide, @Architect |
| .ai/templates/ | @Architect | @Architect, @Guide |
| .ai/memory/ | @RetroFacilitator, @Tutor | All agents (append); @Tutor owns **learning-progress** + **user-learning-profile** updates |
| .ai/plans/active/ | @Guide | All execution agents |
| packages/shared/src/contracts/ | @Architect | @Architect, @Backend, @Frontend |
| packages/ui/ | @DesignSystem | @Frontend, @DesignSystem |
| apps/ | @Frontend, @Backend | Execution agents |
```

---

### 4. `/help agents` — Agent Swarm Reference

**Output:**
```markdown
## Sovereign Agent Swarm (35 Agents)

### Leadership Tier
| Agent | Role | When to invoke |
|-------|------|----------------|
| @Founder | Non-technical interface | Business vision, progress reports |
| @Guide | Master orchestrator | /next, /status, sprint planning |
| @Architect | System design, contracts | /plan, /contract, architecture questions |

### Execution Tier
| Agent | Role | When to invoke |
|-------|------|----------------|
| @Frontend | UI components, a11y, RTL | Building UI components |
| @Backend | APIs, services, logic | Building backend features |
| @DBA | DB schemas, migrations | Database changes |

### Quality Tier
| Agent | Role | When to invoke |
|-------|------|----------------|
| @QA | Test suites, coverage | /test, test writing |
| @Reviewer | Code review, drift gating | Pre-merge review |
| @Security | OWASP, zero-trust | /quality security, security-sensitive code |
| @DesignSystem | Visual tokens, components | UI component creation |
| @Content | i18n keys, UX copy | All user-facing text |
| @VisualQA | Visual regression | Post-build visual validation |
| @BrandGuardian | Brand grammar, emotional intent | Brand-sensitive features |

### Infrastructure Tier
| Agent | Role | When to invoke |
|-------|------|----------------|
| @Automation | CI/CD, Git, deployment | /branch, /commit, /push, /deploy |
| @Router | Task routing, parallelism | /swarm, multi-step features |
| @ContractLock | Zod validation, fingerprints | /contract validate/lock |
| @ContextSlicer | Context loading, token budgets | Pre-execution context |
| @Optimizer | Performance, Lighthouse | /diagnose performance |

### Intelligence Tier
| Agent | Role | When to invoke |
|-------|------|----------------|
| @MetricsAgent | Velocity, compliance scores | /metrics dashboard |
| @RiskAgent | 5×5 risk register | /metrics risk, feature planning |
| @AnalyticsAgent | Trend analysis | /metrics (future enhancement) |
| @ForecastingAgent | Probabilistic forecasting | /metrics forecast |

### Learning Tier
| Agent | Role | When to invoke |
|-------|------|----------------|
| @RetroFacilitator | Retrospectives | /retro start |
| @EscalationHandler | Blocked tasks, SBAR | Blocked work, critical failures |
| @Tutor | Teaching, explanations | After significant actions (Founder mode) |

**Full agent definitions:** `.ai/agents/[agent-name].md`
```

---

### 5. `/help mode` — Mode Reference

**Output:**
```markdown
## Operational Modes

| Mode | Audience | Verbosity | Best for |
|------|----------|-----------|----------|
| **founder** | Non-technical | High — explain everything | Business users, vision setting |
| **pro** | Technical | Low — assume expertise | Developers, architects |
| **hybrid** | Mixed | Adaptive — detect from context | Teams with varying skills |
| **build** | Any | Minimal — just code | Fast code generation |
| **brand** | Designers | Moderate — design rationale | Design system, brand work |
| **gov** | Compliance | High — compliance detail | Security audits, gov projects |

**Current mode:** [mode]
**Switch mode:** `/mode switch --mode [mode]`
**Check status:** `/mode status`

### Mode Behaviors
| Behavior | founder | pro | hybrid | build | brand | gov |
|----------|---------|-----|--------|-------|-------|-----|
| Plain language | ✅ | ❌ | Adaptive | ❌ | ❌ | ❌ |
| Technical detail | ❌ | ✅ | Adaptive | ✅ | ✅ | ✅ |
| @Tutor active | ✅ | ❌ | Adaptive | ❌ | ❌ | ❌ |
| @DesignSystem active | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| @BrandGuardian active | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| @Security active | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Quality gates enforced | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

**Quality gates are non-negotiable in all modes.**
```

---

### 6. `/help [command-name]` — Specific Command Help

**Flow:**
1. Read command file: `.ai/commands/[command-name].md`
2. Extract usage, parameters, examples
3. Present concise help

**Output:**
```markdown
## Help: /[command-name]

**Agent:** @AgentName
**Purpose:** [One-line description]

### Usage
```bash
/[command-name] [subcommand] [--flag value]
```

### Examples
```bash
/[command-name] [example 1]
/[command-name] [example 2]
```

**Full documentation:** `.ai/commands/[command-name].md`
```

---

## Contextual Help

@Guide provides contextual help based on user's current situation:

| User situation | Proactive help offered |
|----------------|----------------------|
| Just ran `/init` | "If you used bare `/init`, confirm your summary then continue to PRD/scaffold per playbook. Next often: `/brand` if design-first, else `/plan [feature]` — see `.ai/commands/init.md`" |
| Running `/plan` for first time | "Here's how planning works: /plan → /contract → /build → /test → /deploy" |
| After contract lock | "Contract locked! Ready to build. Run `/build [feature]` or `/swarm run [feature]`" |
| Quality gate failure | "Gate failed: [details]. Run `/diagnose [type]` to investigate, or ask me what to do" |
| Sprint complete | "Sprint done! Run `/retro start` to reflect, then `/metrics dashboard` for stats" |

---

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| "Unknown command" | Command not in help system | Check spelling, or command doesn't exist |
| "Command not found" | `.ai/commands/[name].md` missing | Command handler not created yet |
| "No help available" | Help topic not defined | Use general /help or ask specific question |

---

## Integration Points

- **@Guide:** Primary help provider, contextual guidance
- **@Founder:** Translates help to business language in founder mode
- **@Tutor:** Explains concepts after help interactions in founder mode
- **All agents:** Can reference help system when users ask domain-specific questions

---

*Command Version: 1.0 | Created: 2026-04-08 | Maintained by: @Guide*
