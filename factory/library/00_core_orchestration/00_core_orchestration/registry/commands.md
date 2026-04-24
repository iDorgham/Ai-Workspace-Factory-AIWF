# Sovereign Workspace — Command Router v3.2
# ============================================================
# Documentation mirror only.
# Canonical executable routing source: `.ai/cli-layer/command-routing.json`.
# Maps every natural language command to its primary agent,
# required context, validation gates, and next steps.
# Zero flags. Zero manual paths. Zero ambiguity.
# ============================================================

---

## COMMAND ROUTING TABLE

| Command | Primary Agent | Required Context | Output | Hard Block? |
|---------|--------------|-----------------|--------|------------|
| `/brand` | brand-agent | `.ai/templates/brand-discovery/questions.json` | Guided brand strategy interview output: `content/sovereign/reference/market_positioning.md`, `content/sovereign/reference/brand-voice/*.md`, `.ai/logs/brand-session-[timestamp].json` | No |
| `/brand workshop` | brand-agent | `.ai/templates/brand-discovery/questions.json` | Alias of `/brand` in meeting mode (branding expert + user) | No |
| `/research competitors` | research-agent | `content/sovereign/reference/market_positioning.md` | `content/sovereign/scraped/*/info.md`, `index.json` | No |
| `/scrape all competitors blog` | scraper-agent | `content/sovereign/scraped/index.json` | `scraped/content/blog/` | No |
| `/scrape all competitors projects` | scraper-agent | `content/sovereign/scraped/index.json` | `scraped/content/sovereign/projects/` | No |
| `/scrape all competitors all website` | scraper-agent | `content/sovereign/scraped/index.json` | Full `scraped/` | No |
| `/scrape [name] website` | scraper-agent | `content/sovereign/scraped/index.json`, competitor slug | `scraped/content/pages/` | No |
| `/scrape [name] all website` | scraper-agent | `content/sovereign/scraped/index.json`, competitor slug | Full `scraped/` | No |
| `/sync` | scraper-agent | `content/sovereign/scraped/index.json`, `sync-status.json` per competitor | Delta updates, `.ai/logs/sync-delta.jsonl` | No |
| `/extract brand voice from [source]` | brand-agent | Source text | `content/sovereign/reference/brand-voice/voice_refinement.md` | No |
| `/refine brand voice` | brand-agent | `content/` recent files, `content/sovereign/reference/brand-voice/` | Updated `style_rules.md`, `glossary.md` | No |
| `/create website pages` | creator-agent | Brand voice, keyword maps, positioning | `content/sovereign/website-pages/` | Via `/review` |
| `/create blog posts about [topic]` | creator-agent | Brand voice, keyword maps, topic | `content/sovereign/blog-posts/` | Via `/review` |
| `/create project pages` | creator-agent | Brand voice, project data | `content/sovereign/projects/` | Via `/review` |
| `/create landing pages for [campaign]` | creator-agent | Brand voice, campaign brief | `content/sovereign/landing-pages/` | Via `/review` |
| `/compare sovereign vs competitor [name]` | creator-agent | Sovereign draft + competitor scraped data | `content/sovereign/comparisons/` | Via `/review` |
| `/intel competitor [name]` | research-agent | `content/sovereign/scraped/index.json`, `content/sovereign/scraped/[slug]/info.md`, `content/sovereign/scraped/[slug]/scraped/content/` | `content/sovereign/scraped/[slug]/analysis/intel_brief.md`, `.ai/logs/intelligence-report-[timestamp].jsonl` | No |
| `/intel market snapshot` | research-agent | `content/sovereign/scraped/index.json`, competitor profile + scraped summaries | Cross-competitor trend summary + `.ai/logs/intelligence-report-[timestamp].jsonl` | No |
| `/intel opportunities` | research-agent | `content/sovereign/reference/market_positioning.md`, trend summary, competitor coverage | `content/sovereign/comparisons/opportunity-map-[timestamp].md`, `.ai/logs/intelligence-report-[timestamp].jsonl` | No |
| `/polish content in content/` | seo-agent + brand-agent | Draft Markdown, keyword maps, brand voice | Optimized in-place Markdown | Via `/review` |
| `/optimize images in content/` | seo-agent | Images in `content/`, manifest | `assets-seo.json`, WebP refs | Via `/review` |
| `/review` | workflow-agent | Staged `content/` drafts | `.ai/logs/quality-report-[timestamp].json` | No |
| `/approve` | workflow-agent | `.ai/logs/quality-report-[timestamp].json` (all gates passed) | Locked content metadata | Blocked if gates fail |
| `/revise [feedback]` | creator-agent or seo-agent | Feedback text, failing content | Revised Markdown | Via `/review` |
| `/export` | workflow-agent | Approved content (status: approved) | `content/sovereign/outputs/csv-exports/`, `content/sovereign/outputs/cms-packs/` | Blocked if not approved |
| `/archive old content` | workflow-agent | Files > 30 days | `archive/`, `archive-index.json` | No |
| `/memory save` | workflow-agent + memory-manager | Current session state | `.ai/memory/context-cache/` | No |
| `/memory load` | memory-manager | `.ai/memory/context-cache/` | Restored session context | No |
| `/memory clear` | memory-manager | Active session | Cleared temp context | No |
| `/budget check` | guide-agent | Current token usage | Usage report + recommendations | No |
| Command | Subcommand | Agent | Purpose |
| :--- | :--- | :--- | :--- |
| **`/plan`** | `content` | content-planner | Structured discovery interview |
| | `blueprint` | spec-architect | Generates high-density SDD specs |
| | `status` | orchestrator | Real-time phase progress/gap audit |
| | `review` | orchestrator | Strategic alignment vs intent check |
| | `adr` | spec-architect | Auto-generates ADRs with hashes |
| **`/create`** | `content` | creator-agent | Scaffolds content into workspace |
| | `image` | visualize-agent | Generates industrial visual assets |
| | `page` | creator-agent | Builds page structures with locale |
| | `spec` | spec-architect | Generates specs and test fixtures |
| | `docs` | docs-curator | Auto-generates system documentation |
| **`/dev`** | `init` | factory-manager | Env setup and dependency resolution |
| | `implement` | developer-agent | Autonomous spec-governed generation |
| | `test` | integrity-auditor| Multi-tier compliance testing |
| | `fix` | healing-bot | Recursive remediation of drift |
| | `build` | deployment-spec | Compiles and optimizes artifacts |
| **`/audit`** | `health` | integrity-auditor| Industrial health scoring |
| | `content` | creator-agent | Multi-locale consistency audit |
| | `security` | security-auditor | SAST/DAST and secrets scanning |
| | `logs` | orchestrator | Log aggregation and tracing |
| | `seo` | seo-agent | Technical SEO and meta-audit |
| **`/git`** | `auto` | repository-agent | Silent versioning and tagging |
| | `release` | deployment-spec | Sovereign handover and release |
| | `review` | repository-agent | PR consensus and auto-approval |
| | `rollback` | repository-agent | Recovery to stable compliance state |
| | `deploy` | deployment-spec | Shard distribution with routing |
| **`/guide`** | `brainstorm` | master-guide | Multi-agent strategy consensus |
| | `learn` | recursive-engine | Friction-to-skill conversion |
| | `heal` | healing-bot | Predictive structural monitoring |
| | `chaos` | chaos-validator | Stress testing and resilience |
| | `dashboard` | orchestrator | Real-time KPI/Health UI |
| | `tutor` | guide-agent | Interactive pedagogy and onboarding |
| **`/help`** | | guide-agent | usage reference and sovereignty info |

