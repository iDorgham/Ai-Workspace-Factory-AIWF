# Sovereign Workspace — Documentation Hub

**Workspace Organization:** Categorized by function and operational phase

This folder contains all system documentation, configuration, and reference materials for the Sovereign Universal AI Workspace v3.2-Phase1.3a.

---

## Source of truth

- **Runtime contracts, command routing, adapters, memory:** repository **`.ai/`** at the repo root (for example `.ai/agents.md`, `.ai/commands-multi-tool.md`, `.ai/cli-layer/`, `.ai/tool-adapters/`, `.ai/memory/state.json`).
- **`.ai/workspace/`:** curated docs, templates, QA assets, and phase write-ups. Not every numbered “virtual” section exists as a subfolder here; when in doubt, follow the paths below or open `.ai/`.
- **Operational JSON / JSONL logs:** **`.ai/logs/`** (append-only audit trails, test exports, path-integrity reports).
- **Active content projects:** [`content/README.md`](../../content/README.md) (canonical `content/<slug>/` list and `active_project` values).
- **HTML quick guide (browser):** [`docs/workspace-user-guide/index.html`](../../docs/workspace-user-guide/index.html) — overview, full command routing table, CLI flags, and local verification (open the file locally; uses `assets/guide.css` beside it).

### Cleanup policy (hygiene vs triage)

- **Safe to delete anytime:** editor/OS cruft (`.DS_Store`, `__pycache__/`, `*.pyc`) — covered by root `.gitignore`; remove if committed by mistake.
- **Do not delete as “junk”:** append-only logs under `.ai/logs/` (for example `workflow.jsonl`, `tool-performance.jsonl`, scrape/sync traces) unless you adopt an explicit retention or rotation policy.
- **Review before delete or move:** generated test exports (`day-*-test-results.json`), migration report JSON/MD under `.ai/migrations/` (regenerate from the `.py` check scripts), and historical narrative under `archive/legacy-snapshots/` (formerly `.ai/workspace/09-logs-reports/legacy-snapshots/`).
- **Inventory:** run `python3 .ai/scripts/workspace_inventory.py` → `.ai/logs/workspace-cleanup-inventory.md`.

---

## Local verification (no CI)

From the repository root:

```bash
python3 .ai/scripts/audit_path_integrity.py
python3 .ai/scripts/audit-workspace-integrity.py
python3 .ai/scripts/check_mirror_drift.py
python3 .ai/scripts/workspace_health.py
python3 .ai/scripts/docs_quality_gate.py
python3 .ai/scripts/test-flag-parser.py
python3 .ai/scripts/test-tool-router.py
python3 .ai/scripts/run-smoke-tests.py
python3 .ai/scripts/workspace_inventory.py
```

`audit_path_integrity.py` regenerates `.ai/logs/path-integrity-summary.md` after each run (keeps it newer than `path-integrity-report.json` for `audit-workspace-integrity.py`).

---

## 📚 Folder Structure

### 🏗️ **01-system-architecture/** 
Core system design and strategy documents
- `ARCHITECTURE-v3.2-AGENT-CLARITY.md` — System design principles
- `PHASE-1-VISUAL-ARCHITECTURE.md` — Architecture diagrams and visual flow
- `IMPLEMENTATION-ROADMAP-v3.2.md` — Development timeline and milestones
- `v3.1-vs-v3.2-SUMMARY.md` — Version comparison and upgrade path

**When to use:** Understanding overall system design, comparing versions, reviewing architecture decisions.

---

### 🤖 **Agent contracts (canonical: `.ai/`)**
Agent definitions, responsibilities, and data governance live under **`.ai/`** (not duplicated under `.ai/workspace/`). Start with `.ai/agents.md`, `.ai/data-ownership-multi-tool.md`, and `.ai/error-recovery.md`.

**When to use:** Determining agent responsibilities, checking permissions, understanding data flows.

---

