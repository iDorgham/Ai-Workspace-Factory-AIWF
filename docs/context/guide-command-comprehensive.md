# `/guide` command — comprehensive context (AIWF)

**Purpose:** Single reference for humans and **other AI tools** planning improvements to `/guide`.  
**Scope:** Slash command behavior, Humanization Engine, mirrors, rules, agents, subagents, skills, routing registries, sync scripts, and **known collisions** with similarly named artifacts.  
**Last reviewed:** 2026-05-02  
**Canonical command spec:** `.ai/commands/guide.md` (Humanization **v3.5** — Sovereign Guardian · Master Teacher · SDD Overseer)  
**v3.5 additions:** `.cursor/rules/guide-response-style.mdc`, `.ai/skills/guide_teaching/`, `.ai/skills/guide_sdd_mastery/`, `.ai/subagents/guide_teacher.md`, `.ai/subagents/guide_sdd_guardian.md`, `antigravity.md` v2.2.0

---

## 1. Executive summary

| Layer | What it is |
|--------|------------|
| **User-facing** | Cursor / Antigravity slash command **`/guide`** (and prefixes `g/`, `guide>`, `>>guide`, `[guide]` per spec). |
| **Persona** | **Antigravity** — T0 root persona; active on `/guide` triggers only; otherwise assistants behave as standard models. |
| **Spec** | **Humanization Engine v3.5** lives entirely in **`.ai/commands/guide.md`** (no separate `guide_humanize.md`). |
| **Global UX rule** | **Every** substantive reply in this workspace ends with the **guide-style handoff footer** (see §5). |
| **Instructor mode** | Natural language after `/guide` (when not a known subcommand token) → teach first; do not answer “unrecognized subcommand” for real questions. |
| **Compliance** | Egyptian **Law 151/2020** called out for MENA/Egypt context; deploy policy and governance elsewhere in `AGENTS.md`. |

---

## 2. Version and metadata (edit when bumping)

| Artifact | Typical version / note |
|----------|-------------------------|
| `humanization_version` in `.ai/commands/guide.md` frontmatter | **3.4.0** |
| `aiwf_version` in same file | **v21.0.0** |
| `version` (command-registry tier) | **20.0.0** (OMEGA tier in frontmatter) |
| `.ai/agents/core/antigravity.md` | **v2.1.0** |
| `.ai/subagents/guide_instructor.md` | **v1.0.0** |
| `.ai/subagents/guide_teacher.md` | **v1.0.0** (Master Teacher) |
| `.ai/subagents/guide_sdd_guardian.md` | **v1.0.0** (SDD audits) |

**Reasoning hash** in `guide.md` frontmatter is the traceability anchor for that revision (e.g. `sha256:aiwf-guide-terminal-explain-2026-05-02`).

---

## 3. File map — canonical, mirrors, and where to edit

### 3.1 Canonical source (edit here first)

| Path | Role |
|------|------|
| **`.ai/commands/guide.md`** | **Single source of truth** for `/guide`: subcommands, instructor mode, v21 planning intelligence, tone engine, brand grammar, memory, operational constraints, templates, pre-response checklist, validation suite. |

### 3.2 Required mirrors (keep byte-identical after substantive edits)

| Path | Notes |
|------|--------|
| **`factory/library/commands/guide.md`** | Outbound factory library mirror. Sync: `cp .ai/commands/guide.md factory/library/commands/guide.md` |
| **`.cursor/commands/guide.md`** | Cursor slash injection; must match canonical. |
| **`.antigravity/commands/guide.md`** | Antigravity layer; same. |

**Automated sync:** `bash factory/scripts/core/sync_ide_triple_layer.sh` rsyncs **`.ai/commands/`** → `.cursor/commands/` and `.antigravity/commands/`, then **deletes** legacy duplicates: `commands-multi-tool.md`, `commands_multi_tool.md`, **`guide_humanize.md`**.

### 3.3 Related command registry (not a second humanization spec)

| Path | Role |
|------|------|
| **`.ai/commands/commands.md`** | Command router + **MULTI-TOOL RANKINGS**; slash-doc sync instructions point at `sync_ide_triple_layer.sh`. |
| **`.cursor/commands/README.md`** | Documents canonical tree under `.ai/commands/` and merged files policy. |

### 3.4 Legacy / parallel paths (do not confuse with Antigravity `/guide`)

