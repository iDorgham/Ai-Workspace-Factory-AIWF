---
type: Generic
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# 🏭 AIWF v7.0.0 — Complete Command System Guide
**Workspace Guide** | Auto-provisioned to `docs/00-guides/`
*Last updated: 2026-04-23 | Version: 7.0.0*

---

## What is AIWF?

The **AI Workspace Factory (AIWF)** is a sovereign, spec-driven development system. It turns your raw ideas into production-ready digital products using a structured, traceable workflow governed by AI agents working together.

Think of it as a **factory floor**:
- You give it an idea → it produces a spec → agents build it → tests validate it → you deploy it.
- Every step is logged, versioned, and reversible.

---

## The 6-Step Workflow

```
1. IDEA           →  /do "your idea"
2. PLAN           →  /plan
3. BUILD          →  /dev --phase=1
4. TEST           →  /test --phase=1
5. FIX (if needed)→  /fix
6. DEPLOY         →  /deploy --preview
```

---

## Command Reference

### `/do "idea or description"` — Idea to PRD
**What it does**: Transforms a raw idea into a structured Product Requirements Document (PRD) with requirement IDs (REQ-001, REQ-002...) and acceptance criteria.

**Usage:**
```
/do "build a hotel booking platform for Red Sea resorts"
/do "create an invoice management system" --region=egypt
/do --from=existing-prd.md --region=mena
```

**Outputs:**
- `docs/01-plans/{date}_{slug}_prd.md` — Your PRD
- `plan/00-prd/requirements-trace.json` — REQ-ID trace skeleton

**Tips:**
- Be specific. "Hotel booking" → better. "App" → too vague (will ask clarifying questions).
- Add `--region=egypt|redsea|mena` if your project targets MENA markets.

---

### `/plan` — Generate Full SDD Blueprint
**What it does**: Reads your PRD and generates the complete technical specification package — architecture, database schema, contracts, task graph, and validation reports.

**Usage:**
```
/plan
/plan --from=plan/00-prd/prd.md --region=redsea
/plan --phase=1 --validate-only
/plan --dry-run
```

**Outputs (auto-routed to docs/):**
- `docs/02-specs/{date}_{slug}_spec.md` — Human spec narrative
- `docs/03-architecture/{date}_{slug}_design.md` — Mermaid architecture
- `docs/03-architecture/{date}_{slug}_db-schema.sql` — Database schema
- `docs/04-contracts/{date}_{slug}_api-contract.yaml` — API contract
- `docs/05-reports/{date}_{slug}_spec-lint-report.md` — Validation

**Validation gates run automatically:**
- spec-lint (all fields populated)
- contract-check (all acceptance criteria have test fixtures)
- trace-matrix (all REQ-IDs traced)
- regional-compliance (if `--region` active)

> ⚠️ `/dev` cannot run until all gates pass.

---

### `/dev --phase=N` — Build It
**What it does**: Implements the code for a specific phase using Library-First composition. Automatically creates a Git branch, makes traceable commits, and pushes to remote.

**Usage:**
```
/dev --phase=1
/dev --phase=2 --auto-fix
/dev --phase=1 --auto-merge --region=redsea
```

**Git automation (silent):**
- Creates branch: `phase/1-{slug}`
- Commits with format: `feat({slug}): description #sdd-trace:REQ-001`
- Auto-merge to main ONLY if all 5 gates pass

**Blocked if:**
- `spec.yaml` not approved (`Dorgham-Approved`)
- Contract Guardian reports failures
- Spec-lint not at 100%

---

### `/test --phase=N` — Validate
**What it does**: Runs all unit, integration, contract, and regional tests. Generates a coverage report.

**Usage:**
```
/test --phase=1
/test --phase=1 --region=egypt
/test --phase=1 --stress
```

**Outputs:**
- `docs/05-reports/{date}_{slug}_contract-coverage.json`
- `docs/05-reports/{date}_{slug}_trace-matrix.json`

**Required for auto-merge:** ≥100% contract coverage on all `contract_gate: true` items.

---

### `/fix [target]` — Diagnose & Repair
**What it does**: Identifies failures, maps them to spec.yaml acceptance criteria, and proposes patches. Healing Bot v2 can auto-apply safe fixes.

**Usage:**
```
/fix last
/fix --auto-fix
/fix contracts
/fix --spec-sync
```

**Options:**
- `--auto-fix` → Let Healing Bot v2 apply safe patches automatically
- `--spec-sync` → Realign implementation with spec if they've drifted
- `contracts` → Re-validate all contract fixtures