### ⚙️ **03-cli-layer/** (documentation in `.ai/workspace/`)
CLI design notes that accompany the live implementation in **`.ai/cli-layer/`**.
- `CLI-LAYER-IMPLEMENTATION-GUIDE.md` — Phase 2a implementation details
- `CLI-LAYER-VISUAL-DESIGN.md` — CLI flag design specifications

**When to use:** Understanding CLI design; for live flag/router/error templates, read `.ai/cli-layer/`.

---

### 🔌 **Tool adapters (canonical: `.ai/tool-adapters/`)**
Canonical adapter contracts, registry JSON, and routing markdown live under **`.ai/tool-adapters/`** (interface, per-tool adapters, fallback routing).

**When to use:** Adding or debugging tools — edit and review files in `.ai/tool-adapters/`, not under `.ai/workspace/`.

---

### 💾 **05-memory-state/** (snapshot + live state)
- **`.ai/workspace/05-memory-state/phase-1-status.json`** — Phase 1 activation snapshot for docs
- **Live session state:** `.ai/memory/state.json`

**When to use:** Historical phase status here; current pipeline position in `.ai/memory/state.json`.

---

### 🎨 **06-brand-reference/**
Sovereign brand identity and market positioning
- `market-positioning.md` — Studio niche, target clients, unique selling propositions
- `06-brand-reference/content/sovereign/reference/brand-voice/style-rules.md` — Writing tone and voice guidelines
- `06-brand-reference/content/sovereign/reference/brand-voice/glossary.md` — Approved terminology and prohibited terms
- `06-brand-reference/content/sovereign/reference/brand-voice/tone-examples.md` — Voice examples by context
- `06-brand-reference/content/sovereign/reference/brand-voice/voice-refinement.md` — Brand voice analysis and evolution
- `brand-discovery.md` — Brand discovery process and framework

**When to use:** Creating content, checking tone consistency, understanding brand positioning.

**⚠️ Note:** Fill in `market-positioning.md` before first use.

---

### 📋 **Content templates (canonical: `.ai/templates/`)**
Content blueprints and export schemas
- `.ai/templates/content-blueprints/` — Reusable content templates (`blog-post.md`, `website-page.md`, `project-page.md`, `landing-page.md`)
- `.ai/templates/seo-meta-templates/` — SEO metadata schemas (`meta-template.json`)
- `.ai/templates/csv-schemas/` — Data export formats (`content-export.json`)
- `.ai/templates/brand-discovery/` — Brand discovery questionnaire (`questions.json`)

**When to use:** Starting new content, standardizing content format, preparing exports. Stub: `.ai/workspace/07-content-templates/README.md`.

---

### 🧪 **08-testing/**
Test cases and quality assurance
- `08-testing/tests/day-2-flag-parser-tests.json` — CLI flag parsing tests (10/10 ✅)
- `08-testing/tests/day-3-tool-router-tests.json` — Tool routing tests (12/12 ✅)
- `08-testing/tests/day-4-smoke-tests.json` — Integration smoke tests (10/10 ✅)
- `08-testing/tests/day-5-*-adapter-tests.json` — Per-tool adapter tests
- `TASK-5-*-SPEC.md` — Adapter specification documents (Markdown in `08-testing/`)

**When to use:** Verifying system integrity, running quality gates, validating changes.

---

### 📊 **09-logs-reports/**
Phase write-ups, guides, milestone notes, and **legacy snapshots** of day-level exports.
- Top-level `*.md` — Phase status, integration plans, day guides
- `legacy-snapshots/` — Stub pointer only; historical files live under **`archive/legacy-snapshots/`** at the repo root (see `legacy-snapshots/README.md` there).
- `milestones/` — Short “ready” notes and HTML snapshots

**Canonical operational logs** → `.ai/logs/`.

**When to use:** Reviewing progress, reading phase narratives; use `.ai/logs/` for live audit trails.

---