---

## INTENT PARSING RULES

The guide-agent must resolve these ambiguities before routing:

### Scope Resolution
- `/scrape all competitors blog` → scope: ALL entries in `index.json` where `sync_enabled: true`
- `/scrape [name] website` → scope: SINGLE competitor matching `[name]` slug or closest match
- `/create blog posts about [topic]` → topic extracted from command; if multi-word, preserve full phrase
- `/revise [feedback]` → feedback applied to the LAST created/polished content item in `state.json`
- `/plan release` → triggers `.ai/scripts/silent_phase_release.py` to increment version and tag Git without user prompt.

### Competitor Name Matching
1. Exact slug match in `index.json` → use directly
2. Partial name match → use highest confidence match, confirm with user if < 80% confidence
3. No match → ask: "I don't have [name] in the competitor registry. Run `/research competitors` first, or provide the URL directly."

### Missing Context Defaults
| Missing | Default Action |
|---------|---------------|
| `market_positioning.md` empty | Respond: "Your brand foundation isn't set up yet. Run `/brand` to complete a professional brand discovery session first." |
| `brand-voice/style_rules.md` empty | Respond: "Brand voice rules are not defined. Run `/brand` (full session) or `/extract brand voice from [source]` if you have existing copy." |
| No competitor data for `/create` | Generate from brand positioning + keyword research alone |
| No keyword map for `/polish` | Mine keywords from content topic + market positioning |
| No images for `/optimize images` | Report: "No images found in content/. Add images to your draft files first." |

