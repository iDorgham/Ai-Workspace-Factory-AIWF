# Workspace Index — Complete File Listing

**Generated:** 2026-04-13 (Phase 2 layout refresh)  
**Scope:** `.ai/workspace/` documentation tree + pointers to live `.ai/` (including `.ai/logs/` and `.ai/templates/`)

---

## 📊 Directory structure (`.ai/workspace/`)

Runtime contracts, adapters, templates, logs, and live session state are **not** duplicated here — they live under **`.ai/`** at the repository root.

```
.ai/workspace/
├── README.md, INDEX.md, START_HERE.md, ORGANIZATION-SUMMARY.txt
├── 01-system-architecture/     # design & roadmaps (+ README)
├── 03-cli-layer/               # CLI design notes (live files: ../.ai/cli-layer/)
├── 05-memory-state/            # phase-1-status.json snapshot (live: ../.ai/memory/state.json)
├── 06-brand-reference/         # brand docs (+ content/sovereign/reference/market_positioning.md, brand-voice/)
├── 07-content-templates/        # stub README → canonical `.ai/templates/`
├── 08-testing/                 # TASK specs; JSON tests under 08-testing/tests/
├── 09-logs-reports/            # phase reports; legacy-snapshots/ (stub → archive/legacy-snapshots/); milestones/
├── 10-archive/                 # historical copies + archive-index.json
├── _quick-reference/
└── _setup-guides/
```

### Canonical locations (repo root)

| Concern | Path |
|--------|------|
| Agents, ownership, commands | `.ai/agents.md`, `.ai/commands*.md`, `.ai/data-ownership*.md` |
| CLI + tool routing (live) | `.ai/cli-layer/` |
| Tool adapters + registry | `.ai/tool-adapters/`, `.ai/tool-registry.json` |
| Session memory | `.ai/memory/state.json` |
| Append-only / audit logs | `.ai/logs/` |
| Active `content/<slug>/` projects (table + slugs) | [`content/README.md`](../../content/README.md) |

---

## 🎯 Navigation by Role

### For **Architects**
- `01-system-architecture/ARCHITECTURE-v3.2_AGENT_CLARITY.md`
- `01-system-architecture/PHASE_1_VISUAL_ARCHITECTURE.md`
- `.ai/agents.md`
- `.ai/data_ownership_multi_tool.md`

### For **Content Creators**
- `06-brand-reference/content/sovereign/reference/market_positioning.md`
- `06-brand-reference/content/sovereign/reference/brand-voice/style_rules.md`
- `.ai/templates/content-blueprints/` (all templates)
- `_quick-reference/QUICK_REFERENCE.md`

### For **Developers / Engineers**
- `03-cli-layer/` (CLI design notes)
- `.ai/cli-layer/` and `.ai/tool-adapters/` (live routing + adapters)
- `08-testing/tests/` (JSON test cases) and `08-testing/TASK-*.md`
- `.ai/sub-agent-contracts.json`

### For **Brand Strategists**
- `06-brand-reference/content/sovereign/reference/market_positioning.md`
- `06-brand-reference/content/sovereign/reference/brand-voice/`
- `06-brand-reference/brand_discovery.md`
- `09-logs-reports/` (brand analysis reports)

### For **Project Managers**
- `01-system-architecture/IMPLEMENTATION-ROADMAP-v3.2.md`
- `09-logs-reports/` (all completion reports)
- `.ai/memory/state.json` (current progress)
- `_setup-guides/IMPLEMENTATION_CHECKLIST.md`

### For **New Team Members**
- `_setup-guides/README.md` (start here)
- `README.md` (main navigation)
- `06-brand-reference/README.md` (brand training)
- `.ai/templates/` (content formats)

---

## 🔍 Quick Lookup by Task

| Task | Files |
|------|-------|
| Understanding system design | `01-system-architecture/` |
| Creating content | `06-brand-reference/`, `.ai/templates/` |
| Using multiple AI tools | `.ai/tool-adapters/`, `03-cli-layer/`, `.ai/cli-layer/` |
| Setting up workspace | `_setup-guides/` |
| Finding a command | `_quick-reference/QUICK_REFERENCE.md` |
| Checking permissions | `.ai/data_ownership_multi_tool.md` |
| Running tests | `08-testing/tests/`, `08-testing/TASK-*.md` |
| Reviewing progress | `09-logs-reports/`, `.ai/logs/` |
| Comparing versions | `10-archive/previous-versions/` |
| Accessing brand voice | `06-brand-reference/content/sovereign/reference/brand-voice/` |

---

## 📊 File Categories

### Documentation (.md files) — 65 files
- System architecture: 5
- Agent contracts: 6
- CLI layer: 5
- Tool adapters: 14
- Brand reference: 5
- Content templates: 4
- Setup guides: 5
- Quick reference: 4
- Task specs: 6
- Completion reports: 11 (growing)

### Configuration (.json files) — 16 files
- Tool registry and adapters: 5
- Memory state: 2
- Test cases: 7
- Templates and schemas: 2

### Archive (historical) — 11 files
- Previous versions: 2
- Competitor data: indexed
- Content archives: indexed

---

## ✅ Completeness Checklist

- [x] System architecture documented
- [x] All agents defined
- [x] Data ownership rules established
- [x] CLI layer complete (Phase 2a)
- [x] 8 tool adapters implemented
- [x] 4 execution modes working
- [x] 32/32 tests passing
- [x] Content templates created
- [x] Brand reference started
- [x] Memory system initialized
- [x] 4 README files created
- [x] Setup guides written

---

## 🚀 Next Steps

**Starting a new session?**
1. Read `README.md` (main overview)
2. Read `_setup-guides/README.md` (setup checklist)
3. Review `06-brand-reference/README.md` (brand training)
4. Reference `.ai/templates/` (content formats)

**Looking up specific info?**
→ Use this `INDEX.md` to find the right folder, then check that folder's `README.md`

**Debugging an issue?**
→ Check `.ai/data-ownership*.md` (permissions), `.ai/cli-layer/` (routing), or `08-testing/` (test cases)

---

## 📝 Notes

- Structure designed for 3+ team members working simultaneously
- All folders have dedicated README files explaining purpose
- Files are versioned (v3.2.0-Phase1.3a)
- 100% test coverage (32/32 tests passing)
- Last organized: 2026-04-13

---

**Questions?** See root `README.md` or specific folder `README.md` for guidance.
