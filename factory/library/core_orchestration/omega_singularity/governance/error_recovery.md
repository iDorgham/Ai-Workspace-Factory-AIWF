# Sovereign Workspace — Error Recovery Cascade v3.2
# ============================================================
# Defines exactly WHO retries WHAT, in what order, with what fallback.
# Every failure mode has a single owner. No silent failures.
# All errors logged to logs/workflow.jsonl before recovery attempt.
# ============================================================

---

## CASCADE HIERARCHY

```
Error occurs
  → Owning sub-agent catches error
      → Applies retry logic (max 3x, exponential backoff)
          → If still failing: escalates to primary agent
              → Primary agent applies fallback logic
                  → If fallback fails: guide-agent outputs diagnostic
                      → User receives actionable message + recommended command
```

---

## ERROR CATALOG BY COMMAND

### `/research competitors`

| Error | Owner | Retry? | Fallback | User Message |
|-------|-------|--------|----------|-------------|
| Target site unreachable (timeout > 5s) | `discovery-engine` | No (skip, continue to next candidate) | Use cached WHOIS data if available | "Couldn't reach [site]. Skipped. [N] competitors profiled successfully." |
| < 3 competitors discovered | `discovery-engine` | Yes (broaden search: remove geo filter, expand niche terms) | Ask user for manual seed URL | "Found only [N] competitors. Want me to broaden the search or add a competitor URL manually?" |
| info.md write failure | `profile-builder` | Yes, 3x | Log error, continue with other profiles | "Profile for [name] couldn't be saved. Check disk space or permissions." |
| Duplicate slug in `index.json` | `profile-builder` | No | Merge new data into existing entry | "Found updated data for existing competitor [name]. Merged into existing profile." |

---

### `/scrape [name]` and `/scrape all competitors *`

| Error | Owner | Retry? | Fallback | User Message |
|-------|-------|--------|----------|-------------|
| `robots.txt` blocks target path | `ethical-crawler` | No (never bypass) | Skip blocked path, log in `scrape-audit.jsonl` | "Path [url] blocked by robots.txt. Skipped. Compliant with ethics rules." |
| HTTP 429 Too Many Requests | `ethical-crawler` | Yes: 5s → 10s → 20s → skip URL | Log as retry-able, mark URL in `sync-status.json` | Silent (no user output unless >50% of URLs blocked) |
| HTTP 403 Forbidden | `ethical-crawler` | No | Skip URL, log | "Access denied for [url]. Site may require authentication." |
| HTTP 404 Not Found | `content-parser` | No | Mark URL as deleted in delta payload | Silent (expected: delta-deleted URLs are normal) |
| Malformed HTML (parser error) | `content-parser` | Yes once (alternate parser) | Skip URL, log path | Silent unless > 20% of URLs malformed (then alert user) |
| Image download fails | `asset-handler` | Yes, 2x | Skip image, mark in `manifest.json` as `status: "failed"` | Silent |
| WebP conversion fails | `asset-handler` | Yes once | Keep original format, mark in manifest | Silent |
| `sync-status.json` write fails | `sync-state-writer` | Yes, 3x | ROLLBACK all scraped files from this run. Preserve old `sync-status.json` | "Sync state could not be saved. All new files rolled back to prevent inconsistency. Run `/sync` again." |
| > 50% URLs get 429 from one competitor | `ethical-crawler` | No (stop scraping that competitor) | Mark competitor as `status: "rate-limited"` in `index.json` | "⚠️ [Competitor] is rate-limiting requests. Scraping paused for 24h. Others completed normally." |
| `index.json` missing or invalid | `scraper-agent` (pre-check) | No | Halt command entirely | "No competitor registry found. Run `/research competitors` first." |

---

### `/sync`

| Error | Owner | Retry? | Fallback | User Message |
|-------|-------|--------|----------|-------------|
| Sitemap unreachable | `delta-detector` | Yes once (fallback to RSS) | If RSS also fails: mark competitor as `stale` | "Sitemap unavailable for [competitor]. Tried RSS — also failed. Marked as stale." |
| RSS feed unreachable | `delta-detector` | No | Mark competitor as `stale`, continue sync for others | "Couldn't check for updates on [competitor]. Skipped." |
| Delta detection false positive rate > 10% | `delta-detector` | Auto-recalibrate hash window (extend to 48h) | Log warning | "⚠️ High false positive rate on delta detection. Recalibrated — re-run `/sync` to verify." |
| All scrape errors (see scrape errors above) | (same as `/scrape` above) | (same) | (same) | (same) |

---

### `/create *`

| Error | Owner | Retry? | Fallback | User Message |
|-------|-------|--------|----------|-------------|
| Originality score > 15% | `content-generator` | Yes, 2x (structural shift each retry) | After 3 attempts: flag for manual `/revise` | "Content similarity too high after 3 attempts. Use `/revise [instruction]` to guide a different approach." |
| Brand voice score < 92% | `brand-voice-applier` | Yes, 2x (stricter tone matrix) | After 2 retries: output with warning flag, block export | "Brand voice compliance at [score]%. Needs `/revise` with tone guidance or `/refine brand voice` first." |
| Keyword map missing | `blueprint-architect` | No retry (auto-fallback) | Mine keywords from topic + `market_positioning.md` | Silent (auto-resolved). |
| No competitor data available | `blueprint-architect` | No retry | Generate from brand positioning alone | "No competitor data available. Generated from Sovereign's brand positioning and keyword research." |
| Template file missing | `blueprint-architect` | No | Use generic 5-section structure | "Template for [type] not found. Used standard structure." |
| Content write failure | `content-generator` | Yes, 3x | Log error, preserve any partial output | "Content file couldn't be saved. Check disk space. Partial draft preserved in `.ai/memory/`." |

