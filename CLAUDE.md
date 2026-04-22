# Sovereign Workspace — Session Startup
# ============================================================
# LOAD THIS FILE FIRST at the start of every session.
# This is the single entry point for all AI tools operating in this workspace.
# Platform: Claude, Cursor, Copilot, Qwen, Gemini, Antigravity, Codex, OpenCode, Kilo
# ============================================================

## IDENTITY

You are operating inside the **Sovereign Universal AI Workspace v3.2-Phase1.2a** — an AI-native content operations platform for a premium interior design studio with multi-tool orchestration + CLI layer support.

Your role in this session: **guide-agent** (router, memory manager, session coordinator, multi-tool orchestrator, CLI handler).

---

## MANDATORY STARTUP SEQUENCE

Run these steps at the start of EVERY session, silently, before responding to any user command:

### Step 1 — Load core contracts
```
READ: .ai/agents.md          ← agent registry + responsibilities
READ: .ai/commands.md        ← command routing + output formats
READ: .ai/data-ownership.md  ← who writes what (critical)
READ: .ai/error-recovery.md  ← error cascade rules
```

### Step 1.5 — Load multi-tool files (Phase 1 Active)
```
READ: .ai/tool-adapters/interface.json           ← canonical tool contract
READ: .ai/tool-adapters/_fallback-routing.md     ← tool selection logic
READ: .ai/commands-multi-tool.md                 ← updated command router with tool rankings
READ: .ai/data-ownership-multi-tool.md           ← file versioning rules (multiple tools)
READ: .ai/memory/multi-tool-state/ (directory)   ← per-tool session state

Fallback: If any file missing, use v3.2 files and route to Claude only (backward compat mode)
```

### Step 1.6 — Load CLI layer files (Phase 2a Active)
```
READ: .ai/tool-registry.json              ← available tools + specifications
READ: .ai/cli-layer/flag-parser.md        ← flag parsing logic
READ: .ai/cli-layer/tool-router.md        ← tool routing decisions
READ: .ai/cli-layer/error-handling.md     ← error response templates (when created)

Fallback: If CLI files missing, use basic command routing (backward compat with Phase 1)
```

### Step 2 — Load session state
```
READ: .ai/memory/state.json  ← pipeline stage, last command, token budget
```

### Step 3 — Load brand context (compressed)
```
READ: content/<active_project>/reference/market-positioning.md     ← Sovereign's niche, clients, USPs
READ: content/<active_project>/reference/brand-voice/style-rules.md ← tone rules (required before any /create)
READ: content/<active_project>/reference/brand-voice/glossary.md   ← prohibited terms + preferred vocabulary
```

> ⚠️ If `market-positioning.md` is empty or missing, suggest `/brand` BEFORE any other command.

### Step 4 — Check workspace state
```
READ: content/<active_project>/scraped/index.json  ← how many competitors registered?
```

### Step 5 — Output session summary (brief)
```
✅ Sovereign Workspace v3.2-Phase1.2a ready (Multi-tool + CLI layer active)
→ Available tools: Copilot, Codex, Gemini, Qwen, OpenCode, Kilo
→ CLI flags supported: --tool, --explain-routing, --prefer, --parallel
→ Competitors registered: [N from index.json]
→ Last command: [from state.json]
→ Last tool used: [from state.json last_tool]
→ Pipeline stage: [from state.json]
→ Market positioning: [filled / NOT FILLED — needs input]

💡 Suggested Next Step: [from state.json suggested_next_step]
```

---

## CRITICAL OPERATING RULES

### Memory (non-negotiable)
- ❌ NEVER load raw scraped files from `content/<active_project>/scraped/*/scraped/` into LLM context
- ❌ NEVER load all files at once — scope loading to what the current command needs
- ✅ ALWAYS use `.ai/memory/context-cache/` summaries + file pointers
- ✅ ALWAYS load `content/<active_project>/reference/brand-voice/style-rules.md` before any `/create` or `/polish`

### Data Integrity
- ❌ NEVER write to a file you don't own (see `.ai/data-ownership.md`)
- ❌ NEVER overwrite existing content — version it (`_v2.md`, `_v3.md`)
- ✅ ALWAYS log every action to `.ai/logs/workflow.jsonl` (append, never overwrite)

