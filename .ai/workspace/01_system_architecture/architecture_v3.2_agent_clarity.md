# Sovereign Workspace v3.2: Clarified Agent Architecture
**Status:** Revision for Approval | **Focus:** Eliminate Agent Overlap, Establish Clear Ownership  
**Problem Addressed:** v3.1 had ambiguous responsibility boundaries between sub-agents; scaled poorly  
**Solution:** Hierarchical responsibility model with single-purpose agents and explicit handoff contracts

---

## 1. CRITICAL GAPS IN v3.1 & PROPOSED FIXES

### v3.1 Issues (Current)
| Issue | Symptom | Risk |
|-------|---------|------|
| **Overlapping sub-agents** | `scraper-agent` + `delta-sync-agent` both claim URL delta detection | Duplicate work, missed edge cases, unpredictable failures |
| **Unclear error ownership** | Which agent retries on 429? `scraper-agent` or `ethics-compliance`? | Silent failures, inconsistent recovery |
| **Content flow ambiguity** | Does `creator-agent` or `brand-agent` apply voice rules first? | Tone drift, reprocessing loops |
| **Sync state management** | `sync-status.json` updated by both scraper and delta-sync — which is authoritative? | Data corruption, stale timestamps |
| **Memory layer undefined** | Guide agent vs. workflow agent — who compresses context? | Context bloat, token waste |

### v3.2 Solution
- **Single Responsibility Principle:** Each agent owns exactly one decision boundary
- **Explicit Handoff Contracts:** Input spec → Agent logic → Output spec → Next agent
- **Authoritative Owners:** One agent "owns" each data file (e.g., `scraper-agent` owns `sync-status.json`, only it writes)
- **Error Recovery Cascades:** Errors bubble up through a defined hierarchy; clear who retries
- **Memory Centralization:** `guide-agent` alone manages context compression and session state

---

## 2. REVISED AGENT HIERARCHY & RESPONSIBILITY MODEL

### Tier 1: Gateway Agents (Command Entry Points)
These agents parse intent, load context, and delegate to execution agents. **They never perform work directly.**

```
┌─────────────────────────────────────────────────────────────────┐
│                      GUIDE AGENT (Router)                        │
│  - Parses natural command → Intent + Entities + Missing Context  │
│  - Loads .ai/memory/ + session state                             │
│  - Routes to Primary Execution Agent (see Tier 2)                │
│  - Manages token budget, suggests next steps                     │
│  - OWNS: state.json, context-cache/, token tracking             │
│  - ERROR OWNER: Catches parse failures, fallback Q&A             │
└─────────────────────────────────────────────────────────────────┘
```

**Responsibilities:**
- Parse `/research competitors` → Determine if new research or update existing
- Parse `/sync` → Load `index.json`, identify enabled competitors
- Parse `/create blog posts about [topic]` → Extract topic, validate context, load brand voice
- Reject ambiguous input with exactly 1 clarifying question
- Update `state.json` after each command completes

**Output Contract:** JSON routing payload with parsed intent, entity list, context summary

---

### Tier 2: Primary Execution Agents
Each agent owns one major workflow. Sub-agents report only to their primary agent.

#### `RESEARCH AGENT` (Command: `/research competitors`)
**Owns:** Competitor discovery, profiling, initial data extraction  
**Authoritative Files:** `content/sovereign/scraped/*/info.md`, `index.json`  
**Handles:** Research intent, profile generation, external discovery  
**Error Owner:** Handles discovery failures (site unreachable, no contact info found)  

**Workflow:**
```
guide-agent 
  → [parses: /research competitors]
  → research-agent [owns entire flow]
    ├─ SUB: discovery-engine [web search, competitive profiling]
    │   └─ Input: Sovereign brand positioning from reference/
    │   └─ Output: {candidate_competitors: [{name, url, niche, confidence_score}]}
    │   └─ Validation: confidence_score ≥ 70%, site responds in <5s
    │
    ├─ SUB: profile-builder [extracts contact, social, service types]
    │   └─ Input: list of URLs, info extraction templates
    │   └─ Output: info.md with {name, url, niche, services, contact, socials}
    │   └─ Validation: ≥ 3 data points extracted, no PII leaked
    │
    └─ Writes: content/sovereign/scraped/[slug]/info.md, updates index.json
         └─ Validation: JSON schema match, no duplicates
         └─ Error recovery: If write fails 3x, logs diagnostic, pauses
```

