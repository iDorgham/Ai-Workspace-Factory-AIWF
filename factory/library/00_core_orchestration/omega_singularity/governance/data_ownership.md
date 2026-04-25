# Sovereign Workspace — Data Ownership Registry v3.2
# ============================================================
# CRITICAL: Every data file has exactly ONE authoritative owner.
# Only the owner may write. All others are read-only.
# Violations of this contract cause data corruption and sync failures.
# ============================================================

---

Versioning authority: `.ai/versioning.md` (canonical).

## OWNERSHIP MATRIX: 3-Tier Architecture Updates (v2.0 Transformation)

### Core State & Registries
| File / Path | Owner Agent | Read-Only Agents | Write Rule | On Write Failure |
|-------------|-------------|-----------------|-----------|-----------------|
| `AI Workspace Factory/.ai/memory/workspace-index.json` | `master-guide` | ALL agents | Append/Upsert on `/master sync`. | Rollback. |
| `workspaces/clients/[slug]/001_[project]/.ai/memory/state.json` | `guide-agent` (Project-level) | `master-guide` (Sync-only) | Full state UPSERT. | Restore backup. |
| `workspaces/clients/[slug]/metadata.json` | `master-guide` | `guide-agent` | Write on `/create-client`. | Rollback. |

### Dashboards
| File / Path | Owner Agent | Read-Only Agents | Write Rule | On Write Failure |
|-------------|-------------|-----------------|-----------|-----------------|
| `AI Workspace Factory/.ai/dashboard/*` | `master-guide` | ALL agents | Rewrite index, strictly via lazy-load widgets. | Restore widget. |
| `workspaces/clients/[slug]/dashboard/*` | `master-guide` | `guide-agent` | Rewrite client-level index. | Restore widget. |
| `workspaces/clients/[slug]/001_[project]/dashboard/*` | `guide-agent` | ALL agents | Updates via lazy-loaded widgets. NO LLM logic. | Log failure. |
| `*/dashboard/brainstorm_suggestions.md` | `brainstorm-agent` (Proactive) | `guide-agent` | Max 2 suggestions. Archive on dismiss. | Preserve original. |

---

