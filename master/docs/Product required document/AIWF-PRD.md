# 📄 AI WORKSPACE FACTORY — PRODUCT REQUIREMENTS DOCUMENT (PRD) v5.0.1

**Document Status:** Hardened Stable Release  
**Version:** 5.0.1  
**Owner:** Dorgham  
**Date:** April 20, 2026  
**Reference Contexts:** `WORKSPACE_MASTER_CONTEXT.md`, `QWEN_CONTEXT.md`  
**Target Execution Environment:** Qwen, Cursor, Claude, Gemini, OpenCode, Kilo  
**Primary Output:** Production-ready multi-purpose sovereign composition engine  

---

## 1. EXECUTIVE SUMMARY

The AI Workspace Factory will transition from a single-pipeline, hardcoded content generator into a **deterministic, multi-purpose composition engine** capable of autonomously generating, orchestrating, and maintaining isolated AI workspaces across 30+ marketing/advertising pipelines. This release (v5.0.1) decouples the legacy Galeria routing, enforces strict metadata/workspace structural separation, deploys a cross-workspace Master Guide with memory aggregation, integrates a Proactive Brainstorm Agent, and replaces static views with a three-tier, lazy-loaded dashboard system. The v5.0.1 update introduces **Industrial Hardening**, including multi-IDE rule mirroring (Cursor, Copilot, Claude, Gemini), cross-platform symlink fallbacks, and strict manifest schema validation. All transformations preserve 100% backward compatibility and execute through a 6-phase gated rollout with automated validation (6/6 smoke tests).

---

## 2. PROBLEM STATEMENT & STRATEGIC IMPERATIVES

| Current Limitation | Business/Technical Impact | v5.0.0 Solution |
|-------------------|--------------------------|----------------|
| Hardcoded `content-machine-editorial` routing | Blocks reuse across non-Galeria verticals; forces manual profile mapping | Deterministic alias resolver mapping 30 simplified pipelines → 29 existing composition profiles |
| Flat `workspaces/<slug>/` hierarchy | Metadata pollution, agent boundary violations, cross-project context bleed | Strict separation: `clients/<slug>/` = metadata only; `001_<slug>/` = sovereign `.ai/` workspaces |
| No cross-project memory or oversight | Redundant work, missed pattern reuse, fragmented strategic insights | Master Guide with root `.ai/` memory layer, `workspace-index.json`, and pattern detection engine |
| Brainstorming requires manual triggers | Missed contextual optimization; high cognitive load | Proactive Mode Brainstorm Agent monitoring 6 contextual triggers, outputting ≤2 suggestions/session |
| Static, token-heavy dashboards | High context waste, poor IDE rendering, sync overhead | Three-tier lazy-loaded widget system with delta-only sync, token budget <5%, archive protocol |
| Library health at 38/100 (integrity) | Dead-weight components dilute composition accuracy | Strict `library-first` enforcement + pre-generation validation against certified component registry |

---

## 3. SCOPE & BOUNDARIES

### ✅ In Scope

- Pipeline alias mapping & deterministic routing in `factory/scripts/compose.py`
- Corrected folder hierarchy (`clients/` vs `001_<slug>/`) with `--structure` validation
- Master Guide root agent + cross-workspace memory aggregation & `/master sync`
- Brainstorm Agent dual-mode (Command + Proactive) with dismissal/accept/refine routing
- Three-tier dashboard recreation (Root → Client → Project) using Widget Spec v2.0
- New CLI commands: `/create-client`, `/create-project`, `/dashboard`
- Legacy workspace migration, governance enforcement, token optimization
- 6-phase execution with deterministic smoke tests & snapshot rollback

### ❌ Out of Scope

- Creating new core library components (strict `library-first` policy per `WORKSPACE_MASTER_CONTEXT.md`)
- Altering the 17-department taxonomy or 29 composition profiles
- Modifying foundational 9-agent tier hierarchy logic or `tool_router_v2.py` architecture
- Building proprietary UI applications outside Markdown/CLI routing
- Changing existing ethical scraping, PII filtering, or ≤15% similarity constraints

---

## 4. CORE ARCHITECTURAL PRINCIPLES & GOVERNANCE