| Path | Warning |
|------|---------|
| **`factory/library/subcommands/guide.md`** | Describes a **different** “Guide” workflow (routing user intent to `/plan`, `/develop`, `/github`, etc.). **Not** the Antigravity Humanization Engine. Treat as naming collision when searching. |
| **`factory/library/archive/legacy_pillars/**/.../guide.md`** | Historical / pillar copies; may drift. Prefer `.ai/commands/guide.md` + `factory/library/commands/guide.md`. |
| **`factory/library/archive/legacy_pillars/.../guide-protocol.md`** | Orchestration protocol; related theme, different contract. |

---

## 4. Command tree (behavioral contract)

Summarized from **`.ai/commands/guide.md`**. Implementations should match this tree even if routing JSON is incomplete.

### 4.1 Meta

- `/guide help` — full reference text  
- `/guide ping` — activation check (v3.5 string)  

### 4.2 Instructor (default for non-token remainder)

- `/guide` + natural language question/topic  
- `/guide explain <topic>`  
- `/guide understand <concept>`  

**Dispatch rule:** multi-word or question-shaped input → **instructor**; single mistyped token near `plan`/`heal`/… → suggest closest match + `/guide help`.

### 4.3 Creative / pedagogical

- `/guide brainstorm about [topic]` — humanized **A / B / C** directions (+ brand grammar on visual topics)  
- `/guide brainstorm` or `/guide brainstorm [system context]` — **strategic** route to `master_guide` (not the 3-direction humanized path)  
- `/guide tutor [topic]` — Anchor → Explore → Extend  
- `/guide learn [topic]` — friction → skill extraction (`recursive_engine` in AGENT lore)  

### 4.4 v21 planning intelligence (dense, structured)

- `/guide plan [type]` — types: `development`, `content`, `seo`, `social_media`, `marketing`, `business`, `media`, `branding`  
- `/guide plan status` — reads **`.ai/plan/_manifest.yaml`**  
- `/guide spec [topic]` — ≥12 spec bullets, density gate framing  
- `/guide gate [phase_path]` — density gate explanation + `spec_density_gate_v2.py` invocation  
- `/guide adapter [task]` — CLI adapter recommendation + ledger reminder  

### 4.5 System routing (no humanization layer in spec)

- `/guide heal` → healing_bot  
- `/guide chaos` → chaos_validator  
- `/guide dashboard` → orchestrator  

### 4.6 Session controls

- `/guide mode:[poet|mentor|critic|explorer|co_creator]`  
- `/guide creativity:[high|medium|low]`  
- `/guide memory:view | export | clear`  

### 4.7 Activation aliases (per spec)

`/guide`, `g/`, `guide>`, `>>guide`, `[guide]` — equivalent triggers.

---

## 5. Rules (Cursor / global assistant behavior)

### 5.1 Always-on: handoff footer

| Path | `alwaysApply` |
|------|----------------|
| **`.cursor/rules/guide-handoff-footer.mdc`** | **true** |

### 5.2 `/guide` body structure (Antigravity only)

| Path | `alwaysApply` |
|------|----------------|
| **`.cursor/rules/guide-response-style.mdc`** | **true** (rule text: apply layout **only** on `/guide` turns) |

**Effect:** After substantive answers, append in order:

1. `---`  
2. `### What to do next` — 2–4 short bullets, plain English, scoped to the task  
3. **Exactly one** of:  
   - `### Next prompt` — one fenced ```text block, **one line**, real `/…` from `.cursor/commands/` or `.ai/commands/`  
   - `### Next terminal command` — one fenced `bash`/`text` block, **one line**, real command  

**Critical pairing:** If step 3 is **Next terminal command**, at least one bullet in step 2 must explain **what the command does** (not inside the fence).  

Mirrored to **`.antigravity/rules/`** and **`.ai/rules/`** by `sync_ide_triple_layer.sh` (authoritative UI tree is **`.cursor/rules/`**).

### 5.3 In-spec constraints (from `guide.md`)

Non-exhaustive list for implementers:

- **snake_case** for file paths and identifiers in planning output  
- **Append-only language** in guidance tone  
- **≥12** distinct spec bullets when blueprinting; **C4** mandatory from phase-01 in v21 narrative  
- **Multi-CLI:** assign an adapter for generation tasks; Arabic → **qwen** + Law 151 anonymisation  
- **No blocking Omega Relay** assumption (≤1s timeout, non-fatal)  
- **Canonical mirror discipline** after editing `guide.md`  
- **Tripartite SDD labels** when producing planning output: `development:`, `content:`, `social:`  

---

## 6. Agents (T0 / routed)

