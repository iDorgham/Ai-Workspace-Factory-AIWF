# 🤖 AIWF AGENT REGISTRY (v8.0.0)

The AI Workspace Factory operates via a specialized swarm of agents, each governed by specific sovereign protocols and consensus rules.

---

## 🏛️ CORE AGENTS — T0 (Always Active)

| Agent | Role | Responsibility |
| :--- | :--- | :--- |
| **Master Guide** | Orchestrator | High-level strategy, orchestration, cross-project sync, Omega Gate mediation, and global memory management. |
| **Healing Bot v2** | Supervisor | Predictive structural monitoring, drift detection, and auto-remediation. Executes `/dev fix`. |
| **Swarm Router v3** | Mediator | Routes tasks across agents, resolves conflicts via multi-agent consensus (≥2/3 agreement required). |
| **Recursive Engine** | Scientist | Analyzes session friction and corrections → converts into permanent skill manifests. |
| **Chaos Validator** | Stress-Tester | Injects controlled stressors to verify isolation boundaries and adaptive recovery. |
| **Repository Agent** | Guardian | Manages `/git auto` protocols, silent versioning, and industrial traceability. |

---

## 🔬 SPECIALIZED SUB-AGENTS — T1 (Dynamically Spun by Swarm Router v3)

| Sub-Agent | Role | Responsibility |
| :--- | :--- | :--- |
| **Spec Architect** | Designer | Builds and validates `spec.md` + `spec.yaml` per the AIWF SDD Blueprint schema. |
| **Contract Guardian** | Enforcer | Enforces `api-contract.yaml`, `state-contract.json`, and all test fixtures. Blocks `/dev` if contracts fail. |
| **Regional Adapter** | Localizer | Injects Egypt/Red Sea/MENA adaptations: Arabic RTL, Fawry/Vodafone Cash, Law 151/2020 data residency, EGP/SAR/AED handling, tourism/hospitality features. |
| **Deployment Specialist** | Deployer | Manages Vercel deployments, environment variables, preview/production separation. Only invoked via `/deploy`. |
| **Integrity Auditor** | Inspector | Runs path integrity, sovereignty checks, and `/audit` suite analysis. |
| **CI Specialist** | Workflow Tech| Autonomous repair of CI/CD failures via `/git action fix`. |
| **Security Auditor** | Sentinel | Predictive security patching and hardening via `/git security fix`. |
| **Visualize Agent** | Designer | High-fidelity asset generation via `/create image`. |
| **Creator Agent** | Assembler | Scaffolds high-fidelity content via `/create content`. |
| **Scraper Agent** | Ingestor | High-performance data extraction via `/content scrape`. |

---

## 🛠️ COMPOSITION AGENTS — T2

| Agent | Role | Responsibility |
| :--- | :--- | :--- |
| **Factory Scaffolder** | Architect | Assembles new sovereign workspaces from curated `factory/library/` components. |
| **Profile Auditor** | Gatekeeper | Ensures workspace profiles align with library schemas and compliance rules. |

---

## 📋 REQUIRED SKILLS (Enforced Across All Agents)

- **Library-First Composition**: Always pull from `factory/library/` and `factory/shards/` (industrial OS sources) before generating ad-hoc.
- **Append-Only Traceability**: All mutations include ISO-8601 timestamp + Reasoning Hash + rollback pointer.
- **Fail-Forward Recovery**: Errors trigger repair branches, not session termination.
- **Token Efficiency**: Session overhead < 2.5% via structured outputs.
- **MENA Sovereignty & Cultural Compliance**: Regional adaptations applied when `--region` flag is active.
- **Spec-Driven Execution**: All implementation gated on validated `spec.yaml` contract.
- **Silent Versioning & Tagging**: Version increments and Git tagging are performed automatically and silently upon phase completion.

---

## 📜 SOVEREIGN SDD PROTOCOLS (Planning Rules)

All SDD Planning phases must adhere to the following mandatory industrial standards:

