---
type: Command
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---


# /plan — Feature & Sprint Planning

## Syntax
```
/plan [phase]/[spec]             → SDD default: phase + spec slug (e.g. 01-auth/01-login) — triggers SOS after confirmation
/plan [feature-name] --legacy    → Flat single-file or legacy package under features/[name] (see below)
/plan [phase]/[spec] [--no-contract] [--dry-run-plan] [--no-sos] [--founder]
/plan sprint [N]                 → Plan sprint N
/plan roadmap                    → Create or update product roadmap
/plan backlog                    → Review and prioritize backlog
/plan --founder                  → Force Founder mode (non-technical flow)
/plan --no-sos                   → Skip SOS / prompt.md generation after spec files are written

/plan sos [phase]/[spec]         → Full SOS pass for that spec (manifest + prompt.md)
/plan sos --refresh [phase]/[spec] → Regenerate prompt.md only (re-runs compression + gate map)
/plan sos prompt [phase]/[spec]   → Print execution-ready body of prompt.md (or task slice if split)
/plan sos status [phase]/[spec]   → Orchestration view (phase manifest + gate readiness)
```

## Spec-Driven Development (SDD) — default

Every **`/plan [phase]/[spec]`** run produces (or updates) a **spec folder** whose **`plan.md`** MUST include:

| Section | Purpose |
|--------|---------|
| **User Story** | Who, what, why — plain language |
| **Acceptance Criteria** | Numbered, **testable** statements; each gets an **AC ID** (e.g. `AC-01`) for traceability |
| **Data Shape** | **Plain language only** — fields, types in words, required/optional; feeds `@ContractLock` auto-Zod |
| **Test Scenarios** | Scenarios aligned to AC IDs (Given/When/Then or concise bullets) |
| **Edge Cases** | Boundary conditions and failure modes |

**Post-confirmation hook (automatic):** After the user confirms the spec (Founder: proceed; Pro: explicit approval):

1. **`spec:validate`** — `@Architect` + `@QA` confirm AC completeness and testability; vague specs → clarification loop (no Zod write).  
2. **`contract:auto-generate`** — `@ContractLock` (+ `@Architect` on ambiguity) parses **Data Shape** → updates **`contracts.md`** in the spec folder and syncs Zod to `packages/shared/src/contracts/`.  
3. **`contract:auto-validate`** — validate syntax, SHA-256 lock in **`.contract-locks.json`**, confirm alignment with **`plan.md`** + **`contracts.md`**.  
4. **SOS** — `@Router` runs SOS-1…7 → updates **`.ai/plans/active/features/[phase]/manifest.md`**; writes **`prompt.md`** inside the spec folder; optional **`[spec]/sos/`** only when runtime hooks apply (not the default SDD layout).  
5. **`/build`** — only after pre-flight + **`prompt.md`** (unless **`--no-sos`**) align with gates.

**Founder flow:** Never ask the user to write Zod. After confirmation, technical steps (Zod + SOS) run **without** exposing schema syntax to the user.

### Exploration flags (`--no-contract`, `--dry-run-plan`)

| Flag | Behavior |
|------|----------|
| `--no-contract` | **Planning-only escape hatch:** does **not** require existing locked contracts before **drafting** the feature plan. Emits a **CRITICAL** reminder: `/build` and execution swarms stay **blocked** until **`spec:validate`** + **`contract:auto-generate`** + **`contract:auto-validate`** complete for every touched domain (normally automatic after spec confirmation). Violates default SDD flow — use for discovery, spikes, or rehearsal. |
| `--dry-run-plan` | **Read-only rehearsal:** prints the intended **phase/spec** tree, task tier sketch, and agent assignments **without** writing spec files, **`prompt.md`**, phase **`manifest.md`**, or sprint mutations. Optional: one line to `command-logs` if policy requires rehearsal traceability. |
| `--legacy` | Use **flat** layout: **`.ai/plans/active/features/[name].md`** (and optional legacy package / `sos/` beside it) instead of **`[phase]/[spec]/`**. |

