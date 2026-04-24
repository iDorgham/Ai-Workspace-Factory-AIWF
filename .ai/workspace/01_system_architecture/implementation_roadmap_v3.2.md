# Sovereign Workspace v3.2: Implementation Roadmap
**Target:** Clarified agent architecture with zero user-facing changes  
**Scope:** Script refactoring + testing + validation  
**Timeline:** 4 weeks  
**Effort:** Moderate (refactor existing agents, don't build new features)

---

## PHASE 1: FOUNDATION & CONTRACTS (Week 1)

### Deliverable: Updated Agent & Data Ownership Definitions

**Task 1.1: Update `.ai/agents.md`**
- [ ] Replace agent list with 3-tier hierarchy (Gateway, Primary, Utility)
- [ ] Define primary responsibility for each agent (single sentence)
- [ ] List sub-agents per primary agent + their specific contracts
- [ ] Define error recovery ownership (who retries what)
- [ ] Format: YAML or Markdown with JSON examples for contracts
- [ ] QA: Review with product + engineering for ambiguities

**Task 1.2: Create `.ai/data_ownership.md`**
- [ ] List all data files (index.json, sync-status.json, content/*, etc.)
- [ ] Specify: Authoritative owner, read-only agents, write rule, backup rule
- [ ] Format: YAML or table format
- [ ] Validation: No file without explicit owner; no orphaned files

**Task 1.3: Create `.ai/error_recovery.md`**
- [ ] Map each command → failure mode → owner agent → retry logic
- [ ] Specify: Max retries, backoff strategy, fallback action, logging
- [ ] Example: "/sync fails → scraper-agent retries 3x (5s, 10s, 20s) → if still fails, log as stale"
- [ ] Validation: All 12 commands covered; all failure paths defined

**Task 1.4: Create `.ai/sub-agent-contracts.json`**
- [ ] JSON schema defining input/output for each sub-agent
- [ ] Validation rules (types, required fields, thresholds)
- [ ] Example:
  ```json
  {
    "delta-detector": {
      "input": {"index.json": "required", "sync_status.json": "required"},
      "output": {"delta_payload": {"new_urls": "array", "updated_urls": "array"}},
      "validation": {"false_positive_rate": "<10%", "only_deltas_24h_old": true}
    }
  }
  ```

**Deliverable Acceptance Criteria:**
- [ ] `.ai/agents.md` reviewed + approved by product + engineering lead
- [ ] `.ai/data_ownership.md` covers 100% of data files with no orphans
- [ ] `.ai/error_recovery.md` covers all 12 commands + all failure modes
- [ ] `.ai/sub-agent-contracts.json` is valid JSON, all sub-agents have contracts

---

## PHASE 2: REFACTOR CORE SCRIPTS (Weeks 2-3)

### Deliverable: Updated Python scripts with clear agent responsibility

**Track 2A: Scraper Agent Refactoring**

**Task 2.1: Separate delta-detector logic into `.ai/scripts/scraper/delta_detector.py`**
- [ ] Extract URL hashing logic from `scraper_engine.py`
- [ ] Input: index.json, sync-status.json
- [ ] Output: delta-payload.json {competitor_slug: {new, updated, deleted URLs}}
- [ ] Validation: Check false positives, test on 5+ competitors
- [ ] Unit tests: ≥10 test cases (new URLs, updated URLs, deleted URLs, edge cases)
- [ ] Integration test: Verify output is correct JSON schema

**Task 2.2: Refactor `.ai/scripts/scraper/scraper_engine.py`**
- [ ] Remove delta-detection logic (now in delta_detector.py)
- [ ] Make `scraper_engine.py` ONLY handle fetching + parsing (given URLs)
- [ ] Add explicit `sync-state-writer` function (only agent that writes sync-status.json)
- [ ] Input: delta-payload.json + competitor URLs
- [ ] Output: Updated scraped/ folder + sync-status.json (written only here)
- [ ] Error handling: Explicit ownership — scraper_engine catches network errors, logs with retry guidance
- [ ] Unit tests: ≥15 test cases (200 OK, 404, 429, timeout, malformed HTML)

**Task 2.3: Refactor `.ai/scripts/scraper/ethics_compliance.py`**
- [ ] Remove sync-state writes (now only in scraper_engine.py)
- [ ] Responsibility: robots.txt parsing, rate limiting, PII filtering only
- [ ] Input: URLs, raw HTML, robots.txt
- [ ] Output: Compliance pass/fail + sanitized payload
- [ ] Error handling: If violation detected, skip URL, log reason (not blocking entire scrape)
- [ ] Unit tests: ≥10 test cases (robots.txt rules, rate limits, PII patterns)

**Track 2B: Creator Agent Refactoring**

**Task 2.4: Separate brand-voice-applier into `.ai/scripts/creator/[brand_voice_applier].py`**
- [ ] Extract tone validation logic from `content_generator.py`
- [ ] Input: Draft Markdown, content/sovereign/reference/brand-voice/style_rules.md
- [ ] Output: {tone_score, drift_flags, applied_rules}
- [ ] Validation: Tone ≥ 92% required; if <92%, suggest rewrite
- [ ] Unit tests: ≥10 test cases (different tone styles, glossary violations, edge cases)
- [ ] Blocking: If tone < 92%, return validation error (creator-agent retries or escalates)

**Task 2.5: Refactor `.ai/scripts/creator/content_generator.py`**
- [ ] Focus ONLY on content generation + originality check
- [ ] Remove brand-voice application (now in brand_voice_applier.py)
- [ ] Input: outline.json, keyword targets, brand positioning
- [ ] Output: Draft Markdown {frontmatter, body, assets-refs}
- [ ] Validation: Originality ≤ 15% semantic similarity
- [ ] Error handling: If >15%, rewrite with structural shift
- [ ] Unit tests: ≥10 test cases (different topic types, similarity edge cases)

**Task 2.6: Refactor `.ai/scripts/creator/[compare_engine].py`**
- [ ] No changes to logic; clarify that this is only owned by creator-agent
- [ ] Input: Sovereign draft + competitor source
- [ ] Output: content/sovereign/comparisons/*.md with structured diffs
- [ ] Validation: All diffs are actionable (not just "different")
- [ ] Unit tests: Verify diffs match expected format

**Track 2C: SEO Agent Refactoring**

**Task 2.7: Refactor `.ai/scripts/seo/seo_optimizer.py`**
- [ ] Split into two functions: keyword_auditor(), technical_auditor()
- [ ] keyword_auditor() input: Markdown, keyword list → output: {density, placement, cannibal_flags}
- [ ] technical_auditor() input: Markdown → output: {seo_meta.json with H-structure, meta, Flesch score}
- [ ] Error handling: Clear ownership — keyword_auditor catches density violations, technical_auditor catches readability
- [ ] Unit tests: ≥15 test cases (density edge cases, H-structure validation, readability)

**Task 2.8: Refactor `.ai/scripts/seo/[image_seo_auditor].py`**
- [ ] Responsibility: Alt-text generation, WebP conversion, lazy-load, schema only
- [ ] Input: Images in content/, image manifest
- [ ] Output: Updated .md refs, assets-seo.json
- [ ] Validation: 100% alt-text, 100% WebP, WCAG AA contrast (sampled)
- [ ] Error handling: Image conversion fail → skip, log path (don't block)
- [ ] Unit tests: ≥10 test cases (various image formats, conversion failures, alt-text edge cases)

**Track 2D: Workflow Agent Refactoring**

**Task 2.9: Refactor `.ai/scripts/workflow/quality_checker.py`**
- [ ] Convert gates from sequential to parallel execution
- [ ] Gates: SEO (≥85%), Brand (≥92%), Readability (≥65), Image SEO (100%), Originality (≤15%)
- [ ] Input: Staged content + all validators
- [ ] Output: quality-report.json {gate: {passed, score, violations}}
- [ ] Implementation: Use `concurrent.futures.ThreadPoolExecutor` or async/await
- [ ] Error handling: All gates run even if one fails; report all violations
- [ ] Unit tests: ≥5 test cases (all pass, partial fail, all fail, timeout handling)

**Task 2.10: Refactor `.ai/scripts/workflow/[approval_gate].py`**
- [ ] Input: quality-report.json
- [ ] Logic: If all gates passed → lock content, set approved_at timestamp
- [ ] Output: Updated metadata.json {approved: true, approved_at, approved_by}
- [ ] Error handling: If gates not passed → reject, output which gates failed + specific violations
- [ ] Unit tests: ≥5 test cases (all pass, partial fail, no report found)

**Task 2.11: Refactor `.ai/scripts/workflow/export_packager.py`**
- [ ] Input: Approved content (approved: true in metadata)
- [ ] Logic: Validate schema, bundle Markdown + metadata, generate CSV
- [ ] Output: content/sovereign/outputs/{csv-exports/, cms-packs/}
- [ ] Error handling: If not approved → block export, ask for `/approve` first
- [ ] Unit tests: ≥5 test cases (valid content, missing metadata, schema validation failures)

**Task 2.12: Refactor `.ai/scripts/workflow/archive_manager.py`**
- [ ] Input: Content files, cutoff date (>30 days)
- [ ] Logic: Gzip old files, create pointer manifest, update archive-index.json
- [ ] Output: archive/*.gz + archive-index.json
- [ ] Error handling: Decompress verification; if fails, rollback
- [ ] Unit tests: ≥5 test cases (successful archive, compression failure, corruption detection)

**Track 2E: Brand Agent Refactoring**

**Task 2.13: Refactor `.ai/scripts/brand/voice_validator.py`**
- [ ] Input: Draft Markdown, content/sovereign/reference/brand-voice/
- [ ] Output: {compliance_score, violations}
- [ ] Validation threshold: ≥ 92%
- [ ] Error handling: Return violations, suggest fixes (don't auto-rewrite)
- [ ] Unit tests: ≥10 test cases (compliant content, violations, edge cases)

**Task 2.14: Refactor `.ai/scripts/brand/[tone_analyzer].py`**
- [ ] Input: Text sample (existing content or provided text)
- [ ] Output: voice-profile.json {lexicon, pacing, cta_style, tone_intensity}
- [ ] Validation: ≥10 samples analyzed, clusters match
- [ ] Unit tests: ≥5 test cases (different text types, clustering accuracy)

**Task 2.15: Refactor `.ai/scripts/brand/[drift_detector].py`**
- [ ] Input: Recent .md files in content/, style_rules.md
- [ ] Output: drift-report.json {violations}
- [ ] Validation: <20% false positives
- [ ] Unit tests: ≥10 test cases (violations, false positives)

**Deliverable Acceptance Criteria (Track 2A-E):**
- [ ] All scripts refactored with clear single responsibility
- [ ] No file is written by 2+ agents (explicit ownership enforced)
- [ ] Error handling uses defined cascades (no ad-hoc retries)
- [ ] All unit tests pass (≥70 test cases total)
- [ ] Code review: All changes reviewed for clarity + efficiency

---

## PHASE 3: MEMORY MANAGER & INTEGRATION (Week 3)

**Task 3.1: Create `.ai/scripts/core/memory_manager.py`**
- [ ] Responsibility: Context compression, session state, token budgeting
- [ ] Functions:
  - `load_context(command)` → Loads .ai/memory/ + relevant cache summaries + file pointers (NOT raw files)
  - `save_context(state_dict)` → Compresses results, updates state.json, clears temp cache
  - `budget_check()` → Tracks token usage per command; suggests `/memory save` if >70% used
- [ ] Rule: Never load raw competitor scraped files into context
- [ ] Unit tests: ≥10 test cases (context loading, compression, budget tracking)

**Task 3.2: Update `.ai/scripts/core/cli_router.py`**
- [ ] Input: User command (natural language)
- [ ] Logic: Parse intent → extract entities → load context via memory_manager → route to primary agent
- [ ] Output: JSON routing payload {primary_agent, sub_agents, context_summary}
- [ ] Error handling: Ambiguous input → output exactly 1 clarifying question
- [ ] Unit tests: ≥12 test cases (one per command, edge cases)

**Task 3.3: Update `.ai/scripts/core/workflow_orchestrator.py`**
- [ ] Orchestrate all agent calls in proper sequence
- [ ] Enforce pipeline: Research → Scrape/Sync → Create → Polish → Review → Approve → Export
- [ ] Error handling: Cascade errors up agent hierarchy; clear who retries
- [ ] Logging: All state transitions to logs/workflow.jsonl
- [ ] Unit tests: ≥10 test cases (full pipeline, partial failure scenarios)

**Deliverable Acceptance Criteria:**
- [ ] `memory_manager.py` prevents raw file injection into LLM context
- [ ] `cli_router.py` unambiguously maps each command to single primary agent
- [ ] `workflow_orchestrator.py` enforces clear pipeline + error cascades
- [ ] All 3 modules have ≥10 unit tests each
- [ ] Integration test: Run full `/research` → `/scrape` → `/create` → `/review` → `/approve` → `/export` pipeline

---

## PHASE 4: TESTING & VALIDATION (Week 4)

### Deliverable: Comprehensive test suite + cross-platform validation

**Task 4.1: Unit Test Suite**
- [ ] Expand existing tests: ≥100 unit tests total (covering all agents + sub-agents)
- [ ] Coverage target: ≥85% code coverage
- [ ] Test framework: pytest (or existing)
- [ ] CI/CD: Automated test run on every commit

**Task 4.2: Integration Tests**
- [ ] Test full command pipeline for each of 12 commands
- [ ] Scenarios:
  - Happy path: `/research competitors` → `/sync` → `/create` → `/review` → `/approve` → `/export` (all gates pass)
  - Partial failure: `/create` generates content <92% brand voice → `/review` fails brand gate → `/revise` → `/approve`
  - Error recovery: `/sync` encounters 429 → retry logic → eventual skip → continue
- [ ] Test count: ≥20 integration tests
- [ ] Success criteria: All paths execute without errors; state transitions logged correctly

**Task 4.3: Cross-Platform Validation**
- [ ] Test on Claude CLI (primary)
- [ ] Test on Cursor (secondary)
- [ ] Test on Copilot CLI (tertiary)
- [ ] Verify: Command syntax identical, output format identical, execution deterministic
- [ ] Documentation: Cross-platform parity matrix in `.ai/COMPATIBILITY.md`

**Task 4.4: Performance Benchmarking**
- [ ] Measure `/review` latency: Should be ~6s (parallel gates) vs 20s (v3.1 sequential)
- [ ] Measure memory usage: Should be ≥40% lower (explicit memory manager)
- [ ] Measure error recovery cycles: Should be deterministic + logged
- [ ] Regression test: No performance degradation vs v3.1

**Task 4.5: Documentation Review**
- [ ] Verify ARCHITECTURE-v3.2_AGENT_CLARITY.md matches implemented code
- [ ] Verify v3.1-vs-v3.2_SUMMARY.md is accurate
- [ ] Update code comments to reference agent contracts in `.ai/sub-agent-contracts.json`
- [ ] Create runbook: How to debug agent failures (flowchart in `DEBUGGING.md`)

**Deliverable Acceptance Criteria:**
- [ ] ≥100 unit tests, ≥85% coverage
- [ ] ≥20 integration tests, all pass
- [ ] Cross-platform parity verified on 3+ CLI tools
- [ ] Performance benchmarks show 3x faster `/review`, 40% lower memory
- [ ] No regressions vs v3.1

---

## PHASE 5: ROLLOUT & DEPLOYMENT (Post-Week 4)

**Task 5.1: Staged Rollout**
- [ ] Week 1: Deploy to dev environment
- [ ] Week 2: Deploy to staging environment
- [ ] Week 3: Deploy to production with feature flag (if needed)
- [ ] Rollback plan: Revert to v3.1 `.ai/agents.md` if critical issues found

**Task 5.2: Post-Deployment Monitoring**
- [ ] Monitor logs for unexpected error patterns
- [ ] Track command success rates (all 12 commands)
- [ ] Monitor memory usage + context window efficiency
- [ ] Collect user feedback on speed + reliability improvements

---

## RESOURCE ALLOCATION

| Phase | Owner | Duration | Effort | Notes |
|-------|-------|----------|--------|-------|
| Phase 1: Contracts | Product + Engineering Lead | 1 week | 5 person-days | Review + consensus building |
| Phase 2A: Scraper Refactor | Senior Engineer #1 | 5 days | 5 person-days | High-risk, careful testing |
| Phase 2B: Creator Refactor | Senior Engineer #2 | 5 days | 4 person-days | Moderate risk |
| Phase 2C: SEO Refactor | Senior Engineer #3 | 3 days | 2 person-days | Lower risk |
| Phase 2D: Workflow Refactor | Senior Engineer #4 | 4 days | 3 person-days | Critical for gates, testing |
| Phase 2E: Brand Refactor | Junior Engineer + Code Review | 3 days | 2 person-days | Moderate complexity |
| Phase 3: Memory + Integration | Senior Engineer #1 | 4 days | 4 person-days | Integration complexity |
| Phase 4: Testing + Validation | QA + Senior Engineer #2 | 5 days | 5 person-days | Comprehensive testing |
| Phase 5: Rollout | DevOps + Product | 2 weeks | 3 person-days | Monitoring + feedback |
| **Total** | — | **4 weeks** | **~33 person-days** | 1 product lead + 4-5 engineers |

---

## SUCCESS METRICS

| Metric | Target | Measurement |
|--------|--------|-------------|
| Zero user-facing changes | 100% command compatibility | Verify all 12 commands work identically |
| Agent responsibility clarity | No ambiguous ownership | Data ownership audit: 100% of files have explicit owner |
| Error recovery clarity | Deterministic cascades | Code review: All error paths have defined owner |
| Performance improvement | 3x faster `/review` | Benchmark: Sequential 20s → Parallel ~6s |
| Memory efficiency | 40% lower token use | Memory profiling: explicit manager reduces bloat |
| Test coverage | ≥85% code coverage | pytest coverage report |
| Cross-platform parity | Same behavior on 3+ CLIs | Manual testing on Claude, Cursor, Copilot |
| Debugging time | 50% faster issue diagnosis | Compare debugging time v3.1 vs v3.2 (5 incident scenarios) |

---

## RISK MITIGATION

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Refactoring breaks existing commands | Low (well-scoped) | High (user downtime) | Comprehensive integration tests before rollout |
| Performance regression | Low (parallel gates faster) | Medium | Benchmark phase 4; rollback plan ready |
| Memory manager doesn't prevent file injection | Low (explicit design) | High (token waste) | Unit tests + code review + integration tests |
| Cross-platform parity issues | Medium (3+ CLI tools) | Medium | Test on all 3 platforms in Phase 4 |
| Schedule slippage | Medium (4-week timeline) | Medium | Assign dedicated resources; daily standups |

---

## APPENDIX: FILE STRUCTURE POST-REFACTOR

```
.ai/scripts/
├── core/
│   ├── cli_router.py                    [NEW] Parse commands, route to agents
│   ├── workflow_orchestrator.py          [REFACTORED] Orchestrate agent chains
│   ├── memory_manager.py                 [NEW] Context compression + session state
│   └── error_handler.py                  [EXISTING/CLARIFIED] Error cascade logic
│
├── scraper/
│   ├── delta_detector.py                 [NEW] ONLY delta detection
│   ├── scraper_engine.py                 [REFACTORED] Fetch + parse + state write
│   ├── ethics_compliance.py              [REFACTORED] robots.txt + rate limit + PII
│   └── content_parser.py                 [EXISTING]
│
├── creator/
│   ├── blueprint_architect.py            [EXISTING]
│   ├── content_generator.py              [REFACTORED] Generation + originality only
│   ├── brand_voice_applier.py            [NEW] ONLY voice validation
│   └── compare_engine.py                 [EXISTING/CLARIFIED]
│
├── seo/
│   ├── seo_optimizer.py                  [REFACTORED] keyword + technical auditors
│   ├── image_seo_auditor.py              [REFACTORED] Alt-text + WebP + schema
│   └── readability_fixer.py              [EXISTING]
│
├── brand/
│   ├── voice_validator.py                [EXISTING/CLARIFIED]
│   ├── tone_analyzer.py                  [EXISTING/CLARIFIED]
│   └── drift_detector.py                 [EXISTING/CLARIFIED]
│
└── workflow/
    ├── quality_checker.py                [REFACTORED] Parallel gates
    ├── approval_gate.py                  [NEW] ONLY approval logic
    ├── export_packager.py                [EXISTING/CLARIFIED]
    └── archive_manager.py                [EXISTING/CLARIFIED]
```

---

## APPROVAL SIGN-OFF

- [ ] Product Lead: Approves architecture + timeline
- [ ] Engineering Lead: Approves technical approach + resource allocation
- [ ] QA Lead: Approves testing strategy
- [ ] DevOps Lead: Approves rollout plan

---

**Next Step:** Schedule kickoff meeting to begin Phase 1 (contracts definition).