| Principle | Enforcement Rule | Reference |
|-----------|------------------|-----------|
| **Library-First Composition** | All workspaces assemble exclusively from `factory/library/`. New components only if capability missing. | `WORKSPACE_MASTER_CONTEXT.md` §1, §12 |
| **Sovereign Workspace Isolation** | Each `001_<slug>/` contains complete `.ai/` layer. Zero cross-project writes without Master Guide mediation. | `WORKSPACE_MASTER_CONTEXT.md` §7 |
| **Deterministic Routing** | Pipeline aliases resolve via JSON table before profile injection. Zero LLM inference for routing. | `QWEN_CONTEXT.md` Phase 1 |
| **Strict Data Ownership** | One owner per file. Cross-agent writes require owner mediation. Logs are append-only. | `WORKSPACE_MASTER_CONTEXT.md` §5, §12 |
| **Lazy-Loaded Dashboards** | `<!-- INCLUDE: widget-id -->` directives. Token weight caps enforced per tier. | Widget Spec v2.0 |
| **Gate-Enforced Pipeline** | `/export` → requires `/approve` → requires `/review`. Hard blocks on skips. | `WORKSPACE_MASTER_CONTEXT.md` §12 |
| **Ethics & Compliance** | `robots.txt` compliance, PII filtering, ≤15% semantic similarity, MENA legal alignment. | `WORKSPACE_MASTER_CONTEXT.md` §12 |

---

## 5. FUNCTIONAL REQUIREMENTS (DETAILED)

### 5.1 Pipeline Decoupling & Alias Mapping

| ID | Requirement | Data Source | Acceptance Criteria |
|----|-------------|-------------|---------------------|
| FR-1.1 | Implement `pipeline-alias-mapping.json` mapping 30 simplified pipelines to 29 existing profiles | `factory/library/`, `_taxonomy.json` | All 30 IDs resolve to valid profile + required agents/skills; failsafe to `fallback_profile` |
| FR-1.2 | Backward compatibility shim for `--pipeline galeria` | Legacy routing table | Auto-resolves to `content-machine-editorial` + SEO pipeline; zero routing conflicts |
| FR-1.3 | Alias resolver integrated into `compose.py --pipeline` | `compose.py` v4.0.0+ | CLI flags parsed before scaffolding; `--explain-routing` outputs deterministic path |

### 5.2 Folder Structure Correction & Sovereign Initialization

| ID | Requirement | Validation Script | Acceptance Criteria |
|----|-------------|-------------------|---------------------|
| FR-2.1 | `workspaces/clients/<slug>/` contains ONLY metadata | `audit_path_integrity.py` | NO `.ai/`, NO `src/`, NO executable files |
| FR-2.2 | `workspaces/clients/<slug>/001_<slug>/` = sovereign workspace | `audit_path_integrity.py` | Contains full 3-tier `.ai/`, `dashboard/`, `prd.md`, `plan.md`, `src/` |
| FR-2.3 | Enforce `--structure` validation pre-generation | `compose.py --structure` | Blocks malformed trees; enforces `001_`, `002_` numbering |

### 5.3 Master Guide & Root Memory Layer

| ID | Requirement | Data Flow | Acceptance Criteria |
|----|-------------|-----------|---------------------|
| FR-3.1 | Root `.ai/` layer with `master-guide.md` | Reads `.ai/memory/workspace-index.json` + `user-skill-profile.json` | Aggregates deltas from ≥3 projects without token overflow |
| FR-3.2 | `/master sync all` command | Project `state.json` → root memory | Updates `workspace-index.json`; applies Context Compression (95) skill |
| FR-3.3 | Cross-workspace pattern detection | `skill-memory/` + `state.json` | Triggers at ≥3 project threshold; outputs to root dashboard strategic panel |

### 5.4 Brainstorm Agent Integration (Proactive Mode)

| ID | Requirement | Trigger Logic | Acceptance Criteria |
|----|-------------|---------------|---------------------|
| FR-4.1 | Dual-mode operation (Command + Proactive) | Command: `/brainstorm [mode]`. Proactive: contextual scan | Max 2 suggestions/session; writes to `dashboard/brainstorm-suggestions.md` |
| FR-4.2 | 6 trigger conditions monitored | Stall (>2 sessions), Pattern Match, Gap Detection, Cross-Workspace, Skill Alignment, Pipeline Opportunity | Each trigger maps to deterministic rule set; no LLM guesswork |
| FR-4.3 | Dismiss/Accept/Refine routing | `/brainstorm dismiss/accept/refine [id]` | Logs decision to `memory/`; updates widget state; archives after 7d |
| FR-4.4 | Gate-lock enforcement | `/review`, `/export` active | Proactive Mode suspends; UI shows `🔒 Read-Only` badge |

