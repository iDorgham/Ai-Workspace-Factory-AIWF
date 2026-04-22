# Sovereign Workspace — Data Ownership Registry v3.2 (Multi-Tool Edition)
**Revision:** Phase 1 Multi-Tool Support  
**Last Updated:** 2026-04-13

Versioning authority: `.ai/versioning.md` (canonical).

Registry references:
- Agent ownership source: `.ai/registry/agents.registry.json`
- Sub-agent execution source: `.ai/registry/subagents.registry.json`
- Skill mapping source: `.ai/registry/skills.registry.json`
- Compatibility mapping: `.ai/compat/*.legacy-map.json`

---

## CRITICAL MULTI-TOOL RULE

**A file's owner is determined by:**
1. Which AGENT created it (creator-agent, seo-agent, etc.)
2. Which TOOL executed the agent (Claude, Gemini, Codex, etc.)

**Ownership example:**
- `content/sovereign/blog-posts/[slug]_[tool]_v[version].md` → Owned by creator-agent (via Claude)
- `content/sovereign/blog-posts/[slug]_[tool]_v[version].md` → Owned by creator-agent (via Gemini)
- Both are valid outputs; user chooses which to use

---

## OWNERSHIP MATRIX (Multi-Tool)

| File / Path | Owner Agent | Tool(s) | Write Rule | Versioning | On Write Failure |
|-------------|-------------|---------|-----------|-----------|-----------------|
| `content/sovereign/scraped/index.json` | research-agent | Claude, Gemini, Codex | Append only. Never overwrite existing slugs. | Global version | Preserve original. Log failure. Retry once. |
| `content/sovereign/scraped/[slug]/info.md` | research-agent | Claude, Gemini, Codex | Create on discovery. Update on `/research` re-run. | Global version | Preserve original. |
| `content/sovereign/scraped/[slug]/sync-status.json` | scraper-agent | Codex, OpenCode, Claude | Write ONLY after scrape validates. | Global version | Rollback scraped files. Preserve old sync-status.json. |
| `content/sovereign/scraped/[slug]/scraped/content/*` | scraper-agent | Codex, OpenCode | New files versioned: `[slug]_v2.md`. Never overwrite. | Global version | Rollback and log. |
| `content/sovereign/scraped/[slug]/scraped/images/*` | scraper-agent | Codex, OpenCode | Deduplicate by MD5 hash before write. | Global version | Skip image, log path. |
| `content/sovereign/scraped/[slug]/analysis/*` | creator-agent | Claude, Gemini | Write on `/compare`. Append comparisons; version if re-comparing same pair. | Global version | Log failure, preserve old. |
| `content/sovereign/scraped/[slug]/analysis/intel-brief.md` | research-agent | Gemini, Copilot, Codex | Write on `/intel competitor [name]`. Version on re-run. | Global version | Log failure, preserve old. |
| `content/sovereign/reference/market-positioning.md` | guide-agent (human-editable) | N/A | Human edits directly. Agents read only. | Manual | N/A (human file) |
| `content/sovereign/reference/brand-voice/style-rules.md` | brand-agent | Claude, Gemini, Copilot | Append new rules. Deprecate with `[DEPRECATED]` tag. | Global version | Preserve original. |
| `content/sovereign/reference/brand-voice/voice-refinement.md` | brand-agent | Claude, Gemini | Overwrite on each `/extract brand voice` run. **Tool-suffixed if conflict:** `voice-refinement_[tool].md` | Per-tool version | Log failure. |
| `content/sovereign/reference/brand-voice/glossary.md` | brand-agent | Claude, Gemini | Append only. Never remove approved terms. | Global version | Preserve original. |
| `content/sovereign/reference/brand-voice/tone-examples.md` | brand-agent | Claude, Gemini | Append examples after each `/extract`. **Tool-tracked:** `{tool: claude, examples: [...]}`| Per-tool version | Preserve original. |
| `content/[type]/[slug].md` | creator-agent | Claude, Gemini, Copilot | Create on `/create`. **Branching on tool:** `[slug]_[tool]_v[n].md` | **Per-tool version** | Log failure, preserve draft. |
| `content/[type]/[slug]_polish.md` | creator-agent (primary) + seo-agent (secondary) | Claude (polish) / Gemini (polish) | `/polish` overwrites in-place. No branching. First tool wins. | Global version | Log failure. |
| `content/[type]/seo-meta.json` | seo-agent | Claude, Gemini | Write after each `/polish` run. **Merged:** includes scores from all tools. | Global version | Log failure. |
| `content/assets-seo-[timestamp].json` | seo-agent | Gemini (primary), Claude (fallback) | Upsert by image path. Never delete. | Global version | Log failure. |
| `content/sovereign/_references/keyword-maps.md` | seo-agent | Claude, Gemini | Update after each `/polish` run. Append new keywords. | Global version | Log failure. |
| `content/sovereign/comparisons/[sovereign_vs_*].md` | creator-agent | Claude, Gemini | Write on `/compare`. **Version by tool:** `[slug]_[tool]_v[n].md` | **Per-tool version** | Log failure. |
| `content/sovereign/comparisons/opportunity-map-[timestamp].md` | research-agent | Copilot, Gemini, Codex | Write on `/intel opportunities`. **Version by tool:** `opportunity-map_[tool]_v[n].md` | **Per-tool version** | Log failure. |
| `content/sovereign/comparisons/diff-logs-[timestamp].jsonl` | creator-agent | Claude, Gemini | Append one JSON line per comparison. **Includes tool field.** | Global log | Log failure. |
| `.ai/logs/workflow.jsonl` | guide-agent (all agents append via guide-agent) | All | Append only. Never delete. **Includes: tool, tool_rank, status per line.** | Global log | Buffer in memory, retry. |
| `.ai/logs/tool-performance.jsonl` | guide-agent (new file) | All | Append performance metrics. **Tool-tagged per line.** | Global log | Buffer in memory, retry. |
| `.ai/logs/scrape-audit.jsonl` | scraper-agent | Codex, OpenCode, Claude | Append only. **Per-line: tool, url, status.** | Global log | Buffer in memory, retry. |
| `.ai/logs/sync-delta.jsonl` | scraper-agent | Codex, OpenCode | Append one JSON line per `/sync` run. **Includes tool field.** | Global log | Buffer in memory, retry. |
| `.ai/logs/content-polish-[timestamp].jsonl` | seo-agent | Claude, Gemini | Append one JSON line per `/polish` run. **Includes tool field.** | Global log | Buffer in memory, retry. |
| `.ai/logs/intelligence-report-[timestamp].jsonl` | research-agent | Gemini, Copilot, Codex, Qwen | Append one JSON line per `/intel*` run. **Includes tool + scope field.** | Global log | Buffer in memory, retry. |
| `.ai/logs/quality-report-[timestamp].json` | workflow-agent | Claude (primary) | Overwrite on each `/review` run. **Includes results from all tools.** | Timestamped backups | Preserve old report. |
| `archive/archive-index-[timestamp].json` | workflow-agent | Claude | Append entries on each `/archive` run. | Global version | Preserve original. |
| `archive/[type]/*` | workflow-agent | Claude | Write compressed `.gz` + decompression-verified. | Global version | Rollback on checksum failure. |
| `content/sovereign/outputs/csv-exports/*` | workflow-agent | Claude | Write on `/export`. **Per-tool:** `[slug]_[tool]_v[n].csv` | **Per-tool version** | Log failure. |
| `content/sovereign/outputs/cms-packs/*` | workflow-agent | Claude | Write on `/export`. ZIP bundle, **per-tool:** `[slug]_[tool]_v[n].zip` | **Per-tool version** | Log failure. |
| `.ai/memory/state.json` | guide-agent | guide-agent only | Update after every command. **Global state, not tool-specific.** | Timestamped | Rollback to previous state. |
| `.ai/memory/multi-tool-state/[tool].session.json` | guide-agent (per tool) | (tool-specific state) | Write after each command via that tool. **Isolated per tool.** | Per-tool version | Preserve existing cache. |
| `.ai/memory/context-cache/*` | memory-manager (via guide-agent) | All | Write on `/memory save`. Clear on `/memory clear`. | Global cache | Preserve existing cache. |
| `.ai/templates/*` | Human-editable | N/A | Agents NEVER write. Human edits only. | Manual | N/A |

