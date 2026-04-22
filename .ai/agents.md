# Sovereign Workspace — Agent Registry v3.2
# DEPRECATED MONOLITH NOTICE
# This file is maintained for backward compatibility only.
# Canonical sources:
# - .ai/registry/agents.registry.json
# - .ai/agents/*.md
# - .ai/compat/agents.legacy-map.json
# ============================================================
# DO NOT LOAD DIRECTLY.
# Startup authority is defined in `CLAUDE.md`.
# This file is a compatibility reference for legacy tooling.
# Single Responsibility Principle: each agent owns one decision boundary.
# ============================================================

---

## TIER 1 — GATEWAY AGENT

### `guide-agent`
**Role:** Command router, session manager, context guardian.
**Owns:** `.ai/memory/state.json`, `.ai/memory/context-cache/`, token budget tracking.
**Never performs work directly.** Delegates all execution to Tier 2 agents.

**Responsibilities:**
- Parse every user command → extract intent, entities, scope, missing context
- Load `.ai/memory/state.json` + relevant cache summaries before routing
- Route to exactly one primary Tier 2 agent per command
- Ask exactly ONE clarifying question if context is ambiguous (never multiple)
- After each command: compress results, update `state.json`, clear temp cache
- Always end response with: `💡 Suggested Next Step: [command]`
- Track token budget; warn at 70% usage; suggest `/memory save`

**Memory Rules:**
- NEVER load raw scraped files into LLM context
- ALWAYS load summarized cache pointers from `.ai/memory/context-cache/`
- ALWAYS load `content/sovereign/reference/brand-voice/style-rules.md` before any `/create` or `/polish`

---

## TIER 2 — PRIMARY EXECUTION AGENTS

### `research-agent`
**Trigger Commands:** `/research competitors`
**Owns:** `content/sovereign/scraped/*/info.md`, `content/sovereign/scraped/index.json`
**Single Responsibility:** Discover and profile competitor businesses.

**Sub-Agents:**
1. `discovery-engine` — Web search + relevance scoring for competitor candidates
2. `profile-builder` — Extracts name, URL, niche, services, contact, socials from each site
3. `trend-miner` — Detects recurring market signals across competitor datasets
4. `opportunity-scorer` — Scores whitespace opportunities by demand/saturation confidence
5. `intel-synthesizer` — Produces actionable intelligence briefs and snapshot summaries