### 5.5 Three-Tier Dashboard System

| ID | Requirement | Widget Spec | Acceptance Criteria |
|----|-------------|-------------|---------------------|
| FR-5.1 | Root dashboard (`.ai/dashboard/`) | `widget-root-*` components | Global status, cross-patterns, strategic recs, token health |
| FR-5.2 | Client dashboard (`clients/<slug>/dashboard/`) | `widget-client-*` components | Metadata view, project roster, brand DNA, Master Guide insights |
| FR-5.3 | Project dashboard (`001_<slug>/dashboard/`) | `widget-project-*` components | Pipeline progress, agent roster, task status, brainstorm panel |
| FR-5.4 | Lazy loading & token governance | `<!-- INCLUDE: widget-id -->` | <5% session budget; delta sync >5% threshold; archive protocol active |
| FR-5.5 | Deterministic rendering | JSON/Markdown parsing only | Zero LLM inference for data extraction; fails gracefully on missing source |

### 5.6 CLI & Command System Updates

| ID | Requirement | Routing Path | Acceptance Criteria |
|----|-------------|--------------|---------------------|
| FR-6.1 | `/create-client` generates metadata-only folder | `compose.py` + client scaffold | Produces `README.md`, `metadata.json`, client dashboard |
| FR-6.2 | `/create-project` generates sovereign workspace | `compose.py --pipeline` + alias resolver | Initializes `.ai/`, dashboard, PRD, plan; registers to root index |
| FR-6.3 | `/dashboard [scope]` renders targeted view | Dashboard renderer + lazy loader | Supports `root`, `client`, `project`; mirrors to `.cursor/rules/` |
| FR-6.4 | Flag parsing & tool routing integration | `.ai/cli-layer/command-routing.json` | `--tool`, `--explain-routing`, `--prefer`, `--parallel` all functional |

---

## 6. NON-FUNCTIONAL REQUIREMENTS

| Category | Requirement | Threshold | Measurement |
|----------|-------------|-----------|-------------|
| **Token Economics** | Dashboard render cost | <5% session budget | `state.json` delta tracking |
| **Performance** | Lazy render load time | <800ms in IDE | Cursor/Qwen render benchmark |
| **Reliability** | Append-only log integrity | 0 truncation/deletion events | `audit-workspace-integrity.py` |
| **Security** | Ethical scraping & PII | ≤15% semantic similarity; robots.txt compliant | Scraper-agent audit log |
| **Compliance** | MENA legal/financial alignment | AAOIFI/IFSB, Egypt GAFI, UAE DLD rules | Compliance checklist in metadata |
| **Scalability** | Cross-workspace sync | ≤10 concurrent projects without drift | `/master sync` timeout check |
| **Maintainability** | Library health baseline | ≥70/100 integrity post-remediation | `deep_audit_report.md` delta |

---

## 7. SYSTEM ARCHITECTURE & DATA FLOW

```
[CLI / IDE Input] → /command --flags
        ↓
.tool_router_v2.py → parses flags, resolves tool adapter (copilot|codex|gemini|qwen|opencode|kilo)
        ↓
[Phase 1-2] compose.py → resolves pipeline alias via JSON table → scaffolds corrected structure
        ↓
[Phase 3] master-guide.md → reads .ai/memory/workspace-index.json → aggregates deltas
        ↓
[Phase 4] brainstorm-agent.md → monitors context triggers → appends to dashboard/brainstorm-suggestions.md
        ↓
[Phase 5] dashboard/index.md → lazily renders widgets via <!-- INCLUDE: widget-id -->
        ↓
[Phase 6] audit scripts → validate structure, ownership, token budget, pipeline gates
        ↓
[Output] → Autonomous workspace in workspaces/clients/<slug>/001_<slug>/
```