| Agent file | Tier | Relationship to `/guide` |
|------------|------|----------------------------|
| **`.ai/agents/core/antigravity.md`** | T0 | **Primary owner** of `/guide` behavior; Humanization **v3.5**; Guardian + Teacher + SDD overseer; **creative** vs **instructor** vs **planning** paths; skills `guide_instructor_domains`, `guide_teaching`, `guide_sdd_mastery`; optional subagents `guide_teacher`, `guide_sdd_guardian`, `guide_instructor`. |
| **`.ai/agents/core/master_guide.md`** | T0 | Strategic oversight; `/guide brainstorm` (without `about`) routes here per command spec. |
| **Healing / chaos / dashboard** | T1/T0 per `AGENTS.md` registry | Named targets for `/guide heal`, `/guide chaos`, `/guide dashboard` (behavior defined at orchestration layer; not re-specified in this doc). |
| **`recursive_engine`** | Scientist role in `AGENTS.md` | Associated with `/guide learn` in product narrative. |

**Factory mirrors:** e.g. `factory/library/agents/workspace_imports/ai/agents/core/antigravity.md` may exist from industrial sync — treat **`.ai/agents/core/`** as the human-edited source unless your pipeline says otherwise.

**Separate command family:** **`.ai/rules/antigravity.md`** documents **`/antigravity`** (`status`, `sync`, `learn`) — related branding, **not** the same as `/guide`.

---

## 7. Subagents

| Path | Role |
|------|------|
| **`.ai/subagents/guide_instructor.md`** | **T1** domain-grounded deep lessons. |
| **`.ai/subagents/guide_teacher.md`** | **T1** syllabus-scale **Master Teacher** (layered pedagogy). |
| **`.ai/subagents/guide_sdd_guardian.md`** | **T1** SDD / density / gate **audits**. |

Optional sync to IDE: `sync_ide_triple_layer.sh --with-subagents`.

---

## 8. Skills

### 8.1 First-class `/guide` support skills (`.ai/skills/`)

| Skill folder | Purpose |
|--------------|---------|
| **`.ai/skills/guide_instructor_domains/skill.md`** | Domain → repo anchor map for **instructor mode**; spelling (Vercel, GitHub). |
| **`.ai/skills/guide_teaching/skill.md`** | Layered L0–L3 teaching, ESL-friendly habits. |
| **`.ai/skills/guide_sdd_mastery/skill.md`** | SDD vocabulary, density gate, C4, manifests. |

### 8.2 Triggers elsewhere

| Reference | Note |
|-----------|------|
| **`.ai/skills/factory_library_pillars/skill.md`** | Lists `"/guide learn"` among triggers for pillar work — coupling between factory library evolution and `/guide learn`. |

### 8.3 Official / external “Antigravity” skills (library)

Blueprints under `factory/library/archive/legacy_pillars/.../antigravity_awesome*` — **external** skill packs; not the same as the **Antigravity persona** spec. Include in audits so naming does not confuse contributors.

---

## 9. Routing and machine-readable bindings

### 9.1 `.ai/registry/routing/command_routing.json`

**`commands`** entries include discrete **`guide_*`** pattern groups, for example:

- `guide_plan_status`, `guide_plan_type`  
- `guide_brainstorm_about`, `guide_brainstorm`  
- `guide_spec`, `guide_gate`, `guide_adapter`  
- `guide_learn`, `guide_tutor`  
- `guide_heal_chaos_dashboard`  
- `guide_mode`, `guide_creativity`, `guide_memory`  
- `guide_help_ping`  
- `guide_root` — pattern `^/guide$` only  

Each entry has `ranking`, `fallback_policy`, `confidence_threshold` for multi-CLI tool routing.

### 9.2 Gap analysis (useful for improvement planning)

As of the routing slice above:

- There is **no** dedicated regex id for `/guide explain …` or `/guide understand …` (instructor aliases rely on model behavior + slash body).  
- There is **no** catch-all pattern for `/guide <arbitrary natural language>` — free-text instructor mode is specified in **markdown** for the LLM, not encoded as a single routing row.  
- **`guide_root`** only matches bare `/guide`; partial trees may classify unknown tails differently depending on tool-router version.

**Improvement idea:** add `guide_instructor` pattern `^/guide (.+)$` with lower priority than specific subcommands, or explicit `explain` / `understand` rows.

### 9.3 Other registries