**Handoff Contract:**
- **INPUT:** Parsed intent, brand positioning from `reference/`, active `index.json`
- **OUTPUT:** New/updated `content/sovereign/scraped/[slug]/` folder + `index.json` entry with `{slug, url, niche, sync_enabled: true, last_sync: null}`
- **NEXT:** guide-agent suggests `/scrape all competitors blog` or `/sync`

---

#### `SCRAPER AGENT` (Commands: `/scrape *`, `/sync`)
**Owns:** URL discovery, delta detection, ethical scraping, asset management  
**Authoritative Files:** `sync-status.json`, `scraped/content/`, `scraped/images/`, `.ai/logs/sync-delta.jsonl`  
**Handles:** All scraping, delta logic, rate limiting, PII filtering  
**Error Owner:** Handles network failures, 429s, malformed HTML  

**Workflow:**
```
guide-agent
  → [parses: /sync OR /scrape all competitors blog]
  → scraper-agent [owns entire scraping flow]
    ├─ SUB: delta-detector [ONLY reads sync-status.json, compares against live]
    │   └─ Input: index.json (enabled competitors), sync-status.json per competitor
    │   └─ Logic: Hash URLs, compare publish dates, identify delta: {new, updated, deleted}
    │   └─ Output: delta-payload.json {competitor_slug: {new_urls: [], updated_urls: []}}
    │   └─ Validation: 0 false positives (only deltas >24h old are real), <10% false delta rate
    │   └─ ERROR: If sitemap unreachable, fallback to RSS; if both fail, mark competitor stale
    │
    ├─ SUB: ethical-crawler [respects robots.txt, enforces delays, filters PII]
    │   └─ Input: delta-payload, competitor URLs, robots.txt rules
    │   └─ Logic: Fetch only delta URLs, 2s baseline delay, exponential backoff on 429
    │   └─ Output: Raw HTML per URL, asset manifest (images, PDFs)
    │   └─ Validation: 100% robots.txt pass, 0 PII in output, rate limit observed
    │   └─ ERROR: If 429 after backoff, skip URL, log retry-able reason
    │
    ├─ SUB: content-parser [structure extraction: metadata, body, links]
    │   └─ Input: Raw HTML per URL
    │   └─ Output: Structured Markdown {file_path, metadata, body, word_count, publish_date}
    │   └─ Validation: Valid Markdown, <5% malformed HTML tolerance
    │   └─ ERROR: Malformed → skip, log path + error
    │
    ├─ SUB: asset-handler [WebP conversion, lazy-load prep, deduplication]
    │   └─ Input: Image URLs from parsed content, asset manifest
    │   └─ Output: .webp files, lazy-load-ready HTML refs, dedup manifest
    │   └─ Validation: No duplicate images (MD5 hash check), valid WebP
    │   └─ ERROR: Conversion fail → skip image, mark in manifest
    │
    ├─ SUB: sync-state-writer [ONLY agent that writes sync-status.json]
    │   └─ Input: delta-payload, timestamp, scrape results, error log
    │   └─ Output: Updated sync-status.json {last_sync, total_scraped, new_count, errors}
    │   └─ Validation: Timestamp ≤ 5min ago, counts match actual outputs
    │   └─ ERROR: If write fails, rollback scraped files, preserve old sync-status.json
    │
    └─ Writes: content/sovereign/scraped/[slug]/scraped/*, sync-status.json, logs/sync-delta.jsonl
         └─ Validation: Dedup check (no URL appears twice), all files versioned
         └─ ERROR: If >3 write failures, pause and alert
```

**Handoff Contract:**
- **INPUT:** Parsed command (scope: blog only? all? specific competitor?), `index.json`, competitor folders
- **OUTPUT:** Updated `scraped/content/` + `images/`, `sync-status.json`, `.ai/logs/sync-delta.jsonl` entry
- **NEXT:** guide-agent suggests `/create content` or `/compare sovereign vs competitor` or `/sync` again in 24h

**Critical Ownership Rules:**
- ✅ `scraper-agent` ONLY writes `sync-status.json`
- ✅ `scraper-agent` ONLY writes `.ai/logs/sync-delta.jsonl`
- ❌ No other agent touches these files
- ❌ `delta-detector` reads only, does not write