**Combined:** `/plan 01-auth/01-login --no-contract --dry-run-plan` → show intended layout; **no** writes under **`.ai/plans/active/features/`**.

**Compatibility:** `--dry-run-plan` implies `--no-sos` for outputs (nothing generated). If `--no-sos` is also passed explicitly, behavior is unchanged.

### Runtime execution hooks (optional)

When present on the feature package, **@RuntimeOrchestrator** and `/swarm --live` consume these fields (filesystem-only; no services).

Store in **spec folder** **`context.md`** frontmatter **or** a dedicated **`runtime.yaml`** beside **`plan.md`** (path: **`.ai/plans/active/features/[phase]/[spec]/`**):

```yaml
runtime_enabled: false        # true → expect /swarm --live behavior + sos/runtime_state.md updates
feedback_interval: task       # task | manual — task = poll after each task; manual = only /swarm monitor
state_tracking: manifest      # manifest | full — manifest = tiers from sos/manifest.md; full = also mirror gate_cursor in runtime-state
```

| Field | Type | Purpose |
|-------|------|---------|
| `runtime_enabled` | boolean | If `true`, feature expects adaptive loop; initialize `sos/runtime_state.md` on first `/swarm run --live`. |
| `feedback_interval` | `task` \| `manual` | When to re-read state: after each completed task vs. only on explicit `/swarm monitor`. |
| `state_tracking` | `manifest` \| `full` | `manifest` syncs task rows from **phase `manifest.md`** only; `full` also tracks sequential gate progression in runtime state. |

**Traceability:** When runtime hooks are set, log the values to `.ai/plans/active/audit/command-logs/[YYYY-MM-DD].md` on first swarm start for that feature.

## Primary Agents
- Founder mode: `@Founder` (interface) → `@Architect` (technical plan) → `@Guide` (sprint integration) → `@Router` (SOS)
- Pro mode: `@Architect` + `@Guide` directly → `@Router` (SOS)

---

## Feature Planning Flow (Founder Mode)

### Interactive 5-Step Flow
```
Step 1: @Founder → "What's the name of the feature?"
Step 2: @Founder → "Who uses it and what do they want to accomplish?"
Step 3: @Founder → "How will we know it's working? (3-5 success statements)"
Step 4: @Founder → "How important is this? What business value does it add?"
Step 5: @Founder → Summary + confirmation → "Shall I proceed?"

On confirmation:
→ @Architect finalizes **spec sections** in `plan.md` (hidden technical annotations optional; User Story + AC + Data Shape + Edge Cases stay plain language)
→ **Silent pre-SOS:** **`spec:validate`** → **`contract:auto-generate`** → **`contract:auto-validate`** (no manual `@ContractLock` steps in Founder mode)
→ @Guide adds to sprint
→ @RiskAgent scores risks
→ @Router runs **SOS-1…7** (see below) → phase **`manifest.md`** + spec **`prompt.md`** (**Spec ID**, **Linked AC**, **Contract ref**, gates)
→ @Tutor explains what was planned (Founder: business language)
```

## Feature Planning Flow (Pro Mode)

### Direct Technical Plan
```
/plan booking-flow

→ @Architect generates:
  - User story + acceptance criteria (testable; AC IDs)
  - Data Shape (plain language) + Edge Cases + Test Scenarios
  - Task breakdown (D-CDD adapted: SPEC→CONTRACT(auto)→STUB→TEST→IMPLEMENT)
  - Risk assessment (5×5 matrix)
  - Definition of Done
  - Platform adaptation notes (RTL, a11y, i18n)

→ @Guide integrates into current sprint
→ **Silent pre-SOS:** **`spec:validate`** → **`contract:auto-generate`** → **`contract:auto-validate`**
→ @RiskAgent adds to risk register
→ @Router runs **SOS-1…7** → phase **`manifest.md`** + spec **`prompt.md`**
```

---

## 📁 SDD folder structure & output routing