---

### `/db` — Database Design
**What it does**: Designs your database schema, generates SQL migrations, seeds, and ERD diagrams.

**Usage:**
```
/db
/db --phase=1 --dry-run
/db --region=egypt
```

**Outputs:**
- `docs/03-architecture/{date}_{slug}_db-schema.sql`
- `docs/03-architecture/{date}_{slug}_db-erd.md`

**Regional note:** When `--region=egypt`, applies Law 151/2020 data residency rules to schema design.

---

### `/git` — Git Control
**What it does**: Full manual control over Git operations and automation toggles.

**Usage:**
```
/git status
/git commit -m "my message"
/git push
/git auto on          ← enable silent automation
/git merge-auto off   ← disable auto-merge
```

---

### `/deploy` — Deploy to Vercel ⚠️ EXPLICIT ONLY
**What it does**: Deploys your workspace to Vercel. **This command NEVER runs automatically** — you must always invoke it explicitly.

**Usage:**
```
/deploy --preview
/deploy --prod --confirm
/deploy --dry-run
/deploy status
/deploy --prod --region=mena --silent
```

**Flow:** Vercel CLI check → project link → env pull → build → deploy → log to `docs/06-releases/`

> Git auto-merge does **NOT** trigger deployment. Always separate.

---

### `/brainstorm` — Ideation & Regional Optimization
**What it does**: Generates structured proposals for new features, regional adaptations, or skill improvements. Produces copyable spec snippets.

**Usage:**
```
/brainstorm --idea
/brainstorm --region=redsea
/brainstorm --skill=redsea-tourism-booking --region=redsea
/brainstorm --spec=01-hotel-booking
```

---

### `/tutorial` — Interactive Learning Mode
**What it does**: Launches step-by-step instructor mode. Walks you through the entire AIWF workflow with explanations, examples, and checkpoints.

**Usage:**
```
/tutorial
/tutorial --start=do
/tutorial --from=step-3
```

---

## Global Flags

These flags work on **every command**:

| Flag | Effect |
| :--- | :--- |
| `--dry-run` | Simulate without writing files |
| `--region=egypt\|redsea\|mena` | Activate MENA regional engine |
| `--validate` | Run gates only, no execution |
| `--auto-fix` | Let Healing Bot v2 fix issues |
| `--silent` | Minimal output |
| `--phase=N` | Target a specific phase |
| `--verbose` | Maximum detail for debugging |

---

## Docs Naming Convention

All generated documents follow:
```
docs/{category}/{YYYY-MM-DD}_{phase-slug}_{type}.{ext}
```

Example:
```
docs/02-specs/2026-04-23_01-hotel-booking_spec.md
docs/05-reports/2026-04-23_01-hotel-booking_contract-coverage.json
```

---

## Governance Quick Reference

| Rule | What It Means |
| :--- | :--- |
| **Omega Gate v2** | Structural changes need `Dorgham-Approval` |
| **Spec-First** | `/dev` blocked until spec is approved |
| **Library-First** | Reuse from `factory/library/` before building new |
| **Explicit Deploy** | `/deploy` = you run it manually, always |
| **5-Gate Auto-Merge** | Tests + Coverage + Approval + Regional + No Mutations |
| **Append-Only Logs** | No log entries are ever deleted |

---

## The Guide Section (End of Every Response)

Every AI response ends with:
```
Guide:
✅ Done: [What was accomplished]
📚 Learn: [Key concept explained]
▶️ Next: [1-3 next actions]
💡 Suggest: [Optional proactive idea]
```

This is mandatory — it ensures you always know what happened, why, and what to do next.

---

## Quick Start Example (Red Sea Tourism App)

```bash
# 1. Describe your idea
/do "hotel and dive center booking platform for Red Sea resorts" --region=redsea

# 2. Generate the full technical plan
/plan --from=plan/00-prd/prd.md --region=redsea

# 3. Build phase 1
/dev --phase=1 --region=redsea

# 4. Run tests
/test --phase=1 --region=redsea

# 5. Deploy to preview for review
/deploy --preview --region=redsea

# 6. Deploy to production when ready
/deploy --prod --confirm --region=redsea
```

---

> 💡 **Run `/tutorial` for an interactive walkthrough** — the instructor will guide you step by step through your first project from idea to deployment.

---

*AIWF-Guide.md | Version 7.0.0 | docs/00-guides/*
*Auto-provisioned by Factory Scaffolder (T2-001)*