---

#### `CREATOR AGENT` (Commands: `/create *`, `/compare`)
**Owns:** Original content generation, blueprint selection, side-by-side comparison  
**Authoritative Files:** `content/`, `content/sovereign/comparisons/`  
**Handles:** Content drafting, structural inspiration (not copying), comparison analysis  
**Error Owner:** Handles generation failures, low originality scores, brand voice drift  

**Workflow:**
```
guide-agent
  → [parses: /create blog posts about [topic] OR /compare sovereign vs [name]]
  → creator-agent [owns entire generation flow]
    │
    ├─ [IF /create]
    │  ├─ SUB: blueprint-architect [selects structural template from competitors + keyword research]
    │  │   └─ Input: Topic, brand voice rules, competitor gap analysis, keyword map
    │  │   └─ Logic: Find gap in competitor coverage (what they don't cover well?), select 1 blueprint structure
    │  │   └─ Output: outline.json {sections: [{heading, purpose, keywords, inspiration_source}]}
    │  │   └─ Validation: Outline ≤ 80% structurally similar to ANY competitor (differs in flow/depth)
    │  │   └─ ERROR: No gap found → fallback to generic best-practice outline
    │  │
    │  ├─ SUB: content-generator [writes original body, applies keywords, enforces voice]
    │  │   └─ Input: outline.json, brand voice matrix, keyword targets
    │  │   └─ Logic: Generate Markdown body following outline, 1-2% keyword density, Flesch ≥ 65
    │  │   └─ Output: Draft Markdown {frontmatter, body, assets-refs}
    │  │   └─ Validation: Originality ≤ 15% semantic similarity vs any competitor
    │  │   └─ ERROR: Similarity > 15% → Rewrite with structural shift + new examples
    │  │
    │  ├─ SUB: brand-voice-applier [applies tone matrix, enforces glossary, fixes drift]
    │  │   └─ Input: Draft Markdown, content/sovereign/reference/brand-voice/
    │  │   └─ Logic: Check lexicon, sentence pacing, CTA style, tone intensity
    │  │   └─ Output: Voice-adjusted Markdown {tone_score, drift_flags, applied_rules}
    │  │   └─ Validation: Tone compliance ≥ 92%, no glossary violations
    │  │   └─ ERROR: Tone < 92% → Auto-rewrite, flag for `/review`
    │  │
    │  └─ Writes: content/[type]/[slug].md, metadata.json
    │     └─ Output Contract: Ready for `/optimize images` + `/polish` stages
    │
    └─ [IF /compare]
       └─ SUB: comparison-analyst [structural + tonal side-by-side diff]
           └─ Input: Sovereign draft + competitor source, brand voice matrix
           └─ Logic: H-structure compare, CTA style compare, tone intensity compare, keyword overlap
           └─ Output: content/sovereign/comparisons/sovereign_vs_[competitor].md[name].md {sections: [{comparison, gap, recommendation}]}
           └─ Validation: Diffs are actionable (not just "different")
           └─ ERROR: Insufficient data → marks as "incomplete, needs review"
           └─ Writes: content/sovereign/comparisons/*.md, diff-logs.jsonl entry
```

**Handoff Contract:**
- **INPUT:** Parsed intent (topic or comparison target), brand voice rules, competitor data (for inspiration only), keyword maps
- **OUTPUT:** Draft Markdown in `content/` or `content/sovereign/comparisons/`, with metadata and tone score
- **NEXT:** guide-agent suggests `/optimize images` → `/polish content` → `/review` → `/approve`

**Critical Ownership Rules:**
- ✅ `creator-agent` ONLY creates content (never scrapes competitors)
- ✅ Must load `content/sovereign/reference/brand-voice/` before every generation
- ❌ Does not write `sync-status.json` or manage scraper state

---

#### `SEO AGENT` (Commands: `/polish content`, `/optimize images`)
**Owns:** On-page optimization, keyword mapping, readability, image SEO, technical fixes  
**Authoritative Files:** `content/`, `assets-seo.json`, `seo-meta.json`  
**Handles:** SEO validation, keyword density, heading structure, alt-text generation  
**Error Owner:** Handles readability failures, keyword conflicts, image format issues  