**Read Path:** Deterministic JSON/Markdown parsing. Zero LLM inference for data extraction.  
**Write Path:** Owner-agent only → append-only → delta threshold check (>5%) → widget update → ISO-8601 timestamp.  
**Memory Layer:** `.ai/memory/state.json` + `context-cache/` + `skill-memory/` per project. Root aggregates via `/master sync`.

---

## 8. PHASE-GATED EXECUTION PLAN

| Phase | Title | Dependencies | Deliverables | Validation Gate | Rollback Trigger |
|-------|-------|--------------|--------------|-----------------|------------------|
| 1 | Pipeline Decoupling & Alias Mapping | ✅ COMPLETE | 30 pipelines mapped; deterministic routing enabled. |
| 2 | Folder Structure Correction & Sovereign Init | ✅ COMPLETE | Sovereign hierarchy enforced; `audit_path_integrity.py` deployed. |
| 3 | Master Guide & Root Memory Layer | ✅ COMPLETE | Root `.ai/` initialized; `sync_master_memory.py` functional. |
| 4 | Brainstorm Agent Integration | ✅ COMPLETE | Dual-mode proactive triggers functional; suggestions dashboard deployed. |
| 5 | Three-Tier Dashboard Recreation | ✅ COMPLETE | Root/Client/Project dashboards functional with lazy-load engine. |
| 6 | Backward Compatibility & Smoke Tests | ✅ COMPLETE (v5.0.1 Hardened) | Smoke test suite passed (6/6); multi-IDE mirroring verified. |

---

## 9. MIGRATION & BACKWARD COMPATIBILITY STRATEGY

1. **Snapshot Pre-Run:** Git tag `v5.0.0-pre-migration`. Copy `workspaces/` to `.backup/v4.0.0-workspaces/`.
2. **Legacy Path Mapping:** Run `migrate-legacy-workspaces.py` to move old `projects/` → `workspaces/clients/galeria-properties/001_...`.
3. **Memory Preservation:** Retain all `.ai/memory/`, `state.json`, `workflow.jsonl`. Map to new structure via UUID cross-reference.
4. **Dashboard Archival:** Move legacy dashboard files to `dashboard/archive/v4-legacy/`. Generate new tiered structure.
5. **Compatibility Shim:** `--pipeline galeria` and legacy commands remain functional via alias table.
6. **Integrity Verification:** Post-migration hash comparison (`sha256sum`) on all critical memory/log files. Zero delta allowed.

---

## 10. RISK MANAGEMENT & MITIGATION

| Risk | Probability | Impact | Mitigation | Owner |
|------|-------------|--------|------------|-------|
| Alias routing mismatch | Low | High | Fallback to `fallback_profile`; hard CLI validation | `guide-agent` |
| Cross-project memory bleed | Medium | Critical | Strict `.ai/` isolation; Master Gate mediation only | `master-guide` |
| Dashboard token overflow | Medium | Medium | Lazy load + delta sync + <5% budget cap | `memory-manager` |
| Brainstorm suggestion spam | Low | Low | Max 2/session; gate-lock; auto-archive 7d | `brainstorm-agent` |
| Legacy data loss during migration | Low | Critical | Pre-snapshot + hash verification + dry-run mode | `antigravity-agent` |
| Library health degradation | Medium | High | Strict `library-first` + pre-commit audit | `Router` + `CapabilityRegistry` |

---

## 11. VALIDATION, TESTING & SUCCESS METRICS

### 🔍 Smoke Test Matrix

| Test ID | Scenario | Expected Result | Pass/Fail |
|---------|----------|-----------------|-----------|
| ST-01 | `/dashboard root --render` | Cross-workspace overview + ≥1 strategic recommendation | |
| ST-02 | `/dashboard project --render` | Pipeline progress + ≤2 Brainstorm suggestions (lazy load) | |
| ST-03 | Brainstorm Proactive Trigger | Writes exactly 1-2 suggestions to `brainstorm-suggestions.md` | |
| ST-04 | `/brainstorm dismiss [id]` | Removes entry, logs to memory, updates widget state | |
| ST-05 | `/master sync all` | Aggregates project states, updates `workspace-index.json` | |
| ST-06 | Legacy workspace migration | 0 data loss, correct path mapping, intact `.ai/` memory | |
| ST-07 | Pipeline gate enforcement | `/export` fails without `/approve` → `/review` completion | |
| ST-08 | Token budget check | Dashboard + sync operations <5% session allocation | |
| ST-09 | Structure integrity audit | Client folders contain 0 `.ai/`; projects contain full sovereign `.ai/` (Content-level check active) | |
| ST-10 | Full suite execution | `python3 .ai/scripts/run-smoke-tests.py` → 6/6 PASS | |