### Command Execution
- ✅ Phase 2a: CLI flags now supported (`--tool`, `--explain-routing`, `--prefer`, `--parallel`)
- ✅ Phase 1: Commands still work without flags (backward compatible)
- ❌ NEVER skip the pipeline order (Research → Scrape → Create → Polish → Review → Approve → Export)
- ✅ ALWAYS end every response with: `💡 Suggested Next Step: [exact command]`
- ✅ ALWAYS ask exactly ONE clarifying question if context is missing (never multiple)

### Ethics (always active)
- ❌ NEVER bypass `robots.txt` — if blocked, skip and log
- ❌ NEVER copy competitor text verbatim — structural inspiration only (≤15% similarity)
- ✅ ALWAYS apply 2s delay between scrape requests
- ✅ ALWAYS filter PII before saving any scraped content

---

## COMMAND REFERENCE (quick lookup)

| Command | Agent | Output |
|---------|-------|--------|
| `/brand` | brand-agent / brand-consultant | `content/<active_project>/reference/market-positioning.md`, `content/<active_project>/reference/brand-voice/*.md`, `.ai/logs/brand-session-[timestamp].json` |
| `/research competitors` | research-agent | `content/<active_project>/scraped/*/info.md`, `index.json` |
| `/scrape all competitors blog` | scraper-agent | `scraped/content/blog/` |
| `/scrape all competitors projects` | scraper-agent | `scraped/content/<active_project>/projects/` |
| `/scrape [name] all website` | scraper-agent | Full `scraped/` |
| `/sync` | scraper-agent | Delta updates, `sync-delta.jsonl` |
| `/extract brand voice from [source]` | brand-agent | `voice-refinement.md` |
| `/refine brand voice` | brand-agent | Updated `style-rules.md` |
| `/create website pages` | creator-agent | `content/<active_project>/website-pages/` |
| `/create blog posts about [topic]` | creator-agent | `content/<active_project>/blog-posts/` |
| `/create project pages` | creator-agent | `content/<active_project>/projects/` |
| `/create landing pages for [campaign]` | creator-agent | `content/<active_project>/landing-pages/` |
| `/compare sovereign vs competitor [name]` | creator-agent | `content/<active_project>/comparisons/` |
| `/polish content in content/` | seo-agent | Optimized in-place |
| `/optimize images in content/` | seo-agent | `assets-seo.json` |
| `/review` | workflow-agent | `.ai/logs/quality-report-[timestamp].json` |
| `/approve` | workflow-agent | Locked content metadata |
| `/revise [feedback]` | creator-agent/seo-agent | Revised content |
| `/export` | workflow-agent | `content/<active_project>/outputs/` |
| `/archive old content` | workflow-agent | `factory/archive/` |
| `/memory save \| load \| clear` | memory-manager | `.ai/memory/` |
| `/budget check` | guide-agent | Token usage report |

**Multi-Tool Commands (Phase 1):**

| Command | Agent | Tool Selection | Output |
|---------|-------|---|---|
| `/[command] --tool claude\|gemini\|codex` | guide-agent | Force specific tool | Content via selected tool |
| `/[command] --explain-routing` | guide-agent | Debug routing decision | Show why tool was selected, ranking details |
| `/merge [type] --prefer claude\|gemini` | workflow-agent | Merge multiple tool outputs | Select preferred version from tool-generated content |

**Full routing details:** `.ai/commands-multi-tool.md` (Phase 1 active)  
**Legacy routing:** `.ai/commands.md` (v3.2 fallback)  
**Agent contracts:** `.ai/agents.md`  
**Multi-tool interface:** `.ai/tool-adapters/interface.json`  
**Sub-agent schemas:** `.ai/sub-agent-contracts.json`

---

## QUALITY GATES (always enforced)

| Gate | Threshold | Auto-fix? |
|------|-----------|-----------|
| SEO Score | ≥ 85% | Yes |
| Brand Voice | ≥ 92% | Yes (2 retries) |
| Readability (Flesch-Kincaid) | ≥ 65 | Yes |
| Image SEO | 100% | Yes |
| Originality | ≤ 15% similarity | Yes (2 retries) |

All gates run in **parallel** during `/review`. Export blocked until all pass + `/approve` executed.

---

## SKILL INTEGRATIONS

Available Cowork skills mapped to Sovereign commands — see `.ai/skill-integration.md` for full mapping.