---

## VERSIONING RULES (Multi-Tool Mirror)

Canonical rules are defined in `.ai/versioning.md`.

### Rule 1: Content Creation (Branching by Tool)

When `/create blog-posts` is executed:
- **Claude executes first:** Output saved as `content/sovereign/blog-posts/[slug]_[tool]_v[version].md`
- **Claude fails, Gemini executes:** Output saved as `content/sovereign/blog-posts/[slug]_[tool]_v[version].md`
- **Both tools succeed (parallel):** Both files created, user chooses preferred
- **Re-run same command:** Version increments: `post_1_claude_v2.md`, `post_1_gemini_v2.md`

### Rule 2: Optimization (In-Place, No Branching)

When `/polish content` or `/optimize images` executes:
- **First tool optimizes:** Overwrites in-place (no branching)
  - `content/sovereign/blog-posts/[slug].md` → optimized by Claude
- **Second tool used (fallback):** Overwrites in-place again
  - `content/sovereign/blog-posts/[slug].md` → re-optimized by Gemini
- **No version history.** Previous version backed up to: `.ai/memory/polish-backup/post_1_[timestamp].md`

### Rule 3: Comparison Analysis (Branching by Tool)

When `/compare sovereign vs competitor [name]` executes:
- **Claude:** `content/sovereign/comparisons/sovereign_vs_[competitor]_claude_v[version].md`
- **Gemini:** `content/sovereign/comparisons/sovereign_vs_[competitor]_gemini_v[version].md`
- Both kept; user chooses best analysis