**Workflow:**
```
guide-agent
  → [parses: /polish content in content/ OR /optimize images]
  → seo-agent [owns entire SEO pipeline]
    │
    ├─ [IF /optimize images]
    │  └─ SUB: image-seo-auditor [generates alt-text, WebP, lazy-load, schema]
    │      └─ Input: All images in content/, image manifest
    │      └─ Logic: Generate descriptive alt ≤125 chars (with keyword if relevant), convert to WebP, inject lazy-load + schema
    │      └─ Output: Updated .md refs, assets-seo.json {image_path, alt, format, size, schema_type}
    │      └─ Validation: 100% alt-text, 100% WebP, WCAG AA contrast (sampled)
    │      └─ ERROR: Conversion fail → skip image, log path
    │
    └─ [IF /polish content]
       ├─ SUB: keyword-auditor [density check, cannibalization, placement]
       │   └─ Input: Draft Markdown, target keyword list
       │   └─ Logic: Check density (1-2%), primary keyword in H1/meta, semantic diversity
       │   └─ Output: {keyword_gaps, density_violations, placement_fixes}
       │   └─ Validation: No cannibalization (same keyword in 2+ pages)
       │   └─ ERROR: Cannibalization → flag for manual review
       │
       ├─ SUB: technical-auditor [H-structure, meta, readability]
       │   └─ Input: Draft Markdown
       │   └─ Logic: Validate H1→H6 hierarchy, generate meta description, calculate Flesch-Kincaid
       │   └─ Output: seo-meta.json {title, meta_description, h_structure_valid, flesch_score}
       │   └─ Validation: H-structure valid, Flesch ≥ 65
       │   └─ ERROR: Flesch < 65 → Auto-simplify sentences, recount
       │
       └─ Writes: Updated content/[type]/[slug].md + seo-meta.json
           └─ Validation: All gates pass before output
           └─ Output Contract: Ready for `/review` stage
```

**Handoff Contract:**
- **INPUT:** Draft Markdown in `content/`, keyword maps, image manifest
- **OUTPUT:** Optimized Markdown + `seo-meta.json` + `assets-seo.json` with all gates passed
- **NEXT:** guide-agent suggests `/review` → `/approve`

**Critical Ownership Rules:**
- ✅ `seo-agent` ONLY modifies `content/` for optimization (never content creation)
- ❌ Does not write brand voice files or scraper state

---

#### `BRAND AGENT` (Commands: `/extract brand voice`, `/refine brand voice`)
**Owns:** Tone analysis, voice rule authoring, drift detection  
**Authoritative Files:** `content/sovereign/reference/brand-voice/`, `voice_refinement.md`, `style_rules.md`  
**Handles:** Tone extraction, glossary enforcement, voice validation  
**Error Owner:** Handles ambiguous tone, conflicting rules, glossary gaps  

**Workflow:**
```
guide-agent
  → [parses: /extract brand voice from [source] OR /refine brand voice]
  → brand-agent [owns entire brand voice pipeline]
    │
    ├─ [IF /extract]
    │  └─ SUB: tone-analyzer [extracts lexicon, pacing, CTA style from samples]
    │      └─ Input: Source (existing content, competitor sample, or text)
    │      └─ Logic: Analyze sentence length, adjective intensity, CTA phrasing, formality level
    │      └─ Output: voice-profile.json {lexicon, pacing, cta_style, tone_intensity, examples}
    │      └─ Validation: ≥ 10 samples analyzed, clusters match
    │      └─ Writes: content/sovereign/reference/brand-voice/voice_refinement.md
    │
    └─ [IF /refine]
       ├─ SUB: drift-detector [scans recent content/ for tone violations]
       │   └─ Input: Recent .md files in content/, style_rules.md
       │   └─ Logic: Scan for glossary violations, tone intensity outliers, CTA mismatches
       │   └─ Output: drift-report.json {violations: [{file, line, rule, severity}]}
       │   └─ Validation: Report is actionable (not >20% false positives)
       │   └─ ERROR: >20% false positives → Manual review needed
       │
       ├─ SUB: rule-updater [consolidates rules, detects conflicts]
       │   └─ Input: drift-report.json, existing style_rules.md
       │   └─ Logic: Merge new patterns, flag conflicting rules
       │   └─ Output: Updated style_rules.md {rules: [{name, pattern, examples, priority}]}
       │   └─ Validation: No rule conflicts, all rules tested on ≥3 samples
       │   └─ Writes: content/sovereign/reference/brand-voice/style_rules.md + glossary.md
    │
    └─ Output Contract: Updated brand voice files ready for next `/create` or `/polish`
```