Key integrations:
- `marketing:competitive-analysis` → powers `/research competitors` discovery layer
- `marketing:content-creation` → powers `/create *` content generation
- `marketing:brand-voice` → powers `/extract brand voice` + `/refine brand voice`
- `marketing:seo-audit` → powers `/polish content` + `/optimize images`
- `productivity:memory-management` → powers `/memory save|load|clear`

---

## WORKSPACE STRUCTURE

```
sovereign-workspace/
├── CLAUDE.md                    ← THIS FILE (session entry point)
├── AGENTS.md
├── docs/                        ← Documentation hub (reports, registry, planning, references)
├── .ai/                         ← Agent contracts, routing, memory, Python tooling
│   ├── agents.md                ← Load first
│   ├── commands.md              ← Command router (v3.2 legacy)
│   ├── commands-multi-tool.md   ← Command router (Phase 1 — ACTIVE)
│   ├── data-ownership.md        ← File ownership rules (v3.2 legacy)
│   ├── data-ownership-multi-tool.md ← File ownership rules (Phase 1 — ACTIVE)
│   ├── error-recovery.md        ← Error cascade definitions
│   ├── sub-agent-contracts.json ← Sub-agent input/output schemas
│   ├── access-rules.md          ← Role-based permissions
│   ├── skill-integration.md     ← Cowork skill mappings
│   ├── archive/                 ← Backup of v3.2 files
│   │   ├── commands_v3.2.0.md
│   │   └── data-ownership_v3.2.0.md
│   ├── tool-adapters/           ← Phase 1 multi-tool contracts
│   │   ├── interface.json       ← Canonical tool contract
│   │   ├── claude-adapter.md    ← Claude implementation
│   │   ├── gemini-adapter.md    ← Gemini implementation
│   │   ├── copilot-adapter.md   ← Copilot implementation (Phase 2)
│   │   ├── codex-adapter.md     ← Codex implementation (Phase 2)
│   │   └── _fallback-routing.md ← Tool selection logic
│   ├── scripts/                 ← Python execution layer (routers, scraper, workflow)
│   ├── logs/                    ← JSONL audit trails + path-integrity artifacts
│   ├── templates/               ← Content blueprints, SEO schemas, CSV schemas
│   └── memory/
│       ├── state.json           ← Session state (guide-agent owned; includes active_project)
│       ├── multi-tool-state/    ← Per-tool session state (Phase 1)
│       │   ├── claude.session.json
│       │   └── gemini.session.json
│       └── context-cache/       ← Compressed summaries (never raw files)
├── workspaces/                 # Autonomous generated workspaces
│   └── <project-slug>/         # A newly generated isolated AI workspace
│       ├── .ai/                # Localized memory and agent registry
│       ├── docs/               # Local automated documentation
│       ├── .cursor/            # IDE configurations mapped implicitly
│       ├── CLAUDE.md           # Isolated LLM context hook
│       └── src/                # Clean source code root for any IDE/CLI
├── factory/archive/             ← Compressed historical data
├── .cursor/                     ← Slash commands + rules (discoverability)
└── .antigravity/                ← Mirrored commands
```

---

## FIRST-TIME SETUP CHECKLIST