### Rule 4: Export (Tool-Qualified)

When `/export` executes:
- **From Claude content:** `content/sovereign/outputs/csv-exports/[slug]_[tool]_v[version].csv`
- **From Gemini content:** `content/sovereign/outputs/csv-exports/[slug]_[tool]_v[version].csv`
- User can export specific versions or all

### Rule 5: Global Logs (Tool-Tagged, Never Branched)

All JSONL logs append globally with `tool` field. No branching.
```json
{
  "timestamp": "2026-04-13T10:22:00+02:00",
  "command": "/create blog-posts",
  "tool": "claude",
  "tool_rank": 1,
  "status": "success",
  ...
}
```

---

## CONFLICT RESOLUTION (Multi-Tool Simultaneous Writes)

### Scenario: Claude and Gemini Run Concurrently on `/create blog-posts`

**Initial state:** `content/sovereign/blog-posts/` is empty

**Concurrent execution:**
1. Claude starts generating `post_1.md`
2. Gemini starts generating `post_1.md` (same slug)
3. Claude finishes first → writes `content/sovereign/blog-posts/[slug]_[tool]_v[version].md`
4. Gemini finishes second → writes `content/sovereign/blog-posts/[slug]_[tool]_v[version].md`

**Result:** Both files exist. No conflict. User chooses preferred version.

---

### Scenario: Sequential Fallback (Claude → Gemini)

**Initial state:** `content/sovereign/blog-posts/` is empty

**Execution flow:**
1. Claude starts generating `post_1.md`
2. Claude times out or fails originality check
3. Gemini starts generating same slug `post_1.md`
4. Gemini finishes → writes `content/sovereign/blog-posts/[slug]_[tool]_v[version].md`

**Result:** Gemini output exists. Claude partial output discarded. No file conflict.

---

### Scenario: Polish Overwrites (Sequential)

**Initial state:** `content/sovereign/blog-posts/[slug]_[tool]_v[version].md` exists (drafted by Claude)

**Execution flow:**
1. `/polish content` executed with Claude (Rank 1)
2. Claude optimizes `post_1_claude_v1.md`
3. Claude finishes → overwrites **in-place** (no version change)

**Result:** `post_1_claude_v1.md` is now polished. Backup created at `.ai/memory/polish-backup/post_1_claude_v1_[timestamp].md`

---

### Scenario: Polish Switches Tools (Fallback)

**Initial state:** `content/sovereign/blog-posts/[slug]_[tool]_v[version].md` is unpolished