**Handoff Contract:**
- **INPUT:** Source text for extraction, or existing content for refinement
- **OUTPUT:** Updated `content/sovereign/reference/brand-voice/*` files with new or refined rules
- **NEXT:** guide-agent suggests new `/create` with updated voice, or `/polish` existing content

---

#### `WORKFLOW AGENT` (Commands: `/review`, `/approve`, `/export`, `/archive`)
**Owns:** Quality gates, approval workflow, archival, export coordination  
**Authoritative Files:** `logs/quality-report-[timestamp].json`, `archive/`, `content/sovereign/outputs/`  
**Handles:** Pipeline orchestration, approval logic, data archival, export formatting  
**Error Owner:** Handles gate failures, approval reversals, archival rollbacks  

**Workflow:**
```
guide-agent
  → [parses: /review OR /approve OR /export OR /archive old content]
  → workflow-agent [owns entire workflow orchestration]
    │
    ├─ [IF /review]
    │  └─ SUB: quality-checker [runs all gates in parallel]
    │      └─ Input: Staged content (ready for review)
    │      └─ Gates:
    │         1. SEO validator: score ≥ 85% (keyword, meta, H-structure)
    │         2. Brand validator: tone compliance ≥ 92%
    │         3. Readability validator: Flesch ≥ 65
    │         4. Image SEO validator: 100% alt-text, WebP, schema
    │         5. Originality validator: ≤ 15% similarity to any source
    │      └─ Output: quality-report.json {gate: {passed: bool, score: float, violations: []}}
    │      └─ Validation: All gates run, report is deterministic
    │      └─ ERROR: If gate fails → Output violation list, suggest fixes
    │      └─ Writes: logs/quality-report-[timestamp].json
    │
    ├─ [IF /approve]
    │  └─ SUB: approval-gate [checks quality-report, locks content]
    │      └─ Input: quality-report.json (must exist and all gates pass)
    │      └─ Logic: If all gates ≥ thresholds → lock content, set approved_at timestamp
    │      └─ Output: Lock marker in metadata.json {approved: true, approved_at, approved_by}
    │      └─ Validation: Report exists, all gates passed
    │      └─ ERROR: Gates not passed → Reject approval, output which gates failed
    │      └─ Writes: Updated content metadata
    │
    ├─ [IF /export]
    │  └─ SUB: export-packager [generates CSV + CMS pack]
    │      └─ Input: Approved content (approved: true in metadata)
    │      └─ Logic: Validate schema, bundle Markdown + metadata, generate CSV
    │      └─ Output: content/sovereign/outputs/{csv-exports/, cms-packs/} with valid files
    │      └─ Validation: CSV schema 100% match, no broken links
    │      └─ ERROR: If not approved → Block export, ask for `/approve` first
    │      └─ Writes: content/sovereign/outputs/
    │
    └─ [IF /archive old content]
       └─ SUB: archive-manager [compresses files >30 days, updates index]
           └─ Input: Content files, cutoff date (>30 days)
           └─ Logic: Gzip old files, create pointer manifest, update archive-index.json
           └─ Output: archive/*.gz + archive-index.json {pointer: {original_path, archived_path, checksum}}
           └─ Validation: Checksum match, decompression verified
           └─ ERROR: If decompress fails → Rollback, preserve original
           └─ Writes: archive/, archive-index.json
```

**Handoff Contract:**
- **INPUT:** Staged content for review, or quality-report.json + manual approval decision, or approved content for export
- **OUTPUT:** Quality report (on `/review`) → Lock marker (on `/approve`) → CSV/CMS pack (on `/export`)
- **NEXT:** guide-agent suggests appropriate next step based on gate results

---

### Tier 3: Support & Utility Agents
These agents provide cross-cutting services; they are never called directly but invoked by primary agents.

#### `MEMORY MANAGER` (Invoked by guide-agent only)
**Owns:** Context compression, session state, token budgeting  
**Called By:** `guide-agent` before & after commands  
**Purpose:** Prevent raw file injection into LLM context; track session state; suggest memory savings

**Rules:**
- Never loads raw competitor scraped files into context
- Always uses `.ai/memory/context-cache/` summaries + file pointers
- Tracks token usage per command; suggests `/memory save` if >70% used
- Clears temp cache after command completes