| File | Relevance |
|------|-----------|
| **`.ai/registry/command_bindings.registry.json`** | `_meta.owner` = `guide-agent`; bindings for many commands — inspect when wiring automation. |
| **`.ai/registry/tool_registry.json`** | `antigravity` tool + adapter file path. |
| **`.ai/memory/skill_memory/v7_command_system_manifest.json`** | Lists T0 agents including `master_guide`, `healing_bot_v2`, `recursive_engine`, `chaos_validator`. |

---

## 10. Workspace artifacts referencing `/guide`

Examples (non-canonical; may lag):

- **`.ai/workspace/05_memory_state/phase_1_status.json`** — `command_router` → `.ai/commands/commands.md`  
- **`.ai/workspace/08_testing/tests/day_3_tool_router_tests.json`** — dependencies include command docs  
- **`.ai/workspace/09_logs_reports/milestones/phase_1_dashboard.html`** — narrative diagram mentions command lookup  

Use these for **QA narratives**, not behavioral truth.

---

## 11. AGENTS.md “Learned” facts (durable, human-approved)

The workspace **`AGENTS.md`** may contain bullets such as:

- `/guide` instructor mode and domain map locations  
- Continual-learning index path (local-only under `.cursor/`)  
- Canonical + mirror edit order for `guide.md`  

When improving `/guide`, decide whether new stable facts belong in **`AGENTS.md`** vs a **skill** under `.ai/skills/`.

---

## 12. Operational: editing and verifying

1. Edit **`.ai/commands/guide.md`**.  
2. `cp` to **`factory/library/commands/guide.md`** and IDE copies **or** run:  
   `bash factory/scripts/core/sync_ide_triple_layer.sh`  
3. Optionally run **`python3 factory/scripts/core/industrial_mirror_sync.py`** (invoked at end of sync script when present).  
4. Run validation rows in **`guide.md`** (“VALIDATION SUITE”) — `/guide ping`, instructor smoke, footer pairing, etc.  
5. Append traceability to **`.ai/logs/ledgers/evolution_ledger.jsonl`** when your process requires it (existing repo pattern).

---

## 13. Improvement backlog seeds (for planning AI)

Use as a checklist; prioritize with product owner.

| ID | Theme | Observation |
|----|--------|----------------|
| B1 | **Routing parity** | Instructor + NL `/guide …` not fully expressed in `command_routing.json`. |
| B2 | **Naming collision** | `factory/library/subcommands/guide.md` vs Antigravity `/guide` — rename or cross-link to reduce onboarding risk. |
| B3 | **Test harness** | Add automated tests that `guide.md` frontmatter keys exist and mirror files match hash or mtime. |
| B4 | **Memory** | `/guide memory:*` is session-scoped in spec — clarify if any hook persists data and align with privacy story. |
| B5 | **Agent wiring** | Docs promise routes to `heal` / `chaos` / `dashboard` / `master_guide`; verify orchestrator actually dispatches on those strings. |
| B6 | **v21 plan status** | `/guide plan status` depends on `.ai/plan/_manifest.yaml` — document required schema and failure UX when missing. |
| B7 | **Density gate** | `/guide gate` references `factory/scripts/core/spec_density_gate_v2.py` — keep path and CLI flags in sync with script. |
| B8 | **Footer fatigue** | Global footer on every reply may conflict with “answer only” UX — evaluate rule granularity. |

---

## 14. Quick copy block for external AI system prompt

```text
You are helping improve the AIWF /guide slash command.
Canonical behavior: .ai/commands/guide.md (Humanization v3.5).
Persona agent: .ai/agents/core/antigravity.md (v2.2.0).
Skills: .ai/skills/guide_instructor_domains/, guide_teaching/, guide_sdd_mastery/.
Optional subagents: guide_teacher.md, guide_sdd_guardian.md, guide_instructor.md.
Response body rule: .cursor/rules/guide-response-style.mdc.
Global reply footer rule: .cursor/rules/guide-handoff-footer.mdc (alwaysApply).
Sync commands: bash factory/scripts/core/sync_ide_triple_layer.sh
Do not confuse with factory/library/subcommands/guide.md (different Guide workflow).
Routing patterns: .ai/registry/routing/command_routing.json (guide_* keys).
Known gap: free-text /guide instructor mode is LLM-specified; routing JSON may not list a catch-all pattern.
```

---

## 15. Changelog (this doc)

| Date | Change |
|------|--------|
| 2026-05-02 | Initial comprehensive context doc for `/guide` and related artifacts. |

---

*Governor: Dorgham | AIWF | Reasoning Hash: sha256:docs-context-guide-command-comprehensive-2026-05-02*