- **`/plan [phase]/[spec]`** creates: **`.ai/plans/active/features/[01-phase]/[01-spec]/`**
- On spec confirmation, auto-materialize **seven** planning files from **`.ai/templates/sdd-spec/`** (`plan.md`, `design.md`, `context.md`, `api.md`, `database.md`, `contracts.md`, `structure.md`), then run the **silent pre-flight** (see **Post-confirmation hook** above).
- **`contracts.md`** is auto-filled from **Data Shape** → validated → locked; canonical Zod is **synced** to **`packages/shared/src/contracts/[domain].ts`** (domain may differ from spec slug — record both in **`contracts.md`**).
- **SOS** writes **`prompt.md`** directly inside the spec folder (replaces scattered **`sos/prompts/`** for SDD default).
- **Phase-level manifest:** **`.ai/plans/active/features/[01-phase]/manifest.md`** — dependency graph across specs in that phase, parallel tiers, gate status.
- **Optional legacy:** per-spec **`[spec]/sos/`** (e.g. `runtime_state.md`) only when runtime hooks are enabled — do **not** create a repo-root **`sos/`** unless explicitly required.

**`--no-sos`:** writes / refreshes the **seven** template files + pre-flight through **`contract:auto-validate`** as policy allows, but **skips** **`prompt.md`** generation.

---

## 🔄 SOS integration

**Pre-SOS silent pipeline** (must pass before SOS-1; on failure halt and return **`@Architect`** clarification — do not write **`prompt.md`**):

1. **`spec:validate`**
2. **`contract:auto-generate`**
3. **`contract:auto-validate`**

**SOS-1 to SOS-7** (SDD-optimized outputs):

| Step | Action | Agent(s) | Output |
|------|--------|----------|--------|
| SOS-1 | Parse spec bundle → tasks, AC, data flows | `@Router` + `@Founder` | Task list + AC mapping |
| SOS-2 | Dependency graph + tier groups | `@Router` | Data for phase **`manifest.md`** |
| SOS-3 | Resolve agents per task | `@Router` | Agent matrix |
| SOS-4 | Anti-pattern pre-scan | `@ErrorDetective` | Blocked-pattern notes |
| SOS-5 | Context compression | `@ContextSlicer` | Payload for **`prompt.md`** |
| SOS-6 | Assemble execution prompt | `@Router` | **`prompt.md`** in spec folder |
| SOS-7 | Persist orchestration state | `@Router` | Update **`../manifest.md`** (phase) |

**`prompt.md`** must include: **Spec ID**, **Linked AC**, **Contract ref** (`contracts.md` + `packages/shared/...`), **Test scenarios**, **Gate pipeline**, **Blocked / Unblocks**, **Compressed context**.

### Commands (SOS + plan)

| Command | Behavior |
|---------|----------|
| **`/plan [phase]/[spec]`** | Draft → confirm → silent pre-flight → **seven** spec files → SOS-1…7 → **`prompt.md`** + phase **`manifest.md`** |
| **`/plan [phase]/[spec] --no-sos`** | Same file scaffold + pre-flight as applicable; **skips** **`prompt.md`** |
| **`/plan sos --refresh [phase]/[spec]`** | Regenerate **`prompt.md`** only (re-run SOS-5…6 + manifest touch) |
| **`/plan sos [phase]/[spec]`** | Full SOS pass (all seven steps) |
| **`/plan sos status [phase]/[spec]`** | Read **`manifest.md`** + gate column for that spec |

**`/contract sync [phase]/[spec]`** (see **`.ai/commands/contract.md`**): Re-run **`contract:auto-generate`** + **`contract:auto-validate`** without regenerating **`prompt.md`**.

---

### SOS and /swarm integration

`/swarm run [phase]/[spec]` (or legacy **`[feature-id]`**) should prefer:

- Phase **`manifest.md`** for cross-spec ordering when present
- Spec **`prompt.md`** as the compressed execution brief
- Tier rows in **`manifest.md`** for parallel-safe groups

If **`manifest.md`** / **`prompt.md`** are missing, fall back to **`plan.md`** and warn: *"Run `/plan sos [phase]/[spec]` for optimized execution."*