### Plural vs Singular
- `/create blog posts about [topic]` → generate 3 posts by default (short, medium, long-form variants)
- `/scrape all competitors` → all enabled in `index.json`
- Single `/scrape [name]` → one competitor only

---

## COMMAND CHAIN SUGGESTIONS

After every command, guide-agent outputs one of these next steps:

| Completed Command | Suggested Next Step |
|-------------------|---------------------|
| `/brand` | `/research competitors` (or `/extract brand voice from [source]` if existing copy is available) |
| `/research competitors` | `/scrape all competitors blog` |
| `/scrape all competitors blog` | `/sync` or `/create blog posts about [topic]` |
| `/sync` | `/create blog posts about [topic]` or `/compare sovereign vs competitor [name]` |
| `/create *` | `/polish content in content/` |
| `/compare *` | `/create blog posts about [topic gap identified]` |
| `/intel competitor *` | `/compare sovereign vs competitor [name]` or `/create blog posts about [identified gap]` |
| `/intel market snapshot` | `/intel opportunities` |
| `/intel opportunities` | `/create blog posts about [top opportunity]` |
| `/polish content` | `/optimize images in content/` |
| `/optimize images` | `/review` |
| `/review` (passed) | `/plan` |
| `/review` (failed) | `/revise [specific feedback for failed gate]` |
| `/revise *` | `/review` |
| `/approve` | `/export` |
| `/export` | `/sync` or `/archive old content` |
| `/archive old content` | `/memory clear` then next `/create` |
| `/memory save` | Continue with interrupted command |

---

## QUALITY GATE REFERENCE

All gates run in **parallel** during `/review`:

| Gate | Validator | Threshold | Auto-Fix? | On Failure |
|------|-----------|-----------|-----------|------------|
| SEO Score | `seo_optimizer.py` | ≥ 85% | Yes (keyword inject, meta fix) | List gaps |
| Brand Voice | `voice_validator.py` | ≥ 92% | Yes (tone adjust, max 2 retries) | Flag drift points |
| Readability | Flesch-Kincaid | ≥ 65 | Yes (simplify sentences) | List dense paragraphs |
| Image SEO | `image_seo_auditor.py` | 100% | Yes (generate alt, WebP) | List missing images |
| Originality | Semantic similarity | ≤ 15% | Yes (structural shift, max 2 retries) | Flag similar passages |

---

## PIPELINE ENFORCEMENT

```
VALID FLOW:
/research competitors
  └→ /scrape all competitors blog
       └→ /sync
            └→ /create blog posts about [topic]
                 └→ /polish content in content/
                      └→ /optimize images in content/
                           └→ /review
                                └→ /approve
                                     └→ /export
                                          └→ /archive old content

BLOCKED FLOWS (hard stops):
  /export     ← requires /approve first
  /approve    ← requires /review (all gates passed) first
  /sync       ← requires valid index.json + ≥1 competitor folder
  /optimize   ← requires images in content/ files
```

---

## COMMAND OUTPUT FORMAT

Every command response follows this structure:

```
✅ [Command completed]
→ [What was done — specific, quantified]
→ [Where output was saved]
→ [Any warnings or flags]

💡 Suggested Next Step:
• [Primary recommendation with exact command]
• [Optional alternative command]
```

Example:
```
✅ Sync complete
→ Checked 4 competitors. Detected 6 new blog posts, 2 new projects.
→ Scraped and saved to content/sovereign/scraped/*/scraped/content/
→ Updated sync-status.json for all 4 competitors. Logged to .ai/logs/sync-delta.jsonl.

💡 Suggested Next Step:
• /create blog posts about [topic from gap analysis]
• /compare sovereign vs competitor [name with most new content]
```