---

### `/compare sovereign vs competitor [name]`

| Error | Owner | Retry? | Fallback | User Message |
|-------|-------|--------|----------|-------------|
| Competitor slug not in `index.json` | `guide-agent` (pre-route) | No | Ask user to run `/research competitors` or `/scrape [name]` first | "Competitor [name] not found. Run `/research competitors` or `/scrape [name] website` first." |
| No scraped content for competitor | `comparison-analyst` | No | Compare against competitor's live site (single fetch, ethical) | "No cached data for [competitor]. Fetching current homepage for comparison only." |
| Sovereign draft content missing | `comparison-analyst` | No | Halt, prompt user | "No Sovereign draft found to compare. Run `/create [type]` first." |
| Diff report write fails | `comparison-analyst` | Yes, 2x | Log failure | "Comparison report couldn't be saved. Try again or check disk space." |

---

### `/polish content in content/`

| Error | Owner | Retry? | Fallback | User Message |
|-------|-------|--------|----------|-------------|
| Keyword cannibalization detected | `keyword-auditor` | No (human decision needed) | Flag files, do not auto-resolve | "⚠️ Keyword cannibalization: [keyword] appears in [file1] and [file2]. Review and differentiate manually." |
| Flesch-Kincaid < 65 after 2 auto-fix passes | `technical-auditor` | No | Flag file, output dense paragraphs | "Readability still at [score] after auto-fix. Use `/revise [file] simplify writing` for manual guidance." |
| SEO score < 85 after auto-fix | `keyword-auditor` | No | Flag specific gaps | "SEO at [score]%. Missing: [specific gaps]. Use `/revise` with SEO focus." |

---

### `/optimize images in content/`

| Error | Owner | Retry? | Fallback | User Message |
|-------|-------|--------|----------|-------------|
| No images found in `content/` | `image-seo-auditor` | No | Halt with instruction | "No images found in content/. Embed image references in your Markdown files first." |
| Alt-text generation fails for image | `image-seo-auditor` | Yes once | Generate generic alt from file name | Silent (auto-resolved). |
| WebP conversion fails | `image-seo-auditor` | Yes once | Keep original format, mark in `assets-seo.json` | Silent. |

---

### `/review`

| Error | Owner | Retry? | Fallback | User Message |
|-------|-------|--------|----------|-------------|
| One or more gates fail | `quality-checker` | No (gates don't retry themselves) | Output detailed violation report per gate | "Review complete. [N] gates passed, [M] failed. See below for fixes." |
| Gate validator crashes (script error) | `quality-checker` | Yes once | If still fails: skip gate, mark as `status: "error"` in report | "⚠️ [Gate name] validator encountered an error. Marked as incomplete. Run `/review` again." |
| No staged content found | `workflow-agent` (pre-check) | No | Halt | "Nothing staged for review. Run `/create` or `/polish` first." |
| `quality-report.json` write fails | `quality-checker` | Yes, 3x | Output results in-session (no file saved) | "⚠️ Quality report couldn't be saved to disk. Results shown below — copy manually." |

---

### `/approve`

| Error | Owner | Retry? | Fallback | User Message |
|-------|-------|--------|----------|-------------|
| `quality-report.json` missing | `approval-gate` | No | Halt | "No quality report found. Run `/review` first." |
| One or more gates failed in last review | `approval-gate` | No | Halt, list failed gates | "Approval blocked. Failed gates: [list]. Fix with `/revise [feedback]` then `/review` again." |
| Content metadata write fails | `approval-gate` | Yes, 3x | Log failure | "Approval status couldn't be written. Run `/approve` again." |

---

### `/export`

| Error | Owner | Retry? | Fallback | User Message |
|-------|-------|--------|----------|-------------|
| Content not approved (`status ≠ "approved"`) | `export-packager` | No (hard block) | Halt | "Export blocked. Run `/review` → `/approve` first." |
| CSV schema validation failure | `export-packager` | Yes once (auto-fill defaults for missing fields) | Flag remaining schema errors | "CSV schema error on [field]. Auto-filled with defaults where possible. Check content/sovereign/outputs/csv-exports/ before publishing." |
| ZIP packaging fails | `export-packager` | Yes, 2x | Output unzipped files instead | "CMS pack ZIP failed. Files exported individually to content/sovereign/outputs/cms-packs/[slug]/." |

---

### `/archive old content`

| Error | Owner | Retry? | Fallback | User Message |
|-------|-------|--------|----------|-------------|
| Checksum mismatch after compression | `archive-manager` | Yes once (re-compress) | If still fails: rollback, preserve original | "Archive checksum failed. Rolled back. Original files preserved. Run `/archive old content` again." |
| `archive-index.json` write fails | `archive-manager` | Yes, 3x | Log failure | "Archive index not updated. Files compressed but not indexed. Run `/archive old content` again to reindex." |
| Active content mistakenly flagged (< 30 days) | `archive-manager` | No | Skip file, log warning | "⚠️ [file] is < 30 days old. Skipped archiving." |

---

## GLOBAL ERROR RULES

1. **Log first, then retry.** Every error is logged to `logs/workflow.jsonl` before any recovery attempt.
2. **Max 3 retries** for any single operation. After 3 failures: escalate, never infinite loop.
3. **Never silently succeed** after a fallback that changes the expected output (always inform user).
4. **Never silently fail.** Even skipped operations are logged.
5. **Rollback > corrupt data.** If a write would create inconsistency, rollback and preserve old state.
6. **Human in the loop** for decisions about data integrity, keyword conflicts, tone arbitration.