### 📊 KPI Targets

| Metric | Baseline | Target (v5.0.0) | Measurement |
|--------|----------|----------------|-------------|
| Pipeline Routing Accuracy | Hardcoded | >99% deterministic | `audit_path_integrity.py` |
| Dashboard Render Cost | ~15-20% | <5% session tokens | `state.json` delta |
| Brainstorm Precision | Manual-only | >85% trigger relevance | Accept/dismiss ratio |
| Migration Data Loss | N/A | 0% | Pre/post hash comparison |
| Governance Violations | Occasional | 0 critical blocks | Audit script errors |
| Library Health Integrity | 38/100 | ≥70/100 | `deep_audit_report.md` |

---

## 📎 APPENDIX A: KEY FILE PATHS & CONTEXT CROSS-REFERENCES

| Resource | Path | Context Reference |
|----------|------|-------------------|
| Master Context | `docs/context/WORKSPACE_MASTER_CONTEXT.md` | §1-12, Governance, Library |
| Qwen Context | `docs/qwen/QWEN_CONTEXT.md` | Audit reality, Phase status, Agents |
| PRD v4.0.0 | `docs/workspace/prd/AI_WORKSPACE_FACTORY_PRD.md` | Baseline architecture |
| Playbook v4.0.0 | `docs/workspace/playbook/AI_WORKSPACE_FACTORY_PLAYBOOK.md` | Operational manual |
| Deep Audit Report | `docs/workspace/report/deep_audit_report.md` | Health score, remediation |
| Pipeline Alias Table | `factory/library/pipeline-alias-mapping.json` | FR-1.1 |
| Tool Router v2 | `.ai/scripts/tool_router_v2.py` | CLI routing, flags |
| Path Integrity Audit | `.ai/scripts/audit_path_integrity.py` | FR-2.1, ST-09 |
| Smoke Tests | `.ai/scripts/run-smoke-tests.py` | ST-10 |
| Data Ownership | `.ai/data-ownership.md` | §4, Governance |
| Workspace Index | `.ai/memory/workspace-index.json` | FR-3.1 |
| Sync Config | `.ai/dashboard/sync-config.json` | Widget Spec v2.0 |
| Dashboard Integrity Audit | `.ai/scripts/audit-dashboard-integrity.py` | FR-5.4 |
| Profile Schema | `factory/registry/profile-schema.json` | FR-2.3, v5.0.1 |

## 📎 APPENDIX B: WIDGET METADATA SCHEMA (v2.0)

```json
{
  "widget_id": "string",
  "version": "string",
  "owner_agent": "string",
  "last_updated": "ISO-8601",
  "token_weight": "light|medium|heavy",
  "data_source": "string",
  "update_trigger": "string",
  "lazy_load": true,
  "archive_ttl_days": 7,
  "gate_lock": false
}
```

Embedded in Markdown as: `<!-- WIDGET: {...} -->`  
Parsed by renderer via deterministic JSON extractor. Zero LLM inference.

## 📎 APPENDIX C: COMMAND ROUTING MAP

| Command | Tier | Owner | Flags | Output |
|---------|------|-------|-------|--------|
| `/create-client` | CLI | `compose.py` | `--tool`, `--explain-routing` | Client metadata + dashboard |
| `/create-project` | CLI | `compose.py` + Alias Resolver | `--pipeline`, `--parallel`, `--tool` | Sovereign `.ai/` + workspace |
| `/dashboard` | CLI | Dashboard Renderer | `[scope]`, `--render` | Lazy-loaded Markdown view |
| `/master sync` | T1 | `master-guide` | `all`, `[scope]` | Root memory aggregation |
| `/brainstorm` | T2 | `brainstorm-agent` | `[mode]`, `dismiss/accept/refine [id]` | Contextual suggestions + memory log |