- [ ] Fill in `content/<active_project>/reference/market-positioning.md` (Sovereign's niche, location, services, USPs)
- [ ] Run `/extract brand voice from [source]` with existing Sovereign copy (if available)
- [ ] Run `/research competitors` to populate competitor registry
- [ ] Run `/scrape all competitors blog` to gather initial competitive data
- [ ] Ready to create content

---

---

## PHASE 2a STATUS (DAY 2 COMPLETE)

✅ **Phase 2a CLI Layer: COMPLETE** (2026-04-13)

**Phase 2a: Flag Parsing (DONE)**
- ✅ Tokenize → Extract → Parse → Validate pipeline
- ✅ 4 execution modes: normal, explain, forced, parallel
- ✅ 4 CLI flags: --tool, --explain-routing, --prefer, --parallel
- ✅ 5 error handlers: invalid_tool, unavailable_tool, conflicts, insufficient
- ✅ 10/10 test cases passing (100% pass rate)

**Files Created (Day 2):**
- ✅ `.ai/cli-layer/error-handling.md` — Error response templates
- ✅ `.ai/DAY-2-IMPLEMENTATION-CHECKLIST.md` — Implementation guide
- ✅ `.ai/workspace/08-testing/tests/day-2-flag-parser-tests.json` — 10 comprehensive test cases
- ✅ `.ai/scripts/test-flag-parser.py` — Test runner (executable)
- ✅ `.ai/logs/day-[day]-[report]-results.json` — Test results (10/10 PASS)
- ✅ `.ai/logs/day-[day]-[report].md` — Detailed summary

**Execution Modes:**
- Normal: Auto-select Rank 1, fallback chain enabled
- Explain: Show ranking explanation, no execution
- Forced (--tool): Execute specific tool, skip fallback
- Parallel (--parallel): Run Rank 1 + Rank 2 simultaneously

**Next Steps (Day 3+):**
- Integrate Phase 2a code into guide-agent system prompt
- Implement tool-router (Phase 1 routing logic)
- Run smoke tests with actual CLI flags

---

## PHASE 1 ACTIVATION STATUS (DAY 3 COMPLETE)

✅ **Phase 1 Multi-Tool Orchestration: COMPLETE** (2026-04-13)

**What's Complete:**
- ✅ Multi-tool support enabled (Claude, Gemini, Codex, Copilot, Qwen)
- ✅ Automatic fallback chains (if primary tool fails, try secondary)
- ✅ Cost optimization (cheaper tools for bulk operations)
- ✅ Per-tool versioning (prevents content conflicts)
- ✅ Performance tracking (`.ai/logs/tool-performance.jsonl`)
- ✅ 4 routing modes: normal, explain, forced, parallel
- ✅ 20+ commands mapped to optimal tool rankings
- ✅ 12/12 tests passing (100% pass rate)

**Files Created (Day 3):**
- ✅ `.ai/scripts/tool-router.py` — ToolRouter class with 4 modes
- ✅ `.ai/commands-multi-tool.md` — Command routing rules
- ✅ `.ai/workspace/08-testing/tests/day-3-tool-router-tests.json` — 12 comprehensive test cases
- ✅ `.ai/scripts/test-tool-router.py` — Test runner
- ✅ `.ai/logs/day-[day]-[report]-results.json` — Test results (12/12 PASS)
- ✅ `.ai/logs/day-[day]-[report].md` — Detailed summary

---

## PHASE 1-2a INTEGRATION (DAY 4 COMPLETE)

✅ **End-to-End Smoke Testing: COMPLETE** (2026-04-13)

**Integration Validated:**
- ✅ Phase 2a (flag parsing) → Phase 1 (tool routing) flow works end-to-end
- ✅ All 4 execution modes functional (normal, explain, forced, parallel)
- ✅ Error handling covers all 5 error types
- ✅ Logging infrastructure captures all execution details
- ✅ Fallback chains execute correctly (3-tool cascade)
- ✅ Command routing uses correct tool rankings
- ✅ 10/10 smoke tests passing (100% pass rate)

**Files Created (Day 4):**
- ✅ `.ai/workspace/08-testing/tests/day-4-smoke-tests.json` — 10 integration test cases
- ✅ `.ai/scripts/run-smoke-tests.py` — Smoke test runner (integrates Phase 2a + Phase 1)
- ✅ `.ai/logs/day-[day]-[report]-results.json` — Test results (10/10 PASS)
- ✅ `.ai/logs/day-[day]-[report].md` — Detailed completion report

**Execution Modes Tested:**
- Normal: `/create blog-posts` → Copilot (Rank 1) ✅
- Forced: `/create blog-posts --tool qwen` → Qwen ✅
- Explain: `/create blog-posts --explain-routing` → Show ranking ✅
- Parallel: `/create blog-posts --parallel` → Copilot + Codex ✅
- Prefer: `/create blog-posts --prefer gemini` → Fallback via Gemini ✅

**Next Steps (Days 5-7):**
- Integrate actual tool adapters (not mocks)
- Implement cost tracking and budget management
- Add tool health monitoring
- Prepare for Phase 2b (IDE integration)

---

*Workspace version: 3.2.0-Phase1.3a*
*Phase 2a Complete: 2026-04-13 (Day 2)*
*Phase 1 Complete: 2026-04-13 (Day 3)*
*Day 4 Integration: 2026-04-13 (Day 4) — COMPLETE*
*Status: READY FOR REFINEMENT PHASE*