1. **High-Density Specification**: Each planning phase MUST contain at least **5 unique specifications** (`spec.md` + `spec.json`).
2. **Agent Proliferation**: Each version must introduce or refine at least one **specialized sub-agent** (T1) dedicated to the phase's core domain.
3. **Skill Synthesis**: At least **2 new skills** discovered during implementation must be codified into the global skill library (`.ai/skills/`).
4. **OMEGA Health Audit**: Every phase must include a mandatory **Health & Performance Optimization** task targeting a perfect 100/100 OMEGA-tier score.
5. **Library-First Evolution**: Each phase must include a dedicated task for **refining and enhancing the core library** (`factory/library/`).
6. **Autonomous Automation**: Every phase must introduce at least one **automation script** or internal tool refinement.
7. **Command Ergonomics**: Existing CLI commands and subcommands must be **refined for efficiency** and cinematic logic flow.
8. **Invisible Traceability**: Versioning and Git tags must be applied **automatically and silently** without blocking the main workflow.

---

## 🧠 Learned User Preferences
- **egyptian_arabic_content_master**: Embed reference data inside the skill; do not link `docs/ar.md`; keep English alongside Arabic in `prompt_library/`; prioritize **humanized Egyptian Arabic** quality across **web**, **blogs**, **marketing**, **articles**, **ads**, **social**, **business comms**, **video scripts**, **storytelling**, **humor**, **contracts**, and **legal-plain-language**.
- **Industrial Aesthetic**: Prefers dark mode, high-tech, and "premium" visual styling for all artifacts and UIs.
- **Library-First**: Prioritizes reuse and versioning over ad-hoc generation.
- **Traceability**: Requires ISO-8601 timestamps and Reasoning Hashes for all autonomous mutations.
- **Skills Layout Convention**: Store each skill in its own folder named after the skill with `skill.md` inside.
- **`/guide` handoff focus**: Keep **one** short next-step list scoped to the **current** task; avoid extra **workspace-wide “what to develop next”** lists that conflict with a single **Next prompt** or **Next terminal command**. When the next step is a terminal line, spell out **in plain words** what that command does (see `.cursor/rules/guide-handoff-footer.mdc`).
- **Pre-commit vendored bundles:** Upstream import trees `factory/library/skills/github_imports/`, `factory/library/skills/nexu_open_design/`, and `factory/library/agents/github_imports/` stay on the **skip_prefixes** list in `factory/scripts/core/pre_commit_gate.py` and `pre_commit_hook_v2.py`; first-party paths elsewhere remain strict.
- **`workspaces/clients/README.md` framing:** Keep that file **product- and website-first** (portfolio + CMS story, docs links, IDE workspace hints); do not center **AIWF** monorepo branding, slash-command catalogs, factory materialize scripts, galaxy-tier tables, or SDD gate tutorials there unless the user explicitly asks for platform framing.