---

## 3. ERROR RECOVERY CASCADE (Who Retries What)

When a command fails, errors cascade up the agent hierarchy. Each agent knows its retry responsibility.

```
Command Failure → Who Retries?

/sync fails to detect deltas
  → scraper-agent / delta-detector owns retry
  → Retry logic: Fallback from sitemap to RSS; if both fail, check manual URL list
  → Max 3 retries with exponential backoff
  → If still fails: Log to sync-delta.jsonl as "stale", mark competitor for manual check

/create blog posts fails on SEO score < 85%
  → creator-agent / content-generator owns first retry (rewrite with different approach)
  → If still < 85% after 2 retries → escalate to seo-agent / technical-auditor
  → If still < 85% after 3 attempts total → flag in quality-report, ask for `/revise [feedback]`

/approve fails (gates not passed)
  → workflow-agent / approval-gate owns decision: which gate failed?
  → Output specific gate that failed + violation list
  → Recommend which agent to re-invoke: seo-agent for SEO, brand-agent for tone, etc.
  → Do NOT retry automatically; ask user for `/revise`

Scraper gets 429 Too Many Requests
  → scraper-agent / ethical-crawler owns retry with exponential backoff
  → Retries: Wait 5s, 10s, 20s, then skip URL and log
  → If >50% of competitor URLs get 429 → Mark competitor as temporarily blocked, suggest manual check

Content parsing fails (malformed HTML)
  → scraper-agent / content-parser owns decision: retry or skip
  → Retry once with different parser; if still fails, skip URL, log path + error
  → Do NOT block entire scrape; continue with other URLs
```

---

## 4. DATA FILE OWNERSHIP (Who Writes What)

Each data file is owned by exactly one agent. Only that agent writes; others read only.

| Data File | Authoritative Owner | Read-Only Agents | Write Rule | Backup Rule |
|-----------|-------------------|------------------|-----------|------------|
| `index.json` | `research-agent` | All agents | Add competitor on discovery; never overwrite existing | Git commit after each update |
| `sync-status.json` | `scraper-agent` | guide-agent, workflow-agent | Update ONLY after scrape completes + validation | Preserve old on write failure |
| `scraped/content/*` | `scraper-agent` | creator-agent (for inspiration) | Version files as `_v2.md`, `_v3.md` | Delta log in sync-delta.jsonl |
| `content/sovereign/reference/brand-voice/*` | `brand-agent` | creator-agent, seo-agent | Append new rules; never delete old rules | Git history preserved |
| `content/*` | `creator-agent` | seo-agent, workflow-agent | Create draft; seo-agent optimizes in-place | metadata.json version tracking |
| `seo-meta.json` | `seo-agent` | workflow-agent | Update after polish; never overwrite by creator-agent | Backup on validation failure |
| `content/sovereign/comparisons/*` | `creator-agent` | workflow-agent | Create + version | Git history |
| `logs/*.jsonl` | `guide-agent` | All agents (append-only) | Each agent appends own log entries | Rotation at 100MB per file |
| `quality-report.json` | `workflow-agent` | All agents (read-only) | Overwrites on each `/review` | Backups in logs/ |
| `archive/*` | `workflow-agent` | guide-agent (pointer loading) | Compress + create manifest | Checksum verification mandatory |
| `.ai/memory/state.json` | `guide-agent` | All agents (read-only) | Update after each command | Rollback on corruption |

**Rule:** If agent X needs to write data owned by agent Y, it writes to a temp file and calls agent Y's writer function. No direct writes across ownership boundaries.

---

## 5. COMMAND FLOW MAPPING (Route → Primary Agent → Sub-Agents → Output)