**Legacy flat package:** If **`sos/manifest.md`** + **`sos/prompts/`** exist under a legacy feature folder, `/swarm` may still consume them; SDD default is **inline** **`prompt.md`**.

---

### SOS re-generation

Run **`/plan sos --refresh [phase]/[spec]`** after AC changes, new tasks, contract domain rename, or anti-pattern updates. **`prompt.md`** is overwritten; **[SDD-STRUCT-02]** — do not hand-edit **`prompt.md`**.

---

## Output — SDD spec package (default)

Canonical path:

```
.ai/plans/active/features/[01-phase-name]/
├── manifest.md
└── [01-spec-name]/
    ├── plan.md
    ├── design.md
    ├── context.md
    ├── api.md
    ├── database.md
    ├── contracts.md
    ├── structure.md
    └── prompt.md              ← SOS output (after confirmation unless --no-sos)
```

Full reference: **`docs/workspace/reference/feature_plan_package_layout.md`**.

**Legacy (`/plan --legacy [name]`):** flat **`.ai/plans/active/features/[name].md`** and/or old **feature-id** package with **`sos/prompts/`** remain supported for migration; new work uses **phase/spec**.

```markdown
# Feature Plan: [Feature Name]

**Project Type:** [web | mobile | etc.]
**Priority:** High / Medium / Low
**Business Impact:** [Short description + expected value]
**Owner:** @Founder (business) / @Guide (execution)
**Created:** YYYY-MM-DD | **Sprint:** N

## User Story
As a [user role],
I want to [action],
so that [benefit].

## Acceptance Criteria (Gherkin)
- Given [context] When [action] Then [expected outcome]
- Given [context] When [action] Then [expected outcome]
- Given [context] When [action] Then [expected outcome]
(minimum 3, maximum 7)

## Contracts Required
- Primary: `packages/shared/src/contracts/[domain].ts` — Status: DRAFT
- Related: [list any others]

## Task Breakdown (D-CDD Sequence)
| ID | Task | Agent | Dependencies | Gate | Status |
|----|------|-------|-------------|------|--------|
| T-001 | Define + lock Zod contract | @Architect | None | Contract compiles | ☐ |
| T-002 | Stub API endpoints | @Backend | T-001 | Types match | ☐ |
| T-003 | Write contract tests | @QA | T-001 | Tests pass | ☐ |
| T-004 | Implement UI components | @Frontend | T-001 | compliance | ☐ |
| T-005 | Implement API logic | @Backend | T-002, T-003 | Integration tests | ☐ |
| T-006 | E2E + visual tests | @QA + @VisualQA | T-004, T-005 | Playwright pass | ☐ |
| T-007 | @Reviewer final review | @Reviewer | T-006 | Approved | ☐ |

## Risk Assessment (5×5)
| Risk | Likelihood | Impact | Score | Mitigation | Owner |
|------|-----------|--------|-------|-----------|-------|

## RTL / i18n / A11y Requirements
- [ ] CSS logical properties in all layout code
- [ ] i18n keys for all UI strings
- [ ] Arabic translations added to messages/ar.json
- [ ] WCAG 2.1 AA on all interactive elements
- [ ] Visual RTL parity tested

## Definition of Done
- [ ] Contract locked + validated
- [ ] Code passes compliance (tokens, a11y, i18n, RTL)
- [ ] Test coverage: Unit 45% + Integration 30% + E2E happy path
- [ ] @Reviewer approved
- [ ] @VisualQA visual regression passed (LTR + RTL)
- [ ] @MetricsAgent baseline updated

**Plan Version:** 1.0 | **Last Updated:** YYYY-MM-DD
```

---

*Invokes: @Founder (founder mode) · @Architect · @Guide · @RiskAgent · @ContractLock · @Router (SOS) · @ContextSlicer (SOS) · @ErrorDetective (SOS anti-pattern scan) · @RuntimeOrchestrator (optional runtime hooks + `/swarm --live` contract)*