## LEGACY MATRIX
|-------------|-------------|-----------------|-----------|-----------------|
| `content/sovereign/scraped/index.json` | `research-agent` | ALL agents | Append only. Never overwrite existing slugs. | Preserve original. Log failure. Retry once. |
| `content/sovereign/scraped/[slug]/info.md` | `research-agent` | scraper-agent, creator-agent | Create on discovery. Update on `/research` re-run (append new data, never delete). | Preserve original. |
| `content/sovereign/scraped/[slug]/sync-status.json` | `scraper-agent` (sync-state-writer sub-agent) | guide-agent, workflow-agent | Write ONLY after scrape completes AND validation passes. | Rollback scraped files. Preserve old `sync-status.json`. |
| `content/sovereign/scraped/[slug]/scraped/content/*` | `scraper-agent` | creator-agent (read-only, structural inspiration) | New files always versioned: `[slug]_v2.md`. Never overwrite existing versions. | Rollback and log. |
| `content/sovereign/scraped/[slug]/scraped/images/*` | `scraper-agent` (asset-handler sub-agent) | seo-agent | Deduplicate by MD5 hash before write. Skip duplicates silently. | Skip image, log path. |
| `content/sovereign/scraped/[slug]/analysis/*` | `creator-agent` (comparison-analyst) | workflow-agent | Write on `/compare`. Append new comparisons; version if re-comparing same pair. | Log failure, preserve old. |
| `content/sovereign/scraped/[slug]/analysis/intel_brief.md` | `research-agent` (intel-synthesizer) | creator-agent, workflow-agent | Write on `/intel competitor [name]`. Version on re-run: `intel-brief_v2.md`. | Log failure, preserve old. |
| `content/sovereign/reference/market_positioning.md` | `guide-agent` (human-editable) | research-agent, creator-agent, seo-agent | Human edits directly. Agents read only. Never auto-overwrite. | N/A (human file) |
| `content/sovereign/reference/brand-voice/style_rules.md` | `brand-agent` (rule-updater) | creator-agent, seo-agent, workflow-agent | Append new rules. Never delete existing rules (deprecate with `[DEPRECATED]` tag instead). | Preserve original. |
| `content/sovereign/reference/brand-voice/voice_refinement.md` | `brand-agent` (tone-analyzer) | creator-agent | Overwrite on each `/extract brand voice` run (it's an extraction result, not history). | Log failure. |
| `content/sovereign/reference/brand-voice/glossary.md` | `brand-agent` (rule-updater) | creator-agent, seo-agent | Append only. Never remove approved terms. Mark outdated terms as `[OUTDATED]`. | Preserve original. |
| `content/sovereign/reference/brand-voice/tone_examples.md` | `brand-agent` | creator-agent | Append examples after each `/extract` or `/refine`. | Preserve original. |
| `content/[type]/[slug].md` | `creator-agent` | seo-agent (optimize in-place), workflow-agent (lock) | creator-agent creates. seo-agent optimizes in-place (never recreates). workflow-agent sets `status` only. | Log failure, preserve draft. |
| `content/[type]/seo-meta.json` | `seo-agent` | workflow-agent | Write after each `/polish` run. | Log failure. |
| `content/assets-seo-[timestamp].json` | `seo-agent` | workflow-agent, creator-agent | Upsert by image path. Never delete entries (mark removed images as `status: "removed"`). | Log failure. |
| `content/sovereign/_references/keyword_maps.md` | `seo-agent` | creator-agent, brand-agent | Update after each `/polish` run. Append new keywords; never remove mapped keywords. | Log failure. |
| `content/sovereign/comparisons/[sovereign_vs_*].md` | `creator-agent` | workflow-agent | Write on `/compare`. Version if re-running same comparison: `sovereign_vs_[slug]_v2.md`. | Log failure. |
| `content/sovereign/comparisons/opportunity-map-[timestamp].md` | `research-agent` (opportunity-scorer) | creator-agent, workflow-agent | Write on `/intel opportunities`. Version on re-run: `opportunity-map_v2.md`. | Log failure, preserve old. |
| `content/sovereign/comparisons/diff-logs-[timestamp].jsonl` | `creator-agent` | workflow-agent | Append only. One JSON line per comparison run. | Log failure. |
| `.ai/logs/workflow.jsonl` | `guide-agent` (all agents append via guide-agent) | ALL agents (read) | Append only. Never delete. One JSON line per action. | Buffer in memory, retry append. |
| `.ai/logs/scrape-audit.jsonl` | `scraper-agent` | guide-agent, workflow-agent | Append only. One JSON line per URL scraped or skipped. | Buffer in memory, retry. |
| `.ai/logs/sync-delta.jsonl` | `scraper-agent` | guide-agent, workflow-agent | Append only. One JSON line per `/sync` run. | Buffer in memory, retry. |
| `.ai/logs/content-polish-[timestamp].jsonl` | `seo-agent` | guide-agent, workflow-agent | Append only. One JSON line per `/polish` run. | Buffer in memory, retry. |
| `.ai/logs/intelligence-report-[timestamp].jsonl` | `research-agent` | guide-agent, workflow-agent, creator-agent | Append only. One JSON line per `/intel*` run. | Buffer in memory, retry. |
| `.ai/logs/quality-report-[timestamp].json` | `workflow-agent` (quality-checker) | ALL agents | Overwrite on each `/review` run. Previous report backed up to `.ai/logs/quality-report-[timestamp].json`. | Preserve old report. |
| `archive/archive-index-[timestamp].json` | `workflow-agent` (archive-manager) | guide-agent | Append entries on each `/archive` run. Never delete existing entries. | Preserve original. |
| `archive/[type]/*` | `workflow-agent` (archive-manager) | guide-agent (pointer loading) | Write compressed `.gz` files + decompression-verified. Never archive active files. | Rollback on checksum failure. |
| `content/sovereign/outputs/csv-exports/*` | `workflow-agent` (export-packager) | None (final output) | Write on `/export`. Never overwrite: version as `[slug]_v2.csv`. | Log failure. |
| `content/sovereign/outputs/cms-packs/*` | `workflow-agent` (export-packager) | None (final output) | Write on `/export`. ZIP bundle, version if re-exporting. | Log failure. |
| `.ai/memory/state.json` | `guide-agent` | ALL agents (read) | Update after every command completes. | Rollback to previous state on corruption. |
| `.ai/memory/context-cache/*` | `memory-manager` (via guide-agent) | ALL agents (load via guide-agent only) | Write on `/memory save`. Clear on `/memory clear`. | Preserve existing cache. |
| `.ai/templates/*` | Human-editable | ALL agents (read) | Agents NEVER write to templates. Human edits only. | N/A |

---

## CROSS-AGENT WRITE PROTOCOL

If Agent A needs data written to a file owned by Agent B:

```
WRONG: Agent A writes directly to file owned by Agent B
RIGHT: Agent A writes to temp buffer → calls Agent B's writer function → Agent B validates + writes

Example:
  creator-agent needs to update assets-seo.json (owned by seo-agent)
  → creator-agent flags: "image ref added to content/sovereign/blog-posts/[slug].md"
  → seo-agent picks up flag on next /optimize or /polish run
  → seo-agent writes assets-seo.json
```

---

## LOG FORMAT STANDARD

All JSONL log entries must follow this schema:

```json
{
  "timestamp": "2026-04-13T10:22:00+02:00",
  "command": "/sync",
  "agent": "scraper-agent",
  "sub_agent": "delta-detector",
  "status": "success | partial | failed",
  "duration_ms": 1420,
  "details": {
    "competitors_checked": 4,
    "new_urls": 6,
    "updated_urls": 2,
    "errors": []
  }
}
```

---

## VALIDATION RULE

Before any write, the writing agent must confirm:
1. It is the authoritative owner of the target file
2. The file path is within the expected directory
3. The write follows the stated write rule (append vs overwrite vs upsert)
4. A backup exists if the write rule says "preserve original on failure"
\n## Tool Adapters\n- Path: .ai/scripts/tool_adapters/*\n- Owner: Infrastructure Automation Bot\n- Sync: Append-only metrics to health_metrics.log\n