| Command | Primary Agent | Sub-Agent 1 | Sub-Agent 2 | Sub-Agent 3 | Output File | Approval Required |
|---------|---------------|-------------|-------------|-------------|------------|-------------------|
| `/research competitors` | research-agent | discovery-engine | profile-builder | — | `content/sovereign/scraped/*/info.md`, `index.json` | No (auto-creates) |
| `/scrape all competitors blog` | scraper-agent | delta-detector | ethical-crawler → content-parser | asset-handler | `scraped/content/blog/` | No (raw data) |
| `/sync` | scraper-agent | delta-detector | ethical-crawler → content-parser | sync-state-writer | `sync-status.json`, `.ai/logs/sync-delta.jsonl` | No (state only) |
| `/create blog posts about [topic]` | creator-agent | blueprint-architect | content-generator | brand-voice-applier | `content/sovereign/blog-posts/` | **YES** (via `/review`) |
| `/compare sovereign vs [name]` | creator-agent | comparison-analyst | — | — | `content/sovereign/comparisons/` | **YES** (via `/review`) |
| `/polish content in content/` | seo-agent | keyword-auditor | technical-auditor | — | Updated `content/` | **YES** (gates must pass) |
| `/optimize images in content/` | seo-agent | image-seo-auditor | — | — | `assets-seo.json` | **YES** (100% alt check) |
| `/extract brand voice from [source]` | brand-agent | tone-analyzer | — | — | `content/sovereign/reference/brand-voice/` | No (auto-updates) |
| `/refine brand voice` | brand-agent | drift-detector | rule-updater | — | `content/sovereign/reference/brand-voice/` | No (auto-updates) |
| `/review` | workflow-agent | quality-checker | — | — | `logs/quality-report-[timestamp].json` | No (output only) |
| `/approve` | workflow-agent | approval-gate | — | — | metadata.json lock | **YES** (human decision) |
| `/export` | workflow-agent | export-packager | — | — | `content/sovereign/outputs/` | Blocked if not approved |
| `/archive old content` | workflow-agent | archive-manager | — | — | `archive/` | No (auto-archives) |

---

## 6. IMPLEMENTATION CHECKLIST (v3.2 Rollout)

- [ ] **Agent Responsibilities Document** (this file) reviewed and approved by product + engineering
- [ ] **Data Ownership Registry** updated in `.ai/config.md` (which agent owns which file)
- [ ] **Error Recovery Flowchart** implemented in `.ai/scripts/core/error_handler.py` (clear retry ownership)
- [ ] **Sub-Agent Contracts** defined in `.ai/agents.md` (input spec → output spec for each sub-agent)
- [ ] **Quality Gate Validator** (`.ai/scripts/workflow/quality_checker.py`) verifies all gates in parallel, not sequentially
- [ ] **Memory Manager** refactored to prevent raw file loading into LLM context (`.ai/memory_manager.py`)
- [ ] **Command Router** updated to unambiguously map each command to single primary agent (`.ai/scripts/core/cli_router.py`)
- [ ] **E2E Tests** written for each agent independently + integration tests for agent chains
- [ ] **Documentation** (this file) embedded in `.ai/AGENT_CLARITY.md` for reference during execution
- [ ] **Cross-Platform Testing** on Claude CLI, Cursor, Copilot to verify parity

---

## 7. BACKWARD COMPATIBILITY & MIGRATION NOTES

**v3.1 → v3.2 is a structural refactor; command syntax unchanged.**

| v3.1 Behavior | v3.2 Behavior | User-Facing Change |
|---------------|---------------|-------------------|
| Multiple agents could write `sync-status.json` | Only `scraper-agent` writes | None (internal) |
| Unclear error owner on 429 | Clear cascade: scraper-agent retries | Improved reliability, same CLI |
| Brand voice applied by `creator-agent` | Brand voice applied by `creator-agent` BUT validated by separate sub-agent | Same output; clearer logic |
| Memory layer unclear | `memory-manager` sub-agent owns all compression | Faster context loading, same UX |

**Rollout Strategy:**
1. Deploy updated `.ai/agents.md` with clear responsibility boundaries
2. Refactor scripts incrementally (one agent at a time)
3. Run integration tests after each agent refactor
4. No user-facing changes during rollout

---

## 8. ACCEPTANCE CRITERIA FOR v3.2

- [ ] Each agent has exactly one primary responsibility (no overlap)
- [ ] Data ownership is unambiguous (one authoritative owner per file)
- [ ] Error recovery paths are deterministic and logged
- [ ] Sub-agents have explicit input/output contracts (JSON specs)
- [ ] Quality gates run in parallel, not sequentially (faster `/review`)
- [ ] Memory manager prevents raw file injection into context
- [ ] All commands work end-to-end with new architecture
- [ ] Cross-platform execution tested on ≥3 CLI tools
- [ ] No performance regression vs v3.1

---

**Status:** Ready for engineering review & implementation planning