### 📦 **10-archive/**
Historical data and previous versions
- `previous-versions/` — v3.2.0 legacy files
  - `commands_v3.2.0.md`
  - `data-ownership_v3.2.0.md`
- `archive-index.json` — Archived competitor data

**When to use:** Comparing old versions, recovering historical data, understanding evolution.

---

### 🚀 **_setup-guides/** (Priority)
Quick-start and implementation guides
- `IMPLEMENTATION-CHECKLIST.md` — Phase activation checklist
- `PHASE-1-SETUP-GUIDE.md` — Multi-tool orchestration setup
- `GUIDE-AGENT-SYSTEM-PROMPT-ADDENDUM.md` — System prompt extensions
- `GUIDE-AGENT-SYSTEM-PROMPT-ADDENDUM-PHASE2A.md` — CLI layer system prompt

**When to use:** Setting up a new workspace, integrating new tools, onboarding.

---

### 📌 **_quick-reference/** (Priority)
Cheat sheets and quick lookups
- `QUICK-REFERENCE.md` — Command cheat sheet
- `PHASE-1-ARCHITECTURE-SUMMARY.md` — Phase 1 overview
- `commands.md` — v3.2 command reference (backward compatibility)
- `skill-integration.md` — Cowork skill mappings

**When to use:** Looking up command syntax, finding quick answers, navigating features.

---

## 🎯 Quick Navigation

**I need to…**

| Task | Folder | File |
|------|--------|------|
| Understand system design | `01-system-architecture/` | `ARCHITECTURE-v3.2-AGENT-CLARITY.md` |
| Check who owns a file | `.ai/` | `data-ownership.md` or `data-ownership-multi-tool.md` |
| Execute a command with flags | `.ai/cli-layer/` + `.ai/workspace/03-cli-layer/` | live templates in `.ai/cli-layer/` |
| Add a new tool | `.ai/tool-adapters/` | `interface.json` + new adapter |
| Check session state | `.ai/memory/` | `state.json` |
| Write brand-consistent content | `06-brand-reference/` | `content/sovereign/reference/brand-voice/style-rules.md` |
| Create new content | `.ai/templates/` | `content-blueprints/*.md` |
| Run tests | `08-testing/tests/` | `day-*-*-tests.json` |
| Review what was done | `09-logs-reports/` + `.ai/logs/` | phase docs here; live logs in `.ai/logs/` |
| Compare old versions | `10-archive/` | `previous-versions/` |
| Set up workspace | `_setup-guides/` | `IMPLEMENTATION-CHECKLIST.md` |
| Find a command | `_quick-reference/` | `QUICK-REFERENCE.md` |

---

## 📖 Entry Points

**Starting a new session?** → Read `_setup-guides/IMPLEMENTATION-CHECKLIST.md`

**Need a quick command?** → See `_quick-reference/QUICK-REFERENCE.md`

**Investigating a design decision?** → Check `01-system-architecture/ARCHITECTURE-v3.2-AGENT-CLARITY.md`

**Debugging a tool issue?** → Review `.ai/tool-adapters/` (registry + relevant adapter)

**Checking permissions?** → See `.ai/data-ownership-multi-tool.md`

---

## 🔄 Workflow Integration

These docs support the Sovereign content pipeline:

**Research** → **Scrape** → **Create** → **Polish** → **Review** → **Approve** → **Export**

See `.ai/templates/` for blueprints and `06-brand-reference/` for tone/positioning guidance at each stage.

---

## 📝 Notes

- All files follow semantic versioning (v3.2.0-Phase1.3a)
- Multi-tool support is Phase 1 ✅ (complete as of 2026-04-13)
- CLI layer (Phase 2a) is complete ✅
- Testing coverage: 32/32 tests passing (100%)
- Last updated: 2026-04-13

---

**Questions?** See `_quick-reference/QUICK-REFERENCE.md` for the command reference or check the specific folder README below.