**Input Contract:**
- `content/sovereign/reference/market-positioning.md` (Sovereign's niche, tier, geo, services)
- `content/sovereign/reference/brand-voice/style-rules.md` (for positioning comparison)
- `content/sovereign/scraped/index.json` (existing competitors to avoid duplicates)

**Output Contract:**
- `content/sovereign/scraped/[slug]/info.md` per discovered competitor
- Updated `content/sovereign/scraped/index.json` with new entries `{slug, url, niche, last_scraped: null, sync_enabled: true, status: "active"}`
- `content/sovereign/scraped/[slug]/analysis/intel-brief.md` for competitor-level intelligence runs
- `content/sovereign/comparisons/opportunity-map-[timestamp].md` for portfolio-level opportunity analysis
- `.ai/logs/intelligence-report-[timestamp].jsonl` append-only intelligence execution log

**Validation Gates:**
- Confidence score ≥ 70% per candidate
- Site responds in < 5s
- No duplicate slugs in `index.json`
- Minimum 3 data points extracted per profile

**Error Handling:**
- Site unreachable → skip, log reason, continue to next
- Ambiguous niche → ask one clarifying question, apply answer to all candidates
- < 3 candidates found → broaden search parameters before asking user
- Insufficient evidence for scoring → output `needs_more_data` confidence band and do not hard-rank

**Intelligence Commands (additive):**
- `/intel competitor [name]` → competitor-level brief from scraped + profile signals
- `/intel market snapshot` → cross-competitor trend summary for current workspace scope
- `/intel opportunities` → scored whitespace map with recommended content/comparison-[slug].md next steps

---

### `scraper-agent`
**Trigger Commands:** `/scrape *`, `/sync`
**Owns:** `content/sovereign/scraped/*/scraped/`, `content/sovereign/scraped/*/sync-status.json`, `.ai/logs/sync-delta.jsonl`
**Single Responsibility:** Detect content changes and ethically scrape only deltas.

**Sub-Agents (ordered pipeline):**
1. `delta-detector` — Reads `sync-status.json`, compares against live site; outputs delta payload
2. `ethical-crawler` — Fetches only delta URLs; respects `robots.txt`; enforces rate limits
3. `content-parser` — Converts raw HTML to structured Markdown
4. `asset-handler` — Downloads images, converts to WebP, deduplicates
5. `sync-state-writer` — **ONLY agent that writes `sync-status.json`** after validation

**Input Contract:**
- `content/sovereign/scraped/index.json` (scope: which competitors, which content types)
- `content/sovereign/scraped/[slug]/sync-status.json` (last sync state, URL hashes)

**Output Contract:**
- `content/sovereign/scraped/[slug]/scraped/content/{blog,projects,pages}/[slug].md`
- `content/sovereign/scraped/[slug]/scraped/images/` (WebP, deduped, `manifest.json`)
- Updated `content/sovereign/scraped/[slug]/sync-status.json`
- Appended entry to `.ai/logs/sync-delta.jsonl`

**Validation Gates:**
- 100% `robots.txt` compliance before any fetch
- 2s minimum delay between requests; exponential backoff on 429/503
- Zero PII in output (emails, phones, names auto-redacted)
- Zero duplicate URLs (MD5 hash check)
- False delta rate < 10%

**Error Handling:**
- 429 → backoff 5s, 10s, 20s → skip URL, log as retry-able
- Sitemap unreachable → fallback to RSS → if both fail, mark competitor as `stale` in `index.json`
- Malformed HTML → skip URL, log path, continue (never block full scrape)
- Write failure 3x → rollback scraped files, preserve old `sync-status.json`, alert

---

### `creator-agent`
**Trigger Commands:** `/create website pages`, `/create blog posts about [topic]`, `/create project pages`, `/create landing pages for [campaign]`, `/compare sovereign vs competitor [name]`
**Owns:** `content/`, `content/sovereign/comparisons/`, `.ai/logs/diff-logs-[timestamp].jsonl`
**Single Responsibility:** Generate original Sovereign content and comparison diffs.

**Sub-Agents — Create flow:**
1. `blueprint-architect` — Selects content structure based on gap analysis + topic
2. `content-generator` — Writes original Markdown body (keywords, flow, structure)
3. `brand-voice-applier` — Validates and adjusts tone against `content/sovereign/reference/brand-voice/`

**Sub-Agents — Compare flow:**
1. `comparison-analyst` — Runs structural + tonal + keyword diff vs competitor

**Input Contract:**
- `content/sovereign/reference/brand-voice/style-rules.md` (MANDATORY, loaded first)
- `content/sovereign/reference/brand-voice/glossary.md`
- `content/sovereign/_references/keyword-maps.md`
- `content/sovereign/scraped/[slug]/scraped/content/` (structural inspiration only — never copy)
- `.ai/templates/content-blueprints/[type].md`

**Output Contract:**
- `content/[type]/[slug].md` with YAML frontmatter `{title, meta_description, keywords, author, created_at, version, tone_score, originality_score, status: "draft"}`
- `content/sovereign/comparisons/sovereign_vs_[competitor].md` for compare commands

**Validation Gates:**
- Semantic similarity to any source ≤ 15%
- Brand voice compliance ≥ 92%
- Auto-retry with structural shift if originality fails; max 2 retries
- If tone < 92% after 2 retries → flag for `/review`, do not silently pass

**Error Handling:**
- No competitor data available → generate from brand positioning + keyword research alone
- Keyword map missing → mine from `content/sovereign/reference/market-positioning.md` + topic
- Tone drift > 8% → auto-retry with stricter voice matrix

---

### `seo-agent`
**Trigger Commands:** `/polish content in content/`, `/optimize images in content/`
**Owns:** `content/` (optimization only, never creation), `seo-meta.json`, `assets-seo.json`
**Single Responsibility:** On-page SEO optimization, image SEO, readability.

**Sub-Agents — Polish flow:**
1. `keyword-auditor` — Checks density (1-2%), placement, cannibalization
2. `technical-auditor` — Validates H-structure, generates meta, checks Flesch-Kincaid

**Sub-Agents — Image optimize flow:**
1. `image-seo-auditor` — Alt-text generation, WebP conversion, lazy-load, schema injection

**Input Contract:**
- Draft Markdown files in `content/`
- `content/sovereign/_references/keyword-maps.md`
- `.ai/templates/seo-meta-templates/meta-template.json`

**Output Contract:**
- Updated Markdown files (in-place optimization)
- `content/[type]/seo-meta.json` per content folder
- `content/assets-seo-[timestamp].json` (global image SEO registry)

**Validation Gates:**
- SEO score ≥ 85% (keyword, meta, H-structure combined)
- Flesch-Kincaid ≥ 65
- 100% image alt-text (≤ 125 chars, descriptive, keyword-aware where relevant)
- 100% WebP conversion
- Zero keyword cannibalization across `content/`

**Error Handling:**
- Flesch < 65 → auto-simplify sentences, re-measure, max 2 passes
- Image conversion fail → skip image, log path, continue
- Keyword cannibalization detected → flag specific files, do not auto-resolve (human decision)

---

### `brand-agent`
**Trigger Commands:** `/brand`, `/extract brand voice from [source]`, `/refine brand voice`
**Owns:** `content/sovereign/reference/brand-voice/` (all files), `.ai/logs/brand-session-[timestamp].json`
**Single Responsibility:** Define, maintain, and evolve Sovereign's tone, voice rules, and brand identity.

**Sub-Agents — Brand discovery flow (`/brand`):**
1. `brand-consultant` — Interactive 28-question interview across 7 phases; generates all brand foundation files
   - **Script:** `.ai/scripts/brand/brand_consultant.py`
   - **Protocol:** `.ai/brand-discovery.md`
   - **Question Bank:** `.ai/templates/brand-discovery/questions.json`
   - **Output:** `content/sovereign/reference/brand-voice/style-rules.md`, `content/sovereign/reference/brand-voice/glossary.md`, `content/sovereign/reference/brand-voice/tone-examples.md`, `content/sovereign/reference/brand-voice/voice-refinement.md`, `.ai/logs/brand-session-[timestamp].json`
2. `brand-interviewer` — Meeting-mode facilitator for discovery sessions
   - Handles phase transitions, clarifying follow-ups, and answer confidence checks
   - Keeps user in one-question-at-a-time interview flow
3. `brand-synthesizer` — Converts answers into operational brand rules
   - Produces concise “voice decisions” and ties each to writing behavior
   - Ensures outputs are usable by creator-agent and seo-agent without ambiguity
4. `brand-governance-checker` — Consistency guard before write
   - Detects contradictions between positioning, tone, and glossary
   - Flags unresolved conflicts before final file generation

**Sub-Agents — Extract flow (`/extract brand voice`):**
1. `tone-analyzer` — Extracts lexicon, pacing, CTA style from sample text

**Sub-Agents — Refine flow (`/refine brand voice`):**
1. `drift-detector` — Scans `content/` for tone violations against current rules
2. `rule-updater` — Merges new patterns, resolves conflicts, updates rule files

**Input Contract:**
- `/brand`: `.ai/templates/brand-discovery/questions.json` (question bank), interactive user input
- `/extract`: Source text (provided by user or from `content/` files)
- `/refine`: Existing `content/sovereign/reference/brand-voice/style-rules.md` and `glossary.md`

**Output Contract:**
- `/brand` → Full brand foundation suite (5 files + session log)
- `/extract` → `content/sovereign/reference/brand-voice/voice-refinement.md` (extraction results)
- `/refine` → Updated `content/sovereign/reference/brand-voice/style-rules.md`, updated `glossary.md`

**Pipeline Rule:**
- `/brand` MUST run before `/create *` if `market-positioning.md` is empty
- `/brand` proposes positioning updates, but does not overwrite `market-positioning.md` automatically
- `/brand workshop` is treated as the same command intent as `/brand` (meeting-mode alias)

**Validation Gates:**
- ≥ 10 text samples analyzed per extraction
- Rule conflicts resolved before writing (no two rules contradict)
- False positive rate < 20% in drift detection
- All new rules tested against ≥ 3 existing content samples

**Error Handling:**
- Insufficient samples → request more from user (exactly 1 ask)
- Conflicting rules detected → present conflict pair, ask user to arbitrate
- Drift > 20% false positives → mark report as needing manual review

---

### `workflow-agent`
**Trigger Commands:** `/review`, `/approve`, `/revise [feedback]`, `/export`, `/archive old content`, `/memory save | load | clear`
**Owns:** `.ai/logs/quality-report-[timestamp].json`, `archive/`, `content/sovereign/outputs/`, `.ai/memory/` (with guide-agent)
**Single Responsibility:** Quality gates, approval flow, archival, and export.

**Sub-Agents:**
1. `quality-checker` — Runs all 5 gates IN PARALLEL (SEO, Brand, Readability, Image SEO, Originality)
2. `approval-gate` — Checks `quality-report.json`, locks content, sets `approved_at`
3. `export-packager` — Bundles approved content → CSV + CMS pack
4. `archive-manager` — Compresses files > 30 days, updates `archive-index.json`

**Input Contract:**
- Staged content in `content/` with `status: "draft"` in frontmatter
- `.ai/logs/quality-report-[timestamp].json` (for `/approve` and `/export`)
- Content metadata (for archive cutoff date logic)

**Output Contract:**
- `/review` → `.ai/logs/quality-report-[timestamp].json` with per-gate scores + violations
- `/approve` → Content frontmatter updated `{status: "approved", approved_at: "[timestamp]"}`
- `/export` → `content/sovereign/outputs/csv-exports/[slug].csv`, `content/sovereign/outputs/cms-packs/[slug].zip`
- `/archive` → `archive/[type]/[slug].md.gz`, updated `archive/archive-index-[timestamp].json`

**Validation Gates (all run in PARALLEL):**
- SEO score ≥ 85%
- Brand voice compliance ≥ 92%
- Flesch-Kincaid ≥ 65
- Image SEO 100% (alt, WebP, schema)
- Originality ≤ 15% semantic similarity

**Hard Blocks:**
- `/export` blocked if `status` ≠ `"approved"` in content frontmatter
- `/approve` blocked if `quality-report.json` missing or any gate fails
- Archive rollback mandatory if checksum verification fails

**Error Handling:**
- Gate failure → output specific gate name + violation list + recommended fix command
- Export without approval → reject with message: "Run /review → /approve first"
- Archive corruption → rollback, preserve original files, log to `.ai/logs/workflow.jsonl`

---

## TIER 3 — MAINTENANCE & UTILITY AGENTS

### `antigravity-agent`
**Trigger Commands:** `/antigravity status`, `/antigravity sync`, `/antigravity learn`
**Owns:** `.cursor/hooks/`, `.cursor/commands/`, `.antigravity/commands/`
**Single Responsibility:** Workspace maintenance, command synchronization, and continual learning.

**Sub-Agents:**
1. `sync-engine` — Synchronizes commands between `.antigravity/commands/`, `.cursor/commands/`, and `.cursor/rules/`.
2. `continual-learning-engine` — Processes session transcripts for incremental learning.

---

### `memory-manager`
**Invoked by:** `guide-agent` only (before and after every command)
**Single Responsibility:** Context compression, session state, token budgeting.

**Rules (non-negotiable):**
- NEVER load raw scraped files into LLM context
- ALWAYS use file pointers + compressed summaries from `.ai/memory/context-cache/`
- Load only what the current command needs (scoped loading)
- Compress results after command completes; update `state.json`
- If token budget > 70% → suggest `/memory save` before continuing

---

## GLOBAL ENFORCEMENT RULES

1. **Pipeline order (enforced):** Research → Scrape/Sync → Create → Polish → Review → Approve → Export
2. **No command skips the pipeline** (e.g., no Export before Approve)
3. **All output versioning follows:** `.ai/versioning.md`
4. **All actions logged** to `.ai/logs/workflow.jsonl` with: timestamp, command, agent, status, duration
5. **Ethics layer always active:** robots.txt parsed before every scrape, PII filtered, rate-limited
6. **Zero verbatim copying:** structural inspiration only, similarity ≤ 15%
7. **Missing context** → exactly 1 clarifying question, then apply safe defaults
8. **Every response ends with:** `💡 Suggested Next Step: [specific command]`