**Execution flow:**
1. `/polish content --tool claude` executed
2. Claude times out or fails quality gate
3. Guide-agent **optionally** retries with Gemini (if > 30 articles)
4. Gemini optimizes same file
5. Gemini finishes → overwrites **in-place** (replaces Claude's previous polish attempt)

**Result:** `post_1_claude_v1.md` is now polished by Gemini. Original Claude draft lost (but backup exists).

**Recommendation:** Use `/review` before committing; if quality differs, keep both versions via branching.

---

## CROSS-AGENT WRITE PROTOCOL (Multi-Tool)

If Tool A (via Agent X) needs data written to a file owned by Tool B (via Agent Y):

```
WRONG: Tool A writes directly to file owned by Agent Y
RIGHT: Tool A writes to staging buffer → calls Agent Y's writer → Agent Y validates + writes

Example:
  Gemini (creator-agent) needs to add image metadata to assets-seo.json (owned by seo-agent)
  → Gemini flags: "image refs added to content/sovereign/blog-posts/[slug].md"
  → seo-agent picks up flag on next /optimize or /polish run
  → seo-agent (any tool) writes assets-seo.json with Gemini's new images
```

---

## FILE MERGING RULES (User Choice)

### Merge Command: `/merge content --prefer [tool]`

When multiple tools generate the same content:
```bash
# Use Claude's version as primary
/merge content --prefer claude

# Use Gemini's version as primary
/merge content --prefer gemini

# Manual selection of which files to merge
/merge content --select post_1_claude_v1 post_2_gemini_v1 post_3_claude_v1
```

**Merge output:**
- Selected versions are renamed to remove tool suffix
- Non-selected versions are archived to `.ai/memory/unused-versions/`
- Merge logged to `.ai/logs/workflow.jsonl`

---

## LOG FORMAT STANDARD (Multi-Tool)

All JSONL log entries must include tool information:

```json
{
  "timestamp": "2026-04-13T10:22:00+02:00",
  "command": "/create blog-posts",
  "agent": "creator-agent",
  "tool": "claude",
  "tool_rank": 1,
  "sub_agent": "content_generator",
  "status": "success | partial | failed",
  "duration_ms": 4200,
  "details": {
    "posts_generated": 3,
    "brand_voice_score": 0.94,
    "originality_score": 0.97,
    "cost_usd": 0.25,
    "fallback_reason": null,
    "fallback_tool": null
  }
}
```

**If fallback occurred:**
```json
{
  "status": "success_with_fallback",
  "details": {
    "primary_tool": "claude",
    "primary_tool_error": "timeout",
    "fallback_tool": "gemini",
    "fallback_tool_status": "success",
    ...
  }
}
```

---

## VALIDATION RULE (Multi-Tool)

Before any write, the writing tool must confirm:
1. ✅ The owning agent is identified (creator-agent, seo-agent, etc.)
2. ✅ The tool executing is allowed by that agent
3. ✅ The file path follows versioning convention (`_[tool]_v[n]` if branching)
4. ✅ A backup exists if the write rule says "preserve original on failure"
5. ✅ The write respects conflict resolution rules (branch, merge, or overwrite)

---

## MULTI-TOOL WRITE CHECKLIST

Before executing **any** write operation, guide-agent verifies:

- [ ] Agent who should own file is identified
- [ ] Tool executing that agent is authorized
- [ ] File path includes version or tool suffix if required
- [ ] No conflicting write in progress (single-writer execution in guide-agent routing)
- [ ] Backup mechanism is ready (for in-place overwrites)
- [ ] Log entry prepared (with tool, timestamp, status)
- [ ] Rollback procedure defined (in case of write failure)

---

## MONITORING & ADAPTIVE VERSIONING

### Monthly Ownership Review
1. Scan `.ai/logs/workflow.jsonl` for ownership violations
2. If Tool X frequently needs write permission for files owned by Agent Y, consider redesigning ownership
3. Update `.ai/data-ownership-multi-tool.md` with refined rules

### Tool Performance Impact on Ownership
- If Tool A (Claude) consistently outperforms Tool B (Gemini) on a task, upgrade Tool A's rank
- If Tool B's results require less revision, consider making Tool B the default
- Update `.ai/tool-adapters/_fallback-routing.md` based on 30-day performance trends

---

## BACKWARD COMPATIBILITY (Single-Tool Assumption)

For commands executed by single tool only (no fallback):
- Files use simple naming: `content/sovereign/blog-posts/[slug].md` (no tool suffix)
- Versioning remains: `post_1_v1.md` → `post_1_v2.md` (global, not per-tool)
- Log entries include `tool` field (new) but logic unchanged

**Migration path:** If a single-tool command later triggers fallback:
- First tool's output: `post_1.md` → renamed to `post_1_[tool]_v1.md`
- Second tool's output: `post_1_[tool2]_v1.md`
- Both preserved; user chooses

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 3.2.0 (Original) | 2026-04-13 | Single-tool (Claude) ownership model |
| 3.2.1 (Multi-Tool Phase 1) | 2026-04-13 | Added tool-aware versioning, conflict resolution, per-tool state |