## 📋 Learned Workspace Facts
- **Human docs layout:** Canonical specs live under **`docs/`** by category — **`docs/overview/CONTEXT.md`**, **`docs/product/PRD.md`**, **`docs/product/ROADMAP_LONGTERM.md`**, **`docs/guides/`**, **`docs/profile/`** (operator playbooks: commands, design onboarding, git, hooks — replaces legacy **`PROFILE_DOCS/`** in WEB_OS_TITAN materialization), **`docs/planning/`**, **`docs/context/`**, **`docs/reports/`**; index **`docs/README.md`**. Legacy root stubs (`docs/PRD.md`, …) were moved to **`docs/archive/legacy-root-redirects/`**.
- **`/guide` Humanization (v3.5):** Antigravity = **Sovereign Guardian · Master Teacher · SDD Process Overseer**; natural-language `/guide …` is **instructor mode** first; **layered teaching (L0–L3)** + **inline SDD guardian** per `.ai/commands/guide.md` and **`.cursor/rules/guide-response-style.mdc`**. Skills: `.ai/skills/guide_instructor_domains/`, `guide_teaching/`, `guide_sdd_mastery/`. **Canonical + mirror:** edit `.ai/commands/guide.md`, then `cp` to `factory/library/commands/guide.md` or `bash factory/scripts/core/sync_ide_triple_layer.sh`. Persona: `.ai/agents/core/antigravity.md` (**v2.2.0**). Optional subagents: `guide_teacher.md`, `guide_sdd_guardian.md`, `guide_instructor.md`.
- **Continual-learning index**: `.cursor/hooks/state/continual-learning-index.json` — parent transcript paths + mtimes only (no secrets); **local** under `.cursor/` — never commit; IDE/hooks refresh on disk.
- **Root Directory**: `/Users/Dorgham/Documents/Work/Devleopment/AIWF`
- **Sovereign Isolation**: All client work is strictly contained within `workspaces/<slug>/`.
- **Governance**: All structural changes require explicit `Dorgham-Approval` via Omega Gate v2.
- **Deploy Policy**: Vercel deployment ONLY via explicit `/deploy` command — never auto-triggered.
- **Canonical library layout**: Skill bundles under `factory/library/skills/<skill_id>/` (each folder is typically a mirrored `.ai/skills/` tree with `skill.md`); **agents + governance** outbound mirror under `factory/library/core_orchestration/` (`registry/agents`, `omega_singularity/governance` — see `industrial_mirror_sync.py`); subcommands under `factory/library/subcommands`, subagent registry at `factory/library/subagents/registry.json`, imported design packs (VoltAgent awesome-design-md) under `factory/library/design/<provider>/design.md` with catalog `factory/library/design/README.md`; runtime specialized subagents live under `.ai/subagents` (not `.ai/agents/specialized/subagents`). Workspace **stubs** for `/init` live under `factory/stubs/` (e.g. `distribution/`, `fintech/`); **design** and **subagents** catalogs are canonical under `factory/library/design/` and `factory/library/subagents/` (also mirrored into `factory/library/templates/` and `.ai/templates/` by `external_library_sync.py` — not duplicated under `factory/templates/`).
- **CORE_OS_SAAS template**: `factory/shards/CORE_OS_SAAS` is a pnpm workspace + Turborepo (`turbo.json`, root scripts call `turbo run`); Next.js app root is `apps/web`; for Next `15.0.0-rc.0` in that template use `apps/web/next.config.mjs` (TypeScript next config is not loaded).
- **`active_phase` & `phase.spec.json`:** In `.ai/plan/_manifest.yaml`, **`active_phase`** is the numeric phase **`id`** (e.g. `18`), not alphanumeric rows like **`18G`**; avoid duplicate **`status: active`**. When **`phase.spec.json`** is neither **`draft`** nor **`planned`**, v21 density applies — use **`pending`** for scaffolds that may proceed without claiming **`active_phase`**; promote **`active`** only via coordinated manifest workflow.
- **`/mat` (`factory_materialize.sh`):** **Template roots** resolve in order: **`MAT_TEMPLATES_DIR`** (if set and contains immediate template subdirs) → **`factory/shards/`** → else **`workspaces/templates/`** when shards are empty; the script echoes which root was chosen. **After copy**, **only** the template **folder basename** → target **slug** is substituted in text; **do not** bulk-rewrite `factory/shards`, `workspaces/templates`, or legacy template roots to `workspaces/<layer>` — that breaks paths from inside `workspaces/clients|personal/<slug>/`. Keep **`bin/materialize.sh`** and **`factory/library/scripts/workspace_imports/ai/scripts/factory_materialize.sh`** aligned with **`.ai/scripts/factory_materialize.sh`**.
- **Commands canonical merge**: Maintain **one** merged router registry at **`.ai/commands/commands.md`** (not parallel **`commands_multi_tool`** / **`commands-multi-tool`** files under **`.cursor/commands/`**); after edits, sync **`.cursor/commands/`** and local **`.antigravity/commands/`** to match **`.ai/commands/`** via **`bash factory/scripts/core/sync_ide_triple_layer.sh`**, and keep **`factory/library/commands/`** mirrors in step per Outbound Mirror Protocol. For broader **`.ai/`** → **`factory/library/`** propagation (agents, skills, subagents, rules, plans), run **`python3 factory/scripts/core/industrial_mirror_sync.py`** after substantive changes.

---

*Registry version: 8.0.0*
*Last updated: 2026-05-01T01:15:29Z*
*AIWF System Compatibility: v20.0.0*
